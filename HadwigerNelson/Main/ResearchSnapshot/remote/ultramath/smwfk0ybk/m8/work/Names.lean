import Mathlib
import ImportGraph.Imports.RequiredModules
open Lean
run_cmd do
  let env ← getEnv
  let names := env.header.moduleNames
  let md := env.header.moduleData
  for i in [0:names.size] do
    let m := names[i]!
    if (`OAI).isPrefixOf m then
      for c in md[i]!.constNames do
        logInfo m!"#@{m}\t{c}"
