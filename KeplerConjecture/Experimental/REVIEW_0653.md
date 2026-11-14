# Review 0653 — two further defects, a retracted counterexample, and the ring-excess hypotheses

Block `K15-REVIEW-0653-E`. Receipt `15:04:13Z`. Follow-up to `e71a177`.

Both reported defects are real, both are repaired, and the counterexample I built on one of them
is **retracted**: it was an unbounded-polytope artefact of exactly the class the previous block
added a witness for.

---

## 1. Defect 3: `origin_interior_certificate` gave a false certificate

At `f502b9a` (and `7bea443`, same blob),

```
origin_interior_certificate([(1,0,0),(0,1,0),(0,0,1)])  =  (True, 1, 1)
```

although all three points satisfy `x+y+z = 1`, so the origin is not in their convex hull at all.

**Cause.** Two independent errors in one helper.

1. **The wrong normal.** The code used `cross(b, c)` — normal to the plane through `0, b, c` —
   where the plane through `a, b, c` has normal `cross(b−a, c−a)`. On the witness:
   `cross(b,c) = (1,0,0)` while `cross(b−a,c−a) = (1,1,1)`, the plane actually containing the
   three points. With the wrong normal the "supporting plane" is a different plane altogether,
   and the margin computed against it is meaningless.
2. **No affine-dimension check.** A point set lying in a plane has no interior in `R³`. The
   routine never asked, so for a 2-dimensional input it happily reported an interior.

**Repair.** `origin_interior_certificate` now (a) returns `False` unless the normals affinely
span `R³` (a four-point determinant test, `_affine_dim_3`), and (b) builds each candidate plane
from `cross(b−a, c−a)`. Witness **W3** keeps the exact input and now reports

```
(False, 'the normals span less than 3 dimensions: no interior in R^3', 0)
```

**What this did and did not break.** The helper is used inside `polytope_volume` (boundedness)
and inside the radius routine. On the five controls the wrong normal happened to give the same
answer, which is why the controls passed in 24.8 s locally and did not catch it: the controls
are bounded polytopes whose supporting planes are plentiful, and a wrong plane through the
origin, if it is not "supporting" for the actual set, is discarded. The defect is real for
inputs where a *false* supporting plane is accepted — as in W3 — and that is exactly a
certificate-integrity failure, not a numerical one.

---

## 2. Defect 4: a floating sphere mesh and an unproved `1e-9`

`spanning_constant` computed `c` by meshing the sphere with **numpy floats** and then
subtracting the mesh diameter plus a hard-coded `1/10⁹`. Neither the mesh nor the subtraction
was justified: the mesh vertices are numerical, and `1e-9` was a guess.

**Repair: an exact radius witness with no mesh and no epsilon.** The quantity needed is
`c = min_{|u|=1} max_i u·n_i`. If `B(0,r) ⊆ conv{n_i}` then every unit `u` has
`max_i u·n_i ≥ r`, because `r·u` lies in the hull and `r = u·(r u) = Σλ_i (u·n_i) ≤ max_i u·n_i`.
And `conv{n_i}` lies in each of its supporting half-spaces, so

```
c  ≥  min over supporting planes of  |k| / |m|        (plane m·p = k),
```

which is the inradius of the hull about the origin — computed **exactly** from the same
supporting-plane enumeration, with only `sqrt` enclosed rigorously by `sqrt_iv`.

Witness **W4**: on the cube's six normals this returns `c = 0.577350269190 = 1/√3` exactly (the
octahedron's inradius, eight supporting planes) — a value known in closed form, so the routine
is checked against something independent.

*(A first attempt at this used a tetrahedron with vertices among the normals. That fails on the
cube: `0` is interior to the octahedron but lies in no tetrahedron spanned by four of its
vertices, because any four include an antipodal pair and give a zero barycentric coordinate. The
inradius formulation has no such restriction.)*

---

## 3. The `0.707055` counterexample is RETRACTED

I claimed that twelve unit normals could give a polytope of volume `0.707055`, and used that to
argue the twelve-face bound `vol D' ≥ V_dod` was false. **That was wrong**, for the reason the
brief gives.

**Exact input.** `np.random.default_rng(11)`, `20 000` draws of `ns = normal(size=(12,3))`
normalised, each evaluated by vertex enumeration plus `scipy.ConvexHull`. The minimum found was
`0.707055`, at a draw beginning with

```
[-0.427367229556, -0.9023888648,  0.055241178365]
[-0.336700025073, -0.491907202018, 0.802907465228]
[ 0.396773477589, -0.684859941436, 0.611177280417]
```

**Audit.** (i) Every `{y : y·n_i ≤ 1}` contains the unit ball, so any finite volume is at least
`4π/3 = 4.188790`; `0.707055` is impossible. (ii) Feeding that exact 12-tuple to the *repaired*
`origin_interior_certificate` returns `False` — the half-spaces do not bound a polytope, the
region is unbounded, and the vertex enumeration found a partial vertex set whose hull is what
`ConvexHull` measured. So the number is an artefact of an unbounded polytope: precisely the
error class of W2, committed by the routine that W2 was added to guard.

**Consequence.** The pure statement "twelve half-spaces at distance `1` have volume `≥ V_dod`"
is **not refuted** by me, and I have no counterexample. It is simply unproved. The conditional
result of `REVIEW_0608` §11 therefore stands exactly as stated: conditional, with the premise
`vol D' ≥ 5.5400` open — neither proved nor refuted.

---

## 4. The volume contract, now with independent witnesses

`polytope_volume` was checked before only on bodies that are symmetric (cube) or that arose from
the geometry under study. It now has a contract:

| body | exact volume | returned |
| --- | --- | --- |
| cube `[-1,1]³` | `8` | `8`, 8 vertices |
| regular tetrahedron | `8/3` | `8/3`, 4 vertices |
| octahedron `|x|+|y|+|z| ≤ 1` | `4/3` | `4/3`, 6 vertices |
| box `2 × 3 × 4` | `24` | `24`, 8 vertices |
| coplanar normals (unbounded) | ∞ | **refused** |

The octahedron is checked because it is the *dual* of the cube and exercises the 8-plane
combinatorics; the box because its facet distances differ, which the cube's do not. Together with
W2 (four-vertex unbounded) and W3 (coplanar), the routine now has both low-dimensional and
adversarial coverage.

---

## 5. Status of the previous claims

| claim | status |
| --- | --- |
| `K15-E091`/`E095` certified enclosure | **repaired again**; five controls pass with the exact radius, width `1.2e-18` |
| `K15-E094'` certified regions | **unchanged**, but see below: produced with a radius that used the mesh, so **pending** re-certification with the exact radius |
| `K15-E099` conditional twelve-face theorem | **conditional**, premise open, not refuted (§3) |
| continuum certificates / universal pair claims | **pending**, as instructed |

An honest remark on `E094'`: the region runs used the mesh-based radius. The change to the exact
inradius alters `c`, hence `R`, hence the slack. The numbers are not expected to move much
(`c` was `0.73` by mesh; the inradius gives `0.577350` for the cube, and for the C5 normals the
table below), but "not expected to move much" is not a certificate, and the region claims must be
recomputed before they are quoted again.
