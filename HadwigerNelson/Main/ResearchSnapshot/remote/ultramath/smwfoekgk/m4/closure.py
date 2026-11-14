import os,re,collections
root='/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/lean'
mods={}
for dp,dn,fn in os.walk(os.path.join(root,'OAI')):
    for f in fn:
        if f.endswith('.lean'):
            p=os.path.join(dp,f)
            m='OAI.'+os.path.relpath(p,os.path.join(root,'OAI'))[:-5].replace('/','.')
            src=open(p).read()
            mods[m]=dict(lines=len(src.splitlines()),imports=re.findall(r'^import\s+(\S+)',src,re.M))
short=lambda m:m.replace('OAI.','')
def clos(roots, ban=frozenset()):
    seen=set(); st=list(roots)
    while st:
        y=st.pop()
        if y in seen or y in ban or y not in mods: continue
        seen.add(y); st.extend(mods[y]['imports'])
    return seen
roots=[m for m in mods if m.startswith('OAI.Geometry.PlaneColoring.') or m.startswith('OAI.Analysis.PlaneSpectrum.')]
# full closure of the headline modules
full=clos(['OAI.Geometry.PlaneColoring.Five','OAI.Geometry.PlaneColoring.Chromatic','OAI.Geometry.PlaneColoring.NullSetRobust','OAI.Geometry.PlaneColoring.Seven','OAI.Geometry.PlaneColoring.Transfer'])
print('full closure of headline set:',len(full),sum(mods[m]['lines'] for m in full))
# try banning the relative-singularity chain
ban={'OAI.MeasureTheory.CompactFactors.Approximation','OAI.MeasureTheory.CompactFactors.ConditionalLimits',
     'OAI.Analysis.PlaneSpectrum.ConditionalSpectrum','OAI.Analysis.PlaneSpectrum.PhaseCollision',
     'OAI.Analysis.PlaneSpectrum.PhaseEncoding','OAI.Analysis.PlaneSpectrum.FourierTests',
     'OAI.Analysis.PlaneSpectrum.SmallArcs','OAI.Analysis.PlaneSpectrum.Multipliers',
     'OAI.MeasureTheory.CompactFactors.ConditionalSelection'}
banned=frozenset(ban)
after=clos(['OAI.Geometry.PlaneColoring.Five','OAI.Geometry.PlaneColoring.Chromatic','OAI.Geometry.PlaneColoring.NullSetRobust','OAI.Geometry.PlaneColoring.Seven','OAI.Geometry.PlaneColoring.Transfer'],banned)
lost=sorted(full-after)
print('\nbanning the relative-singularity chain loses modules:')
for m in lost: print(f"  {mods[m]['lines']:5d} {short(m)}")
print('total lost', sum(mods[m]['lines'] for m in lost))
# who uses InvariantMean / Characters / Centers etc. after the ban?
print('\nstill reachable but orphaned-by-ban modules (partial):')
for m in sorted(full & after):
    if any(i in banned for i in mods[m]['imports']):
        print('  importer',short(m),'lines',mods[m]['lines'])
