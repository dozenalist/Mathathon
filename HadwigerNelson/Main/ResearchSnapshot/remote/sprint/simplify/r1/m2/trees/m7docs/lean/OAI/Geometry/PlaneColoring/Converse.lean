import OAI.Geometry.PlaneColoring.States

set_option linter.style.haveILetI false

namespace OAI

noncomputable section
open MeasureTheory Filter Topology Set
namespace EuclideanFiveColor

theorem finite_config_proper {k : ℕ} {c : ℂ → Fin k} (hc : Measurable c) (hw : WeakColoring k c)
    {ι : Type*} [Finite ι] (z : ι → ℂ) :
    ∃ q : ℂ, ∀ v w : ι, ‖z v - z w‖ = 1 → c (q + z v) ≠ c (q + z w) := by
  classical
  have hone : ∀ v : ι, DensityOne (Set.univ : Set ℂ) (z v) := by
    intro v
    have hb : ∀ᶠ r : ℝ in 𝓝[>] (0:ℝ),
        volume ((Set.univ : Set ℂ) ∩ Metric.closedBall (z v) r) /
          volume (Metric.closedBall (z v) r) = 1 := by
      filter_upwards [self_mem_nhdsWithin] with r hr
      rw [Set.univ_inter,
        ENNReal.div_self (Metric.measure_closedBall_pos volume (z v) hr).ne'
          (isCompact_closedBall (z v) r).measure_ne_top]
    exact Filter.Tendsto.congr' (hb.mono fun r hr => hr.symm) tendsto_const_nhds
  obtain ⟨q, -, hq⟩ := finite_density_realization (k := k) (c := c) hc hw z
    (fun _ => Finset.univ) (fun v => by simpa using hone v)
  exact ⟨q, fun v w h => hq v w h⟩

theorem exists_properColoring_of_finset {k : ℕ} [NeZero k]
    (h : ∀ F : Finset ℂ, ∃ c : ℂ → Fin k,
      ∀ x ∈ F, ∀ y ∈ F, ‖x - y‖ = 1 → c x ≠ c y) :
    ∃ c : ℂ → Fin k, ProperColoring k c := by
  classical
  letI : CompactSpace (ℂ → Fin k) := Pi.compactSpace
  let t : ℂ × ℂ → Set (ℂ → Fin k) := fun p =>
    {c | c p.1 ≠ c p.2} ∪ {c | ¬ ‖p.1 - p.2‖ = 1}
  have ht : ∀ p, IsClosed (t p) := by
    intro p
    apply IsClosed.union
    · have hcont : Continuous (fun c : ℂ → Fin k => (c p.1, c p.2)) :=
        (continuous_apply p.1).prodMk (continuous_apply p.2)
      exact (isClosed_discrete {q : Fin k × Fin k | q.1 ≠ q.2}).preimage hcont
    · by_cases hd : ‖p.1 - p.2‖ = 1 <;> simp [hd]
  have hfip : ∀ u : Finset (ℂ × ℂ), (⋂ p ∈ u, t p).Nonempty := by
    intro u
    obtain ⟨c, hc⟩ := h (u.image Prod.fst ∪ u.image Prod.snd)
    refine ⟨c, ?_⟩
    simp only [mem_iInter, t]
    intro p hp
    have h1 : p.1 ∈ u.image Prod.fst ∪ u.image Prod.snd :=
      Finset.mem_union_left _ (Finset.mem_image_of_mem _ hp)
    have h2 : p.2 ∈ u.image Prod.fst ∪ u.image Prod.snd :=
      Finset.mem_union_right _ (Finset.mem_image_of_mem _ hp)
    by_cases hd : ‖p.1 - p.2‖ = 1
    · left
      exact hc p.1 h1 p.2 h2 hd
    · right; exact hd
  have hcomp : IsCompact (Set.univ : Set (ℂ → Fin k)) := isCompact_univ
  obtain ⟨c, -, hc⟩ := hcomp.inter_iInter_nonempty t ht (fun u => by simpa using hfip u)
  refine ⟨c, fun x y hxy => ?_⟩
  simp only [Set.mem_iInter] at hc
  have h1 : c ∈ t (x, y) := hc (x, y)
  simp only [t, mem_union] at h1
  rcases h1 with h1 | h1
  · exact h1
  · exact absurd hxy h1

theorem properColoring_of_weak {k : ℕ} [NeZero k] {c : ℂ → Fin k}
    (hc : Measurable c) (hw : WeakColoring k c) :
    ∃ d : ℂ → Fin k, ProperColoring k d := by
  classical
  apply exists_properColoring_of_finset
  intro F
  obtain ⟨q, hq⟩ := finite_config_proper (k := k) hc hw (fun x : F => (x : ℂ))
  exact ⟨fun x => c (q + x), fun x hx y hy hxy =>
    hq ⟨x, hx⟩ ⟨y, hy⟩ (by simpa using hxy)⟩

end EuclideanFiveColor
end

end OAI
