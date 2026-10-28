const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+__dirname+'/ov.html');await p.waitForTimeout(2500);await p.evaluate(()=>document.fonts.ready);
const shots=[['bg','','bg'],['frame','','frame'],['end','','end'],
['chip','Har guest ka <b>apna naam</b> 💌','c1'],['chip','Scratch karo, <b>date</b> dikhegi ✨','c2'],
['chip','Countdown + <b>venue</b> 📍','c3'],['chip','Har <b>function</b> ki details 🎉','c4']];
for(const [m,c,n] of shots){await p.evaluate(([m,c])=>setMode(m,c),[m,c]);await p.screenshot({path:n+'.png',omitBackground:m!='bg'&&m!='end'});}
await b.close();})();
