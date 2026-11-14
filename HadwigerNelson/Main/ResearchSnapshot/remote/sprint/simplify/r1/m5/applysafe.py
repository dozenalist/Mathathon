#!/usr/bin/env python3
"""Apply a safe dead-declaration set to a tree, preserving every structural line."""
import json, re, sys, pathlib, shutil, collections

ENDL = re.compile(r"^\s*end(\s|$)")
STRUCT = re.compile(r"^\s*(variable|open|section|omit|attribute|set_option|universe|local\b|private\b|scoped\b|noncomputable\b|include\b|namespace\b)\b")

def region(lines, start, end):
    j = end
    while j > start and lines[j-1].strip() == '': j -= 1
    while j > start and (ENDL.match(lines[j-1]) or STRUCT.match(lines[j-1])
                         or lines[j-1].lstrip().startswith('--')): j -= 1
    if j > start and lines[j-1].strip().endswith('-/'):
        k = j - 1
        while k > start and not lines[k-1].strip().startswith('/--'): k -= 1
        j = k
    while j > start and lines[j-1].strip() == '': j -= 1
    return j

def main():
    dead = json.load(open(sys.argv[1]))
    src, dst = sys.argv[2], sys.argv[3]
    if pathlib.Path(dst).exists(): shutil.rmtree(dst)
    shutil.copytree(pathlib.Path(src) / "lean" / "OAI", pathlib.Path(dst) / "lean" / "OAI")
    bymod = collections.defaultdict(list)
    for d in dead: bymod[d["mod"]].append(d)
    removed = 0
    for mod, ds in bymod.items():
        p = pathlib.Path(dst) / "lean" / "OAI" / (mod.replace(".", "/") + ".lean")
        lines = p.read_text(errors="ignore").splitlines()
        for d in sorted(ds, key=lambda d: -d["line"]):
            start, end = d["line"], min(d["end"], len(lines))
            j = region(lines, start, end)
            keep = [lines[k] for k in range(start-1, j)
                    if ENDL.match(lines[k]) or STRUCT.match(lines[k])]
            removed += (j - (start-1)) - len(keep)
            lines[start-1:j] = keep
        p.write_text("\n".join(lines) + "\n")
    n = sum(1 for f in (pathlib.Path(dst) / "lean" / "OAI").rglob("*.lean")
            for _ in open(f, errors="ignore"))
    print(f"removed {removed} raw lines; tree now {n} raw lines")

main()
