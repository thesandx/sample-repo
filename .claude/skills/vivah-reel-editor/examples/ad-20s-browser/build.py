import subprocess,json
def run(c):subprocess.run(c,check=True)
V=['-c:v','libx264','-crf','17','-preset','fast','-r','30','-an','-pix_fmt','yuv420p']
CR='../hd/create.mp4';SI='../rec/site.mp4';HO='home.mp4'
def priya_full(src,a,d,out):
  # slight overscale + handheld wobble + warm grade + grain
  fc=(f"[0:v]trim={a}:{a+d},setpts=PTS-STARTPTS,fps=30,scale=1150:2044:flags=lanczos,"
      f"crop=1080:1920:'35+12*sin(t*1.7)+6*sin(t*3.9)':'62+10*sin(t*1.3+1)+5*sin(t*4.4)',"
      f"colorbalance=rs=0.03:bs=-0.03:rm=0.02:bm=-0.02,eq=saturation=0.95:contrast=1.03,noise=alls=7:allf=t,setsar=1[o]")
  run(['ffmpeg','-v','error','-y','-i',src,'-filter_complex',fc,'-map','[o]','-t',str(d)]+V+[out])
def page(src,a,b,sp,bar,out,extra=None):
  d=round((b-a)/sp,3)
  fc=(f"[0:v]trim={a}:{b},setpts=(PTS-STARTPTS)/{sp},fps=30,scale=1080:-2:flags=lanczos,crop=1080:1670:0:0,"
      f"pad=1080:1920:0:250:white[p];[1:v]format=rgba[b];[p][b]overlay=0:0")
  ins=['-i',src,'-loop','1','-t',str(d),'-i',bar]
  if extra:
    for i,(png,s,e) in enumerate(extra):
      ins+=['-loop','1','-t',str(d),'-i',png];fc+=f"[x{i}];[x{i}]" if False else ''
    fc+="[q0]";last='q0'
    for i,(png,s,e) in enumerate(extra):
      fc+=f";[{last}][{i+2}:v]overlay=0:0:enable='between(t,{s},{e})'[q{i+1}]";last=f'q{i+1}'
    fc=fc+f";[{last}]setsar=1[o]"
  else: fc+=",setsar=1[o]"
  run(['ffmpeg','-v','error','-y']+ins+['-filter_complex',fc,'-map','[o]','-t',str(d)]+V+[out]);return d
segs=[]
priya_full('a1.mp4',0,3.85,'g01.mp4');segs.append('g01.mp4')
run(['ffmpeg','-v','error','-y','-framerate','30','-i','typ/%03d.png','-vf','format=yuv420p,setsar=1']+V+['g02.mp4']);segs.append('g02.mp4')
page(HO,2.4,3.65,1.0,'bar_home.png','g03.mp4',[('bar_p20.png',0,0.15),('bar_p45.png',0.15,0.3),('bar_p70.png',0.3,0.45),('bar_p90.png',0.45,0.6)]);segs.append('g03.mp4')
for n,(a,b,sp) in enumerate([(3.5,8.1,3.407),(8.1,10.1,2.667),(13.1,16.4,3.667),(17.9,21.94,3.367),(21.94,26.5,3.04),(27.0,28.55,1.0)]):
  o=f'g1{n}.mp4';page(CR,a,b,sp,'bar_home.png',o);segs.append(o)
page(SI,0.6,4.75,1.73,'bar_inv.png','g20.mp4');segs.append('g20.mp4')
priya_full('a4.mp4',0,3.75,'g21.mp4');segs.append('g21.mp4')
run(['ffmpeg','-v','error','-y','-loop','1','-t','0.8','-i','logo.png','-vf',"fps=30,format=yuv420p,setsar=1,fade=in:st=0:d=0.2,zoompan=z='1+0.0008*on':d=1:s=1080x1920:fps=30"]+V+['g22.mp4']);segs.append('g22.mp4')
open('segs.txt','w').write(''.join(f"file '{s}'\n" for s in segs))
run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','segs.txt','-c','copy','base.mp4'])
