"""Build the three static Lesson 4 figures (interfaces and the common centre, Sections 20-23).
Run with Python 3 only; no Pillow, network or browser is needed.
Companion to build-straddle.py and drawn in the same style and palette.
Geometry is to scale in each figure (UNIT px per unit length). Every straddle region
Delta(K) of a segment K is drawn exactly as in Lesson 3: the open radius-1 capsule
about K minus the lens where the two closed unit disks at the endpoints overlap,
as a fine polygon filled even-odd. Intersections are drawn with an even-odd clip path.
"""
from pathlib import Path
import math

OUT = Path(__file__).resolve().parent
INK = "#172c43"
RED = "#b33d39"
BLUE = "#235f9d"
GREEN = "#2f7a4a"
PALE_RED = "#fbe9e5"
PALE_BLUE = "#e7f0fb"
PALE_GREEN = "#e3f2e6"
GREY = "#63758a"

def text(x, y, value, size=26, fill=INK, anchor="start", weight=400, halo=False):
    h = ' stroke="white" stroke-width="6" stroke-linejoin="round" paint-order="stroke"' if halo else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}"{h}>{value}</text>'

def line(x1,y1,x2,y2,stroke=INK,width=3,extra=""):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{stroke}" stroke-width="{width}" {extra}/>'

def dot(x,y,fill=RED,r=7):
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="2"/>'

def svg(name, h, title, desc, parts, defs=""):
    body = "\n".join(parts)
    (OUT/name).write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="720" height="{h}" viewBox="0 0 720 {h}" role="img" aria-labelledby="title desc">\n'
        f'<title id="title">{title}</title><desc id="desc">{desc}</desc>\n'
        + (f'<defs>{defs}</defs>\n' if defs else "") +
        f'<rect width="720" height="{h}" fill="white"/>\n'
        '<g font-family="Segoe UI, Arial, sans-serif">\n'+body+'\n</g></svg>\n',encoding="utf-8")

def arc(cx,cy,r,a0,a1,n):
    # points on a circle, maths angles (counter-clockwise, y up) mapped to SVG
    return [(cx+r*math.cos(a0+(a1-a0)*j/n), cy-r*math.sin(a0+(a1-a0)*j/n)) for j in range(n+1)]

def poly(pts):
    return "M"+" L".join(f"{x:.2f},{y:.2f}" for x,y in pts)+" Z"

def straddle_path(p, q, unit, n=720):
    """Exact Delta(K) for the segment K=[p,q] (SVG coordinates), as an even-odd path:
    the capsule about K with the closed endpoint-disk lens removed."""
    (px,py),(qx,qy) = p,q
    L = math.hypot(qx-px, qy-py)/unit
    ang = math.atan2(-(qy-py), qx-px)          # maths angle of p->q
    capsule = arc(qx,qy,unit,ang-math.pi/2,ang+math.pi/2,n)+arc(px,py,unit,ang+math.pi/2,ang+3*math.pi/2,n)
    th = math.atan2(math.sqrt(1-L*L/4), L/2)
    lens = arc(px,py,unit,ang-th,ang+th,n)+arc(qx,qy,unit,ang+math.pi-th,ang+math.pi+th,n)
    return f"{poly(capsule)} {poly(lens)}"

def polyline(pts, stroke, width, extra=""):
    return f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x,y in pts)}" fill="none" stroke="{stroke}" stroke-width="{width}" {extra}/>'

# ------------------------------------------------- Figure A: an interface model
UNIT = 300.0
KX, KY = 470.0, 330.0              # K is vertical, centred at (KX, KY)
HALF = 0.2                         # K runs from height -0.2 to +0.2
W = 0.18                           # width of each colour strip
ZU = (-0.9, 0.436)                   # z in units relative to the centre of K (y up)
def P(u, v):                       # units -> SVG
    return KX+u*UNIT, KY-v*UNIT
zx, zy = P(*ZU)
yq = ZU[1]-math.sqrt(1-ZU[0]**2)   # where z's unit circle meets the line of K
qx, qy = P(0, yq)
a_q = math.atan2(yq-ZU[1], -ZU[0])  # angle of q seen from z
def circle_pts(a0, a1, n=200):
    return arc(zx, zy, UNIT, a0, a1, n)
# the arc inside the A strip (u in (-W,0)) and inside the B strip (u in (0,W)), restricted to |v|<HALF
def strip_arc(side):
    pts=[]; best=[]
    for j in range(4001):
        a = a_q-0.5+1.0*j/4000
        u = ZU[0]+math.cos(a); v = ZU[1]+math.sin(a)
        inside = abs(v) < HALF and ((-W < u < 0) if side == "A" else (0 < u < W))
        if inside: pts.append(P(u, v))
        elif pts: best = pts if len(pts) > len(best) else best; pts = []
    return pts if len(pts) > len(best) else best
