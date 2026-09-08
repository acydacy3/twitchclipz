#!/usr/bin/env python3
"""kp_gate.py — fuehrt die Regeln aus dem Register gegen echtes Material aus.

Dieses Skript enthaelt bewusst KEINE eigenen Regeln. Alle Regeln stehen in
`tools/kp_regeln.py`; hier werden sie nur ausgefuehrt und das Ergebnis wird zu
einem Exit-Code verdichtet. Der Grund: solange Gate und Regelliste getrennt
gepflegt wurden, konnte eine Regel im Vault stehen und im Gate fehlen, ohne
dass es auffiel — genau so blieben fuenf Regeln monatelang wirkungslos.

    python3 tools/kp_gate.py <serie>              vor dem Render
    python3 tools/kp_gate.py <serie> --nachher    am fertigen Video
    python3 tools/kp_gate.py <serie> --short 03   ein einzelner Short
    python3 tools/kp_gate.py <serie> --fuer longform  vor einem Longform-Bau
    python3 tools/kp_gate.py <serie> --langform   das Langvideo der Serie
    python3 tools/kp_gate.py --system             nur der Systemzustand
    python3 tools/kp_gate.py <serie> --json       maschinenlesbar

Exit-Code
    0   bestanden -> rendern/hochladen erlaubt
    1   mindestens eine harte Regel verletzt -> BLOCKIERT
    2   Serie/Material nicht gefunden
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kp_regeln as R

ROOT = R.ROOT


def shorts_einer_serie(serie):
    nums = set()
    for unter in ("", "skript", "skripte", "configs", "animation", "render", "voiceover"):
        d = os.path.join(serie, unter)
        if not os.path.isdir(d):
            continue
        for name in os.listdir(d):
            m = re.fullmatch(r"(?:short|words|sub)_(\d+)\.(?:txt|json|mp4|mp3|ass)", name)
            if m:
                nums.add(m.group(1))
    sj = os.path.join(serie, "skripte.json")
    if os.path.exists(sj):
        nums.update(json.load(open(sj, encoding="utf-8")).keys())
    return sorted(nums)


def pruefe_short(serie, num, phase, bauart=None, ohne_text=False):
    m = R.Material(serie, num)
    return [regel["pruefung"](m)
            for regel in R.regeln_der_phase(phase, bauart, ohne_text)]


def pruefe_system():
    return [regel["pruefung"](None) for regel in R.regeln_der_phase("dauerhaft")]


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("serie", nargs="?", help="Serien-Ordner, z. B. prosperi")
    ap.add_argument("--short", help="nur dieser Short, z. B. 03")
    ap.add_argument("--nachher", action="store_true",
                    help="das FERTIGE Video pruefen statt der Absicht")
    ap.add_argument("--fuer", choices=["shorts", "longform"], default="shorts",
                    help="welche Bauart geprueft wird (Vorher-Phase)")
    ap.add_argument("--langform", action="store_true",
                    help="das Langvideo der Serie pruefen (render/long.mp4)")
    ap.add_argument("--ohne-captions", dest="ohne_captions", action="store_true",
                    help="Bau ohne eingebrannte Untertitel: Regeln ueber den Text im "
                         "Bild entfallen (R01, R02). Kein Freibrief — R30 misst am "
                         "fertigen Langvideo nach, dass wirklich kein Text drin ist.")
    ap.add_argument("--system", action="store_true", help="nur den Systemzustand pruefen")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if a.system or not a.serie:
        befunde = pruefe_system()
        if a.json:
            print(json.dumps([b.als_dict() for b in befunde], ensure_ascii=False, indent=1))
        else:
            print("=" * 74)
            print("  KP-GATE  —  Systemzustand")
            print("=" * 74)
            for b in befunde:
                print(b)
            print("=" * 74)
        return 1 if any(not b.ok and b.hart for b in befunde) else 0

    serie = a.serie.rstrip("/")
    if not os.path.isdir(serie):
        alt = os.path.join(ROOT, serie)
        if not os.path.isdir(alt):
            print(f"Serie '{a.serie}' nicht gefunden.", file=sys.stderr)
            return 2
        serie = alt

    nums = [a.short] if a.short else shorts_einer_serie(serie)
    if not nums:
        print(f"Keine Shorts in '{serie}' gefunden.", file=sys.stderr)
        return 2

    if a.langform:
        # Die Langvideo-Regeln gelten je SERIE, nicht je Short.
        class _S:
            pass
        traeger = _S()
        traeger.serie = serie
        alle = {"long": [r["pruefung"](traeger) for r in R.regeln_der_phase("langform")]}
        phase = "langform"
    else:
        phase = "nachher" if a.nachher else "vorher"
        bauart = None if phase == "nachher" else a.fuer
        alle = {n: pruefe_short(serie, n, phase, bauart, a.ohne_captions)
                for n in nums}
    verstoesse = [(n, b) for n, bs in alle.items() for b in bs if not b.ok and b.hart]
    warnungen = [(n, b) for n, bs in alle.items() for b in bs if not b.ok and not b.hart]

    if a.json:
        print(json.dumps({
            "serie": serie, "phase": phase, "blockiert": bool(verstoesse),
            "shorts": {n: [b.als_dict() for b in bs] for n, bs in alle.items()},
        }, ensure_ascii=False, indent=1))
        return 1 if verstoesse else 0

    g, ges = R.deckung()
    print("=" * 74)
    wo = ("LANGFORM" if a.langform else
          ("NACHHER" if a.nachher else
           f"VORHER/{a.fuer}"))
    print(f"  KP-GATE {wo} —  {serie}  "
          f"({len(alle)} Einheit(en), {g}/{ges} Regeln erzwungen)")
    print("=" * 74)
    for n, befunde in alle.items():
        print(f"\n{'Langvideo' if n == 'long' else 'Short ' + n}")
        for b in befunde:
            print(b)

    print("\n" + "=" * 74)
    if verstoesse:
        print(f"  BLOCKIERT — {len(verstoesse)} Regelverletzung(en) in "
              f"{len({n for n, _ in verstoesse})} Short(s).")
        print("  Kein Render, kein Upload, bis diese behoben sind.")
        if warnungen:
            print(f"  Zusaetzlich {len(warnungen)} Hinweis(e), nicht blockierend.")
        print("=" * 74)
        return 1
    if warnungen:
        print(f"  BESTANDEN — mit {len(warnungen)} Hinweis(en):")
        for n, b in warnungen:
            print(f"    Short {n}: {b.regel_id} {b.text}")
    else:
        print("  BESTANDEN — alle harten Regeln erfuellt.")
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
