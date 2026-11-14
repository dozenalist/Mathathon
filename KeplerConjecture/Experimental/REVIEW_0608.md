# Review 0608 — two defects in the certified enclosure, and their repair

Block `K15-REVIEW-0608-E`. Receipt `14:17:22Z`. Follow-up to `d289bef`.

The brief was to audit the claimed certificate rather than its decimal outputs. It was right to
insist: **the enclosure was not sound**, for two independent reasons, and the region certifier
had a third defect. All three are confirmed here, repaired, and kept as regression witnesses
that fail on the old code and pass on the new.

The conclusions of the previous block are **not** withdrawn — every one of them is arithmetically
right, because the missing slack is of order `1e-18` at a single point — but they were not
*certified*, and a certificate that is right by accident is not a certificate. `K15-E091` is
marked repaired, and `K15-E094` (the certified regions) is **pending** until the revised
certifier has been rerun.

---

## 1. Defect 1: the slack used an infinity norm against a Euclidean radius

`sandwich` computed `e = max over components of the half-width` of the normal's interval, which
bounds `|n_i − n_i'|_∞`, but then used `R·e` where `R` bounds `|y|_2`. For a 3-vector
`|δn|_2 ≤ √3·|δn|_∞`, so the slack was short by up to a factor `√3`.

> **Witness W1** (exact, `/` = rational). `n_0 = (1,0,0)`, `n = (3/5,4/5,0)`,
> `y = (−4/9,8/9,0)`, `R = 1`. Then `|y|² = 80/81 ≤ 1` and
> `y·(n−n_0) = 8/9 = 0.888…` while `e = 4/5`. Ratio `1.111… > 1`: the bound fails.

It does not fail for every `y`, only for those pointing along the component that carries the
error — which is exactly why the decimal outputs looked right and the certificate was not.

**Repair.** Slack `= R·√3·e_i + f_i` with the rational upper bound `√3 ≤ 7/4`, so every number
in the chain is a `Fraction`. `cell_certificate.py` carries W1 as an executable test.

---

## 2. Defect 2: boundedness was inferred from a vertex radius

The old code checked `max|vertex| ≤ R` over the enumerated vertices and treated that as
boundedness. **An unbounded polyhedron can have vertices.**

> **Witness W2.** The half-spaces `y·n_i ≤ 1` for `n_i = (±2,0,0), (0,±2,0), (0,0,−2)` define
> `{|x| ≤ 1, |y| ≤ 1, z ≥ −1}` — unbounded along `(0,0,1)`, infinite volume — and it has
> exactly **four** vertices, `(±1,±1,−1)`. The old `sandwich` returned a finite value
> `≈ 4/3` for it.

That is the defect that matters most: a finite enclosure for an infinite cell is exactly the
failure mode a certificate exists to prevent, and the radius check could never have caught it.

**Repair.** `polytope_volume` now *decides* boundedness: the polytope `{y : y·n_i ≤ d_i}` with
`d_i > 0` is bounded iff `0 ∈ int conv{n_i}`, and that is decided exactly by enumerating
supporting planes — for every triple of normals whose plane has all the others on one side, the
origin must lie strictly on the hull's side. If it does not, the certificate **refuses**.

*The first version of this repair was itself over-restricted*: it demanded four normals with a
strictly positive dependence, which the cube's six normals never have (any four include an
antipodal pair, so the determinant vanishes) even though `0` is plainly interior. The cube
control caught it; the supporting-plane test replaced it.

---

## 3. Non-circularity: where `R` comes from

The sandwich needs a radius `R` for the true cell, and it must not be obtained from the
sandwich. The repaired chain is:

1. **A priori radius.** Let `c = min_{|u|=1} max_i u·n_i'`. For `y` in the true cell with
   `r = |y|` and `u = y/r`, choose `i` with `u·n_i' ≥ c`:

   ```
   r·c  ≤  r(u·n_i') = y·n_i' ≤ b_i' + r·√3·e_i      ⟹   r·(c − √3 e_max) ≤ b_max
   ```

   so `R := b_max / (c − √3 e_max)` bounds `|y|`. For the C5 fixture this gives
   **`R = 1467/1000 = 1.467`** against a true `max|vertex| = 1.3017` — a good bound, and it
   uses **no volume and no vertex enumeration**.
