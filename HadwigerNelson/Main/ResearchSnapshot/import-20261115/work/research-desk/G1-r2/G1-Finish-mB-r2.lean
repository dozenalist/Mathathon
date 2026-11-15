/-
  A6 palette producer -- swarm smwgwui56, lane B (member m2).

  FINISHES gap G1 of the accepted bridge
  `supervisor/simplify-lean/swarm-smwguinbz/A6-Bridge-m2.lean` -- the A6 sign
  table `SignTable`.

  This file is `G1-Sign-m2.lean` (swarm smwgviqtr, 257 lines) brought to a
  closing form.  Contents, in order:

    §0  an extra import that G1-Sign-m2.lean was missing (see NOTES-mB.md §3).
    §1  `cos_sign_strict`  -- G1b1, the strict cosine sign table.  Unchanged.
    §2  the `direction` / angle interface.  Unchanged.
    §3  the label geometry of the A6 pairing.  Unchanged.
    §4  `sign_of_paired`, `sign_of_paired_fin` -- G1b2.  Unchanged.
    §5  verbatim local copies of the bridge's `arc`, `pos`, `neg`, `SignTable`.
    §6  *** B1 ***  `posT_char` / `negT_char`:  by `decide` over `Fin 6 x Fin 6`,
        the residue rule *is* the bridge's table.  Plus `negT_char_alt`, a
        `decide`-free proof of the same statement, as a fallback.
    §7  *** the closing lemma ***  `signTableT_of_paired` /
        `signTableT_of_paired_fin` : `SignTableT v` from the pairing hypothesis.
        This is what discharges the bridge's `SignTable` *hypothesis*.

  NAMING.  `posT`, `negT`, `arcT`, `SignTableT` are the bridge's `pos`, `neg`,
  `arc`, `SignTable` with their bodies copied character for character.  They are
  local only because `A6-Bridge-m2.lean` has a hyphen in its file name and so
  cannot be `import`ed.  Each of the four is *definitionally equal* to the
  bridge's, so pasting this file's §6/§7 into the bridge is a pure renaming
  `posT -> pos`, `negT -> neg`, `arcT -> arc`, `SignTableT -> SignTable`; the
  paste-ready forms with the bridge's own names are in §7's closing comment and
  in NOTES-mB.md §5.

  STATUS: **NOT COMPILED**.  No `lean`, no `lake`, no build of any kind was run;
  the task forbids it.  Every Mathlib name used below is audited name by name in
  NOTES-mB.md §2 against the pinned checkout
  `.scratch/mathlib4/Mathlib` (Lean 4.34.1), with file:line.  Every
  elaboration claim is a hand check against a call site that already compiles in
  this repository or in that Mathlib, quoted with file:line in NOTES-mB.md.

  No `sorry`, no `admit`, no `native_decide`, no `axiom`, no new assumption.
-/

import OAI.Geometry.PlaneColoring.AngularBoundary
import OAI.Geometry.PlaneColoring.PaletteTransport
-- §0. ADDED relative to G1-Sign-m2.lean -------------------------------------
-- `inner_coe_coe` (§2) uses `OAI.EuclideanFiveColor.direction_inner_real`,
-- which lives in `lean/OAI/Geometry/PlaneColoring/Interfaces.lean:198`.
-- `Interfaces` is NOT in the import closure of either of the two imports
-- above (it *imports* `AngularBoundary`, so adding it is monotone and acyclic).
-- Without this line `direction_inner_real` is an unknown identifier.
-- NOTES-mB.md §3 records the check and §6 the import-free fallback.
import OAI.Geometry.PlaneColoring.Interfaces

namespace OAI

noncomputable section
open Set Filter Topology
open scoped RealInnerProductSpace
namespace EuclideanFiveColor
namespace A6

/-! ## 0.  The residue bookkeeping

`{0,1,5}` and `{2,3,4}` are complementary among the residues mod 6; that is all
the negative side needs, and it is used only by the fallback `negT_char_alt`.
`aspect` of `decide` here: `interval_cases h : m % 6` generalises the expression
`m % 6` (Mathlib/Tactic/IntervalCases.lean:382 `generalizeHyp`), so after the
case split the goal really does contain the literal `0, ..., 5` and `decide`
is evaluating a closed `Nat` proposition. -/

