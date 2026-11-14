# Results — Kepler problem 15

> **Supervisor review, 06:53 Pacific:** C's nonvacuous periodic fixture has
> locally reproduced values and independently checked legality/flow, conditional
> on its volume data; the generic volume algorithm remains under review.
> E's replacement origin-interior helper has a new exact false acceptance and
> its radius mesh lacks a proved error bound. Main C124/C125 retain degree,
> boundary, limit and face-class errors; G13/G14 are not accepted as closed.
> Axial twist repairs do not yet prove the all-orientation near-contact bridge.
> No new best bound or simpler proof is accepted. This scope overrides author
> labels below. See [the review](REVIEW_2026-11-14_0653.md).

> **Supervisor review, 06:08 Pacific:** the named isolated/edgeless flow
> defects are repaired and 69 cases pass locally; generic soundness is unproved.
> E's generic volume enclosure argument fails norm and boundedness checks.
> Main C112's all-twists certificate has a missing constant term, opposite arc
> and invalid endpoint rounding. These certificates are not accepted; their
> underlying geometric statements remain pending. No new best bound or simpler
> proof is established. This scope overrides conflicting author labels. See
> [the review](REVIEW_2026-11-14_0608.md).

> **Supervisor review, 05:23 Pacific:** the generic flow checker at a25f5be
> falsely accepts isolated positive deficits; its acceptance is suspended.
> Main's exact FCC/HCP contact-polytope calculation and X's finite checker
> comparisons pass locally. All eight numerical pilots found no refutation.
> C106-C108 and universal geometric improvements remain pending independent
> review; no new best bound or simpler proof is accepted. This current scope
> overrides conflicting author labels. See [the review](REVIEW_2026-11-14_0523.md).

> **Current supervisor checkpoint, November 14, 03:08 Pacific:** The specific
> X-C014 certificate independently gives density below 0.780718153344. K33b is
> still the stronger checked project control; neither improves known results.
> C081's transfer-floor proof is rejected, and the general sign checker remains
> pending a correctness audit despite passing the named tests. C's explicit
> Gram identities verify only a weak demonstration above density one. No new
> Lean or universal geometric result is accepted. See
> [REVIEW_2026-11-14_0308.md](REVIEW_2026-11-14_0308.md) for current scope.

> **Current supervisor checkpoint, November 14, 02:23 Pacific:** General sign
> checker acceptance remains suspended after a new exact false accept at
> e76a1570 / 201974b. The specific X-C013 rational SOS certificate independently
> verifies a weak bound below 0.794809295672; K33b remains the stronger previously
> checked project control. Neither improves known results. Finite geometric
> tests are inconclusive and CubeDiff is not Lean-verified. See
> [REVIEW_2026-11-14_0223.md](REVIEW_2026-11-14_0223.md) for the current acceptance
> scope; earlier descriptions below do not certify the generic checker.

> **Supervisor checkpoint, November 14, 01:38 Pacific:** Main's generic sign
> checker remains **unsound at revision 9461aae** despite a first repair. X's
> earlier generic checker also had a false accept. The particular K33 files
> passed separate Computation/SymPy checks locally, but general checker acceptance
> and dependent Main-only verdicts are suspended. K15-C029's proof is withdrawn;
> no improved packing bound or simpler Kepler proof is accepted. This
> [independent review](REVIEW_2026-11-14_0138.md) overrides conflicting labels below.

Current state after block `K15-HOUR-20261114-M` (start `2026-11-14T09:14:25Z`).
Only two statuses count here: `VERIFIED_CROSS` (confirmed by two independent
exact implementations) and `PROVED` (a written argument). Everything else lives
in `Main/CLAIMS.md` and is *not* a bound. The sharp theorem is already known
(Hales, formally verified); nothing below reproves it.

## 1. The one checked bound (K15-C023, `VERIFIED_CROSS`)

`Δ(Λ) ≤ 0.779966216777` for every packing of unit balls in `R³`, where the
certificate is Computation's degree-33 rational data
(`out/verified_certificate_K33b.json`, `sha256 525d1d55…`) and the verdict comes
from **two independently written exact checkers**: Computation's `exactcert`
(variable `t = 2π|x|²`) and Main's `shell_check` (variable `u = π|x|²`),
disagreeing on nothing, agreeing on the rational ratio

    p(0)/q(0) = 42935541634304122537361009/230584315533749727927712550.

