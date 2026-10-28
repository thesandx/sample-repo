const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const S=JSON.parse(fs.readFileSync('caps.json'));const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+__dirname+'/cap.html');await p.waitForTimeout(2000);await p.evaluate(()=>document.fonts.ready);
fs.rmSync('cap',{recursive:true,force:true});fs.mkdirSync('cap');
for(let i=0;i<S.length;i++){await p.evaluate(s=>set(s),S[i]);await p.screenshot({path:`cap/${String(i).padStart(3,'0')}.png`,omitBackground:true});}
await b.close();})();
