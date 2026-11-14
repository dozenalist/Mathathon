"""
Two-centre palette CSP at k colours -- decision machinery.

Definitions (see REDUCTION.md for the derivation and the citations).

A *probe* is a finite list of nodes.  Each node is one of
    ('c', p)        a COLOUR node at the plane point p      (domain: singletons {i}, i < k)
    ('p', x, e)     a PALETTE node at centre x, unit direction e
                    (domain: nonempty A subset of {0..k-1} with |A| <= k-3)
Write  pi(node) = p                     for a colour node,
       pi(node) = x + e                 for a palette node.

ADJACENCY RULE (the single rule; every constraint of the paper's Section 5 is an instance):
       u ~ w   <=>   |pi(u) - pi(w)| = 1 .
A labelling assigns each node a nonempty label set from its domain; adjacent nodes must get
DISJOINT sets.

THEOREM (min-map / pullback).
   (a) A labelling L of a probe exists iff the conflict graph Pi(probe) is k-colourable:
         => v |-> min L(v) is a proper k-colouring;
         <= v |-> {colour of pi(v)} is a labelling.
   (b) Pi(probe) is the pullback of the plane's unit-distance graph along pi, so it is
       k-colourable iff the unit-distance graph on the finite point set pi(probe) is.
   (c) A proper k-colouring of the plane gives a labelling of EVERY probe
       (v |-> {c(pi(v))}); hence a probe that is not k-colourable certifies chi(R^2) >= k+1.

All geometry is exact sympy arithmetic over Q(sqrt 3, sqrt 11, ...); every adjacency used in a
certificate is re-checked by exact radical arithmetic, and the "accidental edge" side is reported
with its separation margin.
"""
import itertools
import sympy as sp

# ------------------------------------------------------------------ exact plane geometry
def C(re, im=0):
    return (sp.nsimplify(re), sp.nsimplify(im))

def cadd(a, b):  return (sp.expand(a[0] + b[0]), sp.expand(a[1] + b[1]))
def csub(a, b):  return (sp.expand(a[0] - b[0]), sp.expand(a[1] - b[1]))
def cmul(a, b):  return (sp.expand(a[0]*b[0] - a[1]*b[1]), sp.expand(a[0]*b[1] + a[1]*b[0]))
def cconj(a):    return (a[0], -a[1])
ONE = (sp.Integer(1), sp.Integer(0))
ZERO = (sp.Integer(0), sp.Integer(0))

_COS60 = [sp.Integer(1), sp.Rational(1, 2), sp.Rational(-1, 2), sp.Integer(-1),
          sp.Rational(-1, 2), sp.Rational(1, 2)]
_SIN60 = [sp.Integer(0), sp.sqrt(3)/2, sp.sqrt(3)/2, sp.Integer(0),
          -sp.sqrt(3)/2, -sp.sqrt(3)/2]

def rot(k):
    """e^{i k pi/3}"""
    return (_COS60[k % 6], _SIN60[k % 6])

def pyth_unit(num, den):
    """exact unit complex (num + i den)/sqrt(num^2+den^2); requires num^2+den^2 a square."""
    s = sp.sqrt(sp.Integer(num*num + den*den))
    assert s.is_rational, (num, den)
    return (sp.Rational(num, int(s)), sp.Rational(den, int(s)))

# cos(gamma)=5/6, sin(gamma)=sqrt(11)/6 : the angle of paper Lemma 6.4, gamma/pi irrational
GAMMA = (sp.Rational(5, 6), sp.sqrt(11)/6)

def sequence(*us):
    z = ONE
    for u in us:
        z = cmul(z, u)
    return z

def inv_unit(u):
    return cconj(u)

def upow(u, n):
    z = ONE
    for _ in range(abs(n)):
        z = cmul(z, u)
    return z if n >= 0 else cconj(z)

# ------------------------------------------------------------------ exact tests
def _is_zero(e):
    e = sp.expand(e)
    if e == 0:
        return True
    if not e.is_number:
        return False
    v = complex(sp.N(e, 60))
    if abs(v) > 1e-45:
        return False
    try:
        mp = sp.minimal_polynomial(e, sp.Symbol('x'))
        return sp.simplify(mp) == sp.Symbol('x')
    except Exception:
        return abs(v) < 1e-55

def dist2(p, q):
    d = csub(p, q)
    return sp.expand(d[0]*d[0] + d[1]*d[1])

def unit_gap_exact(p, q):
    return _is_zero(sp.expand(dist2(p, q) - 1))

def gap_float(p, q, dps=50):
    return float(sp.N(sp.expand(dist2(p, q) - 1), dps))

# ------------------------------------------------------------------ nodes and conflict graph
def cnode(p):        return ('c', p)
def pnode(x, e):     return ('p', x, e)

def pi_of(v):
    return v[1] if v[0] == 'c' else cadd(v[1], v[2])

