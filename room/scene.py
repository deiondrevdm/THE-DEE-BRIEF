# Generates room.svg: Dee's bedroom drawn in a 3/4 corner view with ink outlines.
# 3D coords: x runs along the back wall (right), y comes toward the viewer along the left wall, z is up.
import random, math, pathlib
R = random.Random(11)
CX, CY = 640, 560
INK = "#1F1B3A"

def P(x, y, z):
    return (CX + x - 0.78 * y, CY + 0.2 * x + 0.5 * y - z)

def f(n): return f"{n:.1f}"

def poly(points, fill, sw=3, extra=""):
    s = " ".join(f"{f(a)},{f(b)}" for a, b in (P(*p) for p in points))
    return f'<polygon points="{s}" fill="{fill}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round" {extra}/>'

def mY(y, x0, ztop):  # plane facing +y: u -> +x, v -> down
    e, g = P(x0, y, ztop); return f"matrix(1 0.2 0 1 {f(e)} {f(g)})"
def mX(x, yfront, ztop):  # plane facing +x: u -> toward the back wall, v -> down
    e, g = P(x, yfront, ztop); return f"matrix(0.78 -0.5 0 1 {f(e)} {f(g)})"
def mZ(z, x0, y0):  # horizontal plane: u -> +x, w -> +y
    e, g = P(x0, y0, z); return f"matrix(1 0.2 -0.78 0.5 {f(e)} {f(g)})"

def box(x, y, z, w, d, h, top, front, side, sw=3):
    return (poly([(x, y, z + h), (x + w, y, z + h), (x + w, y + d, z + h), (x, y + d, z + h)], top, sw)
            + poly([(x, y + d, z + h), (x + w, y + d, z + h), (x + w, y + d, z), (x, y + d, z)], front, sw)
            + poly([(x + w, y + d, z + h), (x + w, y, z + h), (x + w, y, z), (x + w, y + d, z)], side, sw))

def g(transform, inner, extra=""): return f'<g transform="{transform}" {extra}>{inner}</g>'
def rect(x, y, w, h, fill, sw=3, extra=""): return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="{fill}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round" {extra}/>'
def at(x, y, z): a, b = P(x, y, z); return f"translate({f(a)} {f(b)})"

C = dict(wall="#7C98EC", wallL="#6E8BE6", ceil="#D9D3F5", floor="#A3AEC6", tuft="#8893AE",
         woodT="#F2A867", woodF="#E28E50", woodS="#C9743D",
         lilT="#C9A6F7", lilF="#B08BEE", lilS="#9270DA", inner="#4A3A86",
         musT="#FAD06A", musF="#F2B640", musS="#D99B2A",
         pink="#F57FB5", coral="#F7926E", purple="#8D57C9", yellow="#F8D65A", mint="#7FDBA8",
         sky="#64C7F2", cream="#FFF4DE", red="#F2543D", teal="#2E9C96", navy="#3B3550")
PAL = [C["pink"], C["coral"], C["purple"], C["yellow"], C["mint"], C["sky"], C["cream"], C["red"], C["teal"], "#FF9F1C", "#5B7BE0", "#2A2440"]
pick = lambda a: a[R.randrange(len(a))]
out = []
add = out.append

# ---------- shell ----------
add(f'<polygon points="-200,-20 1800,-20 1800,240 {f(P(0,0,560)[0])},{f(P(0,0,560)[1])} -200,{f(P(0,1100,560)[1])}" fill="{C["ceil"]}"/>')
add(poly([(0,0,0),(1200,0,0),(1200,0,560),(0,0,560)], C["wall"]))
add(poly([(0,0,0),(0,0,560),(0,1200,560),(0,1200,0)], C["wallL"]))
add(poly([(0,0,0),(1200,0,0),(1200,1300,0),(0,1300,0)], C["floor"]))
tufts = []
for _ in range(110):
    x, y = R.uniform(10, 1150), R.uniform(10, 1100); a, b = P(x, y, 0)
    if 0 < a < 1600 and b < 1000: tufts.append(f"M{f(a)} {f(b)} q4 -4 8 0")
add(f'<path d="{" ".join(tufts)}" stroke="{C["tuft"]}" stroke-width="2.5" fill="none" stroke-linecap="round"/>')
add(box(0, 8, 0, 8, 1200, 20, "#F6F1FF", "#E9E2FA", "#DDD4F5", 2.5))
add(box(0, 0, 0, 1200, 8, 20, "#F6F1FF", "#E9E2FA", "#DDD4F5", 2.5))

