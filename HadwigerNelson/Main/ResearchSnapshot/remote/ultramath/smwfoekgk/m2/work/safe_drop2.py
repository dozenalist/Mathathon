#!/usr/bin/env python3
"""Restore deletions whose bare name still occurs in ANY kept source line of the tree.

Usage: python3 safe_drop2.py <srctree-with-OAI> <drop.json> <out.json>

Global fixpoint: a deleted declaration is restored if its name (bare or last
component) occurs as an identifier token in the kept lines of any module.  This is
the safety net for uses the Lean proof term cannot show (simp/attribute hints).
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
for dp, dn, fn in os.walk(os.path.join(src, 'OAI')):
    for f in fn:
        if f.endswith('.lean'):
            p = os.path.join(dp, f)
            text[os.path.relpath(p, src)[:-5].replace('/', '.')] = open(p, encoding='utf-8', errors='replace').read().split('\n')
TOK = re.compile(r"[A-Za-z_][A-Za-z0-9_'!?]*")
restored = []
changed = True
while changed:
    changed = False
    toks = set()
    for mod, ds in bymod.items():
        L = text[mod]
        dead = set()
        for d in ds:
            if d['dead']:
                dead.update(range(d['start'] - 1, min(d['end'], len(L))))
        for i, l in enumerate(L):
            if i not in dead:
                toks.update(TOK.findall(l))
    for mod, ds in bymod.items():
        for d in ds:
            if d['dead'] and d['name'] and (d['name'] in toks or d['name'].split('.')[-1] in toks):
                d['dead'] = False; restored.append((mod, d['name'], d['end'] - d['start'] + 1)); changed = True
kept = [d for d in drops if d['dead']]
json.dump([{k: d[k] for k in ('mod', 'name', 'start', 'end', 'kind')} for d in kept], open(outf, 'w'))
tot = sum(d['end'] - d['start'] + 1 for d in kept)
print('restored %d declarations; final removal %d decls, %d lines' % (len(restored), len(kept), tot))
