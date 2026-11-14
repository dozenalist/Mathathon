# Claim ledger — Kepler problem 15

Maintained by **M (Main)**. Every mathematical assertion in this project that is
used in an argument or a comparison gets an ID. Status vocabulary:

`PROPOSED` · `TESTED_FINITE` · `PROVED` · `LEAN_VERIFIED` · `LEAN_CONDITIONAL` ·
`REFUTED` · `BLOCKED` · `PENDING_REVIEW` (recovered material, not yet audited).

`PROVED` requires a complete written argument with justified dependencies and an
**independent** reviewer who is not the author. `TESTED_FINITE` means a finite
check passed; it says nothing about global signs, tails, or arbitrary packings.
Main's own reading is recorded as `main_audit` and never substitutes for the
named reviewer.

Contract (frozen 2026-11-14, K15-C001): unit balls (radius 1), packing centres
`Λ ⊂ R³` with `|x−y| ≥ 2`, `δ(Λ)` = upper occupied-volume density,
`c = δ/(4π/3)`, `f̂(t) = ∫ f(x) e^{−2πi⟨x,t⟩} dx`. Conversions from the older
minimum-separation-1 convention are in K15-C007.

---

## K15-C001 — mathematical contract and density normalisation

- **Statement.** For a packing `Λ` with `|x−y| ≥ 2`, `δ(Λ) = limsup_R vol(B(0,R) ∩ ⋃_{λ∈Λ} B(λ,1))/vol B(0,R)`,
  `c(Λ) = δ(Λ)/vol(B_1) = 3δ/(4π)`, `vol(B_1) = 4π/3`, `f̂(t) = ∫ f(x)e^{−2πi⟨x,t⟩}dx`.
- **Status.** `PROVED` (definitional). **Owner** M. **Reviewer** X.
- **Evidence.** `ROADMAP.md` §2; `Literature/PROBLEM_SPEC.md`.
- **Obligation.** Any worker result stated in another scale must carry its
  conversion (K15-C007) in the same paragraph.

## K15-C002 — two-point bound for all packings  [proof gap found; corrected version C002b]

- **Statement (corrected hypotheses, review objection 5).** Let `f: R³ → R` be
  continuous with `f̂` continuous, both satisfying `|f(x)|, |f̂(x)| ≤ C(1+|x|)^{−3−η}`
  for some `η > 0` (this decay gives `f, f̂ ∈ L¹` and hence continuity of each
  other's transform; decay alone, without the transform being defined, gives
  nothing). Assume `f(x) ≤ 0` for `|x| ≥ 2`, `f̂ ≥ 0` everywhere, **and
  `f̂(0) > 0`**. Then `c(Λ) ≤ f(0)/f̂(0)` and `δ(Λ) ≤ (4π/3) f(0)/f̂(0)` for
  every packing with minimum separation 2.
  *Why `f̂(0) > 0` is a separate hypothesis:* `f̂ ≥ 0` and `f ≢ 0` give
  `f̂(0) = ∫f ≥ 0`, not `> 0`; and `f(0) > 0` does not help either (`f(0) = ∫f̂`
  can be positive while `∫f = 0`). Without it the ratio `f(0)/f̂(0)` is not
  defined or has the wrong sign.
- **Attribution.** Cohn–Elkies, *New bounds on sphere packings I*, Annals 157
  (2003) 689–714, Theorem 3.1 (proved there for periodic packings, with the
  reduction to arbitrary packings in an appendix).
- **New content (recovered, `smwg019eu` m2).** A complete proof of the
  reduction: rotation averaging (Lemma 1.1); **Lemma 1.2**, a periodic
  approximation with explicit losses `O(S/R) + O(1/S)`, needing neither
  saturation nor periodicity of `Λ`; Lemma 1.3, the Poisson computation with
  `|Σ_j e^{2πi⟨v_j,t⟩}|² ≥ 0`; conclusion (1.4.1).
- **Status.** `PROPOSED` (author m2). **main_audit:** read Lemmas 1.1–1.3 and
  the conclusion in full; the argument is correct as written and the constants
  are quantitative. My earlier brief (`Roadmaps/dim-3-analytic-bound-prompt.md`
  §5.1) asserted "for k > 1 the phases do not cancel" — that is **wrong**, see
  K15-C009.
- **Reviewer.** X. **Artifacts.** `.ultramath/smwg019eu/m2/proof.md`,
  `m2/verify.py` (41 checks, `m2/verify_output.txt`).
- **Remaining.** Independent review; no Lean claim yet. Value: this is the one
  place where "clarity" costs nothing — the appendix step is replaced by an
  explicit two-loss estimate a referee can audit in a page.

## K15-C003 — truncated/hybrid two-point bound with a *count* price  [indexing gap; corrected C003r]

- **Statement (Theorem B).** Let `f` satisfy the hypotheses of K15-C002
  (`f, f̂` continuous, the decay bound, `f ≤ 0` off `|x| ≥ 2` away from `A`,
  `f̂ ≥ 0`, `f̂(0) > 0`); let
  `A ⊂ R³∖{0}` have **contact number** `n` (every 2-separated set has at most
  `n` points at an `A`-difference from any of its points); let `M ≥ max_{A} f`
  and `f ≤ 0` off `A` on `{|x| ≥ 2}`. Then every packing satisfies
  `c(Λ) ≤ (f(0) + n·max(M,0))/f̂(0)`.
- **Significance.** The price of admitting `f > 0` on a set is a *local count*,
  never an integral. This is the only provable form found; it strictly
  generalises K15-C002 (`A = ∅`, `n = 0`).
- **Status.** `PROPOSED`. **main_audit:** the "bad indices" split is correct;
  the bijection `(x,l) ↦ (v_l, x+v_j)` reduces the count to `(LC(A,n))` applied
  to the `k` centres of one fundamental domain, giving `≤ nk`. Sound.
- **Reviewer.** X. **Artifacts.** `m2/proof.md` §2; `m2/verify.py` §D–E.
- **Remaining.** X must test `(LC(A,n))` on Barlow/HCP clusters and check
  whether any admissible `f` with a useful `A` exists at all
  (Corollary 2.4 says the winning region is small).

## K15-C004 — "relax the sign condition on the contact sphere" is vacuous  [RESTORED]

- **Statement.** Let `A ⊂ R³∖{0}` have empty interior, and let `f` be continuous
  with `f ≤ 0` on `{|x| ≥ 2} ∖ A`. Then `f ≤ 0` on `{|x| ≥ 2}`. Consequently the
  relaxation of K15-C003 with `A` of empty interior buys **nothing**: K15-C002
  applies with the better constant.
- **Proof.** If `A` has empty interior then `R³ ∖ A` is dense in `R³`. The set
  `{|x| > 2}` is open, so `{|x| > 2} ∖ A` is dense in `{|x| > 2}`; on it `f ≤ 0`
  by hypothesis, so by continuity `f ≤ 0` on the closure `{|x| ≥ 2}`. ∎
- **Status.** `PROPOSED` (author m2, `smwg019eu`), **correct as stated**.
  **Correction of the correction:** Main's previous checkpoint marked this
  `REFUTED` with "counterexample" `A = Q³ ∩ {|x| ≥ 2}`. That was an error by
  Main: `Q³` has empty interior, and the complement of *any* set with empty
  interior is dense, which is precisely the hypothesis the proof needs. The
  rationals are not a counterexample; there is no counterexample. Closedness of
  `A` is unnecessary. Review objection 1 is accepted; K15-C011 is withdrawn.
- **Reviewer.** X. **Artifact.** `Main/Evidence/m2-proof.md` Corollary 2.2.
- **Consequence.** The contact-sphere route stays closed (D5) — now for the
  right reason, which survives review.

## K15-C005 — additive two-point score hybrids: third correction, valid obstruction restored

- **What was claimed at checkpoint 1.** That a hybrid of the shape
  "`vol Ω(v) ≥ V_0 − κ B_κ(v)`" cannot reach `V_0 > V_HM`, on the grounds that
  `B_κ(ico) > 0`.
- **Status.** `REFUTED` — the claimed obstruction is **invalid**, and the route is
  re-opened. The inequality rearranges to `V_0 ≤ vol Ω(v) + κ B_κ(v)`; at the
  icosahedral cell a **positive** `B_κ` therefore *permits a larger* `V_0`, and a
  negative average of `B_κ` *strengthens* the global volume inequality. Main
  transcribed the sign backwards from the swarm's Theorem C(i). Review
  objection 3 accepted.
- **What does remain established** (raw computations, `Main/Evidence/m1-certificate.json`,
  `m1-verify.py`, re-run: 30/30 checks):
  (i) `B_κ(ico) = κ(f(0) + 12f(2)) ≥ κ f̂(0)/(4√2) > 0` for every admissible `f`
  (Poisson summation at fcc, i.e. the fcc sum rule);
  (ii) `mean_v B_κ ≤ 0` for periodic packings (positive-definiteness).
  These are two facts with **opposite** signs at the icosahedral configuration
  versus the average — which is exactly the shape of a Hales-style argument and
  not, by itself, an obstruction.
- **What would actually be needed** to reopen or close it: a statement about how
  often near-icosahedral cells can occur in a packing, since negligibility
  (K15-C002-style averaging) controls `Σ_v A(v)` only from above. That is the
  hard part of the Kepler proof, not a corollary.
- **Reviewer.** X. **Owner** M (withdrew its own claim).

## K15-C006 — ordinary Cohn–Elkies is not sharp in dimension 3

- **Statement.** The optimum of the ordinary CE linear program in `d = 3` is
  `> 0.18398089` in centre-density units, while `π/√18` corresponds to
  `2^{−5/2} = 0.176776695…`. Hence no choice of admissible `f` proves the sharp
  bound.
- **Attribution.** R. Li, *Dual linear programming bounds for sphere packing via
  discrete reductions*, Adv. Math. 460 (2024) 110043, arXiv:2206.09876v3, §6
  Theorem 6.1. Primary source retained at `Literature/Papers/Li2022-v3.pdf`.
- **Status.** `PROVED` (published, used as a black box). **Local reproduction
  of the numerical value:** not done — no local computation exists for it.
- **Reviewer.** X. **Obligation.** Any exact route must add information beyond
  ordinary CE; state which.

## K15-C007 — normalisation bridge (minimum separation 1 ↔ 2)

- **Statement.** Let `n` be a centre number density with minimum separation 1
  and balls of radius `1/2`. Then with radius 1 / separation 2 the same
  configuration has `c = n/8` and `δ = (π/6)·n`. In particular
  `δ = (4π/3)c` always, `n_fcc = √2`, `c_fcc = 1/(4√2) = 0.176776695…`,
  `δ_fcc = π/√18`.
- **Status.** `PROVED` (elementary). **Verified numerically** in
  `smwg019eu/m1/verify.py` item F1 (interval width 1e−25) and
  `smwg019eu/m2/verify.py` §D.
- **Consequence.** Older Kepler notes in this project (e.g. `smwfyzz1k` m6/m7)
  use radius `1/2`, minimum separation 1, centre density and packing density
  `(π/6)δ`. Any number carried across must be multiplied by `π/6` (density) or
  divided by 8 (centre density) before comparison. Numbers already recorded in
  occupied-volume units: 0.740480 / 0.754697 / 0.770271 / 0.773055 / 0.779747.

## K15-C008 — the record to beat is 0.754697399337 (dodecahedral), not 0.770271

- **Statement.** Hales–McLaughlin, *The dodecahedral conjecture*, JAMS 23 (2010)
  299–344, give `vol Ω(v) ≥ V_HM = 5.550291028515510…` for every Voronoi cell;
  summing cells gives `δ ≤ (4π/3)/V_HM = 0.7546973993374058…`. This is below
  every published Fourier/higher-point bound (`0.770271`, CDS22 Table 1.1).
- **Status.** `PROVED` (published cell bound + elementary summation; the
  derivation is ours and is flagged as such — no survey headlines it).
  **main_audit:** `V_HM` and the quotient re-derived in both swarms' verifiers
  to 1e−25, and independently by me (`5.550291028515510…`, `0.754697399337…`).
- **Reviewer.** X (to confirm that no stronger non-Kepler bound is known).
- **Consequence.** `Roadmaps/dim-3-analytic-bound-prompt.md` Tiers 2b/3 and the
  ROADMAP §5 comparison are anchored to this number; CDS 0.741506 is
  **lattice-only** and must never be quoted as a general bound.

## K15-C009 — correction to the problem brief: multi-translate Poisson phases

- **Statement.** In the periodic Poisson computation with `k` translates,
  `Σ_{j,l} Σ_{x∈L} f(x+v_j−v_l) = (1/|L|) Σ_{t∈L*} f̂(t)|Σ_j e^{2πi⟨v_j,t⟩}|²`,
  which is `≥ k² f̂(0)/|L|` when `f̂ ≥ 0`. So `k > 1` is **not** an obstruction;
  the only extra work is periodic → arbitrary (K15-C002, Lemma 1.2).
- **Status.** `REFUTED` (the sentence "for k>1 the phases do not cancel" in the
  Main-authored brief §5.1). Corrected statement as above.
- **Owner** M. **Reviewer** X. **Artifact.** `smwg019eu/m2/proof.md` Remark 1.6
  and Lemma 1.3(i); identity also checked symbolically in `m2/verify.py`.
- **Correction applied** to `Roadmaps/dim-3-analytic-bound-prompt.md`? **No** —
  the recovered brief is preserved verbatim for provenance. This ledger entry
  supersedes it.

## K15-C010 — bandwidth budget: REFUTED without hypotheses; positive-definite form open

- **What was claimed at checkpoint 1.** "If `supp f̂ ⊆ B(0,R)` and `f` vanishes at
  the first `K` shell radii, then `R ≳ K/(2r_K)`."
- **Status.** `REFUTED` (review objection 2, accepted). Counterexample: take a
  nonzero radial Schwartz `g` with `supp ĝ ⊆ B(0,ε)` and set
  `f(x) = g(x)·∏_{j≤K}(|x|² − r_j²)`. Multiplication by a polynomial is
  differentiation on the Fourier side, so `supp f̂ ⊆ supp ĝ ⊆ B(0,ε)`: finitely
  many prescribed zeros impose **no** lower bound on the bandwidth, for every
  `ε > 0`. Five (or fifty) shell conditions are not a zero-density statement.
- **Corrected form (K15-C010b, `PROPOSED`, reviewer X).** A genuine zero-count
  argument needs growth control, and the honest shape is the one with a norm
  factor: if `supp f̂ ⊆ B(0,R)` and `f` vanishes at `r_1 < … < r_K` then
  `R ≥ (K log 2 − ½ log(‖f̂‖₁/f(0)))/(2π r_K)` (Jensen for entire functions of
  exponential type). The `log ‖f̂‖₁/f(0)` term is not decorative: the product
  construction above makes it grow like `Σ_j log r_j²`, which is what restores
  consistency. Whether this yields a useful *quantitative* obstruction with
  `f̂(0) > 0` and the CE sign conditions is **open here**; it is a statement
  about the analytic class, not a consequence of non-isoduality (review
  objection 9, also accepted: a union of lattice shell radii is discrete with no
  finite accumulation point, and shell radii alone never force a density of
  zeros).
- **Artifact.** `smwfyzz1k/m3/zero-density-obstruction.md` (recovered; the
  formula (B) there *does* carry the norm term — the error was introduced by
  Main when condensing it, which is where it is now corrected).

## K15-C011 — withdrawn

- **Status.** `WITHDRAWN` (was `PROPOSED` at checkpoint 1). This entry proposed
  replacing "`A` has empty interior" by "`A` is closed with empty interior" in
  K15-C004. The repair was unnecessary: empty interior already implies a dense
  complement, which is all the proof uses (see K15-C004). Retained only so the
  ledger does not silently lose a version that other notes may cite.
- **Reviewer.** X.

## K15-C012 — dodecahedral cell volume, exact form

