const {chromium,devices}=require('playwright');
(async()=>{const b=await chromium.launch();
for(const n of ['Neha','Riya','Ankit','Simran']){const c=await b.newContext({...devices['iPhone 13'],deviceScaleFactor:3});const p=await c.newPage();
 await p.goto('https://priya-rahul.vivah.online/'+n,{waitUntil:'networkidle'});await p.waitForTimeout(2500);
 await p.screenshot({path:`gate-${n}.jpg`,type:'jpeg',quality:90});const t=await p.evaluate(()=>document.body.innerText.slice(0,80));console.log(n,JSON.stringify(t));await c.close();}
await b.close();})();
