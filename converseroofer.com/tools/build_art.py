"""Generates illustrated SVG cover art for blog posts and fallback scenes for photo slots."""
import os, random
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "img")
W, H = 1200, 750

def house(x, y, w=260, h=150, roof="#1c2431", wall="#e9dcc9", trim="#ffffff", door="#8d6e4e", win="#bfe0f5", chimney=True, depth=1.0):
    """Gabled house sitting on baseline y (bottom of wall). Scaled by depth for distance."""
    w, h = w*depth, h*depth
    rh = h*0.72
    top = y - h - rh
    g = f'<g>'
    g += f'<rect x="{x}" y="{y-h}" width="{w}" height="{h}" fill="{wall}"/>'
    g += f'<rect x="{x}" y="{y-h}" width="{w}" height="{h}" fill="#000" opacity="{0.28*(1-depth):.2f}"/>'
    if chimney:
        g += f'<rect x="{x+w*0.68}" y="{top+rh*0.35}" width="{w*0.08}" height="{rh*0.5}" fill="#8b5e3c"/>'
    g += f'<polygon points="{x-w*0.06},{y-h} {x+w/2},{top} {x+w*1.06},{y-h}" fill="{roof}"/>'
    g += f'<polygon points="{x+w*0.02},{y-h} {x+w/2},{top+rh*0.12} {x+w*0.98},{y-h}" fill="#000" opacity=".12"/>'
    g += f'<rect x="{x-w*0.07}" y="{y-h-4*depth}" width="{w*1.14}" height="{7*depth}" fill="{trim}"/>'
    # door + windows
    dw, dh = w*0.16, h*0.62
    g += f'<rect x="{x+w/2-dw/2}" y="{y-dh}" width="{dw}" height="{dh}" rx="{3*depth}" fill="{door}"/>'
    for wx in (x+w*0.12, x+w*0.68):
        g += f'<rect x="{wx}" y="{y-h*0.78}" width="{w*0.2}" height="{h*0.36}" rx="{3*depth}" fill="{win}" stroke="{trim}" stroke-width="{4*depth}"/>'
        g += f'<line x1="{wx+w*0.1}" y1="{y-h*0.78}" x2="{wx+w*0.1}" y2="{y-h*0.42}" stroke="{trim}" stroke-width="{3*depth}"/>'
    g += '</g>'
    return g

def tree(x, y, s=1.0, col="#2f6b3a"):
    return (f'<rect x="{x-6*s}" y="{y-40*s}" width="{12*s}" height="{40*s}" fill="#5a3f1e"/>'
            f'<circle cx="{x}" cy="{y-70*s}" r="{40*s}" fill="{col}"/><circle cx="{x-28*s}" cy="{y-50*s}" r="{30*s}" fill="{col}"/><circle cx="{x+28*s}" cy="{y-52*s}" r="{32*s}" fill="{col}"/>')

def cloud(x, y, s=1.0, col="#ffffff", op=0.9):
    return (f'<g fill="{col}" opacity="{op}"><ellipse cx="{x}" cy="{y}" rx="{90*s}" ry="{34*s}"/><circle cx="{x-30*s}" cy="{y-18*s}" r="{34*s}"/>'
            f'<circle cx="{x+20*s}" cy="{y-26*s}" r="{42*s}"/><circle cx="{x+60*s}" cy="{y-10*s}" r="{30*s}"/></g>')

def hail(seed=1, n=70, area=(0,0,W,520), rmin=6, rmax=16):
    rnd = random.Random(seed); g = '<g>'
    for _ in range(n):
        x = rnd.uniform(area[0], area[2]); y = rnd.uniform(area[1], area[3]); r = rnd.uniform(rmin, rmax)
        g += f'<line x1="{x+r*1.2:.0f}" y1="{y-r*4:.0f}" x2="{x:.0f}" y2="{y:.0f}" stroke="#ffffff" stroke-opacity=".25" stroke-width="{r*0.6:.1f}" stroke-linecap="round"/>'
        g += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="url(#hailg)"/>'
    return g + '</g>'

