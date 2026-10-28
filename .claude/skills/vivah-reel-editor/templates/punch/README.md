# Punch-edit template

`punch.html` is a 1080x1920 page with `window.render(t)`; all timings live in the `D` object
(override with `window.REEL = {...}` in a script tag before the main script). Explained in
`../../reference/punch-edit-pipeline.md`.

Before rendering, in a working copy of this folder:
```bash
python3 ../../scripts/fetch_assets.py .          # lottie.min.js, lot.js (Noto Lottie), st/*.png (Fluent 3D)
cp /mnt/project-files/logo-stacked-1810.png .     # brand end-card logo
# background: a still for tests, or swap #bg per frame from your talking clip
ffmpeg -ss 1 -i priya_clip.mp4 -frames:v 1 -vf scale=1080:1920 priya.png
# product frames for the framed cutaway (544 px wide, 30 fps)
mkdir -p src && ffmpeg -i site.mp4 -vf fps=30,scale=544:-2 -q:v 3 src/f%05d.jpg
node ../../scripts/render_frames.js punch.html stills 0.5,6,13,19.5,24   # check these first
node ../../scripts/render_frames.js punch.html frames 25                  # full render
ffmpeg -framerate 30 -i frames/%05d.jpg -i voice_and_sfx.wav -c:v libx264 -crf 16 -pix_fmt yuv420p -c:a aac -shortest out.mp4
```
`web/` holds CC0 sticky notes and the paper texture (sources in `web/list.txt`).
Verified 28 Oct 2026 from a clean container.
