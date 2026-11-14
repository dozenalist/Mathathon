"""The one-centre palette system at a cyclic centre is a CONTINUUM of six-position
instances, one per R-orbit of directions (R = rotation by pi/3).  m5's
interface_csp.py decides one instance at a time ("is THERE a satisfiable ray
geometry"); this file decides whether ANY ray configuration admits a palette
field on the whole circle, which is what a colouring must supply.

DERIVATION (every input cited; see README.md for the display-by-display audit).

Fix a centre x and the l limiting unit directions v_j (j = 0..l-1) of the simple
label cycle of length l in 3..k that Prop. 7.1 supplies.  theta_j = angle(v_j);
the R-orbit of directions is f, Rf, ..., R^5 f, phi = angle(f) in [0, pi/3).
Cells C(c) = ((c+1/2)pi/3, (c+3/2)pi/3), c in 0..5.  For fixed phi each ray's six
signs sig_j^(i) = sign(f_i . v_j), f_i = R^i f, are constant while theta_j - phi
stays in a cell, and there sig_j^(i) = sign(cos((c_j+1-i)pi/3)), i.e. +1 iff
(c_j+1-i) mod 6 in {0,1,5}.  With U = {l,...,k-1},
    O_i = U u {j : sig_(j-1)^(i) = sig_j^(i) = -1}    Lemma 8.1 (outer strip)
    I_i = U u {j : sig_(j-1)^(i) = sig_j^(i) = +1}    Lemma 8.1 (inner strip)
and for a.e. f (paper (5.2) -> Cor 5.4; Lemma 8.1; Prop 5.6 / R5):
    (C1) 1 <= |P_x(f_i)| <= k-3
    (C2) P_x(f_i) meets O_i and meets I_i
    (C3) P_x(f_i) cap P_x(f_(i+1)) = empty
for ALL i = 0..5 at once.  So for a.e. f the six-tuple (P_x(f_i))_i is a MODEL of
the instance with cell vector c(f).  Independently, m6 Thm 1 gives (C4) for a.e. f
and m6 Thm 2 gives (C5).

THE NEW CONSTRAINT.  With x_j := theta_j/(pi/3) - 1/2 and psi := phi/(pi/3),
    c_j(phi) = floor(x_j - psi),
so on psi in [0,1) each coordinate drops by one exactly once, at psi = frac(x_j).
The cells that actually occur therefore form a monotone lattice path
    c0, c0 - e_(j1), ..., c0 - (1,...,1)
in which every node occupies an interval of phi of POSITIVE length (a coincidence
of two thresholds only deletes a node).  Since (C1)-(C3) hold for a.e. phi,
EVERY OCCURRING NODE MUST HAVE A MODEL.  That is the chain condition below.

Exact integer arithmetic; no floating point in any decision.
"""

from itertools import combinations, product

POS = (True, True, False, False, False, True)   # cos(m pi/3) > 0, m = 0..5


def sign_matrix(cell, ell):
    return tuple(tuple(POS[(cell[j] + 1 - i) % 6] for j in range(ell)) for i in range(6))


def oi_sets(cell, ell, k):
    U = 0
    for lab in range(ell, k):
        U |= 1 << lab
    SIG = sign_matrix(cell, ell)
    out = []
    for i in range(6):
        s = SIG[i]
        O = I = U
        for j in range(ell):
            if not s[(j - 1) % ell] and not s[j]:
                O |= 1 << j
            if s[(j - 1) % ell] and s[j]:
                I |= 1 << j
        out.append((O, I))
    return out


def admissible(ell, k, O, I, maxsize=None):
    hi = k - 3 if maxsize is None else min(k - 3, maxsize)
    out = []
    for r in range(1, hi + 1):
        for comb in combinations(range(k), r):
            p = 0
            for lab in comb:
                p |= 1 << lab
            if (p & O) and (p & I):
                out.append(p)
    return out


def iter_models(cell, ell, k, maxsize=None):
    """All cyclicly disjoint palettes satisfying (C1),(C2) here.  Plain
    backtracking; m5's interface_csp.py uses a bitmask reachability DP and
    verify_chain.py compares the two decisions on every cell vector."""
    adm = [admissible(ell, k, O, I, maxsize) for (O, I) in oi_sets(cell, ell, k)]
    if any(not a for a in adm):
        return
    sol = []

    def rec(i):
        if i == 6:
            if not (sol[5] & sol[0]):
                yield tuple(sol)
            return
        for q in adm[i]:
            if not (q & sol[i - 1]):
                sol.append(q)
                yield from rec(i + 1)
                sol.pop()

    for p in adm[0]:
        sol.append(p)
        yield from rec(1)
        sol.pop()


def pc(p):
    return bin(p).count("1")


