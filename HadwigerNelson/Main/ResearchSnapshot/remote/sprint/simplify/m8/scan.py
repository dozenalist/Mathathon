import os, re, sys, json, collections
ROOT = sys.argv[1] if len(sys.argv)>1 else '../../../../lean/OAI'
files={}
for root,d,fs in os.walk(ROOT):
    for f in fs:
        if f.endswith('.lean'):
            p=os.path.join(root,f)
            files[os.path.relpath(p,ROOT)]=open(p).read().splitlines()
# tokenised word counts over whole tree
wordcount=collections.Counter()
perfile=collections.defaultdict(collections.Counter)
for p,lines in files.items():
    for ln in lines:
        # strip comments roughly
        for w in re.findall(r"[A-Za-z_][A-Za-z0-9_'!?]*", ln):
            wordcount[w]+=1
            perfile[p][w]+=1
decl_re=re.compile(r"^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+|partial\s+|unsafe\s+|scoped\s+)*"
                   r"(theorem|lemma|def|abbrev|structure|class|instance|inductive|opaque)\s+([^\s:{(]+)")
ns_open=[]
res=[]
for p in sorted(files):
    stack=[]
    lines=files[p]
    for i,ln in enumerate(lines):
        s=ln.strip()
        if s.startswith('namespace '):
            stack.append(('ns', s.split()[1]))
        elif s.startswith('section'):
            stack.append(('sec', None))
        elif s == 'end' or s.startswith('end '):
            if stack: stack.pop()
        else:
            m=decl_re.match(ln)
            if m:
                kind, name = m.group(1), m.group(2)
                if name.startswith('⟨') or name.startswith('(') : continue
                nsc=[x[1] for x in stack if x[0]=='ns']
                fqn='.'.join(nsc+[name])
                short=name.split('.')[-1]
                res.append(dict(file=p, line=i+1, kind=kind, name=short, fqn=fqn))
print(json.dumps(res))
