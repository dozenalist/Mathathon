# One sharp exact problem at `a = 1/5`: forced offsets, endpoint exceptions, and the periodic bound

Certificate: `forced_a1_5.py` -> `forced_a1_5.out` (exact `Q(sqrt3)`, one process, runs in < 1 s).
Corrections to `CELL-NOGO-v2.md` are applied there (§1 statement, §4 scope of the diameter lemma).

## 0. Carried corrections

* **Interiors are not a partition.** The cells of a tiling are closed convex sets with pairwise
  disjoint interiors whose union is *dense*; the interiors omit the 1-skeleton. Every skeleton point
  belongs to the boundary of all cells meeting there and needs an ownership rule. Hence the strict
  criterion of `CELL-NOGO-v2.md` Lemma 1(1) is available (it uses only interior points) and its
  case 2 (equality endpoints) is rule-dependent.
* **The `K_7` diameter lemma closes only the clique route, and only below `D = 0.24407`.** For the
  honeycomb that is `a < 0.12204`; on `[0.12204, 1/sqrt13)` a 7-clique is not excluded (none found),
  and non-clique 7-chromatic subgraphs are untouched at every `a`.

## 1. The parameter, and why `1/5`

`a = 1/5` is **not** covered by any result I have found or produced: `a = 1/5 < 1/sqrt13 = 0.27735`
lies strictly inside the open regime. It is rational, so every length below is exact in `Q(sqrt3)`,
and it is exactly the tangency value of one ring (`25 a^2 = 1`), which forces the endpoint
bookkeeping to be done properly instead of hidden.

Cell data: circumradius `a = 0.2`, inradius `a sqrt3/2`, **cell diameter `D = 2a = 0.4`**, lattice
spacing `s = a sqrt3 = 0.346410`, `|v|^2 = 3 a^2 N(p,q)` with `N = p^2+pq+q^2` the Eisenstein norm.

## 2. The exact forced set

Strict criterion (`dmin < 1 < dmax`), computed per vector over all 84 lattice vectors with
`N <= 24`:

| ring `N` | `abs(v)` | forced / total | note |
|---|---|---|---|
| 1 | 0.3464 | 0 / 6 | `dmax^2 = 13a^2 = 0.52 < 1` |
| 3 | 0.6000 | **0 / 6** | **endpoint exception: `dmax^2 = 25a^2 = 1` exactly** |
| 4 | 0.6928 | 6 / 6 | |
| 7 | 0.9165 | 12 / 12 | |
| 9 | 1.0392 | 6 / 6 | |
| 12 | 1.2000 | 6 / 6 | |
| 13 | 1.2490 | 12 / 12 | |
| 16 | 1.3856 | **0 / 6** | `dmin >= 1` although `abs(v) < 1+D = 1.4` |
| 19 | 1.5100 | 0 / 12 | `abs(v) > 1+D` |

    F_{1/5} = { v : N(v) in {4, 7, 9, 12, 13} },   |F| = 42.

**Endpoint exceptions saved.** The six tangency vectors, all of ring 3 and all with `dmax^2 = 1`
exactly, are `(1,1), (2,-1), (1,-2), (-1,-1), (-2,1), (-1,2)`. By the weak (closed-cell) criterion
they *are* forced; by the strict criterion they are **not**, and their unit-distance pair is realised
only at tiling vertices (the maximum of a convex function over the hexagon `2V` is attained at a
vertex, and a vertex of `V-V` decomposes into vertices of `V`). Since a vertex belongs to exactly one
cell under any ownership rule, a colouring may legitimately give two tangent cells the same colour —
but it then owes a boundary argument. There are **no** `dmin^2 = 1` vectors at this parameter.

So the allowed same-colour offsets are exactly `N in {1,3} ∪ {N >= 16}`.

**Structural consequence (clusters).** In any proper colouring constant on cell interiors:

* two same-coloured cells at `N in {1,3}` are at distance `<= sqrt3 s = 0.6`;
* hence every colour class splits into clusters — maximal sets of cells pairwise at `N in {1,3}`;
* a cluster has **at most 4 cells**: the seven points of `{0} ∪ N(0)` form `K_7` minus the three
  antipodal pairs, so a clique picks at most one of each pair plus `0`;
