#!/usr/bin/env python3
"""Surgery certificate: exact deletable module set for the Theorem-A route.

Protection rule (conservative): a module M is deletable only if
  (a) every module that imports M is itself deletable, and
  (b) no kept file mentions any declaration name defined in M.
This over-approximates the dependency, so it never deletes a needed module.
"""
import os, re, json, collections, sys
R='/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/lean/OAI'
mods={}; text={}
for root,_,fs in os.walk(R):
    for f in fs:
        if f.endswith('.lean'):
            p=os.path.join(root,f); n='OAI.'+os.path.relpath(p,R).replace('/','.')[:-5]
            t=open(p).read(); text[n]=t
            mods[n]=dict(path=os.path.relpath(p,R), lines=len(t.splitlines()),
                imports=[m.group(1) for m in (re.match(r'^import\s+(OAI\.[\w.]+)\s*$',l) for l in t.splitlines()) if m])
decl=json.load(open('decls2.json'))
bymod=collections.defaultdict(set)
for d in decl:
    n='OAI.'+d['file'][:-5].replace('/','.')
    bymod[n].add(d['name'])
words={n:collections.Counter(re.findall(r"[A-Za-z_][A-Za-z0-9_'!?]*",t)) for n,t in text.items()}
rev=collections.defaultdict(set)
for n,d in mods.items():
    for i in d['imports']: rev[i].add(n)
SEED={'OAI.MeasureTheory.CompactFactors.Centers','OAI.MeasureTheory.CompactFactors.RelativeCenters',
 'OAI.MeasureTheory.CompactFactors.Approximation','OAI.MeasureTheory.CompactFactors.ConditionalLimits',
 'OAI.MeasureTheory.CompactFactors.Factors','OAI.Analysis.PlaneSpectrum.ConditionalSpectrum',
 'OAI.Analysis.PlaneSpectrum.FourierTests','OAI.Analysis.PlaneSpectrum.Multipliers',
 'OAI.Analysis.PlaneSpectrum.SmallArcs','OAI.MeasureTheory.CompactFactors.ConditionalSelection',
 'OAI.Analysis.PlaneSpectrum.PhaseCollision','OAI.Analysis.PlaneSpectrum.PhaseEncoding'}
D=set(SEED)
changed=True
while changed:
    changed=False
    for m in mods:
        if m in D: continue
        if not rev[m] <= D: continue
        keep=[k for k in mods if k not in D]
        names=bymod.get(m,set())
        if any(words[k][n]>0 for k in keep for n in names if len(n)>2): continue
        D.add(m); changed=True
print("deletable modules:", len(D), " lines:", sum(mods[m]['lines'] for m in D))
for m in sorted(D, key=lambda x: mods[x]['path']):
    print(f"  {mods[m]['path']:56s} {mods[m]['lines']:5d}")
print()
print("INTERFACE: kept module -> deletable modules whose names it mentions")
for k in sorted(mods):
    if k in D: continue
    hit=[]
    for m in D:
        names=bymod.get(m,set())
        if any(words[k][n]>0 for n in names if len(n)>2): hit.append(mods[m]['path'].split('/')[-1])
    if hit: print(f"  {mods[k]['path']:56s} -> {sorted(hit)}")
