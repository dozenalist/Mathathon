# Independent audit: the 73-cell, 888-edge `k = 6` UNSAT certificate at `a = 1/5`

Target (read-only, producer = `supervisor/solve-independent/`): `PATCH19.md`, `patch19_cert.json`,
`p19.cnf`, `p19.drup`, `rup.c`, `patch19.py`, `p19_gen.py`. My own copies and logs:
`audit19/` in this directory. Evidence grades: **[A]** machine-checked here; **[P]** paper-level
argument written here; **[S]** source-checked by reading; **[X]** record only, not verified.

## 1. Verdict

**The certificate verifies, independently and unconditionally: the CNF `p19.cnf` is UNSAT.**
`drat-trim` (M. Heule's checker, binary copied from `supervisor/solve-graphs/tools/drat-trim`,
sha256 `a9571deb…e9066`) reports `s VERIFIED` on `p19.cnf` (sha256 `31f35466…3b69`) with
`p19.drup` (sha256 `f4ec9532…1496e`) in **2.63 s**, backward checking, `5144 of 6496` clauses in core,
`36014 of 42110` lemmas in core, `0 RAT lemmas`. Log: `audit19/drat_run.log`. This is *not* a rerun of
the producer's checker; the producer's `rup.c` is a separate, defective program (§4).

What that establishes: **no colouring of those 73 cells with 6 colours has all 888 listed pairs
separated**, hence no 6-colouring of the plane that is constant on the interiors of the Voronoi
hexagons of the triangular lattice of spacing `a√3` at `a = 1/5`. A no-go for **one** cell-constant
family at **one** parameter. Nothing about `chi(R^2)`; nothing at other `a`; not `chi = 8` (§5).

## 2. Geometry, checked independently [P] + [A] (repaired)

**Corrections to my previous version of this section.** (i) The inradius at `a = 1/5` is
`a√3/2 = √3/10 ≈ 0.17321`, not `1/(2√3) ≈ 0.28868` (that is `1/(2√3) = √3/6`, the inradius at
`a = 1/3`). (ii) The extrema of the distance between two translates are **not** `|v| ± 2h(n̂)` in the
centre direction in general: `|v| + 2h(v̂) = max_{w ∈ 2H} ⟨v + w, v̂⟩` is the **maximum projection** onto
`v̂`, hence a **lower** bound for `max_w |v + w|` (as `|x| ≥ ⟨x, v̂⟩`), not an upper bound. A lower bound
`> 1` does certify `dmax > 1`, so that inference is legitimate; the earlier mistake was the word "upper",
not the direction of use. My table's use of `h` for the *minimum* was valid only for the offsets where
the origin projects onto an edge. The certificate uses only the exact polygon formulas, so the point is
moot for it. The correct
object is the Minkowski difference: for a fixed cell `H` (centrally symmetric, so `H − H = 2H`),

    distances realised between H and H+v = { |v + w| : w ∈ 2H },

so `dmin(v) = dist(0, 2H+v)` — computed as `min` over the six edges of point-to-segment distance, and
`0` when `0 ∈ 2H+v` (interior or boundary) — and `dmax(v) = max_{w ∈ 2H} |v+w|`, a convex function on a
polygon, hence attained at a **vertex** of `2H`. A pair of cells is *strictly forced* (i.e. admits
interior points at distance exactly 1) iff `dmin(v) < 1 < dmax(v)`, with strict inequalities because
the realisable distances form the open interval `(dmin, dmax)`.

**Every offset recomputed exactly [A].** `checks/interval_a1.py` recomputes all 42 offsets at `a = 1`
in exact `Q(√3)` arithmetic with the `2H` construction above: **0 mismatches** against
`supervisor/solve-independent/interval_cert.json` (`mu2`, `nu2`), min² ∈ `{3,7,12,16,19}`,
max² ∈ `{28,43,49,64,67}`. Of the 42 minima, **12 are attained at an edge interior and 30 at a polygon
vertex** — so the endpoint contacts are *not* uniformly vertex-to-vertex, and the previous version's
phrasing was wrong to suggest a single type.

**The forced set at `a = 1/5` [P]+[A].**

| `N` | `|v|/a` | `dmin(1)²` | `dmax(1)²` | forced at `a = 1/5`? |
|---|---|---|---|---|
| 1 | `√3` | 0 (cells touch) | 13 | **no**: `dmax = 0.7211 < 1` |
| 3 | `3` | 1 | 25 | **no**: `dmax = 5/5 = 1` exactly, so the open interval is `(0.2, 1)` ∌ 1 |
| 4 | `2√3` | 3 | 28 | yes: `(0.3464, 1.0583)` |
| 7 | `√21` | 7 | 43 | yes |
| 9 | `3√3` | 12 | 49 | yes: `(0.6928, 1.4)` |
| 12 | `6` | 16 | 64 | yes: `(0.8, 1.6)` |
| 13 | `√39` | 19 | 67 | yes: `(0.8718, 1.6372)` |
| 16 | `4√3` | ? | ? | **no**: `dmin(1/5) = 1.0392 > 1` |

`F = {4,7,9,12,13}` with multiplicities `6,12,6,6,12 = 42 = |F|` (Eisenstein representation counts),
matching the producer's asserted `|F| = 42` and the centre degree. `|P| = 73` for `{N ≤ 19}`:
`1+6+6+6+12+6+6+12+6+12 = 73`. The producer's search window (`N ≤ 16`, `|p|,|q| ≤ 5`) suffices because
forcing needs `dmax > 1`, i.e. `a·dmax(1) > 1`, and `dmax(1) ≤ |v|/a + 2 = √3√N + 2 ≤ 1.4·5/... `
— concretely `a = 1/5` gives `√3√N/5 + 0.4 > 1` iff `N > 3.24`, and the largest excluded candidate
`N = 16` is checked directly above.

