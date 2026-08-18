#!/usr/bin/env bash
# Laeuft automatisch beim Start jeder Sitzung.
#
# Zweck: Der Container ist eine Wegwerfumgebung. Ohne diesen Hook muesste
# die Werkzeugkiste in jeder Sitzung von Hand neu aufgebaut werden.
#
# Wichtig: Die Installation laeuft im HINTERGRUND. Ein Hook, der minutenlang
# blockiert, verzoegert den Sitzungsstart — deshalb startet er nur und meldet
# sofort zurueck. Der Fortschritt steht in .claude/setup.log.
#
# Falls dieser Hook je Aerger macht: Datei loeschen, mehr ist es nicht.

REPO="$(cd "$(dirname "$0")/../.." && pwd)"
LOG="$REPO/.claude/setup.log"

if [ ! -f "$REPO/werkzeuge/setup.sh" ]; then
  exit 0
fi

# Schon vollstaendig? Dann nichts tun und nicht laermen.
if python3 -c "import faster_whisper, yt_dlp, vosk" 2>/dev/null \
   && [ -d "$REPO/.agents/skills/faceless-explainer" ]; then
  echo "Werkzeugkiste vollstaendig (ffmpeg, vosk, faster-whisper, yt-dlp, Hyperframes)."
  exit 0
fi

nohup bash "$REPO/werkzeuge/setup.sh" > "$LOG" 2>&1 &

cat <<'HINWEIS'
Werkzeugkiste wird im Hintergrund wiederhergestellt (dauert 1-3 Minuten).
Fortschritt:  cat .claude/setup.log
Von Hand:     bash werkzeuge/setup.sh

Verfuegbar danach:
  python3 werkzeuge/videoblick.py FILM.mp4   Video ansehen
  python3 werkzeuge/hoeren.py FILM.mp4       Tonspur transkribieren
  yt-dlp URL                                 Material laden
HINWEIS
exit 0
