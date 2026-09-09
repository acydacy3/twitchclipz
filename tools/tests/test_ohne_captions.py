#!/usr/bin/env python3
"""Prueft, dass --ohne-captions eine BEHAUPTUNG bleibt und kein Freibrief.

Der Fehler, gegen den das geschrieben ist (F-V9-U): Eine Ausnahme von einer
Regel, die niemand nachmisst, ist ein Schalter zum Abstellen der Regel.
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import kp_regeln as R

fehler = []


def pruefe(name, bedingung, info=""):
    print(("  ok   " if bedingung else "  FEHL ") + name + ("  " + info if info else ""))
    if not bedingung:
        fehler.append(name)


print("Ausnahme --ohne-captions")

# 1) Der Filter trifft genau R01 und R02 -- nicht mehr
mit = {r["id"] for r in R.regeln_der_phase("vorher", "longform")}
ohne = {r["id"] for r in R.regeln_der_phase("vorher", "longform", ohne_text=True)}
weg = mit - ohne
pruefe("uebersprungen werden genau R01 und R02", weg == {"R01", "R02"}, str(sorted(weg)))
pruefe("keine Regel kommt dadurch hinzu", ohne <= mit)

# 2) R30 existiert, ist erzwungen und haengt an der Langform-Phase
r30 = [r for r in R.REGELN if r["id"] == "R30"]
pruefe("R30 ist im Register", len(r30) == 1)
if r30:
    pruefe("R30 hat einen Pruefpunkt", r30[0]["pruefung"] is not None)
    pruefe("R30 laeuft in der Langform-Phase", r30[0]["phase"] == "langform")

# 3) Ohne Marke ist R30 nicht zutreffend, mit Marke misst es


class _S:
    pass


for serie in ("ralston", "nuttyputty"):
    if not os.path.exists(os.path.join(ROOT, serie, "render", "long.mp4")):
        continue
    alt = os.getcwd()
    os.chdir(ROOT)
    try:
        t = _S()
        t.serie = serie
        b = R.p_kein_eingebrannter_text(t)
        marke = os.path.exists(R.ohne_captions_marke(serie))
        pruefe(f"{serie}: R30 {'misst' if marke else 'ist nicht zutreffend'}",
               b.ok, b.text[:60])
    finally:
        os.chdir(alt)

# 3b) R30 prueft den BELEG, nicht die Pixel-Helligkeit (F-V9-W)
import json as _json
import tempfile as _tmp


class _T:
    pass


with _tmp.TemporaryDirectory() as d:
    os.makedirs(os.path.join(d, "s", "render"))
    v = os.path.join(d, "s", "render", "long.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi",
                    "-i", "color=c=white:s=320x180:d=6", "-f", "lavfi",
                    "-i", "anullsrc=r=48000:cl=mono", "-t", "6",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", v],
                   capture_output=True)
    marke = os.path.join(d, "s", "render", "long.ohne-captions.json")
    alt = os.getcwd()
    os.chdir(d)
    try:
        t = _T()
        t.serie = "s"
        # WEISSES Bild, also maximale Bandhelligkeit -- die alte Fassung haette
        # hier blockiert. Ohne Textfilter in der Kette ist es trotzdem in Ordnung.
        _json.dump({"filterkette": "[0:v]scale=1920:1080[v0];[v0]concat=n=1[cat];[cat]copy[vout]"},
                   open(marke, "w"))
        b1 = R.p_kein_eingebrannter_text(t)
        pruefe("weisses Bild ohne Textfilter ist in Ordnung", b1.ok, b1.text[:60])

        _json.dump({"filterkette": "[cat]subtitles=x.ass:fontsdir=/usr/share/fonts[vout]"},
                   open(marke, "w"))
        b2 = R.p_kein_eingebrannter_text(t)
        pruefe("Textfilter in der Kette wird erwischt", not b2.ok, b2.text[:60])

        _json.dump({"grund": "irgendwas"}, open(marke, "w"))
        b3 = R.p_kein_eingebrannter_text(t)
        pruefe("Marke ohne Filterkette gilt als unbelegt", not b3.ok, b3.text[:60])

        # R31 ist ein HINWEIS und darf nie blockieren
        b4 = R.p_bandhelligkeit_hinweis(t)
        pruefe("R31 blockiert nie", b4.ok and not b4.hart, b4.text[:60])
    finally:
        os.chdir(alt)

# 4) Der Riegel reicht das Flag durch
hook = open(os.path.join(ROOT, ".claude", "hooks", "pre-tool-use.py"), encoding="utf-8").read()
pruefe("Riegel reicht --ohne-captions ans Gate durch",
       '"--ohne-captions"' in hook and "--ohne-captions\\b" in hook)

# 5) Das Gate kennt das Flag
p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "kp_gate.py"), "--help"],
                   capture_output=True, text=True, cwd=ROOT)
pruefe("Gate kennt --ohne-captions", "--ohne-captions" in p.stdout)

# 6) Der Bauer setzt und entfernt die Marke
lang = open(os.path.join(ROOT, "nb_lang.py"), encoding="utf-8").read()
pruefe("nb_lang.py setzt die Marke", "long.ohne-captions.json" in lang)
pruefe("nb_lang.py entfernt sie beim Bau MIT Untertiteln", "os.remove(marke)" in lang)

print()
if fehler:
    raise SystemExit(f"{len(fehler)} Fehler: " + ", ".join(fehler))
print("Alle Pruefungen bestanden.")
