import sys, json, pathlib, re, collections
sys.path.insert(0, "harness")
import clos
nodes, et, ev = clos.load(); sp = clos.spans()
full = clos.closure(nodes, et, ev)
dead = [n for n in sp if n not in full]
tree = pathlib.Path("trees/A/lean")
texts = {}
for p in (tree/"OAI").rglob("*.lean"):
    mod = ".".join(p.relative_to(tree).with_suffix("").parts)
    texts[mod] = p.read_text(errors="ignore").splitlines()
safef = json.load(open("work/safe_fix.json"))
safe = set(safef)
# reconstruct "used" rejections: same fixpoint but record mention sites
import importlib
info = {n: (sp[n]["mod"], sp[n]["line"], sp[n]["line"]+sp[n]["lines"]-1, sp[n]["kind"], n.split(".")[-1]) for n in dead}
ATTR = re.compile(r"^\s*@\[(.*)\]\s*$")
def attrs_of(mod, s):
    lines = texts[mod]; s = min(s, len(lines)); out, j = set(), s-2
    while j >= 0:
        m = ATTR.match(lines[j])
        if m: out |= {a.strip() for a in re.split(r"[,\s]+", m.group(1)) if a.strip()}; j -= 1; continue
        t = lines[j].strip()
        if t=="" or t.startswith("--") or t.startswith("/-") or t.startswith("*") or t.startswith("-/"): j -= 1; continue
        break
    return out
BADKIND={"instance","class","structure","inductive","opaque"}
HARMFUL={"simp","instance","reducible","inline","inherit_doc","norm_num","positivity","aesop","ext","to_additive","elab_as_elim","congr","mono","bound","deprecated","local"}
# final candidate (safe) spans
alive = set(dead)
while True:
    span_of_mod = collections.defaultdict(list)
    for n in alive:
        m,s,e,k,sh = info[n]; span_of_mod[m].append((s,e))
    surv = set()
    for m, lines in texts.items():
        killed=set()
        for s,e in span_of_mod.get(m,[]): killed.update(range(s,e+1))
        for i,ln in enumerate(lines,1):
            if i in killed: continue
            surv.update(re.findall(r"[A-Za-z_][A-Za-z0-9_']*", ln))
    drop=[n for n in alive if info[n][3] in BADKIND or (attrs_of(info[n][0], info[n][1]) & HARMFUL) or info[n][4] in surv]
    if not drop: break
    for n in drop: alive.discard(n)
# now for each "used" candidate, classify its mention lines
def is_comment(lines, i, j):
    # crude: line starts with -- or inside a block comment
    ln = lines[i-1]
    st = ln.strip()
    if st.startswith("--"): return True
    # block comment: scan upward for /- vs -/
    depth = 0
    for k in range(i-1, -1, -1):
        t = lines[k]
        if "-/" in t: depth += 1
        if "/-" in t: depth -= 1
        if depth < 0: return True
    return False
res = []
for n in dead:
    if n in alive: continue
    m,s,e,k,sh = info[n]
    if s > len(texts[m]): continue
    killed = set()
    span_of_mod = collections.defaultdict(list)
    for nn in alive:
        mm,ss,ee,kk,ssh = info[nn]; span_of_mod[mm].append((ss,ee))
    for mm in texts:
        for ss,ee in span_of_mod.get(mm,[]): pass
    hits = []
    pat = re.compile(r"\b"+re.escape(sh)+r"\b")
    for mm, lines in texts.items():
        kills = set()
        for kk2, ln2 in enumerate(lines, 1):
            pass
        for i, ln in enumerate(lines, 1):
            if pat.search(ln):
                hits.append((mm, i, ln.strip()[:90], is_comment(lines, i, i)))
    noncomment = [h for h in hits if not h[3]]
    res.append((n, sp[n]["lines"], len(hits), len(noncomment), noncomment[:2]))
res.sort(key=lambda r: -r[1])
print("rejected 'used' decls:", len([r for r in res if r[3] > 0]), " lines:", sum(r[1] for r in res if r[3] > 0))
print("comment-only mentions:", len([r for r in res if r[2] > 0 and r[3] == 0]), " lines:", sum(r[1] for r in res if r[2] > 0 and r[3]==0))
print("\ntop non-comment users:")
for r in res:
    if r[3] > 0: print(f"  {r[1]:4d} lines, {r[3]} noncomment uses: {r[0].split('.')[-1]:35s} e.g. {r[4][0][0].split('.')[-1]}:{r[4][0][1]}  {r[4][0][2][:70]}")
