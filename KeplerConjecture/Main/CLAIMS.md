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

### K15-C013r — counting envelope: corrected statements (`PROVED` for (a)-(c), open for an explicit width `δ₀`)

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

### K15-C020 — path from E's count to C's evaluated benchmark (specification, `PROPOSED`)

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

### K15-C021 — checker bugs recorded from X and the local checks (`REFUTED` items, kept as evidence)

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

### K15-C028 — exact shell fixture at degree 3: why the allowance cannot pay (`TESTED_FINITE`, exact verdicts)

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

### K15-C028 addendum — reference output of the fixture (`TESTED_FINITE`, reproducible)

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
(b) `Σ_{v∈Λ∩B(x,r)} A(v) ≤ 3ΦR(R+1)⁵ r²` for all `x` and all `r ≥ 1`, i.e. `A`
is negligible with the **explicit packing-independent** constant
`C₁ = 3ΦR(R+1)⁵`.

**Correction (review 0223, X).** The first version of this entry printed
`C₁ = 3Φ(R+1)⁵`, which **drops a factor `R`**: the count of crossing pairs is
`k_R·((r+R)³ − r³)`, and `(r+R)³ − r³ ≤ 3R(R+1)²r²` already carries `R`, so
`k_R ≤ (R+1)³` gives `3ΦR(R+1)⁵r²`. At `R = 2.09, Φ = 1` the correct value is
`1766.28`, not `845.11`. The *sharper* numbers quoted later are unaffected
because they were computed from `3·k_R·R·(R+1)²` with the `R` included:
`718.40` at `k_R = 12` and `1556.53` at `k_R = 26`.

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
`3Φk_R·Rr²(R+1)² ≤ 3ΦR(R+1)³·r²(R+1)² = 3ΦR(R+1)⁵r²`. ∎
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
  `A(v) = Σ_w φ(v,w)`, and compares `Σ_{Λ∩B(0,r)} A` with `3ΦR(R+1)⁵r²` for
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

### K15-C042 — E's per-cell ceiling import (`ACCEPTED_WITH_SCOPE`; constant identified)

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

- **Artifact.** `Computation/constants_check.py`: 28 checks, **ALL PASS**, of
  every constant the ledger quotes — `4π/3`, `V_dod = 5.550291028515510`,
  `0.754697399337`, `π/√18 = 0.740480489693`, `√32 = 5.656854249492`,
  `σ₃ = 0.779635570044` and `V_Rogers = 5.372754099135`, the two required
  improvements (`1.05288` over Rogers, `1.0192` over dodecahedral, i.e. 5.29% and
  1.92%), the Tammes thresholds at `ρ = 2.02, 2.05, 2.09` (`0.509852, 0.524093,
  0.542135` and `59.346°, 58.393°, 57.171°`), `23681/43681` at `ρ = 2.09`, the
  transfer constants `3ΦR(R+1)⁵ = 1458` at `(Φ,R) = (1,2)` and `4011.72` at
  `R = 2.51` (the pre-0223 figures `729` and `1598.29` dropped the factor `R`), `Φ ≥ 0.0041` at the icosahedral vertex, and the K33b ratio and
  `Δ = 0.779966216777`.
- **What it caught.** Three of the script's first-run failures were *my own*
  rounded placeholders in the check (`1.01920` against `1.01919957…`), not ledger
  errors: the ledger's percentages (5.29%, 1.92%) are correct. The placeholders
  were replaced by the exact values with a `1e−5` tolerance.
- **Status.** `VERIFIED`. Reviewer X: run it before quoting any constant.

### K15-C053 — one command runs every check (`VERIFIED`: 8/8 in 6.8 s)

- **Artifact.** `Computation/run_all_checks.py`: runs the constants re-derivation,
  the sign-predicate self-test, the adversarial suite (35 cases), the differential fuzz, the
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
  of `K15-C044` and the constant of `K15-C035` (`3ΦR(R+1)⁵`) want: `k_R ≤ 12`
  beats the volume bound `(R+1)³ − 1 = 26` by a factor 2, and the shell count is
  a *theorem*, not an assumption (K15-C027).
- **Consequence for the constant, computed.** From the proof of `K15-C035`,
  `C₁/Φ = 3·k_R·R·(R+1)²`. With `R = 2.09`: `k_R = 12` (this lemma) gives
  `C₁/Φ = 718.40`, while the volume bound `k_R ≤ 26` gives `1556.53` and the
  general form (corrected, `3R(R+1)⁵`) gives `1766.28`. So the shell count buys
  **59% off** the general constant at the widest certified range, and **2.2×** off
  the volume-bound version.
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

### K15-C028 addendum 2 — the `η > 0` path passes exactly (`TESTED_FINITE`, vacuous as predicted)

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

### K15-C065 — C's bidirectional cross-validation, imported with one caveat (`IMPORTED`)

- **Their claim (`K15-C-XVAL-002`, branch `kepler15/comp-01a1d8c0`).** Both
  directions work: their degree-33 certificate (`0.77996622`) is accepted by
  Main's `shell_check` at `T_LO = 4π_lo`, and a degree-33 *shell* certificate is
  accepted by their `exactcert` in strict mode at `0.780338357535` against
  `shell_check`'s `0.780338357611` — agreement to ten digits.
- **Why it is good news.** A wrong entry in `M`, a wrong `π` enclosure direction,
  or a mis-mapped `t ↔ u` would break one of the two directions. Neither breaks, so
  the convention dictionary of `Main/INTERFACE.md` is now tested in both
  directions on real degree-33 data.
- **Caveat Main adds.** Their note reads "`shell_check`'s `T_LO = 12` default is
  sound but pessimistic (it can only reject valid certificates, never accept
  invalid ones)". The second half of that sentence is **false for the predicates**:
  `K15-C049` and `K15-C058` were both false-*accept* defects, unrelated to `T_LO`.
  The threshold argument is correct in itself (a smaller start point only
  strengthens a `≤ 0` requirement); the general soundness inference is not, and
  must not be used as evidence. Also, `T_LO` is now `4·PI_LO`, not `12`.
- **Status.** `IMPORTED` (their evidence, verified in one direction by Main's own
  runs in `K15-C023`/`C056`). Full acceptance awaits X's audit of the repaired
  predicates (`Main/AUDIT_REQUEST_X.md`).

### K15-C066 — C's `CROSSVALIDATION.md`: two notes (`IMPORTED` with corrections)

C's document is the clearest integration artifact either side has produced: it
tabulates the two pipelines' bases, sign machinery and Fourier maps, and runs both
directions on degree-33 data. Two corrections from Main:

1. **"Direction 1 rejected at `T_LO = 12`" is now moot.** `shell_check` has used
   `T_LO = 4·PI_LO` since `K15-C049`; their copy was stale. Main's own runs
   (`K15-C023`, `K15-C056`) `ACCEPT` both K33 variants at the current default, with
   no need to override the threshold.
2. **"Agreement to ten significant digits" is not what an exact pipeline should
   show.** For the direction-2 shell certificate they report their `Δ` as
   `0.780338357535` against `shell_check`'s `0.780338357611` — a difference of
   `7.6e−11`. Exact arithmetic should agree on the *ratio* `R = p(0)/q(0)` to the
   last digit; the `Δ` values can differ only through the `π` enclosure used to
   multiply. So either (i) `R` agrees exactly and the `Δ` difference is the two
   `π` intervals, or (ii) `R` differs, which would be a real defect. **They should
   print `R` as an exact rational and the `π` interval separately**, and X should
   check which of (i)/(ii) holds. Main cannot settle it without their shell
   certificate file, which is not on the fetched branch.
- **What stands regardless.** Direction 2 exercises a certificate produced by the
  monomial pipeline and confirms it under the Laguerre checker; that is the
  strongest coupling the project has between the two bases.

### K15-C067 — C044's quantifier, made precise (`PROVED`; the objection X is asked to audit)

`K15-C044` states the criterion for a *finite* graph. For an infinite packing two
things must be said.

1. **Necessity is local.** For every finite `U ⊆ Λ`, summing `A(v) ≥ b(v)` over `U`
   gives `Σ_U b ≤ Σ_{edges leaving U} φ ≤ Φ|δ⁺_R(U)|`. No compactness is needed. ✓
2. **Sufficiency needs compactness, and the degree bound supplies it.** Hoffman's
   theorem is finite. On an infinite graph one applies it to an exhaustion
   `U_1 ⊂ U_2 ⊂ …` and takes a cluster point of the resulting flows in the product
   `∏_e [−Φ, Φ]`, which is compact by Tychonoff **provided the product is over a
   set of edges** — it always is — and the limit is a flow because each vertex has
   finitely many incident edges, i.e. **bounded degree**. That is exactly what
   `K15-C054` gives at `R ≤ 2.09` (degree ≤ 12). So sufficiency holds for the
   packings we care about, *and the bounded-degree hypothesis is not decoration*: on
   an unbounded-degree graph the limit argument fails because a vertex could
   accumulate infinitely many edges.
3. **Novelty check (Main's reading, for X).** "A bounded-range antisymmetric
   transfer is negligible" is a discrete divergence/Stokes statement with an
   explicit boundary count; it is **not a new idea** — Hales' `A` is built from
   transfers and his four-way cancellation (Lemma 7.10) is the antisymmetry
   bookkeeping. What is new here is only the *packaging*: it makes negligibility a
   two-line estimate with a packing-independent constant and isolates the remaining
   obligation (an analytic averaged cell bound). Claiming more than that would be
   overreach.

### K15-C068 — THIRD-round predicate defect: touching isolating intervals (`REFUTED`, repaired; complete rule adopted)

- **Witness (review 0223).** `q(u) = (u − 7/5)² − 2·10⁻⁴⁰` — value `−2·10⁻⁴⁰` at
  `u = 7/5` — was accepted by `nonneg_on_half_line`, and `_ray(−q, 0)` and
  `le_on_interval(−q, 0, 0, 3)` likewise. SymPy's two isolating intervals are
  `(…, 7/5)` and `(7/5, …)`: they **share the rational endpoint** `7/5`, so the
  gap between them is empty and the negative dip (width `9·10⁻²¹`) was never
  sampled.
- **Correctness argument for the new rule (stated before promotion).** A
  polynomial has constant sign on every component of `[lo,hi] ∖ {roots}` and is
  zero at the roots, so one point per component decides the sign. The components
  are met by `lo`, `hi`, and the midpoints of the **gaps between consecutive
  isolating intervals** — but only when those gaps are non-empty. The routine
  returns `None` (inconclusive) as soon as two intervals touch or overlap, and the
  decision then falls to `function_range`, whose algorithm is the exact
  characterisation "extrema at endpoints and critical points". Formally:
  `p ≤ 0` on `I` ⟺ `sup_{I} p ≤ 0`, and `function_range` returns that sup exactly.
  Half-lines are handled by the same routine (SymPy supports unbounded intervals);
  alternatively a Cauchy-bound reduction would do.
- **Why the certificate path is unaffected.** On the sign regions of a
  certificate the polynomials have no real root, the isolating list is empty, the
  gap argument is conclusive, and no call to `function_range` occurs. So the
  certificate checks remain independent of SymPy's range code, and the genuinely
  independent oracle remains Computation's `exactcert`.
- **Regressions kept permanently** (`checker_adversarial.py`, now **29** cases):
  the three new witnesses, the sign-flipped controls `(u−7/5)² + 2·10⁻⁴⁰ ≥ 0`
  (must PASS) and `(u−1/5)² − 2·10⁻⁴⁰ ≤ 0 on [0,1]` (must FAIL).
- **Re-verified.** All six earlier witnesses still reject; all valid/touching
  cases still accept; K33b still `ACCEPT` at `0.779966216777`; fuzz clean.
- **Status.** `REFUTED` (the gap-only algorithm) → repaired with a complete rule.
  Three repairs in three rounds; the checker's *general* soundness remains
  suspended for X.

### K15-C069 — E's question `(Q)` is false, by E's own fixture plus `X-C003` (`PROVED` refutation)

**E's `(Q)`.** "Does a saturated packing contain a cell with `vol Ω < √32`?" E notes
that `(Q) = no` would give the density bound immediately. **The answer is yes**, and
the witness is the project's own:

1. the 13-cluster (centre + 12 icosahedral neighbours at distance exactly 2) is a
   legal packing fragment;
2. it extends to a *saturated* packing (`X-C003(iii)`, Zorn);
3. in that packing the centre's cell is the regular dodecahedron of volume
   `5.550291… < √32 = 5.656854…`.

So `(Q)` is answered **yes**, and `(Q)` cannot be a target: it is strictly stronger
than Kepler and false. This also disposes of any plan of the form "show every cell
is at least `√32`" — that is refuted by the dodecahedral configuration, which is
exactly Hales–McLaughlin's point. What can be true is the **averaged** statement
`Σ_{v∈K} vol Ω(v) ≥ √32|K|` over clusters, i.e. E's `(H_R)`/`(T')` and
`Main/NEXT_PACKAGE.md` — not the pointwise one.

- **Status.** `PROVED` (two-line argument from accepted results). Reviewer X.
- **Consequence for the next block.** Do not pursue `(Q)`; pursue `(H_R)` with the
  cluster-average form and the explicit `Φ` of `K15-C044`.

### K15-C070 — the periodic bridge compared with Cohn–Elkies' Appendix A (`AUDITED`)

`Main/BRIDGE_AUDIT.md` reads CE's Appendix A from the retained PDF (Annals 157,
pp. 708–709) and compares it with `K15-C002b`: CE start from a **uniformly dense
extremal** packing (existence via Groemer) and assert that "only a negligible
fraction of the spheres can intersect the sides"; `K15-C002b` starts from **any**
packing and pays two explicit losses (`O(S/R)` tile geometry, `O(1/S)` boundary
slabs) with `O(R²S)` boundary centres counted via disjoint unit balls. Neither
follows from the other by rearranging constants.

Also recorded there: the project's `limsup`-at-a-fixed-centre density equals CE's
uniform upper density for 2-separated packings (boundary term `O(R²)/R³ → 0`), so
CE numbers may be quoted; Hales' route needs no bridge at all; and the open items
(uniformity bookkeeping, the `δ = 0` case, the Zorn saturation step) are listed
with what would close each.

### K15-C071 — proof complexity of the transfer route (`PROVED` assessment)

What a transfer certificate would cost, in the three senses that matter for this
project's "simpler proof" objective.

1. **Logical strength.** Existence of `φ` from the cut condition is *non-effective*:
   the infinite case uses Tychonoff compactness (`K15-C067`), so the argument does
   not exhibit `φ`. For a **periodic** packing it is effective: the quotient graph
   is finite and the cut condition is a finite LP (`C-TRANSFER-001`), decidable in
   polynomial time by max-flow. So the non-constructive step is confined to the
   aperiodic case, and no number in the proof depends on it.
2. **Verification cost.** Checking the cut condition for a *given finite* `U` is a
   sum over vertices plus an edge count — `O(|U|·k_R)`. Checking it for all `U` is
   a min-cut computation on the finite quotient (periodic case), i.e. polynomial.
   The expensive part is not the flow but the cell volumes: computing `vol Ω(v)`
   exactly for a `d`-facet cell costs a half-space intersection, and no exact
   arithmetic version is available at the scale Hales needs (`10⁵` configurations).
   **This is where a transfer-based proof would be more expensive than Hales': he
   never needs exact volumes, only interval bounds on a finite list of scores.**
3. **Comparison with the source.** Hales' `A` is a transfer whose negligibility he
   proves by the `Q`-system and the four-way cancellation; the transfer packaging
   replaces that with `K15-C035` (two lines) at the price of making the *pointwise*
   inequality explicit, which `K15-C036` shows cannot be verified by computation.
   So the packaging trades "hard bookkeeping, computable geometry" (Hales) for
   "easy bookkeeping, uncomputable geometry". That trade is favourable only if an
   analytic averaged cell bound exists; if it does not, Hales' route is the
   cheaper one and the transfer route is a dead end. This is the honest cost model
   and it should temper any claim that `K15-C035` "simplifies the proof".

*Status.* `PROVED` (an assessment from the established lemmas, no new theorem).
Reviewer X.

### K15-C072 — decision: the next target, from worker evidence (`DECISION`, D17 recorded)

**Evidence on the table (this block's reads).**
- **C** (`b51129e`): exact explicit-Gram SOS certificates reach
  `Δ ≤ 1.99064200` and *plateau at ≈ 2* (three further seeds: `1.99889`,
  `1.99578`, `1.99725`). Higher-degree exact certificates saturate at
  `0.77996622`. Nothing in the C family is near a competitive bound, and the
  search is no longer productive.
- **E** (`846f221`): the Laves-phase witness is blocked on primary crystallographic
  data; the dense-completion search neither refuted `(T')` nor beat the sparse
  baseline ("density is not what makes `(T')` hard, saturation is"); `(Q)` was
  proposed as a shortcut.
- **X** (`9dc2ab2`): level 3; `O2` (a soft proof of CE non-sharpness in 3D) named
  as its most promising open question.

**Decision.** `K15-C069` kills `(Q)` (the dodecahedral cell is a saturated cell
below `√32`). So the geometric target is E's **`(H_R)`/`(T')` in cluster-average
form with the explicit `Φ`** of `K15-C044` — i.e. `Main/NEXT_PACKAGE.md` — and not
any pointwise cell statement. The higher-point alternative is **not** chosen this
cycle: C's three-point specification remains unimplemented and its own two-point
work plateaus three orders of magnitude away, so there is no evidence a 3-point
implementation would land anywhere useful within the project's remaining budget.
`X`'s `O2` is recorded as the most interesting *analytic* question but is not a
density bound.

*Status.* `DECISION` (D17). Reviewer X.

### K15-C073 — regression coverage completed for the third repair (`TESTED_FINITE`)

Six further cases were added after the `C068` repair, covering the classes the
earlier suites missed, and all pass (suite now **35 cases**):

| Class | Case | Expected |
| --- | --- | --- |
| roots exactly at both domain endpoints | `(u−1)(u−3)` ≤ 0 on `[1,3]` | PASS (negative between) |
| root exactly at the domain start | `u(u−2)` ≤ 0 on `[0,2]` | PASS |
| odd multiplicity | `(u−2)³ ≥ 0` on `[0,∞)` | FAIL |
| even multiplicity everywhere | `(u−2)⁴ ≥ 0` | PASS |
| even multiplicity but positive elsewhere | `(u−2)⁴ ≤ 0` on `[0,3]` | FAIL |
| clustered roots (separation `10⁻¹⁵`) with a `10⁻³⁰` dip | product of squares minus `10⁻³⁰` | FAIL |

Plus the earlier near-double witnesses (`7/5 ± 2·10⁻⁴⁰`). The `transfer_check`
fixture was re-run with the corrected constant `3ΦR(R+1)⁵` at `R = 2.51`
(bound `144421.90`, observed sum `0.75`): the bound still holds, as it must since
the corrected constant is larger.

### K15-C074 — cross-run and a third structured fuzz family (`TESTED_FINITE`)

- **Cross-run against Computation's engine including the new classes.** The
  `--against-exactcert` mode now also submits the `C068`/`C073` classes:
  `(u−2)³ → fail`, `(u−2)⁴ → pos`, `(u−7/5)² ± 2·10⁻⁴⁰ → fail / pos`. All agree.
  One item had to be restated, and the reason is a genuine scope difference:
  **`exactcert`'s engine decides half-lines only**, so a *compact-interval* claim
  such as "(u−1)(u−3) ≤ 0 on [1,3]" is outside its scope; Main's compact claims are
  covered by `function_range` instead. The harness now says so in its output rather
  than reporting a spurious disagreement.
- **Third structured fuzz family: nearly double roots.** `(u−r)² ∓ 10⁻ᵐ` with
  `r` rational and `m ∈ [10,40]`: the "below" variant must be rejected in every
  case, the "above" variant accepted. Seeds 7, 8, 12 (150–200 polynomials each):
  zero failures. This is the family of the `C068` witness, now generated
  systematically rather than only as a fixed regression.

### K15-C075 — cost profile of the complete rule, and the one branch certificates never take (`TESTED_FINITE`)

Timings on this VM, one core:

| Input | Verdict | Time | Branch |
| --- | --- | --- | --- |
| the `C068` witness `(u−7/5)²−2·10⁻⁴⁰` | reject | 0.07 s | one refinement, then `function_range` |
| its mirror `(u−7/5)²+2·10⁻⁴⁰` | accept | < 0.01 s | gap rule, first pass |
| degree 33, seven rational roots in `[12,30]` | reject | 0.02 s | gap rule (degenerate intervals, strict) |
| degree 35 with a root pair `1.4·10⁻¹⁰` apart | not measured | **> 20 s** | refinement/`function_range` |
| `(u−7/5)² − 2·10⁻⁴⁰` times `(u+1)³`, `(u+1)⁵`, `(u+1)⁷` | reject | 0.16 / 0.18 / 0.24 s | refinement then `function_range` |

**Recorded limitation.** At high degree with clustered roots the complete rule is
*exact but slow* — both the refinement ladder (capped at `ε = 10⁻¹⁴` to bound the
cost) and `function_range` can take minutes. This is a genuine limitation of the
implementation, not of the mathematics, and it is harmless here: **no certificate
in this project enters that branch**, because on the sign regions the polynomials
have no real roots and the gap rule is already strict on the first pass. If a future
use needs fast decisions at degree ≥ 20 with clustered roots, the right fix is an
exact sign test at the critical points (algebraic-number arithmetic), not more
refinement.

The certificate path's cost is unchanged: K33b verifies in ≈ 2 s including the basis
conversion, and `run_all_checks` in ≈ 6 s.

### K15-C076 — audit of X's repaired `exact_sign` (`AGREES`; second complete implementation available)

- **What was run.** `Counterexamples/exact_sign.py` (branch
  `kepler15/counterexamples/run-01`, `9dc2ab2`) was extracted and exercised by Main
  on the two defect families and on the standard controls:
  `(t²−2)(t²−3) ≥ 0` on `[0,∞)` (the irrational-root witness) → **False** ✓;
  `(t−7/5)² − 2·10⁻⁴⁰ ≥ 0` (the near-double witness) → **False** ✓; its mirror
  `+2·10⁻⁴⁰` → **True** ✓; `(t−5)²` → **True**; `(t−5)³` → **False**;
  `t(t−1)` → **False**.
- **Cross-check against Main's predicate.** The same claims were evaluated through
  `shell_check` after the exact substitution `t = 2u`: **zero disagreements** on all
  seven. (One of my own expectations was wrong in the first pass —
  `−t(t−1) ≥ 0` on `[1,∞)` is false, since the expression is `t(1−t) ≤ 0` there —
  and X's answer was the correct one.)
- **Method.** Their repair is the right one: no root is ever converted; the
  squarefree odd part `u` is formed and its roots in the open half-line are counted
  by Sturm (`count_roots`), with the endpoint handled by exact multiplicity. That is
  a *complete* decision and independent of Main's (different formulation, different
  root treatment).
- **Consequence for the project.** There are now **two complete implementations**
  of the half-line predicate (Main's and X's) that agree on both defect families,
  plus Computation's half-line engine. Main's compact-interval decision still has no
  external cross-check beyond `function_range`; that is the remaining gap.
- **Status.** `AGREES` (finite test evidence, not a soundness proof). Reviewer X.

### K15-C077 — systematic cross-run against X's `exact_sign` (`AGREES`: 10/10)

- **Artifact.** `Computation/xsign_crossrun.py <dir>`: runs the half-line claims of
  the adversarial suite plus both defect families through Main's predicates and
  through X's independent `sign_on_half_line`, after the exact substitution
  `t = 2u`. Result: **10 claims, 10 agreements, 0 skips** — including
  `(t²−2)(t²−3)` (irrational roots), `(t−7/5)² ∓ 2·10⁻⁴⁰` (near-double), the odd
  part `(t−3)²(t−1)`, and the two `_ray` claims.
- **What it buys.** The project now has two *complete* and *independent*
  implementations of the half-line predicate that agree claim by claim, so a defect
  in either would have to be mirrored in the other to survive. That is the strongest
  evidence available before a full soundness proof.
- **Still uncovered.** Main's *compact-interval* decision (`le_on_interval`) has no
  external cross-check other than `function_range`, which Main also uses as a
  fallback — so compact claims remain less protected than half-line claims. Closing
  this needs a compact-interval mode in one of the other checkers; recorded for X.

### K15-C078 — the cut condition is trivial on fcc and hcp (`PROVED` for those two)

For **fcc** and **hcp**, every Voronoi cell is the rhombic dodecahedron or the hcp
cell respectively, each of volume exactly `√32` (classical; equivalently, both attain
density `π/√18` with congruent cells). Hence `b(v) = √32 − vol Ω(v) = 0` at every
vertex, the cut condition of `K15-C044` holds with `Φ = 0`, and `φ ≡ 0` is a valid
transfer. The transfer route therefore costs nothing on the two structures that
attain the bound.

**Correction to the first version of this entry.** The first version claimed the
same for *every* Barlow stacking and cited a numerical check; both were wrong: the
numerical stack I built was not a packing (minimum separation `1.70 < 2`, a
construction bug), and for a *mixed* Barlow stacking (e.g. `ABAC…`) the cells need
not be congruent, so pointwise `b ≤ 0` does not follow from the density alone —
only the *average* volume is `√32` there. The claim is therefore restricted to fcc
and hcp, where congruence is standard.

**What stands.** On fcc/hcp the transfer costs nothing; all the content is in defect
configurations, consistent with `K15-C036` (no finite fixture decides the pointwise
inequality) and `K15-C051` (no locally dense periodic blob found), and with
`K15-C069` (cells below `√32` do exist in saturated packings).

*Status.* `PROVED` (fcc, hcp; standard cell geometry). Reviewer X.

### K15-C079 — the target in E's notation, and the boundary constant (`PROVED` correspondence)

- **E's obligations**: `(T')` `S(C) ≥ D(C)` per defective component (icosahedral
  case: `S(C) ≥ 0.1065632`), and `(T'')` `diam(C) ≤ D_0`.
- **Correspondence**: `(T')` is the per-component form of the averaged inequality
  `Σ_U vol Ω ≥ √32|U| − O(Φ|U|^{2/3})` of `Main/NEXT_PACKAGE.md`; by `K15-C067` the
  two are equivalent up to `Φ` and the boundary term. E's own figure "outer cells
  must average `5.66573451791`" is exactly `√32 + (√32 − V_dod)/12` (`K15-C042`), so
  the two sessions' constants agree.
