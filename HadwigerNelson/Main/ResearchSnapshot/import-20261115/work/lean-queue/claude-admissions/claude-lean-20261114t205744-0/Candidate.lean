import OAI.Geometry.PlaneColoring.Rigidity
import OAI.Geometry.PlaneColoring.States

/-!
# Even unit-distance walks: reachability, and the finite list obstruction

Source only: this file is *not* built here.

## 1. Reachability (`evenWalk_reachable`)

If `W ⊆ ℂ` is open, `T ⊆ W` is connected, and every point of `T` has a unit
neighbour in `W`, then any two points of `T` are joined by a finite
*even*-length unit-distance walk inside `W`.

The local step is the four-edge `evenPath` of
`OAI.Geometry.PlaneColoring.Rigidity`:
* `open_two_unit_directions` produces, from the unit neighbour of the base
  point, a second non-parallel unit direction inside `W`;
* `evenPath_local` gives radii `r > 0`, `δ > 0` such that the four-edge path
  `q' + evenPath v w h` has all five vertices in `W` for `q'` in the `r`-ball
  and `‖h‖ < δ`;
* `evenPath_edges` gives that its four edges have length exactly one.

Since `evenPath v w h 0 = 0` and `evenPath v w h 4 = h`, the choice `h = q - q'`
gives a four-edge unit walk from `q'` to `q` inside `W`: the local step is
*even*.  The global step is the standard open-and-closed argument: for fixed
`p ∈ T` the set of points of `T` reachable from `p` by an even walk is clopen in
`T`, hence all of `T` (`isClopen_iff` inside the preconnected space `↥T`).

Note on the closedness half of that argument: it must call `evenJoin_near` at
`x.val` itself, never the derived `hnear` (whose input is a member of `A`).  A
point of `closure A` need not belong to `A`, and what has to be proved there is
`EvenJoin W p x.val`, not membership of the nearby point.

## 2. The consumer chain (`finite_list_obstruction`)

`listDensity_of_states` turns the two-real-states input into full planar density
of each vertex list (this is `States.states_densityOne`), and
`finite_density_realization` then produces one point `q` whose colouring respects
every list and differs on every unit pair.  Hence a finite unit-distance pattern
that is not list-colourable does not exist (`finite_list_obstruction`).  The
parity corollary `two_list_obstruction_of_even_walk` is the two-list form: an
*even* walk whose vertices all carry the same two-element list cannot have its
endpoints at unit distance.

No `sorry`, no `admit`, no `axiom`, no `opaque`, no `native_decide`.  Every
ingredient is either proved here or one of the cited declarations of
`Rigidity.lean` / `States.lean`; no missing source fact is asserted.
-/

namespace OAI

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor

/-! ### 1. Walks -/

/-- `UnitWalk W p q n z` says: `z` is a unit-distance walk from `p` to `q` with
`n` unit edges, all of whose vertices lie in `W`. -/
def UnitWalk (W : Set ℂ) (p q : ℂ) (n : ℕ) (z : ℕ → ℂ) : Prop :=
  z 0 = p ∧ z n = q ∧ (∀ i < n, ‖z i - z (i+1)‖ = 1) ∧ ∀ i ≤ n, z i ∈ W

/-- `p` and `q` are joined by a finite even-length unit-distance walk in `W`. -/
def EvenJoin (W : Set ℂ) (p q : ℂ) : Prop :=
  ∃ n : ℕ, Even n ∧ ∃ z : ℕ → ℂ, UnitWalk W p q n z

lemma unitWalk_zero {W : Set ℂ} {p : ℂ} (hp : p ∈ W) :
    UnitWalk W p p 0 (fun _ => p) := by
  refine ⟨rfl, rfl, ?_, ?_⟩
  · intro i hi
    exact absurd hi (Nat.not_lt_zero i)
  · intro i hi
    have hi0 : i = 0 := by omega
    subst hi0
    exact hp

lemma evenJoin_refl {W : Set ℂ} {p : ℂ} (hp : p ∈ W) : EvenJoin W p p :=
  ⟨0, Nat.even_zero, fun _ => p, unitWalk_zero hp⟩

