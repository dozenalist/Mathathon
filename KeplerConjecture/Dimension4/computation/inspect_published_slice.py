"""Inspect a first-shell angular slice of the authors' stored d=13 output.

Uses only the standard library. Requires the ignored cache obtained with
fetch_upstream_metadata.py --fetch --include-d4-slice. This is high-precision
inspection of a floating-point solver output, not its rigorous verification.
"""

import csv
import hashlib
import json
import re
import struct
from decimal import Decimal, getcontext, localcontext
from math import comb, factorial
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_upstream_cache"
PI_TEXT = "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"
SOS_DEGREES = [0, 1, 1, 1, 2]
NUMBER = re.compile(r"[+-]?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?")


def read_archived_indices(data):
    """Decode this one pinned Julia1.7 Vector{Vector{Int64}} serialization.

    This is deliberately not a general Julia deserializer. It rejects a
    different header, unknown encoding, trailing bytes, or non-index values.
    """
    header = bytes.fromhex("37 4a 4c 0a 04 00 00 00 15 10 50 1f 4e 9b 44 02 00 00 00 00 08 e0 f3")
    assert data.startswith(header)
    offset = len(header)
    vectors = []
    for _ in range(20):
        assert data[offset:offset + 3] == bytes([0x15, 0, 8])
        tag = data[offset + 3]
        if tag == 0x31:
            size = struct.unpack_from("<i", data, offset + 4)[0]
            offset += 8
        else:
            assert 223 <= tag <= 255
            size = tag - 223
            offset += 4
        assert 0 < size <= 168
        vector = list(struct.unpack_from("<" + "q" * size, data, offset))
        offset += 8 * size
        assert vector == sorted(set(vector)) and min(vector) > 0
        vectors.append(vector)
    assert offset == len(data)
    assert vectors[-2:] == [list(range(1, 14))] * 2
    return vectors


def parse_first_blocks(data, count):
    text = data.decode("ascii")
    assert text.startswith("yMat =")
    blocks = []
    depth = 0
    start = None
    for i, char in enumerate(text[text.index("{"):], text.index("{")):
        if char == "{":
            depth += 1
            if depth == 2:
                start = i
        elif char == "}":
            depth -= 1
            if depth == 1:
                blocks.append([Decimal(x) for x in NUMBER.findall(text[start:i + 1])])
                if len(blocks) == count:
                    return blocks, i + 1
    raise ValueError("Partial output did not contain all requested complete blocks")


def basis_exponents(l):
    # Source tv(l), in exactly its Julia comprehension order.
    return [(k, b, a) for k in range(14) for b in range(14) for a in range(14)
            if a + 2 * b + 2 * k <= 13 - l]


def selected_exponents(indices, l, block):
    basis = basis_exponents(l)
    return [basis[i - 1] for i in indices[block]]


def evaluate_sos(block, exponents, u, v, t):
    power = lambda x, n: x**n if n else Decimal(1)
    values = [power(t, k) * power(u * v, b) * power(u + v, a) for k, b, a in exponents]
    size = len(values)
    return sum(block[i * size + j] * values[i] * values[j] * (1 if i == j else 2)
               for i in range(size) for j in range(i, size))


def evaluate_p(blocks, indices, u, v, t):
    sos = []
    for j, l in enumerate(SOS_DEGREES):
        first = evaluate_sos(blocks[2 * j], selected_exponents(indices, l, 2 * j), u, v, t)
        second = evaluate_sos(blocks[2 * j + 1], selected_exponents(indices, l + 1, 2 * j + 1), u, v, t)
        sos.append(first + (u - v)**2 * second)
    return (-sos[0] - (u - 1) * (v - 1) * sos[1] - (u + v - 2) * sos[2]
            - ((u + v - 1)**2 - 4 * t) * sos[3] - t * (u * v - t) * sos[4])


def add_scaled(out, p, factor, shift=0):
    for k, c in enumerate(p):
        out[k + shift] += factor * c


def first_shell_polynomial(blocks, indices):
    """Return coefficients of p(1,1,t), where t=<x,y>^2=c^2."""
    sos = []
    for j in (0, 3, 4):
        exponents = selected_exponents(indices, SOS_DEGREES[j], 2 * j)
        matrix = blocks[2 * j]
        size = len(exponents)
        polynomial = [Decimal(0)] * 27
        for i, (ki, _, ai) in enumerate(exponents):
            for m in range(i, size):
                km, _, am = exponents[m]
                polynomial[ki + km] += matrix[i * size + m] * Decimal(2)**(ai + am) * (1 if i == m else 2)
        sos.append(polynomial)
    out = [Decimal(0)] * 29
    add_scaled(out, sos[0], -1)
    add_scaled(out, sos[1], -1)
    add_scaled(out, sos[1], 4, 1)
    add_scaled(out, sos[2], -1, 1)
    add_scaled(out, sos[2], 1, 2)
    while out and out[-1] == 0:
        out.pop()
    return out


