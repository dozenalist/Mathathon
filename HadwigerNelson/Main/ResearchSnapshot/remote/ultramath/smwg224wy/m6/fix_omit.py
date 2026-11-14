#!/usr/bin/env python3
"""Drop `omit ... in` prefixes in files the pruner touched.

A deletion can leave an `omit` (a) dangling, or (b) naming a section variable that no
longer exists in scope.  `omit` is only an optimisation of which section variables a
declaration carries, so removing all of them from the touched files is sound to try;
the build is the check.
"""
import pathlib, re, sys
touched = set()
for ln in pathlib.Path("apply.log").read_text().splitlines():
    m = re.match(r"^\s*-\s*\d+\s+(OAI\.[\w.]+)", ln)
    if m: touched.add(m.group(1))
n = 0
for mod in touched:
    p = pathlib.Path("tree/lean") / (mod.replace(".", "/") + ".lean")
    if not p.exists(): continue
    lines = p.read_text().splitlines(keepends=True)
    out = []
    for l in lines:
        if re.match(r"^\s*omit\b.*\bin\s*$", l):
            n += 1
            continue
        out.append(l)
    p.write_text("".join(out))
print(f"fix_omit: removed {n} `omit` prefixes from {len(touched)} touched modules")
