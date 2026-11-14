import re, pathlib, collections
ROOT=pathlib.Path("lean/OAI")
DECL=re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*(?:theorem|lemma|def|abbrev|structure|class|instance)\s+([A-Za-z0-9_'.]+)")
TOK=re.compile(r"[A-Za-z0-9_']+")
def strip(t):
    t=re.sub(r"/-.*?-/","",t,flags=re.S); return re.sub(r"--[^\n]*","",t)
files=sorted(ROOT.rglob("*.lean"))
texts={p:strip(p.read_text(errors="ignore")) for p in files}
per={p:collections.Counter(TOK.findall(t)) for p,t in texts.items()}
DEL={"Approximation","ConditionalSpectrum","ConditionalLimits","Stationary","PhaseCollision","SmallArcs","Multipliers","FourierTests","PhaseEncoding"}
outside=collections.Counter()
for p in files:
    if p.stem not in DEL: outside.update(per[p])
tot=0
for p in files:
    if p.stem not in DEL: continue
    hits=[]
    for i,ln in enumerate(texts[p].splitlines(),1):
        m=DECL.match(ln)
        if not m: continue
        s=m.group(1).split('.')[-1]
        if len(s)>=10 and outside[s]>0 and '_' not in s[:2]:
            hits.append((outside[s],s,i))
    if hits:
        print(f"### {p.stem} ({texts[p].count(chr(10))} lines)")
        for c,s,i in sorted(hits,reverse=True): print(f"   {c:4d} x {s} (line {i})")
        tot+=len(hits)
print("declarations with outside consumers:",tot)
