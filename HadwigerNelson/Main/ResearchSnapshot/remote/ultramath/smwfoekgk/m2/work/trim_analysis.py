#!/usr/bin/env python3
"""Independent declaration-level trim budget with a complete tokenizer.

Usage: python3 trim_analysis.py <root-with-OAI> <out.json> [roots...]

Roots default to the modules that prove the kept results.  Always kept: every
declaration in a root module, every instance/structure/class/inductive, every
declaration carrying an attribute at its own start line, and every anonymous
declaration.  References are *all* identifier tokens in a declaration's line
span (so `dense_F.extend` and `measurableSet_CF.preimage` count as uses of
`dense_F` and `measurableSet_CF`).  Fixpoint from the roots.
"""
import json, os, re, sys
from collections import defaultdict

root, outf = sys.argv[1], sys.argv[2]
ROOTMODS = set(sys.argv[3:]) or {
    'OAI.Geometry.PlaneColoring.Chromatic', 'OAI.Geometry.PlaneColoring.ConnectedUnitFree',
    'OAI.Geometry.PlaneColoring.NullSetRobust', 'OAI.Geometry.PlaneColoring.Transfer'}
DECL = re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+|partial\s+|unsafe\s+)*"
                  r"(theorem|lemma|def|abbrev|instance|structure|class|inductive|opaque)\s+"
                  r"([A-Za-z_\u00a1-\uffff][A-Za-z0-9_'!?.\u00a1-\uffff]*)")
TOK = re.compile(r"[A-Za-z_\u00a1-\uffff][A-Za-z0-9_'!?.\u00a1-\uffff]*")

decls, F = [], {}
for dp, dn, fn in os.walk(os.path.join(root, 'OAI')):
    for f in sorted(fn):
        if not f.endswith('.lean'):
            continue
        p = os.path.join(dp, f)
        mod = os.path.relpath(p, root)[:-5].replace('/', '.')
        lines = open(p, encoding='utf-8', errors='replace').read().split('\n')
        F[mod] = (p, len(lines))
        n = len(lines)
        starts = []
        for i, l in enumerate(lines):
            m = DECL.match(l)
            if m:
                starts.append((i, m.group(1), m.group(2)))
        for k, (i, kind, name) in enumerate(starts):
            end = (starts[k + 1][0] - 1) if k + 1 < len(starts) else n - 1
            # a declaration's span ends before trailing blank lines
            while end > i and lines[end].strip() == '':
                end -= 1
            decls.append(dict(mod=mod, name=name, kind=kind, start=i + 1, end=end + 1,
                              attr=lines[i].lstrip().startswith('@[')))
byname = defaultdict(list)
for idx, d in enumerate(decls):
    d['idx'] = idx
    if d['name']:
        byname[d['name']].append(idx)
    for part in (d['name'] or '').split('.'):
        if part and part != d['name']:
            byname[part].append(idx)
# per-declaration reference tokens
lines_of = {}
for mod, (p, n) in F.items():
    lines_of[mod] = open(p, encoding='utf-8', errors='replace').read().split('\n')
COMMENT = re.compile(r'/-(?![^/])|-/')
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
for mod, (p, n) in F.items():
    lines_of[mod] = strip_comments(open(p, encoding='utf-8', errors='replace').read().split('\n'))
for d in decls:
    body = '\n'.join(lines_of[d['mod']][d['start'] - 1:d['end']])
    refs = set()
    for tok in TOK.findall(body):
        refs.add(tok)
        if '.' in tok:
            refs.update(tok.split('.'))
    d['refs'] = refs - {d['name']}

keep = set()
for d in decls:
    if (d['mod'] in ROOTMODS or not d['name'] or d['attr']
            or d['kind'] in ('instance', 'structure', 'class', 'inductive')):
        keep.add(d['idx'])
changed = True
while changed:
    changed = False
    used = set()
    for i in keep:
        used |= decls[i]['refs']
    for t in used:
        for j in byname.get(t, ()):
            if j not in keep:
                keep.add(j); changed = True
drop = [d for d in decls if d['idx'] not in keep]
bymod = defaultdict(int); cnt = defaultdict(int)
for d in drop:
    bymod[d['mod']] += d['end'] - d['start'] + 1; cnt[d['mod']] += 1
print('modules %d, declarations %d, total lines %d' % (len(F), len(decls), sum(v[1] for v in F.values())))
print('DROP: %d declarations, %d lines' % (len(drop), sum(bymod.values())))
for m, v in sorted(bymod.items(), key=lambda kv: -kv[1])[:22]:
    print('  %5d (%3d)  %-56s of %d' % (v, cnt[m], m, F[m][1]))
json.dump([dict(mod=d['mod'], name=d['name'], start=d['start'], end=d['end'], kind=d['kind']) for d in drop], open(outf, 'w'))
