import json,base64,os,urllib.request
img="data:image/jpeg;base64,"+base64.b64encode(open('priya916.jpg','rb').read()).decode()
base=('Vertical selfie video, handheld phone camera, realistic Instagram UGC style. The same young Indian woman from the image, blush pink chikankari kurta, '
 'talks straight into the camera in Hindi with clear natural lip movement and expressive face. Natural daylight, soft blurred background. Audio: only her voice, no music. ')
lines={
 'c2':(6,'She rolls her eyes, slightly annoyed, and says: "Paper card pe pandrah-bees hazaar kharch... aur log usse kholte bhi nahi!"'),
 'c3':(7,'She lifts her phone up into frame proudly, smiling, and says: "Maine vivah dot online pe card banaya. Har guest ko uske naam ke saath, seedha WhatsApp pe!"'),
 'c4':(6,'Excited, eyes wide, she says: "Aur sirf saat sau ninyanve rupaye mein! Paanch minute mein ready!"'),
 'c5':(4,'Smiling warmly, pointing down with one finger, she says: "Link bio mein hai, abhi try karo!"'),
}
jobs=json.load(open('jobs.json'))
for k,(d,l) in lines.items():
  b=dict(model='x-ai/grok-imagine-video-1.5-lite',duration=d,resolution='720p',aspect_ratio='9:16',generate_audio=True,prompt=base+l,
    frame_images=[{'type':'image_url','image_url':{'url':img},'frame_type':'first_frame'}])
  r=urllib.request.Request('https://openrouter.ai/api/v1/videos',data=json.dumps(b).encode(),headers={'Authorization':'Bearer '+os.environ['OPENROUTER_KEY'],'Content-Type':'application/json'})
  jobs[k]=json.load(urllib.request.urlopen(r)); print(k,jobs[k])
json.dump(jobs,open('jobs.json','w'))
