/-! ## Cycle 3, member m2, direction B: the same-weight shift `T` -/

namespace Shift

/-! ### Definitions -/

/-- The same-weight shift, on a list of length `k`:
`T(lam)_i = lam_i - k + 2i - 1`  (1-based `i`).
Encoded as "subtract the staircase of `Staircase.lean`, then add the constant
`k`", i.e. `T(lam) = (subStair lam).map (· + k)`, which is literally
`T(lam)_i = mu_i + k`.  The subtraction is the staircase subtraction, whose
non-truncation is exactly `head_bound`; the addition of `k` never truncates. -/
def shiftT (l : List Nat) : List Nat := (subStair l).map (fun x => x + l.length)

/-- The candidate inverse of `shiftT`: `lam_i = b_i + k - 2i + 1`, encoded as
"add the staircase back, then subtract the constant `k`". -/
def shiftInv (l : List Nat) : List Nat := (addStair l).map (fun x => x - l.length)

/-- Weakly decreasing list (a partition is allowed to be empty, and ties are
allowed; `Gap` is the strict two-step version). -/
def WeakDec : List Nat → Prop
  | [] => True
  | [_] => True
  | a :: b :: rest => b ≤ a ∧ WeakDec (b :: rest)

/-! ### Elementary list arithmetic -/

theorem sum_map_add : ∀ (l : List Nat) (c : Nat),
    (l.map (fun x => x + c)).sum = l.sum + c * l.length
  | [], _ => rfl
  | x :: xs, c => by
    have ih : (xs.map (fun x => x + c)).sum = xs.sum + c * xs.length := sum_map_add xs c
    show x + c + (xs.map (fun x => x + c)).sum = x + xs.sum + c * (xs.length + 1)
    rw [ih, Nat.mul_succ]
    omega

theorem addStair_map_add : ∀ (l : List Nat) (c : Nat),
    addStair (l.map (fun x => x + c)) = (addStair l).map (fun x => x + c)
  | [], _ => rfl
  | x :: xs, c => by
    have ih := addStair_map_add xs c
    have hlen : (List.map (fun x => x + c) xs).length = xs.length := List.length_map ..
    show ((x + c) + (2 * (List.map (fun x => x + c) xs).length + 1))
          :: addStair (List.map (fun x => x + c) xs)
        = ((x + (2 * xs.length + 1)) + c) :: List.map (fun x => x + c) (addStair xs)
    rw [hlen, ih]
    congr 1
    omega

theorem map_add_sub_cancel (l : List Nat) (c : Nat) :
    (l.map (fun x => x + c)).map (fun x => x - c) = l := by
  induction l with
  | nil => rfl
  | cons x xs ih => simp only [List.map_cons, ih, Nat.add_sub_cancel]

theorem map_sub_add_of_le : ∀ (l : List Nat) (c : Nat), (∀ x ∈ l, c ≤ x) →
    (l.map (fun x => x - c)).map (fun x => x + c) = l
  | [], _, _ => rfl
  | x :: xs, c, h => by
    have hx : c ≤ x := h x (List.mem_cons_self ..)
    have hxs : ∀ y ∈ xs, c ≤ y := fun y hy => h y (List.mem_cons_of_mem _ hy)
    have ih := map_sub_add_of_le xs c hxs
    simp only [List.map_cons, ih, Nat.sub_add_cancel hx]

/-- Adding the staircase and then subtracting a constant cancels against the
staircase subtraction: no hypothesis on the list is needed, `omega` disposes of
the truncation. -/
theorem subStair_addStair_map_sub : ∀ (l : List Nat) (c : Nat),
    subStair ((addStair l).map (fun x => x - c)) = l.map (fun x => x - c)
  | [], _ => rfl
  | x :: xs, c => by
    have ih := subStair_addStair_map_sub xs c
    simp only [addStair, List.map_cons, subStair, List.length_map, length_addStair, ih]
    congr 1
    omega

/-! ### Length is retained as data -/

@[simp] theorem length_shiftT (l : List Nat) : (shiftT l).length = l.length := by
  simp [shiftT]

@[simp] theorem length_shiftInv (l : List Nat) : (shiftInv l).length = l.length := by
  simp [shiftInv]

/-! ### (i) `T` preserves the weight exactly -/

