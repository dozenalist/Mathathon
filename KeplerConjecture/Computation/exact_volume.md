# Specification: `exact_volume.py`

A proof-carrying exact-volume verifier for a rational polyhedron in `R³`. This file states the
contract; `exact_volume.py` implements it and `tests_exact_volume.py` exercises it.

## 1. Inputs and outputs

* **Input**: a finite list of planes `(a,b,c,d) ∈ Q⁴` meaning the half-space `a·x + b·y + c·z ≤ d`,
  and a rational point `v` strictly inside all of them.
* **Output**: `(volume, certificate)` where `volume ∈ Q` and the certificate is
  `{planes, candidate_planes, interior, vertices, facets[{plane, verts, area}], volume, dropped}`.
* **Guarantee**: the returned volume is the volume of `⋂{planes}`. It is returned only after
  `check_certificate` has verified the certificate by exact rational arithmetic.
* **Failure**: `ValueError` with a named obligation. Never a silently wrong number, never a float.

## 2. Normalisation

A plane is stored as its primitive integer tuple after clearing denominators and dividing by the
gcd of all four entries. **Only positive scaling is admissible**: `(−a,−b,−c,−d)` describes the
opposite half-space. Two planes with equal normal forms are the same half-space and are deduplicated
(this is what makes `(1,0,0,1)` and `(2,0,0,2)` one face, not two). A plane whose direction is a
positive multiple of another's and whose offset is looser is **dominated** and dropped, with the
reason recorded.

## 3. The certificate's obligations

Let `P = ⋂{planes}` and `Q = conv(vertices)`.

| id | obligation | what it buys |
| --- | --- | --- |
| V0 | every **candidate** plane is one of the constraints | otherwise the facets could be built on a half-space not in `cert["planes"]`, so the polytope would be a strict subset of the intersection the volume claims — the same defect as the reviewer's witness (2), in the other direction |
| V1 | every vertex satisfies every plane **in `cert["planes"]`** — all the constraints, not only the candidate ones | `Q ⊆ P` |
| V2 | `a·v < d` for every plane in `cert["planes"]` | a valid apex for the fans |
| V3 | each facet's vertices lie on its plane, `≥ 3`, non-collinear, and the area vector **recomputed from the vertex order** is a positive multiple of the outward normal | the facet is a genuine, outward-oriented 2-face |
| V4 | every vertex lies on `≥ 3` facets | no spurious vertices |
| V5 | the area vectors sum to `0` **and** the facet normals have rank 3 | **boundedness**. Closure gives `Σ λ_f a_f = 0` with `λ_f > 0`; on its own that does *not* bound the polyhedron (the side faces of an infinite triangular prism close with positive weights and the prism is unbounded). With rank 3 it does: any `x` in the recession cone is orthogonal to every `a_f` (`0 = Σλ_f a_f·x = Σλ_f(a_f·x) ≤ 0` forces every `a_f·x = 0`), and a rank-3 family has zero orthogonal complement |
| V6a | the facets are **unique**: distinct plane indices, in range, and no two on the same half-space | without it, duplicating the facet list doubles every area vector, closure still holds (`0 = 2·0`), and the divergence theorem reports twice the volume |
| V6 | (derived) every facet of `P` is listed | a face is `P ∩ {supporting plane}`; any plane meeting `P` in a 2-set is a facet, so the listed facets are all of them, the rest are redundant, and V1 shows they do not cut |
| V7 | `(1/3) Σ_f x_f·A_f > 0` and equal to the certificate's volume | the divergence theorem on a closed oriented surface |
| V8 | the fan volume `Σ_f Σ_triabs det/6` with apex `v` equals V7 | a second derivation that uses **no area vectors**, so it catches an error in the area formula that V5 and V7 both depend on. It is a consistency check between two formulas over the same vertices, not an independent measurement |

`Q ⊆ P` (V1) and `P ⊆ Q` (V3+V6) give `P = Q`; V5 gives boundedness, so `V` is the complete vertex
set of `P`. Every step is rational arithmetic.

## 4. Search is not trusted

`certify_volume(planes, v, candidates=None)`:

* with `candidates=None`, every triple of planes is solved exactly (`det = 0` exactly is the only
  skip) and every solution satisfying all planes is kept;
* with `candidates`, only those planes are enumerated, and then **every other plane is checked
  against every vertex**. A half-space that properly cuts a polytope leaves a vertex outside it, so
  this proves `⋂(all) = ⋂(candidates)`.

Either way the certificate is verified before the volume is returned, and the certificate is the
only thing the volume claim rests on.

## 5. Out of scope

* The certificate says nothing about whether the **plane list** was the right one. For a Voronoi
  cell that is a separate hypothesis; `fixture_nonuniform.cell_volume` checks it with
  `2·max|x−v| ≤ r_max` (every competitor outside `r_max` is farther than twice the cell's
  circumradius) and, globally, with the cell volumes summing to the period volume.
* Nothing here is a packing bound, and nothing here bears on Kepler.

## 6. The audited path, in one paragraph (for X and Main)

**What is audited.** Any volume produced by `fixture_nonuniform.evaluate`, `make_fixture`,
`fixture_dense_shell` or `fixture_nonuniform.cell_volume` comes from `certify_volume`, which returns
only after `check_certificate` has verified the seven obligations by exact rational arithmetic on the
certificate's own data. A third party can re-run `check_certificate` on a stored certificate without
trusting the search, the float pre-pass, scipy, or the person who ran it.

**What is not.** (i) The certificate is about the *plane list it is given*; that the list contains
every competitor within `r_max` is a separate hypothesis, checked by `2·max|x−v| ≤ r_max` and,
globally, by the cells summing to the period volume. (ii) The search is not verified — only its
output is. (iii) Nothing here is a packing bound, and nothing bears on Kepler. (iv) The verifier
computes volumes of *rational* polyhedra; the irrational 13-cluster's dodecahedron enters only
through the closed-form `V_dod` in `period_convention.py`, not through this verifier.

**Where the evidence is.** `tests_exact_volume.py` (25 adversarial checks with hand values),
`out/exact_volume_adversarial.json` (8 fixtures with planes and hand volumes), `crosscheck_volume.py`
(~190 random polytopes against an independent sampler, all V5 rejections carrying an explicit
unbounded ray).
