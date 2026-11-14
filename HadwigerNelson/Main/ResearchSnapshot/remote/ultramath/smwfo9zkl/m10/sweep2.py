"""
Improved two-centre sweep: for each free direction f in a finite exact set, both branches of
Lemma 5.5 are computed, every direction at every centre is closed under the full 60-degree orbit,
and the (5.2) colour nodes at  x + e + v  (e = a_+(f), v = a_-(f)) are added.

Probe class (stated exactly):
  centres      y = d (real), x = 0
  free dirs    F = { R^m t : m = 0..5 }
  palettes     (y, R^m f)  and  (x, R^m a_+(f)), (x, R^m a_-(f))  for f in F, m = 0..5
  colours      the points y + f  and  a_+(f) + a_-(f) = y + f   (an instance of (5.2) at x)

Every node pair at pi-distance 1 is a conflict (the pullback rule).  Decided at k = 4,5,6 and
for palette size bounds 1, 2, 3 by two independent procedures.
"""
import json, itertools
import sympy as sp
from twocentre import *

D_SET = [sp.Rational(a, 10) for a in range(1, 10)]
T_SET = [(3, 4), (5, 12), (8, 15)]

def branches(d, f):
    """exact e^{i a_+-} with  d + f = e^{i a_+} + e^{i a_-},  f a unit complex number."""
    w = cadd((d, sp.Integer(0)), f)
    rho2 = sp.expand(dist2(w, ZERO))          # |w|^2
    if sp.N(rho2, 30) > 4 or sp.N(rho2, 30) < 1e-20:
        return None
    rho = sp.sqrt(rho2)
    kk = sp.sqrt(sp.expand(4 - rho2))/(2*rho)
    half = (sp.expand(w[0]/2), sp.expand(w[1]/2))
    tw = (sp.expand(-w[1]*kk), sp.expand(w[0]*kk))
    ap, am = cadd(half, tw), csub(half, tw)
    assert is_zero(dist2(cadd(ap, am), w)), (d, f)
    return ap, am

def probe(d, tc):
    t = pyth_unit(*tc)
    y = (d, sp.Integer(0))
    nodes = []
    seen = set()
    def add(n):
        key = (n[0], str(sp.srepr(pi_of(n))))
        if key not in seen:
            seen.add(key); nodes.append(n)
    F = [sequence(t, rot(m)) for m in range(6)]
    for f in F:
        br = branches(d, f)
        if br is None:
            continue
        ap, am = br
        add(cnode(cadd(y, f)))                     # (5.2) at centre x with the two branches
        for m in range(6):
            add(pnode(y, sequence(f, rot(m))))
            add(pnode(ZERO, sequence(ap, rot(m))))
            add(pnode(ZERO, sequence(am, rot(m))))
    return nodes

def decide(nodes, k, md, G=None):
    adj, edges, margin = G if G is not None else conflict_graph(nodes)
    okA, model = solve_csp(nodes, adj, k, maxdim=md)
    okB, col = colourable(nodes, adj, k)
    if okA != okB:
        raise RuntimeError("procedures disagree")
    if okA:
        ok, msg = verify_labelling(nodes, adj, k, model, maxdim=md)
        if not ok:
            raise RuntimeError("model verification failed: " + msg)
        ok2, msg2 = verify_colouring_pullback(nodes, adj, min_map(model))
        if not ok2:
            raise RuntimeError("min-map not proper: " + msg2)
        return okA, [sorted(s) for s in model], len(edges), margin
    return okA, None, len(edges), margin

def main():
    out = []
    chis = []
    for (d, tc) in itertools.product(D_SET, T_SET):
        nodes = probe(d, tc)
        adj, edges, margin = conflict_graph(nodes)
        G = (adj, edges, margin)
        chi = None
        for k in range(1, 9):
            ok, _ = colourable(nodes, adj, k)
            if ok:
                chi = k; break
        chis.append(chi)
        row = []
        for k in (4, 5, 6):
            for md in (1, 2, 3):
                ok, model, ne, mg = decide(nodes, k, md, G)
                out.append(dict(d=str(d), t=tc, k=k, md=md, n=len(nodes), edges=ne,
                                margin=mg, sat=ok, model=model, chi=chi))
                row.append(ok)
        print('d=%-4s t=%-9s nodes=%3d edges=%4d chi=%d  SAT@k=4,5,6 x md=1,2,3: %s'
              % (d, tc, len(nodes), len(edges), chi, row))
    with open('sweep2_out.json', 'w') as f:
        json.dump(out, f, indent=1)
    print('\nmax chi over sweep:', max(chis), '  #UNSAT records:', sum(1 for r in out if not r['sat']))

if __name__ == '__main__':
    main()
