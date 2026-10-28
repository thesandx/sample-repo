import json
# (clip offset, [(word,start)], end, area)
C=[(0.0,[('Shaadi',0.05),('ka',0.5),('card',0.78),('abhi',1.04),('bhi',1.18),('paper',1.30),('pe?',1.62),('Bas',2.20),('vivah.online',2.36),('pe',3.36),('jao!',3.50)],3.85,'full'),
(6.9,[('Dono',0.3),('ka',0.98),('naam,',1.14),('shaadi',1.32),('ki',1.66),('date,',1.80),('apne',2.00),('functions',2.26),('aur',2.70),('apna',3.00),('gaana.',3.24),('Bas!',4.18)],11.65,'side'),
(12.0,[('Aur',0.3),('ye',0.76),('dekho,',0.90),('website',1.66),('ready...',2.02),('har',2.42),('guest',2.86),('ke',3.18),('naam',3.28),('ke',3.44),('saath!',3.62)],16.0,'side'),
(16.6,[('Na',0.2),('prompt,',0.56),('na',1.24),('coding...',1.46),('bas',2.12),('paanch',2.32),('minute',2.64),('mein',2.94),('site',3.08),('ready!',3.30)],20.3,'full')]
# chunk into groups of <=3 words, break on punctuation
states=[]
for off,ws,end,area in C:
  chunks=[];cur=[]
  for w in ws:
    cur.append(w)
    if len(cur)==3 or w[0][-1] in ',?!.': chunks.append(cur);cur=[]
  if cur:chunks.append(cur)
  for ci,ch in enumerate(chunks):
    for wi,(w,s) in enumerate(ch):
      nxt=ch[wi+1][1] if wi+1<len(ch) else (chunks[ci+1][0][1] if ci+1<len(chunks) else end-off)
      states.append(dict(words=[x[0] for x in ch],act=wi,t0=round(off+s,3),t1=round(off+nxt,3),area=area))
json.dump(states,open('caps.json','w'),indent=0);print(len(states))
