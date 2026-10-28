import subprocess
TOT=21.233;P0=3.867;D=12.766
def mp(t,X,Y):
  z=1+0.03*(t-P0)/D
  return int(X*z-(1080*z-1080)/2-37),int(Y*z-(1920*z-1920)*0.52-37)
dots=[(5.317,798,1595),(8.25,503,1265),(15.15,503,1320)]
ins=['-i','base.mp4','-i','cap.mov','-ss','0','-t','5.1','-i','a2.mp4','-t','4.0','-i','a3.mp4','-loop','1','-i','cmask.png','-loop','1','-i','cshadow.png','-loop','1','-i','dot.png']
fc=("[2:v]setpts=PTS-STARTPTS+6.9/TB,fps=30,crop=720:1056:0:0,scale=280:410,format=rgba[c2];"
    "[3:v]setpts=PTS-STARTPTS+12.0/TB,fps=30,crop=720:1056:0:0,scale=280:410,format=rgba[c3];"
    "[4:v]format=gray,split=2[m2][m3];[c2][m2]alphamerge[k2];[c3][m3]alphamerge[k3];"
    "[0:v][5:v]overlay=734:1120:enable='between(t,6.9,16.0)'[b0];"
    "[b0][k2]overlay=764:1150:eof_action=pass:enable='between(t,6.9,12.0)'[b1];"
    "[b1][k3]overlay=764:1150:eof_action=pass:enable='between(t,12.0,16.0)'[b2];"
    "[6:v]scale=74:74,format=rgba,split=3[d0][d1][d2];")
last='b2'
for i,(t,X,Y) in enumerate(dots):
  x,y=mp(t,X,Y)
  fc+=f"[{last}][d{i}]overlay={x}:{y}:enable='between(t,{t},{t+0.28})'[e{i}];";last=f'e{i}'
fc+=f"[{last}][1:v]overlay=0:0,format=yuv420p,setsar=1[o]"
subprocess.run(['ffmpeg','-v','error','-y']+ins+['-filter_complex',fc,'-map','[o]','-t',str(TOT),'-c:v','libx264','-crf','17','-preset','medium','-r','30','vid.mp4'],check=True)
# audio
af=("[0:a]atrim=0:3.85,asetpts=PTS-STARTPTS,loudnorm=I=-15:TP=-1.5[v1];"
    "[1:a]atrim=0:5.0,asetpts=PTS-STARTPTS,loudnorm=I=-15:TP=-1.5,adelay=6933|6933[v2];"
    "[2:a]atrim=0:4.0,asetpts=PTS-STARTPTS,loudnorm=I=-15:TP=-1.5,adelay=12000|12000[v3];"
    "[3:a]atrim=0:3.75,asetpts=PTS-STARTPTS,loudnorm=I=-15:TP=-1.5,adelay=16633|16633[v4];"
    "[4:a]aformat=channel_layouts=stereo,volume=1.6[s];"
    "[v1][v2][v3][v4][s]amix=inputs=5:normalize=0:duration=longest,alimiter=limit=0.9,aresample=48000[a]")
subprocess.run(['ffmpeg','-v','error','-y','-i','a1.mp4','-i','a2.mp4','-i','a3.mp4','-i','a4.mp4','-i','sfx.wav','-filter_complex',af,'-map','[a]','-t',str(TOT),'-ar','48000','aud.wav'],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-i','vid.mp4','-i','aud.wav','-c:v','copy','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart','ad20v2.mp4'],check=True)