# ---------- left wall: window, curtains, poster, neon ----------
win = [rect(0, 0, 360, 250, "url(#skyN)"), '<g id="stars">']
for _ in range(24): win.append(f'<circle class="twinkle" cx="{f(R.uniform(10,350))}" cy="{f(R.uniform(10,170))}" r="{1.6 if R.random()<.2 else 1}" fill="#FFF6D8" style="animation-delay:{-R.uniform(0,3):.1f}s"/>')
win.append('</g><circle cx="280" cy="60" r="22" fill="#FFF3D0" stroke="#1F1B3A" stroke-width="2.5"/><circle cx="292" cy="54" r="19" fill="#2A2766"/>')
win.append('<rect id="skyDay" x="0" y="0" width="360" height="250" fill="url(#skyD)"/>')
win.append('<g id="sun"><circle cx="90" cy="70" r="30" fill="#FFD36E" stroke="#1F1B3A" stroke-width="2.5"/><path d="M200 90 q10 -22 32 -12 q14 -16 30 0 q20 2 14 20 h-74 q-14 -4 -2 -8Z" fill="#fff" stroke="#1F1B3A" stroke-width="2.5"/></g>')
win.append('<path d="M0 250 V170 q20 -30 46 -10 q10 -36 44 -22 q26 -24 46 8 q22 -6 26 18 q10 20 -6 36 V250Z" fill="#4FB86A" stroke="#1F1B3A" stroke-width="3"/><path d="M40 210 q14 -10 26 0 M100 196 q12 -8 22 2" stroke="#2F8C4A" stroke-width="3" fill="none"/>')
win.append(f'<rect x="0" y="0" width="360" height="250" fill="none" stroke="{INK}" stroke-width="20"/><rect x="0" y="0" width="360" height="250" fill="none" stroke="#FFFDF6" stroke-width="13"/>')
win.append(f'<path d="M180 0 V250 M0 125 H360" stroke="{INK}" stroke-width="12"/><path d="M180 0 V250 M0 125 H360" stroke="#FFFDF6" stroke-width="6"/>')
win.append('<path d="M40 20 l40 60 M60 20 l30 44 M220 140 l40 60" stroke="#ffffff88" stroke-width="5" stroke-linecap="round"/>')
window_svg = g(mX(0, 640, 490), "".join(win))
window_svg += box(0, 270, 226, 26, 380, 12, "#FFFDF6", "#EDE6F7", "#DCD3F0", 2.5)
cact = f'<path d="M-6 0 v-26 q0 -9 8 -9 q8 0 8 9 v26Z" fill="{C["mint"]}" stroke="{INK}" stroke-width="2.5"/><path d="M-12 -6 h-8 l2 14 h18 l2 -14Z" fill="{C["pink"]}" stroke="{INK}" stroke-width="2.5"/>'
window_svg += g(at(14, 330, 238), f'<path d="M-6 0 v-26 q0 -9 8 -9 q8 0 8 9 v26Z" fill="{C["mint"]}" stroke="{INK}" stroke-width="2.5"/><path d="M-14 -2 h28 l-3 16 h-22Z" fill="{C["pink"]}" stroke="{INK}" stroke-width="2.5"/>')
def curtain():
    s = rect(0, 0, 58, 420, C["lilT"])
    s += f'<path d="M14 8 V412 M30 8 V412 M44 8 V412" stroke="{C["lilS"]}" stroke-width="3"/>'
    return s
window_svg += g(mX(0, 704, 534), curtain()) + g(mX(0, 286, 534), curtain())
window_svg += g(mX(0, 712, 540), f'<rect x="0" y="-5" width="500" height="10" rx="5" fill="{C["yellow"]}" stroke="{INK}" stroke-width="3"/><circle cx="0" cy="0" r="9" fill="{C["yellow"]}" stroke="{INK}" stroke-width="3"/><circle cx="500" cy="0" r="9" fill="{C["yellow"]}" stroke="{INK}" stroke-width="3"/>')
add(f'<g class="hot" data-toggle="win">{window_svg}</g>')

poster = (rect(0, 0, 150, 200, C["pink"]) + f'<circle cx="75" cy="88" r="40" fill="{C["yellow"]}" stroke="{INK}" stroke-width="3"/>'
          f'<ellipse cx="75" cy="92" rx="68" ry="14" fill="none" stroke="{INK}" stroke-width="7"/><ellipse cx="75" cy="92" rx="68" ry="14" fill="none" stroke="{C["mint"]}" stroke-width="3"/>'
          f'<path d="M50 70 q12 -16 30 -8 M60 104 q14 6 30 -4" stroke="{C["coral"]}" stroke-width="5" fill="none" stroke-linecap="round"/>'
          + "".join(f'<path d="M{x} {y} l3 7 7 1 -5 5 1 7 -6 -4 -6 4 1 -7 -5 -5 7 -1Z" fill="#FFF6D8" stroke="{INK}" stroke-width="1.5"/>' for x, y in [(20, 22), (120, 30), (128, 140), (16, 128)])
          + f'<text x="75" y="182" text-anchor="middle" font-family="Shrikhand, Georgia, serif" font-size="24" fill="{C["cream"]}" stroke="{INK}" stroke-width="5" paint-order="stroke">OUT THERE</text>'
          '<rect x="-8" y="-6" width="30" height="12" fill="#ffffffaa" transform="rotate(-20)"/><rect x="128" y="-6" width="30" height="12" fill="#ffffffaa" transform="rotate(20 143 0)"/>')
add(g(mX(0, 236, 430), poster))
mix = (rect(0, 0, 70, 90, C["yellow"]) + f'<rect x="10" y="22" width="50" height="32" rx="4" fill="{C["cream"]}" stroke="{INK}" stroke-width="2.5"/><circle cx="25" cy="38" r="7" fill="{INK}"/><circle cx="45" cy="38" r="7" fill="{INK}"/>'
       f'<text x="35" y="78" text-anchor="middle" font-family="Courier Prime, monospace" font-weight="700" font-size="12" fill="{INK}">MIX VOL.2</text>')
add(g(mX(0, 66, 350), mix))
for (yy, zz, rot, col) in [(62, 236, -6, C["sky"]), (118, 220, 5, C["mint"])]:
    add(g(mX(0, yy, zz), f'<g transform="rotate({rot} 24 28)">' + rect(0, 0, 48, 56, "#FFFDF6", 2.5) + rect(5, 5, 38, 36, col, 2) + '</g>'))
add(g(mX(0, 250, 528), '<text class="neon" x="10" y="40">dee\'s room</text>'))

# ---------- string lights on the back wall ----------
def qbez(p0, p1, p2, t): return ((1-t)**2*p0[0] + 2*(1-t)*t*p1[0] + t*t*p2[0], (1-t)**2*p0[1] + 2*(1-t)*t*p1[1] + t*t*p2[1])
segs = [((20, 0), (250, 56), (480, 4)), ((480, 4), (720, 56), (960, 0))]
bul = [f'<path d="M20 0 Q250 56 480 4 Q720 56 960 0" fill="none" stroke="{INK}" stroke-width="2.5"/>']
cols = ["#FFD36E", "#FF7FA8", "#8FD3FF", "#B6F09C", "#FFB36E"]
k = 0
for s in segs:
    for i in range(1, 12):
        x, y = qbez(*s, i/12); c = cols[k % 5]; k += 1
        bul.append(f'<circle class="twinkle glowb" cx="{f(x)}" cy="{f(y+10)}" r="15" fill="{c}" opacity=".35" style="animation-delay:{-(k*.37)%3:.2f}s"/>')
        bul.append(f'<ellipse cx="{f(x)}" cy="{f(y+10)}" rx="5" ry="7.5" fill="{c}" stroke="{INK}" stroke-width="2"/>')
