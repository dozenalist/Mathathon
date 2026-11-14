import re, pathlib, json, collections
ML = pathlib.Path("/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/.scratch/mathlib4")
imp = {}
for p in ML.rglob("*.lean"):
    rel = p.relative_to(ML)
    if rel.parts[0] not in ("Mathlib",): continue
    mod = ".".join(rel.with_suffix("").parts)
    deps = []
    try:
        for line in p.read_text(errors="ignore").splitlines():
            if line.startswith("import "):
                for d in line[7:].split():
                    deps.append(d)
            elif line.startswith(("theorem","lemma","def","/--","#","@")) or line.startswith("namespace"):
                break
    except Exception: pass
    imp[mod] = deps
print("mathlib modules scanned:", len(imp))
def closure(roots):
    seen=set(); st=[r for r in roots]
    while st:
        m=st.pop()
        if m in seen: continue
        seen.add(m)
        for d in imp.get(m, ()):
            if d not in seen: st.append(d)
    return seen
allm = closure(["Mathlib"])
print("closure of `import Mathlib`:", len(allm))
sets = {}
for f in sorted(pathlib.Path(".scratch/shake_out").glob("*.lean")):
    ms = [l.split()[1] for l in f.read_text().splitlines() if l.startswith("IMPORT ")]
    sets[f.stem] = ms
tot = []
for k,v in sets.items():
    c = closure(v)
    ml = {x for x in c if x.startswith("Mathlib")}
    tot.append((k, len(v), len(ml)))
    print(f"{k:52s} direct={len(v):4d} closure(mathlib)={len(ml):5d}")
U = sorted({m for v in sets.values() for m in v})
print("union direct:", len(U), "union closure:", len({x for x in closure(U) if x.startswith('Mathlib')}))
print("full Mathlib closure:", len({x for x in allm if x.startswith('Mathlib')}))
json.dump(sets, open(".scratch/shake_sets.json","w"))
