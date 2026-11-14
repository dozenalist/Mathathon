"""The two k = 6 palette models of no-go.md, checked end to end.

Labels I = {1,...,6};  triangle T = {1,2,3};  outsiders O = {4,5,6}.
Both models put, for every centre z in R^2 and every direction e = e^{it},

        s(t) = floor(9 t / (2 pi)) mod 3   in  Z/3,
        h(t) = t's step index mod 3  (three colours, period 2 pi/9 per step,
                                      period 2 pi/3 per colour),

and differ only in the palette attached to the colour:

   (M')  PRIMARY, "T-ary pair" model:   P_z(e^{it}) = Q_{s(t)},
         Q_0 = {1,4},  Q_1 = {2,5},  Q_2 = {3,6}     (a perfect matching of I).
         Every palette has two elements, meets T and meets O, and distinct colours carry
         disjoint palettes.  This model is T-ary in the sense of (N1) of
         .ultramath/smwfcr56i/m2/k6_nogo.md.

   (M)   "outsider singleton" variant:  P_z(e^{it}) = {4 + s(t)} subset O.

Checks (each in two independent code paths where it matters):

  A  transport (P3) via the general decomposition  W/2 +/- i (W/|W|) sqrt(1-|W|^2/4)
  B  transport (P3) via the paper's exact Theta_d / alpha_pm formulas
  C  (5.7):  P_z(f) cap P_z(Rf) = empty
  D  palette bound and (6.2):  P not contained in {1,2}, {1,3}, {2,3}
  E  T-arity, |P| >= 2, P meets O  (model M' only), no complementary triples
  F  EXACT rational-arithmetic check of the band  9b/(2 pi) in (1,2) u (-2,-1)
  G  traces (P5): for each edge {i,j} of T the set P(t) minus {i,j} is a singleton
  H  the k = 5 falsification: the 2-valued analogue has a positive-measure agreement set
"""
import numpy as np
from fractions import Fraction

PI = np.pi
KAPPA = PI / 3.0
DMAX = 1.0 / 50.0          # valid for all pairs at distance <= DMAX
CDEV = 4.0                 # rigorous bound |alpha_pm(t) - (t +/- kappa)| <= CDEV*d
LABELS = (1, 2, 3, 4, 5, 6)
T = (1, 2, 3)
EDGES = ((1, 2), (1, 3), (2, 3))
Q = (frozenset({1, 4}), frozenset({2, 5}), frozenset({3, 6}))     # model (M')
SING = (frozenset({4}), frozenset({5}), frozenset({6}))           # model (M)


def step_index(t):
    return int(np.floor(9.0 * t / (2.0 * PI))) % 3


def step_index_alt(t):
    """second implementation: three colours of length 2pi/9, period 2pi/3."""
    h = 2.0 * PI / 9.0
    tt = t % (2.0 * PI)
    return int(np.floor(tt / h + 1e-12)) % 3


def palette(t, table):
    return table[step_index(t)]


# ------------------------------------------------------------------ decompositions
def decompose(W):
    """The two unit vectors s,t with s+t = W (|W| <= 2)."""
    r = abs(W)
    assert r <= 2.0 + 1e-12
    if r < 1e-15:
        return complex(1, 0), complex(-1, 0)
    perp = 1j * (W / r) * np.sqrt(max(0.0, 1.0 - r * r / 4.0))
    return W / 2 + perp, W / 2 - perp


def alpha_pm(d, t):
    z = 1.0 + d * np.exp(-1j * t)
    Theta = t + np.angle(z)
    rho = abs(d + np.exp(1j * t))
    a = np.arccos(rho / 2.0)
    return Theta + a, Theta - a


# -------------------------------------------------------------------------- checks
def check_A(table, n_pair=400, n_dir=200, seed=20260224):
    """transport through the general decomposition, random pairs"""
    rng = np.random.default_rng(seed)
    viol = checked = 0
    worst = 0.0
    for _ in range(n_pair):
        d = DMAX * rng.random()
        A = d * np.exp(2j * PI * rng.random())
        for _ in range(n_dir):
            t = 2 * PI * rng.random()
            sv, tv = decompose(A + np.exp(1j * t))
            p_w = palette(t, table)
            p_s = palette(np.angle(sv), table)
            p_t = palette(np.angle(tv), table)
            checked += 1
            if p_w & p_s or p_w & p_t:
                viol += 1
            for ang in (np.angle(sv), np.angle(tv)):
                diff = np.angle(np.exp(1j * (ang - t)))
                worst = max(worst, abs(abs(diff) - KAPPA))
    return viol, checked, worst


def check_B(table, n_pair=300, n_dir=200, seed=771):
    """transport through the paper's alpha_pm, random displacement direction"""
    rng = np.random.default_rng(seed)
    viol = checked = 0
    worst = 0.0
    for _ in range(n_pair):
        d = DMAX * rng.random()
        th = 2 * PI * rng.random()
        for _ in range(n_dir):
            t = 2 * PI * rng.random()
            s_abs = th + alpha_pm(d, t - th)[0]
            t_abs = th + alpha_pm(d, t - th)[1]
            checked += 1
            worst = max(worst, abs(s_abs - (t + KAPPA)), abs(t_abs - (t - KAPPA)))
            p_w = palette(t, table)
            if p_w & palette(s_abs, table) or p_w & palette(t_abs, table):
                viol += 1
    return viol, checked, worst


