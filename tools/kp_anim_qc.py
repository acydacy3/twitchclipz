#!/usr/bin/env python3
"""kp_anim_qc.py — Animationen messen statt begutachten.

Zwei Fehler haben jede bisher produzierte Animation betroffen, und beide waren
mit blossem Hinsehen leicht zu uebersehen:

  ZU KLEIN     Manim leitet die Buehnenhoehe aus dem Seitenverhaeltnis ab. Im
               Hochformat ergab das rund 25 Einheiten, waehrend die Szenen fuer
               rund 16 geschrieben sind. Der Inhalt sass winzig in der Mitte
               (Failure-Memory F-V9-E).
  ABGESCHNITTEN Beschriftungen liefen ueber den Bildrand hinaus -- "Unterarm"
               und "Eingeklemmt" waren rechts angeschnitten, ohne dass es
               jemandem auffiel.

Beides laesst sich messen. Gemessen wird der Kasten um alles Helle im Bild
(ffmpeg-Filter "bbox"):

  Randabstand   Beruehrt der Inhalt den linken/rechten Rand? -> abgeschnitten
  Fuellgrad     Wie viel der Bildbreite nutzt der Inhalt?    -> zu klein

    python3 tools/kp_anim_qc.py                 alle gerenderten Szenen
    python3 tools/kp_anim_qc.py CrossSection    eine Szene
    python3 tools/kp_anim_qc.py --json

Exit-Code 0 = alle Szenen in Ordnung, 1 = mindestens eine auffaellig.
"""

import argparse
import glob
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA = os.path.join(ROOT, "media", "videos", "manim_scenes")

# Helligkeit, ab der ein Pixel als "Inhalt" gilt.
#
# Kalibriert am 07.09.2026, nachdem der erste Wert (150) RockTrap faelschlich
# als "nutzt nur 14 % der Bildbreite" meldete: die orangen Felswaende liegen
# bei Luma ~133 und fielen damit durch das Raster, gemessen wurde nur noch die
# Schrift. Gegenprobe am dunkelsten Szenen-Hintergrund: Spitze 48.
#   Schwelle 130 -> RockTrap 67 % (richtig), Hintergrund sicher ausgeschlossen
#   Schwelle 150 -> RockTrap 14 % (Fehlalarm)
# Eine Messung ist nur so gut wie ihre Kalibrierung -- deshalb steht sie hier.
SCHWELLE = 130

# Naeher als das an den Rand heisst: vermutlich abgeschnitten.
RAND_PROZENT = 1.5

# Weniger Breite als das heisst: der Inhalt geht im Bild unter.
MIN_FUELLGRAD = 0.30


def frames_einer_szene(video, anzahl=7):
    d = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration", "-of", "csv=p=0", video],
                       capture_output=True, text=True).stdout.strip()
    try:
        dauer = float(d)
    except ValueError:
        return []
    # Den Anfang auslassen: dort ist oft noch nichts eingeblendet.
    return [dauer * (0.25 + 0.7 * i / max(anzahl - 1, 1)) for i in range(anzahl)]


def masse(video, sekunde):
    """(x1, x2, y1, y2, breite, hoehe) des hellen Inhalts, oder None."""
    r = subprocess.run(
        ["ffmpeg", "-v", "info", "-ss", f"{sekunde:.2f}", "-i", video,
         "-frames:v", "1", "-vf", f"bbox=min_val={SCHWELLE}", "-f", "null", "-"],
        capture_output=True, text=True)
    m = re.search(r"x1:(\d+)\s+x2:(\d+)\s+y1:(\d+)\s+y2:(\d+)", r.stderr + r.stdout)
    if not m:
        return None
    x1, x2, y1, y2 = (int(g) for g in m.groups())
    return x1, x2, y1, y2


def bildmasse(video):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "stream=width,height", "-of", "csv=p=0",
                        video], capture_output=True, text=True).stdout.strip()
    try:
        w, h = (int(x) for x in r.split(",")[:2])
        return w, h
    except Exception:
        return 1080, 1920


def pruefe_szene(name, video):
    W, H = bildmasse(video)
    rand = W * RAND_PROZENT / 100.0
    befunde = []
    links_min, rechts_max, breit_max = W, 0, 0
    treffer = 0

    for t in frames_einer_szene(video):
        b = masse(video, t)
        if not b:
            continue
        x1, x2, y1, y2 = b
        treffer += 1
        links_min = min(links_min, x1)
        rechts_max = max(rechts_max, x2)
        breit_max = max(breit_max, x2 - x1)

    if not treffer:
        return {"szene": name, "ok": False, "grund": "kein heller Inhalt messbar",
                "fuellgrad": 0.0}

    fuellgrad = breit_max / W
    if links_min <= rand:
        befunde.append(f"beruehrt den linken Rand ({links_min} px von {W})")
    if rechts_max >= W - rand:
        befunde.append(f"beruehrt den rechten Rand ({W - rechts_max} px Abstand)")
    if fuellgrad < MIN_FUELLGRAD:
        befunde.append(f"nutzt nur {fuellgrad:.0%} der Bildbreite "
                       f"(mindestens {MIN_FUELLGRAD:.0%})")

    return {"szene": name, "ok": not befunde, "grund": "; ".join(befunde),
            "fuellgrad": round(fuellgrad, 3),
            "links": links_min, "rechts_abstand": W - rechts_max}


def gerenderte_szenen(filter_name=None):
    out = []
    for p in sorted(glob.glob(os.path.join(MEDIA, "*", "*.mp4"))):
        if "partial_movie_files" in p:
            continue
        name = os.path.splitext(os.path.basename(p))[0]
        if filter_name and name != filter_name:
            continue
        out.append((name, p))
    return out


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("szene", nargs="?", help="nur diese Szene")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    szenen = gerenderte_szenen(a.szene)
    if not szenen:
        print("Keine gerenderten Szenen gefunden.\n"
              "Erst rendern: manim -qh -r 1080,1920 tools/manim_scenes.py <Klasse>",
              file=sys.stderr)
        return 2

    ergebnisse = [pruefe_szene(n, p) for n, p in szenen]

    if a.json:
        print(json.dumps(ergebnisse, ensure_ascii=False, indent=1))
        return 1 if any(not e["ok"] for e in ergebnisse) else 0

    print("=" * 70)
    print(f"  ANIMATIONS-QC  —  {len(ergebnisse)} Szenen")
    print("=" * 70)
    for e in ergebnisse:
        zeichen = "OK  " if e["ok"] else "FEHL"
        print(f"  [{zeichen}] {e['szene']:<24} Fuellgrad {e['fuellgrad']:>5.0%}"
              + (f"   {e['grund']}" if e["grund"] else ""))
    schlecht = [e for e in ergebnisse if not e["ok"]]
    print("=" * 70)
    if schlecht:
        print(f"  {len(schlecht)} Szene(n) auffaellig — vor dem Einsetzen beheben.")
        return 1
    print("  Alle Szenen fuellen das Bild und laufen nicht ueber den Rand.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
