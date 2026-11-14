import sys, itertools, math
from field import *
from fast import build, coords_float
from colour import colourable, check_colouring

ONE_C = (ONE, ZERO)
ZC = (ZERO, ZERO)
U = ((F(0),F(0),F(0),F(1,6)), (F(0),F(1,6),F(0),F(0)))   # (sqrt33 + i sqrt3)/6, |U|=1

def key(z): return tuple(z[0])+tuple(z[1])

def powvec(u,n):
    out=[ONE_C]; cur=ONE_C
    for _ in range(n-1):
        cur=mul(cur,u); out.append(cur)
    return out

def get_vecs():
    rot6=[ONE_C]
    for _ in range(5): rot6.append(rot(rot6[-1]))
    Uc=(U[0],Kneg(U[1]))
    up=powvec(U,3); um=powvec(Uc,3)
    vecs={}
    for i in range(6):
        for j in (-2,-1,0,1,2):
            base = up[j] if j>=0 else um[-j]
            v=mul(rot6[i],base)
            vecs[key(v)]=v
    return list(vecs.values())

def sumset(vecs, k):
    out={}
    for comb in itertools.combinations_with_replacement(range(len(vecs)), k):
        z=ZC
        for i in comb: z=add(z,vecs[i])
        out[key(z)]=z
    return list(out.values())

def ball(pts, R, tol=1e-9):
    res=[]
    for p in pts:
        x,y=coords_float(p)
        if math.hypot(x,y) <= R+tol: res.append(p)
    return res
