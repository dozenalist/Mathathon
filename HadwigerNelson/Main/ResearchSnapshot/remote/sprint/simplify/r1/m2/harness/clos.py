"""Shared closure helpers over m10's DECLGRAPH.log + SPANS.json (read-only reuse)."""
import json, pathlib, collections
H = pathlib.Path(__file__).resolve().parent
HEAD = ["OAI.EuclideanFiveColor.no_proper_five_coloring",
        "OAI.EuclideanFiveColor.no_proper_five_coloring_algebraic",
        "OAI.Problem160.properColoring_seven",
        "OAI.EuclideanFiveColor.proper_iff_weak",
        "OAI.Problem160.chromaticNumber_bounds",
        "OAI.EuclideanFiveColor.not_proper_five_coloring_compl_null",
        "OAI.EuclideanFiveColor.algebraic_colorable_iff"]
DEF = {"def","abbrev","structure","class","inductive","instance","opaque"}
def load(log=None):
    nodes, et, ev = {}, collections.defaultdict(set), collections.defaultdict(set)
    for ln in (log or (H/"DECLGRAPH.log")).read_text().splitlines():
        if ln.startswith("NODE "):
            _, m, n = ln.split(" ", 2); nodes[n] = m
        elif ln.startswith("EDGET "):
            _, a, b = ln.split(" ", 2); et[a].add(b)
        elif ln.startswith("EDGEV "):
            _, a, b = ln.split(" ", 2); ev[a].add(b)
    return nodes, et, ev
def spans(): return json.loads((H/"SPANS.json").read_text())
def closure(nodes, et, ev, drop_v=(), roots=None):
    drop_v = set(drop_v)
    seen, stack = set(), list(roots if roots is not None else HEAD)
    while stack:
        n = stack.pop()
        if n in seen: continue
        seen.add(n); stack.extend(et.get(n, ()))
        if n not in drop_v: stack.extend(ev.get(n, ()))
    return seen
def lines(S, sp):
    per = collections.Counter()
    for n in S:
        if n in sp: per[sp[n]["mod"]] += sp[n]["lines"]
    return per
