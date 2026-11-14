import re, pathlib, json, collections
ROOT = pathlib.Path("/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/lean")
txt = pathlib.Path("edges.log").read_text()
# parse blocks: "@@@MOD\tK\t[names,]"
use = collections.defaultdict(set)
for m in re.finditer(r"@@@([\w.]+)\t(\d+)\t\[(.*?)\]", txt, re.S):
    f = m.group(1); names = re.findall(r"OAI\.[\w.]+", m.group(3))
    use[f] = set(names)
print("modules with edge data:", len(use))
# declared imports
imports = {}
for p in sorted(ROOT.glob("OAI/**/*.lean")):
    name = ".".join(p.relative_to(ROOT).with_suffix("").parts)
    imports[name] = [d for d in re.findall(r"^import\s+(OAI\.[\w.]+)\s*$", p.read_text(errors="ignore"), re.M)]
def lines(m):
    p = ROOT / (m.replace(".","/")+".lean"); return len(p.read_text(errors="ignore").splitlines())
def closure_use(roots):
    seen, st = set(), list(roots)
    while st:
        n = st.pop()
        if n in seen: continue
        seen.add(n); st.extend(use.get(n, ()))
    return seen
json.dump({k: sorted(v) for k,v in use.items()}, open("use.json","w"), indent=0)
json.dump(imports, open("imports.json","w"), indent=0)
# For the transfer target
T = "OAI.Geometry.PlaneColoring.Transfer"
R = closure_use([T]) - {T}
print(f"transfer: use-closure = {len(R|{T})} modules, {sum(lines(m) for m in R|{T})} lines")
# import closure
def closure_imp(roots):
    seen, st = set(), list(roots)
    while st:
        n = st.pop()
        if n in seen or n not in imports: continue
        seen.add(n); st.extend(imports[n])
    return seen
I = closure_imp([T])
print(f"transfer: import-closure = {len(I)} modules, {sum(lines(m) for m in I)} lines")
print("in import closure, NOT used:", sorted(set(I)-set(R)-{T}))
print("used but not imported (would be a bug):", sorted(set(R)-set(I)))
# per-file prunable imports
totpr = 0
print("\nper-file prunable OAI imports (declared but not used by the file's own constants):")
for f in sorted(imports):
    pr = [d for d in imports[f] if d not in use.get(f, set())]
    if pr:
        print(f"  {f.split('.',1)[1]:58s} drop {[x.split('.')[-1] for x in pr]}  ({sum(lines(x) for x in pr)} lines)")
        totpr += len(pr)
print("total prunable import edges:", totpr)
