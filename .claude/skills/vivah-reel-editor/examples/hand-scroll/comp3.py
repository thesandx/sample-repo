import cv2,numpy as np,subprocess,sys,json
S=1.5;Z=1.12
segs=[('c1.mp4','c1t.json',0,158),('c2.mp4','c2t.json',11,192)]
ch=cv2.imread('chrome.png',cv2.IMREAD_UNCHANGED).astype(np.float32);al=ch[:,:,3:]/255
src=np.float32([(0,0),(1080,0),(1080,2340),(0,2340)])
scap=cv2.VideoCapture('screen2.mp4')
out=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s','1080x1920','-r','24','-i','-','-c:v','libx264','-crf','16','-preset','medium','-pix_fmt','yuv420p',sys.argv[1]],stdin=subprocess.PIPE)
wm=cv2.imread('wmask.png',0)
rng=np.random.default_rng(2);n=0
cx,cy=555,935
M2=np.float32([[Z,0,540-cx*Z],[0,Z,960-cy*Z]])
for vf,tj,a,b in segs:
  T=json.load(open(tj));cap=cv2.VideoCapture(vf);cap.set(cv2.CAP_PROP_POS_FRAMES,a)
  for i in range(a,b):
    ok,im=cap.read();ok2,fr=scap.read()
    if not ok or not ok2: break
    im=cv2.inpaint(im,wm,6,cv2.INPAINT_TELEA)
    im=cv2.resize(im,(1080,1920),interpolation=cv2.INTER_CUBIC)
    f=im.astype(np.float32)
    g=f[:,:,1]-np.maximum(f[:,:,0],f[:,:,2])
    m=np.clip((g-25)/60,0,1);m=cv2.GaussianBlur(m,(3,3),0)[:,:,None]
    lim=np.maximum(f[:,:,0],f[:,:,2])*1.03
    f[:,:,1]=np.where(m[:,:,0]>0.01,np.minimum(f[:,:,1],lim),f[:,:,1])
    # also despill edge halo
    edge=cv2.dilate((m[:,:,0]>0.05).astype(np.uint8),np.ones((7,7),np.uint8))>0
    f[:,:,1]=np.where(edge,np.minimum(f[:,:,1],lim),f[:,:,1])
    scr=np.full((2340,1080,3),255,np.float32)
    scr[150:150+1839]=cv2.resize(fr,(1080,1839),interpolation=cv2.INTER_AREA)
    scr=scr*(1-al)+ch[:,:,:3]*al
    Q=np.float32(T[i]['Q'])*S
    H=cv2.getPerspectiveTransform(src,Q)
    w=cv2.warpPerspective(scr,H,(1080,1920),flags=cv2.INTER_AREA)
    w=cv2.GaussianBlur(w,(0,0),0.6)*0.92+np.float32([6,12,20])
    c=f*(1-m)+w*m
    c=cv2.warpAffine(c,M2,(1080,1920),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT)
    c+=rng.normal(0,2.5,c.shape[:2])[:,:,None]
    out.stdin.write(np.clip(c,0,255).astype(np.uint8).tobytes());n+=1
out.stdin.close();out.wait();print(n)
