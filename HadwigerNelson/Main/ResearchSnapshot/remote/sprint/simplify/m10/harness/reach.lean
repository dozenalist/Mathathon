/-
Sound declaration-level reachability for the headline results.

`#reach NAMES` walks the *proof-term* dependency closure of the given constants
and prints, for every constant it reaches, `REACHDECL <module> <name>`, plus
per-module counts and the total.  Mathlib constants are not followed (Mathlib is
compiled before `OAI`, so it cannot mention `OAI` constants), which makes the
walk cheap and still exact for the `OAI` part.

This is the only sound answer to "what may be deleted": the textual consumer
count of `decls.py` misses uses inside `simp` sets / instances and over-counts
duplicated names, and the import closure over-approximates grossly (82 of 83
modules are imported by the headline modules).

Run:  source scripts/env4341.sh && lean sprint/simplify/m10/harness/reach.lean
-/
import Lean.Util.FoldConsts
import OAI.Geometry.PlaneColoring.Five
import OAI.Geometry.PlaneColoring.Seven
import OAI.Geometry.PlaneColoring.Transfer
import OAI.Geometry.PlaneColoring.Chromatic
import OAI.Geometry.PlaneColoring.NullSetRobust

open Lean Elab Command

partial def reachGo (env : Environment) (seen : NameSet) (n : Name) : NameSet :=
  if seen.contains n then seen
  else
    let seen := seen.insert n
    match env.find? n with
    | none => seen
    | some ci =>
      ci.getUsedConstantsAsSet.toArray.foldl
        (init := seen) (fun s c => if (`OAI).isPrefixOf c then reachGo env s c else s)

def report (roots : List Name) : CommandElabM Unit := do
  let env ← getEnv
  let seen := roots.foldl (init := ({} : NameSet)) (fun s r => reachGo env s r)
  let mut arr : Array (String × String) := #[]
  for n in seen.toArray do
    let m := match env.getModuleIdxFor? n with
      | some i => (env.header.moduleNames[i]!).toString
      | none => "(local)"
    arr := arr.push (m, n.toString)
  let sorted := arr.qsort (fun a b => a.1 < b.1 || (a.1 == b.1 && a.2 < b.2))
  let mut last := ""
  for (m, n) in sorted do
    if m != last then
      logInfo m!"REACHMOD {m}"
      last := m
    logInfo m!"REACHDECL {m} {n}"
  logInfo m!"REACH_TOTAL {arr.size}"

elab "#reach" ids:ident* : command => do
  report (ids.map (fun i => i.getId)).toList

#reach
  OAI.EuclideanFiveColor.no_proper_five_coloring
  OAI.EuclideanFiveColor.no_proper_five_coloring_algebraic
  OAI.Problem160.properColoring_seven
  OAI.EuclideanFiveColor.proper_iff_weak
  OAI.Problem160.chromaticNumber_bounds
  OAI.EuclideanFiveColor.not_proper_five_coloring_compl_null
  OAI.EuclideanFiveColor.algebraic_colorable_iff
