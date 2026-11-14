# Response to K15-REVIEW-0523-C — X-C034 / D8, and the scope of `cut_flow.py`'s public API

Author: Computation (role C). Branch `kepler15/comp-01a1d8c0`. Receipt for this block
`2026-11-14T13:29:44Z`; source at receipt `a25f5be`; X's audit `a35b713`, defect `X-C034` recorded in
X's commit `73e04d1`. Ultramath is ON; **no swarm was run** (the four-chat structure is fixed).

## 0. Accepted, and what it cost

`X-C034 / D8` is correct, and it is the worst kind: an exact verifier that returns OK on an input that
is not OK. Reproduced at `a25f5be` before any edit, with the review's own data:

```
b = (-1,-1,-1,-1,+1),  edges = [(0,1),(1,2),(2,3),(0,3)],  Phi = 1,  flow = 0
verify_flow_exact  -> (ok_cap=True, ok_div=True, div=[0,0,0,0])     # FALSE ACCEPT
feasible_flow      -> a flow                                        # FALSE ACCEPT
find_violating_cut -> None                                          # missed obstruction
singleton_bounds   -> vertex 4 flagged INFEASIBLE_POINTWISE         # the module contradicts itself
```

The cause is exactly as reported: `n = max(max(e) for e in edges) + 1`. Vertex 4 is isolated and
needs `+1`, so `δ⁺({4}) = ∅` and `Σ_U b = +1 > 0`: the instance is infeasible at **every** capacity.
The witness is retained, not deleted: `out/fixture_C034_witness.json`.

## 1. The public contract, stated before the tests

Put at the top of `cut_flow.py`, so the code and the audit are checked against a written statement:

1. **Vertex set.** The vertices of a fixture are `range(len(b))`. They are **never** inferred from
   the edge list. A vertex with no incident edge is isolated; an isolated vertex with `b(v) > 0`
   makes the instance infeasible at every `Φ`.
2. **Edge list.** Undirected, one entry per pair, indices in `range(len(b))`, no self-loops, no
   duplicates in either orientation. A violation raises `FixtureError`; it is never repaired, because
   merging a duplicate doubles that edge's capacity and dropping a self-loop hides a degree.
3. **Flow.** `φ: E → ℚ`, antisymmetric (`φ(w,v) = −φ(v,w)`), `|φ_e| ≤ Φ`, and
   `div_φ(v) = Σ_{w~v} φ(v,w) ≥ b(v)` for **every** `v ∈ range(len(b))`. A key outside `E`, or an
   antisymmetry violation, raises rather than being ignored.
4. **Cut condition.** `Σ_{v∈U} b(v) ≤ Φ|δ⁺(U)|` for every finite `U`. If some `U` has
   `δ⁺(U) = ∅` and `Σ_U b > 0` the instance is infeasible at **every** `Φ`.
5. **Threshold.** `t* = +∞` in the case of (4), otherwise `max(0, sup_U Σ_U b/|δ⁺(U)|)`. The `max(0,·)`
   is the repaired theorem's; a scan that returns a negative number is returning the supremum, not
   `t*`.
6. **Enclosure endpoints.** `b_lo ≤ b ≤ b_hi`. A violating cut found with `b_lo` violates the true
   instance; a flow found for `b_hi` serves the true instance. The directions are never swapped, and
   no verdict is drawn from the wrong end.

## 2. The repair

| # | change | why |
| --- | --- | --- |
| 1 | `n = len(b)` in `verify_flow_exact`, `feasible_flow`, `find_violating_cut` | the defect |
| 2 | `validate_fixture(b, edges)` in all five entry points | malformed input must raise, not be reinterpreted |
| 3 | `check_flow(phi, edges)` in the verifier | a stray key or a non-antisymmetric dict was silently ignored |
| 4 | `feasible_flow` refuses pointwise-infeasible instances before the LP, and handles `edges = []` | `n = 0` used to return `{}`, i.e. "feasible" |
| 5 | negative `Φ` rejected by the verifier and by `feasible_flow` | a negative capacity is not a capacity |
| 6 | `exhaustive_cut_scan`: the `+∞` branch takes precedence over any finite sup | **the D8 witness itself**: every other cut looks harmless, so a finite `best` shadowed `+∞` |
| 7 | `best is None` no longer indexed (D5) | `TypeError` on any edgeless graph |
| 8 | `t* = max(0, sup)`, raw supremum kept as `t_star_raw` (D7) | a negative `t*` is not the theorem's threshold |

Repair 6 is worth singling out: my first version of the repair fixed the vertex range but still
returned `t* = 0` on the witness, because `best` was `(0, U=(0,4))` and `max(0,0) = 0`. The `+∞`
branch has to be checked **first**. The audit caught it because the oracle said infeasible and the
scan said `Φ ≥ 0` suffices.

## 3. The audit: hand expectation / exact oracle / implementation, three ways

`audit_cut_flow_api.py`, 66 checks, exits 0. Expected outcomes are stated twice before the
implementation is consulted:

* a **hand** expectation, written as a literal per case (e.g. "vertex 4 is isolated and needs +1");
* an **exact oracle**: feasibility of `{div(v) ≥ b(v) ∀v, |φ_e| ≤ Φ}` decided by Fourier–Motzkin
  elimination over ℚ. It builds its constraints from `range(len(b))`, so it cannot inherit the
  omission, and it shares no code with `cut_flow.py`.

