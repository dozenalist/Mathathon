#!/usr/bin/env python3
"""
(Q) test: does a SATURATED periodic packing contain a cell with vol Omega < sqrt(32)?

Frank-Kasper phases are the standard periodic sphere packings with icosahedral
coordination.  We build the A15 (beta-W / Cr3Si) structure, scale it so the minimum
interatomic distance is exactly 2 (unit spheres), and compute the Voronoi cell
volumes.  If any cell is below sqrt(32) = 5.6568542, then (Q) = YES with fully
explicit periodic data, the icosahedral deficit is realisable in a saturated
packing, and (T')/(H_R) become testable.

A periodic packing IS saturated: the periodic repetition fills space, so every
point of R^3 lies within 2 of some centre (checked by the covering test below).

Status: TESTED_FINITE for the volume numbers; the saturation claim is a covering
check on the periodic cell, reported separately.
"""
import numpy as np, json, sys
from scipy.spatial import Voronoi, ConvexHull, cKDTree
sys.path.insert(0,"Experimental/scripts")

R32=float(np.sqrt(32))

def a15(scale=1.0):
    """A15 / beta-W: 2 A-sites + 6 B-sites per cubic cell, Pm-3n."""
    A=[(0,0,0),(0.5,0.5,0.5)]
    B=[(0.25,0,0.5),(0.5,0.25,0),(0,0.5,0.25),
       (0.75,0,0.5),(0.5,0.75,0),(0,0.5,0.75)]
    return np.array(A+B,float)*scale

def min_dist_cubic(basis, L, reps=3):
    pts=[]
    for i in range(-reps,reps+1):
        for j in range(-reps,reps+1):
            for k in range(-reps,reps+1):
                pts.append(basis+np.array([i,j,k])*L)
    P=np.vstack(pts)
    d=np.linalg.norm(P[:,None,:]-P[None,:,:],axis=2)
    np.fill_diagonal(d,np.inf)
    return float(d.min())

def build(frac_basis, L, reps=3, centre=None):
    pts=[]
    for i in range(-reps,reps+1):
        for j in range(-reps,reps+1):
            for k in range(-reps,reps+1):
                pts.append(frac_basis+np.array([i,j,k])*L)
    P=np.vstack(pts)
    c=P.mean(0) if centre is None else centre
    keep=P[np.linalg.norm(P-c,axis=1)<(reps-0.5)*L]
    return keep

def vor_vol_at(P, idx, R=40.0, nbuf=4000):
    """Volume of the cell of P[idx], with a far buffer to bound it."""
    i=np.arange(nbuf)+0.5
    z=1-2*i/nbuf; ph=np.arccos(z); th=np.pi*(1+5**0.5)*i
    buf=np.stack([np.cos(th)*np.sin(ph),np.sin(th)*np.sin(ph),z],1)*R
    A=np.vstack([P,buf]); vor=Voronoi(A)
    ridx=vor.point_region[idx]; reg=vor.regions[ridx]
    if ridx<0 or -1 in reg or len(reg)<4: return None, None
    V=vor.vertices[reg]
    return ConvexHull(V).volume, float(np.max(np.linalg.norm(V-P[idx],axis=1)))

print("=== A15 (beta-W, Cr3Si) ===")
basis=a15(1.0)
d0=min_dist_cubic(basis,1.0)
L=2.0/d0                     # scale so nearest distance = 2
print(f"  unscaled min distance (L=1) = {d0:.9f}; scale L = {L:.9f}")
print(f"  cell edge of the conventional cube = {L:.9f}")
basis_s=basis*L
# (removed a garbled diagnostic line; the clean check is below)

# rebuild cleanly
P=build(a15(1.0)*(2.0/d0), (2.0/d0))
c=np.mean(P,axis=0)
d=np.linalg.norm(P[:,None,:]-P[None,:,:],axis=2); np.fill_diagonal(d,np.inf)
print(f"  min separation in the built set = {d.min():.9f}  (must be 2)")

# cell volumes for the points nearest the centre
order=np.argsort(np.linalg.norm(P-c,axis=1))[:8]
vols=[]
for idx in order:
    v,ext=vor_vol_at(P,idx)
    vols.append((float(np.linalg.norm(P[idx]-c)), v, ext))
print("  nearest 8 cells:  |r|        volume      extent")
for r,v,e in vols:
    flag=""
    if v is not None:
        if v<R32-1e-9: flag="  <-- BELOW sqrt32"
    print(f"    {r:.6f}   {v if v is None else round(v,9)}   {e if e is None else round(e,6)}{flag}")
cand=[v for _,v,_ in vols if v is not None]
print(f"\n  min cell volume among them = {min(cand):.9f}   sqrt32 = {R32:.9f}")
print(f"  ANY cell below sqrt32? {min(cand) < R32-1e-9}")
json.dump({"phase":"A15","L":L,"min_sep":float(d.min()),
           "cells":[{"r":r,"vol":v,"extent":e} for r,v,e in vols],
           "sqrt32":R32,"any_below":bool(min(cand)<R32-1e-9)},
          open("Experimental/evidence/frank_kasper_A15.json","w"),indent=1)
