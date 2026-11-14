import re, pathlib, collections
ROOT = pathlib.Path("/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/lean")
def lines(m):
    p = ROOT / (m.replace(".","/")+".lean")
    return len(p.read_text(errors="ignore").splitlines()) if p.exists() else 0
data = collections.defaultdict(dict)   # target -> module -> (def, used, usednames)
tot = {}
for ln in pathlib.Path("used.log").read_text().splitlines():
    if not ln.startswith("@@@"): continue
    parts = ln[3:].split("\t")
    if parts[1] == "usedconstants":
        tot[parts[0]] = int(parts[2]); continue
    tgt, mod, d, u = parts[0], parts[1], int(parts[2]), int(parts[3])
    names = []
    data[tgt][mod] = (d,u,names)
for tgt in data:
    print("="*100); print(tgt, "used constants total:", tot.get(tgt))
    ms = data[tgt]
    Dz = sum(d for d,u,_ in ms.values()); Uz = sum(u for d,u,_ in ms.values())
    print(f"  OAI constants defined in dev: {Dz}, used by target: {Uz}")
    dead = [m for m,(d,u,_) in ms.items() if u==0]
    print(f"  modules in dev: {len(ms)}, with 0 used constants: {len(dead)} = {sum(lines(m) for m in dead)} lines")
    print("  DEAD modules:", *[f"{m.split('.',1)[1]}({lines(m)}L)" for m in sorted(dead)], sep="\n    ")
    live = [(m,d,u,lines(m)) for m,(d,u,_) in ms.items() if u>0]
    print(f"  live modules: {len(live)} = {sum(l for _,_,_,l in live)} lines")
    print("  live modules with low use (used/defined, lines):")
    for m,d,u,l in sorted(live, key=lambda x: x[2]/max(x[1],1)):
        print(f"    {m.split('.',1)[1]:58s} {u:4d}/{d:4d}  {l:5d}L")