def axis_polynomial(blocks, indices):
    """Return coefficients of p(t=0,u,v=0) in the source squared norm u."""
    sos = []
    for j, l in enumerate(SOS_DEGREES[:4]):
        polynomial = [Decimal(0)] * 29
        for parity in (0, 1):
            exponents = selected_exponents(indices, l + parity, 2 * j + parity)
            matrix = blocks[2 * j + parity]
            size = len(exponents)
            for i, (ki, bi, ai) in enumerate(exponents):
                if ki or bi:
                    continue
                for m in range(i, size):
                    km, bm, am = exponents[m]
                    if km or bm:
                        continue
                    polynomial[ai + am + 2 * parity] += matrix[i * size + m] * (1 if i == m else 2)
        sos.append(polynomial)
    out = [Decimal(0)] * 31
    add_scaled(out, sos[0], -1)
    add_scaled(out, sos[1], -1)
    add_scaled(out, sos[1], 1, 1)
    add_scaled(out, sos[2], 2)
    add_scaled(out, sos[2], -1, 1)
    add_scaled(out, sos[3], -1)
    add_scaled(out, sos[3], 2, 1)
    add_scaled(out, sos[3], -1, 2)
    while out and out[-1] == 0:
        out.pop()
    return out


def axis_integral_at_precision(blocks, indices, precision):
    with localcontext() as ctx:
        ctx.prec = precision
        polynomial = axis_polynomial(blocks, indices)
        for u in (Decimal(0), Decimal("0.5"), Decimal(1), Decimal(2)):
            direct = evaluate_p(blocks, indices, u, Decimal(0), Decimal(0))
            assert abs(direct - horner(polynomial, u)) < Decimal(10)**(-precision + 25)
        pi = Decimal(PI_TEXT)
        source_integral = sum(c * Decimal(factorial(k + 1)) / pi**k for k, c in enumerate(polynomial))
        alpha = 4 * source_integral / polynomial[0]
        return polynomial, alpha, pi**2 / (8 * alpha)


def horner(coefficients, x):
    value = Decimal(0)
    for coefficient in reversed(coefficients):
        value = value * x + coefficient
    return value


def chebyshev_u_decomposition(coefficients):
    """Triangular change of basis from c^(2k) to U_(2k)(c)."""
    residual = list(coefficients)
    result = [Decimal(0)] * len(residual)
    for k in reversed(range(len(residual))):
        coefficient = residual[k] / (4**k)
        result[k] = coefficient
        for j in range(k + 1):
            residual[j] -= coefficient * (-1)**(k - j) * comb(k + j, k - j) * 4**j
    assert max(map(abs, residual)) < Decimal(10)**(-getcontext().prec + 15)
    return result


def run_at_precision(blocks, indices, precision):
    with localcontext() as ctx:
        ctx.prec = precision
        zero = Decimal(0)
        one = Decimal(1)
        origin = evaluate_p(blocks, indices, zero, zero, zero)
        polynomial = first_shell_polynomial(blocks, indices)
        # Independent direct quadratic-form evaluation at diagnostic angles.
        for cosine in (zero, Decimal("0.5"), Decimal("0.75"), one):
            direct = evaluate_p(blocks, indices, one, one, cosine**2)
            collapsed = horner(polynomial, cosine**2)
            assert abs(direct - collapsed) < Decimal(10)**(-precision + 25)
        gaussian = (-2 * Decimal(PI_TEXT)).exp()
        samples = []
        for j in range(201):
            cosine = Decimal(j) / 200
            pvalue = horner(polynomial, cosine**2)
            samples.append((cosine, pvalue, gaussian * pvalue / origin))
        return origin, polynomial, samples