def rain(seed=2, n=160):
    rnd = random.Random(seed); g = '<g stroke="#cfe3f5" stroke-opacity=".35" stroke-width="2" stroke-linecap="round">'
    for _ in range(n):
        x = rnd.uniform(0, W); y = rnd.uniform(0, 560); l = rnd.uniform(18, 40)
        g += f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x-l*0.25:.0f}" y2="{y+l:.0f}"/>'
    return g + '</g>'

def lightning(x, y1, y2):
    pts = f"{x},{y1} {x-30},{y1+(y2-y1)*0.4} {x+10},{y1+(y2-y1)*0.45} {x-40},{y2}"
    return f'<polyline points="{pts}" fill="none" stroke="#ffd166" stroke-width="10" stroke-linejoin="round" stroke-linecap="round" filter="url(#glow)"/><polyline points="{pts}" fill="none" stroke="#fff7d6" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>'

def wordmark(dark=True):
    col = "#ffffff" if dark else "#0f1f33"
    return (f'<g opacity=".8" transform="translate({W-250} {H-46})"><rect width="26" height="26" rx="6" fill="#f26a1b"/><path d="M5 15 L13 7 L21 15" fill="none" stroke="#fff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M7 14 V21 H19 V14" fill="none" stroke="#fff" stroke-width="2.5"/>'
            f'<text x="34" y="19" font-family="Inter,Arial,sans-serif" font-size="17" font-weight="800" fill="{col}" letter-spacing=".5">CONVERSE ROOFER</text></g>')

def defs(sky_top, sky_bot, ground_top, ground_bot):
    return f'''<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{sky_top}"/><stop offset="1" stop-color="{sky_bot}"/></linearGradient>
<linearGradient id="ground" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{ground_top}"/><stop offset="1" stop-color="{ground_bot}"/></linearGradient>
<radialGradient id="hailg" cx=".35" cy=".35" r=".7"><stop offset="0" stop-color="#ffffff"/><stop offset=".6" stop-color="#dbe9f7"/><stop offset="1" stop-color="#8fb3d9"/></radialGradient>
<radialGradient id="sun" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff3c4"/><stop offset=".5" stop-color="#ffd166" stop-opacity=".9"/><stop offset="1" stop-color="#ffd166" stop-opacity="0"/></radialGradient>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="8"/></filter>
<filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#0f1f33" flood-opacity=".35"/></filter>
</defs>'''

def scene(kind):
    stormy = kind in ("hail", "storm", "hail-cover", "rain")
    dusk = kind in ("dusk", "questions", "bg")
    if stormy: sky = ("#0b1626", "#2a4363"); ground = ("#2f4a3a", "#1f3328")
    elif dusk: sky = ("#1b2a4a", "#f26a1b"); ground = ("#3d5a44", "#22362a")
    else: sky = ("#2b8ccf", "#bfe3f8"); ground = ("#6fb36a", "#3f8248")
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img">' + defs(*sky, *ground)
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
    if not stormy and not dusk: s += f'<circle cx="980" cy="120" r="130" fill="url(#sun)"/>'
    if dusk: s += f'<circle cx="900" cy="470" r="220" fill="url(#sun)" opacity=".8"/>'
    # clouds
    ccol = "#3d5270" if stormy else ("#ffb98a" if dusk else "#ffffff")
    s += cloud(180, 130, 1.3, ccol, .95) + cloud(620, 90, 1.0, ccol, .85) + cloud(1050, 190, 1.1, ccol, .9)
    if stormy: s += cloud(400, 210, 1.6, "#2a3a52", .9) + cloud(900, 240, 1.5, "#2a3a52", .9)
    # hills / ground
    s += f'<ellipse cx="300" cy="640" rx="700" ry="140" fill="url(#ground)"/><ellipse cx="1000" cy="660" rx="700" ry="150" fill="url(#ground)"/><rect x="0" y="640" width="{W}" height="{H-640}" fill="url(#ground)"/>'
    return s, stormy, dusk

def finish(s, dark=True):
    return s + wordmark(dark) + '</svg>'

