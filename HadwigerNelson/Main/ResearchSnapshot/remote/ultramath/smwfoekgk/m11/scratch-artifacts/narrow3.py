import re, json, pathlib, subprocess, os, sys, shutil
ROOT = pathlib.Path("work/lean/OAI")
SHAKE = json.load(open(".scratch/shake_sets.json"))
SRC = json.load(open(".scratch/srcidx.json"))
TACV = ["Mathlib.Tactic.Linarith","Mathlib.Tactic.Ring","Mathlib.Tactic.NormNum","Mathlib.Tactic.Positivity",
 "Mathlib.Tactic.FieldSimp","Mathlib.Tactic.Push","Mathlib.Tactic.IntervalCases","Mathlib.Tactic.FinCases",
 "Mathlib.Tactic.GCongr","Mathlib.Tactic.FunProp","Aesop.Frontend.Tactic","Mathlib.Tactic.WLOG",
 "Mathlib.Tactic.LinearCombination","Mathlib.Tactic.Polyrith","Mathlib.Tactic.Bound","Mathlib.Tactic.SimpRw",
 "Mathlib.Tactic.Core","Mathlib.Tactic.Ext","Mathlib.Tactic.Group","Mathlib.Tactic.Abel",
 "Mathlib.MeasureTheory.MeasurableSpace.Defs","Mathlib.Order.Filter.Basic",
 "Mathlib.Data.Nat.Notation","Mathlib.Data.Int.Notation","Mathlib.Data.Real.Basic","Mathlib.Analysis.Complex.Polynomial.Basic","Mathlib.Algebra.AlgebraicCard","Mathlib.Topology.Homotopy.Lifting","Mathlib.Analysis.Complex.BranchLogRoot","Mathlib.Analysis.SpecialFunctions.Complex.Arg"]
UNION = sorted({m for v in SHAKE.values() for m in v} | set(TACV))
def cands(nm):
    out=[]
    for c in (nm, nm.split(".")[-1]):
        v = SRC.get(c)
        if isinstance(v, str): out.append(v)
        elif isinstance(v, list): out.extend(v)
    return out[:4]
def run(p, timeout=1800):
    r = subprocess.run(["lean", str(p)], capture_output=True, text=True, env=dict(os.environ), timeout=timeout)
    return r.stdout
def check(modpath, imports, maxiter=4):
    p = ROOT/modpath; orig = p.read_text(); log=[]
    for it in range(maxiter):
        lines = orig.splitlines(); i = lines.index("import Mathlib")
        text = "\n".join(lines[:i] + ["import "+m for m in imports] + lines[i+1:]) + "\n"
        shutil.copy2(p, str(p)+".bak")
        try:
            p.write_text(text); out = run(p)
        finally:
            shutil.copy2(str(p)+".bak", p); os.remove(str(p)+".bak")
        errs = [l for l in out.splitlines() if ": error" in l]
        if not errs: return True, imports, log, []
        added=set()
        for e in errs:
            names = re.findall(r'[`\u2018]([A-Za-z_][A-Za-z0-9_.\']*)', e)
            names += re.findall(r'type class\s*\n\s*([A-Za-z_][A-Za-z0-9_.\']*)', e)
            for nm in names:
                for c in cands(nm):
                    if c not in imports: added.add(c)
        if not added: return False, imports, log, errs[:6]
        log.append(sorted(added)[:8]); imports = sorted(set(imports)|added)
    return False, imports, log, ["maxiter"]
if __name__=="__main__":
    mode = sys.argv[1]; mods = sys.argv[2:]
    if mode=="union":
        for m in mods:
            ok, imps, log, errs = check(m, list(UNION))
            print(("OK   " if ok else "FAIL "), m, "imports=", len(imps), "rounds=", len(log)+1)
            if not ok: print("      ", errs)
            else: json.dump(imps, open(".scratch/final_"+m.replace("/","_")+".json","w"))
