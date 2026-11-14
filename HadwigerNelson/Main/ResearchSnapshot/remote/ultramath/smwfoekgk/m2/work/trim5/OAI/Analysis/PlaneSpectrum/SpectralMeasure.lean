import OAI.Analysis.PlaneSpectrum.Representations

namespace OAI

noncomputable section
open MeasureTheory
open scoped InnerProductSpace ComplexConjugate
namespace EuclideanFiveColor.VectorMeasure
variable {X H : Type*} [TopologicalSpace X] [CompactSpace X] [T2Space X]
  [MeasurableSpace X] [BorelSpace X]
  [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
  (Φ : C(X,ℂ) →⋆ₐ[ℂ] (H →L[ℂ] H)) (v : H)
lemma inner_toLp (f g : C(X,ℂ)) :
    ⟪ContinuousMap.toLp 2 (measure Φ v) ℂ f, ContinuousMap.toLp 2 (measure Φ v) ℂ g⟫_ℂ =
      ⟪Φ f v,Φ g v⟫_ℂ := by
  rw [L2.inner_def]
  calc
    _ = ∫ x, (star f*g) x ∂measure Φ v := by
      apply integral_congr_ae
      filter_upwards [ContinuousMap.coeFn_toLp (μ := measure Φ v) (p := 2) (𝕜 := ℂ) f,
        ContinuousMap.coeFn_toLp (μ := measure Φ v) (p := 2) (𝕜 := ℂ) g] with x hx hy
      simp only [hx,hy,RCLike.inner_apply,ContinuousMap.mul_apply,ContinuousMap.star_apply,Complex.star_def]
      ring
    _ = ⟪v,Φ (star f*g) v⟫_ℂ := integral_complex Φ v _
    _ = _ := by
      rw [map_mul,map_star]
      change ⟪v,star (Φ f) (Φ g v)⟫_ℂ = _
      rw [ContinuousLinearMap.star_eq_adjoint,ContinuousLinearMap.adjoint_inner_right]
def vectorLinear : C(X,ℂ) →ₗ[ℂ] H where
  toFun f := Φ f v
  map_add' f g := by simp
  map_smul' c f := by simp
lemma norm_toLp (f : C(X,ℂ)) :
    ‖ContinuousMap.toLp 2 (measure Φ v) ℂ f‖ = ‖vectorLinear Φ v f‖ := by
  have he := congrArg Complex.re (inner_toLp Φ v f f)
  change RCLike.re (⟪ContinuousMap.toLp 2 (measure Φ v) ℂ f,ContinuousMap.toLp 2 (measure Φ v) ℂ f⟫_ℂ) =
    RCLike.re (⟪Φ f v,Φ f v⟫_ℂ) at he
  rw [inner_self_eq_norm_sq,inner_self_eq_norm_sq] at he
  exact (sq_eq_sq₀ (norm_nonneg _) (norm_nonneg _)).mp he
def cyclicMap : Lp ℂ 2 (measure Φ v) →L[ℂ] H :=
  (vectorLinear Φ v).extendOfNorm (ContinuousMap.toLp 2 (measure Φ v) ℂ).toLinearMap
lemma cyclicMap_toLp (f : C(X,ℂ)) :
    cyclicMap Φ v (ContinuousMap.toLp 2 (measure Φ v) ℂ f) = Φ f v := by
  apply LinearMap.extendOfNorm_eq
  · exact ContinuousMap.toLp_denseRange (E := ℂ) (p := 2) (μ := measure Φ v) (𝕜 := ℂ) (by norm_num)
  · exact ⟨1,fun g => by simp only [one_mul]; exact le_of_eq (norm_toLp Φ v g).symm⟩
lemma norm_cyclicMap (f : Lp ℂ 2 (measure Φ v)) : ‖cyclicMap Φ v f‖ = ‖f‖ := by
  refine (ContinuousMap.toLp_denseRange (E := ℂ) (p := 2) (μ := measure Φ v) (𝕜 := ℂ) (by norm_num)).induction
    (fun y hy => ?_) (isClosed_eq (by fun_prop) (by fun_prop)) f
  obtain ⟨g,rfl⟩ := hy
  rw [cyclicMap_toLp]
  exact (norm_toLp Φ v g).symm
def cyclicIsometry : Lp ℂ 2 (measure Φ v) →ₗᵢ[ℂ] H :=
  ⟨(cyclicMap Φ v).toLinearMap,norm_cyclicMap Φ v⟩
end EuclideanFiveColor.VectorMeasure
end

noncomputable section
open MeasureTheory
open scoped ENNReal NNReal
namespace EuclideanFiveColor.BoundedMeasurable
variable {X : Type*} [MeasurableSpace X] (μ : Measure X) [IsFiniteMeasure μ]
end EuclideanFiveColor.BoundedMeasurable
end

noncomputable section
open scoped ComplexConjugate IsMulCommutative
namespace EuclideanFiveColor.CommutingSpectral
variable {G H : Type*} [CommGroup G]
  [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
  (U : G →* unitary (H →L[ℂ] H))
instance algebra_closed : IsClosed (algebra U : Set (H →L[ℂ] H)) :=
  StarSubalgebra.isClosed_topologicalClosure _
open scoped IsMulCommutative in
instance algebra_commRing : CommRing (algebra U) :=
  let := adjoin_comm U
  inferInstance
instance algebra_commCStar : CommCStarAlgebra (algebra U) where

def generator (g : G) : algebra U :=
  ⟨U g,StarSubalgebra.le_topologicalClosure _ (StarAlgebra.subset_adjoin ℂ _ (Set.mem_range_self g))⟩
@[simp] lemma generator_one : generator U 1 = 1 := by ext; simp [generator]
@[simp] lemma generator_mul (g h : G) : generator U (g*h) = generator U g * generator U h := by
  apply Subtype.ext; change (U (g*h) : H →L[ℂ] H) = (U g : H →L[ℂ] H) * U h
  rw [map_mul]; rfl
variable [TopologicalSpace G] [DiscreteTopology G]
def character (φ : Spectrum U) : PontryaginDual G where
  toFun g := ⟨gelfandStarTransform (algebra U) (generator U g) φ, by
    change gelfandStarTransform (algebra U) (generator U g) φ ∈ Metric.sphere (0:ℂ) 1
    rw [Metric.mem_sphere, dist_zero_right]
    apply CStarRing.norm_of_mem_unitary
    exact Unitary.map_mem ((ContinuousMap.evalStarAlgHom ℂ ℂ φ).comp
      (gelfandStarTransform (algebra U)).toStarAlgHom) (generator_unitary U g)⟩
  map_one' := by apply Subtype.ext; simp
  map_mul' g h := by
    apply Subtype.ext
    change _ = (gelfandStarTransform (algebra U) (generator U g) φ) *
      (gelfandStarTransform (algebra U) (generator U h) φ)
    simp
  continuous_toFun := continuous_of_discreteTopology
def calculus : C(PontryaginDual G,ℂ) →⋆ₐ[ℂ] (H →L[ℂ] H) :=
  (algebra U).subtype.comp <| (gelfandStarTransform (algebra U)).symm.toStarAlgHom.comp
    (ContinuousMap.compStarAlgHom' ℂ ℂ ⟨character U,character_continuous U⟩)
end EuclideanFiveColor.CommutingSpectral
end

noncomputable section
open MeasureTheory
open scoped ENNReal NNReal InnerProductSpace
namespace EuclideanFiveColor.VectorMeasure
open BoundedMeasurable
variable {X H : Type*} [TopologicalSpace X] [CompactSpace X] [T2Space X]
  [MeasurableSpace X] [BorelSpace X]
  [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
  (Φ : C(X,ℂ) →⋆ₐ[ℂ] (H →L[ℂ] H)) (v : H)
omit [T2Space X] in
@[simp] lemma boundedCM_apply (f : C(X,ℂ)) (x : X) : boundedCM f x = f x := rfl
omit [T2Space X] in
end EuclideanFiveColor.VectorMeasure
end

noncomputable section
open MeasureTheory Filter Topology
open scoped ENNReal NNReal InnerProductSpace
namespace PlaneFiveColor.Spectral
open EuclideanFiveColor EuclideanFiveColor.BoundedMeasurable
open EuclideanFiveColor.VectorMeasure EuclideanFiveColor.CommutingSpectral
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
  (U : DiscreteE →* unitary (H →L[ℂ] H)) (v : H)

end PlaneFiveColor.Spectral
end

noncomputable section
open MeasureTheory
open scoped ComplexConjugate
namespace EuclideanFiveColor.CommutingSpectral
variable {G : Type*} [CommGroup G] [TopologicalSpace G] [DiscreteTopology G]
@[simps] def evaluationHom : G →* C(PontryaginDual G,ℂ) where
  toFun := evaluation
  map_one' := evaluation_one
  map_mul' := evaluation_mul
end EuclideanFiveColor.CommutingSpectral
namespace EuclideanFiveColor.CompactIntegral
variable {X : Type*} [TopologicalSpace X] [CompactSpace X] [MeasurableSpace X] [OpensMeasurableSpace X]
  (μ : Measure X) [IsFiniteMeasure μ]
end EuclideanFiveColor.CompactIntegral
namespace EuclideanFiveColor.CommutingSpectral
variable {G : Type*} [CommGroup G] [TopologicalSpace G] [DiscreteTopology G]
  [MeasurableSpace (PontryaginDual G)] [BorelSpace (PontryaginDual G)]
end EuclideanFiveColor.CommutingSpectral
end

end OAI