arcA, arcB = strip_arc("A"), strip_arc("B")
parts = [text(360,46,"A circle that crosses an interface meets both colours",29,anchor="middle",weight=600),
         text(360,82,"Model: colour A on one side of the segment K, colour B on the other.",21,anchor="middle"),
         f'<rect x="{KX-W*UNIT:.2f}" y="{KY-HALF*UNIT:.2f}" width="{W*UNIT:.2f}" height="{2*HALF*UNIT:.2f}" fill="{PALE_BLUE}" stroke="{BLUE}" stroke-width="1.5"/>',
         f'<rect x="{KX:.2f}" y="{KY-HALF*UNIT:.2f}" width="{W*UNIT:.2f}" height="{2*HALF*UNIT:.2f}" fill="{PALE_GREEN}" stroke="{GREEN}" stroke-width="1.5"/>',
         text(KX-W*UNIT-12,KY+50,"colour A",21,fill=BLUE,anchor="end",weight=600),
         text(KX+W*UNIT+12,KY-HALF*UNIT+20,"colour B",21,fill=GREEN,weight=600),
         polyline(circle_pts(a_q-0.42, a_q+0.42), GREY, 2, 'stroke-dasharray="7 6"'),
         polyline(arcA, BLUE, 6), polyline(arcB, GREEN, 6),
         line(*P(0,-HALF), *P(0,HALF), INK, 5),
         text(KX, KY-HALF*UNIT-10, "K", 26, anchor="middle", weight=600),
         line(zx, zy, qx, qy, RED, 3),
         dot(zx, zy, INK, 7), text(zx-14, zy+8, "z", 27, anchor="end", weight=600),
         text((zx+qx)/2-6, (zy+qy)/2+28, "1", 24, fill=RED, anchor="middle", weight=600),
         dot(qx, qy, RED, 6),
         text(KX+W*UNIT+12, qy+7, "crossing q", 20, fill=RED),
         text(KX+W*UNIT+12, KY+44, "unit circle of z:", 18, fill=GREY),
         text(KX+W*UNIT+12, KY+67, "dashed, thick where", 18, fill=GREY),
         text(KX+W*UNIT+12, KY+90, "it runs through A or B", 18, fill=GREY),
         text(360, KY+HALF*UNIT+90, "Near q the circle runs through both A and B, so z is robust in neither colour.", 19, anchor="middle", weight=600)]
svg("interface-model.svg", int(KY+HALF*UNIT+116), "A unit circle crossing an interface meets both of its colours",
    "A short vertical segment K with a strip of colour A on its left and a strip of colour B on its right. A point z to the lower left straddles K. Part of the unit circle around z is drawn dashed; it crosses K at a point q strictly between the ends of K, with a red ruler of length 1 from z to q. Just below q the circle runs through the A strip (thick blue) and just above q through the B strip (thick green).", parts)

# ------------------------------------------------- Figure B: the shadow of one short interface
UNIT = 180.0; L = 0.25
X0, Y0 = 360.0-L/2*UNIT, 300.0       # the centre x
far = (X0+L*UNIT, Y0)
parts = [text(360,44,"A short interface casts a thin shadow on the unit circle",28,anchor="middle",weight=600),
         text(360,78,f"K leaves the centre x eastward; L = {L} is exaggerated.",21,anchor="middle"),
         f'<path d="{straddle_path((X0,Y0), far, UNIT)}" fill="{PALE_RED}" fill-rule="evenodd" stroke="{RED}" stroke-width="1.2"/>',
         f'<circle cx="{X0:.2f}" cy="{Y0:.2f}" r="{UNIT:.2f}" fill="none" stroke="{BLUE}" stroke-width="2.5" stroke-dasharray="7 6"/>',
         line(X0, Y0, far[0], far[1], INK, 6), dot(X0, Y0, INK, 6), dot(far[0], far[1], BLUE, 5),
         text(X0-10, Y0+28, "x", 26, anchor="end", weight=600),
         text((X0+far[0])/2, Y0-16, "K", 24, anchor="middle", weight=600),
         text(far[0]+UNIT+12, Y0-22, "just outside", 18, fill=RED),
         text(far[0]+UNIT+12, Y0+0, "the circle,", 18, fill=RED),
         text(far[0]+UNIT+12, Y0+22, "facing K", 18, fill=RED),
         text(X0-UNIT-12, Y0-22, "just inside", 18, fill=RED, anchor="end"),
         text(X0-UNIT-12, Y0+0, "the circle,", 18, fill=RED, anchor="end"),
         text(X0-UNIT-12, Y0+22, "far side", 18, fill=RED, anchor="end"),
         text(360, Y0+UNIT+44, "Dashed blue: the unit circle around x. Shaded: Δ(K), drawn exactly.", 18, anchor="middle"),
         text(360, Y0+UNIT+70, "Every shaded point is within L of that circle.", 18, anchor="middle"),
         text(360, Y0+UNIT+104, "Shrink K and the whole shadow closes in on the circle.", 21, anchor="middle", weight=600)]
