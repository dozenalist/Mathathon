#!/usr/bin/env python3
"""Hygiene pass on a cut tree: delete declaration-free modules, strip imports of
them, and drop `import OAI.X` lines that another import already implies (Lean
imports are transitive, so this cannot change elaboration)."""
import re, os, sys, pathlib, shutil

IMP = re.compile(r"^import\s+([\w.]+)\s*$")
DECL = re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:noncomputable\s+|private\s+|protected\s+|partial\s+|unsafe\s+|scoped\s+)*(theorem|lemma|def|abbrev|structure|class|instance|inductive|opaque)\s+")

def main():
    src, dst = sys.argv[1], sys.argv[2]
    dst = pathlib.Path(dst)
    if dst.exists(): shutil.rmtree(dst)
    shutil.copytree(pathlib.Path(src) / "lean", dst / "lean")
    root = dst / "lean" / "OAI"
    files, mods = {}, {}
    for p in sorted(root.rglob("*.lean")):
        m = "OAI." + ".".join(p.relative_to(root).with_suffix("").parts)
        L = p.read_text(errors="ignore").splitlines()
        files[m] = p
        mods[m] = [x.group(1) for x in (IMP.match(l) for l in L) if x]
    empty = {m for m, p in files.items()
             if not any(DECL.match(l) for l in p.read_text(errors="ignore").splitlines())}
    print("declaration-free modules:", sorted(empty))
    def anc(m, seen):
        for d in mods.get(m, []):
            if d not in seen and d in mods:
                seen.add(d); anc(d, seen)
        return seen
    removed_imports = 0
    for m, p in files.items():
        L = p.read_text(errors="ignore").splitlines()
        out = []
        kept = set()
        for d in mods[m]:
            if d not in empty and d in mods:
                kept.add(d)
        drop = set()
        for d in mods[m]:
            if d in empty:
                drop.add(d); continue
            if d in mods and d not in kept:
                continue
        # recompute redundancy over the kept imports
        impl = set()
        for d in kept:
            impl |= {d} | anc(d, set())
        for d in kept:
            if sum(1 for e in kept if d in ({e} | anc(e, set()))) and False:
                pass
        # an import d is redundant if some other kept import already implies it
        for d in kept:
            if any(d != e and d in anc(e, set()) for e in kept):
                drop.add(d)
        for l in L:
            g = IMP.match(l)
            if g and g.group(1) in drop:
                removed_imports += 1
                continue
            out.append(l)
        p.write_text("\n".join(out) + "\n")
    for m in empty:
        files[m].unlink()
    n = sum(1 for f in root.rglob("*.lean") for _ in open(f, errors="ignore"))
    print(f"removed {len(empty)} modules, {removed_imports} import lines; "
          f"final tree {n} raw lines over {len(list(root.rglob('*.lean')))} modules")

main()
