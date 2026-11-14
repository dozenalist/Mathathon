"""
Probes: explicit two-centre / multi-centre palette configurations at level k, decided exactly.

Run:  python3 probes.py
Writes probes_out.json with, for every probe: the node list, the edge list of the conflict
graph, its chromatic-number certification (colouring or UNSAT), and the palette model.
"""
import json, random
import sympy as sp
from twocentre import *

# ---------------------------------------------------------------- P1: Moser spindle
def moser_spindle():
    """7 points, all exact in Q(sqrt3, sqrt11); chi = 4 (Moser spindle).
       Built exactly as the paper's Lemma 6.4 configuration: two 'diamonds' (two unit circles
       meeting at a unit-distance pair) sharing one tip, with the two other tips at distance 1.
       The angle between the tips is gamma, cos(gamma) = 5/6 -- the very angle of Lemma 6.4."""
    O = ZERO
    r3 = sp.sqrt(3)
    Q1 = (r3, sp.Integer(0))                      # |OQ1| = sqrt3
    X1 = (r3/2, sp.Rational(1, 2))                # |OX1| = |Q1X1| = 1
    Y1 = (r3/2, sp.Rational(-1, 2))               # |X1Y1| = 1
    #  Q2 = sqrt3 * e^{i gamma},  cos gamma = 5/6, sin gamma = sqrt11/6
    c, s = sp.Rational(5, 6), sp.sqrt(11)/6
    Q2 = (sp.expand(r3*c), sp.expand(r3*s))
    # X2, Y2 = Q2/2 +- i Q2/(2 sqrt3)   (|Q2| = sqrt3, so the two unit-circle intersections
    # are at distance 1 from each other)
    h = (sp.expand(Q2[0]/2), sp.expand(Q2[1]/2))
    perp = (sp.expand(-Q2[1]/(2*r3)), sp.expand(Q2[0]/(2*r3)))
    X2 = cadd(h, perp)
    Y2 = csub(h, perp)
    return [cnode(O), cnode(Q1), cnode(X1), cnode(Y1), cnode(Q2), cnode(X2), cnode(Y2)]

# ---------------------------------------------------------------- P2: Lemma 6.4 gamma-triad
def lemma64_probe():
    """centre x = 0; the six directions e^{i(t+2j pi/3)} and e^{i(t+pi+gamma+2j pi/3)} of
       Lemma 6.4 (with their full R-orbits), and the three points
       z_j = e^{i(t+2j kappa)} + e^{i(t+pi+gamma+2j kappa)},  an equilateral triangle of side 1
       at distance 1/sqrt3 from x.  t is a generic angle: cos t = 3/5, sin t = 4/5."""
    t = pyth_unit(3, 4)
    kap = rot(2)                                   # e^{2 pi i/3}
    g = GAMMA
    nodes = []
    a_dirs, b_dirs = [], []
    for j in range(3):
        a = sequence(t, upow(kap, j))
        b = sequence(t, rot(3), g, upow(kap, j))     # t + pi + gamma + 2j pi/3
        a_dirs.append(a); b_dirs.append(b)
        nodes.append(pnode(ZERO, a))
        nodes.append(pnode(ZERO, b))
        # full R-orbit of each direction (adds the (5.7) sixty-degree exclusions)
        for m in range(1, 6):
            nodes.append(pnode(ZERO, sequence(a, rot(m))))
            nodes.append(pnode(ZERO, sequence(b, rot(m))))
    for j in range(3):
        z = cadd(a_dirs[j], b_dirs[j])
        nodes.append(cnode(z))
    return nodes

def lemma64_points():
    """the three triangle vertices, for the record"""
    t = pyth_unit(3, 4); kap = rot(2)
    out = []
    for j in range(3):
        a = sequence(t, upow(kap, j))
        b = sequence(t, rot(3), GAMMA, upow(kap, j))
        out.append(cadd(a, b))
    return out

# ---------------------------------------------------------------- P3: Lemma 5.5 pair
def lemma55_branches(d_num, d_den, t):
    """exact e^{i alpha_+-} of Lemma 5.5:  y + e^{it} = x + e^{i a+} + e^{i a-},  y = d, x = 0.
       Uses  e^{i a_+-} = (d + e^{it})/2 +- i (d+e^{it}) sqrt(4-rho^2)/(2 rho)."""
    d = sp.Rational(d_num, d_den)
    y = (d, sp.Integer(0))
    w = (sp.expand(y[0] + t[0]), sp.expand(y[1] + t[1]))      # d + e^{it}
    rho2 = sp.expand(w[0]**2 + w[1]**2)
    rho = sp.sqrt(rho2)
    k = sp.sqrt(sp.expand(4 - rho2))/(2*rho)                  # sqrt(1 - rho^2/4)/rho
    half = (sp.expand(w[0]/2), sp.expand(w[1]/2))
    # i*(w * k) = i*(w0+iw1)k = (-w1 k) + i (w0 k)
    tw = (sp.expand(-w[1]*k), sp.expand(w[0]*k))
    ap = cadd(half, tw)
    am = csub(half, tw)
    assert is_zero(dist2(cadd(ap, am), w)), "Lemma 5.5 branch identity failed"
    return y, w, ap, am

