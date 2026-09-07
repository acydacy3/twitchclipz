#!/bin/bash
# Katastrophenprotokoll — Sitzungsstart
#
# Laeuft automatisch, bevor Claude in einer neuen Sitzung anfaengt.
# Zweck: der Container ist bei jedem Start leer. Ohne dieses Skript fehlen
# ffmpeg, vosk, PIL, numpy und die Google-Bibliothek — die Pipeline-Skripte
# sind zwar da, koennen aber nicht laufen. Das fuehlt sich an, als waere
# "alles kaputt". Ist es nicht: es ist nur nichts installiert.
#
# Das Skript muss mit 0 enden, sonst startet die Sitzung gar nicht.
# Deshalb steht hinter jedem Installationsschritt ein "|| true".

set -uo pipefail

PROJEKT="${CLAUDE_PROJECT_DIR:-/workspace/twitchclipz}"

# ---------------------------------------------------------------- Pakete
export DEBIAN_FRONTEND=noninteractive

if ! command -v ffmpeg >/dev/null 2>&1; then
  apt-get update -qq >/dev/null 2>&1 || true
  apt-get install -y -qq --no-install-recommends \
    ffmpeg imagemagick fonts-roboto >/dev/null 2>&1 || true
fi

# --only-binary ist Pflicht: vosk hat keine baubare Quelldistribution und
# reisst beim Bauen den ganzen Aufruf mit. Jedes Paket einzeln, damit ein
# Ausfall nicht die uebrigen verhindert.
for paket in vosk pillow numpy \
             google-api-python-client google-auth-oauthlib google-auth-httplib2
do
  python3 -m pip install --quiet --disable-pip-version-check \
    --only-binary=:all: "$paket" >/dev/null 2>&1 || true
done

# ---------------------------------------------------- Vosk-Sprachmodell
# alphacephei.com ist gesperrt. Der Spiegel kercre123/vosk-models geht nur
# ueber raw.githubusercontent.com (steht auf der Trusted-Liste) — NICHT ueber
# github.com/.../raw/..., denn das laeuft in den GitHub-Proxy, und der laesst
# nur Repos durch, die dieser Sitzung angehaengt sind. Gemessen: 403 gegen
# github.com, 200 und 46 MB gegen raw.githubusercontent.com.
# Bevorzugt /opt: dorthin legt es das Setup-Skript der Umgebung, und von
# dort wird es im Abbild zwischengespeichert — also nur einmal geholt statt
# bei jedem Start. Liegt es nicht da, holt der Hook es selbst ins Projekt.
if [ -d "/opt/vosk-model-small-de-0.15" ]; then
  MODELL="/opt/vosk-model-small-de-0.15"
else
  MODELL="$PROJEKT/vosk-model-small-de-0.15"
  if [ ! -d "$MODELL" ]; then
    (
      cd "$PROJEKT" || exit 0
      curl -sSL --max-time 300 -o vosk.zip \
        "https://raw.githubusercontent.com/kercre123/vosk-models/main/vosk-model-small-de-0.15.zip" \
        && python3 -c "import zipfile;zipfile.ZipFile('vosk.zip').extractall('.')" \
        && rm -f vosk.zip
    ) >/dev/null 2>&1 || true
  fi
fi

# ------------------------------------------------------------- ImageMagick
# Die Standard-Richtlinie verbietet das Schreiben mancher Formate. Fuer die
# Cover brauchen wir PNG und JPEG ohne Einschraenkung.
POLICY="/etc/ImageMagick-6/policy.xml"
if [ -f "$POLICY" ]; then
  sed -i 's/rights="none" pattern="\(PNG\|JPEG\|PDF\)"/rights="read|write" pattern="\1"/g' \
    "$POLICY" 2>/dev/null || true
fi

# -------------------------------------------------------------- Umgebung
echo 'export PYTHONUNBUFFERED=1' >> "${CLAUDE_ENV_FILE:-/dev/null}" 2>/dev/null || true
echo "export VOSK_MODEL=$MODELL" >> "${CLAUDE_ENV_FILE:-/dev/null}" 2>/dev/null || true

# -------------------------------------------- Zusatz-Werkzeuge (Hintergrund)
# pytrends/rembg/realesrgan/manim/piper einmal je Container installieren.
# Laeuft DETACHT im Hintergrund und schreibt NUR ins Log -> 0 Token im Kontext.
# Marker $HOME/.nb_tools_ready verhindert Mehrfach-Installation.
if [ ! -f "$HOME/.nb_tools_ready" ] && [ -f "$PROJEKT/tools/setup-tools.sh" ]; then
  nohup bash "$PROJEKT/tools/setup-tools.sh" >/dev/null 2>&1 &
fi

# ------------------------------------------------- Taeglicher Messpunkt
# Laeuft DETACHT im Hintergrund und schreibt nur in eine Datei -> 0 Token.
#
# Warum automatisch und nicht als Erinnerung: Der Snapshot war als Pflicht
# in der Pflichtliste notiert und lief trotzdem nur dreimal (26., 27., 29.08.).
# Dadurch sind V5 Lengede und V6 Nutty Putty -- 20 Videos -- dauerhaft
# unbewertbar geworden. Das ist der einzige Schaden aus dem Befund vom
# 07.09., der sich NICHT nachtraeglich reparieren laesst. Eine Regel, die
# taeglich ausgefuehrt werden muss, darf nicht an Disziplin haengen.
HEUTE="$(date +%F)"
SNAP="$PROJEKT/YouTube-Knowledge/07-Analytics/snapshots/$HEUTE.json"
if [ ! -f "$SNAP" ]; then
  nohup python3 "$PROJEKT/tools/kp_metrik.py" --snapshot \
    > "$PROJEKT/.claude/messpunkt.log" 2>&1 &
fi

# ---------------------------------------------------------------- Bericht
# Alles ab hier landet im Sitzungskontext. Claude sieht damit sofort, was
# geht und was nicht, statt es erst im Fehlerfall zu merken.
python3 "$PROJEKT/.claude/hooks/statusbericht.py" 2>/dev/null || \
  echo "Statusbericht nicht ausfuehrbar — .claude/hooks/statusbericht.py fehlt."

# ------------------------------------------------- Der naechste Schritt
# Der Ablauf wird aus dem tatsaechlichen Zustand abgeleitet, nicht aus einer
# Notiz. Damit steht in jedem frischen Container von selbst da, was zu tun
# ist -- der Nutzer muss nichts mehr ansprechen.
timeout 240 python3 "$PROJEKT/tools/kp.py" status 2>/dev/null || \
  echo "Ablauf-Status nicht ermittelbar — python3 tools/kp.py status"

exit 0
