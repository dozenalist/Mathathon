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
- **Fix.** Sign changes are now counted on the **odd part** of the polynomial
  (`sqf_list`, keep factors of odd multiplicity), with endpoints tested for the
  required sign, and `≤` (not `<`) as the verdict. Regression cases are now
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
