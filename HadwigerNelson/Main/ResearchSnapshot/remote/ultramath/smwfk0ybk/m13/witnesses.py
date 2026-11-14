"""Extract one (C1)-(C5) witness for EVERY satisfiable k=6 instance, normalised to c_0 = 0,
and verify each witness from the paper's set definition (no search code used in the check)."""
from itertools import product
import json, sys
sys.path.insert(0,"../../smwfhd5sl/m5")
import interface_csp as m5
from profile2 import sign_word, slivers, first_model

K=6
def check(ell, c, P):
    """Independent check of one palette tuple against (C1)-(C5), from the paper's words."""
    rows = m5.sign_matrix(ell, c)
    U=set(range(ell,K)); T=set(range(ell))
    OI=[]
    for i in range(6):
        pos=set(); neg=set()
        for j in range(ell):
            (pos if rows[i][j]==1 else neg).add(j); (pos if rows[i][j]==1 else neg).add((j+1)%ell)
        OI.append(((T-pos)|U,(T-neg)|U))
    for i in range(6):
        Pi=set(P[i])
        if not (1 <= len(Pi) <= K-3): return "C1"
        if not (Pi & OI[i][0]) or not (Pi & OI[i][1]): return "C2"
    for i in range(6):
        if set(P[i]) & set(P[(i+1)%6]): return "C3"
    full=set(range(K))
    for a in range(6):
        for b in range(a+1,6):
            if len(P[a])==3 and len(P[b])==3 and set(P[a])|set(P[b])==full: return "C4"
    if sum(1 for p in P if len(p)==3)>3: return "C5"
    return None

out=[]; bad=0
for ell in range(3,K+1):
    for c in product(range(6), repeat=ell):
        if c[0]!=0: continue                      # rotation normalisation
        P=first_model(ell,K,c,True)
        if P is None: continue
        P=[sorted(p) for p in P]
        e=check(ell,c,P)
        if e: bad+=1; print("BAD",ell,c,P,e)
        out.append({"l":ell,"cells":list(c),"palettes":P})
json.dump(out, open("witnesses.json","w"))
print(f"witnesses extracted and re-checked: {len(out)}   failures: {bad}")
from collections import Counter
print("per l:", Counter(w["l"] for w in out))
print("palette sizes:", Counter(tuple(sorted(len(p) for p in w["palettes"])) for w in out))
