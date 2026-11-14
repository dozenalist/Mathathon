"""Read saved rank witnesses and check their determinants modulo a prime.

This does not use the rational elimination or row-selection algorithms that
generated the witnesses.  Matrix construction shares the documented Fourier
algebra.  No files are modified.
"""

import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

from run_diagnostics import canonical_gram, d4_vectors, fourier_interpolation_system


def determinant_mod_prime(matrix, prime):
    a = [[Fraction(x).numerator * pow(Fraction(x).denominator, -1, prime) % prime
          for x in row] for row in matrix]
    assert all(len(row) == len(a) for row in a)
    determinant = 1
    for j in range(len(a)):
        pivot = next((i for i in range(j, len(a)) if a[i][j]), None)
        if pivot is None:
            return 0
        if pivot != j:
            a[pivot], a[j] = a[j], a[pivot]
            determinant = -determinant
        value = a[j][j]
        determinant = determinant * value % prime
        for i in range(j + 1, len(a)):
            multiplier = a[i][j] * pow(value, -1, prime) % prime
            for k in range(j + 1, len(a)):
                a[i][k] = (a[i][k] - multiplier * a[j][k]) % prime
            a[i][j] = 0
    return determinant % prime


def main():
    witnesses = json.loads((Path(__file__).resolve().parent / "rank_witnesses.json").read_text(encoding="utf-8"))
    for witness in witnesses:
        vectors = d4_vectors(witness["shell_cutoff"])
        grams = Counter(canonical_gram(x, y) for x in vectors for y in vectors)
        matrix, dimension, _, _ = fourier_interpolation_system(
            witness["gram_degree"], witness["shell_cutoff"], grams,
            witness["use_derivatives"], Fraction(witness["pi_specialization"]))
        selected = witness["selected_row_indices"]
        assert len(selected) == dimension + 1
        assert len(set(selected)) == len(selected)
        minor = [matrix[j] for j in selected]
        value = determinant_mod_prime(minor, witness["prime"])
        assert value != 0
        assert value == witness["determinant_mod_prime"]
    print(f"Verified {len(witnesses)} nonzero augmented minors modulo a prime.")


if __name__ == "__main__":
    main()
