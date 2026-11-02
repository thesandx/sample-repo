# Flickr CC BY / CC0 / PDM photo search + download (free; attribution needed for CC BY: credits.tsv).
# usage: python3 -I flickr_fetch.py outdir "query" [...]  -> photos, contact sheet per query, credits.tsv
import sys, re, os, json, urllib.request, urllib.parse
from PIL import Image, ImageDraw
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
get = lambda u: urllib.request.urlopen(u, timeout=40).read()
LIC = {4: 'CC BY 2.0', 9: 'CC0', 10: 'Public Domain Mark'}
cred = open(f'{out}/credits.tsv', 'a')
for q in sys.argv[2:]:
    s = get('https://www.flickr.com/search/?text=' + urllib.parse.quote(q) + '&license=4%2C9%2C10').decode('utf8', 'ignore')
    items = s.split('"_flickrModelRegistry":"photo-lite-models",')[1:]
    tiles = []; seen = set()
    for it in items:
        lic = re.search(r'"license":(\d+)', it); 
        if not lic or int(lic.group(1)) not in LIC: continue
        urls = re.findall(r'"(l|c|b|z)":\{"data":\{"displayUrl":"([^"]+)","width":(\d+),"height":(\d+)', it)
        if not urls: continue
        best = max(urls, key=lambda u: int(u[2])); url = 'https:' + best[1].replace('\\/', '/')
        pid = re.search(r'/(\d+)_', url).group(1)
        if pid in seen: continue
        seen.add(pid)
        name = (re.search(r'"realname":"([^"]*)"', it) or re.search(r'"username":"([^"]*)"', it)).group(1) or re.search(r'"username":"([^"]*)"', it).group(1)
        title = (re.search(r'"title":"([^"]*)"', it) or [None, ''])[1]
        f = f'{out}/{pid}.jpg'
        if not os.path.exists(f):
            try: open(f, 'wb').write(get(url))
            except Exception: continue
        cred.write(f'{pid}\t{name}\t{title}\t{LIC[int(lic.group(1))]}\thttps://www.flickr.com/photos/{re.search(chr(34)+"ownerNsid"+chr(34)+r":\"([^\"]+)", it).group(1)}/{pid}\t{q}\n')
        im = Image.open(f).convert('RGB'); w, h = im.size; im.thumbnail((240, 240)); tiles.append((pid, im, f'{w}x{h}'))
        if len(tiles) >= 20: break
    sh = Image.new('RGB', (5 * 250, ((len(tiles) + 4) // 5) * 270 or 10), 'white'); d = ImageDraw.Draw(sh)
    for k, (pid, im, sz) in enumerate(tiles):
        x, y = (k % 5) * 250, (k // 5) * 270; sh.paste(im, (x + 5, y + 5)); d.text((x + 5, y + 250), f'{pid} {sz}', fill='black')
    sh.save(f'{out}/sheet-{q.replace(" ", "_")}.jpg'); print(q, len(tiles))
