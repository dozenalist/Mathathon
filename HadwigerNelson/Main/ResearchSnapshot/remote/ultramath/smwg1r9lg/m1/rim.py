"""The hexagon (TE) extension: (5.3) at every unit pair of the cluster
{x} union {x + R^j e : j in Z/6}, in the six orbit directions.

At a unit pair (x, y) with y = x + a, |a| = 1, Remark 5.3's instance of (5.3) reads

    P_y(f) cap P_x(f) = empty          for a.e. unit direction f,

without any hypothesis on a (Lemma 6 of m9's note).  Applied to the cluster:
the six points y_j = x + R^j e are pairwise at distance 1 when |j-k| = 1 mod 6,
and each is at distance 1 from x, so with Q_{j,m} := P_{y_j}(R^m e):

    (TR1)  Q_{j,m} cap P_m = empty                    (x -- y_j, direction R^m e)
    (TR2)  Q_{j,m} cap Q_{j+1,m} = empty              (y_j -- y_{j+1}, same direction)
    (TR3)  Q_{j,m} cap Q_{j,m+1} = empty              (5.7) at y_j
    (TR4)  1 <= |Q_{j,m}| <= k-3                      (PB) at y_j
    (TR5)  c_j not in Q_{j,m},  c_j := c(y_j)         (SA) at y_j
    (TR6)  c_j in P_j,  c_j != c_{j+1}                (T) at x, and properness

All exact integer arithmetic.
"""
from itertools import product


def bits(mask, k):
    return [x for x in range(k) if (mask >> x) & 1]


def rim_ok(w, i, k, ell, want_witness=False):
    """Does the cluster system have a solution for this orbit word w?"""
    P = [bits(m, k) for m in w]
    for c in product(*P):
        if any(c[j] == c[(j + 1) % 6] for j in range(6)):
            continue                      # cannot happen: P_j cap P_{j+1} = empty
        lists = {}
        ok = True
        for j in range(6):
            for m in range(6):
                av = [x for x in range(k) if x not in P[m] and x != c[j]]
                if not av:
                    ok = False
                    break
                lists[(j, m)] = av
            if not ok:
                break
        if not ok:
            continue
        sol = _grid(lists, k)
        if sol is not None:
            if want_witness:
                return c, sol
            return True
    return None


def _grid(lists, k):
    """Proper colouring of C_6 x C_6 with the given lists (one label per cell)."""
    cells = sorted(lists, key=lambda t: (len(lists[t]), t))
    assign = {}

    def ok(cell, v):
        j, m = cell
        for nb in (((j + 1) % 6, m), ((j - 1) % 6, m), (j, (m + 1) % 6), (j, (m - 1) % 6)):
            if assign.get(nb, None) == v:
                return False
        return True

    def bt(t):
        if t == len(cells):
            return True
        cell = cells[t]
        for v in lists[cell]:
            if ok(cell, v):
                assign[cell] = v
                if bt(t + 1):
                    return True
                del assign[cell]
        return False

    if not bt(0):
        return None
    return {(j, m): assign[(j, m)] for (j, m) in assign}


def verify_rim(w, i, k, c, sol):
    """Check a claimed witness exactly."""
    P = [set(bits(m, k)) for m in w]
    errs = []
    for j in range(6):
        if c[j] not in P[j]:
            errs.append(f"(TR6) c_{j} not in P_{j}")
        if c[j] == c[(j + 1) % 6]:
            errs.append(f"(TR6) c_{j} = c_{j+1}")
    for j in range(6):
        for m in range(6):
            v = sol[(j, m)]
            if v in P[m]:
                errs.append(f"(TR1) Q_{j},{m} meets P_{m}")
            if v == c[j]:
                errs.append(f"(TR5) Q_{j},{m} = c_j")
            for nb in (((j + 1) % 6, m), (j, (m + 1) % 6)):
                if sol[nb] == v:
                    errs.append(f"(TR2/3) Q_{j},{m} = Q_{nb}")
    return errs
