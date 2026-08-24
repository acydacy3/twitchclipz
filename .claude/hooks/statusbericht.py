#!/usr/bin/env python3
"""Sitzungsbericht fuer das Katastrophenprotokoll.

Laeuft am Ende des Sitzungsstart-Hooks. Die Ausgabe landet im Kontext,
damit Claude vom ersten Zug an weiss, was in dieser Sitzung geht und was
nicht — statt es im Fehlerfall einzeln herauszufinden.

Prueft vier Dinge:
  1. Sind die Pipeline-Skripte da?
  2. Sind die Werkzeuge installiert?
  3. Liegen die YouTube-Zugangsdaten vor?
  4. Welche Hosts sind erreichbar?
"""

import os
import shutil
import socket
import subprocess
import sys
from pathlib import Path

PROJEKT = Path(os.environ.get("CLAUDE_PROJECT_DIR", "/workspace/twitchclipz"))

PIPELINE = [
    "transcribe_vosk.py", "align.py", "pauses.py", "bildcheck.py",
    "karaoke.py", "musik.py", "short.py", "serie.py", "lang.py",
    "videocheck.py", "analyse.py",
]

WERKZEUGE = ["ffmpeg", "ffprobe", "convert"]

PAKETE = [
    ("vosk", "vosk"), ("PIL", "pillow"), ("numpy", "numpy"),
    ("googleapiclient", "google-api-python-client"),
]

ZUGANG = ["YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN"]

# Nur Hosts, deren Erreichbarkeit eine Entscheidung aendert.
HOSTS = [
    ("www.googleapis.com", "YouTube Data + Analytics API"),
    ("www.youtube.com", "Recherche, YoutubeTags"),
    ("api.elevenlabs.io", "Voiceover"),
    ("higgsfield.ai", "Bilder"),
]


def haken(ok):
    return "ja " if ok else "NEIN"


def erreichbar(host, timeout=6):
    """Echte Verbindung durch den Proxy, nicht nur DNS."""
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if not proxy:
        try:
            socket.create_connection((host, 443), timeout=timeout).close()
            return True
        except OSError:
            return False
    try:
        r = subprocess.run(
            ["curl", "-sS", "-o", "/dev/null", "-w", "%{http_code}",
             "--max-time", str(timeout), f"https://{host}/"],
            capture_output=True, text=True, timeout=timeout + 4,
        )
        return r.stdout.strip() not in ("", "000")
    except Exception:
        return False


def main():
    zeilen = []
    z = zeilen.append

    z("")
    z("=" * 62)
    z("  KATASTROPHENPROTOKOLL — Sitzungsstart")
    z("=" * 62)

    # 1 ------------------------------------------------------ Skripte
    fehlend = [d for d in PIPELINE if not (PROJEKT / d).is_file()]
    if fehlend:
        z(f"Pipeline:    {len(PIPELINE) - len(fehlend)}/{len(PIPELINE)} da "
          f"— es fehlen: {', '.join(fehlend)}")
    else:
        z(f"Pipeline:    alle {len(PIPELINE)} Skripte da")

    # 2 ---------------------------------------------------- Werkzeuge
    fehlt_w = [w for w in WERKZEUGE if not shutil.which(w)]
    fehlt_p = []
    for modul, paket in PAKETE:
        try:
            __import__(modul)
        except ImportError:
            fehlt_p.append(paket)

    modell = next(
        (p for p in (Path("/opt/vosk-model-small-de-0.15"),
                     PROJEKT / "vosk-model-small-de-0.15") if p.is_dir()),
        PROJEKT / "vosk-model-small-de-0.15",
    )
    if not fehlt_w and not fehlt_p and modell.is_dir():
        z("Werkzeuge:   vollstaendig (ffmpeg, ImageMagick, vosk, PIL, numpy)")
    else:
        teile = []
        if fehlt_w:
            teile.append("Programme: " + ", ".join(fehlt_w))
        if fehlt_p:
            teile.append("Pakete: " + ", ".join(fehlt_p))
        if not modell.is_dir():
            teile.append("Vosk-Sprachmodell")
        z("Werkzeuge:   ES FEHLT — " + " | ".join(teile))
        z("             Der Sitzungsstart-Hook hat sie nicht installiert.")
        z("             Ursache pruefen, bevor die Pipeline benutzt wird.")

    # 3 ------------------------------------------------------- Zugang
    gesetzt = [v for v in ZUGANG if os.environ.get(v)]
    if len(gesetzt) == len(ZUGANG):
        z("YouTube:     OAuth-Zugangsdaten vollstaendig (Schreibzugriff moeglich)")
    elif gesetzt:
        fehlt = [v for v in ZUGANG if v not in gesetzt]
        z(f"YouTube:     UNVOLLSTAENDIG — es fehlen {', '.join(fehlt)}")
    elif os.environ.get("YOUTUBE_API_KEY"):
        z("YouTube:     nur API-Key (Lesezugriff). Kein Hochladen, "
          "kein Sprache-Setzen.")
    else:
        z("YouTube:     KEIN ZUGANG — weder OAuth noch API-Key gesetzt.")
        z("             Umgebungsvariablen in claude.ai/code eintragen,")
        z("             danach eine NEUE Sitzung starten (laufende lesen sie nicht).")

    # 4 --------------------------------------------------------- Netz
    z("-" * 62)
    for host, wofuer in HOSTS:
        z(f"  {haken(erreichbar(host))}  {host:<22} {wofuer}")

    z("=" * 62)
    z("CLAUDE.md ist geladen (Einstieg). Das Langzeitgedaechtnis liegt im")
    z("Obsidian-Vault YouTube-Knowledge/ — Start: YouTube-Knowledge/HOME.md.")
    z("Vor wichtigen Entscheidungen dort suchen (Retrieval before Reinvention).")
    z("Das Originalskript kommt IMMER vom Nutzer. Niemals selbst eins schreiben.")
    z("Der Nutzer arbeitet nicht mit der Kommandozeile: nie einen Befehl")
    z("hinwerfen, sondern selbst erledigen oder Klick-Schritte erklaeren.")
    z("=" * 62)
    z("")

    print("\n".join(zeilen))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # Der Hook darf niemals die Sitzung blockieren.
        print(f"Statusbericht fehlgeschlagen: {e}", file=sys.stderr)
        sys.exit(0)
