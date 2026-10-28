import numpy as np, wave
SR=48000; D=26.4; out=np.zeros(int(SR*D)); rng=np.random.default_rng(1)
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
S=[0,4.6,9.9,16.4,21.6]
for c in [1.28,S[1],S[1]+2.98,S[2],S[2]+3.0,S[3],S[3]+3.24,S[4]]: add(c-0.05,whoosh(0.22),0.35)
add(0,thump(),0.8)
for t in [0,1.28,S[1]+1.46,S[3]+0.86,S[3]+3.24,S[4]]:
  for k in range(4): add(t+k*0.04,pop(900+k*150),0.16)
for t in [S[1]+0.2,S[1]+4.76,S[2]+0.34,S[3]+2.1,S[4]+1.84]: add(t,pop(1200),0.35)
add(S[1]+1.46,whoosh(0.3),0.35); add(S[1]+4.6,whoosh(0.15),0.3)
add(S[2]+3.0,whoosh(0.4),0.5)
for t in [S[2]+4.0,S[2]+4.86]: add(t,tick(),0.25)
for i in range(3): add(S[2]+5.58+0.12+i*0.22,tone(1568,0.25,0.002,0.08)+0.5*tone(2093,0.25,0.002,0.06),0.25)
add(S[3]+0.86,thump(),1.0); add(S[3]+0.86,chime((1568,2093)),0.22)
add(24.6,whoosh(0.3),0.4); add(24.65,chime(),0.4)
out=out/np.max(np.abs(out))*0.45
w=wave.open('sfx.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
