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

# ---------- toy car shelf above the bed ----------
def wheel(x):
    return f'<g transform="translate({x} -7)"><g class="wh"><circle r="7.5" fill="{INK}"/><circle r="3.8" fill="#C9C1D6"/><path d="M0 -3.8 V3.8 M-3.8 0 H3.8" stroke="{INK}" stroke-width="1"/></g></g>'
CARS = {
  "f40": ("#E8302A", 'M2 -8 Q2 -14 10 -15 L30 -17 L44 -27 L60 -27 L70 -18 L88 -15 Q92 -14 92 -9 L92 -6 Q92 -3 88 -3 L6 -3 Q2 -3 2 -8Z',
          'M45 -25 L58 -25 L66 -18 L40 -18Z', '<path d="M-1 -22 h19 v4 h-19Z" fill="#E8302A" stroke="#1F1B3A" stroke-width="2"/><path d="M7 -18 v4 M13 -18 v4" stroke="#1F1B3A" stroke-width="2"/><path d="M24 -11 h14 M26 -8 h10" stroke="#1F1B3A" stroke-width="1.6"/>'),
  "r34": ("#2C5BBF", 'M2 -7 L2 -16 Q3 -18 8 -18 L24 -19 L36 -30 L62 -30 L72 -20 L90 -17 Q93 -16 93 -11 L93 -6 Q93 -3 89 -3 L6 -3 Q2 -3 2 -7Z',
          'M38 -28 L50 -28 L50 -20 L30 -20Z M53 -28 L61 -28 L68 -20 L53 -20Z', '<path d="M-1 -24 h17 v3 h-17Z" fill="#2C5BBF" stroke="#1F1B3A" stroke-width="2"/><path d="M6 -21 v3 M11 -21 v3" stroke="#1F1B3A" stroke-width="2"/><path d="M4 -10 H90" stroke="#1F1B3A" stroke-width="1.2" opacity=".5"/>'),
  "e30": ("#F2EEE4", 'M2 -6 L2 -17 Q2 -19 6 -19 L22 -20 L32 -32 L62 -32 L72 -20 L90 -19 Q93 -19 93 -15 L93 -6 Q93 -3 90 -3 L5 -3 Q2 -3 2 -6Z',
          'M34 -30 L46 -30 L46 -21 L27 -21Z M49 -30 L60 -30 L68 -21 L49 -21Z', '<path d="M-1 -9 h7 M89 -9 h6" stroke="#9A93A8" stroke-width="3"/><path d="M6 -12 H88" stroke="#3B6BC4" stroke-width="2"/><path d="M6 -14 H88" stroke="#E8302A" stroke-width="2"/>'),
}
def car(k):
    col, body, win, extra = CARS[k]
    return (f'<path d="{body}" fill="{col}" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>'
            f'<path d="{win}" fill="#24345C" stroke="{INK}" stroke-width="1.8"/>' + extra + wheel(20) + wheel(74))
cars_svg = box(672, 0, 320, 284, 24, 10, C["woodT"], C["woodF"], C["woodS"], 2.5)
cars_svg += g(mY(1, 672, 330), f'<path d="M20 0 v18 h10 M264 0 v18 h-10" stroke="{INK}" stroke-width="4" fill="none"/>')
car_hots = ""
for k, x in [("f40", 680), ("r34", 772), ("e30", 864)]:
    car_hots += f'<g class="hot car" data-toggle="car" data-car="{k}">' + g(mY(12, x, 330), f'<g class="carbody">{car(k)}</g>') + '</g>'

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
        f'<ellipse class="blob lavablob" cx="0" cy="-30" rx="7" ry="9" fill="#FFE6A8"/><ellipse class="blob b2 lavablob" cx="-3" cy="-44" rx="5" ry="6" fill="#FFE6A8"/>'
        f'<path d="M-14 -66 l4 -16 h20 l4 16Z" fill="{C["purple"]}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>')
