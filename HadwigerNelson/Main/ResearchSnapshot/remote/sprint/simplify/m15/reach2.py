import re,os,collections,sys
BASE='/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/'
lines=[l.split() for l in open('imports.txt')]
file={};imps={}
for t in lines:
    file[t[0]]=t[1]; imps[t[0]]=t[2:]
text={m:open(BASE+file[m]).read() for m in file}
raw={m:text[m].split('\n') for m in file}
decl_re=re.compile(r'^(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+|partial\s+|scoped\s+|local\s+)*(theorem|lemma|def|abbrev|structure|inductive|instance|class)\s+([A-Za-z_][A-Za-z0-9_.\']*)')
decls=[]; name2decls=collections.defaultdict(list)
for m in text:
    starts=[]
    for i,ln in enumerate(raw[m]):
        mo=decl_re.match(ln)
        if mo:
            nm=mo.group(2).split('.')[-1]
            starts.append((i,nm))
    for j,(i,nm) in enumerate(starts):
        end=starts[j+1][0] if j+1<len(starts) else len(raw[m])
        decls.append((m,nm,i,end))
        name2decls[nm].append(len(decls)-1)
allnames=set(name2decls)
tok=re.compile(r"[A-Za-z_][A-Za-z0-9_.']*")
def expand(s):
    out=set()
    for t in s:
        out.add(t)
        for p in t.split('.'):
            out.add(p)
    return out
dmentions=[expand(tok.findall('\n'.join(raw[m][i:e]))) & allnames for m,nm,i,e in decls]
def closure(goals,banned=frozenset()):
    seen=set(); st=list(goals)
    while st:
        nm=st.pop()
        if nm in seen or nm in banned: continue
        seen.add(nm)
        for idx in name2decls.get(nm,()):
            for x in dmentions[idx]:
                if x not in seen: st.append(x)
    return seen
if __name__=='__main__':
    GOALS=[g for g in ['no_proper_five_coloring','properColoring_seven','chromaticNumber_bounds','no_proper_five_coloring_algebraic','not_proper_five_coloring_compl_null','proper_iff_weak','algebraic_colorable_iff'] if g in allnames]
    full=closure(GOALS)
    print("reachable decls:",len(full))
    for ban in ["relative_singularity_approximation","universalGood_of_factor","relative_singularity_successor","UniversalGood","exists_terminal_factor","relative_singularity_base"]:
        sub=closure(GOALS,banned={ban})
        print(f"ban {ban}: lost {len(full-sub)} decls")
    BAN={"relative_singularity_approximation","universalGood_of_factor","relative_singularity_successor","UniversalGood","exists_terminal_factor","relative_singularity_base"}
    lost=full-closure(GOALS,banned=BAN)
    byl=collections.defaultdict(int);bym=collections.defaultdict(int)
    for nm in lost:
        for idx in name2decls[nm]:
            m,nm2,i,e=decls[idx]; byl[m]+=e-i; bym[m]+=1
    print("\nAll six banned -> lost lines",sum(byl.values()),"decls",len(lost))
    for m in sorted(byl,key=lambda x:-byl[x]): print(f"   {byl[m]:6d} {bym[m]:4d} {m}")

def closure2(goals,banned=frozenset(),leaf=frozenset()):
    seen=set(); st=list(goals)
    while st:
        nm=st.pop()
        if nm in seen or nm in banned: continue
        seen.add(nm)
        for idx in name2decls.get(nm,()):
            if nm in leaf: continue
            for x in dmentions[idx]:
                if x not in seen: st.append(x)
    return seen
