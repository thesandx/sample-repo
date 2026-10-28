const {chromium,devices}=require('playwright');const fs=require('fs');
const A=JSON.parse(fs.readFileSync('plan.json'));
(async()=>{const b=await chromium.launch();const c=await b.newContext({...devices['iPhone 13'],deviceScaleFactor:3});await c.addInitScript(()=>{document.addEventListener('DOMContentLoaded',()=>{const st=document.createElement('style');st.textContent='*{user-select:none!important;-webkit-user-select:none!important}';document.head.appendChild(st)})});const p=await c.newPage();
await p.goto('https://priya-rahul.vivah.online/Neha',{waitUntil:'networkidle'});await p.waitForTimeout(2500);
fs.rmSync('fr2',{recursive:true,force:true});fs.mkdirSync('fr2');
const s=await c.newCDPSession(p);const frames=[];
s.on('Page.screencastFrame',async e=>{const i=frames.length;frames.push(e.metadata.timestamp);fs.writeFileSync(`fr2/${String(i).padStart(5,'0')}.jpg`,Buffer.from(e.data,'base64'));try{await s.send('Page.screencastFrameAck',{sessionId:e.sessionId});}catch(_){}});
await s.send('Page.startScreencast',{format:'jpeg',quality:90,maxWidth:1170,maxHeight:2532,everyNthFrame:1});
await p.waitForTimeout(800);
await p.evaluate(()=>{window.__sc=(y,ms)=>{const y0=scrollY,t0=performance.now();const f=t=>{const k=Math.min(1,(t-t0)/ms);const e=1-Math.pow(1-k,3);scrollTo(0,y0+(y-y0)*e);if(k<1)requestAnimationFrame(f)};requestAnimationFrame(f)}});
const T0=Date.now()/1000;const log=[];
const lag=[];for(const [t,ty,a,b2] of A){lag.push([ty,+(Date.now()/1000-T0-t).toFixed(3)]);const w=T0+t-Date.now()/1000;if(w>0)await new Promise(r=>setTimeout(r,w*1000));
  if(ty=='tap')await p.mouse.click(a,b2);
  else if(ty=='scroll'){await p.evaluate(([y,ms])=>{window.__sc=window.__sc||((y,ms)=>{const y0=scrollY,t0=performance.now();const f=t=>{const k=Math.min(1,(t-t0)/ms);const e=1-Math.pow(1-k,3);scrollTo(0,y0+(y-y0)*e);if(k<1)requestAnimationFrame(f)};requestAnimationFrame(f)});__sc(y,ms)},[a,b2*1000]);}
  else if(ty=='down')await p.mouse.down();else if(ty=='up')await p.mouse.up();
  else if(ty=='move'){if(Date.now()/1000-T0-t<0.03)await p.mouse.move(a,b2,{steps:1});}
  else if(ty=='reveal'){for(const n of a.split(',')){const ok=await p.evaluate(n=>{const e=[...document.querySelectorAll('button')].find(b=>b.innerText.trim()=='Reveal the '+n);if(e&&e.offsetParent!==null){e.click();return 1}return 0},n);log.push([t,n,ok]);}}
}
await p.waitForTimeout(2500);await s.send('Page.stopScreencast');
fs.writeFileSync('meta2.json',JSON.stringify({frames,T0,log}));console.log('frames',frames.length,JSON.stringify(log),JSON.stringify(lag.filter(l=>l[0]!='move')));await b.close();})();
