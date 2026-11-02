#!/usr/bin/env bash
# Usage: bash build.sh details.json out.mp4 [music.mp3]   (free, local: Playwright + ffmpeg)
# Stills first:  python3 make_data.py details.json > data.js && node ../../scripts/render_frames.js invite.html stills 3,14,26,33,51,72,82
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); DET=$(realpath "$1"); OUT=$(realpath -m "$2"); MUSIC=${3:-}
cd "$HERE"
python3 make_data.py "$DET" > data.js
DUR=$(python3 -c "import re;print(re.search(r'\"duration\": ([0-9.]+)',open('data.js').read()).group(1))")
FR=$(mktemp -d)
node ../../scripts/render_frames.js invite.html "$FR" "$DUR"
# light paper grain so the flat cream doesn't look synthetic
ffmpeg -v error -y -framerate 30 -i "$FR/%05d.jpg" -vf "noise=alls=4:allf=t,format=yuv420p" -c:v libx264 -crf 26 -preset slow -tune grain -movflags +faststart "$OUT.video.mp4"
if [ -n "$MUSIC" ]; then
  ffmpeg -v error -y -i "$OUT.video.mp4" -i "$MUSIC" -filter_complex "[1:a]atrim=0:$DUR,afade=t=in:d=0.5,afade=t=out:st=$(python3 -c "print($DUR-2)"):d=2,loudnorm=I=-14:TP=-1.5[a]" \
    -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest "$OUT"
  rm "$OUT.video.mp4"
else
  mv "$OUT.video.mp4" "$OUT"
fi
ffmpeg -v error -y -ss 14 -i "$OUT" -frames:v 1 -q:v 2 "${OUT%.mp4}-cover.jpg"
rm -rf "$FR"; echo "done: $OUT ($DUR s)"
