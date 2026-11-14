/-
  supervisor/simplify-verification — block 4 (2026-11-14).
  The finite content of steps 4-5 of the six-step five-cycle argument in
  `supervisor/simplify-verification/AUDIT-FIVE-CYCLE.md` §4b:
  the five possible residues `j` reduce to the two allowed pairs, and those two are
  interchanged by an automorphism of the diagonal system.

  EXACT IMPORT LIST (verified present in mathlib d13f23b723b8a846827a245b89c10fc7d3f11612):
      Mathlib.Data.ZMod.Basic      -- ZMod 5, its ring structure and numerals; pulls ZMod.Defs (Fintype)
      Mathlib.Data.Finset.Image    -- Finset.image; pulls Finset.Basic
      Mathlib.Data.Fintype.Basic   -- `Fin.fintype`, `Fintype.decidableForallFintype`

  Every proof below is `by decide` on a closed statement over the five residues or over `Fin 5`.
  No `sorry`, no `native_decide`, no `axiom`, no `opaque`, no extra hypothesis: the statements are
  decidable facts about `ZMod 5`, so the kernel checks the computation term.  NOT BUILT HERE — the
  build belongs to the serial local-check queue (LOCAL-CHECK-QUEUE.json, item 6).

  PAPER MAP (paper.pdf, pdftotext -layout line numbers):
  * `D i = {i, i+2}`, the five-cycle palette diagonals: p. 40, l. 2114-2117 ("almost every palette
    is exactly one of its diagonals D_i = {i, i+2}").
  * (D) `S(a) ∩ S(Ra) = ∅` and (N) neighbour existence: p. 41, l. 2134-2137.
  * `{j-1, j+2} ⊆ S(2) ∩ S(4)` when `{j, j+1} ⊆ S(3)`: p. 42, l. 2188-2190.
  * "Checking the five possible residues of j leaves only j = 1 or j = 4: their pairs {j-1, j+2}
    are respectively {0,3} and {3,1}; each of j = 0, 2, 3 contains 2 or 4": p. 42, l. 2190-2193.
    `five_residues_reduce_to_two` below is exactly this sentence, with the count made explicit and
    `residue_*_collides` naming, for the three excluded residues, the label that collides.
  * the relabelling "Rotate the label indices so that 0, 1 ∈ S(0)": p. 42, l. 2184 (this is what
    makes `anchor` the right pair, and it is why a reflection fixing `anchor` setwise is available).
-/
import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Finset.Image
import Mathlib.Data.Fintype.Basic

namespace FiveCycleResidues

open Finset

/-- The diagonal attached to a five-cycle palette label. -/
def D (i : ZMod 5) : Finset (ZMod 5) := {i, i + 2}

/-- The distance-2 pair produced by (N) at the two positions adjacent to a `{j, j+1}` contact:
`P j = {j - 1, j + 2}`, the pair the paper puts in `S(2) ∩ S(4)`. -/
def P (j : Fin 5) : Finset (ZMod 5) := {((j : ℕ) : ZMod 5) - 1, ((j : ℕ) : ZMod 5) + 2}

/-- The anchor pair at position 0 (after the paper's relabelling). -/
def anchor : Finset (ZMod 5) := {0, 1}

/-- The compulsory part `{2,4} ⊆ S(1) ∩ S(5)` of the neighbouring lists. -/
def pair24 : Finset (ZMod 5) := {2, 4}

/-- The reflection of labels `k ↦ 1 - k`. -/
def refl (k : ZMod 5) : ZMod 5 := 1 - k

/-! ## 1. Step 4: the five residues reduce to two pairs

The paper spends a residue check here; the content is that exactly two of the five distance-2 pairs
`{j-1, j+2}` avoid `{2,4}`, so for every other `j` the pair collides with `S(1) = S(5) = {2,4}` and
(D) is violated at positions 1/2 (or 4/5). -/

theorem five_residues_reduce_to_two :
    ∀ j : Fin 5, (P j ∩ pair24 = ∅ ↔ ((j : ℕ) : ZMod 5) = 1 ∨ ((j : ℕ) : ZMod 5) = 4) := by
  decide

/-- For the three excluded residues, the label that collides: `j = 0` and `j = 3` collide at `2`,
`j = 2` collides at `4`.  (So the excluded `j` are excluded *by an exhibited label*, not by a
counting argument that the reader has to redo.) -/
theorem residue_zero_collides : (2 : ZMod 5) ∈ P 0 := by decide

theorem residue_two_collides : (4 : ZMod 5) ∈ P 2 := by decide

theorem residue_three_collides : (2 : ZMod 5) ∈ P 3 := by decide

/-! ## 2. Step 5: the reflection that identifies `j = 1` with `j = 4`

`j = 1` gives `P 1 = {0,3}` and `j = 4` gives `P 4 = {3,1} = {1,3}`.  The reflection
`k ↦ 1 - k` fixes the anchor pair and `{2,4}` setwise and swaps the two pairs.  What makes it a
*legitimate* relabelling rather than an ad hoc permutation is the last theorem: it carries every
diagonal `D i` onto a diagonal `D (4 - i)`, so it carries intersections of diagonals to
intersections of diagonals.  Hence "no common label" is preserved, and a configuration with
`{j,j+1} ⊆ S(3)` for `j = 4` reflects to one with `j = 1`. -/

theorem refl_involutive : ∀ k : ZMod 5, refl (refl k) = k := by decide

theorem refl_fixes_anchor : anchor.image refl = anchor := by decide

theorem refl_fixes_pair24 : pair24.image refl = pair24 := by decide

theorem refl_swaps_the_two_allowed_pairs : (P 1).image refl = P 4 := by decide

/-- The reflection is an automorphism of the diagonal system, up to the index relabelling
`i ↦ 4 - i`. -/
theorem refl_image_diagonal : ∀ i : ZMod 5, (D i).image refl = D (4 - i) := by decide

/-! ## 3. What this file does *not* claim

* It does not touch (V): the hypothesis that a given list has no common label is *taken*, not proved.
  `AUDIT-FIVE-CYCLE.md` §2-§3 records that the paper proves it only at positions 0 and 3, and that
  eight configurations satisfy everything else (`checks/five_cycle_licence.py`).
* It does not formalise the six-step argument; it formalises the two finite steps inside it, which
  are the only places where residues are enumerated.
* It does not say anything about `S_i` as sets of directions: `D`, `P` here are purely combinatorial.
-/

end FiveCycleResidues

#print axioms FiveCycleResidues.five_residues_reduce_to_two
#print axioms FiveCycleResidues.refl_image_diagonal
#print axioms FiveCycleResidues.refl_swaps_the_two_allowed_pairs

-- Local audit: print the remaining six axiom sets; theorem bodies are unchanged.
#print axioms FiveCycleResidues.residue_zero_collides
#print axioms FiveCycleResidues.residue_two_collides
#print axioms FiveCycleResidues.residue_three_collides
#print axioms FiveCycleResidues.refl_involutive
#print axioms FiveCycleResidues.refl_fixes_anchor
#print axioms FiveCycleResidues.refl_fixes_pair24
