import cv2,numpy as np,subprocess,sys,math
S=1080/941
bg=cv2.imread('still2.png');bg=cv2.resize(bg,(1080,round(1672*S)),interpolation=cv2.INTER_LANCZOS4)[:1920]
if bg.shape[0]<1920: bg=cv2.copyMakeBorder(bg,0,1920-bg.shape[0],0,0,cv2.BORDER_REPLICATE)
Q=np.float32([(275.9,388.2),(678.6,383.7),(693.4,1232.7),(290.5,1238.6)])*S
f=bg.astype(np.float32)
g=f[:,:,1]-np.maximum(f[:,:,0],f[:,:,2])
a=np.clip((g-25)/70,0,1)
a=cv2.GaussianBlur(a,(3,3),0)[:,:,None]
# despill the hand/frame edge
spill=np.minimum(f[:,:,1],np.maximum(f[:,:,0],f[:,:,2])*1.02)
bgd=f.copy();bgd[:,:,1]=np.where(a[:,:,0]>0,spill,f[:,:,1])
ch=cv2.imread('chrome.png',cv2.IMREAD_UNCHANGED).astype(np.float32)
H=cv2.getPerspectiveTransform(np.float32([(0,0),(1080,0),(1080,2340),(0,2340)]),Q)
cap=cv2.VideoCapture('screen.mp4')
out=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s','1080x1920','-r','30','-i','-','-c:v','libx264','-crf','16','-preset','medium','-pix_fmt','yuv420p',sys.argv[1]],stdin=subprocess.PIPE)
rng=np.random.default_rng(1);i=0
while True:
  ok,fr=cap.read()
  if not ok: break
  scr=np.full((2340,1080,3),255,np.float32)
  scr[150:150+1839]=cv2.resize(fr,(1080,1839),interpolation=cv2.INTER_AREA)
  al=ch[:,:,3:]/255;scr=scr*(1-al)+ch[:,:,:3]*al
  w=cv2.warpPerspective(scr,H,(1080,1920),flags=cv2.INTER_AREA)
  w=w*0.93+np.float32([6,12,20])  # warm, slightly dimmer like ambient
  c=bgd*(1-a)+w*a
  t=i/30
  ang=0.5*math.sin(t*1.3)+0.25*math.sin(t*2.9+1)
  dx=6*math.sin(t*1.1+.5)+3*math.sin(t*3.3);dy=5*math.sin(t*0.9)+2.5*math.sin(t*2.6+2)
  M=cv2.getRotationMatrix2D((540,900),ang,1.045);M[0,2]+=dx;M[1,2]+=dy
  c=cv2.warpAffine(c,M,(1080,1920),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
  c+=rng.normal(0,3,c.shape[:2])[:,:,None]
  out.stdin.write(np.clip(c,0,255).astype(np.uint8).tobytes());i+=1
out.stdin.close();out.wait();print(i)