lemma evenJoin_symm {W : Set ℂ} {p q : ℂ} (h : EvenJoin W p q) : EvenJoin W q p := by
  obtain ⟨n, hn, z, hz0, hzn, hzedge, hzmem⟩ := h
  refine ⟨n, hn, fun i => z (n - i), ?_, ?_, ?_, ?_⟩
  · show z (n - 0) = q
    simpa using hzn
  · show z (n - n) = p
    simpa using hz0
  · intro i hi
    have hlt : n - (i + 1) < n := by omega
    have he : n - i = n - (i + 1) + 1 := by omega
    rw [he]
    simpa [norm_sub_rev] using hzedge (n - (i + 1)) hlt
  · intro i hi
    exact hzmem (n - i) (Nat.sub_le n i)

lemma evenJoin_trans {W : Set ℂ} {p q r : ℂ} (h₁ : EvenJoin W p q) (h₂ : EvenJoin W q r) :
    EvenJoin W p r := by
  obtain ⟨m, hm, z, hz0, hzm, hzedge, hzmem⟩ := h₁
  obtain ⟨n, hn, w, hw0, hwn, hwedge, hwmem⟩ := h₂
  have hqr : q = r := by rw [← hw0, hwn]
  refine ⟨m + n, hm.add hn, fun i => if i ≤ m then z i else w (i - m), ?_, ?_, ?_, ?_⟩
  · show (if 0 ≤ m then z 0 else w (0 - m)) = p
    rw [if_pos (Nat.zero_le m)]
    exact hz0
  · rcases Nat.eq_zero_or_pos n with hn0 | hnpos
    · have hmn : m + n = m := by omega
      rw [if_pos (by omega), hmn, hzm, hqr]
    · rw [if_neg (by omega), show m + n - m = n by omega]
      exact hwn
  · intro i hi
    by_cases h1 : i ≤ m
    · by_cases h1' : i + 1 ≤ m
      · rw [if_pos h1, if_pos h1']
        exact hzedge i (by omega)
      · -- the junction: `i = m`, and `w 0 = q`
        have him : i = m := by omega
        rw [if_pos h1, if_neg h1', him, hzm,
          show m + 1 - m = 1 by omega, ← hw0]
        exact hwedge 0 (by omega)
    · rw [if_neg h1, if_neg (by omega), show i + 1 - m = (i - m) + 1 by omega]
      exact hwedge (i - m) (by omega)
  · intro i hi
    by_cases h1 : i ≤ m
    · rw [if_pos h1]
      exact hzmem i h1
    · rw [if_neg h1]
      exact hwmem (i - m) (by omega)

/-! ### 1b. The local four-edge step -/

/-- **Local even step.**  Every point of `W` that has a unit neighbour in `W` is
even-reachable from all points of `W` that are close enough to it.  The walk is
the four-edge `evenPath` of `Rigidity.lean` taken with `h = q - q'`. -/
theorem evenJoin_near {W : Set ℂ} (hW : IsOpen W) {q : ℂ} (hqW : q ∈ W)
    (hact : ∃ r ∈ W, ‖q - r‖ = 1) :
    ∃ ε > 0, ∀ q' ∈ W, ‖q' - q‖ < ε → EvenJoin W q' q := by
  obtain ⟨r, hrW, hr⟩ := hact
  have hv : ‖r - q‖ = 1 := by simpa [norm_sub_rev] using hr
  have hqv : q + (r - q) ∈ W := by simpa using hrW
  obtain ⟨w, hqw, hw, hwd⟩ := open_two_unit_directions hW hv hqv
  obtain ⟨ρ, hρ, δ, hδ, hloc⟩ := evenPath_local (U := W) (V := W) hW hW hqW hqv hqw
  refine ⟨min ρ δ, lt_min hρ hδ, ?_⟩
  intro q' hq'W hq'
  have hρ' : q' ∈ Metric.ball q ρ := by
    rw [Metric.mem_ball, dist_eq_norm]
    exact lt_of_lt_of_le hq' (min_le_left ρ δ)
  have hδ' : ‖q - q'‖ < δ := by
    have h : ‖q' - q‖ < δ := lt_of_lt_of_le hq' (min_le_right ρ δ)
    simpa [norm_sub_rev] using h
  obtain ⟨hsmall₁, hsmall₂, hmem⟩ := hloc q' (q - q') hρ' hδ'
  have hedges := evenPath_edges hv hw hwd hsmall₁ hsmall₂
  refine ⟨4, by norm_num, fun i => q' + evenPath (r - q) w (q - q') i, ?_, ?_, ?_, ?_⟩
  · show q' + evenPath (r - q) w (q - q') 0 = q'
    simp [evenPath]
  · show q' + evenPath (r - q) w (q - q') 4 = q
    simp [evenPath]
  · intro i hi
    have := hedges ⟨i, hi⟩
    rw [← add_sub_add_left_eq_sub, ← add_sub_add_left_eq_sub]
    exact this
  · intro i hi
    have hi5 : i < 5 := by omega
    have := hmem ⟨i, hi5⟩
    simpa using this