add(g(mY(2, 0, 548), "".join(bul)))

# ---------- projector screen on the back wall ----------
scr = (rect(-12, -14, 324, 20, "#3B3550") + rect(0, 6, 300, 210, "#FFFDF6") + '<g id="scrGlow"><rect x="6" y="12" width="288" height="198" fill="#7FB2FF" opacity=".8"/></g>'
       + rect(-6, 214, 312, 9, "#3B3550") + f'<path d="M280 223 V262" stroke="{INK}" stroke-width="2.5"/><circle cx="280" cy="266" r="6" fill="{C["yellow"]}" stroke="{INK}" stroke-width="2.5"/>')
screen_svg = g(mY(4, 650, 530), scr)

# ---------- corkboard ----------
cork = [rect(0, 0, 200, 140, "#C97B45"), rect(10, 10, 180, 120, "url(#corkp)", 2)]
cardc = ["#FFF4DE", "#9BE3B5", "#FFE6A8", "#FFC1D3", "#BFD4FF"]
for i, (x, y, w, h, r) in enumerate([(20, 18, 50, 36, -6), (80, 16, 48, 40, 4), (138, 22, 42, 34, -3), (24, 70, 44, 50, 3), (82, 74, 52, 36, -4), (142, 66, 40, 46, 7)]):
    inner = rect(x, y, w, h, cardc[i % 5] if i != 3 else "#FFFDF6", 2)
    if i == 3: inner += rect(x+5, y+5, w-10, h-18, C["coral"], 1.5) + f'<circle cx="{x+w/2}" cy="{y+18}" r="7" fill="{C["yellow"]}"/>'
    else: inner += "".join(f'<rect x="{x+6}" y="{y+9+j*8}" width="{(w-12)*(0.6 if j==2 else 1)}" height="2.5" fill="#1F1B3A55"/>' for j in range(3))
    inner += f'<circle cx="{x+w/2}" cy="{y+3}" r="4" fill="{pick([C["red"],C["sky"],C["teal"],C["yellow"]])}" stroke="{INK}" stroke-width="1.5"/>'
    cork.append(f'<g transform="rotate({r} {x+w/2} {y+h/2})">{inner}</g>')
board_svg = g(mY(1, 330, 486), "".join(cork))

# glow-in-the-dark stars above the nightstand
st = ""
for (x, y, s) in [(10, 20, 1), (50, 60, .7), (20, 110, .8), (70, 140, 1.1), (30, 190, .6), (80, 30, .6)]:
    st += f'<path transform="translate({x} {y}) scale({s})" d="M0 -12 L3.5 -4 12 -3.5 5.5 2.5 7.5 11 0 6.5 -7.5 11 -5.5 2.5 -12 -3.5 -3.5 -4Z" fill="#FFF07A" stroke="{INK}" stroke-width="2"/>'
st += f'<path transform="translate(60 92)" d="M0 -14 a14 14 0 1 0 10 24 a11 11 0 1 1 -10 -24Z" fill="#FFF07A" stroke="{INK}" stroke-width="2"/>'
add(g(mY(1, 556, 520), st))

# ---------- bookshelf ----------
bs = [box(30, 0, 0, 260, 80, 470, C["lilT"], C["lilF"], C["lilS"])]
face = [rect(14, 14, 232, 442, C["inner"])]
comps = [(14, 98), (108, 192), (202, 286), (296, 380), (390, 456)]
for b in [98, 192, 286, 380]: face.append(rect(10, b, 240, 10, C["lilT"], 2.5))
for top, bot in comps:
    face.append(f'<rect x="16" y="{top+1}" width="228" height="8" fill="#00000033"/>')
    x = 20
    while x < 238:
        r = R.random()
        if r < .08 and x < 190:
            yy = bot; w = R.randint(40, 52)
            for _ in range(R.randint(3, 4)):
                h = R.randint(8, 11); face.append(rect(x + R.randint(0, 4), yy - h, w, h, pick(PAL), 2)); yy -= h
            x += w + 8; continue
        if r < .12 and x < 205:
            kind = R.randrange(3)
            if kind == 0:
                face.append(f'<path d="M{x} {bot} l3 -20 h20 l3 20Z" fill="{C["coral"]}" stroke="{INK}" stroke-width="2"/><path d="M{x+13} {bot-20} q-14 -16 -6 -30 q8 8 6 30 q4 -22 16 -24 q0 18 -16 24" fill="{C["mint"]}" stroke="{INK}" stroke-width="2"/>')
            elif kind == 1:
                for i in range(3):
                    for j in range(3): face.append(f'<rect x="{x+i*8}" y="{bot-24+j*8}" width="8" height="8" fill="{["#F2543D","#F8D65A","#5B7BE0","#7FDBA8","#FFFDF6","#FF9F1C"][(i+j*2)%6]}" stroke="{INK}" stroke-width="1.5"/>')
            else:
                face.append(f'<path d="M{x+4} {bot} h18 v-6 h-5 v-8 q10 -2 10 -16 h-28 q0 14 10 16 v8 h-5Z" fill="{C["yellow"]}" stroke="{INK}" stroke-width="2"/>')
            x += 34; continue
        w = R.randint(10, 20); h = (bot - top) - R.randint(6, 30); c = pick(PAL)
        lean = x > 210 and R.random() < .7
        b = rect(x, bot - h, w, h, c, 2) + (f'<rect x="{x+2}" y="{bot-h+7}" width="{w-4}" height="3" fill="#ffffff66"/><rect x="{x+2}" y="{bot-14}" width="{w-4}" height="3" fill="#ffffff66"/>' if R.random() < .6 else "")
        face.append(f'<g transform="rotate(-10 {x+w} {bot})">{b}</g>' if lean else b)
        x += w + 1
        if lean: break
