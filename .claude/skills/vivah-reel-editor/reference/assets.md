# Assets: where to get stickers, textures, fonts and brand files

Sandeep's rule: source assets like a human editor would (real stickers and textures from the web),
don't draw them in code. Ask him for anything you can't fetch; he can download from blocked sites
and upload.

## Works from the cloud container
| Asset | Source | Licence | How |
|---|---|---|---|
| Animated emoji (Lottie) | Google Noto: `https://fonts.gstatic.com/s/e/notoemoji/latest/<codepoint>/lottie.json` (browse https://googlefonts.github.io/noto-emoji-animation/) | CC BY 4.0 | `scripts/fetch_assets.py` → `lot.js`; play with lottie-web, **seek** per frame |
| 3D emoji PNG | Microsoft Fluent: `cdn.jsdelivr.net/gh/microsoft/fluentui-emoji@main/assets/<Name>/3D/<name>_3d.png` (hands/people: `<Name>/Default/3D/<name>_3d_default.png`) | MIT | `scripts/fetch_assets.py` → `st/` |
| lottie-web | cdnjs `bodymovin/5.12.2/lottie.min.js` | MIT | fetched by the script |
| Sticky notes, tape, torn paper, stamps, paper textures | rawpixel CC0 PNGs (`images.rawpixel.com/image_png_1300/...`), list with URLs in `templates/punch/web/list.txt` | CC0 | previews may have a baked checkerboard: key it out |
| Animations / captions / UI blocks | HyperFrames catalog (449 items) | Apache 2.0 (GSAP free commercially) | raw HTML at `hyperframes.heygen.com/catalog/{blocks|components}/<slug>.md` |
| Fonts | Google Fonts | OFL | `<link>` in the page with `display=block` |
| ₹500 note | `paisaboltahai.rbi.org.in/images/500-note-front.png` (official RBI image) | | the SPECIMEN stamp was inpainted out for the cutaway |

## Blocked / unreliable
Giphy, Pixabay, Pexels, Freepik (blocked), Wikimedia (429), Openverse (timeouts). Meme clips (e.g.
"The Office yes!") need a licence: skip, or ask Sandeep.

HyperFrames catalog: top picks for vivah were Highlight / Emoji Pop / Kinetic Slam captions, Marker
Highlight, hand-drawn circle/arrow, Strikethrough Replace, Freeze-Frame Dressing, Torn Paper Rip,
Chat Message link card (restyle to WhatsApp), Notification Cascade (RSVPs), Device Frame Stage,
Count Up, Logo Sting end card. Skip branded demos (HeyGen/Slack/Apple), testimonial/social-proof
items, logo effects with glow/3D (brand rules), WebGPU shaders. Remotion is also fine licence-wise for
teams up to 3, but HyperFrames covers everything and is what the pipeline uses.

## Project files (Sandeep's, in `/mnt/project-files/`)
- Logos: `logo-stacked-1810.png` (end cards), `logo-horizontal*.png|svg`, `logo-hindi*.png|svg`,
  `mark-colour-*.png`, `mark-white-*.png`, `wordmark*.png`.
- Ad screens and stickers already cut: `ads/source/scr/*.png` (gate, card, scratch before/after,
  countdown, venue, functions, RSVP, guest gates), `ads/source/st/*.png` (~27 3D emoji).
- Character portraits and sheets: `uploads/hearth/` (ids in `brand-audience-rules.md`).
- Approved hand still: `reels/source/hand-scroll/hand-still-v2.png`.
- Existing Priya clips (reusable for free remixes): `reels/source/ruko-talking/c1–c5.mp4`,
  `v2-demo/g1–g6.mp4, n30.mp4`, `tutorial/t1–t5.mp4`, `ad-20s-browser/a1–a4.mp4`,
  `ad-20s-iphone/h1.mp4`, `format-20s/bf1.mp4` (bestie).
- Site recordings: `reels/source/process/vivah-create-flow-HD-1170.mp4` (local create flow),
  `reels/source/hand-scroll/screen.mp4` (prod invite, 1170x1992).

If you're in a different project without these files, ask Sandeep to upload the logo pack and
character portraits; everything else can be regenerated with the scripts here.
