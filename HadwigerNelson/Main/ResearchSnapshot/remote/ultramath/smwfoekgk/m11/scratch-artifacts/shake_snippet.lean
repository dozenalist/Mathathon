
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
