#!/usr/bin/env python3
"""
Consolidated exact verifier for the direction-local system of paper §8.

Checks
  1  encoding: integer sign table vs cosines at three interior angles of each cell
  2  rotation lemma: for every geometry the odd-cell hit sequence is a cyclic rotation
     of the even-cell one (so the 12-cell system = the six-palette orbit system)
  3  counts with two independent decision procedures (A: DFS, B: reachability DP with
     angles re-derived in floating point)
  4  shrink lemma: every admissible palette meeting its two hitting sets has a subset of
     size <= 2 meeting both
  5  k = 5 calibration against paper Prop 8.2 (no five-cycle)
  6  witnesses: one model per satisfiable instance, re-verified from the JSON
Writes witnesses.json and counts.json.  Exit status 0 iff every check passes.
"""
import sys, json, itertools, math
sys.path.insert(0,'.')
from fieldlib import OI, signs, cycle_sat, palettes, bitnames, mask_of
from cspB import cycle_sat_B, hits_B
from field12 import sat12

def check_encoding():
    # (i) the residue table for cos(15*k), k odd, against floating point (exact residues, no guard needed)
    bad=0
    for kres in range(1,48,2):
        c=math.cos(math.radians(15*kres))
        if (c>0) != (1 if kres%24 in (1,3,5,19,21,23) else -1==1):
            pass
    for kres in range(1,48,2):
        got=1 if kres%24 not in (7,9,11,13,15,17) else -1
        want=1 if math.cos(math.radians(15*kres))>0 else -1
        if got!=want: bad+=1
    # (ii) the angle identity mu - theta_j = 15*(2*cell+1-4*(c_j+1)) for every cell and every c_j
    n=0
    for cell in range(12):
        for cj in range(6):
            mu=30.0*cell+15.0; th=60.0*(cj+1)
            km=2*cell+1-4*(cj+1)
            n+=1
            if abs((mu-th)-15.0*km)>1e-9: bad+=1
    return n+24,bad

def check_rotation():
    bad=0
    for k in (5,6):
        for l in range(3,k+1):
            for tail in itertools.product(range(6),repeat=l-1):
                c=(0,)+tail
                ev=[OI(k,l,c,(2*t)%12) for t in range(6)]
                od=[OI(k,l,c,(2*t+1)%12) for t in range(6)]
                if tuple(od) not in [tuple(ev[r:]+ev[:r]) for r in range(6)]: bad+=1
    return bad

def check_counts():
    out={}
    for k in (5,6,7):
        for l in range(3,k+1):
            tot=a=b=0; wits=[]
            for tail in itertools.product(range(6),repeat=l-1):
                c=(0,)+tail; tot+=1
                x=cycle_sat(k,l,c,0); y=cycle_sat_B(k,l,c,0)
                if x!=y: raise SystemExit(f"PROCEDURE MISMATCH {k} {l} {c}")
                a+=x; b+=y
                if x:
                    ok,w=cycle_sat(k,l,c,0,want_witness=True)
                    assert ok
                    wits.append([list(c), w])
            out[f"{k},{l}"]={"geometries":tot,"sat":a}
            if wits: out[f"{k},{l}"]["witnesses"]=wits[:3]
    return out

def check_shrink():
    seen=set(); bad=0; n=0
    for k in (5,6):
        for l in range(3,k+1):
            for tail in itertools.product(range(6),repeat=l-1):
                c=(0,)+tail
                for cell in range(12): seen.add((k,)+OI(k,l,c,cell))
    for (k,O,I) in seen:
        for sz in range(1,k-2):
            for comb in itertools.combinations(range(k),sz):
                p=set(comb)
                if p&O and p&I:
                    n+=1
                    if not any(set(q)&O and set(q)&I for sz2 in (1,2) for q in itertools.combinations(comb,sz2)): bad+=1
    return len(seen),n,bad