def check_C(table, n_dir=200000):
    """(5.7)"""
    viol = 0
    for j in range(n_dir):
        t = -PI + 2 * PI * j / n_dir
        if palette(t, table) & palette(t + KAPPA, table):
            viol += 1
    return viol, n_dir


def check_DE(table):
    """palette bound, (6.2), (M') extras, no complementary triples"""
    bad = 0
    info = []
    for P in set(table):
        n = len(P)
        if not (1 <= n <= 3):
            bad += 1
        for (i, j) in EDGES:
            if P <= {i, j}:
                bad += 1
        if n == 3 and any((frozenset(LABELS) - P) in set(table) for _ in (0,)):
            bad += 1
        info.append((sorted(P), n, bool(P & set(T)), bool(P & {4, 5, 6})))
    return bad, info


def check_F(n_shift=20000, C=CDEV, dmax=DMAX):
    """EXACT rational check: every shift in the band has 9b/(2pi) in (1,2) u (-2,-1).
       Then, for beta in those intervals, floor(u+beta)-floor(u) is never 0 mod 3."""
    bad = 0
    klo, khi = Fraction(333, 106) / 3, Fraction(22, 7) / 3     # rigorous kappa bounds
    band = Fraction(int(C * dmax * 10 ** 6), 10 ** 6)
    blo, bhi = klo - band, khi + band
    beta_min = 9 * blo / (2 * Fraction(22, 7))                 # small beta bound
    beta_max = 9 * bhi / (2 * Fraction(333, 106))              # large beta bound
    out = [float(beta_min), float(beta_max)]
    if not (beta_min > 1 and beta_max < 2):
        bad += 1
    NX, NB = 3000, 200
    for i in range(NB + 1):
        beta = beta_min + (beta_max - beta_min) * Fraction(i, NB)
        for j in range(NX):
            x = Fraction(j, NX)
            inc = 1 if x < 2 - beta else 2
            if not (inc <= x + beta < inc + 1):
                bad += 1
            if inc % 3 == 0:
                bad += 1
            bp = -beta
            incp = -2 if x < -1 - bp else -1
            if not (incp <= x + bp < incp + 1):
                bad += 1
            if incp % 3 == 0:
                bad += 1
    return bad, out


def check_G(table):
    """(P5): for each edge {i,j} of T there is a probability vector supported in P with
       zero i- and j-coordinates, i.e. P minus {i,j} must be nonempty (then the uniform
       vector on it works, measurably in t).  Reports the worst case and the traces."""
    bad = 0
    detail = []
    for P in set(table):
        for (i, j) in EDGES:
            rest = P - {i, j}
            if not rest:                       # P subseteq {i,j}: forbidden by (P4)
                bad += 1
            detail.append((sorted(P), (i, j), sorted(rest)))
    return bad, detail


def check_H():
    """the two-valued analogue fails: positive-measure agreement set near shift pi/3"""
    h = 2.0 * PI / 9.0

    def s2(t):
        return step_index(t) % 2

    worst = 0.0
    for k in range(101):
        b = KAPPA - 0.2 + 0.4 * k / 100
        beta = (9 * b / (2 * PI)) % 2.0
        worst = max(worst, min(beta, 2.0 - beta) * h)
    hits = 0
    n = 20000
    for j in range(n):
        t = -PI + 2 * PI * j / n
        if s2(t) == s2(t + KAPPA):
            hits += 1
    return worst, hits, n


def main():
    print("step index: two implementations agree:",
          all(step_index(t) == step_index_alt(t) for t in np.linspace(-3 * PI, 3 * PI, 100001)))
    print("s has period 2pi:", all(step_index(t) == step_index(t + 2 * PI)
                                   for t in np.linspace(-PI, PI, 20001)))
    for name, table in (("(M') T-ary pair model", Q), ("(M) singleton variant", SING)):
        print(f"\n================ {name} ================")
        d, info = check_DE(table)
        print(f"  D/E palette census: {info}   violations = {d}")
        gb, gd = check_G(table)
        print(f"  G traces (P5): nonempty P minus edge for all edges: violations = {gb}")
        print(f"     trace data (palette, edge, support of the avoiding trace): {gd}")
        v, n = check_C(table)
        print(f"  C  (5.7): {n} directions, violations = {v}")
        v, n, w = check_A(table)
        print(f"  A  transport (general decomposition): {n} checks, violations = {v}, max|dev| = {w:.4f}")
        v, n, w = check_B(table)
        print(f"  B  transport (paper alpha_pm):        {n} checks, violations = {v}, max|dev| = {w:.4f}")
    bad, beta = check_F()
    print(f"\n  F  exact rational band check: beta range [{beta[0]:.6f}, {beta[1]:.6f}],"
          f" violations = {bad}")
    worst, hits, n = check_H()
    print(f"  H  k = 5 analogue fails: max agreement measure = {worst:.4f};"
          f" grid hits s2(t)=s2(t+pi/3): {hits}/{n}")


if __name__ == "__main__":
    main()