def main():
    indices_data = (CACHE / "latticethreepointdata/indices-13.jls").read_bytes()
    matrix_data = (CACHE / "d4-yMat-first13MB.txt").read_bytes()
    assert hashlib.sha256(indices_data).hexdigest() == "bab8ce29ab11524dea508253a83fdbfca06a0d1ce2f37a026133d4da21c37340"
    assert hashlib.sha256(matrix_data).hexdigest() == "e5b40f2b0616852fe7fd6177dbd353b9b35bfbca93ff5f5e3f0a2a40de92e7d1"
    indices = read_archived_indices(indices_data)
    blocks, consumed = parse_first_blocks(matrix_data, 10)
    for i, block in enumerate(blocks):
        size = len(indices[i])
        assert len(block) == size * size
        assert all(block[a * size + b] == block[b * size + a]
                   for a in range(size) for b in range(size))
    low_origin, low_polynomial, low = run_at_precision(blocks, indices, 60)
    origin, polynomial, high = run_at_precision(blocks, indices, 90)
    stability = max(abs(a[2] - b[2]) for a, b in zip(low, high))
    assert stability < Decimal("1e-40")
    assert abs(origin - Decimal("4.000102455")) < Decimal("1e-15")
    with (HERE / "published_first_shell_slice.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["cosine", "p_in_authors_r1_normalization", "f_with_origin_one", "required_nonpositive"])
        for c, p, f in high:
            writer.writerow([str(c), str(p), str(f), c <= Decimal("0.5") or c == 1])
    selected = [high[j] for j in (0, 50, 100, 120, 140, 150, 160, 180, 190, 200)]
    with localcontext() as ctx:
        ctx.prec = 60
        low_angular = chebyshev_u_decomposition(low_polynomial)
        low_factor = (-2 * Decimal(PI_TEXT)).exp() / low_origin
        low_angular_normalized = [c * low_factor for c in low_angular]
    with localcontext() as ctx:
        ctx.prec = 90
        angular = chebyshev_u_decomposition(polynomial)
        factor = (-2 * Decimal(PI_TEXT)).exp() / origin
        angular_normalized = [c * factor for c in angular]
        inferred_fourier_origin = Decimal(16) / origin
        packing_fraction = Decimal(PI_TEXT)**2 / 32 * origin.sqrt()
    angular_stability = max(abs(a - b) for a, b in zip(low_angular_normalized, angular_normalized))
    assert angular_stability < Decimal("1e-40")
    _, low_alpha, _ = axis_integral_at_precision(blocks, indices, 60)
    axis_coefficients, alpha, axis_bound = axis_integral_at_precision(blocks, indices, 90)
    axis_stability = abs(low_alpha - alpha)
    assert axis_stability < Decimal("1e-40")
    with (HERE / "published_angular_sectors.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["angular_degree", "coefficient_of_U_in_authors_polynomial", "coefficient_of_U_in_origin_one_function"])
        writer.writerows((2 * k, str(a), str(b)) for k, (a, b) in enumerate(zip(angular, angular_normalized)))
    summary = dict(
        status="HIGH_PRECISION_FLOATING_INSPECTION_NOT_RIGOROUS_VERIFICATION",
        source_archive_url="https://dspace.mit.edu/server/api/core/bitstreams/3ad1c7a0-ced0-45b8-8070-310dccc2190c/content",
        source_member="ThreePointSpherePacking/latticethreepointdata/4-13-1024-2-300-1e-20-0.5-4.000102455.sdpa-out",
        source_member_offset=998708224, ymat_relative_offset=22974632,
        retrieved_matrix_range_bytes=len(matrix_data), bytes_through_tenth_complete_block=consumed,
        matrix_range_sha256=hashlib.sha256(matrix_data).hexdigest(),
        indices_sha256=hashlib.sha256(indices_data).hexdigest(),
        matrix_dimensions=[len(v) for v in indices[:10]],
        matrix_entries=sum(len(block) for block in blocks),
        origin_value=str(origin), target_origin_value="4.000102455",
        origin_residual=str(origin - Decimal("4.000102455")),
        inferred_fourier_origin_after_rescaling=str(inferred_fourier_origin),
        density_from_stored_objective=str(packing_fraction),
        decimal_precisions_compared=[60, 90], maximum_sample_difference=str(stability),
        maximum_angular_coefficient_difference=str(angular_stability),
        normalized_axis_integral=str(alpha), axis_integral_precision_difference=str(axis_stability),
        axis_only_density_expression=str(axis_bound),
        normalization="authors: r=1, fhat(0)=1; plotted F(x,y)=f(x/sqrt(2),y/sqrt(2))/f(0), so F(0)=1",
        maximum_sample=dict(cosine=str(max(high, key=lambda row: row[2])[0]),
                            value=str(max(row[2] for row in high))),
        selected_samples=[dict(cosine=str(c), p=str(p), normalized_f=str(f)) for c, p, f in selected],
        angular_average_after_normalization=str(angular_normalized[0]),
        angular_decomposition=[dict(ell=2 * k, normalized_coefficient=str(value))
                               for k, value in enumerate(angular_normalized)],
        first_shell_polynomial_coefficients_in_squared_cosine=[str(c) for c in polynomial],
        axis_polynomial_coefficients_in_source_squared_norm=[str(c) for c in axis_coefficients],
    )
    (HERE / "published_slice_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if "polynomial_coefficients" not in k}, indent=2))


if __name__ == "__main__":
    main()
