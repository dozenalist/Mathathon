import re,pathlib,json,collections,sys
ROOT=pathlib.Path("tree")
files=sorted(ROOT.glob("OAI/**/*.lean"))
DECL=re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+|partial\s+|unsafe\s+|scoped\s+|local\s+)*"
                r"(theorem|lemma|def|abbrev|structure|class|inductive|instance|example)\s+([A-Za-z_][\w'.]*)")
STOP=re.compile(r"^(end|namespace|section|variable|open|#|/-|-/|\}|@\[)")
texts={};blocks=[]
for p in files:
    rel=str(p.relative_to(ROOT)); mod=".".join(p.relative_to(ROOT).with_suffix("").parts)
    t=p.read_text(errors="ignore"); texts[rel]=t
    L=t.splitlines(); n=len(L); starts=[]
    for i,line in enumerate(L):
        m=DECL.match(line)
        if m: starts.append((i,m.group(1),m.group(2),line))
    for i,kind,full,line in starts:
        attributed="@[" in line; b=i-1
        while b>=0:
            s=L[b].strip()
            if s.startswith("@"): attributed=True; b-=1; continue
            if s=="": b-=1; continue
            if s.endswith("-/"):
                kk=b
                while kk>=0 and "/--" not in L[kk] and "/-" not in L[kk]: kk-=1
                if kk>=0 and "@[" in L[kk]: attributed=True
                b=kk-1; continue
            break
        start=b+1; e=n-1
        for mm in range(i+1,n):
            if DECL.match(L[mm]) or STOP.match(L[mm]): e=mm-1; break
        while e>i and L[e].strip()=="": e-=1
        blocks.append(dict(file=rel,mod=mod,start=start,end=e,kind=kind,full=full,
                           short=full.split(".")[-1],attr=attributed))
TOK=re.compile(r"[A-Za-z_][\w']*")
blk=[collections.Counter(TOK.findall("\n".join(texts[b["file"]].splitlines()[b["start"]:b["end"]+1]))) for b in blocks]
live=collections.defaultdict(set)
for i,ts in enumerate(blk):
    for s in ts: live[s].add(i)
hdr=collections.Counter()
for rel,t in texts.items():
    L=t.splitlines(); mask=[True]*len(L)
    for b in blocks:
        if b["file"]==rel:
            for i in range(b["start"],b["end"]+1): mask[i]=False
    hdr.update(TOK.findall("\n".join(L[i] for i in range(len(L)) if mask[i])))
json.dump(blocks,open("ana/blocks.json","w"))
names={"no_proper_five_coloring","no_proper_five_coloring_algebraic","properColoring_seven","chromaticNumber_bounds",
 "proper_iff_weak","algebraic_colorable_iff","not_proper_five_coloring_compl_null","six_le_planeChromaticNumber",
 "planeChromaticNumber_le_seven","not_properColoring_five","not_properColoring_of_le","planeProperColoring_iff",
 "properColoring_of_plane","plane_of_properColoring","properColoring_mono","toPlane","ofPlane","finite_config_proper",
 "exists_properColoring_of_finset","properColoring_of_weak","diam_le_one_of_preconnected_unitFree",
 "not_straddle_of_isPreconnected","proper_to_borel_weak_algebraic"}
mods={"OAI.Geometry.PlaneColoring.Chromatic","OAI.Geometry.PlaneColoring.Seven","OAI.Geometry.PlaneColoring.NullSetRobust",
 "OAI.Geometry.PlaneColoring.Transfer","OAI.Geometry.PlaneColoring.Converse","OAI.Geometry.PlaneColoring.ConnectedUnitFree",
 "OAI.Geometry.PlaneColoring.MeasurableProper","OAI.Geometry.PlaneColoring.MeasurableAssembly",
 "OAI.Geometry.PlaneColoring.Metric","OAI.Geometry.PlaneColoring.Lattice","OAI.Geometry.PlaneColoring.Assembly",
 "OAI.Geometry.PlaneColoring.Basic","OAI.Geometry.PlaneColoring.Covering"}
def run(kinds,attr_excl,protect_mods,protect_names):
    def prot(b): return b["mod"] in protect_mods or b["short"] in protect_names
    dead=set()
    for it in range(60):
        add=[i for i,b in enumerate(blocks) if i not in dead and not prot(b)
             and not (attr_excl and b["attr"]) and b["kind"] in kinds
             and not hdr.get(b["short"],0) and not (live.get(b["short"],set())-{i}-dead)]
        if not add: break
        dead|=set(add)
    return dead
L=lambda d: sum(blocks[i]["end"]-blocks[i]["start"]+1 for i in d)
for label,k,ae,pm,pn in [
 ("conservative (no instance, attr excluded, mods+names protected)",{"theorem","lemma","def","abbrev"},True,mods,names),
 ("+ instances",{"theorem","lemma","def","abbrev","instance"},True,mods,names),
 ("+ structures",{"theorem","lemma","def","abbrev","instance","structure","class","inductive"},True,mods,names),
 ("+ attributed, names-protection only",{"theorem","lemma","def","abbrev","instance","structure","class","inductive"},False,set(),names),
]:
    d=run(k,ae,pm,pn)
    print(f"{label}: {len(d)} decls {L(d)} lines")
    if label.startswith("+ instances"):
        json.dump(sorted(d),open("ana/dead_aggressive.json","w"))
        c=collections.Counter(blocks[i]["file"] for i in d)
        print("   files touched:",len(c))
        for i in sorted(d,key=lambda i:-(blocks[i]["end"]-blocks[i]["start"]+1))[:12]:
            b=blocks[i]; print(f"   {b['end']-b['start']+1:4d} {b['file']}:{b['start']+1} {b['kind']} {b['short']}")
