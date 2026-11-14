# Claims ledger: what is valid, overbroad, or unverified

Scope audit of three sources, done independently in this block. Grades: **valid** (I re-derived or
re-verified it), **overbroad** (true under a narrower hypothesis than stated, or true of a
sub-family while stated of a wider one), **unverified** (no argument given / single
implementation, not checked here). Certificates in this directory: `verify_cell_nogo_v2.py`,
`audit_rect.py`, `square_family.py` (+ their `.out` files).

## A. My own v1 (`CELL-NOGO.md`, honeycomb)

| # | claim | grade | correction / certificate |
|---|---|---|---|
| A1 | distances between two closed convex cells form the interval `[dmin,dmax]` | valid | restated as Lemma 1(1) in v2 |
| A2 | forced `<=> dmin <= 1 <= dmax` | **overbroad** | a colouring cannot be constant on two closed cells with a shared edge; the convention-free criterion is **strict** `dmin < 1 < dmax` (v2 Lemma 1) |
| A3 | "the forced set is **exactly** `N in {1,3,4}` on `[1/sqrt13, 1/2)`" | **overbroad** | false on the small end: `N=7` is forced exactly on `(1/sqrt43,1/sqrt7) ∋ 0.28`, and `N=9` on `(1/7,1/sqrt12)` which overlaps the range. At `a = 0.28` the forced set is `{1,3,4,7,9}`. Exact: `{1,3,4}` only on `(1/sqrt7, 1/2)` |
| A4 | `>= 7` colours for honeycombs with `a in [1/sqrt13, 1/2)` | **valid, with both endpoints corrected** | `(1/sqrt13, 1/2]`: bottom excluded by the tangency certificate (§E), top included because a cell at `a = 1/2` has its unit pair only at opposite vertices (interior distance set `(0,1)`) |
| A5 | "a six-colouring must be cell-free" | **withdrawn** | cannot follow from a restricted parameter family; the small-cell regime (`a <= 1/sqrt13`, cell diameter `<= 0.5547`) is untouched, and that is where a cell-constant colouring would approximate an arbitrary one |
| A6 | square cells at `c = 3/5` need `>= 7` (7-clique) | valid | re-certified under the strict criterion (`square_family.py`: `dmin^2 in {0, 9/25}`, `dmax^2 >= 9/5`) |
| A7 | the paper's `r = 2/5` hexagon is the circumradius of the 7-colouring's cells | valid | `results/COMPRESSED-PROOF.md`; my earlier `4/(5 sqrt3)` was wrong and is fixed |

## B. Retiring rectangle worker (`supervisor/solve-six-colouring/FINDINGS.md`)

Re-verified from its own recorded data (`out/cover.json`) with independent exact `Fraction`
arithmetic, plus re-derivation of its lemmas.

