/-
Sound declaration-level dependency graph of the OAI development from the headline
theorems, split into type-dependencies and value(proof)-dependencies.

`#declgraph NAMES` writes
    NODE <module> <name>
    EDGET <parent> <child>     child occurs in parent's *type*
    EDGEV <parent> <child>     child occurs in parent's *value* (proof term)
Mathlib constants are not followed: Mathlib is compiled before OAI, so it cannot
mention OAI constants; the walk is exact for the OAI part and cheap.

Why the split: replacing the *body* of a declaration frees everything reachable
from it only through value-edges, while its statement still keeps the type-edges
alive.  So a route's line prize is computed with EDGET always active and EDGEV
deactivated at the declarations the route reproves.

Run:  source scripts/env4341.sh && lean sprint/simplify/m10/harness/declgraph.lean
-/
import Lean.Util.FoldConsts
import Lean.Elab.Command
import OAI.Geometry.PlaneColoring.Five
import OAI.Geometry.PlaneColoring.Seven
import OAI.Geometry.PlaneColoring.Transfer
import OAI.Geometry.PlaneColoring.Chromatic
import OAI.Geometry.PlaneColoring.NullSetRobust

open Lean Elab Command

def oai (a : Array Name) : Array Name := a.filter (fun c => (`OAI).isPrefixOf c)

partial def walk (env : Environment) (seen : NameMap (Array Name × Array Name)) (n : Name) :
    NameMap (Array Name × Array Name) :=
  if seen.contains n then seen
  else
    let (td, vd) : Array Name × Array Name :=
      match env.find? n with
      | none => (#[], #[])
      | some ci =>
        let t := oai ci.type.getUsedConstants
        let v := match ci.value? (allowOpaque := true) with
          | some e => oai e.getUsedConstants
          | none => #[]
        (t, v)
    let seen := seen.insert n (td, vd)
    (td ++ vd).foldl (init := seen) (fun s c => walk env s c)

def report (roots : List Name) : CommandElabM Unit := do
  let env ← getEnv
  let g := roots.foldl (init := ({} : NameMap (Array Name × Array Name)))
      (fun s r => walk env s r)
  let keys := (g.toList.map (fun (n, _) => n)).toArray.qsort (fun a b => a.toString < b.toString)
  for n in keys do
    let m := match env.getModuleIdxFor? n with
      | some i => (env.header.moduleNames[i]!).toString
      | none => "(local)"
    logInfo m!"NODE {m} {n}"
  for n in keys do
    let (td, vd) := (g.find? n).getD (#[], #[])
    for c in td do logInfo m!"EDGET {n} {c}"
    for c in vd do logInfo m!"EDGEV {n} {c}"
  let nk := keys.size
  logInfo m!"NODES {nk}"

elab "#declgraph" ids:ident* : command => do
  report (ids.toList.map (fun i => i.getId))

#declgraph
  OAI.EuclideanFiveColor.no_proper_five_coloring
  OAI.EuclideanFiveColor.no_proper_five_coloring_algebraic
  OAI.Problem160.properColoring_seven
  OAI.EuclideanFiveColor.proper_iff_weak
  OAI.Problem160.chromaticNumber_bounds
  OAI.EuclideanFiveColor.not_proper_five_coloring_compl_null
  OAI.EuclideanFiveColor.algebraic_colorable_iff
