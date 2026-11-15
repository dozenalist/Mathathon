"""Build the three static Lesson 3 figures (the straddle region, Sections 16-17).
Run with Python 3 only; no Pillow, network or browser is needed.
Companion to build-density-step.py and drawn in the same style and palette.
Geometry is to scale in each figure (UNIT px per unit length). Delta(K) is drawn
as a fine polygon approximation of its exact boundary arcs, filled even-odd:
the open radius-1 capsule about K minus the lens where both closed endpoint
disks overlap.
"""
from pathlib import Path
import math

OUT = Path(__file__).resolve().parent
INK = "#172c43"
RED = "#b33d39"
BLUE = "#235f9d"
PALE_RED = "#fbe9e5"
PALE_BLUE = "#e7f0fb"
GREY = "#63758a"

def text(x, y, value, size=26, fill=INK, anchor="start", weight=400):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{value}</text>'

def line(x1,y1,x2,y2,stroke=INK,width=3,extra=""):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{stroke}" stroke-width="{width}" {extra}/>'

def dot(x,y,fill=RED,r=7):
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="2"/>'

def svg(name, h, title, desc, parts):
    body = "\n".join(parts)
    (OUT/name).write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="720" height="{h}" viewBox="0 0 720 {h}" role="img" aria-labelledby="title desc">\n'
        f'<title id="title">{title}</title><desc id="desc">{desc}</desc>\n'
        f'<rect width="720" height="{h}" fill="white"/>\n'
        '<g font-family="Segoe UI, Arial, sans-serif">\n'+body+'\n</g></svg>\n',encoding="utf-8")

def arc(cx,cy,r,a0,a1,n):
    # points on a circle, maths angles (counter-clockwise, y up) mapped to SVG
    return [(cx+r*math.cos(a0+(a1-a0)*j/n), cy-r*math.sin(a0+(a1-a0)*j/n)) for j in range(n+1)]

def poly(pts):
    return "M"+" L".join(f"{x:.2f},{y:.2f}" for x,y in pts)+" Z"

# ---------------------------------------------------------------- Figure A: band
UNIT=230.0; L=0.6; N=720
cx,cy=360.0,340.0
px,qx=cx-L/2*UNIT,cx+L/2*UNIT          # endpoints P (left) and Q (right) of K
capsule=(arc(qx,cy,UNIT,-math.pi/2,math.pi/2,N)+arc(px,cy,UNIT,math.pi/2,3*math.pi/2,N))
th=math.atan2(math.sqrt(1-L*L/4),L/2)   # lens corners at (0, +-sqrt(1-L^2/4))
lens=(arc(px,cy,UNIT,-th,th,N)+arc(qx,cy,UNIT,math.pi-th,math.pi+th,N))
parts=[text(360,46,"Many centres thicken a circle into a band",30,anchor="middle",weight=600),
       text(360,82,"Δ(K): some point of K is closer than 1, some point farther than 1.",22,anchor="middle"),
       f'<path d="{poly(capsule)} {poly(lens)}" fill="{PALE_RED}" fill-rule="evenodd" stroke="{RED}" stroke-width="2.5"/>',
       f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{UNIT:.2f}" fill="none" stroke="{BLUE}" stroke-width="2.5" stroke-dasharray="7 6"/>',
       line(px,cy,qx,cy,INK,6),dot(px,cy,BLUE,7),dot(qx,cy,BLUE,7),dot(cx,cy,BLUE,5),
       text(cx,cy-18,"K",27,anchor="middle",weight=600),
       text(cx,cy+36,f"length L = {L}",20,anchor="middle"),
       text(cx,cy-110,"within 1 of all of K",20,anchor="middle"),
       text(cx,cy-84,"(not in Δ(K))",20,anchor="middle",fill=GREY),
       text(cx-UNIT*1.0,cy+9,"Δ(K)",26,anchor="middle",fill=RED,weight=600).replace("<text ",'<text stroke="white" stroke-width="7" stroke-linejoin="round" paint-order="stroke" '),
       text(cx+UNIT*1.0,cy+9,"Δ(K)",26,anchor="middle",fill=RED,weight=600).replace("<text ",'<text stroke="white" stroke-width="7" stroke-linejoin="round" paint-order="stroke" '),
       text(360,cy+UNIT+42,"Outside the band all of K is at least 1 away; inside the white lens all of K is within 1.",16,anchor="middle"),
       text(360,cy+UNIT+68,"Dashed blue: the unit circle of the midpoint of K. It runs through the band, but alone it has zero area.",16,anchor="middle",fill=BLUE),
       text(360,cy+UNIT+102,"The shaded band Δ(K) has positive area.",22,anchor="middle",weight=600)]
svg("straddle-band.svg",int(cy+UNIT+124),"The straddle region of a short segment is a band with positive area",
    f"A horizontal segment K of length {L}, with its two endpoints marked. The shaded region Delta(K) is the open radius-one capsule around K with the white lens removed where the two closed unit disks centred at the endpoints overlap. It forms a ring, thick to the left and right of K and thin above and below it. The unit circle of the midpoint of K is drawn dashed in blue: it runs through the middle of both thick parts of the band, touching the outer boundary only at the top and bottom. It is one of the circles that sweep the band, and alone it has zero area.",parts)

