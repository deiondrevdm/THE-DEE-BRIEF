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
win.append('</g><g><circle cx="280" cy="60" r="22" fill="#FFF3D0" stroke="#1F1B3A" stroke-width="2.5"/><circle cx="292" cy="54" r="19" fill="#2A2766"/></g>')
win.append('<rect id="skyDay" x="0" y="0" width="360" height="250" fill="url(#skyD)"/>')
win.append('<g id="sun"><circle cx="90" cy="70" r="30" fill="#FFD36E" stroke="#1F1B3A" stroke-width="2.5"/><path d="M200 90 q10 -22 32 -12 q14 -16 30 0 q20 2 14 20 h-74 q-14 -4 -2 -8Z" fill="#fff" stroke="#1F1B3A" stroke-width="2.5"/></g>')
win.append('<path d="M0 250 V170 q20 -30 46 -10 q10 -36 44 -22 q26 -24 46 8 q22 -6 26 18 q10 20 -6 36 V250Z" fill="#4FB86A" stroke="#1F1B3A" stroke-width="3"/><path d="M40 210 q14 -10 26 0 M100 196 q12 -8 22 2" stroke="#2F8C4A" stroke-width="3" fill="none"/>')
win.append('<rect id="skyGold" x="0" y="0" width="360" height="250" fill="url(#skyG)" opacity="0"/>')
import random as _r
_rr=_r.Random(5)
win.append('<clipPath id="wClip"><rect x="0" y="0" width="360" height="250"/></clipPath><g clip-path="url(#wClip)"><g id="wRain" style="display:none">'
  + "".join(f'<path class="rainl" d="M{_rr.uniform(0,360):.0f} -30 l-6 26" style="animation-delay:{-_rr.uniform(0,.7):.2f}s;animation-duration:{_rr.uniform(.45,.75):.2f}s"/>' for _ in range(46))
  + '</g><g id="wSnow" style="display:none">'
  + "".join(f'<circle class="snowf" cx="{_rr.uniform(0,360):.0f}" cy="-10" r="{_rr.uniform(1.6,3.4):.1f}" style="animation-delay:{-_rr.uniform(0,7):.2f}s;animation-duration:{_rr.uniform(5,9):.1f}s"/>' for _ in range(40))
  + '</g></g>')
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

# ashtray on the windowsill, joint resting in it, smoke drifting up
ash_x, ash_y = P(14, 616, 238)
add(f'<g class="hot" data-toggle="ash" transform="translate({f(ash_x)} {f(ash_y)})">'
    f'<ellipse cx="0" cy="0" rx="18" ry="7" fill="#2E9C96" stroke="{INK}" stroke-width="2.5"/>'
    f'<ellipse cx="0" cy="-2" rx="12" ry="4" fill="#1E6E6A"/><circle cx="-4" cy="-2" r="1.5" fill="#9C97AA"/><circle cx="3" cy="-1" r="1.2" fill="#9C97AA"/>'
    f'<g id="joint" class="jointg"><path id="jointBody" d="M-6 -3 L20 -11 L21 -8 L-5 0Z" fill="#FFFBF2" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>'
    f'<g class="jface"><circle cx="6" cy="-6.3" r="1.1" fill="{INK}"/><circle cx="10.5" cy="-7.6" r="1.1" fill="{INK}"/><path d="M6.5 -4 q2.6 1.4 5 -1.4" stroke="{INK}" stroke-width=".9" fill="none" stroke-linecap="round"/></g>'
    f'<path d="M-6 -3 L-1 -4.6 L0 -1.6 L-5 0Z" fill="#D9C7A7"/>'
    f'<circle class="ember" cx="20.5" cy="-9.5" r="2.2" fill="#FF7A2A"/>'
    f'<g class="smoke" transform="translate(21 -12)"><path d="M0 0 q-6 -10 2 -20 q7 -10 -1 -22"/><path d="M0 0 q6 -12 -2 -22 q-6 -9 2 -20"/><path d="M0 0 q-4 -9 3 -18 q5 -8 -2 -18"/></g>'
    '</g>'
    '</g>')

import base64
POSTER_IMG = base64.b64encode((pathlib.Path(__file__).parent / "poster.jpg").read_bytes()).decode()
poster = (rect(0, 0, 150, 200, "#FFFDF6")
          + f'<image href="data:image/jpeg;base64,{POSTER_IMG}" x="5" y="5" width="140" height="190" preserveAspectRatio="xMidYMid slice"/>'
          + rect(0, 0, 150, 200, "none")
          + '<rect x="-8" y="-6" width="30" height="12" fill="#ffffffaa" transform="rotate(-20)"/><rect x="128" y="-6" width="30" height="12" fill="#ffffffaa" transform="rotate(20 143 0)"/>')
add('<g id="posterG" class="hot" data-toggle="poster">' + g(mX(0, 236, 430), poster) + '</g>')
mix = (rect(0, 0, 70, 90, C["yellow"]) + f'<rect x="10" y="22" width="50" height="32" rx="4" fill="{C["cream"]}" stroke="{INK}" stroke-width="2.5"/><circle cx="25" cy="38" r="7" fill="{INK}"/><circle cx="45" cy="38" r="7" fill="{INK}"/>'
       f'<text x="35" y="78" text-anchor="middle" font-family="Courier Prime, monospace" font-weight="700" font-size="12" fill="{INK}">MIX VOL.2</text>')
add(g(mX(0, 66, 350), mix))
pol = ""
for k, (yy, zz, rot, col, img) in enumerate([(62, 236, -6, C["sky"], "p2"), (118, 220, 5, C["mint"], "p1")]):
    pol += g(mX(0, yy, zz), f'<g transform="rotate({rot} 24 28)">' + rect(0, 0, 48, 56, "#FFFDF6", 2.5) + rect(5, 5, 38, 36, col, 2)
             + f'<clipPath id="polc{k}"><rect x="6" y="6" width="36" height="34"/></clipPath><image href="/THE-DEE-BRIEF/room/photos/{img}.webp" x="6" y="6" width="36" height="34" preserveAspectRatio="xMidYMid slice" clip-path="url(#polc{k})"/>'
             + f'<rect x="5" y="5" width="38" height="36" fill="none" stroke="{INK}" stroke-width="2"/></g>')
add('<g class="hot" data-go="photos">' + pol + '</g>')
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
        bul.append(f'<ellipse class="bulb" cx="{f(x)}" cy="{f(y+10)}" rx="5" ry="7.5" fill="{c}" stroke="{INK}" stroke-width="2"/>')
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

