# SEED S2 — chosen and stated BEFORE any computation

## Choice
**`S2 = H ∪ R90(H)`**, where `H` is the frozen 553-point Heule set and
`R90(x,y) = (−y, x)` is rotation by 90° about the origin.

`0 = (0,0)` is a vertex of `H` (line 1 of `refs/heule_553.vtx`), so the origin is fixed and the
overlap is at least 1.

## Why this seed, from cached information (no new numbers assumed)
Cached facts about the closed seed `H ∪ (H+τ)`, `τ = (3/2, √3/2)`:
* overlap **58 of 553** points (10.5%) — the translate is close to a symmetry of `H`;
* only **184 new cross edges** on 5487 (3.4%) — the second copy mostly reproduced the first.

A **displacement** is thus a poor amplifier here: it maps `H` near itself. The other exact isometry
class available without leaving the field is **rotation about a point**. `R90` is
* exact in `Q(√3,√5,√11)` by component swap and sign, with **no field extension**;
* order 4 and a rigid motion with no displacement vector, so it cannot reproduce the near-symmetry
  structure that made the closed seed a near-duplicate;
* a genuinely different relation from the closed seed, which is why it is not a repeat.

**Stated as heuristic, not proof:** more cross edges and smaller critical order are guessed to help by
increasing constraint density. Neither is a proven rigidity criterion, and neither is treated as a
prediction that S2 forces anything.

## Method — exact, with NO floating prefilter
Every pair is decided exactly; there is no candidate-filtering step whose completeness would need
proving.
* Coordinates are rational 8-tuples in the basis `{1,3,5,11,15,33,55,165}`. Let `S` = lcm of all
  denominators actually occurring (the independent audit used 288; `S` is recomputed and asserted).
  Each coordinate becomes an integer vector `= coord · S`.
* `d²(p,q) = G_m[i][i] + G_m[j][j] − 2·G_m[i][j]` per basis component `m`, where
  `G_m = X·A_m·Xᵀ + Y·A_m·Yᵀ` and `A_m[p][q] = k` when the basis product table gives
  `basis[p]·basis[q] = k·basis[m]`. All arithmetic is `int64`; magnitudes are asserted below `2^62`.
* **Edge ⟺ `D[0] == S²` and `D[m] == 0` for all `m ≥ 1`.**
* Because this is a bilinear form over all pairs at once, the induced edge set is **complete by
  construction** — not "reported with completeness pending".

## Validation inside the same single job (60 s total)
1. All claimed edges re-verified by the independent `udg.exact.Field` implementation (exact identity
   `d² = 1`), which shares no code with the Gram path.
2. The 2722 frozen `H`-edges are reproduced **exactly**: every one is a claimed edge, and no extra
   edge appears between `H`-points that is not in the frozen edge list. This is what would expose a
   wrong `A_m` table.
3. All claimed vertices distinct after exact dedup; overlap and new-edge counts reported.
4. A 5-colouring, if found, is checked edge-by-edge before being called a witness.

## Outcome rules
* If the job finishes: publish an **exact induced-edge certificate** (`N`, `|E|`, overlap, new edges,
  full edge list, full point list with provenance, hashes, elapsed) plus the verified 5-colouring if
  obtained. No chromatic or forcing claim beyond what is checked.
* If `k=5` is UNSAT: save the CNF, report as **candidate only** — no UNSAT is accepted without a
  verifiable proof, and no proof is attempted beyond what fits.
* If all-pairs completeness or the solver cannot fit the 60 s budget: **label the graph a reported
  subgraph** and write a local-check packet. No induced certificate is claimed.
* No forced-pair search this block; no translation sweep; no second seed; no separate validation
  process.
