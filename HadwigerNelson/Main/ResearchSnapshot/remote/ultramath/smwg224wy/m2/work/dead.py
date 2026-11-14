import json, pathlib, collections, sys
H = pathlib.Path("/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/sprint/simplify/m10/harness")
sys.path.insert(0, str(H))
import importlib.util
spec = importlib.util.spec_from_file_location("an", H/"analyze.py")
# avoid running main(): copy load/closure by exec of the source without the trailing main() call
src = (H/"analyze.py").read_text().replace("\nmain()\n", "\n")
ns = {"__file__": str(H/"analyze.py")}
exec(compile(src, "analyze.py", "exec"), ns)
nodes, et, ev = ns["load"]()
sp = ns["spans"]()
red = ns["closure"](nodes, et, ev)
outside = {n for n in sp if n not in red}
per = collections.Counter(); cnt = collections.Counter()
for n in outside:
    per[sp[n]["mod"]] += sp[n]["lines"]; cnt[sp[n]["mod"]] += 1
print(f"closure nodes {len(red)}; spanned decls in closure {sum(1 for n in red if n in sp)}")
print(f"spanned decls OUTSIDE closure: {len(outside)} decls, {sum(per.values())} lines")
print(f"total span lines {sum(v['lines'] for v in sp.values())}")
for m,l in per.most_common():
    print(f"{l:6d} {cnt[m]:4d}  {m}")
# also: modules with zero spanned decls in closure
allmods = collections.Counter()
for n,v in sp.items(): allmods[v["mod"]] += v["lines"]
mods_in = {sp[n]["mod"] for n in red if n in sp}
print("\nmodules entirely outside the closure:", [m for m in allmods if m not in mods_in])
