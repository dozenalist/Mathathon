"""Independent verification of every claim in README.md.

CHECK 1  my backtracking decision (chain_csp.has_model) == m5's bitmask
         reachability DP (smwfhd5sl/m5/interface_csp.sat_geometry) on EVERY cell
         vector, for k = 4,5,6 and every l in 3..k.
CHECK 2  brute-force chain search (all c0, all orderings) == chain_csp.chain_search,
         for l = 3,4 at k = 6, both with and without coincident thresholds.
CHECK 3  the parity palette field is an admissible one-centre palette system at
         k = 6 for l = 3 and l = 4: (C1),(C2),(C3),(C4),(C5) hold at all six
         orbit positions for EVERY ray configuration.
CHECK 4  (C4)+(C5) never remove a model that has no ternary palette: on the
         all-size-<=2 model sets, tight_ok is true identically.
"""
import sys, os, importlib.util
from itertools import product, permutations, combinations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chain_csp as C

M5 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                  "..", "..", "smwfhd5sl", "m5", "interface_csp.py")


def load_m5():
    spec = importlib.util.spec_from_file_location("m5_interface_csp", M5)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def check1():
    m5 = load_m5()
    bad = 0
    tot = 0
    for k in (4, 5, 6):
        for ell in range(3, k + 1):
            for c in product(range(6), repeat=ell):
                a = C.has_model(c, ell, k)              # my backtracking
                b = m5.sat_geometry(ell, k, c)          # m5's bitmask DP
                tot += 1
                if a != b:
                    bad += 1
                    if bad < 6:
                        print("  MISMATCH", k, ell, c, a, b)
    print(f"CHECK 1: {tot} instances compared (k=4,5,6; l=3..k; all 6^l cell "
          f"vectors), {bad} mismatches")
    return bad == 0


def brute_chain(ell, k, pred, jumps):
    cells = list(product(range(6), repeat=ell))
    full = (1 << ell) - 1
    for c0 in cells:
        if not pred(c0):
            continue
        # DFS over monotone subset chains from eps = 0 to eps = full
        stack = [(0, [c0])]
        while stack:
            eps, nodes = stack.pop()
            if eps == full:
                return nodes
            left = [j for j in range(ell) if not (eps >> j) & 1]
            sizes = range(1, len(left) + 1) if jumps else (1,)
            for r in sizes:
                for sub in combinations(left, r):
                    ne = eps
                    n = list(nodes[-1])
                    for j in sub:
                        ne |= 1 << j
                        n[j] = (n[j] - 1) % 6
                    n = tuple(n)
                    if pred(n):
                        stack.append((ne, nodes + [n]))
    return None


def check2():
    ok = True
    for ell in (3, 4):
        for k in (5, 6):
            pred = lambda c, e=ell, k=k: C.has_model(c, e, k, tight=(k == 6))
            for jumps in (False, True):
                a = brute_chain(ell, k, pred, jumps)
                b = C.chain_search(ell, k, pred, allow_jumps=jumps)
                same = (a is None) == (b is None)
                if a is not None and b is not None:
                    same = all(pred(c) for c in b) and all(pred(c) for c in a)
                print(f"CHECK 2: k={k} l={ell} jumps={jumps}: brute "
                      f"{'YES' if a else 'NO'} / DP {'YES' if b else 'NO'} "
                      f"-> {'agree' if same else 'DISAGREE'}")
                ok = ok and same
    return ok


def check3():
    """The parity field for length l: with U = {l,...,k-1} the outsiders, put
        P(f) = {l}   if f lies in a pi/3-cell of even index,
        P(f) = {l+1} if odd.
    Both labels are outsiders (so they lie in O_i and I_i for EVERY ray
    configuration), the field is measurable, every palette is a singleton, and
    f -> f+pi/3 flips the cell parity, so (5.7) holds for EVERY f.  This exists
    only when |U| >= 2, i.e. l <= k-2 = 4 at k = 6."""
    ok = True
    k = 6
    for ell in (3, 4):
        a, b = 1 << ell, 1 << (ell + 1)
        assert ell + 1 <= k - 1
        P = tuple(a if i % 2 == 0 else b for i in range(6))
        assert all(C.pc(p) == 1 for p in P)                    # (C1) and no ternary
        assert all(1 <= C.pc(p) <= k - 3 for p in P)
        assert all(not (P[i] & P[(i + 1) % 6]) for i in range(6))   # (5.7)
        assert C.tight_ok(P, k)                                # (C4)+(C5)
        bad = 0
        for c in product(range(6), repeat=ell):
            ois = C.oi_sets(c, ell, k)
            for i in range(6):
                O, I = ois[i]
                if not (P[i] & O) or not (P[i] & I):
                    bad += 1
        print(f"CHECK 3: l={ell}, field {sorted(x for x in range(k) if (a>>x)&1)}/"
              f"{sorted(x for x in range(k) if (b>>x)&1)}: (C1),(5.7),(C4),(C5) hold "
              f"identically; (C2) verified at all six positions for all {6**ell} ray "
              f"cell vectors -> {'PASS' if bad == 0 else 'FAIL'}")
        ok = ok and bad == 0
    return ok


def check4():
    ok = True
    for k in (6,):
        for ell in range(3, k + 1):
            bad = 0
            n = 0
            for c in product(range(6), repeat=ell):
                m = C.first_model(c, ell, k, maxsize=2)
                if m is None:
                    continue
                n += 1
                if not C.tight_ok(m, k):
                    bad += 1
            print(f"CHECK 4: k={k} l={ell}: {n} cell vectors carry an all-size<=2 "
                  f"model, {bad} of them fail (C4)/(C5)")
            ok = ok and bad == 0
    return ok


if __name__ == "__main__":
    r = [check1(), check2(), check3(), check4()]
    print("ALL CHECKS PASS" if all(r) else "SOME CHECK FAILED")
    sys.exit(0 if all(r) else 1)