rc.append(box(320, 0, 240, 220, 34, 10, C["woodT"], C["woodF"], C["woodS"], 2.5))
sl = (f'<g transform="rotate(-4 32 70)">{rect(0, 2, 64, 66, C["yellow"])}<circle cx="32" cy="52" r="18" fill="{C["red"]}" stroke="{INK}" stroke-width="2.5"/>{rect(0, 54, 64, 14, C["teal"], 2.5)}</g>'
      f'{rect(66, 0, 66, 68, C["teal"])}<g fill="none" stroke="#FFF4DE" stroke-width="4"><circle cx="99" cy="34" r="8"/><circle cx="99" cy="34" r="17"/><circle cx="99" cy="34" r="26"/></g>'
      f'<g transform="rotate(3 162 68)">{rect(134, 6, 58, 62, C["pink"])}<path d="M134 6 h14.5 v15.5 h-14.5Z M163 6 h14.5 v15.5 h-14.5Z M148.5 21.5 h14.5 v15.5 h-14.5Z M177.5 21.5 h14.5 v15.5 h-14.5Z M134 37 h14.5 v15.5 h-14.5Z M163 37 h14.5 v15.5 h-14.5Z M148.5 52.5 h14.5 v15.5 h-14.5Z M177.5 52.5 h14.5 v15.5 h-14.5Z" fill="#FFF4DE"/></g>')
rc.append(g(mY(16, 326, 318), sl))
records_svg = "".join(rc)

add(f'<g class="hot" data-go="board">{board_svg}</g>')
add(f'<g class="hot" data-go="records">{records_svg}</g>')
add(f'<g class="hot" data-toggle="lava" transform="{at(512, 50, 130)}">{lava}</g>')
add(cars_svg + car_hots)

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
TAN, TANF, TANS = "#FF9A3A", "#FF8A2A", "#E8761C"
lt = box(30, 384, 176, 82, 124, 12, "#F7F2EA", TANF, TANS, 2.5)
lt += g(mZ(188, 40, 396), rect(0, 0, 30, 100, "#E9E3D8", 2) + "".join(f'<path d="M{x} 3 V97" stroke="#BDB5A6" stroke-width="1.2"/>' for x in (8, 15, 22)) + "".join(f'<path d="M3 {y} H27" stroke="#BDB5A6" stroke-width="1.2"/>' for y in range(12, 100, 11)))
lt += g(mY(508, 30, 188), f'<path d="M14 0 C14 24 66 24 66 0" fill="none" stroke="{INK}" stroke-width="10" stroke-linecap="round"/><path d="M14 0 C14 24 66 24 66 0" fill="none" stroke="{TAN}" stroke-width="5" stroke-linecap="round"/>')
lt += box(20, 384, 186, 12, 124, 100, TAN, TANF, TANS, 2.5)
os9 = (f'<rect x="6" y="6" width="112" height="88" rx="10" fill="#F7F2EA" stroke="{INK}" stroke-width="2"/>'
       f'<rect x="14" y="13" width="96" height="70" rx="3" fill="#6F7FC6" stroke="{INK}" stroke-width="2"/>'
       f'<rect x="14" y="13" width="96" height="7" fill="#F4F2F0"/><path d="M14 20 H110" stroke="{INK}" stroke-width="1"/>'
       + rect(26, 28, 58, 40, "#E6E3DE", 1.5) + '<g stroke="#9C98A8" stroke-width="1">' + "".join(f'<path d="M27 {y} H83"/>' for y in (31, 33, 35)) + '</g>'
       + rect(32, 40, 46, 24, "#FFFDF6", 1.2) + f'<g fill="#1F1B3A55"><rect x="36" y="45" width="30" height="2.5"/><rect x="36" y="51" width="36" height="2.5"/><rect x="36" y="57" width="22" height="2.5"/></g>'
       f'<rect x="90" y="26" width="10" height="9" fill="#F4F2F0" stroke="{INK}" stroke-width="1"/><rect x="90" y="42" width="10" height="9" fill="#F4F2F0" stroke="{INK}" stroke-width="1"/>')
lt += g(mX(32, 504, 282), os9)
add(f'<g class="hot" data-go="laptop">{lt}</g>')
ch = f'<g transform="{at(214, 444, 0)}"><path d="M-48 6 L48 -6 M-30 -16 L30 16 M0 -22 L0 22" stroke="{INK}" stroke-width="9" stroke-linecap="round"/><path d="M-48 6 L48 -6 M-30 -16 L30 16 M0 -22 L0 22" stroke="#E6E1F0" stroke-width="5" stroke-linecap="round"/>' + "".join(f'<circle cx="{x}" cy="{y+6}" r="6" fill="{INK}"/>' for x, y in [(-48, 6), (48, -6), (-30, -16), (30, 16), (0, -22), (0, 22)]) + '</g>'
ch += box(207, 437, 10, 14, 14, 82, "#C9C1D6", "#B3AAC6", "#9E95B4", 2.5)
ch += box(166, 398, 92, 96, 92, 20, C["purple"], "#7A47B4", "#673A9C")
ch += box(258, 404, 112, 16, 80, 120, C["purple"], "#7A47B4", "#673A9C")
ch += g(mX(274, 484, 214), f'<path d="M6 16 q30 18 68 -4" stroke="{C["sky"]}" stroke-width="10" fill="none" stroke-linecap="round"/>')
add(ch)

