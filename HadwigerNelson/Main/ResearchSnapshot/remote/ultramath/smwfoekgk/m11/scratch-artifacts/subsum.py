import re, sys, json, pathlib, collections
sys.path.insert(0,'.scratch'); import autoexp
ROOT = autoexp.ROOT
def tokenize(s):
    return re.findall(r'[A-Za-z_][A-Za-z0-9_.\'!?]*|\S', s)
rows = []
for p in sorted(ROOT.rglob("*.lean")):
    rel = str(p.relative_to(ROOT))
    lines = p.read_text(errors="ignore").splitlines()
    ds = autoexp.decls_of(lines)
    for i, d in enumerate(ds):
        if d["kind"] not in ("theorem","lemma"): continue
        sub = lines[d["line"]-1:d["end"]]
        # statement = up to the line containing ':='
        stmt = []
        k = 0
        while k < len(sub):
            stmt.append(sub[k])
            if ":=" in sub[k]: break
            k += 1
        rows.append(dict(file=rel, line=d["line"], name=d["name"], total=d["end"]-d["line"]+1,
                         stmt=" ".join(stmt), stmtlen=len(stmt), toks=tokenize(" ".join(stmt))))
print("decls", len(rows))
# 1) exact duplicate statements (normalised) across whole tree
norm = lambda t: " ".join(x for x in t if x not in ("(", ")", "[", "]", "{", "}", ","))
by = collections.defaultdict(list)
for r in rows: by[norm(r["toks"])].append(r)
dups = [v for v in by.values() if len(v)>1]
print("== exact-statement groups:", len(dups), "decls involved:", sum(len(v) for v in dups),
      "lines:", sum(sum(x["total"] for x in v) for v in dups))
for v in sorted(dups, key=lambda v: -sum(x["total"] for x in v))[:12]:
    print("  ", [(x["file"].split("/")[-1], x["line"], x["name"], x["total"]) for x in v])
# 2) within-file similarity clusters on statements
import itertools
best = []
for f, grp in itertools.groupby(sorted(rows, key=lambda r: r["file"]), key=lambda r: r["file"]):
    g = list(grp)
    for a, b in itertools.combinations(g, 2):
        sa, sb = set(a["toks"]), set(b["toks"])
        if not sa or not sb: continue
        j = len(sa & sb)/len(sa | sb)
        if j > 0.62 and abs(a["total"]-b["total"]) >= 6:
            best.append((j, abs(a["total"]-b["total"]), f, a, b))
best.sort(key=lambda x: -x[1])
print("== within-file close-statement pairs with >=6 line gap:", len(best), "gap mass:", sum(b[1] for b in best))
for j,gap,f,a,b in best[:15]:
    print(f"  gap{gap:4d} j{j:.2f} {f.split('/')[-1]}: {a['name'][:34]}({a['total']}) vs {b['name'][:34]}({b['total']})")
json.dump(rows, open(".scratch/stmts.json","w"))
