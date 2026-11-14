import re, json, pathlib, subprocess, os, sys, shutil
ROOT = pathlib.Path("work/lean/OAI")
SHAKE = json.load(open(".scratch/shake_sets.json"))
NAME_MOD = {}
for line in open("/opt/nucleus/docs/names.tsv", errors="ignore"):
    p = line.rstrip("\n").split("\t")
    if len(p) < 3: continue
    n, mod = p[0], p[2]
    if mod.endswith(".lean") and mod.startswith("Mathlib/"):
        NAME_MOD.setdefault(n, mod)
TAC = {
 "linarith":"Mathlib.Tactic.Linarith","nlinarith":"Mathlib.Tactic.Linarith",
 "ring":"Mathlib.Tactic.Ring","ring_nf":"Mathlib.Tactic.Ring","nonzero":"Mathlib.Tactic.Ring",
 "norm_num":"Mathlib.Tactic.NormNum","positivity":"Mathlib.Tactic.Positivity",
 "field_simp":"Mathlib.Tactic.FieldSimp","omega":"Mathlib.Tactic.Omega",
 "push_neg":"Mathlib.Tactic.PushNeg","interval_cases":"Mathlib.Tactic.IntervalCases",
 "fin_cases":"Mathlib.Tactic.FinCases","gcongr":"Mathlib.Tactic.GCongr",
 "fun_prop":"Mathlib.Tactic.FunProp","aesop":"Mathlib.Tactic.Aesop",
 "norm_cast":"Mathlib.Tactic.NormCast","push_cast":"Mathlib.Tactic.NormCast",
 "filter_upwards":"Mathlib.Order.Filter.Basic","wlog":"Mathlib.Tactic.WLOG",
 "linear_combination":"Mathlib.Tactic.LinearCombination","polyrith":"Mathlib.Tactic.Polyrith",
 "bound":"Mathlib.Tactic.Bound","measurability":"Mathlib.MeasureTheory.Measure.MeasureSpace",
 "continuity":"Mathlib.Topology.ContinuousMap.Basic","group":"Mathlib.Tactic.Group",
 "abel":"Mathlib.Tactic.Abel","simp_rw":"Mathlib.Tactic.SimpRw","let":"Mathlib.Tactic",
 "mod_cast":"Mathlib.Tactic.NormCast","exact_mod_cast":"Mathlib.Tactic.NormCast",
 "rw_mod_cast":"Mathlib.Tactic.NormCast","nth_rewrite":"Mathlib.Tactic.Core",
 "multiparam":"", "ext":"Mathlib.Tactic.Ext","congr":"Mathlib.Tactic.Congr",
}
def mods_of(nm):
    out = []
    for cand in (nm, nm.split(".")[-1]):
        m = NAME_MOD.get(cand)
        if m: out.append(m)
    return out
def to_imp(m): return m
def tactics_in(text):
    s = set()
    for m in re.finditer(r'(?m)^\s*(?:·\s*)?([a-z_][A-Za-z0-9_\']*)\b', text):
        if m.group(1) in TAC and TAC[m.group(1)]: s.add(TAC[m.group(1)])
    return s
def build(modpath, extra, drop=()):
    key = "OAI_" + modpath.replace("/", "_")[:-5]
    base = [to_imp(m) for m in SHAKE[key] if m not in drop]
    imports = sorted(set(base) | set(extra))
    p = ROOT / modpath
    text = p.read_text()
    lines = text.splitlines()
    assert "import Mathlib" in lines, modpath
    i = lines.index("import Mathlib")
    new = lines[:i] + ["import " + m for m in imports] + lines[i+1:]
    return "\n".join(new) + "\n", imports
if __name__ == "__main__":
    mods = sys.argv[1:]
    for modpath in mods:
        p = ROOT / modpath
        orig = p.read_text()
        extra = tactics_in(orig)
        # keep OAI-imported shake names that are not Mathlib.* (shouldn't happen)
        text, imports = build(modpath, extra)
        shutil.copy2(p, str(p)+".bak")
        try:
            p.write_text(text)
            r = subprocess.run(["lean", str(p)], capture_output=True, text=True, env=dict(os.environ), timeout=3000)
            errs = [l for l in r.stdout.splitlines() if ": error" in l]
            print(f"### {modpath}: imports={len(imports)} rc={r.returncode} errors={len(errs)}")
            for l in errs[:12]: print("   ", l[:160])
        finally:
            shutil.copy2(str(p)+".bak", p); os.remove(str(p)+".bak")
