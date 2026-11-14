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

## K15-C002 — two-point (Cohn–Elkies) bound for all packings, with the periodic approximation proved

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

## K15-C003 — truncated/hybrid two-point bound with a *count* price

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

## K15-C005 — two-point + Voronoi additive hybrids: obstruction WITHDRAWN

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

## K15-C010 — bandwidth budget from finitely many zeros: REFUTED as stated

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

## K15-C014 — a grid-discretised Cohn–Elkies LP does not bound anything (negative result)

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
