import OAI.Analysis.PlaneSpectrum.NumberFields

namespace OAI

noncomputable section
open Module
namespace EuclideanFiveColor.GeneralPosition
variable {V : Type*} [AddCommGroup V] [Module ℚ V] [FiniteDimensional ℚ V]

/-- A cover evaluated at a large general-position set contains a spanning monochromatic subset. -/
lemma spanning_selection {ι : Type*} (Q : Finset ι) (S : Finset V) (hS : General S)
    (hcard : Q.card*(finrank ℚ V-1) < S.card)
    (A : ι → V → Prop) (hA : ∀ x ∈ S, ∃ i ∈ Q, A i x) :
    ∃ i ∈ Q, ∃ T ⊆ S, T.card = finrank ℚ V ∧
      Submodule.span ℚ (T : Set V) = ⊤ ∧ ∀ x ∈ T, A i x := by
  classical
  choose f hfQ hfA using fun x : S => hA x x.property
  have hs : Fintype.card Q * (finrank ℚ V-1) < Fintype.card S := by simpa using hcard
  let g : S → Q := fun x => ⟨f x,hfQ x⟩
  obtain ⟨i,hi⟩ := Fintype.exists_lt_card_fiber_of_mul_lt_card g hs
  have hi' : finrank ℚ V ≤ (S.filter (fun x => A i x)).card := by
    have hx : (Finset.univ.filter (fun x : S => g x = i)).card ≤
        (S.filter (fun x => A i x)).card := by
      apply Finset.card_le_card_of_injOn (fun x : S => x.val)
      · intro x hx
        have hg : g x = i := (Finset.mem_filter.mp hx).2
        exact Finset.mem_filter.mpr ⟨x.property,by
          have hh := hfA x
          change A (g x).val x.val at hh
          rwa [hg] at hh⟩
      · intro x hx y hy hxy
        exact Subtype.ext hxy
    omega
  obtain ⟨T,hT,hTc⟩ := Finset.exists_subset_card_eq hi'
  have hTS : T ⊆ S := fun x hx => (Finset.mem_filter.mp (hT hx)).1
  exact ⟨i,i.property,T,hTS,hTc,hS.spans hTS hTc, fun x hx => (Finset.mem_filter.mp (hT hx)).2⟩
end EuclideanFiveColor.GeneralPosition
end

noncomputable section
namespace EuclideanFiveColor.Arithmetic


end EuclideanFiveColor.Arithmetic
end

noncomputable section
open Module
namespace EuclideanFiveColor.Arithmetic
open AlgebraicCayley GeneralPosition


/-- Uniform integral spanning selections extracted from the source's syndetic cover. -/
end EuclideanFiveColor.Arithmetic
end

noncomputable section
namespace EuclideanFiveColor.Arithmetic


end EuclideanFiveColor.Arithmetic
end

noncomputable section
namespace EuclideanFiveColor.CappedResidues
variable {α : Type*} [Field α] [LinearOrder α] [IsStrictOrderedRing α]
variable (m : α → ℝ) (hm0 : m 0 = 1)
  (hd : ∀ a b : α, 0 ≤ a → 0 ≤ b → m a * m b ≤ m |a-b|)
  (c : ℝ) (hc0 : 0 ≤ c) (hc1 : c ≤ 1)

def Good (n : ℕ) (x : α) : Prop := c^n ≤ m x
include hc0 hc1 in
omit [Field α] [LinearOrder α] [IsStrictOrderedRing α] in
include hm0 hc0 hc1 in
omit [LinearOrder α] [IsStrictOrderedRing α] in
include hd hc0 in
omit [IsStrictOrderedRing α] in

variable {p : α} (hp : 0 < p) (hpG : Good m c 1 p)
include hd hc0 hc1 hp hpG in

include hm0 hd hc0 hc1 hp hpG in

include hm0 hd hc0 hc1 hp hpG in

include hm0 hd hc0 hc1 hp hpG in
end EuclideanFiveColor.CappedResidues
end

noncomputable section
namespace EuclideanFiveColor.CappedResidues
variable {α : Type*} [Field α] [LinearOrder α] [IsStrictOrderedRing α]

def signedList (a : ℤ) (x : α) : List α :=
  match a with
  | .ofNat n => List.replicate n x
  | .negSucc n => List.replicate (n+1) (-x)
omit [LinearOrder α] [IsStrictOrderedRing α] in
@[simp] lemma signedList_length (a : ℤ) (x : α) : (signedList a x).length = a.natAbs := by
  cases a <;> simp [signedList]
omit [LinearOrder α] [IsStrictOrderedRing α] in
@[simp] lemma signedList_sum (a : ℤ) (x : α) : (signedList a x).sum = a • x := by
  cases a <;> simp [signedList]
  ring
omit [IsStrictOrderedRing α] in

omit [IsStrictOrderedRing α] in

variable (m : α → ℝ) (hm0 : m 0 = 1)
  (hd : ∀ a b : α, 0 ≤ a → 0 ≤ b → m a*m b ≤ m |a-b|)
  (c : ℝ) (hc0 : 0 ≤ c) (hc1 : c ≤ 1)
  {p : α} (hp : 0 < p) (hpG : Good m c 1 p)
include hm0 hd hc0 hc1 hp hpG in
include hm0 hd hc0 hc1 hp hpG in
end EuclideanFiveColor.CappedResidues
end

end OAI
