from PIL import Image,ImageDraw,ImageFilter
import numpy as np
W,H=1080,1920
SW,SH=660,1430;BZ=18;OX,OY=192,300;SX,SY=OX+BZ,OY+BZ;OW,OH=SW+2*BZ,SH+2*BZ
R_IN=92;R_OUT=R_IN+BZ
# background gradient
y=np.linspace(0,1,H)[:,None]
stops=[(0,(70,28,48)),(0.38,(118,62,84)),(0.68,(186,118,88)),(1,(232,166,60))]
img=np.zeros((H,W,3))
for c in range(3):
  img[:,:,c]=np.interp(y,[s[0] for s in stops],[s[1][c] for s in stops])
xx,yy=np.meshgrid(np.linspace(-1,1,W),np.linspace(-1,1,H))
v=1-0.22*np.clip(xx**2*0.8+(yy*0.9)**2-0.2,0,1)
img*=v[:,:,None]
rng=np.random.default_rng(1);img+=rng.normal(0,2.2,img.shape)
bg=Image.fromarray(np.clip(img,0,255).astype(np.uint8))
# shadow
sh=Image.new('L',(W,H),0);d=ImageDraw.Draw(sh);d.rounded_rectangle([OX+10,OY+40,OX+OW-10,OY+OH+40],R_OUT,fill=150)
sh=sh.filter(ImageFilter.GaussianBlur(38))
bg=Image.composite(Image.new('RGB',(W,H),(20,6,12)),bg,sh)
bg.save('bg.png')
# frame overlay at 2x supersample
S=2
fr=Image.new('RGBA',(W*S,H*S),(0,0,0,0));d=ImageDraw.Draw(fr)
def rr(b,r,**k):d.rounded_rectangle([v*S for v in b],r*S,**k)
# side buttons
for (x0,y0,x1,y1) in [(OX-5,OY+250,OX+2,OY+310),(OX-5,OY+370,OX+2,OY+470),(OX-5,OY+500,OX+2,OY+600),(OX+OW-2,OY+400,OX+OW+5,OY+560)]:
  rr((x0,y0,x1,y1),3,fill=(58,56,60,255))
rr((OX,OY,OX+OW,OY+OH),R_OUT,fill=(70,68,72,255))
rr((OX+3,OY+3,OX+OW-3,OY+OH-3),R_OUT-3,fill=(12,12,14,255))
rr((SX,SY,SX+SW,SY+SH),R_IN,fill=(0,0,0,0))
# dynamic island
iw,ih=212,62;ix=SX+SW//2-iw//2;iy=SY+16
rr((ix,iy,ix+iw,iy+ih),ih//2,fill=(0,0,0,255))
fr=fr.resize((W,H),Image.LANCZOS);fr.save('frame.png')
m=Image.new('L',(W*S,H*S),0);ImageDraw.Draw(m).rounded_rectangle([SX*S,SY*S,(SX+SW)*S,(SY+SH)*S],R_IN*S,fill=255)
m.resize((W,H),Image.LANCZOS).save('smask.png')
prev=bg.copy();prev.paste(Image.new('RGB',(SW,SH),(255,255,255)),(SX,SY));prev.paste(fr,(0,0),fr);prev.save('pchk.png')
print(SX,SY,SW,SH)
