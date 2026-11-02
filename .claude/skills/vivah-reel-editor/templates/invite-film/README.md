# Illustrated wedding video-invite template ("invite film")

Copies the **structure, timing and motion** of the IG reel `DWbD-OMCRcG` (vfx.wala__, 85 s Jain wedding
invite, 720x1280, music only, no voice). Do not reuse that creator's artwork (it's watermarked, and it's
their work). Every illustration comes from art Sandeep downloads (Freepik / Vecteezy / Canva are blocked
from the container, and scraping Vecteezy was refused). Only text and layout are made in code.

## Reference breakdown (measured, 1080x1920 coords = reference x1.5)
| Time | Page | What happens |
|---|---|---|
| 0–9.5 | Intro card 1 | Mughal garden backdrop (arch with hanging vines, plants both sides, railing + peacock + pond). Deity image blurs/grows in at 0.5 s, mantra line wipes in at ~2 s. Two swans glide on the pond the whole intro |
| 9.5–19.5 | Intro card 2 | Text cross-fades: "X Family" (script), "Cordially invites you for Wedding Ceremony of" (serif). Monogram wreath pops ~13 s, initials + couple names in script ~14 s |
| 19.5–31.5 | Intro card 3 | Lineage, one line every ~0.9 s: groom (script), GRAND S/O…, S/O, parents, "with", bride, GRAND D/O…, D/O, parents |
| 31.5 | → | Blur out to grey, blur in |
| 31.5–40.5 | Function 1 (Haldi) | Toran drops from top, matkas pop at both sides, characters on a floor at the bottom. Title (bold serif) then date / day / time / venue wipe in left-to-right, ~0.55 s apart |
| 40.5–50.5 | Function 2 (Mehendi) | same, blur cut |
| 50.5–61 | Function 3 (Sangeet) | white flash cut; flower canopy + lanterns |
| 61–69 | Function 4 (Chaak) | white flash; leaf toran with bells |
| 69–77 | Function 5 (Baraat) | flash to empty cream, then items pop one by one (procession rises, umbrellas pop, garland drops last) |
| 77–84.8 | Function 6 (Vivah) | everything shrinks away, mandap grows from a dot, couple inside |

All of this lives in `make_data.py` (INTRO_CARDS, FN_DUR, FN_IN, FN_STYLE, TIMING). Any number of functions works;
durations/transitions cycle. `--fit 60` rescales the whole film to 60 s.

## Use
```bash
cp details.example.json details.json      # fill in names, lineage, functions, art file names
# put PNGs (transparent) in art/; missing ones render as labelled placeholder boxes
python3 make_data.py details.json > data.js && node ../../scripts/render_frames.js invite.html stills 3,14,26,33,51,72,82
bash build.sh details.json /mnt/project-files/reels/invite-<couple>.mp4 [song.mp3]
```
Full render is ~2,550 frames (85 s at 30 fps), a few minutes, free.

## Art shot list (all transparent PNG, same flat-illustration style, ideally one Freepik/Vecteezy pack)
Intro: `mahavir.png` (Bhagwan Mahavir seated, with halo, ~1:1; Jain default), `monogram-wreath.png` (floral ring, empty centre),
`intro-arch.png` (full-width arch/jharokha top frame, 1080x820), `intro-plants-left.png` (tall garden plants,
mirrored for right), `intro-garden-pond.png` (railing + bushes + peacock + pond strip, 1080x700),
`swan.png` (one swan facing right).
Per function: `<fn>-top.png` (full-width toran / garland / canopy, ~1080x450), `<fn>-main.png`
(the scene: characters doing that ritual, on a floor, ~900x800), optional `<fn>-prop.png` (matka /
lantern / umbrella / dhol; mirrored on the other side).

## Self-sourced art (no uploads needed): `compose_fluent.py`
`python3 compose_fluent.py <sprite_cache> art/ <jain-emblem.png>` builds every slot from fetched assets:
Microsoft Fluent 3D emoji (MIT, jsdelivr: rosette = marigold, swan, peacock, lotus, elephant, horse, dhol,
dancer, bride, groom, diya, lantern, bell, amphora = matka...) arranged into torans, garlands, a mandap, a
garden arch, a pond with railing. Deity card uses the official Jain Prateek Chihna (public domain;
`commons.wikimedia.org/wiki/Special:FilePath/Jainism.svg?width=800` returns a PNG; Wikimedia rate-limits,
retry later). Openclipart (CC0) is reachable too but its art is inconsistent. First film made this way:
2 Nov 2026, Aarav & Siya sample.