lemma mod6_not_mem (m : ℕ) :
    ((m % 6 ∈ ({2, 3, 4} : Finset ℕ)) ↔ ¬ (m % 6 ∈ ({0, 1, 5} : Finset ℕ))) := by
  have hm6 : m % 6 < 6 := Nat.mod_lt m (by norm_num)
  interval_cases h : m % 6 <;> decide

/-! ## 1.  G1b1: the strict cosine sign lemma -/

/-- **The strict sign table of `cos` at the six multiples of `pi/3`.**

For `|s| < pi/6` the six cosines `cos (s + m * pi/3)` have the sign of the residue
`m % 6`: positive for `0, 1, 5` and negative for `2, 3, 4`.  Both sides are strict
(no zero case is reachable): the margin `pi/6` keeps every shifted argument off
the zeros `pi/2 + k pi` of `cos`. -/
lemma cos_sign_strict (s : ℝ) (m : ℕ) (hs : |s| < Real.pi / 6) :
    (0 < Real.cos (s + m * (Real.pi / 3)) ↔ (m % 6 ∈ ({0, 1, 5} : Finset ℕ))) ∧
    (Real.cos (s + m * (Real.pi / 3)) < 0 ↔ (m % 6 ∈ ({2, 3, 4} : Finset ℕ))) := by
  have hpi : 0 < Real.pi := Real.pi_pos
  have hs1 : -(Real.pi / 6) < s := (abs_lt.mp hs).1
  have hs2 : s < Real.pi / 6 := (abs_lt.mp hs).2
  -- (i) reduce `m` modulo 6:  `m * (pi/3) = (m % 6) * (pi/3) + (m / 6) * (2 * pi)`
  have hper : Real.cos (s + (m : ℝ) * (Real.pi / 3))
      = Real.cos (s + ((m % 6 : ℕ) : ℝ) * (Real.pi / 3)) := by
    have hdecomp : (m : ℝ) = ((m % 6 : ℕ) : ℝ) + ((m / 6 : ℕ) : ℝ) * 6 := by
      have h0 : ((m % 6 + 6 * (m / 6) : ℕ) : ℝ) = (m : ℝ) := by
        rw [Nat.mod_add_div]
      rw [← h0] <;> push_cast <;> ring
    have harg : s + (m : ℝ) * (Real.pi / 3)
        = (s + ((m % 6 : ℕ) : ℝ) * (Real.pi / 3))
          + ((m / 6 : ℕ) : ℝ) * (2 * Real.pi) := by
      rw [hdecomp]
      ring
    rw [harg, Real.cos_add_nat_mul_two_pi]
  rw [hper]
  -- (ii) the six residues, one interval computation each
  have hm6 : m % 6 < 6 := Nat.mod_lt m (by norm_num)
  interval_cases h : m % 6
  · -- residue 0 :  s in (-pi/2, pi/2)
    have hp : 0 < Real.cos (s + ((0 : ℕ) : ℝ) * (Real.pi / 3)) := by
      simpa using (Real.cos_pos_of_mem_Ioo (x := s) ⟨by linarith, by linarith⟩)
    exact ⟨iff_of_true hp (by decide), iff_of_false (not_lt.mpr hp.le) (by decide)⟩
  · -- residue 1 :  s + pi/3 in (pi/6, pi/2)
    have hp : 0 < Real.cos (s + ((1 : ℕ) : ℝ) * (Real.pi / 3)) := by
      simpa using
        (Real.cos_pos_of_mem_Ioo (x := s + Real.pi / 3) ⟨by linarith, by linarith⟩)
    exact ⟨iff_of_true hp (by decide), iff_of_false (not_lt.mpr hp.le) (by decide)⟩
  · -- residue 2 :  s + 2 pi/3 in (pi/2, 5 pi/6)
    have hn : Real.cos (s + ((2 : ℕ) : ℝ) * (Real.pi / 3)) < 0 := by
      simpa using
        (Real.cos_neg_of_pi_div_two_lt_of_lt (x := s + 2 * (Real.pi / 3))
          (by linarith) (by linarith))
    exact ⟨iff_of_false (not_lt.mpr hn.le) (by decide), iff_of_true hn (by decide)⟩
  · -- residue 3 :  s + pi in (5 pi/6, 7 pi/6)
    have hn : Real.cos (s + ((3 : ℕ) : ℝ) * (Real.pi / 3)) < 0 := by
      simpa using
        (Real.cos_neg_of_pi_div_two_lt_of_lt (x := s + 3 * (Real.pi / 3))
          (by linarith) (by linarith))
    exact ⟨iff_of_false (not_lt.mpr hn.le) (by decide), iff_of_true hn (by decide)⟩
  · -- residue 4 :  s + 4 pi/3 in (7 pi/6, 3 pi/2)
    have hn : Real.cos (s + ((4 : ℕ) : ℝ) * (Real.pi / 3)) < 0 := by
      simpa using
        (Real.cos_neg_of_pi_div_two_lt_of_lt (x := s + 4 * (Real.pi / 3))
          (by linarith) (by linarith))
    exact ⟨iff_of_false (not_lt.mpr hn.le) (by decide), iff_of_true hn (by decide)⟩
  · -- residue 5 :  shift by -2 pi  first,  then s - pi/3 in (-pi/2, -pi/6)
    have hp : 0 < Real.cos (s + ((5 : ℕ) : ℝ) * (Real.pi / 3)) := by
      have harg : s + ((5 : ℕ) : ℝ) * (Real.pi / 3)
          = (s - Real.pi / 3) + 2 * Real.pi := by
        push_cast
        ring
      rw [harg, Real.cos_add_two_pi]
      exact Real.cos_pos_of_mem_Ioo ⟨by linarith, by linarith⟩
    exact ⟨iff_of_true hp (by decide), iff_of_false (not_lt.mpr hp.le) (by decide)⟩

