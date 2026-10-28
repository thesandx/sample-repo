import json,base64,os,sys,urllib.request
img="data:image/png;base64,"+base64.b64encode(open('first_priya.png','rb').read()).decode()
base=('Realistic vertical smartphone selfie video, filmed on the front camera of an iPhone held at arm\'s length, natural hand shake that gets stronger when she reacts. The same young Indian woman from the image: long dark hair, small maroon bindi, pearl drop earrings, blush pink chikankari kurta. Real skin texture, no beauty filter, natural daylight, background softly out of focus. '
 'She is NOT reading a script: she is a real, expressive Delhi girl ranting to her best friend on an Instagram story, big genuine emotions, lively face, expressive eyebrows, lips and jaw in exact sync with the words. {act} '
 'Voice: a real 24-year-old Delhi woman, everyday Hinglish, native Hindi accent, highly expressive and dramatic, pitch rises and falls, stretched vowels, playful exasperation, recorded on a phone mic. No announcer tone, no flat reading, no music. She says in Hindi: "{line}"')
C={'h1':('Starts with a shocked, disbelieving face, eyebrows shooting up on "paper pe?", then throws her head back and puts her palm on her forehead, stretching out a long dramatic "kyuuuu" with an eye-roll, then snaps forward close to the lens, points straight at the camera and says the last line with a confident, cheeky smile.',
 'शादी का कार्ड... अभी भी पेपर पे?! लेकिन क्यूँ...?? बस विवाह डॉट ऑनलाइन पे जाओ!'),
'h2':('Leans into the lens with wide, horrified eyes and a half laugh on "paper pe?", shakes her head and throws both hands up in frustration while whining a long, stretched "lekin kyuuuu", then calms down, smiles knowingly, and taps the air toward the camera on the last line.',
 'अरे, शादी का कार्ड अभी भी पेपर पे?! लेकिन क्यूँ...?? बस, विवाह डॉट ऑनलाइन पे जाओ!')}
keys=sys.argv[1:] or list(C)
jobs=json.load(open('jobs.json'))
for k in keys:
  act,line=C[k]
  b=dict(model='x-ai/grok-imagine-video-1.5-lite',duration=6,resolution='720p',aspect_ratio='9:16',generate_audio=True,prompt=base.format(act=act,line=line),
    frame_images=[{'type':'image_url','image_url':{'url':img},'frame_type':'first_frame'}])
  r=urllib.request.Request('https://openrouter.ai/api/v1/videos',data=json.dumps(b).encode(),headers={'Authorization':'Bearer '+os.environ['OPENROUTER_KEY'],'Content-Type':'application/json'})
  jobs[k]=json.load(urllib.request.urlopen(r));print(k,jobs[k]['status'])
json.dump(jobs,open('jobs.json','w'))
