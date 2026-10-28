# Punch-edit pipeline (the edit layer)

Every reel so far was edited in code, not in an NLE:

1. **Base footage**: Priya clips (`c1.mp4`…), real site recordings, green-screen clips.
2. **Edit layer**: one HTML page, 1080x1920, with `window.render(t)` that puts every element in
   its state for time `t`. Deterministic (seeded random), so any frame can be rendered alone.
3. **Capture**: `scripts/render_frames.js page.html out 25` (Playwright, 30 fps). Render 4–6
   **stills first** (`... stills 0.5,6,13,19.5,24`), look at them, fix, then render all frames.
4. **Composite + encode** with ffmpeg, mix audio in a separate pass, mux.

Two ways to use the HTML layer:
- **Background inside the page** (punch template, RUKO reel): Priya's frames are `<img>` swapped per
  frame, or a still for tests. Simple; the screenshot is the final frame. Output jpg.
- **Transparent overlay** (v2, tutorial, 20s ads): page body transparent, `render_frames.js ... --png`
  (`omitBackground`), then `ffmpeg -i base.mp4 -framerate 30 -i ov/%05d.png -filter_complex overlay`.
  Better when the base is a long ffmpeg-built video (site recording + keyed Priya).

## The template: `templates/punch/punch.html`

Run `python3 scripts/fetch_assets.py templates/punch-copy` in a copy of the folder first (it pulls
`lottie.min.js`, `lot.js` with Noto animated emoji, Fluent 3D PNGs into `st/`). Then add:
`priya.png` (or per-frame bg), `src/f00001.jpg…` (site recording frames, 544 px wide, 30 fps,
`ffmpeg -i site.mp4 -vf fps=30,scale=544:-2 -q:v 3 src/f%05d.jpg`) and `logo-stacked-1810.png`
from `/mnt/project-files/`. Verified 28 Oct 2026: renders correctly from scratch.

Everything is driven by one data object (`window.REEL` overrides the default):

```js
{dur:25,
 cuts:[0,1.6,5,7.4,...],              // jump cuts: punch zoom alternates 1.04 / 1.16 + 0.05 kick + white flash
 titles:[{w:'RUKO!',t0:0,t1:1.6,st:'hand'}],   // ransom-note title + Lottie sticker at the end
 words:[[0.1,'Ruko'],[0.45,'ruko!'],...],      // Whisper timings, caption window of <=5 words
 lines:[0,10,25,...],                 // word index where a caption group starts
 stickers:[{s:'shock',x:720,y:820,t0:2.7,t1:5,sz:250,tap:false}],  // Lottie if in LOT, else st/<s>.png
 note:[5.3,10],                       // sticky note slides in, red strike draws through the price at +1.2s
 frame:[{t0:12.2,t1:15,a:0.3,sp:1.2}],// framed product screen: plays src frames from a (s) at speed sp
 hw:[10,12.2],                        // handwritten line with a yellow marker highlight wiping in
 stamp:[19.2,21],                     // "SIRF ₹799" rubber stamp slams (scale 2.2 -> 1, rotate -10)
 end:23.4}                            // end card fade/scale in
```

Device recipes (all in the template; copy the CSS/JS to new pages):
- **Ransom-note title**: each letter its own `<span>` with a random font from 7 display fonts and a
  random bg/fg pair from the brand-ish palette, slight random rotate/offset, letters pop in 45 ms
  apart from scale 1.4. Sits on a torn-paper strip (`clip-path` jagged polygon over `web/paper.webp`).
  Auto-shrinks to fit 1030 px. A Lottie emoji pops in (`eBack` overshoot) after the last letter.
- **Captions**: dark rounded pill (`rgba(40,30,34,.62)`), white Poppins 600 44 px, the current
  word in yellow `#FFD84D` 800. In RUKO the caption is bigger (Archivo Black 62 px) with a fixed
  set of accent words in yellow. Keep captions above the bottom 20%.
- **Stickers**: Lottie animations are **seeked**, not played: `anim.goToAndStop((lt*fr)%(op-1), true)`.
  White die-cut border via stacked `drop-shadow(±4px 0 0 #fff)` filters + soft shadow. Pop with
  `eBack`, slow wobble `sin(lt*4)*7deg`. `tap:true` bounces a pointer.
- **Sticky note**: `web/note.png` (CC0 rawpixel) with Permanent Marker text; the struck price is a
  rotated Sindoor bar whose width animates 0→108%.