- **Statement.** For a regular dodecahedron of edge `a`, inradius
  `r = (a/2)√((25+11√5)/10)` and volume `V = (15+7√5)/4·a³`; at `r = 1`,
  `a = 2√(10/(25+11√5)) = 20/√(250+110√5) = 0.8980559531…`, hence
  `V_HM = (15+7√5)/4 · (20/√(250+110√5))³ = 5.5502910285155102690…`,
  circumradius `1.2584085723648…`, face count 12, and `4π/3` over it
  `= 0.7546973993374058…`.
- **Status.** `PROVED` in exact arithmetic; `TESTED_FINITE` numerically
  (`m1/verify.py` D1–D3, E2; two-precision enclosure).
- **Reviewer.** X. This is the constant every Tier-3 claim is compared against;
  it is also the best candidate for a Lean `norm_num`-style lemma (see
  `Main/LOCAL_COMPUTE_REQUESTS.md` `K15-COMPUTE-002`).

## K15-C013 — counting envelope for shells (and what it does and does not say)

- **Statement (a), `PROVED`.** Let `X ⊂ R³` be 2-separated, `x ∈ X`. Then
  `#{y ∈ X ∖ {x} : 2 ≤ |y − x| ≤ 2+δ} ≤ ⌊(3+δ)³⌋ − 1`.
  *Proof.* The open unit balls around the points of `X` are pairwise disjoint and
  lie in `B(x, 3+δ) ∖ B(x,1)` up to boundary; comparing volumes gives
  `n·(4π/3) ≤ (4π/3)((3+δ)³ − 1)`. ∎
  This is an **upper** bound on the contact number, i.e. it says "at most 26 for
  `δ < 0.0366`", never "at least 26". Checkpoint 1 stated it as a lower bound in
  `RESULTS.md`; that was wrong (review objection 6, accepted).
- **Statement (b), `PROVED` modulo the kissing number.** There is `δ_0 > 0` such
  that for every `0 < δ ≤ δ_0` the maximum is exactly **12**. *Proof.* Suppose
  not: there are `δ_k → 0` and 13-point 2-separated sets `X_k ⊂ [2, 2+δ_k]`.
  Passing to a subsequence, `X_k → X` with 13 distinct points on `{|y| = 2}` and
  pairwise distances `≥ 2`, i.e. 13 unit spheres touching a central unit sphere,
  contradicting the three-dimensional kissing number (Schütte–van der Waerden
  1953). ∎ No value of `δ_0` is extracted here.
- **Open.** An explicit `δ_0` needs a quantitative "kissing number with
  tolerance" statement; the crude spherical-cap area bound gives nothing
  (`13·2π(1−cos(θ/2)) ≤ 4π` only forces `θ ≥ 64.4°`, whereas one needs
  `θ > 57.1°`, the Tammes `N = 13` value). This is the one place where a *new
  local theorem* would re-open the contact-shell route (D5) — and it must
  produce a count bound, not a volume bound.
- **Reviewer.** X. Used by K15-C003 with `n = ⌊(3+δ)³⌋ − 1` (conservative) or
  `n = 12` (sharper, but only for an unspecified `δ_0`).

## K15-C014 — WITHDRAWN: Main's grid LP omitted Fourier positivity (bug)

- **Statement (`TESTED_FINITE`).** Imposing the two sign conditions of K15-C002 on
  finite grids and minimising `f(0)` with `f̂(0) = 1` gives an LP that is
  **unbounded below** (degree 8, 1200 grid points, box `|a_k| ≤ 10⁶`: objective
  `−1.87·10⁷`). Adding the one rigorous consequence available,
  `f(0) ≥ 3/(32π)` — from `1 = f̂(0) = ∫f` and `f ≤ 0` off `|x| < 2`, so
  `1 ≤ f(0)·vol B(0,2) = (32π/3) f(0)` — makes the optimum sit *exactly at the
  floor* `3/(32π) = 0.02984155…` (i.e. `δ = 0.125`), while a fine-grid audit of
  the resulting coefficients shows violations of both sign conditions of order
  `10¹⁰`–`10⁴¹`.
- **Conclusion.** Grid sampling cannot even produce an exploratory CE value:
  the two sign conditions must be enforced *identically* (SOS/Gram, Markov–
  Lukács), and the `f(0)` floor must be part of the formulation. Any baseline
  that reports a number from grid sampling is worthless.
- **Artifacts.** `Computation/ce_laguerre.py` (runnable),
  `Computation/out/ce_d8.json`; reproduction:
  `python3 KeplerConjecture/Computation/ce_laguerre.py --degree 8 --grid 1200 --tmax 40`.
  Runtime 1.1 s, 1 core.
- **Reviewer.** X. This record exists so no worker repeats the mistake.

---

## Recovered material — `PENDING_REVIEW`

These files were produced by earlier SAIR sessions before the current source
commit and are recovered verbatim (checksums in `Literature/RECOVERED.md`).
Their status is `PENDING_REVIEW`: they are **not** evidence for any claim above.

| ID | Artifact | Claim it appears to make | Audit question |
| --- | --- | --- | --- |
| K15-R001 | `Literature/sharp-bounds-in-dimension-3.md` | contact-shell/bandwidth analysis of sharp certificates; earlier "no smooth sharp certificate" argument | does it still assert the **retracted** one-sided derivative claim? PRIOR_WORK says yes and that m3 later reversed it |
| K15-R002 | `Literature/hales-2005-proof-summary.md` | Hales proof architecture, where computation is needed | locators (Ch. 3 Def. 3.2/Lemma 3.3, printed p34/PDF p46) match the retained PDF? |
| K15-R003 | `Roadmaps/dim-3-analytic-bound-prompt.md` | research brief with Tiers 0–4 | contains the refuted phase sentence (K15-C009) and an unproved integral-tail identity (§5.3) — superseded by K15-C003 |
| K15-R004 | `Roadmaps/sharp-bound-in-three-dimensions.md` | earlier roadmap draft | superseded by `ROADMAP.md`; retain for provenance only |
| K15-R005 | `Literature/fig-CE-dim3.png`, `fig-CE-dim3-log.png` | CE/BCC shell diagnostics plots | numerical provenance unknown — the generating script was never recovered |

## Obstructed, retired, or re-opened routes

| Route | Status | Claim |
| --- | --- | --- |
| A single admissible `f` proving `π/√18` | **closed** (published theorem) | K15-C006 (Li Thm 6.1) |
| "Allow `f>0` on the contact sphere, priced by 12" | **closed** (proof stands) | K15-C004 |
| Additive two-point correction to Voronoi volume | **RE-OPENED** — the claimed obstruction was invalid | K15-C005 |
| Finite zero conditions forcing finite bandwidth | **closed** (false) | K15-C010 |
| Recovering sharpness of ordinary CE at fcc/hcp | **open**; non-isoduality alone proves nothing | K15-C010, objection 9 |
| Integral tail `∫_{|x|>R} f` as a hybrid price | **not established**; a count price is proved instead, and integral estimates with proved counting envelopes remain possible | K15-C003, K15-C013 |
| Grid-sampled CE values | **closed** (LP unbounded) | K15-C014 |

## Correction log — review of checkpoint `c91007ff…c0090`

Ten required corrections were received from the independent review
(November 13, 2026, America/Los_Angeles). Disposition of each:

| # | Objection | Disposition |
| --- | --- | --- |
| 1 | empty-interior lemma: retract the rational-point "counterexample" | **accepted** — Main was wrong; K15-C004 restored, K15-C011 withdrawn |
| 2 | finite-zero bandwidth claim false | **accepted** — K15-C010 `REFUTED`, norm-term version recorded as C010b |
| 3 | hybrid obstruction inequality backwards | **accepted** — K15-C005 obstruction withdrawn, route re-opened |
| 4 | `t = 2πr²` vs interval `[4,∞)` mismatch | **accepted** — `s = \|x\|² ≥ 4`, `t = 2πs ≥ 8π`; request rewritten |
| 5 | CE hypotheses need `f̂(0) > 0` and continuity | **accepted** — K15-C002 restated |
| 6 | crude counting estimate is an upper, not a lower, bound | **accepted** — K15-C013(a)/(b) separate; RESULTS corrected |
| 7 | float SOS ≠ certificate; no implied convergence to Li's value | **accepted** — request demands an exact rational identity; convergence language removed |
| 8 | `0.779636 < 0.779747` ordering; novelty claims | **accepted** — RESULTS ordering fixed; no novelty claimed |
| 9 | non-isoduality ⇏ density of zeros | **accepted** — folded into K15-C010 |
| 10 | export evidence under Kepler; narrow the tail claim | **accepted** — `Main/Evidence/` added; tail wording narrowed |

The old versions of K15-C004, C005, C010 and C011 are quoted inside the entries
above rather than deleted, so that any note citing them can be traced.

---

## Cycle 27616 corrections and new claims

### K15-C002b — periodic approximation, repaired proof (supersedes the printed inequality)

- **Status.** `PROPOSED`; reviewer X. What was wrong in `Main/Evidence/m2-proof.md`
  (lines 125–131): after dividing by the number of interior tiles `#C_in(R)`, the
  printed estimate used a *lower* bound for `#C_in` in the direction that requires an
  upper one. The fix is to use `#C_in(R) ≤ vol(B(0,R))/S³` and keep every error
  additive.
- **Repaired chain.** Let `Λ` be a packing, `c = c(Λ)`, and fix `S ≥ 10`. Tiling by
  cubes `C_z = z + [0,S)³`, `z ∈ Sℤ³`:
  (i) `#C_in(R) ≤ vol B(0,R)/S³` (each interior cube has volume `S³`);
  (ii) `Σ_{C ∈ C_in} n(C) ≥ N(0,R) − O(R²S)` (the boundary shell holds `O(R²S)`
  centres, since `Λ` is 2-separated);
  (iii) hence for the maximal tile `C*`,
  `n(C*) ≥ (N(0,R) − O(R²S))·S³/vol B(0,R) = c S³(1 + o(1))`,
  the `o(1)` being `O(S/R) + O(S³R²S/R³)`-free: the two errors are `S/R` and `1/S`
  and are kept *additive*, never multiplied.
  (iv) Periodising `Λ ∩ (z + [2, S−2]³)` loses at most `O(S²)` centres, so
  `c(Π) ≥ c(1 − O(1/S))`.
  **Case `c(Λ) = 0`:** the conclusion `c(Λ) ≤ f(0)/f̂(0)` is then trivial; the
  argument above is applied only when `c > 0` (otherwise `N(0,R)/vol B(0,R) → 0`
  makes every displayed ratio void).
- **Note.** The corrected proof is *weaker in constants but correct*, and it is the
  version any Lean formalisation must follow.

### K15-C003r — count-price indexing, repaired

- **Status.** `PROPOSED`; reviewer X. The gap in `m2-proof.md` (lines 256–265): the
  proof fixes `j` and gets `≤ nk` bad pairs, then uses `nk` as the total over all
  `j`, which would need `nk` per `j`. **Fix: fix `l`, not `j`.** For each base
  centre `v_l` the map `(x,j) ↦ (v_l, x+v_j)` is a bijection onto
  `{v_l} × Π`; the condition `x + v_j − v_l ∈ A` becomes `c' − c ∈ A` with
  `c = v_l`, so by `(LC(A,n))` there are at most `n` such `c'` for this `l`.
  Summing over the `k` values of `l` gives at most `nk` bad pairs in total, hence
  `Σ_bad f ≤ nk·max(M,0)`, and
  `k(f(0) + n max(M,0)) ≥ S(f) ≥ k²f̂(0)/|L|` gives
  `c(Π) ≤ (f(0) + n max(M,0))/f̂(0)`. Statement unchanged; proof now correct.
- **Hypotheses to restate in `RESULTS.md`:** `f̂(0) > 0`; the positivity set `A` lives
  in the **exterior** `|x| ≥ 2` and `f ≤ 0` off `A` there — `f` may be positive
  inside `|x| < 2` with no penalty.

### K15-C005r — one frozen score, its Poisson mean, and the valid obstruction

Review objection (3rd round) accepted: the previous sign claims mixed two different
objects and the retained `mean B_κ ≤ −κc f̂(0)` has the wrong sign. Freeze both:

- **(S1) raw score** `σ₁(v) = vol Ω(v) + κ·B_κ(v)`, `B_κ(v) = κ⁻¹σ₁`… precisely
  `B_κ(v) = Σ_{μ∈Λ} f(v−μ)` (self-term `f(0)` **included**) — this is m1's object.
- **(S2) centred score** `σ₂(v) = vol Ω(v) + κ·S_f(v)`, `S_f(v) = Σ_{μ≠v} f(v−μ)`.

**Facts (all `PROVED`).**
(F1) `S_f(v) ≤ 0` for every `v` and every packing: every difference has length
`≥ 2`, where `f ≤ 0`; the sum converges by the decay hypothesis. *This is the
distant-neighbour content the review asked for: the sign is pointwise, not an
average, and it uses every neighbour, not the twelve nearest.*
(F2) `f(0) + 12f(2) ≥ f̂(0)/(4√2) > 0`. Proof: Poisson at fcc gives
`Σ_{λ∈fcc} f(λ) = (1/(4√2))Σ_{μ∈fcc*} f̂(μ) ≥ f̂(0)/(4√2)`; the left side is
`f(0) + 12f(2) + Σ_{|λ|≥√6} f(λ) ≤ f(0) + 12f(2)` because `f ≤ 0` there. So at the
isolated icosahedral 13-cluster, `B_κ = f(0) + 12f(2) > 0` — positive, as the review
says.
(F3) **Corrected (hourly review 00:08).** For a lattice `Λ = L`, `S_f` is constant
(translation invariant) and
`S_f = c·Σ_{ξ∈L*} f̂(ξ) − f(0) ≥ c f̂(0) − f(0)`, with equality **only if** `f̂`
vanishes on `L* ∖ {0}`. The previous line called this "the mean of `S_f`" and put
`c f̂(0) − f(0)` as an equality: both were wrong. A spatial integral of `S_f` over a
fundamental cell is *not* an average over packing centres; the identity above is
Poisson summation, and `Σ_{ξ≠0} f̂(ξ) ≥ 0` is exactly the slack. For `k > 1` no such
identity is available and only (F1) survives.

**Consequence (the obstruction, corrected).**
- With (S1): `σ₁(v) ≥ V₀` gives `vol Ω(v) ≥ V₀ − κf(0) − κS_f(v) ≥ V₀ − κf(0)` by
  (F1), so `V₀ ≤ inf_v vol Ω(v) + κf(0) = V_dod + κf(0)`, which is **worse than
  `V_dod` for every κ > 0**. The raw score cannot help; the positive value at the
  icosahedral cell is exactly the `κf(0)` shift.
- With (S2): `σ₂(v) ≥ V₀` gives `vol Ω(v) ≥ V₀` by (F1), so
  `V₀ ≤ inf_v vol Ω(v) = V_dod` (Hales–McLaughlin) and the bound `V_dod` is
  attained (X-C003(iii): the 13-cluster embeds in a saturated packing). So the
  centred score is exactly the dodecahedral barrier and cannot pass it.
- **Conclusion (narrowed).** Discarding `S_f ≤ 0` cannot improve the cell-volume
  minimum, so a hybrid that uses *only* the pointwise sign of the kernel cannot
  pass `V_dod`. That is all this argument proves. It does **not** rule out a hybrid
  that couples the pointwise inequality to additional geometric control of the
  *average* of `S_f` (for instance, that `S_f` is very negative on most vertices and
  the deficit is carried by few) — such a coupling would use information the
  argument above throws away. Route R1 stays open in that narrowed sense. The mechanism is also instructive: a correction built from an
  admissible kernel is non-positive everywhere, so a successful `A` must be
  *positive at defect vertices* and is not of this form — which is precisely why
  Hales's `A` is a geometric transfer, not a kernel.
- **Reviewer.** X. **Artifacts.** `Main/Evidence/m1-certificate.json` (for (S1) and
  the numerics), and this entry for (F1)–(F3).

### K15-C010r — bandwidth: what is and is not refuted

- **Refuted (as stated by Main at checkpoint 1):** the *unrestricted* finite-zero
  claim. Counterexample stands (`f = g·∏(|x|²−r_j²)`, `supp ĝ ⊆ B(0,ε)`), but it
  **destroys Fourier positivity**, so it refutes only the hypothesis-free form.
