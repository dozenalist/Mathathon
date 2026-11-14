#!/usr/bin/env python3
"""Declaration-level trim budget, v2: column-0 units, anonymous declarations kept.

Usage: python3 trim_analysis2.py <root-with-OAI> <out.json> [rootmodule ...]

A *unit* is a maximal run of lines starting at a line with no leading whitespace.
Units that do not start a declaration (open/variable/namespace/section/attribute/
set_option/example/#check/...) are always kept.  Anonymous `instance`/`example`
units are kept.  Declarations carrying an attribute at their first line are kept,
as are instance/structure/class/inductive.  References = all identifier tokens
(dot-split) of the unit, comments stripped.
"""
import json, os, re, sys
from collections import defaultdict

root, outf = sys.argv[1], sys.argv[2]
ROOTMODS = set(sys.argv[3:]) or {
    'OAI.Geometry.PlaneColoring.Chromatic', 'OAI.Geometry.PlaneColoring.ConnectedUnitFree',
    'OAI.Geometry.PlaneColoring.NullSetRobust', 'OAI.Geometry.PlaneColoring.Transfer'}
DECL = re.compile(r"^(?:theorem|lemma|def|abbrev|instance|structure|class|inductive|opaque)\b\s*"
                  r"([A-Za-z_\u00a1-\uffff][A-Za-z0-9_'!?.\u00a1-\uffff]*)?")
ATTR = re.compile(r"^@\[")
TOK = re.compile(r"[A-Za-z_\u00a1-\uffff][A-Za-z0-9_'!?.\u00a1-\uffff]*")

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
        F[mod] = len(raw)
        code = strip_comments(raw)
        starts = [i for i, l in enumerate(code) if l and not l[0].isspace()]
        for k, i in enumerate(starts):
            end = (starts[k + 1] - 1) if k + 1 < len(starts) else len(code) - 1
            # an attribute block belongs to the declaration that follows it
            first = i
            while first < end and ATTR.match(code[first]) and code[first + 1].lstrip().startswith('@['):
                first += 1
            head = code[i].strip()
            m = DECL.match(head)
            name, kind, isdecl = (m.group(1) if m else None), (m.group(0).split()[0] if m else None), bool(m)
            if isdecl and name is None:
                # anonymous instance/example-like: keep
                isdecl = True
            body = '\n'.join(code[i:end + 1])
            refs = set()
            for tok in TOK.findall(body):
                refs.add(tok)
                if '.' in tok:
                    refs.update(tok.split('.'))
            units.append(dict(mod=mod, name=name, kind=kind, start=i + 1, end=end + 1,
                              decl=isdecl, attr=bool(ATTR.match(code[i].strip())),
                              anon=(isdecl and name is None), refs=refs))
byname = defaultdict(list)
for idx, u in enumerate(units):
    u['idx'] = idx
    if u['name']:
        byname[u['name']].append(idx)
        parts = u['name'].split('.')
        for part in parts[1:]:
            byname[part].append(idx)
        for k in range(2, len(parts) + 1):
            byname['.'.join(parts[-k:])].append(idx)
keep = set()
for u in units:
    if (u['mod'] in ROOTMODS or not u['decl'] or u['attr'] or u['anon']
            or u['kind'] in ('instance', 'structure', 'class', 'inductive')):
        keep.add(u['idx'])
changed = True
while changed:
    changed = False
    used = set()
    for i in keep:
        used |= units[i]['refs']
    for t in used:
        for j in byname.get(t, ()):
            if j not in keep:
                keep.add(j); changed = True
drop = [u for u in units if u['idx'] not in keep]
bymod = defaultdict(int); cnt = defaultdict(int)
for u in drop:
    bymod[u['mod']] += u['end'] - u['start'] + 1; cnt[u['mod']] += 1
print('modules %d, units %d, decl-units %d, total lines %d'
      % (len(F), len(units), sum(u['decl'] for u in units), sum(F.values())))
print('DROP: %d declarations, %d lines' % (len(drop), sum(bymod.values())))
for m, v in sorted(bymod.items(), key=lambda kv: -kv[1])[:20]:
    print('  %5d (%3d)  %-56s of %d' % (v, cnt[m], m, F[m]))
json.dump([dict(mod=u['mod'], name=u['name'], start=u['start'], end=u['end'], kind=u['kind'])
           for u in drop], open(outf, 'w'))
