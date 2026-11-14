import os,re,json,collections
ROOT='lean/OAI'
files={}
for dp,dn,fn in os.walk(ROOT):
    for f in fn:
        if f.endswith('.lean'):
            p=os.path.join(dp,f); files[p]=open(p,encoding='utf-8',errors='ignore').read()
decl_re=re.compile(r'^(?:@\[[^\]]*\]\s*)?(?:(?:private|protected|noncomputable|partial|unsafe|scoped)\s+)*(theorem|lemma|def|abbrev|structure|instance|class|inductive|opaque)\s+([A-Za-z_][\w\u2080-\u209c\'!?]*)',re.M)
attr_re=re.compile(r'@\[([^\]]*)\]\s*$')
tok=re.compile(r'[A-Za-z_][\w\u2080-\u209c\'!?]*')
per_file={}
allconn=collections.Counter()
for p,txt in files.items():
    c=collections.Counter(tok.findall(txt)); per_file[p]=c
    allconn.update(c)
rows=[]
for p,txt in files.items():
    lines=txt.split('\n')
    starts=[(m.start(),m.group(1),m.group(2),txt.count('\n',0,m.start())+1) for m in decl_re.finditer(txt)]
    # exclude names that are also type names used implicitly? keep all
    prev_attr=''
    for i,(pos,kind,name,ln) in enumerate(starts):
        end = starts[i+1][3]-1 if i+1<len(starts) else len(lines)
        span=max(1,end-ln)
        # collect attribute lines just before
        before='\n'.join(lines[max(0,ln-4):ln-1])
        rows.append(dict(file=p,kind=kind,name=name,line=ln,span=span,total=allconn[name],
                         attr=('simp' in before) or ('aesop' in before) or ('norm_num' in before) or ('instance' in before)))
dead=[r for r in rows if r['total']<=1 and r['kind'] not in ('instance','class','inductive','structure') and not r['attr']]
print('decls with total mentions<=1:',len(dead),'lines approx',sum(r['span'] for r in dead))
byfile=collections.Counter()
for r in dead: byfile[r['file']]+=r['span']
for f,s in byfile.most_common(30): print(f'{s:6d}  {f}')
json.dump(dead,open('.ultramath/smwfoekgk/m6/dead.json','w'),indent=0)
print()
print('--- mention==2 (one use) lines:')
d2=[r for r in rows if r['total']==2 and r['kind'] not in ('instance','class','inductive','structure') and not r['attr']]
print(len(d2), sum(r['span'] for r in d2))
