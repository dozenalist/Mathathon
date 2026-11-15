"""Build the two static Lesson 5 figures (three centres, Sections 29-30).
Run with Python 3 only; no Pillow, network or browser is needed.
Companion to build-straddle.py and build-interfaces.py, drawn in the same style and palette.
Figure A is to scale (UNIT px per unit length). Figure B is a bookkeeping table.
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
GREY = "#63758a"
PALE_GREY = "#e9edf2"

def text(x, y, value, size=26, fill=INK, anchor="start", weight=400):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{value}</text>'

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

def arc(cx,cy,r,a0,a1,n=120):
    return [(cx+r*math.cos(a0+(a1-a0)*j/n), cy-r*math.sin(a0+(a1-a0)*j/n)) for j in range(n+1)]

def polyline(pts, stroke, width, extra=""):
    return f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x,y in pts)}" fill="none" stroke="{stroke}" stroke-width="{width}" {extra}/>'

# ------------------------------------------------- Figure A: the unit triangle
UNIT = 300.0
X0, Y0 = 190.0, 430.0
rad = math.radians
yb = (X0+UNIT, Y0)                                   # y = x + e^{ib}, b = 0
zd = (X0+UNIT*math.cos(rad(60)), Y0-UNIT*math.sin(rad(60)))   # z = x + e^{id}, d = 60 deg
parts = [text(360,44,"Two support directions 60° apart make a unit triangle",28,anchor="middle",weight=600),
         text(360,78,"b and d lie in the support of the K-state B at the centre x.",21,anchor="middle"),
         polyline(arc(X0,Y0,UNIT,rad(-12),rad(92)), GREY, 2, 'stroke-dasharray="7 6"'),
         polyline(arc(X0,Y0,UNIT,rad(-10),rad(10)), BLUE, 9),
         polyline(arc(X0,Y0,UNIT,rad(50),rad(70)), BLUE, 9),
         polyline(arc(X0,Y0,58,0,rad(60),40), INK, 2),
         text(X0+70, Y0-28, "60°", 20),
         line(X0, Y0, *yb, INK, 3), line(X0, Y0, *zd, INK, 3), line(*yb, *zd, RED, 4),
         dot(X0, Y0, INK, 7), dot(*yb, GREEN, 8), dot(*zd, GREEN, 8),
         text(X0-12, Y0+8, "x", 27, anchor="end", weight=600),
         text(yb[0]+18, yb[1]+8, "y = x + e^{ib}".replace("e^{ib}", "e<tspan dy=\"-10\" font-size=\"16\">ib</tspan><tspan dy=\"10\"></tspan>"), 23, weight=600),
         text(zd[0]+18, zd[1]-4, "z = x + e<tspan dy=\"-10\" font-size=\"16\">id</tspan><tspan dy=\"10\"></tspan>", 23, weight=600),
         text((X0+yb[0])/2, Y0+28, "1", 22, anchor="middle", weight=600),
         text((X0+zd[0])/2-14, (Y0+zd[1])/2, "1", 22, anchor="end", weight=600),
         text((yb[0]+zd[0])/2+16, (yb[1]+zd[1])/2, "1", 22, fill=RED, weight=600),
         text(360, Y0+92, "Thick blue: the support of B, around b = 0° and d = 60°. Dashed: the unit circle of x.", 17, anchor="middle", fill=BLUE),
         text(360, Y0+126, "y and z are one unit apart because b and d are 60° apart.", 21, anchor="middle", weight=600)]
svg("three-centre-triangle.svg", int(Y0+150), "Two support directions 60 degrees apart give three centres one unit apart",
    "Part of the unit circle around a centre x, drawn dashed. Two short thick blue arcs mark the support of a state B, around the directions b = 0 degrees and d = 60 degrees. The points y = x + e^(ib) and z = x + e^(id) lie on the circle. The sides xy and xz are radii of length 1, and the chord yz, drawn in red, also has length 1, so x, y and z form an equilateral triangle with side 1. The 60 degree angle at x is marked.", parts)

# ------------------------------------------------- Figure B: label bookkeeping
CW, CH = 76, 58
GX, GY = 150, 170
LABELS = range(5)
J, K, X = {0, 1}, {2, 3}, 4
defs = (f'<pattern id="hatch" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
        f'<rect width="10" height="10" fill="{PALE_GREY}"/><line x1="0" y1="0" x2="0" y2="10" stroke="{GREY}" stroke-width="3"/></pattern>')
parts = [text(360,44,"The counting step: one leftover label is forced twice",28,anchor="middle",weight=600),
         text(360,78,"Labels 0–4 split as J = {0,1}, K = {2,3}, X = 4.",21,anchor="middle")]
# column brackets
for lab, cols, col in (("J", (0, 1), BLUE), ("K", (2, 3), GREY), ("X", (4, 4), RED)):
    x1 = GX+cols[0]*CW+6; x2 = GX+(cols[1]+1)*CW-6
    parts += [line(x1, GY-34, x2, GY-34, col, 3), line(x1, GY-34, x1, GY-26, col, 3), line(x2, GY-34, x2, GY-26, col, 3),
              text((x1+x2)/2, GY-42, lab, 21, fill=col, anchor="middle", weight=600)]
for c in LABELS:
    parts.append(text(GX+c*CW+CW/2, GY-6, str(c), 20, anchor="middle", fill=GREY))
rows = [("P", "contains J"), ("Q", "disjoint from P,|not inside K"), ("R", "disjoint from P,|not inside K")]
for r_, (name, note) in enumerate(rows):
    y = GY+r_*CH
    parts.append(text(GX-16, y+CH/2+9, name, 26, anchor="end", weight=600))
    for c in LABELS:
        x = GX+c*CW
        if name == "P":
            fill = PALE_BLUE if c in J else "white"
        else:
            fill = "url(#hatch)" if c in K else (PALE_RED if c == X else "white")
        parts.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" fill="{fill}" stroke="{GREY}" stroke-width="1.5"/>')
        if name == "P" and c in J:
            parts.append(text(x+CW/2, y+CH/2+8, "in P", 18, fill=BLUE, anchor="middle", weight=600))
        if name != "P" and c in J:
            parts += [line(x+16, y+12, x+CW-16, y+CH-12, GREY, 3), line(x+CW-16, y+12, x+16, y+CH-12, GREY, 3)]
        if name != "P" and c == X:
            parts.append(text(x+CW/2, y+CH/2+8, "forced", 18, fill=RED, anchor="middle", weight=600))
    ls = note.split("|")
    for k_, ln in enumerate(ls):
        parts.append(text(GX+5*CW+14, y+CH/2+7+(k_-(len(ls)-1)/2)*20, ln, 17, fill=INK))
# highlight column X in rows Q, R
hx = GX+X*CW
parts.append(f'<rect x="{hx-4}" y="{GY+CH-4}" width="{CW+8}" height="{2*CH+8}" fill="none" stroke="{RED}" stroke-width="4" rx="6"/>')
ky = GY+3*CH
parts += [text(GX-16, ky+40, "Key:", 18, anchor="end", fill=GREY),
          line(GX+4, ky+28, GX+22, ky+46, GREY, 3), line(GX+22, ky+28, GX+4, ky+46, GREY, 3),
          text(GX+32, ky+43, "ruled out (in P)", 17),
          f'<rect x="{GX+200}" y="{ky+26}" width="22" height="22" fill="url(#hatch)" stroke="{GREY}"/>',
          text(GX+230, ky+43, "may be present, cannot be the witness", 17),
          text(360, ky+96, "Q and R each need a label outside K. Striking out J leaves only 4,", 19, anchor="middle"),
          text(360, ky+122, "so 4 lies in both Q and R, and they are not disjoint.", 19, anchor="middle", weight=600)]
svg("three-centre-count.svg", int(ky+146), "Each neighbouring palette must contain the one leftover label",
    "A table with rows P, Q and R, one for each of the three palettes at a common direction, and columns for the labels 0 to 4, bracketed as J = {0,1}, K = {2,3} and X = 4. In row P, cells 0 and 1 are filled: P contains J. In rows Q and R, cells 0 and 1 are crossed out because Q and R are disjoint from P, cells 2 and 3 are hatched because labels of K may be present but cannot be the witness outside K, and cell 4 is marked forced. A red box around column 4 in rows Q and R shows that 4 lies in both, so Q and R are not disjoint.", parts, defs)
print("Built three-centre-triangle.svg, three-centre-count.svg")
