"""How many ray configurations admit a palette field on the whole circle?

A ray configuration at a cyclic centre of length l is (up to a global rotation)
a cell vector c0 and a linear order in which the l thresholds psi = frac(x_j) are
crossed (the order and c0 are independent parameters: c_j = floor(x_j - psi) and
frac(x_j) are read off the same x_j, and any (floor, frac) pair occurs).  So the
configuration space is 6^l * l! and the physical palette-field condition is that
all l+1 nodes of the resulting monotone path are satisfiable.

ways[c0][eps] = number of orderings of the coordinates in eps whose every prefix
SET is satisfiable at the corresponding node.  Total = sum over c0 of
ways[c0][full]; the fraction is over 6^l * l!.
"""
from itertools import product
import chain_csp as C


def count(ell, k, pred):
    full = (1 << ell) - 1
    total = 0
    cells = list(product(range(6), repeat=ell))
    ok_nodes = 0
    for c0 in cells:
        sat = {}
        for eps in range(full + 1):
            v = tuple((c0[j] - ((eps >> j) & 1)) % 6 for j in range(ell))
            sat[eps] = pred(v)
            if sat[eps]:
                ok_nodes += 1
        if not sat[0]:
            continue
        ways = [0] * (full + 1)
        ways[0] = 1
        for eps in range(1, full + 1):
            if not sat[eps]:
                continue
            s = 0
            for j in range(ell):
                if (eps >> j) & 1:
                    s += ways[eps ^ (1 << j)]
            ways[eps] = s
        total += ways[full]
    import math
    return total, 6 ** ell * math.factorial(ell), ok_nodes


if __name__ == "__main__":
    for k in (5, 6):
        for ell in range(3, k + 1):
            pred = lambda c, e=ell, k=k: C.has_model(c, e, k, tight=(k == 6))
            t, N, nodes = count(ell, k, pred)
            print(f"k={k} l={ell}: {t} of {N} ray configurations admit a palette "
                  f"field on the whole circle  ({100.0*t/N:.4f}%)")
