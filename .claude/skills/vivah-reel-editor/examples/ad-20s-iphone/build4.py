import subprocess
def run(c):subprocess.run(c,check=True)
V=['-c:v','libx264','-crf','16','-preset','fast','-r','30','-an','-pix_fmt','yuv420p']
CR='../hd/create.mp4';SI='../rec/site.mp4';HO='home.mp4'
PF=("fps=30,scale=1150:2044:flags=lanczos,crop=1080:1920:'35+12*sin(t*1.7)+6*sin(t*3.9)':'62+10*sin(t*1.3+1)+5*sin(t*4.4)',"
    "colorbalance=rs=0.03:bs=-0.03:rm=0.02:bm=-0.02,eq=saturation=0.95:contrast=1.03,noise=alls=7:allf=t,setsar=1")
# g01: Priya 0-0.95, cash cutaway 0.95-2.2, Priya 2.2-3.85
run(['ffmpeg','-v','error','-y','-i','a1.mp4','-framerate','30','-i','cut/%03d.png','-filter_complex',
 f"[0:v]trim=0:3.85,setpts=PTS-STARTPTS,{PF}[p];[p]split[p1][p2];[p1]trim=0:0.9667,setpts=PTS-STARTPTS[a];[p2]trim=2.2333:3.85,setpts=PTS-STARTPTS[c];"
 "[1:v]fps=30,format=yuv420p,setsar=1,noise=alls=5:allf=t[b];[a][b][c]concat=n=3:v=1[o]",'-map','[o]']+V+['g01.mp4'])
def page(src,a,b,sp,bar,out,extra=()):
  d=round((b-a)/sp,3)
  fc=(f"[0:v]trim={a}:{b},setpts=(PTS-STARTPTS)/{sp},fps=30,scale=1080:-2:flags=lanczos,crop=1080:min(ih\\,1839):0:0,"
      f"pad=1080:2340:0:150:white[p];[1:v]format=rgba[b];[p][b]overlay=0:0[q0]")
  ins=['-i',src,'-loop','1','-t',str(d),'-i',bar];last='q0'
  for i,(png,s,e) in enumerate(extra):
    ins+=['-loop','1','-t',str(d),'-i',png]
    fc+=f";[{last}][{i+2}:v]overlay=0:0:enable='between(t,{s},{e})'[q{i+1}]";last=f'q{i+1}'
  fc+=f";[{last}]setsar=1[o]"
  run(['ffmpeg','-v','error','-y']+ins+['-filter_complex',fc,'-map','[o]','-t',str(d)]+V+[out])
S=[]
run(['ffmpeg','-v','error','-y','-framerate','30','-i','typ2/%03d.png','-vf','setpts=PTS/1.8,fps=30,format=yuv420p,setsar=1','-t','1.0']+V+['s02.mp4']);S.append('s02.mp4')
page(HO,2.9,3.533,1.0,'b2_bar_home.png','s03.mp4',[('b2_bar_p20.png',0,0.1),('b2_bar_p45.png',0.1,0.2),('b2_bar_p70.png',0.2,0.3),('b2_bar_p90.png',0.3,0.4)])
run(['ffmpeg','-v','error','-y','-i','s03.mp4','-filter_complex','[0:v]split=3[a][b][c];[b]crop=760:150:160:380,boxblur=14:2[bb];[c]crop=300:90:560:1465,boxblur=12:2[cc];[a][bb]overlay=160:380[x];[x][cc]overlay=560:1465']+V+['s03b.mp4']);import os;os.replace('s03b.mp4','s03.mp4');S.append('s03.mp4')
for n,(a,b,sp) in enumerate([(3.5,8.1,4.208),(8.1,10.1,3.294),(13.1,16.4,4.529),(17.9,21.94,4.158),(21.94,26.5,3.04),(27.0,28.55,1.0)]):
  o=f's1{n}.mp4';page(CR,a,b,sp,'b2_bar_home.png',o);S.append(o)
page(SI,0.6,4.75,2.306,'b2_bar_inv.png','s20.mp4');S.append('s20.mp4')
open('scr.txt','w').write(''.join(f"file '{s}'\n" for s in S))
run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','scr.txt','-c','copy','scr.mp4'])
# phone composite
D=round(sum(float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout) for f in S),3);print('D',D)
fc=("[0:v]scale=660:1430:flags=lanczos,format=rgba[s];[3:v]format=gray,crop=660:1430:210:318[m];[s][m]alphamerge[sm];"
    "[1:v][sm]overlay=210:318[x];[x][2:v]overlay=0:0,"
    f"scale=w='trunc(1080*(1+0.16*pow(max(0\\,1-t/0.3)\\,2)+0.03*t/{D})/2)*2':h=-2:eval=frame:flags=bicubic,"
    "crop=1080:1920:(iw-1080)/2:(ih-1920)*0.52,setsar=1[o]")
run(['ffmpeg','-v','error','-y','-i','scr.mp4','-loop','1','-i','bg.png','-loop','1','-i','frame.png','-loop','1','-i','smask.png',
     '-filter_complex',fc,'-map','[o]','-t',str(D)]+V+['gphone.mp4'])
run(['ffmpeg','-v','error','-y','-i','a4.mp4','-filter_complex',f"[0:v]trim=0:3.767,setpts=PTS-STARTPTS,{PF}[o]",'-map','[o]']+V+['g21.mp4'])
run(['ffmpeg','-v','error','-y','-loop','1','-t','0.8','-i','logo.png','-vf',"fps=30,format=yuv420p,setsar=1,fade=in:st=0:d=0.2,zoompan=z='1+0.0008*on':d=1:s=1080x1920:fps=30"]+V+['g22.mp4'])
open('segs.txt','w').write("file 'g01.mp4'\nfile 'gphone.mp4'\nfile 'g21.mp4'\nfile 'g22.mp4'\n")
run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','segs.txt','-c','copy','base.mp4'])
