from PIL import Image,ImageFilter,ImageDraw
import numpy as np
im=Image.open('dl/500-note-front.png').convert('RGBA')
a=np.array(im).astype(float)
rgb=a[:,:,:3];al=a[:,:,3]
# crop to opaque body (exclude dark border) 
op=(al>200)&(rgb.sum(2)>120)
ys,xs=np.where(op);print(xs.min(),xs.max(),ys.min(),ys.max())
x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
rgb=rgb[y0:y1,x0:x1].copy()
r,g,b=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
m=(r>g+35)&(r>b+35)
mi=Image.fromarray((m*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(7))
m=np.array(mi)>0;print('stamp px',m.sum())
# diffusion inpaint
fill=rgb.copy();fill[m]=0
known=(~m).astype(float)
acc=fill*known[:,:,None];w=known.copy()
for s in [3,7,15,31,61]:
  pass
out=rgb.copy()
cur=fill.copy()
for it in range(400):
  blur=np.array(Image.fromarray(np.clip(cur,0,255).astype(np.uint8)).filter(ImageFilter.BoxBlur(3))).astype(float)
  cur[m]=blur[m]
out[m]=cur[m]
# add a touch of paper noise to inpainted area
rng=np.random.default_rng(2);out[m]+=rng.normal(0,6,(m.sum(),3))
note=Image.fromarray(np.clip(out,0,255).astype(np.uint8)).convert('RGBA')
# slightly rounded/worn edges
mk=Image.new('L',note.size,0);ImageDraw.Draw(mk).rounded_rectangle([0,0,note.size[0]-1,note.size[1]-1],8,fill=255)
note.putalpha(mk);note.save('note_clean.png');print(note.size)
