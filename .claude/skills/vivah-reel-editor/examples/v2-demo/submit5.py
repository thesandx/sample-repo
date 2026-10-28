import json,base64,os,urllib.request
img="data:image/jpeg;base64,"+base64.b64encode(open('green0.png','rb').read()).decode()
p=('Vertical selfie video, phone held at arm\'s length, the same young Indian woman in the blush pink chikankari kurta talks to the camera like a friendly Instagram creator, '
 'clear natural lip movement, small head nod and a cheerful hand gesture. The background stays a flat, evenly lit pure chroma-key green the whole time. '
 'Voice: a native Hindi-speaking young woman from Delhi, casual everyday Hindustani accent, fast and natural, warm and excited, not formal, not an English accent. '
 'Audio: only her voice, no music. She says in Hindi: "और कूपन कोड NEW30 अप्लाई करो, पूरे तीस परसेंट ऑफ़ मिलेगा!"')
b=dict(model='x-ai/grok-imagine-video-1.5-lite',duration=5,resolution='720p',aspect_ratio='9:16',generate_audio=True,prompt=p,
  frame_images=[{'type':'image_url','image_url':{'url':img},'frame_type':'first_frame'}])
r=urllib.request.Request('https://openrouter.ai/api/v1/videos',data=json.dumps(b).encode(),headers={'Authorization':'Bearer '+os.environ['OPENROUTER_KEY'],'Content-Type':'application/json'})
jobs=json.load(open('jobs.json'));jobs['n30']=json.load(urllib.request.urlopen(r));print(jobs['n30']['status'])
json.dump(jobs,open('jobs.json','w'))
