#!/usr/bin/env python3
"""kp_captions.py — Caption-Woerter aus dem Nutzer-Skript neu setzen.

Das ist das Werkzeug, das Commit 1587675 am 31.08.2026 versprochen hat
("Caption-aus-Skript pipeline-weit erzwungen") und das es nie gab: der Commit
aenderte nur zwei Markdown-Dateien. Der eigentliche Fix lebte in genau einer
Kopie, `ralston/nb_build.py`, und wanderte nie weiter. prosperi und nuttyputty
tragen deshalb bis heute Spracherkennungs-Fehler in ihren Wortlisten —
"Marathon des Apples" statt "Sables", "zwenkt" statt "zwaengt".

Hier wird das serienunabhaengig gemacht:

    Text  kommt aus <serie>/skript/short_XX.txt  (per QUELLE.json belegt)
    Timing kommt aus der vorhandenen Wortliste   (die ASR hoert die ZEITEN richtig)
    align.py fuehrt beides zusammen

    python3 tools/kp_captions.py <serie>              alle Shorts
    python3 tools/kp_captions.py <serie> --short 03
    python3 tools/kp_captions.py <serie> --probe      nur zeigen, nichts schreiben

Die alte Wortliste wird als <name>.asr.json daneben gesichert, nicht
ueberschrieben — der Irrweg gehoert zum Wissen (Guardrail #6).

Exit-Code 0 = alle Shorts stimmen jetzt mit dem Skript ueberein.
"""

import argparse
import json
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import align as _align          # noqa: E402
import kp_regeln as R           # noqa: E402


def skript_tokens(text):
    toks, ends = [], []
    for m in re.finditer(_align.TOKEN_RE, text):
        toks.append(m.group())
        ends.append(bool(re.match(r"\s*[.!?:]", text[m.end():m.end() + 3])))
    return toks, ends


def setze(serie, num, probe=False):
    m = R.Material(serie, num)
    _, text = m.skript
    wp, words = m.words
    if text is None:
        return None, f"Short {num}: kein Skript"
    if not words:
        return None, f"Short {num}: keine Wortliste (Timing fehlt)"

    toks, ends = skript_tokens(text)
    if not toks:
        return None, f"Short {num}: Skript enthaelt keine Woerter"

    fixed = _align.align(words, toks, ends)
    if len(fixed) < max(5, len(toks) // 3):
        return None, (f"Short {num}: Abgleich ergab nur {len(fixed)} von "
                      f"{len(toks)} Woertern — nicht geschrieben")

    geaendert = sum(1 for a, b in zip(words, fixed)
                    if a.get("word") != b.get("word"))
    if probe:
        beispiele = [(a["word"], b["word"]) for a, b in zip(words, fixed)
                     if a.get("word") != b.get("word")][:5]
        return fixed, (f"Short {num}: {geaendert} Woerter wuerden sich aendern"
                       + ("  " + ", ".join(f'"{a}"->"{b}"' for a, b in beispiele)
                          if beispiele else ""))

    sicherung = wp.replace(".json", ".asr.json")
    if not os.path.exists(sicherung):
        shutil.copy2(wp, sicherung)
    json.dump(fixed, open(wp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return fixed, f"Short {num}: {len(fixed)} Woerter gesetzt ({geaendert} geaendert)"


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("serie")
    ap.add_argument("--short")
    ap.add_argument("--probe", action="store_true", help="nur zeigen, nichts schreiben")
    a = ap.parse_args()

    serie = a.serie.rstrip("/")
    if not os.path.isdir(serie):
        serie = os.path.join(ROOT, serie)
        if not os.path.isdir(serie):
            print(f"Serie '{a.serie}' nicht gefunden.", file=sys.stderr)
            return 2

    # Ohne Herkunftsnachweis wird nichts gesetzt: sonst schreibt man womoeglich
    # Spracherkennung ueber Spracherkennung und nennt es "aus dem Skript".
    mp, man = R.Material(serie, "01").manifest
    if man is None:
        print(f"ABBRUCH: {mp} fehlt. Erst das Nutzer-Skript aufnehmen:\n"
              f"  python3 tools/kp_skript.py {a.serie} --aus <datei>", file=sys.stderr)
        return 2

    nums = [a.short] if a.short else [f"{i:02d}" for i in range(1, 21)]
    print("=" * 74)
    print(f"  CAPTIONS AUS SKRIPT  —  {serie}"
          f"{'  (Probelauf)' if a.probe else ''}")
    print("=" * 74)
    getan = 0
    for n in nums:
        if not R.Material(serie, n).voiceover and not R.Material(serie, n).words[0]:
            continue
        fixed, meldung = setze(serie, n, a.probe)
        print(f"  {meldung}")
        getan += bool(fixed)

    if a.probe:
        print("\nProbelauf — nichts geschrieben.")
        return 0

    print(f"\n{getan} Short(s) neu gesetzt. Alte Listen liegen als *.asr.json daneben.")
    print("Gegenprobe:")
    schlecht = 0
    for n in nums:
        if not R.Material(serie, n).words[0]:
            continue
        b = R.p_captions(R.Material(serie, n))
        if not b.ok:
            schlecht += 1
            print(f"  {b.text}")
    if schlecht:
        print(f"{schlecht} Short(s) weichen weiter ab.")
        return 1
    print("  alle Shorts stimmen mit dem Skript ueberein.")
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
