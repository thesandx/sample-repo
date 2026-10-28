import sys,json
from faster_whisper import WhisperModel
m=WhisperModel('small',device='cpu',compute_type='int8')
res={}
for c in sys.argv[1:]:
  segs,_=m.transcribe(__import__('numpy').fromfile(c+'.pcm',dtype='int16').astype('float32')/32768,language='hi',word_timestamps=True,initial_prompt='Hinglish in Roman script.')
  res[c]=[(round(w.start,2),round(w.end,2),w.word.strip()) for s in segs for w in s.words]
  print(c,res[c])
json.dump(res,open('words.json','w'))
