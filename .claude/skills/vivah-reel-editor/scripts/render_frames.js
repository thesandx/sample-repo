// Render an HTML timeline page frame by frame (free, local).
// The page must define window.render(t) (t in seconds) that sets every element's state for time t,
// and may define window.imgReady() returning a Promise that resolves when swapped <img>s are loaded.
//
// Usage:
//   node render_frames.js page.html out_dir 25          # full render, 30 fps, jpg
//   node render_frames.js page.html out_dir 25 --png    # png keeps alpha if the page body is transparent
//   node render_frames.js page.html stills 0,2.5,7      # spot-check stills (png) before a full render
// Then: ffmpeg -framerate 30 -i out_dir/%05d.jpg -c:v libx264 -crf 16 -pix_fmt yuv420p ov.mp4
const {chromium} = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const [page, out, spec] = process.argv.slice(2);
  const png = process.argv.includes('--png'); const FPS = 30;
  const b = await chromium.launch(); const p = await b.newPage({viewport: {width: 1080, height: 1920}});
  await p.goto('file://' + path.resolve(page));
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(1500); // let webfonts + lottie settle
  fs.mkdirSync(out, {recursive: true});
  const times = spec.includes(',') ? spec.split(',').map(Number)
    : Array.from({length: Math.round(parseFloat(spec) * FPS)}, (_, f) => f / FPS);
  const usePng = png || spec.includes(',');
  for (let k = 0; k < times.length; k++) {
    await p.evaluate(t => window.render(t), times[k]);
    await p.evaluate(() => window.imgReady ? window.imgReady() : null);
    const f = `${out}/${String(k).padStart(5, '0')}.${usePng ? 'png' : 'jpg'}`;
    await p.screenshot({path: f, type: usePng ? 'png' : 'jpeg', quality: usePng ? undefined : 95, omitBackground: png});
    if (k % 150 === 0) console.log('frame', k, '/', times.length);
  }
  await b.close();
})();
