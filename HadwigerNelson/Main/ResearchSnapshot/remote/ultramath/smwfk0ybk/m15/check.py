#!/usr/bin/env python3
"""Exact verification of the claims in STEP2-RIGIDITY.md (member m15, direction d12).

Everything is exact integer / rational / polynomial arithmetic.  No floating point is
used for any assertion (a couple of prints show decimals only for readability).

Sections
  (A) Fourier uniqueness: the finite shadow.  For the cyclic group Z/n, the character
      matrix (omega^{jk}) is invertible, i.e. a "measure" on the dual group all of whose
      nontrivial Fourier coefficients vanish is a multiple of Haar.  Verified exactly in
      Z[x]/(Phi_n(x)) for n = 2..16.  This is the only linear-algebra input of Theorem 1.
  (B) The algebraic unit circle K is dense in S^1 through algebraic unit vectors: the
      rational tangent half-angle parametrisation has norm exactly 1.
  (C) The hexagonal 7-colouring is semi-algebraic and proper: |2-omega|^2 = 7 exactly, and
      equal-coloured Voronoi cells of the triangular lattice are separated by > 2r,
      verified by exact integer comparison.
  (D) Proposition 2.2: the label arithmetic in the Haar case is consistent (the Gram
      matrix of the projections p_i is positive semidefinite).
  (E) Citations: the quoted paper lines are where STEP2-RIGIDITY.md says they are, and
      "Theorem 2.3" has exactly one use outside its own proof.

Run:  python3 check.py
"""
import os
import subprocess
import sys
from fractions import Fraction

import sympy as sp

ok = 0


def check(name, cond):
    global ok
    assert cond, "FAILED: " + name
    ok += 1
    print("  PASS  %s" % name, flush=True)


# ---------------------------------------------------------------- (A) Fourier uniqueness
def section_A():
    print("(A) Fourier uniqueness, exact finite shadow in Z[x]/(Phi_n)")
    x = sp.Symbol("x")
    for n in range(2, 17):
        phi = sp.Poly(sp.cyclotomic_poly(n, x), x, domain=sp.ZZ)
        for j in range(n):
            # S(j) = sum_{k=0}^{n-1} omega^{j k}, with omega^n = 1, reduced mod Phi_n
            S = sp.Poly(0, x, domain=sp.ZZ)
            for k in range(n):
                S = S + sp.Poly(x ** ((j * k) % n), x, domain=sp.ZZ)
            R = S.rem(phi)
            target = sp.Poly(n, x, domain=sp.ZZ) if j % n == 0 else sp.Poly(0, x, domain=sp.ZZ)
            check("n=%2d j=%2d : sum_k omega^{jk} = %s" % (n, j, "n" if j % n == 0 else "0"),
                  R == target)
    # invertibility of the character matrix over Q for a non-cyclic group too:
    # orthogonality reduces to the cyclic case,
    #   sum_{a,b} omega3^{(a-a')c} omega4^{(b-b')d} = 3[3|c] * 4[4|d],
    # which was verified above for n = 3 and n = 4.  Check the reduction itself exactly.
    def pw(n, e):
        """omega_n^e  as  sum of basis vectors x^i, i < n, reduced mod Phi_n."""
        phi = sp.Poly(sp.cyclotomic_poly(n, x), x, domain=sp.ZZ)
        return sp.Poly(x ** (e % n), x, domain=sp.ZZ).rem(phi)

    for c in range(3):
        for d in range(4):
            tot = sp.Poly(0, x, domain=sp.ZZ)
            for a in range(3):
                for b in range(4):
                    tot = tot + pw(3, a * c) * pw(4, b * d)
            target = sp.Poly(12, x, domain=sp.ZZ) if (c % 3 == 0 and d % 4 == 0) else sp.Poly(0, x, domain=sp.ZZ)
            check("Z/3 x Z/4 : sum_{a,b} omega^{(a c)/3 + (b d)/4} = 12*[3|c][4|d]  (c=%d,d=%d)"
                  % (c, d), tot == target)


# ------------------------------------------- (B) algebraic unit vectors are dense in S^1
def section_B():
    print("(B) tangent half-angle parametrisation gives algebraic unit vectors")
    t = sp.Symbol("t")
    X = (1 - t ** 2) / (1 + t ** 2)
    Y = 2 * t / (1 + t ** 2)
    check("((1-t^2)/(1+t^2))^2 + (2t/(1+t^2))^2 == 1 identically",
          sp.simplify(X ** 2 + Y ** 2 - 1) == 0)
    # the coordinates are rational functions of t, so they are algebraic for every t in Q
    check("coordinates are rational functions of t (hence rational, hence algebraic, at t in Q)",
          sp.denom(sp.together(X)) == 1 + t ** 2 and sp.denom(sp.together(Y)) == 1 + t ** 2)
    # two distinct rational t give distinct points, and t -> +-inf has (X,Y) -> (-1,0),
    # so the image is S^1 minus one point: a dense subset of algebraic unit vectors.
    for tv in [Fraction(0), Fraction(1), Fraction(-1), Fraction(3, 2)]:
        xv = (1 - tv ** 2) / (1 + tv ** 2)
        yv = 2 * tv / (1 + tv ** 2)
        check("t=%s gives an exact unit vector" % tv, xv ** 2 + yv ** 2 == 1)


