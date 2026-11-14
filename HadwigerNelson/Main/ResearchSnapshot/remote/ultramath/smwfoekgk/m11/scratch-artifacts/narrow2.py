import re, json, pathlib, subprocess, os, sys, shutil
ROOT = pathlib.Path("work/lean/OAI")
SHAKE = json.load(open(".scratch/shake_sets.json"))
NAME_MOD = {}
for line in open("/opt/nucleus/docs/names.tsv", errors="ignore"):
    p = line.rstrip("\n").split("\t")
    if len(p) >= 3 and p[2].startswith("Mathlib/") and p[2].endswith(".lean"):
        NAME_MOD.setdefault(p[0], p[2][:-5].replace("/", "."))
TAC = {
 "linarith":"Mathlib.Tactic.Linarith","nlinarith":"Mathlib.Tactic.Linarith",
 "ring":"Mathlib.Tactic.Ring","ring_nf":"Mathlib.Tactic.Ring","nonzero":"Mathlib.Tactic.Ring",
 "norm_num":"Mathlib.Tactic.NormNum","positivity":"Mathlib.Tactic.Positivity",
 "field_simp":"Mathlib.Tactic.FieldSimp","omega":None,
 "push_neg":"Mathlib.Tactic.Push","interval_cases":"Mathlib.Tactic.IntervalCases",
 "fin_cases":"Mathlib.Tactic.FinCases","gcongr":"Mathlib.Tactic.GCongr",
 "fun_prop":"Mathlib.Tactic.FunProp","aesop":"Aesop.Frontend.Tactic",
 "norm_cast":None,"push_cast":None,
 "filter_upwards":"Mathlib.Order.Filter.Basic","wlog":"Mathlib.Tactic.WLOG",
 "linear_combination":"Mathlib.Tactic.LinearCombination","polyrith":"Mathlib.Tactic.Polyrith",
 "bound":"Mathlib.Tactic.Bound","measurability":"Mathlib.MeasureTheory.MeasurableSpace.Defs",
 "continuity":"Mathlib.Topology.ContinuousMap.Basic","simp_rw":"Mathlib.Tactic.SimpRw",
 "exact_mod_cast":None,"rw_mod_cast":None,
 "mod_cast":None,"nth_rewrite":"Mathlib.Tactic.Core",
 "ext":"Mathlib.Tactic.Ext","group":"Mathlib.Tactic.Group","abel":"Mathlib.Tactic.Abel",
}
def mods_of(nm):
    for cand in (nm, nm.split(".")[-1]):
        m = NAME_MOD.get(cand)
        if m: return [m]
    return []
def tactics_in(text):
    s=set()
    for m in re.finditer(r'(?m)^\s*(?:·\s*)?([a-z_][A-Za-z0-9_\']*)\b', text):
        if m.group(1) in TAC and TAC[m.group(1)]: s.add(TAC[m.group(1)])
    return s
def toks_at(text, line, col):
    ls = text.splitlines()
    if line-1 >= len(ls): return []
    l = ls[line-1]
    return re.findall(r"[A-Za-z_][A-Za-z0-9_']*", l[max(0,col-1):])[:3] + re.findall(r"[A-Za-z_][A-Za-z0-9_']*", l)[:6]
def run_lean(p, timeout=1200):
    r = subprocess.run(["lean", str(p)], capture_output=True, text=True, env=dict(os.environ), timeout=timeout)
    return r.stdout
def solve(modpath, maxiter=6, verbose=True):
    p = ROOT/modpath; key = "OAI_" + modpath.replace("/","_")[:-5]
    orig = p.read_text()
    base = set(SHAKE[key])
    extra = tactics_in(orig)
    imports = sorted(base | extra)
    log=[]
    for it in range(maxiter):
        lines = orig.splitlines()
        i = lines.index("import Mathlib")
        new = lines[:i] + ["import "+m for m in imports] + lines[i+1:]
        text = "\n".join(new) + "\n"
        shutil.copy2(p, str(p)+".bak")
        try:
            p.write_text(text)
            out = run_lean(p)
        finally:
            shutil.copy2(str(p)+".bak", p); os.remove(str(p)+".bak")
        errs = [l for l in out.splitlines() if ": error" in l]
        if not errs:
            return dict(mod=modpath, ok=True, imports=imports, iters=it+1, log=log)
        added=set()
        for e in errs:
            m = re.match(r'.*\.lean:(\d+):(\d+): error(?:\([^)]*\))?: (.*)', e)
            if not m: continue
            ln, col, msg = int(m.group(1)), int(m.group(2)), m.group(3)
            ids = re.findall(r'[`\u2018]([A-Za-z_][A-Za-z0-9_.\']*)', msg)
            for nm in ids:
                for mo in mods_of(nm):
                    if mo not in imports: added.add(mo)
            if "unknown tactic" in msg or "unsolved goals" in msg:
                for tok in toks_at(text, ln, col):
                    if tok in TAC and TAC[tok] and TAC[tok] not in imports:
                        added.add(TAC[tok]); break
            if "unknown notation" in msg or "unknown identifier '‖'" in msg:
                pass
        if not added:
            return dict(mod=modpath, ok=False, imports=imports, iters=it+1, errs=[e[:200] for e in errs[:10]], log=log)
        log.append(sorted(added))
        imports = sorted(set(imports) | added)
    return dict(mod=modpath, ok=False, imports=imports, iters=maxiter, errs=["maxiter"], log=log)
if __name__=="__main__":
    for m in sys.argv[1:]:
        r = solve(m)
        print(("OK   " if r["ok"] else "FAIL "), m, "imports=", len(r["imports"]), "iters=", r["iters"])
        if not r["ok"]: print("     ", r.get("errs"))
