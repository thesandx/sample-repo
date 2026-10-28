#!/usr/bin/env python3
"""Fetch the real sticker/emoji assets the punch template uses (free, licensed for commercial use).

Usage: python3 fetch_assets.py templates/punch
Writes into that folder:
  lottie.min.js            lottie-web 5.12.2 from cdnjs (MIT)
  lot.js                   window.LOT = {name: <Noto animated emoji Lottie JSON>}  (Google Noto animated emoji, CC BY 4.0: credit 'Noto Emoji by Google' if asked)
  st/<name>.png            Microsoft Fluent 3D emoji PNGs (MIT) for static stickers
Add names to the tables below as reels need them. Sandeep wants assets sourced like a human
editor would (real stickers from the web), not drawn in code.
"""
import json, os, sys, urllib.parse, urllib.request

out = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(os.path.join(out, "st"), exist_ok=True)
get = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read()

# name -> Noto emoji codepoint (animated Lottie). Browse: https://googlefonts.github.io/noto-emoji-animation/
NOTO = {"hand": "270b", "money": "1f4b8", "trash": "1f5d1_fe0f", "eyes": "1f440", "sparkle": "2728",
        "love": "1f970", "shock": "1f631", "fire": "1f525", "party": "1f389", "heart_eyes": "1f60d",
        "cry": "1f62d", "ring": "1f48d", "clock": "23f0", "point_down": "1f447", "check": "2705"}
# name -> Fluent emoji folder / file stem (static 3D PNG, transparent)
FLUENT = {"phone": ("Mobile phone", "mobile_phone"), "cursor": ("Backhand index pointing up", "backhand_index_pointing_up"),
          "up": ("Up arrow", "up_arrow"), "gift": ("Wrapped gift", "wrapped_gift"), "pin": ("Round pushpin", "round_pushpin"),
          "calendar": ("Calendar", "calendar"), "ring": ("Ring", "ring"), "money": ("Money with wings", "money_with_wings"),
          "point": ("Index pointing at the viewer", "index_pointing_at_the_viewer"), "music": ("Musical notes", "musical_notes")}

open(os.path.join(out, "lottie.min.js"), "wb").write(get("https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.12.2/lottie.min.js"))
lot = {}
for n, cp in NOTO.items():
    try:
        lot[n] = json.loads(get(f"https://fonts.gstatic.com/s/e/notoemoji/latest/{cp}/lottie.json")); print("noto", n)
    except Exception as e:
        print("noto FAIL", n, cp, e)
open(os.path.join(out, "lot.js"), "w").write("window.LOT=" + json.dumps(lot) + ";")
for n, (folder, stem) in FLUENT.items():
    # hand/people emoji have skin-tone subfolders: <folder>/Default/3D/<stem>_3d_default.png
    base = f"https://cdn.jsdelivr.net/gh/microsoft/fluentui-emoji@main/assets/{urllib.parse.quote(folder)}"
    urls = [f"{base}/3D/{stem}_3d.png", f"{base}/Default/3D/{stem}_3d_default.png"]
    for u in urls:
        try:
            open(os.path.join(out, "st", n + ".png"), "wb").write(get(u)); print("fluent", n); break
        except Exception as e:
            err = e
    else:
        print("fluent FAIL", n, err)
