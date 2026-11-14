import re,os,collections,sys
BASE='/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/'
lines=[l.split() for l in open('imports.txt')]
file={};imps={}
for t in lines:
    file[t[0]]=t[1]; imps[t[0]]=t[2:]
raw={m:open(BASE+file[m]).read().split('\n') for m in file}
def strip_comments(src):
    out=[];i=0;n=len(src);depth=0
    while i<n:
        if depth==0 and src.startswith('/-',i):
            depth=1;i+=2;continue
        if depth>0:
            if src.startswith('/-',i): depth+=1;i+=2;continue
            if src.startswith('-/',i): depth-=1;i+=2;continue
            if src[i]=='\n': out.append('\n')
            i+=1;continue
        if src.startswith('--',i):
            while i<n and src[i]!='\n': i+=1
            continue
        out.append(src[i]);i+=1
    return ''.join(out)
code={m:strip_comments('\n'.join(raw[m])) for m in file}
decl_re=re.compile(r'^(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+|partial\s+|scoped\s+|local\s+)*(theorem|lemma|def|abbrev|structure|inductive|instance|class)\s+([A-Za-z_][A-Za-z0-9_.\']*)')
decls=[];name2decls=collections.defaultdict(list)
for m in raw:
    starts=[]
    for i,ln in enumerate(raw[m]):
        mo=decl_re.match(ln)
        if mo: starts.append((i,mo.group(2).split('.')[-1]))
    for j,(i,nm) in enumerate(starts):
        end=starts[j+1][0] if j+1<len(starts) else len(raw[m])
        decls.append((m,nm,i,end)); name2decls[nm].append(len(decls)-1)
allnames=set(name2decls)
tok=re.compile(r"[A-Za-z_][A-Za-z0-9_.']*")
def expand(s):
    out=set()
    for t in s:
        out.add(t)
        for p in t.split('.'): out.add(p)
    return out
codem={m:code[m].split('\n') for m in file}
dmentions=[expand(tok.findall('\n'.join(codem[m][i:e]))) & allnames for m,nm,i,e in decls]
def cl(goals,leaf=frozenset()):
    seen=set(); st=list(goals)
    while st:
        nm=st.pop()
        if nm in seen: continue
        seen.add(nm)
        if nm in leaf: continue
        for idx in name2decls.get(nm,()):
            for x in dmentions[idx]:
                if x not in seen: st.append(x)
    return seen
GOALS=[g for g in ['no_proper_five_coloring','properColoring_seven','chromaticNumber_bounds','no_proper_five_coloring_algebraic','not_proper_five_coloring_compl_null','proper_iff_weak','algebraic_colorable_iff'] if g in allnames]
cur=cl(GOALS)
dead=[nm for nm in allnames if nm not in cur]
insts=set();attributed=set()
for i,(m,nm,a,b) in enumerate(decls):
    if raw[m][a].startswith('instance') or 'instance' in raw[m][a].split(':')[0]: insts.add(nm)
    if a>0 and '@[' in raw[m][a-1]: attributed.add(nm)
risky=[nm for nm in dead if nm in insts or nm in attributed]
plain=[nm for nm in dead if nm not in risky]
def lines(nms): return sum(e-i for nm in nms for (m,_n,i,e) in [decls[idx] for idx in name2decls[nm]])
print("decls",len(allnames),"reachable",len(cur))
print("DEAD (comment-stripped mentions):",len(dead),"decls,",lines(dead),"lines")
print("  risky (instance or @[...]-attributed):",len(risky),lines(risky),"lines")
print("  plain:",len(plain),lines(plain),"lines")
bym=collections.defaultdict(int);byn=collections.defaultdict(int)
for nm in plain:
    for idx in name2decls[nm]:
        m,_,i,e=decls[idx]; bym[m]+=e-i; byn[m]+=1
for m in sorted(bym,key=lambda x:-bym[x])[:14]: print(f"   {bym[m]:5d} {byn[m]:3d}  {m}")