* distinct clusters are pairwise at distance `>= 4s = 1.3856` (their differences have `N >= 16`).

Density does **not** settle six colours here: a colour class needs `(2/(sqrt3 s^2))/6 = 1.60`
cells per unit area, while disjoint `0.6928`-disks around clusters of size `<= 4` bound a class by
`4/pi(0.6928)^2 = 2.65`. The gap `[1.60, 2.65]` is exactly why the problem stays open; refine it if
you want a density proof.

## 3. Periodic colourings: index `>= 16`, attained

A colouring that is `Lambda_p`-periodic (`Lambda_p` a sublattice of index `d`) must have
`F ∩ Lambda_p = ∅`, because cells in one coset share a colour. All `sigma_1(d)` sublattices of each
index `d <= 25` were enumerated (upper Hermite normal form `<(a,b),(0,c)>`, `ac = d`, `0 <= b < c`):

    d = 2 .. 15 : 0 avoiding sublattices
    d = 16      : 1  -> <(4,0),(0,4)> = 4Z^2
    d = 17, 18  : 0

**Theorem (periodic bound).** At `a = 1/5` every periodic proper colouring has period index
`>= 16`, and 16 is attained by `4Z^2`.

*Proof.* `N` is multiplicative and `N(k lambda) = k^2 N(lambda)`, so a sublattice containing
`lambda` contains `2 lambda`, `3 lambda`, ... and avoidance needs `N(lambda)`, `4N(lambda)`,
`9N(lambda)` all outside `F_N = {4,7,9,12,13}`. `n = 1` gives `4 in F_N`, `n = 3` gives `12 in
F_N`, and `n in {4,7,9,12,13}` are forbidden themselves, so `N(lambda) >= 16` for every nonzero
`lambda`. The packing bound `covolume >= (sqrt3/2) min abs(lambda)^2` then gives
`index = min abs(lambda)^2/(3a^2) = min N >= 16`. `4Z^2` has index 16 and all its norms are
multiples of 16, so it meets `F` in nothing. ∎

The same argument at `a = 2/5` (`F_N = {1,3,4}`, so `n >= 7`, index `>= 7`) is **attained by the
paper's seven-colouring**, whose period is `<(1,3),(0,7)>` of index 7 — an independent confirmation
that the method reproduces the known optimum (and it caught a bug: a lower-triangular HNF
enumeration misses six of the eight index-7 sublattices, including that one, and wrongly reported
`8` as the minimum).

**Consequence for a six-colouring at `a = 1/5`:** no period of index `< 16` can carry one, so each
colour class is a union of at least three cosets, hence clusters of size `<= 4` repeated,
`>= 1.3856` apart, in a lattice-periodic pattern. That is a much smaller search space than "all
colourings", and it is where a bounded search should start — not at small periods.

## 4. What a bounded periodic search would and would not establish

* **UNSAT** for a specific period sublattice `Lambda_p` (a finite graph on `d` cosets, connection set
  `F mod Lambda_p`, `d >= 16`): rules out colourings periodic with that exact period. It is *not* a
  statement about non-periodic colourings, and by itself says nothing about `chi(R^2)`.
* **SAT** gives an explicit periodic labelling with `F ∩ (same-colour differences) = empty`, which is
  a proper colouring **of the cell interiors only**. It is not yet a colouring of the plane: one must
  then (i) fix an ownership rule on the 1-skeleton, (ii) check every skeleton point against all
  points at distance exactly `1`, and (iii) check the tangency pairs of ring 3 — same-coloured
  tangent cells are permitted by the interior criterion and must be shown compatible with the rule.
  Steps (i)–(iii) are exact distance checks on a compact fundamental domain, hence finite, but they
  are not automatic and are not done here.
* The inherited rectangle certificates (`supervisor/solve-six-colouring`) stay restricted to their
  verified **open boxes** `s > 1/60` off the walls `60s, 60t in Z`; nothing from them is reused here.

## 5. State

Exact and closed at `a = 1/5`: the forced set, the endpoint exception list, the cluster structure,
and the periodic index bound `16` (proof + certificate). Open: six-colourability at `a = 1/5`, for
non-periodic colourings and for periods of index `>= 16`. Nothing here bounds `chi(R^2)`.
