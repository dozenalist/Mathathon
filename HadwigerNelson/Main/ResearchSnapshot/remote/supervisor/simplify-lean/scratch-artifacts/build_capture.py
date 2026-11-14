#!/usr/bin/env python3
"""Regenerate a BINDER-format capture from the supervisor's verified summary.
Ordering rule reverse-engineered from the 31 raw rows of the finite theorem, which are reproduced
exactly by it (asserted at the end): type binders at their own indices, then instances except
IsProbabilityMeasure mu, then mu, then IsProbabilityMeasure mu, then the remaining explicit args,
with Z (an implicit value binder) inserted at its own index."""
import json
S = json.load(open("capture/real_summary.json"))
IP = "MeasureTheory.IsProbabilityMeasure μ"
for d in S["declarations"]:
    types = d["typeBinders"]; total = d["totalBinders"]
    z = [t for t in types if t[0] == "Z"]
    xs = [t for t in types if t[0] != "Z"]
    insts = d["instanceTypes"]
    insts_wo = [i for i in insts if i != IP]
    assert IP in insts, d["declaration"]
    expl = d["explicitOrder"]
    seq = [("implicit", n, ty) for (n, ty, _) in xs]
    seq += [("instance", "inst", t) for t in insts_wo]
    seq += [("explicit", "μ", "MeasureTheory.Measure X")]
    seq += [("instance", "inst", IP)]
    seq += [("explicit", n, "?") for n in expl[1:]]
    for (n, ty, idx) in z:
        seq.insert(idx, ("implicit", n, ty))
    assert len(seq) == total, (d["declaration"], len(seq), total)
    print(f"DECL {d['declaration']} {'thm' if 'uniform_precision' in d['declaration'] else 'def'}")
    for i, (k, n, ty) in enumerate(seq):
        print(f"BINDER {d['declaration']} {i} {n} {k} {ty}")
