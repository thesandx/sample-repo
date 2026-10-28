# Real product footage

Product screens in reels are always real recordings. Three sources, best first.

## 1. Live demo invite (prod), free
`https://priya-rahul.vivah.online/<GuestName>` (Priya & Rahul demo; any name works: `/Neha`, `/Riya`,
`/Ankit`, `/Simran`, `/Nani-ji`, `/Sharma-uncle`). Flow: Shri Ganesh gate "Hi <Name>" → tap → song →
scratch the gold foil (date: day/month and year canvases) → countdown → venue (Google Maps) →
Our Families → festivities/functions → RSVP.

```bash
node scripts/record_invite.js Neha fr      # iPhone 13 viewport @3x, CDP screencast -> fr/*.jpg + meta.json
python3 scripts/frames_to_mp4.py fr site.mp4   # constant 30 fps at real speed (1170 px wide)
```
- CDP `Page.startScreencast` gives real animations; ack every frame. **Launch Chromium with
  `--force-device-scale-factor=3`**: from Chromium 153 (Playwright 1.63) the screencast otherwise comes
  out at CSS size (390x664) even though screenshots are 1170 wide. With the flag: 1170x1992 (checked 28 Oct).
- Scratch = mouse down + zig-zag drags over each `<canvas>` (positions read from the DOM).
- Inject `*{user-select:none}` or drags highlight text.
- Smooth scroll with an eased `requestAnimationFrame` loop, not `mouse.wheel`.
- Marks (`[name, time]`) let you cut the recording to the script later.
- Retiming: build per-segment `trim,setpts=(PTS-STARTPTS)*k` chains so each feature appears when
  Priya mentions it (`examples/v2-demo/fc.txt`, `examples/hand-scroll/rt.txt`).
- Still screenshots of guest gates for name-cycling shots: same context, `page.screenshot()` per name.
- Static ad screens were captured at 390x844 @3x; OG image at `/api/og/priya-rahul`.

## 2. Local vivah repo: the create flow in HD, free
For "how I made it in 5 steps" footage without Sandeep's phone. Repo `github.com/thesandx/vivah`
(public, Next.js 16 + Firestore). Add it to the session (`add_repo`) or clone it.
1. `git clone --depth 1 https://github.com/thesandx/vivah ~/vivah && cd ~/vivah && pnpm install`
2. `cp .env.example .env.local`, set `GCP_PROJECT_ID=demo-vivah`, `APP_SLUG=vivah`,
   `FIRESTORE_EMULATOR_HOST=127.0.0.1:8085` (database id becomes `vivah-db`).
3. Emulator: write a `firebase.json` with `{"emulators":{"firestore":{"port":8085}}}` and run
   `npx --yes firebase-tools@15.34.1 emulators:start --only firestore --project demo-vivah --config firebase.json` (Java 21 is present).
4. Seed songs or step 5 ("Your song") won't appear: with `@google-cloud/firestore` write
   `siteContent/wedding-songs` with `slot1..slot4: {name, file:'song-N-x.mp3'}`.
5. `pnpm dev` → `http://localhost:3000`. Invites at `/site/<slug>/<Name>` (e.g. `/site/priya-rahul/Neha`).
6. "Make my website" creates a lead and goes to `/preview/<id>`; payment auto-succeeds locally with
   no keys; no WhatsApp is sent (no token).
7. Record with `examples/tutorial/create.js`: iPhone 13 @3x, hides the Next dev badge
   (init-script CSS `nextjs-portal{display:none}`), types names with `pressSequentially`, fills
   date, a dummy phone number, ticks functions, picks a song, makes the site, then plays the preview.
   Step timestamps → `cf_marks.json`. Output ~1170x1992.
   - Blur fields with `document.activeElement.blur()`, not by clicking the body (that hits the header link).
   - Warm up routes first: the dev server compiles a route on first hit and stalls the recording.
   - The local preview has placeholder venue/parents and a "PREVIEW 30:00" banner, so use the prod
     demo recording for the "result" part.

## 3. Sandeep's own phone recording (26 Oct), handle with care
`/mnt/project-files/reels/source/process/vivah-process-5-steps.mov`: 416x848, 60 fps, 89.7 s.
Low-res: show it small inside a phone/card frame, never full-width.
Map: 0–2 landing (₹799) · 2–11 step 1 names (Riya & Arjun) · 12–28 step 2 date + WhatsApp
number · 28–35 step 3 functions · 36–41 step 4 address · 42–48 step 5 song (audio ~46 s) ·
49–54 "Making…" checklist → ready · 55–85 preview (gate, scratch, countdown, venue, functions,
RSVP; music ~61–72 s) · 85–90 payment sheet, NEW30.
**PRIVACY: always crop or cover the keyboard area.** His full name shows in the keyboard suggestion
bar (~3–11 s) and real phone numbers show in the autofill bar and WhatsApp field (~18–27 s). The
tutorial reel covered the keyboard with a cream box and started step 2 at 13 s. Prefer source 2.

## Green-screen hand scrolling a phone (28 Oct)
Sandeep makes the hand footage himself (ChatGPT still, Google Flow clips) with a flat #00FF00 screen;
we key the real site into it:
- `examples/hand-scroll/track2.py`: per frame, find the green screen quad (smoothed corners) and the
  thumb tip (green pixels missing vs. a template).
- `plan.py`: thumb strokes → timed actions (tap, scratch drags, flick scrolls).
- `rec2.js`: replays those actions live on prod with a CDP screencast, so the real scratch reveal
  lines up with the thumb.
- `comp3.py`: OpenCV key with despill + edge halo fix, perspective-warp the site + browser chrome
  into the quad, inpaint the Flow ✦ watermark, 1.12x zoom, grain; café ambience +14 dB.
- He wants ONE hand scrolling with its own thumb; the first AI hand was rejected for wrong fingers.
