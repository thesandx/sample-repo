import subprocess
TOT=21.2
dots=[(5.30,915,1795),(8.25,480,1650),(15.15,480,1740)]
ins=['-i','base.mp4','-i','cap.mov','-ss','0','-t','5.1','-i','a2.mp4','-t','4.0','-i','a3.mp4','-loop','1','-i','cmask.png','-loop','1','-i','cshadow.png','-loop','1','-i','dot.png']
fc=("[2:v]setpts=PTS-STARTPTS+6.9/TB,fps=30,crop=720:1056:0:0,scale=280:410,format=rgba[c2];"
    "[3:v]setpts=PTS-STARTPTS+12.0/TB,fps=30,crop=720:1056:0:0,scale=280:410,format=rgba[c3];"
    "[4:v]format=gray,split=2[m2][m3];[c2][m2]alphamerge[k2];[c3][m3]alphamerge[k3];"
    "[0:v][5:v]overlay=734:1120:enable='between(t,6.9,16.0)'[b0];"
    "[b0][k2]overlay=764:1150:eof_action=pass:enable='between(t,6.9,12.0)'[b1];"
    "[b1][k3]overlay=764:1150:eof_action=pass:enable='between(t,12.0,16.0)'[b2];"
    "[6:v]format=rgba,split=3[d0][d1][d2];")
last='b2'
for i,(t,x,y) in enumerate(dots):
  fc+=f"[{last}][d{i}]overlay={x}:{y}:enable='between(t,{t},{t+0.28})'[e{i}];";last=f'e{i}'
fc+=f"[{last}][1:v]overlay=0:0,format=yuv420p,setsar=1[o]"
subprocess.run(['ffmpeg','-v','error','-y']+ins+['-filter_complex',fc,'-map','[o]','-t',str(TOT),'-c:v','libx264','-crf','17','-preset','medium','-r','30','vid.mp4'],check=True)
