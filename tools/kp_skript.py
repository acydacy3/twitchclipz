#!/usr/bin/env python3
"""kp_skript.py — Nutzer-Skript aufnehmen und seine Herkunft belegen.

Warum es dieses Werkzeug gibt: Constraint #1 sagt "Das Originalskript kommt
IMMER vom Nutzer". Die Regel "Captions IMMER aus Skript" verliess sich darauf,
dass in <serie>/skript/ das Nutzer-Skript liegt. Bei V7 Prosperi schrieb aber
prosperi/nb_transcribe.py die Spracherkennung nach prosperi/skripte/ -- die
ASR-Ausgabe wurde damit zur vermeintlichen Wahrheitsquelle, und die Regel war
formal erfuellt, waehrend "Marathon des Apples" ins Video gebrannt wurde.

Ein Ordnername beweist nichts. Ein Hash schon.

    python3 tools/kp_skript.py <serie> --aus <datei>     Skript aufnehmen
    python3 tools/kp_skript.py <serie> --pruefen         Manifest gegen Platte
    python3 tools/kp_skript.py <serie> --zeigen          Manifest anzeigen

<datei> ist das, was der Nutzer geliefert hat. Zwei Formate:
  .json   {"01": "Text ...", "02": "Text ..."}
  .txt    Abschnitte, getrennt durch eine Zeile "short_01" / "## short_01" /
          "SHORT 1" -- Gross/Kleinschreibung egal.

Geschrieben wird:
  <serie>/skript/short_XX.txt    der Text, so wie er gerendert wird
  <serie>/skript/QUELLE.json     sha256 je Short + woher + wann

Vertrauensstufen im Manifest (kp_gate.py zeigt sie an, nie verdeckt):
  nutzer            der Nutzer hat diese Datei in dieser Sitzung geliefert
  repo-historisch   aus dem Repo uebernommen, Inhalt gegen die Tonspur geprueft
Alles andere ist unbelegt -- und unbelegt heisst blockiert.
"""

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys

TRENNER = re.compile(r"^\s*(?:#{1,3}\s*)?short[_\s-]*0*(\d{1,2})\s*:?\s*$",
                     re.IGNORECASE)


def sha(text):
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()


def lies_lieferung(pfad):
    """Gibt {"01": "Text", ...} zurueck."""
    roh = open(pfad, encoding="utf-8").read()
    if pfad.endswith(".json"):
        d = json.load(open(pfad, encoding="utf-8"))
        return {str(k).zfill(2): v.strip() for k, v in d.items()}

    teile, aktuell, puffer = {}, None, []
    for zeile in roh.splitlines():
        m = TRENNER.match(zeile)
        if m:
            if aktuell:
                teile[aktuell] = "\n".join(puffer).strip()
            aktuell, puffer = m.group(1).zfill(2), []
            continue
        if aktuell:
            puffer.append(zeile)
    if aktuell:
        teile[aktuell] = "\n".join(puffer).strip()

    if not teile:
        raise SystemExit(
            f"In {pfad} keine Short-Abschnitte gefunden.\n"
            f"Erwartet Trennzeilen wie 'short_01' oder '## short_01'.")
    return teile


def manifest_pfad(serie):
    return os.path.join(serie, "skript", "QUELLE.json")


def lade_manifest(serie):
    p = manifest_pfad(serie)
    if os.path.exists(p):
        return json.load(open(p, encoding="utf-8"))
    return {"serie": os.path.basename(serie.rstrip("/")), "shorts": {}}


def aufnehmen(serie, quelle, vertrauen):
    teile = lies_lieferung(quelle)
    ziel = os.path.join(serie, "skript")
    os.makedirs(ziel, exist_ok=True)
    man = lade_manifest(serie)
    heute = dt.date.today().isoformat()

    for num in sorted(teile):
        text = teile[num]
        if not text:
            print(f"  uebersprungen: Short {num} ist leer")
            continue
        with open(os.path.join(ziel, f"short_{num}.txt"), "w",
                  encoding="utf-8") as f:
            f.write(text + "\n")
        man["shorts"][num] = {
            "sha256": sha(text),
            "zeichen": len(text),
            "geliefert_am": heute,
            "quelle": os.path.relpath(quelle),
            "vertrauen": vertrauen,
        }
        print(f"  Short {num}: {len(text):>5} Zeichen  sha256 {sha(text)[:16]}")

    man["aktualisiert"] = heute
    with open(manifest_pfad(serie), "w", encoding="utf-8") as f:
        json.dump(man, f, ensure_ascii=False, indent=1)
    print(f"\n{len(teile)} Shorts aufgenommen -> {manifest_pfad(serie)}")
    print(f"Vertrauensstufe: {vertrauen}")
    return 0


def pruefen(serie):
    man = lade_manifest(serie)
    if not man["shorts"]:
        print(f"Kein Manifest fuer '{serie}' -- Skript-Herkunft unbelegt.")
        return 1
    schlecht = 0
    for num, e in sorted(man["shorts"].items()):
        p = os.path.join(serie, "skript", f"short_{num}.txt")
        if not os.path.exists(p):
            print(f"  Short {num}: FEHLT auf der Platte ({p})")
            schlecht += 1
            continue
        ist = sha(open(p, encoding="utf-8").read())
        if ist != e["sha256"]:
            print(f"  Short {num}: VERAENDERT seit der Aufnahme")
            print(f"             jetzt {ist[:16]}, aufgenommen {e['sha256'][:16]}")
            schlecht += 1
        else:
            print(f"  Short {num}: unveraendert  [{e.get('vertrauen','?')}]")
    print()
    if schlecht:
        print(f"{schlecht} Abweichung(en) -- kp_gate.py wird blockieren.")
        return 1
    print("Alle Skripte stimmen mit der aufgenommenen Lieferung ueberein.")
    return 0


def zeigen(serie):
    man = lade_manifest(serie)
    if not man["shorts"]:
        print(f"Kein Manifest fuer '{serie}'.")
        return 1
    print(json.dumps(man, ensure_ascii=False, indent=1))
    return 0


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("serie")
    ap.add_argument("--aus", metavar="DATEI",
                    help="vom Nutzer geliefertes Skript (.txt oder .json)")
    ap.add_argument("--vertrauen", default="nutzer",
                    choices=["nutzer", "repo-historisch"],
                    help="woher die Lieferung stammt (Vorgabe: nutzer)")
    ap.add_argument("--pruefen", action="store_true")
    ap.add_argument("--zeigen", action="store_true")
    a = ap.parse_args()

    serie = a.serie.rstrip("/")
    if not os.path.isdir(serie):
        print(f"Serie '{serie}' nicht gefunden.", file=sys.stderr)
        return 2

    if a.aus:
        if not os.path.exists(a.aus):
            print(f"Datei '{a.aus}' nicht gefunden.", file=sys.stderr)
            return 2
        return aufnehmen(serie, a.aus, a.vertrauen)
    if a.pruefen:
        return pruefen(serie)
    if a.zeigen:
        return zeigen(serie)
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
