from PIL import Image,ImageFilter,ImageEnhance
import numpy as np,math
n=Image.open('note_clean.png').rotate(90,expand=True)  # portrait
n=n.resize((340,int(340*n.size[1]/n.size[0])),Image.LANCZOS);nw,nh=n.size;print(nw,nh)
C=1400;fan=Image.new('RGBA',(C,C),(0,0,0,0))
px,py=C//2,C//2+420  # pivot
K=9
for i in range(K):
  ang=38-i*(48/(K-1))  # degrees, left to right
  t=n.copy();t=ImageEnhance.Brightness(t).enhance(0.86+0.14*i/(K-1))
  # shadow
  sh=Image.new('RGBA',t.size,(0,0,0,0));sh.putalpha(t.getchannel('A').point(lambda v:int(v*0.45)))
  sh=sh.filter(ImageFilter.GaussianBlur(10))
  for layer,off in [(sh,(10,6)),(t,(0,0))]:
    L=Image.new('RGBA',(C,C),(0,0,0,0));L.paste(layer,(px-nw//2+off[0],py-nh+90+off[1]),layer)
    L=L.rotate(ang,center=(px,py),resample=Image.BICUBIC)
    fan=Image.alpha_composite(fan,L)
fan=fan.crop(fan.getbbox());fan.save('fan.png');print(fan.size)