2. `c` itself is bounded below by meshing the sphere: `max_i u·n_i` is `1`-Lipschitz in `u`,
   so its minimum over the sphere is at least (minimum over the mesh vertices) minus the mesh
   diameter.
3. **Then** build `Out` with slack `R√3e + f`, certify it bounded (exact, §2), and check every
   one of its vertices satisfies `|y| ≤ R`.
4. **Inner inclusion.** `Inn ⊆ Out`, and `Out ⊆ B(0,R)`, so every `y ∈ Inn` has `|y| ≤ R` and
   the slack inequality may be applied to it: `Inn ⊆ Ω`. No circularity — `Inn`'s inclusion
   rests on `Out`'s radius, which is checked directly.

---

## 4. Defect 3: the region certifier's partition, inputs and output

`certify_region.py` computed `n = round(span/width)` boxes of width `width`. When `span` is not
divisible by `width`, the leftover strip is **never certified** and nothing said so. It also
accepted reversed and empty ranges, and printed floats.

**Repair** (`certify_region_v2.py`):

- `n = ceil(span/width)` boxes of width **`span/n` exactly**, so the boxes tile `[lo,hi]`; the
  tiling is asserted, not assumed.
- empty and reversed ranges are rejected with a message;
- every bound is serialised as a rational **rounded outward to 40 decimals**, with the exact
  rational alongside when it is short enough, and the scheme recorded in the file.

Demonstration on a span that is *not* divisible: `θ ∈ [110, 110.25]`, `φ ∈ [35, 35.25]`,
`width = 0.1` gives `3 × 3 = 9` boxes of `0.0833°` — the old code would have made `2 × 2`
boxes of `0.1°` and silently missed the strip `[110.2, 110.25] × [35.2, 35.25]`.

---

## 5. Status of the previous block's claims

| claim | status |
| --- | --- |
| `K15-E091` certified enclosure | **repaired** (`K15-E095`). The old numbers are right to the digits quoted, because the missing slack is `~1e-18` at a fixed configuration; the *certificate* was not sound |
| `K15-E094` certified regions | **RERUN and re-certified** (`K15-E096`). `[5.872110, 5.927479]` → `[5.859536, 5.940277]`, margin `+0.096119`: the conclusion survives, the numbers moved by `0.026` as the repair predicts |
| five controls | **re-pass** with the repaired slack, width `1.2e-18` |
| a non-family configuration | **certified**: the global search's best legal completion (6 free centres, `5.898473397`) encloses to width `1.2e-10` with `R = 1.449` and a 30-plane boundedness certificate. This is the first end-to-end use of the verifier on something that is not a C5 configuration |
| the two-dodecahedra and Theorem D audits | unaffected (they use no volume) |

**The rerun is done.** With the repaired certifier, exact partition and `√3`-slack:

| region | before the repair | after the repair |
| --- | --- | --- |
| `θ ∈ [110,111] × φ ∈ [35,36]`, 100 boxes | `[5.872110, 5.927479]`, margin `+0.108692` | **`[5.859536, 5.940277]`**, margin **`+0.096119`** |
| `θ ∈ [110,110.25] × φ ∈ [35,35.25]`, 3 × 3 exact boxes | — | `[5.867852, 5.933758]`, margin `+0.104434` |

So the *conclusion* survives — the region is still certified above the threshold — while the
enclosure widened by `0.026` on each side, which is what the missing `√3` and the larger a
priori radius predict. The second row's certificate is in
`evidence/region_110_110p25.json` (1.8 kB, exact rationals rounded outward).

---

## 6. What X should check, in order

1. **W1** — the arithmetic is four lines and needs no code.
2. **W2** — that the four-vertex unbounded polyhedron is refused, and that the *old* code
   returns `4/3` for it.
3. **The radius chain of §3** — specifically that step 1 never mentions a volume.
4. **The partition** — that `n = ceil` with width `span/n` tiles exactly, and that reversed and
   empty inputs are rejected rather than returning a vacuous success.

