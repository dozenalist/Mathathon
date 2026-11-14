#!/usr/bin/env python3
"""Corrected fixed-architecture dead mass.

m10's DECLGRAPH.log emits NODE lines only for declarations *reached* from the 7
headline declarations (it walks the proof-term closure). So a declaration of the
tree that is absent from the NODE lines is outside the closure and its value+type
are never needed: it can be deleted at fixed architecture.

Reports the per-module and total span-lines of those declarations.
"""
import json, collections, sys

H = "sprint/simplify/m10/harness/"
def main():
    nodes = set()
    name2mod = {}
    for line in open(H + "DECLGRAPH.log", encoding="utf-8", errors="ignore"):
        p = line.split()
        if p and p[0] == "NODE":
            nodes.add(p[2]); name2mod[p[2]] = p[1]
    spans = json.load(open(H + "SPANS.json"))
    print(f"{len(nodes)} reached decls, {len(spans)} declarations in SPANS")
    # normalise: SPANS keys may be missing the leading OAI. or have different prefixes
    short = {}
    for n in nodes:
        short.setdefault(n.split(".")[-1], []).append(n)
    missing, dead = [], []
    for n, s in spans.items():
        if n in nodes:
            continue
        # fall back to short-name matching within the same module
        cands = short.get(n.split(".")[-1], [])
        if any(name2mod[c].replace(".", "/") == s["mod"].replace(".", "/") or
               name2mod[c] == s["mod"] for c in cands):
            continue
        if cands:
            missing.append(n)
            continue
        dead.append((n, s))
    per = collections.Counter()
    for n, s in dead:
        per[s["mod"]] += s["lines"]
    tot = sum(s["lines"] for n, s in dead)
    print(f"\nDEAD (absent from the reached set): {len(dead)} declarations, {tot} span-lines")
    for m, L in per.most_common(40):
        print(f"  {L:5d} {m}")
    print(f"\nambiguous (short name reached elsewhere): {len(missing)}")
    dead.sort(key=lambda t: -t[1]["lines"])
    print()
    for n, s in dead[:50]:
        print(f"  {s['lines']:4d} {s['mod']}:{s['line']} {n}")
    json.dump([n for n, s in dead], open("sprint/simplify/r1/m5/dead2.json", "w"), indent=0)

main()
