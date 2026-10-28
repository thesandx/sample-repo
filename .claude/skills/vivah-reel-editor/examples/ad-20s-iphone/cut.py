from PIL import Image,ImageChops
import numpy as np,os,math
os.makedirs('cut',exist_ok=True)
W,H=1080,1920
card=Image.open('card.png').convert('RGB');fan=Image.open('fan.png')
def zoom(im,z,cx=540,cy=900):
  w,h=int(W*z),int(H*z);t=im.resize((w,h),Image.BILINEAR)
  x=int(cx*z-cx);y=int(cy*z-cy);return t.crop((x,y,x+W,y+H))
def zblur(im,z,amt):
  if amt<0.005:return zoom(im,z)
  acc=None;n=6
  for k in range(n):
    f=np.asarray(zoom(im,z*(1+amt*k/n)),dtype=np.float32);acc=f if acc is None else acc+f
  return Image.fromarray((acc/n).astype(np.uint8))
def ease(t):t=min(1,max(0,t));return 1-(1-t)**3
def place_fan(base,p,s,rot,blur):
  # p: 0..1 progress of flight
  acc=None;n=5 if blur else 1
  for k in range(n):
    q=max(0,p-blur*k/n)
    e=ease(q);sc=s*(1.7-0.7*e);r=rot*(1-e)
    f=fan.resize((int(fan.size[0]*sc),int(fan.size[1]*sc)),Image.BILINEAR).rotate(r,expand=True,resample=Image.BILINEAR)
    cx=540+650*(1-e);cy=940-900*(1-e)
    L=base.copy();L.paste(f,(int(cx-f.size[0]/2),int(cy-f.size[1]/2)),f)
    a=np.asarray(L,dtype=np.float32);acc=a if acc is None else acc+a
  return Image.fromarray((acc/n).astype(np.uint8))
N=38
for i in range(N):
  t=i/30
  zc=1.22-0.14*ease(t/1.25)
  if i<12:
    fr=zblur(card,zc,0.12*max(0,1-i/6))
  else:
    bg=zoom(card,zc);dark=0.42+0.58*max(0,1-(i-12)/6)
    bg=Image.fromarray((np.asarray(bg,dtype=np.float32)*dark).astype(np.uint8))
    p=min(1,(i-12)/9);bump=1+0.04*math.exp(-max(0,i-21)/2.0) if i>=21 else 1
    fr=place_fan(bg,p,1.12*bump,-35,0.25 if p<1 else 0)
  a=np.asarray(fr,dtype=np.float32)
  if i>=24:
    lum=a.mean(2,keepdims=True)
    if i<30:
      k=(i-23)/6;red=a*np.array([1.0,0.35,0.35])
      a=a*(1-k)+red*k
    else:
      r=255*(lum/255)**1.5*1.7;red=np.concatenate([r+12,r*0.08,r*0.1],2)
      a=red
    # shake
    dx=int(8*math.sin(i*2.1));dy=int(6*math.cos(i*1.7));a=np.roll(a,(dy,dx),(0,1))
  Image.fromarray(np.clip(a,0,255).astype(np.uint8)).save(f'cut/{i:03d}.png')
