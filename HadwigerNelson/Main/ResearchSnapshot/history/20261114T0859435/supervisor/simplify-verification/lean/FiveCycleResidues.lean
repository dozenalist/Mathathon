/-
  supervisor/simplify-verification — block 4, revised block 5.
  Finite content of steps 4-5 of the six-step five-cycle argument (AUDIT-FIVE-CYCLE.md §4b):
  the five residues reduce to two allowed pairs, and those two are exchanged by a symmetry that
  is a genuine relabelling **at both levels** — state indices and vertex labels.

  ==== THE TWO LEVELS (this is the point of the file) ====
  The five-cycle data live on two different copies of Z/5Z:

  * VERTEX LABELS  k : ZMod 5 — the colour names. `D i = {i, i+2} ⊂ ZMod 5` is the set of labels
    available in state i (paper p. 40, l. 2114-2117).
  * STATE INDICES  i : ZMod 5 — the indexing of the essential supports S_i and hence of the lists
    S(a) = {i : a ∈ S_i} (paper p. 40, l. 2119-2123). `P j = {j-1, j+2}` (paper p. 42,
    l. 2188-2190) and the normalisation pair {0,1} (l. 2184) are STATE-side objects.

  A relabelling of states is only legitimate if a relabelling of labels acts compatibly, i.e. if

      g '' D i = D (h i)          for all state indices i,

  where h is the state map and g the vertex-label map. The two are in general DIFFERENT maps; an
  earlier version of this file used the single map `k ↦ 1-k` on both levels and drew a
  state-level conclusion from it. That is the error corrected here:

      state map h(i) = 1 - i        is induced by   g(k) = 3 - k      (`g_induces_h`)
      state map i ↦ 4 - i           is induced by   k ↦ 1 - k         (`one_minus_k_induces_four_minus_i`)

  The six-step argument needs the state map `i ↦ 1-i` (it must send `P 1 = {0,3}` to
  `P 4 = {1,3}` and fix `{0,1}` and `{2,4}`), so the compatible vertex map is `k ↦ 3-k`, not
  `k ↦ 1-k`.

  ==== TRANSPORT OF EVERY LIST CONDITION ====
  With `g '' D i = D (h i)` and `g`, `h` involutions (`label_transport`), every condition the
  argument uses transports along (g, h):

  * (V) `S(a)` has no common label. If `∀ k, ∃ i ∈ L, k ∉ D i` and `g k ∉ D i` then `k ∉ D (h i)`,
    because `k ∈ D (h i) ⇒ g k ∈ g''D(h i) = D(h(h i)) = D i`. Hence `L` valid ⇒ `h''L` valid.
  * (D) `S(r) ∩ S(r+1) = ∅`. An image of disjoint sets under an injective map is disjoint:
    `h''S(r) ∩ h''S(r+1) = ∅`.
  * (N) `i ∈ S(r)` has a neighbour in `S(r±1)`. Since `h(i+1) = h i - 1` (`h_reverses_step`), the
    image of a neighbour `i±1` is `h i ∓ 1`, which is again a neighbour of `h i`; (N) is symmetric
    in `±1`, so it transports.
  * anchor: `h''{0,1} = {1,0} = {0,1}` (`h_fixes_anchor`) — so the normalisation stays available.
  * pair: `h''{2,4} = {4,2} = {2,4}` (`h_fixes_pair24`), and `h''P 1 = P 4`
    (`h_swaps_allowed_pairs`) — which is exactly what lets "`j = 1` or `j = 4`" be reduced to
    "`j = 1`" without loss.

  ==== CORRECTION (block 6): one statement of the block-5 version was FALSE ====
  The block-5 file asserted `∀ j, (P j).image h = P (h j)`. That is false: at `j = 0`,
  `h '' P 0 = h '' {4,2} = {2,4}` while `P (h 0) = P 1 = {0,3}`. The correct target is `P (-j)`:

      h '' P j = P (-j)          (checked for all five j; `h_image_P` below)

  At `j = 1` this reads `h '' P 1 = P (-1) = P 4 = {1,3}`, which is the only case the argument
  uses, so the retraction of the general `P (h j)` form does not weaken the application - but the
  general form as written was wrong and a reader could have used it at `j = 0`. The companion
  identities `h '' Nb i = Nb (h i)` and `g '' D i = D (h i)` are both correct.

  Lemma 6.7 is NOT touched by any of this: the argument still uses it at the two endpoint
  directions, as printed (l. 2196).

  ==== IMPORTS (exact; all present at mathlib d13f23b723b8a846827a245b89c10fc7d3f11612) ====
      Mathlib.Data.ZMod.Basic      -- ZMod 5, ring structure, numerals; pulls ZMod.Defs (Fintype)
      Mathlib.Data.Finset.Image    -- Finset.image; pulls Finset.Basic
      Mathlib.Data.Fintype.Basic   -- Fintype.decidableForallFintype for `by decide` on `∀ i`
  No `sorry`, no `native_decide`, no `axiom`, no `opaque`, no added hypothesis. NOT BUILT HERE:
  the build is local serial queue item 6 (LOCAL-CHECK-QUEUE.json).
