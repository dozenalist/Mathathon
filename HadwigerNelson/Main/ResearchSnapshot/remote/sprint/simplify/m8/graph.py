import os, re, json, collections
R='/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/lean/OAI'
mods={}
for root,d,fs in os.walk(R):
    for f in fs:
        if f.endswith('.lean'):
            p=os.path.join(root,f)
            n='OAI.'+os.path.relpath(p,R).replace('/','.')[:-5]
            txt=open(p).read()
            imps=[re.match(r'^import\s+(OAI\.[\w.]+)\s*$',l).group(1) for l in txt.splitlines() if re.match(r'^import\s+(OAI\.[\w.]+)\s*$',l)]
            mods[n]=(os.path.relpath(p,R), len(txt.splitlines()), imps)
def closure(start, banned=()):
    seen=set(); st=[start]
    while st:
        m=st.pop()
        if m in seen or m in banned: continue
        seen.add(m); st.extend(mods[m][2])
    return seen
def rev():
    r=collections.defaultdict(list)
    for m,(p,l,ims) in mods.items():
        for i in ims: r[i].append(m)
    return r
if __name__=='__main__':
    FIVE='OAI.Geometry.PlaneColoring.Five'
    ERG='OAI.Analysis.PlaneSpectrum.Ergodicity'
    all_c=closure(FIVE)
    without=closure(FIVE, banned={ERG})
    rig=sorted(all_c-without)
    print("rigidity-only modules (every path from Five passes through Ergodicity):")
    tot=0
    for m in rig:
        p,l,_=mods[m]; tot+=l; print(f"  {p:60s} {l:5d}")
    print("TOTAL rigidity-only:", tot, "in", len(rig), "modules")
    print()
    print("closure(Five)=%d mods %d lines"%(len(all_c), sum(mods[m][1] for m in all_c)))
