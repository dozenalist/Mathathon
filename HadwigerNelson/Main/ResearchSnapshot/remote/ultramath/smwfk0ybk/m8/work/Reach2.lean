import Mathlib
import OAI.Geometry.PlaneColoring.Transfer
import ImportGraph.Imports.RequiredModules

open Lean

run_cmd do
  let env ← getEnv
  let targets : List Name :=
    [ `OAI.EuclideanFiveColor.proper_iff_weak
    , `OAI.EuclideanFiveColor.proper_to_borel_weak
    , `OAI.EuclideanFiveColor.properColoring_of_weak ]
  let names := env.header.moduleNames
  for t in targets do
    let s : NameSet := {t}
    let used ← Lean.Elab.Command.liftCoreM (NameSet.transitivelyUsedConstants s)
    logInfo m!"@@@{t}\tusedconstants\t{used.size}"
    for i in [0:names.size] do
      let m := names[i]!
      if (`OAI).isPrefixOf m then
        let cn := env.header.moduleData[i]!.constNames
        let usedHere := Array.filter (fun n => Lean.NameSet.contains used n) cn
        logInfo m!"@@@{t}\t{m}\t{cn.size}\t{usedHere.size}\t{usedHere.toList}"
