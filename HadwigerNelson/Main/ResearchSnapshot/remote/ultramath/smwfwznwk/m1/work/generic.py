"""Generic free-label sector-word CSP: k labels, cycle C_ell, free label f, palette sizes.

Domain: palettes P with |P| in `sizes`, avoiding the free label, and P not contained in any
edge of C_ell (Lemma 6.2 / (6.2)).  Constraints: disjointness at the six transport offsets
+-(m-1), +-m, +-(m+1) mod 6m, plus (5.7) P(e) cap P(Re) = empty (offset +-m, included).

Two independent complete decision procedures:
  decide_dfs  -- exhaustive backtracking with arc consistency and symmetry breaking;
  decide_sat  -- external CaDiCaL on the obvious CNF.
"""
from itertools import combinations, permutations
import subprocess, tempfile, os

def domain(k, ell, free, sizes):
    E=[frozenset((j,(j+1)%ell)) for j in range(ell)]
    out=[]
    for r in sizes:
        for c in combinations([x for x in range(k) if x!=free], r):
            S=frozenset(c)
            if 1<=len(S)<=3 and not any(S<=e for e in E): out.append(S)
    return out

def offsets(m, n=None):
    n = n or 6*m
    return sorted(set((m+kk)%n for kk in (-1,0,1)) | set((-m+kk)%n for kk in (-1,0,1)))

def compat(V):
    return {X:set(Y for Y in V if not (X&Y)) for X in V}

def automorphisms(V):
    """all permutations of the value set preserving the disjointness graph (backtracking)"""
    V=list(V)
    adj={X:frozenset(Y for Y in V if not (X&Y)) for X in V}
    deg={X:len(adj[X]) for X in V}
    order=sorted(V,key=lambda X:-deg[X])
    auts=[]
    img={}
    def bt(pos):
        if pos==len(order):
            auts.append({X:img[X] for X in V}); return
        X=order[pos]
        for Y in V:
            if Y in img.values(): continue
            if deg[Y]!=deg[X]: continue
            ok=True
            for Z in img:
                if (Z in adj[X]) != (img[Z] in adj[Y]): ok=False; break
            if ok:
                img[X]=Y; bt(pos+1); del img[X]
    bt(0)
    return auts

def orbit_reps(V):
    V=list(V)
    auts=automorphisms(V)
    seen=set(); reps=[]
    for X in V:
        if X in seen: continue
        reps.append(X)
        seen |= {p[X] for p in auts}
    return reps

def decide_dfs(k, ell, free, sizes, m, node_count=False):
    V=domain(k,ell,free,sizes); n=6*m
    offs=[o for o in offsets(m,n) if o%n]
    ADJ=compat(V)
    reps=orbit_reps(V)
    best_nodes=0
    for start in reps:
        dom={i:set(V) for i in range(n)}; dom[0]={start}
        nodes=[0]; sols=[]
        def propagate():
            changed=True
            while changed:
                changed=False
                for i in range(n):
                    for o in offs:
                        j=(i+o)%n
                        for X in list(dom[i]):
                            if not (dom[j]&ADJ[X]): dom[i].discard(X); changed=True
                        if not dom[i]: return False
            return True
        def search():
            nodes[0]+=1
            if not propagate(): return
            cand=None
            for i in range(n):
                if len(dom[i])>1 and (cand is None or len(dom[i])<len(dom[cand])): cand=i
            if cand is None:
                sols.append({i:next(iter(dom[i])) for i in range(n)}); return
            saved={i:set(dom[i]) for i in range(n)}
            for X in sorted(dom[cand],key=lambda S:sorted(S)):
                for i in range(n): dom[i]=set(saved[i])
                dom[cand]={X}; search()
                if sols: return
            for i in range(n): dom[i]=set(saved[i])
        search()
        best_nodes=max(best_nodes,nodes[0])
        if sols:
            return True, [sols[0][i] for i in range(n)], best_nodes
    return False, None, best_nodes

def decide_sat(k, ell, free, sizes, m, timeout=600):
    V=domain(k,ell,free,sizes); n=6*m; d=len(V)
    def var(i,v): return i*d+v+1
    cl=[]
    for i in range(n):
        cl.append([var(i,v) for v in range(d)])
        for a,b in combinations(range(d),2): cl.append([-var(i,a),-var(i,b)])
    for o in offsets(m,n):
        if o%n==0: continue
        for i in range(n):
            j=(i+o)%n
            for a in range(d):
                for b in range(d):
                    if V[a]&V[b]: cl.append([-var(i,a),-var(j,b)])
    with tempfile.NamedTemporaryFile('w',suffix='.cnf',delete=False) as f:
        f.write(f"p cnf {n*d} {len(cl)}\n")
        for c in cl: f.write(" ".join(map(str,c))+" 0\n")
        path=f.name
    try:
        r=subprocess.run(['/opt/lean/bin/cadical','-q',path],capture_output=True,text=True,timeout=timeout)
        out=r.stdout
        if 's SATISFIABLE' not in out: return False, None
        lits=set()
        for line in out.splitlines():
            if line.startswith('v '): lits|={int(x) for x in line.split()[1:] if x!='0'}
        word=[V[v] for i in range(n) for v in range(d) if (i*d+v+1) in lits]
        return True, word
    finally:
        os.unlink(path)

def check(k, ell, free, w, m, sizes=(2,3)):
    """direct check of a word against all conditions"""
    n=6*m; V=set(domain(k,ell,free,sizes)); E=[frozenset((j,(j+1)%ell)) for j in range(ell)]
    bad=[]
    if len(w)!=n: bad.append("length")
    for i,S in enumerate(w):
        S=frozenset(S)
        if S not in V: bad.append(f"bad value {sorted(S)} at {i}")
        if free in S: bad.append(f"free label at {i}")
        if any(S<=e for e in E): bad.append(f"(6.2) violated at {i}")
    for o in offsets(m,n):
        if o%n==0: continue
        for i in range(n):
            if w[i]&w[(i+o)%n]: bad.append(f"offset {o} at {i}: {sorted(w[i])} {sorted(w[(i+o)%n])}")
    return bad
