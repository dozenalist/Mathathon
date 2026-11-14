"""
Exhaustive sweep of two-centre probes (paper Lemma 5.5 geometry) and of the palette-size
freedom, at k = 4, 5, 6.

Class decided (precisely):
  For every d in D_SET, every free direction t in T_SET and every bound  md in {1,2,3}, the probe
      palette nodes (y, R^m t)          m = 0..5,  y = d        (far centre)
      palette nodes (x, R^m a_+), (x, R^m a_-)   m = 0..5, x = 0 (near centre)
  where a_+- are the two exact branches of Lemma 5.5 with  y + e^{it} = x + e^{i a_+} + e^{i a_-},
  is decided under the label-set CSP with 1 <= |P| <= min(md, k-3) (colour nodes: none).
  Two independent procedures: backtracking over label sets, and Glucose-SAT on k-colourability.
  Every SAT verdict is proof-carrying: the returned labelling is re-verified against the
  exact conflict graph, and min(label set) is re-verified to be a proper colouring.
"""
import json, itertools
import sympy as sp
from twocentre import *
from probes import lemma55_branches, lemma64_probe, interface_probe, moser_spindle

D_SET = [sp.Rational(a, 10) for a in range(1, 10)]          # d = 0.1 .. 0.9
T_SET = [(3, 4), (5, 12), (8, 15), (7, 24), (20, 21), (9, 40)]   # cos t, sin t (Pythagorean)

def two_centre_probe(d, tc):
    t = pyth_unit(*tc)
    y = (d, sp.Integer(0))
    w = (sp.expand(d + t[0]), sp.expand(t[1]))
    rho2 = sp.expand(w[0]**2 + w[1]**2)
    rho = sp.sqrt(rho2)
    kk = sp.sqrt(sp.expand(4 - rho2))/(2*rho)
    half = (sp.expand(w[0]/2), sp.expand(w[1]/2))
    tw = (sp.expand(-w[1]*kk), sp.expand(w[0]*kk))
    ap = cadd(half, tw); am = csub(half, tw)
    assert is_zero(dist2(cadd(ap, am), w)), (d, tc)
    nodes = []
    for m in range(6):
        nodes.append(pnode(y, sequence(t, rot(m))))
        nodes.append(pnode(ZERO, sequence(ap, rot(m))))
        nodes.append(pnode(ZERO, sequence(am, rot(m))))
    return nodes

def decide(nodes, k, md):
    adj, edges, margin = conflict_graph(nodes)
    okA, model = solve_csp(nodes, adj, k, maxdim=md)
    okB, col = colourable(nodes, adj, k)
    rec = dict(n=len(nodes), edges=len(edges), margin=margin, k=k, md=md,
               csp=okA, sat=okB)
    if okA != okB:
        raise RuntimeError("procedures disagree: %s" % rec)
    if okA:
        ok, msg = verify_labelling(nodes, adj, k, model, maxdim=md)
        if not ok:
            raise RuntimeError("model verification failed: " + msg)
        ok2, msg2 = verify_colouring_pullback(nodes, adj, min_map(model))
        if not ok2:
            raise RuntimeError("min-map not proper: " + msg2)
        rec['model'] = [sorted(s) for s in model]
    return rec

def main():
    out = []
    maxchi = {}
    for (d, tc) in itertools.product(D_SET, T_SET):
        nodes = two_centre_probe(d, tc)
        adj, edges, margin = conflict_graph(nodes)
        # exact chromatic number by increasing k
        chi = None
        for k in range(1, 8):
            ok, _ = colourable(nodes, adj, k)
            if ok:
                chi = k; break
        for k in (4, 5, 6):
            for md in (1, 2, 3):
                rec = decide(nodes, k, md)
                rec['d'] = str(d); rec['t'] = tc
                out.append(rec)
        maxchi[(str(d), tc)] = chi
        print('d=%-4s t=%-9s nodes=%2d edges=%3d  chi=%s' % (d, tc, len(nodes), len(edges), chi))
    with open('sweep_out.json', 'w') as f:
        json.dump(out, f, indent=1)
    print('\nmax chi over the sweep:', max(maxchi.values()))
    print('records:', len(out), ' any UNSAT?', any(not r['csp'] for r in out))

if __name__ == '__main__':
    main()
