const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:2340}});
await p.goto('file://'+process.argv[2]);await p.waitForTimeout(500);
await p.evaluate(()=>mode('bar',{dom:'priya-rahul.vivah.online'}));await p.screenshot({path:process.argv[3],omitBackground:true});await b.close();})();
