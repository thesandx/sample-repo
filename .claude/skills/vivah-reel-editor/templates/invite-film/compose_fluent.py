#!/usr/bin/env python3
"""Compose every art slot of the invite film from FETCHED assets only (no drawn illustrations).

Sources (all fetched from the web, licences allow commercial use):
  - Microsoft Fluent 3D emoji PNGs (MIT): cdn.jsdelivr.net/gh/microsoft/fluentui-emoji  -> fetched by fetch()
  - Jain Prateek Chihna (official Jain emblem, public domain): commons Special:FilePath/Jainism.svg?width=800
Only layout/design is made here: arranging sprites into garlands, torans, a mandap frame, an arch frame,
water band and railing (flat design shapes, like a card designer would draw in Canva).

Usage: python3 compose_fluent.py <sprite_dir> <out_art_dir> [jain_emblem.png]
"""
import math, os, sys, random, urllib.parse, urllib.request
from PIL import Image, ImageDraw, ImageFilter, ImageOps

SP, OUT = sys.argv[1], sys.argv[2]
EMBLEM = sys.argv[3] if len(sys.argv) > 3 else None
os.makedirs(SP, exist_ok=True); os.makedirs(OUT, exist_ok=True)
FLUENT = {"swan": "Swan", "peacock": "Peacock", "lotus": "Lotus", "rosette": "Rosette", "hibiscus": "Hibiscus",
          "cherry": "Cherry blossom", "herb": "Herb", "palm": "Palm tree", "tree": "Deciduous tree", "plant": "Potted plant",
          "elephant": "Elephant", "horse": "Horse", "longdrum": "Long drum", "drum": "Drum", "dancer": "Woman dancing",
          "bride": "Person with veil", "groom": "Person in tuxedo", "amphora": "Amphora", "diya": "Diya lamp", "bell": "Bell",
          "lantern": "Red paper lantern", "umbrella": "Umbrella", "sunflower": "Sunflower", "leaf": "Leaf fluttering in wind",
          "henna": "Palm up hand", "hands": "Raising hands", "clap": "Clapping hands", "sparkles": "Sparkles", "blossom": "Blossom",
          "tulip": "Tulip", "mango": "Mango", "flute": "Flute", "notes": "Musical notes", "bouquet": "Bouquet", "fire": "Fire", "gem": "Gem stone", "heart": "Red heart"}

def fetch():
    for n, name in FLUENT.items():
        f = f"{SP}/{n}.png"
        if os.path.exists(f): continue
        stem = name.lower().replace(' ', '_')
        b = f"https://cdn.jsdelivr.net/gh/microsoft/fluentui-emoji@main/assets/{urllib.parse.quote(name)}"
        for u in (f"{b}/3D/{stem}_3d.png", f"{b}/Medium/3D/{stem}_3d_medium.png", f"{b}/Default/3D/{stem}_3d_default.png"):
            try: open(f, 'wb').write(urllib.request.urlopen(u, timeout=30).read()); break
            except Exception: pass
fetch()
random.seed(7)
_c = {}
def S(n, w, flip=False, rot=0):
    if n not in _c: _c[n] = Image.open(f"{SP}/{n}.png").convert('RGBA')
    im = _c[n]; h = round(im.height * w / im.width); im = im.resize((w, h), Image.LANCZOS)
    if flip: im = ImageOps.mirror(im)
    if rot: im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    return im
def put(c, im, cx, cy, shadow=True):
    x, y = int(cx - im.width / 2), int(cy - im.height / 2)
    if shadow:
        a = im.split()[3].filter(ImageFilter.GaussianBlur(6)).point(lambda v: v * .28)
        sh = Image.new('RGBA', im.size, (70, 40, 20, 0)); sh.putalpha(a); c.alpha_composite(sh, (x + 5, y + 8))
    c.alpha_composite(im, (x, y))
def save(c, name): c.save(f"{OUT}/{name}"); print('art', name, c.size)
def canvas(w, h): return Image.new('RGBA', (w, h), (0, 0, 0, 0))

