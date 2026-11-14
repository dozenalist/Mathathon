import os, re, collections
R='/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/lean/OAI'
mods={}
for root,_,fs in os.walk(R):
    for f in fs:
        if f.endswith('.lean'):
            p=os.path.join(root,f); n='OAI.'+os.path.relpath(p,R).replace('/','.')[:-5]
            t=open(p).read()
            mods[n]=dict(path=os.path.relpath(p,R), lines=len(t.splitlines()),
                imports=[m.group(1) for m in (re.match(r'^import\s+(OAI\.[\w.]+)\s*$',l) for l in t.splitlines()) if m])
def closure(start, banned=(), extra_edges=()):
    adj={k:set(v['imports']) for k,v in mods.items()}
    for a,b in extra_edges: adj[a].add(b)
    seen,st=set(),[start]
    while st:
        m=st.pop()
        if m in seen or m in banned: continue
        seen.add(m); st.extend(adj.get(m,()))
    return seen
TOWER={'OAI.MeasureTheory.CompactFactors.Centers','OAI.MeasureTheory.CompactFactors.RelativeCenters',
 'OAI.MeasureTheory.CompactFactors.Approximation','OAI.MeasureTheory.CompactFactors.ConditionalLimits',
 'OAI.MeasureTheory.CompactFactors.Factors','OAI.Analysis.PlaneSpectrum.ConditionalSpectrum',
 'OAI.Analysis.PlaneSpectrum.FourierTests','OAI.Analysis.PlaneSpectrum.Multipliers',
 'OAI.Analysis.PlaneSpectrum.SmallArcs','OAI.MeasureTheory.CompactFactors.ConditionalSelection',
 'OAI.Analysis.PlaneSpectrum.PhaseCollision','OAI.Analysis.PlaneSpectrum.PhaseEncoding'}
FIVE='OAI.Geometry.PlaneColoring.Five'
SEVEN='OAI.Geometry.PlaneColoring.Seven'
base=closure(FIVE)
print('closure(Five):',len(base),sum(mods[m]['lines'] for m in base))
after=closure(FIVE,banned=TOWER,extra_edges=[('OAI.MeasureTheory.CompactFactors.Stationary','OAI.Analysis.PlaneSpectrum.InvariantMean')])
lost=sorted(base-after)
print('unreachable after banning tower:',len(lost),sum(mods[m]['lines'] for m in lost))
for m in lost: print(f"   {mods[m]['path']:56s} {mods[m]['lines']:5d}")
print('after:',len(after),sum(mods[m]['lines'] for m in after))
# second cascade: modules whose importers all vanished
print()
print('still-reachable check: Seven closure ok?', len(closure(SEVEN,banned=TOWER)) )
