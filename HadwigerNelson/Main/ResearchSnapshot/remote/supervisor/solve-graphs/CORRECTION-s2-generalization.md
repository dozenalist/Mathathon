# Correction: my generalisation from S2 was too strong, and S2's verification provenance

## What I claimed
In `CERTIFICATE-seed-s2.md` and STATUS I wrote: "vertex 0 is `(0,0)`, which `R90` fixes, forcing
overlap exactly 1. A rotation about a NON-vertex centre is required for a non-clique interface."

**Both halves are wrong and are withdrawn.**

## Why
`R90` fixes the origin, which *guarantees* at least one coincidence. It does **not** bound the overlap
to exactly one: any other point `p` with `R90(p) ∈ V(H)` is a further coincidence, and the measured
overlap of 1 is a **fact about this particular centre**, not a consequence of the centre being a
vertex. Equally, a non-vertex centre is **neither necessary nor sufficient** for a non-clique overlap:
a rotation about a non-vertex can still produce an overlap that happens to be a clique, and a rotation
about a vertex can produce a larger, non-clique overlap.

The correct statements are only these:
* overlap = (points fixed by the transform) ∪ (points whose image is another point of the set);
* overlap size is an empirical property of the chosen map, to be **measured**, not inferred;
* what makes a seed inert is not the overlap's size but whether the two sides are coupled — Theorem A
  needs a **clique interface together with zero cross edges**.

## Verification provenance for S2 — stated honestly
S2's induced completeness was checked **by my own job**, not by an independent audit. What that means
concretely:
* the all-pairs decision and the Gram/bilinear construction were done by `seed_s2.py`;
* the cross-check re-verified all 5444 claimed edges through a *separate* code path
  (`udg.exact.Field`, exact field identity) and reproduced the 2722 frozen `H`-edges exactly;
* those checks are real but they are **self-verification**, and the supervisor has **not**
  independently all-pairs checked S2.

So S2's status is: **self-checked exact induced certificate, pending external all-pairs audit** —
i.e. the same "reported subgraph" caution that `union_tau` carried before its external audit, but with
stronger internal checks. It must not be described as externally verified.

## Retained
S2 stands as a **negative design result**: `overlap = 1`, `A-side 2684 + B-side 2684 + genuine cross
0`, hence a clique-sum, hence `chi = 5` by Theorem A. That conclusion does not depend on the
withdrawn generalisation — it depends only on the measured cross-edge count of 0.