def neighborhood(s, roof="#1c2431", wall="#e9dcc9"):
    s += house(120, 600, depth=.55, roof=roof, wall="#d8cbb6") + house(960, 605, depth=.6, roof=roof, wall="#dcd0bd")
    s += tree(60, 640, 1.1) + tree(1160, 650, 1.2) + tree(760, 610, .8)
    s += f'<g filter="url(#soft)">{house(430, 640, w=340, h=190, roof=roof, wall=wall)}</g>'
    return s

def shingle_field(s, hits=None, shield=False):
    # close-up roof: rows of architectural shingles in perspective
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img">' + defs("#0f1f33","#2b8ccf","#3a3f47","#22262c")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + cloud(200,110,1.3,"#ffffff",.85) + cloud(900,150,1.1,"#ffffff",.8)
    s += f'<polygon points="0,{H} 0,300 {W},180 {W},{H}" fill="#2b2f36"/>'
    rnd = random.Random(7)
    for row in range(0, 14):
        y0 = 300 + row*40; y1 = 180 + row*40
        for col in range(0, 16):
            x = col*80 + (40 if row % 2 else 0) - 40
            xa, xb = x, x+76
            ya = y0 + (y1-y0)*(xa/W); yb = y0 + (y1-y0)*(xb/W)
            shade = rnd.choice(["#3a3f47","#40464f","#353a41","#444a54"])
            s += f'<polygon points="{xa},{ya} {xb},{yb} {xb},{yb+36} {xa},{ya+36}" fill="{shade}" stroke="#1c2027" stroke-width="2"/>'
    s += f'<line x1="0" y1="300" x2="{W}" y2="180" stroke="#1c2027" stroke-width="10"/>'
    if hits:
        for (hx, hy, r) in hits:
            s += f'<circle cx="{hx}" cy="{hy}" r="{r}" fill="#111" opacity=".55"/><circle cx="{hx}" cy="{hy}" r="{r+6}" fill="none" stroke="#f26a1b" stroke-width="4"/>'
    if shield:
        s += f'<g filter="url(#soft)" transform="translate(600 430)"><path d="M0,-150 L120,-105 L120,0 Q120,100 0,150 Q-120,100 -120,0 L-120,-105 Z" fill="#1f9d55"/><path d="M0,-120 L92,-84 L92,0 Q92,78 0,118 Q-92,78 -92,0 L-92,-84 Z" fill="#26b565"/><path d="M-55,5 L-15,45 L60,-40" fill="none" stroke="#fff" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/></g>'
        s += hail(seed=3, n=25, area=(100,80,1100,300), rmin=8, rmax=18)
    return s

def card(x, y, w, h, lines, title="", check=None):
    g = f'<g filter="url(#soft)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="#ffffff"/>'
    if title: g += f'<rect x="{x}" y="{y}" width="{w}" height="46" rx="16" fill="#0f1f33"/><rect x="{x}" y="{y+30}" width="{w}" height="16" fill="#0f1f33"/><text x="{x+20}" y="{y+30}" font-family="Inter,Arial,sans-serif" font-size="18" font-weight="800" fill="#fff">{title}</text>'
    for i, ln in enumerate(lines):
        yy = y + 80 + i*46
        mark = (check or [])[i] if check and i < len(check) else "check"
        if mark == "check": g += f'<circle cx="{x+30}" cy="{yy}" r="13" fill="#e7f7ee"/><path d="M{x+23},{yy} l5,5 l10,-11" fill="none" stroke="#1f9d55" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>'
        elif mark == "q": g += f'<circle cx="{x+30}" cy="{yy}" r="13" fill="#fff1e8"/><text x="{x+30}" y="{yy+6}" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-size="18" font-weight="800" fill="#f26a1b">?</text>'
        elif mark == "x": g += f'<circle cx="{x+30}" cy="{yy}" r="13" fill="#fdecec"/><path d="M{x+24},{yy-6} l12,12 M{x+36},{yy-6} l-12,12" stroke="#c92a2a" stroke-width="3.5" stroke-linecap="round"/>'
        g += f'<rect x="{x+56}" y="{yy-8}" width="{ln}" height="16" rx="8" fill="#dbe4f0"/>'
    return g + '</g>'

covers = {}

