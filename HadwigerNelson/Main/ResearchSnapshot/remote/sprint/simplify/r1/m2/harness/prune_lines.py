#!/usr/bin/env python3
"""Delete declarations by exact (module, line, end) coordinates, preserving structure.

  python3 prune_lines.py --tree DIR --spec SPEC.json [--apply]

SPEC.json = {"decls": {name: {mod, line, end}}, "files": [module, ...]}
Only lines strictly inside a listed span are removed, and of those:
  * structural commands (`end`, `namespace`, `section`, `open`, `variable`, `attribute`, `local`,
    `omit`, `include`, `set_option`, `mutual`, `instance`, `noncomputable`) are KEPT — this is the
    rule whose absence broke m10's and m5's prunes (f20, f37, f38);
  * a comment block is deleted only if it is entirely inside a span.
Prints the number of lines removed per module.  The authoritative check is a build.
"""
import argparse, json, pathlib, re, sys
DECL = re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:noncomputable\s+|private\s+|protected\s+|partial\s+|unsafe\s+|scoped\s+)*"
                  r"(theorem|lemma|def|abbrev|structure|class|instance|inductive|opaque)\s+([^\s:{([]+)")
NS = re.compile(r"^namespace\s+([\w.]+)\s*$")
SEC = re.compile(r"^(?:(?:noncomputable|private|protected|public)\s+)*section(?:\s+[\w.]+)?\s*$")
MUT = re.compile(r"^mutual\s*$")
END = re.compile(r"^end(?:\s+([\w.]+))?\s*$")
STRUCT0 = {"open", "end", "namespace", "variable", "noncomputable", "omit", "include", "instance",
           "section", "local", "universe", "attribute", "scoped", "mutual", "set_option", "example",
           "notation", "infix", "infixl", "infixr", "prefix", "postfix", "macro", "syntax", "elab",
           "deriving", "import", "public", "private", "protected"}
def is_struct(ln):
    if not ln.strip(): return True
    if ln.lstrip().startswith("#"): return True
    return ln.split(None, 1)[0] in STRUCT0
def comment_blocks(lines):
    blocks, i = [], 0
    while i < len(lines):
        if "/-" in lines[i]:
            j = i
            while j < len(lines) and not (j > i and "-/" in lines[j]) and not (j == i and "-/" in lines[i][lines[i].index("/-"):]):
                j += 1
            blocks.append((i, min(j, len(lines)-1))); i = j + 1; continue
        i += 1
    return blocks
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--tree", required=True)
    ap.add_argument("--spec", required=True); ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    tree = pathlib.Path(a.tree)/"lean"; spec = json.loads(pathlib.Path(a.spec).read_text())
    by_mod = {}
    for name, v in spec["decls"].items():
        by_mod.setdefault(v["mod"], []).append((v["line"], v["end"]))
    total = 0
    for m in sorted(set(by_mod) | set(spec.get("files", []))):
        p = tree/(m.replace(".", "/")+".lean")
        if not p.exists(): print("  MISSING", m); continue
        lines = p.read_text().splitlines()
        if m in spec.get("files", []):
            print(f"  -{len(lines):5d} {m} (whole module)"); total += len(lines)
            if a.apply: p.unlink()
            continue
        kill = set()
        for s, e in by_mod[m]:
            kill |= set(range(s, e+1))
        for (a0, b0) in comment_blocks(lines):
            rng = set(range(a0+1, b0+2))
            if rng & kill and not rng <= kill: kill -= rng
        kill = {i for i in kill if not is_struct(lines[i-1])}
        if kill:
            total += len(kill); print(f"  -{len(kill):5d} {m}")
            if a.apply: p.write_text("\n".join(l for i, l in enumerate(lines, 1) if i not in kill) + "\n")
    print(f"TOTAL lines removed: {total}")
main()
