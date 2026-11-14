import os, re, hashlib, collections, sys
R='/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/lean/OAI'
N=int(sys.argv[1]) if len(sys.argv)>1 else 12
files={}
for root,d,fs in os.walk(R):
    for f in fs:
        if f.endswith('.lean'):
            p=os.path.join(root,f)
            files[os.path.relpath(p,R)]=open(p).read().splitlines()
BOIL=re.compile(r'^\s*(open|namespace|variable|import|noncomputable|section|end|scoped|set_option|attribute|@\[|omit|include|universe)\b')
def norm(l):
    l=l.split('--')[0].strip()
    return re.sub(r'\s+',' ',l)
blocks=collections.defaultdict(list)
for p,lines in files.items():
    n=len(lines)
    for i in range(n-N+1):
        w=[norm(lines[i+k]) for k in range(N)]
        if any((not x) or len(x)<12 or BOIL.match(x) for x in w): continue
        h=hashlib.md5('\n'.join(w).encode()).hexdigest()
        blocks[h].append((p,i+1))
groups=[(h,o) for h,o in blocks.items() if len(o)>1]
groups.sort(key=lambda g:(-len(g[1]), g[1][0][0]))
print('repeated', N, '-line proof blocks (boilerplate filtered):', len(groups))
for h,o in groups[:30]:
    print(len(o), [(p.split('/')[-1], a) for p,a in o])
