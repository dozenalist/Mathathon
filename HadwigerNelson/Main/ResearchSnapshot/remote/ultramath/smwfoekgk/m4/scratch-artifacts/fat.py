import os,re,collections,json
root='/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/lean'
files={}
for dp,dn,fn in os.walk(os.path.join(root,'OAI')):
    for f in fn:
        if f.endswith('.lean'):
            p=os.path.join(dp,f)
            m='OAI.'+os.path.relpath(p,os.path.join(root,'OAI'))[:-5].replace('/','.')
            files[m]=open(p).read()
# declaration names (last component) declared per file
decl=re.compile(r'^(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+|partial\s+|scoped\s+)*(theorem|lemma|def|abbrev|structure|instance|class|inductive)\s+([A-Za-z_][\w.\'₀-₉]*)',re.M)
where=collections.defaultdict(set)
per=collections.defaultdict(list)
for m,src in files.items():
    for kind,name in decl.findall(src):
        n=name.split('.')[-1]
        where[n].add(m); per[m].append((kind,name))
tot=sum(len(v) for v in per.values())
print('declarations:',tot,'distinct last-names:',len(where))
# usage: count occurrences of name as a whole word in OTHER files
word=collections.defaultdict(int)
for m,src in files.items():
    for w in set(re.findall(r'[A-Za-z_][\w.\'₀-₉]*',src)):
        word[w.split('.')[-1]]+=1
unused=[]
for m,lst in per.items():
    for kind,name in lst:
        n=name.split('.')[-1]
        if kind=='instance': continue
        if word[n]<=len(where[n]):  # appears only where declared
            unused.append((m,name,kind))
print('possibly-unused decls:',len(unused))
for m,n,k in sorted(unused)[:80]: print(' ',m.replace('OAI.',''),k,n)