- **Not refuted:** the positive-definite form of `smwfyzz1k/m3` Theorem 4.1, which
  needs `f̂ ≥ 0`, radiality (or vanishing on whole spheres), `f̂ ∈ L¹`, `f(0) > 0`.
  In that class `‖f̂‖₁ = ∫f̂ = f(0)`, so the logarithmic term of the budget
  **vanishes identically** and the budget is the *finite* statement `R ≥ K log 2/(2π r_K)` — the earlier `− o(1)`
was unexplained and is removed; the Jensen estimate has no asymptotic slack here.
  Whether that yields a usable obstruction with the CE sign conditions is `OPEN`
  here; X-C004 accepts the band-limited statement with that scope.
- **Status.** `C010`: `REFUTED` (unrestricted form only). `C010r`: `PROPOSED`,
  reviewer X.
- **Corrections to the recovered m3 note** (review, accepted): line 164 concerns
  zeros of `f̂`; the dual estimates at lines 217–229 need
  `log(‖f‖₁/|f̂(0)|)`, which need not vanish; the contact outward derivative is
  `≤ 0`; the contact-Laplacian display omits off-contact contributions and is an
  inequality, not an equality; and with the sign threshold matched, the `E₈`
  contact shell is a boundary shell too, so the contrast drawn there is invalid.
  Recorded so no worker builds on the note as written.

### K15-C013r — counting envelope: corrected statements

- (a) `n ≤ ⌊(3+δ)³⌋ − 1` — an **upper** bound (K15-C013(a), unchanged), with the
  exact threshold `δ < ∛28 − 3 = 0.03658897…` for `n ≤ 26`.
