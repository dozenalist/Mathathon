import re,os,collections,sys,json
BASE='/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/'
lines=[l.split() for l in open('imports.txt')]
file={};imps={}
for t in lines:
    file[t[0]]=t[1]; imps[t[0]]=t[2:]
text={m:open(BASE+file[m]).read() for m in file}
srclines={m:text[m].split('\n') for m in file}
decl_re=re.compile(r'^(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+|partial\s+|scoped\s+|local\s+|@\[[^\]]*\]\s*)*(theorem|lemma|def|abbrev|structure|inductive|instance|class|noncomputable def|noncomputable lemma)\s+([A-Za-z_][A-Za-z0-9_.\']*)')
# per-declaration (module, name, startline, endline)
decls=[]  # (module,name,kind,start,end)
name2decls=collections.defaultdict(list)
for m,t in text.items():
    raw=srclines[m]
    starts=[]
    for i,ln in enumerate(raw):
        mo=decl_re.match(ln)
        if mo:
            nm=mo.group(2).split('.')[-1]
            if len(nm)>=5 and not nm[0].isupper() or (nm[0].isupper() and len(nm)>=5):
                starts.append((i,mo.group(1),nm))
    for j,(i,kind,nm) in enumerate(starts):
        end=starts[j+1][0] if j+1<len(starts) else len(raw)
        decls.append((m,nm,kind,i,end))
        name2decls[nm].append(len(decls)-1)
allnames=set(name2decls)
tok=re.compile(r"[A-Za-z_][A-Za-z0-9_.']*")
mentions={m:set(tok.findall(t)) & allnames for m,t in text.items()}
modnames={}  # module -> set of names defined there
for m,nm,kind,s,e in decls: modnames.setdefault(m,set()).add(nm)

def closure(goals, banned=set(), bannedmods=set()):
    seen=set(); stack=list(goals)
    while stack:
        nm=stack.pop()
        if nm in seen: continue
        if nm in banned: continue
        seen.add(nm)
        for idx in name2decls.get(nm,()):
            m,nm2,kind,s,e = decls[idx]
            if m in bannedmods: continue
            for x in mentions[m]:
                if x not in seen: stack.append(x)
    return seen

GOALS=['no_proper_five_coloring','properColoring_seven','chromaticNumber_bounds',
       'no_proper_five_coloring_algebraic','not_proper_five_coloring_compl_null',
       'proper_iff_weak','algebraic_colorable_iff']
GOALS=[g for g in GOALS if g in allnames]
print("goals present:",GOALS)
full=closure(GOALS)
print("declarations reachable from goals:",len(full))
APPROX={'relative_singularity_approximation','universalGood_of_factor'}
cut=closure(GOALS,banned=APPROX)
lost=full-cut
print("lost when {relative_singularity_approximation, universalGood_of_factor} removed:",len(lost))
bym=collections.defaultdict(int)
byl=collections.defaultdict(int)
for nm in lost:
    for idx in name2decls[nm]:
        m,nm2,kind,s,e=decls[idx]
        bym[m]+=1; byl[m]+=e-s
tot=0
for m in sorted(byl,key=lambda x:-byl[x]):
    print(f"  {byl[m]:6d} lines {bym[m]:4d} decls  {m}")
    tot+=byl[m]
print("TOTAL orphaned lines:",tot)
# also: which "kind" (def/theorem)
