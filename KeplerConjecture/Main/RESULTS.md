# Strongest current results — Kepler problem 15

Checkpoint 2026-11-14 (cycle 1). This file states only what survives review at
this checkpoint. Nothing here is a proof of the Kepler bound; see
`Main/CLAIMS.md` for statuses.

## 1. A complete, self-contained proof of the two-point bound for all packings (K15-C002)

Cohn–Elkies' Theorem 3.1 is stated for all packings but proved for periodic
ones, with the reduction relegated to an appendix. The recovered proof
(`.ultramath/smwg019eu/m2/proof.md`) supplies the missing step as an explicit
estimate:

- **Lemma 1.2 (periodic approximation).** For every packing `Λ` with minimum
  separation 2 and every `ε > 0` there is a periodic packing `Π` with
  `δ(Π) ≥ δ(Λ) − ε`. Proof: tile by cubes of side `S`, take the tile with the
  most centres, delete the two-unit slabs at its boundary, and periodise. Losses
  are `O(S/R) + O(1/S)`, both explicit; no saturation, ergodicity or limiting
  density is assumed.
- **Lemma 1.3.** Poisson summation for `k` translates produces
  `|Σ_j e^{2πi⟨v_j,t⟩}|² ≥ 0`, so multiple translates are covered.
- **Conclusion.** `c(Λ) ≤ f(0)/f̂(0)`, i.e. `δ(Λ) ≤ (4π/3)f(0)/f̂(0)`.

Status: `PROPOSED`; Main read the argument and found it complete; X's
independent review is outstanding. Value: clarity, not a new constant.

## 2. The hybrid two-point bound with a local-count price (K15-C003)

**Theorem B.** If `f` is admissible, `f̂ ≥ 0`, and `f > 0` only on a set `A` with
contact number `n` (at most `n` `A`-differences from any centre of any
2-separated set), with `max_A f ≤ M`, then
`c(Λ) ≤ (f(0) + n·max(M,0))/f̂(0)` for every packing.

This replaces the unprovable "integral tail" of the earlier brief by a finite
count. Consequences already verified: `A = ∅` recovers (1); relaxing on a closed
measure-zero set (the contact sphere) buys nothing (K15-C004/C011); the winning
region for a shell relaxation is controlled by `n·M/f̂(0)`, and `n ≥ 26` for
every shell of positive width under the elementary volume bound
`n(δ) = ⌊(3+δ)³⌋ − 1` (Corollary 2.3).

## 3. Two obstructions that retire routes (K15-C004, K15-C005)

- **Contact-sphere relaxation is vacuous** (correct statement: `A` closed and of
  empty interior). Pricing `f > 0` on `{|x| = 2}` by the kissing number 12
  cannot improve any two-point constant.
- **Additive two-point corrections to Voronoi volume cannot beat 5.550291.**
  At the icosahedral cell the positive-definite correction is `≥ κf̂(0)/(4√2) > 0`
  (so it raises the required cell volume) and on average it is `≤ −κc f̂(0) < 0`
  (wrong sign). Hence `V_0 < V_HM` for every `κ > 0`: the family is strictly
  worse than Hales–McLaughlin. `verify.py` reproduces every constant.

## 4. The frontier, fixed in one place (K15-C008)

`0.740480` (Kepler, Hales) < `0.754697` (dodecahedral, Hales–McLaughlin) <
`0.770271` (three-point, CDS22) < `0.773055` (Muder) < `0.779747` (CE) <
`0.779636` (Rogers). Any new bound below `0.754697399337` is the first of its
kind; `0.741506` (CDS22) is **lattice-only** and is not a general bound.

## 5. What is not established

- No new numerical bound has been produced in this project. CDS22 Table 1.1
  values have not been reproduced locally (`K15-COMPUTE-001`).
- Li's `0.18398089` is quoted, not reproduced.
- The recovered sharpness/uniqueness material is unreviewed and partly
  retracted (`Literature/RECOVERED.md`).
- No Lean module has been kernel-checked under the pinned toolchain.
