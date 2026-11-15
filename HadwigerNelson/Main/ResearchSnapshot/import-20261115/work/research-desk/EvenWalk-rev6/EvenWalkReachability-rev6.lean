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
point outside `A`, and what has to be proved there is
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
  ⟨0, ⟨0, rfl⟩, fun _ => p, unitWalk_zero hp⟩

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
    show ‖z (n - i) - z (n - (i + 1))‖ = 1
    rw [he]
    simpa [norm_sub_rev] using hzedge (n - (i + 1)) hlt
  · intro i hi
    exact hzmem (n - i) (Nat.sub_le n i)

/-- Concatenation of two index sequences glued at `m`: the first sequence up to `m`, the second
(index-shifted) afterwards.  Named so that rewrites can see the `if` inside the applied lambda. -/
def catSeq (m : ℕ) (z w : ℕ → ℂ) (i : ℕ) : ℂ := if i ≤ m then z i else w (i - m)

lemma catSeq_of_le {m : ℕ} {z w : ℕ → ℂ} {i : ℕ} (h : i ≤ m) : catSeq m z w i = z i := by
  simp [catSeq, h]

lemma catSeq_of_gt {m : ℕ} {z w : ℕ → ℂ} {i : ℕ} (h : ¬ i ≤ m) : catSeq m z w i = w (i - m) := by
  simp [catSeq, h]

