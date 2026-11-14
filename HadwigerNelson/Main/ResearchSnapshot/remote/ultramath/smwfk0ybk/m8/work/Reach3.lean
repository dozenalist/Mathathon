import Mathlib
import OAI.Geometry.PlaneColoring.Assembly
import OAI.Geometry.PlaneColoring.Five
import OAI.Geometry.PlaneColoring.Transfer
import ImportGraph.Imports.RequiredModules

open Lean

run_cmd do
  let env ← getEnv
  let all := env.header.moduleNames
  let targets : List Name :=
    [ `OAI.EuclideanFiveColor.no_proper_five_coloring ]
  for t in targets do
    let s : NameSet := {t}
    let ms ← Lean.Elab.Command.liftCoreM (s.transitivelyRequiredModules env)
    let sel := Array.filter (fun m => Lean.NameSet.contains ms m) all
    let oai := Array.filter (fun m => (`OAI).isPrefixOf m) sel
    logInfo m!"### {t}\n  required total {sel.size} (OAI {oai.size})\n  OAI: {Array.toList oai}\n"
