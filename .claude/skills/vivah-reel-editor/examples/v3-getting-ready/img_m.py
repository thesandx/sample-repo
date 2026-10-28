import json,base64,os,urllib.request,re
src="data:image/png;base64,"+base64.b64encode(open('/mnt/project-files/uploads/hearth/2a109b5a-58f5-4c2a-8fcf-3d4c4a290922','rb').read()).decode()
txt=('Edit this photo: keep the exact same woman (same face, hair, pearl earrings, blush pink chikankari kurta). '
 'Make a vertical 9:16 frame from a phone propped on her dressing table: she sits at her bedroom vanity getting ready, her face and shoulders fill the middle of the frame, '
 'she is pressing a small maroon bindi onto her forehead with one fingertip while smiling and glancing at the camera as if chatting with a friend. '
 'Warm natural evening light, cozy Indian bedroom behind her softly out of focus with fairy lights and a mirror edge, a few bangles and a lipstick on the table in the foreground. '
 'Realistic phone camera photo, not a studio shot.')
b={'model':'google/gemini-nano-banana-2.1','modalities':['image','text'],'image_config':{'aspect_ratio':'9:16'},
 'messages':[{'role':'user','content':[{'type':'text','text':txt},{'type':'image_url','image_url':{'url':src}}]}]}
r=urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',data=json.dumps(b).encode(),headers={'Authorization':'Bearer '+os.environ['OPENROUTER_KEY'],'Content-Type':'application/json'})
j=json.load(urllib.request.urlopen(r))
msg=j['choices'][0]['message'];print((msg.get('content') or '')[:200],j.get('usage',{}).get('cost'))
for i,im in enumerate(msg.get('images',[])):
  u=im['image_url']['url'];open(f'mirror{i}.png','wb').write(base64.b64decode(u.split(',',1)[1]));print('saved',i)
