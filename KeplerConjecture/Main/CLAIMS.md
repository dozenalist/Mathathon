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

- **Statement.** Let `f` be admissible in the Cohn–Elkies sense
  (`|f|,|f̂| ≤ C(1+|x|)^{−3−η}`), `f ≢ 0`, `f(x) ≤ 0` for `|x| ≥ 2`, `f̂ ≥ 0`.
  Then every packing with minimum separation 2 satisfies `c(Λ) ≤ f(0)/f̂(0)` and
  `δ(Λ) ≤ (4π/3) f(0)/f̂(0)`.
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

- **Statement (Theorem B).** Let `f` be admissible, `f̂ ≥ 0`, `f(0) > 0`; let
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

## K15-C004 — "relax the sign condition on the contact sphere" is vacuous

- **Statement as submitted.** If `A` has empty interior then (B1)+(B2) force
  `f ≤ 0` on `{|x| ≥ 2}`, so relaxing on the contact sphere buys nothing.
- **Status.** `REFUTED` as stated. **Witness:** `A = Q³ ∩ {|x| ≥ 2}` has empty
  interior but is dense, so `B2` constrains nothing. **Corrected claim
  (K15-C011)** replaces "empty interior" by "closed with empty interior".
- **Why it still matters.** For `A ⊆ {|x| = 2}` (closed, empty interior) the
  conclusion holds and the intended consequence stands: pricing a contact-shell
  relaxation by the kissing number 12 cannot improve any two-point constant.
  This retires a route before it was implemented.
- **Owner** m2 (`smwg019eu`). **Reviewer** X (to confirm the repair).
  **Artifact.** `m2/proof.md` Corollary 2.2.

## K15-C005 — two-point + Voronoi additive score hybrids cannot beat 5.550291

- **Statement.** For every admissible two-point kernel `f` and every `κ > 0`,
  a hybrid of the shape "`vol Ω(v) ≥ V_0 − κ·B_κ(v)`" with `B_κ` built from the
  positive-definite inequality has `V_0 < V_HM = 5.550291028515…`, i.e. gives a
  bound strictly *worse* than Hales–McLaughlin. Two mechanisms:
  (i) at the icosahedral cell `B_κ(ico) ≥ κ f̂(0)/(4√2) > 0` (Poisson at fcc), so
  the correction pushes the required cell volume **up**;
  (ii) averaged over centres, the two-point correction has the *wrong sign*:
  `mean_v B_κ ≤ −κ c f̂(0) < 0` for every periodic packing.
- **Status.** `PROPOSED`; `verify.py` passes (items H1–H4). **main_audit:** the
  fcc Poisson value `f(0)+12f(2) ≥ f̂(0)/(4√2)` is reproduced for five
  admissible `f` in an explicit family; the sign identity (ii) is the standard
  sum-rule slack. I have not yet checked the passage from the per-cell
  inequality to a global bound in a boundary-accounting sense.
- **Reviewer.** X. **Artifact.** `.ultramath/smwg019eu/m1/certificate.json`,
  `m1/verify.py`, `m1/solution.md` (in `m1/work/`).
- **Consequence.** The naive "CE kernel as a correction to Voronoi volume" route
  is closed; DECISIONS D6.

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

## K15-C010 — bandwidth budget for a sharp certificate (independent derivation)

- **Statement.** If `supp f̂ ⊆ B(0,R)` and `f` vanishes at the first `K` shell
  radii of a lattice, then `R ≳ K/(2 r_K)`; for fcc `R ≥ 0.3489, 1.0665, 3.3414,
  10.564` for `K = 10, 10², 10³, 10⁴`. Consequence: no band-limited certificate
  is sharp in `d ≥ 2`.
- **Status.** `PROPOSED` (recovered, `smwfyzz1k` m3 rev. 2, `m4`). Independently
  re-derived twice inside the swarm, not yet reviewed outside it.
- **Reviewer.** X. **Note.** The *qualitative* statement is classical
  (Cohn–Elkies §5; Viazovska's `g` is Schwartz with non-compact support). Do not
  present the budget as new. See also the retraction note in
  `Literature/PRIOR_WORK.md` on contact-shell derivatives.

## K15-C011 — corrected contact-shell relaxation lemma

- **Statement.** In K15-C004 replace "`A` has empty interior" by "`A` is closed
  and has empty interior". Then `{|x| > 2} ∖ A` is dense in `{|x| > 2}`, and with
  `f` continuous and `f ≤ 0` off `A` on `{|x| ≥ 2}` we get `f ≤ 0` on `{|x| ≥ 2}`,
  so K15-C002 applies with the better constant.
- **Status.** `PROPOSED` (repair by Main; trivial proof). **Reviewer.** X.

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

## Obstructed or retired routes (kept deliberately)

| Route | Why retired | Claim |
| --- | --- | --- |
| Any single admissible `f` proving `π/√18` | Li Thm 6.1 | K15-C006 |
| "Allow `f>0` on the contact sphere, priced by 12" | vacuous | K15-C004, C011 |
| Additive two-point correction to Voronoi volume | wrong sign at fcc and on average | K15-C005 |
| Integral tail `∫_{|x|>R} f` as the hybrid price | not a local quantity; needs equidistribution; local route loses a factor 1.3505 | K15-C003, `m2/proof.md` §3.3 |
| Recovering sharpness from ordinary CE at fcc/hcp | fcc is not isodual; equality forces vanishing on a dense set | K15-C010, `smwfyzz1k` m1/m5 (pending review) |
