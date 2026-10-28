#!/usr/bin/env python3
"""Generate talking-character clips on OpenRouter (image-to-video), poll, download.

PAID. Every run costs Sandeep money. Before running:
  1. Tell Sandeep in the thread: what clip(s), which model, seconds, estimated cost in $ and ₹.
  2. Wait for his explicit "yes" in the thread. A yes covers only that ask.
  3. Run with --approved.

Key: read from env OPENROUTER_KEY (or OPENROUTER_API_KEY). If it is missing, STOP and
ask Sandeep for it. Never write the key to a file, a log, a commit or a message.

Usage:
  python3 openrouter_video.py estimate jobs.json            # print cost, no network
  python3 openrouter_video.py submit jobs.json --approved   # submit all pending jobs
  python3 openrouter_video.py poll jobs.json                # poll + download finished clips (polling is free)

jobs.json:
{
  "first_frame": "priya916.jpg",            # 9:16 image of the character (first frame)
  "model": "x-ai/grok-imagine-video-1.5-lite",
  "resolution": "720p",
  "base": "Vertical selfie video ... She says in Hindi: ",
  "clips": {"c1": {"duration": 6, "prompt": "acting direction + line"}}
}
State (job ids, status, file) is written back into jobs.json under "state".
"""
import base64, json, os, sys, time, urllib.request, mimetypes

API = "https://openrouter.ai/api/v1"
# USD per second at 720p, as seen Oct 2026. Re-check https://openrouter.ai/models before quoting.
PRICE_PER_SEC = {
    "x-ai/grok-imagine-video-1.5-lite": 0.19 / 6,   # ~$0.19 per 6s clip (~₹16). DEFAULT.
    # The two below were tested/quoted in Oct 2026 but their exact slugs were not saved:
    # look them up on openrouter.ai/models before use.
    "bytedance/seedance-2.0-mini": 0.38 / 6,        # ~2x Grok Lite, Priya's face drifts. Avoid.
    "bytedance/seedance-2.5": 1.40 / 6,             # ~₹117 per 6s at 720p. Sandeep declined it.
}
INR_PER_USD = 84


def key():
    k = os.environ.get("OPENROUTER_KEY") or os.environ.get("OPENROUTER_API_KEY")
    if not k:
        sys.exit("No OPENROUTER_KEY in env. Ask Sandeep for the key in the thread (do not guess, do not search for it).")
    return k


def req(url, data=None):
    h = {"Authorization": "Bearer " + key()}
    if data is not None:
        h["Content-Type"] = "application/json"
        data = json.dumps(data).encode()
    return urllib.request.urlopen(urllib.request.Request(url, data=data, headers=h), timeout=120)


def estimate(cfg):
    p = PRICE_PER_SEC.get(cfg["model"])
    secs = sum(c["duration"] for k, c in cfg["clips"].items() if k not in cfg.get("state", {}))
    if p is None:
        print(f"unknown price for {cfg['model']}: check openrouter.ai/models first"); return
    usd = secs * p
    print(f"{len(cfg['clips'])} clip(s), {secs}s on {cfg['model']}: ~${usd:.2f} (~₹{usd*INR_PER_USD:.0f})")


def submit(cfg, path):
    if "--approved" not in sys.argv:
        sys.exit("Refusing: add --approved only after Sandeep said yes to this exact spend in the thread.")
    key()  # fail early (and ask Sandeep) if the key is missing
    ff = cfg["first_frame"]
    mime = mimetypes.guess_type(ff)[0] or "image/jpeg"
    img = f"data:{mime};base64," + base64.b64encode(open(ff, "rb").read()).decode()
    st = cfg.setdefault("state", {})
    for k, c in cfg["clips"].items():
        if k in st:
            continue
        body = dict(model=cfg["model"], duration=c["duration"], resolution=cfg.get("resolution", "720p"),
                    aspect_ratio="9:16", generate_audio=True, prompt=cfg["base"] + c["prompt"],
                    frame_images=[{"type": "image_url", "image_url": {"url": img}, "frame_type": "first_frame"}])
        j = json.load(req(f"{API}/videos", body))
        st[k] = {"id": j["id"], "polling_url": j.get("polling_url") or f"{API}/videos/{j['id']}", "status": j["status"]}
        print(k, j["status"])
        json.dump(cfg, open(path, "w"), indent=1)


def poll(cfg, path):
    st = cfg.get("state", {})
    while True:
        pending = 0
        for k, s in st.items():
            if s["status"] in ("completed", "failed", "cancelled", "expired"):
                continue
            j = json.load(req(s["polling_url"]))
            s["status"] = j["status"]
            if j["status"] == "completed":
                # unsigned_urls need the Authorization header; index defaults to 0
                url = (j.get("unsigned_urls") or [f"{API}/videos/{s['id']}/content?index=0"])[0]
                out = f"{k}.mp4"
                open(out, "wb").write(req(url).read())
                s["file"] = out
                s["cost"] = (j.get("usage") or {}).get("cost")
                print(k, "saved", out, "cost", s["cost"])
            elif j["status"] == "failed":
                print(k, "FAILED", j.get("error"))
            else:
                pending += 1
        json.dump(cfg, open(path, "w"), indent=1)
        if not pending:
            break
        time.sleep(30)


if __name__ == "__main__":
    cmd, path = sys.argv[1], sys.argv[2]
    cfg = json.load(open(path))
    {"estimate": lambda: estimate(cfg), "submit": lambda: submit(cfg, path), "poll": lambda: poll(cfg, path)}[cmd]()
