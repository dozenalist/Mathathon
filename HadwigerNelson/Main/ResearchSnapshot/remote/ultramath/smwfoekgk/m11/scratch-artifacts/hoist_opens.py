#!/usr/bin/env python3
"""Hoist every `open`/`open scoped` of a file to two lines after its imports.

The opened-name set at each declaration only grows (names already open stay
open), so nothing that resolved before can fail to resolve; what can change is
that a name becomes ambiguous, which is a compile error, not a silent change.
Files that open a namespace which they declare themselves are left untouched.

usage: hoist_opens.py TREE_ROOT
"""
import os, re, sys

OPEN = re.compile(r'^open(\s+scoped)?\s+(.*)$')
NS = re.compile(r'^namespace\s+([\w.\']+)')
IMP = re.compile(r'^import\s')

def main():
    root = sys.argv[1]
    tot = 0
    for dp, dn, fn in os.walk(root):
        for f in sorted(fn):
            if not f.endswith('.lean'):
                continue
            p = os.path.join(dp, f)
            L = open(p).read().split('\n')
            plain, scoped, keep, lastimp = set(), set(), [], -1
            local = set()
            for l in L:
                s = l.strip()
                m = NS.match(s)
                if m:
                    local.add(m.group(1).split('.')[0])
            for i, l in enumerate(L):
                s = l.strip()
                if IMP.match(s):
                    lastimp = i
                m = OPEN.match(s)
                if m and not s.endswith(' in') and 'renaming' not in s and 'hiding' not in s:
                    names = m.group(2).split()
                    if any(n.split('.')[0] in local for n in names):
                        keep.append(l)
                        continue
                    (scoped if m.group(1) else plain).update(names)
                    tot += 1
                    continue
                keep.append(l)
            if not plain and not scoped:
                continue
            out = keep[:lastimp + 1]
            if plain:
                out.append('open ' + ' '.join(sorted(plain)))
            if scoped:
                out.append('open scoped ' + ' '.join(sorted(scoped)))
            out.extend(keep[lastimp + 1:])
            open(p, 'w').write('\n'.join(out))
    print('hoisted/removed open lines:', tot)

main()
