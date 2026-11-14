import Mathlib

namespace OAI

noncomputable section

open MeasureTheory

namespace Problem160

abbrev Plane := EuclideanSpace ℝ (Fin 2)

def circleDir (t : ℝ) : Plane :=
  WithLp.toLp 2 ![Real.cos t, Real.sin t]

def normalizedAngleMeasure : Measure ℝ :=
  (ENNReal.ofReal (2 * Real.pi))⁻¹ •
    Measure.restrict volume (Set.Ico 0 (2 * Real.pi))

def circleMeasure : Measure Plane :=
  Measure.map circleDir normalizedAngleMeasure

def weakPairMeasure (R : ℝ) : Measure (Plane × Plane) :=
  (Measure.restrict volume (Metric.ball (0 : Plane) R)).prod circleMeasure

def ProperColoring (k : ℕ) : Prop :=
  ∃ c : Plane → Fin k,
    ∀ x y : Plane, dist x y = 1 → c x ≠ c y

def WeakMeasurableColoring (k : ℕ) : Prop :=
  ∃ c : Plane → Fin k,
    AEMeasurable c volume ∧
      ∀ R : ℝ, 0 < R →
        (∑ i : Fin k,
          (weakPairMeasure R)
            {p : Plane × Plane |
              c (Prod.fst p) = i ∧
              c (Prod.fst p + Prod.snd p) = i}) = 0

def planeChromaticNumber : ℕ :=
  sInf {k : ℕ | ProperColoring k}

end Problem160

end

end OAI

open Lean in
run_cmd do
  let env ← getEnv
  let mut used : Std.HashSet Name := {}
  let mut nown : Nat := 0
  for (n, ci) in env.constants.toList do
    if (env.getModuleIdxFor? n).isNone then
      nown := nown + 1
      for c in ci.type.getUsedConstants do used := used.insert c
      if let some v := ci.value? then
        for c in v.getUsedConstants do used := used.insert c
  let mut mods : Std.HashSet Name := {}
  for c in used do
    if let some i := env.getModuleIdxFor? c then
      mods := mods.insert env.header.moduleNames[i]!
  let mut out : Array Name := #[]
  for m in mods do
    if (`Mathlib).isPrefixOf m then out := out.push m
  logInfo m!"SHAKE_BEGIN own={nown} nmods={out.size} used={used.size}"
  for m in out.qsort (fun a b => a.toString < b.toString) do logInfo m!"IMPORT {m}"
  logInfo m!"SHAKE_END"