# ---------------------------------------------------------------- Figure B: contact
UNIT=360.0; YK=0.6                      # K lies on the line at height 0.6 above z
zx,zy=130.0,420.0
k0,k1=0.2,1.05                          # K from x=0.2 (distance 0.632) to x=1.05 (distance 1.209)
lengths=[(0.9,GREY,3),(1.0,RED,5),(1.1,GREY,3)]
ky=zy-YK*UNIT
parts=[text(360,46,"Walking along K, the distance crosses 1",30,anchor="middle",weight=600),
       text(360,82,"Somewhere in between, a ruler from z has length exactly 1.",23,anchor="middle")]
a_c=math.asin(YK)                       # unit circle of z meets K's line here
parts.append(f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x,y in arc(zx,zy,UNIT,a_c-0.35,a_c+0.03,60))}" fill="none" stroke="{GREY}" stroke-width="1.5" stroke-dasharray="6 5"/>')
parts+=[line(zx+k0*UNIT,ky,zx+k1*UNIT,ky,INK,6),
        dot(zx+k0*UNIT,ky,BLUE,6),dot(zx+k1*UNIT,ky,BLUE,6),
        text(zx+k1*UNIT+14,ky+8,"K",27,weight=600)]
for d,col,w in lengths:
    x=math.sqrt(d*d-YK*YK)
    ex,ey=zx+x*UNIT,ky
    parts+=[line(zx,zy,ex,ey,col,w),dot(ex,ey,col if d==1.0 else "white",6)]
    if d==1.0:   # label the contact just above its end on K
        parts.append(text(ex,ky-20,"length exactly 1",21,fill=RED,anchor="middle",weight=600))
    else:        # label the other two rulers part-way along, on their outer sides
        lx,ly=zx+0.6*x*UNIT,zy-0.6*YK*UNIT
        lab,dx,dy,anc={0.9:("0.9 &lt; 1",-14,-4,"end"),1.1:("1.1 &gt; 1",14,16,"start")}[d]
        parts.append(text(lx+dx,ly+dy,lab,21,anchor=anc))
parts+=[dot(zx,zy,INK,7),text(zx-14,zy+8,"z",27,anchor="end",weight=600),
        text(zx+k0*UNIT,ky-20,"closer than 1",19,anchor="middle"),
        text(zx+k1*UNIT-20,ky+34,"farther than 1",19,anchor="start"),
        text(zx+UNIT*math.cos(a_c-0.35)+10,zy-UNIT*math.sin(a_c-0.35)+20,"dashed: unit circle of z",18,fill=GREY),
        text(360,zy+56,"No jump is possible, so the walk meets the unit circle of z.",22,anchor="middle",weight=600)]
svg("straddle-contact.svg",int(zy+80),"Walking along a segment, the distance to z passes through exactly 1",
    "A point z at the lower left and a horizontal segment K above it. One end of K is closer than 1 to z and the other is farther. Three rulers run from z to points of K, of lengths 0.9, exactly 1 (highlighted) and 1.1. A dashed arc of the unit circle around z crosses K at the end of the highlighted ruler.",parts)

# ---------------------------------------------------------------- Figure C: gap
UNIT=240.0
ax_,bx_,y=120.0,600.0,250.0
mx=(ax_+bx_)/2
parts=[text(360,46,"Without connectedness, the distance can jump",30,anchor="middle",weight=600),
       text(360,82,"K is only the two endpoints; the middle of the segment is missing.",23,anchor="middle"),
       line(ax_,y,bx_,y,GREY,3,'stroke-dasharray="10 8"'),
       f'<polyline points="{" ".join(f"{x:.2f},{yy:.2f}" for x,yy in arc(ax_,y,UNIT,-0.1,0.45,60))}" fill="none" stroke="{GREY}" stroke-width="1.5" stroke-dasharray="6 5"/>',
       f'<circle cx="{mx:.2f}" cy="{y:.2f}" r="10" fill="white" stroke="{RED}" stroke-width="3" stroke-dasharray="4 3"/>',
       text(mx,y+46,"missing contact",21,anchor="middle",fill=RED,weight=600),
       text(mx,y+72,"(distance 1, not in K)",19,anchor="middle",fill=RED),
       dot(ax_,y,BLUE,8),dot(bx_,y,BLUE,8),
       text(ax_,y-26,"z = first point of K",21,anchor="middle",weight=600),
       text(ax_,y+46,"distance 0",21,anchor="middle"),
       text(bx_,y-26,"second point of K",21,anchor="middle",weight=600),
       text(bx_,y+46,"distance 2",21,anchor="middle"),
       text(mx,y-120,"dashed arc: unit circle of z",18,anchor="middle",fill=GREY),
       text(360,y+128,"0 &lt; 1 &lt; 2, yet no point of K is exactly one unit from z.",22,anchor="middle",weight=600)]
svg("straddle-gap.svg",int(y+152),"Two separate points: the distance jumps from 0 to 2 and skips 1",
    "Two points of K, two units apart, joined by a dashed line showing the missing middle of the segment. The left point is z itself, at distance 0; the right point is at distance 2. The midpoint, where a dashed arc of the unit circle around z crosses the line, is marked with a dashed red circle as the missing contact: it is at distance 1 from z but does not belong to K.",parts)
print("Built straddle-band.svg, straddle-contact.svg, straddle-gap.svg")
