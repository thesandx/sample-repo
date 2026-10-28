# Generating character clips with OpenRouter (PAID)

## The permission rule (Sandeep, 26 Oct 2026)
Every OpenRouter call costs money and the budget is tight. **Before each call** post in the thread:
> Can I spend about ₹16 ($0.19) on OpenRouter? That's one 6 s Grok Imagine Lite clip of Priya
> saying "…", for the hook of the X reel.

Wait for his explicit yes. A yes covers that ask only. This includes small calls (image edits,
transcription through an LLM, re-tries of a failed clip). Report actual spend afterwards
("this clip cost ₹14"). For reference: ~₹310 was spent on 26 Oct before the rule existed;
since then spends were ₹14–₹85 per approved ask.

## The key
Read from `OPENROUTER_KEY` (scripts also accept `OPENROUTER_API_KEY`). If unset: ask Sandeep to
provide it (e.g. as an environment secret in the cloud environment settings: see
`read_documentation` topic `environment.secrets`). Never echo it, write it to files, commit it,
or paste it into artifacts. Free work (editing, recording, matting) never needs it.

## Models (Oct 2026)

| Use | Model | Price | Notes |
|---|---|---|---|
| Talking clip, image→video **(default)** | `x-ai/grok-imagine-video-1.5-lite` | ~$0.19 per 6 s at 720p (~₹16) | keeps Priya's face, Hindi lip-sync with generated audio, 9:16. Durations 4–7 s used |
| alternative | Seedance 2.0 mini | ~2x Grok Lite | works, but Priya's face drifts |
| premium | Seedance 2.5 | ~₹117 per 6 s 720p | Sandeep chose to stay on Grok Lite |
| refused | Google Veo 3.1 (and Google Flow) | | blocks Priya's photo as a "real person" |
| First-frame image edit | `google/gemini-nano-banana-2.1` via `/api/v1/chat/completions` with `modalities:["image","text"]`, `image_config.aspect_ratio:"9:16"` | ~$0.04 (~₹3) | green-screen Priya, vanity scene, new poses |

Check current prices/slugs on openrouter.ai/models before quoting; these are what was seen.
Rough reel budget: 4–6 clips ≈ ₹65–100. A 20s hook-format reel needs one clip (~₹16).

## API (video)
- `POST https://openrouter.ai/api/v1/videos` with `model, prompt, duration, resolution:"720p",
  aspect_ratio:"9:16", generate_audio:true, frame_images:[{type:"image_url", image_url:{url:"data:image/jpeg;base64,..."}, frame_type:"first_frame"}]`
  → `202 {id, polling_url, status:"pending"}`.
- Poll `GET polling_url` (= `/api/v1/videos/{id}`) every ~30 s: `pending` → `in_progress` →
  `completed` | `failed` (also `cancelled`, `expired`). Polling is free.
- Download `unsigned_urls[0]` (= `/api/v1/videos/{id}/content?index=0`) **with the Authorization header**.
  `usage.cost` gives the real spend.
- `scripts/openrouter_video.py estimate|submit --approved|poll jobs.json` wraps all of this and keeps
  job ids in `jobs.json` so a crashed session can resume polling without paying again.

## First frames
- Crop the character portrait to 9:16 (720x1280 or 1080x1920) and use it as `first_frame`. Free.
- For a cut-out-friendly clip, first make a green-screen frame with the image-edit model
  ("keep the exact same woman… plain flat #00FF00 green background, waist-up, centred, even light").
- For listicle effects you need a **medium shot**: seated, waist-up, headroom, wall visible, static camera.

## Prompts that worked
Base (RUKO reel, 26 Oct):
```
Vertical selfie video, handheld phone camera, realistic Instagram UGC style. The same young Indian
woman from the image, blush pink chikankari kurta, talks straight into the camera in Hindi with clear
natural lip movement and expressive face. Natural daylight, soft blurred background. Audio: only her
voice, no music. <acting direction>, and says: "<line>"
```
Better, emotional hook (20s ad v4, the take Sandeep approved):
```
Realistic vertical smartphone selfie video, filmed on the front camera of an iPhone held at arm's
length, natural hand shake that gets stronger when she reacts. The same young Indian woman from the
image: long dark hair, small maroon bindi, pearl drop earrings, blush pink chikankari kurta. Real skin
texture, no beauty filter, natural daylight, background softly out of focus. She is NOT reading a
script: she is a real, expressive Delhi girl ranting to her best friend on an Instagram story, big
genuine emotions, lively face, expressive eyebrows, lips and jaw in exact sync with the words.
<act: e.g. shocked face, eyebrows up on "paper pe?", head thrown back, palm on forehead on a long
"kyuuuu", then snaps forward, points at the camera, cheeky smile>
Voice: a real 24-year-old Delhi woman, everyday Hinglish, native Hindi accent, highly expressive and
dramatic, pitch rises and falls, stretched vowels, playful exasperation, recorded on a phone mic. No
announcer tone, no flat reading, no music. She says in Hindi: "शादी का कार्ड... अभी भी पेपर पे?! लेकिन क्यूँ...?? बस विवाह डॉट ऑनलाइन पे जाओ!"
```
Lessons:
- Write the spoken line in **Devanagari**, numbers and brand as words ("विवाह डॉट ऑनलाइन",
  "सात सौ निन्यानवे"), otherwise the accent turns anglicised. "NEW30" is read "new thirty".
- Put the acting beat-by-beat in the prompt; flat prompts give flat reads.
- Generate 2 takes of a hook only if Sandeep approves the double cost; pick the livelier one.
- The AI voice still sounds synthetic to Sandeep. Best fix: a real woman's voice recording swapped
  in (stretch each line to the lip movement), or ElevenLabs Voice Changer (Starter plan for
  commercial use). You cannot listen to audio: say so and ask him to judge accents.
- Gemini/Flow outputs can carry a ✦ watermark (bottom right); inpaint it (`cv2.inpaint` with a mask).