bs.append(g(mY(80, 30, 470), "".join(face)))
bs.append(box(170, 14, 470, 80, 52, 14, C["yellow"], "#E9C143", "#CFA92F", 2.5) + box(178, 18, 484, 66, 44, 12, C["sky"], "#4FB4E2", "#3A9CCB", 2.5) + box(174, 16, 496, 72, 48, 12, C["pink"], "#E96BA2", "#D2558C", 2.5))
plant = (f'<path d="M-20 0 l-4 -34 h48 l-4 34Z" fill="{C["coral"]}" stroke="{INK}" stroke-width="3"/><rect x="-28" y="-42" width="56" height="10" rx="3" fill="#FF9F80" stroke="{INK}" stroke-width="3"/>'
         f'<path d="M-6 -42 c-30 -10 -40 -40 -30 -60 c20 6 30 30 30 60 M4 -42 c0 -30 10 -54 28 -62 c6 26 -6 46 -28 62 M0 -42 c-4 -30 -2 -56 6 -70 c10 20 6 46 -6 70" fill="{C["mint"]}" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>'
         f'<path d="M-20 -30 c-10 30 -16 60 -12 100" stroke="{INK}" stroke-width="5" fill="none"/><path d="M-20 -30 c-10 30 -16 60 -12 100" stroke="#4FB86A" stroke-width="2.5" fill="none"/>'
         + "".join(f'<ellipse cx="{x}" cy="{y}" rx="8" ry="5" transform="rotate({r} {x} {y})" fill="{C["mint"]}" stroke="{INK}" stroke-width="2"/>' for x, y, r in [(-28, 0, 50), (-32, 30, 70), (-30, 60, 80)]))
bs.append(g(at(80, 36, 470), plant))
add(f'<g class="hot" data-go="books">{"".join(bs)}</g>')

# ---------- record cabinet, record player, wall shelf with sleeves ----------
rc = []
for (lx, ly) in [(326, 6), (528, 6), (326, 84), (528, 84)]: rc.append(box(lx, ly, 0, 8, 8, 18, "#3B3550", "#2C2840", "#221F33", 2))
rc.append(box(320, 0, 18, 220, 95, 112, C["musT"], C["musF"], C["musS"]))
fr = [rect(12, 10, 98, 92, "#3A2A5E")]
x = 16
while x < 106:
    w = R.randint(4, 6); fr.append(f'<rect x="{x}" y="{100-R.randint(80,86)}" width="{w}" height="86" fill="{pick(PAL)}" stroke="{INK}" stroke-width="1"/>'); x += w + .5
fr.append(rect(120, 10, 88, 92, C["coral"]))
for cx_, cy_ in [(142, 34), (186, 34), (142, 78), (186, 78)]: fr.append(f'<circle cx="{cx_}" cy="{cy_}" r="11" fill="{C["yellow"]}" stroke="{INK}" stroke-width="2"/>')
fr.append(f'<circle cx="164" cy="56" r="11" fill="{C["teal"]}" stroke="{INK}" stroke-width="2"/><rect x="124" y="48" width="6" height="16" rx="3" fill="{INK}"/>')
rc.append(g(mY(95, 320, 130), "".join(fr)))
rc.append(box(338, 12, 130, 140, 74, 24, C["woodT"], C["woodF"], C["woodS"]))
tt = (f'<circle cx="52" cy="37" r="33" fill="#3B3550" stroke="{INK}" stroke-width="3"/>'
      f'<g class="spin"><circle cx="52" cy="37" r="30" fill="#17131F"/><circle cx="52" cy="37" r="23" fill="none" stroke="#2E2840" stroke-width="2"/><circle cx="52" cy="37" r="16" fill="none" stroke="#2E2840" stroke-width="2"/>'
      f'<circle id="recLabel" cx="52" cy="37" r="10" fill="{C["yellow"]}"/><rect x="50" y="27" width="4" height="7" fill="{INK}" opacity=".6"/><circle cx="52" cy="37" r="2" fill="#ddd"/></g>'
      f'<g id="arm" style="transform-origin:122px 14px"><circle cx="122" cy="14" r="6" fill="#E6E1F0" stroke="{INK}" stroke-width="2"/><path d="M122 14 L118 52 L108 60" stroke="{INK}" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M122 14 L118 52 L108 60" stroke="#E6E1F0" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>'
      f'<rect x="100" y="60" width="12" height="7" rx="2" fill="{C["red"]}" stroke="{INK}" stroke-width="1.5"/>')
rc.append(g(mZ(154, 338, 12), tt))
lava = (f'<path d="M-16 0 l6 -18 h20 l6 18Z" fill="{C["purple"]}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
        f'<path d="M-10 -18 l-6 -48 q16 -12 32 0 l-6 48Z" fill="url(#lavaG)" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
        f'<ellipse class="blob" cx="0" cy="-30" rx="7" ry="9" fill="#FFE6A8"/><ellipse class="blob b2" cx="-3" cy="-44" rx="5" ry="6" fill="#FFE6A8"/>'
        f'<path d="M-14 -66 l4 -16 h20 l4 16Z" fill="{C["purple"]}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>')
rc.append(g(at(512, 50, 130), lava))
rc.append(box(320, 0, 240, 220, 34, 10, C["woodT"], C["woodF"], C["woodS"], 2.5))
sl = (f'<g transform="rotate(-4 32 70)">{rect(0, 2, 64, 66, C["yellow"])}<circle cx="32" cy="52" r="18" fill="{C["red"]}" stroke="{INK}" stroke-width="2.5"/>{rect(0, 54, 64, 14, C["teal"], 2.5)}</g>'
      f'{rect(66, 0, 66, 68, C["teal"])}<g fill="none" stroke="#FFF4DE" stroke-width="4"><circle cx="99" cy="34" r="8"/><circle cx="99" cy="34" r="17"/><circle cx="99" cy="34" r="26"/></g>'
      f'<g transform="rotate(3 162 68)">{rect(134, 6, 58, 62, C["pink"])}<path d="M134 6 h14.5 v15.5 h-14.5Z M163 6 h14.5 v15.5 h-14.5Z M148.5 21.5 h14.5 v15.5 h-14.5Z M177.5 21.5 h14.5 v15.5 h-14.5Z M134 37 h14.5 v15.5 h-14.5Z M163 37 h14.5 v15.5 h-14.5Z M148.5 52.5 h14.5 v15.5 h-14.5Z M177.5 52.5 h14.5 v15.5 h-14.5Z" fill="#FFF4DE"/></g>')
