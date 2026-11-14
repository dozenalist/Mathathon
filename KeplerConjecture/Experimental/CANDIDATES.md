# Three candidate mechanisms

Role E (Experimental). One candidate per assigned route. Each is stated so that C can
evaluate it and X can attack it. Global normalisation throughout: **unit spheres**,
centre separation `>= 2`, occupied-volume density, `sqrt(32) = 4 sqrt 2 = 5.656854249`
for FCC/HCP Voronoi volume, target `pi/sqrt(18) = 0.740480489693`. The Fourier
convention, where used, is `fhat(t) = int f(x) exp(-2 pi i <x,t>) dx` and the
CE volume factor is `4pi/3`.

Summary:

| id | route | status | headline |
| --- | --- | --- | --- |
| `K15-E1` | local correction / cluster averaging | criterion **PROVED**; block rule **R2' corrected**; transfer inequality `(T'-R2')` **OPEN, obstructed quantitatively** | replaces Hales's pointwise transfer by cluster averages; the dodecahedral deficit is real and must be repaid configuration-specifically |
| `K15-E2` | strengthened Fourier / 3-point hybrid | **SPECIFIED**, unevaluated, **blocked** on a three-point evaluator absent from my artifacts | 3-point bound plus kissing-type local-mass constraints; genuinely outside Li's obstruction |
| `K15-E3` | independent decomposition / Euler | **OBSTRUCTED** (source-documented) | pure Delaunay fails at the `(2,2,2,2,l,l)` simplex; quantified |

### Current status of `K15-E1` (updated)

- `K15-E001` cluster-averaged criterion: **PROVED** (conditional accounting lemma).
- `K15-E014` at most 12 centres in `[2, 2.09]`, **and** in `[2, 2.05]`: **PROVED**, with
  exact rational thresholds `23681/43681` and `881/1681`, margins `4.94e-04` and
  `1.85e-02`.
- `K15-E013` every Barlow stacking has exactly 12 centres in `[2, 2.09]`: **PROVED**.
- `K15-E032` block rule R2 disjointness: **corrected**, adjacency threshold `4.18`.
- `K15-E041` dodecahedral shortfall `1.385321873` (`2.04 %`): **PROVED**. Kills every
  per-cell-independent argument.
- `K15-E042` angular estimate `4.733968` vs required `5.665735`: **PROVED bound, insufficient**.
- `(T'-R2')` itself: **OPEN**. Best certified per-cell lower bound `4.733968`; best computed
  upper bound `8.167277`; required `5.665735`.

---

## K15-E1 — Cluster-averaged correction (local geometry, discharging)

**Auxiliary object.** A partition `Pi` of `Lambda` into clusters of diameter `<= D`, and a
correction `A : Lambda -> R`; corrected volume `c(v) = vol Omega(v) + A(v)`.

**Theorem.** `K15-E001` in `Experimental/LOCAL_CRITERION.md`: if (C1) bounded cluster
diameter, (C3) `c(v) >= 0`, (C4) `sum_{v in K} c(v) >= sqrt(32)|K|` for every `K in Pi`,
(C5) negligibility of `A`, then `delta(x,r,Lambda) <= pi/sqrt(18) + C/r`. **Proved.**
Strictly generalises Hales Def 3.2 / Lemma 3.3, which is the singleton partition.

**Normalisation.** Unit spheres, `sqrt(32)`. Under (C4) the quantity compared to `sqrt(32)`
is a cluster *average* of corrected cell volumes.

**Equality fixtures.** FCC: every Voronoi cell is a rhombic dodecahedron of volume
`sqrt(32)` exactly, so every cluster average equals `sqrt(32)` and (C4) is tight — good,
equality is attained, as it must be. HCP: every cell also has volume `sqrt(32)`, same
verdict. Barlow stackings: likewise cell volume `sqrt(32)` (all hexagonal-layer
stackings are FCC/HCP-local), so equality persists across the whole equality family and
(C4) cannot distinguish them. This is the correct behaviour: the criterion must not
prefer FCC over HCP.

**Computable evaluator.** Exact dodecahedron volume
`(15+7sqrt5)/4 * (4/sqrt(10+22/sqrt5))^3 = 5.5502910285155105` (verified to `1e-15`);
Voronoi volumes by half-space intersection or `scipy.spatial.Voronoi` with an explicit
saturing shell; cluster average over a named cluster. Script:
`Experimental/scripts/icosa_cluster_test.py`.

**Hardest unproved lemma.** `K15-E004`: for a canonical `Pi` of diameter `<= D` and
simple `A` (ideally `A = 0`), prove (C4) for *every* cluster in *every* saturated packing.
Known: it fails for `|K| = 1` with `A = 0` (icosahedral 13-cluster, `K15-E002`). Open:
whether a bounded `D` repairs it. `D = infinity` with `A = 0` is Kepler, so the whole
content is in the size of `D`.

**Initial counterexample test.** Icosahedral 13-cluster: centre cell `5.5503 < sqrt(32)`,
so it refutes the pointwise version; compute its 13-cluster average in the densest
available completion. Then: perturbed FCC, HCP, and the Barlow stackings. Also test the
degenerate two-point cluster (adjacent pair) and the tetrahedral 4-cluster.

**Known obstruction.** Section 3 of `LOCAL_CRITERION.md`: cell volumes are monotone
decreasing under adding centres, so no finite computation can *certify* (C4); sampling
can only refute. Candidate must therefore be discharged analytically, not numerically.

---

## K15-E2 — Three-point bound plus local-mass (kissing) constraints

