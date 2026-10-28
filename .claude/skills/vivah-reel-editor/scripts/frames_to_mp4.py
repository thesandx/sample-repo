#!/usr/bin/env python3
"""Turn CDP screencast frames (irregular timestamps) into a constant 30 fps mp4.

Usage: python3 frames_to_mp4.py frameDir out.mp4 [fps]
Reads frameDir/meta.json {"frames":[ts,...]} written by record_invite.js / create-flow recorders.
Each output frame shows the latest captured frame at that time, so motion keeps its real speed.
"""
import json, os, subprocess, sys

d, out = sys.argv[1], sys.argv[2]
fps = float(sys.argv[3]) if len(sys.argv) > 3 else 30
ts = json.load(open(os.path.join(d, "meta.json")))["frames"]
t0 = ts[0]
lines = []
for i, t in enumerate(ts):
    nxt = ts[i + 1] if i + 1 < len(ts) else t + 1 / fps
    lines.append(f"file '{os.path.abspath(os.path.join(d, f'{i:05d}.jpg'))}'\nduration {max(0.001, nxt - t):.4f}\n")
lst = os.path.join(d, "concat.txt")
open(lst, "w").write("".join(lines))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
                "-vf", f"fps={fps},scale=trunc(iw/2)*2:trunc(ih/2)*2,format=yuv420p",
                "-c:v", "libx264", "-crf", "16", out], check=True)
print("wrote", out, f"{ts[-1]-t0:.1f}s")