# ---- garland pieces ------------------------------------------------------------------------
MARI = ['rosette', 'sunflower']
def string(c, x, y0, y1, size=34, kinds=('rosette',), end='herb'):
    """vertical marigold string hanging from y0 to y1 at x"""
    d = ImageDraw.Draw(c); d.line([(x, y0), (x, y1)], fill=(110, 80, 40, 200), width=2)
    y, k = y0, 0
    while y < y1:
        put(c, S(kinds[k % len(kinds)], size, rot=random.randint(-30, 30)), x, y, shadow=False); y += size * .78; k += 1
    if end: put(c, S(end, int(size * 1.6), rot=180 if end == 'herb' else 0), x, y1 + size * .7)
def swag(c, x0, x1, y, sag, size=30, kinds=('rosette', 'sunflower')):
    """catenary swag of flowers between two points"""
    n = int((x1 - x0) / (size * .72))
    for i in range(n + 1):
        u = i / n; x = x0 + (x1 - x0) * u; yy = y + sag * math.sin(math.pi * u)
        put(c, S(kinds[i % len(kinds)], size, rot=random.randint(-40, 40)), x, yy, shadow=False)
def leaf_band(c, y, size=70):
    """row of mango-leaf style leaves along the top (toran)"""
    x = -10
    while x < c.width + 40:
        put(c, S('leaf', size, rot=random.choice([-100, -80, -90, -95])), x, y + random.randint(-6, 6)); x += size * .55

