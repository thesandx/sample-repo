import subprocess
def run(c):subprocess.run(c,check=True)
V=['-c:v','libx264','-crf','18','-preset','fast','-r','30','-an']
def full(clip,dur,caps,cmt_from,out):
  # caps: [(png,start,end)]
  ins=['-i',clip]+sum([['-loop','1','-t',str(dur),'-i',p] for p,_,_ in caps],[])+['-loop','1','-t',str(dur),'-i','cmt.png']
  fc=f"[0:v]trim=0:{dur},setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,fps=30,format=rgba[b0];"
  last='b0'
  for i,(p,s,e) in enumerate(caps):
    fc+=f"[{i+1}:v]format=rgba,fade=in:st={s}:d=0.12:alpha=1[c{i}];[{last}][c{i}]overlay=0:0:enable='between(t,{s},{e})'[b{i+1}];";last=f'b{i+1}'
  n=len(caps)+1
  fc+=f"[{n}:v]format=rgba,fade=in:st={cmt_from}:d=0.2:alpha=1[cm];[{last}][cm]overlay=0:0:enable='gte(t,{cmt_from})',format=yuv420p,setsar=1[o]"
  run(['ffmpeg','-v','error','-y']+ins+['-filter_complex',fc,'-map','[o]','-t',str(dur)]+V+[out])
full('t1.mp4',5.8,[('h1.png',0,2.3),('h2.png',2.3,4.5),('h3.png',4.5,5.8)],2.3,'hook.mp4')
full('t5.mp4',5.8,[('o1.png',0,3.1),('o2.png',3.1,5.8)],3.1,'outro.mp4')
# body with face bubbles
B=[('t2.mp4',0.0,4.5),('t3.mp4',6.0,5.7),('t4.mp4',13.15,5.5)]
ins=['-i','body.mp4']
fc="[0:v]format=rgba[b0];";last='b0'
for i,(c,st,d) in enumerate(B):
  ins+=['-i',c]
  fc+=(f"[{i+1}:v]trim=0:{d},setpts=PTS-STARTPTS+{st}/TB,crop=720:1056:0:0,scale=300:440,format=rgba[f{i}];"
       f"[{len(B)+1}:v]format=gray,split=1[m{i}];[f{i}][m{i}]alphamerge[fm{i}];"
       f"[{last}][fm{i}]overlay=740:1100:eof_action=pass:enable='between(t,{st},{st+d})'[r{i}];"
       f"[r{i}][{len(B)+2}:v]overlay=730:1090:enable='between(t,{st},{st+d})'[b{i+1}];")
  last=f'b{i+1}'
ins+=['-loop','1','-i','rr.png','-loop','1','-i','rring.png']
fc+=f"[{last}]format=yuv420p,setsar=1[o]"
run(['ffmpeg','-v','error','-y']+ins+['-filter_complex',fc,'-map','[o]','-t','26.833333']+V+['bodyf.mp4'])
run(['ffmpeg','-v','error','-y','-loop','1','-t','3','-i','end.png','-vf','fps=30,format=yuv420p,setsar=1,fade=in:st=0:d=0.25']+V+['endc.mp4'])
open('all.txt','w').write("file 'hook.mp4'\nfile 'bodyf.mp4'\nfile 'outro.mp4'\nfile 'endc.mp4'\n")
run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','all.txt','-c','copy','vid.mp4'])
# audio
H=5.8;BD=26.833333;O=H+BD
A=[('t1.mp4',0,0,5.8),('t2.mp4',H+0,0,4.5),('t3.mp4',H+6.0,0,5.7),('t4.mp4',H+13.15,0,5.5),('t5.mp4',O,0,5.8)]
ins=sum([['-i',a[0]] for a in A],[]);fc=''
for i,(c,st,_,d) in enumerate(A):
  fc+=f"[{i}:a]atrim=0:{d},asetpts=PTS-STARTPTS,afade=t=out:st={d-0.25}:d=0.25,loudnorm=I=-14:TP=-1.5,aresample=48000,adelay={int(st*1000)}|{int(st*1000)}[a{i}];"
fc+=''.join(f'[a{i}]' for i in range(len(A)))+f"amix=inputs={len(A)}:normalize=0,apad[a]"
TOT=H+BD+5.8+3
run(['ffmpeg','-v','error','-y']+ins+['-filter_complex',fc,'-map','[a]','-t',str(TOT),'-c:a','pcm_s16le','aud.wav'])
run(['ffmpeg','-v','error','-y','-i','vid.mp4','-i','aud.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','160k','-shortest','tutorial_hd2.mp4'])