This is **not** an improvement on Cohn–Elkies 2003 (`0.779747`); it is the first
object in this project whose proof is a finite certificate two independent
programs accept. Reproduce: `python3 KeplerConjecture/Computation/verify_comp_cert.py
<cert.json>` (4 s). The interface that makes it reusable — three conventions, exact
dictionaries, certificate schema — is `Main/INTERFACE.md`; the dictionary is
tested, not asserted (`Computation/interface_xcheck.py`).

## 2. Proved statements that do not depend on computation

1. **Two-point bound for all packings** (K15-C002b): with `f, f̂` continuous, CE
   decay, `f ≤ 0` off `|x| ≥ 2`, `f̂ ≥ 0`, `f̂(0) > 0`, every packing satisfies
   `δ ≤ (4π/3)f(0)/f̂(0)`. The periodic-approximation step has an explicit
   two-loss proof (`O(S/R) + O(1/S)`); its inequality was repaired after review
   (the count of interior tiles must be bounded *above*).
2. **Count-price hybrid** (K15-C003r): if `f > 0` only on a set `A` of contact
   number `n`, with `f ≤ M` there, then `δ ≤ (4π/3)(f(0)+nM)/f̂(0)`. The indexing
   was repaired (fix the base centre `l`, not `j`).
3. **Contact-shell relaxation is vacuous** (K15-C004): if `A` has empty interior,
   a continuous `f ≤ 0` off `A` is `≤ 0` everywhere on `{|x| ≥ 2}`. No
   counterexample exists; Main's earlier "rational points" objection was wrong.
4. **Count on a shell, reduced to one number** (K15-C019): 13 points in
   `2 ≤ |y| ≤ ρ` with pairwise distances `≥ 2` force angular separation
   `≥ arccos(1 − 2/ρ²)`; hence `n(ρ) = 12` exactly, provided the Tammes-13 angle
   is below that threshold (`ρ = 2.05` leaves `1.26°`, `ρ = 2.09` leaves
   `0.034°`). The Tammes input is E's enclosure (K15-C027), which Main re-ran and
   accepts with the scope that the constant's *identification* rests on
   Musin–Tarasov's computer enumeration.
5. **Signed defect estimate** (K15-C029r): with an fcc-compatible negligible `A`,
   `θ·#(D_θ ∩ B(x,r)) ≤ C₁r² + N_A(x,r)`, where `N_A` is the *negative mass* of
   `A` in the ball. Negligibility alone does not bound the defect count — the
   earlier "defect density is zero" claim (K15-C029) is **withdrawn**, its proof
   having assumed `A ≥ 0`. Under that extra hypothesis the statement is true and
   is recorded separately as K15-C029c.
6. **Transfers make negligibility automatic** (K15-C035): if `A` is an
   antisymmetric transfer of range `R` and bound `Φ`, it is negligible with the
   explicit packing-independent constant `C₁ = 3ΦR(R+1)⁵` (factor `R` restored after
   review 0223; the earlier text dropped it). This removes Hales'
   Chapter 5 machinery *if* his correction is recast in transfer form (Main's
   reading, not verified against his text), and leaves only the pointwise
   inequality `Σ_w φ(v,w) ≥ √32 − vol Ω(v)`.
7. **No finite fixture can test that inequality** (K15-C036): cells computed in a
   finite completion are upper bounds for the cells in a packing (monotonicity in
   the point set), so a fixture can refute the required lower bound but never
   confirm it.
6. **Density normalisation** (K15-C024), item by item, including the
   counting-to-volume bridge and the older-convention conversions
   (`c = n/8`, `Δ = (π/6)n`).

## 3. What the two live routes now are, and what each is missing

