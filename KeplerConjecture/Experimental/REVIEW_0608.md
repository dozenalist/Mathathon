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
| `K15-E094` certified regions | **PENDING**. Produced with a slack short by up to `√3` and an incomplete partition. Not withdrawn as observations, not certified |
| five controls | **re-pass** with the repaired slack, width `1.2e-18` |
| a non-family configuration | **certified**: the global search's best legal completion (6 free centres, `5.898473397`) encloses to width `1.2e-10` with `R = 1.449` and a 30-plane boundedness certificate. This is the first end-to-end use of the verifier on something that is not a C5 configuration |
| the two-dodecahedra and Theorem D audits | unaffected (they use no volume) |

The repaired region run over `θ ∈ [110,111] × φ ∈ [35,36]` is in flight; its result is reported
in the final message and in `evidence/`.

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
