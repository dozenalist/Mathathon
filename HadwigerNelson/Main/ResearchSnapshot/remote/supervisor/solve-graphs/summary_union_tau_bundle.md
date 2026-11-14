# Union bundle: reconstruction guide (self-contained)

Everything below is under `supervisor/solve-graphs/`. All grades are for **`G_rep`**, the graph on the
1048 *reported* points with the 5487 *reported* edges. **Induced completeness is PENDING** (a full
exact audit of all 548 628 pairs); see `REFINE-PREREG.md` section 1.

## Files
| file | contents |
|---|---|
| `refs/heule_553.vtx`, `refs/heule_553.edge` | frozen third-party input, 553 points / 2722 edges, unmodified |
| `certs/union_tau_points.txt` | 1048 rows: `index provenance source_index x_coeffs y_coeffs`; provenance is `A` (in H), `B` (in H+tau) or `A+B` (in the 58-point overlap) |
| `certs/union_tau_edges.txt` | 5487 edges, `u v` per line |
| `certs/union_tau_witness.txt` | frozen initial proper 5-colouring, `vertex colour` |
| `certs/refine_union_k5.json` | 17 witnesses, per-step records, 1145 survivors, all counts |
| `certs/union_tau.json` | construction record: counts, τ, prefilter statistics |

## Reconstruction
Points: index `i < 553` is `refs/heule_553.vtx` vertex `i`; index `i >= 553` is
`(refs/heule_553.vtx vertex source_index) + τ` with `τ = (3/2, √3/2)`. Coordinates are 8 rational
coefficients in the basis `{1, √3, √5, √11, √15, √33, √55, √165}` of `Q(√3,√5,√11)`.
Edge `u v` holds iff `|p_u − p_v|² = 1` exactly. Dedup merged 58 exact coincidences; 5487 = 2722
internal to `A` + 2722 internal to `B` + 184 new.

## Verified
* every reported edge is exactly unit (`d² = 1` as a field identity), 0 failures;
* 17 proper 5-colourings, each with 0 monochromatic edges out of 5487;
* `chi(G_rep) = 5` (`>= 5` because `H` is induced inside it and is 4-UNSAT; `<= 5` by the witness);
* survivors after 16 adaptive disequality targets: **1145** (from 110015), reproduced from scratch.

## Not claimed
* induced completeness — pending the full exact audit;
* that any survivor is forced — **unseparated is not forced**;
* any bound on `chi(R²)`; any new 6-vs-7 statement.