What is *not* claimed: that any of this bounds the completion space. A finite family enclosure
does not establish the universal pair inequality, and nothing here says otherwise.

## 7. Hashes

```
source read         d289bef49fa25aea10c4c8c0c7299d5d5449fdd0
superseded          rigorous_cell_volume.py, certify_region.py  (kept for the record; the
                    suite now runs cell_certificate.py, not rigorous_cell_volume.py)
repaired verifier   Experimental/scripts/cell_certificate.py
repaired region     Experimental/scripts/certify_region_v2.py
witnesses           cell_certificate.witness_1, .witness_2  (run: python3 cell_certificate.py)
ledger              K15-E095 (repair), E096 (region repair); K15-E091 repaired, E094 pending
```

---

## 8. Beyond the C5 family: the obstruction, quantified, and the cheaper task

The brief asked, after the repair, for a rigorous tighter enclosure or a stability lemma that
advances beyond the restricted C5 family — and, if that is blocked, for a precise obstruction
and a cheaper geometric task. It is blocked, and here is the obstruction in numbers.

### 8.1 Why the sandwich cannot reach the completion space

A centre that can cut the cell lies in `2 ≤ |z − w1| < 2.603447`. Those centres are 2-separated,
so their unit balls are disjoint and lie in `B(0, 3.603)`, giving

```
N ≤ (4π/3)(3.603³ − 1)/(4π/3) = 45.8   ⟹   at most 45 free centres   ⟹   up to 135 coordinates
```

covering that space at any resolution `w` needs `(1/w)^d` boxes:

```
w = 0.1   d = 2: 1.0e2      d = 45: 1.0e45      d = 135: 1.0e135
w = 0.01  d = 2: 1.0e4      d = 45: 1.0e90      d = 135: 1.0e270
```

The atom is not the issue: at `d = 2` the whole family closes in `10^2` boxes. **The obstruction
is the dimension**, and no refinement of the sandwich touches it — even a perfect atom would
face `(1/w)^{135}`. This is the precise form of what `REVIEW_0523` §2.5 measured as the `6e5`
dependency overhead: that overhead is a *constant*, and it is irrelevant next to a `10^135`
box count.

### 8.2 The cheaper task: the shell-2 sub-problem

The C5 optimum lives in the sub-problem where **every added centre is at distance exactly `2`
from `w1`**. There the structure collapses:

- the added centres are points on a sphere of radius `2`, 2-separated, hence **`60°`-separated**;
- with `c` already a neighbour, the kissing bound allows **at most 11** of them;
- `K15-E014` (from the earlier blocks, exact) already caps the count in `[2, 2.09]` at `12`
  including the fixed ones, so at most `6` free centres lie in that inner shell;
- each must keep distance `≥ 2` from the five ring centres, i.e. lie `≥ 58.28°` from each ring
  direction.

So the shell-2 problem is *at most 11 points on a sphere with a 60° code constraint and five
forbidden caps* — 22 angular parameters under strong combinatorial restrictions, not 135 free
coordinates. `(1/w)^22` at `w = 0.01` is `10^44`, still out of reach, but the kissing constraint
means the configurations are discrete-ish rather than a continuum of independent points; that is
where a *combinatorial* enumeration (which subsets of the "gaps" are occupied) could beat a grid.

**I have not proved that the infimum over completions is attained in the shell-2 sub-problem.**
The natural argument — project a centre radially inward to distance `2`, which only strengthens
its half-space — fails on legality: the projection can land within `2` of another centre. So
shell-2 is a sub-problem, not (provably) the whole problem, and it must be labelled that way.
What the searches say is only this: seeds that were allowed to use radii up to `2.8` settled at
six free centres and never beat `5.897967`, which is the shell-2 optimum found by the C5 family.

### 8.3 The stability route, and what it would take

The alternative is a stability theorem: any cell that is not the exact icosahedral one has
volume at least `V_dod + δ` for an explicit `δ`. That is `(S_dod)`, unproved, and the one
elementary estimate available is weaker than it looks:

