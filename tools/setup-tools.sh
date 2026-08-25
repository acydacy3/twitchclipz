#!/usr/bin/env bash
# Idempotente Installation ALLER Zusatz-Werkzeuge (kostenlos/GitHub).
# Laeuft im Container-Init (setup.sh) ODER im Session-Start-Hook im Hintergrund.
# WICHTIG: schreibt NUR in eine Logdatei, nie viel nach stdout (Token-Schonung).
set -uo pipefail
LOG="${1:-/home/user/twitchclipz/tools/setup-tools.log}"
REPORT="/home/user/twitchclipz/tools/tools-status.txt"
MARK="$HOME/.nb_tools_ready"
mkdir -p "$(dirname "$LOG")" "$HOME/.local/bin"
exec >>"$LOG" 2>&1
echo "=== setup-tools $(date -u +%FT%TZ) ==="
: > "$REPORT"
ok(){ echo "OK   $1" >> "$REPORT"; }
skip(){ echo "SKIP $1 ($2)" >> "$REPORT"; }

# 1) pytrends (Google Trends) — reines pip
if python3 -c "import pytrends" 2>/dev/null; then ok "pytrends"; else
  pip install -q --user pytrends && python3 -c "import pytrends" 2>/dev/null && ok "pytrends" || skip "pytrends" "pip-fail"
fi

# 2) rembg (Freistellen) + onnxruntime — pip, laedt Modell erst bei Nutzung
if python3 -c "import rembg" 2>/dev/null; then ok "rembg"; else
  pip install -q --user "rembg[cpu]" onnxruntime pillow 2>/dev/null && python3 -c "import rembg" 2>/dev/null && ok "rembg" || skip "rembg" "pip-fail"
fi

# 3) Real-ESRGAN (Upscale) — braucht torch CPU (gross, aber Disk reicht)
if python3 -c "import realesrgan" 2>/dev/null; then ok "realesrgan"; else
  pip install -q --user torch torchvision --index-url https://download.pytorch.org/whl/cpu 2>/dev/null
  pip install -q --user realesrgan basicsr 2>/dev/null && python3 -c "import realesrgan" 2>/dev/null && ok "realesrgan" || skip "realesrgan" "torch/basicsr-fail"
fi

# 4) Manim — System-Libs (cairo/pango) via apt, dann pip
if python3 -c "import manim" 2>/dev/null; then ok "manim"; else
  (apt-get update -qq && apt-get install -y -qq libcairo2-dev libpango1.0-dev pkg-config python3-dev ffmpeg) 2>/dev/null
  pip install -q --user manim 2>/dev/null && python3 -c "import manim" 2>/dev/null && ok "manim" || skip "manim" "cairo/pango-oder-pip-fail"
fi

# 5) Piper TTS (deutsche Scratch-VO) — Binary + Voice aus GitHub-Releases
PIPER_DIR="/home/user/twitchclipz/tools/piper"
if [ -x "$PIPER_DIR/piper/piper" ] && [ -f "$PIPER_DIR/de_DE-thorsten-medium.onnx" ]; then ok "piper"; else
  mkdir -p "$PIPER_DIR"
  curl -sL -o "$PIPER_DIR/piper.tgz" "https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_x86_64.tar.gz" && tar xzf "$PIPER_DIR/piper.tgz" -C "$PIPER_DIR" 2>/dev/null && rm -f "$PIPER_DIR/piper.tgz"
  V="https://huggingface.co/rhasspy/piper-voices/resolve/main/de/de_DE/thorsten/medium"
  curl -sL -o "$PIPER_DIR/de_DE-thorsten-medium.onnx" "$V/de_DE-thorsten-medium.onnx"
  curl -sL -o "$PIPER_DIR/de_DE-thorsten-medium.onnx.json" "$V/de_DE-thorsten-medium.onnx.json"
  if [ -x "$PIPER_DIR/piper/piper" ] && [ -s "$PIPER_DIR/de_DE-thorsten-medium.onnx" ]; then ok "piper"; else skip "piper" "download-fail"; fi
fi

# 6) Openverse / YouTube-Suggest: keine Installation (reine HTTP-Helfer) -> immer OK
ok "openverse (HTTP-Helfer nb_openverse.py)"
ok "youtube-suggest (HTTP-Helfer nb_suggest.py)"

echo "=== fertig $(date -u +%FT%TZ) ==="
touch "$MARK"
