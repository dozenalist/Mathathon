import OAI.Geometry.PlaneColoring.CyclicCore
import OAI.Geometry.PlaneColoring.PlanarCovers

namespace OAI

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
/-- The directional subsequence in the last paragraph of interface-cycle follows
from connectedness and an outer contact. Compactness of the continuum is not needed. -/
lemma continuum_has_approach {x y : ℂ} {K : Set ℂ} (hK : IsPreconnected K)
    (hx : x∈K) (hy : y∈K) (hne : y≠x) :
    ∃v : ℂ, ‖v‖=1 ∧ Nonempty (ApproachingContinuum x K v) := by
  let ρ : ℝ := dist y x
  have hρ : 0<ρ := dist_pos.mpr hne
  let r : ℕ → ℝ := fun n => ρ/(n+1)
  have hr (n) : 0<r n := div_pos hρ (by positivity)
  have hrle (n) : r n≤ρ := (div_le_iff₀ (by positivity : 0<(n:ℝ)+1)).mpr (by
    have hn : 0≤(n:ℝ) := Nat.cast_nonneg n
    nlinarith)
  have hr0 : Tendsto r atTop (𝓝 0) := by
    simpa only [r,div_eq_mul_inv,mul_zero,one_mul] using
      (tendsto_const_nhds (x:=ρ)).mul (tendsto_one_div_add_atTop_nhds_zero_nat (𝕜:=ℝ))
  have hq (n) : ∃q∈K,dist q x=r n := by
    have hI := hK.intermediate_value (f:=fun z : ℂ => dist z x) hx hy (continuous_id.dist continuous_const).continuousOn
    apply hI
    exact ⟨by simpa using (hr n).le,hrle n⟩
  choose q hqK hqr using hq
  let w : ℕ → ℂ := fun n => (q n-x)/(r n : ℂ)
  have hwn (n) : ‖w n‖=1 := by
    dsimp [w]
    rw [norm_div,Complex.norm_real,Real.norm_eq_abs,abs_of_pos (hr n),←dist_eq_norm,hqr]
    exact div_self (ne_of_gt (hr n))
  have hwm (n) : w n∈Metric.sphere (0 : ℂ) 1 := by
    simpa only [Metric.mem_sphere,dist_zero_right] using hwn n
  obtain ⟨v,hv,φ,hφ,hlim⟩ := (isCompact_sphere (0 : ℂ) 1).tendsto_subseq hwm
  refine ⟨v,by simpa only [Metric.mem_sphere,dist_zero_right] using hv,?_⟩
  refine ⟨⟨hx,r∘φ,w∘φ,fun n => hr (φ n),hr0.comp hφ.tendsto_atTop,
    fun n => hwn (φ n),hlim,?_⟩⟩
  intro n
  have he : x+(r (φ n) : ℂ)*w (φ n)=q (φ n) := by
    dsimp [w]
    have hn : (r (φ n) : ℂ)≠0 := Complex.ofReal_ne_zero.mpr (ne_of_gt (hr _))
    field_simp
    ring
  exact he ▸ hqK (φ n)
end EuclideanFiveColor
end

noncomputable section
open Set
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Topology
universe u
namespace EuclideanFiveColor
abbrev GraphSpace {V : Type u} (G : SimpleGraph V) := ↥(graphRealization G)
@[simp] lemma graphEdgePoint_zero {V : Type u} (i j : V) : graphEdgePoint i j 0=graphVertex i := by
  simp [graphEdgePoint]
@[simp] lemma graphEdgePoint_one {V : Type u} (i j : V) : graphEdgePoint i j 1=graphVertex j := by
  simp [graphEdgePoint]
@[simp] lemma graphEdgePoint_self {V : Type u} (i : V) (t : ℝ) : graphEdgePoint i i t=graphVertex i := by
  rw [graphEdgePoint,←add_smul]; simp
lemma graphVertex_mem {V : Type u} (G : SimpleGraph V) (i : V) : graphVertex i∈graphRealization G :=
  ⟨i,i,Or.inl rfl,0,by norm_num,by simp⟩
instance graphSpace_compact {V : Type u} [Finite V] (G : SimpleGraph V) : CompactSpace (GraphSpace G) :=
  isCompact_iff_compactSpace.mp (graphRealization_compact G)
lemma graphRealization_singleton {V : Type u} [Subsingleton V] (G : SimpleGraph V) (a : V) :
    graphRealization G={graphVertex a} := by
  ext p
  constructor
  · rintro ⟨i,j,_,t,_,rfl⟩
    simp [Subsingleton.elim i a,Subsingleton.elim j a]
  · rintro rfl
    exact graphVertex_mem G a
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Topology
universe u
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Topology MeasureTheory
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
end EuclideanFiveColor
end

end OAI