# ---------- Y2K mirror with notes stuck to it ----------
mir = (f'<rect x="0" y="0" width="200" height="140" rx="22" fill="#FF8FC2" stroke="{INK}" stroke-width="3"/>'
       f'<rect x="12" y="12" width="176" height="116" rx="14" fill="url(#mirG)" stroke="{INK}" stroke-width="2.5"/>'
       '<path d="M24 26 L58 19 M24 40 L82 27" stroke="#ffffffcc" stroke-width="5" stroke-linecap="round"/>'
       # yellow sticky: horses (top left)
       f'<g transform="rotate(-6 52 44)"><rect x="22" y="18" width="62" height="52" fill="#FFE6A8" stroke="{INK}" stroke-width="2"/>'
       '<rect x="42" y="13" width="22" height="9" fill="#ffffffaa"/>'
       '<text font-family="Patrick Hand, cursive" font-size="10" fill="#1F1B3A" text-anchor="middle"><tspan x="53" y="33">horses don\'t</tspan><tspan x="53" y="45">stop, they</tspan><tspan x="53" y="57">keep going</tspan></text>'
       f'<path d="M40 64 q4 -6 8 0 q4 6 8 0" stroke="{INK}" stroke-width="1.4" fill="none"/></g>'
       # to-do list, tucked into the bottom-left of the frame
       f'<g transform="rotate(3 40 112)"><rect x="-8" y="74" width="98" height="76" fill="#FFFDF6" stroke="{INK}" stroke-width="2"/>'
       '<g stroke="#9FC2F0" stroke-width=".8">' + "".join(f'<path d="M-6 {y} H88"/>' for y in (96, 109, 122, 135)) + '</g>'
       '<path d="M4 75 V149" stroke="#F49AB5" stroke-width=".9"/>'
       '<rect x="30" y="69" width="24" height="9" fill="#ffffffaa"/>'
       '<text x="8" y="89" font-family="Permanent Marker, Patrick Hand, cursive" font-size="10" fill="#1F1B3A">to do:</text>'
       f'<g fill="none" stroke="{INK}" stroke-width="1.1"><rect x="7" y="99.5" width="5" height="5"/><rect x="7" y="112.5" width="5" height="5"/><rect x="7" y="125.5" width="5" height="5"/></g>'
       f'<g class="todoDone"><path d="M7.5 114.5 l2 2.5 4 -6" stroke="#E8577E" stroke-width="1.6" fill="none" stroke-linecap="round"/>'
       '<text font-family="Patrick Hand, cursive" font-size="8.2" fill="#1F1B3A"><tspan x="15" y="105">tell Nicole I love her</tspan><tspan x="15" y="118">water plant</tspan><tspan x="15" y="131">punch a bigot in</tspan><tspan x="15" y="143">the guts</tspan></text>'
       f'<path d="M15 115 H56" stroke="{INK}" stroke-width="1"/></g>'
       f'<path d="M78 136 c-3 -4 -8 -1 -4 3 l4 4 4 -4 c4 -4 -1 -7 -4 -3z" fill="#FF6FAE" stroke="{INK}" stroke-width=".9"/></g>'
       # pink note: kyk noord, fok voort
       f'<g transform="rotate(7 132 46)"><rect x="102" y="20" width="60" height="50" fill="#FFC1D3" stroke="{INK}" stroke-width="2"/>'
       '<rect x="122" y="15" width="20" height="8" fill="#ffffffaa"/>'
       '<text font-family="Patrick Hand, cursive" font-size="10.5" fill="#1F1B3A" text-anchor="middle"><tspan x="132" y="39">kyk noord,</tspan><tspan x="132" y="53">fok voort</tspan></text>'
       f'<path d="M150 64 l3 -5 3 5 -5 -3 h6Z" fill="#F8D65A" stroke="{INK}" stroke-width="1"/></g>'
       # movie ticket stub: White Chicks
       f'<g transform="rotate(-4 140 100)"><path d="M104 84 H176 V92 a4 4 0 0 0 0 8 V116 H104 V100 a4 4 0 0 0 0 -8Z" fill="#BFD4FF" stroke="{INK}" stroke-width="2"/>'
       '<path d="M158 85 V115" stroke="#1F1B3A" stroke-width="1.2" stroke-dasharray="2 2"/>'
       '<text font-family="DM Sans, Arial, sans-serif" fill="#1F1B3A"><tspan x="108" y="93" font-size="5" font-weight="700" letter-spacing=".6">ADMIT ONE</tspan><tspan x="108" y="104" font-size="8.5" font-weight="800">WHITE</tspan><tspan x="108" y="113" font-size="8.5" font-weight="800">CHICKS</tspan></text>'
       '<text x="167" y="100" text-anchor="middle" font-family="DM Sans, Arial, sans-serif" font-size="5" font-weight="700" fill="#1F1B3A" transform="rotate(-90 167 100)">2004</text></g>'
       # a couple of stickers
       f'<g stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"><path d="M96 124 l3 -8 3 8 -8 -5 h10Z" fill="#F8D65A"/><path d="M92 24 l2.5 -6 2.5 6 -6 -4 h7Z" fill="#8FD3F5"/></g>')
board_svg = g(mY(1, 330, 486), mir)

# glow-in-the-dark stars above the nightstand
st = ""
for (x, y, s) in [(10, 20, 1), (50, 60, .7), (20, 110, .8), (70, 140, 1.1), (30, 190, .6), (80, 30, .6)]:
    st += f'<path transform="translate({x} {y}) scale({s})" d="M0 -12 L3.5 -4 12 -3.5 5.5 2.5 7.5 11 0 6.5 -7.5 11 -5.5 2.5 -12 -3.5 -3.5 -4Z" fill="#FFF07A" stroke="{INK}" stroke-width="2"/>'
st += f'<path transform="translate(60 92)" d="M0 -14 a14 14 0 1 0 10 24 a11 11 0 1 1 -10 -24Z" fill="#FFF07A" stroke="{INK}" stroke-width="2"/>'
add(g(mY(1, 556, 520), st))

# ---------- backstage pass (about me) ----------
pass_svg = (f'<circle cx="22" cy="0" r="3.2" fill="#FF6FAE" stroke="{INK}" stroke-width="1.5"/>'
            f'<path d="M22 1 L6 20 M22 1 L38 20" stroke="{INK}" stroke-width="5" stroke-linecap="round"/><path d="M22 1 L6 20 M22 1 L38 20" stroke="#B57BFF" stroke-width="2.8" stroke-linecap="round"/>'
            f'<rect x="0" y="18" width="44" height="60" rx="4" fill="#FFFDF6" stroke="{INK}" stroke-width="2.5"/>'
            f'<rect x="1.3" y="19.3" width="41.4" height="9" rx="3" fill="#FF6FAE"/><path d="M1.3 28.3 H42.7" stroke="{INK}" stroke-width="1.5"/>'
            '<text x="22" y="26" text-anchor="middle" font-family="Bricolage Grotesque, Arial Black, sans-serif" font-weight="800" font-size="5.6" fill="#1F1B3A" letter-spacing=".4">ALL ACCESS</text>'
            f'<rect x="7" y="31" width="30" height="27" rx="2" fill="#BFD4FF" stroke="{INK}" stroke-width="1.5"/>'
            '<svg id="idPhoto" x="7.5" y="31.5" width="29" height="26" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid slice"></svg>'
            '<text x="22" y="66.5" text-anchor="middle" font-family="Bricolage Grotesque, Arial Black, sans-serif" font-weight="800" font-size="7.5" fill="#1F1B3A">DEE</text>'
            f'<g stroke="{INK}" stroke-width=".9">' + "".join(f'<path d="M{x} 69.5 v5"/>' for x in (12, 13.5, 16, 17, 19.5, 21, 22, 24.5, 26, 28.5, 29.5, 32)) + '</g>'
            '<path d="M3 22 L12 76" stroke="#ffffff" stroke-opacity=".5" stroke-width="3"/>')
add('<g id="pass" class="hot" data-go="me">' + g(mY(1, 566, 300), pass_svg) + '</g>')

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
         '<g class="leaves">' f'<path d="M-6 -42 c-30 -10 -40 -40 -30 -60 c20 6 30 30 30 60 M4 -42 c0 -30 10 -54 28 -62 c6 26 -6 46 -28 62 M0 -42 c-4 -30 -2 -56 6 -70 c10 20 6 46 -6 70" fill="{C["mint"]}" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>' '</g>'
         f'<path d="M-20 -30 c-10 30 -16 60 -12 100" stroke="{INK}" stroke-width="5" fill="none"/><path d="M-20 -30 c-10 30 -16 60 -12 100" stroke="#4FB86A" stroke-width="2.5" fill="none"/>'
         + "".join(f'<ellipse cx="{x}" cy="{y}" rx="8" ry="5" transform="rotate({r} {x} {y})" fill="{C["mint"]}" stroke="{INK}" stroke-width="2"/>' for x, y, r in [(-28, 0, 50), (-32, 30, 70), (-30, 60, 80)]))
wcan = (f'<g class="wcan"><g transform="translate(58 -92)"><g class="wtilt">'
        f'<path d="M-4 -6 L-34 -22" stroke="{INK}" stroke-width="7" stroke-linecap="round"/><path d="M-4 -6 L-34 -22" stroke="#5B9BFF" stroke-width="3.5" stroke-linecap="round"/>'
        f'<ellipse cx="-36" cy="-23" rx="5" ry="3.5" fill="#5B9BFF" stroke="{INK}" stroke-width="2" transform="rotate(-30 -36 -23)"/>'
        f'<rect x="-6" y="-20" width="34" height="28" rx="6" fill="#5B9BFF" stroke="{INK}" stroke-width="3"/>'
        f'<path d="M4 -20 q10 -16 20 0" stroke="{INK}" stroke-width="3" fill="none"/><path d="M0 -10 h24" stroke="#9CC4FF" stroke-width="2.5" stroke-linecap="round"/></g></g>'
        + "".join(f'<ellipse class="drop" cx="{x+6}" cy="-110" rx="2.2" ry="3.4" fill="#8FD3F5" stroke="{INK}" stroke-width="1" style="animation-delay:{d}s"/>' for x, d in [(-8, 0), (-2, .15), (-12, .3), (0, .45), (-6, .6)])
        + "".join(f'<path class="spark" d="M{x} {y} l2 -6 2 6 6 2 -6 2 -2 6 -2 -6 -6 -2Z" fill="#FFE27A" stroke="{INK}" stroke-width="1" style="animation-delay:{d}s"/>' for x, y, d in [(-34, -96, 0), (26, -110, .2), (8, -76, .35)])
        + '</g>')
