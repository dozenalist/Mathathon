# Trust and faithfulness audit of the formal chain (swarm smwfk0ybk, m12, d15)

Object of the audit: the *trust* side of `lean/OAI` — what the machine actually checks — as
opposed to the mathematics (d1-d14) or the paper's hypotheses (d2).

## A. What the development proves, and its exact trust base

| item | result |
|---|---|
| `sorry` / `sorryAx` / `admit` tactic | 0 occurrences (the 3 `admit` hits are English prose in docstrings) |
| `native_decide` | 0 (100 `decide` uses, all kernel-checked) |
| `axiom`, `constant`, `opaque` declarations | none (the 4 `axiom` hits are `Classical.axiomOfChoice` and `#print axioms`) |
| `@[implemented_by]`, `extern`, `unsafe`, `partial` | none |
| imports outside `Mathlib` / `OAI` | none |
| oleans vs sources | all 83 oleans newer than their `.lean` (no stale artifact) |
| axiom set of `no_proper_five_coloring`, `no_proper_five_coloring_algebraic`, `no_measurable_weak_five_coloring`, `proper_to_borel_weak(_algebraic)`, `exists_label_field`, `sample_field`, `properColoring_seven`, `chromaticNumber_bounds` | exactly `[propext, Classical.choice, Quot.sound]` |

Top-level types are the paper's, not a surrogate:

* `EuclideanFiveColor.ProperColoring k c := ∀ x y : ℂ, ‖x-y‖ = 1 → c x ≠ c y`
* `EuclideanFiveColor.no_proper_five_coloring : ¬ ∃ c, ProperColoring 5 c`
  = paper Theorem 1.1 ("no proper five-coloring, even when arbitrary color classes are allowed").
* `Problem160.planeChromaticNumber := sInf {k | ProperColoring k}`, with
  `chromaticNumber_bounds : 6 ≤ chi ∧ chi ≤ 7`.

## B. R6 ("machine-checked under two toolchains") — independently reproduced

The tree as it stands builds under the exact bundle toolchain only. The stock toolchain
(Lean 4.33.1 + `/opt/mathlib`) fails 9 modules unpatched (`scripts/build.log`). With
`.ultramath/smwfcr56i/m8/patches2/all.patch` (38 files) applied to a *copy* of the current
`lean/OAI`, the patch applies cleanly and all modules compile:

    cd .ultramath/smwfcr56i/m8
    PORT_SRC=<m12>/portcheck PORT_LIB=<m12>/portlib PORT_LOG=<m12>/portstatus.json python3 port.py
    -> modules 83 ok 83 bad []   total compile 630 s

and under 4.33.1 the certificate reproduces (`portcheck/Audit3.lean`):
`[propext, Classical.choice, Quot.sound]` for all three roots. R6 holds, modulo the patch.

## C. New: the obstruction predicate is not vacuous

`EuclideanFiveColor.WeakColoring` (`Coloring.lean`) is consumed as a hypothesis by every lemma of
the five-colour obstruction, and refuted at k = 5 by `no_measurable_weak_five_coloring`. Nothing in
the bundle exhibited a model of it, so the obstruction could in principle be vacuously true
(e.g. a wrong `direction` or `angularMeasure`). `Audit2.lean` closes that:

    theorem weakColoring_seven_inhabited :
        ∃ d : ℂ → Fin 7, Measurable d ∧ EuclideanFiveColor.WeakColoring 7 d
    theorem weakColoring_five_empty :
        ¬ ∃ d : ℂ → Fin 5, Measurable d ∧ EuclideanFiveColor.WeakColoring 5 d

Both are axiom-clean, and they elaborate under *both* toolchains (2 s each). The predicate hence
discriminates 5 from 7, and the obstruction is non-vacuous.

## D. Faithfulness: Theorem 1.3 is complete, Theorem 1.4 is not the statement formalised

CORRECTION (made after reading `Converse.lean`): both halves of the paper's Theorem 1.3 *are*
formalised, for the null-set predicate:

    proper_to_borel_weak  : ProperColoring k c -> ∃ d, Measurable d ∧ WeakColoring k d
    properColoring_of_weak: Measurable c -> WeakColoring k c -> ∃ d, ProperColoring k d

The second is `Converse.lean` (`finite_config_proper` = Lemma 4.3's density classes + a translate
argument, then `exists_properColoring_of_finset` = Tychonoff compactness in `ℂ → Fin k`), axiom-clean.
So Theorem 1.3 (the equivalence) is machine-checked for `WeakColoring`. What remains is only the
*vocabulary*: the paper states the equivalence and Theorem 1.4 for Definition 1.2. Details below.

The paper states Definition 1.2 (weak measurable: for every R > 0,
`sum_i ∫_{B(0,R)} ∫_{S¹} 1_{A_i}(x) 1_{A_i}(x+u) dσ(u) dx = 0`), then
Theorem 1.3 (proper k-colouring ⟺ weak measurable k-colouring, every k, ZFC) and
Theorem 1.4 (no weak measurable five-colouring). The development instead uses

    Coloring.WeakColoring k c := AEMeasurable c ∧ ∀ᵐ p ∂(volume.prod angularMeasure), c p.1 ≠ c (p.1 + direction p.2)

