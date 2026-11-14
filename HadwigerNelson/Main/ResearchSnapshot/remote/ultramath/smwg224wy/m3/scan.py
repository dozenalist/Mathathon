#!/usr/bin/env python3
"""Route scan on m10's sound declaration graph (read-only use of DECLGRAPH.log).

  python3 scan.py single            # for every node: freed lines if its value-edges go
  python3 scan.py greedy [--min N]  # greedily union single routes, report the ladder
  python3 scan.py free NAME... [--keep NAME...] [--md]

Uses exactly m10's semantics: drop value-edges at the named decls, keep all type-edges,
recompute the closure from the 7 headline roots + keeps, sum spans of what fell out.
"""
import collections
import json
import pathlib
import sys

H = pathlib.Path("/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/sprint/simplify/m10/harness")

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
SP = json.loads((H / "SPANS.json").read_text())


def lines(n):
    s = SP.get(n)
    return s["lines"] if s else 0


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


FULL = closure(())


def freed(drop_v, keep=()):
    red = closure(drop_v, keep)
    f = FULL - red
    return f, sum(lines(n) for n in f)


def per_module(fs):
    per, cnt = collections.Counter(), collections.Counter()
    for n in fs:
        s = SP.get(n)
        if s:
            per[s["mod"]] += s["lines"]
            cnt[s["mod"]] += 1
    return per, cnt


def cmd_free(args):
    keep = []
    if "--keep" in args:
        i = args.index("--keep")
        keep = args[i + 1:]
        args = args[:i]
    d = set(args)
    f, tot = freed(d, keep)
    per, cnt = per_module(f)
    print(f"drop {len(d)} decl(s); freed {len(f)} decls / {tot} lines")
    for m, l in per.most_common():
        print(f"{l:6d} {cnt[m]:4d}  {m}")
    left = {SP[n]["mod"] for n in closure(d, keep) if n in SP}
    gone = sorted({SP[n]["mod"] for n in f if n in SP} - left)
    print("modules emptied:", gone)


def cmd_single():
    out = []
    for n in NODES:
        f, tot = freed({n})
        out.append((tot, len(f), n))
    out.sort(reverse=True)
    for tot, k, n in out[:60]:
        if tot >= 60:
            print(f"{tot:6d} {k:5d}  {NODES[n]}  {n}")


def cmd_greedy(minfree):
    drop, cur = set(), 0
    ladder = []
    while True:
        best = None
        for n in NODES:
            if n in drop:
                continue
            f, tot = freed(drop | {n})
            if best is None or tot > best[0]:
                best = (tot, n)
        if best is None or best[0] - cur < minfree:
            break
        drop.add(best[1])
        ladder.append((best[0], best[1]))
        cur = best[0]
        print(f"+{cur:6d}  {NODES[best[1]]}  {best[1]}")
    print(f"total {cur} lines over {len(drop)} drops")
    per, cnt = per_module(freed(drop)[0])
    for m, l in per.most_common():
        print(f"{l:6d} {cnt[m]:4d}  {m}")


R1 = ({"OAI.PlaneFiveColor.Spectral.exists_terminal_factor",
       "OAI.EuclideanFiveColor.CodedMax.exists_maximal"},
      ["OAI.EuclideanFiveColor.CompactTower.strict_compact_successor"])


def cmd_marginal(args):
    base, keep = set(R1[0]), list(R1[1])
    if "--base" in args:
        i = args.index("--base")
        j = args.index("--keep") if "--keep" in args else len(args)
        base = set(args[i + 1:j])
        keep = list(args[j + 1:]) if "--keep" in args else []
    f0, t0 = freed(base, keep)
    print(f"base: {len(base)} drops, keep {keep} -> {t0} lines")
    out = []
    for n in NODES:
        if n in base:
            continue
        f, tot = freed(base | {n}, keep)
        out.append((tot - t0, len(f) - len(f0), n))
    out.sort(reverse=True)
    print("marginal gain of one more dropped declaration, on top of the base:")
    for d, k, n in out[:45]:
        if d <= 0:
            break
        print(f"{d:6d} {k:5d}  {NODES[n]}  {n}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "marginal":
        cmd_marginal(a[1:])
    elif a[0] == "free":
        cmd_free(a[1:])
    elif a[0] == "single":
        cmd_single()
    elif a[0] == "greedy":
        m = 60
        if "--min" in a:
            m = int(a[a.index("--min") + 1])
        cmd_greedy(m)
