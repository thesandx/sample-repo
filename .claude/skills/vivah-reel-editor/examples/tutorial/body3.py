import subprocess
C='../hd/create.mp4';S='../rec/site.mp4'
SEG=[('s1',C,3.3,8.1,2.09,'k1',None),('s2',C,8.1,12.9,2.09,'k2',None),('s3',C,12.99,17.9,2.04,'k3',None),
('s4',C,17.9,20.4,1.67,'k4',None),('s5',C,20.4,22.4,1.05,'k5',None),('s6',C,23.0,29.0,3.0,'kd',None),
('r1',S,0.2,4.7,2.0,'kr','x1'),('r2',S,6.0,11.0,2.5,'kr','x2')]
tot=0
for n,src,a,b,sp,chip,call in SEG:
  d=round((b-a)/sp,3);tot+=d
  ins=['-i',src,'-loop','1','-t',str(d),'-i','bg.png','-loop','1','-t',str(d),'-i','frame.png','-loop','1','-t',str(d),'-i','mask.png','-loop','1','-t',str(d),'-i',chip+'.png']
  if call: ins+=['-loop','1','-t',str(d),'-i',call+'.png']
  fc=(f"[0:v]trim={a}:{b},setpts=(PTS-STARTPTS)/{sp},fps=30,scale=-2:1440:flags=lanczos,crop=832:1440,format=rgba[v];"
      f"[3:v]format=gray[m];[v][m]alphamerge[vm];[1:v][2:v]overlay=0:0[bg];[bg][vm]overlay=124:240[c];"
      f"[4:v]format=rgba,fade=in:st=0:d=0.15:alpha=1[k];[c][k]overlay=0:0")
  if call: fc+=f"[c2];[5:v]format=rgba,fade=in:st=0.4:d=0.2:alpha=1[x];[c2][x]overlay=0:0:enable='gte(t,0.4)'"
  fc+=",format=yuv420p,setsar=1[o]"
  subprocess.run(['ffmpeg','-v','error','-y']+ins+['-filter_complex',fc,'-map','[o]','-t',str(d),'-r','30','-an','-c:v','libx264','-crf','18','-preset','fast',n+'.mp4'],check=True);print(n,d)
open('body.txt','w').write(''.join(f"file '{s[0]}.mp4'\n" for s in SEG))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','body.txt','-c','copy','body.mp4'],check=True);print('tot',tot)
