"""Palette-level constraint system for a k=6 colouring at a centre whose
transition graph contains the 6-cycle, plus the exact two-centre exclusion.

Labels I = {0,...,5}.  The 6-cycle is 0-1-2-3-4-5-0.

Constraints imposed on a palette function P : S^1 -> 2^I (measurable,
implemented as piecewise constant on n = 6m equal sectors):

 (P0) 1 <= |P| <= 3                      [palette bound, K6-BARRIER.md sec.1]
 (P1) P(e) is not contained in a cycle edge {i,i+1}   [paper (6.2), Lemma 6.2]
 (P2) P(e) cap P(Re) = empty             [paper (5.7), Cor. 5.4]
 (P3) no two complementary 3-sets are both taken on positive measure
                                         [paper (5.2) at k=6, see Lemma A]
 (P4) two-centre exclusion [paper (5.3), Lemma 5.2(3)]: for any two distinct
      centres y,z at distance d,  P_y(f) cap P_z(s_pm(f)) = empty a.e.,
      where s_pm are the two exact unit-vector decompositions
          (y-z) + f = s + t,  |s| = |t| = 1.
"""
import itertools, math
from fractions import Fraction

LABELS = (0, 1, 2, 3, 4, 5)
CYCLE = [(i, (i + 1) % 6) for i in range(6)]
EDGES = frozenset(frozenset(e) for e in CYCLE)


def subsets(s):
    s = sorted(s)
    for r in range(1, len(s) + 1):
        for c in itertools.combinations(s, r):
            yield frozenset(c)


def allowed_values():
    """All subsets of I satisfying (P0) and (P1) for the 6-cycle."""
    out = []
    for S in subsets(LABELS):
        if not (1 <= len(S) <= 3):
            continue
        if any(S <= e or len(S) <= 2 and S in EDGES for e in EDGES):
            continue
        out.append(S)
    return out


def disjoint(a, b):
    return not (a & b)


def check_value(S):
    """(P0),(P1) for a single palette value."""
    if not (1 <= len(S) <= 3):
        return False
    for e in EDGES:
        if S <= e:
            return False
    return True


# ---------------------------------------------------------------- geometry
def shift_branches(f, delta):
    """Exact unit decompositions: delta + f = s + t, |s|=|t|=1.

    f, delta complex numbers of modulus 1 and |delta| resp.  Returns the two
    choices of s (the 'first endpoint'), and the matching t."""
    w = delta + f
    r = abs(w)
    assert 0.0 < r < 2.0
    h = math.sqrt(1.0 - r * r / 4.0)
    u = w / r
    s_plus = w / 2 + 1j * u * h
    s_minus = w / 2 - 1j * u * h
    return (s_plus, w - s_plus), (s_minus, w - s_minus)


def kappa():
    return math.pi / 3


def shift_error_constant(dmax, samples=4000):
    """Sup over f of |s_pm(f) - f*exp(+-i kappa)| / |delta|  for |delta|<=dmax."""
    worst = 0.0
    for j in range(samples):
        th = 2 * math.pi * j / samples
        f = cmath_exp(th)
        for k in range(24):
            ph = 2 * math.pi * k / 24
            for d in (dmax * (0.02 + 0.98 * l / 5) for l in range(6)):
                delta = d * cmath_exp(ph)
                (sp, tp), (sm, tm) = shift_branches(f, delta)
                worst = max(worst, abs(sp - f * cmath_exp(kappa())) / d,
                            abs(sm - f * cmath_exp(-kappa())) / d)
    return worst


def cmath_exp(t):
    return complex(math.cos(t), math.sin(t))


if __name__ == "__main__":
    V = allowed_values()
    print("allowed values:", len(V))
    print("  pairs :", sorted(tuple(sorted(v)) for v in V if len(v) == 2))
    print("  triples:", len([v for v in V if len(v) == 3]))
    print("C (shift error) at d=0.1:", shift_error_constant(0.1))


# ---------------------------------------------------------------- angle bound
def angle_error_constant(dmax, nf=720, nd=12, samples=6):
    """Sup over f, delta (|delta|<=dmax) and branches of the *angular* error
    |arg(s_pm(f)) - (arg f +- kappa)| divided by |delta|."""
    worst = 0.0
    for j in range(nf):
        th = 2 * math.pi * j / nf
        f = cmath_exp(th)
        for k in range(nd):
            ph = 2 * math.pi * k / nd
            for l in range(samples):
                d = dmax * (0.05 + 0.95 * l / max(1, samples - 1))
                delta = d * cmath_exp(ph)
                (sp, tp), (sm, tm) = shift_branches(f, delta)
                e1 = wrap(math.atan2(sp.imag, sp.real) - (th + kappa()))
                e2 = wrap(math.atan2(sm.imag, sm.real) - (th - kappa()))
                worst = max(worst, abs(e1) / d, abs(e2) / d)
    return worst


def wrap(a):
    return (a + math.pi) % (2 * math.pi) - math.pi
