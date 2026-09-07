"""Regressionstest fuer den PreToolUse-Riegel (.claude/hooks/pre-tool-use.py).

Ein Riegel muss zwei Dinge koennen, und beide werden hier geprueft:
  sperren    einen Render/Upload, dessen Material eine Regel verletzt
  durchlassen alles andere -- auch das blosse LESEN einer Build-Datei

Der zweite Teil ist der wichtigere. Ein Riegel mit Fehlalarmen wird
abgeschaltet und schuetzt danach gar nichts mehr. Genau das passierte beim
ersten Entwurf: "sed -n '30,130p' ralston/nb_build.py" wurde blockiert, weil
der Dateiname im Befehl vorkam.

    python3 tools/tests/test_pre_tool_use.py
"""
import json
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HOOK = os.path.join(REPO, ".claude", "hooks", "pre-tool-use.py")
GATE = os.path.join(REPO, "tools", "kp_gate.py")

DURCH, SPERRE = 0, 2


def gate_zustand(serie):
    p = subprocess.run([sys.executable, GATE, serie], cwd=REPO,
                       capture_output=True, text=True)
    return p.returncode


def hook(cmd, werkzeug="Bash"):
    p = subprocess.run(
        [sys.executable, HOOK], cwd=REPO, capture_output=True, text=True,
        input=json.dumps({"tool_name": werkzeug, "tool_input": {"command": cmd}}))
    return p.returncode


def main():
    # Serien nach ihrem aktuellen Gate-Zustand einteilen, statt ihn zu raten.
    rot = [s for s in ("prosperi", "nuttyputty") if gate_zustand(s) == 1]
    gruen = [s for s in ("ralston",) if gate_zustand(s) == 0]
    if not rot:
        print("Keine Serie ist derzeit rot — Sperr-Faelle nicht pruefbar.")
    if not gruen:
        print("Keine Serie ist derzeit gruen — Durchlass-Faelle nicht pruefbar.")

    faelle = [
        # (Befehl, erwartet, Beschreibung)
        ("ls -la",                                    DURCH, "harmloser Befehl"),
        ("cat ralston/nb_build.py",                   DURCH, "Build-Datei lesen"),
        ("grep -n SHORTS ralston/nb_build.py",        DURCH, "Build-Datei durchsuchen"),
        ("sed -n '30,130p' ralston/nb_build.py",      DURCH, "Build-Datei ausschnittweise lesen"),
        ("python3 tools/kp_gate.py ralston",          DURCH, "Gate selbst aufrufen"),
        # Here-Dokument: der Rumpf ist Datentext, kein Befehl. Der Riegel
        # blockierte hier einmal das blosse SCHREIBEN einer Doku-Tabelle.
        ("cat > doku.md <<'EOF'\n| 4 | Rendern | python3 x/nb_build.py |\nEOF",
         DURCH, "Render-Befehl nur als Text schreiben"),
    ]
    for s in gruen:
        faelle += [(f"python3 {s}/nb_build.py", DURCH, f"Render der gruenen Serie {s}")]
    for s in rot:
        faelle += [
            (f"python3 {s}/nb_build.py",            SPERRE, f"Render der roten Serie {s}"),
            (f"python3 {s}/nb_upload.py --longform", SPERRE, f"Upload der roten Serie {s}"),
            (f"python3 nb_lang.py {s}",              SPERRE, f"Longform der roten Serie {s}"),
        ]

    fehler = 0
    for cmd, erwartet, was in faelle:
        ist = hook(cmd)
        ok = ist == erwartet
        fehler += not ok
        print(f"  [{'ok ' if ok else 'FEHL'}] Exit {ist} (erwartet {erwartet})  "
              f"{was:<34} {cmd[:42]}")

    print()
    if fehler:
        print(f"{fehler} Abweichung(en) — der Riegel verhaelt sich nicht wie beschrieben.")
        return 1
    print(f"Alle {len(faelle)} Faelle wie erwartet "
          f"(rot: {rot or '—'} · gruen: {gruen or '—'}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
