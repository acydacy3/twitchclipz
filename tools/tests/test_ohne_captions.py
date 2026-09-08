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
