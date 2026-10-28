# The 38 listicle effects (from Sandeep's two reference reels, 28 Oct 2026)

Sources Sandeep sent: `instagram.com/reel/Def9pj5TWtA` (@tenfoldmarc, "17 video effects Claude can
create", 27 s, CTA "comment STUDIO") and `instagram.com/reel/De2HxUVt3V1` (@vibha.in.progress,
24 effects in 21 s as /slash-command captions, CTA "comment CLAUDE"). 17 + 24 = 41 names; frame
break, headline wall and zoom-through appear in both, so **38 distinct effects**. Some rows below
group variants of one effect (e.g. cover story / pastel word / glass type). Full illustrated
breakdown with frames: Reel Effects Playbook https://claude.ai/artifact/DSBbC5bSDbU1S74M3APCfU

## Why these reels hold attention (copy the structure, not just the effects)
1. **Counted list in the hook** ("17 effects" + a `07/17` counter chip): a finish line, so people stay.
2. **Something new every ~1 s**: one effect per beat of speech until the list ends.
3. **Visible progress**: a checklist card ticks items off (yellow highlight on the current one).
4. **Same face, same seat**: the person never moves; all variety comes from the edit, so ONE
   recording feeds the whole reel.
5. **Captions with one accent word**: white bold sans, key word in yellow (reel 1) or italic serif (reel 2).
6. **CTA shown, not just said**: an Instagram comment box types the keyword, then +Follow flips to Following.
7. **Comment-to-DM**: works only with an auto-DM tool (ManyChat-style). vivah has none yet, so end
   with "link bio mein hai" until Sandeep sets one up.
8. **Meme cutaway** on the emotional last word keeps the final seconds alive (licence it or skip it).

## Footage requirement (important)
Matte effects need a **medium shot with headroom**: Priya seated, waist-up, wall visible behind her,
static camera. All existing Priya clips are tight face close-ups, so text placed behind her is
mostly hidden (verified 28 Oct: `scripts/text_behind.sh` works, but only the edges of "SIRF 799"
peek out around her head). Generating one such clip on Grok Lite is ~$0.19 (₹16): **ask first**.
A real friend's phone recording is better and free.

## Shared building blocks
- **Matte (person cut-out)**: `npx --yes hyperframes@0.8.213 remove-background clip.mp4 -o subj.webm`
  (free, ~1.5–2 fps CPU). Decode with `-c:v libvpx-vp9 -i subj.webm` (else alpha is lost).
  `--background-output plate.webm` is *hole-cut*, not inpainted: to put things behind the person,
  use the original clip as the bottom layer. Stack: **original → middle layer → cut-out**.
  `scripts/text_behind.sh clip.mp4 layer.png out.mp4` does exactly this.
- **Middle / top layers**: HTML pages with `render(t)` rendered by `scripts/render_frames.js --png`
  (transparent), or HyperFrames catalog items (one HTML file each with a paused GSAP timeline; seek
  it from `render(t)`: `tl.seek(t)`). Catalog: https://hyperframes.heygen.com/catalog, raw item at
  `/catalog/{blocks|components}/<slug>.md`, index `/_llms/catalog/catalog.txt`. Apache 2.0.
  HeyGen also publishes a `talking-head-recut` skill (Whisper transcript → timed HTML overlays):
  the same pipeline as ours.
- **Camera moves**: ffmpeg `scale/crop` with expressions in `t`, or CSS transforms on a `<video>`/`<img>`
  frame in the page.
- Fit: **Use** = fits vivah now; **Maybe** = needs the right footage or one careful use; **Skip** = off-brand for brides.

## A. Person cut out from the background (needs a matte)