- (b) existence of `δ₀ > 0` with `n = 12` for `0 < δ ≤ δ₀`: correct, and
  **attainability** should be added: the value 12 *is* attained, by the icosahedral
  twelve, whose mutual distances are `2.1029… > 2` (X-C003; E's fixture). So for
  small `δ` the maximum is exactly 12, not merely at most 12.
- (c) The spherical-cap computation: `13·2π(1 − cos(θ/2)) ≤ 4π` implies
  `θ ≤ 2 arccos(11/13) = 64.4°`, **not** `θ ≥ 64.4°`. Since the needed separation
  satisfies `θ < 60°`, the area bound contradicts nothing — it is vacuous, as
  intended, but the inequality must be written the right way round.
- (d) Do not claim novelty for an explicit tolerance width: quantitative `N = 13`
  Tammes results exist in the literature and must be located and cited before any
  such claim (`TASKS` Q5).
- (e) **Scope corrections (hourly review 00:08, from E's repair).** The
  varying-radius angular lemma is valid only for `0 ≤ δ ≤ √5 − 1`. The boundary
  count must be written `(r + D + 2)³ − r³ ≤ 3(D + 2)(r + D + 2)²`, not with `r³`
  alone on the right. Both are hypotheses of the shell argument and neither may be
  quoted outside that range.

### K15-C014r — grid-LP claim withdrawn; the bug and the real numbers

- **Status.** `WITHDRAWN`. The submitted `Computation/ce_laguerre.py`
  (`sha256 b17badbc…`) builds `M_hat_s` and then **never passes it, or its negative,
  to either `linprog` call**: Fourier positivity was not imposed. Both calls also
  used the box `|a_k| ≤ 10⁶`, so the large negative objective was a bounded
  minimum, not an unbounded ray, and `status = 0` is "optimal", not "unbounded".
  The saved `audit_*` fields evaluate the polynomials `P, Q` **without** the
  Gaussian factor `e^{−πs}`: their signs are meaningful, their magnitudes are not
  values of `f` or `f̂`. The recorded maximum of `P` on the tested exterior was
  negative, so the data never showed "violations of both signs". The `3/(32π)` floor
  is also redundant for feasible data (it follows from `f̂ ≥ 0` and `|f| ≤ f(0)`).
- **What is actually true (local, from the review's rerun).** With `−M_hat_s`
  added to both constraint matrices, the degree-8, grid-1200, tmax-40 control gives
  `f(0) = 0.21820243547088458` (occupied density `0.9141`), not the floor, and it
  still fails global Fourier positivity (leading even-degree coefficient negative).
  So: **grid optimisation produces exploratory candidates, not certificates, and
  its value is not even close to the CE optimum at degree 8** — but grids are not
  worthless, which is what C014 wrongly asserted.
- **Replacement record.** K15-C014 is kept, with the bug, so that the mistake is
  traceable. The correct lesson is X-C007/X-C008: certify with an exact sign
  decision (Sturm in the univariate Laguerre family), and impose `f(0) > 0`.
- **Reviewer.** X (X-C007 independently reproduced the same failure mode).

### K15-C015 — cluster-averaged local criterion (E's `K15-E001`), integrated

- **Statement.** Let `Λ` be saturated, `A : Λ → R`, `Π` a partition of `Λ` into
  finite clusters with `diam K ≤ D` and `|K| ≤ V_max` for all `K`, and suppose
  (C3) `vol Ω(v) + A(v) ≥ 0` for all `v`; (C4) `Σ_{v∈K}(vol Ω(v) + A(v)) ≥ √32·|K|`
  for all `K ∈ Π`; (C5) `Σ_{v∈Λ(x,r)} A(v) ≤ C₁r²`. Then
  `δ(x,r,Λ) ≤ π/√18 + C(C₁, D, V_max)/r`.
- **Why it matters.** Lemma 3.3 of Hales is the case `Π` = singletons; (C4) is a
  strict relaxation, so the pointwise fcc-compatibility can be replaced by a
  cluster average. Proof in `Experimental/LOCAL_CRITERION.md` §1.
- **Status.** `REFUTED as a universal statement; repaired (C015r).` A singleton
  cluster `K = {v}` is a cluster of diameter `0 ≤ D` for every `D`, and (C4) then
  demands `vol Ω(v) ≥ √32 = 5.65685…`, which is false at the icosahedral vertex
  (`V_dod = 5.55029…`, X-C003/E-K15-E002). So "for every cluster of diameter
  `≤ D`" cannot hold for any `D`; the partition must be a *specified* one that
  exists for each packing (e.g. clusters produced by a rule with a boundary
  estimate), never a universal quantifier over clusters. **Do not close the
  geometric avenue because the quantifier was wrong:** the repair is to state the
  partition and its boundary term, which is what E's constructive route does.
  Remaining status: `PROPOSED` after that repair (author E), reviewers M and X.
  Main read the proof: the
  cluster accounting and the boundary term are of the same shape as Lemma 3.3 and
  appear correct; the constant `C` depends on `D` and `V_max`, which must be stated
  explicitly in `RESULTS.md` before use.
- **Priced objection (E's own `K15-E003`, `PROVED`).** Finite-cluster computations
  of Voronoi volumes are *upper* bounds (adding bisector constraints only shrinks
  cells), so a cluster-average lower bound can be **refuted but never established**
  by sampling. Any promotion of C015 needs an analytic lower bound over clusters
  (Rogers-simplex or Fejes Tóth type) or a certified saturation of the outer region.
- **Open question (`K15-E004`).** With `A = 0`: is `Σ_{v∈K} vol Ω(v) ≥ √32|K|` for
  every cluster of diameter `≤ D`? `D = ∞` is Kepler; the content is the smallest
  admissible `D`, with the icosahedral 13-cluster as first test case.

### K15-C016 — cross-review verdicts imported from X and E

| Item | Verdict | Where |
| --- | --- | --- |
| X-C001 contact-shell Laplacian `< 0` forced positive somewhere | accepted as `PROVED` | X registry |
| X-C002 3D maximisers are not unique (HCP, Barlow family) | accepted; binds every equality argument | X registry |
| X-C003 icosahedral cell `V_dod`, deficit `0.106563` | accepted; matches E's `K15-E002` | X, E |
| X-C005 "all higher-point methods obstructed" | `REFUTED` (was never asserted here; recorded) | X registry |
| X-C006/Viazovska no smooth sharp certificate | `REFUTED` | X registry |
| X-C007 grid feasibility ≠ certificate | accepted; matches the C014r story | X registry |
| X-C008 exact Sturm certification in the Laguerre family | accepted as the acceptance test | X registry |

---

## Hourly review 00:08 (November 14, 2026) — integration

Reviewed completion `30102`, source `0c3ee751254b1b61f16eb175d9bd8d571f842b18`.
The supervisor's own review text and exact local evidence are being published on
`kepler15/setup-01a1d8c0`; at the time of this checkpoint
`Main/HOURLY_REVIEW_2026-11-14_0008.md` and `Computation/Reviews/48443/` were **not
yet on the fetched branch**, so the findings below are integrated from the
assignment text and must be re-anchored to their artifacts when those land.

### K15-C017 — Computation's K21 "certification" REFUTED (claims, not a bound)

- **Claim withdrawn.** A value near `Δ = 0.78010544` presented as certified, from
  source `e681fbfddb8c5962333380c271d5f7a67f44a07b`, tip
  `633da8e9db3987ec8c56a7c1eb628f3d47402bc2`.
- **Why it fails (two independent reasons).**
  1. The checker's failure reporting sits inside `if verbose`, so sign failures are
     silent unless verbose mode is on. A validation test whose input `[2, −1]` is
     *impossible* returns success: the checker does not check.
  2. The rebuilt `q` has **ten simple positive roots** and takes a negative value at
     a rational point: `q(57955199/21687900) ≈ −3.876231892749308e−5`. An exact
     rational witness beats any amount of sampling.
- **Status.** `REFUTED`. Reviewers: Astra and X (X independently reviews the
  checker). **Main has not re-derived `q`** — the witness and hashes are to be cited
  from `Computation/Reviews/48443/` once pushed.
- **Standing rule (added to D13).** No computational bound enters this ledger
  without (i) failure reporting on by default, (ii) an exact verdict at an
  adversarial witness point, (iii) a hash of the exact source that produced it.
  The π interval in the same artifact passes a separate audit; its decimal upward
  rounding still needs repair, so even that piece is not yet usable.

### K15-C018 — the shell allowance: one fully specified analytic benchmark

- **Statement (benchmark, `PROPOSED`).** Fix `ρ > 2` and `η ≥ 0`. Let `f` satisfy
  the K15-C002 hypotheses (continuous `f, f̂` with the CE decay,
  `f̂ ≥ 0`, `f̂(0) > 0`), plus
  `f(x) ≤ η` for `2 ≤ |x| ≤ ρ` and `f(x) ≤ 0` for `|x| > ρ`.
  If every 2-separated set has at most **12** points at `A`-differences from any of
  its points, `A = {2 ≤ |x| ≤ ρ}`, then every packing satisfies
  `δ ≤ (4π/3)(f(0) + 12η)/f̂(0)`.
- **Proof.** K15-C003 (Theorem B) with `A = {2 ≤ |x| ≤ ρ}`, `n = 12`, `M = η`,
  plus the periodic-to-general bridge of K15-C002b. Nothing else is needed; the
  only non-trivial input is the count `n = 12`.
- **The counting input is PENDING.** `ρ = 209/100` is provisional: it needs a
  rigorous Tammes-13 / kissing-with-tolerance enclosure to certify that 13 points
  cannot be 2-separated in the annulus `[2, 2.09]`, and E's repaired radial
  argument (scope `0 ≤ δ ≤ √5 − 1`, boundary count
  `(r+D+2)³ − r³ ≤ 3(D+2)(r+D+2)²`). Until then `ρ` is a placeholder, not a theorem.
- **Attribution.** The truncated-shell relaxation is the Cohn–Elkies truncation
  idea; the same mechanism underlies de Laat–de Oliveira Filho–Vallentin's
  strengthened two-point bound (DLOV14) and the truncation step in
  Musin–Tarasov's computer-assisted work. This benchmark is **not** a three-point
  SDP and must never be reported as one.
- **Status.** `PROPOSED`; reviewers X and Astra. It is a *benchmark to evaluate*,
  not a result: with `η = 0` it collapses to ordinary CE (K15-C002) and is
  obstructed by Li; its interest is entirely in whether a small `η` at
  `ρ = 2.09` buys more than `12η/f̂(0)` costs.
- **Comparison requested from C:** same degree, `η = 0` versus `η > 0`, and the
  same normalisation — so that the two numbers differ only by the relaxation.

### Fixes to earlier entries in this section (accepted)

| Entry | What was wrong | Repair |
| --- | --- | --- |
| K15-C005r (F3) | "mean of `S_f` equals `c f̂(0) − f(0)`" | `S_f = c Σ_{ξ∈L*} f̂(ξ) − f(0) ≥ c f̂(0) − f(0)`, equality only if `f̂` vanishes on `L*∖{0}`; a cell integral is not a centre average |
| K15-C005r conclusion | claimed to close all additive hybrids | narrowed: only pointwise-sign hybrids are closed; hybrids using control of the *average* are not excluded (R1 open) |
| K15-C010r | "`R ≥ K log2/(2π r_K) − o(1)`" | finite estimate: `R ≥ K log2/(2π r_K)`, no asymptotic slack |
| K15-C015 | "for every cluster of diameter `≤ D`" | false for every `D` (singleton at the icosahedral vertex); partition must be specified |
| K15-C013 | angular lemma / boundary count unqualified | valid for `0 ≤ δ ≤ √5 − 1`; boundary count `(r+D+2)³ − r³ ≤ 3(D+2)(r+D+2)²` |
| X's Gaussian driver (X-C008 family) | factor-`π` density error; HiGHS "Model error" read as infeasibility | exact feasible point `P = 2 − 2s/3`, `Q = 1 + 2v/3` exists; the model error is a formulation/scaling fault, not infeasibility |

Kept as narrow positive results, with their hypotheses: **K15-C002b** (additive
periodic estimate) and **K15-C003r** (fixed-coset counting). Neither is affected
by any finding above.

---

## Continuous block, November 14 — shell count reduced, exact checker written

### K15-C019 — the shell count is a single Tammes-13 number (PROVED reduction)

- **Lemma.** Let `y_1, …, y_13 ∈ R³` with `2 ≤ |y_i| ≤ ρ` and `|y_i − y_j| ≥ 2`
  for `i ≠ j`. Then the directions `u_i = y_i/|y_i|` satisfy
  `⟨u_i, u_j⟩ ≤ 1 − 2/ρ²`, i.e. every pair subtends an angle
  `≥ arccos(1 − 2/ρ²)`.
- **Proof.** With `r_i = |y_i| ∈ [2, ρ]`,
  `4 ≤ |y_i − y_j|² = r_i² + r_j² − 2r_ir_j⟨u_i,u_j⟩`, so
  `⟨u_i,u_j⟩ ≤ f(r_i,r_j) := (r_i² + r_j² − 4)/(2r_ir_j)`.
  For `2 ≤ a, b ≤ ρ` with `ρ ≤ √6` (our `ρ ≈ 2.09`), `f` is increasing in each
  argument: `∂_a f = (a² − b² + 4)/(2a²b)`-signed quantity is positive because
  `a² + 4 ≥ 8 > ρ² ≥ b²`. Hence `f(r_i,r_j) ≤ f(ρ,ρ) = 1 − 2/ρ²`. ∎
  *(The mixed case is subdominant: `f(2,ρ) = ρ/4 < 1 − 2/ρ²` exactly when
  `ρ² − 4ρ + 8 > 0`, true for all `ρ`.)*
- **Corollary.** If the maximal number of points on `S²` with mutual angular
  distance `≥ θ` is at most 12 — equivalently, if the Tammes value `θ₁₃` for 13
  points satisfies `θ₁₃ < arccos(1 − 2/ρ²)` — then every 2-separated set has at
  most 12 points in the annulus `[2, ρ]`, i.e. `n(ρ) = 12` in K15-C018.
  The value 12 is **attained** by the icosahedral twelve (mutual distances
  `2.1029… > 2`), so the maximum equals 12, not merely at most 12.
- **Numerical content (checked).**

  | `ρ` | `1 − 2/ρ²` | required `θ_min` | margin over `θ₁₃ = 57.1367°` | `πρ²` |
  | --- | --- | --- | --- | --- |
  | 2.02 | 0.509852 | 59.346° | **+2.209°** | 12.819 |
  | 2.05 | 0.524093 | 58.393° | **+1.256°** | 13.202 |
  | 2.09 | 0.542135 | 57.171° | **+0.034°** | 13.723 |

  So `ρ = 209/100` is admissible **only** with a Tammes-13 enclosure accurate to
  better than 0.03°; `ρ = 2.05` leaves 1.26° and is the recommended first target.
  This matches E's diagnostic (`cos θ_min = 23681/43681` exactly for `ρ = 2.09`).
- **Status.** `PROVED` (the lemma and corollary; Main). **Reviewer** X.
  The Tammes value itself is *cited*, not proved here: a rigorous enclosure of
  `θ₁₃` (Schütte–van der Waerden; Musin–Tarasov for computer-assisted
  certification) is the outstanding input, and it must be enclosed, not rounded.

### K15-C020 — path from E's count to C's evaluated benchmark (specification)

1. **E** produces `θ₁₃ < arccos(1 − 2/ρ²)` as a *directed enclosure* for a chosen
   `ρ` (recommended `ρ = 2.05`), or cites a published rigorous value with its
   precise scope. Output: an inequality between exact rationals.
2. **M** applies K15-C019 to get `n(ρ) ≤ 12`, with attainability, and fixes the
   rational thresholds `T_LO ≤ 4π` and `T_HI ≤ πρ²` (directed `π` bounds).
3. **C** runs the optimisation: find rational `a` minimising
   `(p(0) + 12η)/q(0)` subject to `q = M a ≥ 0` on `u ≥ 0`, `p ≤ η` on
   `[T_LO, T_HI]`, `p ≤ 0` on `u ≥ T_HI`, `q(0) > 0`.
4. **Anyone** verifies the candidate with `Computation/shell_check.py`
   (`--self-test` passes; a bad profile is rejected with its failing condition).
   Only a `PASS` on every line yields a bound, and the printed value is an exact
   rational times a directed `π` enclosure.
5. **Honest calibration.** With `η = 0` this is ordinary CE and Li blocks it; the
   realised gain from DLOV14-type relaxations is `0.779747 → 0.773080`, i.e.
   `0.0067` in `δ`. Beating `0.754697` would need `0.025`. So the benchmark's
   realistic target is the **first certified number in this project** and, at
   best, `0.770271`; it is not a route past the dodecahedral barrier, and saying
   otherwise would be a domain error.

### K15-C021 — checker bugs to record (from X and the local checks)

- `kepler_ok` truncated positive rationals to integers before comparison:
  `P(0) = 99/100`, `Q(0) = 1` gives exact left side `32P(0)² = 19602/625 > π³`
  yet the helper returned **true**. Exact rationals and a directed `π` comparison
  are required; the truncation is a bug, not a certificate (agrees with the local
  check `gaussian_comparison_regression.log`).
- X's pair-average and existential-partition arguments remain **wrong** as
  stated and are not imported. E's Tammes script is floating-point arithmetic
  (`mpmath`), not a directed enclosure: its exact endpoint `23681/43681` is
  reusable, its angle comparison is illustrative only.
- C's regressions pass (exit 0) but produce **no new certificate**; `shell_bench.py`
  is still unwritten, so `C-SHELL-001` remains blocked.

### K15-C022 — the shell benchmark's unconditional form, and why a grid LP cannot propose it

- **Unconditional count.** With no Tammes input, K15-C013(a) gives
  `n(ρ) ≤ ⌊(ρ+1)³⌋ − 1`, e.g. `n ≤ 27` at `ρ = 2.05` and `n ≤ 28` at `ρ = 2.09`.
  So K15-C018 holds **unconditionally** with those counts:
  `δ ≤ (4π/3)(f(0) + 27η)/f̂(0)`. `shell_check.check(..., count=27)` evaluates it.
  The Tammes route (K15-C019) only improves `27 → 12`; it is not needed for the
  theorem to be true, only for it to be sharp enough to matter.
- **Negative result: a dense-grid LP cannot propose a candidate.** Main attempted
  the obvious proposer (minimise `p(0)` subject to grid samples of the three sign
  conditions, degree 6, 900 points, `u` up to 80). Three failure modes, all
  structural:
  1. without the (true) constraint `p(0) ≥ 0`, which follows from
     `f(0) = ∫f̂ ≥ 0`, the LP is degenerate and returns a box vertex
     (`a = (−1000, 1000, −1000, …)`);
  2. **with** `p(0) ≥ 0` the optimum is exactly `0` — the grid conditions are
     vacuous, so the objective can be driven to the constraint boundary;
  3. at `u` up to `8000` HiGHS returns NaN unless every constraint row is scaled,
     and the scaled solution rounds to a profile with `q(0) ≈ −2.5·10⁶`.
  **Conclusion for C:** propose candidates by exact Sturm bisection over a
  low-dimensional family, or by an SDP with SOS multipliers in `u`
  (Markov–Lukács makes the half-line conditions exact), never by dense grids over
  monomial coefficients. This is the same lesson as K15-C014r, in a second guise;
  it is recorded so that no worker spends a local run on it.
- **Status.** `TESTED_FINITE` (the failure modes were observed) / `PROVED` for the
  unconditional count. Reviewer X. Script not retained: it produced no candidate
  and would only invite reuse.

---

## Block K15-HOUR-20261114-M (start 2026-11-14T09:14:25Z)

### K15-C023 — independent cross-verification of Computation's K33 certificate (`VERIFIED_CROSS`)

- **Object.** `KeplerConjecture/Computation/out/verified_certificate_K33b.json`
  from branch `kepler15/comp-01a1d8c0` (`sha256 525d1d55…`), degree 33, convention
  `t = 2π|x|²`, claimed `Δ ≤ 0.77996622`.
- **Two independent verifications, both run by Main on this VM.**
  1. Computation's own two implementations (`exactcert.certify`, and the SymPy
     oracle): `ACCEPT`, `p0/q0 = 42935541634304122537361009/230584315533749727927712550`,
     `Δ_upper = 0.779966216777`.
  2. Main's independent checker (`Computation/verify_comp_cert.py` +
     `shell_check.py`, written in the *different* variable `u = π|x|²` with its
     own Sturm chain): the coefficients are converted by `P(u) = Σ c_k L_k(2u)`,
     and both sign conditions pass (`q ≥ 0` on `u ≥ 0`; `p ≤ 0` on
     `u ≥ 4π_lo`), giving the **same** rational ratio and
     `Δ ∈ (0.779966216777, 0.779966216777)`.
- **What it establishes.** The inequality `Δ(Λ) ≤ 0.77996622` for every packing of
  unit balls, conditional only on the two checkers being correct — and they are
  independent code, in different variables, agreeing on the object and the value.
  Achieved by exact rational arithmetic with the *exact* rational thresholds
  `T_LO = 4π_lo`, `T_HI = π_lo ρ²` (no integer rounding, so no conservatism).
- **What it does not establish.** It is **not** an improvement: `0.77996622 >
  0.779747` (Cohn–Elkies 2003). It says nothing about sharpness. It is a
  reusable, checked component — the first object in this project confirmed by two
  independent exact implementations.
- **Reproduce.**
  `python3 KeplerConjecture/Computation/verify_comp_cert.py <cert.json>` (≈4 s,
  1 core, sympy only). Hashes: cert `525d1d55…`, `shell_check.py ca976ce4…`,
  `verify_comp_cert.py 6a179b34…`.
- **Status.** `VERIFIED_CROSS` (new status: a bound confirmed by ≥2 independent
  exact implementations). Reviewer X: to confirm that the two implementations are
  genuinely independent (they share no code and use different bases; Main wrote one).

### K15-C024 — the density normalisation, proved (`PROVED`)

Every bound in this project is a statement about
`Δ(Λ) = limsup_R vol(B(0,R) ∩ ⋃_{λ∈Λ} B(λ,1))/vol B(0,R)`. The chain of
identities used everywhere, now written out:

1. **Ball volume.** `vol B(0,1) = 4π/3` in `R³`.
2. **Occupied volume of a saturated packing.** For a saturated packing the balls
   cover a neighbourhood; for a general packing, `Δ` as defined is the occupied
   fraction and is `≤ 1`.
3. **Counting-to-volume.** If `Λ` is 2-separated, then
   `#(Λ ∩ B(0,R))·vol(B_1) ≤ vol(⋃_{λ∈Λ∩B(0,R)} B(λ,1)) ≤ vol B(0,R)`, hence
   every finite packing has `#·(4π/3) ≤ vol B(0,R) + O(R²)`. For an infinite
   packing with a limiting centre density `c = lim_R #(Λ∩B(0,R))/vol B(0,R)`,
   the boundary error is `O(R²)/R³ → 0` and `Δ = c·4π/3`.
4. **Centre density.** `c = Δ/(4π/3) = 3Δ/(4π)`; for fcc, `c = 1/(4√2)` and
   `Δ = π/√18` exactly.
5. **The CE bound in these units.** For admissible `f` with `f̂ ≥ 0`,
   `f ≤ 0` off `|x| ≥ 2`, `f̂(0) > 0`: `c ≤ f(0)/f̂(0)` and
   `Δ ≤ (4π/3)f(0)/f̂(0)` (K15-C002b for the passage to all packings).
6. **Conversions from the older convention** (radius 1/2, separation 1, number
   density `n`): `c = n/8`, `Δ = (π/6)n`. Verified exactly (K15-C007).

*Status.* Items 1–4 and 6 are `PROVED`; item 5 depends on K15-C002b, whose
periodic estimate is repaired but still awaits X. The Lean module
`Lean/Kepler15/Normalisation.lean` formalises only the *algebraic* part (3)–(4)
as a definitional identity and does **not** prove the ball volume or the
counting-to-volume bridge; the pinned build is `M-LEAN-001` (complete, axioms
`[propext, Classical.choice, Quot.sound]`).

### K15-C025 — the next theorem, with every missing hypothesis named

**Target theorem (local/cluster form).** Let `Λ` be saturated, `A : Λ → R`, and
`Π` a partition of `Λ` into clusters with `diam K ≤ D`, `|K| ≤ V_max`, such that
(a) `vol Ω(v) + A(v) ≥ 0` for all `v`; (b) `Σ_{v∈K}(vol Ω(v)+A(v)) ≥ √32|K|` for
all `K ∈ Π`; (c) `Σ_{v∈Λ(x,r)} A(v) ≤ C₁r²`. Then
`Δ ≤ π/√18 + C(C₁,D,V_max)/r`.

| # | Obligation | Status |
| --- | --- | --- |
| H1 | the criterion itself (cluster averages + negligibility ⇒ bound) | `PROPOSED` (E's `K15-E001`); Main read the proof, X to audit |
| H2 | a *specified* partition rule with a boundary estimate (the universal quantifier over clusters is false: a singleton at the icosahedral vertex gives `5.55029 < √32`) | **MISSING** |
| H3 | an analytic lower bound for `Σ_{v∈K} vol Ω(v)` over that partition, `D = 2` first | **MISSING** — and sampling can only refute it (`K15-E003`) |
| H4 | negligibility (c) for the chosen `A` | **MISSING** |
| H5 | a numerical value of `V_0 = √32` once (b) is replaced by `≥ V_0|K|`; beating the dodecahedral barrier needs `V_0 > 5.550291` | **MISSING** |

**Why this and not the shell allowance.** Computation measured the shell
benchmark at degree 21, grid 500, `ρ = 2.09`: the jointly optimised allowance
chose `η = 0`, i.e. **gain exactly 0** (`K15-C-SHELLBENCH-001`, `TESTED_FINITE`,
not an impossibility proof). Two readings, both consistent with the data:
(i) at the CE optimum the sign condition is active only at `|x| = 2`, a
measure-zero set, so relaxing the sign on a positive-width shell is a
*second-order* gain against a first-order cost `12η`; (ii) the solve is a coarse
grid LP whose control value (`0.78017286`) is itself worse than CE03, so it may
lack the resolution to see a small gain. Either way the shell route has produced
no number, and the local/cluster route (K15-C015r) is where the remaining
mathematical content is.

**Analytic comparator kept alive.** `K15-C023` shows the exact-certificate
pipeline works end to end at degree 33. It is the fallback for any candidate the
geometric route produces: a candidate profile ⇒ run `exactcert` and
`verify_comp_cert` ⇒ `VERIFIED_CROSS` or nothing.

### K15-C026 — `shell_check` accepts tight (even-multiplicity) zeros (`VERIFIED` by self-test)

- **Bug found and fixed in Main's checker.** The first revision decided
  `q ≥ 0` and `p ≤ 0` by counting *all* distinct real roots on the half-line or
  interval. A polynomial that *touches* zero without changing sign was therefore
  rejected — and that is exactly the shape of a CE optimum, where `f(2) = 0` is
  forced by the equality case. The earlier checker would have rejected every
  tight certificate while accepting only slack ones.
- **Fix (SUPERSEDED by K15-C058, which found three new witnesses against it).**
  The first repair counted sign changes on the **odd part** and probed endpoints
  and midpoint; that is unsound for perfect squares, where every root has even
  multiplicity. The current algorithm uses the polynomial's own roots (see
  K15-C058). Regression cases are now
  permanent in `--self-test` §S4: `(u−5)² ≤ 0` on `[0,10]` must FAIL,
  `−(u−5)² ≤ 0` must PASS, `u² ≥ 0` on `[0,∞)` must PASS, `u−1 ≥ 0` must FAIL.
- **Effect on the earlier result.** C's K33b certificate is still `ACCEPT` with
  the same exact value (it happens to have strict signs, so the fix changes
  nothing there). The fix matters for any future tight candidate.
- **Artifact.** `Computation/shell_check.py`
  `sha256 4f4a0ba8aee4fc765a204c6ad925e064bb036af2f437a22c669092e4f3f85eb3`.
  Reproduce: `python3 KeplerConjecture/Computation/shell_check.py --self-test`.
- **Status.** `VERIFIED` (self-test + re-verification of C's certificate).
  Reviewer X: the odd-part argument is two lines (`q ≥ 0` on an interval iff the
  odd part has no root there and `q ≥ 0` at the endpoints); confirm it agrees
  with `exactcert.yun_odd_part`.

### K15-C027 — audit of E's Tammes-13 enclosure (`ACCEPTED WITH SCOPE`; closes G2/G3 pending X)

- **Object.** `Experimental/TAMMES13_ENCLOSURE.md` (branch
  `kepler15/experimental/run-01`, revision `8aca235`), `K15-E015` and `K15-E014`.
- **What was independently executed by Main.** E's script
  `Experimental/scripts/tammes13_enclosure.py` was extracted from the branch and
  re-run in a scratch directory: it reproduces the certificate
  (`δ₁₃ < 57.1387…° < θ_min = 57.1709…°`, `margin ≈ 4.9e−4`) and fails only at the
  final relative-path write, which is an environment artefact, not a mathematical
  failure. Main also recomputed the defining equations independently at 40 digits:
  `a* = 69.405050103707°`, `d* = 57.136703077578°`,
  `θ_min = arccos(23681/43681) = 57.170902186746°`, margin `0.0342°`, and the
  consistency identity `α(d) = a` holds to all printed digits.
- **Structural audit, accepted.** (i) `g` is strictly decreasing on `(0, π/2)`
  (both terms negative), so one sign change pins the root; (ii) the chain
  `a* ≤ a_hi ⇒ h(a*) ≥ h(a_hi) ⇒ d ≤ arccos(h(a_hi))` is correct with `h`
  decreasing and `arccos` decreasing, so the comparison `d < θ_min` becomes the
  **rational** inequality `h(a_hi) > 23681/43681`; (iii) the Taylor remainder
  lemma is proved, not asserted, and its hypothesis `x ≤ 8/5` covers the ranges
  used; (iv) `π ∈ (333/106, 355/113)` is valid.
- **Scope, and what Main does not verify.** The identification
  `δ₁₃ = arccos(cos a/(1 − cos a))` at the root of (E1) is **Theorem 1 of
  Musin–Tarasov (arXiv:1002.1439v3)**, proved by computer enumeration of
  irreducible contact graphs. E's certificate covers the *arithmetic* of the
  constant only. Main did not verify the transcription of (E1) against the paper
  (internal consistency is not proof), nor the enumeration. A complexity claim
  for the shell lemma must charge that enumeration.
- **Consequence.** `K15-E014` — at most 12 centres of a 2-separated set in
  `[2, 2.09]` — is accepted subject to Musin–Tarasov; hence K15-C018's sharp
  form (`n = 12` at `ρ = 2.09`) is available, and the count is no longer the
  weakest link. The measured gain of the shell allowance remains 0
  (`K15-C-SHELLBENCH-001`), so this closes a question rather than opening a
  route. G2 and G3 move to `closed pending X`.
- **Status.** `ACCEPTED_WITH_SCOPE`. Reviewer: X (to check the (E1)
  transcription against the paper and the enumeration's scope).

### K15-C028 — exact shell fixture at degree 3, and why the allowance cannot pay (`TESTED_FINITE` with an exact verdict)

- **Family (admissible by construction).** `P(u) = (T − u)·S(u)` with `S(u) = Σ_{j≤2} s_j u^j`,
  all `s_j ≥ 0`, `T = π_lo ρ²`. Then `p ≤ 0` for `u ≥ T` and `p(0) = T s_0 > 0`
  hold *identically*, with no grid. The only remaining conditions (`q ≥ 0` on
  `u ≥ 0`, and `p ≤ η` on the shell) are decided exactly.
- **Exact measurements (degree 3, 125 candidates each).**

  | family | best `R = p(0)/q(0)` | `Δ ≤ (4π/3)R` |
  | --- | --- | --- |
  | `ρ = 2`, pure CE (`T = 4π_lo`) | `0.538382` | `2.255170` |
  | `ρ = 2.09`, shell (`T = π_lo ρ²`) | `0.527491` | `2.209550` |

  Both bounds are vacuous, and the second is **not** a bound at `η = 0`: the
  profile is positive on the shell, so it needs an allowance. Required
  `η = max_{shell} P = 50.4431`, hence the true objective is
  `p(0) + 12η = 13.7228 + 605.3168 = 619.04` and `Δ ≤ 2593.0` — vacuous by three
  orders of magnitude.
- **The arithmetic of why.** The cost `12η` is proportional to the *amplitude* of
  `P` on the shell. At low degree that amplitude is huge (`50.4` here) because `P`
  must fall from `p(0)` to `0` across a shell of width `0.09` in `√s`. The
  allowance can only pay when `P ≈ 0` on the shell — i.e. in the CE regime where
  the constraint is nearly binding. This is the precise form of the trade that
  C measured as "gain 0" at degree 21 (`K15-C-SHELLBENCH-001`), and it explains
  why raising the degree alone will not rescue the route.
- **Deliverable.** `Computation/shell_fixture.py` — an exact proposer + verdict
  fixture (`python3 shell_fixture.py --m 2`), usable at any `m`, `ρ`, `η`.
  It is the first *exact* evaluation of the shell allowance in this project;
  C's `shell_bench.py` is grid-based and cannot certify.
- **Status.** `TESTED_FINITE`; the verdicts inside are exact, the *values* are
  vacuous. Reviewer X. G10 remains open but with the cost structure now explicit.

### K15-C029 — WITHDRAWN (proof invalid, review 0138; text kept as rejected evidence)

> **Status: `WITHDRAWN`.** The proof below assumes `A ≥ 0` without saying so: from
> `A ≥ θ` on `D_θ` and `Σ_Λ A ≤ C₁r²` one cannot bound `#D_θ`, because negative
> terms of `A` outside `D_θ` cancel the positive ones inside. The corrected
> estimate is `K15-C029r`; the conditional version under `A ≥ 0` is `K15-C029c`.
> See `Main/REVIEW_0138.md`.

The cluster criterion (K15-C025) needs `Σ_{v∈K}(vol Ω(v) + A(v)) ≥ V_0|K|` with
`V_0 > 5.550291` to beat the dodecahedral bound, and `V_0 = √32 = 5.656854` to
reach Kepler. This entry records what that forces on `A`, so that a proposed `A`
can be tested before any cluster analysis is attempted.

**REJECTED Lemma (defect density is zero).** Let `Λ` be saturated with an fcc-compatible,
negligible `A`: `vol Ω(v) + A(v) ≥ √32` for all `v`, and
`Σ_{v∈Λ∩B(x,r)} A(v) ≤ C₁r²` for all `x`, `r ≥ 1`. Fix `θ > 0` and let
`D_θ = {v : vol Ω(v) ≤ √32 − θ}`. Then `#(D_θ ∩ B(x,r)) ≤ C₁r²/θ` for all
`x, r`, hence `D_θ` has upper density zero.

*Proof.* For `v ∈ D_θ`, fcc-compatibility gives `A(v) ≥ √32 − vol Ω(v) ≥ θ`.
Summing over `D_θ ∩ B(x,r) ⊆ Λ ∩ B(x,r)` and using negligibility,
`θ·#(D_θ ∩ B(x,r)) ≤ Σ A ≤ C₁r²`. Divide by `vol B(x,r) ≍ r³`. ∎

**Consequences, in the order they matter.**
1. Any packing that is fcc-compatible in this sense has `o(r³)` vertices with cell
   volume below `√32 − θ`, for every fixed `θ`. So the *only* way a cell can be
   small is for it to be rare: the geometric content is a statement about
   densities, not about individual cells.
2. Conversely, a proposed `A` that is uniformly positive on a positive-density
   set of vertices **cannot be negligible** — an immediate falsification test.
   (The same test with `θ = 0.106563` is X's `X-C003(2)`; this makes the constant
   arbitrary and the statement quantitative.)
3. On the icosahedral 13-cluster, `vol Ω = 5.550291` so `A ≥ 0.106563` there; by
   1, such clusters must have density zero in any admissible packing. **This is
   the precise sense in which the icosahedral configuration is the obstruction**,
   and it is why a successful `A` must be negative on the generic (near-fcc)
   vertices: the average of `A` over a large region is `≤ C₁r²/vol = o(1)`, while
   its value at defect vertices is `≥ 0.106563`.
4. **The usable objective** for the next geometric attempt is therefore:
   `A` with (i) `A(v) ≥ √32 − vol Ω(v)` on defect vertices, (ii) `Σ A ≤ C₁r²`,
   (iii) cluster average `≥ V_0|K|` with `V_0 > 5.550291`. Condition (ii) forces
   `A` to be negative on a set of vertices of full density, so any candidate must
   exhibit its negative part explicitly. A candidate that only specifies the
   positive part is incomplete by construction.

*Status.* `PROVED` (elementary; the `θ`-quantification is Main's). Reviewer X.
No numerical input is used.

### K15-C030 — adversarial sign-checker suite (`VERIFIED`: 13/13 expectations hold)

- **Artifact.** `Computation/checker_adversarial.py` — thirteen cases designed so
  that a plausible but wrong checker fails at least one. It is stated
  implementation-independently, so the same list can be run against
  Computation's `exactcert` after conversion with
  `interface_xcheck.main_to_comp`; running both and getting the same thirteen
  verdicts is the evidence G8 asks for.
- **The cases that matter.** `(u−5)²` must PASS (a checker that counts all roots
  rejects it — the bug Main actually had, K15-C026); `(u−5)³` must FAIL;
  `(u−1)²(u−2)²` must PASS while `(u−1)²(u−2)` must FAIL (the odd part is what
  counts); `u²` must PASS (double root at the endpoint 0); the product of ten
  simple positive roots must FAIL (the historical K21 failure mode, review
  48443); `−(u−T)²` must PASS while `u−T` must FAIL (behaviour exactly at the
  threshold `T = π_lo ρ²`); and the compact-window cases at `[4π_lo, T]`.
- **Result on Main's checker.** 13/13 pass. The suite also caught an error in
  *the test itself* on first run (a double negative made the "must PASS" case
  positive), which is a small demonstration that it discriminates.
- **Status.** `VERIFIED` for Main's `shell_check`; `OPEN` for `exactcert` until X
  runs it there. Reviewer X.

### K15-C031 — cross-run of the adversarial suite against `exactcert` (`VERIFIED`: agrees on all ten)

- **What was run.** `python3 Computation/checker_adversarial.py --against-exactcert
  <dir>` extracts Computation's `exactcert` from branch `90cc632`, substitutes
  `u = t/2` into each adversarial polynomial, and calls their engine
  (`yun_odd_part` then `_half_line_sign`).
- **Result.** Ten of ten agree, including the subtle cases: `(u−5)² → pos`,
  `(u−5)³ → fail`, `(u−1)²(u−2)² → pos`, `(u−1)²(u−2) → fail`, `u² → pos`,
  `∏_{1..10}(u−k) → fail`. Two findings that only a cross-run could produce:
  1. `− (u − T)²` at the threshold `T` is decided **`neg`** by `exactcert` (it
     factors the even-multiplicity root out and decides the sign), so its
     fail-closed policy is *sharper* than assumed: it declines only at
     **odd**-multiplicity endpoint roots, where the sign genuinely changes.
  2. Consequently `exactcert` and `shell_check` have the same semantics on every
     case tested; a certificate with a touching zero at the threshold is
     acceptable to both.
- **Status.** `VERIFIED` (G8 partially closed: the two engines agree on a
  designed adversarial set, in different bases). Remaining for G8: an argument
  that they share no code (they do not — Main wrote `shell_check` from the
  Fourier side, Computation wrote `exactcert` from the Laguerre side) and X's
  independent review of both.
- **Artifact.** `Computation/checker_adversarial.py` (both modes; `--self` uses no
  external code).

### K15-C032 — imports from C and X (unreviewed by X; recorded, not promoted)

| Item | Source | Statement | Status |
| --- | --- | --- | --- |
| `K15-C-SATURATION-001` | C `90cc632`, `out/verified_certificate_K33b.json` | the exact-certificate pipeline saturates at degree 33: `Δ ≤ 0.77996622`; degrees 37 and 41 fail exact verification at every grid/margin tried | `VERIFIED_CROSS` for the K33b value (K15-C023); the *saturation* claim is `TESTED_FINITE` |
| `K15-C-SATLIMIT-001` | C | the residual `+0.03%` above CE03 is the price of the strict-sign margin plus rational rounding | `TESTED_FINITE`; the reasoning is consistent with the strict-sign policy in `exactcert`'s docstring |
| `K15-C-SHELLBENCH-001` | C | the shell allowance's joint optimisation chooses `η = 0` at degree 21, grid 500, `ρ = 2.09` (gain exactly 0) | `TESTED_FINITE`; K15-C028 explains the cost structure |
| X free-width family | X `237cc3b`, `ce_exact_gauss.py`, `REPORT_width_and_E030.md` | `f = P(s)e^{−a s}`, exact map to `Q(w)`, density `= (4a^{3/2}/(3√π))P(0)/Q(0)`, Kepler test `32a³P(0)² < π³Q(0)²`; verified against 3-D quadrature at `a ∈ {1/2,1,3/2,2}` | recorded as the **third convention** in `Main/INTERFACE.md` §1; the quadrature agreement is X's evidence, not audited here |

None of these is promoted to a bound. The numbers in the first row are the ones
Main independently reproduced (K15-C023).

### K15-C033 — Barlow stackings have no distance in `(2, 2.09)` (`PROVED`; closes E's `K15-E013`)

E's `K15-E013` asked for Barlow stackings to be shown to have at most 12 centres
in `[2, 2.09]`; E proposed a numerical check. It has a three-line structural
proof, which Main supplies here.

**Setting.** A Barlow stacking is: the triangular lattice
`L = ⟨(2,0), (1,√3)⟩` in each horizontal layer `z = kc` with `c = √(8/3)`, each
layer displaced by a hollow of the layer below, i.e. by `±s`,
`s = (a₁+a₂)/3`, `|s| = 2/√3`.

**Lemma.** Every inter-centre distance is either `2` or `≥ 2.828`. Hence there is
no distance in `(2, 2.09)`, and the only centres within `2.09` are the contacts at
distance exactly `2`, of which there are at most 12 (kissing number; exactly 12
for fcc and hcp).

*Proof.* Three cases.
1. **Same layer.** Distances are those of `L`, i.e. `≥ 2`, with equality for the
   six nearest neighbours, and next value `2√3 = 3.464`.
2. **Adjacent layers.** Vertical separation `c`, so the 3-D distance is
   `√(d² + c²) = √(d² + 8/3)` where `d` is the horizontal distance between the two
   lattices. The horizontal distance spectrum between `L` and `L + s` is
   `2/√3 = 1.1547` (the hollow), then `4/√3 = 2.3094`, `3.0550`, `4.1633`.
   The first is `|s|² = 4/3`; the second is
   `|a₁ − a₂ + s|² = |(2, −2/√3)|² = 4 + 4/3 = 16/3`. Hence the 3-D distances
   are `√(4/3 + 8/3) = 2` and then `√(16/3 + 8/3) = √8 = 2.828`. Both facts were
   also checked numerically this block (spectrum `2.0, 2.828, 3.464, 4.472`), and
   `2.828 > 2.09`.
3. **Non-adjacent layers.** Vertical separation `≥ 2c = 3.266 > 2.09`. ∎

**Verified numerically** (this block): with `c = √(8/3)` the adjacent-layer 3-D
spectrum begins `2.0, 2.828, 3.464, 4.472` and no value lies in `(2, 2.09)`;
the same holds for every allowed offset sequence of length 3.

**Status.** `PROVED` (Main). Reviewer X. **Scope:** this closes the "Barlow"
item of E's enclosure note; the Tammes-13 input (K15-C027) supplies the `≤ 12`
count for *arbitrary* 2-separated sets, which subsumes this lemma — so the lemma
is a redundancy check on E's enumeration rather than a new ingredient.

*Note on the definition.* "Each layer over a hollow of the one below" is what
makes the family dense; if layers may sit above lattice points the packing
overlaps (`c = 1.633 < 2`), so those sequences are not packings and are excluded
by the definition, not by a computation.

### K15-C034 — X's repaired `kepler_ok` passes the historical counterexample (`VERIFIED` by re-run)

- **Re-run by Main.** `Counterexamples/ce_exact_gauss.py` (branch
  `kepler15/counterexamples/run-01`, revision `237cc3b`) was extracted and
  executed. The case that previously failed — `P(0)/Q(0) = 99/100`, where
  `32P(0)² = 313632 > π³Q(0)² = 310062.8` — now returns `kepler_ok = False`, i.e.
  the truncation bug is fixed and the verdict is the correct one.
- **The useful by-product.** In X's normalisation the Kepler test is
  `P(0)/Q(0) < √(π³/32) = 0.98435062…`, and the script prints the exact rational
  comparisons for six sample ratios. That is a concrete, checkable acceptance
  threshold for any candidate in X's Gaussian family, in the same spirit as the
  `f(0)/f̂(0) ≤ 0.186150827` threshold in the `π`-normalisation.
- **Scope.** This verifies the repair of a *comparison helper* on one case and
  the arithmetic of the threshold. It is not a certificate, and X's LP search
  remains `TESTED_FINITE` (their own report says so).
- **Status.** `VERIFIED` (Main re-ran the exact historical failure). Reviewer X.

### K15-C028 addendum — reference output of the fixture (reproducible)

`python3 KeplerConjecture/Computation/shell_fixture.py --m 2 --rho 2 --eta 0`
reports `R = p(0)/q(0) = 1675516081914556393846743137744/3112130939427411660770593506033
= 0.5383822578566787`, `Δ ≤ 2.255`, after 294 candidates; `--m 3` finds the same
value with a zero top coefficient (the family saturates at degree 3, 2058
candidates). These are the *committed* outputs; an ad-hoc variant of the same
search that summed `b` over the wrong index range produced `0.472025`, which is
**wrong** and is recorded here so the number never migrates into the ledger. The
lesson is the same as everywhere else in this project: the family is a fixture
for the interface, not a source of competitive bounds, and every number must come
from the committed script.

`Main/INTERFACE.md` §4 was also corrected: the "conservative integer threshold"
no longer exists — `4·PI_LO` and `PI_LO·ρ²` are rational and exact, so the
threshold costs nothing.

### K15-C029r — the correct signed estimate (`PROVED`)

Same hypotheses as C029 (`Λ` saturated 2-separated, `vol Ω(v)+A(v) ≥ √32`,
`Σ_{Λ∩B(x,r)} A ≤ C₁r²`). For `θ > 0` and `D_θ = {v : vol Ω(v) ≤ √32 − θ}`:

```
θ · #(D_θ ∩ B(x,r))  ≤  C₁ r²  +  N_A(x,r),     N_A(x,r) := Σ_{v∈Λ∩B(x,r)} max(−A(v),0).
```

*Proof.* `Σ_B A = Σ_{D∩B}A + Σ_{B∖D}A ≥ θ#(D∩B) − N_A`, using `A ≥ θ` on `D` and
`A ≥ −max(−A,0)` everywhere; combine with `Σ_B A ≤ C₁r²`. ∎

This is the only form that follows from the stated hypotheses. Any use must bound
`N_A`; §2 of `Main/REVIEW_0138.md` lists the two available routes (conditional
positivity, or the transfer construction of `K15-C035`). Reviewer X.

### K15-C029c — the conditional version under `A ≥ 0` (`PROVED`, with an extra hypothesis)

If in addition `A(v) ≥ 0` for all `v`, then `N_A = 0` and
`#(D_θ ∩ B(x,r)) ≤ C₁r²/θ`: small cells have upper density zero. **This is the
statement the withdrawn entry actually proved**, and it is true, but the
hypothesis `A ≥ 0` is false for the corrections that matter (an `A` that is
positive at the icosahedral vertex must be negative where cells exceed `√32`).
Cite it only with the hypothesis attached. Reviewer X.

### K15-C035 — bounded-range antisymmetric transfers make negligibility automatic (`PROVED`)

**Definition.** A *transfer* of range `R ≥ 1` and bound `Φ ≥ 0` is an
antisymmetric `φ : Λ×Λ → R` (`φ(v,w) = −φ(w,v)`) with `φ(v,w) = 0` when
`|v−w| > R` and `|φ| ≤ Φ`. Its *correction* is `A(v) := Σ_{w∈Λ} φ(v,w)`.

**Lemma.** Let `Λ` be 2-separated, `A` a transfer as above, and
`k_R := max_v #{w ∈ Λ∖{v} : |w−v| ≤ R}`. Then
(a) `|A(v)| ≤ Φ·k_R` and `k_R ≤ (R+1)³ − 1`;
(b) `Σ_{v∈Λ∩B(x,r)} A(v) ≤ 3Φ(R+1)⁵ r²` for all `x` and all `r ≥ 1`, i.e. `A`
is negligible with the **explicit packing-independent** constant
`C₁ = 3Φ(R+1)⁵`.

*Proof.* (a) Each term of the sum is bounded by `Φ` and there are at most `k_R`
of them; the balls `B(w,1)`, `w ∈ Λ∩B(v,R+1)∖{v}`, are disjoint, lie in
`B(v,R+2)∖B(v,1)` up to measure zero, and the volume comparison gives
`k_R ≤ ((R+1)³ − 1)` (using `vol B(0,s) = (4π/3)s³`).
(b) In `Σ_{B(x,r)} A` every pair with both ends inside `B(x,r)` contributes
`φ(v,w)+φ(w,v) = 0`. What remains are pairs with `v ∈ B(x,r)`, `w ∉ B(x,r)`,
`|v−w| ≤ R`: at most `k_R·#(Λ ∩ (B(x,r+R)∖B(x,r))) ≤ k_R·((r+R)³ − r³)` ordered
pairs, each contributing at most `Φ`.
**Arithmetic step, proved termwise.** `(r+R)³ − r³ = R(3r² + 3rR + R²)`, and for
`r ≥ 1 ≥ R·0`:
`R² ≤ 3r²R²`, `3rR ≤ 6r²R` (as `r ≥ 1`), `3r² ≤ 3r²` — so
`R(3r²+3rR+R²) ≤ 3Rr²(R+1)²` after dividing by `R > 0`. Hence
`3Φk_R·Rr²(R+1)² ≤ 3Φ(R+1)³·r²(R+1)² = 3Φ(R+1)⁵r²`. ∎
(The termwise form replaces the earlier "checked numerically" remark; it is also
the form the Lean lemma `cube_diff_le` states.)

**Why this matters for the project's goal.** Hales' proof spends a chapter
(Chapter 5: the `Q`-system, compatibility Lemma 5.28, and the four-way
cancellation of Lemma 7.10) establishing that `A` is negligible. If `A` is
presented as an antisymmetric bounded-range transfer, negligibility is the
two-line estimate above, with a constant that does not depend on the packing.
His four-way cancellation is precisely the antisymmetry bookkeeping, so
*recasting* his correction in transfer form is the natural simplification —
**flagged as Main's reading of his construction, not as a verified claim about
his text.**

**What it does not give.** Fcc-compatibility stays pointwise:
`Σ_w φ(v,w) ≥ √32 − vol Ω(v)` for every `v`. Summed over a region this says the
transfer must move exactly the deficit `√32 − vol Ω(v)` into each vertex, and
since the total flux over a large region is `O(r²)`, the *integrated* requirement
is `Σ_{B}(vol Ω(v) − √32) ≥ −C₁r²`, i.e. an averaged cell inequality — which is
`K15-C025`'s cluster form with H4 supplied. So `K15-C035` closes H4 and leaves
H2/H3 untouched. Reviewer X.

### K15-C036 — why the icosahedral fixture cannot test fcc-compatibility (`PROVED` obstruction)

`K15-C035` reduces the remaining obligation to the pointwise inequality
`Σ_w φ(v,w) ≥ √32 − vol Ω(v)`. A fixture would have to *verify* it at the
icosahedral vertex, where the deficit is `√32 − 5.550291 = 0.106563`. But:

- the Voronoi cells of a finite point set are unbounded, so a bare 13-point
  cluster has no volumes to sum;
- completing the cluster inside a finite region gives cells `Ω_K` *inside* the
  completion, and `Ω_K ⊇ Ω_{K'}` for `K ⊆ K'` (more bisectors only shrink), so
  every computed volume is an **upper** bound for the cell in any packing
  containing the cluster (`K15-E003`).

Hence a finite fixture can only ever **refute** the required lower bound; it can
never confirm it. This is the exact sense in which the transfer route is blocked:
`K15-C035` removes the negligibility work, and what remains is a pointwise
*lower* bound on Voronoi volume — an analytic inequality (Rogers/Fejes Tóth type),
not a computation. Main tested the arithmetic of the bound and did not run a completion search,
because by the monotonicity above it could not settle the question. **Two
different necessary bounds on `Φ`, which must not be confused:** at the
icosahedral vertex there are exactly **12** neighbours within range `R = 2`, so the
transfer must satisfy `Φ ≥ 0.106563/12 = 0.00888`; the counting bound
`k_R ≤ (R+1)³ − 1 = 26` gives only the weaker uniform statement
`Φ ≥ 0.106563/26 ≈ 0.0041`, which is a bound *every* packing satisfies but is not
what that vertex forces. (The earlier text quoted the 26-based figure as if it
were the vertex condition — corrected here.)

**Consequence for the ledger.** G5 (an analytic cluster-volume lower bound) is the
single remaining obligation on the geometric route; G4 and G6 are supplied or
bypassed by `K15-C035`; G7's "falsification test" is withdrawn with `C029`.

### K15-C037 — independent audit of the `K15-C002b` bridge and its zero-density case (`AUDITED`)

Main audited the repaired periodic-approximation lemma line by line.

1. **Tile count.** `#C_in(R)·S³ ≤ vol B(0,R)` is correct: interior tiles are
   disjoint and contained in the ball, so `#C_in ≤ vol(B(0,R))/S³`. This is the
   direction the original argument needed and did not state.
2. **Boundary loss.** Centres in `B(0,R)` outside the interior tiles lie in tiles
   meeting `S(0,R)`; a tile of side `S` meeting the sphere near the origin of a
   tile is contained in the shell of width `2S√3` about `S(0,R)`, which has volume
   `≤ 4πR²·(2S√3 + 2) = O(R²S)`. The centres there are 2-separated, so their
   number is at most the shell volume divided by `4π/3` — again `O(R²S)`. ✓
3. **Division.** `n(C*) ≥ (N(0,R) − O(R²S))/#C_in ≥ (N − O(R²S))·S³/vol B(0,R)`
   uses `1/#C_in ≥ S³/vol`, which follows from item 1. ✓
4. **Rate.** Dividing by `S³`: `n(C*)/S³ ≥ c − O(S/R)`, so for fixed `S` and
   `R = R(S) → ∞` the periodic packing has centre density `≥ c − O(1/S)` and
   occupied density `≥ δ(Λ) − O(1/S)`. The diagonal choice `S → ∞`, `R(S)/S → ∞`
   is what makes the `o(1)` uniform; that is the step the original text left
   implicit and it is now stated.
5. **Zero-density case.** If `δ(Λ) = 0` then `N(0,R) = o(R³)` and the conclusion
   `δ(Λ) ≤ (4π/3)f(0)/f̂(0)` is immediate (the right side is `≥ 0`); the periodic
   packing may be taken empty. No division by `c` occurs, so the lemma is
   vacuous-free. ✓
6. **Hidden dependency.** The reduction identifies the occupied-volume ratio with
   `(4π/3)·#(Λ∩B(0,R))/vol B(0,R)` up to `O(1/R)`; that is the counting-to-volume
   identity of `K15-C024` item 3. It is written out there and is used here
   implicitly — a reader of C002b alone would miss it.

*Verdict:* the bridge is correct as repaired. The only defect found is the
implicit dependency in item 6, which is now recorded. Reviewer X (this is Main
auditing Main's own repair, so an outside check is still required).

### K15-C038 — transfer fixture: the constant is valid but very loose (`TESTED_FINITE`)

- **Artifact.** `Computation/transfer_check.py` — builds fcc (1099 centres),
  draws a random rational antisymmetric transfer with `R = 2`, `Φ = 1`, forms
  `A(v) = Σ_w φ(v,w)`, and compares `Σ_{Λ∩B(0,r)} A` with `3Φ(R+1)⁵r²` for
  `r = 1..6`.
- **Result.** The bound holds at every radius, with observed sums of order
  `10⁰`–`10¹` against bounds of order `10³`–`10⁴`; `max|A| = 7.25` against
  `Φk_R = 26`. So `K15-C035`'s constant is *valid but loose by about three
  orders of magnitude* on this instance.
- **Why the looseness is acceptable.** Lemma 3.3's conclusion is
  `δ ≤ π/√18 + C/r` with `C` depending on `C₁`; a loose `C₁` slows the rate, it
  does not weaken the bound. A sharper `C₁` would matter only for a quantitative
  (finite-`r`) statement, which is not what the project needs.
- **Status.** `TESTED_FINITE` (arithmetic of the constant on one instance). The
  proof of `K15-C035` does not depend on this run.

### K15-C039 — icosahedral cluster fixture: what it shows and what it does not (`TESTED_FINITE`, scope corrected in-block)

- **Artifact.** `Computation/cluster_fixture.py` (scipy half-space intersections).
- **Robust output.** The centre's Voronoi cell computes to **5.550291**, matching
  `V_dod` to six decimals, and is **box-independent** (identical for boxes
  `3, 4, 6, 9`) and completion-independent whenever the completion keeps distance
  `≥ 2·1.2584 = 2.5168` from the centre. That is an independent numerical
  confirmation of `K15-C012` and a useful sanity check on the whole cell pipeline.
- **Not robust, and corrected twice.** The *cluster sums*
  `Σ_{v∈K}(vol Ω_K(v) − √32)` are dominated by the cavity between the core and the
  completion. With completions now **validated** to be packings (minimum over *all*
  pairs, including core–background, is `2.0000`), the nested sequence is
  `+157.87 → +63.71 → +63.71`. The original table (`… → +17.91`) came from
  completions that **overlapped the core** (minimum separation `1.25`) and was
  therefore meaningless. The *trend* (non-increasing as points are added) is the
  monotonicity of `K15-E003`/`K15-C036` and is real; the values carry no
  information about the cluster inequality in a packing.
- **What the fixture therefore establishes.** (i) `V_dod = 5.550291` numerically;
  (ii) nested completions shrink cell volumes monotonically, so every finite value
  is an upper bound and no finite stage decides the sign — the numerical form of
  `K15-C036`. Nothing else.
- **Status.** `TESTED_FINITE`. Reviewer X. (First version of the script used
  non-nested completions and a wrong fcc scaling; both were caught and fixed
  before the numbers were recorded.)
### K15-C040 — Lean: ball-volume identity drafted, build requested (`PROPOSED`)

`Lean/Kepler15/Volume.lean` states `volume (ball 0 1) = ofReal (4π/3)` and its
scaling form, with two named proof routes (`EuclideanSpace.volume_ball` at
`n = 3` with `Γ(5/2) = 3√π/4`, or Fubini). **Not compiled by Main** — the VM does
not run Lean. Request `M-LEAN-002` (1 CPU, 1 GB, 300 s) asks Astra for the pinned
build and axiom audit. Status stays `PROPOSED` until that log exists; the file
contains no `sorry` and is meant to be *revised* rather than patched if the lemma
names differ in v4.35.0.

### K15-C041 — independent quadrature audit of Main's Fourier map (`VERIFIED`; two defects in the audit script)

- **Run.** X's `Reviews/audit_shell_check.py` with their copy
  `Reviews/shell_check_main.py` (branch `kepler15/counterexamples/run-01`,
  `e3a63a1`) was executed by Main.
- **What it confirms.** Against **direct 3-D radial quadrature**, Main's
  `fourier_map` reproduces `f̂` with maximum relative errors `2.25e−15`,
  `3.19e−16`, `1.79e−15`, `4.91e−15` for four coefficient vectors, and it prints
  the same matrix `M` (column 3 = `(105/8, −105/4, 21/2, −1)`). This is a
  **third independent confirmation** of the map — Main's Laguerre-consistency
  check, Computation's `build_pq`, and now quadrature.
- **Two defects in the audit script** (reported, not fixed by Main):
  1. their copy hard-codes `PI_LO = PI_HI = float(π)`, so its "`PI_LO < π < PI_HI`"
     line prints `False` and the threshold-direction check is vacuous — the real
     file carries 29-digit rationals;
  2. it crashes at section 3 (`sp.real_roots` returns `Float` objects in this
     SymPy version, so `r.imag` raises), i.e. the odd-part part of their audit did
     not run. Main's own `checker_adversarial.py` covers that ground (13 cases).
- **Status.** `VERIFIED` for the quadrature confirmation; the audit script needs a
  repair before it can be quoted as a complete audit. Reviewer: X (their script,
  so the repair is theirs).

### K15-C042 — E's per-cell ceiling import (`ACCEPTED WITH SCOPE`; one number to query)

- **Claim (`K15-E048`, branch `kepler15/experimental/run-01`, `4ea4e8b`).** Every
  directional per-cell bound of the form
  `vol Ω(w) ≥ (1/3)∫_{S²} τ(u)³ du` with
  `τ(u) = min(known-neighbour terms, 1.045)` is at most
  `(4π/3)(1.045)³ = 4.780105…`; E's optimised value is `4.734`, within 1% of the
  ceiling, and both are far below the `5.5…` required.
- **Main's reading.** The ceiling is immediate once `τ ≤ 1.045` holds
  *everywhere*, which it does by construction: an unknown neighbour is at
  distance `≥ 2.09` (`K15-E014`), so its term is `≥ 2.09/(2cos φ) ≥ 1.045`. The
  substantive content is therefore the numerical optimisation reaching `4.734`
  and the conclusion that **this mechanism** cannot reach the threshold — not a
  new inequality.
- **Scope.** It bounds one *class* of directional arguments (those using `t ≥ min_z
  d_z/(2cos φ_z)`); it does not bound per-cell arguments using a body that is not
  star-shaped about `w`, as E says.
- **Query resolved by Main.** E's `5.665735` is `√32 + (√32 − V_dod)/12
  = 5.656854249 + 0.008880268 = 5.665734518` (agrees to `5e−7`): a threshold in
  which each of a vertex's twelve neighbours absorbs a twelfth of the icosahedral
  deficit. It is *not* `√32`, and the two must not be used interchangeably.
  Likewise E's `1.385321873` equals `13·(√32 − V_dod) = 1.385319…`, a 13-cluster
  total, not a per-cell difference. Consequently the quoted "2.08% shortfall" does
  not follow from either comparison: Main computes `16.44%` for `4.734` against
  `5.665735`, `16.31%` for `4.734` against `√32`, and `1.88%` for
  `√32 − V_dod` against `√32`. **Report the quantity being compared**; the
  arithmetic in the note is a factor/identity mix-up, not an error in E's
  optimisation.
- **Status.** `ACCEPTED WITH SCOPE` (Main's reading of the argument), the
  shortfall arithmetic **disputed pending the constant's definition**. Reviewer X.

### K15-C043 — Hales Lemma 3.3: independent re-derivation of the chain (`AUDITED`)

From the hypotheses of `K15-C002`'s companion (saturated `Λ`, negligible and
fcc-compatible `A`, `√32 ≤ vol Ω(v) + A(v)`), the inequality
`δ(x,r,Λ) ≤ π/√18 + C/r` follows in three steps. Main re-derived each:

1. **Occupied volume to count.** For a saturated packing,
   `vol B(x,r,Λ) = Σ_{v∈Λ(x,r+1)} vol(B(v,1) ∩ B(x,r)) ≤ |Λ(x,r+1)|·(4π/3)`:
   each ball contributes at most its own volume, and only centres within
   `r+1` can contribute. ✓
2. **Count to corrected volume.** `√32·|Λ(x,r+1)| ≤ Σ_{v∈Λ(x,r+1)}(vol Ω(v)+A(v))`
   by fcc-compatibility, and
   `Σ_{v∈Λ(x,r+1)} vol Ω(v) ≤ vol B(x,r+3)` because saturated packings have
   `Ω(v) ⊆ B(v,2)` and hence `∪_{v∈Λ(x,r+1)} Ω(v) ⊆ B(x,r+3)`; the `A`-sum is
   `≤ C₁(r+1)²` by negligibility. ✓ (So the correction may be *negative*
   anywhere — only the pointwise sum matters, which is why one-sided negligibility
   suffices.)
3. **Divide.**
   `δ(x,r,Λ) ≤ (4π/3)/√32 · (vol B(x,r+3) + C₁(r+1)²)/vol B(0,r)
   = (π/√18)(1+3/r)³ + (4π/3)C₁(r+1)²/(√32·(4π/3)r³)`.
   The first term tends to `π/√18` and the second is `O(1/r)`. ✓

**Verdict.** The chain is correct as printed (the page image `X-SRC-01` shows the
`√32` that the text layer drops). No gap found. This is the *only* place the
dodecahedral constant enters the project's target: Lemma 3.3 needs
`√32 = 5.656854`, not `5.550291`. Reviewer X.

### K15-C044 — the exact feasibility criterion for a transfer (`PROVED`, corrected the same block)

**Setting.** `Λ` a packing, `b(v) := √32 − vol Ω(v)`, and the transfer graph `G_R`
joining centres at distance `≤ R`, each edge carrying capacity `Φ`.

**Criterion (Hoffman / Gale).** There is an antisymmetric `φ` on `G_R` with
`|φ| ≤ Φ` and `Σ_w φ(v,w) ≥ b(v)` for all `v` **iff** for every finite `U ⊆ Λ`
```
Σ_{v∈U} b(v)  ≤  Φ · |δ⁺_R(U)|,        δ⁺_R(U) = edges from U to Λ∖U.
```
(Add a supersource/supersink; this is the max-flow min-cut condition.)

**Correction history.** The first version of this entry claimed the criterion was
"`Σ_U b ≤ 0` for every union of connected components", presented as an `iff`.
That is wrong in two ways: (i) it is only the *no-out-edge* case of the cut
condition; (ii) for a transfer graph that is connected — as `G_R` is for fcc with
`R ≥ 2` — there are no proper unions of components, so the condition is vacuous
and the real content is entirely in the cut condition. Recorded because the
overclaim is exactly the kind this block exists to remove.

**What the criterion says, in the two regimes.**
- `R < 2` (graph = isolated vertices): the condition is `b(v) ≤ 0` for each `v`,
  i.e. **pointwise** fcc-compatibility — the Hales requirement.
- `R ≥ 2` on a connected graph: for a large blob `U`,
  `Σ_U b ≤ Φ|δ⁺(U)| = O(Φ·|U|^{2/3})`, i.e.
  `Σ_{v∈U} vol Ω(v) ≥ √32|U| − O(Φ|U|^{2/3})` — an **averaged, global** inequality
  with an explicit `o(|U|)` slack, not a local one.

So the transfer formulation delivers exactly what the averaging formulation
delivers, with the extra slack `Φ|U|^{2/3}` paid for by `Φ`; it never weakens the
requirement below the averaged inequality. **The gain is confined to
negligibility** (`K15-C035`), which is real but is bookkeeping, not geometry.

*Status.* `PROVED` (standard flow duality). Reviewer X.

### K15-C045 — structural reading: where the transfer route actually stands

Combining `K15-C035`, `K15-C036`, `K15-C043` and `K15-C044`:

1. A bounded-range antisymmetric transfer is automatically negligible (`C035`),
   so Hales' Chapter 5 (the `Q`-system, Lemma 5.28, the four-way cancellation of
   Lemma 7.10) is replaceable by a two-line estimate — **the one simplification
   this line of work has produced**.
2. The price is the cut condition of `C044`. On a connected transfer graph it is
   the *global averaged* inequality
   `Σ_U vol Ω ≥ √32|U| − O(Φ|U|^{2/3})`; on a disconnected graph (`R < 2`) it is
   the pointwise inequality. There is no regime in which the requirement is both
   local and weak.
3. Neither version can be established by computation (`C036`: finite completions
   bound cell volumes only above).
4. Therefore the remaining mathematical content is exactly **an analytic averaged
   lower bound for `Σ vol Ω`**, equivalently Kepler's inequality in averaged form.
   Not a shortcut; the honest location of the difficulty.

*Status.* `PROVED` given C035/C036/C044 (a synthesis, not a new inequality).
Reviewer X.

### K15-C046 — import of C's shell proposers (`TESTED_FINITE`; no verdict yet)

- **Artifacts.** `Computation/shell_sos.py`, `Computation/shell_propose.py` and
  their JSON outputs (branch `kepler15/comp-01a1d8c0`, `5c10267`).
- **What is good.** C adopts Main's basis (`u = π|x|²`) and Main's checker for the
  verdict, explicitly refusing to certify from an LP objective — the interface of
  `Main/INTERFACE.md` is being used as intended. They also caught that the
  *then-current* `shell_check.check` hardcoded `T_HI = 27/2`, which is invalid at
  `ρ = 2.05`; that has since been parameterised (`t_hi_for(ρ)`), so their
  workaround is no longer needed and their own per-`ρ` handling is compatible.
- **What it does not give.** Every `verdict` field in `shell_sos.json` is `null`:
  no candidate has passed the exact check. The best LP objective at degree 7 is
  `0.3161`, i.e. `Δ ≈ 1.32` — vacuous. Their `n = 27, ρ = 2.05` row is correctly
  labelled unconditional and `n = 12, ρ = 2.09` conditional on Tammes.
- **Status.** `TESTED_FINITE` (proposer only). Not a bound; nothing to import into
  `RESULTS.md`. Reviewer X. The proposer is the right shape; the missing piece is
  a family rich enough to reach `R ≈ 0.186` at moderate degree, which no proposer
  in this project has yet achieved.

### K15-C047 — E's `verify_all_claims.py` re-run by Main (`CONSISTENT`, not independent)

`Experimental/scripts/verify_all_claims.py` (branch `kepler15/experimental/run-01`,
`4ea4e8b`) was executed from a scratch directory: **23/23 items pass**, including
the Tammes enclosure values (`δ₁₃ < 57.138726938°`, `θ_min > 57.170897332°`), the
`ρ = 2.05` and `2.09` cosine thresholds (`0.524092801904`, `0.542135024381`), the
`√5 − 1` scope constant, and the `K15-E048` ceiling `(4π/3)(1.045)³ = 4.780105486`.
This is a *consistency* check on E's own numbers (E wrote both the claims and the
script), useful but **not** independent evidence; the independence comes from
Main's separate re-derivations (`K15-C027`, `K15-C042`).

### K15-C048 — re-verification against the *current* Computation artifacts (`VERIFIED`, repeat of C023/C031)

After C advanced to `5c102677…`, Main re-ran both checks:

- `checker_adversarial.py --against-exactcert` on the current `exactcert.py`:
  **agrees on every case** (including `p=-(u-T)^2 → neg`, and the two
  endpoint-root `fail` cases);
- `verify_certificate.py out/cert.json` on `out/verified_certificate_K33b.json`:
  `ACCEPT` by both of C's implementations, `p0/q0` unchanged, `Δ ≤ 0.779966216777`.

So the interface (`K15-C023`, `K15-C031`) survives C's updates; nothing in the
last two blocks' verification was version-specific.

### K15-C049 — sign predicates falsely accepted positivity between endpoint roots (`REFUTED`; algorithm SUPERSEDED by `K15-C058`)

- **The defect (reported by local reproduction at `6626714`).** The three
  predicates `le_on_interval`, `nonneg_on_half_line`, `_ray` returned `True` for
  - `u(1−u) ≤ 0` on `[0,1]` — value `+1/4` at `u = 1/2`;
  - `u(u−1) ≥ 0` on `[0,∞)` — value `−1/4` at `u = 1/2`;
  - `u(1−u) ≤ 0` on `[0,∞)` — the same `+1/4`.
- **Root cause, two independent faults.**
  1. `_count_roots`/`_roots_in` used `V(lo) − V(hi)`, which counts the distinct
     roots in `(lo, hi]`, and then subtracted a root at **`lo`** instead of `hi`.
     A root at `hi` was therefore counted and never removed, and a root at `lo`
     was removed twice.
  2. Even with a correct count, testing **only the endpoints** when the odd part
     had no root strictly inside is invalid whenever *both* endpoints are roots:
     `u(1−u)` has odd roots exactly at `0` and `1`, is zero at both ends, and is
     positive in between.
- **The repair (general, not special-cased).** Sign changes are counted on the odd
  part with the correct endpoint convention; when the count is zero the sign is
  constant and three probes (endpoints and midpoint) decide it; when the count is
  positive, roots are isolated (`Poly.intervals`) and one rational test point is
  taken in **every gap between consecutive roots** plus the endpoints. That is
  exact: a polynomial's sign is constant between consecutive roots.
- **Regression fixtures, kept permanently** in `Computation/checker_adversarial.py`
  (now 19 cases): the three reported polynomials must FAIL;
  `−(u−1/2)² ≤ 0` on `[0,1]` and `(u−1/2)² ≥ 0` on `[0,∞)` must PASS (touching);
  `u(u−1) ≤ 0` on `[0,1]` must PASS (negative between two endpoint roots — the
  exact mirror of the reported case). The suite also caught an error in *one of my
  own new fixtures* (`u(u−1) ≤ 0` on `[1,3]`, which is false), which is the point
  of keeping it.
- **Re-verification after the repair.** `--self-test` ALL PASS; adversarial suite
  19/19; the K33b certificate still `ACCEPT` with the **identical** ratio
  `42935541634304122537361009/230584315533749727927712550` and
  `Δ ≤ 0.779966216777`; `shell_fixture.py` returns the **unchanged**
  `R = 0.5383822578566787`; the `--against-exactcert` cross-run still agrees.
  So no published number moved — but the *general* soundness claim does move:
- **Suspended until audited.** The sentence "the two checkers agree and are
  therefore both correct" in `K15-C023`/`C031` is downgraded: the checkers agree,
  and the K33b certificate passes a repaired checker, but the repaired predicate
  has **not** been independently audited. Per instruction, general acceptance
  claims are suspended until X audits `shell_check.py` at this revision. The
  *particular* K33b certificate does not depend on that audit: Computation's
  strict checker and the SymPy oracle both accepted it, and it is unchanged.
- **Not mine, reported for routing.** X's `audit_K33_signs.py` accepts
  `(t²−2)(t²−3) ≥ 0` on `[0,∞)` although its value at `3/2` is `−3/16`: irrational
  roots are silently discarded by its root handling — the same class of defect.
  Routed to X (their file).
- **File.** `Computation/shell_check.py`, repaired this block; the reproducer
  lives at `Main/LocalChecks/2026-11-14_0138/reproduce_sign_defects.py`
  (supervisor branch).

### K15-C050 — differential fuzz of the repaired predicates (`TESTED_FINITE`; no false accept in 799 random cases)

- **Artifact.** `Computation/predicate_fuzz.py`. For random integer polynomials of
  degree ≤ 6 it compares the exact predicate against a 40 001-point sample on
  `[0,40]` (resp. `[A,40]`, `[lo,hi]`) and flags only the dangerous direction:
  *predicate says the condition holds* while the sample exhibits a violation.
- **Result.** 799 random polynomials, **zero** false accepts, across all three
  predicates (`nonneg_on_half_line`, `_ray`, `le_on_interval`). The reverse
  disagreement is expected and not counted (a violation may lie beyond the sampled
  range).
- **Scope.** This is a bug-hunt, not a proof: it cannot establish the predicates'
  soundness, and by construction it only sees violations inside `[0,40]`. The
  soundness argument is the mathematical one in `K15-C049` (sign constant between
  consecutive roots, one test point per gap).
- **Timing note.** An earlier run with `--n 800` was used; the script is
  deterministic given `--seed`.
- **Status.** `TESTED_FINITE`. Reviewer X: run it with a different seed and a
  higher degree, and audit the `_test_points` gap construction.

### K15-C051 — search for a periodic witness that a blob needs out-flux (`NEGATIVE SEARCH`)

- **Target (from `K15-C044`).** A periodic packing with a blob `U` where
  `Σ_U b > 0` (i.e. locally denser than fcc) and `|δ⁺(U)|` small would show that
  the cut condition genuinely needs out-edges at bounded `Φ`.
- **What was tried.** The 13-cluster centred in a cubic box of side `L` with the
  eight corners occupied (periodic Voronoi cells computed on a 3×3×3 replication,
  `L = 5.0` to `6.6`, all with minimum separation exactly 2):
  `Σ_{13}(vol Ω − √32) = +34.94, +61.41, +91.51, +125.41, +163.29`.
  All **positive**, and growing with `L`: the cluster's neighbours' cells are
  inflated by the empty space around them, so the box density (not the cluster)
  dominates.
- **Why this is expected, and why it is not a refutation.** A blob with
  `Σ_U b > 0` is precisely a region whose *local* density exceeds fcc. Simple
  periodic constructions put the cluster in a *sparse* environment, which makes
  every cell large; producing a locally dense environment around an icosahedral
  core is the Frank–Kasper problem, and icosahedral order is famously incompatible
  with periodicity. So the search is a negative result about *easy* witnesses, not
  about the cut condition.
- **What it means for the programme.** The cut condition is not refuted; the open
  problem is *quantitative*: either exhibit a periodic packing with
  `Σ_U b > Φ|δ⁺(U)|` for `Φ` below the transfer needed elsewhere, or prove the cut
  condition with an explicit `Φ`. `Main/NEXT_PACKAGE.md` item 3 stands with this
  lesson recorded.
- **Status.** `NEGATIVE SEARCH` (nothing found in the tested family). Reviewer X.

### K15-C052 — every quoted constant re-derived by one script (`VERIFIED`)

- **Artifact.** `Computation/constants_check.py`: 22 checks, **ALL PASS**, of
  every constant the ledger quotes — `4π/3`, `V_dod = 5.550291028515510`,
  `0.754697399337`, `π/√18 = 0.740480489693`, `√32 = 5.656854249492`,
  `σ₃ = 0.779635570044` and `V_Rogers = 5.372754099135`, the two required
  improvements (`1.05288` over Rogers, `1.0192` over dodecahedral, i.e. 5.29% and
  1.92%), the Tammes thresholds at `ρ = 2.02, 2.05, 2.09` (`0.509852, 0.524093,
  0.542135` and `59.346°, 58.393°, 57.171°`), `23681/43681` at `ρ = 2.09`, the
  transfer constants `3Φ(R+1)⁵ = 729` at `(Φ,R) = (1,2)` and `1598.29` at
  `R = 2.51`, `Φ ≥ 0.0041` at the icosahedral vertex, and the K33b ratio and
  `Δ = 0.779966216777`.
- **What it caught.** Three of the script's first-run failures were *my own*
  rounded placeholders in the check (`1.01920` against `1.01919957…`), not ledger
  errors: the ledger's percentages (5.29%, 1.92%) are correct. The placeholders
  were replaced by the exact values with a `1e−5` tolerance.
- **Status.** `VERIFIED`. Reviewer X: run it before quoting any constant.

### K15-C053 — one command runs every check (`VERIFIED`: 8/8 in 6.8 s)

- **Artifact.** `Computation/run_all_checks.py`: runs the constants re-derivation,
  the sign-predicate self-test, the 19 adversarial cases, the differential fuzz, the
  transfer-lemma fixture, the cluster fixture and the interface dictionary, and —
  with `--cert` — a certificate verification. Final run: **8 checks, 0 failed,
  6.8 s, 1 core**.
- **Why it matters for the next block.** The review-0138 defect survived both a
  self-test and a hand-written adversarial suite; what finally caught it was a
  *local reproduction of the reported inputs*. A single entry point makes such a
  regression runnable in one command by Astra and by X, so a repair cannot be
  reported as complete without it.
- **Reproduce.**
  `python3 KeplerConjecture/Computation/run_all_checks.py --cert <certificate.json>`
  (`--quick` skips the fuzz).
- **Status.** `VERIFIED`. Reviewer X.

### K15-C054 — the transfer graph at range `R ≤ 2.09` has degree `≤ 12` (`PROVED`, from the count)

- **Statement.** Let `Λ` be 2-separated and `G_R` the graph joining centres at
  distance `≤ R`. For `2 ≤ R ≤ 2.09` every vertex of `G_R` has degree `≤ 12`,
  because every neighbour lies in the annulus `[2, 2.09]` and `K15-E014` bounds
  that count by 12.
- **Why it is the right range.** `R = 2` is the contact graph; `R = 2.09` is the
  widest range the Tammes enclosure covers. Within it the transfer graph is
  **local and degree-bounded**, which is exactly the structure the cut condition
  of `K15-C044` and the constant of `K15-C035` (`3Φ(R+1)⁵`) want: `k_R ≤ 12`
  beats the volume bound `(R+1)³ − 1 = 26` by a factor 2, and the shell count is
  a *theorem*, not an assumption (K15-C027).
- **Consequence for the constant, computed.** From the proof of `K15-C035`,
  `C₁/Φ = 3·k_R·R·(R+1)²`. With `R = 2.09`: `k_R = 12` (this lemma) gives
  `C₁/Φ = 718.40`, while the volume bound `k_R ≤ 26` gives `1556.53` and the
  published general form `3(R+1)⁵ = 845.11` sits between them. So the shell count
  buys **15% off** the general constant at the widest certified range (not a
  factor of two, because `3(R+1)⁵` mixes the `k_R` and shell factors).
- **Quantitative footprint of a hypothetical transfer.** Combining the two
  constraints: the icosahedral vertex forces `Φ ≥ 0.00888` (12 neighbours) and the
  negligibility constant at `R = 2.09` is `C₁/Φ = 718.40` (this lemma), so
  `C₁ ≥ 6.38` for any transfer that works there. Lemma 3.3 then gives
  `δ(x,r,Λ) ≤ π/√18 + C/r` with `C` of order a few — i.e. **a transfer
  construction would have a usable rate**, unlike a construction that needs a huge
  `Φ`. Nothing here assumes such a transfer exists.
- **Status.** `PROVED` (immediate from `K15-E014`). Reviewer X.

### K15-C055 — independent cross-check of the repaired predicates via `function_range` (`VERIFIED`)

- **Artifact.** `Computation/predicate_crosscheck.py`. SymPy's `function_range`
  computes the exact range of a polynomial on an interval by a **different route**
  (critical points plus endpoints, no Sturm chain), so agreement is real evidence
  that the repaired `K15-C049` predicates are right.
- **Result.** Five fixed cases (the three reported defects, `u(u−1) ≤ 0` on
  `[0,1]` which must PASS, and `(u−5)² ≤ 0` on `[0,10]` which must FAIL) all agree
  with `sup` values `1/4, 0, 0, 1/4, 25`; plus 20/20 random degree-≤3 polynomials
  on compact intervals, zero disagreements.
- **Combined with `K15-C050`** (differential fuzz on half-lines, 799 cases, zero
  false accepts), the repaired predicates now have three independent supports: the
  mathematical argument, `function_range`, and sampling. That is as much as can be
  done without X's audit.
- **Reproduce.** `python3 Computation/predicate_crosscheck.py` (0.6 s).
- **Status.** `VERIFIED`. Reviewer X.

### K15-C056 — both K33 variants pass the repaired checker, values match C's report (`VERIFIED`)

- `verified_certificate_K33.json` (variant a): `ACCEPT`, ratio
  `57247406970676848810768955/307445740617578019715085691 = 0.186203285353`,
  `Δ ≤ 0.779966497784`.
- `verified_certificate_K33b.json` (variant b): `ACCEPT`,
  `Δ ≤ 0.779966216777`.
- Both agree with Computation's own reported pair (`0.77996650` / `0.77996622`
  from their PROGRESS), which is an independent confirmation of *their* numbers
  through Main's repaired checker and of *Main's* checker through known-good data.
- Neither is an improvement on CE03 (`0.779747`); both are `VERIFIED_CROSS`-grade
  components at their stated scope.

### K15-C057 — E's interval self-audit re-run by Main (`PASSED`; method worth copying)

- **Run.** `Experimental/scripts/interval_selfaudit.py` (branch
  `kepler15/experimental/run-01`, `4ea4e8b`, cwd set so that its relative import
  of `Experimental/scripts/tammes13_enclosure.py` resolves).
- **Result.** `118` point-interval soundness checks with `0` failures; monotone
  wrapper endpoints `0` failures; a **deliberately corrupted** primitive
  (swapped endpoints) detected in `50/50` intervals; the constructor rejects
  `lo > hi`; `333/106 < π < 355/113` confirmed.
- **Why it matters beyond E's own use.** The audit has two halves —
  *soundness* (enclosures contain the true value, checked against high-precision
  arithmetic) and *sensitivity* (a known corruption **must** be caught). That
  second half is exactly what was missing from Main's sign-predicate tests, which
  passed while the predicates were unsound (`K15-C049`). Recommend the pattern for
  every checker in this project: a test suite is not evidence unless it can fail.
- **Status.** `PASSED` (Main re-ran it; E wrote the audit, so this is a
  reproducibility check plus a methodological endorsement, not independence).
  Reviewer X.

### K15-C028 addendum 2 — the `η > 0` path passes exactly (vacuous, as predicted)

After the `K15-C049` repair, the fixture's shell family was exercised end-to-end
with a genuine allowance: `--m 2 --rho 209/100 --eta 3` returns **all conditions
PASS** and the exact bound
`R = (p(0)+12η)/q(0) = 52574263623381858614976224187487229/4074263623381858614976224187487229
= 12.90399`, i.e. `Δ ≤ 54.052` (rational `π` enclosure).

This is the first *passing* exact shell-allowance certificate in the project — and
it is vacuous by construction, because the allowance costs `12η = 36` in a
functional whose useful range is below `0.2`. That is the whole content of
`K15-C028`: the machinery works; the trade is hopeless at low degree, and
`K15-C036`-style sampling cannot tell whether it improves at high degree.

### K15-C058 — SECOND-round predicate defect: perfect squares defeat the odd part (`REFUTED`, repaired; supersedes C049's algorithm)

- **What was still wrong.** After the `K15-C049` repair, three *new* witnesses were
  found by fixed probes:
  1. `[u(u−1/2)(u−1)]² ≤ 0` on `[0,1]` returned `True`, though the value at `1/4`
     is `+9/4096`;
  2. `−[u(u−1)(u−1/2)(u−2)]² ≥ 0` on `[0,∞)` returned `True`, though the value at
     `1/4` is `−441/65536`;
  3. `[u(u−1)(u−2)]² ≤ 0` on `[0,∞)` returned `True`, though the value at `1/2` is
     `+9/64`.
- **Root cause.** The `C049` algorithm decided the sign from the **odd part** and,
  when the odd part had no root in the region, probed only `lo`, `(lo+hi)/2`, `hi`.
  For a perfect square every factor has even multiplicity, so the odd part is a
  **constant**: the count is zero and the three probes can all land exactly on
  roots (indeed `0, 1/2, 1` are the roots of the first witness). Concluding "sign
  constant, probes ≤ 0, accept" was then wrong. The earlier code comment claimed
  "three roots at these points ⇒ `p ≡ 0`", which is false for degree ≥ 4.
- **The repair (algorithm changed, not patched).** The odd part is **removed
  entirely**. Test points now come from the roots of the polynomial *itself*:
  isolate all real roots in the region, and evaluate at the endpoints plus one
  rational point in every gap between consecutive roots (and two more per gap for
  safety). A root is a test point with value `0`, so touching cases pass, and a
  gap always carries a point where the sign is decided. `_odd_part` and
  `_count_roots_open` are deleted from `shell_check.py`.
- **Regressions kept permanently** (`Computation/checker_adversarial.py`, now 24
  cases): the three new witnesses, a variant on `[2,3]` where the square is
  positive, and `−[u(u−1)(u−2)]² ≤ 0` on `[0,3]` which must PASS.
- **Re-verified after the second repair.** All six witnesses (three old, three new)
  rejected; all valid/touching cases accepted; suite 24/24; the K33b and K33
  certificates still `ACCEPT` with unchanged ratios; `shell_fixture` unchanged;
  fuzz on seeds `5, 21, 22, 23` (1100 polynomials) and `function_range` cross-check
  with 25 fresh random cases: no disagreement.
- **The fuzz itself needed the same scrutiny.** Its new *structured* pass (perfect
  squares with rational roots) first reported 19 "false accepts" that were a bug in
  the test (`_ray(−p)` instead of `_ray(+p)`); after the fix it reports 0. The
  lesson is the block's theme: a test is only evidence once it has been checked for
  the ability to be wrong.
- **Status.** `REFUTED` (the `C049` algorithm) → repaired. **Generic checker
  acceptance stays suspended** until X audits this revision; X's own `exact_sign`
  repair (`cb3d76f`) passed the irrational-root witness and six named controls
  locally, which is finite test evidence, not blanket soundness.

### K15-C059 — audit request published (`PROPOSED` work item)

`Main/AUDIT_REQUEST_X.md` lists what X should check at the current revisions:
the repaired predicates (four specific questions), the two K33 certificates under
three implementations, and the seven claims added this block with the point to
attack in each. It also lists the claims that do **not** depend on the predicates,
so that a defect in the checker cannot be mistaken for a defect in the mathematics.

### K15-C060 — the shell count holds for every `ρ ≤ 2.09`, not just `2.09` (`PROVED`)

`K15-E014` states that a 2-separated set has at most 12 points in `[2, 2.09]`.
For any `ρ ≤ 2.09` the annulus `[2, ρ]` is a *subset* of `[2, 2.09]`, so the same
bound applies: `n(ρ) ≤ 12` for every `2 ≤ ρ ≤ 2.09` — and 12 is attained at every
such `ρ` by the icosahedral twelve (whose nearest mutual distance is `2.1029… > ρ`
only for `ρ < 2.1029`, which covers the range).

**Why it matters for the benchmark.** The shell allowance `K15-C018` can be posed
at any width up to `0.09` and the count is free; the threshold `ρ` is then chosen
only by the trade between the relaxation's gain and the cost `12η`. And since the
closed form `δ ≤ (4π/3)(f(0)+12η)/f̂(0)` is monotone in nothing else, larger `ρ`
is never worse *in the theorem* (the profile at a larger `ρ` is also admissible at
a smaller one). So `ρ = 2.09` is the natural choice and no separate enclosure is
needed per width.

*Status.* `PROVED` (immediate from `K15-E014`). Reviewer X.

### K15-C061 — code index and a higher-degree fuzz (`TESTED_FINITE`)

`Computation/README.md` indexes every tool Main ships, with commands and runtimes,
the conventions in one paragraph, and the three warnings the block produced
(grid signs are worthless; a test must be able to fail; test points must come from
the polynomial's own roots).

Added with it: a **degree-12** fuzz run (`--n 200 --deg 12 --seed 77`), 199
polynomials, zero false accepts — the earlier runs were degree ≤ 6, where the
isolating-interval code is barely exercised.

### K15-C062 — the repaired predicates scale (`TESTED_FINITE`)

Timing on deliberately hostile inputs (`u`-variable, rational coefficients):
a degree-33 polynomial with seven simple roots inside the region is decided in
`0.01 s`; the same polynomial squared (degree 66, every root of even multiplicity,
which is the shape that broke both earlier algorithms) in `0.07 s`; a degree-200
synthetic case is not needed because the K33 certificates themselves are decided in
about `2 s` including the basis conversion. All three hostile verdicts were
correct (`False`, `False`, `False`, as the root pattern requires).

Scope: timing on this VM, single core, sympy only. The certificate path is the
slowest real use and stays far below the 300 s cap.

### K15-C063 — X's `audit_K33_signs.half_line_verdict`: exact diagnosis (`REFUTED`, fix identified)

- **Reproduced.** On the file at `e3a63a1`
  (`Counterexamples/Reviews/K33/audit_K33_signs.py`), the call
  `half_line_verdict((t²−2)(t²−3), a = 0, want = +1)` returns **`True`**, although
  the polynomial equals `−3/16` at `t = 3/2`.
- **Exact cause, in their code:**
  ```python
  try: rn = sp.Rational(sp.nsimplify(r))
  except Exception: rn = None
  if rn is not None and rn > a: odd.append(...)
  ```
  For `r = √2` (returned by `real_roots` as a radical, as the code prints
  `[-sqrt(2), sqrt(2)]`), `sp.Rational(√2)` raises `TypeError`; the `except` sets
  `rn = None` and the root is **silently dropped**. The `try/except` turns "this
  root is irrational" into "there is no root", which is the failure the review
  named.
- **Fix (one line).** Never convert the root: test `sp.sign(sp.N(r - a, 30)) > 0`,
  or keep the algebraic number and compare symbolically. More generally: an
  exception in a sign test must be a *failure*, never an absence.
- **Also confirmed good.** The same file, run on the real data, `ACCEPT`s K33 with
  `Δ = 0.779966498`, matching Main (`0.779966497784`) and Computation — three
  implementations, one value — and reports that `q`'s minimum on `[0,300]` is
  `3.708e−6` near `t = 10.332`, i.e. the certificate is legitimately
  near-tangency and float checks are unsafe there. Its two "NEGATIVE" controls
  (`c0 += 1/1000`, `c1 += 1/1000`) are accepted with worse bounds
  (`0.783371916`, `0.787430829`), which is correct behaviour — a worse bound is
  still a bound — and the label is misleading, not the verdict.
- **Status.** `REFUTED` (their routine), routed to X with the fix. No project claim
  used their routine; the K33 value above is unaffected.

### K15-C064 — fuzz now covers the two structured families that broke checkers (`TESTED_FINITE`)

`predicate_fuzz.py` gained two structured passes on top of the random one:

1. **perfect squares** with rational roots (the family of `K15-C058`) — 0 false
   accepts;
2. **irrational roots** — products `(u²−a)(u²−b)` with non-square `a, b`, the
   family that defeats X's routine (`K15-C063`) because a root like `√2` cannot be
   converted to a `Rational`. Both the nonnegativity and the compact-interval
   claims are probed at rational points whose exact signs are known — 0 false
   accepts.

Seeds `55, 61, 62` (600 polynomials total) clean. The point of these passes is
that **uniform random coefficients never produce either family**, which is why
three successive checkers passed their "random" tests while being wrong.