rc.append(g(mY(16, 326, 318), sl))
records_svg = "".join(rc)

# projector on the right end of the wall shelf
pj = box(474, 4, 250, 56, 26, 32, "#F7EEDB", "#EADFC6", "#D6C9AC")
pj += g(mY(17, 474, 300), f'<circle cx="14" cy="16" r="15" fill="#2A2440" stroke="{INK}" stroke-width="2.5"/><circle cx="42" cy="12" r="17" fill="#2A2440" stroke="{INK}" stroke-width="2.5"/><circle cx="14" cy="16" r="4" fill="#C9C1D6"/><circle cx="42" cy="12" r="4" fill="#C9C1D6"/>')
pj += g(mX(530, 28, 278), f'<circle cx="12" cy="12" r="9" fill="#17131F" stroke="{INK}" stroke-width="2.5"/><circle cx="10" cy="10" r="3" fill="#BFD4FF"/>')

lx, ly = P(538, 16, 268)
beam = [P(650, 4, 524), P(950, 4, 524), P(950, 4, 316), P(650, 4, 316)]
beam_svg = f'<polygon id="beam" points="{f(lx)},{f(ly)} ' + " ".join(f"{f(a)},{f(b)}" for a, b in beam) + '" fill="url(#beamG)" style="mix-blend-mode:screen;pointer-events:none"/>'

add(f'<g class="hot" data-go="board">{board_svg}</g>')
add(f'<g class="hot" data-go="screen">{screen_svg}</g>')
add(f'<g class="hot" data-go="records">{records_svg}</g>')
add(f'<g class="hot" data-go="screen">{pj}</g>')
add(beam_svg)

# ---------- nightstand + mushroom lamp ----------
ns = box(560, 0, 0, 82, 80, 112, C["woodT"], C["woodF"], C["woodS"])
ns += g(mY(80, 560, 112), rect(8, 10, 66, 40, C["woodT"], 2.5) + rect(8, 58, 66, 44, C["woodT"], 2.5) + f'<circle cx="41" cy="30" r="4" fill="{INK}"/><circle cx="41" cy="80" r="4" fill="{INK}"/>'
        f'<circle cx="18" cy="76" r="7" fill="{C["mint"]}" stroke="{INK}" stroke-width="1.5"/><path d="M58 64 l3 6 6 1 -4 4 1 6 -6 -3 -6 3 1 -6 -4 -4 6 -1Z" fill="{C["yellow"]}" stroke="{INK}" stroke-width="1.5"/>')