lemma evenJoin_trans {W : Set ℂ} {p q r : ℂ} (h₁ : EvenJoin W p q) (h₂ : EvenJoin W q r) :
    EvenJoin W p r := by
  obtain ⟨m, hm, z, hz0, hzm, hzedge, hzmem⟩ := h₁
  obtain ⟨n, hn, w, hw0, hwn, hwedge, hwmem⟩ := h₂
  refine ⟨m + n, hm.add hn, catSeq m z w, ?_, ?_, ?_, ?_⟩
  · -- starting point
    rw [catSeq_of_le (i := 0) (Nat.zero_le m)]
    exact hz0
  · -- end point; the glued index `m + n` is `≤ m` only when `n = 0`, and then `q = r`
    rcases Nat.eq_zero_or_pos n with hn0 | hnpos
    · have hqr : q = r := by
        have h : w n = w 0 := by rw [hn0]
        rw [h] at hwn
        exact hw0.symm.trans hwn
      rw [catSeq_of_le (i := m + n) (by omega), show m + n = m by omega, hzm, hqr]
    · rw [catSeq_of_gt (i := m + n) (by omega), show m + n - m = n by omega]
      exact hwn
  · -- the edges, including the junction `i = m` where `z m = q = w 0`
    intro i hi
    by_cases h2 : i ≤ m
    · by_cases h1 : i + 1 ≤ m
      · rw [catSeq_of_le (i := i) h2, catSeq_of_le (i := i + 1) h1]
        exact hzedge i (by omega)
      · have him : i = m := by omega
        rw [catSeq_of_le (i := i) h2, catSeq_of_gt (i := i + 1) h1, him, hzm,
          show m + 1 - m = 1 by omega, ← hw0]
        exact hwedge 0 (by omega)
    · rw [catSeq_of_gt (i := i) h2, catSeq_of_gt (i := i + 1) (by omega),
        show i + 1 - m = (i - m) + 1 by omega]
      exact hwedge (i - m) (by omega)
  · -- every vertex of the concatenation lies in `W`
    intro i hi
    by_cases h1 : i ≤ m
    · rw [catSeq_of_le (i := i) h1]
      exact hzmem i h1
    · rw [catSeq_of_gt (i := i) h1]
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
  -- `evenPath` is `Fin 5`-indexed, so the sequence is defined by `dite` on `i ≤ 4`; the value at
  -- `i = 5` is never used (the walk has length 4).  No `min`-clamp sits inside a `Fin` proof term,
  -- which is what made rev3/rev4 fail with "motive is not type correct".
  let Z : ℕ → ℂ := fun i => if h : i ≤ 4 then q' + evenPath (r - q) w (q - q') ⟨i, by omega⟩ else q
  refine ⟨4, by norm_num, Z, ?_, ?_, ?_, ?_⟩
  · -- `Z 0 = q'`
    simp only [Z, dif_pos (show (0 : ℕ) ≤ 4 by norm_num)]
    simp [evenPath]
  · -- `Z 4 = q` (the `evenPath` endpoint is `h = q - q'`)
    simp only [Z, dif_pos (show (4 : ℕ) ≤ 4 by norm_num)]
    simp [evenPath]
  · -- the edges, including the junction
    intro i hi
    have hi4 : i ≤ 4 := by omega
    have hi4' : i + 1 ≤ 4 := by omega
    simp only [Z, dif_pos hi4, dif_pos hi4']
    -- `evenPath_edges` concludes `∀ i : Fin 4, ‖evenPath v w h i.castSucc - evenPath v w h i.succ‖ = 1`;
    -- `⟨i,hi⟩.castSucc` and `⟨i,hi⟩.succ` are `⟨i,_⟩` and `⟨i+1,_⟩` definitionally.
    -- Fallbacks: `exact hedges ⟨i, hi⟩` by defeq, or `ring` for the `q' + ·` cancellation.
    simpa only [Fin.castSucc_mk, Fin.succ_mk, add_sub_add_left_eq_sub] using hedges ⟨i, hi⟩
  · -- every vertex lies in `W`; `hmem`'s type prints the parity `if` which `ite_self` removes
    intro i hi
    have hi4 : i ≤ 4 := by omega
    simp only [Z, dif_pos hi4]
    simpa only [ite_self] using hmem ⟨i, by omega⟩

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
    -- Closedness via the OPEN COMPLEMENT, with the same local epsilon-lemma: if
    -- `x` lies outside `A` then a nearby `y` of `T` cannot lie in `A` either,
    -- because `EvenJoin W p y.val` would compose with the local walk
    -- `EvenJoin W y.val x.val` to put `x` in `A`.  No `closure` and no
    -- `Subtype.val` inference is involved.
    apply isOpen_compl_iff.mp
    rw [isOpen_iff_forall_mem_open]
    intro x hx
    obtain ⟨ε, hε, hstep⟩ := evenJoin_near hW (hTW x.2) (hact x.val x.2)
    refine ⟨Subtype.val ⁻¹' Metric.ball x.val ε, ?_,
      Metric.isOpen_ball.preimage continuous_subtype_val, by simp [hε]⟩
    intro y hy hyA
    rw [Set.mem_preimage, Metric.mem_ball, dist_eq_norm] at hy
    have h1 : EvenJoin W y.val x.val :=
      hstep y.val (hTW y.2) (by simpa [norm_sub_rev] using hy)
    exact hx (evenJoin_trans hyA h1)
  haveI : PreconnectedSpace ↥T := isPreconnected_iff_preconnectedSpace.mp hpre
  have hne : A.Nonempty := ⟨⟨p, hp⟩, hpa⟩
  -- in this Mathlib `IsClopen s` is `IsClosed s ∧ IsOpen s` (Mathlib/Topology/Defs/Basic.lean:112)
  have hclopen : IsClopen A := ⟨hAclosed, hAopen⟩
  have huniv : A = univ := by
    rcases isClopen_iff.mp hclopen with h | h
    · exact absurd (h ▸ hne) Set.not_nonempty_empty
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
    states_densityOne (c := c) (hc := hc) (hw := hw) (x := x v) (A := A v) (B := B v)
      (J := J v) (K := K v) (t := t v) (u := u v) (hA v) (hB v) (ht v) (hu v) (hne v)

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
  have hbc : b ≠ c := fun h => hcb h.symm
  have hcard : ({b, c} : Finset (Fin k)).card = 2 := by
    rw [Finset.card_insert_of_notMem (by simpa using hbc), Finset.card_singleton]
  have hcard3 : ({a, b, c} : Finset (Fin k)).card = 3 := by
    rw [Finset.card_insert_of_notMem (by simp [hab, Ne.symm hca]), hcard]
  have := Finset.card_le_card hsub
  omega

/-- **Parity, Fin-indexed.**  If every vertex of a walk carries the two-element list
`J` and consecutive colours differ, then the colour at position `m` equals the colour at
position `0` exactly when `m` is even.  The indices are `Fin (N+1)` throughout, so no
`min`-clamping is needed and no `Fin`-versus-`ℕ` coercion is left to `omega`. -/
lemma two_list_sequence_parity {k : ℕ} {J : Finset (Fin k)} (hJ : J.card ≤ 2) {N : ℕ}
    {g : Fin (N + 1) → Fin k} (hg : ∀ v, g v ∈ J)
    (hstep : ∀ i : Fin N, g i.castSucc ≠ g i.succ) :
    ∀ m : ℕ, ∀ hm : m ≤ N, (g ⟨m, Nat.lt_succ_of_le hm⟩ = g 0 ↔ Even m) := by
  intro m
  induction m with
  | zero =>
      intro hm
      exact ⟨fun _ => ⟨0, rfl⟩, fun _ => rfl⟩
  | succ m ihm =>
      intro hm
      have hmN : m ≤ N := by omega
      have ihm' := ihm hmN
      -- the step is taken at the index `m : Fin N`
      have hstepm : g (⟨m, Nat.lt_succ_of_le hmN⟩ : Fin (N + 1)) ≠
          g ⟨m + 1, Nat.lt_succ_of_le hm⟩ := by
        have h := hstep ⟨m, by omega⟩
        -- `Fin.castSucc_mk`/`Fin.succ_mk` exist; the fallback is `exact hstep ⟨m, by omega⟩`
        -- (both casts reduce definitionally on `Fin.mk`).
        simpa only [Fin.castSucc_mk, Fin.succ_mk] using h
      constructor
      · -- forward: equal colours force `m` odd, i.e. `m + 1` even fails
        intro h
        have hne : g ⟨m, Nat.lt_succ_of_le hmN⟩ ≠ g 0 := fun h0 => hstepm (h0.trans h.symm)
        have hodd : ¬ Even m := fun he => hne (ihm'.mpr he)
        exact Nat.even_add_one.mpr hodd
      · -- backward: `m + 1` even forces `m` odd, hence the colour must jump to `g 0`
        intro he
        have hodd : ¬ Even m := by
          intro he'
          obtain ⟨r, hr⟩ := he'
          obtain ⟨t, ht⟩ := he
          omega
        have hne0 : g ⟨m, Nat.lt_succ_of_le hmN⟩ ≠ g 0 := fun h0 => hodd (ihm'.mp h0)
        rcases eq_or_eq_of_mem_card_le_two hJ
          (hg ⟨m, Nat.lt_succ_of_le hmN⟩) (hg 0) (hg ⟨m + 1, Nat.lt_succ_of_le hm⟩)
          hne0 with h | h
        · exact absurd h.symm hstepm
        · exact h

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

/-- **Two-list parity obstruction.**  If the vertices of an even unit-distance walk all
carry the same two-element list, then its endpoints cannot be at unit distance: parity of
the walk forces equal colours at the two ends, while the closing unit edge forces
different ones. -/
theorem two_list_obstruction_of_even_walk {k : ℕ} {c : ℂ → Fin k} (hc : Measurable c)
    (hw : WeakColoring k c) {n : ℕ} (hn : Even n) (z : Fin (n + 1) → ℂ) {J : Finset (Fin k)}
    (hJ : J.card ≤ 2)
    (hedge : ∀ i : Fin n, ‖z i.castSucc - z i.succ‖ = 1)
    (hd : ∀ v : Fin (n + 1), DensityOne {q : ℂ | c q ∈ J} (z v))
    (hclose : ‖z 0 - z ⟨n, Nat.lt_succ_self n⟩‖ = 1) : False := by
  classical
  obtain ⟨q, hq, hdiff⟩ := finite_density_realization hc hw z (fun _ => J) hd
  -- the colour of the translate at each vertex, indexed by `Fin (n+1)` (no clamping)
  set g : Fin (n + 1) → Fin k := fun v => c (q + z v) with hg
  have hgmem : ∀ v, g v ∈ J := fun v => hq v
  have hstep : ∀ i : Fin n, g i.castSucc ≠ g i.succ := by
    intro i
    have h1 : ‖z i.castSucc - z i.succ‖ = 1 := hedge i
    have h2 : c (q + z i.castSucc) ≠ c (q + z i.succ) := hdiff i.castSucc i.succ h1
    simpa only [hg] using h2
  have hpar := two_list_sequence_parity hJ hgmem hstep n (le_refl n)
  have hgn : g ⟨n, Nat.lt_succ_self n⟩ = g 0 := hpar.mpr hn
  have hne := hdiff 0 ⟨n, Nat.lt_succ_self n⟩ hclose
  exact hne (by simpa only [hg] using hgn.symm)

end EuclideanFiveColor
end

end OAI

#print axioms OAI.EuclideanFiveColor.evenWalk_reachable
#print axioms OAI.EuclideanFiveColor.finite_list_obstruction
#print axioms OAI.EuclideanFiveColor.two_list_obstruction_of_even_walk
