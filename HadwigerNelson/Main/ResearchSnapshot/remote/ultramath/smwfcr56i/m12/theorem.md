# The hexagonal-cell (Isbell–Hadwiger) method cannot six-colour the plane

**Sharp constants, three explicit 7-cliques, and machine-checked certificates.**

All numbers below are exact; every decision procedure used is exact arithmetic in
`Q(sqrt 3)` or an exactly specified integer computation.  The verification scripts are
`hexagon_exact.py`, `cellsat.py`, `certs_all.py`, `certify.py`, `intervals.py` in this directory
(log: `verify.log`).

---

## 0. Setting

Fix `d > 0` and let `omega = e^{2 pi i/3} = -1/2 + i sqrt3/2`.  Put

```
Lambda_d = d * Z[omega] = d * { a + b omega : a,b in Z }
```

the triangular lattice of **minimum distance `d`**.  Its Voronoi cell `H` (translate `H_p = p + H`)
is the regular hexagon with

* circumradius `d/sqrt3`, apothem `d/2`, **diameter `2d/sqrt3`**,
* vertices in the six *hole* directions `pi/6 + k pi/3`,
* edge normals (unit vectors) `1`, `omega`, `1+omega`.

The cells `H_p` (`p in Lambda_d`) tile the plane.

**Family `Hex_d`.**  A colouring `c : R^2 -> {1,...,k}` belongs to `Hex_d` if `c` is constant on
the interior of every cell `H_p`.  Equivalently `c = phi o p` where `p(x)` is *some* nearest lattice
point of `x` (any tie-breaking rule) and `phi : Lambda_d -> {1,...,k}`.  This is exactly the family
of colourings produced by the hexagonal construction for `chi(R^2) <= 7`
(Isbell; Hadwiger; used in section 1 of the attached paper with `r = 2/5`, `d = sqrt3 r = 2 sqrt3/5`).

For `v in Lambda_d \ {0}` say `H_0` and `H_v` **strongly conflict** if there are `x in int H_0`,
`y in int H_v` with `|x-y| = 1`.

---
## 1. Results

**Theorem 1 (no six colours, large cells).**  For every `d > sqrt(3/13) = 0.4803844...` and
every `c in Hex_d` with at most 6 colours, `c` is not proper: there exist `x,y` with
`|x-y| = 1` and `c(x) = c(y)`.

**Theorem 2 (no six colours, a second range).**  The same holds for every
`d` with `sqrt(3/25) = 0.3464101... < d < sqrt3/4 = 0.4330127...`.

**Theorem 3.**  The same holds for `sqrt(3/28) = 0.3273268... < d < 1/3`.

**Theorem 4 (sharp seven-colouring).**  Let `Phi : Lambda_d -> Z/7`, `Phi(a + b omega) = a + 2b mod 7`
and `c = Phi o p`.  Then `c` is proper for every `d` with
`sqrt(3/7) = 0.6546536... < d < sqrt3/2 = 0.8660254...`, and `c` is improper for every `d < sqrt(3/7)`.
In particular `c` is proper for the paper's `d = 2 sqrt3/5 = 0.6928203...`; the exact inequality is
`d^2 = 12/25 > 3/7`, i.e. `84 > 75`.

**Theorem 5 (coset colourings: the exact failing inequality for `k = 6`).**  For a coset colouring
by an index-`k` sublattice `Lambda'` of `Lambda_d` the standard sufficient condition is
`lambda_1(Lambda') > 1 + 2d/sqrt3`; it can be met for some `d < sqrt3/2` **iff** `M(k)^2 > 16/3`,
where `M(k)^2` is the largest squared minimum norm of an index-`k` sublattice of `Z[omega]`.
`M(k)^2 = 1,1,3,4,3,4` for `k = 1,...,6`, and `M(7)^2 = 7`: the first success is `k = 7`.
For `k = 6` the failing inequality is `2d > 1 + 2d/sqrt3`, i.e. `d > (3+sqrt3)/4 = 1.1830127...`,
which contradicts the necessary `d < sqrt3/2 = 0.8660254...`.

**Theorem 6 (machine-checked extension to small cells).**  For every `d` in
`(0.21651, 0.86603)` **except** the interval `(0.24019, 0.25000)`, an explicit finite subgraph of the
conflict graph (described in section 7) is not 6-colourable; hence no `c in Hex_d` with 6 colours is
proper there.  Table in section 6; certificates regenerate from `cellsat.py`.

---
## 2. The conflict criterion

Write `2H = H - H`.  In units `d = 1`, `2H` is the hexagon with apothem `1`, circumradius `2/sqrt3`
and vertices `(+-1, +-1/sqrt3)`, `(0, +-2/sqrt3)`; it contains the closed unit disc.

