from itertools import combinations
import sys
E=[(1<<j)|(1<<((j+1)%6)) for j in range(6)]
def adm(S): return 1<=bin(S).count('1')<=3 and not any(S&e==S for e in E)
def dom_in(A):
    out=[]
    for r in (2,3):
        for c in combinations(sorted(A),r):
            S=sum(1<<i for i in c)
            if adm(S): out.append(S)
    return out
def offsets(m):
    n=6*m; return sorted({(m+k)%n for k in (-1,0,1)}|{(-m+k)%n for k in (-1,0,1)})
def decide(m,vals,cap=300000):
    n=6*m; S=set(offsets(m)); nbr={i:sorted({(i+d)%n for d in S}) for i in range(n)}
    ok=[[not(a&b) for b in vals] for a in vals]; assign={}; nodes=[0]
    def rec(k):
        nodes[0]+=1
        if nodes[0]>cap: raise MemoryError
        if k==n: return True
        i=k
        for v in range(len(vals)):
            if all(ok[v][assign[j]] for j in nbr[i] if j in assign):
                assign[i]=v
                if rec(k+1): return True
                del assign[i]
        return False
    try:
        r=rec(0)
    except MemoryError:
        return 'CAP'
    return 'SAT' if r else 'UNSAT'
for size in (4,):
    print(f"=== |A| = {size} (free set size {6-size}) ===", flush=True)
    for A in combinations(range(6),size):
        vals=dom_in(A)
        row=[]
        for m in (5,6,7,9):
            row.append((m,len(vals),decide(m,vals)))
        print("  A=",A," |domain|=",len(vals), row, flush=True)
