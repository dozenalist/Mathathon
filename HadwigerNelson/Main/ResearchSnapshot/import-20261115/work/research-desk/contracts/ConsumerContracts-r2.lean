/-
  THEOREM-CONTRACT CHECKS for the three consumers whose PROOFS change after the
  strict-state branch deletion, and for the three headline roots.

  UNCOMPILED BY ME. A local serial 27-module three-centre build is running in another
  process; compiling this file is the parent's call, not this block's.

  What each `example` below pins:
    * the ORDER of every binder,
    * the TYPE of every binder and of the conclusion,
    * the PRESENCE/ABSENCE of binders (an added instance argument, or an instance the
      integration turned into an explicit argument, makes the plain name fail to have
      the stated Pi-type) — this is the "auto-inference must not hide added instances" test.

  What it CANNOT pin: implicit/explicit binder FLAGS. Definitional equality ignores binder
  information, so a `{c : ...}` that became `(c : ...)` still type-checks here. Flags are
  therefore checked by printing, with `pp.explicit`, against the expected strings recorded in
  MANIFEST.md. Note in particular that `interfaceStateSupport_no_unit` has `c` IMPLICIT while
  `four_support_sequence_no_unit` and `five_support_no_sixty` have `c` EXPLICIT — the two
  `example`s below are written to that asymmetry, so unifying the two conventions breaks one
  of them.

  Namespaces: the three consumers are in `OAI.EuclideanFiveColor`. Root names are as recorded
  in results/VERIFICATION.md; if a root name resolves differently the last block errors, which
  is itself the signal.
-/
import OAI.Geometry.PlaneColoring.FourContinuity
import OAI.Geometry.PlaneColoring.Interfaces
import OAI.Geometry.PlaneColoring.FiveSupport
import OAI.Geometry.PlaneColoring.Chromatic

/- `autoImplicit false`: a mistyped binder name must be an error, not a silently invented
   free variable. Adopted on the swarm audit's recommendation. -/
set_option autoImplicit false

namespace OAI
open EuclideanFiveColor Filter Topology MeasureTheory

/-! ## 1. `four_support_sequence_no_unit` (FourContinuity.lean:441)
      enclosing `variable (c : ℂ → Fin 5) (hc : Measurable c)` at :413 — both EXPLICIT. -/
example :
    ∀ (c : ℂ → Fin 5) (hc : Measurable c)
      (hw : WeakColoring 5 c) {x : ℕ → ℂ} {y : ℂ}
      (hx : ∀ n, FourCenter c (x n)) (hy : FourCenter c y)
      (hxt : Tendsto x atTop (𝓝 y)) {s : Fin 3} (hs : s ≠ 0)
      {b d : ℕ → ℝ} {b₀ d₀ : ℝ}
      (hb : Tendsto b atTop (𝓝 b₀)) (hd : Tendsto d atTop (𝓝 d₀))
      (hbs : ∀ n, b n ∈ fourSupport c hc (x n) s)
      (hds : ∀ n, d n ∈ fourSupport c hc (x n) s),
      ‖direction (b₀ : Angles) - direction (d₀ : Angles)‖ ≠ 1 :=
  EuclideanFiveColor.four_support_sequence_no_unit

/-! ## 2. `interfaceStateSupport_no_unit` (Interfaces.lean:266)
      enclosing `variable {c : ℂ → Fin 5} (hc : Measurable c)` at :255 — `c` IMPLICIT,
      `hc` EXPLICIT. -/
example :
    ∀ {c : ℂ → Fin 5} (hc : Measurable c)
      (hw : WeakColoring 5 c) {x : ℂ}
      (hg : ∀ᵐ t ∂angularMeasure, fourGroup (fourState c hc x t) ⊆ palette c hc x t)
      {s : Fin 3} (hs : s ≠ 0) {t u : Angles}
      (ht : t ∈ interfaceStateSupport hc x s) (hu : u ∈ interfaceStateSupport hc x s),
      ‖direction t - direction u‖ ≠ 1 :=
  EuclideanFiveColor.interfaceStateSupport_no_unit

/-! ## 3. `five_support_no_sixty` (FiveSupport.lean:138)
      enclosing `variable (c : ℂ → Fin 5) (hc : Measurable c)` at :121 — both EXPLICIT. -/
example :
    ∀ (c : ℂ → Fin 5) (hc : Measurable c)
      (hw : WeakColoring 5 c) {x : ℂ} (hx : FiveCenter c x) {a : ℝ} {i : Fin 5}
      (hi : a ∈ fiveSupport c hc x i), a + sixty ∉ fiveSupport c hc x i :=
  EuclideanFiveColor.five_support_no_sixty

/-! ## 4. Printed signatures, for the flag comparison. The expected text is in MANIFEST.md
      (section "Expected printed signatures"); binder FLAGS are visible only here. -/
set_option pp.explicit true in
#check @EuclideanFiveColor.four_support_sequence_no_unit
set_option pp.explicit true in
#check @EuclideanFiveColor.interfaceStateSupport_no_unit
set_option pp.explicit true in
#check @EuclideanFiveColor.five_support_no_sixty

/-! ## 5. Axiom gates: the three consumers, then the three roots. -/
#print axioms EuclideanFiveColor.four_support_sequence_no_unit
#print axioms EuclideanFiveColor.interfaceStateSupport_no_unit
#print axioms EuclideanFiveColor.five_support_no_sixty

#print axioms EuclideanFiveColor.no_proper_five_coloring
#print axioms Problem160.properColoring_seven
#print axioms Problem160.chromaticNumber_bounds   -- was bare, which does not resolve: the name lives in OAI.Problem160 (Chromatic.lean:22,136)

end OAI
