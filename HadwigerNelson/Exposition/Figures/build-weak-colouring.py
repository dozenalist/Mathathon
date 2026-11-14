"""Build the three teaching figures and a paced ruler animation.
Run with Python 3 and Pillow. No network or browser is needed.
The SVGs contain text descriptions; the GIF's static counterpart carries the same lesson.
"""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
W = 720
INK = "#172c43"
RED = "#b33d39"
BLUE = "#235f9d"
PALE_RED = "#fbe9e5"
PALE_BLUE = "#e7f0fb"

def text(x, y, value, size=26, fill=INK, anchor="start", weight=400):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{value}</text>'

def line(x1,y1,x2,y2,stroke=INK,width=3,extra=""):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{width}" {extra}/>'

def dot(x,y,fill=RED,r=7):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="2"/>'

def svg(name, h, title, desc, parts):
    body = "\n".join(parts)
    (OUT/name).write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="720" height="{h}" viewBox="0 0 720 {h}" role="img" aria-labelledby="title desc">\n'
        f'<title id="title">{title}</title><desc id="desc">{desc}</desc>\n'
        f'<rect width="720" height="{h}" fill="white"/>\n'
        '<g font-family="Segoe UI, Arial, sans-serif">\n'+body+'\n</g></svg>\n',encoding="utf-8")

def plane(x,y,w,h,divider):
    return [
        f'<rect x="{x}" y="{y}" width="{divider-x}" height="{h}" fill="{PALE_RED}"/>',
        f'<rect x="{divider}" y="{y}" width="{x+w-divider}" height="{h}" fill="{PALE_BLUE}"/>',
        line(divider,y,divider,y+h,BLUE,2),
        text(x+22,y+36,"RED",23,RED,weight=600),
        text(x+w-22,y+36,"BLUE",23,BLUE,anchor="end",weight=600)]

parts=[text(360,48,"One unit ruler, two outcomes",31,anchor="middle",weight=600)]
for y,p_y,angle,caption,height in [
    (82,208,0,"Point right: different colours. Score 0.",228),
    (328,500,math.pi/2,"Point up: same colour. Score 1.",260)]:
    parts += plane(28,y,664,height,360)
    px,r=300,120
    qx,qy=px+r*math.cos(angle),p_y-r*math.sin(angle)
    parts += [line(px,p_y,qx,qy,INK,6),dot(px,p_y),dot(qx,qy,BLUE if angle==0 else RED),
              text(px-25,p_y+31,"start",24),
              text(qx+16,qy-10,"end",24),
              text(360,y+height-16,caption,26,anchor="middle",weight=600)]
parts += [text(360,634,"The ruler's interior does not enter the test.",25,anchor="middle")]
svg("weak-one-segment.svg",658,"One unit ruler, two outcomes",
    "Red is horizontal coordinate less than zero; blue is zero or greater. Both starts are at minus one half, zero. A unit step right reaches blue and scores zero; a unit step up stays red and scores one.",parts)

cx,cy,r,divider=290,350,170,375
def arc_points(start,end,step=1):
    n=max(1,int((end-start)/step))
    return " ".join(f"{cx+r*math.cos(math.radians(start+(end-start)*j/n)):.2f},{cy-r*math.sin(math.radians(start+(end-start)*j/n)):.2f}" for j in range(n+1))

parts=[text(360,47,"Turn the ruler; keep its start fixed",30,anchor="middle",weight=600),
       text(360,86,"The endpoint travels around the unit circle.",25,anchor="middle")]
parts+=plane(32,116,656,444,divider)
parts += [
    f'<polyline points="{arc_points(60,300)}" fill="none" stroke="{RED}" stroke-width="7"/>',
    f'<polyline points="{arc_points(-60,60)}" fill="none" stroke="{BLUE}" stroke-width="7" stroke-dasharray="12 7"/>']
for a in [-60,60]:
    qx,qy=cx+r*math.cos(math.radians(a)),cy-r*math.sin(math.radians(a))
    parts += [line(cx,cy,qx,qy,"#63758a",2,'stroke-dasharray="5 5"'),dot(qx,qy,BLUE,5)]
parts += [line(cx,cy,cx+r,cy,INK,5),dot(cx,cy),dot(cx+r,cy,BLUE),
          text(cx-14,cy+37,"p",27),text(cx+45,cy-14,"length 1",23),
          text(153,351,"240°",29,RED,weight=600),
          text(499,351,"120°",29,BLUE,weight=600),
          text(360,604,"Solid red: same endpoint colours (240°)",25,anchor="middle"),
          text(360,643,"Dashed blue: different colours (120°)",25,anchor="middle"),
          text(360,698,"Bad fraction = 240° / 360° = 2/3",29,anchor="middle",weight=600)]
