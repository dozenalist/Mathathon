"""Single-centre palette orbit words at k=6 for a cyclic centre. DP over disjointness cycle."""
from itertools import combinations
k=6; FULL=(1<<k)-1
subs=[]
for r in range(1,4):
    for c in combinations(range(k),r):
        m=0
        for i in c: m|=1<<i
        subs.append(m)
def pc(m): return bin(m).count('1')
def subset(m,n): return (m & ~n)==0

def allowed_for_cycle(ell):
    out=[]
    for P in subs:
        ok=True
        for j in range(ell):
            e=(1<<j)|(1<<((j+1)%ell))
            if subset(P,e): ok=False;break
        if ok: out.append(P)
    return out

def words(ell, c2=False, c4=False):
    A=allowed_for_cycle(ell)
    # DP: start w0 in A, build 6 words with w_i & w_{i+1}=0, close w5 & w0 = 0
    res=[]
    adj={a:[b for b in A if not (a&b)] for a in A}
    for w0 in A:
        stack=[(w0,)]
        while stack:
            t=stack.pop()
            if len(t)==6:
                if not (t[5]&w0): res.append(t)
                continue
            for b in adj[t[-1]]:
                stack.append(t+(b,))
    def okc(t):
        if c2 and sum(1 for m in t if pc(m)==3)>3: return False
        if c4:
            for i in range(6):
                for j in range(i+1,6):
                    if t[i]|t[j]==FULL: return False
        return True
    res=[t for t in res if okc(t)]
    return len(A),res

for ell in (3,4,5,6):
    nA,res=words(ell)
    def cnt(c2=False,c4=False):
        return len([t for t in res if (not c2 or sum(1 for m in t if pc(m)==3)<=3) and (not c4 or all((t[i]|t[j])!=FULL for i in range(6) for j in range(i+1,6)))])
    print(f"ell={ell}: |A|={nA} orbit words={len(res)}  +C2={cnt(c2=True)}  +C4={cnt(c4=True)}  +C2C4={cnt(c2=True,c4=True)}")
    if ell==6:
        for t in [t for t in res if sum(1 for m in t if pc(m)==3)<=3][:12]:
            print("   ",[[i for i in range(6) if (m>>i)&1] for m in t])
