import re, json, pathlib, collections
REPO = pathlib.Path("/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo")
ROOT = REPO/"lean"; OUT = pathlib.Path("min")
imports = json.load(open("imports.json"))
allmods = set(imports)
USED_JSON = "used.json"
TARGET_CONST = "OAI.EuclideanFiveColor.proper_iff_weak"
used = set()
DEF_KW = ("theorem","lemma","def","abbrev","structure","class","inductive","instance","example")
MOD_KW = ("noncomputable","private","protected","partial","unsafe","scoped","local")
CTRL_KW = ("namespace","end","section","open","variable","universe","set_option","attribute",
           "notation","macro","omit","include","#print","#check","infix","infixl","infixr","prefix","postfix")
KEYW = set(DEF_KW)|set(CTRL_KW)|set(MOD_KW)

def clean_starts(text):
    n=len(text); out=[]; i=0; depth=0; instr=False; ls=True
    while i<n:
        c=text[i]
        if ls:
            out.append(depth==0 and not instr); ls=False
        if depth>0:
            if text.startswith("/-",i): depth+=1; i+=2; continue
            if text.startswith("-/",i): depth-=1; i+=2; continue
            if c=="\n": ls=True
            i+=1; continue
        if instr:
            if c=="\\": i+=2; continue
            if c=='"': instr=False
            if c=="\n": ls=True
            i+=1; continue
        if text.startswith("/-",i): depth=1; i+=2; continue
        if c=='"': instr=True; i+=1; continue
        if c=="\n": ls=True
        i+=1
    return out

ATTR = re.compile(r"@\[[^\]]*\]")
def strip_attrs(l):
    while True:
        m = ATTR.match(l.lstrip())
        if not m: return l
        l = l.lstrip()[m.end():]

def scan(text):
    lines = text.splitlines(keepends=True)
    offs=[]; o=0
    for l in lines: offs.append(o); o+=len(l)
    clean = clean_starts(text)
    def is_clean(i): return i < len(clean) and clean[i] and lines[i][:1] not in (" ","\t","\n","")
    starts=[]; pending=None
    for i in range(len(lines)):
        if not is_clean(i): continue
        st = strip_attrs(lines[i])
        if st.strip()=="":
            if pending is None: pending=i
            continue
        w = st.split()[0] if st.split() else ""
        if w in ("omit","include") or lines[i].startswith("/--"):
            if pending is None: pending=i
            continue
        if w in KEYW:
            starts.append((i if pending is None else pending, i)); pending=None
    items=[]
    for k,(sc,kw) in enumerate(starts):
        e = starts[k+1][0] if k+1<len(starts) else len(lines)
        items.append((sc,e,strip_attrs(lines[kw]),kw))
    return lines, items

def classify(head):
    toks = head.split(); i=0; mods=[]
    while i<len(toks) and toks[i] in MOD_KW: mods.append(toks[i]); i+=1
    if i>=len(toks): return ("ctrl",None)
    kw = toks[i]
    if kw in DEF_KW:
        name = toks[i+1] if i+1<len(toks) else ""
        name = re.split(r"[:({\[]", name)[0]
        if not name: name = None
        if kw=="instance" and (not name or not re.match(r"^[\w'!?.\u0370-\u03ff\u2100-\u214f]+$", name)): name=None
        if kw=="example": name=None
        return ("decl",(kw,name,tuple(mods)))
    return ("ctrl",kw if kw in CTRL_KW else None)

def extract(path, outdir, used):
    text = path.read_text(errors="ignore")
    lines, items = scan(text)
    stack=[]; keep=[True]*len(lines); stats=collections.Counter()
    for (s,e,head) in items:
        kind,info = classify(head)
        toks = head.split()
        if kind=="decl":
            kw,name,mods = info
            fulls=[]
            if name:
                ns=".".join(x for k,x in stack if k=='ns' and x)
                fulls=[f"{ns}.{name}",name] if ns else [name]
            retained = ("private" in mods) or (name is None) or any(
                u==f or u.endswith("."+f) for u in used for f in fulls)
            if kw=="example": retained=False
            if retained:
                stats["kept"]+=1; stats["keptl"]+=e-s
            else:
                for l in range(s,e): keep[l]=False
                stats["drop"]+=1; stats["dropl"]+=e-s
        if kind=="ctrl" and toks:
            if toks[0]=="namespace" and len(toks)>1: stack.append(('ns',toks[1]))
            elif toks[0]=="section": stack.append(('sec',None))
            elif toks[0]=="end":
                if len(toks)>1:
                    tgt=toks[1]
                    while stack:
                        if stack.pop()[1]==tgt: break
                elif stack: stack.pop()
            if toks[0] in ("#print","#check"):
                for l in range(s,e): keep[l]=False
    out="".join(l for l,kp in zip(lines,keep) if kp)
    op = outdir/path.relative_to(ROOT); op.parent.mkdir(parents=True,exist_ok=True); op.write_text(out)
    return stats, len(text.splitlines()), len(out.splitlines())