> **Prism lemma (true, elementary).** For any normals `n_i` and `b_i ≥ 1`, if `F_j` is the face
> of `D = ⋂{y·n_i ≤ 1}` on the plane `y·n_j = 1` with area `A_j`, then
> `vol ⋂{y·n_i ≤ b_i} ≥ vol D + A_j(b_j − 1)`.
> *Proof.* The prism `P_j = {1 ≤ y·n_j ≤ b_j, y·n_i ≤ 1 (i≠j)}` lies in the larger polytope and
> is disjoint from `D`; its volume is `A_j(b_j − 1)`. ∎

It is true for *any* normals, which is exactly why it does not help: it bounds the gain from
moving one face of a *fixed* base polytope, and the payer problem varies the normals (the ring
sits at `58.28°` instead of the icosahedral `63.43°`). Applied to the frozen cell it says only
that the volume is at least the volume of the base polytope plus a prism, and the base polytope
there is not the dodecahedron.

### 8.3b A precise obstruction: the unit-distance relaxation is 0.19 short

The one reduction that looked promising does not work, and *why* it fails is the most useful
thing in this section.

Every bisector sits at distance `b_i = |v_i|/2 ≥ 1`. Replacing each half-space by the
distance-`1` bisector in the same direction can only **shrink** the cell, so for any completion

```
vol Omega(w1)  >=  min over the six free directions of  vol( 12 faces at distance 1 )
```

— a 6-direction problem with everything at unit distance, which is the only kind of statement a
McLaughlin-type argument can see. Evaluating that relaxation at the C5 directions, certified by
`cell_certificate`:

```
CERTIFIED   vol = [5.572648770, 5.572648771]
threshold (P')  5.763417470          V_dod  5.550291029
shortfall       0.190769
```

Since this is one admissible choice of the six free directions, the relaxation's **minimum** is
at most `5.57265` — well below the threshold. So

> **No argument that uses only "every bisector is at distance ≥ 1" can prove `(P')` at the
> icosahedral pair.** It falls short by `0.19`, which is larger than the whole margin `0.135`
> that `(P')` needs.

The obstruction is not a quirk of the C5 directions: the same relaxation applied to the global
search's best **non-family** completion (6 free centres, actual cell `5.898473397`) gives a
certified base volume of `5.576078423` — also below the threshold by `0.187`. So the unit-
distance relaxation is short in both configurations tested, and the ring-excess term is needed
in both.

That is the precise reason the payer problem is a *stability* question and not a one-cell
question: the content is entirely in the five ring bisectors sitting at `1.051462` instead of
`1`, and any bound that discards that excess — including the imported dodecahedral bound and
every per-cell family tried in the earlier blocks — cannot reach the threshold. The target for
a stability lemma is now explicit: with five of twelve faces at `b = 1.051462`, the volume must
exceed `V_dod + 0.213126`.

### 8.4 One tightening attempt, measured and rejected

The sandwich bounds the normal's motion by a *box* of half-width `e`, i.e. by `√3 e`, while the
normals lie on the unit sphere and move along an arc. Measured over `0.1°` and `0.01°` boxes the
over-estimate is a constant factor:

```
0.1 deg box : sqrt(3) e = 2.961e-03 ,  true max |dn| = 1.197e-03 ,  ratio 2.47
0.01 deg box: sqrt(3) e = 2.960e-04 ,  true max |dn| = 1.197e-04 ,  ratio 2.47
```

so `2.47×` of the slack is an artefact of using a box for an arc. It is **not recoverable cheaply**:
for the pentagon centres `|v| = 2` exactly, so the parameter-Lipschitz route gives
`|n_θ| ≤ 1`, `|n_φ| ≤ sin θ`, hence `|δn| ≤ (1 + sin θ)·δθ = 3.380e-03` — **1.14× worse** than the
box bound it was meant to beat. Recovering the `2.47×` needs the actual displacement over the
box rather than a sup-norm constant, which is what the sandwich already approximates. A `2.47×`
slack reduction would cut the box count by about `6×` in two dimensions; against `10^135` that
is nothing.

**So: no tighter enclosure and no stability lemma beyond the family is delivered here.** What is
delivered is the repaired certificate, the quantified obstruction, and the shell-2 sub-problem
identified as the cheapest place to attack — with its own gap stated rather than papered over.

---

## 9. A proof (not a computation) that the C5 configuration clears the threshold

