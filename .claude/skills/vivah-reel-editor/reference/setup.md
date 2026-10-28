# Environment setup

Target: a Claude Code cloud container (Ubuntu, Node 22, Python 3, Java 21, Chromium + Playwright
preinstalled). Run `bash scripts/setup.sh` once per container. Everything below is free.

## Toolchain

| Tool | Why | Install / notes |
|---|---|---|
| ffmpeg / ffprobe | cut, scale, key, overlay, concat, encode, audio mix | preinstalled. Needs `libvpx-vp9` to *decode* alpha webm |
| Playwright (Chromium) | render HTML edit layers frame-by-frame; record the real site | preinstalled. **Never run `playwright install`** (another version won't find the browser). If a project pins its own Playwright, launch with `executablePath: '/opt/pw-browsers/chromium'`. For HD CDP screencasts add launch arg `--force-device-scale-factor=3` (see site-recording.md) |
| HyperFrames CLI | `remove-background` person matte (free, local, onnxruntime on CPU); catalog of GSAP animations | `npx --yes hyperframes@0.8.213 ...`. **Pin the version**: unpinned `npx hyperframes` once failed with `notarget` because the npm mirror lagged a fresh release. First matte run installs onnxruntime-node (~30 s). Speed ~1.5–2 fps on CPU |
| faster-whisper `small` | word timestamps for captions | `pip install faster-whisper`. Feed PCM through numpy (see `scripts/whisper_words.py`): its PyAV clashed with the system ffmpeg once. Model downloads from Hugging Face on first use (an "unauthenticated HF Hub" warning is harmless) |
| OpenCV (`opencv-python-headless`), numpy, Pillow, scipy | green-screen keying, quad tracking, compositing, procedural frames | pip |
| rembg (`u2net_human_seg`) | older matte route (v4 reel), ~1 frame/s | optional: `pip install "rembg[cpu]"` |
| yt-dlp | download public Instagram reference reels | pip. IG rate-limits anonymous downloads; a plain retry a few minutes later worked. Do not try to bypass IG bot checks |
| Java 21 + firebase-tools | Firestore emulator for the local vivah repo | `npx --yes firebase-tools@15.34.1` |
| pnpm | the vivah repo's package manager | preinstalled |

## Fonts

Loaded in the HTML layers from Google Fonts (`fonts.googleapis.com` is reachable):
- Brand: **Huninn** (English/Roman, wordmark), **Baloo 2** 600/800 (Devanagari).
- Punch-edit ransom letters: Anton, Archivo Black, Bungee, Abril Fatface, Rubik Mono One,
  Courier Prime 700, Poppins 600/800. Handwriting: Permanent Marker.
- Always `await document.fonts.ready` and wait ~1.5 s before the first screenshot
  (`render_frames.js` does this), and use `display=block` in the font URL so fallback fonts never
  get captured.
- Whisper writes Hindi in Devanagari even with a "Roman script" prompt. Keep its timings and
  type the Hinglish caption words yourself.

## Network: what works from the container (Oct 2026)

Works: fonts.googleapis.com / fonts.gstatic.com (incl. Noto animated emoji Lottie), cdn.jsdelivr.net
(Fluent emoji), cdnjs.cloudflare.com, images.rawpixel.com (CC0 PNGs), openrouter.ai,
vivah.online + subdomains, github.com (thesandx/vivah is public), npm, PyPI, Hugging Face,
paisaboltahai.rbi.org.in (official ₹500 note image).

Blocked or unreliable: Giphy, Pixabay, Pexels, Freepik (blocked: ask Sandeep to download and upload
from those), Wikimedia (HTTP 429), Openverse (timeouts), Instagram (rate-limits).

If a host is denied, read the environment network docs (`read_documentation` topic
`environment.network`) rather than guessing.

## Where things live

- `/mnt/project-files/` is the project's shared folder (survives threads). Finished reels:
  `/mnt/project-files/reels/*.mp4` + `-cover.jpg`. Sources: `/mnt/project-files/reels/source/<reel>/`.
  Logos: `/mnt/project-files/logo-*.png|svg`, `mark-*.png`. Sandeep's uploads:
  `/mnt/project-files/uploads/hearth/<id>` (no extension).
- `/mnt/project-files` is a network mount: don't `find` the whole tree, put a trailing slash on
  paths, re-read a shared file ~10 s after writing it.
- Work in a scratch dir, copy only deliverables and sources into project files.

## Encoding defaults

- Reels: 1080x1920, 30 fps (24 fps if the source footage is 24, e.g. Flow clips), H.264
  `-crf 16 -pix_fmt yuv420p`, AAC 48 kHz. Cover = a strong hook frame as jpg.
- Render video and audio in **separate ffmpeg passes**, then mux. A single pass with `apad`+`amix`
  hung once.
- `loudnorm` inside a multi-input mix truncates short clips (the voice dropped out in the 20s ad
  v2). Normalise each voice clip on its own first (`apad`, then `loudnorm`), then mix.
