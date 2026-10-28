import numpy as np, wave
SR=48000; D=18.2; out=np.zeros(int(SR*D)); rng=np.random.default_rng(1)
def add(t,sig,g):
  i=int(t*SR); n=min(len(sig),len(out)-i); out[i:i+n]+=sig[:n]*g
def env(n,a,d): x=np.arange(n)/SR; return np.minimum(1,x/a)*np.exp(-x/d)
def tone(f,dur,a=0.002,d=0.08,f2=None):
  n=int(dur*SR); ff=np.linspace(f,f2 or f,n); ph=2*np.pi*np.cumsum(ff)/SR
  return np.sin(ph)*env(n,a,d)
def pop(f=900): return tone(f,0.12,0.001,0.035,f*1.6)
def tick(): return tone(1800,0.15,0.001,0.05)+0.6*tone(2700,0.15,0.001,0.04)
def thump(): return tone(140,0.35,0.002,0.09,55)
def whoosh(dur=0.35):
  n=int(dur*SR); w=rng.standard_normal(n); k=np.hanning(n)
  y=np.convolve(w,np.ones(12)/12,'same')-np.convolve(w,np.ones(80)/80,'same')
  return y*k*2.5
def chime(fs=(1047,1319,1568)): return sum(tone(f,1.2,0.003,0.35)*(0.8**i) for i,f in enumerate(fs))
add(0,thump(),0.9); add(0,whoosh(0.25),0.5)
for t in (0.12,0.28): add(t,pop(700),0.35)
add(0.5,pop(1000),0.5); add(0.5,thump(),0.4); add(0.9,pop(1300),0.3)
I0,IT=2.0,2.2
for i in range(5):
  add(I0+i*IT-0.08,whoosh(0.3),0.45); add(I0+i*IT+0.05,pop(800+i*120),0.35); add(I0+i*IT+1.6,tick(),0.35)
add(2.65,pop(1500),0.3); add(3.0,whoosh(0.2),0.3)
PR=I0+5*IT
add(PR-0.25,whoosh(0.4),0.5); add(PR+0.6,whoosh(0.25),0.35)
add(PR+0.95,thump(),0.8); add(PR+0.95,chime((1568,2093)),0.25); add(PR+1.5,pop(1200),0.3)
EN=PR+2.4
add(EN-0.2,whoosh(0.35),0.4); add(EN,chime(),0.35); add(EN+0.45,pop(1100),0.35); add(EN+1.0,pop(1400),0.3)
out=out/np.max(np.abs(out))*0.5
w=wave.open('sfx.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
