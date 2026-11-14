import Mathlib
import OAI.Geometry.PlaneColoring.Transfer
open Lean

run_cmd do
  let env ← getEnv
  let names := env.header.moduleNames
  let md := env.header.moduleData
  -- constant -> defining OAI module
  for i in [0:names.size] do
    let m := names[i]!
    if (`OAI).isPrefixOf m then
      let mut acc : NameSet := {}
      for c in md[i]!.constNames do
        let ci ← Lean.Elab.Command.liftCoreM (getConstInfo c)
        for d in ci.getUsedConstantsAsSet do
          if let some dm := env.getModuleFor? d then
            if (`OAI).isPrefixOf dm then acc := Lean.NameSet.insert acc dm
      let arr := Array.filter (fun x => Lean.NameSet.contains acc x && x != m) names
      logInfo m!"@@@{m}\t{arr.size}\t{arr.toList}"
