"""Complete backtracking decision for small m (pairs-only and pairs+triples)."""
import sys
from itertools import combinations
E=[(1<<j)|(1<<((j+1)%6)) for j in range(6)]
def adm(S): return 1<=bin(S).count('1')<=3 and not any(S&e==S for e in E)
def dom(pairs_only, avoid0=True):
    out=[]
    for r in (2,3):
        for c in combinations(range(6),r):
            S=sum(1<<i for i in c)
            if avoid0 and (S&1): continue
            if adm(S): out.append(S)
    return [v for v in out if bin(v).count('1')==2] if pairs_only else out
def offsets(m):
    n=6*m; return sorted({(m+k)%n for k in (-1,0,1)}|{(-m+k)%n for k in (-1,0,1)})
def decide(m, vals, want_count=False, cap=3*10**7):
    n=6*m; S=set(offsets(m))
    adj=[[i for i in range(n) if i!=0 and (i%n) in S]]
    nbr={i:sorted({(i+d)%n for d in S}) for i in range(n)}
    ok=[[not (a&b) for b in vals] for a in vals]
    assign=[-1]*n; nodes=[0]; cnt=[0]
    def dfs(i):
        nodes[0]+=1
        if nodes[0]>cap: raise MemoryError
        if i==n:
            cnt[0]+=1; return not want_count
        for v in range(len(vals)):
            good=True
            for j in nbr[i]:
                if assign[j]>=0 and not ok[v][assign[j]]: good=False; break
            if not good: continue
            assign[i]=v
            stop=dfs(i+1)
            assign[i]=-1
            if stop: return True
        return False
    try:
        sat=dfs(0)
    except MemoryError:
        return ('CAP',None,None)
    return ('SAT' if sat or cnt[0] else 'UNSAT', nodes[0], cnt[0])
P=dom(True); W=dom(False)
print("pairs-only domain", [bin(v) for v in P])
for m in (1,2,3,4,5,6):
    for label,vals in (("pairs",P),("pairs+triples",W)):
        st,nodes,cnt=decide(m,vals)
        print(f"m={m} n={6*m} {label:14s}: {st}  nodes={nodes} sols={cnt}")