The obstruction of §8.3b says the content is in the ring's excess `b = 1.051462 > 1`. That
suggests a lemma that *uses* it, and it works.

> **Ring-excess lemma.** Let `D = {y·n_i ≤ 1, i = 1..12}` be bounded, let the faces on five
> chosen planes have areas `A_i`, and for `b ≥ 1` put `K(b) = D ∩ {y·n_i ≤ b, i ≤ 5}`. Then
>
> ```
> vol K(b) − vol D  =  5(b−1) ∫₀¹ mean(A_i(b(t))) dt  ≥  5(b−1) min_t mean(A_i) .
> ```
>
> *Proof.* Moving one face of a polytope outward at unit speed increases the volume at rate
> equal to that face's area — the added slab is the prism over the face, and the other faces
> are unchanged to first order. Here five faces move at rate `(b−1)` and the other seven do not,
> so `d/dt vol K(b(t)) = (b−1) Σ_{i≤5} A_i(b(t))`. The volume is absolutely continuous and
> piecewise `C¹` along the path (the combinatorial type may change, which does not affect the
> integral), so integrating gives the identity and hence the bound. ∎

**Applied to the C5 direction set** (`c`, the five ring at `58.2825°`, the pentagon at `112°`
with azimuth `36+72k`, the south pole), `ring_excess.py`:

```
vol D (all twelve faces at distance 1)         5.572648770477
vol K (five ring faces at b = 1.051462224238)  5.898007182910
ring face areas: 1.275974 at b=1, 1.251511 at b=1.051462
  sampled at 21 points along the path, monotonically decreasing, minimum at the end
min ring area (sampled lower bound)            1.251511009

V_dod + 5(b−1)·A_min = 5.550291029 + 0.322027701 = 5.872318729
threshold                                            5.763417470
margin                                               +0.108901
```

So **the C5 configuration satisfies `(P')` as a theorem** — `vol Ω(w1) > 5.8723 > 5.7634` —
where the previous block had only the computed value `5.898017`. The bound is weaker than the
truth by `0.026` (as it must be: it uses only `V_dod` for the base and one area lower bound),
and it is robust to the sampling: even taking the area 1 % below the sampled minimum gives
`5.8690`, still `0.106` above the threshold.