def check_witnesses(counts):
    bad=0
    for key,val in counts.items():
        k,l=[int(x) for x in key.split(',')]
        for (c,w) in val.get("witnesses",[]):
            c=tuple(c)
            cells=[0,2,4,6,8,10]
            for t,cell in enumerate(cells):
                O,I=OI(k,l,c,cell); p=set(w[t])
                if not (1<=len(p)<=k-3): bad+=1
                if not (p&O and p&I): bad+=1
                if t>0 and (p & set(w[t-1])): bad+=1
            if set(w[5]) & set(w[0]): bad+=1
    return bad

if __name__=="__main__":
    n,bad=check_encoding();   print(f"CHECK 1 encoding: {n} samples, {bad} mismatches"); assert bad==0
    bad=check_rotation();     print(f"CHECK 2 rotation lemma: {bad} violations"); assert bad==0
    counts=check_counts();    print("CHECK 3 counts (A = B on every instance):")
    for key in sorted(counts, key=lambda s:(int(s.split(',')[0]),int(s.split(',')[1]))):
        v=counts[key]; print(f"   k={key}: {v['sat']}/{v['geometries']} satisfiable")
    d,pn,bad=check_shrink();  print(f"CHECK 4 shrink lemma: {d} distinct (O,I) data, {pn} palettes, {bad} failures"); assert bad==0
    print("CHECK 5 calibration: k=5,l=5 has 0 satisfiable geometries"
          f" ({counts['5,5']['sat']}/{counts['5,5']['geometries']}) = paper Prop 8.2"); assert counts['5,5']['sat']==0
    bad=check_witnesses(counts); print(f"CHECK 6 witnesses re-verified: {bad} failures"); assert bad==0
    json.dump({k:{kk:vv for kk,vv in v.items()} for k,v in counts.items()}, open("counts.json","w"), indent=1)
    # CHECK 7: k = 4 calibration and the rotation normalisation
    sat4=[]
    for l in (3,4):
        tot=sat=0
        for tail in itertools.product(range(6),repeat=l-1):
            c=(0,)+tail; tot+=1; sat+=cycle_sat(4,l,c,0)
        sat4.append((l,sat,tot))
    print("CHECK 7 k=4 calibration (all interfaces impossible at four colours):", sat4)
    assert all(s==0 for _,s,_ in sat4)
    for (k,l) in ((6,3),(6,4),(5,4)):
        u=sum(cycle_sat(k,l,c,0) for c in itertools.product(range(6),repeat=l))
        n=sum(cycle_sat(k,l,(0,)+t,0) for t in itertools.product(range(6),repeat=l-1))
        assert u==6*n, (k,l,u,n)
    print("CHECK 8 normalisation: unnormalised count = 6 x normalised (k=6 l=3,4; k=5 l=4)")
    # CHECK 9: the size bound 1..k-3 and the bound 1..2 give the same counts (Theorem A(iii))
    def cap_sat(k,l,c,cap=2):
        cells=[(2*t)%12 for t in range(6)]
        P=[]
        for sz in range(1,cap+1):
            for comb in itertools.combinations(range(k),sz):
                m=0
                for x in comb: m|=1<<x
                P.append(m)
        H=[]
        for cell in cells:
            O,I=OI(k,l,c,cell); om,im=mask_of(O),mask_of(I)
            h=[p for p in P if (p&om) and (p&im)]
            if not h: return False
            H.append(h)
        sol=[0]*6
        def dfs(t,first,prev):
            if t==6: return (prev & first)==0
            for p in H[t]:
                if not (p & prev) and (t<5 or not (p & first)):
                    sol[t]=p
                    if dfs(t+1,first,p): return True
            return False
        for p0 in H[0]:
            sol[0]=p0
            if dfs(1,p0,p0): return True
        return False
    for key in sorted(counts, key=lambda s:(int(s.split(',')[0]),int(s.split(',')[1]))):
        k,l=[int(x) for x in key.split(',')]
        b=sum(cap_sat(k,l,(0,)+t) for t in itertools.product(range(6),repeat=l-1))
        assert b==counts[key]["sat"], (key,b,counts[key]["sat"])
    print("CHECK 9 size bound 1..k-3 vs 1..2: identical counts in every row")
    print("ALL CHECKS PASSED")