| Route | State | Missing |
| --- | --- | --- |
| **Cluster/partition (geometric)** — E's criterion, cluster averages instead of pointwise fcc-compatibility | criterion proposed; universal quantifier refuted (a singleton at the icosahedral vertex); repaired to a *specified* partition | a partition rule with a boundary estimate; an analytic cluster-volume lower bound at `D = 2`; an explicit `A` whose negative part satisfies the signed estimate `K15-C029r` |
| **Exact-certificate pipeline (analytic)** — rational data + Sturm verdicts | working end to end at degree 33, cross-verified | nothing structural; its ceiling is obstructed by Li, so it is a control and a component, not the theorem |

**Scope of the negative results (narrowed after review 0138).** The shell
allowance found **no gain in the tested scope** (degree 21, grid 500, `ρ = 2.09`;
and `K15-C028` explains why it is expensive: the cost `12η` scales with the
profile's amplitude on the shell). The two-point certifier saturates at degree 33
in *that* implementation, `+0.03%` above CE03. Neither is an impossibility
theorem, and neither family is "closed": a different proposer, a different
degree, or a different relaxation could behave differently.

## 4. The frontier, in one place

`0.740480` (Kepler, Hales) < `0.754697` (dodecahedral, Hales–McLaughlin) <
`0.770271` (three-point, CDS22) < `0.773055` (Muder) < `0.779636` (Rogers) <
`0.779747` (Cohn–Elkies) < `0.779966` (this project, verified). `0.741506`
(CDS22) is **lattice-only** and is not a general bound. No novelty is claimed for
anything in this file.

## 5. What is not established

- No new numerical bound, no improvement over any published value.
- **The certificate's scope changed this block.** Main's `shell_check` was found
  to accept impossible inputs (review 0138: `u(1−u) ≤ 0` on `[0,1]` and two
  others), which was repaired generally and re-verified (`K15-C049`), and the K33b
  certificate still passes it with the identical ratio. But *general* soundness of
  Main's checker is **suspended until X audits the repaired file**; the K33b
  certificate itself does not depend on that audit, being accepted
  independently by Computation's strict checker and by the SymPy oracle.
- The verified certificate's scope is conditional on both checkers being correct;
  X's independent review of that independence is outstanding.
- Two claims were withdrawn this block (`K15-C029`, and `K15-C014` earlier); both
  withdrawals are recorded with their rejected text.
- No Lean claim beyond an algebraic identity (`centreDensity = 3δ/(4π)`, pinned
  Lean 4.35.0, axioms `[propext, Classical.choice, Quot.sound]`). The ball-volume
  and counting-to-volume identities are **not** formalised (G9).
- The cluster route has no value of `V_0` and no cluster-volume bound.

---

## Review 0438 — status note (no number changes)

**Nothing in this section is a bound.** The analytic record to beat remains Hales–McLaughlin's
`0.754697399337`, and the project's best certificate remains `Δ ≤ 0.779966216777` (not an
improvement on the published `0.779747`).

What changed is *structural*, and it is recorded here so that a reader of this file only is not
misled by `CLAIMS.md`:

1. `K15-C094` (every Barlow cell is `√32`) was **repaired** — its Lemma 1 was circular — and now
   rests on an exact contact-polytope bound independently re-derived by Main (`C104`).
2. The pair route's **global bridge** exists (`C106`): a pair constant `K` gives
   `δ ≤ 8π/(3K)`, so `K = 2V_dod` reproduces `0.754697399337` and `K = 2√32` reproduces
   `π/√18`. Every `K > 2V_dod` is an improvement, and the whole remaining gap is a `1.92%`
   increase in that one constant (`C107`).
3. `(L_δ)` — the pair constant exceeds `2V_dod` by *some* positive amount — is **true** by
   compactness (`C108`) with the twist step now certified for **all** twists (`C112`). It implies
   that **if** `ρ > 0` a saturated packing is strictly below the dodecahedral bound. That is
   **conditional and non-quantitative, and it is not a new packing bound.** (An earlier version of
   this item also claimed the equality case of the dodecahedral density bound is empty; that
   average-to-pointwise inference is invalid and is retracted at `C108`.)
4. Because the constant is not explicit, **none of 2–3 is quoted as a bound**, and per the
   supervisor's standing instruction universal lower-volume claims are `PENDING_REVIEW`.
