"""
Diagnostic: isolate the exact non-pointwise input of paper Lemma 6.4 at k = 5 and k = 6.

Lemma 6.4 fixes gamma with cos gamma = 5/6 and forms
    z_j = x + e^{i(t+2j kappa)} + e^{i(t+pi+gamma+2j kappa)} ,  j = 0,1,2,
an equilateral triangle of side 1 at distance 1/sqrt3 from x whose two summand directions carry
OPPOSITE STATES: the state at a_j = t+2j kappa is a singleton {X}, the state at
b_j = t+pi+gamma+2j kappa is a fixed pair D.  (5.2) then gives  colour(z_j) not in
P_x(a_j) U P_x(b_j), and the three vertices are pairwise at distance 1.

The pullback part of this argument is ONLY:
    colour(z_j) not in P_x(a_j) U P_x(b_j)      (a (5.2) instance: |z_j - x - a_j| = 1)
    z_j, z_l at distance 1                       (properness)
Both are instances of  |pi(u) - pi(v)| = 1.  The two *state* inputs are NOT: they are
CONTAINMENT facts  {X} <= P_x(a_j)  and  D <= P_x(b_j)  together with the size bound, and
they come from Definition 5.1 (essential supports of traces) plus the measure-theoretic
transition data, not from any exclusion.

This script decides the two versions and reports, for each k and each palette size bound, the
exact verdict.  It is a diagnostic (the containment constraints are hypotheses, not theorems
about colourings) -- it locates the k-dependence of Lemma 6.4, it does not prove a lower bound.
"""
import itertools, json
import sympy as sp
from twocentre import *

def triad_nodes():
    t = pyth_unit(3, 4)
    kap = rot(2)                                   # e^{2 pi i/3}
    a, b, z = [], [], []
    for j in range(3):
        aj = sequence(t, upow(kap, j))
        bj = sequence(t, rot(3), GAMMA, upow(kap, j))
        a.append(aj); b.append(bj); z.append(cadd(aj, bj))
    return a, b, z

def build(k, state_mode):
    """state_mode:
         'pullback'      only the two pullback constraints (no state info)
         'state'         + containment  label 0 in P(a_j),  {1,2} <= P(b_j)
         'state+size'    + containment and |P| <= k-3 (already in the domain when md=k-3)"""
    a, b, z = triad_nodes()
    nodes = [pnode(ZERO, aj) for aj in a] + [pnode(ZERO, bj) for bj in b] + [cnode(zz) for zz in z]
    adj, edges, margin = conflict_graph(nodes)
    n = len(nodes)
    extra = {}
    if state_mode != 'pullback':
        extra['contains'] = []
        for j in range(3):
            extra['contains'].append((j, frozenset([0])))               # {X} <= P(a_j)
            extra['contains'].append((3+j, frozenset([1, 2])))          # D <= P(b_j)
    return nodes, adj, edges, margin, extra

def solve_with_containment(nodes, adj, k, md, contains):
    """exact backtracking with containment lower bounds."""
    dom = node_domains(nodes, k, maxdim=md)
    if dom is None:
        return False, None
    n = len(nodes)
    for (v, S) in contains:
        dom[v] = [d for d in dom[v] if S <= d]
        if not dom[v]:
            return False, None
    nb = [[j for j in range(n) if adj[i][j]] for i in range(n)]
    assign = [None]*n
    def rec(done):
        if done == n:
            return True
        best, bestlist = None, None
        for v in range(n):
            if assign[v] is None:
                allowed = [d for d in dom[v]
                           if all(assign[w] is None or not (d & assign[w]) for w in nb[v])]
                if bestlist is None or len(allowed) < len(bestlist):
                    best, bestlist = v, allowed
                if not allowed:
                    break
        if not bestlist:
            return False
        for d in bestlist:
            assign[best] = d
            if rec(done+1):
                return True
            assign[best] = None
        return False
    ok = rec(0)
    return ok, (list(assign) if ok else None)

if __name__ == '__main__':
    out = []
    for k in (5, 6, 7):
        for md in (1, 2, 3):
            if md > k-3:
                continue
            for mode in ('pullback', 'state'):
                nodes, adj, edges, margin, extra = build(k, mode)
                contains = extra.get('contains', [])
                ok, model = solve_with_containment(nodes, adj, k, md, contains)
                # independent check with the colouring formulation + containment as forced labels
                # (containment cannot be expressed as a colouring constraint, so we only
                #  cross-check the pullback-only rows with the SAT solver)
                agree = None
                if mode == 'pullback':
                    okB, _ = colourable(nodes, adj, k)
                    agree = (ok == okB)
                if ok:
                    chk, msg = verify_labelling(nodes, adj, k, model, maxdim=md)
                else:
                    chk, msg = None, 'UNSAT'
                rec = dict(k=k, md=md, mode=mode, edges=len(edges), margin=margin,
                           sat=ok, verified=chk, note=msg,
                           cross_check_agree=agree,
                           model=None if not ok else [sorted(s) for s in model])
                out.append(rec)
                print('k=%d  |P|<=%d  %-9s : SAT=%-5s  %s' % (k, md, mode, ok,
                      ('verified' if chk else ('model check FAILED: '+str(msg))) if ok else 'UNSAT'))
    with open('lemma64_diag.json', 'w') as f:
        json.dump(out, f, indent=1)