**Lemma 2.1.**  Let `v in Lambda_d \ {0}` and put
`delta_min(v) = dist(v, 2H)`, `delta_max(v) = max_{w in 2H} |v-w|` (in units `d = 1`).
Then

```
{ |x-y| : x in int H_0, y in int H_v } = ( d*delta_min(v) , d*delta_max(v) ) .
```

*Proof.*  `dist(H_0,H_v) = dist(v, H-H) = dist(v,2H) = delta_min(v)`, and for centrally symmetric
convex `H`, `max{ |x-y| : x in H_0, y in H_v } = max_{w in 2H} |v-w| = delta_max(v)`.
The map `(x,y) |-> |x-y|` is continuous on the connected set `int H_0 x int H_v`, so its image is an
interval; its infimum is `delta_min` (approached by interior points, as the closed cells are the
closure of their interiors) and its supremum is `delta_max`.  Hence the image is
`(d delta_min, d delta_max)` (possibly with left end `0`). `square`

**Corollary 2.2 (strong conflict criterion).**  `H_0` and `H_v` strongly conflict iff
`d delta_min(v) < 1 < d delta_max(v)`.

**Corollary 2.3 (crude annulus).**  If `1/d - 1 < |v| < 1/d + 1` (with `|v|` in lattice units), then
`H_0` and `H_v` strongly conflict.
*Proof.*  `B(0,1) subset 2H` gives `delta_min(v) <= |v| - 1` and `delta_max(v) >= |v| + 1` for
`|v| >= 1`; insert into 2.2. `square`

---
## 3. Exact shell constants

For a shell `n = |v|^2`, `delta_min, delta_max` need not be a function of `n` alone: the script
checks all shells with `n <= 60` and finds a single split, at `n = 49` (the vectors `(+-7,0)` have
`delta_min^2 = 36`, the others `103/3`).  **Every shell used below has `n <= 31`**, and all of those
are unsplit (the check is exact and covers `n <= 48`; the interval computation of section 7 uses every
lattice vector individually, not one representative per shell).  For `d = 1`:

| `n = |v|^2` | `delta_min^2` | `delta_max^2` | strong conflict iff |
|---|---|---|---|
| 1 | 0 | 13/3 | `d > sqrt(3/13)` |
| 3 | 1/3 | 25/3 | `sqrt(3/25) < d < sqrt3` |
| 4 | 1 | 28/3 | `sqrt(3/28) < d < 1` |
| 7 | 7/3 | 43/3 | `sqrt(3/43) < d < sqrt(3/7)` |
| 9 | 4 | 49/3 | `sqrt(3/49) < d < 1/2` |
| 12 | 16/3 | 64/3 | `sqrt(3/64) < d < sqrt(3/16)` |
| 13 | 19/3 | 67/3 | `sqrt(3/67) < d < sqrt(3/19)` |
| 16 | 9 | 76/3 | `sqrt(3/76) < d < 1/3` |

**Lemma 3.1.**  The table is correct.

*Proof (two representative cases; the rest are the same computation, and all eight are re-done in
exact `Q(sqrt 3)` arithmetic by `hexagon_exact.py`).*
`2H` is the intersection of the three slabs `|<x,u>| <= 1`, `u in {1, omega, 1+omega}`, with the six
vertices listed above; `delta_max` is attained at a vertex.

* `n = 1`, `v = (1,0)`: `v` lies on the edge `x = 1` of `2H`, so `delta_min = 0`; the farthest
  vertices are `(-1, +-1/sqrt3)`, at squared distance `4 + 1/3 = 13/3`.
* `n = 7`, `v = 2 - omega = (5/2, -sqrt3/2)`: the nearest point of `2H` is the vertex
  `(1,-1/sqrt3)`, giving `delta_min^2 = (3/2)^2 + (sqrt3/2 - sqrt3/3)^2 = 9/4 + 1/12 = 7/3`; the
  farthest vertex is `(-1, 1/sqrt3)`, giving `delta_max^2 = (7/2)^2 + (5 sqrt3/6)^2 = 49/4 + 25/12 = 43/3`. `square`

---
## 4. Three explicit 7-cliques  (Theorems 1, 2, 3)

Since the cells are monochromatic in `Hex_d`, **seven pairwise strongly conflicting cells force seven
colours**: if two of them had equal colour, Lemma 2.1 would give a monochromatic unit pair.  So it
suffices to exhibit, for each `d`-range, seven lattice points with all `21` pairwise distances in a
conflicting shell.  The three cliques (indices in the basis `1, omega`):

