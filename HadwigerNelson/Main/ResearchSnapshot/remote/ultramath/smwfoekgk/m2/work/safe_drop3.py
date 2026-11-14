#!/usr/bin/env python3
"""Safety net over an exact (proof-term) drop list, with name disambiguation.

Usage: python3 safe_drop3.py <srctree-with-OAI> <drop.json> <out.json>

A dropped declaration is restored if its bare name occurs in the *kept* source
lines of its own module (unambiguous local use, e.g. `simp only [shift_apply]`),
or if that bare name is globally unique in the tree and occurs in the kept lines
of any module.  Global fixpoint.  Comments are stripped before matching.
"""
import json, os, re, sys
from collections import defaultdict

src, dropf, outf = sys.argv[1], sys.argv[2], sys.argv[3]
DECL = re.compile(r"^(?:@\[[^\]]*\]\s*)*(theorem|lemma|def|abbrev|instance|structure|class|inductive|opaque)\b\s*([A-Za-z_][A-Za-z0-9_'!?.]*)?")
TOK = re.compile(r"[A-Za-z_][A-Za-z0-9_'!?]*")

def strip_comments(lines):
    out, depth = [], 0
    for l in lines:
        res, i = [], 0
        while i < len(l):
            if depth == 0 and l.startswith('--', i): break
            if l.startswith('/-', i): depth += 1; i += 2; continue
            if depth > 0 and l.startswith('-/', i): depth -= 1; i += 2; continue
            if depth == 0: res.append(l[i])
            i += 1
        out.append(''.join(res))
    return out

code, allnames = {}, defaultdict(int)
for dp, dn, fn in os.walk(os.path.join(src, 'OAI')):
    for f in fn:
        if not f.endswith('.lean'): continue
        p = os.path.join(dp, f); mod = os.path.relpath(p, src)[:-5].replace('/', '.')
        raw = open(p, encoding='utf-8', errors='replace').read().split('\n')
        code[mod] = strip_comments(raw)
        for l in code[mod]:
            s = l.strip()
            if s and not l[0].isspace():
                m = DECL.match(s)
                if m and m.group(2):
                    allnames[m.group(2)] += 1
drops = json.load(open(dropf))
bymod = defaultdict(list)
for d in drops:
    d['dead'] = True; bymod[d['mod']].append(d)
restored = []
changed = True
while changed:
    changed = False
    toks = {}
    for mod, L in code.items():
        dead = set()
        for d in bymod.get(mod, ()):
            if d['dead']:
                dead.update(range(d['start'] - 1, min(d['end'], len(L))))
        ts = set()
        for i, l in enumerate(L):
            if i not in dead:
                ts.update(TOK.findall(l))
        toks[mod] = ts
    for mod, ds in bymod.items():
        for d in ds:
            if not d['dead'] or not d['name']: continue
            last = d['name'].split('.')[-1]
            local = last in toks.get(mod, ())
            glob = allnames[last] == 1 and any(last in t for t in toks.values())
            if local or glob:
                d['dead'] = False; restored.append((mod, d['name'], d['end'] - d['start'] + 1)); changed = True
kept = [d for d in drops if d['dead']]
json.dump([{k: d[k] for k in ('mod', 'name', 'start', 'end', 'kind')} for d in kept], open(outf, 'w'))
print('restored %d; final removal %d decls, %d lines' % (len(restored), len(kept), sum(d['end'] - d['start'] + 1 for d in kept)))
