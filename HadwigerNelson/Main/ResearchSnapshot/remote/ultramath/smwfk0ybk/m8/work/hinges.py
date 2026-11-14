#!/usr/bin/env python3
"""For each OAI module, count the declarations of the extracted transfer tree whose source
mentions a constant of that module (syntactic over-approximation of the dependency)."""
import re, pathlib, json, collections, importlib.util
spec = importlib.util.spec_from_file_location("ex", pathlib.Path(__file__).with_name("extract.py"))
ex = importlib.util.module_from_spec(spec); spec.loader.exec_module(ex)
n2m = {}
for ln in pathlib.Path("names.log").read_text().splitlines():
    if ln.startswith("#@"):
        parts = ln[2:].split("\t")
        if len(parts) == 2: n2m[parts[1]] = parts[0]
MIN = pathlib.Path("min")
decls = []
for p in sorted(MIN.glob("OAI/**/*.lean")):
    mod = ".".join(p.relative_to(MIN).with_suffix("").parts)
    lines, items = ex.scan(p.read_text())
    for (s, e, head, kw) in items:
        kind, info = ex.classify(head)
        if kind == "decl" and info[1]:
            decls.append((mod, info[1], "".join(lines[s:e])))
refs = collections.defaultdict(set)
for mod, name, txt in decls:
    for tok in set(re.findall(r"[A-Za-z_][\w'.!?]*", txt)):
        if tok in n2m:
            if n2m[tok] != mod: refs[n2m[tok]].add((mod, name))
        else:
            last = tok.split('.')[-1]
            for k in (k for k in n2m if k.endswith("." + last)):
                if n2m[k] != mod: refs[n2m[k]].add((mod, name))
rows = sorted((len(s), m, sorted(s)) for m, s in refs.items())
for n, m, s in rows:
    print(f"{n}\t{m}\t" + "; ".join(f"{a.split('.',1)[1]}.{b}" for a, b in s[:5]))