bs.append('<g id="plant" class="hot" data-toggle="plant">' + g(at(80, 36, 470), plant + wcan) + '</g>')
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

add(f'<g id="mirror" class="hot" data-toggle="mirror">{board_svg}</g>')
add(f'<g class="hot" data-go="records">{records_svg}</g>')
add(f'<g class="hot" data-toggle="lava" transform="{at(512, 50, 130)}">{lava}</g>')
add(cars_svg + car_hots)

# skateboard hung on the wall above the cars: underside facing out, hot-rod flames
L, H = 280, 66
deck = f"M34 0 H{L-34} C{L-8} 0 {L+4} 16 {L+4} {H/2} C{L+4} {H-16} {L-8} {H} {L-34} {H} H34 C8 {H} -4 {H-16} -4 {H/2} C-4 16 8 0 34 0Z"
# flames sweep from the left (nose) toward the right in long tongues
tips = [(150, 7), (215, 19), (175, 31), (240, 44), (165, 57)]
d = "M-10 -4 "
prev_y = -4
for k, (tx, ty) in enumerate(tips):
    vy = ty + 6
    d += f"Q{tx*0.55:.0f} {ty-6} {tx} {ty} Q{tx*0.5:.0f} {ty+4} {tx*0.38:.0f} {vy+2} "
d += f"L-10 {H+6}Z"
inner = d.replace("Q", "Q").replace("M-10 -4", "M-10 4")
sk = (f'<path d="M58 -14 v14 M{L-58} -14 v14" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
      f'<circle cx="58" cy="-16" r="4.5" fill="#9C97AA" stroke="{INK}" stroke-width="2"/><circle cx="{L-58}" cy="-16" r="4.5" fill="#9C97AA" stroke="{INK}" stroke-width="2"/>'
      f'<clipPath id="deckClip"><path d="{deck}"/></clipPath><path d="{deck}" fill="#1F1B3A"/>'
      f'<g clip-path="url(#deckClip)"><path d="{d}" fill="#F2543D"/>'
      f'<path d="{d}" transform="translate(-14 0) scale(.82 1)" fill="#FF9F1C"/><path d="{d}" transform="translate(-20 0) scale(.6 1)" fill="#F8D65A"/></g>'
      f'<path d="{deck}" fill="none" stroke="{INK}" stroke-width="3"/>')
# trucks: baseplate along the board, hanger across it, wheels poking out top and bottom
for tx in (70, L - 70):
    sk += (f'<rect x="{tx-16}" y="{H/2-11}" width="32" height="22" rx="4" fill="#C9C1D6" stroke="{INK}" stroke-width="2.5"/>'
           f'<rect x="{tx-6}" y="-4" width="12" height="{H+8}" rx="5" fill="#E6E1F0" stroke="{INK}" stroke-width="2.5"/>'
           f'<circle cx="{tx}" cy="{H/2}" r="4" fill="#9C97AA" stroke="{INK}" stroke-width="1.6"/>')
    for wy in (-6, H + 6):
        sk += (f'<rect x="{tx-13}" y="{wy-8}" width="26" height="16" rx="7" fill="#FFFBF2" stroke="{INK}" stroke-width="2.5"/>'
               f'<rect x="{tx-6}" y="{wy-4}" width="12" height="8" rx="3" fill="#FF6FAE" stroke="{INK}" stroke-width="1.4"/>')
add(g(mY(2, 676, 462), sk))

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
mug = (f'<path d="M-12 0 v-28 h24 v28 q0 4 -4 4 h-16 q-4 0 -4 -4Z" fill="{C["teal"]}" stroke="{INK}" stroke-width="3"/><path d="M12 -22 q12 0 10 10 q-2 8 -10 6" stroke="{INK}" stroke-width="3" fill="none"/>'
       f'<g class="steam" stroke="#FFFDF6" stroke-width="3" fill="none" stroke-linecap="round"><path d="M-4 -34 q-6 -10 2 -18 q6 -8 0 -16"/><path d="M6 -34 q6 -10 -2 -18 q-6 -8 0 -16"/></g>')
dk += g(at(70, 320, 176), mug)
add(dk)

# open notebook on the desk (click to read it)
nb = (f'<rect x="-4" y="-3" width="104" height="106" rx="4" fill="#F2543D" stroke="{INK}" stroke-width="2.5"/>'
      f'<rect x="0" y="0" width="96" height="48" fill="#FFFBF2" stroke="{INK}" stroke-width="2"/>'
      f'<rect x="0" y="52" width="96" height="48" fill="#FFFBF2" stroke="{INK}" stroke-width="2"/>'
      + "".join(f'<path d="M6 {y} H90" stroke="#9DB4F0" stroke-width=".9"/>' for y in list(range(10, 48, 7)) + list(range(60, 100, 7)))
      + '<path d="M14 2 V46 M14 54 V98" stroke="#F2A0A0" stroke-width=".9"/>'
      + "".join(f'<circle cx="{x}" cy="50" r="2.4" fill="none" stroke="{INK}" stroke-width="1.6"/>' for x in range(8, 96, 8))
      + '<path d="M20 15 q8 -3 16 0 t16 0 M20 22 q10 -2 24 0 M20 29 q6 -3 12 0" stroke="#5B5470" stroke-width="1.1" fill="none" stroke-linecap="round"/>'
      + '<g class="nbtext"><text font-family="Permanent Marker, Marker Felt, Comic Sans MS, cursive" font-size="11.5" fill="#141118"><tspan x="6" y="68">nosy little fucker,</tspan><tspan x="6" y="82">aren\'t you?</tspan></text></g>')
add('<g id="notebook" class="hot" data-toggle="notebook">' + g(mZ(176.5, 12, 514), nb) + '</g>')

# three candles on the desk (click to light / blow out)
def candle(x, y, h, w, col, top):
    cx, cy = P(x, y, 176)
    fl = (f'<g class="cflame" transform="translate(0 {-h-6})"><ellipse cx="0" cy="-2" rx="11" ry="14" fill="#FFC870" opacity=".35" class="cglow"/>'
          f'<path d="M0 -14 C5 -7 6 -2 4 2 C3 5 -3 5 -4 2 C-6 -2 -5 -7 0 -14Z" fill="#FF9F1C" stroke="{INK}" stroke-width="1.6"/>'
          f'<path d="M0 -8 C2 -5 2.5 -2 1.5 1 C1 2.5 -1 2.5 -1.5 1 C-2.5 -2 -2 -5 0 -8Z" fill="#FFF3B0"/></g>')
    return (f'<g transform="translate({f(cx)} {f(cy)})">'
            f'<ellipse cx="0" cy="0" rx="{w}" ry="{w*.42}" fill="{col}" stroke="{INK}" stroke-width="2.5"/>'
            f'<rect x="{-w}" y="{-h}" width="{2*w}" height="{h}" fill="{col}"/>'
            f'<path d="M{-w} {-h} V0 M{w} {-h} V0" stroke="{INK}" stroke-width="2.5"/>'
            f'<ellipse cx="0" cy="{-h}" rx="{w}" ry="{w*.42}" fill="{top}" stroke="{INK}" stroke-width="2.5"/>'
            f'<path d="M{-w*.5} {-h+3} q2 {h*.3} 0 {h*.45}" stroke="{top}" stroke-width="3" fill="none" stroke-linecap="round"/>'
            f'<path d="M0 {-h} v-6" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>{fl}</g>')
add('<g id="candles" class="hot" data-toggle="candles">'
    + candle(118, 692, 46, 10, "#FF8FC2", "#FFC1D9")
    + candle(146, 672, 30, 12, "#B39BFF", "#D6C9FF")
    + candle(138, 650, 20, 9, "#FFF4DE", "#FFFFFF") + '</g>')