| # | claim | grade | finding |
|---|---|---|---|
| B1 | interval lemma and the closed-cell criterion | valid for closed cells | as A2: not the criterion for a plane colouring |
| B2 | window bound: forced `=> |v| < 1 + D`, `D = sqrt(s^2+t^2)` | valid | re-derived: `dmin >= |v| - D`, `dmax <= |v| + D` |
| B3 | monotone box test (Lemma 5) + 7-clique certificate (Lemma 4) | valid | I add: `dmax^2` is *strictly* increasing in `s,t` (both coefficients `(abs(p)+1)^2 >= 1`), so a box certified with `dmax^2 >= 1` at the lower corner is strictly forced inside |
| B4 | counts: 1401 boxes; 681 certified | **valid** | recomputed exactly: both match |
| B5 | all 681 witnesses are genuine 7-cliques | valid | 14301 witness pairs re-checked, **0** failures under the closed criterion and **0** under the open-box (strict-inside) criterion |
| B6 | "the 1401 boxes cover the entire open region `{0 < s <= t, s^2+t^2 < 1}`" | **overbroad** | no box has `i = 0`, so `0 < s <= 1/60` is **not covered at all**, and `s = 1/60` lies in no box. Confirmed on valid probes `(s,t) = (1/120, 1/2)`, `(1/60, 1/2)`, `(1/200, 99/100)`: all in the family, none covered. The "`i = 0` handled by the infimum" remark justifies a monotone bound, not coverage. Their `i >= 26` theorem is unaffected because it is stated only for the band it certifies. |
| B7 | "tangency counts: `dmin = 1` or `dmax = 1` implies forced" | **overbroad** | 174 of 14301 witness pairs sit exactly on an equality at a box corner, so those boxes certify the no-go on the **open** box only; the theorem as stated silently includes the grid walls `60s in Z` or `60t in Z`, which are not certified |
| B8 | "`s^2+t^2 = 1` excluded: the cell contains a unit segment, so no cell colouring is proper" | **overbroad, convention-dependent** | under the half-open rule `[is-s/2, is+s/2) x [jt-t/2, jt+t/2)` the two opposite corners are *not* in the same cell, so this parameter is admissible; under closed cells it is not. Not needed for their theorem |
| B9 | "boundary values are irrelevant: any assignment on edges keeps properness" (§3) | **unverified** | a boundary point must be coloured avoiding the colours of all cells meeting the unit circle about it, and avoiding other boundary points at distance `1`; no argument is given. Not needed for the no-go direction; needed for any positive use of their CSP |
| B10 | K_7 diameter limit `B >= (sqrt7-1)A`, hence `D >= 1 - 2/sqrt7 = 0.24407` | **valid** | re-derived independently (isodiametric + Barbier + disjoint disks): `6A^2 <= B^2 + 2AB`. Consequence for the honeycomb: no 7-clique below `a = 0.12204` |
| B11 | the residual region (`s` small, or `s << t`) is genuinely open | valid | agrees with my §5 |
| B12 | "one implementation, self-checked against a `Fraction` reference; not independently re-implemented" | honest, and now partially remedied | B4/B5/B10 above are an independent second path for the arithmetic and the witness claims |

## C. Retiring graph worker (`supervisor/solve-graphs/REPORT.md`)

Nothing here is used by the cell theorem; recorded so the record is not lost.

| # | claim | grade | finding |
|---|---|---|---|
| C1 | exhaustive colouring counts for diamond / Moser spindle / double-lens (table incl. `chi = 3` diamond, `chi = 4` otherwise) | **valid as pilot data** | consistent with the classical facts; exact arithmetic construction is plausible; not re-run here |
| C2 | diamond tip relation: at `k = 3` forced equal, at `k >= 4` both relations occur (counts 6/0, 24/24, 60/120, 120/360) | **valid as pilot data** | the count is a straightforward computation on a 4-vertex graph; the mechanism is correct *pointwise* |
| C3 | "**hence** every graph built from diamonds and unit edges is at most 4-chromatic" | **unverified / overbroad** | does not follow: a pointwise "not forced" relation says nothing about the global chromatic number, and no construction grammar is stated (which segments may be completed, how closures glue, whether repeated completion stays finite). The Moser spindle is itself such a graph and is 4-chromatic, so the pilot is consistent but the general claim is unsupported. **Not inherited.** |
| C4 | `U(U(C1,C2)) = (C1,C2)` on the spindle closing edge (lens stack is an involution) | unverified pilot | single implementation; retain as an observation, not as a lemma |
| C5 | a finite 6-chromatic unit-distance graph exists (no-5-colouring + de Bruijn–Erdos compactness + algebraic coordinates) | **valid** | standard compactness for graph colouring; the witness is not exhibited and no bound on its size follows |
| C6 | smallest known 5-chromatic graphs have hundreds of vertices (de Grey 1581, Heule 826, later ~509) | unverified here | quoted from memory of the literature in that report; not a claim I rely on |

## D. Net effect

One cell-family no-go survives, with a corrected criterion, a corrected parameter range, and an
exact forced-set description (`CELL-NOGO-v2.md` Theorem 2). Nothing in the three sources bounds
`chi(R^2)`; the only statements with any bearing on a six-colouring are negative statements about
cell-constant families whose cell diameter exceeds `0.5547` (honeycomb) or which lie in the
rectangle worker's certified open boxes with `s > 1/60`.
