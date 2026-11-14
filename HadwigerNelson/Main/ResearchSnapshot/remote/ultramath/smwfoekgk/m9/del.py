import re,pathlib,sys,json,collections
ROOT=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else "tree")
files=sorted(ROOT.glob("OAI/**/*.lean"))
DECL=re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+|partial\s+|unsafe\s+|scoped\s+|local\s+)*"
                r"(theorem|lemma|def|abbrev|structure|class|inductive|instance|example|theorem)\s+([A-Za-z_][\w'.]*)")
STOP=re.compile(r"^(end|namespace|section|variable|open|#|/-|-/|\}|@\[)")
PROTECT_MODS={"Chromatic","Seven","NullSetRobust","Transfer","Converse","ConnectedUnitFree",
              "MeasurableProper","MeasurableAssembly","Metric","Lattice","Basic","Assembly"}
PROTECT_NAMES={"no_proper_five_coloring","no_proper_five_coloring_algebraic","properColoring_seven",
  "chromaticNumber_bounds","proper_iff_weak","algebraic_colorable_iff","not_proper_five_coloring_compl_null",
  "six_le_planeChromaticNumber","planeChromaticNumber_le_seven","not_properColoring_five",
  "not_properColoring_of_le","planeProperColoring_iff","properColoring_of_plane","plane_of_properColoring",
  "properColoring_mono","toPlane","ofPlane","finite_config_proper","exists_properColoring_of_finset",
  "properColoring_of_weak","diam_le_one_of_preconnected_unitFree","not_straddle_of_isPreconnected",
  "proper_to_borel_weak_algebraic","ProperColoring","WeakColoring","planeChromaticNumber","Plane"}
texts={};blocks=[]   # (rel, startline0, endline0(inclusive), kind, full, short, attributed)
for p in files:
    rel=str(p.relative_to(ROOT)); t=p.read_text(errors="ignore"); texts[rel]=t
    L=t.splitlines(); n=len(L)
    starts=[]
    for i,line in enumerate(L):
        m=DECL.match(line)
        if m: starts.append((i,m.group(1),m.group(2),line))
    for k,(i,kind,full,line) in enumerate(starts):
        # backward over docstring/attribute/blank
        j=i; attributed = "@[" in line
        b=i-1
        while b>=0:
            s=L[b].strip()
            if s.startswith("@[") or s.endswith("]") and s.startswith("@"): attributed=True; b-=1; continue
            if s=="" : b-=1; continue
            if s.endswith("-/"):
                # docstring block
                kk=b
                while kk>=0 and "/--" not in L[kk] and "/-" not in L[kk]: kk-=1
                attributed |= ("@[" in L[kk] if kk>=0 else False)
                b=kk-1; continue
            break
        start=b+1
        # end
        e=n-1
        for mm in range(i+1,n):
            if DECL.match(L[mm]) or STOP.match(L[mm]): e=mm-1; break
        # trim trailing blanks
        while e>i and L[e].strip()=="": e-=1
        blocks.append(dict(file=rel,start=start,end=e,kind=kind,full=full,short=full.split(".")[-1],attr=attributed,
                           mod=p.stem))
def is_protected(b):
    return b["mod"] in PROTECT_MODS or b["short"] in PROTECT_NAMES or b["short"] in ("no_proper_five_coloring",)
# token index per block
TOK=re.compile(r"[A-Za-z_][\w']*")
occ=collections.defaultdict(list)      # short -> list of block idx (excluding own)
blk_tokens=[]
for idx,b in enumerate(blocks):
    L=texts[b["file"]].splitlines()[b["start"]:b["end"]+1]
    toks=collections.Counter(TOK.findall("\n".join(L)))
    blk_tokens.append(toks)
for idx,ts in enumerate(blk_tokens):
    for s in ts: occ[s].append(idx)
# also count file-level occurrences outside all blocks (headers, sections, #print etc.)
hdr=collections.Counter()
covered=collections.defaultdict(set)
for idx,b in enumerate(blocks): covered[b["file"]].add(idx)
for rel,t in texts.items():
    L=t.splitlines(); mask=[True]*len(L)
    for idx,b in enumerate(blocks):
        if b["file"]!=rel: continue
        for i in range(b["start"],b["end"]+1): mask[i]=False
    rest="\n".join(L[i] for i in range(len(L)) if mask[i])
    hdr.update(TOK.findall(rest))
# deletable = not protected, not attributed, not instance/structure/class/inductive, name never occurs outside own block
# and (own file's other blocks may use it -> then it's live)
live_occ=collections.defaultdict(set)
for idx,ts in enumerate(blk_tokens):
    for s in ts: live_occ[s].add(idx)
def candidates(deadset):
    out=[]
    for idx,b in enumerate(blocks):
        if idx in deadset: continue
        if is_protected(b) or b["attr"]: continue
        if b["kind"] in ("instance","structure","class","inductive","example"): continue
        s=b["short"]
        if hdr.get(s,0): continue
        users=live_occ.get(s,set())-{idx}-deadset
        if not users: out.append(idx)
    return out
dead=set()
for it in range(30):
    c=candidates(dead)
    if not c: break
    new=set(c)-dead
    dead|=set(c)
    print(f"pass {it}: +{len(new)} decls, total {len(dead)}", file=sys.stderr)
tot=sum(blocks[i]["end"]-blocks[i]["start"]+1 for i in dead)
print(json.dumps({"passes":it,"dead_decls":len(dead),"dead_lines":tot,
  "dead_by_file":collections.Counter(blocks[i]["file"] for i in dead).most_common(),
  "dead_by_kind":collections.Counter(blocks[i]["kind"] for i in dead).most_common()}))
json.dump(sorted(int(i) for i in dead), open("dead_idx.json","w"))
json.dump(blocks, open("blocks.json","w"))
for i in sorted(dead, key=lambda i:-(blocks[i]["end"]-blocks[i]["start"]+1))[:40]:
    b=blocks[i]; print(f"{b['end']-b['start']+1:5d} {b['file']}:{b['start']+1} {b['kind']} {b['full']}")
