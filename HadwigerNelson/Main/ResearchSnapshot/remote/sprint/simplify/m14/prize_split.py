import re, pathlib, collections
ROOT=pathlib.Path("lean/OAI")
DECL=re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*(?:theorem|lemma|def|abbrev|structure|class|instance)\s+([A-Za-z0-9_'.]+)")
TOK=re.compile(r"[A-Za-z0-9_']+")
def strip(t):
    t=re.sub(r"/-.*?-/","",t,flags=re.S); return re.sub(r"--[^\n]*","",t)
files=sorted(ROOT.rglob("*.lean"))
texts={p:strip(p.read_text(errors="ignore")) for p in files}
per={p:collections.Counter(TOK.findall(t)) for p,t in texts.items()}
DELETE={"Approximation","ConditionalSpectrum","ConditionalSelection","PhaseCollision","SmallArcs","Multipliers","FourierTests","PhaseEncoding","ConditionalLimits","Stationary"}
out=collections.Counter()
for p in files:
    if p.stem not in DELETE: out.update(per[p])
for p in files:
    if p.stem not in DELETE: continue
    rows=[]
    for i,ln in enumerate(texts[p].splitlines(),1):
        m=DECL.match(ln)
        if not m: continue
        s=m.group(1).split('.')[-1]
        if out[s]>0: rows.append((out[s],s,i))
    if rows:
        print(f"### {p.stem}")
        for ext,s,i in sorted(rows, reverse=True)[:8]:
            print(f"   {ext:4d} x {s} (line {i})")
