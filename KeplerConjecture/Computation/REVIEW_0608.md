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
python3 fixture_dense_shell.py     # the nonvacuous fixture, exact volumes (~2 s)
python3 cut_flow.py --fixture out/fixture_dense_shell.json   # the evaluated cut and flow
python3 fixture_nonuniform.py      # the engine, its certificate, the two-site theorem (~30 s)
python3 audit_cut_flow_api.py      # 69 checks of the repaired interface
python3 nearcontact_scan.py        # the 500 finite cases (~13 min)
```

Artifacts: `fixture_dense_shell.py`, `out/fixture_dense_shell.json` (coordinates, exact volumes,
`b` enclosures, edges), `fixture_nonuniform.py` (certificate §3, theorem §4),
`nearcontact_scan.py`, `out/nearcontact_scan.json`.

## 7. Clock

Receipt `2026-11-14T14:28:52Z`. The fixture was pushed at `14:30:12Z` (commit `88f882f`), the
certificate and the congruence theorem at `14:33:55Z` (`a958bf3`); this document and the closing
validation follow. Commit times are in the table below and are the evidence.

