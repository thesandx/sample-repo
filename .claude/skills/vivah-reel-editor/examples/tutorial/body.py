import subprocess
SRC='../proc/process.mov'
# name, start, end, speed, mode, chip, callout
SEG=[('s1',2,11,2.5,'mask','k1',None),('s2',13,19,2,'n','k2',None),('s3',28,35,2,'n','k3',None),
('s4',36,41,2,'n','k4',None),('s5',42,48,2,'n','k5',None),('s6',49,55,1.5,'n','kd',None),
('r1',55.5,63,2.5,'pv','kr','x1'),('r2',63,72,2.5,'pv','kr','x2'),('r3',73,84,3,'pv','kr','x3')]
for n,a,b,sp,mode,chip,call in SEG:
  d=(b-a)/sp
  if mode=='pv': crop='crop=416:640:0:80,scale=-2:720,crop=416:720'
  else: crop='crop=416:720:0:0'
  if mode=='mask': crop+=",drawbox=x=0:y=405:w=416:h=315:color=0xFFFCF8:t=fill"
  ins=['-i','bg.png','-i','frame.png','-i','mask.png','-i',chip+'.png']+(['-i',call+'.png'] if call else [])
  fc=(f"[0:v]trim={a}:{b},setpts=(PTS-STARTPTS)/{sp},fps=30,{crop},scale=832:1440:flags=lanczos,format=rgba[v];"
      f"[3:v]format=gray[m];[v][m]alphamerge[vm];[1:v][2:v]overlay=0:0[bg];[bg][vm]overlay=124:240[c];"
      f"[4:v]format=rgba,fade=in:st=0:d=0.15:alpha=1[k];[c][k]overlay=0:0")
  if call: fc+=f"[c2];[5:v]format=rgba,fade=in:st=0.4:d=0.2:alpha=1[x];[c2][x]overlay=0:0:enable='gte(t,0.4)'"
  fc+=",format=yuv420p,setsar=1[o]"
  cmd=['ffmpeg','-v','error','-y','-i',SRC,'-loop','1','-t',str(d)]+ins[:2]+['-loop','1','-t',str(d)]+ins[2:4]+['-loop','1','-t',str(d)]+ins[4:6]+['-loop','1','-t',str(d)]+ins[6:8]+(['-loop','1','-t',str(d)]+ins[8:10] if call else [])
  cmd+=['-filter_complex',fc,'-map','[o]','-t',str(d),'-r','30','-an','-c:v','libx264','-crf','18','-preset','fast',n+'.mp4']
  subprocess.run(cmd,check=True);print(n,round(d,2))
open('body.txt','w').write(''.join(f"file '{s[0]}.mp4'\n" for s in SEG))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','body.txt','-c','copy','body.mp4'],check=True)