def lemma55_probe(dn=1, dd=2, tcs=(3, 4)):
    t = pyth_unit(*tcs)
    y, w, ap, am = lemma55_branches(dn, dd, t)
    x = ZERO
    nodes = []
    # palettes at the far centre y in direction t, and at x in the two branch directions,
    # together with all R-translates (the (5.7) sixty-degree exclusions)
    for m in range(6):
        nodes.append(pnode(y, sequence(t, rot(m))))
        nodes.append(pnode(x, sequence(ap, rot(m))))
        nodes.append(pnode(x, sequence(am, rot(m))))
    return nodes, (y, w, ap, am)

# ---------------------------------------------------------------- P4: hexagonal lattice patch
def hex_patch(R=1):
    nodes = []
    r3 = sp.sqrt(3)
    pts = []
    for i in range(-R, R+1):
        for j in range(-R, R+1):
            p = (sp.Rational(3*i, 2), sp.expand(r3*(sp.Rational(i, 2) + j)))
            pts.append((i, j, p))
    for (i, j, p) in pts:
        nodes.append(cnode(p))
        for m in range(6):
            nodes.append(pnode(p, rot(m)))
    return nodes

# ---------------------------------------------------------------- P5: single-centre 6 palettes
def interface_probe():
    """the six palettes of one cyclic centre, one per orbit direction e^{i(t+k pi/3)}:
       precisely the disjointness half (C1)+(C3) of the m5/m6 interface CSP."""
    t = pyth_unit(3, 4)
    return [pnode(ZERO, sequence(t, rot(m))) for m in range(6)]

# ---------------------------------------------------------------- driver
def chi_of(nodes, kmax=12):
    adj, edges, margin = conflict_graph(nodes)
    out = {}
    for k in range(1, kmax+1):
        ok, col = colourable(nodes, adj, k)
        out[k] = (ok, col)
        if ok:
            break
    return adj, edges, margin, out

def decide(nodes, k, tag, results):
    adj, edges, margin = conflict_graph(nodes)
    okA, model = solve_csp(nodes, adj, k)
    okB, col = colourable(nodes, adj, k)
    rec = dict(probe=tag, k=k, n_nodes=len(nodes),
               n_edges=len(edges), min_separation_margin=margin,
               csp_search=okA, sat_colouring=okB, agree=(okA == okB))
    if okA:
        ok, msg = verify_labelling(nodes, adj, k, model)
        rec['model_verified'] = ok
        rec['model_check'] = msg
        rec['model'] = [sorted(s) for s in model]
        ok2, msg2 = verify_colouring_pullback(nodes, adj, min_map(model))
        rec['min_map_is_proper'] = ok2
        rec['min_map_check'] = msg2
    results.append(rec)
    return rec

if __name__ == '__main__':
    results = []
    probes = []
    M = moser_spindle()
    probes.append(('moser-spindle', M))
    for k in (2, 3, 4, 5, 6):
        r = decide(M, k, 'moser-spindle', results)
        print('moser spindle k=%d : CSP=%s SATcolour=%s agree=%s' %
              (k, r['csp_search'], r['sat_colouring'], r['agree']))
    L = lemma64_probe()
    probes.append(('lemma64-gamma-triad', L))
    for k in (4, 5, 6):
        r = decide(L, k, 'lemma64-gamma-triad', results)
        print('lemma6.4 triad k=%d : CSP=%s SATcolour=%s agree=%s nodes=%d edges=%d' %
              (k, r['csp_search'], r['sat_colouring'], r['agree'], r['n_nodes'], r['n_edges']))
    P, branch = lemma55_probe()
    probes.append(('lemma55-pair-d=1/2', P))
    for k in (4, 5, 6):
        r = decide(P, k, 'lemma55-pair-d=1/2', results)
        print('lemma5.5 pair k=%d : CSP=%s SATcolour=%s agree=%s nodes=%d edges=%d' %
              (k, r['csp_search'], r['sat_colouring'], r['agree'], r['n_nodes'], r['n_edges']))
    H = hex_patch(1)
    probes.append(('hex-patch-R1', H))
    for k in (4, 5, 6):
        r = decide(H, k, 'hex-patch-R1', results)
        print('hex patch k=%d : CSP=%s SATcolour=%s agree=%s nodes=%d edges=%d' %
              (k, r['csp_search'], r['sat_colouring'], r['agree'], r['n_nodes'], r['n_edges']))
    I = interface_probe()
    probes.append(('interface-six-palettes', I))
    for k in (4, 5, 6):
        r = decide(I, k, 'interface-six-palettes', results)
        print('interface six palettes k=%d : CSP=%s SATcolour=%s agree=%s' %
              (k, r['csp_search'], r['sat_colouring'], r['agree']))

    with open('probes_out.json', 'w') as f:
        json.dump(results, f, indent=1)
    print('\nwrote probes_out.json with', len(results), 'records')
