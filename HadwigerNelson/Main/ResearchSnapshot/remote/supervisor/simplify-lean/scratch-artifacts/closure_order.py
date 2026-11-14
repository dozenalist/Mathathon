#!/usr/bin/env python3
"""Root-closed OAI dependency list + sha256 + topological compile order for the two
atom theorem modules. Usage: cd <repo> && python3 .../closure_order.py
Deterministic, stdlib only, <1 s, writes nothing."""
import json, os, re, hashlib
ROOT = 'lean/OAI'
ROOTS = ['OAI.Analysis.PlaneSpectrum.ConditionalSpectrum',
         'OAI.MeasureTheory.CompactFactors.ConditionalLimits']
imp = re.compile(r'^import\s+(OAI\.[A-Za-z0-9_.]+)', re.M)
def path(m): return os.path.join(ROOT, m[len('OAI.'):].replace('.', '/') + '.lean')
G = {}
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if f.endswith('.lean'):
            fp = os.path.join(dp, f)
            G['OAI.' + os.path.relpath(fp, ROOT)[:-5].replace('/', '.')] = imp.findall(open(fp).read())
need, st = set(ROOTS), list(ROOTS)
while st:
    x = st.pop()
    for d in G.get(x, []):
        if d not in need and d in G:
            need.add(d); st.append(d)
order, seen = [], set()
def visit(m):
    if m in seen: return
    seen.add(m)
    for d in G.get(m, []):
        if d in need: visit(d)
    order.append(m)
for m in sorted(need): visit(m)
tot = 0
print(f'| # | module | path | lines | sha256 |')
print('|---|--------|------|-------|--------|')
for i, m in enumerate(order, 1):
    fp = path(m); n = sum(1 for _ in open(fp)); tot += n
    h = hashlib.sha256(open(fp, 'rb').read()).hexdigest()
    print(f'| {i} | `{m}` | `{fp}` | {n} | `{h}` |')
print(f'\nmodules: {len(order)}, lines: {tot}')
