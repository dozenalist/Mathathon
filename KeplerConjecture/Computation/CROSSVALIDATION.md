# Bidirectional cross-validation of the two exact pipelines

Two exact checkers exist in this project, written by different sessions, in different bases,
sharing no code:

| | Computation | Main / X |
| --- | --- | --- |
| basis | Laguerre in `t = 2π|x|²` | monomial in `u = π|x|²` |
| sign decision | own Sturm chain + Yun squarefree decomposition over `Fraction` | SymPy `sturm` / `count_roots` |
| Fourier map | diagonal `(−1)^k` in the Laguerre basis | rational matrix `M`, `M[0][k] = (2k+1)!!/2^k` |
| files | `exactcert.py`, `exactcert_oracle.py` | `shell_check.py` |

## Direction 1 — my certificate, Main's checker

The degree-33 certificate `out/verified_certificate_K33b.json` (`Δ ≤ 0.77996622`), produced by
the Laguerre pipeline and accepted by both of my exact implementations, was converted exactly to
monomial-`u` coefficients and given to `shell_check`:

* `T_LO = 12` (its default): **rejected**, on the shell predicate only — because `12 < 4π`, so it
  demands `p ≤ 0` inside the ball, which CE never requires.
* `T_LO = 4·π_lo`: **accepted**, `Δ ≤ 0.77996622`.

## Direction 2 — a shell certificate, my checker

The reverse direction, which is the stronger test because it uses a certificate the monomial
pipeline produced. Take a degree-33 shell certificate from `shell_propose`, convert its monomial
coefficients back to the Laguerre basis by solving the triangular system
`p(u) = Σ_k c_k L_k^{(1/2)}(2u)`, and run my `exactcert.certify` in strict mode:

```
my checker on the shell certificate : ok = True
my Delta upper bound                : 0.780338357535
shell_check's own value             : 0.780338357611...
```

Agreement to ten significant digits, in strict mode and in the even-multiplicity mode.

## What this establishes

1. **Neither pipeline has a basis-conversion, normalisation or sign-convention error that the
   other would miss.** A wrong factor in `M`, a wrong `π` enclosure direction, or a mis-mapped
   `t ↔ u` would break one of the two directions.
2. The `shell_check` Fourier matrix is correct — independently confirmed by
   `audit_fourier.py` (exact matrix agreement, `M² = I`, and direct quadrature to `1e-13`) and
   now also by a real certificate passing through both bases.
3. Both certificates can be quoted by Main with the other session's checker as the reviewing
   implementation, which is what the roadmap asks for ("exact rational identity, verified by an
   independent checker").

## Caveat

Direction 1 exposes that `shell_check`'s `T_LO = 12` default is *sound but pessimistic*: it can
only ever reject valid certificates, never accept invalid ones. Direction 2 shows the reverse
inclusion holds on a real object, so the two checkers agree on the substance and differ only in
that conservative threshold (`TLO_FINDING.md`).
