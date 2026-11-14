import os, re, hashlib, collections, sys
R='/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/lean/OAI'
N=int(sys.argv[1]) if len(sys.argv)>1 else 8
files={}
for root,d,fs in os.walk(R):
    for f in fs:
        if f.endswith('.lean'):
            p=os.path.join(root,f)
            files[os.path.relpath(p,R)]=open(p).read().splitlines()
def norm(l):
    l=l.split('--')[0].strip()
    return re.sub(r'\s+',' ',l)
blocks=collections.defaultdict(list)
for p,lines in files.items():
    n=len(lines)
    seen=set()
    for i in range(n-N+1):
        w=[norm(lines[i+k]) for k in range(N)]
        if sum(1 for x in w if x)==0: continue
        if any(len(x)<12 for x in w): continue      # skip trivial/short structural lines
        h=hashlib.md5('\n'.join(w).encode()).hexdigest()
        if h in seen: continue
        seen.add(h)
        blocks[h].append((p,i+1,i+N))
groups=[]
for h,occ in blocks.items():
    if len(occ)>1:
        groups.append((h,occ))
groups.sort(key=lambda g:(-len(g[1]), g[1][0][0]))
print('duplicate blocks of', N, 'significant lines:', len(groups))
# greedy maximal coverage: report clusters
for h,occ in groups[:40]:
    print(len(occ), [(p.split('/')[-1], a) for p,a,b in occ])