/-! ## 2.  The `direction` / angle interface

`direction (t : Angles) = Circle.exp t` as a complex unit, so `direction (x : Angles)`
for a real `x` is the unit vector `(cos x, sin x)`; the repository's own
`direction_inner_real` (`Interfaces.lean:198`, hence the §0 import) is the inner
product with it. -/

lemma direction_re_coe (x : ℝ) : (direction ((x : ℝ) : Angles)).re = Real.cos x := by
  rw [direction_real, Circle.coe_exp, Complex.exp_ofReal_mul_I_re]

lemma direction_im_coe (x : ℝ) : (direction ((x : ℝ) : Angles)).im = Real.sin x := by
  rw [direction_real, Circle.coe_exp, Complex.exp_ofReal_mul_I_im]

/-- Inner product of two unit directions: `cos` of the difference of the angles. -/
lemma inner_coe_coe (a b : ℝ) :
    ⟪direction ((a : ℝ) : Angles), direction ((b : ℝ) : Angles)⟫ = Real.cos (a - b) := by
  rw [direction_inner_real a, direction_re_coe b, direction_im_coe b, Real.cos_sub]

/-- `sixAngle j` is the real angle `j * pi/3`. -/
lemma sixAngle_coe (j : Fin 6) :
    sixAngle j = (((j.val : ℝ) * (Real.pi / 3) : ℝ) : Angles) := by
  have hsix : sixAngle j = j.val • (sixty : Angles) := rfl
  have hns : j.val • sixty = (j.val : ℝ) * (Real.pi / 3) := by
    simp only [nsmul_eq_mul, sixty]
  rw [hsix, ← AddCircle.coe_nsmul, hns]

/-- The real representative of `(s : Angles) + sixAngle j`. -/
lemma add_sixAngle_coe (s : ℝ) (j : Fin 6) :
    (s : Angles) + sixAngle j = ((s + (j.val : ℝ) * (Real.pi / 3) : ℝ) : Angles) := by
  rw [sixAngle_coe j, ← AddCircle.coe_add]

/-- The inner product at phase `j` against the unit direction of phase `k`. -/
lemma inner_sixAngle (s : ℝ) (j k : Fin 6) :
    ⟪direction ((s : Angles) + sixAngle j), direction (sixAngle k)⟫
      = Real.cos (s + ((j.val : ℝ) - (k.val : ℝ)) * (Real.pi / 3)) := by
  rw [add_sixAngle_coe s j, sixAngle_coe k, inner_coe_coe]
  congr 1
  ring

/-! ## 3.  The label geometry of A6

