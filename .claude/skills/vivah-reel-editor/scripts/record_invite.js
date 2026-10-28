// Record the REAL product (free): a guest's invite on the live demo site, as an iPhone 13 at 3x,
// via a CDP screencast (smooth, real animations, real scratch reveal).
//
// Usage: node record_invite.js [GuestName] [outDir]
//   -> outDir/00000.jpg..., outDir/meta.json {frames:[timestamps], marks:[[name,t]]}
// Encode with a constant frame rate from the real timestamps (screencast frames arrive irregularly):
//   python3 frames_to_mp4.py outDir site.mp4     (see reference/site-recording.md)
//
// The demo couple is Priya & Rahul. Any name works in the URL (/Neha, /Riya, /Nani-ji ...),
// which is how "every guest sees their own name" shots are made.
const {chromium, devices} = require('playwright'); const fs = require('fs');
(async () => {
  const guest = process.argv[2] || 'Neha'; const dir = process.argv[3] || 'fr';
  // --force-device-scale-factor=3: without it, Chromium 153 screencasts at CSS size (390 px wide) even with deviceScaleFactor 3
  const b = await chromium.launch({args: ['--force-device-scale-factor=3']});
  const c = await b.newContext({...devices['iPhone 13'], deviceScaleFactor: 3});
  // user-select:none stops mouse drags (scratching) from highlighting text
  await c.addInitScript(() => document.addEventListener('DOMContentLoaded', () => {
    const s = document.createElement('style'); s.textContent = '*{user-select:none!important}'; document.head.appendChild(s);
  }));
  const p = await c.newPage();
  await p.goto(`https://priya-rahul.vivah.online/${guest}`, {waitUntil: 'networkidle'}); await p.waitForTimeout(2500);
  fs.rmSync(dir, {recursive: true, force: true}); fs.mkdirSync(dir);
  const s = await c.newCDPSession(p); const frames = []; const marks = [];
  s.on('Page.screencastFrame', async e => {
    const i = frames.length; frames.push(e.metadata.timestamp);
    fs.writeFileSync(`${dir}/${String(i).padStart(5, '0')}.jpg`, Buffer.from(e.data, 'base64'));
    try { await s.send('Page.screencastFrameAck', {sessionId: e.sessionId}); } catch (_) {}
  });
  await s.send('Page.startScreencast', {format: 'jpeg', quality: 88, maxWidth: 1170, maxHeight: 2532, everyNthFrame: 1});
  const mark = n => marks.push([n, Date.now() / 1000]); const W = ms => p.waitForTimeout(ms);
  const scrollTo = (y, ms) => p.evaluate(([y, ms]) => new Promise(r => {
    const y0 = scrollY, t0 = performance.now();
    const f = t => { const k = Math.min(1, (t - t0) / ms); const e = k < .5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
      scrollTo(0, y0 + (y - y0) * e); k < 1 ? requestAnimationFrame(f) : r(); };
    requestAnimationFrame(f); }), [y, ms]);
  const scratch = async (cx, cy) => { await p.mouse.move(cx - 40, cy - 40); await p.mouse.down();
    for (let i = 0; i < 14; i++) await p.mouse.move(cx - 40 + (i % 2 ? 80 : 0), cy - 45 + i * 7, {steps: 4});
    await p.mouse.up(); };
  mark('gate'); await W(2200);                       // Shri Ganesh "You are invited, Hi <Name>" gate
  mark('tap'); await p.mouse.click(195, 560); await W(2500);   // open the invite
  const cv = await p.$$eval('canvas', cs => cs.map(c => { const r = c.getBoundingClientRect(); return [r.left + r.width / 2, r.top + scrollY + r.height / 2]; }));
  const sy = cv.length ? cv[0][1] - 420 : 900;
  mark('scroll1'); await scrollTo(sy, 1800); await W(400);
  mark('scratch'); for (const [x, y] of cv.filter((_, i) => i % 2 == 0)) { await scratch(x, y - sy); await W(150); } await W(1200);
  mark('rest'); let y = sy; const H = await p.evaluate(() => document.documentElement.scrollHeight - innerHeight);
  while (y < H) { y = Math.min(H, y + 520); await scrollTo(y, 1100); await W(900); mark('y' + Math.round(y)); }
  await W(1500); await s.send('Page.stopScreencast');
  fs.writeFileSync(`${dir}/meta.json`, JSON.stringify({frames, marks}));
  console.log('frames', frames.length, 'dur', (frames[frames.length - 1] - frames[0]).toFixed(1), 's');
  await b.close();
})();