**Why ordinary CE is excluded.** Li (Adv. Math. 460 (2024) 110043, arXiv:2206.09876v3,
Theorem 6.1) proves the optimal 3D CE centre-density bound exceeds `0.18398089 >
2^(-5/2)`. In occupied-volume units that is `(4pi/3)(0.18398089) > 0.770...`, above
`pi/sqrt(18)`. No choice of auxiliary function inside ordinary CE can be sharp. The
candidate must therefore add a constraint that is not implied by `f <= 0` off `B_2` and
`fhat >= 0`.

**Auxiliary object.** A pair `(f2, f3)`: `f2` radial with `f2 <= 0` off `B_2`,
`f2hat >= 0`; `f3` a positive-definite three-point kernel with the sign condition of
CDS22 Theorem 1.1 on the admissible triple set, truncated at radius `R`; **plus** the
local-mass constraint family
`mu(B(0,rho)) <= N(rho)` for `rho` in a finite set, where `mu` is the pair-correlation
measure and `N(rho)` the maximal number of centres of a separation-`>= 2` set inside a
ball of radius `rho` around a centre.

**Theorem (target form).** For any packing satisfying both the two-point and the
local-mass constraints, the density is at most the optimum of the resulting SDP, and that
optimum is `< 0.740480489`. The mechanism is legitimate because `N(rho)` is a property of
*every* packing (no periodicity, no crystallinity), so the constraint is universally
valid, unlike a lattice restriction.

**Normalisation.** Local mass counts *centres*, not volume; `N(2) = 12` is the kissing
number (Schutte–van der Waerden). For `rho <= 2`, `N = 0`. For `rho > 2` the exact value
is a "kissing with tolerance" question and must be certified, not guessed.

**Equality fixtures.** FCC and HCP both attain `N(2) = 12` contacts per centre; any
hexagonal-layer stacking does. So the local-mass constraint at `rho = 2` is tight on the
whole equality family, which is required for the bound to be able to reach
`pi/sqrt(18)`. A constraint that excluded HCP would be wrong.

**Computable evaluator.** Reuse C's `(f2, f3)` SDP evaluator; add the linear rows
`mu(B(0,rho_i)) <= N(rho_i)`. Objective in occupied-volume density = `(4pi/3) *
center_density`. Report both normalisations plus the gap to `0.740480489`.

**Hardest unproved lemma.** Two, in order of difficulty: (a) the exact local-mass
function `N(rho)` for `rho` in `(2, 3]` for arbitrary packings — a tolerance version of
the kissing problem; (b) that the constrained SDP optimum actually falls below
`pi/sqrt(18)`. (b) is decidable by computation; (a) is not, and without (a) the
constraint rows are unproved.

**Initial counterexample test.** Barlow stackings: they have the same cell volumes but
*different* contact statistics at `rho > 2`, so they are the sharpest test that the added
rows do not over-constrain. Also: the icosahedral 13-cluster, which has 12 contacts at
distance 2 but violates the FCC contact geometry at larger `rho`.

**Risk, stated plainly.** The published gap is `0.779747 -> 0.770271` from two-point to
three-point, and `0.770271 - 0.740480 = 0.029791` remains. Local-mass rows improved the
two-point bound by `0.006667` (DLOV14). A sum of these does not obviously reach the
target, which is why this candidate is rated *specified, unevaluated*, not promising.

---

## K15-E3 — Pure decomposition / Euler-characteristic route: OBSTRUCTED

**Intended object.** Delaunay decomposition of a saturated packing; density bounded by
`(4pi/3)` divided by the minimal average Delaunay-cell volume per vertex, with the number
of cells per vertex controlled by Euler's formula (tetrahedra `T`, octahedra `O`, with
`T - O = ... ` fixed by the Euler characteristic of the triangulation).

**Why it fails.** Hales, unabridged Section 2.1, records the refuting configuration: the
Delaunay simplex with edge lengths `(2,2,2,2,l,l)`, `l = sqrt(2(3+sqrt6)) = 3.301360...`,
the two long edges meeting at a vertex. It occurs as a Delaunay cell in a saturated
packing and its local density is `~0.78469`, "not only greater than `delta_oct`; it is
even greater than `delta_tet`". No per-simplex Delaunay bound can survive this, and a
grouped version is precisely Hales's "quarters".

**Our reproduction.** `Experimental/scripts/local_density_fixtures.py` (Monte Carlo,
status `TESTED_FINITE`) gives, in unit-sphere normalisation: regular tetrahedron edge 2
`0.77898` (source `~0.7797`), half-octahedron `0.72243` (source `delta_oct ~ 0.72`),
Hales extremal simplex `0.78317` (source `~0.78469`); Monte Carlo standard error `~0.001`,
so the extremal value is consistent with the source but not resolved to five digits.

**Verdict.** Route closed in its pure form by a source-documented configuration that we
have independently reproduced to Monte Carlo accuracy. Recorded so it is not re-attempted.
A repair exists (group simplices, aggregate volumes) but that repair is Hales's
composition of standard regions, so it is not an independent route.

---

## Constraints checked across all three

- **No global crystalline order is assumed** in `K15-E1` or `K15-E2`. `K15-E1`'s (C4) is a
  local statement quantified over clusters of an arbitrary saturated packing; `K15-E2`'s
  local-mass rows hold for every packing.
- **The dodecahedral obstruction** is fatal to pointwise arguments (exact fixture,
  `K15-E002`) and is *not* fatal to `K15-E1` by construction, since averaging is exactly
  the compensation the dodecahedral witness requires. That is `K15-E1`'s reason to exist.
- **The equality family** FCC / HCP / Barlow stackings has constant cell volume `sqrt(32)`
  in all members, so any criterion that is tight on FCC and not on HCP is defective. All
  three candidates are checked against this.
