#!/usr/bin/env python3
"""Execute a measured dead-declaration deletion on a pristine copy of lean/OAI.

Input: sprint/simplify/m10/harness/PRUNE2.json  (drop_decls / drop_modules / drop_imports)
Output: <dest>/OAI  (pruned tree) ; prints per-module removed lines.
"""
import json, os, re, shutil, sys, pathlib, collections

REPO = pathlib.Path("/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo")
SRC = REPO / "lean" / "OAI"
dest = pathlib.Path(sys.argv[1]).resolve()
prune = json.load(open(REPO / "sprint/simplify/m10/harness/PRUNE2.json"))
apply_modules = "--modules" in sys.argv

if (dest / "OAI").exists():
    shutil.rmtree(dest / "OAI")
shutil.copytree(SRC, dest / "OAI")

# group deletions per module
per = collections.defaultdict(list)
for name, v in prune["drop_decls"].items():
    per[v["mod"]].append((v["line"], v["end"], v["lines"], name))

removed = 0
scope_re = re.compile(r"^(namespace\b|section\b|noncomputable section\b|end\b)")
for mod, ranges in sorted(per.items()):
    p = dest / "OAI" / (mod.split(".", 1)[1].replace(".", "/") + ".lean")
    lines = p.read_text().split("\n")
    got = 0
    keep_positions = set()
    for (a, b, n, nm) in sorted(ranges, reverse=True):
        assert 1 <= a <= b <= len(lines), (mod, nm, a, b, len(lines))
        for i in range(a - 1, b):
            if scope_re.match(lines[i].strip()):
                keep_positions.add(i)      # never delete scope structure
    for (a, b, n, nm) in sorted(ranges, reverse=True):
        del_idx = [i for i in range(a - 1, b) if i not in keep_positions]
        for i in reversed(del_idx):
            del lines[i]
        got += len(del_idx)
    p.write_text("\n".join(lines))
    print(f"{mod.split('.')[-1]:<28} removed {got:4d} lines in {len(ranges):3d} ranges")
    removed += got

# scope balance check
bad = []
for p in (dest / "OAI").glob("**/*.lean"):
    o = c = 0
    for line in p.read_text().split("\n"):
        s = line.strip()
        if scope_re.match(s):
            if s.startswith("end"):
                c += 1
            else:
                o += 1
    if o != c:
        bad.append((str(p), o, c))
print("unbalanced files:", len(bad))
for b in bad[:10]:
    print("   ", b)


if apply_modules:
    for mod in prune["drop_modules"]:
        q = dest / "OAI" / (mod.split(".", 1)[1].replace(".", "/") + ".lean")
        if q.exists():
            q.unlink()
            print("dropped module", mod)
    # strip imports of dropped modules everywhere
    for p in (dest / "OAI").glob("**/*.lean"):
        txt = p.read_text()
        out = []
        for line in txt.split("\n"):
            if any(line.strip() == "import " + m for m in prune["drop_modules"]):
                continue
            out.append(line)
        new = "\n".join(out)
        if new != txt:
            p.write_text(new)

print("total removed", removed, "lines of declarations")
