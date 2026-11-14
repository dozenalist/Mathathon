# Response to K15-REVIEW-0608-C — a genuinely nonvacuous cut/flow fixture

Author: Computation (role C). Branch `kepler15/comp-01a1d8c0`. Receipt
`2026-11-14T14:28:52Z`. Source at receipt `bf7998c`. Ultramath is ON; **no swarm was run** (the
review forbids `ultramath_start`).

## 0. What was asked, and what this is

The review asked for "a genuinely nonvacuous 3-D cut/flow fixture with some positive `b`, explicit
legal packing coordinates, exact or rigorous volume enclosures, all boundary/periodic conventions
and an evaluated cut or feasible flow", from a dense local-cell family. That is what §1–§2 are. The
fallback (the engine's completeness assumptions, and the two-site congruence) is §3–§4, and both
came out as theorems rather than as caveats.

## 1. The fixture: a rational dense shell

**Construction.** A central vertex at the origin, and twelve neighbours on an icosahedral shell of
radius `2.0005`, every coordinate rounded to a rational with denominator dividing `10⁶`; period `8Z³`;
thirteen points per cell. The central cell is a slight deformation of the regular dodecahedron, hence
smaller than the Kepler cell.

**Coordinates** (exact; each denominator divides `10⁶`; the origin is the thirteenth point):

```
  (0, 42069/40000, 1701727/1000000)    (42069/40000, 1701727/1000000, 0) 
  (1701727/1000000, 0, 42069/40000)    (0, 42069/40000, -1701727/1000000)
  (42069/40000, -1701727/1000000, 0)   (-1701727/1000000, 0, 42069/40000)
  (0, -42069/40000, 1701727/1000000)   (-42069/40000, 1701727/1000000, 0)
  (1701727/1000000, 0, -42069/40000)   (0, -42069/40000, -1701727/1000000)
  (-42069/40000, -1701727/1000000, 0)   (-1701727/1000000, 0, -42069/40000)
```

(each divided by `10⁶`). They are the icosahedral directions `(0,±1,±φ)`, `(±1,±φ,0)`, `(±φ,0,±1)`
scaled to the shell radius and rounded; the file generates them, so the table is a display, not the
source of truth.

**Conventions, each checked rather than assumed:**

| | statement | how it is checked |
| --- | --- | --- |
| P1 | period `8Z³`, thirteen points per cell | by construction |
| P2 | edges at `R = 2.001`; the shell sits at `2.0005`, so exactly the twelve contacts are edges | `edges_within` enumerates lattice shifts exactly; the file also checks that `R = 2` would give **no** edges and a degree-zero centre (a different, vacuous failure) |
| P2′ | no wrap-around edge: diameter `4.002 < 8 − 3` | exact inequality |
| P3 | cells are Voronoi cells of the **infinite** packing, computed on the torus | the thirteen cells must sum to `|det L| = 512` exactly — the check that none was truncated |
| P4 | `b(v) = √32 − vol Ω(v)`, `√32` enclosed between two rationals | so `b(0) > 0` is the rational inequality `vol Ω(0) < SQ32_LO` |
| P5 | the numbers do not depend on the periodic identification | the central cell is computed at periods 8, 12 and 16 and is **identical** (`5.554454804528846` in all three); its circumradius `1.2587` is far inside the half-period `4` |

**Exact volumes** (rational, from vertex enumeration — see §3 for the certificate):

```
vol Ω(0) = 18842070507019013956653107809977422681162557 /
           3392244814316620265216629000000000000000000
         = 5.554454804529...          <  √32 = 5.6568542494...
vol Ω(shell) = 42.203795432955 each    (all twelve equal, by octahedral symmetry)
Σ vol = 512 exactly
```

Hence

$$b(0) = 0.102399444964... > 0, \qquad b(\text{shell}) = -36.547..., \qquad \textstyle\sum_v b = -438.46.$$

`b(0) > 0` makes the singleton cut bite; `Σ b < 0` means no vertex is pointwise infeasible, so the
fixture is a genuine test rather than a trivial refutation.

## 2. The evaluated cut, and a feasible flow

| quantity | value |
| --- | --- |
| `t*` over **all 8191** subsets (`b_lo` scan) | `0.008533287080295`, attained at `U = {0}` |
| bracket from the `b_hi` scan | `[0.008533287080295, 0.008533287080295]`, width `8.3·10⁻²³`, same maximizer |
| witness cut | `Σ_{U} b_lo = 0.102399444963534` over `|δ⁺({0})| = 12` |
| the condition fails for | every `Φ < 0.008533287080295` |
| a flow exists at | `Φ = 8.54·10⁻³` (verified exactly), and **not** at `8.53·10⁻³` |
| LP minimum capacity (bisection) | `0.008544898000`, i.e. **above** `t*` by `1.2·10⁻⁵` |

The LP minimum being above `t*` is the direction LP duality requires; the gap is `linprog`'s
tolerance, not a mathematical discrepancy (the same check appears in `audit_cut_flow_api.py`).

**What this is.** A legal packing of unit spheres with rational coordinates, on which the cut
condition provably fails below a positive capacity and holds at a slightly larger one. It **refutes**
capacities; a fixture cannot do more, and nothing here supports Kepler.

### 2.1 The nonvacuous window of the family

The shell radius `r` is a parameter: as `r` grows the central cell grows, so `b(0)` falls. The
crossing `vol Ω(0) = √32` cannot be located exactly (`√32` is irrational), so it is **bracketed with
rationals**, each step computing the exact volume:

| | `r` | `vol Ω(0)` |
| --- | --- | --- |
| `b(0) > 0` for | `r ≤ 4322279766317/2147483648000 = 2.01236…` | `5.656849616044` |
| `b(0) < 0` for | `r ≥ 1080569941629/536870912000 = 2.01236…` | `5.656856788442` |

the two endpoints differing by `9.3·10⁻¹¹`. At the last nonvacuous radius `t* = b(0)/12 = 3.9·10⁻⁷`;
at `r = 2.0005`, the fixture of §1, it is `8.53·10⁻³`.

**Cross-check against the irrational fixture.** The period-16 13-cluster has its shell exactly at
`r = 2` and `t* = 8.880·10⁻³`. The rational shell at `r = 2.0005` gives `8.533·10⁻³`, and the family
is monotone in `r`: the two independent constructions — one with irrational coordinates and an exact
dodecahedron, one rational with an exact polyhedron — agree in the direction and magnitude they must.

### 2.2 The patch minimum is exactly `t*`, with an explicit flow

The LP bisection of §2 gives `0.008544898` — above `t*` by `1.2·10⁻⁵`, which is `linprog`'s
tolerance and leaves the value of the patch minimum slightly open. It is not open: the **radial
flow**

$$\varphi(0,j) = \tfrac{1}{12}\,b(0) \quad\text{for all twelve shell vertices } j$$

is feasible at `Φ = t*` **exactly**. Its divergence at the centre is `12 · b(0)/12 = b(0)`, tight;
at each shell vertex it is `−b(0)/12 = −0.008533`, against `b = −36.547`, i.e. `36.54` of slack.
Since the singleton cut `{0}` fails for every `Φ < t*`, the patch minimum is **exactly** `t*`, with
witnesses on both sides. No floating point is involved in either verdict.

### 2.3 Why the shell cannot be filled further

The obvious way to raise `b(0)` is to add neighbours — a denser local cell. It cannot be done here,
and the reason is quantitative: the twelve directions are icosahedral, and the icosahedron's
**covering radius** is `37.377°` (the face centres). So any point at distance `2` from the origin is
within `37.377°` of some shell vertex, hence at distance at most

$$2\cdot 2\sin(37.377°/2) = 1.2817 < 2$$

from it — a legal thirteenth neighbour at radius `2` does not exist. (Sampling 200 000 directions
gives a covering radius of `37.315°`, and the exact value `37.377°` is the face-centre angle; the
bound only needs `≤ 37.377°`.) This is the kissing number `12` in the form that matters here: the
icosahedral shell is **closed**, so §2.1's window is the whole family and `b(0) = 0.1024` at
`r = 2.0005` is within `0.004` of the best this construction can do (`0.1066` at `r = 2` exactly,
the regular dodecahedron).

**The obstruction, stated:** in the dense-shell construction the deficit cannot be increased by
adding contacts, because the maximal kissing configuration already covers every direction. Raising
`b(0)` needs a *different* local geometry, not a fuller shell.

**And the arrangement is what decides**, not the contact count: the *cuboctahedral* 12-shell — which
is exactly FCC's neighbourhood — gives `b(0) = −0.004242` at the same radius `2.0005` and `−0.4350`
at `2.05`, and at radius exactly `2` its cell is the rhombic dodecahedron of volume `√32`, so `b = 0`
there and it can **never** be positive. Same twelve contacts, same distance, opposite verdict:

| shell | `r = 2.0005` | `r = 2` exactly |
| --- | --- | --- |
| icosahedral | `b(0) = +0.102399` | `+0.106563` (the dodecahedron) |
| cuboctahedral (= FCC) | `b(0) = −0.004242` | `0` exactly |

Nonvacuousness is a property of the **arrangement**.

### 2.3b Where the content sits, and convergence of the rational shell

Two checks that the fixture is what it claims.

**The content is exactly one inequality.** Over all 8190 subsets with a non-empty boundary, the
singleton is the unique maximizer and the gap to the second best is enormous:

| `U` | ratio | `Σ_U b` | boundary |
| --- | --- | --- | --- |
| `{0}` | **`+0.008533287080295`** | `+0.102399` | 12 |
| `{0,12}` | `−3.313140158045` | `−36.444542` | 11 |

so the fixture's cut condition reduces to `b(0) ≤ 12Φ`, exactly as for the 13-cluster — a fixture
constrains one capacity and nothing else.

**The rational fixture converges to the ideal one.** Refining the rounding at fixed shell radius
`2.0005`, the central volume settles:

| denominator | central volume | change |
| --- | --- | --- |
| `10⁴` | `5.554154021196409` | — |
| `10⁵` | `5.554497957052789` | `3.44·10⁻⁴` |
| `10⁶` | `5.554454804528846` | `4.32·10⁻⁵` |
| `10⁷` | `5.554454533883713` | `2.71·10⁻⁷` |

The limit is **not** the dodecahedron `5.5502910285` — that is the value at radius exactly `2`,
which the irrational 13-cluster realises; at `r = 2.0005` the limit is `≈5.5544545`. The two
constructions are consistent, not identical.

### 2.4 Soundness evidence at scale

The review notes that generic soundness remains a proof obligation. It is not discharged here, but
the evidence behind it is no longer twelve hand-written cases: `fuzz_cut_flow.py` draws **random**
instances (`n ≤ 4`, `b ∈ {−2..2}`, random edge sets, rational `Φ`) and decides each one three ways —
the exhaustive cut scan (exact), Fourier–Motzkin elimination over ℚ (`fm_feasible`, built from
`range(len(b))`, so it cannot repeat the D8 omission), and the interface's own verdicts — then
requires that

* any returned flow passes `verify_flow_exact` **and** the oracle agrees it is feasible;
* any returned witness is a genuine violation **and** the oracle agrees it is infeasible;
* `Φ ≥ t*` is feasible and `Φ = t* − 1/4` is not.

| run | instances | flows verified | witnesses | disagreements |
| --- | --- | --- | --- | --- |
| seeds 0, 1, 2 | 6 000 | — | — | **0** |
| seed 42 | 20 000 | 8 716 | 11 284 | **0** |

That is evidence, not a proof: it samples a distribution, and the oracle is capped (it returns
`None` rather than blowing up, and undecided instances are skipped, never counted as agreement).
What it does establish is that the three decision procedures do not disagree anywhere in 26 000
random instances — which is the shape of evidence a soundness proof would have to explain.

## 3. Completeness of the exact volume algorithm (fallback, first item)

The engine enumerates vertices from a set `A` of half-spaces proposed by a floating-point pre-pass.
Nothing used to check that the pre-pass kept every facet — a float filter could in principle drop
one and shrink the cell silently. The engine now carries an **exact certificate**:

* **(C1)** every facet of the computed hull lies on a plane of `A`. All vertices satisfy every
  `A`-plane by construction, so `hull ⊆ ⋂A`; C1 says the hull's boundary is made of `A`-planes,
  hence `hull = ⋂A` — a polytope, hence bounded.
* **(C2)** every **discarded** plane contains every vertex, so `⋂D` does not cut the hull.
* **(C3)** the hull is non-degenerate.

Then the true cell `= ⋂A ∩ ⋂D = hull`, and the volume is exact with **no reliance on the float pass**.

**The triangulation is now qhull-free as well.** Computing the boundary from a `scipy` convex hull
failed with `QH6154` (a flat initial simplex) on a coplanar facet of a *shell* cell — a float
fragility in a computation that was otherwise exact end to end. Since every vertex already lies on
identified planes, the facets are read off directly (the vertices exactly on each plane), ordered by
an exact angular sort around the facet centroid, and fanned into triangles joined to the interior
point. Every arithmetic step is rational; `scipy` is no longer used by the engine at all. The known
cases (cube `8`, BCC `a³/2`), the partition identity, and the sampler cross-check (`0.2σ`) all still
pass, and the family bracket is unchanged to the last digit.

Two things had to be got right, and the first version got them wrong:

1. **A plane of `A` that supports no facet is redundant, not an error.** Its half-space contains the
   cell. The 13-cell shell fixture produces such planes, because its coordinates are rounded to
   `10⁻⁶` and near-duplicate bisectors appear; a check that demanded "every active plane is a facet"
   failed on exactly that fixture.
2. **The check must fire when a facet is dropped**, or it is decoration. The control
   (`_drop_active = k`) fires on 2 of 3 single drops; the third is a redundant plane, which is
   legitimately harmless — that is precisely the distinction in (1).

## 4. Two-site periodic congruence (fallback, second item)

**Theorem.** Let `Λ = {A,B} + L` have exactly two points per cell and `A − B ∉ L`. Then the two
Voronoi cells on the torus `R³/L` are congruent; in particular `vol Ω(A) = vol Ω(B)` and
`b(A) = b(B)`.

**Proof.** Let `σ(x) = A + B − x`, the point reflection in the midpoint of `A` and `B`.
(i) `σ(x + n) = σ(x) − n`, and `−n ∈ L` because every lattice is centrally symmetric (`−L = L`), so
`σ` descends to the torus. (ii) A point reflection is an isometry, so `σ` is an isometry of the
torus. (iii) `d(σx, A) = min_n |A + B − x − A − n| = min_n |x − B + n| = d(x, B)`, using `−L = L`;
symmetrically `d(σx, B) = d(x, A)`. (iv) Hence `σ` maps `{d(·,A) ≤ d(·,B)}` onto
`{d(·,B) ≤ d(·,A)}`, i.e. `cell(A)` onto `cell(B)`. ∎

**Consequence.** A nonuniform **2-point** periodic fixture cannot exist. That is why the smallest
nonuniform fixture has three points (`fixture_nonuniform.py`); the earlier numerical evidence was a
symptom of the theorem, not evidence for it. The check reflects the exact vertex set of one cell
through the midpoint and compares it with the other's, on three configurations — exact vertex sets,
not volumes alone.

## 5. What is NOT claimed

* **The 500 finite cases were re-run after the engine changed.** The qhull-free volume code (§3)
  recomputes all 500 instances of `nearcontact_scan.py` to a byte-identical JSON: still `0` with
  `t* > 0`, densities `0.6206–0.7392`. That re-run is the check that the engine change did not move
  any number.
* **The 500 finite cases stay finite evidence.** `nearcontact_scan.py` scans 500 near-contact
  instances in five families at densities `0.6206–0.7392` and finds `t* = 0` in every one. That is
  `TESTED_FINITE`: it says the criterion is vacuous in those families, **not** that it is vacuous in
  general, and it is not a theorem.
* **No equivalence.** `K15-C-CUTIMPLIES-003` is one implication (finite-`U` cut condition ⇒
  `ρ ≤ 1/√32`). The converse is open.
* **Generic soundness remains a proof obligation**, and here is exactly what is and is not discharged:
  every *positive* output of the interface is exactly verified — a returned flow is checked against
  `|φ| ≤ Φ` and `div ≥ b` at every vertex, and a reported violating cut by exact rational arithmetic
  — but (a) "no flow found" is not a claim of infeasibility, (b) the LP path uses floating point
  internally before its output is verified, and (c) `t*` from the scan equals the LP optimum only by
  LP duality, which is checked numerically to `10⁻⁵`, not formalised here.
* **No exact contact matching is assumed** anywhere for saturated packings; the only geometric input
  is the cell-volume partition identity, which holds for every packing.

## 6. Files and reproduction

```bash
cd KeplerConjecture/Computation
python3 fixture_dense_shell.py     # the fixture, its conventions, the window (~30 s)
python3 cut_flow.py --fixture out/fixture_dense_shell.json   # the evaluated cut and flow
python3 fixture_nonuniform.py      # the engine, its certificate, the two-site theorem (~30 s)
python3 audit_cut_flow_api.py      # 69 checks of the repaired interface
python3 fuzz_cut_flow.py 20000 42  # 20 000 random instances, three-way (~15 s)
python3 nearcontact_scan.py        # the 500 finite cases (~13 min)
```

Artifacts: `fixture_dense_shell.py`, `out/fixture_dense_shell.json` (coordinates, exact volumes,
`b` enclosures, edges), `fixture_nonuniform.py` (certificate §3, theorem §4),
`nearcontact_scan.py`, `out/nearcontact_scan.json`.

## 7. Clock

Receipt `2026-11-14T14:28:52Z`. Every commit of this block, on the real clock:

| commit | UTC | what |
| --- | --- | --- |
| `88f882f` | 14:30:12 | a NONVACUOUS 3-D cut/flow fixture -- rational coordinates, exact volu... |
| `a958bf3` | 14:33:55 | certify the volume engine's completeness; prove two-site congruence |
| `fab3fef` | 14:35:53 | the nonvacuous window of the dense-shell family |
| `a981271` | 14:38:40 | qhull-free exact triangulation; convention checks; the nonvacuous window |
| `efd6b76` | 14:41:12 | the patch minimum is exactly t*, and the shell's closure obstruction |
| `16a693e` | 14:41:30 | register -- the nonvacuous fixture, its window, the obstruction, and ... |
| `926cdb7` | 14:50:05 | 26 000 random instances, three-way, no disagreement |
| `f84a91e` | 14:54:04 | the cut profile (one inequality) and convergence of the rational shell |
| `222971b` | 14:54:20 | runtimes for the two new scripts and the fuzz |
| `e1ed10d` | 14:55:35 | the arrangement decides -- icosahedral vs cuboctahedral 12-shells |
| `38a04a8` | 15:11:41 | record the cuboctahedral contrast and the post-change re-run |

**Substantive work accounting.** The fixture, the certificate, the theorem and the review were
pushed by `14:41Z`. The compute-bound portion is `nearcontact_scan.py` at **15 m 53 s** for the
post-change re-run (500 instances) and `fuzz_cut_flow.py` at 26 000 instances; the rest is writing
and the validation sweeps. Stated separately because a previous block was called out for counting
verification as substance.

**Mode.** Ultramath is ON; **no swarm was run** and `ultramath_start` was not called, as the review
requires.

**No Lean.** Nothing in this block needed a Lean build, so nothing was sent to Astra.
