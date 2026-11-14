import json, pathlib

M9 = pathlib.Path("/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/.ultramath/smwfoekgk/m9")
decls = json.load(open(M9 / "ana/decls_ns.json"))
mods = sorted(set(d["mod"] for d in decls))
names = sorted(set(d["full"] for d in decls if d["full"]))
(M9 / "ana/names.txt").write_text("\n".join(names) + "\n")
hdr = "\n".join("import " + m for m in mods)
body = r'''
open Lean Elab Command

run_cmd do
  let txt ← IO.FS.readFile "ana/names.txt"
  let names := txt.splitOn "\n"
  let env ← getEnv
  let mut out : Array String := #[]
  let mut missing : Array String := #[]
  for n in names do
    if n == "" then continue
    let nm := n.toName
    match env.find? nm with
    | none => missing := missing.push n
    | some ci =>
      let mut acc : Array Name := #[]
      acc := acc ++ ci.type.getUsedConstants
      match ci with
      | .thmInfo ti => acc := acc ++ ti.value.getUsedConstants
      | .defnInfo di => acc := acc ++ di.value.getUsedConstants
      | .opaqueInfo oi => acc := acc ++ oi.value.getUsedConstants
      | .inductInfo ii => acc := acc ++ ii.type.getUsedConstants
      | .ctorInfo cti => acc := acc ++ cti.type.getUsedConstants
      | .recInfo ri => for r in ri.rules do acc := acc ++ r.rhs.getUsedConstants
      | .axiomInfo ai => acc := acc ++ ai.type.getUsedConstants
      | .quotInfo _ => pure ()
      out := out.push (n ++ "\t" ++ String.intercalate " " (acc.toList.map toString))
  IO.FS.writeFile "ana/deps.txt" (String.intercalate "\n" out.toList ++ "\n")
  IO.FS.writeFile "ana/deps_missing.txt" (String.intercalate "\n" missing.toList ++ "\n")
'''
(M9 / "deps.lean").write_text(hdr + "\n" + body)
print("wrote deps.lean with", len(mods), "imports,", len(names), "names")