-/
import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Finset.Image
import Mathlib.Data.Fintype.Basic

namespace FiveCycleResidues

open Finset

/-- VERTEX level: the label set of state `i`. -/
def D (i : ZMod 5) : Finset (ZMod 5) := {i, i + 2}

/-- STATE level: the distance-2 pair `{j-1, j+2}` the paper puts in `S(2) ∩ S(4)`. -/
def P (j : ZMod 5) : Finset (ZMod 5) := {j - 1, j + 2}

/-- STATE level: the normalisation pair `{0,1} ⊆ S(0)`. -/
def anchor : Finset (ZMod 5) := {0, 1}

/-- STATE level: the compulsory part `{2,4} ⊆ S(1) ∩ S(5)`. -/
def pair24 : Finset (ZMod 5) := {2, 4}

/-- STATE map: the reflection of state indices used in step 5 of the argument. -/
def h (i : ZMod 5) : ZMod 5 := 1 - i

/-- VERTEX map: the relabelling of colour names compatible with `h`. -/
def g (k : ZMod 5) : ZMod 5 := 3 - k

/-- The map used by mistake in the first version of this file (correct as a statement, but it
induces the state map `i ↦ 4 - i`, which does NOT swap `P 1` and `P 4`). -/
def g' (k : ZMod 5) : ZMod 5 := 1 - k

/-! ## 0. The commuting identity: the one place the two levels meet -/

theorem g_induces_h : ∀ i : ZMod 5, (D i).image g = D (h i) := by decide

theorem one_minus_k_induces_four_minus_i : ∀ i : ZMod 5, (D i).image g' = D (4 - i) := by decide

theorem g_involutive : ∀ k : ZMod 5, g (g k) = k := by decide

theorem h_involutive : ∀ i : ZMod 5, h (h i) = i := by decide

/-- Label-level form of the commuting identity: membership of a label in state `i` is the same as
membership of the relabelled label in the relabelled state. This is the pointwise input to the
transport of (V). -/
theorem label_transport : ∀ (i k : ZMod 5), (k ∈ D i ↔ g k ∈ D (h i)) := by decide

/-! ## 1. Step 4: five residues reduce to two allowed pairs -/

theorem five_residues_reduce_to_two : ∀ j : ZMod 5, (P j ∩ pair24 = ∅ ↔ j = 1 ∨ j = 4) := by
  decide

theorem residue_zero_collides : (2 : ZMod 5) ∈ P 0 := by decide

theorem residue_two_collides : (4 : ZMod 5) ∈ P 2 := by decide

theorem residue_three_collides : (2 : ZMod 5) ∈ P 3 := by decide

/-! ## 2. Step 5: the state reflection and its action on every object the argument uses -/

theorem h_reverses_step : ∀ i : ZMod 5, h (i + 1) = h i - 1 := by decide

/-- Correct target: `P (-j)`, not `P (h j)`. See the correction note in the header. -/
theorem h_image_P : ∀ j : ZMod 5, (P j).image h = P (-j) := by decide

theorem h_fixes_anchor : anchor.image h = anchor := by decide

theorem h_fixes_pair24 : pair24.image h = pair24 := by decide

theorem h_swaps_allowed_pairs : (P 1).image h = P 4 := by decide

/-! ## 3. Transport of (V), (D), (N) along the compatible pair `(g, h)`

