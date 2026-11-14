"""Sweep of exact omega(F) and linear-mod-6 colourings over rational parallelograms.

All arithmetic is Fraction; nothing here uses floating point for a claimed fact
(the only float is a printed diagnostic).
"""
from fractions import Fraction as Fr
from para6 import Para, graph, max_clique, linear_mod6

def omega(a, b):
    para = Para(a, b)
    F = para.forced_set()
    V, adj = graph(F)
    Cl = max_clique(sorted(V), adj)
    return para, F, len(Cl), sorted(Cl), linear_mod6(F)

def row(a, b):
    para, F, w, Cl, sol = omega(a, b)
    print(f"a={tuple(map(str,a))} b={tuple(map(str,b))} |F|={len(F):3d} omega={w:2d} "
          f"lin6={'YES '+str(sol[0]) if sol else 'no ':8s} diam2={para.diam2}")

if __name__ == '__main__':
    print("=== SQUARE family: a=(s,0), b=(0,s), s^2+s^2<1 ===")
    for num, den in [(1,5),(1,4),(2,7),(3,10),(1,3),(7,20),(9,25),(2,5),(19,50),
                     (9,22),(21,50),(11,25),(9,20),(1,2),(3,5)]:
        s = Fr(num, den)
        if 2*s*s >= 1:
            print(f"s={s} skipped (diam^2={2*s*s} not < 1)")
            continue
        row((s, Fr(0)), (Fr(0), s))
    print()
    print("=== RECTANGLE family: a=(s,0), b=(0,t) ===")
    for s, t in [(Fr(1,3),Fr(1,3)),(Fr(1,3),Fr(1,2)),(Fr(1,4),Fr(1,2)),(Fr(1,4),Fr(3,4)),
                 (Fr(2,5),Fr(1,2)),(Fr(1,2),Fr(1,2)),(Fr(1,3),Fr(4,5)),(Fr(1,5),Fr(9,10)),
                 (Fr(1,10),Fr(19,20)),(Fr(1,6),Fr(7,8))]:
        if s*s + t*t >= 1:
            print(f"({s},{t}) skipped: diam^2 = {s*s+t*t} not < 1")
            continue
        row((s, Fr(0)), (Fr(0), t))
    print()
    print("=== slanted parallelograms ===")
    sl = [((Fr(1,3),Fr(0)), (Fr(1,4),Fr(1,4))),
          ((Fr(1,3),Fr(0)), (Fr(1,6),Fr(1,3))),
          ((Fr(2,5),Fr(0)), (Fr(1,5),Fr(1,5))),
          ((Fr(2,5),Fr(0)), (Fr(1,10),Fr(1,2))),
          ((Fr(1,2),Fr(0)), (Fr(1,10),Fr(1,2))),
          ((Fr(1,2),Fr(0)), (Fr(1,4),Fr(2,5))),
          ((Fr(1,4),Fr(0)), (Fr(1,2),Fr(1,4))),
          ((Fr(1,5),Fr(0)), (Fr(3,10),Fr(1,5))),
          ((Fr(3,10),Fr(0)), (Fr(1,5),Fr(1,4))),
          ((Fr(1,3),Fr(1,3)), (Fr(1,3),Fr(-1,3))),   # rhombus, 60 degrees
          ((Fr(1,2),Fr(1,2)), (Fr(1,2),Fr(-1,2))),   # rhombus, 90 -> square
         ]
    for a, b in sl:
        if a[0]*b[1]-a[1]*b[0] == 0:
            print("degenerate", a, b); continue
        d2 = max(a[0]**2+a[1]**2, b[0]**2+b[1]**2,
                 (a[0]+b[0])**2+(a[1]+b[1])**2, (a[0]-b[0])**2+(a[1]-b[1])**2)
        if d2 >= 1:
            print(f"a={a} b={b} skipped: diam^2={d2} not < 1"); continue
        row(a, b)

