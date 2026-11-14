#!/usr/bin/env python3
"""Compute the maximal SOUND deletion set for lean/OAI.

  python3 prune.py --json OUT

Outputs:
  * `drop_decls`: declarations not reachable in the proof-term graph from the
    advertised surface (the 7 headline declarations) -> safe to delete;
  * `drop_modules`: modules with no remaining declaration -> whole file goes;
  * `drop_imports`: OAI imports that are not needed by the surviving declarations;
  * `kept`: declarations to keep.
Soundness: the graph is the Lean proof-term closure, so deleting any declaration
outside it cannot change any proof term of the surviving ones.
"""
import json, pathlib, collections, argparse, re

H = pathlib.Path(__file__).resolve().parent
IMP = re.compile(r"^import\s+(OAI\.[\w.]+)\s*$", re.M)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", default=str(H / "DECLGRAPH.log"))
    ap.add_argument("--json", default=str(H / "PRUNE.json"))
    ap.add_argument("--target", default=".")
    ap.add_argument("--force", default=None,
                    help="file of declaration names (one per line, short or full) that must be kept")
    a = ap.parse_args()
    sp = json.loads((H / "SPANS.json").read_text())
    nodes, et, ev = {}, collections.defaultdict(set), collections.defaultdict(set)
    for ln in pathlib.Path(a.log).read_text().splitlines():
        ln = ln.strip()
        if ln.startswith("NODE "): _, m, n = ln.split(" ", 2); nodes[n] = m
        elif ln.startswith("EDGET "): _, x, y = ln.split(" ", 2); et[x].add(y)
        elif ln.startswith("EDGEV "): _, x, y = ln.split(" ", 2); ev[x].add(y)
    keep = set(nodes)
    if a.force and pathlib.Path(a.force).exists():
        want = [l.strip() for l in pathlib.Path(a.force).read_text().splitlines() if l.strip()]
        sp_by_short = collections.defaultdict(list)
        for k in sp:
            sp_by_short[k.split(".")[-1]].append(k)
        added = []
        for w in want:
            cands = [k for k in sp if k == w] or sp_by_short.get(w.split(".")[-1], [])
            for c in cands:
                if c not in keep: added.append(c)
        # recompute the closure with the forced declarations as extra roots
        st = list(added)
        while st:
            n = st.pop()
            if n in keep: continue
            keep.add(n)
            for c in (et.get(n, set()) | ev.get(n, set())):
                if c in nodes and c not in keep: st.append(c)
        print(f"forced {len(added)} declaration(s) back in")
    nodes = {n: m for n, m in nodes.items() if n in keep}
    drop_decls = {k: v for k, v in sp.items() if k not in keep}
    # modules that keep at least one declaration
    mods_kept = {v["mod"] for k, v in sp.items() if k in keep}
    mods_all = sorted({v["mod"] for v in sp.values()})
    drop_modules = [m for m in mods_all if m not in mods_kept]
    # module -> declarations kept in it
    bymod = collections.defaultdict(list)
    for k, v in sp.items():
        if k in keep: bymod[v["mod"]].append(k)
    # used modules: which module declares each needed constant
    tgt = pathlib.Path(a.target)
    imports = {}
    for m in mods_all:
        p = tgt / "lean" / (m.replace(".", "/") + ".lean")
        imports[m] = [d for d in IMP.findall(p.read_text(errors="ignore"))] if p.exists() else []
    exports = {}
    def exp(m):
        if m in exports: return exports[m]
        s = {m}
        for d in imports.get(m, []):
            s |= exp(d)
        exports[m] = s; return s
    drop_imports = {}
    for m in mods_kept:
        ks = bymod[m]
        need = set()
        for k in ks:
            for c in (et.get(k, set()) | ev.get(k, set())):
                if c in nodes: need.add(nodes[c])
        need -= {m}
        cur = list(dict.fromkeys(imports.get(m, [])))
        for D in list(reversed(cur)):
            trial = [d for d in cur if d != D]
            cov = set()
            for d in trial: cov |= exp(d)
            if need <= cov:
                cur = trial; drop_imports.setdefault(m, []).append(D)
    out = dict(drop_decls=drop_decls, drop_modules=drop_modules, drop_imports=drop_imports,
               kept=sorted(keep), declared=sorted(sp))
    pathlib.Path(a.json).write_text(json.dumps(out, indent=0))
    n = sum(v["lines"] for v in drop_decls.values())
    print(f"declarations to delete : {len(drop_decls):4d}  span lines {n}")
    print(f"modules to delete whole: {len(drop_modules)}  {drop_modules}")
    nl = sum(len(v) for v in drop_imports.values())
    print(f"imports to delete      : {nl} across {len(drop_imports)} modules")
    tot = n + nl
    for m in drop_modules:
        p = tgt / "lean" / (m.replace(".", "/") + ".lean")
        if not p.exists(): p = tgt / (m.replace(".", "/") + ".lean")
        # lines of the module not already covered by deleted declaration spans
        full = len(p.read_text().splitlines())
        covered = sum(v["lines"] for k, v in drop_decls.items() if v["mod"] == m)
        tot += full - covered
        print(f"  whole-module {m}: +{full - covered} (file {full})")
    print(f"TOTAL raw-line saving  : {tot}")

main()
