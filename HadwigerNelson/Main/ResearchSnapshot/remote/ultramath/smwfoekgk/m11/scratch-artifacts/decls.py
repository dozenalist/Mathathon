import re, sys, pathlib, json
root = pathlib.Path("work/lean/OAI")
DECL = re.compile(r'^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+|partial\s+|unsafe\s+)*'
                  r'(theorem|lemma|def|abbrev|instance|example|structure|inductive|class|opaque)\b')
out = []
for p in sorted(root.rglob("*.lean")):
    lines = p.read_text(errors="ignore").splitlines()
    cur = None
    decls = []
    for i, l in enumerate(lines):
        m = DECL.match(l)
        if m and not l.lstrip().startswith("--"):
            if cur: decls.append(cur)
            nm = re.match(r'^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*\w+\s*([^\s:{(\[]+)?', l)
            cur = dict(kind=m.group(1), line=i+1, name=(nm.group(1) if nm else ""), text=l)
    if cur: decls.append(cur)
    for j, d in enumerate(decls):
        d["end"] = decls[j+1]["line"]-1 if j+1 < len(decls) else len(lines)
        d["len"] = d["end"] - d["line"] + 1
        d["file"] = str(p.relative_to(root))
    out += decls
out.sort(key=lambda d: -d["len"])
json.dump(out, open(".scratch/decls.json","w"))
print("decls:", len(out), "total lines covered:", sum(d["len"] for d in out))
for d in out[:25]:
    print(f'{d["len"]:5d}  {d["file"]}:{d["line"]}  {d["kind"]} {d["name"][:60]}')
