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

**`E094'` re-certified with the exact radius.** The exact inradius *improves* the constants
rather than weakening them, because the mesh under-estimated `c`:

```
C5 normals:  mesh gave c >= 0.730508 ;  exact inradius c = 0.768212  (20 supporting planes)
             mesh gave R = 1.467     ;  exact R = 1.37              -> tighter slack

region theta in [110,110.25] x phi in [35,35.25], 3 x 3 exact boxes
   mesh radius   [5.867852, 5.933758]   margin +0.104434
   exact radius  [5.869101, 5.932503]   margin +0.105684     <- tighter, as predicted
```

`evidence/region_110_110p25_exactradius.json`. The `1°` region is re-running with the exact
radius; its result is reported in the final message. Neither is a universal claim: both are
continuum statements **within the C5 family**.

---

## 6. The ring-excess lemma: a self-contained conditional proof, and an audit of its premise

### 6.1 The lemma, self-contained

> **Lemma.** Let `P` be a bounded polytope with the origin interior, `P = ⋂_{i=1}^{n} {y·n_i ≤ d_i}`
> with `|n_i| = 1`, and let `J ⊆ {1..n}` be a set of faces. For `b ≥ 1` put
> `P(b) = ⋂_{i∈J}{y·n_i ≤ b·d_i} ∩ ⋂_{i∉J}{y·n_i ≤ d_i}`. Then
>
> ```
> vol P(b) − vol P  =  (b−1) Σ_{i∈J} d_i ∫₀¹ A_i(t) dt  ≥  (b−1) Σ_{i∈J} d_i · min_t A_i(t) ,
> ```
>
> where `A_i(t)` is the area of the `i`-th face of `P(t)`.

*Proof.* `t ↦ P(t)` is a linear homothety of the face planes; the volume is absolutely continuous
in `t` (a convex body whose support function is Lipschitz in `t`), and where the combinatorial
type is constant the derivative is `Σ_i d_i A_i(t)` — moving one face outward at speed `d_i`
appends a prism of base `A_i(t)` and height `d_i dt`, and the other faces do not move. The
identity follows by integrating over the finitely many intervals of constant type; at the
finitely many type changes the derivative is discontinuous but the volume is continuous, so the
integral is unaffected. ∎

Nothing here is specific to the dodecahedron, and nothing uses a computation.

### 6.2 Its use, and exactly what is assumed

Applying it to the payer cell with `J` the five ring faces, `d_i = 1`, `b = ρ_r/2`:

```
vol Ω(w1)  =  vol D' + (b−1)·5·mean_t A_ring(t) ,        D' = Ω with the ring faces at 1,
```

so for the twelve-face class

```
(P')  follows from   vol D' + 5(b−1)·A_min  ≥  5.763417470 ,
```

and with the uncut-disk bound `A_min ≥ π t*² = 0.868315` (§`REVIEW_0608` 11) the single remaining
premise is `vol D' ≥ 5.5400`.

### 6.3 Auditing the `5.5400` premise

`D'` is the unit-distance polytope of the twelve directions — `c`, the five ring directions at
`58.2825°`, and six free ones constrained by 2-separation (`60°` from `c` and from each other,
`≥ 58.28°` from each ring direction). `premise_audit.py` minimises `vol D'` over that admissible
set, by local search from the C5 configuration and from six random legal restarts:

```
C5 configuration                        vol D' = 5.572649
local search from C5 (25 s)                    5.567413
six random legal restarts (random walk inside the legal region)
                                       5.567434, 5.567417, 5.567420, 5.567425, 5.567421, 5.567420

minimum found  5.567413          premise 5.540000   slack +0.027413
                                 V_dod     5.550291  the minimum is +0.017122 above it
```

**Seven independent starts converge to the same value to five digits**, which is what a genuine
minimum of a smooth functional looks like. The premise holds with slack `0.027`, and — more
interesting — the admissible minimum sits only `0.0171` above `V_dod`, suggesting that the
sharper statement `vol D' ≥ V_dod` may be true on the admissible family even though it is false
in general (§3). That would be a *stability* statement about the icosahedron: moving five of the
twelve directions from `63.43°` to `58.28°` raises the unit-distance volume by at least `0.017`.

**Caveat, stated plainly.** This is a numerical minimisation, not a proof. It bounds the minimum
from *above*; the premise needs a lower bound. What it does establish is that the premise is not
knife-edge, that it is not an artefact of one configuration, and that the search does not drift
towards `5.5400` — all seven starts stop `0.027` short of it.

*(A first version of the sampler drew directions from scratch and found **zero** legal sets in
`6 × 4000` tries; the legal region is far too small in twelve dimensions for rejection sampling.
The random-walk restart replaced it and works immediately.)*

### 6.4 What would close it

A proof that `vol D' ≥ 5.54` (or the sharper `≥ V_dod`) for every admissible six-direction set.
Equivalently, a lower bound on the volume of a twelve-face unit-distance polytope whose five
"ring" directions are held at `58.2825°`. This is a stability statement about the dodecahedron's
neighbourhood, and it is the smallest remaining target on the pair route.

---

## 7. The premise is TRUE, by Lindelöf 1869 — the twelve-face theorem is restored

The audit of §6.3 was overtaken by a literature check, and the outcome is better than "the
premise holds numerically".

