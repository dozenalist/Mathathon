#!/usr/bin/env python3
"""Fixed-architecture deletable mass: declarations of the tree that are NOT in the
type+value closure of the 7 headline declarations (per m10's DECLGRAPH.log).

Also reports the *type-only* requirement: declarations reachable by type-edges from
a live declaration must be kept even if their value is unused (their STATEMENT is
needed), so the truly deletable ones are those outside the full closure.
"""
import json, sys, collections

H = "sprint/simplify/m10/harness/"
HEADLINES = [
    "OAI.EuclideanFiveColor.no_proper_five_coloring",
    "OAI.EuclideanFiveColor.properColoring_seven",
    "OAI.EuclideanFiveColor.proper_iff_weak",
    "OAI.EuclideanFiveColor.chromaticNumber_bounds",
    "OAI.EuclideanFiveColor.algebraic_colorable_iff",
]

def main():
    nodes, edges = {}, collections.defaultdict(set)
    for line in open(H + "DECLGRAPH.log", encoding="utf-8", errors="ignore"):
        p = line.split()
        if not p:
            continue
        if p[0] == "NODE":
            nodes[p[2]] = p[1]
        elif p[0] in ("EDGET", "EDGEV"):
            edges[p[1]].add(p[2])
    print(f"{len(nodes)} nodes, {sum(len(v) for v in edges.values())} edges")
    spans = json.load(open(H + "SPANS.json"))
    # resolve headline names: they may be namespaced differently
    have = {n for n in nodes}
    roots = []
    for h in HEADLINES:
        if h in have:
            roots.append(h)
        else:
            cand = [n for n in have if n.endswith(h.split(".", 1)[1])]
            roots.extend(cand)
    print("roots:", len(roots))
    for r in roots[:10]:
        print("   ", r)
    seen = set(roots)
    dq = list(roots)
    while dq:
        p = dq.pop()
        for c in edges.get(p, ()):
            if c not in seen:
                seen.add(c); dq.append(c)
    print(f"closure: {len(seen)} declarations")
    dead = [n for n in nodes if n not in seen]
    def span(n):
        s = spans.get(n)
        return s["lines"] if s else 0
    def mod(n):
        s = spans.get(n)
        return s["mod"] if s else nodes.get(n, "?")
    per = collections.Counter()
    tot = 0
    for n in dead:
        L = span(n); tot += L
        per[mod(n)] += L
    print(f"dead declarations: {len(dead)}, {tot} span-lines (of {sum(v['lines'] for v in spans.values())} spanned)")
    for m, L in per.most_common(30):
        print(f"  {L:5d} {m}")
    json.dump(sorted(dead), open("sprint/simplify/r1/m5/dead.json", "w"), indent=0)

main()
