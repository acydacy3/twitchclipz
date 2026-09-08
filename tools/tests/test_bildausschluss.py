#!/usr/bin/env python3
"""Prueft den Bildausschluss: Fremdmaterial + begruendet Aussortiertes.

Warum es diesen Test gibt: Der Mechanismus ist die einzige Stelle, an der ein
Bild aus dem Schnitt faellt. Faellt er still aus (z. B. weil AUSSORTIERT.json
unlesbar wird oder die .gitignore-Ausnahme wieder verschwindet), landen die
themenfremden Bilder aus F-V9-T wieder im Video — und nichts meldet sich.
"""
import json
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import kp_regeln as R

fehler = []


def pruefe(name, bedingung, info=""):
    print(("  ok   " if bedingung else "  FEHL ") + name + ("  " + info if info else ""))
    if not bedingung:
        fehler.append(name)


print("Bildausschluss")

# 1) Fremdmaterial-Konvention
pruefe("ref_ gilt als Fremdmaterial",
       R.bild_ausgeschlossen("x", "x/bilder/ref_01.jpg") is not None)
pruefe("getty im Namen gilt als Fremdmaterial",
       R.bild_ausgeschlossen("x", "x/bilder/getty_123.jpg") is not None)
pruefe("hf_ ist erlaubt",
       R.bild_ausgeschlossen("x", "x/bilder/hf_s01_wueste.jpg") is None)

# 2) AUSSORTIERT.json wird gelesen und liefert den GRUND zurueck
with tempfile.TemporaryDirectory() as d:
    os.makedirs(os.path.join(d, "serie", "bilder", "short_08"))
    json.dump({"short_08/01.jpg": "Historisches Schwarzweiss"},
              open(os.path.join(d, "serie", "bilder", "AUSSORTIERT.json"), "w"))
    R._AUSSORTIERT_CACHE.clear()
    alt = os.getcwd()
    os.chdir(d)
    try:
        g = R.bild_ausgeschlossen("serie", "serie/bilder/short_08/01.jpg")
        pruefe("aussortiertes Bild wird erkannt", g is not None, f"({g})")
        pruefe("der Grund kommt mit zurueck", g == "Historisches Schwarzweiss")
        pruefe("Nachbarbild bleibt drin",
               R.bild_ausgeschlossen("serie", "serie/bilder/short_08/02.jpg") is None)
    finally:
        os.chdir(alt)
        R._AUSSORTIERT_CACHE.clear()

# 3) Echte Serien: die Entscheidungen von 08.09. gelten noch
for serie, datei, soll in (
        ("nuttyputty", "nuttyputty/bilder/short_08/01.jpg", True),
        ("nuttyputty", "nuttyputty/bilder/short_06/01.jpg", False),
        ("lengede", "lengede/bilder/broll/das-wunder-von-lengede-1.jpg", True)):
    if not os.path.isdir(os.path.join(ROOT, serie)):
        continue
    alt = os.getcwd()
    os.chdir(ROOT)
    R._AUSSORTIERT_CACHE.clear()
    try:
        g = R.bild_ausgeschlossen(serie, datei)
        pruefe(f"{datei} {'raus' if soll else 'drin'}", (g is not None) == soll,
               f"({(g or '')[:40]})")
    finally:
        os.chdir(alt)

# 4) Der Longform-Bauer ruft wirklich diese Funktion auf
quelle = open(os.path.join(ROOT, "nb_lang.py"), encoding="utf-8").read()
pruefe("nb_lang.py nutzt bild_ausgeschlossen", "bild_ausgeschlossen(serie, p)" in quelle)

# 5) Die Entscheidungsdateien sind nicht gitignoriert
import subprocess
for f in ("nuttyputty/bilder/AUSSORTIERT.json", "nuttyputty/bilder/HERKUNFT.json"):
    if not os.path.exists(os.path.join(ROOT, f)):
        continue
    p = subprocess.run(["git", "check-ignore", f], cwd=ROOT, capture_output=True)
    pruefe(f"{f} ist versioniert", p.returncode != 0)

print()
if fehler:
    raise SystemExit(f"{len(fehler)} Fehler: " + ", ".join(fehler))
print("Alle Pruefungen bestanden.")