| # | Effect | What you see | How to build | Fit | Vivah use |
|---|---|---|---|---|---|
| 1 | Cover story | Huge word behind the head like a magazine cover ("EDIT") | original → giant serif/condensed word (layer) → cut-out. Animate letter-spacing or a slow scale on the word | Use | "SIRF ₹799", "SHAADI", "PRIYA & RAHUL" behind Priya |
| 2 | Pastel word | Same, soft pastel colour block words | as #1, pastel fills (Blush/Lotus), rounded font | Use | "pyaara invite" in blush |
| 3 | Glass type | Same, frosted-glass letters | as #1; word layer = `backdrop-filter: blur()` text mask, or blur the original inside a text mask in ffmpeg (`alphamerge`) | Maybe | price behind her, once |
| 4 | Frame break | Person sits inside a photo/magazine frame; head/hand pokes out of it | scale the original into a frame (border image), then overlay the full-size cut-out on top so parts outside the frame stay visible ("made in one clip") | Use | Priya inside a paper wedding card frame, leaning out into the phone |
| 5 | Headline wall | Sticky notes / headlines / posts pinned on the wall behind | cards (HTML, slight rotation, pin sticker, shadow) between original and cut-out; stagger pop-ins with ticks | Use | Function cards: Haldi, Mehendi, Sangeet, Phere with guest names |
| 6 | Depth scatter | Cards both behind and in front of the person | some cards in the middle layer, some drawn above the cut-out | Use | name invites floating around her |
| 7 | Couch wall | Phone screens/posts pinned on the wall behind a seated person | as #5 with phone-screenshot cards | Use | Guests' named invite screenshots (Neha, Riya, Nani ji…) on the wall |
| 8 | Gravity drop | Text tags fall and pile up behind her | middle layer: tags with a simple physics drop (y += v, v += g, bounce damping, rotation) per frame in `render(t)` | Use | "printing", "courier", "RSVP calls" fall away like old chores |
| 9 | Paper cut | Person becomes a white-bordered sticker on a scribbled collage, ransom-note text | cut-out + thick white stroke (dilate the alpha: `cv2.dilate` or stacked CSS drop-shadows) + drop shadow, placed on paper texture (`templates/punch/web/paper.webp`) with ransom letters | Use | "100% PERSONAL" collage; matches the punch-edit look Sandeep liked |
| 10 | Green screen | Person stands in front of an app UI | cut-out over the real site recording (the v2 format) | Use | Priya in front of the live invite (already our best format) |
| 11 | Doodle boil | White outline traced round the body + wobbly hand-drawn doodles | edge of the matte (`cv2.Canny` or alpha dilate minus alpha) stroked white; doodle SVGs re-jittered every 3 frames (boil) | Maybe | hearts and a doodled mandap around Priya |

## B. Camera moves (no matte needed)

| # | Effect | What you see | How to build | Fit | Vivah use |
|---|---|---|---|---|---|
| 12 | Digital zoom | Fast punch-in on a detail | `scale` keyframes (ffmpeg `zoompan` or crop expr), ease-out, plus a whoosh | Use | punch into "Hi Neha" on the gate |
| 13 | Zoom-through cut | Punch-in with motion blur, cut to next shot through the blur | zoom 1→1.5 over 6 frames with radial/averaged blur (`cut.py` `zblur` averages 6 zoom levels), next shot starts blurred and settles | Use | zoom into her phone screen, land on the guest's named invite |
| 14 | Swipe (before/after) | Diagonal line wipes one look into another with "before"/"after" labels | two layers, animated `clip-path: polygon()` diagonal, white divider line | Use | paper card → vivah site; gold foil → scratched date |
| 15 | Pause point | Freeze frame, pause icon, "PAUSED" scribble | hold one frame (`tpad`/loop), grey tint, pause glyph pop, handwritten text | Use | freeze on her shocked face: "PAUSED: ₹40,000 for cards?" |
| 16 | Pull-back reveal | Frame pulls out to reveal more | start scaled in (2x) on a detail, ease to 1x | Maybe | pull back from the phone screen to Priya holding it |
| 17 | Vertigo (dolly zoom) | Subject stays, background stretches | needs matte: background scales up while the cut-out scales down | Maybe | the "kitna mehenga?!" shock beat |
| 18 | Orbit | Picture circles/rotates around | CSS 3D `rotateY` on a framed video | Maybe | one transition at most |

## C. Fake UI on top of the video

