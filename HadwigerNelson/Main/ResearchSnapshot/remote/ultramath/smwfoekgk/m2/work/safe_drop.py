#!/usr/bin/env python3
"""Restore deletions whose name still occurs in kept source (projective/dot uses).

Usage: python3 safe_drop.py <srctree-with-OAI> <drop.json> <out.json>

A deleted declaration is restored if its bare name occurs as an identifier token
anywhere in the lines that survive.  Runs to a fixpoint (restored lines can
mention further deleted names).  This turns a purely reachability-based budget
into a source-level self-consistent one; it cannot certify attribute-based uses.
"""
import json, os, re, sys
from collections import defaultdict

src, dropf, outf = sys.argv[1], sys.argv[2], sys.argv[3]
drops = json.load(open(dropf))
bymod = defaultdict(list)
for d in drops:
    d['dead'] = True
    bymod[d['mod']].append(d)

text = {}
for mod in bymod:
    p = os.path.join(src, mod.replace('.', '/') + '.lean')
    text[mod] = open(p, encoding='utf-8').read().split('\n')

ident = re.compile(r"[A-Za-z_][A-Za-z0-9_'!?]*")
def kept_text(mod):
    lines = text[mod]
    dead = set()
    for d in bymod[mod]:
        if d['dead']:
            dead.update(range(d['start'] - 1, min(d['end'], len(lines))))
    return [l for i, l in enumerate(lines) if i not in dead], dead

restored = []
changed = True
while changed:
    changed = False
    for mod, ds in bymod.items():
        kt, _ = kept_text(mod)
        toks = set()
        for l in kt:
            toks.update(ident.findall(l))
        for d in ds:
            if not d['dead'] or not d['name']:
                continue
            if d['name'] in toks:
                d['dead'] = False
                restored.append((mod, d['name'], d['end'] - d['start'] + 1))
                changed = True

kept = [d for d in drops if d['dead']]
json.dump([{k: d[k] for k in ('mod', 'name', 'start', 'end', 'kind')} for d in kept], open(outf, 'w'))
tot = sum(d['end'] - d['start'] + 1 for d in kept)
print(f"restored {len(restored)} declarations; final removal {len(kept)} decls, {tot} lines")
for m, n, l in restored[:40]:
    print(f"   restored {n} ({l} lines) in {m}")