# ---- Blog covers ----
# 1. Hail on shingles: close-up shingles with hail hits and falling hail
s = shingle_field(None, hits=[(300,470,22),(620,520,18),(860,400,26),(450,640,20),(1000,600,16),(180,620,14)])
s += hail(seed=11, n=60, area=(0,0,W,420), rmin=8, rmax=20)
covers["cover-hail-shingles"] = finish(s)

# 2. Claim guide: bright day, house, document card with checks
s, _, _ = scene("day"); s = neighborhood(s)
s += card(760, 250, 330, 300, [180,220,150,200], title="Roof inspection report", check=["check","check","check","check"])
covers["cover-claim-guide"] = finish(s)

# 3. Seven questions: dusk, house, checklist with question marks
s, _, _ = scene("questions"); s = neighborhood(s, roof="#141c2b")
s += card(80, 220, 330, 330, [200,160,220,180,150], title="Before you sign", check=["q","q","check","q","x"])
covers["cover-seven-questions"] = finish(s)

# 4. Nine signs: day, house with numbered callouts and magnifier
s, _, _ = scene("day"); s = neighborhood(s)
for i,(cx,cy) in enumerate([(600,300),(770,455),(365,455),(470,560),(700,560),(850,640)], 1):
    s += f'<circle cx="{cx}" cy="{cy}" r="20" fill="#f26a1b" stroke="#fff" stroke-width="4" filter="url(#soft)"/><text x="{cx}" y="{cy+7}" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-size="20" font-weight="800" fill="#fff">{i}</text>'
s += f'<g filter="url(#soft)" transform="translate(940 250)"><circle r="95" fill="#ffffff" fill-opacity=".25" stroke="#0f1f33" stroke-width="16"/><line x1="70" y1="70" x2="150" y2="150" stroke="#0f1f33" stroke-width="26" stroke-linecap="round"/></g>'
covers["cover-nine-signs"] = finish(s)

# 5. Class 4: shingles + shield with hail bouncing
covers["cover-class4"] = finish(shingle_field(None, shield=True))

# ---- Fallback scenes ----
s, _, _ = scene("day"); covers["ph-house"] = finish(neighborhood(s))
s, _, _ = scene("hail"); s = neighborhood(s, roof="#141c2b", wall="#cfc3b0"); s += hail(seed=5, n=90, area=(0,0,W,600), rmin=7, rmax=18); covers["ph-hail"] = finish(s)
s, _, _ = scene("storm"); s += lightning(880, 60, 420); s = neighborhood(s, roof="#141c2b", wall="#cfc3b0"); s += rain(); covers["ph-storm"] = finish(s)
covers["ph-roof"] = finish(shingle_field(None))
s, _, _ = scene("day"); s = neighborhood(s)
s += f'<g stroke="#8d6e4e" stroke-width="14" stroke-linecap="round"><line x1="820" y1="640" x2="700" y2="330"/><line x1="880" y1="640" x2="760" y2="330"/></g>'
for i in range(7): t=i/6; s += f'<line x1="{820-120*t+2}" y1="{640-310*t}" x2="{880-120*t-2}" y2="{640-310*t}" stroke="#8d6e4e" stroke-width="10" stroke-linecap="round"/>'
s += f'<g filter="url(#soft)"><rect x="150" y="560" width="170" height="80" rx="10" fill="#f26a1b"/><rect x="200" y="540" width="70" height="30" rx="8" fill="#0f1f33"/><rect x="170" y="590" width="130" height="8" rx="4" fill="#0f1f33" opacity=".3"/></g>'
covers["ph-tools"] = finish(s)
s, _, _ = scene("day"); s = neighborhood(s)
s += f'<g filter="url(#soft)" transform="translate(960 330)"><path d="M0,-110 L88,-77 L88,0 Q88,74 0,110 Q-88,74 -88,0 L-88,-77 Z" fill="#1f9d55"/><path d="M-40,4 L-11,33 L44,-30" fill="none" stroke="#fff" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/></g>'
covers["ph-shield"] = finish(s)
s, _, _ = scene("dusk"); covers["ph-bg"] = finish(neighborhood(s, roof="#141c2b"))

for name, svg in covers.items():
    open(os.path.join(OUT, name + ".svg"), "w").write(svg)
print("wrote", len(covers), "images")
