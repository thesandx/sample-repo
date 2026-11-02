#!/usr/bin/env python3
"""Bright, natural art set for the invite film: real photos (Flickr CC BY / CC0, fetched with
flickr_fetch.py) placed in gold arch frames on colourful gradient backgrounds, with a real marigold
garland photo as the top toran. Only frames, gradients and borders are design; every picture is a
real photo. The Jain emblem (public domain) is the Mahavir card.

Usage: python3 compose_photo.py <photo_dir> <out_art_dir> <jain_emblem.png> picks.json
picks.json: {"garland": "<id>", "intro": "<id>", "functions": {"mehendi": "<id>", ...}, "colors": {"mehendi": ["#hex","#hex"], ...}}
"""
import json, math, os, random, sys
from PIL import Image, ImageDraw, ImageFilter, ImageOps

PH, OUT, EMB, PICKS = sys.argv[1:5]
os.makedirs(OUT, exist_ok=True)
pk = json.load(open(PICKS))
GOLD, GOLD2 = (222, 172, 70, 255), (255, 230, 160, 255)
random.seed(3)

def photo(pid): return Image.open(f'{PH}/{pid}.jpg').convert('RGB')
def cover(im, w, h, fy=.5):
    s = max(w / im.width, h / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - w) // 2; y = int((im.height - h) * fy); return im.crop((x, y, x + w, y + h))
def hexc(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def arch_mask(w, h, SS=3):
    m = Image.new('L', (w * SS, h * SS), 0); d = ImageDraw.Draw(m); r = w * SS / 2
    d.rectangle([0, r, w * SS, h * SS], fill=255); d.ellipse([0, 0, w * SS, 2 * r], fill=255)
    return m.resize((w, h), Image.LANCZOS)

def framed(pid, W=1080, H=840, pw=760, ph=780, fy=.5):
    """photo cropped into a tall arch with a double gold border and a soft shadow"""
    c = Image.new('RGBA', (W, H), (0, 0, 0, 0)); x0, y0 = (W - pw) // 2, H - ph - 20
    outer = arch_mask(pw + 36, ph + 36)
    sh = Image.new('RGBA', outer.size, (60, 10, 20, 0)); sh.putalpha(outer.filter(ImageFilter.GaussianBlur(14)).point(lambda v: v * .45))
    c.alpha_composite(sh, (x0 - 18 + 8, y0 - 18 + 14))
    gold = Image.new('RGBA', outer.size, GOLD); gold.putalpha(outer); c.alpha_composite(gold, (x0 - 18, y0 - 18))
    inner = arch_mask(pw + 12, ph + 12); w2 = Image.new('RGBA', inner.size, (255, 248, 230, 255)); w2.putalpha(inner); c.alpha_composite(w2, (x0 - 6, y0 - 6))
    p = cover(photo(pid), pw, ph, fy).convert('RGBA'); p.putalpha(arch_mask(pw, ph)); c.alpha_composite(p, (x0, y0))
    return c

def garland_top(pid, W=1080, H=330, canvas_h=None):
    """real marigold-garland photo as a toran: top band of the photo with a scalloped lower edge + gold trim"""
    band = cover(photo(pid), W, H, 0.0).convert('RGBA')
    SS = 3; m = Image.new('L', (W * SS, H * SS), 0); d = ImageDraw.Draw(m)
    base = H - 70
    d.rectangle([0, 0, W * SS, base * SS], fill=255)
    for x in range(0, W + 1, 90): d.ellipse([x * SS, (base - 50) * SS, (x + 90) * SS, (base + 60) * SS], fill=255)
    m = m.resize((W, H), Image.LANCZOS); band.putalpha(m)
    c = Image.new('RGBA', (W, canvas_h or H), (0, 0, 0, 0))
    trim = Image.new('RGBA', (W, H), GOLD); trim.putalpha(m.filter(ImageFilter.MaxFilter(9)))
    sh = Image.new('RGBA', (W, H), (60, 10, 20, 0)); sh.putalpha(m.filter(ImageFilter.GaussianBlur(10)).point(lambda v: v * .5))
    c.alpha_composite(sh, (0, 10)); c.alpha_composite(trim); c.alpha_composite(band)
    return c

def bg(c1, c2, W=1080, H=1920):
    """bright vertical gradient + soft bokeh dots (design)"""
    a, b = hexc(c1), hexc(c2); im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H; d.line([(0, y), (W, y)], fill=tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3)))
    bok = Image.new('RGBA', (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(bok)
    for _ in range(26):
        r = random.randint(20, 70); x, y = random.randint(0, W), random.randint(250, H)
        bd.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, random.randint(25, 60)))
    bok = bok.filter(ImageFilter.GaussianBlur(8)); im = im.convert('RGBA'); im.alpha_composite(bok); return im

def emblem(col=(120, 30, 40, 255)):
    im = Image.open(EMB).convert('RGBA'); a = im.split()[3]
    g = Image.new('RGBA', im.size, col); g.putalpha(a); g.thumbnail((420, 520), Image.LANCZOS)
    c = Image.new('RGBA', (420, 520), (0, 0, 0, 0)); c.alpha_composite(g, ((420 - g.width) // 2, (520 - g.height) // 2)); return c

def ring_frame(W=400):
    SS = 3; c = Image.new('RGBA', (W * SS, W * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(c); R = W * SS / 2
    for r, w in ((R - 12, 10), (R - 40, 4)): d.ellipse([R - r, R - r, R + r, R + r], outline=GOLD, width=w)
    for i in range(36):
        a = 2 * math.pi * i / 36; x, y = R + (R - 26) * math.cos(a), R + (R - 26) * math.sin(a); d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=GOLD2)
    return c.resize((W, W), Image.LANCZOS)

def blank(w, h): return Image.new('RGBA', (w, h), (0, 0, 0, 0))

if __name__ == '__main__':
    def save(im, n): im.save(f'{OUT}/{n}'); print('art', n, im.size)
    save(emblem(), 'jain-emblem.png'); save(ring_frame(), 'monogram-wreath.png')
    save(garland_top(pk['garland'], canvas_h=820), 'intro-arch.png')
    save(blank(320, 760), 'intro-plants-left.png'); save(blank(190, 190), 'swan.png')
    save(framed(pk['intro'], 1080, 700, 980, 540, .55), 'intro-garden-pond.png')
    save(bg(*pk['colors']['intro']), 'bg-intro.png')
    for fn, pid in pk['functions'].items():
        save(garland_top(pk['garland']), f'{fn}-top.png'); save(framed(pid, fy=pk.get('fy', {}).get(fn, .5)), f'{fn}-main.png')
        save(bg(*pk['colors'][fn]), f'bg-{fn}.png')
