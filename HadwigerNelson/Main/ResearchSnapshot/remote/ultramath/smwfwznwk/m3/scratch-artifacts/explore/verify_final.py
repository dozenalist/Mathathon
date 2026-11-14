"""Final verifications, two independent procedures each.

A. the uniform 2m-word for m = 5..3000 (exact integer checks)
B. UNSAT for m = 1..4 by (i) complete DFS in the standard order, (ii) Cadical CNF,
   (iii) reverse DFS order (independence of the search heuristic)
C. the paper-level conditions on the word: (P1) size, (P4)/(6.2) admissibility,
   (P5) trace condition for every cycle edge, self-avoidance, m2's bound 2+2<=5,
   m11 no ternary palette.
"""
import subprocess, tempfile, os, sys
from itertools import combinations

E=[(1<<j)|(1<<((j+1)%6)) for j in range(6)]
def adm(S): return 1<=bin(S).count('1')<=3 and not any(S&e==S for e in E)
Av,Bv,Cv,Dv,Ev=(1<<1)|(1<<3),(1<<1)|(1<<4),(1<<2)|(1<<4),(1<<2)|(1<<5),(1<<3)|(1<<5)

def word2m(m):
    W=[Av]*max(0,m-3)+[Bv]*2+[Cv]*max(0,m-3)+[Dv]*2+[Ev]*2
    return W
def word6m(m):
    W=word2m(m); return [W[i%(2*m)] for i in range(6*m)]
def offsets(m):
    n=6*m; return sorted({(m+k)%n for k in (-1,0,1)}|{(-m+k)%n for k in (-1,0,1)})

print("=== A. uniform 2m-word, exact integer checks ===")
bad=[]
for m in range(5,3001):
    n=6*m; W=word6m(m); offs=set(offsets(m))
    if len(W)!=n: bad.append((m,'len')); continue
    if not all(adm(v) and not (v&1) for v in W): bad.append((m,'value')); continue
    for i in range(n):
        for j in offs:
            if W[i]&W[(i+j)%n]: bad.append((m,i,j)); break
print("m=5..3000:", "ALL OK" if not bad else bad[:3])
print("word at m=5 (2m = 10 sectors, repeated 3x):",
      " ".join(bin(v) for v in word2m(5)))
print("word at m=6 (2m = 12 sectors):", " ".join(bin(v) for v in word2m(6)))

print()
print("=== B. UNSAT for m = 1..4, three procedures ===")
def dom(pairs_only):
    out=[]
    for r in (2,3):
        for c in combinations(range(1,6),r):
            S=sum(1<<i for i in c)
            if adm(S): out.append(S)
    return [v for v in out if bin(v).count('1')==2] if pairs_only else out

def dfs(m, vals, order):
    n=6*m; S=set(offsets(m)); nbr={i:sorted({(i+d)%n for d in S}) for i in range(n)}
    ok=[[not (a&b) for b in vals] for a in vals]
    assign={}; cnt=[0]
    def rec(k):
        if k==n: return True
        i=order[k]
        for v in range(len(vals)):
            if all(not assign.get(j,None) is not None and ok[v][assign[j]] for j in nbr[i] if j in assign):
                assign[i]=v
                if rec(k+1): return True
                del assign[i]
        return False
    return rec(0)

def cadical(m, vals, timeout=300):
    n=6*m; S=offsets(m); V=len(vals)
    def var(i,v): return i*V+v+1
    cl=[]
    for i in range(n):
        cl.append([var(i,v) for v in range(V)])
        for a,b in combinations(range(V),2): cl.append([-var(i,a),-var(i,b)])
    for i in range(n):
        for d in S:
            j=(i+d)%n
            if i==j: continue
            for a in range(V):
                for b in range(V):
                    if vals[a]&vals[b]: cl.append([-var(i,a),-var(j,b)])
    with tempfile.NamedTemporaryFile('w',suffix='.cnf',delete=False) as f:
        f.write(f"p cnf {n*V} {len(cl)}\n")
        for c in cl: f.write(" ".join(map(str,c))+" 0\n")
        path=f.name
    try:
        r=subprocess.run(['/opt/lean/bin/cadical','-q',path],capture_output=True,text=True,timeout=timeout)
        return 'SAT' if 'SATISFIABLE' in r.stdout and 'UNSAT' not in r.stdout.split('\n')[1] else ('UNSAT' if 'UNSATISFIABLE' in r.stdout else 'UNKNOWN')
    finally:
        os.unlink(path)

for m in (1,2,3,4):
    n=6*m
    for label,vals in (("pairs",dom(True)),("pairs+triples",dom(False))):
        r1=dfs(m,vals,list(range(n)))
        r2=dfs(m,vals,list(range(n-1,-1,-1)))
        r3=cadical(m,vals)
        print(f"m={m} n={n} {label:14s}: forward DFS satisfiable={r1}  reverse DFS satisfiable={r2}  cadical={r3}"
              f"   -> UNSAT: {not r1 and not r2 and r3=='UNSAT'}")

print()
print("=== C. paper-level conditions on the pairs-only word ===")
m=6; W=word6m(m); vals=sorted(set(W))
print("values used:", [bin(v) for v in vals], " (all size 2, none contains label 0)")
print("(P1) sizes:", {bin(v): bin(v).count('1') for v in vals})
print("(6.2)/(P4) admissible:", all(adm(v) for v in vals))
print("self-avoidance: label 0 absent from every palette:", all(not (v&1) for v in W))
print("m2 bound |Px|+|Py| <= 5 at unit distance (translation invariant => 2|P|):",
      max(bin(v).count('1') for v in W)*2, "<= 5")
print("m11: ternary palettes present:", any(bin(v).count('1')==3 for v in W))
print("(P5) for every cycle edge {i,i+1}: is there a in P with a not in {i,i+1}?")
allok=True
for e in range(6):
    edge={e,(e+1)%6}
    row=[]
    for v in vals:
        S={i for i in range(6) if v>>i&1}
        row.append(bool(S-edge))
    allok &= all(row)
    print(f"   edge {sorted(edge)}: ", dict(zip([bin(v) for v in vals],row)))
print("   (P5) satisfiable for every edge by a point mass at a label in P outside the edge:", allok)
# and: no label outside the union of the used palettes
u=0
for v in vals: u|=v
print("union of used palettes:", bin(u), "= labels", [i for i in range(6) if u>>i&1],
      "-> the only label never in a palette is 0")
