#!/usr/bin/env python3
"""Most conservative trim: drop a declaration only if its NAME occurs nowhere else.

Usage: python3 global_token_trim.py <root-with-OAI> <out.json>

A declaration is dropped iff all hold:
  * its bare (last-component) name occurs in NO other line of the whole tree
    (this covers `simp [foo]`, `rw [foo]`, `exact foo`, dot-notation, and mentions
    in comments, so it is a strong safety margin),
  * it is not instance/structure/class/inductive and carries no attribute,
  * it is not private.
Doc-comment/attribute blocks are re-attached to the following declaration.
"""
import json, os, re, sys
from collections import defaultdict

root, outf = sys.argv[1], sys.argv[2]
DECL = re.compile(r"^(?:@\[[^\]]*\]\s*)*(theorem|lemma|def|abbrev|instance|structure|class|inductive|opaque)\b\s*"
                  r"([A-Za-z_][A-Za-z0-9_'!?.]*)?")
TOK = re.compile(r"[A-Za-z_][A-Za-z0-9_'!?]*")

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

units, F = [], {}
for dp, dn, fn in os.walk(os.path.join(root, 'OAI')):
    for f in sorted(fn):
        if not f.endswith('.lean'):
            continue
        p = os.path.join(dp, f)
        mod = os.path.relpath(p, root)[:-5].replace('/', '.')
        raw = open(p, encoding='utf-8', errors='replace').read().split('\n')
        code = strip_comments(raw)
        F[mod] = (len(raw), raw, code)
        starts = [i for i, l in enumerate(code) if l and not l[0].isspace()]
        for k, i in enumerate(starts):
            end = (starts[k + 1] - 1) if k + 1 < len(starts) else len(code) - 1
            m = DECL.match(code[i].strip())
            units.append(dict(mod=mod, name=(m.group(2) if m else None),
                              kind=(m.group(1) if m else None), start=i + 1, end=end + 1,
                              attr=code[i].strip().startswith('@['),
                              private=code[i].strip().startswith('private')))
# merge doc/attribute blocks into the following declaration
merged = []
i = 0
while i < len(units):
    u = units[i]
    if u['name'] is None and i + 1 < len(units) and units[i + 1]['mod'] == u['mod']:
        head = F[u['mod']][2][u['start'] - 1].strip()
        if head.startswith('/--') or head.startswith('@['):
            nxt = dict(units[i + 1]); nxt['start'] = u['start']; merged.append(nxt); i += 2; continue
    merged.append(u); i += 1

# token -> list of (mod, line) outside the declaring unit
occ = defaultdict(list)
for u in merged:
    n = F[u["mod"]][0]
    for idx, line in enumerate(F[u['mod']][2]):
        if u['start'] - 1 <= idx <= u['end'] - 1:
            continue
        for t in TOK.findall(line):
            occ[t].append((u['mod'], idx + 1))
drop = []
for u in merged:
    if not u['name'] or u['kind'] in ('instance', 'structure', 'class', 'inductive') or u['attr'] or u['private']:
        continue
    last = u['name'].split('.')[-1]
    if occ.get(last) or occ.get(u['name']):
        continue
    drop.append(u)
bymod = defaultdict(int); cnt = defaultdict(int)
for u in drop:
    bymod[u['mod']] += u['end'] - u['start'] + 1; cnt[u['mod']] += 1
print('GLOBALLY UNMENTIONED: %d declarations, %d lines' % (len(drop), sum(bymod.values())))
for m, v in sorted(bymod.items(), key=lambda kv: -kv[1])[:18]:
    print('  %5d (%3d)  %-56s of %d' % (v, cnt[m], m, F[m][0]))
json.dump([dict(mod=u['mod'], name=u['name'], start=u['start'], end=u['end'], kind=u['kind']) for u in drop], open(outf, 'w'))
