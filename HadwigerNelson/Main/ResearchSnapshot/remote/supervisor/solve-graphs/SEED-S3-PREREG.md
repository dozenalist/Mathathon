# SEED S3 — chosen and stated BEFORE any computation

## Choice
**`S3 = H ∪ (H + u)`** with the **unit** displacement `u = (1/2, √3/2)`, exact in `Q(√3,√5,√11)`.

`H` = frozen 553-point Heule set (`refs/heule_553.vtx`, unmodified). `|u|² = 1/4 + 3/4 = 1`, so `u` is a
unit vector — a 60° lattice step.

## The intended interaction, stated explicitly in advance
Because `|u| = 1`, **every point `w` of `H` is at distance exactly 1 from `w + u`**. So for every `w`
whose image is *not* a coincidence, the pair `(w, w+u)` is a **genuine A-only/B-only unit edge**. The
copy is therefore coupled to the original at every non-coinciding vertex, by construction and with no
numerical luck: the coupling is a consequence of `|u| = 1` alone.

This gives an exact identity the job will verify:
> `genuine_cross_edges >= 553 - overlap`,
with the pairs `(w, w+u)` supplying them explicitly (a coincidence at `w` removes exactly that one).

## Why this and not another rotation/translation
Cached, measured facts: the translate by `τ = (3/2,√3/2)` gave overlap 58 and **184** genuine cross
edges; the rotation `R90` about the origin gave overlap 1 and **0** genuine cross edges and was inert.
So the productive variable is the number of genuine cross edges, and a **unit** displacement maximises
it by the identity above rather than by chance. Unlike S2 this does not rely on any claim about which
points coincide — the overlap is measured, and the bound on cross edges is derived from `|u| = 1`.

`u` has denominator 2, dividing 288, so no coincidence is ruled out in advance; conversely coincidences
are possible and the interface may be nonempty. Whatever it is, it is **measured and reported**.

## Method — exact, no floating prefilter, with a proved overflow bound
* Coordinates as rational 8-tuples in basis `{1,3,5,11,15,33,55,165}`; `S` = lcm of occurring
  denominators (expected 288, asserted).
* `d²(p,q)_m = G_m[i][i] + G_m[j][j] − 2 G_m[i][j]` with `G_m = X A_m Xᵀ + Y A_m Yᵀ`,
  `A_m[p][q] = k` when `basis[p]·basis[q] = k·basis[m]`. All pairs at once, `int64`.
* **Overflow bound.** `|X| ≤ S·max|coeff|`. Each Gram entry is a sum of at most `8·8` terms each of
  magnitude `≤ max|X|²·max k` with `max k ≤ 165`. Hence
  `|G| ≤ 64·(S·M)²·165` and `|D| ≤ 4·max|G|`. The job asserts `max|G| < 2^62` on the actual data,
  which is a *checked* bound, and prints the measured maximum. If the assertion failed the job would
  abort rather than publish.
* **Edge ⟺ `D[0] = S²` and `D[m] = 0` for `m ≥ 1`.** Complete by construction: no candidate filter
  exists whose completeness would need proving.

## Structural gate (stop rule, decided before looking)
After building, classify every edge as A-only/A-only, B-only/B-only, or **genuine A↔B**, and record the
full overlap mapping `w ↦ w+u` for coincidences. Then:
* if **genuine cross edges = 0**, the seed is **structurally inert**: record it and **STOP** without
  solving (Theorem A territory). No fallback seed, no sweep.
* otherwise the seed is structurally nontrivial; only then spend remaining time on a 5-colouring.

## Validation inside the same single job
1. Every claimed edge re-verified by the independent `udg.exact.Field` path (exact `d² = 1`).
2. The 2722 frozen `H`-edges reproduced exactly (0 missed, 0 extra inside `H`).
3. All points distinct after exact dedup; the `prop` identity `(w, w+u)` cross edges are counted and
   compared against `553 − overlap`.
4. A 5-colouring, if sought, is checked against **all** edges before being called a witness.

## Outcome rules
* No UNSAT claim without a verifiable proof; if the solver says UNSAT, save the CNF and report
  **candidate only**.
* No forced-pair search; no second seed; no separate validation process; one process, 60 s total.
* If the seed is inert or the budget is exhausted, publish the measured structure and stop.
