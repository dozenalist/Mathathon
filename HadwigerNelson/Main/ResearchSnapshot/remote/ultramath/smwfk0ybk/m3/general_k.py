"""The closed-form witnesses for l = 3, 4 at every k: P_i = {l} for i even, {l+1} for i odd.

Checked against the paper's LITERAL sliver definition, every clause of (C1)-(C5), and the
general-k form of pair exclusion (A u B = Fin k, not only the k = 6 form).
"""
from itertools import product, combinations
from csp_vacuity import sig_matrix
from paper_defs import paper_slivers


def check(k, l):
    pal = [{l} if i % 2 == 0 else {l + 1} for i in range(6)]
    n = bad = 0
    for tail in product(range(6), repeat=l - 1):
        c = (0,) + tail
        sig = sig_matrix(l, c)
        n += 1
        ok = True
        for i in range(6):
            O, I = paper_slivers(l, k, sig[i])
            P = pal[i]
            if not (1 <= len(P) <= k - 3) or not (P & O) or not (P & I):
                ok = False
        if ok and any(pal[i] & pal[(i + 1) % 6] for i in range(6)):
            ok = False
        if ok and any(pal[i] | pal[j] == set(range(k)) for i, j in combinations(range(6), 2)):
            ok = False
        if not ok:
            bad += 1
    return n, bad, pal


if __name__ == "__main__":
    tot = fails = 0
    for k in range(4, 10):
        for l in (3, 4):
            if l + 2 > k:
                print(f"k={k} l={l}: outside the theorem's hypothesis l <= k-2, skipped")
                continue
            n, bad, pal = check(k, l)
            tot += n
            fails += bad
            print(f"k={k} l={l}: palettes {pal} satisfy (C1)-(C5) on {n-bad}/{n} geometries")
    print(f"total geometries {tot}, failures {fails}")