Label `i : Fin 6` of a paired six-tuple carries the direction of phase
`2 * (i.val / 2)`: `i = 0,1` give phase `0`, `i = 2,3` phase `2`, `i = 4,5`
phase `4`. -/

lemma two_mul_div_two_le_add_six (i j : Fin 6) : 2 * (i.val / 2) ≤ j.val + 6 := by
  have hi : i.val < 6 := i.isLt
  have h1 : 2 * (i.val / 2) ≤ i.val := by
    rw [Nat.mul_comm]
    exact Nat.div_mul_le_self i.val 2
  exact Nat.le_trans h1 (Nat.le_trans (Nat.le_of_lt hi) (Nat.le_add_left 6 j.val))

lemma two_mul_div_two_lt_six (i : Fin 6) : 2 * (i.val / 2) < 6 := by
  have h1 : 2 * (i.val / 2) ≤ i.val := by
    rw [Nat.mul_comm]
    exact Nat.div_mul_le_self i.val 2
  exact lt_of_le_of_lt h1 i.isLt

/-! ## 4.  G1b2: the sign of the inner product at phase `j`

The residue is written exactly as in the bridge's `pos_char`,
`(j.val + 6 - 2 * (i.val / 2)) % 6`:  shifting `j.val` by `+6` costs a full turn
`2 * pi`, which `cos` does not see, and lets the natural-number subtraction
`j.val + 6 - 2 * (i.val / 2)` stay in `NN`. -/

theorem sign_of_paired (v : Fin 6 → ℂ) (k : Fin 6 → Fin 6)
    (hk : ∀ i : Fin 6, (k i).val = 2 * (i.val / 2))
    (hv : ∀ i : Fin 6, v i = direction (sixAngle (k i)))
    (j : Fin 6) (s : ℝ) (hs : |s| < Real.pi / 6) (i : Fin 6) :
    (0 < ⟪direction ((s : Angles) + sixAngle j), v i⟫ ↔
        (j.val + 6 - 2 * (i.val / 2)) % 6 ∈ ({0, 1, 5} : Finset ℕ)) ∧
      (⟪direction ((s : Angles) + sixAngle j), v i⟫ < 0 ↔
        (j.val + 6 - 2 * (i.val / 2)) % 6 ∈ ({2, 3, 4} : Finset ℕ)) := by
  have hle : 2 * (i.val / 2) ≤ j.val + 6 := two_mul_div_two_le_add_six i j
  have hcast : ((j.val + 6 - 2 * (i.val / 2) : ℕ) : ℝ)
      = (j.val : ℝ) + 6 - ((2 * (i.val / 2) : ℕ) : ℝ) := by
    rw [Nat.cast_sub hle] <;> push_cast <;> ring
  have hinner : ⟪direction ((s : Angles) + sixAngle j), v i⟫
      = Real.cos (s + ((j.val + 6 - 2 * (i.val / 2) : ℕ) : ℝ) * (Real.pi / 3)) := by
    have hred : ⟪direction ((s : Angles) + sixAngle j), v i⟫
        = Real.cos (s + ((j.val : ℝ) - ((2 * (i.val / 2) : ℕ) : ℝ)) * (Real.pi / 3)) := by
      rw [hv i, inner_sixAngle, hk i]
    rw [hred]
    have harg : s + ((j.val + 6 - 2 * (i.val / 2) : ℕ) : ℝ) * (Real.pi / 3)
        = (s + ((j.val : ℝ) - ((2 * (i.val / 2) : ℕ) : ℝ)) * (Real.pi / 3))
          + 2 * Real.pi := by
      rw [hcast]
      ring
    rw [harg, Real.cos_add_two_pi]
  rw [hinner]
  exact cos_sign_strict s (j.val + 6 - 2 * (i.val / 2)) hs

/-- G1b2 with the task's literal hypothesis shape: the paired six-tuple
`v i = direction (sixAngle <.2 * (i.val / 2), _>.)`. -/
theorem sign_of_paired_fin (v : Fin 6 → ℂ)
    (hv : ∀ i : Fin 6,
      v i = direction (sixAngle ⟨2 * (i.val / 2), two_mul_div_two_lt_six i⟩))
    (j : Fin 6) (s : ℝ) (hs : |s| < Real.pi / 6) (i : Fin 6) :
    (0 < ⟪direction ((s : Angles) + sixAngle j), v i⟫ ↔
        (j.val + 6 - 2 * (i.val / 2)) % 6 ∈ ({0, 1, 5} : Finset ℕ)) ∧
      (⟪direction ((s : Angles) + sixAngle j), v i⟫ < 0 ↔
        (j.val + 6 - 2 * (i.val / 2)) % 6 ∈ ({2, 3, 4} : Finset ℕ)) :=
  sign_of_paired v (fun i => ⟨2 * (i.val / 2), two_mul_div_two_lt_six i⟩)
    (fun _ => rfl) hv j s hs i