# ---------- old-school TV on a cabinet next to the desk ----------
tv = box(6, 702, 0, 124, 112, 60, C["woodT"], C["woodF"], C["woodS"])
tv += g(mY(814, 6, 60), rect(10, 8, 104, 44, C["woodT"], 2.5) + f'<rect x="54" y="26" width="16" height="6" rx="3" fill="{INK}"/>')
tapes = "".join(rect(10 + i * 18, 10, 15, 42, ["#3B3550", "#2A2440", "#3B3550", "#2A2440", "#3B3550"][i], 2) + f'<rect x="{12 + i * 18}" y="16" width="11" height="14" fill="{[C["yellow"], C["pink"], C["sky"], C["mint"], C["coral"]][i]}"/>' for i in range(5))
tv += g(mX(130, 814, 60), rect(6, 6, 100, 48, "#2A2440", 2.5))
tv += box(14, 712, 60, 104, 94, 98, "#EAE3D3", "#D9D0BC", "#C7BCA4")
crt = (f'<rect x="4" y="6" width="64" height="80" rx="10" fill="#3B3550" stroke="{INK}" stroke-width="2.5"/>'
       f'<rect x="10" y="12" width="52" height="66" rx="14" fill="#2C4442" stroke="{INK}" stroke-width="2"/>'
       f'<g id="scrGlow"><rect x="10" y="12" width="52" height="66" rx="14" fill="#7FB2FF"/></g>'
       f'<path d="M16 22 q6 -6 16 -6" stroke="#FFFFFF77" stroke-width="4" fill="none" stroke-linecap="round"/>'
       f'<circle cx="80" cy="20" r="6" fill="#3B3550" stroke="{INK}" stroke-width="2"/><circle cx="80" cy="38" r="6" fill="#3B3550" stroke="{INK}" stroke-width="2"/>'
       f'<path d="M80 16 v4 M80 34 l3 3" stroke="#EAE3D3" stroke-width="2"/>'
       + "".join(f'<path d="M73 {y} H88" stroke="{INK}" stroke-width="2"/>' for y in range(54, 82, 5)))
tv += g(mX(118, 806, 158), crt)
ax_, ay_ = P(66, 759, 158)
tv += (f'<path d="M{f(ax_)} {f(ay_)} l-40 -62 M{f(ax_)} {f(ay_)} l30 -66" stroke="{INK}" stroke-width="3.5"/>'
       f'<circle cx="{f(ax_-40)}" cy="{f(ay_-62)}" r="4" fill="{C["red"]}" stroke="{INK}" stroke-width="2"/><circle cx="{f(ax_+30)}" cy="{f(ay_-66)}" r="4" fill="{C["red"]}" stroke="{INK}" stroke-width="2"/>'
       f'<ellipse cx="{f(ax_)}" cy="{f(ay_)}" rx="14" ry="7" fill="#3B3550" stroke="{INK}" stroke-width="2.5"/>')
add(f'<g class="hot" data-go="screen">{tv}</g>')


# ---------- rug + floor clutter ----------
rug = rect(0, 0, 360, 280, "#8FD3F5") + "".join(f'<path d="M{x} 6 V274" stroke="#B9E5FA" stroke-width="7"/>' for x in range(20, 360, 26)) + rect(0, 0, 360, 280, "none") \
      + "".join(f'<path d="M{x} 280 v12 M{x} 0 v-12" stroke="{INK}" stroke-width="2"/>' for x in range(8, 360, 14))
