import os,re,collections
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
top=reach([TOP]); EXCL=top-reach([TOP],banned={'MeasureTheory.CompactFactors.Approximation'})
SURV=sorted(top-EXCL)
decl=re.compile(r'^(?:@\[[^\]]*\]\s*)?(?:protected\s+|private\s+|noncomputable\s+|partial\s+|scoped\s+)*(theorem|lemma|def|abbrev|structure|instance|class|inductive)\s+([A-Za-z0-9_\u2080-\u209f\'₀-₉]+)')
def declared(path):
    out=set()
    for line in open(path):
        mm=decl.match(line)
        if mm: out.add(mm.group(2))
    return out
survnames=set()
for m in SURV: survnames|=declared(mods[m][0])
exclnames={m:declared(mods[m][0]) for m in sorted(EXCL)}
surv_text={m:open(mods[m][0]).read() for m in SURV}
print("module                                  lines  decls  extern-used-names(unique to it)")
loadbearing={}
for m in sorted(EXCL):
    used=[]
    for nm in sorted(exclnames[m]):
        if nm in survnames or len(nm)<5: continue
        pat=re.compile(r'(?<![A-Za-z0-9_.])'+re.escape(nm)+r'(?![A-Za-z0-9_])')
        hit=[s for s in SURV if pat.search(surv_text[s])]
        if hit: used.append((nm,hit))
    loadbearing[m]=used
    print(f"{m:40s} {mods[m][2]:5d} {len(exclnames[m]):5d}   {len(used)}")
    for nm,hit in used: print(f"      {nm:34s} <- {', '.join(hit)}")
print()
print("DEAD (no external use):", [(m,mods[m][2]) for m in EXCL if not loadbearing[m]])
print("dead lines:", sum(mods[m][2] for m in EXCL if not loadbearing[m]))
print("live lines:", sum(mods[m][2] for m in EXCL if loadbearing[m]))
