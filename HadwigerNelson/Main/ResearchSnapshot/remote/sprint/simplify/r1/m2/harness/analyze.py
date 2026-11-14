#!/usr/bin/env python3
"""Offline accounting on the sound declaration graph (NODE/EDGET/EDGEV).

  python3 analyze.py stats
  python3 analyze.py free NAME [NAME ...]        # what a route that reproves NAME frees
  python3 analyze.py free --module OAI.X.Y        # ... reproves every value in module X.Y
  python3 analyze.py indeg [--module M] [--min-lines N]

`free` computes: reachable-with-all-edges  minus  reachable-with-EDGEV-of-the-given-
names-deleted (EDGET always kept, since the statement survives).  The difference,
attributed to modules through SPANS.json, is the number of declaration lines a route
that reproves exactly those declarations can delete.
"""
import re, sys, json, pathlib, argparse, collections

H = pathlib.Path(__file__).resolve().parent

def load(log=H / "DECLGRAPH.log"):
    nodes, et, ev = {}, collections.defaultdict(set), collections.defaultdict(set)
    for ln in pathlib.Path(log).read_text().splitlines():
        ln = ln.strip()
        if ln.startswith("NODE "):
            _, m, n = ln.split(" ", 2); nodes[n] = m
        elif ln.startswith("EDGET "):
            _, a, b = ln.split(" ", 2); et[a].add(b)
        elif ln.startswith("EDGEV "):
            _, a, b = ln.split(" ", 2); ev[a].add(b)
    return nodes, et, ev

ROOTS = ["OAI.EuclideanFiveColor.no_proper_five_coloring",
         "OAI.EuclideanFiveColor.no_proper_five_coloring_algebraic",
         "OAI.Problem160.properColoring_seven",
         "OAI.EuclideanFiveColor.proper_iff_weak",
         "OAI.Problem160.chromaticNumber_bounds",
         "OAI.EuclideanFiveColor.not_proper_five_coloring_compl_null",
         "OAI.EuclideanFiveColor.algebraic_colorable_iff"]

def closure(nodes, et, ev, drop_v=(), roots=None):
    drop_v = set(drop_v)
    seen, stack = set(), list(roots if roots is not None else ROOTS)
    while stack:
        n = stack.pop()
        if n in seen: continue
        seen.add(n)
        stack.extend(et.get(n, ()))
        if n not in drop_v:
            stack.extend(ev.get(n, ()))
    return seen

def spans():
    return json.loads((H / "SPANS.json").read_text())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd")
    ap.add_argument("names", nargs="*")
    ap.add_argument("--log", default=str(H / "DECLGRAPH.log"))
    ap.add_argument("--module", default=None)
    ap.add_argument("--min-lines", type=int, default=0)
    ap.add_argument("--md", action="store_true")
    ap.add_argument("--keep", nargs="*", default=[], help="names whose value-edges stay")
    ap.add_argument("--keep-module", nargs="*", default=[], help="modules whose value-edges stay")
    a = ap.parse_args()
    nodes, et, ev = load(a.log)
    sp = spans()
    if a.cmd == "stats":
        miss = [n for n in nodes if n not in sp]
        per = collections.Counter()
        for n in nodes:
            if n in sp: per[sp[n]["mod"]] += sp[n]["lines"]
        tot = sum(per.values())
        print(f"nodes {len(nodes)}  type-edges {sum(len(v) for v in et.values())}  "
              f"value-edges {sum(len(v) for v in ev.values())}")
        print(f"nodes with a source span: {len(nodes)-len(miss)}/{len(nodes)}")
        if miss: print("  unmatched (first 5):", miss[:5])
        print(f"declaration lines inside the closure: {tot}")
        for m, l in per.most_common():
            print(f"{l:6d} {m}")
        return
    drop = set(a.names)
    if a.module:
        drop |= {n for n, m in nodes.items() if m == a.module}
    if not drop:
        sys.exit("nothing to drop")
    # --keep / --keep-module: force these declarations (with their value-edges) to stay
    # reachable, modelling "the restructure still needs this machinery".
    keep = set(a.keep) | {n for n, m in nodes.items() if m in a.keep_module}
    drop = drop - keep
    full = closure(nodes, et, ev)
    red = closure(nodes, et, ev, drop_v=drop, roots=ROOTS + sorted(keep))
    freed = full - red
    per = collections.Counter(); cnt = collections.Counter()
    for n in freed:
        if n in sp:
            per[sp[n]["mod"]] += sp[n]["lines"]; cnt[sp[n]["mod"]] += 1
    print(f"dropped value-edges at {len(drop)} declaration(s)")
    print(f"freed {len(freed)} of {len(full)} declarations, {sum(per.values())} lines "
          f"({sum(cnt.values())} of them with a source span)")
    if a.md:
        print("| module | freed decls | freed lines |\n|---|---|---|")
        for m, l in per.most_common():
            print(f"| `{m}` | {cnt[m]} | {l} |")
        print(f"| **TOTAL** | {sum(cnt.values())} | **{sum(per.values())}** |")
    else:
        for m, l in per.most_common():
            print(f"{l:6d} {cnt[m]:4d}  {m}")
    # whole modules that disappear
    mods_left = {sp[n]["mod"] for n in red if n in sp}
    gone = sorted({sp[n]["mod"] for n in freed if n in sp} - mods_left)
    if gone: print("modules emptied:", gone)

main()
