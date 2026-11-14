#!/usr/bin/env python3
"""Exact dead-declaration trim: Lean-environment constant dependency graph.

Usage: python3 exact_trim.py <root-with-OAI> <deps.txt> <out.json>

deps.txt comes from deps.lean: lines `fullName|dep1 dep2 ...` for every constant in
the environment of the four kept-result root modules, with references taken from the
constant's type and value (so tactic-generated proofs are included).

A source declaration is dropped iff
  * its full name is not reachable from the root declarations, and
  * its name is not mentioned in any non-declaration command of any module,
and it is not private / attributed / instance / structure / class / inductive.
"""
import json, os, re, sys
from collections import defaultdict

root, depsf, outf = sys.argv[1], sys.argv[2], sys.argv[3]
ROOTMODS = {'OAI.Geometry.PlaneColoring.Chromatic', 'OAI.Geometry.PlaneColoring.ConnectedUnitFree',
            'OAI.Geometry.PlaneColoring.NullSetRobust', 'OAI.Geometry.PlaneColoring.Transfer'}
DECL = re.compile(r"^(?:@\[[^\]]*\]\s*)*"
                  r"(theorem|lemma|def|abbrev|instance|structure|class|inductive|opaque)\b\s*"
                  r"([A-Za-z_\u00a1-\uffff][A-Za-z0-9_'!?.\u00a1-\uffff]*)?")
TOK = re.compile(r"[A-Za-z_\u00a1-\uffff][A-Za-z0-9_'!?.\u00a1-\uffff]*")

deps = {}
for line in open(depsf, encoding='utf-8'):
    line = line.rstrip('\n')
    if not line:
        continue
    n, _, rest = line.partition('|')
    deps[n] = rest.split() if rest else []
print(f'constants: {len(deps)}; OAI constants: {sum(1 for n in deps if n.startswith("OAI."))}')

units, modlines = [], {}
for dp, dn, fn in os.walk(os.path.join(root, 'OAI')):
    for f in sorted(fn):
        if not f.endswith('.lean'):
            continue
        p = os.path.join(dp, f)
        mod = os.path.relpath(p, root)[:-5].replace('/', '.')
        raw = open(p, encoding='utf-8', errors='replace').read().split('\n')
        modlines[mod] = raw
        starts = [i for i, l in enumerate(raw) if l and not l[0].isspace()]
        for k, i in enumerate(starts):
            end = (starts[k + 1] - 1) if k + 1 < len(starts) else len(raw) - 1
            while end > i and raw[end].strip() == '':
                end -= 1
            head = raw[i].strip()
            m = DECL.match(head)
            units.append(dict(mod=mod, name=(m.group(2) if m else None),
                              kind=(m.group(1) if m else None), start=i + 1, end=end + 1,
                              attr=head.startswith('@['), private='private' in head.split('{')[0]))

# merge docstring/attribute-only units into the declaration that follows them,
# so that deleting a declaration cannot leave a dangling doc comment or attribute
merged = []
for u in units:
    head = modlines[u['mod']][u['start'] - 1].strip()
    if (u['name'] is None and merged and merged[-1]['mod'] == u['mod']
            and (head.startswith('/--') or head.startswith('@[') or head.startswith('-- '))):
        pass
    merged.append(u)
units2 = []
i = 0
while i < len(merged):
    u = merged[i]
    if u['name'] is None and i + 1 < len(merged) and merged[i + 1]['mod'] == u['mod']:
        head = modlines[u['mod']][u['start'] - 1].strip()
        if head.startswith('/--') or head.startswith('@['):
            nxt = dict(merged[i + 1])
            nxt['start'] = u['start']
            units2.append(nxt)
            i += 2
            continue
    units2.append(u)
    i += 1
units = units2
# namespace tracking -> full names
cur = []
for u in units:
    L = modlines[u['mod']]
    # recompute namespace state by walking this module from the top each time is too slow;
    # instead do a single pass below
u_ns = {}
for u in units:
    u_ns[u['start'], u['mod']] = None
state = defaultdict(list)
for u in units:
    pass
names = {}
stacks = defaultdict(list)
for u in units:
    stack = stacks[u['mod']]
    L = modlines[u['mod']]
    head = L[u['start'] - 1].strip()
    words = head.split()
    if words and words[0] == 'namespace':
        stack.append(('ns', words[1]))
    elif words and words[0] == 'section':
        stack.append(('sec', None))
    elif words and words[0] == 'end':
        if stack:
            stack.pop()
    else:
        if u['name']:
            pre = '.'.join(n for k, n in stack if k == 'ns')
            names[(u['mod'], u['start'])] = (pre + '.' + u['name']) if pre else u['name']
for u in units:
    u['full'] = names.get((u['mod'], u['start']))

# roots: every declaration whose module is a root module
roots = {u['full'] for u in units if u['mod'] in ROOTMODS and u['full']}
print(f'root declarations: {len(roots)}')
seen, work = set(), list(roots)
while work:
    n = work.pop()
    if n in seen:
        continue
    seen.add(n)
    for d in deps.get(n, ()):
        if d not in seen:
            work.append(d)
print(f'reachable constants: {len(seen)} (of which OAI: {sum(1 for n in seen if n.startswith("OAI."))})')

# tokens in non-declaration commands (must survive: elaboration may need the name)
nod = set()
for u in units:
    if not u['name']:
        for tok in TOK.findall('\n'.join(modlines[u['mod']][u['start'] - 1:u['end']])):
            nod.add(tok)
            if '.' in tok:
                nod.update(tok.split('.'))

keep, drop = [], []
for u in units:
    if not u['name']:
        continue
    full = u['full']
    ok = (u['kind'] in ('instance', 'structure', 'class', 'inductive') or u['attr'] or u['private']
          or (full is not None and full in seen)
          or u['name'] in nod or u['name'].split('.')[-1] in nod)
    (keep if ok else drop).append(u)
bymod = defaultdict(int); cnt = defaultdict(int)
for u in drop:
    bymod[u['mod']] += u['end'] - u['start'] + 1; cnt[u['mod']] += 1
print('EXACT DROP: %d declarations, %d lines' % (len(drop), sum(bymod.values())))
for m, v in sorted(bymod.items(), key=lambda kv: -kv[1])[:25]:
    print('  %5d (%3d)  %-58s of %d' % (v, cnt[m], m, len(modlines[m])))
json.dump([dict(mod=u['mod'], name=u['name'], start=u['start'], end=u['end'], kind=u['kind'])
           for u in drop], open(outf, 'w'))
