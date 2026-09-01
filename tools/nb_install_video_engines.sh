#!/usr/bin/env bash
# nb_install_video_engines.sh — installiert die Abhängigkeiten der vendorten
# Video-Engines ON DEMAND (node_modules/.venv sind bewusst NICHT im Repo).
#
# Neuer Container klont `main` → Code + Rezepte + Templates sind da, aber die
# schweren deps fehlen. Dieses Skript holt sie idempotent nach. Nur ausführen,
# wenn eine Engine wirklich gebraucht wird (Remotion-Render, video-use-Schnitt).
#
#   bash tools/nb_install_video_engines.sh [all|video-use|shotcraft|openmontage|watch]
#
# Standard = "core": nur die leichten, gratis Python-Bits (video-use + faster-whisper),
# damit Transkription/Schnitt sofort laufen. Node/Remotion nur bei Bedarf.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
TARGET="${1:-core}"

# Remotion soll NICHT sein eigenes Chromium ziehen — vorinstalliertes nutzen.
export PUPPETEER_SKIP_DOWNLOAD=1
export PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1

pip_install() { python3 -m pip install --quiet --disable-pip-version-check "$@"; }

install_core() {
  echo "== core: Gratis-Python (video-use-Schnitt + faster-whisper) =="
  # faster-whisper ist bereits da (hoeren.py). Ergänze nur, was den Helfern fehlt.
  pip_install librosa matplotlib pillow numpy requests \
    && echo "  ok: librosa/matplotlib/pillow/numpy/requests" \
    || echo "  WARN: pip core teils fehlgeschlagen"
}

install_video_use() {
  install_core
  echo "== video-use: optionale Manim-Slots =="
  python3 -c "import manim" 2>/dev/null && echo "  manim ok" || echo "  (manim optional — bei Bedarf: pip install manim)"
  echo "  Transkription GRATIS via helpers/transcribe_local.py (kein ElevenLabs-Key nötig)."
}

install_node_project() {  # $1 = dir, $2 = label
  local dir="$1" label="$2"
  if ! command -v npm >/dev/null 2>&1; then echo "  FEHLER: npm fehlt"; return 1; fi
  echo "== $label: npm install in $dir =="
  ( cd "$dir" && npm install --no-audit --no-fund 2>&1 | tail -4 ) \
    && echo "  ok: $label node_modules" || echo "  WARN: npm install $label fehlgeschlagen"
  echo "  Hinweis: Remotion bringt seine eigene chrome-headless-shell mit (via npm)."
  echo "           Render OHNE --browser-executable aufrufen. Das vorinstallierte"
  echo "           /opt/pw-browsers-Chrome NICHT übergeben (lehnt old-headless ab)."
  echo "           Getestet: npx remotion render src/index.ts <Comp> out.mp4 --concurrency=1"
}

install_shotcraft() {
  install_node_project ".claude/skills/video-shotcraft/template" "video-shotcraft"
}

install_openmontage() {
  echo "== OpenMontage: Python (nur GRATIS-Kern, keine Cloud/GPU) =="
  pip_install pyyaml pydantic jsonschema python-dotenv pillow numpy requests fastapi uvicorn watchfiles \
    && echo "  ok: openmontage core-python" || echo "  WARN: openmontage pip teils fehlgeschlagen"
  echo "  (Cloud-APIs google-genai/openai NICHT installiert — kostenpflichtig, nur auf Anfrage.)"
  install_node_project "tools/vendor/OpenMontage/remotion-composer" "OpenMontage-Remotion"
}

install_watch() {
  echo "== watch: yt-dlp + ffmpeg (ansehen/transkribieren) =="
  command -v yt-dlp >/dev/null 2>&1 && echo "  yt-dlp ok" || pip_install yt-dlp
  command -v ffmpeg >/dev/null 2>&1 && echo "  ffmpeg ok" || echo "  FEHLER: ffmpeg fehlt"
  echo "  Transkript gratis über Video-Captions bzw. faster-whisper (kein API-Key)."
}

case "$TARGET" in
  core)        install_core ;;
  video-use)   install_video_use ;;
  shotcraft)   install_shotcraft ;;
  openmontage) install_openmontage ;;
  watch)       install_watch ;;
  all)         install_video_use; install_shotcraft; install_openmontage; install_watch ;;
  *) echo "Unbekannt: $TARGET"; echo "Nutze: core|video-use|shotcraft|openmontage|watch|all"; exit 2 ;;
esac
echo "== fertig ($TARGET) =="
