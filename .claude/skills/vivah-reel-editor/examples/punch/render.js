const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{
 const mode=process.argv[2]; const out=process.argv[3];
 const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
 await p.goto('file://'+path.resolve('punch.html'));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(1500);
 fs.mkdirSync(out,{recursive:true});
 let times=[];
 if(mode==='full'){const D=parseFloat(process.argv[4]);for(let f=0;f<Math.round(D*30);f++)times.push(f/30);}
 else times=mode.split(',').map(Number);
 for(let k=0;k<times.length;k++){await p.evaluate(t=>window.render(t),times[k]);await p.evaluate(()=>window.imgReady());
  await p.screenshot({path:`${out}/${String(k).padStart(5,'0')}.${mode==='full'?'jpg':'png'}`,type:mode==='full'?'jpeg':'png',quality:mode==='full'?95:undefined});}
 await b.close();
})();
