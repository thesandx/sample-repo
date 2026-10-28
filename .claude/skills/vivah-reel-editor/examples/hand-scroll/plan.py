import json
c1=json.load(open('c1t.json'));c2=json.load(open('c2t.json'))
css=lambda t:(t[0]*390/400, t[1]*0.9824-54.2)
A=[]
OFF=6.15
A.append([1.25,'tap',*css(c1[30]['tip'])])
A.append([4.0,'scroll',700,0.95])
def scratch(clip,f0,f1,off,dx=0,lo=0,hi=390):
  t=next(clip[f]['tip'] for f in range(f0,f1) if clip[f]['tip']);x,y=css(t);A.append([f0/24+off-0.01,'move',min(hi,max(lo,x+dx)),y]);A.append([f0/24+off,'down',None,None])
  for f in range(f0,f1+1):
    t=clip[f]['tip']
    if not t: continue
    x,y=css(t);x=min(hi,max(lo,x+dx))
    for k in range(2):
      A.append([(f+k/2)/24+off,'move',x+(22 if (f+k)%2 else -22),y+(-10 if f%2 else 10)])
  A.append([f1/24+off+0.02,'up',None,None])
scratch(c1,117,152,0)
A.append([6.45,'reveal','day,month',None])
scratch(c2,12,26,OFF,dx=70,lo=262,hi=332)
A.append([OFF+27/24,'reveal','year',None])
for f0,f1,y in [(24,36,1300),(42,56,1880),(69,80,2480),(87,101,3120),(111,141,3720),(146,156,4950)]:
  d=(f1-f0)/24+(0.9 if f1==156 else 0.45)
  A.append([f0/24+OFF,'scroll',y,d])
A.sort(key=lambda a:a[0]);json.dump(A,open('plan.json','w'));print(len(A),A[:3],A[-3:])
