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
region for a shell relaxation is controlled by `n·M/f̂(0)`, and the count `n` may be taken as
`⌊(3+δ)³⌋ − 1` for a shell of width `δ` (K15-C013(a), a volume bound). That is an
*upper* bound on the contact number, not a lower one. The true maximum is
exactly 12 for all sufficiently thin shells (K15-C013(b), compactness plus the
kissing number); an explicit width is open.

## 3. One obstruction, one withdrawal (K15-C004, K15-C005)

- **Contact-sphere relaxation is vacuous (K15-C004, stands).** If `A` has empty
  interior then `R³∖A` is dense, so a continuous `f` that is `≤ 0` on
  `{|x| ≥ 2}∖A` is `≤ 0` on `{|x| ≥ 2}`. Pricing `f > 0` on `{|x| = 2}` by the
  kissing number 12 cannot improve any two-point constant. (At checkpoint 1 this
  entry was marked refuted by Main on the strength of a bad example; the review
  is right and the entry is restored.)
- **Additive two-point corrections to Voronoi volume (K15-C005): obstruction
  WITHDRAWN, route re-opened.** The two computations are real — the
  positive-definite correction is `≥ κf̂(0)/(4√2) > 0` at the icosahedral cell
  and has non-positive mean — but they do not exclude the family: in
  `V_0 ≤ vol Ω(v) + κB_κ(v)` a positive value at the icosahedral configuration
  *permits* a larger `V_0`. No bound is obtained, in either direction.

## 4. The frontier, fixed in one place (K15-C008)

`0.740480` (Kepler, Hales) < `0.754697` (dodecahedral, Hales–McLaughlin) <
`0.770271` (three-point, CDS22) < `0.773055` (Muder 1998) < **`0.779636`
(Rogers 1958) < `0.779747` (Cohn–Elkies 2003)**. The last two are in the right
order as written and the two-point bound is the *worse* of them; checkpoint 1
had them transposed. `0.741506` (CDS22) is **lattice-only** and is not a general
bound. No novelty is claimed for anything in this file: the unrestricted sharp
bound is already a theorem (Hales), and "first below 0.754697" would be a claim
about a restricted class that has not been compared with the literature.

## 5. What is not established

- No new numerical bound has been produced in this project. CDS22 Table 1.1
  values have not been reproduced locally (`K15-COMPUTE-001`).
- Li's `0.18398089` is quoted, not reproduced.
- The recovered sharpness/uniqueness material is unreviewed and partly
  retracted (`Literature/RECOVERED.md`).
- No Lean module has been kernel-checked under the pinned toolchain.
