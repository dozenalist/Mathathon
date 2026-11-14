# Seed S3 = H ∪ (H + u), u = (1/2, √3/2), |u| = 1 — nontrivial exact certificate

**Verification provenance: SELF-CHECKED, not externally audited.** Everything below was produced and
checked inside one process by `seed_s3.py`, using two independent code paths (the int64 bilinear form,
and `udg.exact.Field` re-verification of every edge) plus exact reproduction of the frozen `H` edge set.
No supervisor or third-party audit of S3's all-pairs completeness has been performed. Treat it as a
self-checked exact certificate **pending external audit**, not as externally verified.

## Object
`S3` = induced unit-distance graph on `V(H) ∪ (V(H)+u)`, `H` the frozen 553-point Heule set
(`refs/heule_553.vtx` sha256 `7e43a025…`, `.edge` sha256 `b339b6a7…`, unmodified), `u = (1/2, √3/2)`
exact in `Q(√3,√5,√11)`, verified `|u|² = 1` in the field.

| quantity | value |
|---|---|
| points before dedup | 1106 |
| **distinct points** | **940** |
| **overlap** | **166** (30% of `H`) |
| denominator lcm | **288** |
| pairs decided exactly (all) | **441 330** |
| **induced edges** | **5119** |
| A-only / B-only edges | 1325 / 1331 |
| **genuine A-only↔B-only cross edges** | **307** |
| edges touching an overlap point | 2156 |
| overlap a clique? | **No** — 166 points cannot be pairwise unit apart (`K_4`-free) |
| proper 5-colouring | **found, all-edge checked: 0 monochromatic** |
| elapsed | **0.36 s** of the 60 s budget |

## The intended interaction, stated in advance and confirmed in full
`|u| = 1` forces `|w − (w+u)| = 1`, so every `w` whose image is not a coincidence contributes a genuine
cross edge. Measured: **553 of 553** pairs `(w, w+u)` are present as edges, **0 missing** — the
pre-registered bound `≥ 553 − overlap` is satisfied with room to spare. The coupling is a consequence of
`|u| = 1`, not of numerical luck.

## Exactness, and the proved overflow bound
All pairs decided by an `int64` bilinear form
`d²(p,q)_m = G_m[i][i] + G_m[j][j] − 2G_m[i][j]`, edge iff `D[0] = 288²` and `D[m] = 0` for `m ≥ 1`.
**No floating prefilter exists in this job**, so induced completeness holds by construction.

Overflow: with `|X| ≤ S·M` and Gram entries sums of at most `T²` terms of size `≤ max|X|²·max k`
(`T = 8`, `max k = 165`), `|D| ≤ 4·T²·max|X|²·max k`. The job computes this bound on the actual data —
**1.401 × 10¹⁰**, against `2⁶² = 4.612 × 10¹⁸` — asserts it, and also asserts the measured
`max |G| < 2⁶²` before publishing.

## Validation performed in the same job
1. All 5119 edges re-verified by the independent `udg.exact.Field` path: **0 failures**.
2. The 2722 frozen `H`-edges reproduced exactly: **0 missed, 0 extra inside `H`** — the check that
   would expose a wrong multiplication table.
3. Provenance classification counts sum to `|E|`: `1325 + 1331 + 307 + 2156 = 5119`.
4. The 5-colouring was checked against **all** 5119 edges before being recorded: 0 monochromatic.

## `chi = 5`
The A-side is an induced copy of `H` (all 2722 edges present, none extra), so `chi(S3) ≥ 5`; the
verified 5-colouring gives `chi(S3) ≤ 5`. Hence `chi(S3) = 5`.

## Why this differs from the two closed seeds
* `R90` about the origin: overlap 1, **0** genuine cross edges → clique-sum, inert.
* `τ = (3/2,√3/2)`: overlap 58, 184 cross edges, but that search is **closed**.
* `u`: overlap **166** (a genuine, non-clique interface) **and** 307 genuine cross edges, with all 553
  intended pairs realised. This is the first seed carrying both a substantial interface and a
  substantial coupling, and it is **not** a clique-sum.

## Not claimed
No forced-equal pair; no `chi ≥ 6`; no `chi(R²)` statement; no UNSAT (none arose). **No forced-pair
search was run.** The 166-point overlap shows `H` is partly invariant under a 60° unit step — a fact
about `H`, not a general principle.
