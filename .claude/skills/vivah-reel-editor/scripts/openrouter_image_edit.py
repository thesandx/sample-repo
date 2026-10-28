#!/usr/bin/env python3
"""Edit a character photo into a new first frame (green screen, vanity scene, medium shot...).

PAID (~$0.04 = ~₹3 per image in Oct 2026). Ask Sandeep first, state model + cost, wait for yes,
then run with --approved. Key from env OPENROUTER_KEY / OPENROUTER_API_KEY; if missing, ask Sandeep.

Usage:
  python3 openrouter_image_edit.py in.png "Edit this photo: keep the exact same woman ..." out_prefix --approved
Writes out_prefix0.png, out_prefix1.png ... and prints the reported cost.
"""
import base64, json, os, sys, urllib.request, mimetypes

if "--approved" not in sys.argv:
    sys.exit("Refusing: needs Sandeep's yes in the thread, then --approved.")
k = os.environ.get("OPENROUTER_KEY") or os.environ.get("OPENROUTER_API_KEY")
if not k:
    sys.exit("No OPENROUTER_KEY in env. Ask Sandeep for the key.")
src, text, prefix = sys.argv[1:4]
mime = mimetypes.guess_type(src)[0] or "image/png"
url = f"data:{mime};base64," + base64.b64encode(open(src, "rb").read()).decode()
body = {"model": "google/gemini-nano-banana-2.1", "modalities": ["image", "text"],
        "image_config": {"aspect_ratio": "9:16"},
        "messages": [{"role": "user", "content": [{"type": "text", "text": text},
                                                  {"type": "image_url", "image_url": {"url": url}}]}]}
r = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=json.dumps(body).encode(),
                           headers={"Authorization": "Bearer " + k, "Content-Type": "application/json"})
j = json.load(urllib.request.urlopen(r, timeout=180))
msg = j["choices"][0]["message"]
print((msg.get("content") or "")[:200], "cost:", j.get("usage", {}).get("cost"))
for i, im in enumerate(msg.get("images", [])):
    open(f"{prefix}{i}.png", "wb").write(base64.b64decode(im["image_url"]["url"].split(",", 1)[1]))
    print("saved", f"{prefix}{i}.png")
