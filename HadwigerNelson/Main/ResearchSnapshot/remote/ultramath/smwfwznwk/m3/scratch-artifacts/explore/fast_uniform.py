import sys
from itertools import combinations
E=[(1<<j)|(1<<((j+1)%6)) for j in range(6)]
def adm(S): return 1<=bin(S).count('1')<=3 and not any(S & e == S for e in E)
Av,Bv,Cv,Dv,Ev = ((1<<1)|(1<<3)),((1<<1)|(1<<4)),((1<<2)|(1<<4)),((1<<2)|(1<<5)),((1<<3)|(1<<5))
def word2m(m):
    W=[Av]*(m-3)+[Bv]*2+[Cv]*(m-3)+[Dv]*2+[Ev]*2
    assert len(W)==2*m, (m,len(W))
    return W
bad=[]
for m in range(6,3001):
    W=word2m(m); n2=2*m
    errs=[]
    for i in range(n2):
        for d in (m-1,m,m+1):
            if W[i] & W[(i+d)%n2]: errs.append((i,d))
    # the 6m word
    W6=[W[i%n2] for i in range(6*m)]; n=6*m
    offs=sorted({(m+k)%n for k in (-1,0,1)}|{(-m+k)%n for k in (-1,0,1)})
    errs6=[(i,j) for i in range(n) for j in offs if W6[i] & W6[(i+j)%n]]
    adm_ok=all(adm(v) and not (v&1) for v in W)
    if errs or errs6 or not adm_ok: bad.append((m,errs[:2],errs6[:2],adm_ok))
print("m=6..3000, reduced-2m and full-6m transport + admissibility:", "ALL OK" if not bad else bad[:5])
print("values used:", [bin(v) for v in (Av,Bv,Cv,Dv,Ev)])
