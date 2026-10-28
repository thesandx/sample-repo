#!/usr/bin/env bash
# "Cover story" / text-behind-the-head effect (free, local). Also the base for frame break,
# headline wall, couch wall, gravity drop, paper cut: anything that sits BETWEEN background and person.
#
# Usage: bash text_behind.sh clip.mp4 layer.png out.mp4 [start] [dur]
#   layer.png: 1080x1920 transparent PNG (or a .mov/.webm with alpha) holding the text/cards.
#   Make it with render_frames.js --png from an HTML page, or with PIL.
#
# Stack (bottom -> top): original clip, layer, cut-out person.
# Use the ORIGINAL clip as the bottom layer: HyperFrames' --background-output plate is hole-cut
# (the person area is transparent, not inpainted), so it is only useful when you want to
# replace the background entirely.
# Speed: ~1.5-2 fps on CPU (2 s clip = ~70 s incl. first-run onnxruntime install).
# Needs footage with headroom (medium shot, wall behind); tight face close-ups leave no room.
# HyperFrames is pinned: npx "latest" once resolved to a version the npm mirror did not have yet (notarget).
set -euo pipefail
clip=$1; layer=$2; out=$3; ss=${4:-0}; dur=${5:-}
work=$(mktemp -d -p .)
ffmpeg -v error -y -ss "$ss" ${dur:+-t $dur} -i "$clip" -vf "scale=1080:1920:flags=lanczos,fps=30" \
  -c:v libx264 -crf 14 -c:a aac "$work/src.mp4"
npx --yes "hyperframes@${HF_VER:-0.8.213}" remove-background "$work/src.mp4" -o "$work/subj.webm" --quality best 2>&1 | grep -v "npm notice" | tail -2
loop=""; case "$layer" in *.png|*.jpg) loop="-loop 1";; esac
# -c:v libvpx-vp9 BEFORE -i is required, otherwise ffmpeg's native vp9 decoder drops the alpha channel
ffmpeg -v error -y -i "$work/src.mp4" $loop -i "$layer" -c:v libvpx-vp9 -i "$work/subj.webm" \
  -filter_complex "[1:v]scale=1080:1920,format=rgba[l];[0:v][l]overlay=0:0:shortest=1[a];[2:v]format=rgba[s];[a][s]overlay=0:0:shortest=1,format=yuv420p[v]" \
  -map "[v]" -map 0:a? -c:v libx264 -crf 16 -c:a copy "$out"
echo "wrote $out"; rm -rf "$work"
