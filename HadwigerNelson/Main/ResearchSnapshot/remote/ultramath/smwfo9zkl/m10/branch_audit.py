"""
Edge-level audit of the hypothesis of Lemma 5.2(3) that the FIRST summand is a local
diffeomorphism in the angular coordinate (the non-parallelism hypothesis is automatic: a unit
pi-gap forces the two summands to meet at 2pi/3).

For a palette edge (z,f) ~ (x,s) with  z + f = x + s + t, |t| = 1, the constraint (5.3) is
available in orientation "free direction f at z, first summand s at x" provided the branch map
   theta |-> alpha(theta),      alpha + beta = (z - x) + e^{i theta},   alpha(x-side)
has non-zero derivative at theta = arg f.  Swapping the roles of the two nodes gives the second
orientation.  The edge is legitimate iff at least one orientation has a non-degenerate branch.

This script reports, for every edge of every probe used in the report, the minimum over edges of
the maximum over orientations of |d alpha / d theta|  (mpmath, 30 digits, exact geometry from
the probe).
"""
import mpmath as mp
import sympy as sp
from twocentre import *

mp.mp.dps = 30

def cnum(p):
    return mp.mpf(str(sp.N(p[0], 30))) + 1j*mp.mpf(str(sp.N(p[1], 30)))

def branch_deriv(zc, xc, f):
    """|d alpha / d theta| for the two branches, free direction f (unit) at centre zc,
       first summand alpha at centre xc.  Returns (d_plus, d_minus)."""
    base = cnum(zc) - cnum(xc)
    out = []
    for sign in (+1, -1):
        def alpha(theta):
            w = base + mp.e**(1j*theta)
            r = abs(w)
            k = mp.sqrt(1 - r**2/4)/r
            return w/2 + sign*1j*w*k
        th = mp.arg(cnum(f))
        h = mp.mpf('1e-8')
        d = (alpha(th+h) - alpha(th-h))/(2*h)
        out.append(abs(d))
    return tuple(out)

def audit(nodes, adj, verbose=False):
    worst = mp.inf
    worst_edge = None
    par = [pi_of(v) for v in nodes]
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            if not adj[i][j]:
                continue
            if nodes[i][0] != 'p' or nodes[j][0] != 'p':
                continue                    # (5.2)/(properness) need no such hypothesis
            A, B = nodes[i], nodes[j]
            # orientation 1: free direction A's at A's centre, first summand B's at B's centre
            d1 = branch_deriv(A[1], B[1], A[2])
            # orientation 2: the other way round
            d2 = branch_deriv(B[1], A[1], B[2])
            best = max(max(d1), max(d2))
            if best < worst:
                worst, worst_edge = best, (i, j, d1, d2)
    return worst, worst_edge

if __name__ == '__main__':
    import sweep2, probes
    allworst = mp.inf
    for d in sweep2.D_SET:
        for tc in sweep2.T_SET:
            nodes = sweep2.probe(d, tc)
            adj, edges, margin = conflict_graph(nodes)
            w, e = audit(nodes, adj)
            allworst = min(allworst, w)
            print('two-centre d=%-4s t=%-8s edges=%4d  min over edges of max-over-orientation |dalpha/dtheta| = %s'
                  % (d, tc, len(edges), mp.nstr(w, 8)))
    for name, nd in [('moser-spindle', probes.moser_spindle()),
                     ('lemma64-triad', probes.lemma64_probe()),
                     ('lemma55-pair', probes.lemma55_probe()[0]),
                     ('hex-patch', probes.hex_patch(1)),
                     ('interface', probes.interface_probe())]:
        adj, edges, margin = conflict_graph(nd)
        w, e = audit(nd, adj)
        if w < allworst:
            allworst = w
        print('%-15s edges=%4d  worst painter-edge branch derivative = %s'
              % (name, len(edges), mp.nstr(w, 8) if w < mp.inf else 'no palette-palette edge'))
    print('\nglobal minimum =', mp.nstr(allworst, 8), ' (must be > 0 for every edge to be a (5.3) instance)')
