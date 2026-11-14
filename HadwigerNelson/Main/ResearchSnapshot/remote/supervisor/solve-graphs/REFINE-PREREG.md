# Grade correction, restriction-map precision, and pre-registration for the k = 5 refinement

Written **before** the run. ONE process, 60 s total, checkpoint per step.

## 1. Grade correction on `union_tau` (explicit downgrade)
The union result is hereby graded **"reported embedded edge graph"**, not "verified induced graph".
Reason, stated plainly: the floating prefilter nominated candidates in the band `|d²−1| < 10⁻⁶`, and
re-checking the 400 rejected candidates nearest to distance 1 **does not prove that the prefilter
missed no unit pair**. A full exact audit of all `1048·1047/2 = 548,628` pairs is in progress
elsewhere; until it completes, the induced completeness of the edge list is **pending**.

What the current evidence does and does not support:

| claim | status now |
|---|---|
| every one of the 5487 reported edges is exactly unit | **verified** (exact field identity, 0 failures) |
| the reported 5487-edge graph `G_rep` has a proper 5-colouring | **verified** (0 monochromatic edges, independently re-checked) |
| `chi(G_rep) = 5` | **verified** for `G_rep` |
| `G_rep` is the **induced** unit-distance graph on the 1048 points | **PENDING** (independent full exact audit) |
| `chi` of the true induced graph `G_ind ⊇ G_rep` | `>= 5` holds (more edges cannot add colourability); `<= 5` **pending** |

All results in this block are therefore statements about **`G_rep`**: the graph on the 1048 reported
points with the 5487 reported edges. If the audit later adds edges, the survivor/witness statements
here remain correct for `G_rep` and their status for `G_ind` must be re-examined.

## 2. Retraction of the blanket "forcedness can only increase"
I previously wrote that adding the B-copy means "forcedness can only increase". That is **not** a
statement that transfers without a restriction map, and as written it is withdrawn. The precise
version:

> **Restriction-map fact.** `H` is an induced subgraph of `G_rep`. Every proper 5-colouring of
> `G_rep` restricts along `iota : V(H) → V(G_rep)` to a proper 5-colouring of `H`. Hence for a pair
> `{p,q} ⊆ iota(V(H))`: **non-forced in `H` implies non-forced in `G_rep`** (any `G_rep`-colouring
> would restrict to an `H`-colouring separating them, and none such exists in `H`).

This gives an inference **only** for pairs with both endpoints inside the `H` copy. For a pair with at
least one **B-only** endpoint there is **no** implication in either direction, because no restriction
map connects those vertices to `H`. So the interesting candidates are pairs with a B-only endpoint;
pairs internal to the `H` copy are already known non-forced by the 34-witness certificate, and the
refinement run below will re-establish that only for witnesses of `G_rep` itself.

## 2a. CORRECTION (added after the run)
Section 2's implication is **backwards** and is retracted; see `CORRECTION-restriction-map.md`. The
correct fact is "forced in H implies forced in G_rep", which gives **no** elimination here. All 1145
survivors remain untested candidates.

## 3. Pre-registered refinement
* Input: `G_rep` — 1048 vertices, the 5487-edge list in `certs/union_tau_edges.txt`, and the frozen
  initial witness in `certs/union_tau_witness.txt`. **The frozen witness is never modified.**
* `W` = list of witnesses, starting with the frozen one. `S` = intersection over `W` of the
  non-adjacent pairs coloured equally.
* At each step: recompute signatures (`v ↦ (c_w(v))_w`) and the surviving classes; among untested
  pairs in `S` take the lexicographic minimum of `(−class size, use[i]+use[j], i, j)` — largest
  remaining equal-signature class, then least-used endpoints, then smallest indices. Deterministic.
* Solve with the combinatorial **disequality** constraint `c(i) != c(j)` (5 binary clauses). This edge
  is never a unit edge.
* On SAT: verify the witness against **all 5487 reported edges**; if invalid, stop. Retain it, update
  `S` and the classes immediately, checkpoint.
* On UNSAT: **stop at once**, save the exact CNF (and attempt a proof only if the solver binding
  supports it in budget). Record as a **candidate forced pair only**, never as forcing, until
  independent verification.
* Cap: at most **16** targets, and stop when the deadline is reached.
* **Survivors are never claimed forced merely because they are unseparated.**

## 4. Scope
Statements are about `G_rep` at `k = 5`. A confirmed `k = 5` forced pair would give an explicit
6-chromatic unit-distance graph after the geometry branch's amplifier and would simplify the analytic
proof; it is useful work, though it would **not** be a new `6`-vs-`7` bound.
