import Mathlib

namespace OAI

noncomputable section

namespace Problem160

/-- A covering by small cells, whose equally colored distinct centers are far
apart, gives a proper coloring of the unit-distance graph. The covering need
not form a partition: classical choice assigns boundary points to one cell. -/
theorem exists_unit_distance_coloring_of_center_cover
    {X I : Type*} [PseudoMetricSpace X] {k : ℕ}
    (center : I → X) (color : I → Fin k) (r : ℝ)
    (hcover : ∀ x : X, ∃ i : I, dist x (center i) ≤ r)
    (hdiam : 2 * r < 1)
    (hsep : ∀ i j : I, i ≠ j → color i = color j →
      1 + 2 * r < dist (center i) (center j)) :
    ∃ c : X → Fin k, ∀ x y : X, dist x y = 1 → c x ≠ c y := by
  classical
  choose cell hcell using hcover
  refine ⟨fun x => color (cell x), ?_⟩
  intro x y hdist hcolor
  by_cases hsame : cell x = cell y
  · have htriangle := dist_triangle x (center (cell x)) y
    have hx := hcell x
    have hy := hcell y
    rw [← hsame] at hy
    rw [dist_comm (center (cell x)) y] at htriangle
    linarith
  · have hfar := hsep (cell x) (cell y) hsame hcolor
    have htriangle₁ := dist_triangle (center (cell x)) x (center (cell y))
    have htriangle₂ := dist_triangle x y (center (cell y))
    have hx := hcell x
    have hy := hcell y
    rw [dist_comm (center (cell x)) x] at htriangle₁
    linarith

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