**Lindelöf (1869).** Among convex polyhedra with `n` faces circumscribed about a sphere of radius
`r`, the surface area is minimised by the regular polyhedron, and for `n = 4, 6, 12` the
minimiser is the regular tetrahedron, hexahedron and **dodecahedron** respectively. Since
`V = S·r/3`, this minimises the volume too.

**Application.** `D'` is an intersection of twelve half-spaces at distance `≥ 1` from the origin.
Move every face that lies farther than `1` in to `1`: the volume can only decrease, and the
result is a twelve-faced polyhedron circumscribed about the unit ball. By Lindelöf its volume is
at least `V_dod`. Hence

```
vol D'  >=  V_dod = 5.550291029  >=  5.540000 ,
```

**the premise of §6.2 holds unconditionally**, and the conditional theorem of `REVIEW_0608` §11
becomes a theorem modulo Lindelöf (imported, exactly as Hales–McLaughlin is imported elsewhere in
this project).

This also explains the audit of §6.3 rather than contradicting it: seven starts converged to
`5.567413`, which is `0.0171` above `V_dod`, and Lindelöf says the true minimum over *all*
twelve-faced unit-distance polytopes is `V_dod`, attained at the icosahedral directions — which
our family cannot reach because the ring is pinned at `58.2825°` instead of `63.43°`. The two
numbers are consistent, and the `0.0171` is the price of the pinned ring.

**What this does NOT do.** It does not extend to thirteen or more faces: Lindelöf's bound for
`n = 13` is a different (smaller) regular-polyhedron value only for `n = 4, 6, 12` — for other
`n` the minimiser is a non-regular polyhedron and its volume is smaller than `V_dod`. The
thirteen-face case remains open, with the `0.042` gap recorded in `REVIEW_0608` §11.1.

**Citation.** L. Lindelöf, *Propriétés générales des polyèdres qui, sous une étendue superficielle
donnée, renferment le plus grand volume*, Bull. Acad. Sci. St. Pétersbourg **14** (1869),
257–269. Located via the survey arXiv:1509.08859, which states Theorem 2.1 in the form used
above and records `f = 4, 6, 12` as the equality cases. **Not verified in the original**: I have
the secondary statement only, and a referee should confirm that Lindelöf's theorem is stated for
polyhedra circumscribed about a sphere with the equality cases as quoted.

---

## 8. The thirteen-face case, stated exactly

With the premise proved (§7), the only remaining gap on the pair route at the icosahedral pair is
completions with **thirteen or more faces**. It is worth recording exactly what it would take,
because the numbers say the obstruction is in the *area* bound rather than in the volume bound.

Same lemma, thirteen faces, `J` the five ring faces:

```
vol Ω(w1)  =  vol D'' + 5(b−1)·mean_t A_ring(t) ,      D'' has thirteen faces at distance >= 1,
5(b−1)     =  0.257311121  per unit of area.
```

The thirteen-face base is at most `5.498284` (the icosahedral twelve plus one extra face at
distance `1`, measured in `REVIEW_0608` §11.1), so

```
(P') for thirteen faces  <=  vol D'' + 0.257311·A_min  >=  5.763417
                         <=  A_min >= (5.763417 − 5.498284)/0.257311 = 1.030400
                            and  vol D'' >= 5.498284 .
```

| ingredient | today | needed |
| --- | --- | --- |
| provable `A_min` (uncut disk, worst point of the path) | `0.868315` | `1.030400` |
| true `A_min` in the configurations measured | `1.249 – 1.276` | — |
| thirteen-face base bound `vol D''` | none (Lindelöf's `n = 13` value is below `V_dod`) | `5.498284` |

**So the gap is not in the geometry but in the certificate of one number.** The uncut-disk
argument gives `0.868`; the true ring faces have area `1.25`, comfortably above the `1.030` the
argument needs. The disk bound is lossy because it takes the worst single admissible neighbour
independently of the others: it ignores that the cutting centres are 2-separated *from each
other*, so the ones that would cut the same face at the worst angle cannot all be present. Making
that quantitative is the concrete next step, and it is a finite sphere-packing question about
five caps, not an analytic one.

## 9. Hashes and reviewer obligations

```
source read        e71a1779bddaa47693b153106af6ee8521af9ab6
repaired verifier  Experimental/scripts/cell_certificate.py   (W1-W4 + volume contract)
region certifier   Experimental/scripts/certify_region_v2.py
pilot request      Experimental/COMPUTE_REQUEST_0653.md
ledger             K15-E099 (theorem modulo Lindelöf), K15-E100 (the Lindelöf input)
                   K15-E091/E094' pending re-certification with the exact radius
```

**For X, in order.** (1) Witness W3 — three coplanar normals must be *refused*; the old helper
returned `(True, 1, 1)`. (2) Witness W4 — the exact inradius on the cube's normals must be
`1/√3`; there is no mesh and no epsilon left in the radius path. (3) The volume contract —
octahedron `4/3`, box `2×3×4 = 24`, coplanar normals refused. (4) The retraction in §3: confirm
that the offending 12-tuple is unbounded and that `0.707055 < 4π/3`. (5) The Lindelöf citation —
**secondary source only**, and the original should be checked before the twelve-face theorem is
quoted as unconditional.

**Pending, and not to be quoted:** the region certificates of `K15-E094'` (computed with the
mesh-based radius), and any universal pair claim. Twelve faces is a class, not all completions.