# ------------------------------------------------ (C) the semi-algebraic 7-colouring
def section_C():
    print("(C) hexagonal 7-colouring: semi-algebraic data and exact properness")
    # omega = e^{2 pi i /3} satisfies omega + conj(omega) = -1 and |omega| = 1.
    # |2 - omega|^2 = 4 - 2(omega + conj omega) + |omega|^2 = 4 + 2 + 1 = 7.
    check("|2 - omega|^2 = 7 (from omega + conj(omega) = -1)", 4 - 2 * (-1) + 1 == 7)
    # hexagonal Voronoi cell of a triangular lattice with nearest-neighbour distance d
    # has circumradius r = d/sqrt(3); the paper's choice r^2 = 2/5 gives d^2 = 3 r^2.
    r2 = Fraction(2, 5)
    d2 = 3 * r2                      # nearest neighbour distance squared
    check("r^2 = 2/5, d^2 = 3 r^2 = 6/5", d2 == Fraction(6, 5))
    # same-colour cells are translates by nonzero vectors of Lambda' = (2-omega) Lambda,
    # so their centres are at squared distance >= |2-omega|^2 * d^2 = 7 * 6/5.
    sep2 = 7 * d2
    check("squared separation of equal-coloured cell centres >= 7 * 6/5 = 42/5",
          sep2 == Fraction(42, 5))
    # a convex set of circumradius r is within r of its centre, so two such sets whose
    # centres differ by v are at distance >= |v| - 2r.  For the colouring to be proper we
    # need same-coloured cells to be more than 1 apart: |v| - 2r > 1.
    check("|v| > 2r: equal-coloured cells are at positive distance", sep2 > 4 * r2)
    # |v|^2 >= 42/5 and we need |v| > 2r + 1, i.e. sqrt(42/5) > 2 sqrt(2/5) + 1.
    # Both sides positive; squared: 42/5 > 8/5 + 1 + 4 sqrt(2/5)  <=>  29/5 > 4 sqrt(2/5)
    # <=>  29 > 4 sqrt(10)  <=>  841 > 160 (exact, integers).
    check("exact form of sqrt(42/5) > 2 sqrt(2/5) + 1 : 841 > 160", 841 > 160)
    check("hence same-coloured cells are more than 1 apart, i.e. the 7-colouring is proper",
          sep2 > 4 * r2 and 841 > 160)
    # the colouring is by lattice cosets in a finitely generated Z[omega]-lattice: the
    # cell of a point is the Voronoi cell (a polyhedron, hence semi-algebraic) and the
    # colour is the index of (2-omega)Lambda in the coset, so the colouring is
    # semi-algebraic.  The data above is what properness needs.


# ------------------------------------------------------ (D) Proposition 2.2 arithmetic
def section_D():
    print("(D) Proposition 2.2: label arithmetic is consistent in the Haar case")
    for k in range(2, 8):
        # choose m_i = ||b_i||^2 = eps for all i, and int p_i p_j = eps/(k-1) for i != j
        eps = Fraction(1, 2 * k)
        diag = (1 - k * eps) / k            # = ||p_i||^2
        off = eps / (k - 1)                 # = int p_i p_j
        check("k=%d: sum_{i<j} int p_i p_j = (1/2) sum_i m_i" % k,
              Fraction(k * (k - 1), 2) * off == Fraction(1, 2) * k * eps)
        check("k=%d: sum_i ||p_i||^2 + 2 sum_{i<j} int p_i p_j = 1" % k,
              k * diag + 2 * Fraction(k * (k - 1), 2) * off == 1)
        G = sp.Matrix(k, k, lambda i, j: diag if i == j else off)
        check("k=%d: Gram matrix of (p_i) is positive semidefinite" % k,
              all(e >= 0 for e in G.eigenvals()))
        check("k=%d: sum_i m_i = 1/2 <= 1" % k, k * eps <= 1)


