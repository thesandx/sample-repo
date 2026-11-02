#!/usr/bin/env python3
"""Design-only art set ("royal": maroon + gold foil) for the invite film. No illustrations at all:
every slot is geometric ornament (arches, borders, mandalas, hanging lamps, gems) drawn as layout/design.
The only picture is the Jain emblem (official, public domain), recoloured gold, for the Mahavir card.

Usage: python3 compose_royal.py <out_art_dir> <jain_emblem.png> [accent per function in order...]
"""
import math, os, sys
from PIL import Image, ImageDraw, ImageFilter

OUT, EMB = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
SS = 2                                       # supersample for smooth lines
GOLD, GOLD2, GOLD3 = (231, 190, 104, 255), (250, 226, 160, 255), (168, 118, 42, 255)

def cv(w, h): return Image.new('RGBA', (w * SS, h * SS), (0, 0, 0, 0))
def fin(c, glow=True):
    w, h = c.width // SS, c.height // SS
    im = c.resize((w, h), Image.LANCZOS)
    if glow:   # soft warm glow + drop shadow so the gold sits on the velvet
        a = im.split()[3]
        g = Image.new('RGBA', im.size, (255, 200, 110, 0)); g.putalpha(a.filter(ImageFilter.GaussianBlur(6)).point(lambda v: v * .35))
        sh = Image.new('RGBA', im.size, (20, 0, 5, 0)); sh.putalpha(a.filter(ImageFilter.GaussianBlur(4)).point(lambda v: v * .5))
        out = Image.new('RGBA', im.size, (0, 0, 0, 0)); out.alpha_composite(sh, (0, 0)); out.alpha_composite(g); out.alpha_composite(im); return out
    return im
def P(v): return v * SS
def line(d, pts, col=GOLD, w=3): d.line([(P(x), P(y)) for x, y in pts], fill=col, width=P(w), joint='curve')
def circ(d, cx, cy, r, col=GOLD, w=3, fill=None): d.ellipse([P(cx - r), P(cy - r), P(cx + r), P(cy + r)], outline=col if w else None, width=P(w) if w else 0, fill=fill)
def petal(d, cx, cy, ang, L, W, col=GOLD, fill=None, w=3):
    """lens-shaped petal from (cx,cy) outward at angle ang"""
    pts = []
    for i in range(41):
        u = i / 40; along = L * u; side = W * math.sin(math.pi * u) * (1 if i <= 20 else 1)
        pts.append((along, side))
    pts = pts + [(L * (1 - i / 40), -W * math.sin(math.pi * (1 - i / 40))) for i in range(41)]
    ca, sa = math.cos(ang), math.sin(ang)
    poly = [(P(cx + x * ca - y * sa), P(cy + x * sa + y * ca)) for x, y in pts]
    d.polygon(poly, fill=fill, outline=col if w else None, width=P(w) if w else 0)
def diamond(d, cx, cy, r, col=GOLD, fill=None):
    d.polygon([(P(cx), P(cy - r)), (P(cx + r * .62), P(cy)), (P(cx), P(cy + r)), (P(cx - r * .62), P(cy))], fill=fill or col)
def chain(d, x, y0, y1, gem=None):
    line(d, [(x, y0), (x, y1)], GOLD3, 2)
    for y in range(int(y0) + 14, int(y1), 26): circ(d, x, y, 3, GOLD, 0, fill=GOLD)
    diamond(d, x, y1 + 16, 16, fill=gem or GOLD); circ(d, x, y1 + 40, 5, GOLD, 0, fill=GOLD2)

def mandala(d, cx, cy, R, accent, rings=4):
    for k in range(rings):
        r = R * (1 - k * .22); n = 12 + k * 4 if k % 2 == 0 else 16 + k * 4
        for i in range(n):
            a = 2 * math.pi * i / n + (k % 2) * math.pi / n
            petal(d, cx + (r * .55) * math.cos(a), cy + (r * .55) * math.sin(a), a, r * .45, r * .07 + 6,
                  GOLD, fill=accent if k == 1 else None, w=3)
        circ(d, cx, cy, r * .55, GOLD3, 2)
    circ(d, cx, cy, R * .18, GOLD, 4); circ(d, cx, cy, R * .1, GOLD, 0, fill=accent)
    for i in range(36):
        a = 2 * math.pi * i / 36; circ(d, cx + R * 1.04 * math.cos(a), cy + R * 1.04 * math.sin(a), 4, GOLD, 0, fill=GOLD2)

def frame_lines(d, W, H, inset=34):
    for o, w in ((inset, 4), (inset + 12, 2)):
        d.rectangle([P(o), P(o), P(W - o), P(H - o)], outline=GOLD, width=P(w))
    for x, y in ((inset, inset), (W - inset, inset), (inset, H - inset), (W - inset, H - inset)):
        diamond(d, x, y, 22, fill=GOLD2)

def cusped_arch(d, W, top, spring, inset, col=GOLD, w=4):
    """Mughal multi-cusp arch outline from left spring point to right"""
    cx = W / 2; rx = cx - inset; pts = []
    for i in range(181):
        a = math.pi * (1 - i / 180); x = cx + rx * math.cos(a); y = spring - (spring - top) * math.sin(a) ** .8
        y += 16 * abs(math.sin(a * 9))          # cusps
        pts.append((x, y))
    line(d, [(inset, 820)] + pts + [(W - inset, 820)], col, w)