(An earlier quick run of mine reported ring areas of `1.0889`; that number was wrong — it fanned
over the face's vertices in enumeration order instead of cyclically. The area routine is checked
against the cube, where every face area is exactly `4`, and against §2's determinant volume.)

### 9.1 What this does and does not prove

- **Proves**: for the C5 direction set, with the five ring neighbours at `2.102924` and the
  other seven at `2`, the payer cell exceeds `5.763417470`.
- **Does not prove**: the inequality for other completions. The lemma applies to any direction
  set, but two things are missing for the general case: a lower bound on `vol D` when the
  completion has more than twelve faces (§8.1 allows up to 45 centres), and a lower bound on the
  ring face areas over all admissible direction sets. In the C5 set the areas are `1.25`; for a
  completion that squeezes the ring faces they could be smaller, and the bound scales with them.
- **Suggests the target**: the general statement to aim at is

  > `vol D + 5(b−1)·A_min(directions) ≥ 5.763417470` for **every** admissible direction set,

  i.e. a lower bound on a *product* of the base volume and the ring face areas. That is a
  different object from the stability statement of §8.3, and it is the concrete form the
  obstruction of §8.3b suggests.

---

## 10. The reduction the lemma gives: `(P')` becomes a face-area inequality

The ring-excess lemma applied with `vol D ≥ V_dod` gives, for **any** completion whose cell has
exactly twelve faces,

```
vol Omega(w1)  >=  V_dod + 5 (b − 1) · A_min ,      b = 1.051462224238
```

so the inequality `(P')` follows as soon as `A_min`, the smallest area of the five ring faces in
the unit-distance polytope, clears

```
A*  =  (5.763417470 − 5.550291029) / (5 · 0.051462224238)  =  0.828283 .
```

That is a **geometric inequality about five face areas**, and it is not tight in practice:

| configuration | faces | ring face areas | `A_min` | margin `A_min − A*` |
| --- | --- | --- | --- | --- |
| C5 (`θ=112°`, centre distance `2`) | 12 | `1.275974` ×5 | `1.275974` | `+0.448` |
| global search best, non-family | 12 | `1.2748 … 1.2794` (min `1.249221`) | `1.249221` | `+0.421` |

Both are certified, both clear the requirement by a factor of about `1.5`, and the resulting
bounds are `5.872319` (C5) and `5.871765` (non-family) — each about `0.109` above the threshold.

### 10.1 Status, stated precisely

- **Proved**: `(P')` at the icosahedral pair for every completion whose cell has exactly twelve
  faces and whose ring-face areas are at least `0.828283`. Both configurations ever found lie in
  this class with `50 %` slack.
- **Open (i)**: that every twelve-face completion has `A_min ≥ 0.828283`. The six free directions
  are `60°`-separated from each other and from the five ring directions; a free face at `60°`
  from a ring face can remove roughly half of it, so a *priori* the area could fall to about
  `0.6` — below `A*`. Whether six such faces can crowd one ring face simultaneously is exactly
  the question, and it is a finite sphere-packing question, not an analytic one.
- **Open (ii)**: completions with thirteen or more faces. There `vol D ≥ V_dod` is false, the
  lemma's base term shrinks, and a separate argument is needed. (§8.1 allows up to 45 centres in
  the cutting shell; the searches never found more than six free centres to be useful, but "the
  searches never found" is not a proof.)

**Numerical support for open (i), such as it is.** Sampling 400 random legal six-direction sets
(the free directions `60°`-separated from each other and from `c`, and at least `58.28°` from
each ring direction), the smallest ring face area found is `1.275974` — attained at the C5
configuration itself, which is `54 %` above `A*`. The search's best completion gives `1.249221`.
So every configuration examined has about half again the area the lemma needs. That is a
numerical observation and not a proof — 400 samples over a 12-dimensional legal set is a
gesture, not a covering — but it says the target is not knife-edge.

**Open (i) is the cheaper target of the two**, and it is the concrete deliverable I would hand
to the next block: a finite optimisation over six points on a sphere with a `60°` code
constraint, asking whether the five ring faces can be driven below `0.828283`. That is *far*
smaller than the 135-coordinate completion space, and the lemma turns it into a statement about
areas rather than volumes.

---

## 11. Theorem: `(P')` at the icosahedral pair holds for every twelve-face completion

This is the block's main positive result, and it is a proof, not a computation.

> **Theorem (`K15-E099`).** Let the icosahedral cluster be present — `c` at distance `2` from
> `w1`, five ring centres at `ρ_r = 2.102924…` in the ring directions. Let `z_1..z_6` be any
> further centres at distance `≥ 2` from `w1`, all 2-separated, and suppose `Ω(w1)` has
> **exactly twelve faces**. Then
>
> ```
> vol Ω(w1)  >  5.773718  >  5.763417470 = 2√32 − V_dod .
> ```

*Proof.*

**(1) Base polytope.** Let `D'` be `Ω(w1)` with the five ring faces moved in to distance `1`,
every other face left where it is. Note the inclusion is `D' ⊆ Ω(w1)` — pushing faces *in*
shrinks the polytope — so the volume inequality cannot come from the inclusion, and an earlier
draft of this proof wrongly wrote `D' ⊇ Ω`. What is true is stronger and simpler: **`D'` is the
Voronoi cell of `w1` with respect to the same twelve neighbours**, hence every face of `D'` is at
distance `≥ 1` and the imported Hales–McLaughlin bound gives `vol D' ≥ V_dod` directly. (That
theorem is about Voronoi cells of 2-separated point sets; it needs neither saturation nor the
full configuration.)

**(2) Ring-excess lemma (§9).** The path runs from `K(1) = D'` to `K(b) = Ω(w1)`, so moving the
five ring faces from `1` to `b = ρ_r/2` gains
`5(b−1)·mean_t A_ring(t)` where the mean is over the path and `A_ring` are the ring-face areas
of the polytope at that point. Hence

```
vol Ω(w1) = vol D' + 5(b−1)·mean_t A_ring(t) ≥ vol D' + 5(b−1)·A_min ≥ V_dod + 5(b−1)·A_min ,
```

with `A_min` the least ring-face area anywhere on the path.

**(3) A guaranteed uncut disk, at every point of the path.** Put the ring plane at distance
`R ∈ [1,b]` and take `y` on it with in-plane radius `t`, so `|y| = √(R²+t²)` and the angle
between `y` and the ring normal is `arctan(t/R)`. A centre `z` at distance `ρ` cuts `y` only if
`y·n_z > ρ/2`, i.e. only if

```
angle(y, n_z)  <  arccos( (ρ/2)/√(R²+t²) ) .
```

But `angle(y,n_z) ≥ α(ρ) − arctan(t/R)` with `cos α(ρ) ≤ (ρ² + ρ_r² − 4)/(2ρρ_r)` (the
constraint `|z − ring| ≥ 2`). So `y` is **uncut** whenever

```
arctan(t/R)  ≤  α(ρ) − arccos( (ρ/2)/√(R²+t²) ) .
```

Evaluating over `ρ ∈ [2, 2.603447]` (centres beyond cannot cut, `REVIEW_0353` §2) the worst case
is `ρ = 2` at every `R`, and the worst `R` is `b = ρ_r/2`, where the boundary is `t/R = 1/2`
exactly:

```
t* = R/2 = ρ_r/4 = 0.525731112119…      π t*² = 0.868314853691…
```

(At `R = 1` the same computation gives `t* = 0.557537`, so the minimum really is at `b`.)

The boundary at the worst point is an exact identity, which is worth recording because it is
what makes `t* = ρ_r/4` clean rather than fitted: at `t/R = 1/2`,

```
|y| = R√5/2 ,  d/|y| = 4/(ρ_r√5) = 0.85065080835204 ,
arctan(1/2) + arccos(4/(ρ_r√5)) = 26.56505118° + 31.71747441° = 58.28252559° = arccos(ρ_r/4)
```

— verified symbolically to `10^-134`. (A first version of this check used `1/√(5/4)` for
`d/|y|`, which is `cos 26.57°` and not the right quantity; the identity itself was never in
doubt, the check was.) Every
ring face of every polytope on the path therefore contains an uncut disk of area
`≥ π(ρ_r/4)² = 0.868315`, so `A_min ≥ 0.868315`.

**(4) Conclusion.**

```
vol Ω(w1) ≥ 5.550291029 + 5·0.051462224238·0.868314854
          = 5.550291029 + 0.223427069  =  5.773718097  >  5.763417470 .   ∎
```

All quantities in the chain are rational intervals from `rational_interval.py`;
`pair_theorem_12faces.py` computes it and prints `margin ≥ +0.010301`.

### 11.1 Scope, and where it stops

- **Proved**: `(P')` at the icosahedral pair for **every** completion whose payer cell has
  exactly twelve faces. No search, no enumeration, no floating point in the conclusion.
- **Not proved**: thirteen or more faces. That is not an oversight — it is where the argument
  fails, and the failure is quantifiable. Adding one face at distance `1` to the dodecahedral
  cell costs `0.052007` in volume (computed over a direction grid: `5.550291 → 5.498284`), while
  the ring-excess gain is only `0.223427`; the thirteen-face bound would be `5.721711`, which is
  `0.042` **below** the threshold. So a proof for `≥ 13` faces needs a genuinely different input,
  not a better constant here.
- **The margin is small**: `0.0103`, i.e. `0.18 %`. It is a real inequality but not a comfortable
  one, and a referee should expect it to be the first thing to break if any hypothesis is
  weakened.

### 11.2 What changed against the earlier blocks

The previous state was: `5.550291 ≤ inf vol Ω(w1) ≤ 5.897967`, threshold `5.763417`, with the
upper end a computation and no lower bound beyond the imported one. The state now is:

| class | lower bound | status |
| --- | --- | --- |
| twelve-face completions | `5.773718` | **proved** (this section) |
| thirteen or more faces | `V_dod = 5.550291` | imported only; argument fails at `0.042` short |

So the payer problem is now **solved on the twelve-face class** and open only where more than
twelve constraints are active.