def tight_ok(mod, k):
    if sum(1 for p in mod if pc(p) == k - 3) > k // 2:      # (C5)
        return False
    full = (1 << k) - 1
    for a, b in combinations(mod, 2):                        # (C4)
        if (a | b) == full and (a & b) == 0:
            return False
    return True


def first_model(cell, ell, k, tight=False, maxsize=None):
    for mod in iter_models(cell, ell, k, maxsize):
        if tight and not tight_ok(mod, k):
            continue
        return mod
    return None


def has_model(cell, ell, k, tight=False, maxsize=None):
    return first_model(cell, ell, k, tight, maxsize) is not None


# ------------------------------------------------------------------ chain search

def base6(cell, ell):
    n = 0
    for j in range(ell):
        n = n * 6 + cell[j]
    return n


def unbase6(n, ell):
    out = [0] * ell
    for j in range(ell - 1, -1, -1):
        out[j] = n % 6
        n //= 6
    return tuple(out)


def cells_of(ell):
    return list(product(range(6), repeat=ell))


def chain_search(ell, k, pred, allow_jumps=True):
    """Return a list of cell vectors c0, c1, ..., c0-(1..1) forming a monotone
    path with pred true at every node, or None.

    With w := c0 - (1,...,1) (final node) and delta := (1,...,1) - eps, the nodes
    are w + delta as delta decreases from (1,...,1) to 0.  allow_jumps=False
    restricts to one-coordinate steps (all l thresholds distinct).
    """
    cells = cells_of(ell)
    N = len(cells)
    num = {c: i for i, c in enumerate(cells)}
    SAT = {num[c] for c in cells if pred(c)}
    if not SAT:
        return None
    full = (1 << ell) - 1
    # T[delta] = { index(w) : w + delta in SAT }
    T = {}
    T[0] = SAT
    for delta in range(1, full + 1):
        prev_delta = delta & (delta - 1)                 # clear lowest set bit
        j = (delta ^ prev_delta).bit_length() - 1        # the coordinate added
        T[delta] = {num[tuple((w[jj] - (1 if jj == j else 0)) % 6 for jj in range(ell))]
                    for w in (cells[i] for i in T[prev_delta])}
    popc = lambda d: bin(d).count("1")
    order = sorted(range(full + 1), key=lambda d: -popc(d))
    reach = {}
    for delta in order:
        cands = [d for d in range(full + 1)
                 if (d & delta) == delta and d != delta and
                 (allow_jumps or popc(d) == popc(delta) + 1)]
        prev = set()
        for d in cands:
            prev |= reach[d]
        reach[delta] = T[delta] & prev if delta != full else set(T[full])
    if not reach[0]:
        return None
    # reconstruct
    w = cells[min(reach[0], key=lambda i: i)]
    path = [0]
    delta = 0
    while delta != full:
        cands = [d for d in range(full + 1)
                 if (d & delta) == delta and d != delta and
                 (allow_jumps or popc(d) == popc(delta) + 1)]
        nxt = [d for d in cands if num[w] in reach[d]]
        if not nxt:
            break
        delta = min(nxt, key=popc)
        path.append(delta)
    return [tuple((w[j] + ((delta >> j) & 1)) % 6 for j in range(ell)) for delta in path]


def show(mod):
    return " ".join("{" + ",".join(str(i) for i in range(32) if (p >> i) & 1) + "}" for p in mod)


if __name__ == "__main__":
    import sys
    kk = [int(a) for a in sys.argv[1:]] or [4, 5, 6]
    print(" k ell  geoms  (C1-3)  (C1-5)  size<=2 |  chain(C1-3)  chain(C1-5)  chain(size<=2)   [jumps]")
    for k in kk:
        for ell in range(3, k + 1):
            cells = cells_of(ell)
            pred = {
                "13": lambda c, e=ell, k=k: has_model(c, e, k),
                "15": lambda c, e=ell, k=k: has_model(c, e, k, tight=True),
                "sm": lambda c, e=ell, k=k: has_model(c, e, k, maxsize=2),
            }
            cnt = [sum(1 for c in cells if pred[t](c)) for t in ("13", "15", "sm")]
            ch = {t: chain_search(ell, k, pred[t]) for t in ("13", "15", "sm")}
            f = lambda x: "yes" if x else "NO "
            print(f"{k:>2} {ell:>3} {len(cells):>6} {cnt[0]:>7} {cnt[1]:>7} {cnt[2]:>7} |"
                  f" {f(ch['13']):>12} {f(ch['15']):>12} {f(ch['sm']):>14}", flush=True)
            for t in ("13", "15", "sm"):
                if ch[t]:
                    print(f"      chain({t}) jumps-ok:", " -> ".join(str(n) for n in ch[t]))
