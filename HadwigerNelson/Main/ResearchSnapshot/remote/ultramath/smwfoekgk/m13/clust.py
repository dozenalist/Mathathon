import re, pathlib, collections
ROOT = pathlib.Path("lean/OAI")
CL = {
 "factor":  ["(hq : Measurable q)", "hqcov"],
 "kernel":  ["[IsMarkovKernel κ]", "hκcov"],
 "centered":["hκcov", "hLcov"],
 "orbit":   ["MeasurableConstSMul"],
 "sbr":     ["StandardBorelSpace X"],
}
tot = collections.Counter(); decls = collections.Counter()
for p in ROOT.rglob("*.lean"):
    txt = p.read_text(errors="ignore")
    lines = txt.splitlines()
    # split into blocks at top-level declarations
    starts = [i for i,l in enumerate(lines) if re.match(r"^(theorem|lemma|def|abbrev|instance|structure)\b", l) or re.match(r"^(private |protected |noncomputable )*(theorem|lemma|def)\b", l)]
    starts.append(len(lines))
    for a,b in zip(starts, starts[1:]):
        seg = "\n".join(lines[a:min(b, a+40)])
        head = seg.split(":= by")[0].split(":=\n")[0]
        n = sum(head.count(k) for k in CL["factor"]) 
        if "hqcov" in head and "Measurable q" in head:
            decls["factor"] += 1; tot["factor"] += head.count("\n")+1
        if "[IsMarkovKernel κ]" in head and "hκcov" in head:
            decls["kernel"] += 1; tot["kernel"] += head.count("\n")+1
        if "hLcov" in head and "hκcov" in head:
            decls["centered"] += 1; tot["centered"] += head.count("\n")+1
print("cluster   #decls  signature-lines")
for k in CL:
    print(f"{k:9s} {decls[k]:5d} {tot[k]:8d}")
