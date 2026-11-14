import os,re
root='/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/lean'
mods={}
for dp,dn,fn in os.walk(os.path.join(root,'OAI')):
    for f in fn:
        if f.endswith('.lean'):
            p=os.path.join(dp,f); m='OAI.'+os.path.relpath(p,os.path.join(root,'OAI'))[:-5].replace('/','.')
            mods[m]=dict(lines=len(open(p).read().splitlines()),src=open(p).read())
short=lambda m:m.replace('OAI.','')
banned=['OAI.MeasureTheory.CompactFactors.Approximation','OAI.MeasureTheory.CompactFactors.ConditionalLimits',
 'OAI.Analysis.PlaneSpectrum.ConditionalSpectrum','OAI.Analysis.PlaneSpectrum.PhaseCollision',
 'OAI.Analysis.PlaneSpectrum.PhaseEncoding','OAI.Analysis.PlaneSpectrum.FourierTests',
 'OAI.Analysis.PlaneSpectrum.SmallArcs','OAI.Analysis.PlaneSpectrum.Multipliers',
 'OAI.MeasureTheory.CompactFactors.ConditionalSelection']
cand=['OAI.Analysis.PlaneSpectrum.Basic','OAI.Analysis.PlaneSpectrum.Characters','OAI.Analysis.PlaneSpectrum.ConditionalSpectrum',
'OAI.Analysis.PlaneSpectrum.FourierTests','OAI.Analysis.PlaneSpectrum.InvariantMean','OAI.Analysis.PlaneSpectrum.Multipliers',
'OAI.Analysis.PlaneSpectrum.PhaseCollision','OAI.Analysis.PlaneSpectrum.PhaseEncoding','OAI.Analysis.PlaneSpectrum.SmallArcs',
'OAI.MeasureTheory.CompactFactors.Approximation','OAI.MeasureTheory.CompactFactors.Centers',
'OAI.MeasureTheory.CompactFactors.ConditionalLimits','OAI.MeasureTheory.CompactFactors.ConditionalSelection',
'OAI.MeasureTheory.CompactFactors.RelativeCenters']
survivors=[m for m in mods if m not in banned and m not in cand]
decl=re.compile(r'^(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+|partial\s+|scoped\s+)*(?:theorem|lemma|def|abbrev|structure|instance|class|inductive)\s+([A-Za-z_][\w.\'₀-₉]*)',re.M)
tot=0; dead=[]
for m in cand:
    names={n.split('.')[-1] for n in decl.findall(mods[m]['src'])}
    used=set()
    for s in survivors:
        ws=set(re.findall(r'[A-Za-z_][\w.\'₀-₉]*',mods[s]['src']))
        used |= (names & ws)
    dead.append((m,len(names),len(used),sorted(used)[:6]))
for m,n,u,ex in dead:
    print(f"{mods[m]['lines']:5d} {short(m):52s} decls={n:3d} used-in-survivors={u:3d} {ex}")
print()
print('total lines of candidate set:',sum(mods[m]['lines'] for m in cand))
print('candidates with ZERO use by survivors:',sum(mods[m]['lines'] for m in cand if [d for d in dead if d[0]==m][0][2]==0))