add(g(mZ(0.5, 200, 420), rug))
add(box(548, 250, 0, 92, 66, 14, C["yellow"], "#E9C143", "#CFA92F", 2.5) + box(554, 254, 14, 80, 58, 12, C["mint"], "#69C893", "#56B07E", 2.5) + box(552, 250, 26, 86, 62, 10, C["coral"], "#E97C59", "#D46A48", 2.5))
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
add(f'<g transform="translate(560 978) rotate(-10)">{shoe}</g><g transform="translate(650 994) rotate(6)">{shoe}</g>')
pad = (f'<path d="M-40 -14 q-18 0 -20 18 q-2 18 12 18 q10 0 16 -10 h64 q6 10 16 10 q14 0 12 -18 q-2 -18 -20 -18Z" fill="#C9C1D6" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
       f'<path d="M-40 -4 h-12 M-46 -10 v12" stroke="{INK}" stroke-width="4" stroke-linecap="round"/><circle cx="36" cy="-6" r="4" fill="{C["red"]}" stroke="{INK}" stroke-width="2"/><circle cx="46" cy="2" r="4" fill="{C["sky"]}" stroke="{INK}" stroke-width="2"/>'
       f'<path d="M0 -14 q10 -30 40 -26" stroke="{INK}" stroke-width="2.5" fill="none"/>')

# ---------- PS2 in the cabinet, controller and games on the floor ----------
ps2 = (f'<rect x="9" y="18" width="94" height="28" rx="2" fill="#1E1C24" stroke="{INK}" stroke-width="2"/>'
       f'<path d="M14 25 H66 M14 39 H66" stroke="#3A3746" stroke-width="2"/><path d="M68 18 V46" stroke="#3A3746" stroke-width="2"/>'
       f'<rect x="73" y="23" width="9" height="5" fill="#0E0D12"/><rect x="86" y="23" width="9" height="5" fill="#0E0D12"/><rect x="73" y="34" width="9" height="6" fill="#0E0D12"/><rect x="86" y="34" width="9" height="6" fill="#0E0D12"/>'
       f'<circle cx="18" cy="32" r="2.6" fill="#5AA8FF"/>')
cab_x, cab_y = P(130, 760, 28)
pad = (f'<path d="M-40 -14 q-18 0 -20 18 q-2 18 12 18 q10 0 16 -10 h64 q6 10 16 10 q14 0 12 -18 q-2 -18 -20 -18Z" fill="#33303C" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
       f'<path d="M-40 -4 h-12 M-46 -10 v12" stroke="#9C97AA" stroke-width="4" stroke-linecap="round"/>'
       f'<circle cx="-14" cy="6" r="6" fill="#55515F" stroke="{INK}" stroke-width="2"/><circle cx="14" cy="6" r="6" fill="#55515F" stroke="{INK}" stroke-width="2"/>'
       f'<circle cx="38" cy="-10" r="3.5" fill="#4CC38A"/><circle cx="46" cy="-3" r="3.5" fill="#F2543D"/><circle cx="38" cy="4" r="3.5" fill="#5B9BFF"/><circle cx="30" cy="-3" r="3.5" fill="#FF6FAE"/>')
padx, pady = 318, 868
GAME_ART = [
  ("#FF6FAE", f'<rect x="8" y="10" width="28" height="18" rx="3" fill="#FFE6A8" stroke="{INK}" stroke-width="1.5"/><circle cx="16" cy="19" r="3.5" fill="{INK}"/><circle cx="28" cy="19" r="3.5" fill="{INK}"/><rect x="6" y="38" width="32" height="5" fill="#FFE6A8"/><rect x="6" y="46" width="22" height="4" fill="{INK}"/>'),
  ("#151418", f'<path d="M4 44 L40 18" stroke="#FF9F1C" stroke-width="5"/><path d="M4 50 L40 24" stroke="#4CC38A" stroke-width="3"/><rect x="6" y="6" width="22" height="7" fill="#FF9F1C"/><path d="M10 34 l8 -4 h12 l6 4 v4 h-26Z" fill="#5B9BFF" stroke="#FFF4DE" stroke-width="1"/>'),
  ("#7FD36A", f'<path d="M22 12 c-12 6 -14 22 0 30 c14 -8 12 -24 0 -30Z" fill="#FFF4DE" stroke="{INK}" stroke-width="1.5"/><path d="M22 14 V40" stroke="#4E9A3F" stroke-width="2"/><rect x="6" y="46" width="32" height="5" fill="#FFF4DE"/>'),
]
games = f'<path d="M{f(cab_x)} {f(cab_y)} C{f(cab_x+60)} {f(cab_y+20)} {padx-90} {pady+40} {padx-40} {pady+4}" stroke="{INK}" stroke-width="3" fill="none"/>'
games += f'<g transform="translate({padx} {pady}) rotate(-14)">{pad}</g>'
for i, ((gx_, gy_, rot), (col, art)) in enumerate(zip([(226, 548, -10), (290, 566, 14), (244, 612, -24)], GAME_ART)):
    case = f'<g transform="rotate({rot} 22 30)">{rect(0, 0, 44, 60, col, 2.5)}<rect x="0" y="0" width="5" height="60" fill="#00000033"/>{art}</g>'
    games += f'<g class="hot game" data-go="games" data-game="{i}">' + g(mZ(0.8, gx_, gy_), case) + '</g>'
