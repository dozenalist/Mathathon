import re, pathlib, sys, json
ROOT = pathlib.Path("lean")
pat = re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+|partial\s+|unsafe\s+|scoped\s+|local\s+)*"
                 r"(theorem|lemma|def|abbrev|instance|structure|inductive|class|example)\s+([A-Za-z_][\w.'‹›₀-₉]*)")
out = []
for p in sorted(ROOT.glob("OAI/**/*.lean")):
    mod = ".".join(p.relative_to(ROOT).with_suffix("").parts)
    lines = p.read_text(errors="ignore").splitlines()
    starts = []
    for i, l in enumerate(lines):
        m = pat.match(l)
        if m: starts.append((i, m.group(1), m.group(2)))
    for k, (i, kind, name) in enumerate(starts):
        end = starts[k+1][0] if k+1 < len(starts) else len(lines)
        out.append({"mod": mod, "kind": kind, "name": name, "line": i+1, "len": end-i})
json.dump(out, open(".ultramath/smwfoekgk/m13/decls.json","w"))
print("decls:", len(out))
import collections
agg = collections.defaultdict(int)
for d in out: agg[d["mod"]] += d["len"]
print("\n== biggest declarations in Geometry ==")
for d in sorted([d for d in out if "Geometry" in d["mod"]], key=lambda d: -d["len"])[:25]:
    print(f'{d["len"]:5d}  {d["mod"].replace("OAI.Geometry.PlaneColoring.","")}:{d["line"]}  {d["kind"]} {d["name"]}')
print("\n== biggest declarations everywhere ==")
for d in sorted(out, key=lambda d: -d["len"])[:20]:
    print(f'{d["len"]:5d}  {d["mod"]}:{d["line"]}  {d["kind"]} {d["name"]}')
