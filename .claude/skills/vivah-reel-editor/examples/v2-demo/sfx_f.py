import numpy as np, wave
SR=48000; D=38.8; out=np.zeros(int(SR*D)); rng=np.random.default_rng(2)
def add(t,s,g):
  i=int(t*SR); n=min(len(s),len(out)-i); out[i:i+n]+=s[:n]*g
def env(n,a,d): x=np.arange(n)/SR; return np.minimum(1,x/a)*np.exp(-x/d)
def tone(f,dur,a=0.002,d=0.08,f2=None):
  n=int(dur*SR); ff=np.linspace(f,f2 or f,n); return np.sin(2*np.pi*np.cumsum(ff)/SR)*env(n,a,d)
def pop(f=900): return tone(f,0.12,0.001,0.035,f*1.6)
def whoosh(dur=0.35):
  n=int(dur*SR); w=rng.standard_normal(n); y=np.convolve(w,np.ones(12)/12,'same')-np.convolve(w,np.ones(80)/80,'same'); return y*np.hanning(n)*2.5
def chime(fs=(1047,1319,1568)): return sum(tone(f,1.2,0.003,0.35)*(0.8**i) for i,f in enumerate(fs))
G=[0,4.75,10.6,15.7,22.25,26.8]
add(1.65,whoosh(0.3),0.4)
for t in [G[0]+1.38,G[1]+0.74,G[2],G[2]+3.58,G[3]+0.84,G[3]+2.58,G[4],G[4]+2.64]: add(t,pop(1000),0.3)
add(G[1]+2.88,tone(2200,0.08,0.001,0.02),0.3)
add(G[5]+0.84,tone(140,0.35,0.002,0.09,55),0.9); add(G[5]+0.84,chime((1568,2093)),0.2)
add(G[5]+5.32,whoosh(0.3),0.35); add(G[5]+5.37,chime(),0.35)
add(G[5]+7.6,tone(140,0.35,0.002,0.09,55),0.7); add(G[5]+7.6,chime((1319,1568,2093)),0.3)
out=out/np.max(np.abs(out))*0.4
w=wave.open('sfx_f.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