add(f'<g data-zoom="games"><g class="hot" data-go="games">' + g(mX(130.5, 814, 60), ps2) + '</g>' + games + '</g>')

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
ax, ay = P(800, 250, 112)
add(f"""<g id="catA" class="hot cat" data-cat="catA"><g transform="translate({f(ax)} {f(ay)}) scale(.9)"><g class="breathe">
<ellipse cx="0" cy="0" rx="74" ry="36" fill="#F09A3E" stroke="{INK}" stroke-width="3.5"/>
<g stroke="#B85C1A" stroke-width="5" fill="none" stroke-linecap="round"><path d="M-12 -34 q7 14 0 26"/><path d="M8 -35 q7 14 0 26"/><path d="M28 -31 q7 12 0 22"/><path d="M46 -24 q6 10 0 18"/></g>
<g class="tail"><path d="M66 8 C72 32 30 42 -10 36 C-38 33 -56 28 -64 20" stroke="{INK}" stroke-width="23" fill="none" stroke-linecap="round"/><path d="M66 8 C72 32 30 42 -10 36 C-38 33 -56 28 -64 20" stroke="#F09A3E" stroke-width="16" fill="none" stroke-linecap="round"/>
<g stroke="#B85C1A" stroke-width="4"><path d="M40 30 v10"/><path d="M14 33 v10"/><path d="M-14 31 v10"/></g></g>
<ellipse cx="-28" cy="30" rx="13" ry="7" fill="#FFF4DE" stroke="{INK}" stroke-width="2.5"/>
<g class="head">
<path d="M-84 -10 L-80 -44 L-58 -24 Z" fill="#F7A54E" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/><path d="M-80 -16 L-78 -34 L-66 -24 Z" fill="#F6B7C4"/>
<path d="M-52 -26 L-42 -36 L-38 -33 L-34 -36 L-30 -14 Z" fill="#F7A54E" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/><path d="M-47 -24 L-41 -31 L-37 -29 L-34 -31 L-33 -18 Z" fill="#F6B7C4"/>
<circle cx="-58" cy="2" r="29" fill="#F7A54E" stroke="{INK}" stroke-width="3.5"/>
<g stroke="#B85C1A" stroke-width="3" stroke-linecap="round"><path d="M-64 -24 v8"/><path d="M-57 -26 v9"/><path d="M-50 -24 v8"/></g>
<ellipse cx="-57" cy="14" rx="12" ry="8" fill="#FFF4DE"/>
<g class="sleep" stroke="{INK}" stroke-width="2.8" fill="none" stroke-linecap="round"><path d="M-74 0 q5 5 10 0"/><path d="M-52 0 q5 5 10 0"/></g>
<g class="mad"><ellipse cx="-69" cy="0" rx="6.5" ry="5.5" fill="#D6EA4A" stroke="{INK}" stroke-width="2.5"/><ellipse cx="-47" cy="0" rx="6.5" ry="5.5" fill="#D6EA4A" stroke="{INK}" stroke-width="2.5"/><rect x="-70" y="-4" width="2.4" height="8" rx="1" fill="{INK}"/><rect x="-48" y="-4" width="2.4" height="8" rx="1" fill="{INK}"/>
<path d="M-78 -11 L-62 -6 M-38 -11 L-52 -6" stroke="{INK}" stroke-width="3.2" stroke-linecap="round"/>
<path d="M-67 13 q10 14 20 0 Z" fill="#7A1F3A" stroke="{INK}" stroke-width="2"/><path d="M-64 13 l2 6 l2 -6Z M-53 13 l2 6 l2 -6Z" fill="#fff" stroke="{INK}" stroke-width="1"/></g>
<path d="M-60 9 h6 l-3 4 Z" fill="#E8577E" stroke="{INK}" stroke-width="1.2"/>
<g stroke="{INK}" stroke-width="1.4"><path d="M-72 14 l-18 -2 M-72 17 l-18 3 M-42 14 l18 -2 M-42 17 l18 3"/></g>
</g>
</g></g></g>""")
add(f'<text class="zz" x="{f(ax-74)}" y="{f(ay-52)}" font-size="24">z</text><text class="zz" x="{f(ax-58)}" y="{f(ay-62)}" font-size="17">z</text>')
cx_, cy_ = P(280, 560, 0)
O, B, W = "#F0923A", "#2B2733", "#FFFBF2"
add(f"""<g id="supraPos" transform="translate({f(cx_)} {f(cy_)})"><g id="catB" class="hot cat" data-cat="catB"><g class="flip">
<ellipse cx="0" cy="2" rx="52" ry="8" fill="#1F1B3A" opacity=".18"/>
<g class="walker"><g class="breathe">
<g class="tail"><path d="M-40 -40 C-62 -46 -70 -70 -58 -90" stroke="{INK}" stroke-width="14" fill="none" stroke-linecap="round"/><path d="M-40 -40 C-62 -46 -70 -70 -58 -90" stroke="{O}" stroke-width="8" fill="none" stroke-linecap="round"/><path d="M-62 -76 C-64 -84 -61 -88 -58 -90" stroke="{B}" stroke-width="8" fill="none" stroke-linecap="round"/></g>
<g class="leg b"><rect x="-34" y="-34" width="11" height="34" rx="5" fill="{W}" stroke="{INK}" stroke-width="3"/></g>
<g class="leg"><rect x="20" y="-34" width="11" height="34" rx="5" fill="{W}" stroke="{INK}" stroke-width="3"/></g>
<ellipse cx="0" cy="-38" rx="44" ry="19" fill="{W}"/>
<clipPath id="calClip"><ellipse cx="0" cy="-38" rx="44" ry="19"/></clipPath>
<g clip-path="url(#calClip)"><path d="M-46 -60 C-30 -50 -26 -38 -8 -42 C4 -46 10 -58 0 -62Z" fill="{O}"/><path d="M8 -62 C10 -48 24 -44 30 -50 C36 -56 30 -62 20 -64Z" fill="{B}"/><path d="M-46 -40 C-38 -30 -30 -26 -24 -22 L-46 -18Z" fill="{B}"/><path d="M14 -30 C20 -26 30 -26 36 -22 L20 -16Z" fill="{O}"/></g>
<ellipse cx="0" cy="-38" rx="44" ry="19" fill="none" stroke="{INK}" stroke-width="3.5"/>
<g class="leg"><rect x="-26" y="-32" width="11" height="32" rx="5" fill="{W}" stroke="{INK}" stroke-width="3"/></g>
<g class="leg b"><rect x="28" y="-32" width="11" height="32" rx="5" fill="{W}" stroke="{INK}" stroke-width="3"/></g>
<path d="M36 -66 L38 -90 L52 -72Z" fill="{B}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/><path d="M39 -71 L40 -84 L48 -73Z" fill="#F6B7C4"/>
<path d="M58 -72 L70 -90 L72 -64Z" fill="{O}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/><path d="M61 -70 L69 -83 L70 -67Z" fill="#F6B7C4"/>
<circle cx="54" cy="-58" r="19" fill="{W}"/>
<clipPath id="calHead"><circle cx="54" cy="-58" r="19"/></clipPath>
<g clip-path="url(#calHead)"><path d="M34 -80 L52 -78 L48 -62 C42 -60 36 -64 34 -70Z" fill="{B}"/><path d="M58 -80 C60 -66 66 -60 76 -62 L76 -80Z" fill="{O}"/></g>
<circle cx="54" cy="-58" r="19" fill="none" stroke="{INK}" stroke-width="3.5"/>
<circle cx="50" cy="-61" r="3" fill="{INK}"/><circle cx="64" cy="-61" r="3" fill="{INK}"/><circle cx="51" cy="-62" r="1" fill="#fff"/><circle cx="65" cy="-62" r="1" fill="#fff"/>
<path d="M54 -54 h6 l-3 4Z" fill="#E8577E" stroke="{INK}" stroke-width="1.2"/>
<path d="M57 -50 q-3 4 -7 2 M57 -50 q3 4 7 2" stroke="{INK}" stroke-width="1.6" fill="none" stroke-linecap="round"/>
<g stroke="{INK}" stroke-width="1.3"><path d="M46 -52 l-16 -2 M46 -50 l-16 3 M68 -52 l16 -2 M68 -50 l16 3"/></g>
</g></g></g></g></g>""")

