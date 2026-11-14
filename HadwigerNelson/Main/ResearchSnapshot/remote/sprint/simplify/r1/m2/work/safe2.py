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
DOTTED = re.compile(r"[A-Za-z_][A-Za-z0-9_'.]*(?:\.[A-Za-z_][A-Za-z0-9_']*)*")
ATTR = re.compile(r"^\s*@\[(.*)\]\s*$")
HARMFUL = {"simp","instance","reducible","inline","inherit_doc","norm_num","positivity","aesop","ext","to_additive","elab_as_elim","congr","mono","bound","deprecated","local"}
BADKIND = {"instance","class","structure","inductive","opaque"}
info = {n: (sp[n]["mod"], sp[n]["line"], sp[n]["line"]+sp[n]["lines"]-1, sp[n]["kind"], n.split(".")[-1], n) for n in dead}
def attrs_of(mod, s):
    lines = texts[mod]; s = min(s, len(lines)); out, j = set(), s-2
    while j >= 0:
        m = ATTR.match(lines[j])
        if m: out |= {a.strip() for a in re.split(r"[,\s]+", m.group(1)) if a.strip()}; j -= 1; continue
        t = lines[j].strip()
        if t=="" or t.startswith("--") or t.startswith("/-") or t.startswith("*") or t.startswith("-/"): j -= 1; continue
        break
    return out
def mentions(tok, n):
    """is the dotted token a plausible reference to declaration n (full name n)?"""
    if tok == n.split(".")[-1]: return True          # unqualified
    parts = n.split(".")
    for k in range(1, len(parts)):
        if tok.endswith("." + ".".join(parts[k:])): return True   # qualified suffix
    return False
alive = set(dead)
while True:
    span_of_mod = collections.defaultdict(list)
    for n in alive:
        m,s,e,k,sh,fn = info[n]; span_of_mod[m].append((s,e))
    surv = collections.defaultdict(set)
    for m, lines in texts.items():
        killed = set()
        for s,e in span_of_mod.get(m, []): killed.update(range(s, e+1))
        for i, ln in enumerate(lines, 1):
            if i in killed: continue
            for tok in DOTTED.findall(ln): surv[m].add(tok)
    alltok = set()
    for m in surv: alltok |= surv[m]
    drop = []
    for n in alive:
        m,s,e,k,sh,fn = info[n]
        if k in BADKIND: drop.append((n,"kind:"+k)); continue
        a = attrs_of(m,s)
        if a & HARMFUL: drop.append((n,"attr:"+sorted(a&HARMFUL)[0])); continue
        if any(mentions(t,n) for t in alltok): drop.append((n,"used")); continue
    if not drop: break
    for n,r in drop: alive.discard(n)
def L(S): return sum(sp[n]["lines"] for n in S)
print(f"SAFE(qualified) {len(alive)} decls {L(alive)} lines  (of {len(dead)}/{L(dead)})")
json.dump({n: {"mod": sp[n]["mod"], "lines": sp[n]["lines"]} for n in sorted(alive)}, open("work/safe2.json","w"), indent=0)
per = collections.Counter()
for n in alive: per[sp[n]["mod"]] += sp[n]["lines"]
for m,l in per.most_common(10): print(f"  {l:5d} {m}")
