# Build scripts from past reels (reference copies)

Copied from `/mnt/project-files/reels/source/` on 28 Oct 2026, text files only (no clips, frames or
keys). They were written as quick one-offs with hard-coded paths and timings, so read them for
technique rather than running them as-is. The cleaned-up, reusable versions are in `../scripts/`.

| Folder | Reel | Look at it for |
|---|---|---|
| `motion-5-cheezein/` | 18 s motion-graphics reel (rejected) | first `render(t)` timeline, phone framing |
| `punch/` | punch-edit preview | the original template (also in `../templates/punch/`) |
| `ruko-talking/` | first talking-Priya punch reel | master timeline from clips, Whisper → captions, WhatsApp notification stack, `submit2.py` OpenRouter call, `wt.py` Whisper |
| `v2-demo/` | v2 + FINAL NEW30 | `rec.js` prod recording, `fc.txt` retiming chain, transparent overlay `ov.html`/`ovf.html` + `render.js`, coupon end card, `submit3/5.py` (green-screen Priya, Devanagari line) |
| `v3-getting-ready/` | vanity / bindi story | `img_m.py` image edit (nano banana), phone pop-up + WhatsApp chat + reaction bubbles in `v3.html` |
| `v4-story-demo/` | free remix | `cut.py` rembg cut-out, `gates.js` guest-name screenshots, `ov4.html` |
| `format-20s/` | 20 s hook + silent demo | pink chip labels `ov.html`, `snap.js`, `submit6.py` bestie hook |
| `tutorial/` | 5-step tutorial + 30 s cut | `create.js` local create-flow recorder, `cf_marks.json`, `body*.py` framed body with keyboard mask, `final*.py` hook/face bubble/outro/end card assembly |
| `ad-20s-browser/` | 20 s ad v1 (rejected look) | iOS status bar + Safari URL pill + keyboard typing (`chrome.html`), handheld wobble filter, touch dots, `sfx.py` with room tone |
| `ad-20s-iphone/` | 20 s ad v2–v4 | `phone.py` iPhone mockup + gradient, `cut.py` ₹500-notes cutaway, `build4.py` full assembly, `submit9.py` emotional-hook prompt |
| `hand-scroll/` | 15 s hand-scrolling iPhone | `track2.py` quad + thumb tracking, `plan.py`, `rec2.js` action replay on prod, `comp3.py` key + despill + watermark inpaint |

Note: the recorders here (`rec.js`, `rec2.js`, `create.js`) predate Chromium 153; add
`args:['--force-device-scale-factor=3']` to `chromium.launch()` or the screencast comes out at 390 px wide.

Note: `tutorial/create.js` types a dummy phone number (`9876543210`) into the local form; never use
a real number.
