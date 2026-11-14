#!/usr/bin/env python3
"""Import-graph analysis of lean/OAI: module sizes, closures, exclusive chains."""
import os, re, sys, json

ROOT = "/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/lean"

def mods():
    out = {}
    for dirpath, _, files in os.walk(os.path.join(ROOT, "OAI")):
        for f in files:
            if f.endswith(".lean"):
                p = os.path.join(dirpath, f)
                rel = os.path.relpath(p, ROOT)[:-5].replace("/", ".")
                imports = []
                with open(p, encoding="utf-8") as fh:
                    for line in fh:
                        m = re.match(r"^import\s+(OAI\S+)", line)
                        if m:
                            imports.append(m.group(1))
                        elif re.match(r"^(theorem|lemma|def|namespace|noncomputable|open|section|/--|#)", line) and not line.startswith("import"):
                            if imports or True:
                                pass
                n = sum(1 for _ in open(p, encoding="utf-8"))
                out[rel] = dict(path=p, lines=n, imports=imports)
    return out

M = mods()

def closure(starts, graph=None):
    seen = set()
    stack = list(starts)
    while stack:
        m = stack.pop()
        if m in seen:
            continue
        seen.add(m)
        for i in (graph or M)[m]["imports"]:
            if i in M:
                stack.append(i)
    return seen

def size(ms):
    return sum(M[m]["lines"] for m in ms)

if __name__ == "__main__":
    head = ["OAI.Geometry.PlaneColoring.Five"]
    cl = closure(head)
    print("total modules", len(M), "total lines", size(M))
    print("closure of Five:", len(cl), "lines", size(cl))
    outside = set(M) - cl
    print("outside closure:", len(outside), "lines", size(outside))
    for m in sorted(outside, key=lambda m: -M[m]["lines"]):
        print("   OUT %6d %s" % (M[m]["lines"], m))
    # reverse deps
    rev = {m: [] for m in M}
    for m, d in M.items():
        for i in d["imports"]:
            if i in rev:
                rev[i].append(m)
    print("\n--- modules by group ---")
    groups = {}
    for m in M:
        g = ".".join(m.split(".")[1:3])
        groups.setdefault(g, [0, 0])
        groups[g][0] += 1
        groups[g][1] += M[m]["lines"]
    for g, (c, n) in sorted(groups.items(), key=lambda t: -t[1][1]):
        print("%7d %3d %s" % (n, c, g))