def closure(roots):
    seen,st=set(),list(roots)
    while st:
        n=st.pop()
        if n in seen or n not in imports: continue
        seen.add(n); st.extend(imports[n])
    return seen

def ident_tokens(txt):
    return set(re.findall(r"[A-Za-z_\u0370-\u03ff][\w'!?]*", txt))

def run(T="OAI.Geometry.PlaneColoring.Transfer", target="OAI.EuclideanFiveColor.proper_iff_weak",
        outdir="min", usedjson="used.json"):
    global OUT, used
    OUT = pathlib.Path(outdir)
    used = set(json.load(open(usedjson))[target]) - allmods
    print("target", target, "used OAI constants:", len(used), "root", T, "->", outdir)
    C=sorted(closure([T]))
    parsed={}
    for m in C:
        path = ROOT/(m.replace(".","/")+".lean")
        text = path.read_text(errors="ignore")
        lines, items = scan(text)
        parsed[m]=(path,text,lines,items)
    # initial retention from proof-term reachability
    info=[]   # (module, idx, s,e,head,kind,name,retained)
    for m in C:
        path,text,lines,items = parsed[m]
        stack=[]
        for idx,(s,e,head,kw) in enumerate(items):
            kind,inf = classify(head)
            toks = head.split()
            name=None; mods=()
            if kind=="decl": _,name,mods = inf
            if kind=="ctrl" and toks:
                if toks[0]=="namespace" and len(toks)>1: stack.append(('ns',toks[1]))
                elif toks[0]=="section": stack.append(('sec',None))
                elif toks[0]=="end":
                    if len(toks)>1:
                        tgt=toks[1]
                        while stack:
                            if stack.pop()[1]==tgt: break
                    elif stack: stack.pop()
            full=None
            if name:
                ns=".".join(x for k,x in stack if k=='ns' and x)
                full = f"{ns}.{name}" if ns else name
            init = False
            if kind=="decl":
                if name is None or "private" in mods: init=True
                elif full and any(u==full or u.endswith("."+full) for u in used): init=True
                if inf[0]=="example": init=False
                if lines[s].lstrip().startswith("@[") or lines[kw].lstrip().startswith("@["): init=True   # attributed lemmas: simp/aesop sets are implicit
            info.append([m,idx,s,e,head,kind,full,init,kw])
    # fixpoint: add declarations whose name is mentioned in retained source
    byname = {}
    for r in info:
        if r[5]=="decl" and r[6]:
            byname.setdefault(r[6].split(".")[-1], []).append(r)
    changed=True; it=0
    while changed:
        changed=False; it+=1
        toks=set()
        for r in info:
            if r[5]=="ctrl" or r[7]:
                m,i= r[0],r[1]
                _,text,lines,items = parsed[m]
                toks |= ident_tokens("".join(lines[r[2]:r[3]]))
        for nm, rs in byname.items():
            if nm in toks:
                for r in rs:
                    if not r[7]: r[7]=True; changed=True
    print("fixpoint iterations:", it)
    # emit
    tot0=tot1=0; per={}
    for m in C:
        path,text,lines,items = parsed[m]
        keep=[True]*len(lines)
        kd=dr=0
        for r in info:
            if r[0]==m and r[5]=="decl" and not r[7]:
                for l in range(r[2],r[3]): keep[l]=False
                dr+=1
        out="".join(l for l,kp in zip(lines,keep) if kp)
        op = OUT/path.relative_to(ROOT); op.parent.mkdir(parents=True,exist_ok=True); op.write_text(out)
        a,b=len(text.splitlines()),len(out.splitlines()); per[m]=(a,b); tot0+=a; tot1+=b
        print(f"{m.split('.',1)[1]:58s} {a:5d} -> {b:5d}")
    print(f"TOTAL {tot0} -> {tot1} lines ({(tot1/tot0-1)*100:.1f}%)  retained decls {sum(1 for r in info if r[5]=='decl' and r[7])}/{sum(1 for r in info if r[5]=='decl')}")
    json.dump(per, open("extract_stats.json","w"), indent=1)

if __name__=="__main__":
    import sys
    if len(sys.argv) > 1:
        run(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        run()
