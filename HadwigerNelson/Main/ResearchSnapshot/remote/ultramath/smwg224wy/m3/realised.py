#!/usr/bin/env python3
"""Realised (raw-file) deletion accounting for a route, on a stage tree.

analyze.py sums *declaration spans*, which is the right currency for "what a route
frees".  The sprint's deliverable is measured in *raw file lines* (linecount.py /
BASELINE.json: 31277 at 83 modules).  When a module is emptied its whole file goes,
so the realised saving is larger by the module preamble (imports, namespace, open).
This script adds that back, and adds the closure-free modules that can be dropped
outright.  Sources of truth are m10's DECLGRAPH.log + a stage-tree SPANS.json.

  python3 realised.py free NAME... [--keep NAME...] [--spans F] [--root D]
"""
import collections
import json
import pathlib
import sys

REPO = pathlib.Path("/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo")
H = REPO / "sprint/simplify/m10/harness"
ROOTS = ["OAI.EuclideanFiveColor.no_proper_five_coloring",
         "OAI.EuclideanFiveColor.no_proper_five_coloring_algebraic",
         "OAI.Problem160.properColoring_seven",
         "OAI.EuclideanFiveColor.proper_iff_weak",
         "OAI.Problem160.chromaticNumber_bounds",
         "OAI.EuclideanFiveColor.not_proper_five_coloring_compl_null",
         "OAI.EuclideanFiveColor.algebraic_colorable_iff"]


def load():
    nodes, et, ev = {}, collections.defaultdict(set), collections.defaultdict(set)
    for ln in (H / "DECLGRAPH.log").read_text().splitlines():
        ln = ln.strip()
        if ln.startswith("NODE "):
            _, m, n = ln.split(" ", 2)
            nodes[n] = m
        elif ln.startswith("EDGET "):
            _, a, b = ln.split(" ", 2)
            et[a].add(b)
        elif ln.startswith("EDGEV "):
            _, a, b = ln.split(" ", 2)
            ev[a].add(b)
    return nodes, et, ev


NODES, ET, EV = load()


def closure(drop_v, keep=()):
    drop_v = set(drop_v)
    seen, stack = set(), list(ROOTS) + list(keep)
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n)
        stack.extend(ET.get(n, ()))
        if n not in drop_v:
            stack.extend(EV.get(n, ()))
    return seen


def main(argv):
    sp_path = REPO / ".ultramath/smwg224wy/m3/SPANS_stage.json"
    root = REPO / "sprint/simplify/stage"
    if "--spans" in argv:
        sp_path = pathlib.Path(argv[argv.index("--spans") + 1])
    if "--root" in argv:
        root = pathlib.Path(argv[argv.index("--root") + 1])
    argv = [a for i, a in enumerate(argv) if not (i and argv[i - 1] in ("--spans", "--root"))]
    argv = [a for a in argv if a not in ("--spans", "--root")]
    attr = "--attr" in argv
    argv = [x for x in argv if x != "--attr"]
    keep = []
    if "--keep" in argv:
        i = argv.index("--keep")
        keep = [x for x in argv[i + 1:] if x]
        argv = argv[:i]
    drop = set(argv)

    sp = json.loads(sp_path.read_text())
    raw = {}
    for p in sorted((root / "lean" / "OAI").rglob("*.lean")):
        mod = ".".join(p.relative_to(root / "lean").with_suffix("").parts)
        raw[mod] = len(p.read_text(errors="ignore").splitlines())
    decl = collections.Counter()
    for v in sp.values():
        decl[v["mod"]] += v["lines"]
    preamble = {m: raw[m] - decl[m] for m in raw}

    full = closure(())
    red = closure(drop, keep)
    freed = full - red
    if attr:
        allgl = set(json.loads((REPO / ".ultramath/smwg224wy/m3/GLOBALISH_ALL.json").read_text()))
        while True:
            extra = sorted(((full - closure(drop, keep)) & allgl) - set(keep))
            if not extra:
                break
            keep = keep + extra
        red = closure(drop, keep)
        freed = full - red
    per = collections.Counter()
    cnt = collections.Counter()
    for n in freed:
        s = sp.get(n)
        if s:
            per[s["mod"]] += s["lines"]
            cnt[s["mod"]] += 1
    live = {sp[n]["mod"] for n in red if n in sp}
    emptied = sorted({sp[n]["mod"] for n in freed if n in sp} - live)
    free_mods = sorted(m for m in raw if m not in {sp[n]["mod"] for n in full if n in sp})

    dec = sum(per.values())
    pre = sum(preamble.get(m, 0) for m in emptied)
    freemod = sum(raw[m] for m in free_mods)
    print(f"drop {len(drop)} decl(s), keep {len(keep)}")
    print(f"  declaration lines freed : {dec}")
    print(f"  + preamble of emptied modules ({len(emptied)}): {pre}  {emptied}")
    print(f"  + closure-free modules ({len(free_mods)}): {freemod}  {free_mods}")
    print(f"  = realised raw-line saving: {dec + pre + freemod}")
    if "--md" in sys.argv:
        print("| module | freed decls | freed decl lines | file lines |")
        print("|---|---|---|---|")
        for m, l in per.most_common():
            print(f"| `{m.split('.')[-1]}` | {cnt[m]} | {l} | {raw.get(m,'-')} |")
        print(f"| **TOTAL** | {sum(cnt.values())} | **{dec}** | |")


main(sys.argv[1:])
