"""Reproduce exact algebra and finite D4 shell diagnostics (standard library).

Run: python run_diagnostics.py
Generated artifacts are written beside this script, independent of the cwd.
These checks do not optimize an SDP or prove global sign inequalities.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from fractions import Fraction
from itertools import product
from math import factorial, isqrt, pi
from pathlib import Path

from gram_fourier import (
    derivative,
    evaluate,
    format_polynomial,
    fourier,
    laplacian,
    monomials,
    rational_rank,
    symmetric_basis,
)

HERE = Path(__file__).resolve().parent


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def d4_vectors(max_squared_norm: int):
    bound = isqrt(max_squared_norm)
    return [
        x
        for x in product(range(-bound, bound + 1), repeat=4)
        if sum(x) % 2 == 0 and dot(x, x) <= max_squared_norm
    ]


def twice_isodual(x):
    """Return 2*A*x, where A=diag(H_2,H_2)/2 and H_2=[[1,1],[1,-1]]."""
    a, b, c, d = x
    return a + b, a - b, c + d, c - d


def canonical_gram(x, y):
    u, v = dot(x, x), dot(y, y)
    return min(u, v), max(u, v), abs(dot(x, y))


def exact_checks():
    count = 0
    for n in (1, 2, 4):
        for m in monomials(6):
            p = {m: Fraction(1)}
            assert fourier(fourier(p, n), n) == p, (n, m)
            count += 1
    # Independent known one-variable Gaussian/Laguerre identities.
    for n in (1, 2, 4, 8):
        for k in range(9):
            expected = {
                (j, 0, 0): Fraction((-1) ** j * factorial(k), factorial(j))
                * generalized_binomial(Fraction(k) + Fraction(n, 2) - 1, k - j)
                for j in range(k + 1)
            }
            assert fourier({(k, 0, 0): Fraction(1)}, n) == expected, (n, k)
            count += 1
    assert fourier({(0, 0, 2): Fraction(1)}, 4) == {
        (0, 0, 2): Fraction(1),
        (1, 0, 0): Fraction(-1, 2),
        (0, 1, 0): Fraction(-1, 2),
        (0, 0, 0): Fraction(1),
    }
    assert fourier({(1, 1, 0): Fraction(1)}, 4) == {
        (1, 1, 0): Fraction(1),
        (1, 0, 0): Fraction(-2),
        (0, 1, 0): Fraction(-2),
        (0, 0, 0): Fraction(4),
    }
    # W^2-UV/n is harmonic in x and y separately, hence a +1 eigenfunction.
    for n in (2, 4, 8):
        harmonic = {(0, 0, 2): Fraction(1), (1, 1, 0): Fraction(-1, n)}
        assert not laplacian(harmonic, n)
        assert fourier(harmonic, n) == harmonic
        count += 1
    for _, p in symmetric_basis(8):
        q = fourier(p)
        assert all(c % 2 == 0 for a, b, c in q)
        assert q == {(b, a, c): v for (a, b, c), v in q.items()}
        count += 1
    # An independent Cartesian Hermite expansion tests the mixed terms.
    for n in (2, 4):
        for m in monomials(3):
            p = {m: Fraction(1)}
            assert cartesian_fourier(expand_gram(p, n)) == expand_gram(fourier(p, n), n), (n, m)
            count += 1
    return count + 2


def cartesian_multiply(p, q):
    out = {}
    for a, ca in p.items():
        for b, cb in q.items():
            m = tuple(x + y for x, y in zip(a, b))
            out[m] = out.get(m, Fraction(0)) + ca * cb
    return {m: c for m, c in out.items() if c}


def expand_gram(p, n):
    zero = (0,) * (2 * n)
    generators = [{}, {}, {}]
    for j in range(n):
        for generator, coordinates in ((0, (j, j)), (1, (j + n, j + n)), (2, (j, j + n))):
            m = list(zero)
            for coordinate in coordinates:
                m[coordinate] += 1
            generators[generator][tuple(m)] = Fraction(1)
    out = {}
    for powers, coefficient in p.items():
        expanded = {zero: coefficient}
        for generator, power in zip(generators, powers):
            for _ in range(power):
                expanded = cartesian_multiply(expanded, generator)
        for m, c in expanded.items():
            out[m] = out.get(m, Fraction(0)) + c
    return {m: c for m, c in out.items() if c}


def cartesian_fourier(p):
    """Independent product of one-dimensional Gaussian/Hermite formulas."""
    out = {}
    for powers, coefficient in p.items():
        total_degree = sum(powers)
        assert total_degree % 2 == 0
        for reductions in product(*(range(k // 2 + 1) for k in powers)):
            m = tuple(k - 2 * j for k, j in zip(powers, reductions))
            c = coefficient * (-1) ** (total_degree // 2 + sum(reductions))
            for k, j in zip(powers, reductions):
                c *= Fraction(factorial(k), 4**j * factorial(j) * factorial(k - 2 * j))
            out[m] = out.get(m, Fraction(0)) + c
    return {m: c for m, c in out.items() if c}


def generalized_binomial(a: Fraction, k: int) -> Fraction:
    answer = Fraction(1)
    for j in range(k):
        answer *= (a - j) / (j + 1)
    return answer


def shell_diagnostics(max_squared_norm=12):
    vectors = d4_vectors(max_squared_norm)
    shells = Counter(dot(x, x) for x in vectors)
    grams = Counter(canonical_gram(x, y) for x in vectors for y in vectors)
    for x in vectors:
        ax2 = twice_isodual(x)
        assert dot(ax2, ax2) == 2 * dot(x, x)
        assert len({c % 2 for c in ax2}) == 1  # Ax in Z^4 or Z^4+(1/2)^4.
        assert twice_isodual(ax2) == tuple(2 * c for c in x)
    for x in vectors:
        for y in vectors:
            assert dot(twice_isodual(x), twice_isodual(y)) == 2 * dot(x, y)
            assert sum(a * b for a, b in zip(twice_isodual(x), y)) % 2 == 0
    for u, v, w in grams:
        assert w * w <= u * v
        assert all(q == 0 or q >= 2 for q in (u, v, u + v - 2 * w, u + v + 2 * w))
    # Jacobi's four-square formula restricted to even norms.
    for squared_norm, count in shells.items():
        if squared_norm:
            expected = 8 * sum(d for d in range(1, squared_norm + 1)
                               if squared_norm % d == 0 and d % 4 != 0)
            assert count == expected
    with (HERE / "d4_gram_shells.csv").open("w", newline="", encoding="utf-8") as stream:
        fields = ["u", "v", "abs_t", "ordered_pair_count", "gram_rank", "strict_sign_interior",
                  "dual_u", "dual_v", "dual_abs_t"]
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for (u, v, w), count in sorted(grams.items()):
            rank = 2 if u * v > w * w else (1 if u + v else 0)
            strict = all(q > 2 for q in (u, v, u + v - 2 * w, u + v + 2 * w))
            writer.writerow(dict(u=u, v=v, abs_t=w, ordered_pair_count=count,
                                 gram_rank=rank, strict_sign_interior=int(strict),
                                 dual_u=str(Fraction(u, 2)), dual_v=str(Fraction(v, 2)),
                                 dual_abs_t=str(Fraction(w, 2))))
    return vectors, shells, grams


def interpolation_diagnostics(grams):
    """Exact necessary conditions on P only; not Fourier/sign feasibility.

    This uses unscaled Gram coordinates (u,v,t), which changes coefficients
    but not the span of the polynomial space.  Points within the shell cutoff
    are forced zeros.  Optional derivatives are imposed only at full-rank,
    strict interior Gram points, where sign+equality force stationarity.
    """
    results = []
    for degree in range(1, 7):
        basis = [p for _, p in symmetric_basis(degree)]
        origin = [evaluate(p, 0, 0, 0) for p in basis]
        for cutoff in (2, 4, 6):
            points = [g for g in sorted(grams) if 0 < g[0] + g[1] and g[1] <= cutoff]
            zeros = [[evaluate(p, *g) for p in basis] for g in points]
            jets = []
            for u, v, w in points:
                if u * v > w * w and all(q > 2 for q in (u, v, u + v - 2 * w, u + v + 2 * w)):
                    for j in range(3):
                        jets.append([evaluate(derivative(p, j), u, v, w) for p in basis])
            for use_jets, rows in ((False, zeros), (True, zeros + jets)):
                rank = rational_rank(rows)
                rank_plus_origin = rational_rank(rows + [origin])
                results.append(dict(gram_degree=degree, dimension=len(basis), shell_cutoff=cutoff,
                                    zero_orbits=len(points), derivative_rows=len(jets) if use_jets else 0,
                                    rank=rank, normalization_possible=rank_plus_origin > rank))
    with (HERE / "finite_interpolation.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(results[0]))
        writer.writeheader()
        writer.writerows(results)
    return results


def fourier_interpolation_system(degree, cutoff, grams, use_jets, specialization=Fraction(3)):
    """Build the augmented matrix; row order is part of the witness format."""
    basis = [p for _, p in symmetric_basis(degree)]
    transformed = [fourier(p) for p in basis]
    normalization = [
        [evaluate(p, 0, 0, 0) for p in basis] + [Fraction(1)],
        [evaluate(p, 0, 0, 0) for p in transformed] + [Fraction(4)],
    ]
    points = [g for g in sorted(grams) if 0 < g[0] + g[1] and g[1] <= cutoff]
    zeros = []
    jets = []
    for u, v, w in points:
        primal = tuple(specialization * z for z in (u, v, w))
        dual = tuple(z / 2 for z in primal)
        zeros.append([evaluate(p, *primal) for p in basis] + [Fraction(0)])
        zeros.append([evaluate(p, *dual) for p in transformed] + [Fraction(0)])
        # Fourier positivity makes every nonzero dual zero stationary.
        # At full-rank Gram points, the Gram map is a submersion.
        if u * v > w * w:
            for j in range(3):
                jets.append([evaluate(derivative(p, j), *dual) for p in transformed] + [Fraction(0)])
        # In the strict sign interior the same conclusion holds for f.
        if u * v > w * w and all(z > 2 for z in (u, v, u + v - 2 * w, u + v + 2 * w)):
            for j in range(3):
                jets.append([evaluate(derivative(p, j), *primal) for p in basis] + [Fraction(0)])
    rows = zeros + (jets if use_jets else []) + normalization
    return rows, len(basis), len(zeros), len(jets) if use_jets else 0


def modular_row_witness(rows, prime=1000003):
    """Select a nonsingular minor modulo a prime, independent of rational rank."""
    matrix = [[int(Fraction(x).numerator) * pow(int(Fraction(x).denominator), -1, prime) % prime
               for x in row] for row in rows]
    original_indices = list(range(len(rows)))
    selected = []
    determinant = 1
    rank = 0
    for column in range(len(matrix[0])):
        pivot = next((j for j in range(rank, len(matrix)) if matrix[j][column]), None)
        if pivot is None:
            return None
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        original_indices[rank], original_indices[pivot] = original_indices[pivot], original_indices[rank]
        selected.append(original_indices[rank])
        value = matrix[rank][column]
        determinant = determinant * value % prime
        inverse = pow(value, -1, prime)
        matrix[rank] = [x * inverse % prime for x in matrix[rank]]
        for j in range(rank + 1, len(matrix)):
            factor = matrix[j][column]
            if factor:
                matrix[j] = [(x - factor * y) % prime for x, y in zip(matrix[j], matrix[rank])]
        rank += 1
    return dict(prime=prime, selected_row_indices=selected, determinant_mod_prime=determinant)


def fourier_interpolation_diagnostics(grams):
    """Certify finite interpolation impossibility with a rational specialization.

    Every matrix entry is a rational polynomial in pi.  If the augmented
    matrix [A|b] has rank N+1 at pi=3, one of its (N+1)-minors is a nonzero
    rational polynomial.  It cannot vanish at the transcendental number pi.
    Thus rank[A(pi)|b]=N+1>N>=rank A(pi), proving inconsistency of the actual
    system.  A failure to attain rank N+1 here is explicitly inconclusive.
    This is a symbolic certificate argument, not replacing pi by 3 in f.
    """
    specialization = Fraction(3)
    results = []
    witnesses = []
    for degree in range(2, 11):
        for cutoff in (2, 4, 6):
            for use_jets in (False, True):
                rows, dimension, zero_count, jet_count = fourier_interpolation_system(
                    degree, cutoff, grams, use_jets, specialization)
                augmented_rank = rational_rank(rows)
                impossible = augmented_rank == dimension + 1
                if impossible:
                    witness = modular_row_witness(rows)
                    assert witness is not None
                    witnesses.append(dict(gram_degree=degree, shell_cutoff=cutoff,
                                          use_derivatives=use_jets, pi_specialization=str(specialization),
                                          **witness))
                results.append(dict(
                    gram_degree=degree, dimension=dimension, shell_cutoff=cutoff,
                    zero_rows=zero_count, derivative_rows=jet_count,
                    pi_specialization=str(specialization), augmented_rank=augmented_rank,
                    outcome="PROVED_INCONSISTENT" if impossible else "INCONCLUSIVE",
                ))
    with (HERE / "fourier_interpolation.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(results[0]))
        writer.writeheader()
        writer.writerows(results)
    (HERE / "rank_witnesses.json").write_text(json.dumps(witnesses, indent=2) + "\n", encoding="utf-8")
    return results


def main():
    algebra_checks = exact_checks()
    vectors, shells, grams = shell_diagnostics()
    interpolation = interpolation_diagnostics(grams)
    fourier_interpolation = fourier_interpolation_diagnostics(grams)
    summary = {
        "status": "EXACT_FINITE_DIAGNOSTICS_ONLY",
        "scope": "Algebra and finite shell necessary conditions; no SDP optimization or global sign verification.",
        "fourier_normalization": "exp(-2*pi*i*dot(z,xi))",
        "algebra_checks_passed": algebra_checks,
        "max_squared_norm": 12,
        "d4_vectors_including_origin": len(vectors),
        "d4_shell_counts": dict(sorted(shells.items())),
        "ordered_pairs": len(vectors) ** 2,
        "canonical_gram_orbits_including_origin": len(grams),
        "gram_basis_dimensions": {str(k): len(symmetric_basis(k)) for k in range(15)},
        "isodual_map": "A=diag([[1,1],[1,-1]],[[1,1],[1,-1]])/2; Gram(Ax,Ay)=Gram(x,y)/2",
        "density_target": pi * pi / 16,
        "published_degree13_lattice_upper_bound": 0.616858175,
        "published_upper_bound_minus_target": 0.616858175 - pi * pi / 16,
        "finite_interpolation_rows": len(interpolation),
        "fourier_interpolation_rows": len(fourier_interpolation),
        "fourier_interpolation_inconsistency_certificates": sum(
            row["outcome"] == "PROVED_INCONSISTENT" for row in fourier_interpolation
        ),
        "all_assertions_passed": True,
    }
    (HERE / "results.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    examples = []
    for name, p in symmetric_basis(3):
        examples.append(f"{name}: {format_polynomial(p)}\n  Fourier: {format_polynomial(fourier(p))}")
    (HERE / "fourier_examples.txt").write_text("\n".join(examples) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
