"""Exact arithmetic for the algebraic model used by de Grey / Parts:
   z = (a + b*sqrt(33) + i c*sqrt(3) + i d*sqrt(11)) / 12,  a,b,c,d in Z.
Squared distance between two such points:
   |z-w|^2 = (P + 2*R*sqrt(33)) / 144,   P = da^2+33db^2+3dc^2+11dd^2,  R = da*db+dc*dd.
Hence |z-w| = 1  <=>  R == 0 and P == 144   (exact, integer arithmetic).
"""
from fractions import Fraction

def sqdist_num(d):
    da,db,dc,dd = d
    P = da*da + 33*db*db + 3*dc*dc + 11*dd*dd
    R = da*db + dc*dd
    return P, R

def unit(d):
    P,R = sqdist_num(d)
    return R == 0 and P == 144

def approx(d):
    import math
    da,db,dc,dd = d
    return ((da + db*math.sqrt(33))/12.0, (dc*math.sqrt(3) + dd*math.sqrt(11))/12.0)

def points_box(B, congruence=True):
    pts=[]
    for a in range(-B,B+1):
        for b in range(-B,B+1):
            for c in range(-B,B+1):
                for d in range(-B,B+1):
                    if congruence and (a - b + c + d) % 4 != 0:
                        continue
                    if (a,b,c,d)==(0,0,0,0):
                        pts.append((a,b,c,d))
                    else:
                        pts.append((a,b,c,d))
    return pts

def unit_graph(pts):
    idx = {p:i for i,p in enumerate(pts)}
    n=len(pts)
    adj=[set() for _ in range(n)]
    import itertools
    cols = list(zip(*pts))
    # bucket by first coordinate difference to speed up
    for i in range(n):
        a,b,c,d = pts[i]
        for j in range(i+1,n):
            A,Bc,C,D = pts[j]
            if unit((A-a,Bc-b,C-c,D-d)):
                adj[i].add(j); adj[j].add(i)
    return adj