theorem sum_shiftT {lam : List Nat} (hp : Pos lam) (hg : Gap lam) :
    (shiftT lam).sum = lam.sum := by
  have h1 : (shiftT lam).sum = (subStair lam).sum + lam.length * lam.length := by
    simp only [shiftT, length_subStair, sum_map_add]
  have h2 : lam.sum = (subStair lam).sum + lam.length * lam.length := by
    have key : (addStair (subStair lam)).sum
        = (subStair lam).sum + lam.length * lam.length := by
      rw [sum_addStair, length_subStair]
    rw [addStair_subStair lam hp hg] at key
    exact key
  rw [h1, h2]

/-! ### (ii) The image satisfies the `B_n` membership condition `k <= entry` -/

theorem mem_shiftT_ge {lam : List Nat} :
    ∀ x ∈ shiftT lam, lam.length ≤ x := by
  intro x hx
  obtain ⟨y, _, rfl⟩ := List.mem_map.1 hx
  omega

/-- The `(iv)` statement in pointwise membership form: the entries of `T(lam)`
are exactly the staircase coordinates shifted up by `k`. -/
theorem mem_shiftT_iff (l : List Nat) (x : Nat) :
    x ∈ shiftT l ↔ ∃ y ∈ subStair l, x = y + l.length := by
  simp only [shiftT, List.mem_map]
  constructor
  · rintro ⟨y, hy, h⟩; exact ⟨y, hy, h.symm⟩
  · rintro ⟨y, hy, h⟩; exact ⟨y, hy, h.symm⟩

/-- `(iv)` literally, as a pointwise statement on indices (`getElem?` so that no
length bookkeeping is needed). -/
theorem shiftT_entry (l : List Nat) (i : Nat) :
    (shiftT l)[i]? = ((subStair l)[i]?).map (fun x => x + l.length) := by
  simp [shiftT]

/-- The inverse formula, pointwise. -/
theorem shiftInv_entry (l : List Nat) (i : Nat) :
    (shiftInv l)[i]? = ((addStair l)[i]?).map (fun x => x - l.length) := by
  simp [shiftInv]

/-! ### (iii) Both inverse laws, on the correctly stated subtypes -/

/-- `shiftInv` is a left inverse of `shiftT` on positive gap partitions (so `T`
is injective there).  Hypotheses `Pos`/`Gap` are the domain `D_n`. -/
theorem shiftInv_shiftT {lam : List Nat} (hp : Pos lam) (hg : Gap lam) :
    shiftInv (shiftT lam) = lam := by
  have h1 : shiftInv (shiftT lam)
      = (addStair (shiftT lam)).map (fun x => x - lam.length) := by
    simp only [shiftInv, length_shiftT]
  rw [h1]
  have h2 : addStair (shiftT lam)
      = (addStair (subStair lam)).map (fun x => x + lam.length) := by
    simp only [shiftT]
    exact addStair_map_add (subStair lam) lam.length
  rw [h2, addStair_subStair lam hp hg, map_add_sub_cancel]

/-- `shiftT` is a left inverse of `shiftInv` on the `B_n`-shaped subtype:
every entry at least the length.  Length is retained as data (it is the
`l.length` in the statement). -/
theorem shiftT_shiftInv {b : List Nat} (h : ∀ x ∈ b, b.length ≤ x) :
    shiftT (shiftInv b) = b := by
  have h1 : shiftT (shiftInv b)
      = (subStair (shiftInv b)).map (fun x => x + b.length) := by
    simp only [shiftT, length_shiftInv]
  rw [h1]
  have h2 : subStair (shiftInv b) = b.map (fun x => x - b.length) := by
    simp only [shiftInv]
    exact subStair_addStair_map_sub b b.length
  rw [h2, map_sub_add_of_le b b.length h]

end Shift

#print axioms RR127.Shift.sum_map_add
#print axioms RR127.Shift.addStair_map_add
#print axioms RR127.Shift.map_add_sub_cancel
#print axioms RR127.Shift.map_sub_add_of_le
#print axioms RR127.Shift.subStair_addStair_map_sub
#print axioms RR127.Shift.length_shiftT
#print axioms RR127.Shift.length_shiftInv
#print axioms RR127.Shift.sum_shiftT
#print axioms RR127.Shift.mem_shiftT_ge
#print axioms RR127.Shift.mem_shiftT_iff
#print axioms RR127.Shift.shiftT_entry
#print axioms RR127.Shift.shiftInv_entry
#print axioms RR127.Shift.shiftInv_shiftT
#print axioms RR127.Shift.shiftT_shiftInv
