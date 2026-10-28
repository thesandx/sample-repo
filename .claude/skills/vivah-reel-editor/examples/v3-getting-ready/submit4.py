import json,base64,os,urllib.request
img="data:image/jpeg;base64,"+base64.b64encode(open('mirror0.png','rb').read()).decode()
base=('Vertical phone video, phone propped on a dressing table, static camera. The same young Indian woman in the blush pink chikankari kurta is getting ready at her vanity in her cozy bedroom, '
 'chatting casually to the camera in Hindi like she is telling her best friend a story, natural relaxed expressions, clear natural lip movement, '
 'warm evening light, realistic UGC phone footage. Audio: only her natural conversational voice with a little room tone, no music. ')
lines={
 'm1':(5,'She finishes pressing the bindi on her forehead, then turns to the camera excited and says: "Pata hai, meri shaadi ka invite dekh ke saare friends pagal ho gaye!"'),
 'm2':(7,'She puts on a bangle while talking, smiling proudly: "Humne apni khud ki wedding website banayi, itni pyaari! Aur har friend ko uska personal link bheja."'),
 'm3':(7,'She adjusts her earring, then laughs and says: "Link kholte hi unka naam aata hai, bilkul paper card jaisa! Sab pooch rahe the, yaar ye kaise banaya?"'),
 'm4':(6,'She tucks her hair behind her ear and explains happily: "Date scratch karke reveal hoti hai, aur venue, saare functions bhi wahi pe."'),
 'm5':(6,'She picks up a lipstick, pauses, looks at the camera with a playful smirk and says: "Sab soch rahe the bahut mehenga hoga... main boli, na yaar, bas saat sau ninyanve!"'),
 'm6':(4,'She smiles and points down at the camera: "vivah dot online, link bio mein hai!"'),
}
jobs=json.load(open('jobs.json'))
for k,(d,l) in lines.items():
  b=dict(model='x-ai/grok-imagine-video-1.5-lite',duration=d,resolution='720p',aspect_ratio='9:16',generate_audio=True,prompt=base+l,
    frame_images=[{'type':'image_url','image_url':{'url':img},'frame_type':'first_frame'}])
  r=urllib.request.Request('https://openrouter.ai/api/v1/videos',data=json.dumps(b).encode(),headers={'Authorization':'Bearer '+os.environ['OPENROUTER_KEY'],'Content-Type':'application/json'})
  jobs[k]=json.load(urllib.request.urlopen(r)); print(k,jobs[k]['status'])
json.dump(jobs,open('jobs.json','w'))