add(ns)
lamp = (f'<ellipse cx="0" cy="0" rx="24" ry="8" fill="#C8502A" stroke="{INK}" stroke-width="3"/><rect x="-5" y="-70" width="10" height="68" fill="#FFF4DE" stroke="{INK}" stroke-width="3"/>'
        f'<path id="lampShade" d="M-44 -64 Q0 -128 44 -64 Z" fill="#FF7A45" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
        f'<path d="M-30 -84 q8 -14 20 -18" stroke="#FFFFFF99" stroke-width="5" fill="none" stroke-linecap="round"/>'
        + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFF4DE" stroke="{INK}" stroke-width="1.5"/>' for x, y, r in [(-16, -78, 5), (12, -92, 6), (24, -72, 4)]))
lamp_x, lamp_y = P(600, 40, 112)
add(f'<g class="hot" data-toggle="lamp" transform="translate({f(lamp_x)} {f(lamp_y)})">{lamp}</g>')

# ---------- desk, laptop, chair (left wall) ----------
dk = box(0, 262, 0, 140, 14, 162, C["woodT"], C["woodF"], C["woodS"])
dk += box(0, 600, 0, 140, 80, 162, C["woodT"], C["woodF"], C["woodS"])
dk += g(mX(140, 680, 150), rect(8, 8, 64, 60, C["woodT"], 2.5) + rect(8, 76, 64, 64, C["woodT"], 2.5) + f'<rect x="30" y="34" width="20" height="6" rx="3" fill="{INK}"/><rect x="30" y="104" width="20" height="6" rx="3" fill="{INK}"/>')
dk += box(0, 250, 162, 156, 440, 14, C["woodT"], C["woodF"], C["woodS"])
dk += box(30, 560, 176, 70, 50, 8, C["pink"], "#E96BA2", "#D2558C", 2.5) + box(34, 564, 184, 62, 44, 8, C["cream"], "#EFE2C8", "#DCCCAE", 2.5)
mug = (f'<path d="M-12 0 v-28 h24 v28 q0 4 -4 4 h-16 q-4 0 -4 -4Z" fill="{C["teal"]}" stroke="{INK}" stroke-width="3"/><path d="M12 -22 q12 0 10 10 q-2 8 -10 6" stroke="{INK}" stroke-width="3" fill="none"/>'
       f'<g class="steam" stroke="#FFFDF6" stroke-width="3" fill="none" stroke-linecap="round"><path d="M-4 -34 q-6 -10 2 -18 q6 -8 0 -16"/><path d="M6 -34 q6 -10 -2 -18 q-6 -8 0 -16"/></g>')
dk += g(at(70, 320, 176), mug)
add(dk)
lt = box(30, 380, 176, 84, 130, 6, "#E6E1F0", "#D3CCE3", "#BEB6D2", 2.5)
lt += box(22, 380, 182, 8, 130, 92, "#E6E1F0", "#D3CCE3", "#BEB6D2", 2.5)
scr_ui = (rect(6, 6, 118, 80, "#24345C", 2) + rect(14, 14, 56, 36, "#C9D3E8", 1.5) + f'<rect x="14" y="14" width="56" height="6" fill="{INK}"/>'
          + rect(52, 38, 64, 40, "#FFF4DE", 1.5) + f'<rect x="52" y="38" width="64" height="6" fill="{INK}"/><g fill="#1F1B3A66"><rect x="58" y="50" width="40" height="3"/><rect x="58" y="58" width="50" height="3"/><rect x="58" y="66" width="30" height="3"/></g>'
          f'<circle cx="22" cy="72" r="4" fill="{C["yellow"]}"/><circle cx="34" cy="72" r="4" fill="{C["pink"]}"/>')
lt += g(mX(30, 508, 270), scr_ui)
add(f'<g class="hot" data-go="laptop">{lt}</g>')
ch = f'<g transform="{at(214, 444, 0)}"><path d="M-48 6 L48 -6 M-30 -16 L30 16 M0 -22 L0 22" stroke="{INK}" stroke-width="9" stroke-linecap="round"/><path d="M-48 6 L48 -6 M-30 -16 L30 16 M0 -22 L0 22" stroke="#E6E1F0" stroke-width="5" stroke-linecap="round"/>' + "".join(f'<circle cx="{x}" cy="{y+6}" r="6" fill="{INK}"/>' for x, y in [(-48, 6), (48, -6), (-30, -16), (30, 16), (0, -22), (0, 22)]) + '</g>'
ch += box(207, 437, 10, 14, 14, 82, "#C9C1D6", "#B3AAC6", "#9E95B4", 2.5)
ch += box(166, 398, 92, 96, 92, 20, C["purple"], "#7A47B4", "#673A9C")
ch += box(258, 404, 112, 16, 80, 120, C["purple"], "#7A47B4", "#673A9C")
ch += g(mX(274, 484, 214), f'<path d="M6 16 q30 18 68 -4" stroke="{C["sky"]}" stroke-width="10" fill="none" stroke-linecap="round"/>')
add(ch)

# ---------- rug + floor clutter ----------
rug = rect(0, 0, 360, 280, "#8FD3F5") + "".join(f'<path d="M{x} 6 V274" stroke="#B9E5FA" stroke-width="7"/>' for x in range(20, 360, 26)) + rect(0, 0, 360, 280, "none") \
      + "".join(f'<path d="M{x} 280 v12 M{x} 0 v-12" stroke="{INK}" stroke-width="2"/>' for x in range(8, 360, 14))
add(g(mZ(0.5, 200, 420), rug))
add(g(mZ(0.5, 120, 620), rect(0, 0, 70, 44, "#3B3550", 2.5) + rect(8, 8, 54, 16, C["yellow"], 2) + f'<circle cx="22" cy="32" r="5" fill="#E6E1F0" stroke="{INK}" stroke-width="2"/><circle cx="48" cy="32" r="5" fill="#E6E1F0" stroke="{INK}" stroke-width="2"/>'))
add(box(380, 470, 0, 92, 66, 14, C["yellow"], "#E9C143", "#CFA92F", 2.5) + box(386, 474, 14, 80, 58, 12, C["mint"], "#69C893", "#56B07E", 2.5) + box(384, 470, 26, 86, 62, 10, C["coral"], "#E97C59", "#D46A48", 2.5))
for i in range(3):
    add(box(430, 250 + i * 3, i * 12, 76, 44, 12, "#3B3550", "#2C2840", "#221F33", 2.5))
    add(g(mY(294 + i * 3, 430, (i + 1) * 12), f'<rect x="10" y="3" width="40" height="6" fill="{[C["yellow"],C["pink"],C["sky"]][i]}"/>'))
def sock(c):
    return (f'<path d="M0 0 h18 v26 q0 6 6 6 h14 q8 0 8 8 q0 8 -8 8 h-26 q-12 0 -12 -12Z" fill="#FFFDF6" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
            f'<path d="M0 6 h18 M0 12 h18" stroke="{c}" stroke-width="3"/><path d="M30 32 q8 0 8 8 q0 8 -8 8 h-4 v-16Z" fill="{c}" stroke="{INK}" stroke-width="2.5"/>')
add(f'<g transform="translate(720 690) rotate(-30)">{sock(C["pink"])}</g>')
add(f'<g transform="translate(470 905) rotate(60)">{sock(C["sky"])}</g>')
shoe = (f'<path d="M0 0 q-2 -18 14 -20 l10 -10 h18 q10 14 30 16 q10 2 10 12 v4Z" fill="{C["coral"]}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
        f'<path d="M-2 0 h86 v8 h-86Z" fill="#FFFDF6" stroke="{INK}" stroke-width="3"/><path d="M24 -28 l8 10 M34 -28 l6 10" stroke="{INK}" stroke-width="2.5"/><path d="M50 -10 l8 -4 l6 6" stroke="#FFFDF6" stroke-width="3" fill="none"/>')
add(f'<g transform="translate(150 930) rotate(-12)">{shoe}</g><g transform="translate(232 968) rotate(8)">{shoe}</g>')
pad = (f'<path d="M-40 -14 q-18 0 -20 18 q-2 18 12 18 q10 0 16 -10 h64 q6 10 16 10 q14 0 12 -18 q-2 -18 -20 -18Z" fill="#C9C1D6" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
       f'<path d="M-40 -4 h-12 M-46 -10 v12" stroke="{INK}" stroke-width="4" stroke-linecap="round"/><circle cx="36" cy="-6" r="4" fill="{C["red"]}" stroke="{INK}" stroke-width="2"/><circle cx="46" cy="2" r="4" fill="{C["sky"]}" stroke="{INK}" stroke-width="2"/>'
       f'<path d="M0 -14 q10 -30 40 -26" stroke="{INK}" stroke-width="2.5" fill="none"/>')
add(f'<g transform="translate(800 820) rotate(-8)">{pad}</g>')

# ---------- bed ----------
bed = box(656, 0, 0, 308, 20, 240, C["woodT"], C["woodF"], C["woodS"])
bed += g(mY(20, 656, 240), rect(22, 18, 264, 120, "url(#cane)", 2.5))
bed += box(660, 20, 0, 300, 450, 70, C["woodT"], C["woodF"], C["woodS"])
bed += box(668, 22, 70, 286, 444, 40, C["cream"], "#EFE2C8", "#DCCCAE")
def pillow(x0, col, line):
    t = mZ(110, x0, 34)
    shape = f'<rect x="0" y="0" width="122" height="74" rx="26" fill="{col}" stroke="{INK}" stroke-width="3"/>'
    return (f'<g transform="translate(0 16) {t}"><rect x="0" y="0" width="122" height="74" rx="26" fill="{line}" stroke="{INK}" stroke-width="3"/></g>'
            f'<g transform="translate(0 2) {t}">{shape}<path d="M20 22 l12 8 12 -8 12 8 M60 46 l12 8 12 -8 12 8" stroke="{line}" stroke-width="4" fill="none"/></g>')
bed += pillow(684, C["pink"], "#D2558C") + pillow(818, C["yellow"], "#CFA92F")
patch = ["#F2543D", C["teal"], C["yellow"], C["pink"], C["mint"], C["cream"], C["lilT"], "#FF9F1C", C["sky"]]
q = []
for i in range(7):
    for j in range(6): q.append(f'<rect x="{i*41}" y="{j*53.5}" width="41" height="53.5" fill="{pick(patch)}"/>')
q.append(f'<g stroke="#FFFDF6" stroke-width="2" stroke-dasharray="5 4">' + "".join(f'<path d="M{i*41} 0 V321"/>' for i in range(1, 7)) + "".join(f'<path d="M0 {j*53.5} H287"/>' for j in range(1, 6)) + '</g>')
q.append(rect(0, 0, 287, 321, "none"))
bed += g(mZ(110.5, 668, 147), "".join(q))
fq = "".join(f'<rect x="{i*41}" y="0" width="41" height="66" fill="{pick(patch)}"/>' for i in range(7)) + f'<g stroke="#FFFDF6" stroke-width="2" stroke-dasharray="5 4">' + "".join(f'<path d="M{i*41} 0 V66"/>' for i in range(1, 7)) + '</g>' + rect(0, 0, 287, 66, "none")
bed += g(mY(468, 668, 110.5), fq)
sq = "".join(f'<rect x="{j*53.5}" y="0" width="53.5" height="66" fill="{pick(patch)}"/>' for j in range(6)) + f'<g stroke="#FFFDF6" stroke-width="2" stroke-dasharray="5 4">' + "".join(f'<path d="M{j*53.5} 0 V66"/>' for j in range(1, 6)) + '</g>' + rect(0, 0, 321, 66, "none")
bed += g(mX(955, 468, 110.5), sq)
add(bed)

# ---------- the cats ----------
ax, ay = P(770, 330, 112)
add(f'''<g id="catA" class="hot cat" data-cat="catA"><g transform="translate({f(ax)} {f(ay)}) scale(.9)"><g class="breathe">
<ellipse cx="0" cy="0" rx="74" ry="36" fill="#F09A3E" stroke="{INK}" stroke-width="3.5"/>
<g stroke="#B85C1A" stroke-width="5" fill="none" stroke-linecap="round"><path d="M-12 -34 q7 14 0 26"/><path d="M8 -35 q7 14 0 26"/><path d="M28 -31 q7 12 0 22"/><path d="M46 -24 q6 10 0 18"/></g>
<g class="tail"><path d="M66 8 C72 32 30 42 -10 36 C-38 33 -56 28 -64 20" stroke="{INK}" stroke-width="23" fill="none" stroke-linecap="round"/><path d="M66 8 C72 32 30 42 -10 36 C-38 33 -56 28 -64 20" stroke="#F09A3E" stroke-width="16" fill="none" stroke-linecap="round"/>
<g stroke="#B85C1A" stroke-width="4"><path d="M40 30 v10"/><path d="M14 33 v10"/><path d="M-14 31 v10"/></g></g>
<ellipse cx="-28" cy="30" rx="13" ry="7" fill="#FFF4DE" stroke="{INK}" stroke-width="2.5"/>
<path d="M-84 -10 L-80 -44 L-58 -24 Z" fill="#F7A54E" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/><path d="M-80 -16 L-78 -34 L-66 -24 Z" fill="#F6B7C4"/>
<path d="M-52 -26 L-32 -46 L-30 -14 Z" fill="#F7A54E" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/><path d="M-47 -24 L-35 -37 L-34 -18 Z" fill="#F6B7C4"/>
<circle cx="-58" cy="2" r="29" fill="#F7A54E" stroke="{INK}" stroke-width="3.5"/>
<g stroke="#B85C1A" stroke-width="3" stroke-linecap="round"><path d="M-64 -24 v8"/><path d="M-57 -26 v9"/><path d="M-50 -24 v8"/></g>
<ellipse cx="-57" cy="14" rx="12" ry="8" fill="#FFF4DE"/>
<g stroke="{INK}" stroke-width="2.8" fill="none" stroke-linecap="round"><path d="M-74 0 q5 5 10 0"/><path d="M-52 0 q5 5 10 0"/></g>
<path d="M-60 9 h6 l-3 4 Z" fill="#E8577E" stroke="{INK}" stroke-width="1.2"/>
<g stroke="{INK}" stroke-width="1.4"><path d="M-72 14 l-18 -2 M-72 17 l-18 3 M-42 14 l18 -2 M-42 17 l18 3"/></g>
</g></g></g>''')
add(f'<text class="zz" x="{f(ax-74)}" y="{f(ay-52)}" font-size="24">z</text><text class="zz" x="{f(ax-58)}" y="{f(ay-62)}" font-size="17">z</text>')
bx, by = P(870, 190, 112)
add(f'''<g id="catB" class="hot cat" data-cat="catB"><g transform="translate({f(bx)} {f(by)}) scale(.9)"><g class="breathe">
<g class="tail"><path d="M-80 8 C-100 14 -104 34 -92 46" stroke="{INK}" stroke-width="20" fill="none" stroke-linecap="round"/><path d="M-80 8 C-100 14 -104 34 -92 46" stroke="#2E2A38" stroke-width="13" fill="none" stroke-linecap="round"/></g>
<ellipse cx="0" cy="0" rx="86" ry="30" fill="#2E2A38" stroke="{INK}" stroke-width="3.5"/>
<path d="M-50 -16 q50 -16 100 -6" stroke="#4A4458" stroke-width="6" fill="none" stroke-linecap="round"/>
<ellipse cx="-58" cy="22" rx="22" ry="10" fill="#2E2A38" stroke="{INK}" stroke-width="3"/>
<ellipse cx="66" cy="26" rx="14" ry="7" fill="#FFF4DE" stroke="{INK}" stroke-width="2.5"/><ellipse cx="94" cy="24" rx="13" ry="7" fill="#FFF4DE" stroke="{INK}" stroke-width="2.5"/>
<path d="M66 -26 L62 -60 L88 -40 Z" fill="#2E2A38" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/><path d="M68 -32 L66 -50 L80 -40 Z" fill="#E8577E"/>
<path d="M98 -40 L118 -58 L118 -24 Z" fill="#2E2A38" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/><path d="M104 -38 L114 -48 L114 -32 Z" fill="#E8577E"/>
<circle cx="90" cy="-12" r="28" fill="#2E2A38" stroke="{INK}" stroke-width="3.5"/>
<path d="M68 6 Q90 18 112 6" stroke="{INK}" stroke-width="8" fill="none"/><path d="M68 6 Q90 18 112 6" stroke="{C["red"]}" stroke-width="5" fill="none"/><circle cx="90" cy="15" r="5" fill="{C["yellow"]}" stroke="{INK}" stroke-width="2"/>
<ellipse cx="90" cy="0" rx="11" ry="7" fill="#FFF4DE"/>
<g stroke="#D6CFE6" stroke-width="2.8" fill="none" stroke-linecap="round"><path d="M74 -14 q5 4 10 0"/><path d="M96 -14 q5 4 10 0"/></g>
<path d="M87 -5 h6 l-3 4 Z" fill="#E8577E"/>
<g stroke="#D6CFE6" stroke-width="1.3"><path d="M78 0 l-20 -3 M78 3 l-20 3 M102 0 l20 -3 M102 3 l20 3"/></g>
</g></g></g>''')

# ---------- light ----------
gx, gy = lamp_x, lamp_y - 90
lvx, lvy = P(512, 50, 175)
lpx, lpy = P(30, 444, 225)
add('<rect id="nightTint" x="-50" y="-50" width="1700" height="1100" fill="#1B1442" style="mix-blend-mode:multiply;pointer-events:none" opacity=".16"/>')
add(f'<g style="pointer-events:none"><circle id="lampGlow" class="glow" cx="{f(gx)}" cy="{f(gy)}" r="320" fill="url(#warm)"/>'
    f'<circle class="glow" cx="{f(lvx)}" cy="{f(lvy)}" r="70" fill="url(#pinkG)" opacity=".7"/><circle class="glow" cx="{f(lpx)}" cy="{f(lpy)}" r="110" fill="url(#blueG)" opacity=".7"/>'
    + g(mX(0, 250, 528), '<text class="neon" x="10" y="40" opacity=".4" style="mix-blend-mode:screen">dee\'s room</text>') + '</g>')
add('<g id="fx" style="pointer-events:none"></g>')

DEFS = f'''<defs>
<pattern id="cane" width="14" height="14" patternUnits="userSpaceOnUse"><rect width="14" height="14" fill="#F7D9A8"/><circle cx="7" cy="7" r="4" fill="none" stroke="#C99A5E" stroke-width="1.6"/><path d="M0 0 L14 14 M14 0 L0 14" stroke="#DDB27A" stroke-width="1"/></pattern>
<pattern id="corkp" width="8" height="8" patternUnits="userSpaceOnUse"><rect width="8" height="8" fill="#D9A86C"/><circle cx="2" cy="3" r=".9" fill="#A97A45"/><circle cx="6" cy="6" r=".7" fill="#EAC690"/></pattern>
<linearGradient id="skyN" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1C1C4E"/><stop offset=".6" stop-color="#4A3278"/><stop offset="1" stop-color="#E0726A"/></linearGradient>
<linearGradient id="skyD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5DB8F5"/><stop offset="1" stop-color="#BFE8FB"/></linearGradient>
<linearGradient id="lavaG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFB36E"/><stop offset="1" stop-color="#FF5C8A"/></linearGradient>
<linearGradient id="beamG" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#FFF6D8" stop-opacity=".6"/><stop offset="1" stop-color="#FFF6D8" stop-opacity=".06"/></linearGradient>
<radialGradient id="warm"><stop offset="0" stop-color="#FFC870" stop-opacity=".75"/><stop offset=".45" stop-color="#FF9F4A" stop-opacity=".25"/><stop offset="1" stop-color="#FF9F4A" stop-opacity="0"/></radialGradient>
<radialGradient id="pinkG"><stop offset="0" stop-color="#FF7A8A" stop-opacity=".7"/><stop offset="1" stop-color="#FF7A8A" stop-opacity="0"/></radialGradient>
<radialGradient id="blueG"><stop offset="0" stop-color="#8FB6FF" stop-opacity=".6"/><stop offset="1" stop-color="#8FB6FF" stop-opacity="0"/></radialGradient>
<filter id="neonGlow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>'''

svg = ('<svg id="room" viewBox="0 0 1600 1000" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="roomTitle">'
       '<title id="roomTitle">Dee\'s bedroom, seen from the corner: a lilac bookshelf, a record player on a mustard cabinet, a projector screen over the bed, two sleeping cats on a patchwork quilt, and a desk with a laptop under the window</title>'
       + DEFS + "".join(out) + "</svg>")
(pathlib.Path(__file__).parent / "room.svg").write_text(svg)
print("scene", len(svg))
