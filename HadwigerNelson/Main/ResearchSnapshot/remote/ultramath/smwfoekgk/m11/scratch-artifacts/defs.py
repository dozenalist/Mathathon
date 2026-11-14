import re, sys, json, pathlib, collections
sys.path.insert(0,'.scratch'); import autoexp
ROOT = autoexp.ROOT
rows = json.load(open(".scratch/stmts.json"))
# collect def-like decls
defs = []
for p in sorted(ROOT.rglob("*.lean")):
    rel=str(p.relative_to(ROOT)); lines=p.read_text(errors="ignore").splitlines()
    for d in autoexp.decls_of(lines):
        if d["kind"] in ("def","structure","inductive","class","abbrev","opaque"):
            defs.append(dict(file=rel, line=d["line"], name=d["name"], kind=d["kind"], total=d["end"]-d["line"]+1))
print("defs", len(defs))
names = {}
for d in defs:
    n = d["name"].split(".")[-1]
    if len(n)>=3 and re.match(r'^[A-Za-z_]', n): names.setdefault(n, []).append(d)
# attribute rows to defs by token mention
mass = collections.defaultdict(lambda: [0,0,0])  # n_lemmas, total_lines, proof_lines
for r in rows:
    toks = set(r["toks"])
    for n, ds in names.items():
        if n in toks:
            m = mass[n]; m[0]+=1; m[1]+=r["total"]
best = sorted(mass.items(), key=lambda kv: -kv[1][1])[:40]
print(f'{"def":28s} {"#lem":>5s} {"tot":>6s} {"avg":>6s}  file')
for n,(c,t,_) in best:
    d = names[n][0]
    print(f'{n:28s} {c:5d} {t:6d} {t/max(c,1):6.1f}  {d["file"].split("/")[-1]}:{d["line"]} ({d["kind"]},{d["total"]}l)')
json.dump({n:[c,t] for n,(c,t,_) in mass.items()}, open(".scratch/defmass.json","w"))