| # | Effect | What you see | How to build | Fit | Vivah use |
|---|---|---|---|---|---|
| 19 | Held fake phone | A rounded rectangle composited into the hands; each effect plays inside it | track/estimate the hand position (static seat makes this easy: fixed rect), draw phone frame + screen video in the layer above the original, hands from the cut-out on top if fingers overlap | Use | Priya holding a phone that shows each feature (listicle idea 1) |
| 20 | UI world | Chat window/app UI floats beside the person | HTML mockup with live animation | Use | WhatsApp chat "Neha, aapka invite 💌" + link preview + reply |
| 21 | Checklist | To-do card ticks off, current item highlighted | HTML card, items tick at timed beats (tick SFX) | Use | "Shaadi checklist": venue ✓, functions ✓, invite ✓, ₹799 ✓ |
| 22 | Counter chip | "07/17 Jiggle delete" top-left | HTML chip, number rolls per item | Use | "03/08" on the listicle |
| 23 | Badge unlock | Game toast "Achievement unlocked 47/48" with trophy | HTML toast slides in, shine sweep (moving gradient), chime | Use | "Achievement unlocked: saare guests invited" (no fake counts) |
| 24 | Uninstall | Progress bar "Uninstalling: editing apps" | HTML iOS-style progress sheet | Use | "Uninstalling: printing press, courier wala, card dukaan" |
| 25 | Jiggle delete | iOS home-screen icons jiggle, ✕ badges, icons pop away | HTML grid of icons, `rotate(sin(t*30)*2deg)`, ✕ tap, scale-out pop | Use | icons "Printing press", "Courier", "Card dukaan ₹40k", "Excel guest list"; last one left is the vivah mark |
| 26 | Comment panel | Instagram comment sheet; keyword types itself in | HTML replica of the IG comment sheet, typed letter by letter with key clicks | Use (with auto-DM) | "Comment SHAADI" end card |
| 27 | Follow button flip | +Follow flips to Following | HTML button, 3D flip or colour swap at a beat | Use | after the CTA |
| 28 | Bento | Her video becomes one tile in a bento grid next to a big stat tile | CSS grid; video tile shrinks into place | Maybe | tiles: name card, map, countdown, ₹799 (no fake numbers) |
| 29 | Eye dropper | Picker cursor samples a colour, swatch pops out | cursor sprite + sampled pixel colour + swatch | Maybe | pick her lehenga colour, site theme changes to match |
| 30 | Prompt bar | AI prompt box typing | HTML | Skip | too techy for brides |
| 31 | Timeline | Editing timeline UI | HTML | Skip | |
| 32 | Artifact studio | Tool dashboard | HTML | Skip | our product UI is the site itself |

## D. Looks and filters

| # | Effect | What you see | How to build | Fit | Vivah use |
|---|---|---|---|---|---|
| 33 | Contact sheet | Film-strip grid of the same clip, one frame circled red, others crossed | grid of frames at offsets (`ffmpeg select` / `tile`), marker circle SVG drawn on (stroke-dashoffset), red ✕ marks | Use | her mirror selfies, red circle on the one holding the invite |
| 34 | Whiteboard | Hand-drawn flow boxes and arrows | marker SVG paths animated with stroke-dashoffset | Maybe | "Naam likho → photo daalo → link bhejo" |
| 35 | Riso | Pink print grain, misregistered colours | split channels, offset, halftone/grain overlay | Maybe | once, as a pattern break |
| 36 | Engraving | Banknote engraving line pattern | line-screen shader / threshold over sine lines | Maybe | could look like an old wedding card |
| 37 | Projector | Flickering projector light | brightness flicker + vignette + dust overlay | Maybe | |
| 38 | ASCII / pixel-me / oscilloscope / chart grow | Video as text, 8-bit sprite, green line graph, growing chart | canvas/shader | Skip | tech-creator look, off-brand |

## Three vivah reels using these (proposed, not yet made)

**1. "Shaadi invite ki 8 cheezein jo paper card nahi kar sakta"** (copies the format closely).
Priya seated holding a phone frame at chest height, counter chip "03/08", pink checklist at the side.
0–1 s title + checklist, VO "Paper card nahi kar sakta ye 8 cheezein…" · 01 Har guest ka naam:
zoom-through into "Neha ji" on the Ganesh card · 02 Scratch se date: swipe on the gold foil ·
03 Venue map: pull-back from the Maps pin · 04 Saare functions: headline wall behind her ·
05 Countdown digits rolling · 06 Gaana: pause point with a music note · 07 WhatsApp RSVP chat
bubbles cascade · 08 Price: "SIRF ₹799" behind her head · 9–15 s phone drops, word captions,
comment panel types SHAADI (only if auto-DM exists), Follow flips.

**2. "Maine apni shaadi se ye sab uninstall kar diya"** (comedy, fake UI).
0–3 s Priya at the mirror with bindi, uninstall bar "Uninstalling: card wale uncle…" · 3–7 s
jiggle-delete home screen (Printing press, Courier, Card dukaan ₹40k, Excel guest list) · 7–11 s one
icon left, the vivah mark: tap, zoom-through into the site · 11–15 s badge unlock, end card ₹799.

**3. "Meri shaadi ka cover story"** (soft, aesthetic).
0–3 s "PRIYA & RAHUL" huge behind her head · 3–6 s contact sheet of getting-ready shots, red circle
on the one with the phone · 6–10 s frame break: inside a paper card frame, leans out into the phone ·
10–15 s paper-cut sticker Priya over the site recording, ransom "100% PERSONAL", URL end card.

Next step that was offered to Sandeep: build these effects as a reusable HyperFrames "vivah effects
pack" so a new reel only needs a new talking clip.