# ---------------------------------------------------------------------------------------------
def arch():
    W, H = 1080, 820; c = cv(W, H); d = ImageDraw.Draw(c)
    frame_lines(d, W, 1920)
    cusped_arch(d, W, 90, 360, 90); cusped_arch(d, W, 112, 372, 110, GOLD3, 2)
    for x in (260, 400, 680, 820): chain(d, x, 120 + abs(540 - x) * .25, 200 + abs(540 - x) * .35)
    for i in range(-3, 4): petal(d, 540 + i * 34, 70, -math.pi / 2, 40 - abs(i) * 6, 9, GOLD, fill=GOLD if i == 0 else None)
    return fin(c)

def pillar():
    W, H = 320, 760; c = cv(W, H); d = ImageDraw.Draw(c)
    x = 110
    line(d, [(x - 22, 40), (x - 22, 740)], GOLD, 3); line(d, [(x + 22, 40), (x + 22, 740)], GOLD, 3)
    for y in range(80, 720, 90):
        for a in range(8): petal(d, x, y, a * math.pi / 4, 30, 8, GOLD, w=2)
        circ(d, x, y, 6, GOLD, 0, fill=GOLD2)
    return fin(c)

def base_band(accent=(150, 30, 60, 255)):
    W, H = 1080, 700; c = cv(W, H); d = ImageDraw.Draw(c)
    mandala(d, 540, 700, 330, accent)
    for y, r in ((560, 26), (610, 20)):
        for x in range(0, W + 1, int(r * 2)): d.arc([P(x - r), P(y - r), P(x + r), P(y + r)], 0, 180, fill=GOLD, width=P(2))
    line(d, [(0, 640), (W, 640)], GOLD, 3)
    return fin(c)

def glint():
    c = cv(190, 190); d = ImageDraw.Draw(c)
    for a, L in ((0, 80), (math.pi / 2, 80), (math.pi / 4, 34), (3 * math.pi / 4, 34)):
        for s in (1, -1): petal(d, 95, 95, a + (0 if s > 0 else math.pi), L, 7, GOLD2, fill=GOLD2, w=0)
    return fin(c)

def wreath():
    W = 400; c = cv(W, W); d = ImageDraw.Draw(c)
    circ(d, 200, 200, 175, GOLD, 4); circ(d, 200, 200, 150, GOLD3, 2)
    for i in range(24):
        a = 2 * math.pi * i / 24; petal(d, 200 + 150 * math.cos(a), 200 + 150 * math.sin(a), a, 44, 10, GOLD, fill=(140, 28, 56, 255) if i % 2 else None)
    for i in range(48): a = 2 * math.pi * i / 48; circ(d, 200 + 186 * math.cos(a), 200 + 186 * math.sin(a), 3, GOLD, 0, fill=GOLD2)
    return fin(c)

def emblem():
    im = Image.open(EMB).convert('RGBA'); a = im.split()[3]
    g = Image.new('RGBA', im.size, GOLD); g.putalpha(a); g.thumbnail((420, 520), Image.LANCZOS)
    c = Image.new('RGBA', (420, 520), (0, 0, 0, 0)); c.alpha_composite(g, ((420 - g.width) // 2, (520 - g.height) // 2))
    halo = cv(420, 520); hd = ImageDraw.Draw(halo)
    for i in range(48):
        a = 2 * math.pi * i / 48; petal(hd, 210 + 150 * math.cos(a), 250 + 150 * math.sin(a), a, 36, 5, GOLD3, w=2)
    out = fin(halo); out.alpha_composite(fin(c.resize((c.width * SS, c.height * SS)))); return out

def top(accent):
    W, H = 1080, 450; c = cv(W, H); d = ImageDraw.Draw(c)
    line(d, [(0, 30), (W, 30)], GOLD, 4); line(d, [(0, 44), (W, 44)], GOLD3, 2)
    for x in range(0, W + 1, 90):              # scalloped valance with gems
        d.arc([P(x), P(0), P(x + 90), P(120)], 0, 180, fill=GOLD, width=P(4))
        diamond(d, x + 45, 128, 12, fill=accent)
    for i, x in enumerate(range(45, W, 180)): chain(d, x, 120, 230 + (i % 2) * 60, gem=accent)
    return fin(c)

def main(accent):
    W, H = 1080, 800; c = cv(W, H); d = ImageDraw.Draw(c)
    mandala(d, 540, 800, 420, accent, rings=4)
    return fin(c)

def lamp(accent):
    W, H = 200, 320; c = cv(W, H); d = ImageDraw.Draw(c)
    line(d, [(100, 0), (100, 110)], GOLD3, 2)
    d.polygon([(P(60), P(150)), (P(100), P(110)), (P(140), P(150)), (P(120), P(220)), (P(80), P(220))], fill=accent, outline=GOLD, width=P(4))
    for y in (150, 185): line(d, [(66, y), (134, y)], GOLD, 2)
    for x in (80, 100, 120): chain(d, x, 220, 250 + (x == 100) * 20)
    return fin(c)

if __name__ == '__main__':
    acc = {'mehendi': (52, 120, 60, 255), 'ring': (180, 40, 80, 255), 'haldi': (214, 160, 20, 255),
           'baraat': (190, 30, 40, 255), 'phere': (220, 90, 20, 255), 'vivah': (220, 90, 20, 255),
           'sangeet': (120, 40, 140, 255), 'chaak': (30, 110, 120, 255)}
    def save(im, n): im.save(f'{OUT}/{n}'); print('art', n, im.size)
    save(emblem(), 'jain-emblem.png'); save(wreath(), 'monogram-wreath.png'); save(arch(), 'intro-arch.png')
    save(pillar(), 'intro-plants-left.png'); save(base_band(), 'intro-garden-pond.png'); save(glint(), 'swan.png')
    for k, a in acc.items():
        save(top(a), f'{k}-top.png'); save(main(a), f'{k}-main.png'); save(lamp(a), f'{k}-prop.png')
