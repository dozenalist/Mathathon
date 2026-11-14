import sys
from pysat.solvers import Solver
from pysat.formula import CNF

def build_cnf(n, adj, k):
    cnf = CNF()
    var = lambda v,c: v*k + c + 1     # v in 0..n-1, c in 0..k-1
    for v in range(n):
        cnf.append([var(v,c) for c in range(k)])
        for c in range(k):
            for c2 in range(c+1,k):
                cnf.append([-var(v,c), -var(v,c2)])
    for v in range(n):
        for w in adj[v]:
            if w>v:
                for c in range(k):
                    cnf.append([-var(v,c), -var(w,c)])
    return cnf, var

def colourable(n, adj, k, solver='glucose3', verbose=False):
    cnf, var = build_cnf(n, adj, k)
    with Solver(name=solver, bootstrap_with=cnf.clauses) as s:
        r = s.solve()
        if r:
            model = s.get_model()
            col = [0]*n
            for v in range(n):
                for c in range(k):
                    if model[var(v,c)-1] > 0:
                        col[v]=c
            return True, col, len(cnf.clauses)
        return False, None, len(cnf.clauses)

def check_colouring(n, adj, col, k):
    for v in range(n):
        if not (0 <= col[v] < k): return False
        for w in adj[v]:
            if col[w]==col[v]: return False
    return True

def clique_number_upper(n, adj, bound=10):
    # simple: find max clique up to bound via networkx
    return None