TAN, TANF, TANS = "#FF9A3A", "#FF8A2A", "#E8761C"
lt = box(30, 384, 176, 82, 124, 12, "#F7F2EA", TANF, TANS, 2.5)
lt += g(mZ(188, 40, 396), rect(0, 0, 30, 100, "#E9E3D8", 2) + "".join(f'<path d="M{x} 3 V97" stroke="#BDB5A6" stroke-width="1.2"/>' for x in (8, 15, 22)) + "".join(f'<path d="M3 {y} H27" stroke="#BDB5A6" stroke-width="1.2"/>' for y in range(12, 100, 11)))
lt += g(mY(508, 30, 188), f'<path d="M14 0 C14 24 66 24 66 0" fill="none" stroke="{INK}" stroke-width="10" stroke-linecap="round"/><path d="M14 0 C14 24 66 24 66 0" fill="none" stroke="{TAN}" stroke-width="5" stroke-linecap="round"/>')
lt += box(20, 384, 186, 12, 124, 100, TAN, TANF, TANS, 2.5)
os9 = (f'<rect x="6" y="6" width="112" height="88" rx="10" fill="#F7F2EA" stroke="{INK}" stroke-width="2"/>'
       f'<rect x="14" y="13" width="96" height="70" rx="3" fill="#6F7FC6" stroke="{INK}" stroke-width="2"/>'
       f'<rect x="15" y="14" width="94" height="68" fill="#E7B4E0"/><ellipse cx="46" cy="68" rx="16" ry="8" fill="#F09A3E" stroke="{INK}" stroke-width="1.2"/><circle cx="34" cy="66" r="6" fill="#F7A54E" stroke="{INK}" stroke-width="1.2"/><path d="M66 74 C64 60 70 54 76 54 C82 54 88 60 86 74Z" fill="#FFFBF2" stroke="{INK}" stroke-width="1.2"/><circle cx="77" cy="50" r="6" fill="#FFFBF2" stroke="{INK}" stroke-width="1.2"/><path d="M68 62 q4 -4 8 2" stroke="#F0923A" stroke-width="3" fill="none"/>'
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
ax_, ay_ = P(32, 728, 158)
tv += (f'<path d="M{f(ax_)} {f(ay_)} l-40 -62 M{f(ax_)} {f(ay_)} l30 -66" stroke="{INK}" stroke-width="3.5"/>'
       f'<circle cx="{f(ax_-40)}" cy="{f(ay_-62)}" r="4" fill="{C["red"]}" stroke="{INK}" stroke-width="2"/><circle cx="{f(ax_+30)}" cy="{f(ay_-66)}" r="4" fill="{C["red"]}" stroke="{INK}" stroke-width="2"/>'
       f'<ellipse cx="{f(ax_)}" cy="{f(ay_)}" rx="14" ry="7" fill="#3B3550" stroke="{INK}" stroke-width="2.5"/>')
import math as _m
_bx, _by = P(72, 764, 158)
def _bumps(front):
    pts = []
    for i in range(22):
        t = 2 * _m.pi * i / 22
        if (_m.sin(t) >= 0) == front:
            pts.append((_bx + 48 * _m.cos(t), _by - 4 + 20 * _m.sin(t), 9.5 if front else 8.5))
    return pts
def _fluff(pts, fill):
    return ("".join(f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="2.6"/>' for x, y, r in pts)
            + "".join(f'<circle cx="{f(x)}" cy="{f(y)}" r="{r-1.3}" fill="{fill}"/>' for x, y, r in pts))
cbed = (f'<g id="catBed"><ellipse cx="{f(_bx)}" cy="{f(_by+8)}" rx="54" ry="25" fill="#2F8A4C" stroke="{INK}" stroke-width="3"/>'
        + _fluff(_bumps(False), "#6FD08A")
        + f'<ellipse cx="{f(_bx)}" cy="{f(_by-3)}" rx="36" ry="13" fill="#3FA45E" stroke="{INK}" stroke-width="2.2"/>'
        + f'<path d="M{f(_bx-18)} {f(_by-4)} q4 -3 8 0 M{f(_bx+6)} {f(_by-6)} q4 -3 8 0" stroke="#7FDD99" stroke-width="2" fill="none" stroke-linecap="round"/>'
        + _fluff(_bumps(True), "#7FDB97")
        + "".join(f'<path d="M{f(_bx+dx)} {f(_by+dy)} q3 -3 6 0" stroke="#B5F0C4" stroke-width="1.8" fill="none" stroke-linecap="round"/>' for dx, dy in [(-34, 10), (-12, 17), (14, 17), (32, 9)])
        + '</g>')
tv += cbed
add(f'<g class="hot" data-go="screen">{tv}</g>')


# ---------- rug + floor clutter ----------
# rug: hot pink + cobalt blue chevrons with a zigzag border
PINK, COB = "#FF2E93", "#1F4FD8"
rug = rect(0, 0, 360, 280, COB)
for k, y in enumerate(range(20, 270, 36)):
    col = PINK if k % 2 == 0 else "#FFFBF2"
    d = "M18 " + str(y + 18) + " " + " ".join(f"L{x + 18} {y} L{x + 36} {y + 18}" for x in range(18, 324, 36))
    rug += f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{9 if col == PINK else 3}" stroke-linejoin="miter"/>'
zig = "M0 0 " + " ".join(f"l9 -9 l9 9" for _ in range(20))
rug += f'<rect x="0" y="0" width="360" height="280" fill="none" stroke="{PINK}" stroke-width="22"/>'
rug += f'<path d="{zig}" transform="translate(0 16)" fill="none" stroke="#FFFBF2" stroke-width="2.5"/><path d="{zig}" transform="translate(0 273)" fill="none" stroke="#FFFBF2" stroke-width="2.5"/>'
rug += rect(0, 0, 360, 280, "none") + "".join(f'<path d="M{x} 280 v12 M{x} 0 v-12" stroke="{INK}" stroke-width="2"/>' for x in range(8, 360, 14))
add(g(mZ(0.5, 200, 420), rug))
def sock(c):
    return (f'<path d="M0 0 h18 v26 q0 6 6 6 h14 q8 0 8 8 q0 8 -8 8 h-26 q-12 0 -12 -12Z" fill="#FFFDF6" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
            f'<path d="M0 6 h18 M0 12 h18" stroke="{c}" stroke-width="3"/><path d="M30 32 q8 0 8 8 q0 8 -8 8 h-4 v-16Z" fill="{c}" stroke="{INK}" stroke-width="2.5"/>')
add(f'<g transform="translate(470 905) rotate(60)">{sock(C["sky"])}</g>')
shoe = (f'<path d="M0 0 q-2 -18 14 -20 l10 -10 h18 q10 14 30 16 q10 2 10 12 v4Z" fill="{C["coral"]}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
        f'<path d="M-2 0 h86 v8 h-86Z" fill="#FFFDF6" stroke="{INK}" stroke-width="3"/><path d="M24 -28 l8 10 M34 -28 l6 10" stroke="{INK}" stroke-width="2.5"/><path d="M50 -10 l8 -4 l6 6" stroke="#FFFDF6" stroke-width="3" fill="none"/>')
add(f'<g transform="translate(600 650) rotate(-10)">{shoe}</g><g transform="translate(676 668) rotate(6)">{shoe}</g>')
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
games += f'<g class="hot" data-go="games"><g transform="translate({padx} {pady}) rotate(-14)">{pad}</g></g>'
for i, ((gx_, gy_, rot), (col, art)) in enumerate(zip([(226, 548, -10), (290, 566, 14), (244, 612, -24)], GAME_ART)):
    case = f'<g transform="rotate({rot} 22 30)">{rect(0, 0, 44, 60, col, 2.5)}<rect x="0" y="0" width="5" height="60" fill="#00000033"/>{art}</g>'
    games += g(mZ(0.8, gx_, gy_), case)
add(f'<g data-zoom="games">' + g(mX(130.5, 814, 60), ps2) + games + '</g>')

# ---------- bed ----------
bed = box(656, 0, 0, 308, 20, 240, C["woodT"], C["woodF"], C["woodS"])
bed += g(mY(20, 656, 240), rect(22, 18, 264, 120, "url(#cane)", 2.5))
bed += box(660, 20, 0, 300, 450, 70, C["woodT"], C["woodF"], C["woodS"])
bed += box(668, 22, 70, 286, 444, 40, C["cream"], "#EFE2C8", "#DCCCAE")
def pillow(x0, col, line):
    # big, plump pillows propped against the headboard
    t = mY(40, x0, 214)
    body = "M14 18 C30 2 104 0 128 12 C142 20 144 40 140 60 C138 82 142 98 128 104 C100 114 34 114 12 104 C0 96 4 80 4 60 C4 40 0 28 14 18Z"
    return (f'<g transform="{t}">'
            f'<path d="{body}" transform="translate(4 6)" fill="{line}" stroke="{INK}" stroke-width="3"/>'
            f'<path d="{body}" fill="{col}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
            f'<path d="M30 22 C60 14 96 14 120 22" stroke="#ffffff88" stroke-width="7" fill="none" stroke-linecap="round"/>'
            f'<path d="M20 40 C46 56 98 56 124 40 M22 78 C50 66 96 66 122 80" stroke="{line}" stroke-width="3" fill="none" stroke-linecap="round" opacity=".7"/>'
            f'<path d="M14 18 l-8 -6 M128 12 l8 -7 M12 104 l-8 6 M128 104 l9 6" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
            f'</g>')
bed += pillow(676, C["pink"], "#D2558C") + pillow(810, C["yellow"], "#CFA92F")
patch = ["#F2543D", C["teal"], C["yellow"], C["pink"], C["mint"], C["cream"], C["lilT"], "#FF9F1C", C["sky"]]
q = []
for i in range(7):
    for j in range(6): q.append(f'<rect x="{i*41}" y="{j*53.5}" width="41" height="53.5" fill="{"#1F1B3A" if (i+j)%2 else "#FFFBF2"}"/>')
q.append(f'<g stroke="#8E87A3" stroke-width="2" stroke-dasharray="5 4">' + "".join(f'<path d="M{i*41} 0 V321"/>' for i in range(1, 7)) + "".join(f'<path d="M0 {j*53.5} H287"/>' for j in range(1, 6)) + '</g>')
q.append(rect(0, 0, 287, 321, "none"))
bed += g(mZ(110.5, 668, 147), "".join(q))
fq = "".join(f'<rect x="{i*41}" y="0" width="41" height="66" fill="{"#1F1B3A" if (i+6)%2 else "#FFFBF2"}"/>' for i in range(7)) + f'<g stroke="#8E87A3" stroke-width="2" stroke-dasharray="5 4">' + "".join(f'<path d="M{i*41} 0 V66"/>' for i in range(1, 7)) + '</g>' + rect(0, 0, 287, 66, "none")
bed += g(mY(468, 668, 110.5), fq)
sq = "".join(f'<rect x="{j*53.5}" y="0" width="53.5" height="66" fill="{"#1F1B3A" if (6+j)%2 else "#FFFBF2"}"/>' for j in range(6)) + f'<g stroke="#8E87A3" stroke-width="2" stroke-dasharray="5 4">' + "".join(f'<path d="M{j*53.5} 0 V66"/>' for j in range(1, 6)) + '</g>' + rect(0, 0, 321, 66, "none")
bed += g(mX(955, 468, 110.5), sq)
add(bed)

# seasonal props (shown by the page on the right dates)
_tx, _ty = P(300, 160, 0)
add(f'<g id="sXmas" style="display:none" transform="translate({f(_tx)} {f(_ty)})">'
    f'<rect x="-8" y="-14" width="16" height="14" fill="#8C5A33" stroke="{INK}" stroke-width="2.5"/>'
    f'<path d="M0 -110 L34 -50 H18 L42 -14 H-42 L-18 -50 H-34Z" fill="#2E9C5A" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
    f'<path d="M0 -122 l4 9 10 1 -8 6 3 10 -9 -6 -9 6 3 -10 -8 -6 10 -1Z" fill="#F8D65A" stroke="{INK}" stroke-width="1.8"/>'
    + "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="{c}" stroke="{INK}" stroke-width="1.5"/>' for x, y, c in [(-14, -60, "#F2543D"), (10, -78, "#5B9BFF"), (18, -30, "#FF6FAE"), (-22, -26, "#F8D65A"), (4, -44, "#F2543D")])
    + '</g>')
_px, _py = P(578, 58, 112)
add(f'<g id="sHallo" style="display:none" transform="translate({f(_px)} {f(_py)})">'
    f'<ellipse cx="0" cy="-12" rx="17" ry="13" fill="#FF8A2A" stroke="{INK}" stroke-width="2.5"/><path d="M-6 -24 q-2 12 0 24 M6 -24 q2 12 0 24" stroke="#C25E14" stroke-width="2" fill="none"/>'
    f'<path d="M0 -25 q1 -7 6 -9" stroke="#2E9C5A" stroke-width="3" fill="none" stroke-linecap="round"/>'
    f'<path d="M-10 -15 l4 -4 4 4Z M3 -15 l4 -4 4 4Z" fill="#FFE27A"/><path d="M-9 -6 q9 6 18 0 l-3 2 -3 -2 -3 2 -3 -2 -3 2Z" fill="#FFE27A"/></g>')
_flags = "".join(
    f'<path d="M{18+i*21} 0 l18 0 -9 22Z" fill="{["#FF6FAE","#F8D65A","#5B9BFF","#7FDBA8","#F2543D"][i%5]}" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>'
    f'<text x="{27+i*21}" y="12" text-anchor="middle" font-family="Bricolage Grotesque, Arial Black, sans-serif" font-weight="800" font-size="9" fill="#1F1B3A">{ch}</text>'
    for i, ch in enumerate("HAPPY BDAY DEE") if ch != " " or True)
add('<g id="sBday" style="display:none">' + g(mY(21, 662, 236), f'<path d="M10 0 Q150 12 296 0" fill="none" stroke="{INK}" stroke-width="2"/>' + _flags) + '</g>')

# y2k scatter cushions
def cush(x, y, inner):
    cx, cy = P(x, y, 110)
    return f'<g transform="translate({f(cx)} {f(cy)}) scale(1.35)">{inner}</g>'
FUZZ = 'stroke-dasharray="3 2"'
heart = (f'<path d="M0 -6 C0 -24 -28 -26 -28 -8 C-28 6 -10 14 0 24 C10 14 28 6 28 -8 C28 -26 0 -24 0 -6Z" transform="translate(0 -22)" fill="#FF8FC2" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
         f'<path d="M0 -6 C0 -24 -28 -26 -28 -8 C-28 6 -10 14 0 24 C10 14 28 6 28 -8 C28 -26 0 -24 0 -6Z" transform="translate(0 -22)" fill="none" stroke="#FFC4DD" stroke-width="2" {FUZZ}/>'
         '<path d="M-16 -36 q4 -6 10 -6" stroke="#ffffffaa" stroke-width="4" fill="none" stroke-linecap="round"/>')
smiley = (f'<circle cx="0" cy="-22" r="23" fill="#F8D65A" stroke="{INK}" stroke-width="3"/>'
          f'<ellipse cx="-8" cy="-27" rx="3" ry="5" fill="{INK}"/><ellipse cx="8" cy="-27" rx="3" ry="5" fill="{INK}"/>'
          f'<path d="M-12 -16 q12 12 24 0" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/>')
fly = (f'<path d="M0 -24 C-8 -46 -34 -46 -30 -28 C-28 -18 -12 -18 0 -22Z M0 -24 C8 -46 34 -46 30 -28 C28 -18 12 -18 0 -22Z" fill="#B39BFF" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
       f'<path d="M0 -20 C-6 -4 -26 0 -24 -12 C-22 -18 -10 -20 0 -20Z M0 -20 C6 -4 26 0 24 -12 C22 -18 10 -20 0 -20Z" fill="#8FD3F5" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
       f'<rect x="-3" y="-34" width="6" height="26" rx="3" fill="{INK}"/><circle cx="-18" cy="-32" r="3" fill="#FFFBF2"/><circle cx="18" cy="-32" r="3" fill="#FFFBF2"/>')
fur = (f'<rect x="-26" y="-44" width="52" height="40" rx="14" fill="#FF6FAE" stroke="{INK}" stroke-width="3"/>'
       f'<rect x="-26" y="-44" width="52" height="40" rx="14" fill="none" stroke="#FFB3D4" stroke-width="3" {FUZZ}/>'
       '<path d="M-14 -34 l4 6 M2 -36 l3 6 M14 -30 l-4 6 M-6 -20 l5 4" stroke="#FFC4DD" stroke-width="2" stroke-linecap="round"/>')
add(cush(706, 74, fur) + cush(778, 66, heart) + cush(866, 70, smiley) + cush(930, 78, fly))


# ---------- girl sitting on the floor against the right side of the bed, turned toward the viewer ----------
SK, SKD, HAIR, HL = "#F4C4A1", "#E3AE89", "#E8742A", "#F6D27A"
def limb(d, w, col, cls=""):
    return (f'<path d="{d}" stroke="{INK}" stroke-width="{w+5}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
KT = "0;.28;.36;.46;.52;.56;.62;.72;.8;1"
SM, RE, AS, TP = "M16 -112 L46 -100 L30 -140", "M16 -112 L40 -78 L72 -88", "M16 -112 L36 -64 L50 -6", "M16 -112 L36 -64 L50 -2"
ARM = [SM, SM, RE, AS, AS, TP, AS, RE, SM, SM]
HANDS = ["30 -140", "30 -140", "72 -88", "50 -6", "50 -6", "50 -2", "50 -6", "72 -88", "30 -140", "30 -140"]
TATS = ["38 -120", "38 -120", "56 -83", "43 -35", "43 -35", "43 -33", "43 -35", "56 -83", "38 -120", "38 -120"]
def anim_d(): return f'<animate attributeName="d" dur="12s" repeatCount="indefinite" keyTimes="{KT}" values="{";".join(ARM)}"/>'
def arm_path(stroke, w, extra=""):
    return f'<path d="{ARM[0]}" stroke="{stroke}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round" {extra}>{anim_d()}</path>'
gx, gy = P(992, 300, 0)
G = f'<g id="girl" class="girl hot" data-toggle="girl" transform="translate({f(gx)} {f(gy)}) scale(1.15)">'
G += '<ellipse cx="50" cy="6" rx="105" ry="13" fill="#1F1B3A" opacity=".18"/>'
# ashtray on the floor by her left hip (against the bed)
G += (f'<ellipse cx="52" cy="6" rx="15" ry="5.5" fill="#2E9C96" stroke="{INK}" stroke-width="2.5"/><ellipse cx="52" cy="4" rx="9" ry="3" fill="#1E6E6A"/>'
      '<g class="ash"><circle cx="51" cy="-8" r="1.6"/><circle cx="55" cy="-10" r="1.3"/><circle cx="53" cy="-12" r="1.1"/></g>')
# far leg (her left), stretched out, green sock
G += limb("M-6 -8 L70 2 L140 12", 19, SKD) + limb("M140 12 L154 2", 14, "#7FDBA8") + '<path d="M144 9 l2 -8 M150 8 l2 -8" stroke="#F8D65A" stroke-width="3"/>'
# far arm upper part (behind the torso)
LEFT = "M-16 -116 L-30 -64 L20 -36"
# torso in the EAT THE RICH tee
G += (f'<path id="tee" d="M-26 -122 C-10 -128 14 -126 26 -118 C30 -84 30 -46 28 -14 L-22 -12 C-28 -50 -30 -90 -26 -122Z" fill="#2B2733" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
      f'<g class="hoodie"><path d="M-16 -50 H20 L24 -24 H-18Z" fill="#5A4CD8" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
      f'<path d="M-25 -119 C-22 -136 22 -136 25 -117" stroke="{INK}" stroke-width="15" fill="none" stroke-linecap="round"/><path d="M-25 -119 C-22 -136 22 -136 25 -117" stroke="#6A5CFF" stroke-width="10" fill="none" stroke-linecap="round"/>'
      f'<path d="M-2 -122 l-1 12 M14 -122 l1 12" stroke="#FFFBF2" stroke-width="2" stroke-linecap="round"/><circle cx="-3" cy="-109" r="2" fill="#FFFBF2" stroke="{INK}" stroke-width="1"/><circle cx="15" cy="-109" r="2" fill="#FFFBF2" stroke="{INK}" stroke-width="1"/></g>'
      '<text id="shirtTxt" x="7" y="-90" text-anchor="middle" font-family="Oswald, Impact, sans-serif" font-weight="700" fill="#FFFBF2"><tspan x="7" y="-90" font-size="11.5" letter-spacing=".3">EAT THE</tspan><tspan x="7" y="-75" font-size="13.5" letter-spacing="1">RICH</tspan></text>')
G += f'<path d="M-24 -22 L28 -20 L36 4 L-20 8Z" fill="#3D57A6" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/><path d="M6 -21 L8 6" stroke="#2C428A" stroke-width="2"/>'
# near leg (her right), knee up, star tattoo on the knee, pink sock
G += limb("M14 -8 L62 -78 L104 10", 20, SK) + limb("M104 10 L124 4", 14, "#FF6FAE") + '<path d="M109 8 l2 -8 M116 7 l2 -8" stroke="#FFFBF2" stroke-width="3"/>'
G += f'<path d="M60 -84 l2.4 5 5.4 .5 -4 3.6 1.2 5.3 -5 -2.8 -5 2.8 1.2 -5.3 -4 -3.6 5.4 -.5Z" fill="{INK}"/>'
# book open on her lap, held by her left hand (full sleeve)
G += (f'<path d="M30 -48 L4 -36 L6 -28 L30 -40 L58 -32 L58 -40Z" fill="#3A3A42" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>'
      f'<path d="M8 -32 L30 -43 L54 -35 L30 -40Z" fill="#FFFBF2" stroke="{INK}" stroke-width="1.4"/>')
G += (limb(LEFT, 12, SK) + f'<path d="{LEFT}" stroke="#2E9C96" stroke-width="12" fill="none" stroke-dasharray="5 3" stroke-linecap="round" stroke-linejoin="round"/>'
      f'<path d="{LEFT}" stroke="#F2543D" stroke-width="5" fill="none" stroke-dasharray="2 7" stroke-linecap="round"/>'
      f'<circle cx="20" cy="-36" r="6.5" fill="{SK}" stroke="{INK}" stroke-width="2.5"/>')
G += '<g id="girlHead">'
# neck + head, 3/4 view, looking down at the book; orange hair with thick blonde highlights in a messy bun
G += (f'<rect x="-6" y="-134" width="14" height="14" fill="{SK}" stroke="{INK}" stroke-width="2.5"/>'
      f'<circle cx="-10" cy="-176" r="12" fill="{HAIR}" stroke="{INK}" stroke-width="2.5"/>'
      f'<path d="M-16 -180 q6 -6 12 -2" stroke="{HL}" stroke-width="3.5" fill="none" stroke-linecap="round"/>'
      f'<circle id="girlFace" cx="4" cy="-150" r="23" fill="{SK}" stroke="{INK}" stroke-width="3"/>'
      f'<path d="M-19 -146 C-22 -170 -4 -180 14 -174 C22 -170 26 -164 26 -158 C14 -162 4 -160 -2 -152 C-6 -146 -10 -136 -14 -132 C-18 -136 -19 -140 -19 -146Z" fill="{HAIR}" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>'
      f'<path d="M-12 -150 C-12 -162 -2 -170 8 -170 M-4 -140 C-6 -152 2 -162 14 -166 M14 -172 C20 -170 23 -166 24 -162" stroke="{HL}" stroke-width="4" fill="none" stroke-linecap="round"/>'
      f'<path d="M24 -158 C28 -150 27 -140 22 -134" stroke="{HAIR}" stroke-width="5" fill="none" stroke-linecap="round"/><path d="M25 -154 C27 -148 26 -142 23 -137" stroke="{HL}" stroke-width="2" fill="none" stroke-linecap="round"/>'
      f'<ellipse cx="-8" cy="-148" rx="4" ry="5.5" fill="{SKD}" stroke="{INK}" stroke-width="1.6"/>'
      f'<path class="eyes-c" d="M6 -150 q4 3 8 0 M17 -151 q3 2 6 0" stroke="{INK}" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
      f'<g class="roll"><ellipse cx="10" cy="-151" rx="4.6" ry="4" fill="#fff" stroke="{INK}" stroke-width="1.5"/><ellipse cx="20" cy="-152" rx="3.6" ry="3.8" fill="#fff" stroke="{INK}" stroke-width="1.5"/>'
      f'<circle class="pup" cx="10" cy="-150" r="1.9" fill="{INK}"/><circle class="pup" cx="20" cy="-151" r="1.7" fill="{INK}"/>'
      f'<path d="M5 -152.5 q5 -3.5 10 0 M16.4 -153.6 q3.6 -2.6 7.2 0" stroke="{INK}" stroke-width="2" fill="{SK}"/></g>'
      f'<path d="M21 -146 l3 5 l-4 1" stroke="{INK}" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
      f'<path d="M12 -137 q4 2 8 0" stroke="#C2564A" stroke-width="2.4" fill="none" stroke-linecap="round"/>'
      f'<circle cx="10" cy="-142" r="3" fill="#F2A0A0" opacity=".5"/>')
# headphones over her hair, cord down to her shorts pocket
G += (f'<path d="M-10 -136 C-16 -110 -30 -70 -6 -40 C6 -26 14 -20 18 -14" stroke="{INK}" stroke-width="2" fill="none"/>'
      f'<path d="M-17 -152 C-17 -186 27 -190 29 -156" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"/>'
      f'<path d="M-17 -152 C-17 -186 27 -190 29 -156" stroke="#FF6FAE" stroke-width="3.5" fill="none" stroke-linecap="round"/>'
      f'<rect x="24" y="-164" width="9" height="18" rx="4" fill="#3B3550" stroke="{INK}" stroke-width="2"/>'
      f'<rect x="-19" y="-162" width="16" height="25" rx="7" fill="#3B3550" stroke="{INK}" stroke-width="2.5"/>'
      f'<rect x="-15" y="-157" width="8" height="15" rx="4" fill="#FF6FAE"/>')
G += '</g>'
# near arm (her right): smokes, rests on her knee, taps ash; two patchwork tattoos ride on the forearm
G += arm_path(INK, 17) + arm_path(SK, 12)
G += (f'<g><animateTransform attributeName="transform" type="translate" dur="12s" repeatCount="indefinite" keyTimes="{KT}" values="{";".join(TATS)}"/>'
      f'<g stroke="{INK}" stroke-width="1"><rect x="-6" y="-4" width="6" height="6" fill="#F2543D"/><rect x="-3" y="-4" width="3" height="3" fill="#F8D65A"/>'
      '<rect x="2" y="-2" width="6" height="6" fill="#5B9BFF"/><rect x="2" y="1" width="3" height="3" fill="#7FDBA8"/></g></g>')
hand = (f'<circle cx="0" cy="0" r="6.5" fill="{SK}" stroke="{INK}" stroke-width="2.5"/>'
        f'<path d="M3 -3 L20 -12 L21 -9 L4 0Z" fill="#FFFBF2" stroke="{INK}" stroke-width="1.4"/>'
        '<circle class="ember" cx="21" cy="-10.5" r="2.4" fill="#FF7A2A"/>'
        '<g class="smoke" transform="translate(22 -13)"><path d="M0 0 q-6 -10 2 -20 q7 -10 -1 -22"/><path d="M0 0 q6 -12 -2 -22 q-6 -9 2 -20"/></g>')
G += (f'<g transform="translate(30 -140)"><animateTransform attributeName="transform" type="translate" dur="12s" repeatCount="indefinite" keyTimes="{KT}" values="{";".join(HANDS)}"/>{hand}</g>')
# exhale
G += '<g class="exhale2" transform="translate(16 -142)"><circle cx="0" cy="0" r="5"/><circle cx="6" cy="-9" r="7"/><circle cx="14" cy="-20" r="9"/></g>'
G += '</g>'
add(G)

# ---------- the cats ----------
ax, ay = P(800, 250, 112)
add('<g id="miataPos">')
add(f"""<g id="catA" class="hot cat" data-cat="catA"><g transform="translate({f(ax)} {f(ay)}) scale(.74)"><g class="breathe">
<ellipse cx="0" cy="0" rx="74" ry="36" fill="#F09A3E" stroke="{INK}" stroke-width="3.5"/>
<g stroke="#B85C1A" stroke-width="5" fill="none" stroke-linecap="round"><path d="M-12 -34 q7 14 0 26"/><path d="M8 -35 q7 14 0 26"/><path d="M28 -31 q7 12 0 22"/><path d="M46 -24 q6 10 0 18"/></g>
<g class="tail"><path d="M66 8 C72 32 30 42 -10 36 C-38 33 -56 28 -64 20" stroke="{INK}" stroke-width="23" fill="none" stroke-linecap="round"/><path d="M66 8 C72 32 30 42 -10 36 C-38 33 -56 28 -64 20" stroke="#F09A3E" stroke-width="16" fill="none" stroke-linecap="round"/>
<g stroke="#B85C1A" stroke-width="4"><path d="M40 30 v10"/><path d="M14 33 v10"/><path d="M-14 31 v10"/></g></g>
<ellipse cx="-28" cy="30" rx="13" ry="7" fill="#FFF4DE" stroke="{INK}" stroke-width="2.5"/>
<g class="head">
<g class="bdayhat"><path d="M-74 -30 L-46 -36 L-64 -70Z" fill="#FF6FAE" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/><path d="M-70 -38 L-52 -42 M-67 -50 L-56 -52" stroke="#F8D65A" stroke-width="3"/><circle cx="-64" cy="-72" r="5" fill="#F8D65A" stroke="{INK}" stroke-width="2"/></g>
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
<g transform="translate(-62 26)"><g class="paw">
<path d="M0 -9 C-16 -12 -34 -11 -46 -9 C-50 -8 -52 -4 -52 0 C-52 5 -49 8 -45 8 C-32 9 -16 10 0 9Z" fill="#F09A3E" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>
<path d="M-14 -10 q3 9 0 19 M-28 -10 q3 9 0 18" stroke="#B85C1A" stroke-width="3.5" fill="none" stroke-linecap="round"/>
<ellipse cx="-56" cy="0" rx="12" ry="11" fill="#F7A54E" stroke="{INK}" stroke-width="3"/>
<ellipse cx="-56" cy="3" rx="6" ry="5" fill="#F6B7C4"/>
<circle cx="-64" cy="-6" r="2.6" fill="#F6B7C4"/><circle cx="-67" cy="1" r="2.6" fill="#F6B7C4"/><circle cx="-64" cy="8" r="2.6" fill="#F6B7C4"/>
<g fill="#FFFDF6" stroke="{INK}" stroke-width="1.3" stroke-linejoin="round"><path d="M-66 -9 C-73 -14 -77 -14 -79 -11 C-75 -11 -71 -9 -68 -6Z"/><path d="M-68 -2 C-76 -4 -80 -2 -81 1 C-77 0 -73 1 -69 2Z"/><path d="M-67 5 C-74 6 -78 9 -78 12 C-75 10 -71 9 -67 9Z"/></g>
</g></g>
<g class="streaks"><path d="M-96 -42 Q-134 -24 -128 18"/><path d="M-110 -40 Q-146 -18 -138 22"/><path d="M-124 -34 Q-156 -10 -146 26"/></g>
</g></g></g>""")
add(f'<text class="zz" x="{f(ax-60)}" y="{f(ay-44)}" font-size="20">z</text><text class="zz" x="{f(ax-48)}" y="{f(ay-54)}" font-size="15">z</text>')
add('</g>')
cx_, cy_ = P(280, 560, 0)
O, B, W = "#F0923A", "#2B2733", "#FFFBF2"
add('<g id="catBedFront" style="display:none">' + _fluff(_bumps(True), "#7FDB97") + "".join(f'<path d="M{f(_bx+dx)} {f(_by+dy)} q3 -3 6 0" stroke="#B5F0C4" stroke-width="1.8" fill="none" stroke-linecap="round"/>' for dx, dy in [(-34, 10), (-12, 17), (14, 17), (32, 9)]) + '</g>')
_kx, _ky = P(374, 210, 0)
add(f'<g id="chips" class="hot" data-toggle="chips" transform="translate({f(_kx)} {f(_ky)})"><g class="chipbag">'
    f'<ellipse cx="6" cy="2" rx="30" ry="6" fill="#1F1B3A" opacity=".18"/>'
    + "".join(f'<ellipse class="chip" cx="{x}" cy="{y}" rx="6" ry="3.6" fill="#F8C94A" stroke="{INK}" stroke-width="1.6" transform="rotate({r} {x} {y})"/>' for x, y, r in [(24, 0, -10), (33, -3, 20), (28, 5, 5), (-22, 3, 15)])
    + f'<g transform="rotate(-8)"><path d="M-17 0 L-19 -42 l4.75 -4 4.75 4 4.75 -4 4.75 4 4.75 -4 4.75 4 4.75 -4 4.75 4 L17 0 Z" fill="#FF4FA3" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
    f'<path d="M-18.6 -36 H18.6" stroke="{INK}" stroke-width="2"/><path d="M-18.4 -33 H18.4" stroke="#FFE27A" stroke-width="3"/>'
    f'<circle cx="0" cy="-18" r="10" fill="#FFE27A" stroke="{INK}" stroke-width="2"/>'
    '<text x="0" y="-16" text-anchor="middle" font-family="Bricolage Grotesque, Arial Black, sans-serif" font-weight="800" font-size="5.6" fill="#1F1B3A" transform="rotate(-10 0 -18)">CRNCH</text>'
    f'<path d="M-12 -6 l2 -4 M10 -8 l3 -3" stroke="#FFFFFF" stroke-opacity=".6" stroke-width="2" stroke-linecap="round"/></g></g></g>')
add(f"""<g id="supraPos" transform="translate({f(cx_)} {f(cy_)})"><g class="supz"><text class="zz" x="30" y="-70" font-size="18">z</text><text class="zz" x="42" y="-80" font-size="13">z</text></g><g id="catB" class="hot cat" data-cat="catB"><g class="flip"><g transform="scale(.9)">
<ellipse cx="0" cy="2" rx="52" ry="8" fill="#1F1B3A" opacity=".18"/>
<g class="napcat">
<path d="M-40 -10 C-54 6 -14 14 22 4" stroke="{INK}" stroke-width="14" fill="none" stroke-linecap="round"/>
<ellipse cx="0" cy="-22" rx="46" ry="23" fill="{W}"/>
<clipPath id="calNap"><ellipse cx="0" cy="-22" rx="46" ry="23"/></clipPath>
<g clip-path="url(#calNap)"><path d="M-48 -44 C-30 -36 -24 -22 -6 -26 C6 -30 10 -42 0 -48Z" fill="{O}"/><path d="M6 -48 C10 -34 24 -30 32 -36 C38 -42 32 -48 20 -50Z" fill="{B}"/><path d="M-48 -20 C-40 -10 -30 -4 -22 0 L-48 4Z" fill="{B}"/></g>
<ellipse cx="0" cy="-22" rx="46" ry="23" fill="none" stroke="{INK}" stroke-width="3.5"/>
<path d="M-34 -8 C-28 -30 -4 -32 2 -12" stroke="{INK}" stroke-width="2.5" fill="none" stroke-linecap="round"/>
<path d="M-40 -10 C-54 6 -14 14 22 4" stroke="{O}" stroke-width="8" fill="none" stroke-linecap="round"/>
<path d="M10 3.5 C16 3 20 4 22 4" stroke="{B}" stroke-width="8" fill="none" stroke-linecap="round"/>
<ellipse cx="26" cy="-4" rx="9" ry="5.5" fill="{W}" stroke="{INK}" stroke-width="2.6"/>
<ellipse cx="40" cy="-3" rx="9" ry="5.5" fill="{W}" stroke="{INK}" stroke-width="2.6"/>
<path d="M28 -40 L28 -62 L42 -46Z" fill="{B}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/><path d="M31 -45 L31 -56 L38 -47Z" fill="#F6B7C4"/>
<path d="M50 -46 L62 -62 L64 -38Z" fill="{O}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/><path d="M53 -45 L61 -56 L62 -42Z" fill="#F6B7C4"/>
<circle cx="46" cy="-26" r="18" fill="{W}"/>
<clipPath id="calNapH"><circle cx="46" cy="-26" r="18"/></clipPath>
<g clip-path="url(#calNapH)"><path d="M26 -48 L44 -46 L40 -30 C34 -28 28 -32 26 -38Z" fill="{B}"/><path d="M50 -48 C52 -34 58 -28 68 -30 L68 -48Z" fill="{O}"/></g>
<circle cx="46" cy="-26" r="18" fill="none" stroke="{INK}" stroke-width="3.5"/>
<g stroke="{INK}" stroke-width="2.4" fill="none" stroke-linecap="round"><path d="M37 -28 q4 3 8 0 M50 -28 q4 3 8 0"/></g>
<path d="M45 -22 h6 l-3 4Z" fill="#E8577E" stroke="{INK}" stroke-width="1.2"/>
<path d="M48 -18 q-3 3 -6 1.5 M48 -18 q3 3 6 1.5" stroke="{INK}" stroke-width="1.5" fill="none" stroke-linecap="round"/>
<g stroke="{INK}" stroke-width="1.2"><path d="M38 -20 l-14 -1 M38 -18 l-14 3 M58 -20 l14 -1 M58 -18 l14 3"/></g>
</g>
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
<g class="eyeo"><circle cx="50" cy="-61" r="3" fill="{INK}"/><circle cx="64" cy="-61" r="3" fill="{INK}"/><circle cx="51" cy="-62" r="1" fill="#fff"/><circle cx="65" cy="-62" r="1" fill="#fff"/></g><g class="eyec" stroke="{INK}" stroke-width="2.4" fill="none" stroke-linecap="round"><path d="M46 -61 q4 3 8 0 M60 -61 q4 3 8 0"/></g>
<path d="M54 -54 h6 l-3 4Z" fill="#E8577E" stroke="{INK}" stroke-width="1.2"/>
<path d="M57 -50 q-3 4 -7 2 M57 -50 q3 4 7 2" stroke="{INK}" stroke-width="1.6" fill="none" stroke-linecap="round"/>
<g stroke="{INK}" stroke-width="1.3"><path d="M46 -52 l-16 -2 M46 -50 l-16 3 M68 -52 l16 -2 M68 -50 l16 3"/></g>
</g></g></g></g></g></g>""")

# ---------- light ----------
gx, gy = lamp_x, lamp_y - 90
lvx, lvy = P(512, 50, 175)
lpx, lpy = P(30, 444, 225)
add('<rect id="goldTint" x="-50" y="-50" width="1700" height="1100" fill="#FF9F4A" style="mix-blend-mode:soft-light;pointer-events:none" opacity="0"/>')
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
<linearGradient id="mirG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#DCEBFA"/><stop offset=".5" stop-color="#B9CDF0"/><stop offset="1" stop-color="#E6D7F7"/></linearGradient>
<linearGradient id="lavaG" x1="0" y1="0" x2="0" y2="1"><stop id="lava0" offset="0" stop-color="#FFB36E"/><stop id="lava1" offset="1" stop-color="#FF5C8A"/></linearGradient>
<linearGradient id="beamG" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#FFF6D8" stop-opacity=".6"/><stop offset="1" stop-color="#FFF6D8" stop-opacity=".06"/></linearGradient>
<linearGradient id="skyG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF9F6E"/><stop offset=".6" stop-color="#FFC878"/><stop offset="1" stop-color="#FFE2A8"/></linearGradient>
<radialGradient id="warm"><stop offset="0" stop-color="#FFC870" stop-opacity=".75"/><stop offset=".45" stop-color="#FF9F4A" stop-opacity=".25"/><stop offset="1" stop-color="#FF9F4A" stop-opacity="0"/></radialGradient>
<radialGradient id="lavaGlowG"><stop id="lavaGlowStop" offset="0" stop-color="#FF7A8A" stop-opacity=".75"/><stop offset="1" stop-color="#FF7A8A" stop-opacity="0"/></radialGradient>
<radialGradient id="pinkG"><stop offset="0" stop-color="#FF7A8A" stop-opacity=".7"/><stop offset="1" stop-color="#FF7A8A" stop-opacity="0"/></radialGradient>
<radialGradient id="blueG"><stop offset="0" stop-color="#8FB6FF" stop-opacity=".6"/><stop offset="1" stop-color="#8FB6FF" stop-opacity="0"/></radialGradient>
<filter id="neonGlow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>'''

svg = ('<svg id="room" viewBox="0 0 1600 1000" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="roomTitle">'
       '<desc id="roomTitle">Dee\'s bedroom, seen from the corner: a lilac bookshelf, a record player on a mustard cabinet, toy cars on a shelf over the bed, a ginger cat asleep on a checkerboard bedspread, a girl with headphones reading on the floor beside the bed, a calico cat on the rug, a desk with a retro laptop under the window and an old TV beside it</desc>'
       + DEFS + "".join(out) + "</svg>")
(pathlib.Path(__file__).parent / "room.svg").write_text(svg)
print("scene", len(svg))
