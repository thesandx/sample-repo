import numpy as np,wave
SR=48000;TOT=21.2;N=int(SR*TOT);rng=np.random.default_rng(3)
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
for k in range(12): add(tick(),3.867+0.2+0.09*k,0.18)
add(tap(),5.317,0.35);add(whoosh(0.35),3.75,0.22);add(whoosh(0.3),16.5,0.14)
for k in range(5):add(tick(),7.0+0.11*k,0.12)
for k in range(5):add(tick(),7.75+0.1*k,0.12)
add(tap(),8.25,0.3)
for k in range(5):add(tap(),9.067+(13.3+0.38*k-13.1)/3.667,0.25)
add(tap(),11.167,0.3);add(chime(),12.72,0.16);add(tap(),15.15,0.3)
out=np.clip(out,-1,1)
with wave.open('sfx.wav','w') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(SR);f.writeframes((out*32767).astype(np.int16).tobytes())