def conflict_graph(nodes, margin_report=True, dps=45):
    """adjacency  u ~ w  <=>  |pi(u) - pi(w)| = 1.

    Every pi-value is evaluated once to `dps` decimal digits with mpmath; pair gaps are formed
    in that precision, and any pair whose gap is numerically zero to 1e-25 is then re-checked by
    EXACT radical arithmetic before an edge is emitted.  Non-edges keep a reported separation
    margin, so an accidental edge would show up as a tiny margin."""
    import mpmath as mp
    mp.mp.dps = dps
    n = len(nodes)
    psi = [pi_of(v) for v in nodes]
    num = [(mp.mpf(str(sp.N(p[0], dps))), mp.mpf(str(sp.N(p[1], dps)))) for p in psi]
    adj = [[False]*n for _ in range(n)]
    edges = []
    min_margin = float('inf')
    for i in range(n):
        for j in range(i+1, n):
            dx = num[i][0] - num[j][0]; dy = num[i][1] - num[j][1]
            g = float(dx*dx + dy*dy - 1)
            if abs(g) < 1e-25:
                if not unit_gap_exact(psi[i], psi[j]):
                    raise RuntimeError("unit gap failed exact re-check: %d %d" % (i, j))
                adj[i][j] = adj[j][i] = True
                edges.append((i, j))
            else:
                min_margin = min(min_margin, abs(g))
    if margin_report:
        return adj, edges, min_margin
    return adj, edges

# ------------------------------------------------------------------ domains
def palette_domain(k, maxdim=None):
    hi = k - 3 if maxdim is None else min(maxdim, k - 3)
    if hi < 1:
        return None
    out = []
    for sz in range(1, hi+1):
        out.extend(itertools.combinations(range(k), sz))
    return [frozenset(s) for s in out]

def node_domains(nodes, k, maxdim=None):
    d = palette_domain(k, maxdim)
    if d is None:
        return None
    return [[frozenset([i]) for i in range(k)] if v[0] == 'c' else list(d) for v in nodes]

# ------------------------------------------------------------------ procedure A: exact CSP search
def solve_csp(nodes, adj, k, maxdim=None):
    """backtracking search over label SETS (independent of the colouring formulation)."""
    n = len(nodes)
    dom = node_domains(nodes, k, maxdim)
    if dom is None:
        return False, None
    assign = [None]*n
    nb = [[j for j in range(n) if adj[i][j]] for i in range(n)]

    def rec(done):
        if done == n:
            return True
        best, bestlist = None, None
        for v in range(n):
            if assign[v] is None:
                allowed = []
                for d in dom[v]:
                    ok = True
                    for w in nb[v]:
                        if assign[w] is not None and (d & assign[w]):
                            ok = False
                            break
                    if ok:
                        allowed.append(d)
                if bestlist is None or len(allowed) < len(bestlist):
                    best, bestlist = v, allowed
                if not allowed:
                    break
        if not bestlist:
            return False
        bestlist.sort(key=lambda s: (len(s), tuple(sorted(s))))
        for d in bestlist:
            assign[best] = d
            if rec(done+1):
                return True
            assign[best] = None
        return False

    ok = rec(0)
    return ok, (list(assign) if ok else None)

# ------------------------------------------------------------------ procedure B: k-colouring via SAT
def colourable(nodes, adj, k):
    """decide k-colourability of the conflict graph with Glucose3 (independent code path)."""
    from pysat.solvers import Glucose3
    n = len(nodes)
    if n == 0:
        return True, []
    def var(v, c):     # v in 1..n, c in 0..k-1
        return (v-1)*k + c + 1
    cls = []
    for v in range(1, n+1):
        cls.append([var(v, c) for c in range(k)])
    for v in range(1, n+1):
        for c1 in range(k):
            for c2 in range(c1+1, k):
                cls.append([-var(v, c1), -var(v, c2)])
    for i in range(n):
        for j in range(i+1, n):
            if adj[i][j]:
                for c in range(k):
                    cls.append([-var(i+1, c), -var(j+1, c)])
    with Glucose3(bootstrap_with=cls) as s:
        if not s.solve():
            return False, None
        m = s.get_model()
        val = set(x for x in m if x > 0)
        col = []
        for v in range(1, n+1):
            c = [c for c in range(k) if var(v, c) in val]
            col.append(c[0] if c else None)
        return True, col

# ------------------------------------------------------------------ verifier
def verify_labelling(nodes, adj, k, model, maxdim=None):
    n = len(nodes)
    hi = k-3 if maxdim is None else min(maxdim, k-3)
    for v in range(n):
        s = model[v]
        if not s:
            return False, "node %d: empty label set" % v
        if any(not (0 <= i < k) for i in s):
            return False, "node %d: label out of range" % v
        if nodes[v][0] == 'c':
            if len(s) != 1:
                return False, "node %d: colour node is not a singleton" % v
        else:
            if not (1 <= len(s) <= hi):
                return False, "node %d: palette size %d outside [1,%d]" % (v, len(s), hi)
    for i in range(n):
        for j in range(i+1, n):
            if adj[i][j] and (model[i] & model[j]):
                return False, "adjacent %d,%d share label(s) %s" % (i, j, sorted(model[i] & model[j]))
    return True, "ok"

def min_map(model):
    return [min(s) for s in model]

def verify_colouring_pullback(nodes, adj, colour):
    """the colouring given by c(v) = colour[pi(v)] must be proper on the conflict graph."""
    n = len(nodes)
    for i in range(n):
        for j in range(i+1, n):
            if adj[i][j] and colour[i] == colour[j]:
                return False, "conflict edge %d,%d monochromatic" % (i, j)
    return True, "ok"

is_zero = _is_zero            # public alias (used by probes.py)
