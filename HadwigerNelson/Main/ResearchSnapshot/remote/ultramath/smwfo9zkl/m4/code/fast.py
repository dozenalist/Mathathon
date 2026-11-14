import sys, math, time
from fractions import Fraction as F
from field import *
from models import model, key

def coords_float(z):
    x,y = z
    def val(t):
        return float(t[0]) + float(t[1])*math.sqrt(3) + float(t[2])*math.sqrt(11) + float(t[3])*math.sqrt(33)
    return val(x), val(y)

def build(pts, tol=1e-6, verify=True):
    n=len(pts)
    xy=[coords_float(p) for p in pts]
    grid={}
    for i,(x,y) in enumerate(xy):
        grid.setdefault((math.floor(x),math.floor(y)),[]).append(i)
    adj=[set() for _ in range(n)]
    for i,(x,y) in enumerate(xy):
        cx,cy=math.floor(x),math.floor(y)
        for dx in (-2,-1,0,1,2):
            for dy in (-2,-1,0,1,2):
                for j in grid.get((cx+dx,cy+dy),()):
                    if j<=i: continue
                    X,Y=xy[j]
                    d=math.hypot(x-X,y-Y)
                    if abs(d-1.0)<tol:
                        if (not verify) or is_unit(sub(pts[j],pts[i])):
                            adj[i].add(j); adj[j].add(i)
    return adj
