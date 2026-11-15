"""Build the Lesson 6 figure (the case fan of Theorem 1.4, Section 33).
Run with Python 3 only; no Pillow, network or browser is needed.
Drawn in the same style and palette as the other lesson figures. A diagram, not to scale.
"""
from pathlib import Path
import math

OUT = Path(__file__).resolve().parent
INK = "#172c43"; RED = "#b33d39"; BLUE = "#235f9d"; GREY = "#63758a"
PALE_RED = "#fbe9e5"; PALE_BLUE = "#e7f0fb"; PALE_GREY = "#eef1f5"

def text(x, y, value, size=20, fill=INK, anchor="middle", weight=400):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{value}</text>'

def box(cx, cy, w, h, lines, fill=PALE_BLUE, stroke=BLUE, bold_first=True, ident=""):
    out = [f'<rect id="{ident}" x="{cx-w/2:.1f}" y="{cy-h/2:.1f}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>']
    n = len(lines)
    for k, ln in enumerate(lines):
        out.append(text(cx, cy + (k-(n-1)/2)*22 + 7, ln, 18, weight=600 if (k == 0 and bold_first) else 400))
    return out

def arrow(x1, y1, x2, y2, label="", ident="", stroke=INK):
    ang = math.atan2(y2-y1, x2-x1); L = 12
    hx = [x2-L*math.cos(ang+a) for a in (0.45, -0.45)]; hy = [y2-L*math.sin(ang+a) for a in (0.45, -0.45)]
    out = [f'<line class="arrow" data-id="{ident}" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="2.5"/>',
           f'<polygon points="{x2:.1f},{y2:.1f} {hx[0]:.1f},{hy[0]:.1f} {hx[1]:.1f},{hy[1]:.1f}" fill="{stroke}"/>']
    if label:
        out.append(text((x1+x2)/2 + (14 if x2 >= x1 else -14), (y1+y2)/2 + 2, label, 17, fill=RED, anchor="start" if x2 >= x1 else "end", weight=600))
    return out

W, H = 720, 560
parts = [text(360, 40, "Every branch ends in the same contradiction", 27, weight=600),
         text(360, 72, "The case fan of Theorem 1.4 (a diagram, not to scale)", 19, fill=GREY)]
parts += box(400, 125, 380, 50, ["Weak measurable five-colouring (assumed)"], PALE_GREY, GREY, ident="assume")
parts += arrow(400, 150, 400, 188, ident="assume-step5")
parts += box(400, 225, 380, 70, ["Step 5: Proposition 7.1", "a cycle of length ℓ ∈ {3, 4, 5}"], ident="step5")
xs = [195, 400, 605]
labs = [("ℓ = 5", ["Proposition 8.2", "six-direction pattern"]),
        ("ℓ = 4", ["Proposition 8.5", "antipodal pairs, parity"]),
        ("ℓ = 3", ["Proposition 8.10", "Moser spindle"])]
for x, (lab, lines) in zip(xs, labs):
    parts += arrow(400, 260, x, 330, lab, ident="step5-branch")
    parts += box(x, 365, 190, 66, lines, ident="branch")
    parts += arrow(x, 398, 400 + (x-400)*0.25, 452, ident="branch-contra")
parts += box(400, 482, 260, 56, ["Contradiction"], PALE_RED, RED, ident="contra")
# grey bracket for the inputs
parts += [f'<path d="M 64 100 L 52 100 L 52 450 L 64 450" fill="none" stroke="{GREY}" stroke-width="2.5"/>',
          f'<text x="38" y="275" font-size="15" fill="{GREY}" text-anchor="middle" transform="rotate(-90 38 275)">steps 1–4 and 6: inputs used inside the branches</text>']
parts.append(text(360, 538, "Step 5 has no fourth outgoing arrow: the three cases are all the cases.", 18, weight=600))
body = "\n".join(parts)
desc = ("A top box, weak measurable five-colouring assumed, has one arrow down to a box for step 5, Proposition 7.1: "
        "a cycle of length 3, 4 or 5. Exactly three arrows leave that box, labelled length 5, length 4 and length 3, to boxes for "
        "Proposition 8.2 (six-direction pattern), Proposition 8.5 (antipodal pairs and parity) and Proposition 8.10 (Moser spindle). "
        "Each of the three has an arrow into one shared box marked contradiction. A grey bracket on the left marks steps 1 to 4 and 6 "
        "as inputs used inside the branches.")
(OUT/"proof-casefan.svg").write_text(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">\n'
    f'<title id="title">Every case of the extracted cycle ends in the same contradiction</title><desc id="desc">{desc}</desc>\n'
    f'<rect width="{W}" height="{H}" fill="white"/>\n<g font-family="Segoe UI, Arial, sans-serif">\n{body}\n</g></svg>\n', encoding="utf-8")
print("Built proof-casefan.svg")
