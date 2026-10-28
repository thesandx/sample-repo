const {chromium}=require('playwright');
const S={bg:{bg:1},frame:{frame:1},end:{end:1},cmt:{cmt:1},
k1:{chip:{n:'1',t:'Dono ka naam ✍️'}},k2:{chip:{n:'2',t:'Shaadi ki date 📅'}},k3:{chip:{n:'3',t:'Functions chuno 🎉'}},
k4:{chip:{n:'4',t:'Apna address 🔗'}},k5:{chip:{n:'5',t:'Apna gaana 🎵'}},kd:{chip:{t:'Website ready ✅'}},kr:{chip:{t:'Aur website aisi dikhti hai 😍'}},
x1:{call:{t:'Har guest ka apna naam 💌',x:150,y:980}},x2:{call:{t:'Scratch karo ✨',x:180,y:1020}},x3:{call:{t:'Venue + functions 📍',x:420,y:1240}},
h1:{cap:'Shaadi ka card<br>maine khud banaya 💌'},h2:{cap:'Sab pooch rahe<br>kisne banaya? 😍'},h3:{cap:'Chalo batati hoon ✨'},
o1:{cap:'Mummy ne poore<br>khandaan ko forward kiya! 😂'},o2:{cap:'Comment LINK 👇'}};
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+__dirname+'/ov.html');await p.waitForTimeout(2500);await p.evaluate(()=>document.fonts.ready);
for(const n in S){await p.evaluate(o=>show(o),S[n]);await p.screenshot({path:n+'.png',omitBackground:!(S[n].bg||S[n].end)});}
await b.close();})();
