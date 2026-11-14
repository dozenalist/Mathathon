#!/usr/bin/env python3
"""Apply a declaration-deletion budget (m12's drop.json format) to a copy of lean/OAI.

Usage: python3 apply_drop.py <srcroot> <dstroot> <drop.json> [more.json ...]

Each json is a list of {mod,name,start,end,kind}; spans are 1-based inclusive
line spans in the *source* module and are removed bottom-up.
Reports per-module and total removed lines, and writes <dstroot>/../drop-applied.json.
"""
import json, os, shutil, sys
from collections import defaultdict


def strip_comments(lines):
    out, depth = [], 0
    for l in lines:
        res, i = [], 0
        while i < len(l):
            if depth == 0 and l.startswith('--', i):
                break
            if l.startswith('/-', i):
                depth += 1; i += 2; continue
            if depth > 0 and l.startswith('-/', i):
                depth -= 1; i += 2; continue
            if depth == 0:
                res.append(l[i])
            i += 1
        out.append(''.join(res))
    return out

def main():
    src, dst = sys.argv[1], sys.argv[2]
    drops = []
    for f in sys.argv[3:]:
        drops.extend(json.load(open(f)))
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    bymod = defaultdict(list)
    for d in drops:
        bymod[d['mod']].append(d)
    removed = defaultdict(int)
    names = defaultdict(list)
    for mod, ds in bymod.items():
        rel = mod.replace('.', '/') + '.lean'
        p = os.path.join(dst, rel)
        lines = open(p, encoding='utf-8').read().split('\n')
        keep = [True] * len(lines)
        # sanity: the first line of each span should mention the declaration name
        for d in ds:
            seg = '\n'.join(lines[d['start'] - 1:d['end']])
            if d['name'] and d['name'] not in seg:
                print(f"WARN span/name mismatch {mod}:{d['start']}-{d['end']} {d['name']}")
        # code[i] == '' exactly for blank and comment-only lines
        code = strip_comments(lines)
        for d in sorted(ds, key=lambda x: -x['start']):
            lo = d['start'] - 1
            # swallow a preceding doc-comment / attribute block, else it dangles
            while lo > 0:
                prev = code[lo - 1].strip()
                # a command modifier line ending in `in` belongs to the next command
                if prev.endswith(' in') or prev == 'in':
                    lo -= 1
                    continue
                if code[lo - 1].strip() == '' or prev.startswith('@['):
                    if lines[lo - 1].strip().startswith('@[') and code[lo - 1].strip() != '':
                        lo -= 1
                        continue
                    if code[lo - 1].strip() == '':
                        lo -= 1
                        continue
                break
            for i in range(lo, min(d['end'], len(lines))):
                if keep[i]:
                    keep[i] = False
                    removed[mod] += 1
            names[mod].append(d['name'])
        out = [l for l, k in zip(lines, keep) if k]
        open(p, 'w', encoding='utf-8').write('\n'.join(out))
    tot = sum(removed.values())
    print(f"applied {len(drops)} deletions, {tot} lines removed from {len(bymod)} modules")
    for m in sorted(removed, key=lambda x: -removed[x]):
        print(f"  {removed[m]:5d}  {m}  ({len(names[m])} decls)")
    json.dump({m: names[m] for m in names}, open(os.path.join(os.path.dirname(dst.rstrip('/')), 'drop-applied.json'), 'w'), indent=0)

if __name__ == '__main__':
    main()
