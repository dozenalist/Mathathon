import OAI.Geometry.PlaneColoring.GraphRealization
import OAI.Geometry.PlaneColoring.Interfaces
import OAI.Geometry.PlaneColoring.Sectors

namespace OAI

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
/-- Vanishing exceptional measure is enough: almost every point is outside the
exceptional sets infinitely often. No summability or nesting is required. -/
lemma ae_frequently_notMem_of_measure_tendsto_zero {X : Type*} [MeasurableSpace X]
    {μ : Measure X} {E : ℕ → Set X}
    (hE : Tendsto (fun n => μ (E n)) atTop (𝓝 0)) :
    ∀ᵐ z ∂μ, ∃ᶠ n in atTop, z ∉ E n := by
  let T : ℕ → Set X := fun N => ⋂ n ≥ N, E n
  have hT : ∀ N, μ (T N) = 0 := by
    intro N
    apply le_antisymm _ (by positivity)
    apply ge_of_tendsto hE
    filter_upwards [eventually_ge_atTop N] with n hn
    exact measure_mono (fun z hz => (mem_iInter.mp (mem_iInter.mp hz n)) hn)
  have hn : μ (⋃ N, T N) = 0 := measure_iUnion_null hT
  filter_upwards [measure_eq_zero_iff_ae_notMem.mp hn] with z hz
  rw [← not_eventually]
  intro he
  obtain ⟨N,hN⟩ := eventually_atTop.mp he
  exact hz (mem_iUnion.mpr ⟨N,mem_iInter.mpr fun n => mem_iInter.mpr (hN n)⟩)

/-- Pointwise differentiation plus vanishing exceptional sets gives the measure
exclusion used for both the mesh bound and the common continuum exclusions. -/
lemma ae_ne_one_of_eventual_bound {X : Type*} [MeasurableSpace X]
    {μ : Measure X} {p : ℕ → X → ℝ} {f : X → ℝ} {E : ℕ → Set X} {U : Set X}
    {α : ℝ} (hα : 0 < α)
    (hp : ∀ᵐ z ∂μ, Tendsto (fun n => p n z) atTop (𝓝 (f z)))
    (hE : Tendsto (fun n => μ (E n)) atTop (𝓝 0))
    (hb : ∀ z ∈ U, ∀ᶠ n in atTop, z ∉ E n → p n z ≤ 1-α) :
    ∀ᵐ z ∂μ, z ∈ U → f z ≠ 1 := by
  filter_upwards [hp,ae_frequently_notMem_of_measure_tendsto_zero hE] with z hz hgood hzU hf
  have hgt : ∀ᶠ n in atTop, 1-α < p n z :=
    hz.eventually (Ioi_mem_nhds (by rw [hf]; linarith))
  obtain ⟨n,hn,hbnd,hlarge⟩ := (hgood.and_eventually ((hb z hzU).and hgt)).exists
  exact (not_lt_of_ge (hbnd hn)) hlarge
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Filter Topology MeasureTheory MeasureTheory.Measure
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Filter Topology TopologicalSpace
universe u v
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Filter Topology MeasureTheory TopologicalSpace
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
lemma CommonInterface.symm {c : ℂ → Fin 5} {x : ℂ} {i j : Fin 5}
    (h : CommonInterface c x i j) : CommonInterface c x j i := by
  obtain ⟨K,v,hv,hK,hi,hj⟩ := h
  exact ⟨K,v,hv,hK,hj,hi⟩
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Filter Topology TopologicalSpace MeasureTheory
namespace EuclideanFiveColor
end EuclideanFiveColor
end

end OAI
