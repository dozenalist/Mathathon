import OAI.Geometry.PlaneColoring.Chromatic
import OAI.Geometry.PlaneColoring.NullSetRobust
import OAI.Geometry.PlaneColoring.Transfer
import OAI.Geometry.PlaneColoring.ConnectedUnitFree

open Lean Elab Command

run_cmd do
  let env ← getEnv
  let mut lines : Array String := #[]
  for (n, ci) in env.constants.toList do
    let mut acc : Array String := #[]
    for c in ci.type.getUsedConstants do acc := acc.push c.toString
    match ci.value? with
    | some v => for c in v.getUsedConstants do acc := acc.push c.toString
    | none => pure ()
    lines := lines.push s!"{n}|{" ".intercalate acc.toList}"
  IO.FS.writeFile "/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/.ultramath/smwfoekgk/m2/work/deps.txt"
    ("\n".intercalate lines.toList)
  IO.println s!"wrote {lines.size} constants"