/-! ## 5.  Local verbatim copies of the bridge's four definitions

Bodies copied character for character from
`supervisor/simplify-lean/swarm-smwguinbz/A6-Bridge-m2.lean` sections 2 and 5.
Because the bodies are identical, `posT = pos`, `negT = neg`, `arcT = arc` and
`SignTableT = SignTable` all hold by `rfl` once the two files are in one
namespace -- i.e. the paste into the bridge is a pure renaming. -/

/-- The open fundamental arc `(-pi/6, pi/6)` inside `Angles = AddCircle (2*pi)`.
Copy of the bridge's `arc`. -/
def arcT : Set Angles := {t | ∃ s : ℝ, |s| < Real.pi / 6 ∧ (s : Angles) = t}

/-- Labels with positive inner product at phase `j`.  Copy of the bridge's `pos`. -/
def posT : Fin 6 → Finset (Fin 6) :=
  fun j => if j = 0 then {0, 1} else if j = 1 then {0, 1, 2, 3} else
    if j = 2 then {2, 3} else if j = 3 then {2, 3, 4, 5} else
    if j = 4 then {4, 5} else {0, 1, 4, 5}

/-- Labels with negative inner product at phase `j` (complement of `posT j`).
Copy of the bridge's `neg`. -/
def negT (j : Fin 6) : Finset (Fin 6) := Finset.univ \ posT j

/-- The A6 sign table on the fundamental arc.  Copy of the bridge's `SignTable`. -/
def SignTableT (v : Fin 6 → ℂ) : Prop :=
  ∀ (j : Fin 6) (t : Angles), t ∈ arcT →
    (∀ i : Fin 6, (0 < ⟪direction (t + sixAngle j), v i⟫) ↔ i ∈ posT j) ∧
    (∀ i : Fin 6, (⟪direction (t + sixAngle j), v i⟫ < 0) ↔ i ∈ negT j)

/-! ## 6.  B1: the residue rule *is* the bridge's table

