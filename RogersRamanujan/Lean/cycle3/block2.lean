/-! ### Bonus: the order facts that make `T : D_n → B_n` a bijection -/

namespace Shift

/-! #### The order half: `T(lam)` is a partition -/

theorem weakDec_map_add : ∀ (l : List Nat) (c : Nat), WeakDec l →
    WeakDec (l.map (fun x => x + c))
  | [], _, _ => trivial
  | [_], _, _ => trivial
  | a :: b :: t, c, h => by
    have hba : b ≤ a := h.1
    have ih := weakDec_map_add (b :: t) c h.2
    simp only [List.map_cons]
    exact ⟨by omega, ih⟩

/-- The staircase coordinates of a positive gap partition are weakly decreasing.
(Same proof as `RogersRamanujan/Lean/StaircaseOrder.lean`;
restated here so this file stays a single self-contained target.) -/
theorem weakDec_subStair : ∀ l : List Nat, Pos l → Gap l → WeakDec (subStair l)
  | [], _, _ => trivial
  | [_], _, _ => trivial
  | a :: b :: t, hp, hg => by
    have hba : b + 2 ≤ a := hg.1
    have ih : WeakDec (subStair (b :: t)) :=
      weakDec_subStair (b :: t) (pos_of_cons hp) hg.2
    cases t with
    | nil =>
      show b - 1 ≤ a - 3 ∧ WeakDec (subStair (b :: []))
      exact ⟨by omega, ih⟩
    | cons c t =>
      show b - (2 * (t.length + 1) + 1) ≤
        a - (2 * ((t.length + 1) + 1) + 1) ∧ WeakDec (subStair (b :: c :: t))
      exact ⟨by omega, ih⟩

/-- `T` sends `D_n` to partitions (`WeakDec`). -/
theorem weakDec_shiftT {l : List Nat} (hp : Pos l) (hg : Gap l) : WeakDec (shiftT l) :=
  weakDec_map_add (subStair l) l.length (weakDec_subStair l hp hg)

/-! #### The codomain half: `shiftInv` lands back in `D_n` on `B_n` -/

theorem addStair_pos : ∀ l : List Nat, Pos (addStair l)
  | [] => by
    intro x hx
    simp [addStair] at hx
  | m :: ms => by
    intro x hx
    simp only [addStair, List.mem_cons] at hx
    rcases hx with rfl | hx
    · omega
    · exact addStair_pos ms x hx

theorem weakDec_addStair : ∀ (l : List Nat), WeakDec l → Gap (addStair l)
  | [], _ => trivial
  | [_], _ => trivial
  | a :: b :: t, hwd => by
    have hba : b ≤ a := hwd.1
    have ih : Gap (addStair (b :: t)) := weakDec_addStair (b :: t) hwd.2
    show b + (2 * t.length + 1) + 2 ≤ a + (2 * (t.length + 1) + 1) ∧
      Gap (addStair (b :: t))
    exact ⟨by omega, ih⟩

/-- Every entry of `addStair b` strictly exceeds any bound on the entries of `b`.
This is what makes the "subtract the constant `k`" step non-truncating. -/
theorem addStair_gt : ∀ (b : List Nat) (c : Nat), (∀ x ∈ b, c ≤ x) →
    ∀ y ∈ addStair b, c < y
  | [], c, _ => by
    intro y hy
    simp [addStair] at hy
  | x :: xs, c, h => by
    have hx : c ≤ x := h x (List.mem_cons_self ..)
    have hxs : ∀ y ∈ xs, c ≤ y := fun y hy => h y (List.mem_cons_of_mem _ hy)
    have ih := addStair_gt xs c hxs
    intro y hy
    simp only [addStair, List.mem_cons] at hy
    rcases hy with rfl | hy
    · omega
    · exact ih y hy

theorem pos_map_sub (l : List Nat) (c : Nat) (h : ∀ y ∈ l, c < y) :
    Pos (l.map (fun x => x - c)) := by
  intro x hx
  obtain ⟨y, hy, rfl⟩ := List.mem_map.1 hx
  have := h y hy
  omega

theorem gap_map_sub : ∀ (l : List Nat) (c : Nat), Gap l → (∀ y ∈ l, c ≤ y) →
    Gap (l.map (fun x => x - c))
  | [], _, _, _ => trivial
  | [_], _, _, _ => trivial
  | a :: b :: t, c, hg, h => by
    have hba : b + 2 ≤ a := hg.1
    have hb : c ≤ b := h b (by simp)
    have htail : ∀ y ∈ (b :: t), c ≤ y := fun y hy => h y (List.mem_cons_of_mem _ hy)
    have ih : Gap (List.map (fun x => x - c) (b :: t)) := gap_map_sub (b :: t) c hg.2 htail
    show b - c + 2 ≤ a - c ∧ Gap (List.map (fun x => x - c) (b :: t))
    exact ⟨by omega, ih⟩