```
C1 = { (0,0), (1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,-1) }     pairwise |v|^2 in {1,3,4}
C2 = { (-1,0), (0,-1), (0,2), (1,1), (2,0), (2,3), (3,2) }       pairwise |v|^2 in {3,9,12}
C3 = 2*C1 = { (0,0), (±2,0), (0,±2), (2,2), (-2,-2) }            pairwise |v|^2 in {4,12,16}
```

(The `21` pairwise squared norms are exactly the sets shown; the script verifies all three cliques
factor by factor.)  Intersecting the conflict intervals of Lemma 3.1:

* `C1`: `max` of the lower bounds `sqrt(3/13)`, and `min` of the upper bounds
  `min(sqrt3, 1) = 1`; so the clique is a 7-clique for `sqrt(3/13) < d < 1`.  Together with the
  separate observation that for `d >= 1` a single cell has diameter `2d/sqrt3 > 1` and hence contains
  an interior unit pair (so no `Hex_d` colouring is proper), this is Theorem 1: **every
  `d > sqrt(3/13)`**.
* `C2`: `max(sqrt(3/25), sqrt(3/49), sqrt(3/64)) < d < min(sqrt3, 1/2, sqrt(3/16))`, i.e.
  `sqrt(3/25) < d < sqrt3/4` — Theorem 2.
* `C3`: `max(sqrt(3/28), sqrt(3/64), sqrt(3/76)) < d < min(1, sqrt(3/16), 1/3)`, i.e.
  `sqrt(3/28) < d < 1/3` — Theorem 3.

---
## 5. The sharp seven-colouring (Theorem 4)

`Phi(a + b omega) = a + 2b mod 7` is a surjective homomorphism `Z[omega] -> Z/7` with
`Phi(2 - omega) = 2 - 2 = 0`, so `ker Phi = (2-omega) Z[omega]`, an index-7 *similar* sublattice
(`|2-omega|^2 = 7`).  Moreover `a + 2b = 0 (7)` implies

```
|a + b omega|^2 = a^2 - ab + b^2 = (-2b)^2 + 2b^2 + b^2 = 7 b^2 = 0  (mod 7),
```

so **every nonzero element `v` of `ker Phi` has `|v|^2 >= 7`** (attained at `v = 2-omega`).
Two distinct cells of equal colour therefore differ by `v` with `|v|^2 in {7, 21, 28, ...} d^2`.

* If `d > sqrt(3/7)` and `|v|^2 = 7 d^2`: by Lemma 3.1, `d^2 delta_min^2 = 7 d^2/3 > 1`, so there is
  no conflict.
* If `|v|^2 >= 21 d^2`: `delta_min(v) >= |v| - 2/sqrt3`, so
  `d delta_min >= d(sqrt21 - 2/sqrt3) = 3.4279... d > 3.4279 * 0.65465 > 1`: no conflict.
* Cells are convex sets of diameter `2d/sqrt3 < 1`, so no unit pair lies in one cell.

Hence `c` is proper.  Conversely, for `d < sqrt(3/7)` the two cells `H_0` and `H_{2-omega}` (same
colour) strongly conflict, since `d^2 delta_min^2 = 7d^2/3 < 1 < 43 d^2/3`, so `c` is improper.
(The borderline `d = sqrt(3/7)` is exactly where the closed cells' distance equals `1`; we make no
claim there.  For `d <= sqrt(3/43) = 0.2641` use Corollary 2.3 instead: the kernel's norm set has all
consecutive gaps `< 2` — finite check to norm `200` in the script, and the tail bound
`sqrt7 (b+1)/(b sqrt3) < 2` for `b >= 7` — so the annulus `(1/d - 1, 1/d + 1)` always meets it.)
`square`

**Remark.**  The paper's sufficient condition `(sqrt21 - 2) r > 1` is equivalent to
`d > 0.67062...`; Theorem 4 sharpens it to `d > sqrt(3/7) = 0.65465...`.

---
## 6. Coset colourings and the `k = 6` failing inequality (Theorem 5)

For a sublattice `Lambda'` of index `k` and `phi` the coset map, two same-coloured cells differ by
`v in Lambda' \ {0}`, and `|x - y| >= |v| - 2d/sqrt3`.  So

```
lambda_1(Lambda') > 1 + 2d/sqrt3  ==>  the coset colouring is proper.
```

Writing `lambda_1 = M d` with `M` the minimal norm of the sublattice in units `d = 1`, a suitable
`d < sqrt3/2` exists iff `M > 2/sqrt3 + 2/sqrt3 = 4/sqrt3`, i.e. `M^2 > 16/3`.  Enumerating the HNF
forms `(a,b,c)` with `ac = k`, `0 <= b < c`, and reducing each basis exactly (Gauss reduction with
rational arithmetic) gives

```
 k :  1  2  3  4  5  6  |  7  8  9 10 11 12 13 14 15 16 ...
M^2:  1  1  3  4  3  4  |  7  7  9  7  7 12 13 12 13 16 ...
```

