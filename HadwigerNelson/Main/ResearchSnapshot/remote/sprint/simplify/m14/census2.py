#!/usr/bin/env python3
"""Fast declaration census: token counts over the corpus, minus the declaring site."""
import re, sys, pathlib, collections
ROOT=pathlib.Path("lean/OAI")
DECL = re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*(theorem|lemma|def|abbrev|structure|class|instance)\s+([A-Za-z0-9_'.]+)")
TOK = re.compile(r"[A-Za-z0-9_']+")
def strip(t):
    t = re.sub(r"/-.*?-/", "", t, flags=re.S)
    return re.sub(r"--[^\n]*", "", t)
files = sorted(ROOT.rglob("*.lean"))
texts = {p: strip(p.read_text(errors="ignore")) for p in files}
glob = collections.Counter()
for p,t in texts.items(): glob.update(TOK.findall(t))
per = {p: collections.Counter(TOK.findall(t)) for p,t in texts.items()}
pref = sys.argv[1] if len(sys.argv)>1 else ""
for p in files:
    rel = str(p.relative_to(ROOT))
    if not rel.startswith(pref): continue
    lines = texts[p].count("\n")
    outs=[]
    for i,ln in enumerate(texts[p].splitlines(),1):
        m=DECL.match(ln)
        if not m: continue
        short=m.group(2).split('.')[-1]
        own = per[p][short] - 1
        ext = glob[short] - per[p][short]
        if ext>0: outs.append((ext,short,own,i,m.group(1)))
    if outs:
        print(f"### {rel} ({lines} lines, {len(outs)} exported)")
        for ext,short,own,i,kind in outs:
            print(f"   {ext:4d} {rel}:{i:4d} {kind} {short}")
