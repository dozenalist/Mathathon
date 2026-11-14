"""Exact first-shell angular diagnostics. Python 3.10+, standard library only.

These checks concern a single pair of radii. They do not construct a Fourier-
positive function on R^8 or establish a packing bound.
"""

from collections import Counter
from fractions import Fraction as Q
from itertools import product
import json
from math import comb
from pathlib import Path


def add(a, b):
    out = dict(a)
    for degree, coefficient in b.items():
        out[degree] = out.get(degree, Q(0)) + coefficient
    return {d: c for d, c in out.items() if c}


def scale(a, c):
    return {d: v * c for d, v in a.items() if v * c}


def multiply(a, b):
    out = {}
    for i, x in a.items():
        for j, y in b.items():
            out[i + j] = out.get(i + j, Q(0)) + x * y
    return {d: c for d, c in out.items() if c}


def evaluate(poly, c):
    return sum((a * c**d for d, a in poly.items()), Q(0))


def gegenbauer_u(n):
    older, current = {0: Q(1)}, {1: Q(2)}
    if n == 0:
        return older
    for _ in range(1, n):
        older, current = current, add(
            multiply({1: Q(2)}, current), scale(older, Q(-1))
        )
    return current


def sphere_moment(degree):
    """E[c^degree] for cosine between independent uniform S^3 directions.

    Even moments are Catalan(k)/4^k, obtained from the beta integral.
    """
    if degree % 2:
        return Q(0)
    k = degree // 2
    return Q(comb(2 * k, k), (k + 1) * 4**k)


def spherical_mean(poly):
    return sum((a * sphere_moment(d) for d, a in poly.items()), Q(0))


def determinant(matrix):
    a = [list(map(Q, row)) for row in matrix]
    result = Q(1)
    for col in range(len(a)):
        pivot = next((i for i in range(col, len(a)) if a[i][col]), None)
        if pivot is None:
            return Q(0)
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            result = -result
        value = a[col][col]
        result *= value
        for i in range(col + 1, len(a)):
            factor = a[i][col] / value
            for j in range(col, len(a)):
                a[i][j] -= factor * a[col][j]
    return result


def main():
    q = multiply(
        multiply({2: Q(1)}, {2: Q(1), 0: Q(-1, 4)}),
        {0: Q(1), 2: Q(-1)},
    )
    expansion = scale(
        add(add(gegenbauer_u(0), scale(gegenbauer_u(2), Q(2))),
            scale(gegenbauer_u(6), Q(-1))),
        Q(1, 64),
    )
    assert q == expansion
    assert spherical_mean(q) == Q(1, 64)

    # A separate, nonnegative dual-shell profile. These two profiles have
    # NOT been shown to arise as a function and its Fourier transform.
    dual_q = multiply(q, {2: Q(1), 0: Q(-1, 4)})
    dual_expansion = {}
    for ell, coefficient in ((0, 2), (2, 3), (4, 1), (6, -1), (8, -1)):
        dual_expansion = add(dual_expansion,
                             scale(gegenbauer_u(ell), Q(coefficient, 256)))
    assert dual_q == dual_expansion
    assert spherical_mean(dual_q) == Q(1, 128)
    assert evaluate(dual_q, Q(1, 4)) > 0
    assert evaluate(dual_q, Q(3, 4)) > 0

    # Enumerate the actual first shell, rather than assuming its angle list.
    roots = [v for v in product((-1, 0, 1), repeat=4)
             if sum(t * t for t in v) == 2 and sum(v) % 2 == 0]
    assert len(roots) == 24
    distributions = []
    for x in roots:
        distributions.append(Counter(Q(sum(a*b for a, b in zip(x, y)), 2)
                                     for y in roots))
    assert all(d == distributions[0] for d in distributions)
    counts = distributions[0]
    assert counts == {Q(-1): 1, Q(-1, 2): 8, Q(0): 6,
                      Q(1, 2): 8, Q(1): 1}
    assert all(evaluate(q, c) == 0 for c in counts)
    assert all(evaluate(dual_q, c) == 0 for c in counts)

    # Factor signs are an exact continuum proof on the stated intervals:
    # c^2 >= 0; 1-c^2 >= 0 on [-1,1]; c^2-1/4 changes sign at +/-1/2.
    # These rational points are supplementary sanity checks, not the proof.
    assert evaluate(q, Q(1, 4)) < 0
    assert evaluate(q, Q(3, 4)) > 0
    for degree in range(6):
        discrete = sum(Q(n, 24) * c**degree for c, n in counts.items())
        assert discrete == sphere_moment(degree)

    angles = [Q(0), Q(1, 2), Q(1)]
    matrix = [[evaluate(gegenbauer_u(ell), c) for ell in (0, 2, 10)]
              for c in angles]
    assert determinant(matrix) == 12
    matrix_026 = [[evaluate(gegenbauer_u(ell), c) for ell in (0, 2, 6)]
                  for c in angles]
    assert determinant(matrix_026) == 0
    assert all(sum(a*b for a, b in zip(row, (1, 2, -1))) == 0
               for row in matrix_026)

    # A positive safe-angle quadrature that excludes entire angular families:
    # both supported points satisfy all lattice signs for every r,s>=sqrt(2).
    for ell in range(2, 50, 2):
        if ell % 12 in (4, 6):
            u = gegenbauer_u(ell)
            assert (evaluate(u, Q(0)) + evaluate(u, Q(1, 2))) / 2 == 0

    harmonics = []
    for ell in range(0, 17, 2):
        u = gegenbauer_u(ell)
        mean = sum(Q(n, 24) * evaluate(u, c) for c, n in counts.items())
        assert spherical_mean(u) == (1 if ell == 0 else 0)
        harmonics.append({"angular_degree": ell,
                          "effective_radial_dimension": 4 + 2*ell,
                          "root_shell_mean": str(mean)})

    output = {
        "scope": "Exact one-shell angular algebra; no global certificate",
        "status": "all exact checks passed",
        "first_shell_size": len(roots),
        "cosine_multiplicities_per_root": {
            str(c): counts[c] for c in sorted(counts)},
        "q_coefficients_in_c": {str(k): str(v) for k, v in sorted(q.items())},
        "q_gegenbauer_coefficients": {"0": "1/64", "2": "1/32", "6": "-1/64"},
        "q_continuous_spherical_mean": str(spherical_mean(q)),
        "q_discrete_root_shell_mean": "0",
        "dual_q_gegenbauer_coefficients": {
            "0": "1/128", "2": "3/256", "4": "1/256",
            "6": "-1/256", "8": "-1/256"},
        "dual_q_continuous_spherical_mean": str(spherical_mean(dual_q)),
        "dual_q_status": "Independent local profile, not Fourier transform of q",
        "safe_angle_quadrature": {
            "nodes": ["0", "1/2"], "weights": ["1/2", "1/2"],
            "annihilated_angular_degrees_mod_12": [4, 6]},
        "evaluation_matrix_0_2_10": [[str(x) for x in row] for row in matrix],
        "evaluation_determinant_0_2_10": "12",
        "harmonic_shell_means": harmonics,
    }
    destination = Path(__file__).with_name("angular_profiles.json")
    destination.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
