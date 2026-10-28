import cv2,numpy as np,sys,json
cap=cv2.VideoCapture(sys.argv[1]);R=[]
while True:
  ok,im=cap.read()
  if not ok:break
  f=im.astype(np.float32);m=((f[:,:,1]-np.maximum(f[:,:,0],f[:,:,2]))>50).astype(np.uint8)
  m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
  n,lab,st,_=cv2.connectedComponentsWithStats(m);k=1+np.argmax(st[1:,4]);m=(lab==k).astype(np.uint8)
  ys,xs=np.where(m);y0,y1,x0,x1=ys.min(),ys.max(),xs.min(),xs.max();hh=y1-y0;ww=x1-x0
  # right edge (never occluded) and top edge; left/bottom robust
  def edge(rows,side):
    P=[]
    for y in rows:
      r=np.where(m[y])[0]
      if len(r): P.append(((r.max() if side else r.min()),y))
    return np.array(P,float)
  rows=range(int(y0+.1*hh),int(y1-.1*hh),4)
  Rp=edge(rows,1);Lp=edge(rows,0)
  T=[];B=[]
  for x in list(range(int(x0+.12*ww),int(x0+.3*ww),3))+list(range(int(x1-.3*ww),int(x1-.12*ww),3)):
    c=np.where(m[:,x])[0]
    if len(c):T.append((x,c.min()));B.append((x,c.max()))
  T=np.array(T,float);B=np.array(B,float)
  def rob(P,ix,iy):
    a,b=np.polyfit(P[:,ix],P[:,iy],1)
    for _ in range(3):
      res=np.abs(P[:,iy]-(a*P[:,ix]+b));keep=res<max(2,np.median(res)*2.5)
      a,b=np.polyfit(P[keep,ix],P[keep,iy],1)
    return a,b
  # left edge: thumb pushes min x inward -> take points near the extreme (smallest x after line fit)
  l=rob(Lp,1,0);r=rob(Rp,1,0);t=rob(T,0,1);bo=rob(B,0,1)
  def X(v,h):
    a,c=v;d,e=h;y=(d*c+e)/(1-d*a);return [a*y+c,y]
  Q=[X(l,t),X(r,t),X(r,bo),X(l,bo)]
  # thumb: non-green pixels inside quad
  qm=np.zeros_like(m);cv2.fillConvexPoly(qm,np.int32(Q),1)
  qm=cv2.erode(qm,np.ones((7,7),np.uint8))
  th=((qm==1)&(m==0)).astype(np.uint8);th=cv2.morphologyEx(th,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
  tip=None
  if th.sum()>300:
    ys,xs=np.where(th);i=np.argmax(xs-0.6*ys);tip=[int(xs[i]),int(ys[i])]
    # also topmost
  R.append(dict(Q=Q,tip=tip,area=int(th.sum())))
json.dump(R,open(sys.argv[2],'w'))
print(len(R))
