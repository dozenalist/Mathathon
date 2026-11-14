# Corrected AC-conditional enumeration: 174 survivors, 12 orbits

**Scope.** Finite statement about `q ∈ {0,…,5}^6` with `q0 = 0` (one representative per
label-translation class), six-cycle interfaces `E_i = {i,(i+1) mod 6}`, labels `C = {0,…,5}`,
**conditional on Theorem AC**. No all-angle claim, no plane claim, no `WeakColoring6`.
Grades: **[P]** written argument, **[C]** exact computation, **[relayed]** from Astra/parent,
**[conditional]** rests on AC (paper-level, **not** Lean-checked).

## 1. The bug, and the corrected count **[C]**
`ac_filter_enum.py` computed reachability correctly but then rebuilt a witness **greedily**:

```python
nxt = next((p for p in A[j] if (p & cur) == 0 ...), None)   # first fit, no backtracking
```

A first-fit choice can dead-end at `j = 5` although a valid cyclic path exists, so branches that
*were* satisfiable were reported unsatisfiable — **false negatives**, and the reported 95 was too low.
Correct count: **174**.

Fixed by DP with **full predecessor tracking** (`pred[j][p]` stored for every reachable `p`), and
independently cross-checked by a **separately written backtracking DFS** with no shared code path.

| stage | count |
|---|---|
| candidates `q ∈ {0..5}^6`, `q0 = 0` | **7776** (unchanged) |
| pass AC filter | **1420** (unchanged) |
| **survivors: AC + six-orbit feasible** | **174** (was wrongly 95) |

The two independent methods return **identical survivor sets** (asserted), and every one of the 174
witnesses was re-verified by a direct constraint checker over **all six cells** — 0 failures.

**Reproduction of the parent's data point.** `q = (0,0,1,2,3,4)` is a survivor and the code returns
exactly the witness given in the audit:
`{1,4}, {2,5}, {0,3}, {2,4}, {1,5}, {0,3}`.

## 2. Structural necessary property forced by AC **[P][C]**
For a same-direction group of size `s`, `⋃_{i∈G} E_i` contains at least `s+1` labels, so AC's
requirement `|⋃ E_i| ≤ 3` forces:

> **every direction is used by at most 2 positions, and if used twice the two positions are adjacent
> (consecutive mod 6).**

Verified computationally across all 174 survivors. The resulting multiplicity patterns:

| pattern | survivors |
|---|---|
| `(2,1,1,1,1)` | 84 |
| `(2,2,1,1)` | 72 |
| `(2,2,2)` | 4 |
| `(1,1,1,1,1,1)` | 14 |

(The old file's claim `|G_d| ≤ 2` was correct; it is retained, now with its proof and its
adjacency refinement.)

## 3. Dihedral / direction-reflection classification **[P][C]**
Candidate maps: `φ(q)_i = ε · q_{σ(i)}`, `ε = ±1`, `σ` a dihedral self-map of the six positions
(`rot_k`, `ref_k`), then renormalised by subtracting `φ(q)_0` — 24 maps.

*Each map was verified as a genuine symmetry, not assumed:* for every φ, `feasible(φ(q)) ==
feasible(q)` for **all 7776** candidates, and φ is a bijection of the declared space. **All 24
passed.** (The constraint-preserving map on the data is `q ↦ ε q∘σ` together with the phase/angle
relabelling `(j, c) ↦ (ε j, ε c)`, which is what makes the sign table `sign cos((c+j−q_i)π/3)`
invariant.)

Result: the 174 survivors form **12 orbits**, sizes `24,24,24,24,12,12,12,12,12,12,4,2`
(sum 174, checked).

### The 12 minimal representatives
| # | rep `q` | multiplicity pattern | orbit size |
|---|---|---|---|
| 1 | `(0,0,1,2,3,4)` | (2,1,1,1,1) | 24 |
| 2 | `(0,0,1,2,3,5)` | (2,1,1,1,1) | 24 |
| 3 | `(0,0,1,2,4,4)` | (2,2,1,1) | 24 |
| 4 | `(0,0,1,2,4,5)` | (2,1,1,1,1) | 12 |
| 5 | `(0,0,1,3,3,2)` | (2,2,1,1) | 12 |
| 6 | `(0,0,1,3,3,4)` | (2,2,1,1) | 12 |
| 7 | `(0,0,1,3,3,5)` | (2,2,1,1) | 12 |
| 8 | `(0,0,1,3,4,2)` | (2,1,1,1,1) | 24 |
| 9 | `(0,0,1,3,4,4)` | (2,2,1,1) | 12 |
| 10 | `(0,0,2,2,4,4)` | (2,2,2) | 4 |
| 11 | `(0,1,2,3,4,5)` | (1,1,1,1,1,1) | 2 |
| 12 | `(0,1,3,5,4,2)` | (1,1,1,1,1,1) | 12 |

Witnesses for all 174 are in `certs/ac_survivors_174.json`; orbit membership in
`certs/ac_orbits_174.json`.

Two structural remarks visible from the table: every representative starts `(0,0,…)` except the two
permutation-type ones, and the `(2,2,2)` and permutation patterns have tiny or single orbits, so the
bulk of the class (96 + 72 = 168 of 174) sits in the two "one doubled direction or two" families.

## 4. What is not done, and deliberately so
* **No extra filter was added.** In particular no AC-axis or axis-aligned variant, and **no filter for
  mixed orientations** — mixed orientation groups do **not** share a common strip, so AC does not
  apply to them and inventing a constraint there would be unproved.
* **No bigger search.** The declared space is exhausted; the numbers 7776 / 1420 / 174 are complete
  counts, not partial scans.
* AC remains **paper-level and not Lean-checked**; the local fixed three-centre theorem is reported as
  Lean-passed with standard axioms and the moving extension is compiling locally **[relayed]**.
  Lemma 6.7 = `five_support_step_ban`, retained.

## 5. Reproduce
```
cd supervisor/solve-graphs && python3 ac_filter_enum2.py     # 0.36 s, one process, one thread
```
