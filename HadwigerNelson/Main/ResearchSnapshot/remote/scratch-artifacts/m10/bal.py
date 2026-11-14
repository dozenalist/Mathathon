import pathlib, re, sys
root = pathlib.Path(sys.argv[1])
bad = []
for p in sorted(root.rglob("*.lean")):
    t = p.read_text()
    op = len(re.findall(r"/-", t)); cl = len(re.findall(r"-/", t))
    ns = len(re.findall(r"^(?:namespace|section|mutual)\b", t, re.M)) + len(re.findall(r"^noncomputable section", t, re.M))
    en = len(re.findall(r"^end\b", t, re.M))
    if op != cl or ns != en:
        bad.append((str(p).split("OAI/")[-1], op, cl, ns, en))
for b in bad: print("  ", b)
print("files with imbalance:", len(bad), "of", len(list(root.rglob("*.lean"))))