- **Framed product cutaway**: white rounded card (580x1000) slides up from below with overshoot,
  tilted -3°, and swaps `<img src>` to the site-recording frame for time t (`window.imgReady()`
  waits for the swap before the screenshot).
- **Stamp**: Rubik Mono One in a thick Sindoor border, `mix-blend-mode:multiply`.
- **Punch zoom + flash**: background scale alternates per cut, a short 0.05 kick, a 0.08 s white
  flash at 50%, a sine shake in the first 0.4 s of the hook.
- **End card**: cream, stacked logo, CTA lines, Sindoor URL pill.

Other overlay devices built in later reels (see `examples/`):
- WhatsApp notification stack / RSVP cascade (`.nf` cards in `ruko-talking/reel.html`).
- WhatsApp chat with a link-preview card and the friend's reply (v3/v4 `ov*.html`).
- Guest-name gates cycled with a hand-drawn marker ring (`tutorial/ring.png`, v4).
- Numbered step chips over a phone recording (`tutorial/ov.html`).
- Pink chip labels that change per feature over a framed recording (`format-20s/ov.html`).
- iOS status bar + Safari URL pill + iOS keyboard typing intro, grey touch dots
  (`ad-20s-browser/chrome.html`, `ad-20s-iphone/chrome2.html`).
- iPhone mockup with Dynamic Island + record pill on a maroon→gold gradient
  (`ad-20s-iphone/phone.py` draws `bg.png`, `frame.png`, `smask.png`; `build4.py` composites with a
  zoom-pop entry).
- ₹500-notes cutaway: paper card zoom-blur → note fan flies in with motion blur → red tint + shake
  (`ad-20s-iphone/cut.py`, procedural PIL frames).

## Talking-head footage handling

- Trim each Priya clip to the spoken part (Whisper word timings), lay them on a master timeline
  `S=[0,4.6,9.9,...]`, map word times to master time (`S[clip]+t`).
- Add jump cuts mid-line (at a pause) to get the punch-zoom rhythm without new footage.
- "Realistic phone" look for full-screen Priya (20s ads): overscale 1150x2044 then crop with a
  sine handheld wobble, warm colour balance, `noise=alls=7:allf=t`:
  ```
  fps=30,scale=1150:2044,crop=1080:1920:'35+12*sin(t*1.7)+6*sin(t*3.9)':'62+10*sin(t*1.3+1)+5*sin(t*4.4)',
  colorbalance=rs=0.03:bs=-0.03:rm=0.02:bm=-0.02,eq=saturation=0.95:contrast=1.03,noise=alls=7:allf=t
  ```
- **Priya in the corner over the site (v2 format)**: generate her on a flat green background
  (image edit of her photo, ~₹3), animate that, then `colorkey`/OpenCV key + despill and overlay
  bottom-left (~40% width). Or cut her out of any clip with `hyperframes remove-background`
  (or rembg `u2net_human_seg`, keep the largest component, cut at a table line).
- **Face bubble** (tutorial): 300x440 rounded portrait card, crop 720x1056 from the top of the
  clip, white border + shadow. Sandeep wants full face plus some neck, not a tight circle.
- **Corner card** (20s ads): 280x410, white border, shadow.
- Retime the site recording so each feature lands on the line that mentions it: build an ffmpeg
  `trim,setpts=(PTS-STARTPTS)*k` chain per segment (see `v2-demo/fc.txt`).

## Audio

- Voice = the clips' own audio. Normalise each clip separately: `apad,loudnorm=I=-16:TP=-1.5`,
  trim back, then concat/amix. Never `loudnorm` inside the multi-input mix (it cut short clips).
- SFX from `scripts/sfx.py` with a cue list taken from the same timeline as the visuals: pops on
  stickers, 4 rising pops on ransom letters, whoosh on cuts, thump on hook/stamp, chime on price
  and end card, ticks on checklists, taps + key clicks on screen interactions, room tone at -50 dB
  for "realistic" edits. Mix SFX ~10–14 dB under the voice.
- Video and audio in separate ffmpeg passes, then `-c:v copy` mux. End the video right after the
  last spoken word + end card (Sandeep flagged a silent last 5 s once).

## Quality checklist before sending
- Spot-check stills at every section change; watch for fallback fonts, missing stickers, text in
  the bottom 20%, captions covering Priya's mouth, Sandeep's private info, AI watermarks (Gemini/Flow
  ✦ mark: inpaint with OpenCV, see `hand-scroll/comp3.py`).
- `ffprobe` duration, 1080x1920, audio present, no silence gaps where she should speak.
- Make a cover jpg from the strongest hook frame.
