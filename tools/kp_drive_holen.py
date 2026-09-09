#!/usr/bin/env python3
"""kp_drive_holen.py — Serien-Material aus Google Drive in den Repo-Ordner holen.

WARUM ES DAS GIBT
-----------------
Am 08.09.2026 sollten die fehlenden Langvideos gebaut werden. Fuer drei Serien
(San Jose, Okene, Lengede) lag im Repo nichts mehr: Voiceover und Bilder waren
nie eingecheckt, und der Container ist eine Wegwerfumgebung. Der naheliegende
Ausweg — die veroeffentlichten Shorts von YouTube laden — scheitert an
"Sign in to confirm you're not a bot": aus einem Rechenzentrum laesst YouTube
keinen Download zu, auch nicht fuer eigene Videos.

Das Material lag die ganze Zeit im Drive des Nutzers. Dieses Werkzeug holt es
von dort und legt es in der Ordnerstruktur ab, die nb_lang.py erwartet.

    python3 tools/kp_drive_holen.py <serie> --ordner <DRIVE_ORDNER_ID>
    python3 tools/kp_drive_holen.py <serie> --ordner <ID> --probe

Zuordnung nach Dateiname (Drive-Namen sind historisch uneinheitlich):
    "voice 3.mp3", "lengede 3.mp3", "short_03.mp3"  -> voiceover/short_03.mp3
    "V4_short07_*.webp", "*_s07_*.jpg"              -> bilder/S07/
    alles andere Bild                                -> bilder/broll/

Heruntergeladen wird nur, was fehlt. Fremdmaterial (ref_*, Presse-, Getty-)
wird uebersprungen — dieselbe Definition wie Regel R24.
"""

import argparse
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from kp_regeln import ist_fremdmaterial            # noqa: E402

BILD_ENDUNGEN = (".jpg", ".jpeg", ".png", ".webp")
TON_ENDUNGEN = (".mp3", ".wav", ".m4a")
VIDEO_ENDUNGEN = (".mp4", ".mov", ".webm")


def nummer(name):
    """Short-Nummer aus einem Drive-Dateinamen ziehen, sonst None."""
    n = name.lower()
    for muster in (r"short[_\s-]*(\d{1,2})", r"voice[_\s-]*(\d{1,2})",
                   r"_s(\d{1,2})[_.]", r"[a-z]+\s*(\d{1,2})\.(?:mp3|wav|m4a)$"):
        m = re.search(muster, n)
        if m:
            return f"{int(m.group(1)):02d}"
    return None


def ziel_fuer(serie, datei):
    name = datei["title"]
    low = name.lower()
    nr = nummer(name)
    if low.endswith(TON_ENDUNGEN):
        if not nr:
            return None, "Tondatei ohne erkennbare Nummer"
        return os.path.join(serie, "voiceover", f"short_{nr}.mp3"), None
    if low.endswith(VIDEO_ENDUNGEN):
        # Fertige Shorts. Fuer San Jose liegt im Drive NUR das -- kein
        # Voiceover, keine Bilder. Damit ist kein echter 16:9-Neubau moeglich,
        # nur die Montage der fertigen Shorts (nb_concat_shorts.py --wide).
        # Die tragen ihre eingebrannte Fortschrittsleiste und ihr CTA mit;
        # das ist ein sichtbarer Nachteil und wird nicht verschwiegen.
        if not nr:
            return None, "Video ohne erkennbare Nummer"
        return os.path.join(serie, "output", f"short_{nr}.mp4"), None
    if low.endswith(BILD_ENDUNGEN):
        if ist_fremdmaterial(name):
            return None, "Fremdmaterial (R24) — nie ins Sendematerial"
        endung = os.path.splitext(low)[1]
        if nr:
            return os.path.join(serie, "bilder", f"S{nr}",
                                f"{os.path.splitext(name)[0]}{endung}"), None
        sicher = re.sub(r"[^A-Za-z0-9._-]+", "_", name)
        return os.path.join(serie, "bilder", "broll", sicher), None
    return None, "kein Ton, kein Bild, kein Video"


def drive_liste(ordner_id):
    """Nutzt den Drive-Konnektor ueber eine JSON-Datei, die der Aufrufer
    vorbereitet hat — dieses Skript hat selbst keinen Drive-Zugang.

    Erwartet <scratch>/drive_<ordner_id>.json mit der Antwort von
    mcp__Google_Drive__search_files (Feld "files").
    """
    for kandidat in (f"drive_{ordner_id}.json",
                     os.path.join(os.environ.get("KP_SCRATCH", "."),
                                  f"drive_{ordner_id}.json")):
        if os.path.exists(kandidat):
            d = json.load(open(kandidat, encoding="utf-8"))
            return d.get("files", d if isinstance(d, list) else [])
    raise SystemExit(
        f"Keine Dateiliste gefunden. Erst mit dem Drive-Konnektor auflisten und\n"
        f"die Antwort als drive_{ordner_id}.json ablegen (Feld 'files').")


def holen(datei_id, ziel):
    os.makedirs(os.path.dirname(ziel), exist_ok=True)
    r = subprocess.run([sys.executable, "-m", "gdown", datei_id, "-O", ziel,
                        "--quiet"], capture_output=True, text=True)
    return r.returncode == 0 and os.path.exists(ziel) and os.path.getsize(ziel) > 1000


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("serie")
    ap.add_argument("--ordner", required=True, help="Drive-Ordner-ID")
    ap.add_argument("--probe", action="store_true", help="nur zeigen, nichts holen")
    a = ap.parse_args()

    serie = os.path.join(ROOT, a.serie.rstrip("/"))
    dateien = drive_liste(a.ordner)
    print("=" * 74)
    print(f"  DRIVE -> {a.serie}   ({len(dateien)} Eintraege im Ordner)"
          f"{'   [Probelauf]' if a.probe else ''}")
    print("=" * 74)

    geholt = uebersprungen = vorhanden = 0
    for d in sorted(dateien, key=lambda x: x.get("title", "")):
        if d.get("mimeType", "").endswith("folder"):
            continue
        ziel, grund = ziel_fuer(serie, d)
        name = d["title"]
        if not ziel:
            print(f"  ueberspringe  {name[:44]:<46} {grund}")
            uebersprungen += 1
            continue
        rel = os.path.relpath(ziel, ROOT)
        if os.path.exists(ziel) and os.path.getsize(ziel) > 1000:
            vorhanden += 1
            continue
        if a.probe:
            print(f"  wuerde holen  {name[:44]:<46} -> {rel}")
            geholt += 1
            continue
        ok = holen(d["id"], ziel)
        print(f"  {'geholt' if ok else 'FEHLER':<12}  {name[:44]:<46} -> {rel}")
        geholt += ok

    print("-" * 74)
    print(f"  {geholt} geholt · {vorhanden} schon vorhanden · "
          f"{uebersprungen} uebersprungen")
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
