# Results — Kepler problem 15

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
   explicit packing-independent constant `C₁ = 3Φ(R+1)⁵`. This removes Hales'
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
