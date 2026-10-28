import json,base64,os,urllib.request
img="data:image/png;base64,"+base64.b64encode(open('first_bestie.png','rb').read()).decode()
p=('Vertical selfie video, close-up, phone held at arm\'s length. The same young Indian woman with short bob hair, round glasses and a mustard yellow t-shirt '
 'looks at the camera in happy shock: at the start she covers her mouth with her hand, eyes wide, then drops her hand and talks excitedly to the camera, '
 'almost emotional, like telling her followers big news. Clear natural lip movement, small head shakes of disbelief. Plain light grey wall behind her, soft indoor light. '
 'Voice: a native Hindi-speaking young woman from Delhi, casual everyday Hindustani, fast, natural, excited and a little teary, not formal, no English accent. '
 'Audio: only her voice, no music. She says in Hindi: "यार! प्रिया ने शादी का कार्ड भेजा... और उस पे मेरा नाम लिखा है!"')
b=dict(model='x-ai/grok-imagine-video-1.5-lite',duration=6,resolution='720p',aspect_ratio='9:16',generate_audio=True,prompt=p,
  frame_images=[{'type':'image_url','image_url':{'url':img},'frame_type':'first_frame'}])
r=urllib.request.Request('https://openrouter.ai/api/v1/videos',data=json.dumps(b).encode(),headers={'Authorization':'Bearer '+os.environ['OPENROUTER_KEY'],'Content-Type':'application/json'})
jobs=json.load(open('jobs.json'));jobs['bf1']=json.load(urllib.request.urlopen(r));print(jobs['bf1'])
json.dump(jobs,open('jobs.json','w'))