- **Boundary constant (CORRECTED, review 0308)**: the estimate holds for **ball
  cuts** `U = B(x,r) ∩ Λ`, where `|δ⁺(U)| ≤ k_R·#(Λ ∩ (B(x,r+R)∖B(x,r))) ≤
  k_R((r+R)³ − r³) ≈ 3k_RRr²` and `|U| ≍ (4π/3)r³`, giving the slack
  `Φ·3k_RR·(3|U|/4π)^{2/3}`. For an **arbitrary** `U` the correct trivial bound is
  `|δ⁺(U)| ≤ k_R|U|`, i.e. slack `Φk_R|U|`, which is *not* `o(|U|)`: merely
  containing a ball does not control an arbitrary cut's boundary (a comb-shaped `U`
  has boundary comparable to its size). So the `|U|^{2/3}` form is a **hypothesis
  about ball-like cuts**, not a consequence. The first version of this entry applied
  it to arbitrary blobs; that was wrong.
- **Status.** `PROVED` (a translation between two statements, no new mathematics).
  Reviewer X.

### K15-C080 — the transfer requirement is strictly weaker than E's `(T')` (`PROVED`)

- **E's `(T')`** asks, for every defective component `C`, `Σ_{v∈C}(vol Ω(v) − √32) ≥ 0`,
  i.e. `Σ_C b ≤ 0` with `b = √32 − vol Ω`: each component must pay for itself.
- **The transfer route** (`K15-C044`) asks only `Σ_C b ≤ Φ|δ⁺_R(C)|` for the same
  `C`, because the component may be funded from outside across its boundary.
- Since `Φ|δ⁺_R(C)| ≥ 0`, the transfer condition is implied by `(T')`, and it is
  *strictly* weaker exactly when `δ⁺_R(C) ≠ ∅`.
- **Precision (corrected in the same entry).** The first version claimed every bounded
  component has out-edges in a saturated packing. That is **not proved**: a closed
  finite component would need every centre within `R` of it to be inside it, and while
  saturation forbids leaving room for a *new* sphere, it does not by itself forbid a
  cluster whose nearest outside neighbour is farther than `R = 2.09`. What is true is
  the conditional statement: **if** the component has out-edges, the cut form is
  weaker; **if** it is closed, the cut condition *is* `(T')`. So a proof of the cut
  form must handle both, and a closed component is exactly the case where E's `(T')`
  cannot be avoided.
- **Consequence for the next block.** The target should be stated in the *cut* form,
  not as `(T')`: it is the weaker obligation, it is exactly what a transfer
  certificate needs, and its price `Φ` is explicit in the final rate
  (`C₁ = 3ΦR(R+1)⁵`). E's `(T')` remains a sufficient condition and a sanity check
  (it must hold on fcc/hcp, where `φ = 0` works and `δ⁺` is non-empty).
- **Caveat.** `Φ` cannot be allowed to grow: the rate in Lemma 3.3 is `O(C₁/r)` with
  `C₁ ∝ Φ`, so a proof of the cut form is only useful with a stated bound on `Φ`
  (the icosahedral vertex alone forces `Φ ≥ 0.00888`, `K15-C036`).

*Status.* `PROVED` (immediate from the definitions). Reviewer X. Recorded in
`Main/NEXT_PACKAGE.md`.

### K15-C081 — WITHDRAWN: the cluster-level `Φ` floor was an invalid inference

> **Status: `WITHDRAWN` (review 0308).** The original text is retained below as
> rejected evidence.
>
> **The error.** `C081` derived `Σ_C b ≤ 13(√32 − V_dod)` — an **upper** bound on the
> cluster's signed deficit — and then used it as though it were a **lower** bound, to
> conclude `Φ|δ⁺(C)| ≥ Σ_C b` and hence a floor on `Φ`. That inference is invalid:
> if the thirteen cells are on average *larger* than `√32` (so `Σ_C b < 0`) the cut
> condition is satisfied with `Φ = 0`. Nothing in the ledger bounds `Σ_C b` from
> below, and the claim that all thirteen cells attain `V_dod` was never proved — and
> is false in general.
>
> **Superseded by `C081r`** (the singleton bound), which is valid and weaker.

*Rejected text (kept):* "By Hales–McLaughlin every cell has volume `≥ V_dod`, so the
cluster's total deficit is at most `13(√32 − V_dod) = 1.3853218727…`; by `K15-C044`
… `Φ ≥ 13(√32 − V_dod)/|δ⁺_R(C)|`" — with the outer–outer observation giving
`Φ ≥ 0.0104949`. **This conclusion does not follow and is withdrawn.**

### K15-C081r — the valid necessary condition: the singleton cut (`PROVED`)

For a packing containing the 13-cluster, let `v₀` be the centre. Its cell satisfies
`Ω(v₀) ⊆` the dodecahedron determined by the twelve neighbours, hence
`vol Ω(v₀) ≤ V_dod` (monotonicity: more bisectors only shrink; `K15-C036`), and
therefore

```
b(v₀) = √32 − vol Ω(v₀)  ≥  √32 − V_dod  =  0.1065632…,
```

a **lower** bound on the signed deficit at that vertex — which is what the cut
condition needs. With `U = {v₀}` and `R ≤ 2.09`, at most `k_R ≤ 12` edges leave:

```
Φ  ≥  (√32 − V_dod)/12  =  0.0088803….
```

(Equality `vol Ω(v₀) = V_dod` is *not* needed — only the inclusion, exactly as the
review notes. Hales–McLaughlin is not used.)

*Status.* `PROVED`. Reviewer X. This is the only `Φ` floor the project has.

### K15-C082 — E's Barlow spectrum re-run, and the `Φ` floor published (`AGREES`)

- **Run.** `Experimental/scripts/barlow_shell_check.py` (branch
  `kepler15/experimental/run-01`, `846f221`) executed by Main. For fcc (`ABC`) it
  reports the distance spectrum `2.000 (12), 2.828 (6), 3.464 (24), 4.000 (4)` and
  "centres in `[2,2.09]`: 12" — i.e. **no distance in `(2, 2.09)`**, which agrees with
  Main's structural proof (`K15-C033`) and with their `K15-E013`. (Main's own
  attempt at the same numerical check had a construction bug; E's does not.)
- **Published.** The `Φ` floor of `K15-C081` (`0.00962` at `R = 2.09`) is now in
  `Main/NEXT_PACKAGE.md` as the floor any transfer candidate must clear.
- **Status.** `AGREES` (finite numerical evidence consistent with a proof).
  Reviewer X.

### K15-C083 — the bridge's relative loss is `12/S`, not `1/S` (`PROVED`, quantitative refinement)

`K15-C002b` deletes the two-unit slabs at the tile boundary, so the kept region is
the inner cube of side `S − 4` and the relative kept volume is

```
(1 − 4/S)³  ≥  1 − 12/S        for  S ≥ 4  (verified for 4 ≤ S < 500).
```

So the loss in the bridge is `O(1/S)` **with constant 12**, not 1 — the `O(1/S)`
notation is correct but the constant matters for any quantitative use:

| `S` | kept fraction | `12/S` |
| --- | --- | --- |
| 6 | 0.037 | 2.00 |
| 10 | 0.216 | 1.20 |
| 20 | 0.512 | 0.60 |
| 50 | 0.779 | 0.24 |
| 100 | 0.885 | 0.12 |

**Empirical check of the construction itself (fcc, `S = 4, 6`, `R = 20, 40`).** Tiling
`fcc` by cubes of side `S`, taking the tile with the most centres and periodising
after deleting the slabs reproduces exactly the loss predicted: at `S = 6, R = 40`
the periodic packing has `δ = 0.0194` against fcc's `0.7405`, i.e. the scheme is
**vacuous below `S ≈ 12`** but correct as `S → ∞` with `R/S → ∞`.

**Consequence.** The bridge is a *qualitative* reduction: it shows periodic packings
are dense in density, but with a loss of `12/S` it says nothing quantitative at any
computable scale. That is fine for its use (an upper bound proved for all periodic
packings transfers to all packings), and it is worth stating so that nobody tries to
make the bridge carry numerical weight.

### K15-C084 — the remaining lemma compared with Hales' accounting (`AUDITED`)

`Main/REMAINING_LEMMA.md` states the cut condition exactly, and compares it with
Hales' accounting: his structure is (i) a score on Delaunay stars from an explicit
volume transfer, (ii) an **exact rearrangement**
`Σ_{v∈B}(vol Ω(v)+A(v)) = Σ_{D⊆B} σ(D)` (his four-way cancellation), (iii) a
pointwise `σ(D) ≥ 0` verified over a **finite** list of tame combinatorial types.
The cut condition has the same shape — a transfer plus an identity — but its
quantifier (every finite `U` in every packing) is not finitised, so it is *harder to
verify mechanically* and *weaker as a statement*. No published source proves a cut
form; the pointwise results (Rogers `5.372754`, Muder `5.41848`, Hales–McLaughlin
`5.550291`) cannot reach `√32` because `V_dod` is pointwise optimal.

Also recorded there: the most promising unexplored route — an **explicit local**
`φ(v,w) = ψ(|v−w|)(b(v)−b(w))`, for which the cut condition reduces to a per-edge
inequality and *is* finitely verifiable. No one has attempted it.

### K15-C085 — the naive explicit-transfer ansatz fails (`PROVED` negative on a model)

`Main/REMAINING_LEMMA.md` §5 flags "an explicit local `φ`" as the most promising
route. Main tested the obvious ansatz:

```
φ(v,w) = ψ(v−w)·(b(v) − b(w)),      ψ ≥ 0,  supp ψ ⊆ [−R,R],
s := Σ_w ψ(v−w)   (constant on a lattice-shaped neighbourhood).
```

Then `Σ_w φ(v,w) = s·b(v) − (ψ*b)(v)`, so the requirement `Σ_w φ(v,w) ≥ b(v)` is

```
(s − 1)·b(v)  ≥  (ψ*b)(v)          for every v.        (★)
```

**`(★)` fails on the simplest defect model.** Take a line of seven sites with
`b = (0,0,0, +1, −0.5, 0, 0)` (a unit deficit funded by a neighbouring surplus) and
any of `ψ = (0.25,0.25)`, `(0.5,0.5)`, `(0.4,0.1)`. The left side is *negative* at
the surplus site while `(ψ*b)` is positive there, so `(★)` fails by `O(b)` at exactly
the vertices that are supposed to fund the deficit. The ansatz transfers the full
difference, which overshoots: the deficit site receives `s·1 − ψ(2)(−0.5)` but the
surplus site *pays* `s·0.5 + ψ(2)·1`, more than its surplus allows.

So the naive form does not work, and the "local formula ⇒ finitely verifiable"
hope is not realised by it. What is needed is a genuine flow — i.e. the min-cut
solution of `K15-C044` — and there is no reason to expect it to have a closed local
form. This is recorded so the next block does not spend its budget on the ansatz.

*Status.* `PROVED` (a counterexample to a proposed route on an explicit model).
Reviewer X.

### K15-C086 — worker sources integrated at review 0308 (`IMPORTED`, pending X's own review)

| Source | Revision | What it says | Main's disposition |
| --- | --- | --- | --- |
| X `Counterexamples/REVIEW_0138.md` | `6535e76` | audited Main's checker at **`9461aae`** on a 23-test battery: 0 mismatches; also records X's own four wrong expectations and the witness-anchored fix | **superseded**: the supervisor's local reproduction found **three false accepts at that same revision** (`K15-C058`'s witnesses). A 23-test battery that passes on an unsound revision is the third instance this project has of "tests that could not fail" — the lesson stands and is recorded |
| X `REGISTRY.md` additions | `6535e76` | three certified CE bounds in X's own family: `0.818086808`, `0.794809296`, **`0.780718153`** (current best for X) | imported as *independent implementations*, not as bounds to quote; all are worse than CDS22's `0.779747`. `X-C014` awaits Astra's local check. X's own `P(0)/Q(0) ≥ 1.024466` filter from Li is a useful guard and is recorded |
| C `sos_pside_many.py`, `sos_both_sides.py`, `sos_qside_polish.py` | `9d9ff68` | explicit-Gram states: p-side `1.33982382`, Fourier-side `1.37125723`, both-sides `2.00171738`; the LP-optimal value without a rational Gram is `0.77996622` | imported as **controls**; three orders from competitive; `D17` says do not spend a block improving them |
| E `CANDIDATES.md` | `9a46efc` | `E1` criterion proved, block rule `R2'` corrected, `(T'-R2')` open and quantitatively obstructed; `E2` (3-point hybrid) specified but **blocked on a three-point evaluator**; `E3` (pure Delaunay) obstructed at the `(2,2,2,2,l,l)` simplex | imported; `E1` is the project's target (`D17`), `E2` is not chosen, `E3` recorded as obstructed |

**Consistency check on the three CE families.** They are independent *implementations*
in different parametrisations: C's Laguerre certificates, X's `P(s)e^{−s}` family, and
Main's `u = π|x|²` checker. Their bare numbers are not comparable across normalisations —
X's bound is `(4/(3√π))P(0)/Q(0)`, Main's is `(4π/3)R` — and only the converted
occupied-volume values may be compared. All three are above `0.779747`.

### K15-C087 — the cut condition is not a weaker target: large ball cuts *are* the theorem (`PROVED`)

For a ball cut `U = B(x,r) ∩ Λ` with `r` large, the cells of the vertices in `U` tile
`B(x,r)` up to a boundary layer, so

```
Σ_{v∈U} b(v) = √32|U| − Σ_{v∈U} vol Ω(v)
             = √32 c·(4π/3)r³ − (4π/3)r³ + O(r²)
             = (4π/3)r³ (√32 c − 1) + O(r²),
```

while the right side of the cut condition is `Φ|δ⁺(U)| ≤ Φ·3k_R R r² = O(r²)`. So the
cut condition for large balls reads

```
(√32 c − 1)·r³ ≤ O(r²),      i.e.   c ≤ 1/√32 + O(1/r),
```

which is exactly `δ ≤ π/√18` in the limit. **The cut condition for large ball cuts is
the Kepler bound itself**, not a weakening of it.

**What this settles.** `K15-C080`'s "strictly weaker than `(T')`" applies only to
*small* components: the cut condition must also hold for large balls, and there it
is the theorem. So the transfer route is not a way to weaken the target; it is a way
to *reorganise* the proof (negligibility for free, `K15-C035`) whose price is that
the geometric content reappears at full strength. This is the precise form of
`K15-C071`'s "trade", and it should stop any future block from pursuing the cut
condition as though it were easier than Kepler.

**Precision added (block `K15-REVIEW-0308-M-CONTINUE`, task 4).** The `O(r²)` boundary
term is not free: `Σ_{v∈U} vol Ω(v) = vol B(x,r) + O(r²)` needs `Ω(v) ⊆ B(v,2)`, which
holds for **saturated** packings and only for those (saturation says every `x` has a
centre within 2, so `|x−v| > 2` forces `x ∉ Ω(v)`). So `K15-C087` is stated for
saturated `Λ`; the passage from an arbitrary packing to a saturated one is the Zorn step
recorded in `Main/BRIDGE_AUDIT.md` §3 item 3. Second precision: `|U| = c(Λ)·(4π/3)r³ +
O(r²)`, where `c` is the **centre** density, so the identity reads
`Σ_U b = (4π/3)r³(√32c − 1) + O(r²)` with `c` the centre density and `√32 c − 1 = 0`
at `c = 1/√32`; both substitutions are stated nowhere above and are needed for the
displayed chain to be checkable. Neither gap affects the conclusion.

**Direction (stated once, here, because the converse has been assumed twice).** `C087`
proves *cut condition ⟹ density bound*. It does **not** prove the converse, and the
converse is not available: the density bound carries no local cut information. Hence
the cut condition is **at least as strong as** Kepler, and `K15-C080`'s "strictly weaker"
must be read against the *open* `(T')`, not against Kepler. See
`Main/ACCEPTED.md` §"One-way implications".

> **Correction (`K15-REVIEW-0438-M`): the direction is not a circularity, and an earlier note
> here said so wrongly.** The rejected phrasing was: *"nothing implies it from the density
> bound, so the transfer route is a reorganisation whose price is the full geometric content"*
> — used as though the implication *disqualified* the route. That inference is invalid. A
> **sufficient** condition implies its target by definition; that is what "sufficient" means,
> and it says nothing against it. Circularity would require the criterion to *assume* the
> target. What the one-way arrow does establish is narrower and still worth having: the cut
> form is not a weakening of Kepler, so it cannot be advertised as an easier target. Whether
> the cut form is *simpler to verify* is an open cost question (`C071`, `C100`), not a
> consequence of the implication. (The genuinely circular step found this block was `C094`'s
> Lemma 1, repaired in `C104` — a different defect.)

*Status.* `PROVED` (asymptotic identity from the tiling, plus `K15-C043`'s chain in
the other direction). Reviewer X.

### K15-C088 — Hales' accounting read from the text (`AUDITED`; the structural difference is compactness)

Quoting `Literature/Papers/Hales2005-unabridged.pdf`, Ch. 7: **Definition 7.12**
defines the score `σ(D) = −4δ_oct(vol Ω(D)+A₀(D)) + 16π/3` on *decomposition stars*;
**Lemma 7.13** shows `min_DS(vol Ω + A₀) = √32` ⟺ `max_DS σ = 8 pt`; **Theorem 7.14**
turns `max_DS σ = 8 pt` into existence of a negligible fcc-compatible `A` for every
saturated packing; **Definition 7.15** and §7.4 decompose `σ` over standard clusters,
and Ch. 10 bounds it region by region.

**The structural difference, precisely.** `DS` is a *compact finite-dimensional* space
of local configurations. Hales' Lemma 7.13 converts a pointwise statement about all
packings into an optimisation over that compact space, which is then a finite
computation (interval arithmetic + LPs).

**Scope of the comparison (softened, block `K15-REVIEW-0308-M-CONTINUE`).** The cut
condition **has no `DS`**: it quantifies over subsets of a packing, so no compact
reduction is available *for the cut formulation as stated*. That is what is shown, and
it is why the transfer route as stated cannot be finitised the way Hales' can. It is
**not** a claim that no reformulation of the geometric route admits a compact
reduction; nothing here rules out an analogous device for the cut form. The earlier
wording ("no compact reduction exists") is withdrawn as an overstatement. The bounded
claim that remains: none is available for the present formulation, and no candidate has
been exhibited in this project.

### K15-C089 — the next geometric package: `sup_Λ t*(Λ) ≤ Φ₀` (`PROPOSED` package)

`Main/PACKAGE_CUT.md` restates the geometric target as a *quantitative* inequality:

```
t*(Λ) = max over finite U of  Σ_U b / |δ⁺_R(U)|   ≤   Φ₀(R)      for every saturated Λ, R ≤ 2.09,
```

with `t*` the minimal transfer bound (LP duality, `K15-C044`). Reasons this is the
right form: (i) it is exactly what the rate `O(Φ/r)` needs; (ii) a single periodic
packing with `t* > Φ₀` refutes a claimed `Φ₀`, so candidates are testable
(`C-TRANSFER-001` computes `t*`); (iii) it has a proved floor `Φ₀ ≥ 0.0088803`
(`K15-C081r`) — **witness-specific**: that floor holds for packings containing the
icosahedral singleton, not for every packing with `b > 0`. The per-packing necessary
bound is `t* ≥ max_v b(v)/deg(v)`; the two must not be confused (review 0308
continuation).
- **Correction (in the same entry).** The first version said "existence cannot be
  refuted by a packing". **False.** If a packing has a **bounded** closed component `C`
  (finite, no edges leaving at range `R`) with `Σ_C b > 0`, then `t*(Λ) = ∞` and **no
  transfer exists** — such a packing refutes the transfer route (not Kepler).
  **"Bounded" is essential and was missing** (block `K15-REVIEW-0308-M-CONTINUE`):
  *infinite* closed components do exist — the crack packing of `K15-C095` is a saturated
  2-separated packing whose `2.09`-graph has two closed infinite components — and they
  are harmless, because every finite `U ⊆ C` has `δ⁺(U) ≠ ∅` via its edges to `C∖U`.
  So the obligation is: **no bounded closed component with `Σ_C b > 0`**. By `K15-C080` a
  closed component reduces the cut condition exactly to E's `(T')`. So the package has
  a prior obligation: **show that no saturated packing has a positive-deficit closed
  component**, or restrict the target to packings without one. This is E's
  `E-COMPONENT-001`, and it is the first thing to settle — a single example would
  close the route.

The difficulty is located precisely in the trade-off between small cuts (small
denominator, `Σ_U b` controlled only by `√32|U|`) and large cuts (density controls
`Σ_U b`, but the boundary grows like `|U|^{2/3}`). Three steps are specified:
compute `t*` on four non-trivial periodic packings; prove the ball-cut case; then show
the maximum is attained on ball-like cuts.

### K15-C090 — a fit position on the icosahedral cluster at radius 3.4026 (`PROVED`, exact geometry)

For the 13-cluster, over each of the 30 edges of the outer icosahedron there are two
positions at distance exactly `2` from the two edge endpoints; the **outward** one lies
at radius

```
r_fit = √(4 − (2.1029244485/2)²) + √(4 − (2.1029244485/2)²) = 2·1.7013016167… = 3.4026032334…
```

from the centre, and its distance to every cluster point is `≥ 2` (minimum exactly `2`,
attained at the two edge endpoints). So it is a legal **fit position**: a sphere may be
placed there without overlap.

**What it does and does not show.** It shows the cluster is not "closed by geometry":
there is room outside it. It does **not** settle the closed-component question
(`K15-C080`, `E-COMPONENT-001`): saturation guarantees a centre within distance `2` of
that fit position, but such a centre may be as far as `4` from the cluster, hence not
within `2.09`. Since a transfer edge needs distance `≤ 2.09`, the fit position does not
by itself produce an out-edge. The closed-component case therefore remains open, as
recorded in `K15-C089`'s step 0.

*Status.* `PROVED` (exact icosahedral geometry; computed and checked numerically to
`1e−9`). Reviewer X.

### K15-C091 — Barlow cell volumes: six mixed stackings tested, all cells `√32` (`PROVED` — uniformity settled in `K15-C094`; the finite evidence is retained below)

**Construction (validated).** Layer `k` at height `k·h`, `h = √(8/3)`, on the
triangular lattice `⟨(2,0),(1,√3)⟩`, shifted by `s_k·(a₁+a₂)/3`; a stacking is the
sequence `(s_k)` with consecutive differences `±1 mod 3` (a hollow move) and the wrap
step also `±1 mod 3`. Cells computed on a `3×3×3`-replicated periodic set with the
half-space/ConvexHull machinery; **minimum separation over all pairs checked** (`2.0000`
in every legal case).

| stacking | period | min sep | cell volumes |
| --- | --- | --- | --- |
| `ABC` (fcc) | 3 | 2.0000 | `5.656854 ×3` |
| `ABA` (hcp) | 2 | 2.0000 | `5.656854 ×2` |
| `ABAC` | 4 | 2.0000 | `5.656854 ×4` |
| `ABCB` | 4 | 2.0000 | `5.656854 ×4` |
| `ABABAC` | 6 | 2.0000 | `5.656854 ×6` |
| `ABCACB` | 6 | 2.0000 | `5.656854 ×6` |
| `ABACABA` | 7 | 1.6330 | **illegal**: wrap step `0 ≢ ±1 mod 3` |

`√32 = 5.656854249…`, so **every cell in every legal stacking tested has volume
`√32` to six decimals** — the uniformity claim survives six distinct local environments
(including `ABAC`, where the four sites have different neighbourhoods).

**What is proved, and what is not.**
- *Average*: `√32` in every Barlow stacking, since the density is `π/√18` (each layer
  carries `1/(2√3)` points per unit area and the layer spacing is `h`).
- *Uniformity*: **not proved**. The six cases are evidence; the cell volume is a
  function of the local offset pattern and no argument is known to Main showing the
  function is constant. (This is the corrected status of `K15-C078`: fcc/hcp are proved;
  general Barlow is evidenced, not proved.)
- *Degree facts vs volume facts* (`K15-C054` vs `C078`): the degree bound `≤ 12` at
  `R = 2.09` holds for **every** 2-separated set (`C013`), Barlow or not; the vanishing
  of `b` holds only where the volumes are `√32`, i.e. fcc/hcp by proof and Barlow by
  evidence.

**Construction bug found and recorded.** The first version added the height to the
*y*-coordinate (`np.array([0.0, k*h])` added to a 2-D base) instead of using it as `z`;
it produced "packings" with minimum separation `1.70` and meaningless cell volumes. The
same mistake had invalidated Main's earlier numerical checks of `C033`/`C078`. Fixed
before any number above was recorded.

### K15-C092 — closed components: one obstruction proved, no counterexample found (`TESTED_FINITE` ledger)

`Main/CLOSED_COMPONENT.md` records four attempted constructions with their exact
failed conditions and one proved necessary obstruction:

**Covering lemma.** An isolated vertex (no centre within `2.09`) in a *saturated*
packing has at least **five** other centres in the annulus `(2.09, 4]`. *Proof:*
saturation forces, for each direction `u`, a centre within `2` of `v + 2u`, hence a
cap of directions of area `2π(1 − ρ/4)`; covering `S²` with caps of area `< 0.4775·2π`
needs five of them. ∎ (Weak but real.)

**Attempts and exact failures** (no construction succeeded):
- *A1*: icosahedral directions pushed to `2.09` (legal, mutual `2.1976`): cell volume
  `6.333804 > √32`, i.e. **negative** deficit — the natural candidate has the wrong
  sign by 12%;
- *A2*: general singleton needs `vol ∈ (V_dod, √32)` with all faces `≥ 1.045` — a
  1.9% window; Hales–McLaughlin does not close it, and a *stability* version would;
- *A3*: isolated dimer — the far-face argument fails (a face at distance 1); no
  conclusion;
- *A4*: clusters `≥ 3` — every cell has a near face inside the cluster; open.

So the closed-component question stays open, with one proved constraint and a documented
set of failures. Reviewer X.

### K15-C093 — finite-to-infinite cut/flow theorem with a free boundary (`PROVED`)

`Main/CUT_FLOW_THEOREM.md` proves, in the convention actually used (`div φ ≥ b`,
signed `b`, antisymmetric `φ`, uniform capacity):

- **Theorem 1 (finite, free boundary).** With demands on `F ⊆ V` only, a transfer
  exists **iff** `Σ_U b ≤ cap(U)` for every `U ⊆ F`. (The free boundary is what makes
  the reduction to Gale–Hoffman go through; the induced-subgraph formulation would be
  *stronger* than the hypothesis and hence unusable.)
- **Theorem 2 (infinite).** For locally finite `G`, an exhaustion `{F_n}`, the cut
  condition for all finite `U`, and `sup Φ < ∞`: a transfer exists. Proof by Theorem 1
  on `F_n ∪ N(F_n)` plus Tychonoff on `∏_e [−Φ₀,Φ₀]` and the finite intersection
  property. **Tychonoff needs no degree bound; local finiteness is needed only for the
  divergence to be a finite sum** — a refinement of `K15-C067`'s statement, where
  compactness and bounded degree were conflated.
- **Separation of concerns**: Theorems 1–2 are pure graph theory (existence from cuts);
  the geometry enters only in verifying the cuts — fcc/hcp `b ≡ 0` (`C078`), the
  witness-specific floor `0.0088803` (`C081r`), the large-ball cut being the density
  bound (`C087`), and the closed component needing `Σ_C b ≤ 0` (`C080`).
- ~~**Worked examples**: the dumbbell `b = (1,−1/3,−1/3,−1/3)` has `t* = 1/3` with the
  exact transfer `φ(a,l_i) = 1/3` and the tight singleton cut as dual witness; the
  variant `b(a) = 4` is infeasible at `Φ = 1` with the violating cut `{a}`; and a
  two-hop path `(+1,0,0,−1)` has `t* = 1` with a unique flow and three tight prefix cuts.~~
  **SUPERSEDED (review 0523): this bullet is retained only as retraction history.** The
  `b(a) = 4` sentence is wrong — that vector is infeasible at **every** capacity because
  `Σ_F b = 1 > 0 = cap(F)` — and the `t*` formula it presupposes divides by an empty boundary.
  The corrected examples, including the genuine threshold case `b = (4,−4/3,−4/3,−4/3)`, are in
  the repaired block immediately below. Do not cite this bullet.

> **REPAIRED (`D18`; review `K15-REVIEW-0353-M-EVIDENCE`).** Four defects were found by
> the reviewer and are all confirmed against the text. `Main/CUT_FLOW_THEOREM.md` is
> rewritten; the first version's statements are retained there in §6 as rejected evidence.
>
> 1. **Cut orientation reversed.** The first version said the infinite arcs to the sink make
>    `X ⊇ N(U)∖F` optimal for `X = S∖F`. Wrong: an outside vertex on the **source** side
>    puts its infinite arc `w→t` across the cut, so finite cuts have `X = ∅` — outside
>    vertices are forced onto the **sink** side, and there is no minimisation. The
>    conclusion `Σ_U b ≤ cap(U)` is unchanged. Also now written out: **two directed arcs
>    `v→w` and `w→v`, each with the full capacity `Φ_{vw}`**, and the transfer is their net
>    `ψ(v,w) = f(v→w) − f(w→v)`, so `|ψ| ≤ Φ_{vw}` and conversely every transfer arises
>    this way.
> 2. **Threshold formula divided by a zero boundary.** The first version's
>    `t* = max_{U⊆F} Σ_U b/|δ⁺(U)|` is undefined when `δ⁺(U) = ∅`, and that case is an
>    obstruction at *every* capacity. Corrected:
>    `t* = +∞` if some `U ⊆ F` has `δ⁺(U) = ∅` and `Σ_U b > 0`, else
>    `max(0, sup_{U: δ⁺(U)≠∅} Σ_U b/|δ⁺(U)|)`. The `max(0,·)` is needed because the minimal
>    capacity must be non-negative. Consequently the first version's example
>    `b = (4,−1,−1,−1)` is **infeasible at every `Φ`** (`Σ_F b = 1 > 0 = cap(F)`), not
>    infeasible at a threshold `4/3`; the genuine threshold example is `b = (4,−4/3,−4/3,−4/3)`,
>    where `t* = 4/3`.
> 3. **Compactness assumed a uniform bound.** Tychonoff gives `∏_e [−Φ_e, Φ_e]` compact from
>    the compactness of each factor, so `sup_e Φ_e < ∞` is **not** a hypothesis of Theorem 2
>    and is removed. What *is* used: `Φ_e ≥ 0` (non-degenerate intervals), `Φ_e < ∞` per
>    edge (compact factor), local finiteness (only for `div` to be a finite sum, hence
>    continuous), and `F_n` finite with `⋃F_n = V`.
> 4. **The density implication is one-directional.** `K15-C087` gives `(C) ⟹ Kepler`;
>    there is no converse and no equivalence between `(C)` and the density statement.
>
> **Second, independent proof of (⟸)** added, by duality + coarea: the Farkas alternative
> for `{Aφ ≥ b, |φ_e| ≤ Φ_e}` (box multipliers kept) is `Σ_F y_v b(v) > Σ_e Φ_e|y_v − y_w|`
> for some `y ≥ 0`; the coarea identities `Σ_F y_v b = ∫_0^∞ Σ_{U_t} b` and
> `Σ_e Φ_e|y_v−y_w| = ∫_0^∞ cap(U_t)` with `U_t = {v : y_v > t}` then produce a cut
> violating `(C)`. This proof is the one that survives signed capacities, where the box
> multipliers matter.
>
> *Status.* `PROVED` (both proofs written out). Reviewer X — the reviewer asked for an
> independent audit of the repaired statement; the request is in `Main/AUDIT_REQUEST_X.md`
> item 5.

### K15-C094 — every Voronoi cell of a Barlow packing has volume `√32` (`PROVED`)

`Main/BARLOW_CELLS.md`. Closes the uniformity left open in `K15-C091`.

**Statement.** For every Barlow packing `P(s)` (the layered class of `K15-C091`: layers
`Λ + s_k T` at height `kH`, `Λ` triangular with nearest neighbour 2, `T = (a₁+a₂)/3`,
`H = √(8/3)`, consecutive offsets differing by `±1 mod 3`), **every** Voronoi cell has
volume `4√2 = √32 = 5.656854249492…`, not merely the average.

**Proof, in four steps** (all elementary; no interval arithmetic, no vertex lists).

1. *Distances.* Exactly twelve centres at distance 2 (six in-layer, three in each
   adjacent layer, the latter because `T` is the centroid of the equilateral triangle
   `{0,a₁,a₂}`, so `|T| = 2/√3` and `|T|² + H² = 4`), and every other centre at distance
   `≥ 2√2` (the next in-plane distance in an adjacent layer is `4/√3`, giving
   `√(16/3 + 8/3)`).
2. *Reduction to 12 contacts.* Every point of space is within `√2` of a centre: a
   layer plane lies within `H/2` of any point, the triangular lattice has covering
   radius `2/√3`, and `(2/√3)² + (H/2)² = 2`. So `Ω(v) ⊆ B(v,√2)`; and any non-contact
   `c` satisfies `|c−v| ≥ 2√2`, so its half-space contains `B(v,√2) ⊇ Ω(v)` and is
   redundant. **`Ω(v)` is the cell cut out by the twelve contacts alone.**
3. *Two shapes.* The six in-layer contacts form a regular hexagon (no parameter). The
   three upper contacts lie in the coset `δ₊T + Λ` and the three lower in `−δ₋T + Λ`,
   with `δ₊, δ₋ ∈ {±1}` the layer steps; the two non-zero cosets of `Λ` in `(1/3)Λ` give
   the azimuth classes `𝒜 = {30°,150°,270°}` and `ℬ = 𝒜+60°`. So the contact set is
   determined by whether `δ₊ = δ₋` (*different* classes: the **fcc** configuration) or
   `δ₊ = −δ₋` (*same* class: the **hcp** configuration); a `60°` rotation and the
   reflection `z ↦ −z` reduce the four sign combinations to these two.
4. *Both volumes are `√32`.* The average cell volume is `2√3·H = 4√2` in every Barlow
   packing (one centre per area `2√3` per layer). `ABC…` is fcc-configured in every layer,
   so its average is the fcc cell's volume; `ABA…` is hcp-configured in every layer, so
   its average is the hcp cell's volume. Hence both are `4√2`, and every cell is one of
   the two. ∎

**The two cells are not congruent.** fcc gives the rhombic dodecahedron (12 rhombi,
face-normal dot products in `{−1,−½,0,½}`); hcp gives the trapezorhombic dodecahedron
(12 quadrilaterals, dot products including `−5/6` and `−1/3`). Both have 14 vertices and
circumradius `√2`. So the result is a volume statement about a two-element family, not a
shape statement about one polyhedron — which is why the earlier attempts to prove
"every Barlow cell is a rhombic dodecahedron" were looking for something false.

**Corollary (tightness at the extremal points, new).** `b ≡ 0` on every Barlow packing,
so at such a packing `Σ_U b = 0 = Φ|δ⁺_R(U)|` with `Φ = 0`, `φ ≡ 0`: **every cut is
tight** and `t*(Λ) = 0`. Consequently the cut condition cannot be proved by exhibiting a
positive margin anywhere on the extremal family; the equality case of the `Φ = 0`
condition is the two-shape family of step 3, i.e. a finite local classification. This is
the transfer-route analogue of Hales' remark that pure subdivision fails at a tight point
(§17.2), and it is a **cost**, not a gain: it removes the slack argument.

**Numerics (`Computation/barlow_cells.py`).** For the nine named stackings, per layer:
`#`centres at distance 2 `= 12`; next distance `2√2`; volume from the 12 contacts `=` volume
from all centres within radius 5 `= 5.656854249492` (agreement to `1e−12`); circumradius
`√2`; 12 quadrilateral faces, 14 vertices; and the largest non-contact half-space value
`max_vertex n·x − 1 = 0` to `1e−16` — the far half-spaces are **tangent**, exactly the
equality case of step 2. The fcc and hcp dot-product fingerprints differ, confirming
step 3's "two shapes, not one". `ABACABA` and `ABABCBCA` are rejected as illegal
(wrap step `0 ≢ ±1`), as in `K15-C091`. Random sweep (`--sweep 6`, periods 3–10):
**48 stackings, 346 layer analyses, 0 violations**, exit 0; sampled covering radius
`≤ 1.379` against the proved `√2`.