The six-step argument reflects a configuration of six lists. The *positions* `r : ZMod 6` are not
moved (the paper's directions `R^r a` stay where they are); only the state indices inside each list
are relabelled. Below, `Lists = ZMod 6 → Finset (ZMod 5)` is a configuration, and `push` relabels
every list by `h` while leaving `r` alone. The statements are the paper's own quantifiers:

* (V) "no common label": `∀ k, ∃ i ∈ L, k ∉ D i` — paper p. 42, l. 2180-2183 (a list with empty
  diagonal intersection is the negation);
* (D) `S(r) ∩ S(r+1) = ∅` for every `r` — p. 41, l. 2134;
* (N) every `i ∈ S(r)` has a neighbour in `S(r+1)` *and* in `S(r-1)` — p. 41, l. 2135-2137.

Each proof is two or three lines: involutivity plus `g_induces_h` (or `nb_image`). No enumeration of
six lists, no case split on `r`, no use of the eight countermodels' specific values. -/

/-- (V) as a predicate: the list `L` has no common label. -/
def NotCommon (L : Finset (ZMod 5)) : Prop := ∀ k : ZMod 5, ∃ i ∈ L, k ∉ D i

/-- (N) as a predicate: every index of `L` has a neighbour in `M`. -/
def Nb (i : ZMod 5) : Finset (ZMod 5) := {i - 1, i + 1}

def HasNbr (L M : Finset (ZMod 5)) : Prop := ∀ i ∈ L, (Nb i ∩ M).Nonempty

/-- A configuration: one list per position `r : ZMod 6`. -/
abbrev Lists := ZMod 6 → Finset (ZMod 5)

/-- Relabel every list by the state reflection; positions unchanged. -/
def push (S : Lists) : Lists := fun r => (S r).image h

theorem nb_image : ∀ i : ZMod 5, (Nb i).image h = Nb (h i) := by decide

/-- **(V) transports.** If `L` has no common label then so does `h '' L`:
apply the hypothesis to the relabelled label `g k`, and use `g '' D (h i) = D i` (`h_involutive`)
to move the failure of membership back. -/
theorem notCommon_image (L : Finset (ZMod 5)) (hL : NotCommon L) :
    NotCommon (L.image h) := by
  intro k
  obtain ⟨i, hi, hki⟩ := hL (g k)
  refine ⟨h i, Finset.mem_image.mpr ⟨i, hi, rfl⟩, ?_⟩
  intro hk
  exact hki (by
    have hmem : g k ∈ (D (h i)).image g := Finset.mem_image.mpr ⟨k, hk, rfl⟩
    rwa [g_induces_h, h_involutive] at hmem)

/-- **(D) transports.** Injectivity of `h` carries disjointness to disjointness. -/
theorem disjoint_image (L M : Finset (ZMod 5)) (hd : Disjoint L M) :
    Disjoint (L.image h) (M.image h) := by
  rw [Finset.disjoint_left] at hd ⊢
  intro x hx hy
  obtain ⟨a, ha, rfl⟩ := Finset.mem_image.mp hx
  obtain ⟨b, hb, hba⟩ := Finset.mem_image.mp hy
  have hba' : b = a := by rw [← h_involutive b, hba, h_involutive a]
  exact hd ha (hba' ▸ hb)

/-- **(N) transports.** A neighbour `m` of `i` maps to a neighbour `h m` of `h i` because
`h '' Nb i = Nb (h i)`; this is where the reversal `h (i+1) = h i - 1` is absorbed.

The witness must be *introduced before* the intersection is split: `Nonempty` is `∃ a, a ∈ _`, not a
membership, and the intersection is `Nb (h i) ∩ M.image h` in that order. (An earlier version fed a
membership proof to `refine ⟨·, ·⟩` and tried `rw [Finset.mem_inter]` before producing the witness;
that does not elaborate and left `neighbour_family_push` depending on `sorryAx`.) -/
theorem hasNbr_image (L M : Finset (ZMod 5)) (hLM : HasNbr L M) :
    HasNbr (L.image h) (M.image h) := by
  intro x hx
  obtain ⟨i, hi, rfl⟩ := Finset.mem_image.mp hx
  obtain ⟨m, hm⟩ := hLM i hi
  obtain ⟨hmNb, hmM⟩ := Finset.mem_inter.mp hm
  have hNb : h m ∈ Nb (h i) := by
    have hmem : h m ∈ (Nb i).image h := Finset.mem_image.mpr ⟨m, hmNb, rfl⟩
    rwa [nb_image] at hmem
  exact ⟨h m, Finset.mem_inter.mpr ⟨hNb, Finset.mem_image.mpr ⟨m, hmM, rfl⟩⟩⟩

/-- The three transports, stated on configurations: positions unchanged. -/
theorem valid_family_push (S : Lists) (hS : ∀ r, NotCommon (S r)) :
    ∀ r, NotCommon (push S r) := fun r => notCommon_image (S r) (hS r)

theorem disjoint_family_push (S : Lists) (hS : ∀ r, Disjoint (S r) (S (r + 1))) :
    ∀ r, Disjoint (push S r) (push S (r + 1)) :=
  fun r => disjoint_image (S r) (S (r + 1)) (hS r)

theorem neighbour_family_push (S : Lists)
    (hS : ∀ r, HasNbr (S r) (S (r + 1)) ∧ HasNbr (S r) (S (r - 1))) :
    ∀ r, HasNbr (push S r) (push S (r + 1)) ∧ HasNbr (push S r) (push S (r - 1)) :=
  fun r => ⟨hasNbr_image (S r) (S (r + 1)) (hS r).1,
            hasNbr_image (S r) (S (r - 1)) (hS r).2⟩

/-! ## 3. What this file does not claim

* (V) — "this list has no common label" — is *taken*, never derived; see AUDIT-FIVE-CYCLE.md §2-§3
  and `checks/five_cycle_licence.py` (eight countermodels with (V) only at positions 0 and 3).
* The six-step argument is not formalised here; only its finite residue steps and the symmetry.
* These are FINITE facts about lists. They do not say anything about accumulation of five-cycle
  centres, and they do not assume (NC-1): the transport is a statement about what a reflection
  preserves, not a supply of the missing no-common-label hypothesis at position 1.
-/

end FiveCycleResidues

#print axioms FiveCycleResidues.g_induces_h
#print axioms FiveCycleResidues.label_transport
#print axioms FiveCycleResidues.five_residues_reduce_to_two
#print axioms FiveCycleResidues.h_swaps_allowed_pairs
#print axioms FiveCycleResidues.notCommon_image
#print axioms FiveCycleResidues.h_image_P
#print axioms FiveCycleResidues.one_minus_k_induces_four_minus_i
