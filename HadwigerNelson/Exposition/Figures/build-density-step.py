"""Build the three static Lesson 2 figures (the density step, Sections 11-12).
Run with Python 3 only; no Pillow, network or browser is needed.
Companion to build-weak-colouring.py and drawn in the same style and palette.
Geometry is to scale: one unit = 360 px, so the radius h and the angle h (radians)
are the same number, exactly as in the lesson.
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
UNIT = 360.0

def text(x, y, value, size=26, fill=INK, anchor="start", weight=400):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{value}</text>'

def line(x1,y1,x2,y2,stroke=INK,width=3,extra=""):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{width}" {extra}/>'

def dot(x,y,fill=RED,r=7):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="2"/>'

def disk(x,y,r,fill=PALE_BLUE,stroke=GREY,width=3,extra=""):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" {extra}/>'

def speck(x,y,r=3):
    # a non-colour-i speck; colour i is drawn pale blue, everything else red
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{RED}"/>'

def arrow(x1,y1,x2,y2,stroke=INK,width=3):
    ang=math.atan2(y2-y1,x2-x1); L=12
    hx=[x2-L*math.cos(ang+a) for a in (0.45,-0.45)]
    hy=[y2-L*math.sin(ang+a) for a in (0.45,-0.45)]
    return (line(x1,y1,x2,y2,stroke,width)+
            f'<polygon points="{x2:.1f},{y2:.1f} {hx[0]:.1f},{hy[0]:.1f} {hx[1]:.1f},{hy[1]:.1f}" fill="{stroke}"/>')

def svg(name, h, title, desc, parts):
    body = "\n".join(parts)
    (OUT/name).write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="720" height="{h}" viewBox="0 0 720 {h}" role="img" aria-labelledby="title desc">\n'
        f'<title id="title">{title}</title><desc id="desc">{desc}</desc>\n'
        f'<rect width="720" height="{h}" fill="white"/>\n'
        '<g font-family="Segoe UI, Arial, sans-serif">\n'+body+'\n</g></svg>\n',encoding="utf-8")

def legend(y, note="not colour i (at most 1% of each disk)", x0=150):
    return [f'<rect x="{x0}" y="{y-16}" width="22" height="22" fill="{PALE_BLUE}" stroke="{GREY}" stroke-width="2"/>',
            text(x0+32,y+2,"colour i",23),
            speck(x0+150,y-5,5),
            text(x0+164,y+2,note,23)]

# ---------------------------------------------------------------- Figure A: slide
H=70.0
ax,ay=180.0,215.0
bx,by=ax+UNIT,ay
starts=[(0,0),(-38,28),(30,-44),(-22,-52),(44,22),(8,50)]
parts=[text(360,46,"Slide the ruler along u₀",31,anchor="middle",weight=600),
       text(360,84,"Every start in B(a,h) lands in B(b,h), the same disk slid one unit.",24,anchor="middle"),
       disk(ax,ay,H),disk(bx,by,H),
       speck(ax-50,ay+40),speck(ax+20,ay-55),speck(ax+55,ay+12),
       speck(bx+48,by-38),speck(bx-30,by+52),speck(bx-58,by-10)]
for dx,dy in starts:
    parts+=[line(ax+dx,ay+dy,bx+dx,by+dy,INK,3 if (dx,dy)!=(0,0) else 6),
            dot(ax+dx,ay+dy,BLUE,5 if (dx,dy)!=(0,0) else 7),dot(bx+dx,by+dy,BLUE,5 if (dx,dy)!=(0,0) else 7)]
parts+=[arrow(ax,ay-H-22,ax+90,ay-H-22,INK,3),text(ax+100,ay-H-14,"u₀",26),
        text(ax-10,ay+30,"a",27,weight=600),text(bx-10,by+30,"b",27,weight=600),
        text(ax,ay+H+34,"B(a,h)",25,anchor="middle"),text(bx,by+H+34,"B(b,h)",25,anchor="middle"),
        text(360,ay+H+34,"length 1",24,anchor="middle"),
        text(360,352,"In this one direction, most starts give a bad ruler.",25,anchor="middle",weight=600)]
parts+=legend(428,"not colour i (a small share of each disk)",x0=110)
svg("density-slide.svg",450,"Slide the ruler along u-zero",
    "Two disks of radius h, one centred at a and one at b, one unit apart. Six parallel unit rulers start inside the left disk and point in the direction u-zero; each endpoint lands inside the right disk at the same offset. Both disks are mostly colour i with a few specks of other colours.",parts)

# ---------------------------------------------------------------- Figure B: turn
H=60.0  # radius h in px; angle h in radians is H/UNIT = 1/6
ang_h=H/UNIT
ax,ay=170.0,250.0
bx,by=ax+UNIT,ay
parts=[text(360,46,"Turn slightly: directions within angle h of u₀",30,anchor="middle",weight=600),
       text(360,84,"Start anywhere in B(a,h); turn by at most h radians.",24,anchor="middle"),
       disk(ax,ay,H),
       disk(bx,by,2*H,PALE_BLUE,GREY,3,'stroke-dasharray="10 7"'),
       disk(bx,by,H,"none","#b5c1cf",2),
       speck(ax-40,ay+30),speck(ax+25,ay-42),
       speck(bx+70,by-80),speck(bx-95,by+45),speck(bx+30,by+100),speck(bx-20,by-60)]
# arc of tip travel from the centre start a
n=24
pts=" ".join(f"{ax+UNIT*math.cos(-ang_h+2*ang_h*j/n):.1f},{ay-UNIT*math.sin(-ang_h+2*ang_h*j/n):.1f}" for j in range(n+1))
parts.append(f'<polyline points="{pts}" fill="none" stroke="{GREY}" stroke-width="2" stroke-dasharray="4 4"/>')
fan=[(0,0,0.0),(0,0,ang_h),(0,0,-ang_h),(-32,22,0.5*ang_h),(30,-34,-0.7*ang_h),(20,36,0.85*ang_h),(0,-50,0.15),(5,45,-0.14)]
for dx,dy,t in fan:
    px,py=ax+dx,ay+dy
    qx,qy=px+UNIT*math.cos(t),py-UNIT*math.sin(t)
    main=(dx,dy)==(0,0)
    parts+=[line(px,py,qx,qy,INK,5 if main and t==0 else 2.5),dot(px,py,BLUE,5),dot(qx,qy,BLUE,5)]
parts+=[text(ax-10,ay+H+30,"a",27,weight=600),text(bx-10,by+30,"b",27,weight=600),
        text(ax,ay-H-18,"B(a,h)",24,anchor="middle"),
        text(bx,by+2*H+30,"B(b,2h): radius 2h, area ×4",24,anchor="middle"),
        text(bx+2*H+8,by+8,"2h",23),
        text(300,ay-104,"turn by at most h",22,anchor="middle"),
        text(360,446,"A turn of at most h moves the tip less than h: tips stay within 2h of b.",21,anchor="middle",weight=600)]
parts+=legend(500,"not colour i: ≤ 1% of B(a,h) and ≤ 1% of B(b,2h)",x0=40)
svg("density-turn.svg",524,"Turn the ruler slightly: tips land in a disk of radius two h",
    "The start disk of radius h around a is on the left. A fan of unit rulers leaves it in directions within angle h of u-zero. Their tips spread over a dashed disk of radius two h around b, drawn with the smaller radius-h disk faintly inside it; two tips land outside the small disk but still inside the dashed one, because a start offset and a turn add up. A dashed arc shows how far a tip travels when the ruler turns from one edge of the fan to the other.",parts)

# ---------------------------------------------------------------- Figure C: slices
R=58.0
parts=[text(360,46,"Some failing starts move; their share does not",28,anchor="middle",weight=600),
       text(360,82,"One fan direction per slice; failing starts ≤ 1% + 4% = 5% of B(a,h).",21,anchor="middle")]
rows=[("u₁",-0.1,(-30,-25),(20,-36)),("u₂",0.0,(-30,-25),(20,0)),("u₃",0.1,(-30,-25),(20,36))]
y0=112; rh=136
for k,(name,t,s1,s4) in enumerate(rows):
    y=y0+k*rh; cy=y+rh/2; cx=276.0
    parts+=[f'<rect x="28" y="{y}" width="664" height="{rh-10}" fill="#f7f9fb" stroke="#d6dde6" stroke-width="2"/>',
            text(50,cy+8,f"direction {name}",24,weight=600),
            arrow(60,cy+44,60+54*math.cos(t),cy+44-54*math.sin(t),INK,3),
            disk(cx,cy,R),
            f'<circle cx="{cx+s1[0]:.1f}" cy="{cy+s1[1]:.1f}" r="{0.1*R:.1f}" fill="{RED}"/>',
            f'<circle cx="{cx+s4[0]:.1f}" cy="{cy+s4[1]:.1f}" r="{0.2*R:.1f}" fill="{PALE_RED}" stroke="{RED}" stroke-width="2"/>',
            text(348,cy-14,"start not colour i: ≤ 1% (solid spot)",16),
            text(348,cy+16,"endpoint not colour i, slid back: ≤ 4% (outline)",16),
            text(348,cy+46,"so ≥ 95% of starts give a bad ruler",19,weight=600)]
parts+=[text(360,y0+3*rh+22,"In every direction of the fan, at least 95% of starts give a bad ruler.",21,anchor="middle",weight=600)]
svg("density-slices.svg",y0+3*rh+44,"Direction slices: endpoint failures move, the total failing share stays at most five percent",
    "Three stacked rows, one for each of three directions in the fan. Each row shows the same start disk B(a,h) in colour i with two small failing regions: a solid red spot of area at most one percent for starts that are not colour i, in the same place in every row, and a red-outlined spot of area at most four percent for starts whose endpoint is not colour i, in a different place in each row, shifted straight up or down as the direction changes. Their total share is at most five percent in every row.",parts)
print("Built density-slide.svg, density-turn.svg, density-slices.svg")
