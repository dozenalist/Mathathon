"""Exact constructions of unit-distance graphs (coordinates in Q(sqrt3, sqrt11))."""
from fractions import Fraction as Fr
from .graph import PointSet

S3 = lambda F, a=1: {3: Fr(a)}          # a*sqrt(3)
S33 = lambda F, a=1: {33: Fr(a)}        # a*sqrt(33)
R = lambda q: {1: Fr(q)}                # rational


def _add(ps, name, xy):
    return ps.P(name, xy=xy)


def _comb(F, *terms):
    """sum of {basis: coeff} dicts, merged."""
    out = {}
    for t in terms:
        for b, c in t.items():
            out[b] = out.get(b, Fr(0)) + Fr(c)
    return {b: c for b, c in out.items() if c}


def _scale(t, q):
    return {b: c * Fr(q) for b, c in t.items()}


def _sum_pts(F, *xs):
    n = len(xs[0])

    def addc(a, b):
        o = dict(a)
        for k, v in b.items():
            o[k] = o.get(k, Fr(0)) + v
        return {k: v for k, v in o.items() if v}

    return tuple(addc(a, b) for a, b in zip(xs[0], xs[1]))


def tip(ps, name, xy):
    """Add a tip point given as (xexpr, yexpr) dicts."""
    return ps.P(name, xexpr=xy[0], yexpr=xy[1])


def add_diamond(ps, i, j, prefix, d2=None):
    """Add the two apexes of the diamond on segment (i,j) of length sqrt(3): the two
    points at distance exactly 1 from both endpoints.  apex = mid +- perp*sqrt(3)/6."""
    F = ps.F
    d2e = ps.sqdist(i, j)
    if d2 is None:
        d2 = 3 if F.is_zero(F.sub(d2e, F.rat(3))) else (1 if F.is_zero(F.sub(d2e, F.one)) else None)
    assert d2 in (1, 3), f"segment length^2 must be 1 or 3, got {d2e}"
    xi, yi = ps.pts[i]
    xj, yj = ps.pts[j]
    half = F.rat(Fr(1, 2))
    mx = F.mul(F.add(xi, xj), half)
    my = F.mul(F.add(yi, yj), half)
    dx = F.sub(xj, xi)
    dy = F.sub(yj, yi)
    px, py = F.neg(dy), dx                       # 90-degree rotation
    c = F.mul(F.sqrt(3), F.rat(Fr(1, 6) if d2 == 3 else Fr(1, 2)))   # sqrt3/6 or sqrt3/2
    ox, oy = F.mul(px, c), F.mul(py, c)
    a1 = (F.add(mx, ox), F.add(my, oy))
    a2 = (F.sub(mx, ox), F.sub(my, oy))
    i1 = ps.P(prefix + "a1", xexpr=None, yexpr=None, xy=_to_expr(F, a1))
    i2 = ps.P(prefix + "a2", xexpr=None, yexpr=None, xy=_to_expr(F, a2))
    # exactness assertions: an apex is at distance 1 from both tips, and the two
    # apexes are sqrt(3) apart.  If any fails, the construction is wrong.
    for t in (i, j):
        e = ps.sqdist(i1, t)
        assert F.is_zero(F.sub(e, F.one)), f"apex not unit from tip {t}"
        e = ps.sqdist(i2, t)
        assert F.is_zero(F.sub(e, F.one)), f"apex2 not unit from tip {t}"
    sep = ps.sqdist(i1, i2)
    want = F.rat(3) if d2 == 3 else F.rat(3)
    assert F.is_zero(F.sub(sep, F.rat(4 - d2))), f"apex separation wrong: {sep}"
    return i1, i2


def _to_expr(F, pt):
    def back(x):
        out = {}
        for c, b in zip(x, F.basis):
            if c:
                out[b] = c
        return out
    return (back(pt[0]), back(pt[1]))


def diamond(radicands=(3, 11)):
    ps = PointSet(radicands)
    t0 = tip(ps, "t0", ({}, {}))
    t1 = tip(ps, "t1", ({3: Fr(1)}, {}))
    a, b = add_diamond(ps, t0, t1, "t0t1.")
    return ps, {"tips": (t0, t1), "closing": []}


def moser(radicands=(3, 11)):
    """Moser spindle: two diamonds sharing tip K, far tips at unit distance."""
    ps = PointSet(radicands)
    K = tip(ps, "K", ({}, {}))
    C1 = tip(ps, "C1", ({3: Fr(1)}, {}))
    C2 = tip(ps, "C2", ({3: Fr(5, 6)}, {33: Fr(1, 6)}))
    add_diamond(ps, K, C1, "KC1.")
    add_diamond(ps, K, C2, "KC2.")
    assert ps.F.is_zero(ps.F.sub(ps.sqdist(C1, C2), ps.F.one)), "tips not unit apart"
    return ps, {"tips": (K, C1, C2), "closing": [(C1, C2)]}


def spindle_triangle(radicands=(3, 11)):
    """Three tips t0,t1,t2 with consecutive distances sqrt(3) (a diamond on each) and
    |t2-t0| = 1.  Exact closure of the chain with collinear first step."""
    ps = PointSet(radicands)
    t0 = tip(ps, "t0", ({}, {}))
    t1 = tip(ps, "t1", ({3: Fr(1)}, {}))
    t2 = tip(ps, "t2", ({3: Fr(1, 6)}, {33: Fr(1, 6)}))
    assert ps.F.is_zero(ps.F.sub(ps.sqdist(t0, t1), ps.F.rat(3)))
    assert ps.F.is_zero(ps.F.sub(ps.sqdist(t1, t2), ps.F.rat(3)))
    assert ps.F.is_zero(ps.F.sub(ps.sqdist(t2, t0), ps.F.one)), "closure failed"
    add_diamond(ps, t0, t1, "t0t1.")
    add_diamond(ps, t1, t2, "t1t2.")
    return ps, {"tips": (t0, t1, t2), "closing": [(t0, t2)]}
