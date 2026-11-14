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

## 2. Geometry, checked independently by hand [P]

Cells: Voronoi hexagons of circumradius `a = 1/5`, inradius `a√3/2 = 1/(2√3)`, lattice spacing
`a√3 = √3/5`, nearest-neighbour distance `√3/5 = 0.34641`. For a lattice offset `v` the two cells can
be at distance `t` iff `t` ranges over the interval `(|v| − 2h(n̂), |v| + 2h(n̂))` open, where `h` is the
hexagon's support function; this is `dist(0, 2V + v)` to `max_{w ∈ 2V}|v + w|`, and `2V` has
circumradius `2a = 0.4`. With `|v| = a√3·√N = √3√N/5`:

| `N` | `v` | `|v|` | forced? | reason |
|---|---|---|---|---|
| 1 | (1,0) | 0.3464 | **no** | `|v| + 2h = 0.3464 + 0.3464 = 0.6928 < 1` (h = inradius along a neighbour direction) |
| 3 | (1,1) | 0.6 | **no** | `|v| + 2h = 0.6 + 0.4 = 1` **exactly**; the only distance-1 pairs are vertices, i.e. boundary, so an interior-constant colouring is unconstrained |
| 4 | (2,0) | 0.6928 | yes | `0.3464 < 1 < 1.0928` |
| 7 | (2,1) | 0.9165 | yes | `0.52 < 1 < 1.32` |
| 9 | (3,0) | 1.0392 | yes | `0.6928 < 1 < 1.4392` |
| 12 | (2,2) | 1.2 | yes | `0.81 < 1 < 1.59` |
| 13 | (3,1) | 1.2489 | yes | `0.85 < 1 < 1.65` |
| 16 | (4,0) | 1.3856 | **no** | `|v| − 2h = 1.3856 − 0.3464 = 1.0392 > 1` |
| 19, 21 | | 1.51, 1.59 | no | `|v| − 2h > 1` |

Two consequences that make the producer's set correct and non-trivial:
* `F = {N ∈ {4,7,9,12,13}}` is exactly the forced set, with multiplicities `6, 12, 6, 6, 12 = 42 = |F|`
  (Eisenstein representation counts `r(N) = 6∏(e_i+1)` over primes `≡ 1 mod 3`), matching the
  producer's asserted `|F| = 42` and the centre's degree 42 [P].
* **The strict inequality is load-bearing at `N = 3`**, and the producer's `forced()` uses strict
  `<`/`>` (`patch19.py`: `return (dmn<Q3(1)) and (dmx>Q3(1))`) [S]. A non-strict criterion would add
  `N = 3` and be *wrong*: the distance-1 pairs there are vertices only, so constancy on interiors
  forces nothing. Conversely the crude bound `|v| − 2a` would wrongly add `N = 16`. Both errors are
  avoided.
* `|P| = 73` for `N(v) ≤ 19`: `1 + 6+6+6+12+6+6+12+6+12 = 73` over `N ∈ {0,1,3,4,7,9,12,13,16,19}` [P].
* The forced-search window `|p|,|q| ≤ 5`, `N ≤ 16` is sufficient: forcing needs `|v| < 1 + 2a = 1.4`,
  i.e. `N < 16.33`, so `N ≤ 16` [P].

Note the units in `forced()`: `dmn`, `dmx` are *squared* distances compared to `1`. For nonnegative
quantities `t < 1 ⟺ t² < 1`, so this is correct, merely written in squared units — I checked both
directions of each inequality above in distance units.

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