theorem shiftInv_pos {b : List Nat} (h : ∀ x ∈ b, b.length ≤ x) : Pos (shiftInv b) :=
  pos_map_sub (addStair b) b.length (addStair_gt b b.length h)

theorem shiftInv_gap {b : List Nat} (hwd : WeakDec b) (h : ∀ x ∈ b, b.length ≤ x) :
    Gap (shiftInv b) :=
  gap_map_sub (addStair b) b.length (weakDec_addStair b hwd)
    (fun y hy => Nat.le_of_lt (addStair_gt b b.length h y hy))

/-! #### The packaged bijection `D_n ≃ B_n`, and the weight identity -/

/-- Domain: positive descending-with-gap-two lists (length retained). -/
abbrev DGap := { l : List Nat // Pos l ∧ Gap l }

/-- Codomain: partitions whose smallest part is at least the length. -/
abbrev BSmall := { b : List Nat // WeakDec b ∧ ∀ x ∈ b, b.length ≤ x }

def toB (l : DGap) : BSmall :=
  ⟨shiftT l.1, weakDec_shiftT l.2.1 l.2.2, fun x hx => by
    rw [length_shiftT]
    exact mem_shiftT_ge x hx⟩

def toD (b : BSmall) : DGap :=
  ⟨shiftInv b.1, shiftInv_pos b.2.2, shiftInv_gap b.2.1 b.2.2⟩

theorem toD_toB (l : DGap) : toD (toB l) = l := by
  apply Subtype.ext
  exact shiftInv_shiftT l.2.1 l.2.2

theorem toB_toD (b : BSmall) : toB (toD b) = b := by
  apply Subtype.ext
  exact shiftT_shiftInv b.2.2

/-- Same weight, at the subtype level. -/
theorem weight_toB (l : DGap) : (toB l).1.sum = l.1.sum :=
  sum_shiftT l.2.1 l.2.2

/-! #### Witnesses: the theorems are not vacuous, and the hypotheses are needed -/

theorem witness_T_531 : shiftT [5, 3, 1] = [3, 3, 3] := by decide
theorem witness_T_41 : shiftT [4, 1] = [3, 2] := by decide
theorem witness_T_641 : shiftT [6, 4, 1] = [4, 4, 3] := by decide
theorem witness_inv_443 : shiftInv [4, 4, 3] = [6, 4, 1] := by decide

/-- `Gap` is needed for weight preservation: `[1,3]` is positive but not a gap
partition, and `T` there loses weight (`[2,4]`, weight 6 against 4). -/
theorem witness_gap_needed : (shiftT [1, 3]).sum ≠ [1, 3].sum := by decide

/-- `Pos` is needed for injectivity: `T` collapses `[0]` and `[1]`. -/
theorem witness_not_injective : shiftT [0] = shiftT [1] ∧ [0] ≠ [1] := by decide

/-- The `WeakDec` half of the `B_n` condition is not implied by "smallest part
at least the length": `[2,5]` is positive, has length 2 and every entry at
least 2, but `shiftInv [2,5] = [3,4]` is not a gap partition.  This is why
`shiftT_shiftInv` carries only the entry bound while `shiftInv_gap` carries
`WeakDec`. -/
theorem witness_weakDec_needed : ¬ Gap (shiftInv [2, 5]) := by
  intro h
  exact absurd h.1 (by decide)

end Shift

#print axioms RR127.Shift.weakDec_map_add
#print axioms RR127.Shift.weakDec_subStair
#print axioms RR127.Shift.weakDec_shiftT
#print axioms RR127.Shift.addStair_pos
#print axioms RR127.Shift.weakDec_addStair
#print axioms RR127.Shift.addStair_gt
#print axioms RR127.Shift.pos_map_sub
#print axioms RR127.Shift.gap_map_sub
#print axioms RR127.Shift.shiftInv_pos
#print axioms RR127.Shift.shiftInv_gap
#print axioms RR127.Shift.toD_toB
#print axioms RR127.Shift.toB_toD
#print axioms RR127.Shift.weight_toB
#print axioms RR127.Shift.witness_T_531
#print axioms RR127.Shift.witness_T_41
#print axioms RR127.Shift.witness_T_641
#print axioms RR127.Shift.witness_inv_443
#print axioms RR127.Shift.witness_gap_needed
#print axioms RR127.Shift.witness_not_injective
#print axioms RR127.Shift.witness_weakDec_needed
