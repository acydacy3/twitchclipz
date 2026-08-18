#!/usr/bin/env bash
# setup.sh — stellt die Werkzeugkiste in einer frischen Sitzung wieder her.
#
# WARUM ES DAS GIBT: Der Container wird nach jeder Sitzung weggeworfen.
# Alles, was nicht im Repo liegt, ist beim naechsten Mal weg. Dieses Skript
# holt in wenigen Minuten alles zurueck.
#
# Es laeuft automatisch ueber .claude/hooks/session-start.sh. Von Hand:
#   bash werkzeuge/setup.sh
#
# Was NICHT installiert wird und warum, steht am Ende der Ausgabe.

set -u
cd "$(dirname "$0")/.." || exit 1
echo "=== Werkzeugkiste Katastrophenprotokoll ==="

ok()   { printf '  [da]     %s\n' "$1"; }
neu()  { printf '  [neu]    %s\n' "$1"; }
warn() { printf '  [FEHLT]  %s\n' "$1"; }

# --- 1. Systemwerkzeuge (kommen mit dem Container) -----------------------
command -v ffmpeg  >/dev/null && ok "ffmpeg  $(ffmpeg -version | head -1 | cut -d' ' -f3)" || warn "ffmpeg"
command -v node    >/dev/null && ok "node    $(node -v)"  || warn "node"
command -v python3 >/dev/null && ok "python3 $(python3 -V | cut -d' ' -f2)" || warn "python3"

# --- 2. Python-Pakete ----------------------------------------------------
py_hol() {  # $1 = Importname, $2 = Paketname
  if python3 -c "import $1" 2>/dev/null; then
    ok "$2"
  else
    neu "$2 wird installiert ..."
    pip3 install --quiet "$2" 2>&1 | grep -v "WARNING: Running pip" | tail -2
    python3 -c "import $1" 2>/dev/null && ok "$2 bereit" || warn "$2 (Installation fehlgeschlagen)"
  fi
}
py_hol vosk vosk                     # Spracherkennung der Pipeline (Wortzeiten)
py_hol faster_whisper faster-whisper # Whisper ohne PyTorch-Ballast
py_hol yt_dlp yt-dlp                 # Material laden

# --- 3. Vosk-Sprachmodell (deutsch) --------------------------------------
MODELL="vosk-model-small-de-0.15"
if [ -d "$MODELL" ]; then
  ok "Vosk-Modell $MODELL"
else
  neu "Vosk-Modell wird geladen (~45 MB) ..."
  curl -sSL -o /tmp/vosk.zip \
    "https://github.com/kercre123/vosk-models/raw/main/$MODELL.zip" 2>/dev/null \
    && unzip -q -o /tmp/vosk.zip -d . && rm -f /tmp/vosk.zip \
    && ok "Vosk-Modell bereit" || warn "Vosk-Modell (Spiegel pruefen)"
fi

# --- 4. Hyperframes: HTML -> MP4, mit 28 fertigen Skills ------------------
# Offizielles Repo von HeyGen. Bringt u.a. faceless-explainer,
# captions-overlay und embedded-captions mit — genau unser Kanaltyp.
if [ -d ".agents/skills/hyperframes" ] || [ -d ".agents/skills/faceless-explainer" ]; then
  ok "Hyperframes-Skills"
else
  neu "Hyperframes wird installiert ..."
  npx -y skills add heygen-com/hyperframes >/dev/null 2>&1 \
    && ok "Hyperframes bereit" || warn "Hyperframes (npx-Fehler)"
fi

# --- 5. Remotion: Video aus React, programmatisch -------------------------
# Nur auf Wunsch — zieht ~400 MB. Aufruf: bash werkzeuge/setup.sh --remotion
if [ "${1:-}" = "--remotion" ]; then
  if [ -d "node_modules/remotion" ]; then
    ok "Remotion"
  else
    neu "Remotion wird installiert (~400 MB, dauert) ..."
    npm install --silent remotion @remotion/cli @remotion/renderer 2>&1 | tail -2
    [ -d "node_modules/remotion" ] && ok "Remotion bereit" || warn "Remotion"
  fi
else
  printf '  [aus]    Remotion (mit: bash werkzeuge/setup.sh --remotion)\n'
fi

echo
echo "Eigene Werkzeuge:"
printf '  videoblick.py  Video ansehen (Frames)     python3 werkzeuge/videoblick.py FILM.mp4\n'
printf '  hoeren.py      Tonspur transkribieren     python3 werkzeuge/hoeren.py FILM.mp4\n'
echo
echo "Bewusst NICHT installiert:"
printf '  Edits app  — Instagram-Handyapp, laeuft nicht auf einem Linux-Server.\n'
printf '               Was sie kann (Untertitel, Aufraeumen), macht karaoke.py bereits.\n'
printf '  Apify      — kostenpflichtiger Cloud-Dienst, braucht Konto und Schluessel.\n'
printf '               Transkripte holt hoeren.py lokal und kostenlos.\n'
printf '  Higgsfield — reiner Webdienst ohne lokales Paket. Bleibt Handarbeit.\n'
echo "=== fertig ==="
