const {chromium,devices}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const c=await b.newContext({...devices['iPhone 13'],deviceScaleFactor:3});await c.addInitScript(()=>{const add=()=>{const st=document.createElement('style');st.textContent='nextjs-portal{display:none!important}';document.documentElement.appendChild(st)};if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',add);else add();});const p=await c.newPage();
await p.goto('http://localhost:3000/',{waitUntil:'networkidle',timeout:90000});await p.waitForTimeout(2000);
// warm up: dev server compiles preview route on first hit, avoid long stall during recording
fs.rmSync('cf',{recursive:true,force:true});fs.mkdirSync('cf');
const s=await c.newCDPSession(p);const frames=[];const marks=[];
s.on('Page.screencastFrame',async e=>{const i=frames.length;frames.push(e.metadata.timestamp);fs.writeFileSync(`cf/${String(i).padStart(5,'0')}.jpg`,Buffer.from(e.data,'base64'));try{await s.send('Page.screencastFrameAck',{sessionId:e.sessionId});}catch(_){}});
await s.send('Page.startScreencast',{format:'jpeg',quality:90,maxWidth:1170,maxHeight:2532,everyNthFrame:1});
const mark=n=>{marks.push([n,Date.now()/1000]);console.log('mark',n)};const W=ms=>p.waitForTimeout(ms);
const scrollTo=async(y,ms)=>{await p.evaluate(([y,ms])=>new Promise(r=>{const y0=scrollY,t0=performance.now();const f=t=>{const k=Math.min(1,(t-t0)/ms);const e=k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2;scrollTo(0,y0+(y-y0)*e);k<1?requestAnimationFrame(f):r();};requestAnimationFrame(f);}),[y,ms]);};
mark('hero');await W(1800);
const fy=await p.evaluate(()=>{const h=document.getElementById('start');return h.getBoundingClientRect().top+scrollY-170;});
mark('toform');await scrollTo(fy,1200);await W(500);
mark('names');const bride=p.getByLabel("Bride's name").first();await bride.click();await W(250);await bride.pressSequentially('Priya',{delay:140});await W(300);
const groom=p.getByLabel("Groom's name").first();await groom.click();await W(250);await groom.pressSequentially('Rahul',{delay:140});await p.evaluate(()=>document.activeElement&&document.activeElement.blur());await W(1200);
await p.getByRole('button',{name:'Begin our story'}).first().click();await W(900);
mark('date');await p.locator('input[name=weddingDate]').click();await W(300);await p.locator('input[name=weddingDate]').fill('2026-12-07');await W(1600);
mark('phone');const ph=p.locator('input[name=phone]');await ph.click();await ph.pressSequentially('9876543210',{delay:80});await W(900);
await p.getByRole('button',{name:/Add our functions/}).click();await W(900);
mark('functions');for(const f of ['Tilak','Haldi','Mehndi','Sangeet','Reception']){const l=p.getByRole('checkbox',{name:f}).first();if(await l.count()){await l.click({force:true})}else{const t=p.getByText(f,{exact:true}).first();if(await t.count())await t.click();}await W(380);}await W(900);
await p.getByRole('button',{name:'Choose our address'}).first().click();await W(1500);
mark('address');await W(1400);
await p.getByRole('button',{name:/Choose our song/}).first().click();await W(1000);
mark('song');const r=p.getByRole('radio');console.log('radios',await r.count());if(await r.count()>1){await r.nth(1).click({force:true});}await W(1500);
mark('make');await p.getByRole('button',{name:'Make my website'}).first().click();
await p.waitForURL(/preview/,{timeout:60000}).catch(e=>console.log('nourl',e.message));mark('preview');await p.waitForLoadState('networkidle').catch(()=>{});await W(2500);
mark('gate_tap');await p.mouse.click(195,560);await W(2600);
const cv=await p.$$eval('canvas',cs=>cs.map(c=>{const r=c.getBoundingClientRect();return [r.left+r.width/2,r.top+scrollY+r.height/2];}));console.log('canvas',JSON.stringify(cv));
const sy=cv.length?cv[0][1]-420:900;
const scratch=async(cx,cy)=>{await p.mouse.move(cx-40,cy-40);await p.mouse.down();for(let i=0;i<14;i++){await p.mouse.move(cx-40+(i%2?80:0),cy-45+i*7,{steps:4});}await p.mouse.up();};
mark('scroll1');await scrollTo(sy,1600);await W(300);
mark('scratch');for(const [x,y] of cv.filter((_,i)=>i%2==0)){await scratch(x,y-sy);await W(150);}await W(1200);
let y=sy;const H=await p.evaluate(()=>document.documentElement.scrollHeight-innerHeight);
while(y<H){y=Math.min(H,y+520);await scrollTo(y,1000);await W(800);mark('y'+Math.round(y));}
await W(800);
const cont=p.getByRole('button',{name:/Continue/}).first();if(await cont.count()){mark('pay');await cont.click().catch(()=>{});await W(2500);}
await s.send('Page.stopScreencast');
fs.writeFileSync('cf_meta.json',JSON.stringify({frames,marks}));console.log('frames',frames.length,'dur',frames[frames.length-1]-frames[0]);
await b.close();})();