i.e. the *null-set form* (the set of monochromatic unit pairs is a product-null set). Consequences:

1. `Basic.WeakMeasurableColoring` (Definition 1.2 verbatim) is only ever *produced*
   (`weakMeasurableColoring_of_aemeasurable_proper`, `weakMeasurableColoring_seven`); no theorem
   consumes it. In particular `¬ WeakMeasurableColoring 5` (Theorem 1.4 as printed) is not stated,
   even though Theorem 1.3 is complete for `WeakColoring`.
2. This does not affect Theorem 1.1: its chain needs only
   proper -> measurable null-set-form -> contradiction, which is complete.

The one missing bridge is `WeakMeasurableColoring k -> ∃ c, Measurable c ∧ WeakColoring k c`:
from `sum_i (volume.restrict (ball 0 R) × circleMeasure){p | c p.1 = c p.2 + 0}`... precisely,
from the Definition-1.2 identity for every R (nonnegative integrand, sum finite) each monochromatic
pair set is null for every R, hence null for `volume.prod circleMeasure` (countable exhaustion of
the plane by balls), i.e. the null-set form; plus a measurable representative of an a.e.-measurable
`c`, and the transport along the isometry `Plane ≅ ℂ` and `circleMeasure ≅ angularMeasure.map direction`.
Every ingredient is standard (`Measure.iUnion_null_iff`, `Measure.restrict_prod`, `AEMeasurable.mk`,
`LinearIsometryEquiv.measurePreserving`, `Measure.map_prod_map`); none is in the bundle. So (D) is
a *statement-level* gap repairable by measure algebra, not a mathematical error, and the paper's own
remark ("unchanged by modifying the coloring on a plane Lebesgue null set") is its content.

## E. The previous run's Lean files, audited (they are outside `lean/OAI` and outside R6)

`Collapse.lean` (m7), `OrbitLemma.lean` (m6), `InterfaceStates.lean` (m5) are not among the 83
modules; the record's claims about them were never covered by a build. Copied to `prev/` and
elaborated here (`prev/`: 2.8 s, 2.2 s, 3.1 s): all compile under Lean 4.33.1 + `/opt/mathlib`,
all `#print axioms` give `[propext, Classical.choice, Quot.sound]`, and a `sorry`/`axiom`/
`native_decide`/`implemented_by`/`opaque` sweep is empty (the hits are `#print axioms` and prose).

Statement check:

* `PaletteCollapse.exists_coloring_of_palette` carries **three** hypotheses, not two:
  (hne) "P0" every unit direction lies in some palette, (htr) "P1" the transfer condition, and
  (hbig) `∀ u : Fin k → ℂ, ∃ s, ‖s‖ = 1 ∧ ∀ i, s ≠ u i ∧ s ≠ -(u i)`. `hbig` is a cardinality
  pinch, discharged for every k by `exists_unit_avoiding`, so the record's "P0 + P1 ⟹ colouring"
  is correct in content but omits it in phrasing.
* `PaletteOrbit.all_ternary_is_alternating` is the combinatorial core of (C4)/(C5): all six
  palettes ternary + adjacent disjoint ⟹ the alternating complementary pattern. Faithful.
* `PaletteCollapse.no_palette_five_of_no_five_coloring` took the five-colouring obstruction as a
  *hypothesis*, and `Collapse.lean` imports only Mathlib, so the record's non-vacuity certificate
  ("the palette axiom system is unsatisfiable at level 5") was not machine-checked unconditionally.

Closed: `CollapseW1.lean` (in this directory) appends the development's
`OAI.EuclideanFiveColor.no_proper_five_coloring` to the collapse body and proves

    theorem no_palette_five_unconditional :
        ¬ ∃ Q : Fin 5 → ℂ → Set ℂ, (P0 Q) ∧ (P1 Q)

axiom-clean under **both** toolchains (2.4 s / 2.8 s). Check:
    source scripts/env4341.sh && lean .ultramath/smwfk0ybk/m12/CollapseW1.lean

## F. Summary of the audit

1. The formal chain behind `6 ≤ chi(R^2)` is trustworthy at the level a machine can be: no
   unproved steps, no nonstandard axioms, no compiler-trust steps, no stale artifacts, faithful
   top-level types, and it reproduces under two independent toolchain+library pairs.
2. The one load-bearing predicate that had no exhibited model (`WeakColoring`) is now proved
   inhabited at k = 7 and empty at k = 5, so the obstruction is non-vacuous.
3. Two faithfulness gaps remain, neither affecting Theorem 1.1: (i) the paper's Theorems 1.3/1.4
   are formalised only in the null-set vocabulary and only in the forward direction of 1.3 —
   the vocabulary bridge is a measure-transport exercise, not new mathematics; (ii) the level-5
   non-vacuity statement needed (and now has) an unconditional Lean form.

