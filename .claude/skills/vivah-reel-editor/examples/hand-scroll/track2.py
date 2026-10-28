import cv2,numpy as np,sys,json
R=json.load(open(sys.argv[2]))
Qs=np.array([r['Q'] for r in R],float)
# temporal smoothing of corners (centered moving average, 5 frames)
k=np.ones(5)/5;S=Qs.copy()
for a in range(4):
  for b in range(2):
    S[:,a,b]=np.convolve(np.pad(Qs[:,a,b],2,mode='edge'),k,'valid')
W,H=400,860;dst=np.float32([(0,0),(W,0),(W,H),(0,H)])
cap=cv2.VideoCapture(sys.argv[1]);out=[];tmpl=None
for i in range(len(R)):
  ok,im=cap.read();f=im.astype(np.float32)
  m=((f[:,:,1]-np.maximum(f[:,:,0],f[:,:,2]))>50).astype(np.uint8)
  M=cv2.getPerspectiveTransform(np.float32(S[i]),dst)
  c=cv2.warpPerspective(m,M,(W,H))
  if tmpl is None: tmpl=cv2.erode(c,np.ones((5,5),np.uint8))
  th=((tmpl==1)&(c==0)).astype(np.uint8);th=cv2.morphologyEx(th,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
  tip=None;a=int(th.sum())
  if a>400:
    n,lab,st,_=cv2.connectedComponentsWithStats(th);kk=1+np.argmax(st[1:,4]);ys,xs=np.where(lab==kk)
    j=np.argmax(xs);tip=[int(xs[j]),int(ys[j])]
  out.append(dict(Q=S[i].tolist(),tip=tip,area=a))
json.dump(out,open(sys.argv[3],'w'))
for i in range(0,len(out),3): print(i,out[i]['tip'],out[i]['area'],end=' | ')
