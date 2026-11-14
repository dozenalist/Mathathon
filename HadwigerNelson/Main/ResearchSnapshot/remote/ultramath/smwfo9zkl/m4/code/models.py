import sys
from field import *
from itertools import product

def key(z): return tuple(z[0])+tuple(z[1])

def model(B, cong=True, orbits=True):
    pts=[]; seen=set()
    rng = range(-B,B+1)
    for a,b,c,d in product(rng,repeat=4):
        if cong and (a-b+c+d) % 4 != 0: continue
        z = from_ints(a,b,c,d)
        cand = orbit(z) if orbits else [z]
        for w in cand:
            k=key(w)
            if k not in seen:
                seen.add(k); pts.append(w)
    return pts

def graph(pts):
    n=len(pts); adj=[set() for _ in range(n)]
    # bucket by real-part buckets for speed: just O(n^2) for small n
    for i in range(n):
        for j in range(i+1,n):
            if is_unit(sub(pts[j],pts[i])):
                adj[i].add(j); adj[j].add(i)
    return adj