svg("interface-shadow.svg", int(Y0+UNIT+126), "The straddle region of a short interface hugs the unit circle",
    f"A centre x with its unit circle drawn dashed in blue. A short segment K of length {L} (exaggerated) leaves x to the east. The shaded region Delta(K) is a crescent just outside the circle on the east side and a matching crescent just inside the circle on the west side, each at most {L} thick; both thin out toward north and south, where the inner crescent reaches slightly past north and south onto the east side. Every shaded point is within distance {L} of the unit circle.", parts)

print("Built interface-model.svg, interface-shadow.svg")

# ------------------------------------------------- Figure C: two interfaces in a 40-degree cone
UNIT = 180.0; L = 0.3; HALF_ANG = math.radians(20)
X0, Y0 = 330.0, 300.0
ends = [(X0+L*UNIT*math.cos(s*HALF_ANG), Y0-L*UNIT*math.sin(s*HALF_ANG)) for s in (1, -1)]
d1, d2 = straddle_path((X0,Y0), ends[0], UNIT), straddle_path((X0,Y0), ends[1], UNIT)
defs = f'<clipPath id="clip2"><path d="{d2}" clip-rule="evenodd"/></clipPath>'
parts = [text(360,44,"Two interfaces in a 40° cone",28,anchor="middle",weight=600),
         text(360,78,"Six labels. K₁ excludes {1,2} and K₂ excludes {3,4}. L = 0.3, exaggerated.",21,anchor="middle"),
         f'<path d="{d1}" fill="{PALE_BLUE}" fill-rule="evenodd" stroke="{BLUE}" stroke-width="1" opacity="0.9"/>',
         f'<path d="{d2}" fill="{PALE_GREEN}" fill-rule="evenodd" stroke="{GREEN}" stroke-width="1" opacity="0.9"/>',
         f'<path d="{d1}" fill="#e59a91" fill-rule="evenodd" clip-path="url(#clip2)"/>',
         f'<circle cx="{X0:.2f}" cy="{Y0:.2f}" r="{UNIT:.2f}" fill="none" stroke="{INK}" stroke-width="1.5" stroke-dasharray="7 6"/>',
         line(X0, Y0, *ends[0], BLUE, 5), line(X0, Y0, *ends[1], GREEN, 5), dot(X0, Y0, INK, 6),
         text(X0-10, Y0+6, "x", 24, anchor="end", weight=600),
         text(ends[0][0]+6, ends[0][1]-6, "K₁", 21, fill=BLUE, weight=600),
         text(ends[1][0]+6, ends[1][1]+20, "K₂", 21, fill=GREEN, weight=600),
         text(X0+UNIT+L*UNIT+22, Y0-8, "both straddle", 18, fill=RED, weight=600),
         text(X0+UNIT+L*UNIT+22, Y0+14, "regions:", 18, fill=RED, weight=600),
         text(X0+UNIT+L*UNIT+22, Y0+36, "only 5, 6 left", 18, fill=RED, weight=600),
         text(360, Y0+UNIT+44, "Blue: Δ(K₁), no 1 or 2.  Green: Δ(K₂), no 3 or 4.  Red: in both.", 18, anchor="middle"),
         text(360, Y0+UNIT+70, "Red hugs the dashed circle around x; up to zero area, only 5 and 6 can appear there.", 18, anchor="middle"),
         text(360, Y0+UNIT+104, "CC60 says this configuration cannot occur.", 21, anchor="middle", weight=600)]
svg("interface-cone.svg", int(Y0+UNIT+126), "Two interfaces in a narrow cone leave a long region for the leftover labels",
    "A centre x with its unit circle dashed. Two short segments K1 and K2 of length 0.3 (exaggerated) leave x in directions 20 degrees above and below east, 40 degrees apart. Their straddle regions are shaded blue and green; where they overlap, shaded red, labels 1, 2, 3 and 4 are all excluded, so only labels 5 and 6 could appear. The red overlap is a long thin crescent just outside the circle on the side the segments point to, with a matching crescent inside the circle on the far side.", parts, defs)
print("Built interface-cone.svg")
