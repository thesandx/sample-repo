const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{const out=process.argv[2],D=parseFloat(process.argv[3]);
 const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
 await p.goto('file://'+path.resolve('ov4.html'));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(2500);
 fs.mkdirSync(out,{recursive:true});
 for(let f=0;f<Math.round(D*30);f++){await p.evaluate(t=>window.render(t),f/30);
  await p.screenshot({path:`${out}/${String(f).padStart(5,'0')}.png`,omitBackground:true});}
 await b.close();})();