# ---------- light ----------
gx, gy = lamp_x, lamp_y - 90
lvx, lvy = P(512, 50, 175)
lpx, lpy = P(30, 444, 225)
add('<rect id="nightTint" x="-50" y="-50" width="1700" height="1100" fill="#1B1442" style="mix-blend-mode:multiply;pointer-events:none" opacity=".16"/>')
add(f'<g style="pointer-events:none"><circle id="lampGlow" class="glow" cx="{f(gx)}" cy="{f(gy)}" r="320" fill="url(#warm)"/>'
    f'<circle id="lavaGlow" class="glow" cx="{f(lvx)}" cy="{f(lvy)}" r="80" fill="url(#lavaGlowG)" opacity=".8"/><circle class="glow" cx="{f(lpx)}" cy="{f(lpy)}" r="110" fill="url(#blueG)" opacity=".7"/>'
    + g(mX(0, 250, 528), '<text class="neon" x="10" y="40" opacity=".4" style="mix-blend-mode:screen">dee\'s room</text>') + '</g>')
add('<g id="fx" style="pointer-events:none"></g>')

DEFS = f'''<defs>
<pattern id="cane" width="14" height="14" patternUnits="userSpaceOnUse"><rect width="14" height="14" fill="#F7D9A8"/><circle cx="7" cy="7" r="4" fill="none" stroke="#C99A5E" stroke-width="1.6"/><path d="M0 0 L14 14 M14 0 L0 14" stroke="#DDB27A" stroke-width="1"/></pattern>
<pattern id="corkp" width="8" height="8" patternUnits="userSpaceOnUse"><rect width="8" height="8" fill="#D9A86C"/><circle cx="2" cy="3" r=".9" fill="#A97A45"/><circle cx="6" cy="6" r=".7" fill="#EAC690"/></pattern>
<linearGradient id="skyN" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1C1C4E"/><stop offset=".6" stop-color="#4A3278"/><stop offset="1" stop-color="#E0726A"/></linearGradient>
<linearGradient id="skyD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5DB8F5"/><stop offset="1" stop-color="#BFE8FB"/></linearGradient>
<linearGradient id="lavaG" x1="0" y1="0" x2="0" y2="1"><stop id="lava0" offset="0" stop-color="#FFB36E"/><stop id="lava1" offset="1" stop-color="#FF5C8A"/></linearGradient>
<linearGradient id="beamG" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#FFF6D8" stop-opacity=".6"/><stop offset="1" stop-color="#FFF6D8" stop-opacity=".06"/></linearGradient>
<radialGradient id="warm"><stop offset="0" stop-color="#FFC870" stop-opacity=".75"/><stop offset=".45" stop-color="#FF9F4A" stop-opacity=".25"/><stop offset="1" stop-color="#FF9F4A" stop-opacity="0"/></radialGradient>
<radialGradient id="lavaGlowG"><stop id="lavaGlowStop" offset="0" stop-color="#FF7A8A" stop-opacity=".75"/><stop offset="1" stop-color="#FF7A8A" stop-opacity="0"/></radialGradient>
<radialGradient id="pinkG"><stop offset="0" stop-color="#FF7A8A" stop-opacity=".7"/><stop offset="1" stop-color="#FF7A8A" stop-opacity="0"/></radialGradient>
<radialGradient id="blueG"><stop offset="0" stop-color="#8FB6FF" stop-opacity=".6"/><stop offset="1" stop-color="#8FB6FF" stop-opacity="0"/></radialGradient>
<filter id="neonGlow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>'''

svg = ('<svg id="room" viewBox="0 0 1600 1000" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="roomTitle">'
       '<title id="roomTitle">Dee\'s bedroom, seen from the corner: a lilac bookshelf, a record player on a mustard cabinet, toy cars on a shelf over the bed, a ginger cat asleep on a patchwork quilt, a calico cat on the rug, a desk with a retro laptop under the window and an old TV beside it</title>'
       + DEFS + "".join(out) + "</svg>")
(pathlib.Path(__file__).parent / "room.svg").write_text(svg)
print("scene", len(svg))
