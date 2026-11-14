import os,re,collections,json
root='/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/lean'
files={}
for dp,dn,fn in os.walk(os.path.join(root,'OAI')):
    for f in fn:
        if f.endswith('.lean'):
            p=os.path.join(dp,f)
            m='OAI.'+os.path.relpath(p,os.path.join(root,'OAI'))[:-5].replace('/','.')
            files[m]=open(p).read().splitlines()
# word counts across whole tree
wc=collections.Counter()
for m,ls in files.items():
    for w in re.findall(r"[A-Za-z_][\w.'₀-₉]*", "\n".join(ls)):
        wc[w.split('.')[-1]]+=1
decl=re.compile(r"^(?P<attr>@\[[^\]]*\]\s*)?(?P<mods>(?:private|protected|noncomputable|partial|scoped|unsafe)\s+)*(?P<kind>theorem|lemma|def|abbrev|structure|class|inductive|instance)\s+(?P<name>[A-Za-z_][\w.'₀-₉]*)")
res=[]
for m,ls in files.items():
    for i,line in enumerate(ls):
        mt=decl.match(line)
        if not mt: continue
        kind=mt.group('kind'); name=mt.group('name'); last=name.split('.')[-1]
        if kind=='instance': continue
        if mt.group('attr'): continue
        if wc[last]<=1:
            # find extent: until next declaration at same or lesser indent
            j=i+1
            while j<len(ls) and not decl.match(ls[j]):
                j+=1
            res.append((m,i+1,j,last,kind,j-i))
tot=sum(r[5] for r in res)
print('attribute-free declarations whose name occurs nowhere else in the tree:')
print('  count:',len(res),' lines:',tot)
bym=collections.Counter()
for r in res: bym[r[0]]+=r[5]
for m,l in bym.most_common(20): print(f"  {l:5d} {m.replace('OAI.','')}")
json.dump(res,open('dead.json','w'))