## 3. Patch → CNF mapping, checked at the count level [S]+[P]

`p19.cnf` header `p cnf 438 6496`; first clauses `1 2 3 4 5 6 0`, `-1 -2 0`, matching `p19_gen.py`'s
`var(v,c) = v*6+c+1` with the at-least-one clause first and the `C(6,2) = 15` at-most-one pairs next.
Counts: `438 = 73·6`; `6496 = 73·16 + 888·6 = 1168 + 5328`. **No symmetry breaking, no colour
permutation clauses, no extra assumptions** — so UNSAT of this CNF is a statement about the graph, not
about a normal form [S].

**Not verified here:** the literal-by-literal correspondence between each of the 888 binary edge
clauses and the `edges_indexed` list of `patch19_cert.json`. That would need a second program run and
this block's computation budget (60 s, one process) went to `drat-trim`. What is verified is that the
CNF is UNSAT as supplied, and that its *shape and counts* are exactly those of a 73-vertex,
888-edge 6-colouring encoding. A wrong edge set would have to be shape-and-count-identical to escape
this check; the generator's code (`p19_gen.py`, 3 lines of edge clauses over `C["edges_indexed"]`) makes
that unlikely but it is **not** excluded by evidence in hand.

## 4. The producer's checker `rup.c`: the reported defect is real, and lethal to its own claim [S]

Confirmed at `rup.c:46-56`:

```c
int *tmp=malloc(n*sizeof(int)); int p=0;
for(k...) if(litval(lits[k])!=-1) tmp[p++]=lits[k];
for(k...) if(litval(lits[k])==-1) tmp[p++]=lits[k];   /* both loops run over all k */
...
int nonfalse=p;                                        /* p == n here, always */
if(nonfalse==0){ *cf=1; return; }                      /* DEAD */
if(n==1){ ... }                                        /* ok */
...
if(nonfalse==1){ ... }                                 /* DEAD */
```

So `nonfalse == n` unconditionally, and both branches keyed on `nonfalse` are dead:
* a proof clause **falsified at level 0** is added with its first two (false) literals as watches —
  exactly the watch-invariant violation the producer reports as "defect (i), fixed";
* a proof clause **unit at level 0** is never enqueued — the producer's "defect (ii), fixed" is inert.

Neither dead branch can make an invalid proof pass, because `propagate()` returns a conflict only when
a clause's remaining watched literal is genuinely false (`if(litval(first)==-1) return 1;`), so the
message `RUP VERIFIED: 42109 steps` is not *evidence of unsoundness* — but it is **not evidence of
validity either**: the two paths that would matter for a level-0 unit/falsified lemma never executed,
and the run's `rc 0` cannot distinguish "all steps RUP" from "all steps RUP in the cases the code
handles". Treat the producer's `rc 0` as **no information**; `drat-trim`'s `s VERIFIED` replaces it.
Also note `rup.c` ignores deletion lines entirely; the supplied proof contains no `d` lines, so this is
moot here, and ignoring deletions is sound anyway (each retained clause is itself verified as a
consequence, so by induction every retained clause is implied by the CNF).

## 5. Claims I do NOT accept

* **`chi(G[P]) = 8`.** Machine-decided by two CDCL solvers with an explicit verified 8-colouring
  (`0` monochromatic edges of 888) and a reported 7-UNSAT, but **no certificate for 7-UNSAT**. So:
  `chi ≥ 8` — [X], record only; `chi ≤ 8` — [X] as run, and a verified 8-colouring is checkable in
  principle (colour class sizes `12,10,10,9,9,9,8,6` are recorded). Only `chi ≥ 7` is certified here.
* **"The honeycomb family is excluded for `a ∈ (1/√13, 1/2]` and at `a = 1/5`."** The first range is a
  *different* theorem (the earlier certified `N ∈ {1,3,4}` family). At `a = 1/5` what is certified is
  this patch, for cell-constant colourings. Both are no-gos for cell-constant families, not for the
  plane; they do not combine into a statement about `chi(R^2)`. The untested range
  `a ∈ (0.12204, 0.27735) \ {0.2}` is exactly that — untested.
* Any claim that six colours die *for the plane*: a hypothetical 6-colouring may be non-constant on
  cells, and nothing here rules that out.

## 6. Acceptance checklist (independent)

| # | check | verdict |
|---|---|---|
| 1 | CNF is a 6-colouring encoding of a 73-vertex graph, no symmetry breaking | pass [S] (counts `73·16 + 888·6`) |
| 2 | edge set = forced pairs at `a = 1/5`, strict-interior criterion | pass [P] (table §2; `N = 3` boundary and `N = 16` both correctly excluded) |
| 3 | 73 cells = `{N ≤ 19}` | pass [P] |
| 4 | CNF UNSAT, by an independent checker | **pass [A]** `drat-trim`: `s VERIFIED`, 2.63 s |
| 5 | producer's `rup.c` verdict | reject as evidence (§4, dead `nonfalse`) |
| 6 | edge-clause ↔ `edges_indexed` literal-level match | **not verified** (budget) |
| 7 | `chi(G[P]) = 8` | **not certified** (only `chi ≥ 7` is) |
| 8 | relevance to `chi(R^2)` | none claimed; cell-constant family only |

**Net:** the claim "this 73-cell patch has no proper 6-colouring" is **accepted**, on independent
certificate verification, with the scope of §1 and the one unverified correspondence in §3 row 6.
Everything the producer says above `k = 6`, or about the plane, or about `chi = 8`, is not accepted
here.
