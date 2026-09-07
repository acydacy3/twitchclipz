#!/usr/bin/env python3
"""PreToolUse-Hook — haelt Render und Upload an, wenn kp_gate.py rot ist.

Warum das noetig ist: Bis heute war jede Produktionsregel Prosa. Sie stand im
Vault, im Statusbericht und in der Pflichtliste -- und wurde trotzdem gebrochen,
ohne dass es jemand merkte ("Marathon des Apples" ging live). Der Grund ist
strukturell: das Modell war fuer die Durchsetzung seiner eigenen Regeln
zustaendig. Ein PreToolUse-Hook ist es nicht -- er laeuft vor dem Werkzeugaufruf
und kann ihn mit Exit-Code 2 verhindern.

Was hier blockiert wird: NUR Befehle, die tatsaechlich rendern oder hochladen.
Alles andere laeuft unberuehrt durch -- ein Hook, der beim Arbeiten stoert,
wird abgeschaltet und schuetzt dann gar nichts mehr.

Exit-Codes (Claude-Code-Vertrag):
    0   durchlassen
    2   blockieren; stderr wird dem Modell als Begruendung gezeigt
"""

import json
import os
import re
import subprocess
import sys

REPO = os.environ.get("CLAUDE_PROJECT_DIR") or \
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Befehle, die Material erzeugen oder veroeffentlichen. Nur diese werden geprueft.
#
# Wichtig: es muss ein AUSFUEHREN sein, kein blosses Vorkommen des Dateinamens.
# "sed -n '30,130p' ralston/nb_build.py" liest die Datei und rendert nichts --
# ein Hook, der so etwas blockiert, steht beim Arbeiten im Weg und wird
# abgeschaltet. Deshalb muss ein Python-Aufruf davorstehen.
_AUSFUEHREN = r"(?:python3?|py|uv\s+run)\s+(?:-\w+\s+)*"
RENDER = re.compile(
    _AUSFUEHREN + r"\S*\b(?:nb_build|short|serie|nb_lang|lang)\.py\b")
UPLOAD = re.compile(
    _AUSFUEHREN + r"\S*\b(?:nb_upload|upload_all|youtube_upload)\.py\b")

# Serien-Ordner heraussuchen: "python3 prosperi/nb_build.py" -> prosperi
SERIE_IM_PFAD = re.compile(r"([A-Za-z0-9_-]+)/(?:nb_build|nb_upload)\.py")
# "python3 nb_lang.py prosperi" / "python3 lang.py ralston/"
SERIE_ALS_ARG = re.compile(
    r"\b(?:nb_lang|lang|serie|short)\.py\s+(?:--\S+\s+)*([A-Za-z0-9_-]+)/?")


def ohne_heredoc(cmd):
    """Text in Here-Dokumenten ist Daten, kein Befehl.

    Gefunden am 07.09.2026: Dieser Riegel blockierte einen Aufruf, der lediglich
    eine Dokumentationstabelle SCHRIEB, in der ein Render-Befehl als Beispiel
    vorkam. Er blockierte danach sogar seine eigene Reparatur, weil auch die
    den Beispieltext enthielt -- ein sauberer Beweis, dass er nicht ueberredbar
    ist, und zugleich ein Fehlalarm. Ein Riegel mit Fehlalarmen wird
    abgeschaltet und schuetzt danach gar nichts mehr. Deshalb wird der Rumpf
    jedes Here-Dokuments vor der Pruefung entfernt.
    """
    raus, im_dok, ende = [], False, None
    for z in cmd.split("\n"):
        if im_dok:
            if z.strip() == ende:
                im_dok, ende = False, None
            continue
        m = re.search(r"<<-?\s*['\"]?([A-Za-z_][A-Za-z0-9_]*)['\"]?", z)
        if m:
            im_dok, ende = True, m.group(1)
            raus.append(z[:m.start()])
            continue
        raus.append(z)
    return "\n".join(raus)


