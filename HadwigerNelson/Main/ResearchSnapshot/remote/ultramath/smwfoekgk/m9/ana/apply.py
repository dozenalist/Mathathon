import json,pathlib,collections,sys
blocks=json.load(open("ana/blocks.json"))
dead=json.load(open("ana/dead_aggressive.json"))   # 104 decls, includes instances
dead=[i for i in dead if blocks[i]["kind"]!="instance"]
# redo fixpoint without instances, keep protection as in del2 conservative
import re
ROOT=pathlib.Path("work")
texts={};B=[]
for b in blocks: texts.setdefault(b["file"], pathlib.Path("tree",b["file"]).read_text().splitlines())
TOK=re.compile(r"[A-Za-z_][\w']*")
blk=[collections.Counter(TOK.findall("\n".join(texts[b["file"]][b["start"]:b["end"]+1]))) for b in blocks]
live=collections.defaultdict(set)
for i,ts in enumerate(blk):
    for s in ts: live[s].add(i)
hdr=collections.Counter()
for f,t in texts.items():
    L=t; mask=[True]*len(L)
    for i,b in enumerate(blocks):
        if b["file"]==f:
            for j in range(b["start"],b["end"]+1): mask[j]=False
    hdr.update(TOK.findall("\n".join(L[j] for j in range(len(L)) if mask[j])))
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
D=set()
for it in range(60):
    add=[i for i,b in enumerate(blocks) if i not in D and b["mod"] not in mods and b["short"] not in names
         and not b["attr"] and b["kind"] in ("theorem","lemma","def","abbrev")
         and not hdr.get(b["short"],0) and not (live.get(b["short"],set())-{i}-D)]
    if not add: break
    D|=set(add)
print("deleting",len(D),"decls",sum(blocks[i]["end"]-blocks[i]["start"]+1 for i in D),"lines",file=sys.stderr)
per=collections.defaultdict(list)
for i in D: per[blocks[i]["file"]].append(blocks[i])
removed=0
for f,bs in per.items():
    L=list(texts[f]); drop=set()
    for b in bs:
        s,e=b["start"],b["end"]
        # also swallow one following blank line
        while e+1<len(L) and L[e+1].strip()=="": e+=1
        for j in range(s,e+1): drop.add(j)
        removed+=e-s+1
    out=[L[j] for j in range(len(L)) if j not in drop]
    p=ROOT/f; p.write_text("\n".join(out)+"\n")
json.dump(sorted(D),open("ana/dead_final.json","w"))
print("files touched",len(per),"raw lines removed",removed,file=sys.stderr)
