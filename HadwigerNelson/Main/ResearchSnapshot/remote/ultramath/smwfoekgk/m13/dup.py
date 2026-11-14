import re, pathlib, json, collections, hashlib
ROOT = pathlib.Path("lean")
decls = json.load(open(".ultramath/smwfoekgk/m13/decls.json"))
byt = collections.defaultdict(list)
for d in decls: byt[d["mod"]].append(d)
def stmt_text(mod, d):
    p = ROOT / (mod.replace(".", "/") + ".lean")
    lines = p.read_text(errors="ignore").splitlines()
    seg = lines[d["line"]-1 : d["line"]-1+d["len"]]
    out = []
    for l in seg:
        s = l.strip()
        if s.startswith(("theorem","lemma")) and ":=" in s:
            out.append(s.split(":=")[0]); break
        if l.rstrip().endswith(":= by") or l.strip()==":= by": break
        out.append(s)
        if re.search(r":=\s*by\s*$", l) or l.rstrip().endswith(":= by"): break
    t = " ".join(out)
    t = t.split(":= by")[0]
    t = re.sub(r"^(theorem|lemma)\s+", "", t)
    t = re.sub(r"^[\w.'‹›₀-₉]+\s*", "", t)          # drop name
    t = re.sub(r"\s+", " ", t)
    return t
seen = collections.defaultdict(list)
for mod, ds in byt.items():
    for d in ds:
        if d["kind"] not in ("theorem","lemma"): continue
        try: t = stmt_text(mod, d)
        except Exception: continue
        if len(t) < 25: continue
        seen[t].append((mod.replace("OAI.",""), d["line"], d["len"], d["name"]))
groups = {k: v for k, v in seen.items() if len(v) > 1}
tot = 0
print(f"exact duplicate statements: {len(groups)} groups")
for k, v in sorted(groups.items(), key=lambda kv: -sum(x[2] for x in kv[1]))[:18]:
    s = sum(x[2] for x in v)
    tot += s
    print(f"  [{s:3d} lines] {len(v)} copies: " + " | ".join(f'{m.split(".")[-1]}:{l}' for m,l,_,_ in v))
    print(f"        {k[:150]}")