def serie_finden(cmd):
    m = SERIE_IM_PFAD.search(cmd)
    if m:
        return m.group(1)
    m = SERIE_ALS_ARG.search(cmd)
    if m and os.path.isdir(os.path.join(REPO, m.group(1))):
        return m.group(1)
    return None


def blockieren(text):
    print(text, file=sys.stderr)
    sys.exit(2)


# R23 — TikTok wird NIE automatisch bespielt.
# Beleg: automatisch terminiert = 1 View je Video, vom Nutzer selbst
# hochgeladen = Tausende. Bis heute war das eine Zeile im Vault. Jetzt haelt
# der Riegel jeden Buffer-Post an, der auf einen TikTok-Kanal zielt.
TIKTOK = re.compile(r"tiktok", re.I)


def pruefe_tiktok(daten):
    werkzeug = daten.get("tool_name", "")
    if not werkzeug.startswith("mcp__Buffer__"):
        return
    if "create_post" not in werkzeug and "update_post" not in werkzeug:
        return
    roh = json.dumps(daten.get("tool_input") or {}, ensure_ascii=False)
    if TIKTOK.search(roh):
        blockieren(
            "KP-GATE (R23): Buffer-Post auf einen TikTok-Kanal angehalten.\n"
            "TikTok wird NIE automatisch bespielt — automatisch terminiert "
            "brachte 1 View je Video, vom Nutzer selbst hochgeladen Tausende.\n"
            "Richtiger Weg: die fertigen Shorts an den Nutzer geben "
            "(SendUserFile), er laedt sie selbst hoch.")


def main():
    try:
        daten = json.load(sys.stdin)
    except Exception:
        sys.exit(0)          # nichts Verwertbares -> nicht im Weg stehen

    pruefe_tiktok(daten)

    if daten.get("tool_name") != "Bash":
        sys.exit(0)
    cmd = (daten.get("tool_input") or {}).get("command", "")
    if not cmd:
        sys.exit(0)
    cmd = ohne_heredoc(cmd)

    ist_render = bool(RENDER.search(cmd))
    ist_upload = bool(UPLOAD.search(cmd))
    if not (ist_render or ist_upload):
        sys.exit(0)

    serie = serie_finden(cmd)
    if not serie:
        blockieren(
            "KP-GATE: Render-/Upload-Befehl erkannt, aber der Serien-Ordner "
            "liess sich nicht bestimmen.\n"
            f"Befehl: {cmd[:160]}\n"
            "Rufe den Befehl so auf, dass der Serien-Ordner im Pfad steht "
            "(z. B. 'python3 prosperi/nb_build.py'), damit das Gate pruefen kann.")

    gate = os.path.join(REPO, "tools", "kp_gate.py")
    if not os.path.exists(gate):
        sys.exit(0)          # Gate nicht installiert -> alte Welt, nicht blocken

    try:
        p = subprocess.run([sys.executable, gate, serie],
                           cwd=REPO, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        blockieren("KP-GATE: Pruefung ueberschritt 120 s und wurde abgebrochen. "
                   "Kein Render/Upload ohne bestandene Pruefung. "
                   f"Von Hand: python3 tools/kp_gate.py {serie}")

    if p.returncode == 0:
        sys.exit(0)          # gruen -> durchlassen
    if p.returncode == 2:
        # Material nicht gefunden: das ist kein Freibrief.
        blockieren(f"KP-GATE: '{serie}' konnte nicht geprueft werden.\n"
                   f"{p.stderr.strip()}\n"
                   f"Von Hand pruefen: python3 tools/kp_gate.py {serie}")

    was = "Upload" if ist_upload else "Render"
    blockieren(
        f"KP-GATE hat den {was} von '{serie}' angehalten — "
        f"mindestens eine Produktionsregel ist verletzt.\n\n"
        f"{p.stdout.strip()}\n\n"
        f"Behebe die oben genannten Stellen und rufe den Befehl erneut auf. "
        f"Einzelpruefung: python3 tools/kp_gate.py {serie} --short XX")


if __name__ == "__main__":
    main()
