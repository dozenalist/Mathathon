"""Non-vacuity check for the pair-transition statement.

The hexagonal seven-colouring (Voronoi cells of the triangular lattice with side s = 0.4 and
spacing L = sqrt3 * s; colour = the coset of i + j*omega in Z[omega]/(2 - omega) = (i + 2j) mod 7) is a proper
colouring of the plane: the minimal non-zero kernel vector of the index-seven sublattice has length
sqrt7 * L = 1.833... > 1 + 2s = 1.8, so same-coloured cells are never at unit distance.

This script samples unit pairs and records which of the 21 label pairs occur, showing that
"every pair occurs at unit distance" (Theorem A's conclusion) is compatible with an actual proper
colouring - i.e. the conclusion is not vacuous and not by itself contradictory.

Run: python3 hex_pairs.py
"""
import random
import math
from itertools import combinations

S = 0.4
L = math.sqrt(3) * S
W = complex(-0.5, math.sqrt(3) / 2)          # omega = e^{2 pi i / 3}


def lattice_index(z):
    """Nearest point of the triangular lattice L*(i + j*omega) to z; returns (i, j)."""
    # Voronoi-relevant: minimise |z - L(i + j w)|^2 over a small window around the real solution
    # real coordinates: L*(i - j/2), L*(j*sqrt3/2)
    x, y = z.real, z.imag
    j0 = y / (L * math.sqrt(3) / 2)
    i0 = x / L + j0 / 2
    best = None
    for j in (math.floor(j0) - 1, math.floor(j0), math.floor(j0) + 1, math.ceil(j0)):
        for i in (math.floor(i0) - 1, math.floor(i0), math.floor(i0) + 1, math.ceil(i0)):
            p = L * (i + j * W)
            d = abs(z - p)
            if best is None or d < best[0]:
                best = (d, (i, j))
    return best[1]


def colour(z):
    i, j = lattice_index(z)
    return (i + 2 * j) % 7


def main():
    random.seed(20261114)
    counts = {p: 0 for p in combinations(range(7), 2)}
    same = 0
    N = 400000
    for _ in range(N):
        x = complex(random.uniform(-40, 40), random.uniform(-40, 40))
        theta = random.uniform(0, 2 * math.pi)
        y = x + complex(math.cos(theta), math.sin(theta))
        a, b = colour(x), colour(y)
        if a == b:
            same += 1
            continue
        counts[tuple(sorted((a, b)))] += 1
    print(f"sampled unit pairs: {N}")
    print(f"same-coloured unit pairs (must be 0): {same}")
    missing = [p for p, c in counts.items() if c == 0]
    print(f"label pairs never seen at unit distance: {missing}")
    for p, c in sorted(counts.items()):
        print(f"  pair {p}: {c}")
    assert same == 0, "colourings sampled a monochromatic unit pair: check the cell size"
    assert not missing, "some pair never occurs: adjust sampling"
    print()
    print("All 21 label pairs occur at unit distance in a proper 7-colouring.")
    print("So Theorem A's conclusion is consistent with an actual colouring; it is a necessary")
    print("condition on a six-colouring, not a contradiction.")


if __name__ == "__main__":
    main()