The first `k` with `M(k)^2 > 16/3` is `k = 7`.  For `k = 6`, `M(6)^2 = 4` and the criterion becomes
the failing inequality

```
2d > 1 + 2d/sqrt3   <=>   d > (3 + sqrt3)/4 = 1.1830127...  >  sqrt3/2 = 0.8660254...,
```

which is incompatible with the cell-diameter requirement `2d/sqrt3 < 1`.  Hence **no six-colouring of
this kind exists, and seven is optimal for the method** (Theorem 4 attains it).

---
## 7. Machine-checked extension to small cells (Theorem 6)

For `d <= sqrt(3/13)` the cliques above disappear (the shell `|v|^2 = 1` stops conflicting), and the
conflict graph becomes a "thick shell" graph.  The conflict graph depends on `d` only through its
**shell set** `S(d) = { |v|^2 : H_0 and H_v strongly conflict }`, which is constant between the finitely
many critical values `d = 1/delta_max(n)`, `1/delta_min(n)`.  On each such interval we take a window
`W_K = { v : |v|^2 <= K }`, form the exact conflict graph on `W_K`, and refute 6-colourability with
`cadical`.  Result (window `|V|`, edges `|E|`, exact interval on which this graph is a subgraph of the
conflict graph):

| `d` tested | shell set | window `|V|` | `|E|` | 6-colourable | interval covered |
|---|---|---|---|---|---|
| 0.217 | {12,13,16,19,21,25,27,28,31} | 85 | 1500 | no | (0.21651, 0.22177) |
| 0.235 | {12,13,16,19,21,25,27,28} | 91 | 1494 | no | (0.22177, 0.24019) |
| 0.250 | {9,12,13,16,19,21} | 85 | 1140 | no | (0.25000, 0.26414) |
| 0.275 | {7,9,12,13,16,19,21} | 43 | 498 | no | (0.26414, 0.28475) |
| 0.300 | {7,9,12,13,16,19} | 43 | 438 | no | (0.28475, 0.31109) |
| 0.320 | {7,9,12,13,16} | 61 | 648 | no | (0.31109, 0.32733) |
| 0.333 | {4,7,9,12,13} | 37 | 336 | no | (0.33333, 0.34641) |
| 0.400 | {3,4,7,9,12} | 37 | 336 | no | (0.39736, 0.43301) |
| 0.460 | {3,4,7,9} | 37 | 297 | no | (0.43301, 0.48038) |

Together with Theorems 1–3 (which
cover `(0.32733, 0.33333)`, `(0.34641, 0.43301)` and `(0.48038, 0.86603)`) this proves the claim of
Theorem 6:  every `d in (0.21651, 0.86603)` outside `(0.24019, 0.25000)` is excluded (a certificate at
`d = 0.245` for the missing window did not finish within 140 vertices).  The excluded
window sizes are 37–91 vertices, i.e. tiny; the remaining gap and the range below `0.2165` we did not
settle (there the required windows exceed 140 vertices and the solver did not finish).

Minimal witnesses found by greedy vertex deletion: 7 vertices at `d = 0.4` (a 7-clique: the second
clique `C2` of section 4), 25 vertices at `d = 0.46`, 27 at `d = 1/3`, 41 at `d = 0.3`, 65 at `d = 0.25`.
So for `d = 1/3` and `d = 0.46` the obstruction is not a clique.

---
## 8. What is *not* proved here

1. Nothing is claimed about colourings that are not constant on the hexagonal cells, and nothing is
   claimed about `chi(R^2)` itself.  This note is a no-go result for one construction family — the
   only family that produces the known upper bound `chi(R^2) <= 7`.
2. Whether some other (non-cell) construction can six-colour the plane is untouched.
3. The interval `(0.24019, 0.25000)` and `d < 0.21651` are not covered by Theorem 6, and Theorem 1–3
   do not reach them.  The exact conflict graph there is a thick-shell graph that we could not exclude
   with windows of <= 140 vertices.
4. At `d = sqrt(3/7)` the colouring of Theorem 4 is marginal and not decided.

---
## 9. Reproduce

```
python3 hexagon_exact.py      # shell constants, 21 clique pairs, M(k) table, Thm 4 checks
python3 numeric_check.py      # independent floating-point sanity check of the colouring formula
python3 certs_all.py          # SAT certificates for the nine listed d (~10-20 min; --force to redo)
python3 certify.py            # minimal witnesses by greedy vertex deletion
python3 intervals.py          # exact d-intervals on which each certificate applies (all vectors)
python3 summary.py            # clique intervals
```
`cadical` is the SAT solver used; `certificates.json` stores the windows.
