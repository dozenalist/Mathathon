import OAI.Analysis.PlaneSpectrum.Basic

open Lean Elab Command

#check @Environment.constants
#check @Environment.addDecl
#check @Lean.Environment.constants
#check @Lean.SMap
#check @Lean.Environment.header
#check @Lean.NameMap

run_cmd do
  let env ← getEnv
  let cs := env.constants
  logInfo m!"type: {← Lean.Meta.inferType (← Lean.Meta.mkConst ``Environment.constants)}"
  logInfo m!"size? {repr cs.map₂.size}"
  let some ci := env.find? ``OAI.PlaneFiveColor.Spectral.j
    | logInfo "not found"
  logInfo m!"j found: {ci.toConstantVal.name}"
