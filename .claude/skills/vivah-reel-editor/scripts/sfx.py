#!/usr/bin/env python3
"""Synthetic sound effects track (free, no licensing questions). 48 kHz mono wav.

Usage: python3 sfx.py cues.json sfx.wav
cues.json: {"dur": 25, "room": true, "cues": [[0.0,"thump",0.8],[1.6,"whoosh",0.4],[2.7,"pop",0.4],
            [5.0,"pops",0.18],[15,"tick",0.25],[19.2,"chime",0.3],[3.1,"tap",0.3],[4.0,"keys",0.2,1.2]]}
Kinds: pop (sticker appears), pops (4 rising pops = title letters), tick (checklist), thump (hook/stamp),
whoosh (cut / slide), chime (price / end card), tap (screen tap), keys (typing burst; 4th value = seconds).
room=true adds room tone at about -50 dB so silences don't sound dead (used in the "realistic" ads).
Mix it under the voice at about -14 to -10 dB relative; Sandeep adds music himself in Instagram.
"""
import json, sys, wave
import numpy as np

SR = 48000
rng = np.random.default_rng(1)


def env(n, a, d):
    x = np.arange(n) / SR
    return np.minimum(1, x / a) * np.exp(-x / d)


def tone(f, dur, a=0.002, d=0.08, f2=None):
    n = int(dur * SR); ff = np.linspace(f, f2 or f, n)
    return np.sin(2 * np.pi * np.cumsum(ff) / SR) * env(n, a, d)


def whoosh(dur=0.35):
    n = int(dur * SR); w = rng.standard_normal(n)
    y = np.convolve(w, np.ones(12) / 12, "same") - np.convolve(w, np.ones(80) / 80, "same")
    return y * np.hanning(n) * 2.5


K = {
    "pop": lambda: tone(1200, 0.12, 0.001, 0.035, 1900),
    "tick": lambda: tone(1800, 0.15, 0.001, 0.05) + 0.6 * tone(2700, 0.15, 0.001, 0.04),
    "thump": lambda: tone(140, 0.35, 0.002, 0.09, 55),
    "whoosh": lambda: whoosh(0.3),
    "chime": lambda: sum(tone(f, 1.2, 0.003, 0.35) * (0.8 ** i) for i, f in enumerate((1047, 1319, 1568))),
    "tap": lambda: tone(2400, 0.05, 0.0005, 0.012) * 0.7 + rng.standard_normal(int(0.05 * SR)) * env(int(0.05 * SR), 0.0005, 0.006) * 0.3,
}

cfg = json.load(open(sys.argv[1]))
out = np.zeros(int(SR * cfg["dur"]))


def add(t, sig, g):
    i = int(t * SR); n = min(len(sig), len(out) - i)
    if n > 0: out[i:i + n] += sig[:n] * g


for c in cfg["cues"]:
    t, kind, g = c[0], c[1], c[2]
    if kind == "pops":
        for k in range(4): add(t + k * 0.045, tone(900 + k * 150, 0.12, 0.001, 0.035, (900 + k * 150) * 1.6), g)
    elif kind == "keys":
        dur = c[3] if len(c) > 3 else 1.0; x = t
        while x < t + dur:
            add(x, K["tap"](), g * (0.6 + 0.4 * rng.random())); x += 0.07 + 0.06 * rng.random()
    else:
        add(t, K[kind](), g)
out = out / (np.max(np.abs(out)) or 1) * 0.5
if cfg.get("room"):
    out += np.convolve(rng.standard_normal(len(out)), np.ones(40) / 40, "same") * 10 ** (-50 / 20) * 3
w = wave.open(sys.argv[2], "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
print("wrote", sys.argv[2])
