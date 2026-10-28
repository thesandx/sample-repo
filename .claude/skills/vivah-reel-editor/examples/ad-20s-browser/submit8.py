import json,base64,os,urllib.request
img="data:image/png;base64,"+base64.b64encode(open('first_priya.png','rb').read()).decode()
base=('Realistic vertical smartphone selfie video, filmed on the front camera of an iPhone held at arm\'s length, slight natural hand shake. The same young Indian woman from the image: long dark hair, small maroon bindi, pearl drop earrings, blush pink chikankari kurta. Real skin texture with pores and fine detail, no beauty filter, no smoothing, natural soft daylight, background softly out of focus. She behaves like a normal girl recording an Instagram story, not an actress: natural blinks, small glances away from the lens, a quick breath before speaking, relaxed shoulders, small head tilts, lips and jaw move in exact sync with the words. {act} '
 'Voice: a real 24-year-old woman from Delhi speaking everyday casual Hindi-Hinglish, native Hindi accent, natural pace with tiny pauses, warm, slightly informal, recorded on a phone mic in a quiet room. No English accent, no announcer tone, no music, no background sound. She says in Hindi: "{line}"')
C={'a1':(4,'Raises one eyebrow as if surprised, leans slightly toward the lens, then points straight at the camera on the last word.','शादी का कार्ड अभी भी पेपर पे? बस विवाह डॉट ऑनलाइन पे जाओ!'),
'a2':(6,'Glances down at her phone and back, counts four things on her fingers, relaxed and quick.','दोनों का नाम... शादी की डेट... अपने फंक्शन... और अपना गाना। बस!'),
'a3':(4,'Eyes widen with a happy smile, a small excited nod.','और ये देखो, वेबसाइट रेडी... हर गेस्ट के नाम के साथ!'),
'a4':(4,'Shakes her head gently while saying no prompt no coding, then a big confident smile.','ना प्रॉम्प्ट, ना कोडिंग... बस पाँच मिनट में साइट रेडी!')}
jobs=json.load(open('jobs.json'))
for k,(d,act,line) in C.items():
  b=dict(model='x-ai/grok-imagine-video-1.5-lite',duration=d,resolution='720p',aspect_ratio='9:16',generate_audio=True,prompt=base.format(act=act,line=line),
    frame_images=[{'type':'image_url','image_url':{'url':img},'frame_type':'first_frame'}])
  r=urllib.request.Request('https://openrouter.ai/api/v1/videos',data=json.dumps(b).encode(),headers={'Authorization':'Bearer '+os.environ['OPENROUTER_KEY'],'Content-Type':'application/json'})
  jobs[k]=json.load(urllib.request.urlopen(r));print(k,jobs[k]['status'])
json.dump(jobs,open('jobs.json','w'))
