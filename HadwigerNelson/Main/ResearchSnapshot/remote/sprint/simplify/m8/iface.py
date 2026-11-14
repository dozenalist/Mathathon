import os, re, json, collections
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
cnt=collections.Counter(d['name'] for d in decl)
bymod=collections.defaultdict(set)
for d in decl:
    if len(d['name'])>=5 and cnt[d['name']]==1 and d['kind'] in ('theorem','lemma','def','abbrev','structure'):
        bymod['OAI.'+d['file'][:-5].replace('/','.')].add(d['name'])
words={n:collections.Counter(re.findall(r"[A-Za-z_][A-Za-z0-9_'!?]*",t)) for n,t in text.items()}
SEED=['OAI.MeasureTheory.CompactFactors.Centers','OAI.MeasureTheory.CompactFactors.RelativeCenters',
 'OAI.MeasureTheory.CompactFactors.Approximation','OAI.MeasureTheory.CompactFactors.ConditionalLimits',
 'OAI.MeasureTheory.CompactFactors.Factors','OAI.Analysis.PlaneSpectrum.ConditionalSpectrum',
 'OAI.Analysis.PlaneSpectrum.FourierTests','OAI.Analysis.PlaneSpectrum.Multipliers',
 'OAI.Analysis.PlaneSpectrum.SmallArcs','OAI.MeasureTheory.CompactFactors.ConditionalSelection',
 'OAI.Analysis.PlaneSpectrum.PhaseCollision','OAI.Analysis.PlaneSpectrum.PhaseEncoding']
for m in SEED:
    used_by=[]
    for n in sorted(bymod[m]):
        files=[k for k in mods if k!=m and words[k][n]>0]
        if files: used_by.append((n,[mods[k]['path'].split('/')[-1] for k in files]))
    print(f"== {mods[m]['path']}  ({mods[m]['lines']} lines, {len(bymod[m])} private-to-it declarations)")
    if not used_by: print("   no externally referenced declaration -> module is dead weight if its importers go")
    for n,fs in used_by: print(f"   {n:44s} <- {fs}")
