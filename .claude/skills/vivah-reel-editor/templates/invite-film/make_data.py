#!/usr/bin/env python3
"""details.json -> data.js for invite.html.

All timings and layout positions are measured from the reference reel (IG DWbD-OMCRcG, 720x1280,
scaled x1.5 to 1080x1920). Usage: python3 make_data.py details.json > data.js
Optional: --fit SECONDS rescales every page duration so the film ends at that length.
"""
import json, sys

# ---- measured from the reference ---------------------------------------------------------
INTRO_CARDS = [9.5, 10.0, 12.0]               # deity / invite+monogram / lineage   (0 - 31.5 s)
FN_DUR = [9.0, 10.0, 10.5, 8.0, 8.0, 7.8]     # per function page, reused cyclically
FN_IN = ['blur', 'blur', 'flash', 'flash', 'flash', 'popout']   # how each function page arrives
FN_STYLE = ['drop', 'drop', 'drop', 'drop', 'pops', 'pops']     # 'drop': top border falls, art there; 'pops': items pop one by one
TIMING = dict(layerIn=0.8, textAt=0.8, stagger=0.55, wipe=1.0, blur=0.6, flash=0.45, popOut=0.5, cardOut=0.4)

def page_text(f):
    """Function page lines; y grows ~78 px a line like the reference (title at ~600)."""
    rows, y = [], 590
    rows.append(dict(txt=f['name'], style='title', y=y)); y += 100
    if f.get('tagline'):
        rows.append(dict(txt=f['tagline'], style='small', y=y)); y += 46 * (f['tagline'].count('\n') + 1) + 40
    for key, gap in (('date', 78), ('day', 110), ('time', 78), ('venue', 78)):
        if f.get(key):
            rows.append(dict(txt=f[key], style='body', y=y)); y += gap + 52 * f[key].count('\n')
    assert y < 1536, 'text runs into the bottom 20%: shorten the tagline/venue'
    return rows

def fn_layers(art, style):
    L = []
    pops = style == 'pops'
    if art.get('top'):
        L.append(dict(src=art['top'], x=0, y=0, w=1080, h=450, **{'in': 'drop'}, at=(1.8 if pops else 0.15), sway=0.6))
    if art.get('prop'):   # same prop both sides (matkas / umbrellas / lanterns), mirrored on the right
        y = 900 if pops else 1240
        L.append(dict(src=art['prop'], x=30, y=y, w=200, h=320, **{'in': 'pop'}, at=(0.9 if pops else 0.35), bob=3))
        L.append(dict(src=art['prop'], x=850, y=y, w=200, h=320, mirror=True, **{'in': 'pop'}, at=(1.1 if pops else 0.45), bob=3, ph=1.3))
    if art.get('main'):
        L.append(dict(src=art['main'], x=0, y=1120, w=1080, h=800, **{'in': 'pop' if pops else 'fade'},
                      at=(0.3 if pops else 0), dur=(0.7 if pops else 0.25), breathe=0.006))
    return L

def build(d, fit=None):
    pages, t = [], 0.0
    ia = d.get('intro_art', {})
    intro_layers = [
        dict(src=ia.get('arch', 'intro-arch.png'), x=0, y=0, w=1080, h=820, **{'in': 'fade'}, dur=0.6, sway=0.2),
        dict(src=ia.get('plants', 'intro-plants-left.png'), x=0, y=760, w=320, h=760, **{'in': 'fade'}, dur=0.6, sway=0.5),
        dict(src=ia.get('plants', 'intro-plants-left.png'), x=760, y=760, w=320, h=760, mirror=True, **{'in': 'fade'}, dur=0.6, sway=0.5, ph=2),
        dict(src=ia.get('garden', 'intro-garden-pond.png'), x=0, y=1220, w=1080, h=700, **{'in': 'none'}),
        dict(src=ia.get('swan', 'swan.png'), x=300, y=1500, w=190, h=190, **{'in': 'fade'}, at=1.0, drift=120, driftSpeed=0.22),
        dict(src=ia.get('swan', 'swan.png'), x=600, y=1520, w=170, h=170, mirror=True, **{'in': 'fade'}, at=1.4, drift=110, driftSpeed=0.18, ph=2.0),
    ]
    c1, c2, c3 = INTRO_CARDS
    g, b = d['groom'], d['bride']
    cards = [
        dict(t0=0, t1=c1, layers=[dict(src=d['deity']['art'], x=330, y=230, w=420, h=520, **{'in': 'blur'}, at=0.5, dur=1.2)],
             lines=[dict(txt=d['deity']['line'], style='body', y=790, size=42, at=2.0)]),
        dict(t0=c1, t1=c1 + c2, layers=[dict(src=d['monogram_art'], x=340, y=560, w=400, h=400, **{'in': 'pop'}, at=3.8, dur=0.8)],
             lines=[dict(txt=d['family_line'], style='script2', y=330, at=0.5),
                    dict(txt=d['invite_line'], style='serif', y=420, size=38, at=1.4),
                    dict(txt=d.get('monogram_letters', ''), style='script', y=690, size=110, at=4.4),
                    dict(txt=d['couple_line'], style='script', y=990, size=96, at=4.8)]),
        dict(t0=c1 + c2, t1=c1 + c2 + c3, textAt=0.4, stagger=0.9,
             lines=[dict(txt=g['name'], style='script', y=250),
                    dict(txt=g['grand'], style='serif', y=400, size=34),
                    dict(txt=g['rel'], style='serif', y=510),
                    dict(txt=g['parents'], style='serif', y=575, size=38),
                    dict(txt='with', style='serif', y=720),
                    dict(txt=b['name'], style='script', y=790),
                    dict(txt=b['grand'], style='serif', y=945, size=34),
                    dict(txt=b['rel'], style='serif', y=1055),
                    dict(txt=b['parents'], style='serif', y=1120, size=38)]),
    ]
    T0 = sum(INTRO_CARDS)
    pages.append(dict(t0=0, t1=T0, layers=intro_layers, cards=cards))
    t = T0
    for i, f in enumerate(d['functions']):
        dur = f.get('dur', FN_DUR[i % len(FN_DUR)])
        style = f.get('style', FN_STYLE[min(i, len(FN_STYLE) - 1)] if i < len(FN_STYLE) else 'drop')
        pages.append(dict(t0=t, t1=t + dur, **{'in': f.get('fx', FN_IN[i % len(FN_IN)])},
                          layers=fn_layers(f.get('art', {}), style),
                          lines=page_text(f)))
        t += dur
    if fit:
        k = fit / t
        for p in pages:
            p['t0'] *= k; p['t1'] *= k
            for c in p.get('cards', []): c['t0'] *= k; c['t1'] *= k
        t = fit
    return dict(bg=d.get('bg', '#F7EBD3'), ink=d.get('ink', '#4A3524'), duration=round(t, 3), timing=TIMING, pages=pages)

if __name__ == '__main__':
    args = sys.argv[1:]
    fit = None
    if '--fit' in args:
        fit = float(args[args.index('--fit') + 1]); del args[args.index('--fit'):args.index('--fit') + 2]
    data = build(json.load(open(args[0])), fit)
    print('window.INVITE = ' + json.dumps(data, ensure_ascii=False, indent=1) + ';')
