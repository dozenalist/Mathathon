import re,os,collections,json
ROOT='/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/'
lines=[l.split() for l in open('imports.txt')]
file={};imps={}
for t in lines:
    file[t[0]]=t[1]; imps[t[0]]=t[2:]
text={m:open(ROOT+file[m]).read() for m in file}
decl_re=re.compile(r'^(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+|partial\s+|scoped\s+|local\s+)*(theorem|lemma|def|abbrev|structure|inductive|instance|class)\s+([A-Za-z_][A-Za-z0-9_.\']*)',re.M)
defs=collections.defaultdict(list)   # name -> [modules]
for m,t in text.items():
    for kind,name in decl_re.findall(t):
        nm=name.split('.')[-1]
        if len(nm)<4: continue
        defs[nm].append(m)
# name -> defining modules
name2mods=collections.defaultdict(set)
for m,t in text.items():
    for kind,name in decl_re.findall(t):
        name2mods[name.split('.')[-1]].add(m)
# reference index: for each name, which modules mention it
refs=collections.defaultdict(set)
for m,t in text.items():
    for nm in name2mods:
        if nm in t: refs[nm].add(m)
CUT={'OAI.MeasureTheory.CompactFactors.Approximation','OAI.MeasureTheory.CompactFactors.ConditionalLimits'}
out=[]
for nm,ms in sorted(name2mods.items()):
    users=refs[nm]
    ext=users-set(ms)
    if ext and ext<=CUT:
        for m in ms:
            out.append((m,nm,sorted(ext)))
print("declarations referenced ONLY from {Approximation,ConditionalLimits}:")
by=collections.defaultdict(list)
for m,nm,ext in out: by[m].append(nm)
for m in sorted(by):
    print(f"  {m}: {len(by[m])} decls")
    print("    ", ", ".join(by[m]))
