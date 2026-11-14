import OAI.Geometry.PlaneColoring.Five
open Lean Elab Command

run_cmd do
  let env ← getEnv
  for n in [`OAI.EuclideanFiveColor.no_proper_five_coloring,
            `OAI.Geometry.PlaneColoring.Five,
            `OAI.EuclideanFiveColor.no_measurable_weak_five_coloring] do
    match env.find? n with
    | none => IO.println s!"{n}: MISSING"
    | some ci =>
      IO.println s!"{n}: ctor={ci.constructorIdx}, valSome={(ci.value?).isSome}"
      match ci with
      | .thmInfo v => IO.println s!"  thmInfo value usedConstants={v.value.getUsedConstants.size}"
      | .defnInfo v => IO.println s!"  defnInfo value usedConstants={v.value.getUsedConstants.size}"
      | .opaqueInfo _ => IO.println "  opaque"
      | _ => IO.println "  other"
