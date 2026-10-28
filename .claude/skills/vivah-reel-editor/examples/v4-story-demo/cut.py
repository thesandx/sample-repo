import sys,glob,os,numpy as np
from rembg import remove,new_session
from PIL import Image,ImageFilter
from scipy import ndimage
s=new_session('u2net_human_seg')
fs=sorted(glob.glob('../v3/bg/f*.jpg'))
for f in fs:
  o='cut/'+os.path.basename(f).replace('.jpg','.png')
  if os.path.exists(o): continue
  im=Image.open(f).convert('RGB')
  m=np.array(remove(im,session=s,only_mask=True)).astype(np.float32)/255
  lab,n=ndimage.label(m>0.5)
  if n>1:
    sz=ndimage.sum(np.ones_like(m),lab,range(1,n+1));keep=np.argmax(sz)+1
    big=ndimage.binary_dilation(lab==keep,iterations=6);m=m*big
  m[int(1920*0.705):,:]=0  # cut at table line
  a=Image.fromarray((m*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
  im.putalpha(a)
  im.crop((90,180,990,1354)).save(o)
print('done',len(fs))
