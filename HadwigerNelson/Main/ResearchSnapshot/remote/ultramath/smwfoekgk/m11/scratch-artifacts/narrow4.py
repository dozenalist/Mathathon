import re, json, pathlib, subprocess, os, sys, shutil
ROOT = pathlib.Path("work/lean/OAI")
SHAKE = json.load(open(".scratch/shake_sets.json")); SRC = json.load(open(".scratch/srcidx.json"))
TACV = ["Mathlib.Tactic.Linarith","Mathlib.Tactic.Ring","Mathlib.Tactic.NormNum","Mathlib.Tactic.Positivity",
 "Mathlib.Tactic.FieldSimp","Mathlib.Tactic.Push","Mathlib.Tactic.IntervalCases","Mathlib.Tactic.FinCases",
 "Mathlib.Tactic.GCongr","Mathlib.Tactic.FunProp","Aesop.Frontend.Tactic","Mathlib.Tactic.WLOG",
 "Mathlib.Tactic.LinearCombination","Mathlib.Tactic.Polyrith","Mathlib.Tactic.Bound","Mathlib.Tactic.SimpRw",
 "Mathlib.Tactic.Core","Mathlib.Tactic.Ext","Mathlib.Tactic.Group","Mathlib.Tactic.Abel",
 "Mathlib.MeasureTheory.MeasurableSpace.Defs","Mathlib.Order.Filter.Basic",
 "Mathlib.Data.Nat.Notation","Mathlib.Data.Int.Notation","Mathlib.Data.Real.Basic"]
def homes(nm, cap=2):
    out=[]
    for c in (nm, nm.split(".")[-1]):
        v=SRC.get(c)
        if isinstance(v,str) and v not in out: out.append(v)
    return out[:cap]
LISTY = re.compile(r'\b(?:simp|simpa|dsimp|rw|erw|simp_rw|simp_all|aesop|norm_num)\b[^\n]*?\[([^\]]*)\]')
def simp_homes(text):
    s=set()
    for m in LISTY.finditer(text):
        for tok in re.findall(r"[A-Za-z_][A-Za-z0-9_.']*", m.group(1)):
            for h in homes(tok): s.add(h)
    return s
def base_for(modpath, extranames=()):
    key="OAI_"+modpath.replace("/","_")[:-5]
    text=(ROOT/modpath).read_text()
    b=set(SHAKE[key])|set(TACV)|simp_homes(text)
    for n in extranames:
        for h in homes(n,4): b.add(h)
    return sorted(b)
def run(p, timeout=1800):
    r=subprocess.run(["lean",str(p)],capture_output=True,text=True,env=dict(os.environ),timeout=timeout)
    return r.stdout
def check(modpath, imports, maxiter=3):
    p=ROOT/modpath; orig=p.read_text(); shift=len(imports)-1; log=[]
    for it in range(maxiter):
        lines=orig.splitlines(); i=lines.index("import Mathlib")
        text="\n".join(lines[:i]+["import "+m for m in imports]+lines[i+1:])+"\n"
        shutil.copy2(p,str(p)+".bak")
        try:
            p.write_text(text); out=run(p)
        finally:
            shutil.copy2(str(p)+".bak",p); os.remove(str(p)+".bak")
        errs=[l for l in out.splitlines() if ": error" in l]
        if not errs: return True, imports, [], shift
        added=set()
        for e in errs:
            names=re.findall(r'[`\u2018]([A-Za-z_][A-Za-z0-9_.\']*)',e)
            m=re.match(r'.*\.lean:(\d+):(\d+): error',e)
            if m and ("unknown tactic" in e or "unsolved goals" in e or "linarith" in e or "simpa" in e or "failed to synthesize" in e):
                ln=int(m.group(1))-shift
                ls=orig.splitlines()
                if 1<=ln<=len(ls):
                    for tok in re.findall(r"[A-Za-z_][A-Za-z0-9_.']*", ls[ln-1]):
                        for c in SRC.get(tok,[]) if False else ([SRC[tok]] if isinstance(SRC.get(tok),str) else []): added.add(c)
            for nm in names:
                for h in homes(nm): added.add(h)
        added-=set(imports)
        if not added: return False, imports, [e[:150] for e in errs[:5]], shift
        log.append(sorted(added)[:6]); imports=sorted(set(imports)|added)
    return False, imports, ["maxiter"], shift
if __name__=="__main__":
    for m in sys.argv[1:]:
        ok, imps, errs, sh = check(m, base_for(m))
        print(("OK   " if ok else "FAIL "), m, "imports=",len(imps))
        if not ok:
            for e in errs:
                mm=re.match(r'.*\.lean:(\d+):',e)
                print("      ", (f"orig~{int(mm.group(1))-sh}: " if mm else "")+e[:140])
        else:
            json.dump(imps, open(".scratch/final_"+m.replace("/","_")+".json","w"))
