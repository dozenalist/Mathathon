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
repaired verifier   Experimental/scripts/cell_certificate.py
repaired region     Experimental/scripts/certify_region_v2.py
witnesses           cell_certificate.witness_1, .witness_2  (run: python3 cell_certificate.py)
ledger              K15-E095 (repair), E096 (region repair); K15-E091 repaired, E094 pending
```
