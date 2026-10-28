#!/usr/bin/env python3
"""Word-level timings for Hinglish speech (free, local, faster-whisper 'small' on CPU).

Usage: python3 whisper_words.py c1.mp4 c2.mp4 ...   -> words.json {"c1": [[start, end, "word"], ...]}

Why PCM via numpy: the PyAV version that faster-whisper pulls in clashed with the container's
ffmpeg, so decode with the ffmpeg CLI to 16 kHz mono s16 and pass a float array instead.
Whisper often spells Hindi words oddly; fix the caption text by hand, keep its timings.
"""
import json, subprocess, sys, os
import numpy as np
from faster_whisper import WhisperModel

m = WhisperModel("small", device="cpu", compute_type="int8")
res = {}
for f in sys.argv[1:]:
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    audio = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768
    segs, _ = m.transcribe(audio, language="hi", word_timestamps=True,
                           initial_prompt="Hinglish in Roman script.")
    k = os.path.splitext(os.path.basename(f))[0]
    res[k] = [(round(w.start, 2), round(w.end, 2), w.word.strip()) for s in segs for w in s.words]
    print(k, " ".join(w[2] for w in res[k]))
json.dump(res, open("words.json", "w"), ensure_ascii=False, indent=1)
