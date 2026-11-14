#!/usr/bin/env python3
"""Which OAI identifiers used by EncodingCore's body are NOT reachable from its own imports?
Usage: cd <repo> && python3 supervisor/simplify-lean/.scratch/check_scope.py [snapshot_dir]
Deterministic, stdlib only, <1 s. Prints the import closure size, the two import-direction
facts, and the missing-identifier table."""
import os, re, sys
ROOT = 'lean/OAI'
SNAP = sys.argv[1] if len(sys.argv) > 1 else 'supervisor/simplify-lean/snapshots/enc-feb15b727d97c29c'
imp = re.compile(r'^import\s+(OAI\.[A-Za-z0-9_.]+)', re.M)
decl = re.compile(r'^(?:@\[[^\n]*\]\s*)?(?:private |protected |noncomputable |partial |local |scoped )*'
                  r'(?:theorem|lemma|def|abbrev|structure|inductive|class|instance)\s+([A-Za-z0-9_\'!?]+)', re.M)
G, owner = {}, {}
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if not f.endswith('.lean'):
            continue
        fp = os.path.join(dp, f)
        m = 'OAI.' + os.path.relpath(fp, ROOT)[:-5].replace('/', '.')
        src = open(fp).read()
        G[m] = imp.findall(src)
        for n in decl.findall(src):
            owner.setdefault(n, set()).add(m)
def clos(x):
    seen, st = set(), [x]
    while st:
        y = st.pop()
        if y in seen: continue
        seen.add(y); st.extend(G.get(y, []))
    return seen
CS = 'OAI.Analysis.PlaneSpectrum.ConditionalSpectrum'
CL = 'OAI.MeasureTheory.CompactFactors.ConditionalLimits'
print(f'{CL} imports {CS}:', CS in clos(CL))
print(f'{CS} imports {CL}:', CL in clos(CS))
roots = ['OAI.Analysis.PlaneSpectrum.FourierTests', 'OAI.Analysis.PlaneSpectrum.SmallArcs',
         'OAI.MeasureTheory.CompactFactors.ConditionalSelection']
U = set(roots)
for r in roots: U |= clos(r)
print('union closure of EncodingCore.lean\'s 3 imports:', len(U), 'modules;',
      'ConditionalSpectrum in it:', CS in U)
body = open(os.path.join(SNAP, 'EncodingCore.lean')).read()
body = body[body.index('theorem uniform_precision_contradiction'):]
missing = []
for n in sorted(set(re.findall(r'[A-Za-z_][A-Za-z0-9_\']*', body))):
    if n in owner and n != 'EncodingApproximationAt' and not (owner[n] & U):
        missing.append((n, sorted(owner[n])))
print('identifiers defined in OAI but unreachable from those imports:', len(missing))
for n, f in missing:
    print(f'  {n:38s} {f}')
