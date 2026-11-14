import re, pathlib, json, collections
ROOT = pathlib.Path(__file__).resolve().parent.parent / "tree"
files = sorted(ROOT.glob("OAI/**/*.lean"))
DECL = re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+|partial\s+|unsafe\s+|scoped\s+)*"
                  r"(theorem|lemma|def|abbrev|structure|class|inductive|instance|example)\s+([A-Za-z_][\w'.]*)")
TOK = re.compile(r"[A-Za-z_][\w']*")
info, texts, tokcount = {}, {}, {}
for p in files:
    rel = str(p.relative_to(ROOT)); t = p.read_text(errors="ignore"); texts[rel]=t
    decls=[]
    for i,L in enumerate(t.splitlines()):
        m = DECL.match(L)
        if m: decls.append((i+1, m.group(1), m.group(2), m.group(2).split(".")[-1]))
    info[rel]=decls
    tokcount[rel]=collections.Counter(TOK.findall(t))
extent={}
for rel,decls in info.items():
    n=len(texts[rel].splitlines())
    for k,(ln,kind,full,short) in enumerate(decls):
        end = decls[k+1][0]-1 if k+1<len(decls) else n
        extent[(rel,ln)]=max(0,end-ln+1)
allnames=collections.defaultdict(list)
for rel,decls in info.items():
    for ln,kind,full,short in decls: allnames[short].append((rel,ln,kind,full))
dead=[]
for short,defs in allnames.items():
    ownfiles={r for r,_,_,_ in defs}
    ext={r:c for r,c in ((r,tokcount[r].get(short,0)) for r in tokcount) if c and r not in ownfiles}
    if not ext:
        own=sum(tokcount[r].get(short,0) for r in ownfiles)
        if own<=len(defs):
            dead.append((short,sum(extent[(r,ln)] for r,ln,_,_ in defs),defs))
print(json.dumps({"total_decls":sum(len(v) for v in info.values()),"dead_candidates":len(dead),"dead_lines":sum(x[1] for x in dead)}))
for short,ls,defs in sorted(dead,key=lambda x:-x[1]):
    print(f"{ls:5d}  {short}  "+"; ".join(f"{r}:{ln}({k})" for r,ln,k,fu in defs))
