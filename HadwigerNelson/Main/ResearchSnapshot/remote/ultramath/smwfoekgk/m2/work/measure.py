#!/usr/bin/env python3
"""Per-module Lean line measurement + import closure, for sprint/simplify.

Usage: python3 measure.py [TREE_ROOT ...]
TREE_ROOT defaults to ../../../lean  (i.e. repo/lean when run from
.ultramath/smwfoekgk/m2/work).  Prints a per-module table sorted by lines,
totals, and the import closure of the headline modules.
"""
import os, sys, collections

def scan(root):
    mods, lines = {}, {}
    for dp, dn, fn in os.walk(os.path.join(root, 'OAI')):
        for f in fn:
            if f.endswith('.lean'):
                p = os.path.join(dp, f)
                rel = os.path.relpath(p, root)
                m = rel[:-5].replace('/', '.')
                mods[m] = p
                lines[m] = sum(1 for _ in open(p, encoding='utf-8', errors='replace'))
    imp = collections.defaultdict(list)
    for m, p in mods.items():
        for ln in open(p, encoding='utf-8', errors='replace'):
            s = ln.strip()
            if s.startswith('import '):
                for t in s[7:].split():
                    if t.startswith('OAI.'):
                        imp[m].append(t)
    return mods, lines, imp

def closure(imp, mods, m):
    seen, st = set(), [m]
    while st:
        x = st.pop()
        if x in seen or x not in mods:
            continue
        seen.add(x); st.extend(imp[x])
    return seen

def main():
    roots = sys.argv[1:] or [os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'lean')]
    roots = [os.path.normpath(r) for r in roots]
    tabs = []
    for r in roots:
        mods, lines, imp = scan(r)
        tabs.append((r, mods, lines, imp))
        print(f"== {r}: {len(mods)} modules, {sum(lines.values())} lines")
    if len(tabs) == 2:
        (r0, m0, l0, i0), (r1, m1, l1, i1) = tabs
        print("\n-- per-module delta (after - before), only nonzero --")
        tot = 0
        for m in sorted(set(l0) | set(l1)):
            d = l1.get(m, 0) - l0.get(m, 0)
            if d:
                tot += d
                print(f"{d:+6d}  {m}   {l0.get(m,0)} -> {l1.get(m,0)}")
        print(f"\nTOTAL DELTA: {tot:+d} lines; {len(l1)} modules vs {len(m0)}")
        gone = sorted(set(m0) - set(m1))
        new = sorted(set(l1) - set(l0))
        if gone:
            print(f"removed modules ({len(gone)}, {sum(l0[m] for m in gone)} lines): {gone}")
        if new:
            print(f"new modules ({len(new)}): {new}")
        r1, m1b, l1b, i1b = tabs[1]
        base = sum(l0.values())
        print(f"\nafter: {sum(l1.values())} lines ({(sum(l1.values())-base)/base*100:+.2f}% vs before)")
    else:
        r, mods, lines, imp = tabs[0]
        for m in sorted(lines, key=lambda x: -lines[x]):
            print(f"{lines[m]:6d}  {m}")
        for head in ('OAI.Geometry.PlaneColoring.Five', 'OAI.Geometry.PlaneColoring.Chromatic',
                     'OAI.Geometry.PlaneColoring.Transfer',
                     'OAI.Geometry.PlaneColoring.NullSetRobust'):
            if head in mods:
                c = closure(imp, mods, head)
                print(f"closure({head}) = {len(c)} mods, {sum(lines[x] for x in c)} lines")

if __name__ == '__main__':
    main()