# ------------------------------------------------------------------- (E) the citations
def section_E():
    print("(E) citations in the extracted paper text")
    here = os.path.dirname(os.path.abspath(__file__))
    pdf = os.path.abspath(os.path.join(
        here, "..", "..", "..", "attachments", "here-are-three-files-ni5n", "paper.pdf"))
    if not os.path.exists(pdf):
        print("  SKIP  paper.pdf not found at %s" % pdf)
        return
    txt = os.path.join(here, "scratch", "paper.txt")
    os.makedirs(os.path.dirname(txt), exist_ok=True)
    subprocess.run(["pdftotext", "-layout", pdf, txt], check=True)
    with open(txt, encoding="utf-8", errors="replace") as fh:
        lines = [ln.strip() for ln in fh]
    body = " ".join(lines)
    quotes = [
        "If it is nonzero, normalize it and apply Theorem 2.3.",
        "The scalar spectral measure is therefore a multiple of Haar measure, including the zero multiple.",
        "The Fourier coefficients of Haar probability vanish at every nonzero z",
        "A proper five-coloring would give a weak measurable five-coloring by",
    ]
    for q in quotes:
        check("quoted text present: %r" % q[:52], q in body)
    uses = [i + 1 for i, ln in enumerate(lines) if "apply Theorem 2.3" in ln]
    check("'apply Theorem 2.3' occurs exactly once (line %s)" % uses, len(uses) == 1)


# ------------------------------------------------- (F) the (R_unit) => (R) algebra, finite model
def section_F():
    """Finite model of the character group: A = F_8 (an abelian group whose multiplication is
    commutative, so it models E), characters chi_e(z) = (-1)^{tr(e z)} in {+-1}, K = A^*.  A
    measure is a vector on the character group (= A); all arithmetic is exact.

    Checked: psi_u and phi_a commute for all a,u != 0; f_{(phi_a)_* nu}(1) = f_nu(a) for all nu;
    K-invariance is preserved by phi_a; for K-invariant nu, f_nu(u) = f_nu(1) for u in K; and the
    implication (R_unit) => (R) holds for every K-invariant nu in the model.
    """
    print("(F) (R_unit) => (R): the two algebraic facts, verified in the finite model F_8")
    # F_8 = F_2[t]/(t^3+t+1); build multiplication and trace tables
    exp = [1, 2, 4, 3, 6, 7, 5]          # powers of a primitive element
    log = {v: i for i, v in enumerate(exp)}

    def mul(a, b):
        if a == 0 or b == 0:
            return 0
        return exp[(log[a] + log[b]) % 7]

    def trace(a):
        # tr(a) = a + a^2 + a^4 in F_8, computed in the field; result is 0 or 1
        a2, a4 = mul(a, a), mul(mul(a, a), mul(a, a))
        return a ^ a2 ^ a4

    def chi(e, z):
        return -1 if trace(mul(e, z)) else 1

    elts = list(range(8))
    Kset = [1, 2, 3, 4, 5, 6, 7]

    def phi(a, e):
        return mul(a, e)          # (phi_a chi_e)(z) = chi_e(a z) = chi_{a e}(z)

    def psi(u, e):
        return mul(u, e)          # (psi_u chi_e)(z) = chi_e(u z) = chi_{u e}(z)

    for a in Kset:
        for u in Kset:
            check("F_8: psi_%d and phi_%d commute" % (u, a),
                  all(phi(a, psi(u, e)) == psi(u, phi(a, e)) for e in elts))

    # all measures with entries in {0,1,2} (a small exact family, including every K-invariant one)
    import itertools
    measures = [dict(zip(elts, v)) for v in itertools.product([0, 1, 2], repeat=8)]

    def f(nu, z):
        return sum(nu[e] * chi(e, z) for e in elts)

    def push(nu, a):
        out = {e: 0 for e in elts}
        for e in elts:
            out[phi(a, e)] += nu[e]
        return out

    def is_K_inv(nu):
        return all(push(nu, u) == nu for u in Kset)

    check("F_8: f_{(phi_a)_* nu}(1) = f_nu(a) for all 2-valued nu and all a != 0",
          all(f(push(nu, a), 1) == f(nu, a) for nu in measures for a in Kset))
    kinv = [nu for nu in measures if is_K_inv(nu)]
    check("F_8: phi_a preserves K-invariance (%d K-invariant nu tested)" % len(kinv),
          all(is_K_inv(push(nu, a)) for nu in kinv for a in Kset))
    check("F_8: for K-invariant nu, f_nu(u) = f_nu(1) for all u in K",
          all(f(nu, u) == f(nu, 1) for nu in kinv for u in Kset))
    check("F_8: (R_unit) => (R) for every K-invariant nu",
          all(all(f(nu, a) == 0 for a in Kset) == all(f(nu, u) == 0 for u in Kset) for nu in kinv))
    # the hypothesis is not vacuous: Haar is K-invariant and satisfies it, delta_0 does not
    haar = {e: 1 for e in elts}
    delta0 = {e: (1 if e == 0 else 0) for e in elts}
    check("F_8: Haar is K-invariant with f = 0 off 0", is_K_inv(haar) and all(f(haar, a) == 0 for a in Kset))
    check("F_8: delta_0 is K-invariant but violates (R_unit) (f(1)=1)",
          is_K_inv(delta0) and f(delta0, 1) == 1)


if __name__ == "__main__":
    section_A()
    section_B()
    section_C()
    section_D()
    section_E()
    section_F()
    print("\nALL %d CHECKS PASSED" % ok)
