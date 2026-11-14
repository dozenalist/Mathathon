import Lean.Util.FoldConsts
import Lean.Elab.Command
open Lean Elab Command

partial def walk (env : Environment) (seen : NameMap (Array Name)) (n : Name) :
    NameMap (Array Name) :=
  if seen.contains n then seen
  else
    let deps : Array Name :=
      match env.find? n with
      | none => #[]
      | some ci => (ci.getUsedConstantsAsSet.toArray).filter (fun c => (`Lean).isPrefixOf c)
    let seen := seen.insert n deps
    deps.foldl (init := seen) (fun s c => walk env s c)

def report (roots : List Name) : CommandElabM Unit := do
  let env ← getEnv
  let g := roots.foldl (init := ({} : NameMap (Array Name))) (fun s r => walk env s r)
  let keys := (g.toList.map (fun (n, _) => n)).toArray.qsort (fun a b => a.toString < b.toString)
  for n in keys do
    let m := match env.getModuleIdxFor? n with
      | some i => (env.header.moduleNames[i]!).toString
      | none => "(local)"
    logInfo m!"NODE {m} {n}"
  let mut e : Nat := 0
  for n in keys do
    for c in (g.find? n).getD #[] do
      logInfo m!"EDGE {n} {c}"
      e := e + 1
  let nk := keys.size
  logInfo m!"NODES {nk} EDGES {e}"

elab "#declgraph" ids:ident* : command => do
  report (ids.toList.map (fun i => i.getId))

#declgraph List.map
