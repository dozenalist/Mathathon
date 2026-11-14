import sys, json, pathlib, re, collections
sys.path.insert(0, "harness")
import clos
nodes, et, ev = clos.load(); sp = clos.spans()
full = clos.closure(nodes, et, ev)
dead = [n for n in sp if n not in full]
tree = pathlib.Path("trees/A/lean")
texts, modlines = {}, {}
for p in (tree/"OAI").rglob("*.lean"):
    mod = ".".join(p.relative_to(tree).with_suffix("").parts)
    texts[mod] = p.read_text(errors="ignore").splitlines()
# candidate info
info = {}
for n in dead:
    v = sp[n]; info[n] = (v["mod"], v["line"], v["line"] + v["lines"] - 1, v["kind"], n.split(".")[-1])
ATTR = re.compile(r"^\s*@\[(.*)\]\s*$")
HARMFUL = {"simp","instance","reducible","inline","inherit_doc","norm_num","positivity","aesop","ext","to_additive","elab_as_elim","congr","mono","bound","deprecated","local"}
BADKIND = {"instance","class","structure","inductive","opaque"}
def attrs_of(mod, s):
    lines = texts[mod]
    if s - 2 >= len(lines): s = len(lines)
    out, j = set(), s - 2
    while j >= 0:
        m = ATTR.match(lines[j])
        if m:
            out |= {a.strip() for a in re.split(r"[,\s]+", m.group(1)) if a.strip()}; j -= 1; continue
        t = lines[j].strip()
        if t == "" or t.startswith("--") or t.startswith("/-") or t.startswith("*") or t.startswith("-/"): j -= 1; continue
        break
    return out
alive = set(dead)
reason = {}
while True:
    # survivor text: all lines not inside a live candidate span
    span_of_mod = collections.defaultdict(list)
    for n in alive:
        m, s, e, k, sh = info[n]; span_of_mod[m].append((s, e))
    surv_words = set()
    for m, lines in texts.items():
        masks = sorted(span_of_mod.get(m, []))
        killed = set()
        for s, e in masks: killed.update(range(s, e + 1))
        for i, ln in enumerate(lines, 1):
            if i in killed: continue
            surv_words.update(re.findall(r"[A-Za-z_][A-Za-z0-9_']*", ln))
    drop = []
    for n in alive:
        m, s, e, k, sh = info[n]
        if s > len(texts[m]): drop.append((n, "span oob")); continue
        if k in BADKIND: drop.append((n, "kind:" + k)); continue
        a = attrs_of(m, s)
        if a & HARMFUL: drop.append((n, "attr:" + sorted(a & HARMFUL)[0])); continue
        if sh in surv_words: drop.append((n, "used")); continue
    if not drop: break
    for n, r in drop:
        alive.discard(n); reason[r] = reason.get(r, 0) + 1
def L(S): return sum(sp[n]["lines"] for n in S)
print(f"dead {len(dead)} ({L(dead)} lines) -> SAFE {len(alive)} ({L(alive)} lines)")
print("rejected:", dict(sorted(reason.items(), key=lambda kv: -kv[1])))
json.dump({n: {"mod": sp[n]["mod"], "lines": sp[n]["lines"]} for n in sorted(alive)}, open("work/safe_fix.json","w"), indent=0)
per = collections.Counter()
for n in alive: per[sp[n]["mod"]] += sp[n]["lines"]
for m, l in per.most_common(8): print(f"   {l:4d} {m}")
