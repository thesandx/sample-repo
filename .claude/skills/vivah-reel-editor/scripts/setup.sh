#!/usr/bin/env bash
# One-time setup for a fresh cloud container (Ubuntu, Node 22, Python 3).
# Everything here is free and local. Nothing here calls OpenRouter.
# Usage: bash .claude/skills/vivah-reel-editor/scripts/setup.sh
set -euo pipefail

echo "== system tools"
for t in ffmpeg ffprobe node npx python3; do
  command -v "$t" >/dev/null || { echo "MISSING: $t (apt-get install -y ffmpeg / install Node 22)"; exit 1; }
done
ffmpeg -hide_banner -encoders 2>/dev/null | grep -q libvpx-vp9 || echo "WARN: ffmpeg has no libvpx-vp9 (needed to decode HyperFrames alpha .webm)"

echo "== python packages"
pip install -q faster-whisper opencv-python-headless numpy pillow scipy yt-dlp 2>&1 | grep -v "Running pip as the 'root'" || true
# rembg is optional (older matte route used for v4). HyperFrames remove-background is preferred now.
# pip install -q "rembg[cpu]"

echo "== playwright (Chromium is pre-installed in Claude cloud containers; do NOT run 'playwright install')"
node -e "require('playwright');console.log('playwright ok')" 2>/dev/null || npm i -g playwright@1 >/dev/null

echo "== HyperFrames CLI (Apache 2.0, free, local)"
npx --yes "hyperframes@${HF_VER:-0.8.213}" --version 2>&1 | grep -v "npm notice" | tail -1

echo "== whisper model warm-up (downloads ~460MB 'small' model once)"
python3 - <<'PY'
from faster_whisper import WhisperModel
WhisperModel('small', device='cpu', compute_type='int8'); print('faster-whisper small ready')
PY

echo "== reachability of asset hosts"
for u in \
  "https://fonts.gstatic.com/s/e/notoemoji/latest/1f525/lottie.json" \
  "https://cdn.jsdelivr.net/gh/microsoft/fluentui-emoji@main/assets/Fire/3D/fire_3d.png" \
  "https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.12.2/lottie.min.js" \
  "https://fonts.googleapis.com/css2?family=Huninn" \
  "https://priya-rahul.vivah.online/Neha" ; do
  printf "%-90s %s\n" "$u" "$(curl -s -o /dev/null -w '%{http_code}' --max-time 15 "$u")"
done

echo "== OpenRouter key"
if [ -n "${OPENROUTER_KEY:-${OPENROUTER_API_KEY:-}}" ]; then
  echo "key present in env (never print it, never commit it)"
else
  echo "NO KEY: ask Sandeep for the OpenRouter key before any paid generation. Free work can continue."
fi
echo "setup done"