The implementation must agree with both on every path: `feasible_flow` non-`None`, `find_violating_cut`
non-`None`, `Φ ≥ t*`, and every returned flow re-verified exactly.

**Two of my own hand expectations were wrong, and the three-way check found them** — recorded because
that is the evidence the check has teeth:

* `A11` (`b = (−1,2,−1,1)` on a path of length 3, `Φ = 1`) I called feasible. It is not: vertex 1
  needs 2, forcing `φ(0,1) = −1` and `φ(1,2) = +1`, and then vertex 3 needs `+1` from the same edge.
* the "capacity violated" case used `b = (0,0)`, where `|φ| = 2` violates the divergence bound for an
  unrelated reason; with `b = (0,−2)` the capacity check is the only one that fires.

| group | cases | what it pins down |
| --- | --- | --- |
| A | the review's witness at `Φ = 1`, `10⁶`, `0` | every path rejects; `evaluate_external` emits no `PATCH_FEASIBLE` |
| B | 12 three-way cases | hand = oracle = flow = scan = cut, on paths, stars, disconnected components |
| C | self-loop, duplicate (both orientations), out-of-range, non-pair | `FixtureError` from all four paths |
| D | unknown key, non-antisymmetric, capacity violated | the verifier's own rejections |
| E | `b_lo = (−1,−1) < b < b_hi = (+1,−1)`, edgeless | the evaluator claims **neither** a flow nor a violation: the honest answer for a straddling enclosure |
| F | structural | the divergence has `len(b)` entries; a reintroduced `max(edges)+1` fails immediately |

## 4. Reconcilement of D4, D5, D7 against the actual revision

**D5 (latent).** `exhaustive_cut_scan` raised `TypeError` whenever no subset had a crossing edge.
Live, now fixed: edgeless input returns `+∞` if some `b(v) > 0` and `0` otherwise. Tested (S18, audit
B).

**D7 (cosmetic).** With all `b < 0` the scan reported a negative `t*`. Live, now fixed: `t* = 0` and
the raw supremum is kept in `t_star_raw`. `b = (−1,−2)` on one edge gives `t* = 0`, raw `−1`.

**D4 (the fixture).** The premise as stated — "all 12 ring cells are unbounded, so `b = −∞` there" —
is **not true of the code at the revision audited, and not true of the periodic packing**:

* `icos_b()` at `4bcbd3a` already gave each ring cell the finite volume `(4096 − V_DOD)/12`, hence
  `b_ring ≈ −335.2`. There is no `−∞` anywhere in the fixture.
* In the periodic packing the cells are bounded: the thirteen torus cells partition the period cube,
  sum to `4096.000000000`, and each ring cell has volume `340.870809080957` (measured to `3.4·10⁻¹³`
  by half-space intersection, and exact given the partition identity plus congruence —
  `period_convention.py`). The unbounded cells appear only if the thirteen points are read as a
  *non-periodic* finite set, which is not the fixture.
* What is true, and is recorded as `V4` in `cut_flow.py`: the fixture is **unsaturated**
  (`max hole ≥ 12.327`), so it cannot support Hales-type local arguments. That is a statement about
  what the fixture may be used for, not about whether the cut condition can be evaluated on it.

Where D4's spirit is right, stated precisely: the fixture's cut condition is **one inequality**. Over
all 8191 subsets, exactly one has `Σ_U b > 0` — the singleton `{0}` — because every subset containing
a ring vertex has `Σ_U b ≤ −335.1`. So the fixture yields the number `0.008880268414739` and nothing
else. It is evidence, but thin evidence, and it is not evidence of the Hales type.

## 5. What this block does NOT establish

* The repair is about the **API's contract**, not about the geometry. Nothing here changes any bound.
* `K15-C-CUTIMPLIES-003` remains **one implication**: the finite-`U` cut condition forces
  `ρ ≤ 1/√32`. The converse — Kepler ⇒ a finite `Φ` works — is open, and **no equivalence is claimed**.
* Nothing here assumes or asserts exact contact matchings for saturated packings. The only geometric
  statement used is the cell-volume partition identity, which holds for every packing.
* The audit's oracle decides feasibility of the *finite* LP. It says nothing about the infinite
  packing; that is what `cut_flow.py`'s "PATCH_FEASIBLE only" label is for, and it is unchanged.

## 6. Files and how to run

```bash
cd KeplerConjecture/Computation
python3 audit_cut_flow_api.py     # 66 checks, three-way; exit 0
python3 tests_cut_flow.py         # S1-S18 including the witness; exit 0
python3 cut_flow.py --fixture out/fixture_C034_witness.json   # the witness: no flow, UNBOUNDED cut
```

Artifacts: `cut_flow.py` (contract + repair), `audit_cut_flow_api.py`,
`out/fixture_C034_witness.json`, `tests_cut_flow.py` S16–S18, `CLAIM_REGISTER.md`.

## 7. Clock

Receipt `2026-11-14T13:29:44Z`. The repair was pushed at `13:33:03Z` (commit `ae545b9`); this
document, the register update and the geometric item follow, and the closing line is written from
`date -u` at the end of the block.
