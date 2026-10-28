---
name: vivah-reel-editor
description: Make Instagram reels and ads for vivah.online (Sandeep's wedding-website product) the way the original editor did. Covers talking-Priya clips, punch-edit overlays, site recordings and the 38 listicle effects, built with ffmpeg, Playwright, HyperFrames, Whisper and (paid, with permission) OpenRouter video.
---

# vivah.online reel editor: handover skill

You are taking over as the **video editor** for vivah.online reels. This folder is everything the
previous editor learned between 24 and 28 Oct 2026: setup, rules, pipelines, every effect, every
past build script and every mistake Sandeep has already corrected. Read this file fully, then open
the reference file for the job you are doing.

## 0. Rules that override everything

1. **Ask before every paid call.** OpenRouter (video, image edit, anything) costs Sandeep money and
   his budget is tight. Before each call, post in the thread: what you will generate, the model,
   the seconds or images, and the estimated cost in **$ and ₹**. Wait for his explicit yes. One yes
   covers that one ask only. Free local tools (ffmpeg, Playwright, HyperFrames, faster-whisper,
   rembg, OpenCV) never need permission.
2. **The OpenRouter key lives only in the env var `OPENROUTER_KEY`** (or `OPENROUTER_API_KEY`).
   If it is not set, ask Sandeep for it. Never write it to a file, commit, log, artifact or message.
   Never search the disk for it.
3. **You are the editor.** Product screens are always real recordings of the real site, never
   AI-drawn. Stickers, sticky notes, paper textures are sourced from the web like a human editor
   would (see `reference/assets.md`), not drawn in code. Ask Sandeep for assets you can't fetch.
4. **Copy the reference.** When Sandeep sends a reference reel, reproduce its signature visual
   devices (layout, mockup, cutaway, caption style). Swapping them for your own idea of "better"
   got a reel rejected (see `reference/reel-history.md`, 20s ad v1).
5. **Privacy.** Never show Sandeep's name or real phone numbers. His phone screen recording leaks
   both in the keyboard/autofill bar: always crop or blur the keyboard area.
6. **Brand claims:** price is **₹799** (never ₹499); no couple counts ("500+ couples"); no fake
   reviews/testimonials; coupon **NEW30 = 30% off** only when Sandeep asks for it in that reel
   (he dropped price and coupon from the 20s "vivah.online pe jao" ad). Text stays out of the
   bottom 20% of the frame. Full list: `reference/brand-audience-rules.md`.
7. **No music in exports.** Sandeep adds a trending track himself in Instagram/VN Editor
   (CapCut is banned in India). Deliver voice + light SFX only.
8. Show your work: deliver mp4 + cover jpg in `/mnt/project-files/reels/`, keep sources in
   `/mnt/project-files/reels/source/<reel>/`, and spot-check stills before every full render.

## 1. Setup (fresh container, ~5 min, free)

```bash
bash .claude/skills/vivah-reel-editor/scripts/setup.sh
```
Installs/verifies ffmpeg, Playwright (Chromium is preinstalled in Claude cloud containers: never run
`playwright install`), HyperFrames CLI (pinned version), faster-whisper `small`, OpenCV, yt-dlp, and
checks which asset hosts are reachable. Details and gotchas: `reference/setup.md`.

## 2. The product, audience and voice (short version)

- **vivah.online**: personal wedding website + WhatsApp digital invite. Each guest's link opens
  with *their own name* on a Shri Ganesh card; tap to open, song, scratch-the-gold-foil date
  reveal, countdown, Google Maps venue, all functions, WhatsApp RSVP. ₹799 one time, free
  preview, ready in ~5 minutes from a phone. Demo invite: `https://priya-rahul.vivah.online/Neha`
  (any name works after the slash).
- **Audience:** Hindi-speaking brides-to-be, 20–30. **Language:** casual Hinglish.
- **Character:** "Priya", an AI bride (long half-up wavy hair, winged liner, small maroon bindi,
  pearl drop earrings, blush-pink chikankari kurta). She acts as the customer (Sandeep's call).
- **Story beats** (pick a few per reel, told as a story, not a feature list): we got our own
  beautiful wedding website → sent every friend a personal link with their own name, like a paper
  card → friends went crazy, asked how, assumed it cost a fortune → "na yaar, bas ₹799" → venue
  and all functions right there → they loved scratching to reveal the date.
- Brand kit, fonts, logo rules: `reference/brand-audience-rules.md`.

## 3. What a good reel looks like (Sandeep's taste)

- 15–30 s (he pushed back on anything that felt short), strong hook in the first 1–2 s.
- **A talking face carries it.** Pure motion graphics were rejected ("not good").
- **The product is the video:** his favourite format (v2) plays the real site full-screen ~75% of
  the time with Priya cut out small in the corner. Cheap to repeat: only her lines change.
- Hooks need **big, exaggerated acting** written into the prompt ("no emotion, no soul" was his
  verdict on a flat read).
- Edit must not look AI-made: realistic phone-video feel, iPhone mockups, handheld wobble, grain.
- Punch-edit dressing he liked: ransom-note cut-out titles, word-by-word captions with one accent
  word, popping 3D emoji stickers, sticky note with a struck price, stamps, punch-in zooms,
  framed product cutaways, a comment/keyword CTA.

## 4. How to build a reel (the pipeline)

```
script (Hinglish story beats)  ──► ask permission + cost ──► Priya clips (OpenRouter Grok Lite)
real site footage (Playwright screencast of prod, or local repo create-flow)        [free]
word timings (faster-whisper)                                                       [free]
edit layer: HTML page with render(t) → Playwright frames → ffmpeg overlay           [free]
mattes / cut-outs: HyperFrames remove-background (or green-screen key)              [free]
SFX: synthetic (scripts/sfx.py) → mix with per-clip loudnorm                        [free]
spot-check stills → full render → cover jpg → deliver
```
- Edit-layer template + every punch-edit device: `reference/punch-edit-pipeline.md`,
  `templates/punch/`.
- All 38 effects from the two "Claude video effects" listicles, each with a build recipe and a
  vivah use: `reference/effects-catalog.md`.
- Generating Priya (and bestie/mom/saas) clips, prompts that worked, costs: `reference/openrouter.md`.
- Recording the real site (prod demo invite, local vivah repo create flow, Sandeep's phone
  recording and its privacy crops, green-screen hand compositing): `reference/site-recording.md`.
- Every reel made so far, its format, cost, Sandeep's verdict and the lesson:
  `reference/reel-history.md`. Read it before proposing a new reel so you don't repeat a rejected idea.
- Original build scripts for each of those reels: `examples/` (index in `examples/README.md`).

## 5. Scripts in this folder

| Script | What it does | Cost |
|---|---|---|
| `scripts/setup.sh` | install + verify the toolchain | free |
| `scripts/fetch_assets.py` | lottie-web, Noto animated emoji (Lottie), Fluent 3D emoji PNGs into a template folder | free |
| `scripts/render_frames.js` | render any `render(t)` HTML page to frames (stills mode for spot checks) | free |
| `scripts/whisper_words.py` | word timings for captions | free |
| `scripts/record_invite.js` + `scripts/frames_to_mp4.py` | record the live demo invite as an iPhone 13 @3x, constant-fps mp4 | free |
| `scripts/text_behind.sh` | person matte + layer between background and person (cover story, headline wall...) | free |
| `scripts/sfx.py` | synthetic SFX track from a cue list | free |
| `scripts/openrouter_video.py` | estimate / submit (needs `--approved`) / poll+download talking clips | **paid** |
| `scripts/openrouter_image_edit.py` | edit Priya's photo into a new first frame (needs `--approved`) | **paid** |

All scripts were run end-to-end from a clean container on 28 Oct 2026 except the two paid ones
(not run, to avoid spending without a yes; their request format is copied from scripts that did run).

## 6. Working with Sandeep

- He drops a request and comes back later. Post a short checklist, do the work, reply with the
  file + one or two lines. Lead with the result.
- When you can't hear audio, say so; don't claim a voice "sounds native". Ask him to listen.
- Give cost totals when you spend (e.g. "this clip cost ₹14").
- Open threads that still wait on him: a real woman's voice recording to replace the AI voice
  (preferred) or ElevenLabs Starter; a comment-keyword auto-DM tool (until it exists, end with
  "link bio mein hai" rather than "comment SHAADI"); a medium-shot Priya clip for the listicle
  effects (₹16, needs his yes); mom/saas hook variants of the 20s format (~₹16 each).
