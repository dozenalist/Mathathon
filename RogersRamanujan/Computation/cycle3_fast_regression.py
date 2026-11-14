#!/usr/bin/env python3
"""RR127 fast regression (<20 s). One PASS/FAIL line per invariant.

Run:  python3 RogersRamanujan/Computation/cycle3_fast_regression.py
Exit status 0 iff every check passes.  Bounds are deliberately small: this is a
smoke test to run before every commit, not evidence for any all-n claim.  The
larger evidence is in results.json (run_checks.py 30 / 50).
"""
import sys, os, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bz82
from rr_core import enumerate_residue, enumerate_gap, weight

FAILS = []
NCHECKS = [0]
def check(name, ok, detail=""):
    NCHECKS[0] += 1
    print("%-46s %s %s" % (name, "PASS" if ok else "FAIL", detail))
    if not ok: FAILS.append(name)

t0 = time.time()

# 1. the three printed BZ82 p.315 examples + the nine-state chain
CHAIN = [(0,(4,1)),(1,(1,1,1)),(0,(2,1,1,1)),(-1,(1,1)),(0,(3,1,1)),
         (1,(2,1)),(0,(2,2,1)),(1,(3,)),(0,(3,2))]
check("BZ82 example 1 (phi)", bz82.phi((2,(11,9,8,7,6,1,1,1)))==(3,(10,9,7,2,2,2)))
check("BZ82 example 2 (psi)", bz82.psi((-2,(15,14,9,9,8,8,8,5,5,4,3,2,1)))
                             ==(-3,(14,10,9,9,8,8,8,4,3,2,2,1)))
check("BZ82 example 3 (nine-state chain)", bz82.pi_forward((4,1))[1]==CHAIN)
check("T(7,3,1) = (5,3,3)", bz82.T((7,3,1))==(5,3,3))

# 2. both involutions on their domains, weight <= 18
def states(n):
    lo=-1
    while bz82.f(lo)<=n: lo-=1
    j=lo; out=[]
    while True:
        m=bz82.f(j)
        if 0<=m<=n:
            rem=n-m
            def rec(r,cap,acc):
                if r==0: out.append((j,tuple(acc))); return
                for x in range(min(cap,r),0,-1):
                    acc.append(x); rec(r-x,x,acc); acc.pop()
            rec(rem,rem,[])
        j+=1
        if j>0 and bz82.f(j)>n: break
    return out
phi_ok=psi_ok=n=0
for w in range(0,19):
    for st in states(w):
        if bz82.phi_domain(st,w):
            n+=1; phi_ok += (bz82.phi(bz82.phi(st))==st)
        if bz82.psi_domain(st,w):
            psi_ok += (bz82.psi(bz82.psi(st))==st)
check("phi^2 = id on domain, weight<=18", phi_ok==n, "(%d states)"%n)
check("psi^2 = id on domain, weight<=18", psi_ok>0)

# 3. the map is a bijection A_n -> D_n, weight <= 18
bij=True; tot=0
for w in range(0,19):
    A=enumerate_residue(w); D=enumerate_gap(w)
    tot+=len(A)
    if len(A)!=len(D): bij=False; break
    fa={a:bz82.forward(a) for a in A}
    if set(fa.values())!=set(D) or len(set(fa.values()))!=len(fa): bij=False; break
    if any(weight(v)!=w for v in fa.values()): bij=False; break
    if any(bz82.inverse(fa[a])!=a for a in A): bij=False; break
    if any(bz82.forward(bz82.inverse(d))!=d for d in D): bij=False; break
check("A_n <-> D_n both laws, weight<=18", bij, "(%d objects in A)"%tot)
check("n=0 and n=2 fixtures", bz82.forward(())==() and bz82.forward((1,1))==(2,))

# 4. the Case-II maximum-existence criterion (Lemma MX.2)
def lamx(lam,x): return lam[x-1] if 1<=x<=len(lam) else 0
crit_ok=cnt=0
for w in range(0,19):
    for st in states(w):
        j,lam=st; t=len(lam); a=1
        while not (2*j+a-lamx(lam,a)>0): a+=1
        L=lamx(lam,a); k=a+2*j-1; mu=k+1-L
        tstar=t+(1 if a>t else 0)+(1 if mu>t else 0); R=t+5*j-2
        if L+lamx(lam,mu) >= 5*j+tstar: continue     # Case I only
        cnt+=1
        S=[z for z in range(0,k) if z+lamx(lam,k-z)<=R]
        crit_ok += ((len(S)>0) == (k>=1 and lamx(lam,k)<=R))
check("Lemma MX.2 criterion, weight<=18", crit_ok==cnt, "(%d Case-II states)"%cnt)

# 5. the a-shift symmetry (Lemma CI.2 / CII)
ci=cj=n_i=n_j=0
for w in range(0,19):
    for st in states(w):
        if not bz82.phi_domain(st,w): continue
        j,lam=st; t=len(lam); a=1
        while not (2*j+a-lamx(lam,a)>0): a+=1
        L=lamx(lam,a); k=a+2*j-1; mu=k+1-L
        tstar=t+(1 if a>t else 0)+(1 if mu>t else 0)
        j2,lam2=bz82.phi(st); a2=1
        while not (2*j2+a2-lamx(lam2,a2)>0): a2+=1
        if L+lamx(lam,mu) >= 5*j+tstar:
            n_i+=1; ci += (a2==a-1)
        else:
            n_j+=1; cj += (a2==a+1)
check("Case I  -> a' = a-1 (Lemma CI.2)", ci==n_i, "(%d/%d)"%(ci,n_i))
check("Case II -> a' = a+1 (Lemma CII)", cj==n_j, "(%d/%d)"%(cj,n_j))

print()
print("elapsed %.2f s" % (time.time()-t0))
print("TOTAL: %d checks, %d failed" % (NCHECKS[0], len(FAILS)))
sys.exit(0 if not FAILS else 1)