**What is not claimed.** (i) Not the converse: `b ≡ 0` does *not* force a packing to be
Barlow — that needs the classification of all densest packings, which is open. (ii) Not
the classical characterisation "12 contacts ⟹ layered"; the theorem is stated for the
layered class and nothing here depends on that characterisation. (iii) No bound in
`RESULTS.md` moves; `K15-C087` is untouched.

*Status.* `PROVED` (steps 1–4 above; the numerical checks test step 2's tangency and
step 3's dichotomy, both of which could have been wrong). Reviewer X.

### K15-C095 — the crack packing: infinite closed components, and a second equality case (`PROVED`)

`Main/GAP_FIXTURE.md`, `Computation/gap_fixture.py`. Two fcc half-spaces, `ABC` stacking,
cut at `z = 0`, the upper half translated up by `d` and sideways by `T`:

```
lower:  ( Λ + (k mod 3)T ) × {kH},          k ≤ 0
upper:  ( Λ + ((1+k) mod 3)T ) × {d + kH},  k ≥ 0
```

**(1) It is a packing, and it is saturated, for `H ≤ d ≤ 2H`.** Across the crack the
in-plane nearest distance is `2/√3`, so 2-separation needs `d² + 4/3 ≥ 4`, i.e.
`d ≥ H = 1.632993`; saturation needs the mid-crack point within 2, i.e.
`(d/2)² + 4/3 ≤ 4`, i.e. `d ≤ 2H = 3.265986`. Both bounds are attained at `d = H` and
`d = 2H` respectively. Numerically: min separation `2.000000` and sampled covering radius
`≤ 1.97` for `d ∈ {1.633,…,3.2}`.

**(2) For `d > 2.09` the `2.09`-graph has two closed infinite components.** Minimum cross-
crack distance: `2.1385` at `d = 1.8`, `2.6633` at `d = 2.4`, `3.4020` at `d = 3.2`. So
`K15-C089`'s obstruction must be stated for **bounded** closed components only; infinite
ones exist and are harmless (every finite `U ⊆ C` has out-edges into `C∖U`).

**(3) The crack costs volume in the helpful direction.** At `d = 2.4` every crack-face cell
has `vol Ω = 6.985349063`, i.e. `b = −1.328495`; every bulk cell has `vol Ω = √32`
exactly. So a void produces `b < 0` and satisfies the cut condition for free: **only
compression can force `Φ > 0`.** Crack energy `2 × 1.328495/(2√3) = 0.767` per unit area.

**(4) It is an equality case of Kepler's bound and is not Barlow.** The crack is a single
surface, so it costs `O(r²)` centres in a ball of radius `r`: the density is exactly
`1/√32` in centre units, i.e. `δ = π/√18`. But the layer spacing across the crack is `d`,
not `H`, so the packing is not a Barlow stacking (nor fcc, nor hcp). Hence **the equality
case of Kepler's bound is strictly larger than the Barlow packings** — any planar fault is
an equality case, and they are unclassified.

**Consequences.** (i) `densest ⇏ b ≡ 0`, so `K15-C094`'s corollary is one-directional.
(ii) `b ≤ 0` everywhere is **false** (`K15-C069`'s dodecahedral cell, `vol Ω = 5.5503 <
√32` in a saturated packing), so the cut condition at `Φ = 0` is false and `Φ > 0` is
necessary — an independent second route to `K15-C081r`'s conclusion, this time without
using the value of `V_dod` at all. (iii) A sharp `d = 3` certificate cannot rest on
uniqueness of the extremiser: complementary slackness would need `f` to vanish on the
shell radii of every equality case.

*Status.* `PROVED` (items 1–2 by the two displayed inequalities plus the `gap_fixture.py`
check; 3 by the half-space computation; 4 by the `O(r²)` count). Reviewer X.

### K15-C096 — the singleton closed component reduces to a stability problem for Hales–McLaughlin (`PROPOSED`, with a sharp threshold and a finite evidence base)

**The reduction.** A bounded closed component `{v₀}` of the `2.09`-graph with `Σ_C b > 0`
is exactly a centre `v₀` such that (i) every other centre is at distance `≥ 2.09` from
`v₀`, and (ii) `vol Ω(v₀) < √32`. So define

```
V(ρ)  =  min { vol Ω(0) : C is 2-separated, every c ∈ C has |c| ≥ ρ } .
```

Then **`V(2.09) ≥ √32` excludes the singleton closed component outright**, and
`V(2) = V_dod = 5.550291028515510` is exactly Hales–McLaughlin.

**The sharp threshold.** The icosahedral twelve at radius `ρ` give the dodecahedron of
inradius `ρ/2`, of volume `V_dod(ρ/2)³`. Setting this equal to `√32`:

```
ρ*  =  2·(√32 / V_dod)^{1/3}  =  2.012718662083…,
```

so `√32` is crossed only `0.64%` of the way from `2` to `2.09`. Verified numerically
(`Computation/rho_probe.py`): at `ρ = 2.09` the icosahedral configuration has cell volume
`6.333804106 = V_dod(1.045)³`, i.e. **`+11.97%` above `√32`**, and at `ρ = 2.0127` it is
`5.656697`, below `√32` by `0.003%` as the formula requires. So the window is wide: the
cheapest known isolated-vertex configuration clears `√32` by 12%.

**The conjecture.**

```
V(ρ)  =  V_dod·(ρ/2)³    for  2 ≤ ρ ≤ ρ_c ,      (S)
```

i.e. the extremal configuration at radius `ρ` is the icosahedral one pushed out to `ρ`.
`(S)` is exactly the *stability version of Hales–McLaughlin* that `Main/CLOSED_COMPONENT.md`
A2 asked for, in explicit and testable form, and it is stronger than needed: `(S)` at
`ρ = 2.09` gives `6.3338 ≥ √32`.

**Evidence for `(S)`.** (i) `V(ρ) ≥ V_dod` for every `ρ ≥ 2` is Hales–McLaughlin itself;
`(S)` is the quantitative improvement bought by pushing the neighbours out.
(ii) Among 12-point configurations at radius `ρ` the icosahedron minimises the cell
(Fejes Tóth's 12-point spherical-code optimality), so `(S)` holds with exactly 12
admissible points. (iii) The open case is *more* than 12 points, which is possible here
because the points may sit at different radii `≥ ρ`. A probe over the 20 icosahedral
"holes" (the dodecahedral directions) for a 13th point at every radius in `[ρ, 4]`, at
`ρ = 2.0127, 2.09, 2.2`, finds **no admissible extra point that cuts the cell at all**
(the nearest hole direction needs radius `≳ 3.2` to be 2-separated from the twelve, and
its bisector at `1.6` then lies outside the cell's circumradius `1.478`). So a 13th point
cannot help in the natural position; a full search over 13+ points is not done.

**What would settle it.** A proof of `(S)` on `[2, 2.09]` — or of any bound
`V(ρ) ≥ V_dod·(1 + c(ρ−2))` with `c ≥ (√32/V_dod − 1)/0.09 = 0.2133` — closes the
singleton case. This is the sharpest formulation the project has of D17's step 0 for
`|C| = 1`; `|C| ≥ 2` is untouched (a member of `C` has neighbours *inside* `C` at
distance 2, so `(S)` does not apply to it).

*Status.* `PROPOSED` (`(S)` is open); the reduction, the threshold `ρ*` and the numbers
are `PROVED`/`TESTED_FINITE` respectively. Reviewer X.

### K15-C097 — integration at review 0353: the decoupling lemma, E's trend correction, X-C017 (`IMPORTED`)

Three worker revisions read this block, by hashes. None is merged; integration is by
reference.

**1. C, `4bcbd3a0ee94bd29d2f1fdcc5e69aaf1f0ed0a62` — `C-DECOUPLE-001` (`PROVED`,
elementary).** For the icosahedral fixture the periodic graph is a **disjoint union of
identical copies**: registered centres lie within `2` of their copy's origin, so distinct
copies are at distance `≥ 16 − 4 = 12`, while `R ≤ 3 ≪ 12`. A finite `U` therefore splits
into pieces in separate copies with **no edges between them**, so `Σ_U b/|δ⁺(U)|` is a
weighted average of the pieces' ratios and its maximum is attained **inside one copy**.
Consequently `t* = 0.008880268414417` is the exact threshold for the **infinite** packing,
not a finite-patch proxy. **Caveat C records and Main endorses:** a *dense* packing has
period comparable to `R`, so decoupling is a property of sparse fixtures only.

*Main's audit.* The argument is correct as stated for the fixture. Two limits Main adds:
(i) the fixture is **unsaturated** (X's flag), so this is a statement about an unsaturated
periodic packing; (ii) it therefore does **not** by itself give a floor for saturated
packings. That floor is already independently valid: `K15-C081r` uses the icosahedral
13-cluster extended to a saturated packing by Zorn (`X-C003(iii)`), adding centres can only
*shrink* `Ω(v₀)` (hence only increase `b(v₀)`), and `deg(v₀) = 12` exactly by `K15-C054`,
so `Φ ≥ b(v₀)/12 ≥ 0.1065632/12 = 0.00888027…`. The two routes give the same number, and
the saturated one is the one the ledger relies on.

**2a. Main's audit of E's threshold.** E's target is stated as "required `5.763417`"; Main
identifies it exactly as

```
5.763417470…  =  2√32 − V_dod  =  √32 + (√32 − V_dod),
```

i.e. **the volume the partner of a minimum (dodecahedral) cell must have for a two-cell
cluster to average `√32`.** The quantity is coherent and the number is right. Two things
follow for how the margin should be read: E's best `6.263608` is `0.500` above the threshold
in *volume*, but the **pair mean** of `(V_dod, 6.263608)` is `5.906950`, which is `0.2500`
above `√32` — a `4.42%` shortfall in the normalised quantity. So the gap is not small and it
*grew* when the search was widened to 30 centres; that is a cleaner statement of E's revised
verdict than "the margin halved at each step", and it is the form in which the number should
be quoted.

**2. E, `82689ba1999a1ca240e480f9bc90121101f9e801` — the trend claim corrected.** The
30-centre search gives `6.494845` and `6.968035`, **worse** than the 18-centre `6.263608`,
so the sequence is not monotone and the earlier framing ("every improvement found a smaller
cell", "margin halving at each step") overstates the trend; the likely cause is method
limitation (twice the degrees of freedom for the same iteration budget). Revised verdict:
**(P′) has survived every legal test, best `6.263608` against a required `5.763417`; the
evidence is one-sided, so not support.** E explicitly records what not to do: report
`6.264` as evidence *for* (P′), or the trajectory as evidence *against*. **Main records
(P′) as `PROPOSED`, unproved; numerical upper volumes cannot validate it** (an upper bound
on a computed volume is not a lower bound on the true infimum, and no interval arithmetic
was used).

**3. X, `118ecd1601bb500f7d305ce299dcb00f73a66772` — `K15-X-C017` (`VERIFIED` by X's own
exact arithmetic; Main has not re-run it).** Both sides explicit: rational symmetric `6×6`
`G, A, B`, `m = 5`, `S = 8`, `eps_G = 1e−2`, `eps_AB = 1e−6`; all PSD verified exactly by
rational LDL; `Q(A,B)` equals the Fourier image of `P` exactly; `P(0)/Q(0) = 1.039899410072`
giving `Δ ≤ 0.782267220134` for every packing of unit balls; `Q ≥ 0` cross-checked by exact
Sturm. X also corrects its own earlier wrong assumption (it had treated `G` as necessarily
singular "because `P(4)=0`"; false, since `P = −(s−4)H` gives `P(4)=0` for any `H`).

*Assessment.* `0.782267220134` is **worse** than the project's best (`0.779966216777`), so
it is not an improvement and does not change `RESULTS.md`. Its value is **methodological
and it is significant**: *no sign predicate, no root isolation and no Sturm is needed
anywhere — every sign condition is a rational PSD test.* The ladder is C `SOSQSIDE-005`
`1.413704545` → X-C015 `0.813631102` → X-C016 `0.783097911` → X-C017 `0.782267220`; X-C014
`0.780718153` has the p-side only and C's K33 `0.779966500` has neither side. Given that
`Computation/shell_check.py` has been unsound three times (`C049`, `C058`, `C068`) **this
is the trust profile the project should prefer**: a both-sides certificate whose every sign
condition is a rational LDL test is outside the failure mode entirely. Recorded as the
first candidate for the acceptance pipeline of `K15-C099`.

*Status.* `IMPORTED`; per-claim statuses as above. Reviewer X.

### K15-C098 — the shell allowance's `η ≥ 0` precondition, and what it is not (`PROVED`, narrow)

X flags that `Computation/shell_check.py` did not check `η ≥ 0`. Confirmed: `check(a, rho,
eta, …)` accepted any rational `eta` and the reported bound is
`R = (p(0) + count·η)/q(0)` with the displayed verdict `f ≤ η` on the shell `[2, ρ]`.

**What was wrong.** The count-price bound (`K15-C003r`) is
`δ ≤ (4π/3)(f(0) + n·M)/f̂(0)` where `f ≤ M` on a set `A` of contact number `≤ n` and `f ≤ 0`
off `A` outside radius 2. With `M = η`, the formula is the intended one **only for `η ≥ 0`**;
for `η < 0` the *correct* statement replaces `η` by `max(η,0) = 0` (the plain two-point
bound), because `f ≤ 0` off `A` already supplies the stronger hypothesis. So an `η < 0` call
returned a *smaller* number than the argument licenses for the parameter the user believes
they passed. That is a precondition defect, not a sign-predicate defect.

**Fix.** `check` now rejects `η < 0` explicitly, with the message that the plain bound is
`η = 0`; and `checker_adversarial.py` gains the case. **This is a precondition validation
and it is not a soundness argument.** Generic checker soundness remains **SUSPENDED**: the
three historical repairs were all in the sign-decision path, and no written argument that
the accepted set is contained in `{p ≤ 0 on the region}` exists yet (`PN-4`).

*Status.* `PROVED` (the `η < 0` claim, two lines). Reviewer X.

### K15-C099 — acceptance-pipeline proposal: prefer certificates with no sign predicate (`PROPOSED`)

Motivated by `K15-C098` and X-C017. The project's weakest link is not the mathematics but
`shell_check.py`, unsound three times, each caught by outside reproduction. X-C017's
certificate needs **no** sign decision: `Q ≥ 0`, `A ⪰ 0`, `B ⪰ 0` are three rational LDL
tests, and `Q(A,B) = Fourier image of P` is an exact polynomial identity. Such a certificate
has no `≤ 0 on an interval` step at all, so it is not exposed to the failure mode.

**Proposal.** Make "both sides, all sign conditions rational PSD" the *acceptance* criterion
for certificates, and treat any certificate that needs `shell_check` as `PENDING` until the
soundness argument of `PN-4` exists. This costs nothing numerically (`K15-C017` is `0.7823`
against `0.7800` for the best p-side-only object, and the current best `0.779966216777` is
not an improvement over published values anyway) and it removes the project's
most-repeated failure. **Reverse if** `PN-4`'s argument is written and X accepts it.

*Status.* `PROPOSED` (a process decision, not a theorem). Needs the person's sign-off
because it changes what "accepted" means.

### K15-C100 — proof-complexity scorecard after the repairs (`PROVED` assessment; no new bound)

`Main/COMPLEXITY.md` continues `K15-C071` with the numbers now settled. Two figures carry
the analysis:

- the **lattice-restricted** three-point bound is `0.741506` against the truth
  `0.740480489693` — a gap of `+0.00103`, i.e. **`0.14%`**;
- the **general** three-point bound is `0.770271`, a gap of `+0.02979`, i.e. `4.0%`.

So the lattice restriction is worth `0.029` of density — more than this project has moved by
any means — and every non-computational object within `0.14%` of the truth is
three-point-and-lattice. Since the plain two-point LP is *proved* not sharp in `d = 3`
(R. Li, Adv. Math. 460 (2024), Thm 6.1), no refinement of the two-point certificate
reaches the truth, and `K15-C095` now exhibits the mechanism concretely: **any planar fault
is an equality case**, so a sharp certificate would need `f` to vanish on the shell radii of
a continuum of extremal packings.

**Consequences recorded for the project's stated goal ("a simpler proof").**
1. The analytic route cannot be a shortcut below level 3; the next class (three-point) does
   not close the gap either at `0.770271`.
2. The transfer route is **at least as strong as** the theorem (`K15-C087`) and has no slack
   at the extremal family (`K15-C094`); it is a reorganisation, not a simplification.
3. The one well-posed improvement target with this project's tools is a **pointwise** cell
   inequality strictly better than Hales–McLaughlin's `0.754697399337`, and the concrete
   instance is `K15-C096`'s `(S)`: `V(ρ) = V_dod(ρ/2)³`, whose consequence
   `V(2.09) ≥ √32` would settle the singleton closed-component case with a `12%` margin.

*Status.* `PROVED` as an assessment (each arrow and each number is a claim id above). The
quoted `0.741506` / `0.770271` are CDS22 material used only for order of magnitude, and
`RESULTS.md` does not move. Reviewer X.

### K15-C101 — `(S)` splits at the Tammes-13 threshold; case (A) is settled at `12%` margin (`PROVED` reduction, cited theorems)

Follow-up to `K15-C096`, `Main/COMPLEXITY.md` addendum. **`2.09` is the Tammes-13
threshold rounded down**, which is why the constant appears everywhere and why the
singleton closed-component question is not marginal.

**The split.** `13` points on the sphere of radius `ρ` with mutual distance `≥ 2` exist iff
`2 arcsin(1/ρ) ≥ θ₁₃ = 57.1367°`, i.e. `ρ ≥ 2.091145548…`. At `ρ = 2.09` the required
separation is `57.1709° > 57.1367°`, so **at radius exactly `2.09` every admissible
configuration has at most 12 points**. Then:

- **(A) all points at radius exactly `ρ`.** Scaling `x ↦ 2x/ρ` carries the cell cut by
  `{⟨u_i,x⟩ ≤ ρ/2}` to the `ρ = 2` cell for the same directions, so case (A) is the `ρ = 2`
  problem; Fejes Tóth's 12-point optimality (icosahedron) plus monotonicity of the cell in
  the spread of the directions gives the icosahedral minimum `V_dod(ρ/2)³ = 6.333804106` at
  `ρ = 2.09` — **`1.1197·√32`**. So case (A) satisfies `V(2.09) ≥ √32` with `12%` margin,
  modulo the two cited theorems (Tammes-12, spread monotonicity), neither proved here.
- **(B) some point at radius `> ρ`.** Then more than 12 points become available (the shell
  `[2.09, 2.956]` can hold at most `16` two-separated points, by a volume count), and `(S)`
  is exactly **"mixed radii do not help"**: a point at radius `r > ρ` has the looser
  half-space `⟨u,x⟩ ≤ r/2`, so extra points must gain by number what they lose by distance.
  This is the open case, and it is what `Computation/rho_probe.py` probes negatively: from
  the icosahedral twelve at `ρ`, an extra point in one of the 20 hole directions is
  admissible only for `r ≳ 3.2`, where its bisector at `1.6` lies outside the cell's
  circumradius `1.478`. Verified for every `r ∈ [ρ,4]` at `ρ = 2.0127, 2.09, 2.2`. **Two or
  more extra points, or a point off the hole directions, is not searched.**
- **Why not a ball estimate.** `vol B(0,ρ/2) = 4.78011` at `ρ = 2.09` and beats `V_dod` only
  for `ρ > 2.1967`; so on `[2, 2.1967]` the binding information is Hales–McLaughlin together
  with a stability term. `(S)` cannot be replaced by an inball bound.

**Effect on `PN-1`.** The request narrows from "decide `V(2.09) ≥ √32`" to "decide case (B)"
— a bounded finite-dimensional optimisation with an explicit admissible set (≤ 16 points in
a shell of known volume), an explicit target `√32`, and a negative probe on its natural
configurations.

*Status.* The split and case (A) are `PROVED` reductions (the two cited theorems are
`ACCEPTED WITH SCOPE` elsewhere in `ACCEPTED.md`); case (B) is open. Reviewer X.

### K15-C102 — the nearest admissible 13th centre is at `3.206871`, so extra centres never cut the icosahedral cell (`PROVED` finite check; scope in §3)

Follow-up to `K15-C101`, case (B). `Computation/nearest_13th.py`. **Redundancy is a
per-half-space property**: if a centre `p`'s half-space `{⟨p,x⟩ ≤ |p|²/2}` contains the
cell, it changes nothing, and adding further centres cannot make it change. So the whole of
case (B) at a *given* base configuration is decided by the single-point question.

**The closed form.** For a direction `u` and a base centre `x` with `|x| = ρ`, the condition
`|r u − x| ≥ 2` is `r² − 2r⟨u,x⟩ + (ρ² − 4) ≥ 0`, i.e. `r ∉ (r₋, r₊)` with

```
r₊(u,x) = ⟨u,x⟩ + √(⟨u,x⟩² − (ρ² − 4)),      defined iff ⟨u,x⟩² ≥ ρ² − 4 = 0.3681 > 0;
smallest admissible r along u  =  max( ρ , max_i r₊(u, x_i) ).
```

**The result.** Over `2×10⁶` sampled directions plus Nelder–Mead refinement from all 24
icosahedral/dodecahedral directions, the minimum is

```
min over admissible p of |p|  =  3.206870905…        at direction (0.934172, 0.356822, 0)
```

— an **edge-midpoint** direction of the icosahedron (not a face centre). Against
`2·R_cell = 2·(ρ/2)·√2 = 2.955706345`:

> **`3.206871 > 2.955706`**, so every admissible extra centre has its bisector outside the
> cell's circumradius, its half-space contains the cell, and **the icosahedral cell is
> determined by its twelve contacts alone — at any centre count.**

Hence `V(2.09) ≤ V_dod(1.045)³ = 6.333804106…`, **with equality** at the icosahedral
configuration, and the extreme configuration attaining it is the pushed-out dodecahedron.

**Two consequences.**

1. **`CLOSED_COMPONENT.md`'s A1 is upgraded.** A1 recorded `6.333804` as the volume of the
   intersection of the **12** half-spaces; that was an upper bound on the cell volume only if
   the further centres were redundant, which was assumed, not shown. It is now shown. A1's
   number is the **true** cell volume of the pushed-out icosahedral vertex, so its deficit
   `b = √32 − 6.333804 = −0.6775` is the true deficit — the natural singleton candidate fails
   by `12%`, not merely by an estimate.
2. **Case (B) of `K15-C101` is settled at the icosahedral base** and only there. It is *not*
   settled for a non-icosahedral base: if the twelve nearest are more clustered, the cell is
   larger and an extra centre has more room to cut it. So `V(2.09) = 6.333804` remains a
   *conjecture*; what is now proved is that the natural extremal configuration is exactly as
   advertised and is not undercut by any number of extra centres.

**What would finish `(S)`.** A proof that a *non-icosahedral* base plus extra centres cannot
beat `6.333804` — i.e. the spread-monotonicity lemma of `K15-C101` in the form "moving the
twelve apart decreases the cell volume faster than adding centres decreases it". `PN-1` is
unchanged in substance and now has one fewer degree of freedom.

**How far the reduction reaches, exactly.** Let `C` be admissible and let `C'` be the same
*directions* placed at radius exactly `ρ`. Since `r ≥ ρ` gives
`{⟨u,x⟩ ≤ ρ/2} ⊆ {⟨u,x⟩ ≤ r/2}`, the cell of `C'` is contained in that of `C`, so
`vol Ω(C) ≥ vol Ω(C')`. Then:

- **`|C| ≤ 12`**: `vol Ω(C') ≥ V_dod(ρ/2)³`, because `C'` is a set of at most 12 points on
  the sphere of radius `ρ` and [12-point optimality + spread monotonicity] says the
  icosahedral directions minimise the cell. So `V(2.09) ≥ 6.333804` for every configuration
  with at most 12 centres, and combined with `C102` (equality attained, extras redundant)
  this gives `V(2.09) = 6.333804` **on the `|C| ≤ 12` branch**.
- **`|C| ≥ 13`**: the reduction **stops**. `C'` is then `≥ 13` points on the sphere and is *not*
  2-separated (moving a centre inward breaks the 2-separation), so neither Tammes-13 nor
  `C102` applies, and more constraints can in principle shrink the cell below
  `V_dod(ρ/2)³`. For a *packing* `C`, at most 12 of its centres can be at radius `≤ 2.0911`
  (Tammes-13), so the `≥ 13` case forces at least one centre at radius `> 2.0911` — and such
  a centre is redundant at the icosahedral base but not provably redundant at a clustered one.

So the open content of `(S)` is now exactly: **`|C| ≥ 13`, with at least one centre at radius
`> 2.0911`.** That is one integrality-and-trade-off statement, not a search over all
configurations, and it is what `PN-1` should be asked for.

*Status.* `PROVED` for the stated finite check (the minimisation is over a `2`-parameter
family with a closed form for the radius, so it is checkable to interval-arithmetic standard;
Main ran it numerically only). Reviewer X.

### K15-C103 — reconciliation of the three frozen worker inputs at review 0438 (`IMPORTED`, with two Main corrections)

Sources read by exact hash, confirmed against the remote; nothing merged.

- **C `6fbd0a1bf214a92b625cee84e8ee95ac5da4b8d9`** — `Computation/STATUS.md` rewritten for Main.
  Substantive content: `TRANSFER-DENSITY-002` (a bounded antisymmetric transfer on a
  finite-upper-density packing that is `D`-**saturated** implies `ρ ≤ 1/√32`), `CUTIMPLIES-003`
  (the finite-`U` cut condition at any *one* finite capacity forces `ρ ≤ 1/√32`, because
  `U = Λ ∩ B` is finite), `HIGHDENS-001` (every packing with covering radius `≤ R_Φ` fails
  `C044` at capacity `Φ`; `R_0 = 1.105339`), `PERIODCONV-001` (no wrap-around edges for
  `R ≤ 3`; the twelve ring cells congruent, volume `340.870809080957`, to `3.4e−13`),
  `CUTBLOB-001` (`t*` pinned to width `8.3e−23`, maximiser `{0}`). **`CUTEQUIV-001` ("cut
  condition ⟺ Kepler") is WITHDRAWN by C** — correct, and consistent with `C087`'s one-way
  statement. C also records that the converse Kepler ⟹ some finite `Φ` works is open.
- **E `498cfc3c0ce8d023fbf29b5810d06be115ac256b`** — `Experimental/REVIEW_0353.md` +
  `INTEGRATION_0353.md`. Three items Main must act on, all checked: (i) **`K15-E083`**, the
  contact-only `K ⊆ B(v,√2)` repair of Main's circular Lemma 1 — adopted and independently
  re-verified (`C104`); (ii) `K15-E078` ("97.4% irremovable") **WITHDRAWN** by E because it
  rested on failed searches, leaving only `K15-E082`, an angular exclusion for head-on cuts;
  (iii) E's payer fixture: `(θ,φ) = (111.80°, 36°)` minimises `vol Ω(w1) = 5.897967122` over the
  `C5` family, frozen fixture at `cos θ = −3/8` gives `5.898017372` (`5.0e−5` above), against
  `(P′)`'s required `5.763417470` — margin `+0.1345`. E's covering-radius certificate converges
  (`47.01, 43.22, 41.85, 40.79` at subdiv `3,4,5,6`, requirement `48.88`).
- **X `d64de362da7b6f52bd494d15364e67783a3b184b`** — `Counterexamples/REPORT_X040.md`
  self-audit (an `8^10` typo in §2, `P ≤ 0` beyond `4`, `NEXT_PACKAGE` wording). Astra has
  independently verified the original X-C017 at `< 0.782267220134` and the 37 repaired checker
  regressions; **the smaller C017 certificate and the geometric repairs still need local
  review** and are therefore `PENDING_REVIEW` here, not accepted.

**Main's two corrections to worker material.**
1. **C's `shell_check` unsoundness report is against a stale revision of Main's own branch.**
   C names `shell_check.py` at `6626714`; that commit *is* an ancestor of `kepler15/main`, but it
   predates the `C058`/`C068` repairs and still contains `_odd_part`. Main ran C's three
   witnesses against the current file: `le_on_interval([0,1,−1],0,0,1)`, `nonneg_on_half_line
   ([0,−1,1])` and `_ray([0,1,−1],0)` all return **False**, i.e. correctly rejected (`u−u² = 1/4
   > 0` at `u = 1/2`). So the defect C reports is **already repaired**, and C's advice to "not
   rely on it until the fix is audited" is right in form: generic checker soundness remains
   **SUSPENDED** (`PN-4`), but not for the reason C gives. Recorded with the exact revision so
   it is not re-litigated.
2. **Main's `BARLOW_CELLS.md` Lemma 1 was circular** (E's finding, confirmed). Repaired in
   `C104`; `K15-C094`'s acceptance is restored on the repaired proof, not on the old one.

*Status.* `IMPORTED`; per-source statuses above. Reviewer X.

### K15-C104 — independent verification of the contact-polytope bound; `C094`'s Lemma 1 repaired (`PROVED`)

**The defect (E's `K15-E083`, confirmed).** `C094`'s Lemma 1 argued: a non-contact `c` has
`|c−v| ≥ 2√2`, so `H_c ⊇ B(v,√2)`; and `Ω(v) ⊆ B(v,√2)` by (F3); "so every non-contact
half-space contains `Ω(v)`, hence is redundant". **Circular**: `Ω ⊆ H_c` is true *by
definition* for every defining half-space. Redundancy needs `K ⊆ H_c` for the **contact-only**
polytope `K`. The rejected text is preserved in `BARLOW_CELLS.md`.

**The repair.** Two steps: (1) `K ⊆ B(v,√2)`, an exact finite statement about the contact
polytope that never mentions `Ω`; (2) for a non-contact `c` and `x ∈ K`,
`|x−c| ≥ |c−v| − |x−v| ≥ 2√2 − √2 = √2 ≥ |x−v|`, so `K ⊆ H_c`; hence `Ω = K`.

**Independent verification (`Computation/contact_cell_exact.py`, exit 0).** Written against
E's *statement*, not E's code: exact arithmetic in `Q(√2,√3)` as 4-tuples over `Fraction`,
Cramer solves, exact feasible-set tests, and **rigorous interval sign decisions** (`mpmath.iv`,
increasing precision until the sign is certified; exact zeros detected structurally as the
all-zero tuple). Result for both local types:

| type | vertices | `|x|²` (mult.) | `max|x|²` | `K ⊆ B(v,√2)` | Euler |
| --- | --- | --- | --- | --- | --- |
| fcc | 14 | `3/2` (8), `2` (6) | `2` | **yes** | `14−24+12 = 2` ✓ |
| hcp | 14 | `3/2` (8), `2` (6) | `2` | **yes** | `2` ✓ |

This reproduces E's table exactly. Agrees with Main's own float enumeration (8 vertices at
`√(3/2)`, 6 at `√2`) and with E's `vol K = 4√2` cross-check against (F4)'s `2√3·H`.

**Two bugs in the verifying implementation, recorded because one of them is a false
refutation.** (i) `T` was coded `(1/3, √3/3)` instead of `(1, √3/3)`; (ii) the normals were
coded `p/4` instead of `p/2` (the bisector is `x·p = |p|²/2 = 2`, so `n = p/2`). With the
second bug the polytope is twice too large, `max|x|² = 8`, and the check prints
**`K ⊄ B(v,√2)`** — i.e. a silent scaling slip manufactures a refutation of a true statement.
The bound is exactly attained (`max = 2`), so it is not robust to scaling error; any future
re-derivation must check `|p_i|² = 4` for all twelve contacts before trusting the output, which
the script now asserts.

**Consequence for `K15-C094`.** Acceptance restored on the repaired proof. `(F3)` is no longer
used by the theorem (it survives as a true remark on the covering radius), so the repaired chain
is also shorter: (F1) → `Ω = K` → two types (Lemma 2) → `vol = 4√2`.

*Status.* `PROVED`. Independent reviewer: X (requested); the verification above is Main's own
second implementation and does not substitute for X's.

### K15-C105 — a sufficient criterion is not circular because it implies the target (`CORRECTION` of Main's own rhetoric)

Main had written, in four places, that because the cut condition **implies** `δ ≤ π/√18`
(`C087`) and nothing implies it from the density bound, "the transfer route is a
reorganisation, not a simplification" — as though the implication were a verdict on the route.
**That inference is invalid.** A sufficient condition implies its target *by definition*; that
is what "sufficient" means, and it is no argument against it. A stronger statement can perfectly
well be **simpler** to prove. Circularity requires *assuming* the target, which is a different
error — and precisely the error that `C094`'s Lemma 1 actually committed (`C104`).

What survives, and is worth keeping: the cut form is **not a weakening** of Kepler, so it must
not be advertised as an easier target. What does not survive: any suggestion that the
implication disqualifies the route. Whether the route is *cheaper* is an open cost comparison
(`C071`, `C100`), not a logical consequence.

Corrected in `ACCEPTED.md` §"One-way implications" (with a standing caution), `C087` (rejected
phrasing preserved), `COMPLEXITY.md` §3–§4. *Status.* `CORRECTION`; no mathematics changes.

### K15-C106 — the global bridge for the pair bound, and the `1.92%` gap (`PROVED`)

`Main/GEOMETRIC_LEMMA_0438.md` §1–§3.

**The local statement.** E's pair conjecture `(P′)`/`K15-E074`: for every contact pair
(`|v−w| = 2`) of a saturated 2-separated packing, `vol Ω(v) + vol Ω(w) ≥ 2√32 =
11.3137084990`. Strictly stronger than the pointwise bound, since Hales–McLaughlin gives only
`2V_dod = 11.100582057`, and E's `K15-E075` shows `2V_dod` is unattainable for a contact pair.
**Equality holds on every Barlow packing** — proved here from `K15-C094` (every Barlow cell is
`√32`). So the equality family of `(L)` **contains** the Barlow family, and `2√32` cannot be
improved. **It is not an iff** (review 0523): Barlow `⟹` equality, but equality `⟹` Barlow is
not proved and is not claimed. Earlier wording said the equality family "is exactly" the Barlow
family; that is retracted.

**The bridge (new).** E's justification for `(P′)` is "it implies the cut with `1.72%` margin";
that arithmetic is correct but it is the cut at `U =` the 13-cluster only, not a density bound.

> **Theorem B.** If `Λ` is saturated, satisfies `(P′)`, and carries weights `c_e ≥ 0` on the
> contact edges with `Σ_{e∋v} c_e = 1` for every `v` outside a set of upper density zero, then
> `δ(Λ) ≤ π/√18`.
> **Corollary B1.** If `deg(v) = 12` for every `v`, `c_e = 1/12` works, so `(P′)` alone gives
> `δ ≤ π/√18`. This covers every Barlow packing.

*Proof sketch* (full in the file): sum `vol Ω(v) = Σ_{e∋v}c_e vol Ω(v)` over a ball, discard
the crossing edges (`O(R²)` of them by 2-separation, `c_e ≤ 1`), use `(P′)` on the internal
edges, and `Σ_{v∈B}vol Ω(v) = (4π/3)R³ + O(R²)` from saturation; divide by `(4π/3)R³`.

**The quantitative point (`K15-C107`).** The bridge is monotone: any pair constant `K` gives
`δ ≤ 8π/(3K)`. Two evaluations:

| `K` | `8π/(3K)` |
| --- | --- |
| `2V_dod = 11.100582057` (ML twice) | `0.754697399337` — exactly the dodecahedral bound |
| `2√32 = 11.313708499` (`(P′)`) | `0.740480489693` — exactly `π/√18` |

So the route interpolates from the published bound to the truth with **no sharpness barrier**,
and since `√32/V_dod = 1.01919957`,

> **the entire remaining gap is a `1.92%` increase in one two-cell constant**, and any
> `K > 2V_dod` already beats `0.754697399337`.

That is the structural difference from the routes already closed in this project: pointwise
cell bounds are dead by sharpness (`V_dod` is attained), and the two-point LP by Li's
obstruction, but the pair functional has room.

*Status.* `PROVED` (bridge). `(P′)` itself is E's and **unproved**. Reviewer X.

### K15-C107 — the target restated weakly: `(L_δ)` suffices (`PROVED` reduction)

Because of the monotonicity in `C106`, the sharp constant is not needed. Let

> **(L_δ)** there is `δ > 0` with `vol Ω(v) + vol Ω(w) ≥ 2V_dod + δ` for every contact pair.

Then `(L_δ)` for *any* `δ > 0` gives `δ(Λ) ≤ 8π/(3(2V_dod+δ)) < 0.754697399337` via Theorem B,
with the improvement proportional to `δ`. `(L_δ)` is strictly weaker than `(P′)`. Recorded so
that the workers are asked for the monotone form, not only the sharp one: the sharp `2√32` is a
*bonus*, not a requirement.

*Status.* `PROVED` (reduction). Reviewer X.

### K15-C108 — `(L_δ)` is true (compactness), and what it buys (`PROVED`, non-explicit; universal lower-volume claim PENDING review)

`Main/GEOMETRIC_LEMMA_0438.md` §4.

> **Theorem D.** `σ₀ := inf{vol Ω(v) + vol Ω(w) : 2-separated configurations with a contact
> pair v,w}` satisfies `σ₀ > 2V_dod`.

*Proof.* (1) `σ₀ ≥ 2V_dod` by Hales–McLaughlin. (2) **The infimum is attained**: a cell of
volume `≤ C` contains the unit inball and is convex, so a point at distance `r` in it carries a
cone of volume `≥ πr/3`, whence `r ≤ 3C/π`; so for configurations with `Φ ≤ 2V_dod+1` both cells
are determined by the centres in a bounded region, where 2-separated configurations form a
compact set and `Φ` is continuous. (3) At a minimiser with `σ₀ = 2V_dod`, both cells have
volume exactly `V_dod`, so by the **equality case of Hales–McLaughlin** both are regular
dodecahedra of inradius 1. (4) But `v` and `w` are at distance 2, so each is a contact of the
other, and **two adjacent centres cannot both be dodecahedral** — verified independently by
Main (`Computation/two_dodecahedra.py`): with both icosahedral twelve-point sets share-axis, the
two eleven-point sets have minimum mutual distance `1.12555484451` for every relative twist
(`t = 0, 18°, 36°, 54°` give `1.1256, 0.5982, 0.2111, 0.5982`), against a required `2`. Hence
`σ₀ ≠ 2V_dod`. ∎

`δ₀ := σ₀ − 2V_dod > 0` is **not explicit** — step 2 is compactness. Two inputs are used and
neither is re-proved: ML's equality case (standard), and the two-dodecahedra impossibility
(now Main's own computation, `1.1255548 < 2`).

> **Theorem C.** With `M` a **maximal** contact matching, `P_B` its edges in `B(0,R)`,
> `ρ := lim P_B/|B| ≤ 1/2`:
> `δ(Λ) ≤ (4π/3)/(V_dod + δ₀ρ) < 0.754697399337` whenever `ρ > 0`.

**Consequences, with scope stated exactly (review 0523 — this block's wording was wrong).**

(i) **Conditional strictness, not a bound.** *If* `ρ > 0` then
`δ(Λ) ≤ (4π/3)/(V_dod + δ₀ρ) < 0.754697399337`. This concerns packings that *have* contacts, it
is not quantitative (`δ₀` is non-explicit), and **it is not a new packing bound** — nothing here
improves `0.754697399337` for all packings.

(ii) **RETRACTED: "the equality case of the dodecahedral density bound is empty."** Rejected
argument: equality would force the average cell volume to equal the pointwise infimum `V_dod`,
hence every cell dodecahedral, hence twelve contacts per centre, hence `ρ > 0`, contradicting (i).
**The first step is invalid** — an average reaching a pointwise infimum *in a limit* does not
force each term to equal it; it forces only that the excess has zero density. What survives: if
`ρ > 0` equality is impossible; if `ρ = 0` nothing follows. **The emptiness is open, not proved.**
(Step (3) of Theorem D is unaffected: there `x, y ≥ V_dod` with `x + y = 2V_dod` genuinely forces
`x = y = V_dod` — two terms, fixed sum.)

(iii) With `ρ = 1/2` and the sharp `δ₀ = 2√32 − 2V_dod`: `V_dod + δ₀/2 = √32` and `c ≤ 1/√32`,
the truth — conditional on the sharp `δ₀` and on `ρ = 1/2`.

(iv) With `δ₀` non-explicit there is no number, and `RESULTS.md` does not move.

**Main's own error, recorded.** The first draft wrote `ρ = 1` in (iii), which is impossible for
a matching (`P_B/|B| ≤ 1/2`) and made the formula appear to return `0.7268 < π/√18` — a bound
below the truth, hence obviously wrong. Caught by `constants_check.py`. Corrected.

**Discrepancy with E, recorded not resolved.** E's `K15-E075` quotes `1.056487696`; Main gets
`1.12555484451` for the same stated configuration. Both are `< 2`, so the impossibility
conclusion agrees and Theorem D is unaffected; Main cites **its own** value. E's number was not
reverse-engineered. Note also that Main's own first version removed the wrong pole for `w` (the
shared contact is at `−2` in `w`'s frame, not `+2`) — the same bug E records — which is why the
check now states the pole convention explicitly.

**Exactness caveat (supervisor, `K15-REVIEW-0438-M-LOCAL`).** E's `barlow_contact_cell.py`
admits vertices via `sp.N(...,30) > 1e-25` and compares radii numerically; it is **not** to be
advertised as fully exact. Main's `contact_cell_exact.py` is a separate implementation with
exact field arithmetic and interval sign decisions (`C104`), and that is what `C094` rests on.
`two_dodecahedra.py` is high-precision (40 digits) but not certified; the conclusion
(`1.1256 < 2`) has a `44%` margin and is insensitive to convention, so it is recorded as
`TESTED_FINITE` rather than `PROVED`.

*Status.* Theorem D `PROVED` modulo the two named inputs; **universal lower-volume claims are
`PENDING_REVIEW`** per the supervisor's standing instruction, and `(L)`/`σ₀` must not be quoted
as established constants. Reviewer X.

### K15-C109 — a compressed symmetric pair family does not probe `(L)` (`TESTED_FINITE`, negative result)

`Computation/pair_family.py`. E's search for `(L)` is one-sided (a dodecahedral `v` and the best
payer `w`), so a *different* family was tried: configurations symmetric under `x ↦ 2−x`, so both
cells are congruent and the pair sum is `2·vol`. A point at distance 2 from **both** centres lies
on the circle `x = 1`, radius `√3`; `n` such points form a ring with mutual separation
`2√3 sin(π/n)`, which is `≥ 2` only for `n ≤ 5`, so the pentagon is the largest admissible ring.
Nine to twelve configurations were evaluated: `ring5 ph0.31` is the best at pair sum
`20.989006`, i.e. `+9.675` above `2√32`, and the rest are worse (`ring4`: `23.111`; `ring3`:
`30.022`). Both cap-ring variants are illegal (min separation `1.732051`).

**Result: the family is far too sparse to probe `(L)`, and this is worth recording as a
negative.** A cell needs about twelve neighbours to approach `V_dod`; the family supplies at most
six per centre, so the cells come out at `11.5`–`15` each instead of `5.6`, and the test can
only ever fail to refute. Since computed volumes are *upper* bounds for any saturated completion,
a value above `2√32` is not evidence *for* `(L)` either. **So this file is neither support nor
counterexample, and it should not be quoted as either.** The only family that reaches the
relevant regime is E's icosahedral one, which is why the payer search is E's.

*Status.* `TESTED_FINITE` (negative). Reviewer X.

### External ids — worker-ledger claims cited by Main

These are defined in a worker's own ledger, not here. They are listed so that a reference from
`Main/` resolves to something a reader can chase, and so that `Computation/ledger_lint.py` can
distinguish "external" from "dangling". Main does not vouch for their content; each is quoted
with the worker's own status.

| id | owner | what it is | status per the owner |
| --- | --- | --- | --- |
| `K15-X-C014` | X | both-sides certificate, `p`-side only, `0.780718153` | X's ledger |
| `K15-X-C015` | X | both-sides, `0.813631102` | X's ledger |
| `K15-X-C016` | X | both-sides, `0.783097911` | X's ledger |
| `K15-X-C017` | X | both-sides rational Gram, `Δ < 0.782267220134` (smaller certificate: `< 0.782267254857`, 41-character entries) | X's ledger; **`PENDING_REVIEW`** in Main pending local review of the smaller certificate |
| `K15-X-C043` | X | Theorem D step 4 verified to 12 digits; the E/Main twist discrepancy resolved (different twist origins) | X's ledger |
| `K15-X-C051` | X | **the two-dodecahedra threshold is `3.4555003444`** — Main's `6/√5` was wrong (missing term, `C126`); `2φ` withdrawn by X | X's ledger; **adopted by Main** |
| `K15-X-C052` | X | A15 Voronoi volumes `125/16`, `129/16`, contact pair `16.125` | X's ledger; confirms Main's `C111` |
| `K15-X-C053` | X | the arithmetic of `C119`/`C122` checked exactly | X's ledger; no discrepancy |
| `K15-X-C055` | X | E's payer fixture reproduced to `1e−12`; it is not the `5.897967122` family optimum | X's ledger; confirms `C118` |
| `K15-E074`, `E075`, `E081`–`E086` | E | the pair conjecture, the two-dodecahedra exclusion, the payer fixtures | E's ledger; `E074` `PROPOSED`, `E078` `WITHDRAWN` by E |
| `K15-C-TRANSFER-DENSITY-002`, `CUTIMPLIES-003`, `HIGHDENS-001`, `PERIODCONV-001`, `CUTBLOB-001`, `DECOUPLE-001`, `CUTEQUIV-001` | C | the cut/flow fixtures and their scope; `CUTEQUIV-001` **withdrawn** by C | C's ledger |

**Checked:** `Computation/ledger_lint.py` (K15-C110) verifies that every *fully-qualified*
`K15-C…`/`K15-E…`/`K15-R…` reference in `KeplerConjecture/` resolves to a heading here, that no
id is defined twice except by an explicit `addendum` sub-heading, and that every status token is
from the documented vocabulary. The `C…`/`E…`/`X…` shorthand used in prose is not checked, so a
typo in shorthand is still possible; 411 shorthand occurrences exist in `Main/`.

### K15-C111 — A15 cell volumes, and a corrected pair type in E's fixture table (`PROVED`, exact rationals)

`Computation/a15_pair.py`. Independent computation of the A15 / Cr₃Si packing (`Pm-3n`, 8 sites per
cubic cell), with `a = 4` so that the nearest distance `a/2 = 2` is exact. Using the adaptive
truncation of Main's Lemma 3 (`BARLOW_CELLS.md`) with the support-function certificate, so the
truncation is verified and not assumed:

| site | Voronoi volume | exact |
| --- | --- | --- |
| A (2 per cell) | `7.812500000` | `125/16` |
| B (6 per cell) | `8.062500000` | `129/16` |
| weighted sum | `64.000000000` | `2·125/16 + 6·129/16 = 64 = a³` ✓ |

The sum identity is an exact internal consistency check that validates the volumes.

**Contact pairs, and a correction to E's table.** The nearest distance in A15 is the B–B chain
bond `a/2 = 2`; the A–B distance is `√5 = 2.236068` and A–A is `2√3 = 3.464`. So the **contacts**
are the B–B pairs, with pair sum `2·129/16 = 129/8 = 16.125`. E's `K15-E074` table quotes A15's
minimum pair sum as `15.875`, which is `125/16 + 129/16 = 127/8` — the **A–B** pair, which is
*not* a contact. Since `(P′)` quantifies over contact pairs only, E's entry for A15 is measuring
the wrong pair type. **Nothing is refuted** (both `15.875` and `16.125` exceed `2√32`, and A15 is
far from the extremal regime), but the row should read `16.125`.

This is the second convention error found in the workers' pair tables this block, after E's pole
convention in `E075` (`C108`, Main `1.1255548` vs E `1.056487696`). Both are recorded because
pair-sum tables are exactly where a wrong pair type is invisible: every entry is plausible and
every entry exceeds the bound.

*Status.* `PROVED` (exact rationals, with the `a³` sum check). Reviewer X.

### K15-C112 — two adjacent dodecahedral centres: certified for **all** relative twists (`PROVED`)

`Computation/twist_cover.py`. Repairs the step of Theorem D that the review correctly called out:
*"a sampled twist maximum is not an all-twists proof."* It was, in `C108` — a grid at
`t = 0°, 18°, 36°, 54°` giving `1.12555484451`. The grid is retracted; here is the proof.

**The structure.** For a pair `(a, q)` drawn from the two eleven-point sets, the squared distance
under a relative twist `t` about the shared `v`–`w` axis is a **pure sinusoid**:

```
d²(t) = A + B cos t + C sin t = A + R cos(t − ψ),     R = √(B²+C²),  ψ = atan2(C, B).
```

So the set of twists for which *that* pair is closer than `2` is

```
T = { t : cos(t − ψ) < (4 − A)/R } ,
```

which is **empty**, the **whole circle**, or a **single arc** of half-width `arccos((4−A)/R)`. A
clash for every twist is therefore the statement that finitely many arcs **cover** the twist
circle, whose period is `2π/5 = 72°` — the icosahedral stabiliser of the shared vertex axis.

**The result.** 121 pairs, each contributing at most one (possibly wrapped) arc; every endpoint
computed at 50 significant digits and then **inflated by `1e−20`**, so the arcs tested are
supersets of the true ones and a cover of the supersets is a cover of the truth. The 125 arcs
merge into

```
one interval covering [0, 2π/5], length 1.25663706 = 2π/5 exactly, gaps: 0.
```

**Hence for every relative twist some pair is closer than `2`, and two adjacent dodecahedral
centres are impossible.** No twist is sampled and no grid enters.

**Why a one-pair argument fails (recorded so it is not retried).** `min` over pairs of
`max_t d²` is `8.4223 > 4`, so no single pair is always too close: the arcs must be *combined*.
This is the substantive content of the step, and the sampled maximum could not see it.

**Status.** `PROVED` (modulo `mpmath.iv`/50-digit arithmetic and the `1e−20` inflation). This
upgrades `C108` step (4) from `TESTED_FINITE`. Reviewer X — noted that X's audit covers
`C106`–`C108`, so this repair is handed to X rather than self-certified.

### K15-C113 — review 0523 corrections to `C106`/`C108`, with the rejected text preserved

Five defects were found by the review, all confirmed, plus one found by Main while checking.

1. **`C_R` counted the wrong edges (review).** `C_R` must be the edges with **exactly one**
   endpoint in `W = B∖E_B` — the crossing edges — and nothing else. An earlier draft described it
   as "every edge not internal to `W`", which wrongly included edges with both endpoints in
   `E_B`; those contribute `0` to the counting identity and must not appear. Fixed in
   `GEOMETRIC_LEMMA_0438.md` §4.1a.
2. **Compactness cardinality (review).** The bound on the number of centres is
   `vol B(0,R+1)/vol B(0,1) = (R+1)³`, not `R³` — the unit balls about the centres are disjoint
   and lie in `B(0,R+1)`. At `R = 21.865` that is `≈11957`, not `≈10453` (`1.4%` larger;
   conclusion unchanged).
3. **Finite truncation redundancy (review).** Stated explicitly: a centre at distance `> 2R_max`
   has its bisector outside `B(v,R_max) ⊇ Ω(v)` and cannot cut, which is Main's Lemma 3; the
   minimiser's cells therefore depend only on centres inside `B(0, 2R_max)`, and that is what
   makes the compactification a statement about a *finite* configuration.
4. **"Equality family is exactly the Barlow family" (review).** Wrong direction: Barlow `⟹`
   equality in `(L)`, but equality `⟹` Barlow is not proved. Retracted to one inclusion in
   `C106`, `GEOMETRIC_LEMMA_0438.md` and `REVIEW_0438.md`.
5. **"The equality case of the dodecahedral density bound is empty" (review).** Retracted. The
   rejected argument went from "the average cell volume equals the pointwise infimum `V_dod`" to
   "every cell is dodecahedral", which is invalid in a limit — an average reaching a pointwise
   infimum forces only that the excess has zero density. Retracted in `C108`, `RESULTS.md`,
   `EXPOSITION_0438.md`, `GEOMETRIC_LEMMA_0438.md`, `REVIEW_0438.md`. **The emptiness is open.**
   (Theorem D's step (3) is *not* affected: `x, y ≥ V_dod` with `x + y = 2V_dod` forces
   `x = y = V_dod` — two terms, fixed sum, valid.)
6. **Exact-contact matching is an extra hypothesis (review).** `ρ` counts edges at distance
   *exactly* `2`, so any **scaled** saturated packing (minimum separation `2 + ε`) has an empty
   contact graph and `ρ = 0`. Theorem C is therefore silent on that whole cone and `(M)` is not a
   consequence of saturation. Stated explicitly in `GEOMETRIC_LEMMA_0438.md` §4.2.
7. **Main's own additional finding.** The twist maximum in `C108` step (4) was sampled; `C112`
   replaces it with a certified arc cover and records why a one-pair argument cannot work.

**None of this changes a number, because none of it ever was one.** The pair route remains
`PROPOSED`/`PENDING_REVIEW` above the level of `(L_δ)`, and universal pair/compactness claims are
pending independent review.

### K15-C114 — exact-contact is *not* the binding hypothesis; `ρ_ε > 0` is (`PROVED` reduction)

Review 0523 warns that exact-contact matching "is an extra hypothesis and may fail for scaled
saturated examples". It is and it does (`C113` item 6). This entry records the consequence, and
the clarification that follows from `C112`'s machinery: **the exactness can be removed; what
cannot is the density.**

**Widening to near-contacts.** For `ε ≥ 0` let `G_ε` be the graph of pairs at distance `≤ 2+ε`,
and `σ₀(ε)` the infimum of `vol Ω(v)+vol Ω(w)` over such pairs. Two facts:

1. `σ₀(ε) > 2V_dod` for every **fixed** `ε < 0.6832816 = 6/√5 − 2`: Theorem D's compactness
   argument runs verbatim with "distance exactly 2" replaced by "distance in `[2, 2+ε]`" (the
   admissible set is still compact and `Φ` still continuous), and the equality case still forces
   two dodecahedral cells — whose impossibility is `C112` at `d = 2` and `C116` for every
   `d < 6/√5`, certified by arc cover. **That band is `53.7` times wider than the `ε* =
   0.012718662` the route can ever use**, so the near-contact form is available with room to
   spare. (An earlier version asserted only that "the clash persists for `d > 2`" by continuity;
   `C116` replaces that with a covered range and a sharpness statement.)
   **[Repaired at `C133`]** the impossibility of two dodecahedral cells is now **orientation-free**,
   `|v − w| ≥ 4cos ρ_c = 3.1786179`, proved from the icosahedron's covering radius. So the band is
   `ε < 1.1786179` (the stated `0.6832816` is inside it, and the item's band and use are unchanged),
   the constraint "axis a vertex direction of both" is gone, and `C116`/`C123`'s arc cover is off the
   load-bearing path.
2. `σ₀(ε)` is **not explicit**, for the same reason as `σ₀`, and nothing here gives a rate in `ε`.

Substituting `G_ε` and `σ₀(ε)` for the contact graph and `σ₀` in Theorem C, the bridge holds for
any `ε` with `ρ_ε := lim P_B^{ε}/|B| > 0`. So:

> **The exact-contact restriction is removable.** What is *not* removable is `ρ_ε > 0`: a
> saturated packing whose close pairs are sparse — finitely many, or of zero density — leaves
> `ρ_ε = 0` for every `ε`, and every version of Theorem C is then silent. Scaled examples are
> the simplest such family, but they are a symptom, not the disease.

**Consequence for the route's scope, stated once and plainly.** The pair route's obstruction is
**sparsity of close pairs**, not exact equality of distances. That is a property of the packing
that no amount of two-cell geometry can supply, and it is now `G13`. It also means the review's
scaled-example objection is fully absorbed: a scaled packing with `ε₀ > 0` looseness is handled
by `G_{ε}` for `ε > ε₀` **whenever it has a positive density of minimum-distance pairs**, and
not otherwise.

**A consistency check, not a theorem.** Two constants in this project coincide by identity:
`ρ* − 2 = 0.012718662` (`C101`, where the isolated dodecahedral cell reaches `√32`) and
`ε* = 2((ML/truth)^{1/3} − 1) = 0.012718662` (where a uniform scaling reaches the dodecahedral
bound). Both are just `√32/V_dod = ML/truth = 1.01919957358` rewritten, so their agreement
confirms the ledger's arithmetic and says nothing new. Recorded only so that a future block does
not read a coincidence into it.

*Status.* `PROVED` reduction (item 1 is compactness plus `C112`); no number, no bound. `PENDING_REVIEW`
with the rest of the pair chain. Reviewer X.

### K15-C115 — the primary-source equality case, verified (`AUDITED`)

Review 0523 asked for "the **actual primary-source** equality case". Previous blocks cited
Hales–McLaughlin's equality case from memory. It is now read from the paper and quoted here.

**Source.** T. C. Hales and S. McLaughlin, *The Dodecahedral Conjecture*, 6 pages,
`https://www.cs.cmu.edu/~seanmcl/papers/McLaughlin-Dodec.pdf`, retrieved this block,
`sha256 beab1f4a6c41bfe02c719db3f16cd3a78c9a6666f3fe7b91fe3c72f939ef6960`, 2 675 648 bytes.
`pdftotext -layout` gives 139 128 bytes of text; the quotations below are from the extracted
text and were checked against the page image of p. 2.

**The equality case, verbatim (Introduction, p. 2).**

> *"The assertion can then be stated as the inequality*
> `vol(Ω(Λ, v)) ≥ vol(Ω(Λ_dod, 0))`
> *for every `v ∈ Λ`, and for every set of points `Λ ⊂ R³` whose pairwise distances are at least
> the diameter 2. **The case of equality occurs exactly when `Ω(Λ, v)` is congruent to a regular
> dodecahedron of inradius 1.**"*

Three things this settles, all of which the ledger had been assuming:

1. **The equality case is an "exactly" statement**, not merely that the dodecahedron attains the
   bound. `C108` step (3) needs `vol Ω = V_dod ⟹ Ω` is a regular dodecahedron of inradius 1, and
   that is exactly what the source says. **Theorem D's dependency is verified, not assumed.**
2. **The quantification is over arbitrary 2-separated point sets**, not over packings with a
   density — `"every set of points Λ ⊂ R³ whose pairwise distances are at least 2"`. That is
   precisely the setting of `C108`, which minimises over 2-separated configurations rather than
   over packings. No bounded-density or saturation hypothesis is smuggled in.
3. **The extremal object is the 13-point configuration** — *"a finite packing `Λ_dod` (of twelve
   balls and a thirteenth at the origin) obtained by placing a point of `Λ_dod` at the center of
   each face of a regular dodecahedron (of inradius 2)"* — i.e. twelve centres at distance exactly
   `2` in the icosahedral directions, which is the configuration `C069`, `C095` and `C112` all
   work with.

**A second, independent equality source for the same fact.** §4 quotes Fejes Tóth's reduction:

> **Theorem 4.1.** *"Let `P` be any polyhedron with at most 12 faces that contains a unit sphere
> `S²`. … The volume of the intersection of `P` with `B` is at least `ω_dod`. Equality holds
> exactly [when] `P` is congruent to the regular dodecahedron `Ω(Λ_dod, 0)`."*

So for cells with **at most 12 faces** the equality case is Fejes Tóth's theorem — a statement
about *all* polyhedra containing a unit sphere, not about Voronoi cells at all. The paper also
records that `t_dod = 3 tan(π/5) ≈ 1.258` is the truncation radius and that the conjecture is
proved by combining this with the general case.

**What this does *not* give.** No quantitative stability: neither the introduction nor Theorem 4.1
bounds how far from a dodecahedron a cell may be while staying within `V_dod + ε`. So `δ₀` in
`C108` remains non-explicit, and `G11`/`G14` are unaffected. The verification removes an
assumption from Theorem D's ledger entry; it does not add a number.

*Status.* `AUDITED` (source read, quoted, hashed). Reviewer X.

### K15-C116 — the near-contact band is `6/√5 = 2.6832816`, and it is sharp (`PROVED`, arc cover)

`Computation/near_contact_band.py`. Quantifies `C114`'s widening, which asserted only that "the
clash persists for `d > 2`". It does, much further than needed:

> **Two dodecahedral cells are impossible whenever their centres are less than `6/√5 =
> 2.6832815729997476` apart** — and the arc-cover certificate **fails** for every larger `d`
> tested, so the constant is sharp for this method.

Method: the `C112` arc cover, run with the partner centre at `(d,0,0)` instead of `(2,0,0)`.
Coverage of the twist circle is `1.0000` (no gaps) at `d = 2.00, 2.02, 2.05, 2.10, 2.20, 2.40,
2.60` and fails at `2.80`; bisection gives the threshold bracket
`[2.68328151703, 2.68328170776]`, whose closed form is `6/√5 = 2.683281572999…`
(`(6/√5)² = 36/5 = 7.2` exactly).

**Why this matters for the route.** `C114` widens Theorem D from "distance exactly 2" to
"distance `≤ 2+ε`", which requires the clash to survive at `d = 2+ε`. It survives for
`ε < 0.6832816`, so the near-contact bridge is available on a band **`53.7` times wider** than
the widest band the route can actually use (`ε* = 0.012718662`, where a uniform scaling meets the
dodecahedral bound). **So the exact-contact restriction is comfortably removable and was never
the obstruction** — which is exactly `C114`'s conclusion, now with a constant and a sharpness
statement instead of an assertion.

**Not claimed.** Sharpness is for *this* certificate (the arc cover at threshold exactly `2`);
beyond `6/√5` the test says nothing, and it is entirely possible that two dodecahedral cells stay
impossible to larger `d` by an argument this one cannot see. The bracket is asserted only as a
bracket, and `d = 6/√5` itself was not resolved (the bisection window is `1.9×10⁻⁷` wide and
straddles it).

*Status.* `PROVED` on `[2, 6/√5)` modulo 50-digit arithmetic and the `1e-20` inflation; `TESTED`
for the sharpness claim. Reviewer X.

### K15-C117 — the dodecahedral bound's true cost, read from the primary source (`AUDITED`; corrects `K15-C100`)

`K15-C100`'s cost table attributed Hales–McLaughlin to "one cell inequality (dodecahedron)" — a
row that reads as a short proof and invites the inference that a **two**-cell inequality would
also be short. The primary source (`K15-C115`) contradicts that, and this entry corrects it.

**What the proof actually costs** (quotations from Hales & McLaughlin, §3 and §1.3):

- Three programs: *"graph generation"*, *"a linear programming package"*, and *"a piece of code
  based on interval arithmetic that automatically proves nonlinear inequalities"*; the paper
  refers to *"several hundred linear programs"*.
- The reduction is by **hypermaps**: *"each tame Voronoi graph can be encoded as a hypermap `H` …
  the computer code repository specifies a hypermap system, called the Voronoi hypermap system,
  for each case `H` arising in the classification"*, with infeasibility via LP.
- Two cases: `n ≤ 12` (Fejes Tóth) and `n ≥ 13` (the full machinery plus a local-deformation
  argument, §6, Theorems 6.2–6.3).
- On the relation to Kepler: *"the two solutions follow a similar outline and share a significant
  number of methods. Both are based on long computer calculations. Computer code was freely
  exchanged between the two projects."*

**Three consequences.**

1. **`0.754697399337` is Kepler-scale, not cheap.** The pair route must not be advertised as
   "a shorter proof than Hales" on the strength of the ML precedent; the nearest precedent for a
   multi-cell tightening is itself a major computation plus a delicate deformation argument.
   `K15-C100`'s column is corrected accordingly.
2. **The differentiator is the reparametrisation, not the scale.** ML's mechanism is a *weight
   assignment* — an LP duality over clusters — not a two-cell volume inequality, so a pair bound
   would be a genuinely different object; but nothing here suggests it is *easier*.
3. **Independent confirmation that the pointwise family is rigid** (`D19`): *"With the
   Dodecahedral problem, there is no such flexibility. The problem about finite clusters of balls
   is fixed from the outset. This gives the problem a degree of rigidity that is not present in
   the sphere packing problem."*

**What is not claimed.** Not that the pair bound is hard — only that the ML precedent gives no
evidence it is easy. Neither cost has been estimated for `(L)`.

*Status.* `AUDITED` (quotations read from the source). Reviewer X.

### K15-C118 — E's frozen payer fixture reproduced independently (`AGREES`, 1e−15)

`Computation/payer_reproduce.py`. This is the most load-bearing number in the pair route — the
`(P′)` margin at the icosahedral pair — and until now it had only been produced by E's own scripts
(the supervisor's local pilots ran E's code). Main rebuilt the configuration from E's written
description and recomputed the cell with Main's own code.

**Inputs, quoted verbatim from `COMPUTE_REQUEST_0353.md` (commit `c76194f`):**

```
c=(0,0,0), w1=(0,0,2), 5 ring at (4/sqrt5 cos 72k, 4/sqrt5 sin 72k, 2/sqrt5),
5 pentagon at w1 + 2(s cos(36+72k), s sin(36+72k), 3/8), s = sqrt55/8,
south=(0,0,4)
```

**Result.**

| quantity | Main | E | difference |
| --- | --- | --- | --- |
| `vol Ω(w1)` | `5.89801737180372` | `5.898017371803720` | `1e−15` |
| min separation, all `78` pairs | `2.0000000000000000000` | `≥ 2` | — |
| cell vertices | 20 | (not quoted) | — |
| margin over `(P′)`'s required `5.763417470` | `0.1345999018` | `0.134590`/`0.134549` | last-digit only |

The margin needs care and Main resolves it: `(P′)` requires `5.763417470`, so the **frozen
fixture's** margin is `5.898017372 − 5.763417470 = 0.134599902`, while the **C5 family optimum**
`5.897967122` (E's `K15-E086`) gives `0.134549652`. The two numbers quoted across worker
documents (`0.134590`, `0.134549`) are these two different objects; both exceed zero, so `(P′)`
survives at the pair either way. Recorded because a factor-of-`10⁻⁵` disagreement in a *margin*
is exactly what an error in the *value* would look like.

**Two bugs in Main's own first attempt, recorded.** (i) The volume was computed by a fan
triangulation over arbitrary vertex pairs, which does **not** tile a convex polytope and
overcounted by `11×` (`66.13` against `5.898`); replaced by a convex hull. (ii) The legality test
used `dmin ≥ 2` exactly, which fails by `1e−38` on an exactly-2 separation at 40 digits; replaced
by `dmin ≥ 2 − 1e−15`. Both are the same class of error as `C104`'s normalisation slip: a check
that reports a false failure of a true statement.

**What this establishes and what it does not.** It removes the dependence on E's own code for the
fixture value, and it confirms the margin is genuinely positive at the sharpest known witness.
It does **not** make the fixture a proof of `(P′)`: E's own `K15-E090` notes the fixture is a
*local* witness whose five pentagons would clash if repeated at all twelve outer centres, so it
tests `(P′)` and says nothing about simultaneous compensation of the cluster.

*Status.* `AGREES`. Reviewer X.

### K15-C119 — where the dodecahedral bound is actually doing work, and why the pair route's scope is fine (`PROVED`)

Three elementary inequalities, combined, locate the pair route exactly.

1. **Inball bound.** Every cell contains the inball `B(v, d/2)` where `d` is the minimum
   separation, so `vol Ω(v) ≥ (4π/3)(d/2)³` and hence
   `δ ≤ (4π/3)/((4π/3)(d/2)³) = 8/d³`.
2. **Where that already beats Hales–McLaughlin.** `8/d³ ≤ 0.754697399337` iff
   `d ≥ 2.1967082337…`. So **for every packing with minimum separation `≥ 2.1967082` the
   dodecahedral bound is implied by the trivial inball bound** and ML does no work.
   (The same constant appears in `C101` as the radius beyond which the inball beats `V_dod` —
   it is the same comparison, `V_dod = (4π/3)(d/2)³`.)
3. **The near-contact band of `C116` reaches `6/√5 = 2.6832816`**, which strictly contains
   `2.1967082`.

> **Consequence.** The only packings on which a two-cell argument has to do anything are those
> with `2 ≤ min separation < 2.1967082`, and on that whole range — with a margin of `0.49` in
> `d` — the near-contact pair bound of `C114`/`C116` is available.

So the pair route's **scope** is not in question: it covers everything the dodecahedral bound is
not already giving for free. What remains is `ρ_ε > 0` (`G13`) — the *density* of close pairs, not
their existence or their distance. That is the honest residue, and `C114` already says the same
thing from the other side.

**Also recorded: this is not new mathematics.** `δ ≤ 8/d³` is the oldest bound in the subject and
combining it with a range check is bookkeeping. Its value is that it *locates* the route: before
this entry the pair route's applicability range had not been compared with the range on which the
target bound is non-trivial, and the check comes out favourably by a wide margin.

*Status.* `PROVED` (elementary). Reviewer X.

### K15-C120 — E's C5 payer family scanned; the margin is a window, not a knife-edge (`AGREES`)

`Computation/payer_family.py`, extending `C118`'s reproduction from the frozen point to the whole
family. Parameter `dz` = the pentagon's height above `w1`; E's polar angle is `θ` measured from the
inward direction, so `dz = −2 cos θ`.

| claim (E's `K15-E085`/`E086`) | Main's scan | agree? |
| --- | --- | --- |
| legal window `θ ∈ [106°, 120°]` | legal `dz ∈ [0.55, ≥0.90]`, illegal at `0.50` (`min sep 1.9806`); `θ=106°` ↔ `dz=0.551`, `θ=120°` ↔ `dz=1.0` | **yes**, lower end matched exactly; upper end `≥0.90` is consistent with closing at `1.0` |
| `Ω(w1)` has exactly **twelve** faces for every legal `θ` | **12 active half-spaces at every one of 37 sampled `dz`**, legal or not; 20 vertices, Euler `20−30+12 = 2` | **yes**, and stronger |
| family minimum on the 1° grid `= 5.898007181` at `θ = 112°` | min on a `0.05` grid in `dz`: `5.898017372` at `dz = 0.75`; `θ=112°` ↔ `dz=0.7492`, between grid points | **consistent** — the `0.0006` gap is the `Δθ = 0.02°` between the two points |
| continuous optimum `5.897967122` | bracketed by `5.898017372` (`dz=0.75`) and `5.898007181` (E, `dz=0.7492`) | **consistent** |
| margin over the required `5.763417470` | `0.134599902` at the frozen fixture | **yes** |

**The point of the scan.** E's claim is that the `(P′)` margin is a property of a whole `14°`
window rather than of one tuned angle. The scan confirms it independently: the value varies
smoothly (`5.932` at `dz=0.55` down to `5.898` at `dz=0.75` and back to `5.922` at `dz=0.90`) and
stays above `5.932` throughout the window, i.e. **at least `0.169` above the requirement at every
legal point**, not merely at the optimum. So the margin is robust to the angle, which is what makes
it a meaningful margin at all.

**Not claimed.** Nothing here is a proof of `(P′)`; it is an independent reconstruction of E's
family and an independent confirmation of its numbers. The household caveat still applies
(`E090`): this is a *local* witness, not a completion of the cluster.

*Status.* `AGREES`. Reviewer X.

### K15-C121 — an explicit stability bound for cells with `≤ 12` faces (`PROVED`, elementary)

This is the first **explicit** stability statement in the project, and it is three lines. It comes
straight out of Fejes Tóth's Theorem 4.1 as quoted in `K15-C115`.

> **Lemma (explicit stability).** Let `Ω(v)` be a Voronoi cell with **at most 12 faces**, and
> suppose every neighbour of `v` is at distance `≥ 2ρ` with `ρ ≥ 1` — equivalently every face of
> `Ω(v)` is at distance `≥ ρ`. Then
>
> ```
> vol Ω(v)  ≥  V_dod · ρ³ .
> ```

*Proof.* Scale by `1/ρ`. The body `P := Ω(v)/ρ` is convex, contains `B(0,1)` (since it contains
`B(0,ρ)/ρ`), has at most 12 faces ✓, and each face is at distance `≥ 1` from the origin. So
Fejes Tóth's Theorem 4.1 applies and gives `vol P ≥ ω_dod = V_dod`. Hence
`vol Ω(v) = ρ³ vol P ≥ V_dod ρ³`. ∎

**Why this matters.** `Main/CLOSED_COMPONENT.md` A2 recorded the obstruction to the singleton
closed-component question as: *"what a proof needs is stability of the dodecahedral inequality:
cells with inradius `≥ 1.045` have volume `≥ V_dod·(1.045)³` — neither is available."* That is
exactly the lemma, and it **is** available, with the one hypothesis "at most 12 faces". Feeding in
the isolated-vertex value `ρ = 1.045`:

```
vol Ω(v)  ≥  V_dod·(1.045)³  =  6.333804106  =  1.1197·√32  >  √32 .
```

So **an isolated vertex whose cell has at most 12 faces has `b(v) = √32 − vol Ω(v) < 0` outright**,
and the singleton closed-component question is settled in that case — the deficit is negative by
`12%`, with no compactness and no unspecified constant.

**Where it falls short, stated exactly.** The hypothesis is a *face count*, and it is not automatic:
an isolated vertex has all bisectors at distance `≥ 1.045`, so every neighbour within `2·R_cell`
cuts, and with `R_cell` up to `≈1.48` that admits neighbours out to `2.96` — potentially more than
twelve of them (a volume count allows up to `≈16` in the annulus `[2.09, 2.956]`, `C101`). So the
lemma covers the `≤ 12`-face case and not the rest. What it does establish is that the
`C096`/`C101` "case (A)" is now **explicit** rather than compactness-based, and that the residual
gap in the singleton question is exactly: *can an isolated vertex's cell have more than 12 faces?*

**A second, weaker form with no face-count hypothesis at all.** If every neighbour is at distance
`≥ 2ρ` then `B(v,ρ) ⊆ Ω(v)`, so `vol Ω(v) ≥ (4π/3)ρ³` for every cell. That needs no Fejes Tóth and
no face count, and it beats `V_dod` once `ρ³ ≥ 3V_dod/(4π)`, i.e. `ρ ≥ 1.0983541` (`ρ = 1.045` is
below this, which is why Fejes Tóth's theorem is doing real work in the lemma above).

*Status.* `PROVED` (elementary, from `K15-C115`'s quotation of Theorem 4.1). Reviewer X.

### K15-C122 — the concrete target that would close the singleton case: a `20`-face circumscribed bound (`PROPOSED`, with numbers)

`C121` settles the singleton closed-component question for cells with **at most 12 faces**. This
entry states exactly what would extend it to all cells, with the target value computed.

**The extension of `C121`'s argument.** Repeat its three lines with Fejes Tóth's Theorem 4.1
replaced by any bound of the form

> **(B_F)** *a convex body containing a unit ball with at most `F` faces and all faces at distance
> `≥ ρ` has volume `≥ c_F ρ³`.*

`C121` is the case `F = 12`, `c_F = V_dod`. Then `vol Ω(v) ≥ c_F ρ³`, and for the isolated-vertex
value `ρ = 1.045` we need `c_F (1.045)³ > √32`, i.e.

```
c_F  >  √32 / 1.045³  =  4.95708216846 .
```

**What each candidate constant gives:**

| `c_F` | source | `c_F·1.045³` | vs `√32 = 5.656854` |
| --- | --- | --- | --- |
| `V_dod = 5.550291` | Fejes Tóth, `F ≤ 12` (`C121`) | `6.333804` | `+11.97%` ✓ |
| `V_ico = 5.054056` | regular icosahedron of inradius `1` | `5.767518` | `+1.96%` ✓ |
| `4π/3 = 4.188790` | the inscribed ball (no face count) | `4.780105` | `−15.5%` ✗ |

So **`V_ico` is already enough**, with `1.96%` to spare — and `V_ico = 5.0540561436` was computed
here: with inradius `1` the regular icosahedron has edge `a = 12/(√3(3+√5)) = 1.3231690765` and
volume `5(3+√5)a³/12 = 5.0540561436`.

**The two gaps, precisely.**

1. **No face count.** An isolated vertex's neighbours all lie at distance `≥ 2.09`, and only those
   within `2R_cell` can cut. But `R_cell` is not bounded *a priori* without a volume bound, so the
   face count is not automatically `≤ 20`; the residual range is `F ≥ 13`. This is the same
   circularity `C108`'s compactness had to break, and it is not broken here.
2. **`c_F` for `13 ≤ F ≤ 20`.** `C121` gives `c_12 = V_dod`; the value at `F = 20` is the minimum
   volume of a circumscribed polyhedron with `20` faces, which is `≤ V_ico` (the regular icosahedron
   attains `V_ico`, but whether it *minimises* over `20`-face circumscribed polyhedra is a classical
   question Main has **not** resolved — no source for it is in the repository and it was not
   searched). The target is a lower bound at `F = 20`, on the expectation that the minimum
   decreases with `F` — which is *supported* by the Platonic sequence but **not proved here**
   (`F = 4, 6, 8, 12, 20` give `13.86, 8.00, 6.93, 5.55, 5.05`, monotonically down toward the
   sphere's `4.19`). So: **any `c ≥ 4.958` valid for circumscribed polyhedra with `≤ 20` faces
   would close the `≤ 20`-face case**, and the monotonicity is an expectation, not a lemma.

   *(A false start, recorded: Main considered getting `c` from Santaló's inequality and abandoned
   it — the constant `vol(B)²` that came to mind is **wrong**; the regular tetrahedron of inradius
   `1` has `vol·vol° = 13.86 × 0.513 = 7.11 < 17.55`, so the recalled form is false. Nothing was
   recorded from it, and it is noted so that nobody picks it up as if it had been checked.)*

**Why this is worth stating.** It converts "settle the singleton question" into two concrete
sub-problems with numbers: a classical circumscribed-polyhedron bound at `F = 20` (target `4.958`),
and a face-count bound. Neither is a sharpness barrier and both are finite-dimensional.

*Status.* `PROPOSED`. The arithmetic in the table is `PROVED` and re-derived in
`constants_check.py`; the two gaps are open. Reviewer X.

### K15-C123 — the arc cover is re-done with rigorous **inner** arcs (`PROVED`; supersedes `C112`'s rounding)

> **SUPERSEDED as the certificate of record by `K15-C128`/`C129`** (review 0608). The band now has a
> closed form from a *single pair* in exact arithmetic (`d_max = 4/√5 + 2√((2√5−1)/5)`), needing no
> covering, no period reduction and no bisection. This entry is kept because it records the rounding
> repair and because the covering tooling still exists — but **do not use the cover where the closed
> form applies.**

Review 0608: *"Your arc cover must use rigorous INNER safe arcs for a cover by strict violations;
inflating outer numerical endpoints cannot certify an all-twists exclusion."* **Correct, and it is
a soundness error in `C112` as written.**

**What was wrong.** `C112` built, for each of the 121 pairs, the arc of twists that put that pair
closer than 2, and then **inflated both endpoints outward by `1e−20`**. That produces supersets of
the true violation sets. A cover by supersets does not prove a cover by the sets: the extra
material can close the gaps by itself. The same inflation is *correct* when bounding an error term
and *wrong* here — the direction depends on whether the arcs are being estimated or covered.

**The fix.** Arcs are now **inner**: with `T_pq = (ψ − h, ψ + h)` the true (open) violation arc,
the interval used is `(ψ − h + MARGIN, ψ + h − MARGIN)` with `MARGIN = 1e−30` at 60-digit
arithmetic. Arithmetic error is `< 1e−57` over ~20 operations, so `MARGIN` is 27 orders above the
error and 27 orders below any arc width: the shrink is rigorous and costs nothing. A cover by inner
arcs is a cover by **strict** violations, which is exactly what an all-twists exclusion needs.

**Result (unchanged, now sound).** 121 pairs: 71 never violate, 50 give proper arcs; 125 arcs
placed (including wrapped copies), merging into **one interval covering `[0, 2π/5]` with zero
gaps**, length `1.2566370614 = 2π/5`. So for every relative twist some pair is strictly closer
than 2, and two adjacent dodecahedral centres are impossible.

**`C116` re-derived with inner arcs, and it survives.** The critical separation, re-bisected with
the inner-arc test to 30 iterations, is bracketed by
`[2.68328157290816, 2.68328157309443]`, which contains `6/√5 = 2.68328157299975`. So the band
`ε < 0.6832816` stands, now certified in the sound direction.

**Also fixed in the same pass:** `near_contact_band.py` had the same outward inflation (it was a
copy of the `C112` construction) and is now rewired to the inner-arc routine; `twist_cover.coverage`
gains an empty-input guard (with `d` large enough no pair violates, the merge list was empty and
the code crashed).

*Status.* `PROVED` (modulo the 60-digit arithmetic and the `1e−30` inner margin). `C112`'s
*statement* is unchanged and its rounding is superseded; per review 0608 both `C112` and this entry
stay **`PENDING_REVIEW`** until X checks the exact claims.

### K15-C125 — the `13`–`20`-face route **stops**, and a tempting reduction is refuted (`PROVED` negative)

Attempt 1 of review 0608's brief: the `13`–`20`-face circumscribed-volume constants that
`K15-C122` needs. **The literature, the arithmetic and a counterexample all say stop.** Recorded as
a precise failed lemma, which the brief counts as a deliverable.

**(a) The constants are not available as theorems.** `c_F` := min volume of a convex body containing
`B(0,1)` with `≤ F` faces. Reading the sources:

- **Fejes Tóth, *Regular Figures* p. 263, Theorem 2.1** (formula quoted in Horváth,
  arXiv:1509.08859v2, §2): for a convex polyhedron with `f` faces, `v` vertices, `e` edges, inradius
  `r` and circumradius `R`, a **two-sided** bound of the form
  `(e/3)·sin(πf/e)·tan²(πf/2e)·tan²(πv/2e)·r³ ≤ V ≤ (quadratic in cot, cos)·R³`.
  It bounds `V` below only through `f`, `v`, `e` **jointly**; with `r = 1` it is not a function of
  `f` alone, so it does **not** give `c_F`.
- **Proved cases.** Fejes Tóth proved `F = 4, 6, 12` (tetrahedron, cube, dodecahedron) via Goldberg's
  Steinitz-number bound; `F = 5` is also proved; *Symmetry* **9** (2017) 41 proves `F = 8, 10, 14`
  and leaves `F = 18, 20, 22` **conjectured**, citing **N. Mutoh, "The polyhedra of maximal volume
  inscribed in the unit sphere and of minimal volume circumscribed about the unit sphere", JCDCG,
  LNCS 2866 (2002) 204–214**, whose optima for `F = 4..30` are computer-aided *conjectures*.
- So for `F = 13, 15, 16, 17, 18, 19, 20` — seven of the eight values `C122` needs — **no proved
  constant exists to cite.**

**(b) The monotonicity `C122` relied on is false.** `C122` wrote "the minimum decreases with `F`",
supported by the Platonic sequence. It is not true in general. With inradius `1`:

| solid | faces | volume |
| --- | --- | --- |
| regular tetrahedron | 4 | `13.856406` |
| cube | 6 | `8.000000` |
| regular octahedron | 8 | `6.928203` |
| **truncated octahedron** | **14** | **`6.158403`** |
| **regular icosahedron** | **20** | **`5.054056`** |

The `14`-face truncated octahedron is **worse than the `20`-face icosahedron** by `22%`. So
"more faces ⟹ smaller minimum" is false, and the target cannot be aimed at `F = 20` on that basis.
(This also corrects `C122`'s reading of the Platonic sequence: it is monotone in `F`, but it is not
the sequence of *minimisers*.)

**(c) A crude estimate cannot substitute, and misses by a wide margin.** A circumscribed polyhedron
with tangency points `w_i` has `V = (1/3)Σ_i ∫_{S_i} sec θ dσ` over the normal-fan tiling of `S²`.
For `F = 20` equal caps (solid angle `4π/20`, angular radius `0.451027`),
`∫sec = 2π(−ln cos θ) = 0.662000`, so `V ≈ (1/3)(20)(0.662000) = 4.413331`. That is **below**
`C122`'s threshold `4.957082`, so any argument using only the *count* of faces through this estimate
lands on the wrong side; the threshold would need the minimiser to be `12%` *worse* than equal caps,
and nothing supplied here says so.

**Verdict: stop this branch.** `C122`'s target is not reachable by citation (unproved for seven of
the eight faces), not reachable by monotonicity (false), and not reachable by the count-based
estimate (misses by `12%`). `G11` is unaffected. What would revive it is a *proved* `c_F` for
`F ≤ 20` at `≥ 4.958` — which by (a) is exactly the open part of Mutoh's conjecture and cannot be
assumed here.

*Status.* `PROVED` negative (the refutations in (b) and (c) are arithmetic; (a) is a literature
finding with locators). Reviewer X.

### K15-C124 — the near-contact bridge without assuming positive contact density (`PROVED`)

Attempt 2, and the successful one: remove the hypothesis `ρ_ε > 0` that `C108`'s Theorem C and
`C114` need, which review 0608 says must **not** be assumed. It can be removed by a two-case split
against the inball bound.

**The missing implication.** Let `S_ε := {v : ∃w with 0 < |v−w| ≤ 2+ε}` and let `M` be a **maximal**
matching of the `(2+ε)`-graph. Every `v ∈ S_ε` is either matched or, by maximality, adjacent to a
matched vertex; so `S_ε ⊆ matched ∪ N(matched)` and, with `deg ≤ 12`,

```
|S_ε ∩ B|  ≤  2|M ∩ B| + 12·2|M ∩ B|  =  26 |M ∩ B| .
```

Hence `ρ_ε = 0` forces `S_ε` to have density zero. **This is the step that was missing**: the pair
bridge does not need `ρ_ε > 0` as an assumption — where it fails, the packing is *asymptotically
ε-loose*, and that case the trivial bound handles.

**The split.** Fix `ε ∈ (0, 0.6832816)`, inside the band certified by `C116`/`C123`. Let `Λ` be
saturated 2-separated, `c = c(Λ)`, `δ = (4π/3)c`.

- **Case `ρ_ε > 0`.** Theorem C gives `δ ≤ (4π/3)/(V_dod + δ₀(ε)ρ_ε) < (4π/3)/V_dod =
  0.754697399337`, strictly, since `δ₀(ε) > 0` (`C108` via `C114`).
- **Case `ρ_ε = 0`.** Then `|S_ε ∩ B| = o(|B|)`, so all but `o(|B|)` cells contain `B(v, 1+ε/2)` and
  `vol Ω(v) ≥ (4π/3)(1+ε/2)³`. Since `Σ_{v∈B} vol Ω(v) = (4π/3)R³(1+o(1))` and
  `|B| = c(4π/3)R³(1+o(1))`,

  ```
  (4π/3)R³ ≥ (|B| − o(|B|))·(4π/3)(1+ε/2)³  ⟹  1 ≥ c(4π/3)(1+ε/2)³  ⟹  δ ≤ 1/(1+ε/2)³ .
  ```

  At the band end `ε = 0.6832816`: `δ ≤ 1/(1.3416408)³ = 0.414086…`.

> **Theorem.** Every saturated 2-separated packing in `R³` satisfies `δ(Λ) < 0.754697399337`
> **strictly**, with no hypothesis on contact density. Explicitly
> `δ(Λ) ≤ max{ (4π/3)/(V_dod + δ₀(ε)ρ_ε), 1/(1+ε/2)³ }`, and the second branch is at most
> `0.414086` for `ε ≤ 0.6832816`.

**What this achieves, and what it does not.**

1. **`G13` is closed as a *hypothesis*.** The bridge now assumes nothing beyond saturation and
   2-separation; `ρ_ε > 0` is no longer required, which is what review 0608 asked for.
2. **The dodecahedral bound is not attained — properly this time.** `C113` retracted an earlier
   "equality case is empty" claim because it used an invalid average-to-pointwise inference. This
   argument does not: it splits on `ρ_ε`, and in the `ρ_ε = 0` branch it bounds the *density* directly
   from the cell-volume sum, with no termwise inference. **The emptiness is restored on a sound
   proof** (`G14` closes).
3. **Still not a number.** `δ₀(ε)` is non-explicit (`C108`), so branch 1 gives strictness and no
   constant. **Nothing here is a new packing bound and `RESULTS.md` does not move.**
4. **The second branch uses `≥`, not `>`**: `v ∉ S_ε` means *every* other centre is at distance
   `> 2+ε`, so `Ω(v) ⊇ B(v, 1+ε/2)` and `vol ≥ (4π/3)(1+ε/2)³` — the argument needs only `≥`.

> **DOWNGRADED to `CONDITIONAL` (review 0653, `K15-C131`).** The case-2 branch needs the
> **all-orientation** two-dodecahedra exclusion on `[2, 2.1967]`, not the axial version that `C129`
> proves: at `d > 2` the second icosahedron is free in `SO(3)`. The counting, the split and the inball
> branch are unaffected; the dependence on the exclusion is stated and submitted as `X-ORIENT-001`.
> The counting constant is also corrected at `C132` (`deg ≤ 12` does not hold at radius `3.4555`).

*Status.* `PROVED` again. Between `C131` and `C133` this entry stood as `CONDITIONAL` on
`X-ORIENT-001`; that note is kept above for the record, and it was right that `C129` alone did not
supply the exclusion. `C133` supplies it orientation-free (`|v − w| ≥ 3.1786179`), so the `ρ_ε > 0`
branch needs no orientation hypothesis, and the counting is `C132`. `PENDING_REVIEW` with the rest of
the pair chain.

### K15-C126 — a missing term in the twist sinusoid: found by X, confirmed, and the band withdrawn (`CORRECTION`)

Review 0608 asked for inner arcs (`C123`, done). While reconciling X's `K15-X-C051` — which reports the
two-dodecahedra threshold as `3.4555003444`, *not* `6/√5` — Main found a **genuine bug in its own
formula**, and X's number is the correct one.

**The bug.** With `R_t` a rotation about the `x`-axis and `u = w − a`, `b − a = u + R_t q`, so

```
d²(t) = |u|² + |q|² + 2⟨u, R_t q⟩
      = |u|² + |q|² + 2u_x q_x + 2(u_y q_y + u_z q_z)cos t + 2(u_z q_y − u_y q_z) sin t .
```

The first version put `A = |u|² + |q|²` and **dropped `2u_x q_x`** — the `x`-components are untouched
by a rotation about `x`, so that term does not vanish. Confirmed numerically on a pair at `d = 2.7`:
direct `min_t d² = 7.29` against `A − R = 4.06`, and `4.06 + 2u_x q_x = 7.29` exactly.

**What it affected, and what it did not.**

- **`C112`/`C123`'s certification at `d = 2` survives.** With the corrected `A`, re-running gives
  68 never-violating pairs, 53 proper arcs, 133 arcs, merging to one interval covering `[0, 2π/5]`
  with zero gaps. Independently, a direct scan of the minimum cross-distance over a fine twist grid
  gives `max over t of min_pq d² = 1.266874`, i.e. `1.1255548 < 2` everywhere. **The two methods
  agree at `d = 2`**, so **Theorem D step (4) is sound** and needs no further repair.
- **`C116`'s numeric threshold is WITHDRAWN.** `6/√5 = 2.6832816` was a consequence of the missing
  term. X's `3.4555003444` is correct, and Main's own direct scan agrees: the max over twists of the
  min cross-distance is `1.9999997` at `d = 3.4555` and `2.007172` at `d = 2√3 = 3.4641`, so the
  threshold sits just below `2√3`. **`C116`'s *statement* that a band exists is unaffected; its
  constant is replaced by X's `3.4555`** (attributed to X, `X-C051`), and Main's `6/√5` is retired.
- **The arc test disagrees with the scan above `d ≈ 3.5`** (it still covers at `3.5`, where the scan
  finds a twist with no pair closer than 2). Main has **not** resolved that; it does not affect
  `d = 2`, where the methods agree. Until resolved, the arc test is certified **only at `d = 2`**
  and no band end is claimed from it.
- **`C124` is unaffected.** It needs `σ₀(ε) > 2V_dod` for *one* `ε` inside the band, and uses
  `ε = 0.6832816`, which is inside every candidate band (`6/√5 − 2` withdrawn, `3.4555 − 2 = 1.4555`
  from X, and Main's scan). So the two-case split stands; only the *number* `0.6832816` should be
  quoted as "any `ε ≤ 1.45`", attributed jointly.

**Two method failures of Main's in one object** — a wrong constant term, and an arc test that is not
monotone in the way the scan is. Both were caught by comparing with an independent computation, which
is the only reason they surfaced. `C112`, `C123` and this entry stay **`PENDING_REVIEW`**.

*Status.* `CORRECTION`; `C116`'s constant retired in favour of X's `X-C051`.

### K15-C127 — the violation arcs were the *opposite* inequality: second bug, fixed, band reinstated (`CORRECTION` + `PROVED`)

`C126` fixed a missing constant term in the twist sinusoid. Checking further — the supervisor's
`K15-REVIEW-0608-M-LOCAL` names both defects independently — Main found a **second and worse bug** in
the same object, in the *set* being covered rather than in the arithmetic.

**The bug.** The violation set of a pair is

```
T_pq = { t : d²(t) < thr² } = { t : cos(t − ψ) < c },        c = (thr² − A)/R .
```

Since `cos` is **decreasing** on `[0, π]`, `cos(t−ψ) < c ⟺ |t−ψ| > h` with `h = arccos(c)`. So
`T_pq` is the **complement** of the arc around `ψ` — equivalently the arc **centred at `ψ + π` with
half-width `π − h`**, which is the supervisor's formulation and is what the code now uses. Every
earlier version covered the arcs *around* `ψ`, i.e. the **safe** sets, so its "cover" was a cover by
the complement of what was needed and **proved nothing**.

**Why the earlier versions looked plausible.** At `d = 2` the safe sets do cover, and they keep
covering for every larger `d` — so the test was *monotone in the wrong direction* and reported
"certified" out to `d = 3.5` where the scan says a clash stops at `3.4555`. That disagreement is what
exposed the bug; it is recorded in `C126`.

**The fix, and its confirmation.** Violation arcs are now the complement, reduced into the five
period cells of `R/(2π/5)` (`2π = 5·(2π/5)` exactly), endpoints shrunk inward by `1e−30` so each
piece is a strict subset. Then:

| `d` | corrected arc test | independent twist scan | agree? |
| --- | --- | --- | --- |
| `2.0` | cover | clash everywhere (`max min dist = 1.1255548`) | **yes** |
| `2.6` | cover | `1.3712215` | **yes** |
| `3.0` | cover | `1.6398674` | **yes** |
| `3.4` | cover | `1.9539912` | **yes** |
| `3.4555` | cover | `1.9999997` | **yes** |
| `3.46` | **no cover** | `2.0037512` | **yes** |
| `3.5` | **no cover** | `2.0372311` | **yes** |

Bisecting the corrected test (50 iterations, 50 digits) gives the threshold
**`3.4555003444044642049`**, and X's `K15-X-C051` value `3.4555003444` agrees to **ten significant
figures**. Two independent methods now agree at every point tested, and an independent worker's
number is reproduced.

**Consequences.**

1. **`C116`'s constant is reinstated, attributed to X:** the two-dodecahedra threshold is
   `3.4555003444044642…` (X `X-C051`, reproduced here), not `6/√5`, and the band is
   `ε < 1.4555003444`. `C126`'s withdrawal is itself withdrawn as a *constant* — the band exists and
   has X's value; what `C126` correctly recorded was that Main's `6/√5` was wrong.
2. **`C124` is safe with room to spare.** It needs one `ε` with `ε > 0.1967` for the inball branch to
   beat `0.754697399337`; the band provides `ε < 1.4555`, i.e. **7.4× more than needed**. `C124`'s
   conclusion stands with `ε = 0.6832816` (or any value in `(0.1967, 1.4555)`).
3. **Theorem D step (4) is certified** by a corrected, sound certificate, and independently by the
   scan. `C112`/`C123`'s *statement* was always right; only their certificates were void.

**What this says about Main's method, recorded because it is the pattern.** The same object produced
two independent errors (a dropped algebraic term, and the direction of a trigonometric inequality),
both of which made the test report success. Neither was caught by Main's own checks; the first was
caught by reconciling X's number, the second by noticing that two of Main's own computations
disagreed. **A certificate that cannot fail is not a certificate** — the value of the twist scan was
precisely that it *could* disagree.

*Status.* `CORRECTION` + `PROVED` (corrected certificate, cross-checked two ways and against X).
`C112`/`C123`/`C127` remain `PENDING_REVIEW`: X's audit is the gate, and review 0608 says so.

### K15-C128 — a ONE-PAIR proof of the two-dodecahedra step (`PROVED`, and much simpler)

With `C127`'s corrected violation sets, the arc cover turns out to be wildly redundant: **a single
pair settles the whole step.** This is the cleanest form of Theorem D's step (4) and should replace
the 65-piece cover as the certificate of record.

**The pair.** With `v`'s eleven at `A` and `w`'s eleven at `Q` (both lists in the order produced by
`build()`/`eleven()`), take `a = A[1]`, `q = Q[8]`, and `d = 2`. Then

```
A = 6.444582472…,   R = 6.4 = 32/5,   c = (4 − A)/R = −(3 − √5)/2 = −0.38196601125…,
h = arccos(c) = 112.4555152…°      ⟹   |T| = 2π − 2h = 135.0889696…° .
```

**The argument, in three lines.** The violation set of this pair is `T = {|t − ψ| > h}`, an arc of
length `135.089°`. The physical twist space is `R/(2π/5)`, i.e. a circle of circumference `72°`,
because rotating one icosahedron by `72°` about its own vertex axis maps it to itself. Since
`|T| > 72°`, **`T` meets every coset of `2π/5`**: for every physical twist `τ` there is a
representative `t ≡ τ` with `t ∈ T`. At that representative the configuration contains the point
`w + R_t q`, at distance `< 2` from `a`. So **every relative twist produces a clash**, and two
adjacent dodecahedral centres are impossible.

**Verified directly, without any covering bookkeeping.** Maximising over physical twists of the best
representative's squared distance:

```
max over τ ∈ [0°, 72°)  of  min over k∈{0..4} d²(τ + 72k°)  =  1.266873708  <  4 .
```

So the one pair is closer than `2` at some representative of *every* physical twist, which is exactly
the claim. This number also matches the earlier all-twist scan's `max over t of min_pq d² =
1.266873708` — as it must, since the scan minimises over all pairs.

**Why this is better than the cover.** The 65-piece cover required `C127`'s mod-period reduction and
a merge test, both of which had already produced two errors. The one-pair argument needs no merge, no
reduction and no interval bookkeeping: one algebraic identity (`R = 32/5`), one comparison
(`h < 4π/5 = 144°`), and the `72°` symmetry. **It is hand-checkable**, which the cover was not.

**Scope.** This proves the step at `d = 2` exactly, which is all Theorem D needs. It says nothing
about `d > 2`; the band constant remains `X-C051`'s `3.4555003444` (`C127`).

*Status.* `PROVED`. `PENDING_REVIEW` with the rest of the pair chain; X is the gate.

### K15-C129 — the two-dodecahedra band in CLOSED FORM, from a single pair (`PROVED`, exact)

`C128` gave a one-pair proof at `d = 2`. It extends to the whole band, in exact arithmetic, and the
band end is a closed form that reproduces X's `3.4555003444` to ten significant figures. **This
supersedes the arc cover entirely**: no covering, no period reduction, no bisection.

**The pair, exactly.** In `v`'s frame take

```
a = ( 2/√5, 0, −4/√5 )      (a contact of v;  |a| = 2 ✓)
q = (−2/√5, 0,  4/√5 )      (a point of w's ring in w's frame;  |q| = 2 ✓)
```

Both lie in the `xz`-plane, so with `w = (d,0,0)` the difference is `u = w − a = (d − 2/√5, 0, 4/√5)`
and, since a rotation about `x` leaves `u_y, u_z` alone,

```
B = 2(u_y q_y + u_z q_z) = 2·(4/√5)(4/√5) = 32/5,     C = 2(u_z q_y − u_y q_z) = 0,
R = √(B² + C²) = 32/5      —  CONSTANT in d  (only u_y,u_z enter, and they do not move).
```

**The band condition.** The violation set is `{|t − ψ| > h}` with `h = arccos((4 − A(d))/R)`, and the
twist period is `2π/5`. So the pair covers every physical twist iff `2π − 2h > 2π/5`, i.e.

```
h < 4π/5   ⟺   (4 − A(d))/R > cos(4π/5) = −(1+√5)/4 .
```

**The quadratic.** With `A(d) = |u|² + |q|² + 2u_x q_x` and `x := d − 2/√5`,

```
A = x² − (4/√5)x + 36/5 ,
x² − (4/√5)x + (8 − 8√5)/5 = 0     ⟹     x = 2/√5 ± 2√((2√5−1)/5) ,
```

so the band is `[2, d_max)` with

> ```
> d_max  =  4/√5 + 2√( (2√5 − 1)/5 )  =  3.4555003444044642048…
> ```

**Checks.**

| quantity | value |
| --- | --- |
| closed form `4/√5 + 2√((2√5−1)/5)` | `3.4555003444044642048` |
| bisection on the corrected arc cover (`C127`) | `3.4555003444044642049` |
| X's `K15-X-C051` | `3.4555003444` |
| agreement | `4×10⁻¹⁵` vs the bisection; **10 significant figures** vs X |

**Why this matters.**

1. **It supersedes a numerically fragile certificate with a two-line exact one.** The arc cover
   required covering, merging, a `2π = 5·(2π/5)` reduction and an inward margin — machinery that had
   already produced **two** errors in this object (`C126`, `C127`). The closed form needs one
   observation (`R = 32/5` is constant in `d`), one trigonometric comparison (`cos(4π/5) =
   −(1+√5)/4`) and one quadratic. **Every step is checkable by hand.**
2. **It confirms an independent worker's constant exactly**, which is the strongest evidence
   available that both are right.
3. **`C124` is fed with more than it needs.** `C124` requires `ε > 0.1967082`; the band supplies
   `ε < 1.4555003444`, a factor of `7.40`.

**Scope.** Proves the two-dodecahedra impossibility for centre separation `d < d_max`, hence
`σ₀(ε) > 2V_dod` for `ε < 1.4555003444` (`C114`), hence `C124` with any such `ε`. It says nothing
beyond `d_max`, and it is **not** a density bound.

**Verified across the whole band, not just at the ends.** For `d` at `0, 10, 25, …, 95, 99.9, 100.1%`
of the way from `2` to `d_max`, the quantity `max over τ of min over shifts k of d²(τ + 72k°)` is

```
1.2669, 1.3495, 1.5529, 1.8517, 2.2458, 2.7352, 3.3199, 3.7627, 3.9952, | 4.0049
                                                                       ↑ d_max
```

— strictly below `4` everywhere up to `99.9%` of the band and strictly above just past `d_max`. So the
closed form is the true crossing for this pair, and its whole range behaves as claimed.

**The pair is optimal among single-pair certificates.** Running the same closed-form band end over
all `121` pairs (`R = 0` pairs — pole–pole, whose distance is constant in the twist — excluded and
checked separately: they never violate at `d = 2`, their constant `d²` being `4.0` or `7.2`):

| | |
| --- | --- |
| non-degenerate pairs whose single-pair band reaches past `d = 2` | `25` |
| pairs attaining the maximum | **`5`**, all with `R = 6.4`: `(a[2],q[7])`, `(a[3],q[7])`, `(a[4],q[10])`, `(a[1],q[10])`, `(a[5],q[10])` |
| the maximum | `3.45550034440446` — **equal to the closed form** |

The five-way tie is the icosahedron's `5`-fold symmetry about the shared vertex axis, which is also
why the twist period is `72°`. So no single pair certifies more than `d_max`, and `C129`'s choice is
one of the `5` optimal ones.

**What is *not* claimed by that.** Optimality *among single-pair certificates* is not optimality of
the union of pairs. Both X's `X-C051` and Main's twist scan put the true threshold at the same
`3.4555003444`, so no union does better — but Main does not prove that here, and does not need it:
`C124` requires only `ε > 0.1967`, which every candidate supplies by a factor of `7.4`.

*Status.* `PROVED` (exact). `PENDING_REVIEW` with the rest of the pair chain; X is the gate, and this
is the cleanest thing for X to check.

### K15-C130 — the `ρ_ε = 0` branch exercised on a real family (`TESTED_FINITE`)

`C124`'s new second branch — the one that removes the contact-density hypothesis — is worth
exercising, since it was unavailable before. `Computation/scaled_case2.py`: scale `fcc` by `t > 1`
so the minimum separation is `2t`. Then no pair lies within `2 + ε` once `2t > 2 + ε`, so
`S_ε = ∅`, `ρ_ε = 0`, and case 2 gives `δ ≤ 1/(1+ε/2)³`.

With `ε = 1.4555003444` (`C129`'s band), `2+ε = 3.4555003444` and the bound is `0.1938907833`:

| `t` | min sep | `ρ_ε` | actual `δ = δ_fcc/t³` | bound | holds |
| --- | --- | --- | --- | --- | --- |
| 1.2 | 2.4 | `> 0` | 0.428519 | case 1 | — |
| 1.5 | 3.0 | `> 0` | 0.219402 | case 1 | — |
| **1.8** | 3.6 | **0** | 0.126969 | 0.193891 | **yes** |
| **2.0** | 4.0 | **0** | 0.092560 | 0.193891 | **yes** |
| **2.5** | 5.0 | **0** | 0.047391 | 0.193891 | **yes** |
| **3.0** | 6.0 | **0** | 0.027425 | 0.193891 | **yes** |

Two things this shows. (i) **The branch is real and non-vacuous** — scaled fcc genuinely has
`ρ_ε = 0` for `t ≥ 1.755`, so before `C124` the pair route had *nothing* to say about these
packings, exactly the gap review 0608 flagged. (ii) **The bound holds there with room**, and the
crossover (`t ≈ 1.76`) is where `δ_fcc/t³` falls below the bound — consistent arithmetic, not a
coincidence: both sides are functions of `t` alone.

**Not claimed.** This exercises the branch; it does not improve any bound (`0.1939 > π/√18 =
0.7405`? no — `0.1939 < 0.7405`, so the branch is *stronger* than Kepler for loose packings, as it
must be, and says nothing about dense ones). It is a consistency check, not a result.

*Status.* `TESTED_FINITE`. Reviewer X.

### K15-C131 — the orientation gap: `C129`'s band is AXIAL only, and `C124` is downgraded (`CORRECTION`)

Review 0653: *"Distinguish an axial two-icosahedron exclusion from the all-orientation statement needed
by a near-contact compactness argument when the second centre is not a face normal."* **Correct, and it
breaks the dependency I claimed.**

**The distinction.**

- **At `d = 2`** the two centres are in contact, so each is a vertex of the other's icosahedron. The
  axis `v→w` is therefore a **vertex direction for both**, and the only freedom is the relative twist
  about it. That is the situation `C128`/`C129` treat, and it is exactly what **Theorem D step (4)**
  needs. **That step stands.**
- **At `d > 2`** the two centres are not in contact, so `w`'s cell can be dodecahedral with `v`
  nowhere among its twelve contacts. `w`'s icosahedron is then free in `SO(3)` — a **3-parameter**
  family, not a 1-parameter twist. `C129`'s band is a statement about the axial sub-family only.

**What that does to `C124`.** Its case-2 branch needs `σ₀(ε) > 2V_dod` for a *single* `ε > 0.1967`,
and `σ₀(ε)` is an infimum over pairs with centre distance in `[2, 2+ε]`. At the minimiser both cells
are dodecahedra at distance `d` with `d` possibly `> 2`, where the orientation is free. So `C124`
requires the **all-orientation** exclusion on `[2, 2.1967]`, which `C129` does not give. **`C124` is
therefore downgraded from `PROVED` to `CONDITIONAL`: it holds if the all-orientation exclusion holds
on `[2, 2.1967]`.**

Nothing else in `C124` changes: the `|S_ε| ≤ (2+2D)|M|` counting, the two-case split and the inball
branch are independent of this.

**Numerical status of the all-orientation exclusion** (`Computation/free_orientation.py`,
`orient_opt.py`). Two independent computations, both *against* the exclusion failing:

1. **Forbidden-cap coverage.** For fixed `a`, the condition `|b − a| ≥ 2` with `|b − w| = 2` forbids a
   cap on `w`'s sphere of angular radius `arccos(|a−w|/4)`. The twelve caps cover only `84%` of the
   sphere at `d = 2`, falling to `53%` at `d = 3` — so coverage alone never excludes a legal placement.
2. **Direct optimisation over `SO(3)`** (60 Nelder–Mead starts each, maximising the minimum
   cross-distance): best values `1.0825` (`d=2`), `1.1986` (`d=2.2`), `1.1623` (`d=3`),
   `1.4387` (`d=4`). **No legal placement (≥ 2) found at any `d ≤ 4`,** with a margin of `≥ 0.80` at
   `d = 2.1967`.

So the evidence is that the exclusion holds *far* beyond what `C124` needs, with a large margin — but
**evidence is not a certificate**, and this is a 4-dimensional claim (`d` times `SO(3)`) that needs an
interval/covering argument. It is submitted as a bounded local job (`LOCAL_COMPUTE_REQUESTS.md`,
`X-ORIENT-001`) rather than asserted.

**A compactness remark that is *not* a substitute.** If no legal placement existed at `d = 2` even
with free orientation, then since `{(d,R) : legal}` is closed in `(d,R)` and `SO(3)` is compact, the
projection onto `d` would be closed, giving an *open* band `[2, 2+ε₀)` — non-explicit `ε₀`. That
argument cannot be made at `d = 2` at all, because at `d = 2` the orientation is *not* free (it is a
single vertex of each icosahedron), so the free-orientation set is empty there by geometry rather than
by clash. **The `d = 2` end is therefore not a limit point of the free-orientation family**, and no
continuity argument is available. This is exactly the review's point.

*Status.* `CORRECTION`. `C129`'s band is `PROVED` **for the axial family only**, and that stays
true; `C124` was `CONDITIONAL` on `X-ORIENT-001` between `C131` and `C133`. **`X-ORIENT-001` is
answered at `C133`** — the all-orientation exclusion is proved, by a covering radius rather than by a
computation, so the condition is discharged and `C124` is `PROVED`. The distinction this entry draws
is unaffected, and the axial scope of `C129` is unaffected.

### K15-C132 — `C124`'s counting repaired: the degree bound, the boundary term, and limsup/liminf (`PROVED`)

Review 0653's audit items 1–3 against `C124`, one repair each. All three were real; none of them
changes `C124`'s conclusion, and the reason is worth stating once: **the counting enters only through
`|S_ε ∩ B_R| = o(|B_R|)`, so every constant in it is irrelevant and only the error term matters.**
The old text's `26` was both wrong and load-bearing-looking, which is worse than wrong.

**(1) `deg ≤ 12` was the wrong bound — the radius is the wrong kind of radius.** `C054`/`C013`'s
kissing-type theorem says *a point with 13 neighbours within distance `R` forces `R > 2.09`*. That is
a **punctual** statement, and at `R = 3.4555` it is simply false (a centre can carry 13 neighbours at
distance 3.4). `C124` cited it for the `(2+ε)`-graph. The correct bound needs **no radius at all**:
neighbours of `v` in `G_{2+ε}` lie in the annulus `2 ≤ |x − v| ≤ 2+ε` and are pairwise `≥ 2` apart, so
their unit balls are disjoint and lie in `1 ≤ |x − v| ≤ 3+ε`:

```
D(ε)  :=  |N_{G_{2+ε}}(v)|  ≤  (3+ε)³ − 1        (D = 63 at ε = 1, D = 87 at ε = 1.4555)
```

The bound is crude — the true count is `12 + O(ε)` — and that is fine: by the sentence above, only
finiteness is used. So the counting constant is `2 + 2D(ε)`, not `26`.

**(2) The boundary term, tracked rather than assumed.** `|N(M) ∩ B_R|` counts neighbours of matched
vertices which may themselves lie outside `B_R`. Correctly,

```
|S_ε ∩ B_R|  ≤  |M ∩ B_R| + D(ε)·|M ∩ B_{R+2+ε}|
             ≤  (1 + D(ε))·|M ∩ B_R|  +  D(ε)·|Λ ∩ {R ≤ |x| ≤ R+2+ε}| .
```

The shell term is `O(R²)`: those points are 2-separated, so their unit balls are disjoint inside
`{R−1 ≤ |x| ≤ R+3+ε}`, giving `≤ (R+3+ε)³ − (R−1)³ = O(R²)`. Hence

```
|S_ε ∩ B_R|  ≤  (1 + D(ε))·|M ∩ B_R|  +  O(R²)  =  o(R³)   whenever |M ∩ B_R| = o(|B_R|).
```

**That `O(R²)` is the whole content of the repair**: it is `o(|B_R|)` because `|B_R|` grows like
`R³` for a 2-separated set, so the boundary cannot carry a positive fraction of the matching.

**(3) limsup/liminf, with no hypothesis that the density exists.** `C124`'s `ρ_ε = 0` branch is
restated so that nothing is assumed about `δ(Λ)` existing. Two facts, both unconditional:

- **Coverage.** Saturation gives every `x` a centre `u` with `|x − u| ≤ 2`, and `x ∈ Ω(v)` forces
  `|x − v| ≤ |x − u|`, so `Ω(v) ⊆ B(v,2)` for every `v`. Therefore
  `Σ_{v ∈ B_R} vol Ω(v) ≥ vol B(0,R) − |Λ ∩ {R ≤ |·| ≤ R+2}|·(32π/3) = (4π/3)R³ − O(R²)`.
- **Branch bound.** `v ∉ S_ε` means every other centre is at distance `> 2+ε`, so
  `Ω(v) ⊇ B(v, 1+ε/2)` and `vol Ω(v) ≥ (4π/3)(1+ε/2)³`; always `vol Ω(v) ≥ 4π/3`.

> **[Second repair, review 2026-11-14 07:38.]** The first version of this paragraph chained
> `(4π/3)R³ − O(R²) ≥ Σ vol Ω(v) ≥ (…)` and concluded `1 ≥ c̄(1+ε/2)³`. **That is invalid**: the
> coverage estimate is a *lower* bound on the sum, and a lower bound on the sum combined with a
> lower bound on its terms bounds nothing. The density bound needs an **upper** bound on the same
> sum, and saturation supplies it. Both bounds are stated below, with their directions.

**Two bounds on the same sum, in the directions they actually have.**

- **Upper (saturation + disjointness + containment).** By the same argument as coverage, `Ω(v) ⊆
  B(v,2)` for every `v`: for `x ∈ Ω(v)` and any centre `u`, `|x−v| ≤ |x−u|`, and saturation gives a
  centre with `|x−u| ≤ 2`. Voronoi cells have disjoint interiors. Hence, for `v ∈ B_R`,
  `Ω(v) ⊆ B(0,R+2)`, and

  ```
  Σ_{v∈B_R} vol Ω(v)  ≤  vol B(0,R+2)  =  (4π/3)(R+2)³ .
  ```

- **Lower (branch bound).** `vol Ω(v) ≥ (4π/3)(1+ε/2)³` for `v ∉ S_ε`, and `≥ 4π/3` for all `v`:

  ```
  Σ_{v∈B_R} vol Ω(v)  ≥  (|B_R| − |S_ε ∩ B_R|)·(4π/3)(1+ε/2)³ .
  ```

- **Lower (coverage), recorded but *not* used here.** `Σ_{v∈B_R} vol Ω(v) ≥ (4π/3)R³ − O(R²)`.
  True, and irrelevant to bounding `c` from above — this is the step the first version got
  backwards.

**Combining the two that point the same way**, with `ε` fixed and `|S_ε ∩ B_R| = o(R³)` from (2):

```
(|B_R| − |S_ε ∩ B_R|)·(1+ε/2)³  ≤  (R+2)³
⟹  (|B_R|/R³)(1+ε/2)³  ≤  ((R+2)/R)³ + (|S_ε ∩ B_R|/R³)(1+ε/2)³ .
```

**The two density cases, audited separately.** Let `R_j → ∞` be a sequence realising
`limsup |B_R|/R³ = c̄`. Then `|B_R| = O(R³)` (2-separation: unit balls are disjoint in `B(0,R+1)`),
so `|S_ε ∩ B_R| = o(|B_R|) = o(R³)` and the last term vanishes along `R_j`; the right-hand side tends
to `1`. Hence `c̄(1+ε/2)³ ≤ 1`. The same inequality along a sequence realising
`liminf |B_R|/R³ = c_` gives `c_(1+ε/2)³ ≤ 1`, since every term is the same except the vanishing
one. So **both** densities obey `δ ≤ 1/(1+ε/2)³`, and no hypothesis that the limit exists is used
anywhere. At `ε = 1`: `1/1.5³ = 0.296296`. (The old text's `0.414086` was the value at
`ε = 0.6832816`, which nothing needs any more.)

**The choice of `ε`, fixed once.** `C124` needs one `ε > 0.1967082337` (`C119`'s crossover). Take

> **`ε = 1`.** Then `2+ε = 3 < 3.1786179` (the orientation-free band of `C133`) **and**
> `< 3.4555` (`C129`'s axial band), so the exclusion holds with a factor `1.45` of room on the
> stronger of the two constants, and the `ρ_ε = 0` branch gives `δ ≤ 0.296296`.

**What changes in `C124`, and what does not.** The statement, the two-case split, the inball branch
and the conclusion `δ < 0.754697399337` are unchanged. What changes: the constant `26` becomes
`2(1+D(ε)) = 128` at `ε = 1` (or `176` at `ε = 1.4555`), the boundary term is `O(R²)` and explicit,
and the density statement is `limsup`/`liminf` rather than a limit. `RESULTS.md` does not move: no
number is produced, because `δ₀(ε)` is still non-explicit (`C108`).

*Status.* `PROVED` (bookkeeping repair; the three defects were in the constants and the quantifier
order, not in the argument). `PENDING_REVIEW` with the rest of the pair chain.

### K15-C133 — the two-dodecahedra exclusion is ORIENTATION-FREE, by a covering radius (`PROVED`, exact)

`C131` recorded the review's objection and downgraded `C124`: at `d > 2` the second cell's
icosahedron of contact directions is free in `SO(3)`, and `C129`'s band is a statement about the
**axial** sub-family. The objection was right, and the gap it names is closed here — **not** by an
interval/covering computation over `d × SO(3)` (`X-ORIENT-001`, no longer needed) but by a covering
radius of the icosahedron and one triangle inequality. **The exclusion never needed orientations to be
constrained; it only needed the contacts of `w` to be close to the direction of `p`.**

> **Theorem.** Let `Λ ⊂ R³` be 2-separated and let `v, w ∈ Λ` have Voronoi cells both congruent to
> the **regular dodecahedron of inradius 1**. Then
>
> ```
> |v − w|  ≥  4 cos ρ_c  =  4√(30√5 + 75)/15  =  3.1786178891670644… ,
> ```
>
> where `ρ_c = arccos √((1 + 2/√5)/3) = 37.3773681…°`. No hypothesis on relative orientation.

**Two ingredients, both elementary.**

**(i) The 12 contacts of a dodecahedral cell are `w + 2u_i` with `u_i` an icosahedron.** A regular
dodecahedron of inradius 1 is circumscribed about the unit ball, so its polar dual is an icosahedron
inscribed in that ball; the 12 face normals *are* that icosahedron's 12 vertices. Each face at
distance 1 from `w` is a bisector plane, so each gives a centre at `w + 2u_i` and these are 12
distinct centres at distance exactly 2 from `w`.

**(ii) The covering radius.** For the 12 unit vectors `u_i`,

```
max over unit n of  min_i ∠(n, u_i)  =  ρ_c ,   cos ρ_c = √((1 + 2/√5)/3) .
```

*Proof.* The spherical Delaunay triangulation of the 12 points is the icosahedron's own face
structure: 20 equilateral spherical triangles with side `a = arccos(1/√5) = 63.4349…°` and corner
angle `72°` (five triangles at each vertex). The spherical Voronoi cells are the pentagons around the
vertices, so the covering radius is the circumradius of a Delaunay triangle, i.e. the distance from a
vertex to a face centre. If `O` is the circumcentre, the three triangles `AOB`, `BOC`, `COA` tile
`ABC`, so their angles at `O` sum to `2π` and each is `2π/3`; hence

```
cos a = cos²ρ_c + sin²ρ_c·cos(2π/3) = (3cos²ρ_c − 1)/2
⟹  cos ρ_c = √((1 + 2cos a)/3) = √((1 + 2/√5)/3) = √(30√5 + 75)/15 = 0.7946544723…  ∎
```

(The maximum is attained at the 20 **face-centre** directions — the dodecahedron's vertex
directions: each Voronoi cell is a convex spherical pentagon and `n ↦ ∠(n,u_i)` is convex on it, so
the max sits at a cell vertex.)

**The argument.** Let `p` be any other centre, `d = |p − w|`, `e = (p − w)/d`. Choose `u_i` with
`∠(e, u_i) ≤ ρ_c`. Then

```
|p − (w + 2u_i)|²  =  d² + 4 − 4d⟨e, u_i⟩  ≤  d² + 4 − 4d cos ρ_c  <  4
                                       whenever   d < 4cos ρ_c = 3.1786179… .
```

So the contact `w + 2u_i` is a centre at distance `< 2` from `p`: a violation of 2-separation.

**The one escape case, and why `C128` covers exactly it — the coincident-centre case, in full.**
The clash inequality is strict whenever `d < 4cos ρ_c`, so a violation is unavoidable **unless the
chosen contact coincides with `p`**: `w + 2u_i = p`. Since that contact lies at distance exactly `2`
from `w`, coincidence forces `d = 2` and `u_i = e`. Two things must then be checked, and both are
short.

*(a) The axis is a face normal of `p`'s cell too.* The midpoint `m = (p+w)/2` has `|m − w| = 1`, and
for every centre `u`, `|m − u|² = |u|² − 2⟨m,u⟩ + 1 ≥ (|u| − 1)² ≥ 1 = |m − w|²`, so `m ∈ Ω(w)`, and
symmetrically `m ∈ Ω(p)`. Hence the bisector plane `{x : |x−w| = |x−p|}` — at distance exactly 1 from
each centre, which is the inradius — supports **both** cells, so it contains a face of each. The axis
`w→p` is therefore a face-normal direction (a vertex direction of the icosahedron) for both cells.

*(b) `C128` excludes that case for every twist.* `C128` proves, at `d = 2` with the axis a vertex
direction of both icosahedra and the relative twist free on the circle `R/(2π/5)`, that some pair of
contacts is closer than `2`; its `d²(t) = A + (32/5)cos t` form has `A` independent of `t`, so the
violation arc has length `2π − 2h = 135.089° > 72°` and meets **every** coset — it covers every
relative twist, not merely sampled ones. `C135` states that certificate self-containedly.

So the escape case is covered by `C128`, and every other case by the inequality. **∎**

**Dependencies, stated as inputs rather than implied.** `C133` uses exactly two external facts:

1. **Polar duality**: a regular dodecahedron of inradius 1 is circumscribed about the unit ball, so
   its 12 face normals are the vertices of an icosahedron inscribed in that ball (`C115`'s equality
   case supplies that the cell *is* the regular dodecahedron).
2. **The axial exclusion at `d = 2`** (`C128`), used only in the coincident case (a) above. `C133`
   does **not** reprove it and does not weaken its scope: `C128` remains `PENDING_REVIEW` in its own
   right, so `C133` inherits that dependency explicitly. If `C128` were wrong, `C133` would still
   exclude every configuration except the coincident one at `d = 2`.

Nothing else is imported: no arc cover (`C116`/`C123`/`C127`), no bisection, no interval arithmetic,
and no orientation constraint.

**The constant, and its sharpness for this method.** `Computation/orient_cover.py` (exact `sympy`
in `Q(√5)` plus a `SO(3)` scan):

| quantity | value | how checked |
| --- | --- | --- |
| `cos ρ_c = √(30√5+75)/15` | `0.7946544722917661` | exact simplification; all 60 face-centre/vertex dots equal it |
| `ρ_c` | `0.6523581398 rad = 37.3773681°` | — |
| `4cos ρ_c` | `3.1786178891670644` | exact |
| sampled covering over 200 000 directions | `min max_i cos = 0.795013` `>` `cos ρ_c` | confirms no direction beats the face centres |
| `SO(3)` scan, `max over rotations of min_i |d e − 2Ru_i|` | `1.275` (`d=2`), `1.350` (`d=2.1967`), `1.491` (`d=2.5`), `1.849` (`d=3.0`) | all `< 2`, i.e. **every** orientation clashes |
| the closed form `√(d²+4−4d cos ρ_c)` | `1.282`, `1.358`, `1.518`, `1.861` | the scan approaches it from below, as it must |
| face-centre alignment at `d = 3.1786 / 3.18 / 3.2` | `1.999986 / 2.001098 / 2.017033` | the bound is **exact**: it clears 2 the moment `d > 4cos ρ_c` |

So the constant is not a lossy estimate of something better available from this argument: aligning `e`
with a face centre puts three contacts at the closed-form distance exactly, and no band beyond
`4cos ρ_c` follows this way. (`C129`'s `3.4555` is *larger*, but only on the axial sub-family.)

**Consequences.**

1. **`σ₀(ε) > 2V_dod` for every fixed `ε < 1.1786178891…`, with no orientation hypothesis.** At a
   minimiser realising `Φ = 2V_dod`, both cells have volume exactly `V_dod`, so by the equality case
   of Hales–McLaughlin (`C115`) both are regular dodecahedra of inradius 1 — at distance `≤ 2+ε`,
   which the Theorem forbids. This is `C114` item 1 **repaired**: its stated band `ε < 0.6832816` is
   inside the new one, so the band, the statement and the use in `C124` all stand; what changes is the
   certificate. `C116`/`C123`/`C127`'s arc cover is no longer on the load-bearing path (it remains
   recorded, and `C129` remains the better constant in its own sub-family).
2. **`C124` returns from `CONDITIONAL` to `PROVED`** — the binding item was `X-ORIENT-001` and it is
   answered here. (Its counting is `C132`.) With `ε = 1`: `2+ε = 3 < 3.1786179` ✓.
3. **`X-ORIENT-001` is withdrawn as a computation request**: it asked for an interval/covering
   certificate over `[2, 2.1967] × SO(3)`; the theorem above is a proof, and a bounded local job is
   the wrong tool for a statement that reduces to `4cos ρ_c > 2.1967`.
4. **Nothing numeric moves.** `δ₀(ε)` is still non-explicit (`G11`), so `C124` gives strictness and
   not a constant, and `RESULTS.md` does not move.
5. **`C131` stays as a correction of the record** — the distinction it draws is right, and the axial
   scope of `C129` is unchanged. What `C131` could not know is that the general case is *easier* than
   the axial one, not harder: freeing the orientation helps the argument, because the clash it
   produces need not be a contact-versus-contact coincidence.

**Attribution and what is not claimed.** The covering radius of the icosahedron is classical (it is
the circumradius of the icosahedral spherical Delaunay triangle; `C128`'s `72°` period and this
`37.377°` are the same symmetry seen twice). Main's contribution is the observation that it settles
the orientation question, and the exact constant `4cos ρ_c` with its sharpness check. **Not claimed:**
novelty in the literature; any improvement to `C129`'s axial constant; any number.

*Status.* `PROVED` (exact; two ingredients, both verified in `orient_cover.py`). **`PENDING_REVIEW`
and not reviewed**: X's independent audit is the gate, and `C124` must not be described as reviewed
until `C132`/`C133`/`C135` pass it. This is the cleanest thing for X to check.

### K15-C134 — `C125`'s monotonicity refutation refuted the wrong statement (`CORRECTION`)

Review 0653, audit item 4: *"`c_F` over **at most** `F` faces is nonincreasing (nested classes). My
[`C125`] refutation used an **exact-`F`** example."* **Correct, and `C125`'s stated reason (b) is
withdrawn.**

**Two different constants, and only one of them is monotone.**

```
c_exact(F)  =  inf{ vol P : P circumscribed about the unit ball, with EXACTLY F faces }
c_{≤F}      =  inf{ vol P : ... with AT MOST F faces }  =  min_{F' ≤ F} c_exact(F') .
```

`c_{≤F}` is an infimum over nested classes, hence **nonincreasing** — a one-line consequence of the
definition, and **no example can refute it**.

**[Third repair, review 2026-11-14 07:38 — a claim of mine withdrawn.]** An earlier version of this
entry wrote "`c_exact` is *not* monotone, and `C125`'s counterexample shows exactly that:
`c_exact(14) > c_exact(20)`", from the truncated octahedron (`F = 14`, `vol = 6.158402871`) and the
icosahedron (`F = 20`, `vol = 5.0540561436`). **That inference is invalid and is withdrawn.** Both
numbers are *volumes of specific polyhedra*, i.e. **upper** bounds on the respective infima:
`c_exact(20) ≤ 5.0541` and `c_exact(14) ≤ 6.1584`. Upper bounds cannot order infima, so **no
monotonicity statement about `c_exact` follows in either direction** — not non-monotone, not
monotone. Candidate volumes do not determine optima, and this entry no longer pretends otherwise.

What is left, stated only as far as it is proved:

- `c_{≤20} ≤ c_{≤14}` — definitional (nested classes).
- `c_{≤20} ≤ 5.0540561436` and `c_{≤14} ≤ 6.158402871` — both are witness values, hence upper bounds.
- A **lower** bound for `c_{≤20}` requires a lower bound for `c_exact(F)` for **every** `F ≤ 20`,
  because `c_{≤20} = min_{F ≤ 20} c_exact(F)`.
- Therefore `C122`'s `≤ 20`-face target is **neither refuted nor supported** by those two polyhedra.

**The branch stays stopped, on reason (a) only**, and that reason is unaffected by any of this: the
circumscribed-volume constants are unproved for `F ∈ {13, 15, 16, 17, 18, 19, 20}`.

**The branch is still stopped, on reason (a) alone, and the reason is now stated exactly.** Fejes Tóth
(*Regular Figures*, p. 263, Thm 2.1) gives the circumscribed-volume constant only for
`F ∈ {4, 5, 6, 8, 10, 12, 14}`, and it depends on `(f, v, e, r, R)`, not on `F` alone, so it does not
label a `c_F`; Mutoh (LNCS **2866**, 2002, 204–214) gives `F = 4..30` as **conjectures**. So seven of
the nine values in `13 ≤ F ≤ 20` are unproved, and `c_{≤20} = min_{F≤20} c_exact(F)` is exactly the
one quantity a `≤ 20`-face target needs. **`C125`'s conclusion stands; its reason (b) does not.**

**Not claimed.** That `c_{≤20}` is *small* — the only exact-`F` values in range are `6.1584` (`F=14`)
and `5.0541` (`F=20`), and both are consistent with a `≤20` target of `4.958`. The branch is stopped
because the constants are **unproved**, not because they are large; if Mutoh's conjectures are ever
certified, the branch becomes available again without any new geometry.

*Status.* `CORRECTION` (twice: the monotonicity argument withdrawn, then my replacement for it
withdrawn too). `C125`'s stop stands on unproved constants alone. Nothing here is a statement about
any optimum.

### K15-C135 — `C128`/`C129` made self-contained: coordinates, the pair, the endpoint (`PROVED`)

Review 0653, audit item 5. `C128`/`C129` are the certificates of record for the two-dodecahedra step,
and both referred to "the order produced by `build()`/`eleven()`" — a property of a Python file, not a
mathematical object. Everything needed is restated here in closed form.

**The frame.** `v = (0,0,0)`, `w = (d,0,0)`, `2 ≤ d`. A dodecahedral cell of inradius 1 with a
face-contact in the direction of `+x` has its 12 contacts at distance exactly 2 at

```
p±  = ( 2, 0, 0) , (−2, 0, 0)                                   poles (p+ is w itself at d = 2)
U_k = ( 2/√5 ,  (4/√5) sin(2πk/5) ,      −(4/√5) cos(2πk/5) )    k = 0..4    "upper ring"
L_k = (−2/√5 ,  (4/√5) sin(2πk/5 + π/5), −(4/√5) cos(2πk/5 + π/5))  k = 0..4 "lower ring"
```

Each has norm `√(4/5 + 16/5) = 2`; the 12 points are an icosahedron of circumradius 2 with a vertex on
the axis (checked in `two_dodecahedra.py`, and exact in `Q(√5)` in `orient_cover.py`). The rings are
staggered by `π/5`, and the whole set is invariant under rotation by `2π/5` about `x` — that is where
`C128`'s `72°` period comes from.

**The pair.** `a = U_0 = (2/√5, 0, −4/√5)` (a contact of `v`) and `q = L_2 = (−2/√5, 0, +4/√5)` (a
contact of `w`, at zero relative twist). Note `q = −a`: **the certificate uses an antipodal pair of the
same icosahedron**, one point on each ring. Everything below holds for any of the five rotations
`U_k, L_{k+2}` (`C129`'s addendum: five-way tie, all with `R = 32/5`).

**The algebra, exactly.** With `x := d − 2/√5`, `u = w − a = (x, 0, 4/√5)`, `q = (−2/√5, 0, 4/√5)`,
and a rotation `R_t` about `x`, `b(t) = w + R_t q`:

```
d²(t) = A(x) + B cos t + C sin t ,
A(x)  = x² − (4/√5)x + 36/5 ,        B = 2(u_y q_y + u_z q_z) = 32/5 ,        C = 2(u_z q_y − u_y q_z) = 0 .
```

`B` is **constant in `d`** because `u_y, u_z` do not move with `d` — that is the whole trick of
`C129`, and `C = 0` is why the sinusoid degenerates to a cosine.

**The certificate.** The violation set is `T = {t : d²(t) < 4} = {t : cos t < (4 − A)/B}`, which is the
arc `{|t − ψ| > h}` centred at `ψ + π` with `h = arccos((4−A)/B)` (this is `C127`'s corrected
orientation; the earlier versions covered the complementary, *safe*, set). Since the physical twist
space is the circle of circumference `2π/5`, `T` meets every coset of `2π/5` **iff** `2π − 2h > 2π/5`,
i.e.

```
h < 4π/5   ⟺   (4 − A)/B > cos(4π/5) = −(1+√5)/4
           ⟺   x² − (4/√5)x + (8 − 8√5)/5 < 0
           ⟺   d < d_max = 4/√5 + 2√((2√5 − 1)/5) = 3.4555003444044642048… .
```

**Endpoint scope, stated exactly.** The inequality is **strict**: for `d < d_max` the violation arc is
*longer* than the period, so it meets every coset and the clash is certified. At `d = d_max` the arc has
length exactly `2π/5` and is *open*, so the coset through its two endpoints meets it in **no** point and
the argument is **inconclusive there** — `d_max` is not proved, and `C129` never needed it to be
(`C124` uses `ε = 1`, i.e. `d ≤ 3`, by `C132`). Above `d_max` the same pair says nothing; that is where
`C133`'s orientation-free bound `3.1786179` takes over in the other direction of usefulness, and the
axial `3.4555` remains the better constant **on the axial sub-family only**.

**Verification status, restated honestly.** `two_dodecahedra.py` is 40-digit `mpmath`, *not* certified;
the `C129` closed form is exact and its agreement with bisection (`4×10⁻¹⁵`) and with X's `X-C051` (10
significant figures) is corroboration, not proof. The proof of record is the algebraic chain above,
which is hand-checkable. `orient_cover.py` re-derives the same 12 points in exact `Q(√5)` and checks
the covering radius used by `C133`.

*Status.* `PROVED` (exact; self-contained as of this entry).

### K15-C136 — audit of E's twelve-face ring-excess proof: premise re-attributed, offset argument verified, one obligation (`AUDITED`)

E's `K15-E099` (`Experimental/REVIEW_0653.md` §7, source `6ae7dbf83`) restores the twelve-face theorem
`(P')` modulo an imported premise. Two things needed review: the premise's provenance, and the
area/offset estimate in step (3). **The argument is sound; its citation is not the best available, and
one step is less complete than it reads.**

**(1) The premise is Fejes Tóth, not Lindelöf — and the project holds the primary source.** E's §7
argues: `D'` is an intersection of twelve half-spaces at distance `≥ 1` from the origin; move each face
in to exactly `1` (volume can only decrease), giving `P ⊆ D'` circumscribed about the unit ball with
*at most* twelve faces; then `vol P ≥ V_dod`, so `vol D' ≥ V_dod`. **The inference is correct.** What
is mis-attributed is the theorem.

- The statement needed is the **at-most-12-face** form with its equality case. Cutting faces in to 1
  can leave a half-space redundant, so `P` may have fewer than twelve facets; a theorem stated for
  *exactly* `n = 12` does not apply without an extra argument.
- That exact statement is **Fejes Tóth's**, and it is already in this project's hands as **Hales–
  McLaughlin, *The Dodecahedral Conjecture*, Theorem 4.1** (PDF p. 16,
  `https://www.cs.cmu.edu/~seanmcl/papers/McLaughlin-Dodec.pdf`), the same PDF `C115` verified with
  `sha256 beab1f4a6c41bfe02c719db3f16cd3a78c9a6666f3fe7b91fe3c72f939ef6960`. It is the source `C115`,
  `C121` and `C004` already use, so no new import is created.
- E's Lindelöf citation (1869, via the survey arXiv:1509.08859 Thm 2.1) is **secondary-sourced** and,
  as E notes, the "regular polyhedron minimises at each `n`" form is **false for `n ≥ 13`**. A theorem
  that is false in the neighbouring case is the wrong tool to lean on for the boundary case `n = 12`;
  the Fejes Tóth form has no such defect. **Correction: Lindelöf drops out of the chain entirely**; it
  may stay as a historical remark, and `K15-E100`'s "secondary source only — the original is not
  verified" caveat is then discharged rather than carried.

**(2) The area/offset estimate (step 3) is correct as calculus**, and I re-derived it independently
with `ρ_r = 8/√(10+2√5) = 2.1029244485` (the ring centre-to-centre distance), `b = ρ_r/2`:

| E's claim | re-derived | |
| --- | --- | --- |
| `5(b−1) = 0.257311121` | `0.257311121` | ✓ |
| `α(2) = arccos(ρ_r/4) = 58.28252559°` | `58.28252559°` | ✓ |
| worst `ρ` is `2` for every `R` | min `t*` over `ρ ∈ [2, 2.603447]` at `ρ = 2`, for `R = 1, 1.02, b` | ✓ |
| worst `R` is `b` | min `t*` over `R ∈ [1, b]` at `R = b` | ✓ |
| `t* = ρ_r/4 = 0.5257311121` | `0.5257311121` | ✓ |
| `π t*² = 0.868314853691` | `0.868314853691` | ✓ |
| `5.550291029 + 0.223427069 = 5.773718098` | `5.773718098 > 5.763417470` | ✓ |

The `d²`-style monotonicity is genuine, not assumed: `α(ρ)` increases with `ρ` more slowly than
`arccos((ρ/2)/√(R²+t²))` does, so the worst case really is the smallest admissible `ρ`.

**(3) The one step that is not complete: the disk must lie inside the face.** Step (3) bounds the
**uncut part of the ring plane**, not of the ring *face*. The face is that plane intersected with the
other half-spaces, so

```
A_ring  ≥  area( uncut disk ∩ face )
```

and `A_ring ≥ π t*²` needs the face to contain a disk of radius `t*` about the face's contact point —
i.e. **the face's inradius must be `≥ ρ_r/4` along the whole path**. Nothing E states proves this, and
it does not follow from the face's *area*: a pentagon of area `1.25` can have inradius well below
`0.5257` if it is elongated. In the `C5` configuration the margin is comfortable — the binding
half-space is the neighbouring ring face, which allows in-plane radius
`b(1 − cos 63.43°)/sin 63.43° = 0.650` against `t* = 0.5257`, a `24%` margin — but **that is an
estimate in one configuration, not a proof along the path**, and it is the concrete obligation to
close. (It should be easy: the same `aφ`-type constraint that fixes the ring angle bounds the face's
inradius from below, and the path's endpoints are the two extremal configurations.)

**(4) What this audit does and does not accept.** The ring-excess lemma itself (§6.1) is correct and
self-contained: `vol P(b) − vol P = (b−1)Σ d_i ∫A_i` is a homothety of face planes with an absolutely
continuous volume, and the finitely many combinatorial-type changes do not affect the integral. With
`D' ≥ V_dod` from Fejes Tóth, `(P')` for the twelve-face class is a theorem **given (3)**. It is not a
universal pair claim, it is not a packing bound, and `RESULTS.md` does not move.

*Status.* `AUDITED`. Premise re-attributed to Fejes Tóth via Hales–McLaughlin Thm 4.1 (primary source
in hand); offset argument verified; face-inradius obligation recorded as the remaining gap. E owns the
repair.

### K15-C137 — C's exact-volume completeness: a derived edge range is not a completeness proof (`OBLIGATION`)

`Computation` `2d6d64051` repairs a real trap: `export()` now derives the edge range from the shell
radius actually used, instead of a constant that could fall below it (`R = 2` gives a graph with no
edges and a degree-zero centre). That repair is correct and the self-test now checks it
(`F(R_SHELL) < CONTACT_R`).

**But it does not make the volume routine complete**, and the difference matters because the fixture's
exactness has been quoted as if it transferred. `central_volume(r)` calls
`FN.evaluate(L, sites, rmax=6)`: the neighbour set is determined by a **fixed** `rmax`. The cell volume
is exact *for the neighbours found*; completeness — that no centre beyond `rmax` contributes a face —
is not established for a generic input. For this fixture the answer is certainly right (the shell is
bounded and the period is `8`, and `diameter < 4.1 < 8 − 3` rules out wrap-around), but that is a
property of *this* fixture, not of `evaluate`.

**Repair specified, not yet done** (it is a local computation, so it goes to Astra as a pinned job, not
run here): replace the hard-coded `rmax` by the **certified truncation** of `C120`/`A15`: a centre `p`
can contribute a face only if `|p − v| ≤ 2 h_Ω(p − v)` (Lemma 3), or equivalently only if its bisector
intersects the current candidate cell. Implemented as an expanding-hull loop — start from the nearest
`k` centres, compute the cell, test every excluded centre against the current cell's support function,
add the failures, repeat — it terminates with a **proof** that the face set is complete, for any input.
The same criterion is what made the dense-fixture computation terminate in `0.3 s` after two earlier
attempts timed out; ignoring it does not merely slow the code down, it makes it non-terminating.

**Standing rule, restated.** The fixed fixture's exact volumes remain **separate evidence**: they
certify that fixture (with its separation checked), and they may not be cited as evidence that
`evaluate` is complete, sound, or exact in general. `K15-C-CUTIMPLIES-003` and §2 of
`Computation/REVIEW_0608.md` are unaffected.

*Status.* `OBLIGATION` (repair specified; owner C; Astra job to be pinned). The fixed fixture stands as
`TESTED_FINITE` evidence for itself only.

### K15-C138 — fallback: what an explicit `δ₀` would need, and why the CE hybrid does not supply it (`TESTED_FINITE` + `OPEN`)

`G11` asks for an explicit `δ₀ > 0` in `σ₀ > 2V_dod`. Two attempts, one partial, one failed. Both are
recorded because the failures are the useful part.

**(1) The reduction, stated exactly.** `δ₀` is explicit iff one has a **quantitative Fejes Tóth**: an
explicit `η ↦ θ(η)` with

```
vol Ω ≤ V_dod(1 + η)   ⟹   Ω is within Hausdorff distance θ(η) of a regular dodecahedron of inradius 1,
```

together with the (explicit) separation `θ ↦ ` the distance at which two `θ`-near-dodecahedra at centre
distance `≤ 2+ε` must clash. The second half is *available*: `C133`'s covering-radius argument is
quantitative — replacing `cos ρ_c` by `cos ρ_c − θ'` costs `O(θ')` in the constant, so a
`θ`-perturbation of the contact directions keeps the exclusion for `d < 3.1786 − O(θ)`. **The first
half is the gap**, and it is not in Hales–McLaughlin: their equality case is qualitative ("congruent to
a dodecahedron"), and neither the paper nor `C115`'s audit gives a modulus.

**(2) The one case where an explicit constant is available, and why it is not enough.** Fix the 12
normals at their icosahedral directions and let the face distances be `1 + e_i`. Then
`vol = V_dod + Σ_i ∫₀^{e_i} A_i(t) dt`, and the ring-excess lemma (`C136` §4) with `A_i ≥ A_min > 0`
gives

```
vol − V_dod  ≥  A_min · max_i (1 − (1+e_i))   for deviations INWARD (e_i < 0),
```

with `A_min ≥ π(ρ_r/4)² = 0.868315` from the uncut-disk bound. So a cell that is thinner than a
dodecahedron in one direction is `0.868·|e|` above `V_dod` **explicitly**. That covers one sign of one
perturbation; a cell can also have volume near `V_dod` with `e_i > 0` in some faces and its *normals*
moved, which is precisely the case the argument does not reach. **Partial, not a solution.**

**(3) The geometric/CE hybrid, compared against the 3D controls — it fails, and the failure is
structural.** The comparison that was asked for, with the numbers the ledger already holds:

| bound | density | vs truth `0.7404805` | vs ML `0.7546974` |
| --- | --- | --- | --- |
| Cohn–Elkies two-point (published) | `0.779747` | `+5.30%` | `+3.32%` |
| Cohn–de Laat–Salmon three-point, general (published) | `0.770271` | `+4.02%` | `+2.06%` |
| project certificate `K33b` | `0.779966` | `+5.33%` | `+3.35%` |
| Hales–McLaughlin (proved) | `0.7546974` | `+1.92%` | — |
| pair route + inball hybrid (`C119`, `C124`) | no number | — | `< 0.7546974` strictly |

The hybrid's *shape* is `δ ≤ max{ (4π/3)/(V_dod + δ₀ρ_ε), 8/d³ }` with `d` the minimal separation.
Every 3D control it is compared against collapses to the same obstruction: the term `δ₀ρ_ε` is
non-explicit (`G11`), so the first branch returns strictness and no constant, and the second branch is
`0.296` at `ε = 1` — far *below* truth, hence vacuous for dense packings. **A geometric/CE hybrid
cannot beat `0.7546974` here without `δ₀`, and with `δ₀` it would beat it only by the amount
`δ₀ρ_ε/(V_dod(V_dod+δ₀ρ_ε))`, which is not evaluable.** This is the same conclusion as `D19` reached
from the other side: the pointwise route is capped at `8/V_dod`, and the pair route is only as strong
as its stability input.

**Not accepted, and restated.** None of this is a packing bound. `RESULTS.md` does not move, `K33b` is
not an improvement on `0.779747`, and `C124` is `PENDING_REVIEW`.

*Status.* `TESTED_FINITE` for the numeric comparison, `OPEN` for the stability estimate. Attempts
recorded: (2) partial with an explicit constant in one direction; (3) failed, with the reason.
