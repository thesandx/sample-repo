import json,base64,os,urllib.request
img="data:image/jpeg;base64,"+base64.b64encode(open('green0.png','rb').read()).decode()
base=('Vertical selfie video, phone held at arm\'s length, the same young Indian woman in the blush pink chikankari kurta talks to the camera in Hindi like a friendly Instagram creator, '
 'clear natural lip movement, small natural head movements and hand gestures, warm and casual. The background stays a flat, evenly lit pure chroma-key green the whole time, no objects, no shadows. '
 'Audio: only her voice, natural and conversational, no music. She says: ')
lines={
 'g1':(5,'"Sab pooch rahe the, ye shaadi wali website kahan se banayi? Toh lo, dikhati hoon!"'),
 'g2':(6,'"Har guest ka apna invite, uske naam ke saath. Tap karo, aur card khulta hai, gaane ke saath!"'),
 'g3':(6,'"Date scratch karke reveal hoti hai, aur shaadi tak ka live countdown bhi!"'),
 'g4':(7,'"Venue seedha Google Maps pe, aur Haldi, Mehndi, Sangeet, saare functions ek hi jagah."'),
 'g5':(5,'"RSVP bhi WhatsApp pe, toh pata chal jaata hai kaun aa raha hai."'),
 'g6':(8,'"Aur ye sab sirf saat sau ninyanve rupaye mein, paanch minute mein ready! Link bio mein hai."'),
}
jobs=json.load(open('jobs.json'))
for k,(d,l) in lines.items():
  b=dict(model='x-ai/grok-imagine-video-1.5-lite',duration=d,resolution='720p',aspect_ratio='9:16',generate_audio=True,prompt=base+l,
    frame_images=[{'type':'image_url','image_url':{'url':img},'frame_type':'first_frame'}])
  r=urllib.request.Request('https://openrouter.ai/api/v1/videos',data=json.dumps(b).encode(),headers={'Authorization':'Bearer '+os.environ['OPENROUTER_KEY'],'Content-Type':'application/json'})
  jobs[k]=json.load(urllib.request.urlopen(r)); print(k,jobs[k]['status'])
json.dump(jobs,open('jobs.json','w'))
