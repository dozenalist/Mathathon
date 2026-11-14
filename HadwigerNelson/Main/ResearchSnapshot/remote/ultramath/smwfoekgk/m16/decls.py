import graph as g, re, collections, sys

M = g.M
decl = re.compile(r"^\s*(?:@\[[^\]]*\]\s*)?(?:noncomputable\s+|private\s+|protected\s+|partial\s+)?(theorem|lemma|def|abbrev|instance|structure|class|inductive)\s+([A-Za-z_][A-Za-z0-9_.'!?]*)")

names = {}   # module -> set of decl names (last component)
for m, d in M.items():
    s = set()
    with open(d["path"], encoding="utf-8") as fh:
        for line in fh:
            mt = decl.match(line)
            if mt:
                nm = mt.group(2).split(".")[-1]
                if len(nm) > 3:
                    s.add(nm)
    names[m] = s

# tokens per module (identifiers used in the file body)
tok = re.compile(r"[A-Za-z_][A-Za-z0-9_'!?]*")
uses = {}
for m, d in M.items():
    with open(d["path"], encoding="utf-8") as fh:
        txt = fh.read()
    uses[m] = collections.Counter(tok.findall(txt))

def group(m):
    return m.split(".")[1] + "." + m.split(".")[2]

if __name__ == "__main__":
    # for each module, list names of decls from a *different* group that it uses
    for target in sorted(M):
        tg = group(target)
        others = collections.defaultdict(list)
        for nm in names[target]:
            consumers = [o for o in M if o != target and uses[o][nm] > 1]
            if consumers:
                others[nm] = consumers
        # only print decls that are used outside the target's own group
        ext = {nm: cs for nm, cs in others.items() if any(group(c) != tg for c in cs)}
        if ext:
            print("### %s (%d lines)" % (target.replace("OAI.", ""), M[target]["lines"]))
            for nm, cs in sorted(ext.items()):
                print("   %-45s <- %s" % (nm, ", ".join(sorted(c.split(".")[-1] for c in cs))))
