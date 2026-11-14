from itertools import product
# (P1) w(k+1)!=w(k); (P2) w(k+1) not in {w(k), w(k+2)}  on Z/6, values in an m-set
def words(m):
    out=[]
    for w in product(range(m), repeat=6):
        ok=True
        for k in range(6):
            a,b,c=w[k],w[(k+1)%6],w[(k+2)%6]
            if b==a: ok=False;break
            if b==c: ok=False;break
        if ok: out.append(w)
    return out
for m in (2,3,4):
    W=words(m)
    full=[w for w in W if len(set(w))==m]
    print("m=",m,"total",len(W),"using all",len(full), "check (m-1)^6+(m-1)",(m-1)**6+(m-1))
W=words(3)
from collections import Counter
c=Counter()
for w in W:
    if len(set(w))<3: c[w]+=1
two=[w for w in W if len(set(w))==2]
print("2-valued words inside 3 labels:",two)
# period structure of 2-valued
for w in two:
    print(w, [w[k]==w[(k+2)%6] for k in range(6)])
