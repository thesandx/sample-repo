import numpy as np,wave
SR=48000;TOT=20.1;N=int(SR*TOT);rng=np.random.default_rng(3)
out=np.zeros(N)
def add(sig,t,g):
  i=int(t*SR);j=min(N,i+len(sig));out[i:j]+=sig[:j-i]*g
def lp(x,a):
  y=np.zeros_like(x);s=0
  for i,v in enumerate(x):s+=a*(v-s);y[i]=s
  return y
# pink-ish room tone
w=rng.standard_normal(N);room=lp(w,0.02);room/=np.abs(room).max();out+=room*10**(-50/20)
def tick(f=4200,d=0.03):
  n=int(d*SR);t=np.arange(n)/SR;e=np.exp(-t*180)
  return (rng.standard_normal(n)*0.6+np.sin(2*np.pi*f*t))*e
def tap():
  n=int(0.05*SR);t=np.arange(n)/SR;return (np.sin(2*np.pi*1800*t)*0.6+rng.standard_normal(n)*0.4)*np.exp(-t*120)
def whoosh(d=0.4):
  n=int(d*SR);t=np.arange(n)/SR;x=rng.standard_normal(n);env=np.sin(np.pi*t/d)**2
  y=lp(x,0.05)+lp(x,0.2)*np.linspace(0,1,n);return y/np.abs(y).max()*env
def chime():
  n=int(1.2*SR);t=np.arange(n)/SR;y=np.zeros(n)
  for f,a,dl in [(1318.5,1,0),(1975.5,.7,0.09)]:
    k=int(dl*SR);tt=t[:n-k];y[k:]+=a*np.sin(2*np.pi*f*tt)*np.exp(-tt*4)
  return y/np.abs(y).max()
for k in range(12): add(tick(),5.6+(0.2+0.09*k)/1.8,0.18)
add(tap(),6.406,0.35);add(whoosh(0.35),5.483,0.22);add(whoosh(0.3),15.383,0.14)
for k in range(5):add(tick(),7.287+0.089*k,0.12)
for k in range(5):add(tick(),7.894+0.081*k,0.12)
add(tap(),8.299,0.3)
for k in range(5):add(tap(),8.933+(13.3+0.38*k-13.1)/4.529,0.25)
add(tap(),10.633,0.3);add(chime(),12.183,0.16);add(tap(),14.388,0.3)
out=np.clip(out,-1,1)
def riffle(d=0.4):
  n=int(d*SR);y=np.zeros(n)
  for k in range(14):
    i=int(k*n/15);m=int(0.012*SR);t=np.arange(m)/SR
    y[i:i+m]+=rng.standard_normal(m)*np.exp(-t*260)*(0.6+0.4*rng.random())
  return lp(y,0.5)
def boom():
  n=int(0.7*SR);t=np.arange(n)/SR
  y=np.sin(2*np.pi*(55+60*np.exp(-t*18))*t)*np.exp(-t*5)+lp(rng.standard_normal(n),0.08)*np.exp(-t*25)*0.6
  return y/np.abs(y).max()
add(whoosh(0.45),0.84,0.22);add(whoosh(0.35),1.22,0.3);add(riffle(0.4),1.28,0.35);add(boom(),1.64,0.5);add(whoosh(0.25),2.06,0.15)
out=np.clip(out,-1,1)
with wave.open('sfx.wav','w') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(SR);f.writeframes((out*32767).astype(np.int16).tobytes())
