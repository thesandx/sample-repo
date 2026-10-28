import json,base64,os,urllib.request
img="data:image/png;base64,"+base64.b64encode(open('first_priya.png','rb').read()).decode()
base=('Vertical selfie video, close-up, phone held at arm\'s length. The same young Indian woman with long dark hair, maroon bindi, pearl drop earrings and blush pink kurta '
 'talks to the camera like a friendly Instagram creator, outdoors with a soft blurred background. Clear natural lip movement, natural head movement and small hand gestures. {act} '
 'Voice: a native Hindi-speaking young woman from Delhi, casual everyday Hindustani, natural and warm, not formal, no English accent. '
 'Audio: only her voice, no music. She says in Hindi: "{line}"')
C={'t1':(6,'Excited and proud, eyebrows raised, a little playful.','अपनी शादी का कार्ड मैंने खुद बनाया... सब पूछ रहे हैं किसने बनाया! चलो बताती हूँ।'),
't2':(5,'Explaining calmly, counting on her fingers.','पहले दूल्हा-दुल्हन का नाम, फिर शादी की डेट।'),
't3':(6,'Explaining, counting on her fingers, smiling.','फिर सारे फंक्शन, अपना वेबसाइट एड्रेस, और अपना पसंदीदा गाना।'),
't4':(6,'Happy and excited, a small clap.','बस! हर मेहमान को उसके नाम वाला लिंक, व्हाट्सऐप पे... सिर्फ़ सात सौ निन्यानवे रुपये में!'),
't5':(6,'Laughing, then points down at the comments.','मम्मी ने खुद पूरे खानदान को फॉरवर्ड किया! लिंक चाहिए? कमेंट करो LINK।')}
jobs=json.load(open('jobs.json'))
for k,(d,act,line) in C.items():
  b=dict(model='x-ai/grok-imagine-video-1.5-lite',duration=d,resolution='720p',aspect_ratio='9:16',generate_audio=True,prompt=base.format(act=act,line=line),
    frame_images=[{'type':'image_url','image_url':{'url':img},'frame_type':'first_frame'}])
  r=urllib.request.Request('https://openrouter.ai/api/v1/videos',data=json.dumps(b).encode(),headers={'Authorization':'Bearer '+os.environ['OPENROUTER_KEY'],'Content-Type':'application/json'})
  jobs[k]=json.load(urllib.request.urlopen(r));print(k,jobs[k]['status'])
json.dump(jobs,open('jobs.json','w'))