Both proofs are a single `decide` over `Fin 6 x Fin 6`: the quantifier is inside
the proposition (`∀ (j i : Fin 6), ...`, the bridge's own `pos_char` shape), so
after typeclass search `decide` sees a closed 36-case `Finset`/`Nat` computation,
and every ingredient (`posT`, `Finset.univ \ ·`, `%`, `Finset` membership) is
computable.  This is the same `decide` the bridge itself already uses for
`pos_char`, `resOut_spec`, `resIn_spec`, `g_eq`; see NOTES-mB.md §4 for the check
that `decide` can reduce `Finset.univ : Finset (Fin 6)`, and for why the
quantifier must be inside the proposition rather than a binder.

Note the orientation: residue first, table second -- exactly the shape the sign
table is consumed in (`sign_of_paired`'s residue gives *the* table member, so
one `Iff.trans` per side closes `SignTable`). -/

/-- **B1, positive side.**  At phase `j`, the residue rule of the six paired
directions names exactly the bridge's `pos j`.

The `∀` is *inside* the proposition, not in the binder, because `decide` has to
see a closed statement: with `posT` applied to a free variable `j` nothing
reduces.  This is the same shape as the bridge's own `pos_char`. -/
lemma posT_char : ∀ (j i : Fin 6),
    ((j.val + 6 - 2 * (i.val / 2)) % 6 ∈ ({0, 1, 5} : Finset ℕ)) ↔ i ∈ posT j := by
  decide

/-- **B1, negative side.**  At phase `j`, the negative residue rule names
exactly the bridge's `neg j`. -/
lemma negT_char : ∀ (j i : Fin 6),
    ((j.val + 6 - 2 * (i.val / 2)) % 6 ∈ ({2, 3, 4} : Finset ℕ)) ↔ i ∈ negT j := by
  decide

/-- `negT` is the complement of `posT` (the bridge's `neg_mem`). -/
lemma negT_mem (j i : Fin 6) : (i ∈ negT j) ↔ ¬ (i ∈ posT j) := by
  simp [negT]

/-- **B1, negative side, `decide`-free fallback.**  Same statement as
`negT_char`, proved from `posT_char` and `mod6_not_mem` instead of by deciding
over `negT` directly.  If `negT_char`'s `decide` does not reduce on the parent's
toolchain, delete it and use this one -- nothing else changes. -/
lemma negT_char_alt : ∀ (j i : Fin 6),
    ((j.val + 6 - 2 * (i.val / 2)) % 6 ∈ ({2, 3, 4} : Finset ℕ)) ↔ i ∈ negT j := by
  intro j i
  rw [negT_mem j i, ← posT_char j i]
  exact mod6_not_mem (j.val + 6 - 2 * (i.val / 2))

/-! ## 7.  The closing lemma: `SignTable` from the pairing hypothesis

The only real hypothesis is the one the A6 configuration supplies:
**the six approach directions are the six A6 palette directions, paired**, i.e.
label `i` carries `direction (sixAngle (2 * (i.val / 2)))` -- `i = 0,1` the same
direction, `i = 2,3` the next, `i = 4,5` the last.  Under it, `SignTable v` is
unconditional. -/

/-- **The bridge's `SignTable` from the paired approach directions.**  Paste
into the bridge with `SignTableT := SignTable`, `posT := pos`, `negT := neg`,
`arcT := arc` (all four by `rfl`). -/
theorem signTableT_of_paired (v : Fin 6 → ℂ) (k : Fin 6 → Fin 6)
    (hk : ∀ i : Fin 6, (k i).val = 2 * (i.val / 2))
    (hv : ∀ i : Fin 6, v i = direction (sixAngle (k i))) :
    SignTableT v := by
  intro j t ht
  obtain ⟨s, hs, hst⟩ := ht
  subst hst
  exact ⟨fun i => ((sign_of_paired v k hk hv j s hs i).1).trans (posT_char j i),
    fun i => ((sign_of_paired v k hk hv j s hs i).2).trans (negT_char j i)⟩

/-- **The same, with the canonical pairing and no `k` to supply.** -/
theorem signTableT_of_paired_fin (v : Fin 6 → ℂ)
    (hv : ∀ i : Fin 6,
      v i = direction (sixAngle ⟨2 * (i.val / 2), two_mul_div_two_lt_six i⟩)) :
    SignTableT v :=
  signTableT_of_paired v (fun i => ⟨2 * (i.val / 2), two_mul_div_two_lt_six i⟩)
    (fun _ => rfl) hv

/-! ### Paste-ready forms with the bridge's own names

Inside `supervisor/simplify-lean/swarm-smwguinbz/A6-Bridge-m2.lean`, in the same
namespace `OAI.EuclideanFiveColor.A6`, the two B1 lemmas are literally

    lemma pos_char' : ∀ (j i : Fin 6),
        ((j.val + 6 - 2 * (i.val / 2)) % 6 ∈ ({0, 1, 5} : Finset ℕ)) ↔ i ∈ pos j := by
      decide

    lemma neg_char' : ∀ (j i : Fin 6),
        ((j.val + 6 - 2 * (i.val / 2)) % 6 ∈ ({2, 3, 4} : Finset ℕ)) ↔ i ∈ neg j := by
      decide

which are the converses of the bridge's existing `pos_char`, and the closing
lemma is `signTable_of_paired` above with `posT/negT/arcT/SignTableT` renamed to
`pos/neg/arc/SignTable`.  Note that the `SignTable v` *hypothesis* can only be
discharged once the caller supplies `hv` -- the pairing of the six approach
directions is A6 data, not a consequence of `ApproachingContinuum`. -/

end A6
end EuclideanFiveColor
end

end OAI

#print axioms OAI.EuclideanFiveColor.A6.cos_sign_strict
#print axioms OAI.EuclideanFiveColor.A6.sign_of_paired_fin
#print axioms OAI.EuclideanFiveColor.A6.signTableT_of_paired
#print axioms OAI.EuclideanFiveColor.A6.signTableT_of_paired_fin