svg("weak-turning-ruler.svg",730,"A whole turn has bad fraction two thirds",
    "The pivot is half a unit left of a vertical colour boundary. The unit circle intersects the boundary at angles sixty and three hundred degrees. The solid red arc covers two hundred forty degrees with equal endpoint colours. The dashed blue arc covers one hundred twenty degrees with different endpoint colours.",parts)

parts=[text(360,48,"Move the start; then choose a direction",29,anchor="middle",weight=600),
       text(360,89,"Two independent choices",25,anchor="middle"),
       '<circle cx="220" cy="280" r="132" fill="#f1f5f9" stroke="#63758a" stroke-width="3"/>',
       text(105,278,"disk B",30,weight=600),
       text(108,313,"area |B|",25),
       '<circle cx="295" cy="266" r="7" fill="#172c43"/>',
       line(295,266,495,202,INK,6),
       '<circle cx="495" cy="202" r="7" fill="#172c43"/>',
       text(294,306,"p",27),
       text(510,206,"p + u",27),
       text(366,216,"length 1",24),
       text(360,462,"1. Choose p by area inside B.",27,anchor="middle",weight=600),
       text(360,505,"2. Choose a unit direction independently.",27,anchor="middle",weight=600),
       text(360,555,"The endpoint may lie outside B.",26,anchor="middle")]
svg("weak-observation-window.svg",586,"Average over a bounded observation window",
    "A starting point p is chosen uniformly by area inside a disk B. Independently a unit direction is chosen. The illustrated endpoint p plus u lies outside B, which is allowed. Averaging local angular bad fractions over B gives the bad-pair probability P sub B.",parts)

# Animated guided turn: the colour of the endpoint determines the current score.
# A caption and a discrete score change only at mathematically correct angular intervals.
def font(sz,bold=False):
    candidates=[Path("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"),
                Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")]
    for candidate in candidates:
        if candidate.exists(): return ImageFont.truetype(str(candidate),sz)
    return ImageFont.load_default(size=sz)

def frame(angle,caption,final=False):
    im=Image.new("RGB",(W,730),"white")
    d=ImageDraw.Draw(im)
    def label(x,y,s,sz=26,fill=INK,bold=False,anchor="la"):
        d.text((x,y),s,font=font(sz,bold),fill=fill,anchor=anchor)
    label(360,21,"Hold the start still. Turn the ruler.",30,bold=True,anchor="ma")
    label(360,68,caption,25,anchor="ma")
    d.rectangle((32,116,divider,560),fill=PALE_RED)
    d.rectangle((divider,116,688,560),fill=PALE_BLUE)
    d.line((divider,116,divider,560),fill=BLUE,width=2)
    label(54,130,"RED",23,RED,True)
    label(666,130,"BLUE",23,BLUE,True,"ra")
    # faint full circle; the thick trace records the part of the turn already visited
    d.ellipse((cx-r,cy-r,cx+r,cy+r),outline="#b5c1cf",width=2)
    for a in range(0,int(angle)):
        mid=math.radians(a+.5)
        col=RED if math.cos(mid)<.5 else BLUE
        p1=(cx+r*math.cos(math.radians(a)),cy-r*math.sin(math.radians(a)))
        p2=(cx+r*math.cos(math.radians(a+1)),cy-r*math.sin(math.radians(a+1)))
        d.line((*p1,*p2),fill=col,width=7)
    rad=math.radians(angle)
    qx,qy=cx+r*math.cos(rad),cy-r*math.sin(rad)
    bad=math.cos(rad)<.5-1e-12
    d.line((cx,cy,qx,qy),fill=INK,width=6)
    for x,y,col in [(cx,cy,RED),(qx,qy,RED if bad else BLUE)]:
        d.ellipse((x-8,y-8,x+8,y+8),fill=col,outline=INK,width=2)
    label(cx-10,cy+18,"p",27)
    if final:
        label(360,591,"A full turn: 240° same, 120° different",27,bold=True,anchor="ma")
        label(360,646,"Bad fraction = 2/3",32,bold=True,anchor="ma")
    else:
        label(360,591,"Current score: "+("1 — same colour" if bad else "0 — different colours"),29,bold=True,anchor="ma")
        label(360,643,"The score tests just this one placement.",25,anchor="ma")
    return im

frames=[];durations=[]
def add(a,caption,ms,final=False):
    frames.append(frame(a,caption,final));durations.append(ms)
add(0,"Start red; endpoint blue.",2200)
for start,end in [(0,90),(90,180),(180,360)]:
    for a in range(start+4,end,4):
        add(a,"Watch where the endpoint lands.",70)
    if end==90:add(90,"Point up: both endpoints are red.",2000)
    elif end==180:add(180,"Point left: both endpoints are still red.",2000)
    else:add(360,"Now average over the whole turn.",4000,True)
frames[0].save(OUT/"weak-turning-ruler.gif",save_all=True,append_images=frames[1:],
               duration=durations,loop=0,optimize=True,disposal=2)
print(f"Built 3 SVGs and {len(frames)} GIF frames; duration {sum(durations)/1000:.1f}s.")