## G. The record's own headline claims, re-verified (all axiom-clean)

| claim | Lean declaration | axioms |
|---|---|---|
| paper Thm 1.1 | `EuclideanFiveColor.no_proper_five_coloring` | three standard |
| paper Thm 1.3, both directions (null-set form) | `proper_iff_weak : (∃ c, ProperColoring k c) ↔ ∃ c, Measurable c ∧ WeakColoring k c` | three standard |
| forward half | `proper_to_borel_weak`, `proper_to_borel_weak_algebraic` | three standard |
| reverse half | `properColoring_of_weak` (+ `finite_config_proper`, `exists_properColoring_of_finset`) | three standard |
| paper Thm 1.4 (null-set form) | `no_measurable_weak_five_coloring` | three standard |
| T1 `chi(E) = chi(C)` | `algebraic_colorable_iff` | three standard |
| T2 null-set robustness | `not_proper_five_coloring_compl_null` | three standard |
| R3 connected+unit-free ⟹ diam ≤ 1 | `diam_le_one_of_preconnected_unitFree` | three standard |
| `6 ≤ chi ≤ 7` | `chromaticNumber_bounds` | three standard |
| `Chi.lean`'s seven-colouring | `properColoring_seven`, `exists_measurable_proper_seven` | three standard |

Note: `proper_iff_weak` makes the two halves of Theorem 1.3 a single statement, so the earlier
finding recorded above ("only the forward half") is superseded — corrected in section D.

## H. This run's own Lean deliverables, audited from fresh copies

Copied into `swarm/`, built with `lean -o` under Lean 4.33.1, axioms printed:

* `m2/Indep.lean` — `PaletteIndep.card_ternary_le_three(_union_form)`, axiom-clean.
* `m6/TightCore.lean` — `TightCSP.tight_of_plain`, `TightCSP.sat_tight_iff_sat_plain`, axiom-clean.
  This is the strong negative answer to Step 1 (the (C4)/(C5) tightening is inert for every k ≥ 5).
* `m10/work/Shrink.lean` — builds (the coordinatewise shrinking step).
* `m11/work/Core.lean` — `SwarmM11.no_four_points` (no four points in a Euclidean space of
  dimension ≤ 2 are pairwise at distance r > 0) and `no_measure_fixed_difference_norm`,
  axiom-clean. Both are true and correctly stated.
* `m16/M5Interface.lean`, `m16/PaletteShrink.lean`, `m16/Tightened.lean` —
  `InterfaceStates.tightened_silent_at_six`, axiom-clean.
* `tight/TightenedSAT.lean` (mine) — `tightened_sat_k6_ell3`, `tightened_sat_k6_ell4`: at k = 6, for
  every sign matrix and ell = 3,4, a model of (C1)-(C5) exists. Independent of m6's shrinking
  theorem; the witness is m5's own `altPal` outsider singletons, and (C4),(C5) are checked as
  predicates (`C4`: no two palettes cover `Fin 6`; `C5`: at most three ternary).

All twelve files are free of `sorry`/`native_decide`/`axiom` and print only the three standard
axioms. No defect found anywhere in the swarm's formal output.

## I. Verdict

* Defects in the chi ≥ 6 chain: none found.
* Defects in the swarm's own machine-checked output: none found.
* Faithfulness corrections to the record: three (hbig omitted in the collapse's phrasing; the
  level-5 non-vacuity theorem was conditional — now unconditional in `CollapseW1.lean`; module
  count 83 not 78), and one gap: paper Theorem 1.4 in Definition-1.2 vocabulary.
* New: obstruction predicate non-vacuity (k = 7 inhabited, k = 5 empty); an independent
  machine-checked witness that the tightened k = 6 CSP is satisfiable.

## J. The weak predicate's threshold (Audit6.lean, axiom-clean under both toolchains)

The bundle proves monotonicity in the number of colours for `ProperColoring` (`properColoring_mono`)
but **not** for `EuclideanFiveColor.WeakColoring`, so "no measurable weak 5-colouring" did not by
itself exclude `k ≤ 5`. Supplied here:

    weakColoring_mono : k ≤ m -> Measurable c -> WeakColoring k c -> ∃ d, Measurable d ∧ WeakColoring m d
    weakChromaticNumber := sInf {k | ∃ c : ℂ → Fin k, Measurable c ∧ WeakColoring k c}
    weakChromaticNumber_bounds : 6 ≤ weakChromaticNumber ∧ weakChromaticNumber ≤ 7
    no_weak_of_le_five (k) (hk : k ≤ 5) : ¬ ∃ c : ℂ → Fin k, Measurable c ∧ WeakColoring k c

So the measurable weak chromatic number of the plane (null-set predicate) is 6 or 7, exactly the
range of `chi(R^2)`: the measurability removal does not move the threshold. Together with section C
(k = 5 empty, k = 7 inhabited) the predicate's threshold is pinned to {6,7}, which is the precise
sense in which the obstruction is non-vacuous.