def toran(W=1080, H=450, style='haldi'):
    c = canvas(W, H)
    if style in ('haldi', 'chaak'):
        leaf_band(c, 34, 90)
        for k, (a, b) in enumerate([(0, 270), (270, 540), (540, 810), (810, 1080)]):
            swag(c, a + 10, b - 10, 110, 70, 30, ('hibiscus', 'rosette', 'sunflower'))
            swag(c, a + 10, b - 10, 92, 46, 26, ('rosette',))
        for x in (14, 270, 540, 810, 1066):
            if style == 'haldi': string(c, x, 70, 360, 30, ('rosette', 'sunflower'))
            else: string(c, x, 70, 300, 26, ('rosette',), end='bell')
    elif style == 'mehendi':
        for x in range(60, W, 160):
            d = ImageDraw.Draw(c); d.line([(x, 0), (x, 120 + (x // 160 % 2) * 60)], fill=(110, 80, 40, 220), width=2)
            put(c, S('lantern', 90), x, 170 + (x // 160 % 2) * 60)
        swag(c, -20, 540, 10, 90, 34, ('rosette', 'hibiscus')); swag(c, 540, 1100, 10, 90, 34, ('rosette', 'hibiscus'))
        for x in range(140, W, 160): string(c, x, 0, 260, 28, ('sunflower', 'rosette'), end='rosette')
    elif style == 'sangeet':
        for i in range(70):   # bougainvillea-like canopy of pink blooms + leaves
            x = random.uniform(-20, W + 20); y = random.uniform(-10, 70 + 50 * abs(math.sin(x / 160)))
            put(c, S(random.choice(['cherry', 'hibiscus', 'hibiscus', 'herb']), random.randint(60, 100), rot=random.randint(0, 359)), x, y, shadow=False)
        for x in (90, 990):
            d = ImageDraw.Draw(c); d.line([(x, 60), (x, 200)], fill=(110, 80, 40, 220), width=3); put(c, S('lantern', 80), x, 250)
        for x in range(200, 900, 110): string(c, x, 80, 150 + (x % 3) * 30, 26, ('cherry',), end='herb')
    elif style in ('baraat', 'vivah'):
        for row, (y, sag, sz) in enumerate([(0, 120, 40), (0, 90, 34)]):
            for a in range(-60, W, 240): swag(c, a, a + 240, y, sag, sz, ('rosette', 'hibiscus', 'sunflower') if row == 0 else ('sunflower', 'rosette'))
        for x in range(-60, W + 60, 240): string(c, x, 0, 300, 28, ('rosette', 'sunflower'), end='herb')
    return c

def floor(c, y, color=(222, 199, 170, 255), edge=(170, 120, 90, 255)):
    d = ImageDraw.Draw(c); d.rectangle([0, y, c.width, c.height], fill=color); d.rectangle([0, y, c.width, y + 10], fill=edge)
    for x in range(0, c.width, 60): d.ellipse([x + 22, y + 26, x + 38, y + 42], fill=(200, 160, 120, 255))

def scene(kind, W=1080, H=800):
    c = canvas(W, H); _scene(c, kind, 900, H); return c

def _scene(c, kind, W, H):
    """draw at 900 wide, then shift right by 90 so floors run full-bleed"""
    full = c; c = canvas(W, H)
    c = canvas(W, H)
    if kind == 'haldi':
        floor(c, 600)
        put(c, S('clap', 150, rot=10), 150, 430); put(c, S('clap', 150, flip=True, rot=-10), 750, 430)
        put(c, S('bride', 380), 450, 450)
        for x, y in ((290, 640), (610, 640)): put(c, S('mango', 90), x, y)
        for i in range(10): put(c, S(random.choice(['rosette', 'sunflower']), 44, rot=random.randint(0, 360)), random.uniform(80, 820), random.uniform(660, 760), shadow=False)
    elif kind == 'mehendi':
        floor(c, 620, (236, 218, 180, 255), (150, 160, 60, 255))
        put(c, S('henna', 300, rot=-15), 210, 420); put(c, S('bride', 360), 560, 440)
        for x in (90, 820): put(c, S('plant', 140), x, 640)
        put(c, S('bouquet', 120), 760, 700)
    elif kind == 'sangeet':
        floor(c, 640, (232, 205, 170, 255), (180, 100, 80, 255))
        for i, x in enumerate((140, 330, 560, 760)):
            put(c, S('dancer', 230, flip=i % 2 == 1), x, 470 + (i % 2) * 20)
        put(c, S('longdrum', 130), 450, 680); put(c, S('notes', 120), 450, 230)
    elif kind == 'chaak':
        d = ImageDraw.Draw(c); d.rectangle([0, 600, W, H], fill=(160, 200, 110, 255)); d.rectangle([0, 600, W, 610], fill=(110, 160, 70, 255))  # grass
        for x in (110, 790): put(c, S('amphora', 150), x, 560)
        put(c, S('bride', 280), 330, 480); put(c, S('groom', 280), 580, 480)
        for x in range(150, 800, 100): put(c, S('diya', 70), x, 690)
    elif kind == 'baraat':
        floor(c, 650, (238, 130, 160, 255), (200, 60, 110, 255))
        for i in range(24): put(c, S(random.choice(['hibiscus', 'cherry', 'rosette']), 56, rot=random.randint(0, 360)), random.uniform(0, W), random.uniform(680, 790), shadow=False)
        put(c, S('drum', 140), 90, 580); put(c, S('elephant', 300), 300, 500); put(c, S('horse', 260, flip=True), 580, 520)
        put(c, S('groom', 150), 600, 340); put(c, S('drum', 140), 810, 580)
    elif kind == 'ring':    # ring ceremony: couple facing, big ring between, sparkles + bouquets
        floor(c, 640, (240, 214, 200, 255), (200, 120, 140, 255))
        put(c, S('bride', 300), 230, 470); put(c, S('groom', 300), 670, 470)
        put(c, S('ring', 170, rot=-12), 450, 330); put(c, S('sparkles', 90), 540, 230); put(c, S('sparkles', 70), 360, 250)
        put(c, S('heart', 70), 450, 480)
        for x in (80, 820): put(c, S('bouquet', 120), x, 650)
    elif kind == 'phere':   # mandap with the sacred fire in the middle, couple on both sides
        d = ImageDraw.Draw(c)
        d.rounded_rectangle([60, 700, W - 60, 760], 18, fill=(230, 150, 175, 255))
        for x in (130, W - 130):
            d.rounded_rectangle([x - 26, 230, x + 26, 710], 12, fill=(244, 196, 210, 255)); string(c, x, 230, 690, 32, ('rosette', 'hibiscus'), end=None)
        d.pieslice([70, 90, W - 70, 380], 180, 360, fill=(240, 170, 195, 255)); d.rectangle([70, 225, W - 70, 260], fill=(230, 120, 160, 255))
        swag(c, 100, W - 100, 250, 60, 34, ('rosette', 'hibiscus'))
        d.rectangle([380, 600, 520, 690], fill=(200, 120, 80, 255)); d.rectangle([370, 590, 530, 610], fill=(170, 90, 60, 255))  # havan kund
        put(c, S('fire', 140), 450, 530)
        put(c, S('bride', 230), 270, 560); put(c, S('groom', 230), 630, 560)
        for x in (330, 570): put(c, S('diya', 70), x, 690)
    elif kind == 'vivah':   # mandap: two pillars + canopy, garlanded, couple inside
        d = ImageDraw.Draw(c)
        d.rounded_rectangle([60, 700, W - 60, 760], 18, fill=(230, 150, 175, 255))
        for x in (150, W - 150):
            d.rounded_rectangle([x - 26, 230, x + 26, 710], 12, fill=(244, 196, 210, 255)); string(c, x, 230, 690, 32, ('rosette', 'hibiscus'), end=None)
        d.pieslice([90, 90, W - 90, 380], 180, 360, fill=(240, 170, 195, 255)); d.rectangle([90, 225, W - 90, 260], fill=(230, 120, 160, 255))
        swag(c, 120, W - 120, 250, 60, 34, ('rosette', 'hibiscus'))
        put(c, S('sparkles', 90), W / 2, 140)
        put(c, S('bride', 250), 360, 560); put(c, S('groom', 250), 560, 560); put(c, S('diya', 90), 450, 700)
    # stretch the floor row (first opaque row from the bottom-left) across the full width, then place the scene
    FLOOR = {'haldi': ((222, 199, 170), 600), 'mehendi': ((236, 218, 180), 620), 'sangeet': ((232, 205, 170), 640),
             'chaak': ((160, 200, 110), 600), 'baraat': ((238, 130, 160), 650), 'ring': ((240, 214, 200), 640)}
    if kind in FLOOR:
        col, y = FLOOR[kind]; band = c.crop((0, y, 1, H)).resize((full.width, H - y))
        full.alpha_composite(band, (0, y))
    full.alpha_composite(c, (90, 0))

def prop(kind, W=200, H=320):
    c = canvas(W, H)
    if kind == 'matka':
        for i, s in enumerate((150, 130, 110)): put(c, S('amphora', s), W / 2, H - 70 - i * 95)
        put(c, S('herb', 80), W / 2, 40)
    elif kind == 'drum': put(c, S('longdrum', 170), W / 2, H - 110)
    elif kind == 'umbrella': put(c, S('umbrella', 190), W / 2, 140); put(c, S('umbrella', 150), W / 2, 210)
    elif kind == 'diya': put(c, S('lantern', 110), W / 2, 120); put(c, S('diya', 120), W / 2, H - 60)
    return c

# ---- intro pieces ---------------------------------------------------------------------------
def arch(W=1080, H=820):
    c = canvas(W, H); d = ImageDraw.Draw(c)
    col = (215, 180, 176, 255)
    m = Image.new('L', (W, H), 255); md = ImageDraw.Draw(m)       # frame = rect minus a cusped arch opening
    md.rectangle([70, 330, W - 70, H], fill=0); md.ellipse([70, 40, W - 70, 620], fill=0)
    for k in range(5): md.ellipse([150 + k * 160, 20, 290 + k * 160, 160], fill=0)
    frame = Image.new('RGBA', (W, H), col); frame.putalpha(m); c.alpha_composite(frame)
    d.line([(70, 330), (70, H)], fill=(185, 145, 140, 255), width=6); d.line([(W - 70, 330), (W - 70, H)], fill=(185, 145, 140, 255), width=6)
    for x, y in ((40, 40), (W - 40, 40)):
        for i in range(9): put(c, S(random.choice(['hibiscus', 'cherry', 'herb']), random.randint(60, 90), rot=random.randint(0, 359)), x + random.uniform(-40, 80) * (1 if x < 500 else -1), y + random.uniform(-20, 140), shadow=False)
    for x in (230, 400, 680, 850): string(c, x, 60, 260 + (x % 3) * 50, 24, ('cherry', 'herb'), end='cherry')
    return c

def plants(W=320, H=760):
    c = canvas(W, H)
    put(c, S('palm', 300), 120, 300); put(c, S('tree', 240), 160, 520); put(c, S('plant', 160), 90, 660); put(c, S('herb', 120, rot=-20), 250, 640)
    return c

def garden(W=1080, H=700):
    c = canvas(W, H); d = ImageDraw.Draw(c)
    for i in range(9): put(c, S('tree', random.randint(150, 200)), 120 + i * 110, 150 + random.randint(-10, 10))
    def railing(y):
        d.rectangle([0, y, W, y + 18], fill=(214, 186, 170, 255)); d.rectangle([0, y + 92, W, y + 104], fill=(214, 186, 170, 255))
        for x in range(10, W, 34): d.rounded_rectangle([x, y + 18, x + 16, y + 92], 7, fill=(229, 205, 192, 255))
    railing(230)
    for yy in range(334, 600):                    # water band
        t = (yy - 334) / 266; d.line([(0, yy), (W, yy)], fill=(int(150 + 40 * t), int(214 + 15 * t), int(222 + 10 * t), 255))
    for k in range(14):
        y = 360 + k * 18; x0 = (k * 97) % 300
        for x in range(-40 + x0, W, 300): d.arc([x, y, x + 120, y + 14], 200, 340, fill=(230, 247, 250, 255), width=3)
    for x, y in ((180, 520), (520, 560), (880, 500)): put(c, S('lotus', 80), x, y, shadow=False)
    railing(590)
    put(c, S('peacock', 260), 210, 180)
    return c

def emblem(path, W=420, H=520):
    im = Image.open(path).convert('RGBA'); a = im.split()[3]
    col = Image.new('RGBA', im.size, (122, 52, 22, 255)); col.putalpha(a)       # brown-maroon ink like the card text
    col.thumbnail((W, H), Image.LANCZOS); c = canvas(W, H); c.alpha_composite(col, ((W - col.width) // 2, (H - col.height) // 2)); return c

def wreath(W=400, H=400):
    c = canvas(W, H)
    for i in range(26):
        a = i / 26 * 2 * math.pi; put(c, S('herb', 70, rot=-math.degrees(a) - 90), W / 2 + 165 * math.cos(a), H / 2 + 165 * math.sin(a), shadow=False)
    for i in range(18):
        a = i / 18 * 2 * math.pi + .1; put(c, S(['rosette', 'hibiscus', 'cherry'][i % 3], 58, rot=i * 40), W / 2 + 160 * math.cos(a), H / 2 + 160 * math.sin(a), shadow=False)
    return c

if __name__ == '__main__':
    if EMBLEM: save(emblem(EMBLEM), 'jain-emblem.png')
    save(wreath(), 'monogram-wreath.png'); save(arch(), 'intro-arch.png'); save(plants(), 'intro-plants-left.png')
    save(garden(), 'intro-garden-pond.png'); swan = canvas(190, 190); put(swan, S('swan', 170), 95, 95, shadow=False); save(swan, 'swan.png')
    for fn, st, pr in (('haldi', 'haldi', 'matka'), ('mehendi', 'mehendi', None), ('sangeet', 'sangeet', 'drum'),
                       ('chaak', 'chaak', 'diya'), ('baraat', 'baraat', 'umbrella'), ('vivah', 'vivah', None),
                       ('ring', 'sangeet', 'diya'), ('phere', 'vivah', None)):
        save(toran(style=st), f'{fn}-top.png'); save(scene(fn), f'{fn}-main.png')
        if pr: save(prop(pr), f'{fn}-prop.png')
