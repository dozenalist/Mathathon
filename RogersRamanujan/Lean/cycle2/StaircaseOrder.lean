/-
RR127 / SAIR Mathathon problem 127 -- cycle 2, member m2, direction D.

The MISSING ORDER STATEMENT for the frozen staircase module.

`StaircaseBase.lean` is a byte-identical copy of
`RogersRamanujan/Lean/Staircase.lean` (sha256
c7acbcd74866958596acc458a7231939ebe01969a0723179bfdaaf263cbeb280); it is copied
here only because this VM has no `.olean` for it and I must not write into
`RogersRamanujan/Lean/`.  With `import StaircaseBase` this file builds on the
kernel-checked definitions `Pos`, `Gap`, `subStair`, `addStair` unchanged and
adds what `Lean/README.md` lists as "computational only (checker)":

  * `WeakDec` and `subStair_weakDec`: the staircase coordinates of a positive
    gap partition are weakly decreasing -- the order half of "mu is a
    partition".
  * `addStair_gap` : the staircase map is onto weakly decreasing lists, i.e.
    `addStair` sends the coordinate object back to `Pos`/`Gap`.
  * the two inverse laws *as maps between the correctly specified subtypes*
    (`Subtype` = retained length, zeros allowed), packaged in `StairBridge`.
  * length retention, weight, and the zero padding made explicit
    (`AllZero`/`subStair_zero_tail`): the zeros of the coordinate list are a
    terminal block, so a coordinate list is "positive part ++ padding", and
    the padding must be kept because `addStair` needs the length.

Mathlib-free: `import Init` only (reached through `StaircaseBase`), `omega`/`simp`.
No `sorry`, no custom axiom.

Verification command (from the directory holding both files):
  LEAN_PATH="$PWD:$LEAN_PATH" lean StaircaseOrder.lean
-/
import StaircaseBase

namespace RR127

/-! ## The order law -/

/-- Weakly decreasing ("monotone") list of naturals.  `WeakDec (subStair lam)`
is the statement that the staircase coordinates of `lam` are a partition with
zeros allowed. -/
def WeakDec : List Nat → Prop
  | [] => True
  | [_] => True
  | a :: b :: rest => b ≤ a ∧ WeakDec (b :: rest)

theorem weakDec_head {a b : Nat} {rest : List Nat} (h : WeakDec (a :: b :: rest)) :
    b ≤ a := h.1

theorem weakDec_tail {a b : Nat} {rest : List Nat} (h : WeakDec (a :: b :: rest)) :
    WeakDec (b :: rest) := h.2

/-- Padding: all entries are `0`. -/
def AllZero : List Nat → Prop
  | [] => True
  | a :: rest => a = 0 ∧ AllZero rest

/-- Arithmetic engine for the order law: the staircase constant drops by two per
step, so a gap of two in `lam` becomes an inequality in the coordinates.
Truncating subtraction is covered: `omega` splits on it. -/
theorem sub_le_sub_add_two {a b c : Nat} (h : b + 2 ≤ a) : b - c ≤ a - (c + 2) := by
  omega

/-! ## `subStair` is weakly decreasing (the missing half) -/

theorem subStair_weakDec : ∀ l : List Nat, Pos l → Gap l → WeakDec (subStair l)
  | [], _, _ => trivial
  | [_], _, _ => trivial
  | a :: b :: t, hp, hg => by
    have hba : b + 2 ≤ a := hg.1
    have ih : WeakDec (subStair (b :: t)) :=
      subStair_weakDec (b :: t) (pos_of_cons hp) hg.2
    cases t with
    | nil =>
      show b - 1 ≤ a - 3 ∧ WeakDec (subStair (b :: []))
      exact ⟨by omega, ih⟩
    | cons c t =>
      show b - (2 * (t.length + 1) + 1) ≤
        a - (2 * ((t.length + 1) + 1) + 1) ∧ WeakDec (subStair (b :: c :: t))
      exact ⟨by omega, ih⟩

/-! ## `addStair` sends coordinate objects back to `Pos`/`Gap` -/

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

theorem addStair_gap : ∀ l : List Nat, WeakDec l → Gap (addStair l)
  | [], _ => trivial
  | [_], _ => trivial
  | a :: b :: t, hwd => by
    have hba : b ≤ a := hwd.1
    have ih : Gap (addStair (b :: t)) := addStair_gap (b :: t) hwd.2
    show b + (2 * t.length + 1) + 2 ≤ a + (2 * (t.length + 1) + 1) ∧
      Gap (addStair (b :: t))
    exact ⟨by omega, ih⟩

/-! ## Zero padding is a terminal block -/

theorem allZero_of_weakDec_zero : ∀ rest : List Nat, WeakDec (0 :: rest) → AllZero rest
  | [], _ => trivial
  | [c], hw => by
    have hc : c ≤ 0 := hw.1
    exact ⟨by omega, trivial⟩
  | c :: d :: u, hw => by
    have hc : c ≤ 0 := hw.1
    have hc0 : c = 0 := by omega
    have ih : AllZero (d :: u) := allZero_of_weakDec_zero (d :: u) (hc0 ▸ hw.2)
    exact ⟨hc0, ih⟩

/-- The zeros of a staircase coordinate list form a terminal block.  This is
what "zero padding" means: dropping the zeros is lossy, because the length `k`
is what `addStair` consumes. -/
theorem subStair_zero_tail {lam : List Nat} {a : Nat} {rest : List Nat}
    (hp : Pos lam) (hg : Gap lam) (h : subStair lam = a :: rest) (ha : a = 0) :
    AllZero rest := by
  have h1 : WeakDec (a :: rest) := h ▸ subStair_weakDec lam hp hg
  have h2 : WeakDec (0 :: rest) := ha ▸ h1
  exact allZero_of_weakDec_zero rest h2

