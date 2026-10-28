const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:2340}});
await p.goto('file://'+__dirname+'/chrome2.html');await p.waitForTimeout(800);
fs.rmSync('typ2',{recursive:true,force:true});fs.mkdirSync('typ2');
// typing: 0-0.25 empty, then type "vivah.online" ~0.09s/char, hold, press go at 1.55
const word='vivah.online';const N=54;
for(let i=0;i<N;i++){const t=i/30;let n=Math.max(0,Math.min(word.length,Math.floor((t-0.2)/0.09)+1));if(t<0.2)n=0;
 const press=t>=1.45?'go':(n>0&&n<=word.length&&(t-0.2)%0.09<0.06&&t<0.2+word.length*0.09?word[n-1]:null);
 await p.evaluate(([s,bl,pr])=>mode('typing',{text:s,blink:bl,press:pr}),[word.slice(0,n),Math.floor(t*2)%2==0||n<word.length,press]);
 await p.screenshot({path:`typ2/${String(i).padStart(3,'0')}.png`});}
for(const [n,o] of [['bar_home',{dom:'vivah.online'}],['bar_inv',{dom:'priya-rahul.vivah.online'}],['bar_prev',{dom:'vivah.online'}]]){await p.evaluate(o=>mode('bar',o),o);await p.screenshot({path:'b2_'+n+'.png',omitBackground:true});}
for(const pr of [20,45,70,90]){await p.evaluate(pr=>mode('bar',{dom:'vivah.online',prog:pr}),pr);await p.screenshot({path:`b2_bar_p${pr}.png`,omitBackground:true});}
console.log(JSON.stringify(await p.evaluate(()=>{mode("typing",{});return goRect()})));await b.close();})();