/-! ### 1c. Global reachability -/

/-- **Even-walk reachability.**  Let `W` be open, `T ⊆ W` connected, and let
every point of `T` have a unit neighbour in `W`.  Then any two points of `T`
are joined by a finite even-length unit-distance walk in `W`. -/
theorem evenWalk_reachable {W : Set ℂ} (hW : IsOpen W) {T : Set ℂ} (hT : IsConnected T)
    (hTW : T ⊆ W) (hact : ∀ p ∈ T, ∃ q ∈ W, ‖p - q‖ = 1) :
    ∀ p ∈ T, ∀ q ∈ T, EvenJoin W p q := by
  classical
  have hpre : IsPreconnected T := hT.isPreconnected
  intro p hp q hq
  set A : Set ↥T := {x | EvenJoin W p x.val} with hA
  have hpa : (⟨p, hp⟩ : ↥T) ∈ A := evenJoin_refl (hTW hp)
  have hnear : ∀ x ∈ A, ∃ ε > 0, ∀ y : ↥T, ‖y.val - x.val‖ < ε → y ∈ A := by
    intro x hxA
    obtain ⟨ε, hε, hloc⟩ := evenJoin_near hW (hTW x.2) (hact x.val x.2)
    refine ⟨ε, hε, ?_⟩
    intro y hy
    have hyW : y.val ∈ W := hTW y.2
    have h1 : EvenJoin W y.val x.val := hloc y.val hyW (by simpa [norm_sub_rev] using hy)
    -- `hxA : EvenJoin W p x.val` is the hypothesis bound at the `intro`; `x.2` is only
    -- membership in `T` and is NOT an `EvenJoin`, so it cannot be passed here.
    exact evenJoin_trans hxA (evenJoin_symm h1)
  have hAopen : IsOpen A := by
    rw [isOpen_iff_forall_mem_open]
    intro x hx
    obtain ⟨ε, hε, hball⟩ := hnear x hx
    refine ⟨Subtype.val ⁻¹' Metric.ball x.val ε, ?_,
      Metric.isOpen_ball.preimage continuous_subtype_val, by simp [hε]⟩
    intro y hy
    rw [Set.mem_preimage, Metric.mem_ball, dist_eq_norm] at hy
    exact hball y hy
  have hAclosed : IsClosed A := by
    -- Closedness must use `evenJoin_near` at `x.val` itself, *not* `hnear`: a point
    -- of `closure A` need not lie in `A`, so `hnear` (whose input is a member of
    -- `A`) is not available here, and the conclusion wanted is `x ∈ A`, not `y ∈ A`.
    rw [← closure_subset_iff_isClosed]
    intro x hx
    obtain ⟨ε, hε, hstep⟩ := evenJoin_near hW (hTW x.2) (hact x.val x.2)
    have hopen : IsOpen (Subtype.val ⁻¹' Metric.ball x.val ε) :=
      Metric.isOpen_ball.preimage continuous_subtype_val
    have hxmem : x ∈ Subtype.val ⁻¹' Metric.ball x.val ε := by simp [hε]
    obtain ⟨y, hyb, hyA⟩ := Set.mem_closure_iff.mp hx _ hopen hxmem
    rw [Set.mem_preimage, Metric.mem_ball, dist_eq_norm] at hyb
    exact evenJoin_trans hyA (hstep y.val (hTW y.2) hyb)
  haveI : PreconnectedSpace ↥T := isPreconnected_iff_preconnectedSpace.mp hpre
  have hne : A.Nonempty := ⟨⟨p, hp⟩, hpa⟩
  have huniv : A = univ := by
    rcases isClopen_iff.mp ⟨hAopen, hAclosed⟩ with h | h
    · exact absurd (h ▸ hne) (not_nonempty_empty)
    · exact h
  have : (⟨q, hq⟩ : ↥T) ∈ A := by rw [huniv]; exact mem_univ _
  exact this

/-! ### 2. The consumer chain -/

/-- Full planar density of each vertex list, at that vertex.  In the geometric
application this is produced by `listDensity_of_states`, i.e. by
`States.states_densityOne`. -/
def ListDensity {ι : Type*} (c : ℂ → Fin k) (z : ι → ℂ) (L : ι → Finset (Fin k)) : Prop :=
  ∀ v : ι, DensityOne {q : ℂ | c q ∈ L v} (z v)

/-- `states_densityOne` in the form needed by the walk consumer: the two real
states attached to a vertex, at the two representation angles, give full density
of that vertex's list `(J v ∪ K v)ᶜ` at the vertex. -/
lemma listDensity_of_states {k : ℕ} {c : ℂ → Fin k} (hc : Measurable c)
    (hw : WeakColoring k c) {ι : Type*} (x : ι → ℂ) (t u : ι → ℝ)
    (A B : ι → Set ℝ) (J K : ι → Finset (Fin k))
    (hA : ∀ v, RealState hc (x v) (A v) (J v)) (hB : ∀ v, RealState hc (x v) (B v) (K v))
    (ht : ∀ v, LineDensityZero (A v)ᶜ (t v)) (hu : ∀ v, LineDensityZero (B v)ᶜ (u v))
    (hne : ∀ v, Real.sin (u v - t v) ≠ 0) :
    ListDensity c (fun v => angularSum (x v) 1 (angleChart (t v, u v)))
      (fun v => (J v ∪ K v)ᶜ) := by
  intro v
  simpa only [ListDensity, Finset.mem_compl] using
    states_densityOne hw (hA v) (hB v) (ht v) (hu v) (hne v)

/-- Two elements of a two-element finset: a member distinct from one of two
distinct members must be the other one. -/
lemma eq_or_eq_of_mem_card_le_two {k : ℕ} {J : Finset (Fin k)} (hJ : J.card ≤ 2) {a b c : Fin k}
    (ha : a ∈ J) (hb : b ∈ J) (hc : c ∈ J) (hab : a ≠ b) : c = a ∨ c = b := by
  by_contra h
  push_neg at h
  obtain ⟨hca, hcb⟩ := h
  have hsub : ({a, b, c} : Finset (Fin k)) ⊆ J := by
    intro x hx
    simp only [Finset.mem_insert, Finset.mem_singleton] at hx
    rcases hx with rfl | rfl | rfl
    · exact ha
    · exact hb
    · exact hc
  have hcard : ({b, c} : Finset (Fin k)).card = 2 := by simp [hcb]
  have hcard3 : ({a, b, c} : Finset (Fin k)).card = 3 := by
    rw [Finset.card_insert_of_notMem (by simp [hab, Ne.symm hca]), hcard]
  have := Finset.card_le_card hsub
  omega

/-- **Parity.**  Along a sequence of two-list vertices with adjacent colours
distinct, the colour equals `f 0` exactly at the even positions. -/
lemma two_list_sequence_parity {k : ℕ} {J : Finset (Fin k)} (hJ : J.card ≤ 2)
    {f : ℕ → Fin k} {N : ℕ} (hf : ∀ i ≤ N, f i ∈ J) (hstep : ∀ i < N, f i ≠ f (i+1)) :
    ∀ i ≤ N, (f i = f 0 ↔ Even i) := by
  intro i hiN
  induction i with
  | zero => simp
  | succ j ih =>
    have hj : j ≤ N := by omega
    have ih' := ih hj
    constructor
    · intro h
      have hne : f j ≠ f (j + 1) := hstep j (by omega)
      have hjn : f j ≠ f 0 := fun hj0 => hne (hj0.trans h.symm)
      have : ¬ Even j := by simpa [ih'] using hjn
      omega
    · intro h
      have hodd : ¬ Even j := by omega
      have hjn : f j ≠ f 0 := by simpa [ih'] using hodd
      have hne : f j ≠ f (j + 1) := hstep j (by omega)
      rcases eq_or_eq_of_mem_card_le_two hJ (hf j hj) (hf 0 (Nat.zero_le N))
        (hf (j + 1) (by omega)) hjn with h1 | h1
      · exact absurd h1 hne
      · exact h1

/-- **Finite list obstruction.**  A finite unit-distance pattern whose vertices
carry lists of full planar density and which admits no list-respecting proper
colouring is impossible: `finite_density_realization` exhibits a translate of the
whole pattern that is simultaneously coloured inside every list and properly,
contradicting the combinatorial hypothesis. -/
theorem finite_list_obstruction {k : ℕ} {c : ℂ → Fin k} (hc : Measurable c)
    (hw : WeakColoring k c) {ι : Type*} [Finite ι] (z : ι → ℂ) (L : ι → Finset (Fin k))
    (hd : ListDensity c z L)
    (hno : ∀ f : ι → Fin k, (∀ v, f v ∈ L v) →
      ∃ v w : ι, ‖z v - z w‖ = 1 ∧ f v = f w) : False := by
  obtain ⟨q, hq, hdiff⟩ := finite_density_realization hc hw z L hd
  obtain ⟨v, w, hvw, heq⟩ := hno (fun v => c (q + z v)) (fun v => hq v)
  exact hdiff v w hvw heq

/-- **Two-list parity obstruction.**  If the vertices of an even unit-distance
walk all carry the same two-element list, then its endpoints cannot be at unit
distance: parity of the walk forces equal colours at the two ends, while the
closing unit edge forces different ones. -/
theorem two_list_obstruction_of_even_walk {k : ℕ} {c : ℂ → Fin k} (hc : Measurable c)
    (hw : WeakColoring k c) {n : ℕ} (hn : Even n) (z : Fin (n + 1) → ℂ) {J : Finset (Fin k)}
    (hJ : J.card ≤ 2)
    (hedge : ∀ i : Fin n, ‖z i.castSucc - z i.succ‖ = 1)
    (hd : ∀ v : Fin (n + 1), DensityOne {q : ℂ | c q ∈ J} (z v))
    (hclose : ‖z 0 - z ⟨n, Nat.lt_succ_self n⟩‖ = 1) : False := by
  classical
  obtain ⟨q, hq, hdiff⟩ := finite_density_realization hc hw z (fun _ => J) hd
  set f : ℕ → Fin k := fun i => c (q + z ⟨min i n, by omega⟩) with hf
  have hfmem : ∀ i ≤ n, f i ∈ J := fun i _ => hq _
  have hstep : ∀ i < n, f i ≠ f (i + 1) := by
    intro i hi
    have h1 : (⟨min i n, by omega⟩ : Fin (n + 1)) = i.castSucc :=
      Fin.ext (by simp [Nat.min_eq_left (by omega)])
    have h2 : (⟨min (i + 1) n, by omega⟩ : Fin (n + 1)) = i.succ :=
      Fin.ext (by simp [Nat.min_eq_left (by omega)])
    have hne := hdiff _ _ (hedge ⟨i, hi⟩)
    simpa only [hf, h1, h2] using hne
  have hpar := two_list_sequence_parity hJ hfmem hstep n (le_refl n)
  have hfn : f n = f 0 := hpar.mpr hn
  have h0 : (⟨min 0 n, by omega⟩ : Fin (n + 1)) = 0 := Fin.ext (by simp)
  have hn' : (⟨min n n, by omega⟩ : Fin (n + 1)) = ⟨n, Nat.lt_succ_self n⟩ := Fin.ext (by simp)
  have hne := hdiff 0 ⟨n, Nat.lt_succ_self n⟩ hclose
  exact hne (by simpa only [hf, h0, hn'] using hfn)

end EuclideanFiveColor
end

end OAI