/-- `0 <= x` for `x : Nat` is automatic: the old `subStair_nonneg` carries no
content.  Recorded so the claim is machine-checked rather than asserted. -/
theorem nonneg_is_vacuous (l : List Nat) (x : Nat) : x ∈ l → 0 ≤ x :=
  fun _ => Nat.zero_le x

/-! ## Length retention and weight, in one block -/

theorem subStair_length_sum (lam : List Nat) (hp : Pos lam) (hg : Gap lam) :
    (subStair lam).length = lam.length ∧
      (subStair lam).sum = lam.sum - lam.length * lam.length :=
  ⟨length_subStair lam, weight_subStair (n := lam.sum) hp hg rfl⟩

theorem addStair_length_sum (m : List Nat) :
    (addStair m).length = m.length ∧
      (addStair m).sum = m.sum + m.length * m.length :=
  ⟨length_addStair m, sum_addStair m⟩

/-! ## The equivalence between the two subtypes -/

/-- `D`-shaped objects: positive, gap two, with the length retained. -/
def StairGap := { l : List Nat // Pos l ∧ Gap l }

/-- Coordinate objects: weakly decreasing, zeros allowed, length retained. -/
def StairCoord := { m : List Nat // WeakDec m }

def subStairMap : StairGap → StairCoord :=
  fun l => ⟨subStair l.1, subStair_weakDec l.1 l.2.1 l.2.2⟩

def addStairMap : StairCoord → StairGap :=
  fun m => ⟨addStair m.1, addStair_pos m.1, addStair_gap m.1 m.2⟩

theorem addStairMap_subStairMap (l : StairGap) : addStairMap (subStairMap l) = l := by
  apply Subtype.ext
  exact addStair_subStair l.1 l.2.1 l.2.2

theorem subStairMap_addStairMap (m : StairCoord) : subStairMap (addStairMap m) = m := by
  apply Subtype.ext
  exact subStair_addStair m.1

/-- A packaged bijection (core Lean has no `Equiv`; this is the same four fields). -/
structure StairBridge where
  toFun : StairGap → StairCoord
  invFun : StairCoord → StairGap
  left_inv : ∀ l, invFun (toFun l) = l
  right_inv : ∀ m, toFun (invFun m) = m

def stairBridge : StairBridge where
  toFun := subStairMap
  invFun := addStairMap
  left_inv := addStairMap_subStairMap
  right_inv := subStairMap_addStairMap

/-- The subtype form of "length retained, weight drops by `k * k`". -/
theorem subStairMap_facts (l : StairGap) :
    (subStairMap l).1.length = l.1.length ∧
      (subStairMap l).1.sum = l.1.sum - l.1.length * l.1.length :=
  subStair_length_sum l.1 l.2.1 l.2.2

/-! ## Witnesses: the new statements are not vacuous, and the hypotheses are needed -/

theorem witness_41 : subStair [4, 1] = [1, 0] := rfl

theorem witness_weakDec_41 : WeakDec (subStair [4, 1]) :=
  subStair_weakDec [4, 1]
    (by intro x hx; simp only [List.mem_cons, List.not_mem_nil, or_false] at hx
        rcases hx with rfl | rfl <;> omega)
    (show Gap [4, 1] from ⟨by decide, trivial⟩)

/-- Negative control: `Pos` alone does not give the order law.  `[1,3]` is
positive but not a gap partition, and its staircase image `[0,2]` is *not*
weakly decreasing.  So `Gap` is doing real work in `subStair_weakDec`. -/
theorem witness_gap_hypothesis_needed : ¬ WeakDec (subStair [1, 3]) := by
  intro h
  exact absurd h.1 (by decide)

/-- Padding witnesses: `subStair [5,3,1] = [0,0,0]`, the first coordinate is
already `0`, and the remaining ones are all `0`. -/
theorem witness_padding : AllZero [0, 0] :=
  subStair_zero_tail (lam := [5, 3, 1]) (a := 0) (rest := [0, 0])
    (by intro x hx; simp only [List.mem_cons, List.not_mem_nil, or_false] at hx
        rcases hx with rfl | rfl | rfl <;> omega)
    (show Gap [5, 3, 1] from ⟨by decide, ⟨by decide, trivial⟩⟩) rfl rfl

/-- Padding carries the length: dropping a trailing zero is *not* harmless,
because `addStair` consumes the length.  Same positive part, different object. -/
theorem witness_padding_carries_length : addStair [1] ≠ addStair [1, 0] := by decide

end RR127

#print axioms RR127.subStair_weakDec
#print axioms RR127.addStair_pos
#print axioms RR127.addStair_gap
#print axioms RR127.allZero_of_weakDec_zero
#print axioms RR127.subStair_zero_tail
#print axioms RR127.subStair_length_sum
#print axioms RR127.addStair_length_sum
#print axioms RR127.addStairMap_subStairMap
#print axioms RR127.subStairMap_addStairMap
#print axioms RR127.nonneg_is_vacuous
#print axioms RR127.subStairMap_facts
#print axioms RR127.witness_41
#print axioms RR127.witness_weakDec_41
#print axioms RR127.witness_gap_hypothesis_needed
#print axioms RR127.witness_padding
#print axioms RR127.witness_padding_carries_length
