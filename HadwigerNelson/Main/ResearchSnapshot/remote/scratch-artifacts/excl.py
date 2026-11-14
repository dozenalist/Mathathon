import os,re,collections,sys
R='lean/OAI'
mods={}
for dp,dn,fn in os.walk(R):
    for f in fn:
        if f.endswith('.lean'):
            p=os.path.join(dp,f); name=os.path.relpath(p,R)[:-5].replace('/','.')
            imp=[t[4:] for line in open(p) if line.strip().startswith('import ') for t in line.split() if t.startswith('OAI.')]
            mods[name]=(p,set(imp),sum(1 for _ in open(p)))
deps={m:v[1] for m,v in mods.items()}
def reach(start,banned=frozenset()):
    seen=set(); st=list(start)
    while st:
        x=st.pop()
        if x in seen or x in banned: continue
        seen.add(x); st.extend(deps.get(x,()))
    return seen
TOP='Geometry.PlaneColoring.Five'
top=reach([TOP])
EXCL=top-reach([TOP],banned={'MeasureTheory.CompactFactors.Approximation'})
SURV=sorted(top-EXCL)
print("exclusive:",len(EXCL),sum(mods[m][2] for m in EXCL),"survivors:",len(SURV),sum(mods[m][2] for m in SURV))
# collect declared names in exclusive modules
decl=re.compile(r'^(?:@\[[^\]]*\]\s*)?(?:protected\s+|private\s+|noncomputable\s+|partial\s+|scoped\s+)*(theorem|lemma|def|abbrev|structure|instance|class|inductive|opaque)\s+([A-Za-z0-9_\u2080-\u209f\'₀-₉]+)')
names=collections.defaultdict(list)
for m in sorted(EXCL):
    for line in open(mods[m][0]):
        mm=decl.match(line)
        if mm: names[mm.group(2)].append(m)
surv_text={m:open(mods[m][0]).read() for m in SURV}
excl_text={m:open(mods[m][0]).read() for m in EXCL}
used=collections.defaultdict(list)
for nm,locs in names.items():
    if len(nm)<4: continue
    pat=re.compile(r'(?<![A-Za-z0-9_.])'+re.escape(nm)+r'(?![A-Za-z0-9_])')
    for m in SURV:
        if pat.search(surv_text[m]): used[nm].append(m)
print("\n== identifiers declared in the exclusive closure and referenced from a surviving module ==")
tot=0
for nm,ms in sorted(used.items(),key=lambda kv:-len(kv[1])):
    print(f"  {nm:40s} <- {', '.join(ms)}")
print("count:",len(used))
