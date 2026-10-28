import numpy as np, wave
SR=48000; D=32.5; out=np.zeros(int(SR*D)); rng=np.random.default_rng(3)
def add(t,s,g):
  i=int(t*SR); n=min(len(s),len(out)-i); out[i:i+n]+=s[:n]*g
def env(n,a,d): x=np.arange(n)/SR; return np.minimum(1,x/a)*np.exp(-x/d)
def tone(f,dur,a=0.002,d=0.08,f2=None):
  n=int(dur*SR); ff=np.linspace(f,f2 or f,n); return np.sin(2*np.pi*np.cumsum(ff)/SR)*env(n,a,d)
def pop(f=900): return tone(f,0.12,0.001,0.035,f*1.6)
def whoosh(dur=0.35):
  n=int(dur*SR); w=rng.standard_normal(n); y=np.convolve(w,np.ones(12)/12,'same')-np.convolve(w,np.ones(80)/80,'same'); return y*np.hanning(n)*2.5
def chime(fs=(1047,1319,1568)): return sum(tone(f,1.2,0.003,0.35)*(0.8**i) for i,f in enumerate(fs))
def ding(): return tone(1760,0.3,0.002,0.09)+0.5*tone(2637,0.3,0.002,0.07)
M=[0,4.6,11.05,17.7,23.05,28.4]
for a in [M[1]+2.26,M[3]]: add(a,whoosh(0.35),0.4)
add(M[1]+4.45,ding(),0.25); add(M[1]+5.5,ding(),0.25)
for k in range(3): add(M[2]+4.28+k*0.5,ding(),0.22)
add(M[4]+1.3,pop(1000),0.3); add(M[4]+3.3,whoosh(0.15),0.3)
add(M[4]+3.94,tone(140,0.35,0.002,0.09,55),0.9); add(M[4]+3.94,chime((1568,2093)),0.2)
add(M[5],pop(1000),0.3); add(M[5]+1.7,whoosh(0.3),0.35); add(M[5]+1.75,chime(),0.35)
out=out/np.max(np.abs(out))*0.4
w=wave.open('sfx.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
