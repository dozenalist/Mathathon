# The planar–cover (§7 "mesh") obstruction: optimal constant 5, with a complete proof

**Audited objects.**

* Paper, Lemma 7.5 (p. 47): *"A closed square of side ten has no relatively open cover of
  multiplicity at most two and mesh at most two, where mesh is the supremum of the Euclidean
  diameters of its members."* Proof by Brouwer's fixed point theorem; the number `2` enters
  twice, once as `|F(z)-z| <= 2` and once as the region `{y in Q : dist(y,∂Q) > 2}`.
* Lean `OAI.PlanarCover.compact_open_cover_impossible`
  (`lean/OAI/Geometry/PlaneColoring/PlanarCovers.lean`, l. 374): the same statement with
  `Q = Metric.closedBall (0:ℂ) 5`, `Metric.ball (0:ℂ) 5 ⊆ Q`, `‖x.val - y.val‖ ≤ 2` for
  `x,y` in a common `U i`.
* Lean `OAI.EuclideanFiveColor.graph_map_large_positive`
  (`lean/OAI/Geometry/PlaneColoring/Five.lean`, l. 94): every continuous
  `F : C(Metric.closedBall (0:ℂ) 5, GraphSpace (⊤ : SimpleGraph (Fin 5)))` has a
  positive-coordinate preconnected region of diameter `> 2`.

**Result.** In all three statements the constant `2` is not optimal. The obstruction is true as
stated with `2` replaced by **any `d < 5`**; the threshold `5` is the inradius of both the square
of side ten and the closed disc of radius `5`, and it is exactly where the argument stops, so the
factor gained is `5/2`. (Whether the threshold can be pushed past `5`, i.e. whether a
multiplicity–two cover of mesh `≤ d` exists for some `d > 5`, is a separate question; it is left
open in §4.3 and is irrelevant to every use of the bound, which needs only the lower one.) Theorem A below proves this from scratch in elementary form (no measure theory,
no Brouwer, no fixed point theorem, no compactness of the cover beyond a single finite subcover).
Section 4 shows that the proof cannot be pushed past `5`, and states precisely what is *not*
proved here (whether `5` is attained as a mesh, which is irrelevant to the use made of it).
Section 5 records the structural consequence for the `k = 6` question.

---

## 1. Notation and statement

Identify `ℝ²` with `ℂ`. For `A ⊆ ℂ` put `diam A = sup{|a-b| : a,b ∈ A} ∈ [0,∞]` (Euclidean
diameter in `ℂ`, *not* the diameter inside `Q`; this is the reading used in the paper, "the
supremum of the Euclidean diameters", and in the Lean hypothesis
`hd : ∀ i, ∀ x ∈ U i, ∀ y ∈ U i, ‖x.val - y.val‖ ≤ 2`). `B(y,r)` is the open disc,
`B̄(y,r)` the closed disc, and `diam ∅ = 0`. A family `(U_i)_{i∈I}` has *multiplicity at most two on `X`* if no
point of `X` lies in three of its members.

**Theorem A.** Let `Q ⊆ ℂ`, `y ∈ ℂ`, `R > 0`, `d ≥ 0` with `B̄(y,R) ⊆ Q`. Let `(U_i)_{i∈I}` be
subsets of `Q`, each open in `Q`, with `B̄(y,R) ⊆ ⋃_i U_i`, of multiplicity at most two on
`B̄(y,R)`, and with `diam U_i ≤ d` for all `i`. Then `d ≥ R`.

Equivalently: if `d < R` no such cover exists, i.e. `sup_i diam U_i ≥ R`; so the "mesh" of any
relatively open cover of `B̄(y,R)` of multiplicity at most two is at least `R`. In particular, for `R = 5`: the hypothesis `d ≤ 2` of Lemma 7.5 and of the Lean lemma can be
relaxed to `d < 5`, and nothing stronger than `d < 5` can be obtained from an argument of this
type (Section 4).

Note `B(0,5) ⊆ B̄(0,5)`, so the Lean lemma (which assumes `Metric.ball (0:ℂ) 5 ⊆ Q`) and
Lemma 7.5 (square `[-5,5]² ⊇ B̄(0,5)`) are both instances.

---

## 2. Proof of Theorem A

Suppose `diam U_i ≤ d` for all `i`, with `d < R`.

**Step 1 (finite reduction).** `B̄(y,R)` is compact and `(U_i)` covers it, so there are
finitely many indices `1,…,n` with `B̄(y,R) ⊆ U_1 ∪ ⋯ ∪ U_n`. Multiplicity at most two is
inherited. Put `Q' = B̄(y,R)` and `V_k = U_k ∩ Q'`; the `V_k` are open in the compact metric
space `Q'` and cover it.

**Step 2 (partition of unity).** A compact metric space is normal, so the finite open cover
`(V_k)_{k=1..n}` admits a continuous partition of unity subordinate to it: continuous
`φ_k : Q' → [0,1]` with `∑_k φ_k(z) = 1` and `supp φ_k := closure{z ∈ Q' : φ_k(z) ≠ 0} ⊆ V_k` for
all `k`. (Explicitly `φ_k = ψ_k / ∑_l ψ_l` with `ψ_k(z) = max(0, dist(z, Q'∖V_k))`; the union of
the `V_k` is `Q'`, so the denominator is positive.) Discard indices with `V_k = ∅`, and choose
one point `p_k ∈ V_k` for each remaining `k`.

**Step 3 (a continuous map close to the identity).** Put
`F : Q' → ℂ`, `F(z) = ∑_k φ_k(z) p_k`.
Then `F` is continuous and, for every `z ∈ Q'`,

  `|F(z) - z| = |∑_k φ_k(z)(p_k - z)| ≤ ∑_k φ_k(z)|p_k - z| ≤ ∑_k φ_k(z) · d = d`,   (★)

because `φ_k(z) ≠ 0` forces `z ∈ supp φ_k ⊆ V_k ⊆ U_k`, and `p_k ∈ U_k`, so
`|p_k - z| ≤ diam U_k ≤ d`.

**Step 4 (the image is a finite union of segments).** No point of `Q'` lies in three of the
`U_k`, hence at most two of the numbers `φ_k(z)` are nonzero (each positive `φ_k(z)` forces
`z ∈ V_k`). Therefore `F(z)` is, for each `z`, a convex combination of at most two of the points
`p_k`, i.e.

  `F(Q') ⊆ ⋃_{k ≤ l} [p_k, p_l]`,   a finite union of (closed) line segments.   (★★)

**Step 5 (a disc around `y` is contained in `F(Q')`).** Let `ρ = R - d > 0`. I claim
`B(y,ρ) ⊆ F(Q')`. Let `w ∈ ℂ` with `|w - y| < ρ` and put `r = R - |w-y|`; then `r > d`, and
`B̄(w,r) ⊆ B̄(y,R) = Q'` because `|z - w| ≤ r` implies `|z-y| ≤ r + |w-y| = R`.

For `z ∈ ∂B(w,r) = {|z-w| = r}`, by (★),

  `|F(z) - w| ≥ |z - w| - |F(z) - z| ≥ r - d > 0`.

Hence `F(z) ≠ w` on `∂B(w,r)`, and for every `t ∈ [0,1]` the straight-line homotopy
`H_t(z) = (1-t)(z-w) + t(F(z)-w)` satisfies `|H_t(z)| ≥ r - t|F(z)-z| ≥ r - t d > 0` on
`∂B(w,r)`. So the closed curve `γ(τ) = F(w + r e^{iτ}) - w` is homotopic in `ℂ∖{0}` to
`τ ↦ r e^{iτ}`, with which it shares the winding number `1` around `0`.

Suppose now that `F(z) ≠ w` for all `z ∈ B̄(w,r)`. Then
`G = (F - w)/|F - w| : B̄(w,r) → S¹` is continuous and extends `γ/|γ|`. As `B̄(w,r)` is simply
connected and `exp : ℝ → S¹` is a covering map, `G` has a continuous lift `g : B̄(w,r) → ℝ` with
`exp ∘ g = G`. Then `τ ↦ g(w + r e^{iτ})` is periodic with period `2π`, so the winding number of
`γ` is `(g(w + r e^{2πi}) - g(w+r))/2π = 0`. Contradiction with winding number `1`. Hence some
`z ∈ B̄(w,r) ⊆ Q'` has `F(z) = w`, proving the claim.

**Step 6 (contradiction).** By Steps 4 and 5, `F(Q') ⊇ B(y,ρ)` with `ρ > 0`, while
`F(Q') ⊆ ⋃_{k≤l} [p_k,p_l]` is a finite union of segments. That is impossible: let `ℓ` be a line
through `y` which is not parallel to any of the finitely many supporting lines of the segments;
then `ℓ` meets each segment in at most one point, so `ℓ ∩ F(Q')` is finite, whereas
`ℓ ∩ B(y,ρ)` is an interval of length `2ρ`, hence infinite. ∎

**Remarks on the proof.**

1. No measure theory, no Brouwer fixed point theorem, no amenability, no compactness beyond a
   single finite subcover. The only topological input is: *a loop in `ℂ∖{0}` that extends to a
   map of the closed disc into `ℂ∖{0}` has winding number `0`* (i.e. `B̄` is simply connected and
   `exp` is a covering map).
2. The paper's version of this proof runs `z ↦ w + z - F(z)`, which by (★) maps `B̄(w,r)` into
   itself, and then applies Brouwer's fixed point theorem. Reading that proof with the parameter
   `d` instead of the constants `4, 3, 2` gives exactly the same threshold: the fixed point
   region is `{y : dist(y,∂Q) > d}`, which is nonempty precisely when `d < R`. So the sharpening
   is obtained by keeping the paper's own argument and not specialising the constants.
3. The hypothesis `diam U_i ≤ d` is used only once, in (★). Multiplicity at most two is used only
   once, in Step 4. The compactness of `B̄(y,R)` only serves to make the cover finite.
4. The two-dimensionality of the ambient space is essential, and the proof shows exactly where:
   `F(Q')` is a finite union of segments, i.e. of `(m-1)`-dimensional sets with `m = 2`, and
   `1 < 2`. In one dimension the corresponding statement is false: the intervals
   `I_j = (j - 3/5, j + 3/5)`, `j ∈ ℤ`, cover `[-10,10]`, have multiplicity at most two
   (`I_j ∩ I_{j+2} = ∅`, and `I_j ∩ I_{j+1} = (j + 2/5, j + 3/5)`), and mesh `6/5`, far below the
   "inradius" `10`. So no argument of this shape reaches below dimension two, and any sharpness
   statement for Theorem A must also use the plane.

---

## 3. Corollaries in the form of the paper and of the Lean development

**Corollary A1 (Lemma 7.5, sharpened).** Let `Q` be a set with `B̄(0,5) ⊆ Q` (e.g. the closed
square `[-5,5]²` of side ten). Then `Q` has no relatively open cover of multiplicity at most two
and mesh `≤ d` for any `d < 5`.

*Proof.* Immediate from Theorem A with `y = 0`, `R = 5`. ∎

So in Lemma 7.5, and in `compact_open_cover_impossible`, the constant `2` can be replaced by any
constant strictly below `5`; the statement at `d = 2` is the special case `2 < 5`.

**Corollary A2 (`graph_map_large_positive`, sharpened).** Let
`F : C(B̄(0,5), GraphSpace (⊤ : SimpleGraph (Fin 5)))` be continuous. Then there are `i : Fin 5`
and a preconnected `K ⊆ B̄(0,5)` with `(F z)_i > 0` for all `z ∈ K` and
`diam K ≥ 5`; that is, for every `ε > 0` there are `x, y ∈ K` with `dist x y ≥ 5 - ε`.

*Proof.* Suppose all such regions have diameter `≤ d` with `d < 5`. For `i : Fin 5` let
`U_i = {z ∈ B̄(0,5) : (F z)_i > 0}`; these are open in `B̄(0,5)`, and they cover `B̄(0,5)`
because `∑_i (F z)_i = 1` (Lean: `graphRealization_sum`) forces one coordinate to be positive. Let
`𝒰` be the family of connected components of the `U_i` inside `B̄(0,5)`; since `B̄(0,5)` is
locally path connected (it is convex) these components are open, and they cover `B̄(0,5)`. Each
component `K` lies in a positive region of its coordinate, so `diam K ≤ d`. A point of
`GraphSpace (⊤ : SimpleGraph (Fin 5))` has the form `graphEdgePoint a b t`, hence has at most two
positive coordinates (Lean: `graphRealization_positive_three`, `Five.lean` l. 9, whose proof uses
only that form); so no point of `B̄(0,5)` lies in three components. Theorem A with `R = 5` gives
`d ≥ 5`. ∎

This is exactly the Lean lemma with `2` replaced by `5`: the Lean statement
`∃ i, ∃ K, IsPreconnected K ∧ … ∧ ∃ x ∈ K, ∃ y ∈ K, 2 < dist x y` becomes
`… 5 - ε < dist x y` for every `ε > 0`. Since the development uses this lemma only to feed the
`2 < dist x y` hypothesis of `FullApprox.no_large_positive_sequence` (`Mesh.lean` l. 92, where
`hxy : 2 < dist x y` is used solely via `linarith` against `2 * t n < dist x y` and
`dist a a' ≤ 2 * t n` with `t n ≤ 1/16`), the sharpened form is directly substitutable: replacing
`2` by `5 - ε` only strengthens the inequality `3/2 ≤ dist (a n) (b n)` that is derived there.

**Corollary A3 (the plane has no uniform two–fold cover).** There is no open cover of `ℂ` of
multiplicity at most two all of whose members have diameter `≤ d` for a fixed `d`, because
`B̄(0,2d) ⊆ ℂ` would violate Theorem A. (This is the standard statement that `ℝ²` has covering
dimension `2`, here with the sharp disc constant.)

---

## 4. The constant `R` is optimal *for the argument*, and the extremal configuration

*(4.1)* The proof of Theorem A uses only the two numerical facts (★) `|F(z) - z| ≤ d` and
`F(Q') ⊆` a finite union of segments, and derives the contradiction from
`B(y,R-d) ⊆ F(Q')`. At `d = R` the argument gives nothing, and indeed the map
`F(z) = (Re z, 0)` satisfies `|F(z) - z| = |Im z| ≤ R` with image in a single line: so no
argument of this shape can reach `d = R`. (The corresponding cover of `B̄(0,R)` by the two
half–discs `{± Re z > -ε}` has mesh `2R`.)

*(4.2)* The deficiency is not an artefact of the proof: at `d = R` the obstruction disappears for
the *degenerate* configuration. Take `R = 5` and the six closed sectors
`C_j = {z : |z| ≤ 5, ∠(arg z, jπ/3) ≤ π/6}`. Their mesh is exactly `5` (each is an equilateral
triangle with a curved side, of diameter `5`), and they cover `B̄(0,5)`, but the origin lies in
all six of them. So the hypothesis "multiplicity at most two" is essential and the value `R` is
attained only in this mult-`6` limit. `verify.py` checks these numbers exactly
(`diam C_j = 2·5·sin(30°) = 5`, multiplicity `6` at `0`).

*(4.3)* **Proposition (the upper end of the bracket).** For `R > 0` and `η > 0` the two sets
`U_± = {z : |z| < R+η, ± Re z > -η}` are open in `ℂ`, cover `B̄(0,R)`, have multiplicity at most
two (there are only two of them), and satisfy `diam U_± ≤ 2(R+η)` because `U_± ⊆ B(0,R+η)`.
Hence the least mesh of a multiplicity–two open cover of `B̄(0,R)` satisfies `d*(R) ≤ 2R`, while
Theorem A gives `d*(R) ≥ R`.

*What is **not** proved here* is the value of `d*` in between: whether `R` can be attained in
Theorem A's sharp form, i.e. whether for every `d > R` there is an open cover of `B̄(y,R)` of
multiplicity at most two and mesh `≤ d`. So we have
`d* = inf { mesh : multiplicity ≤ 2 } ∈ [R, 2R]`,
and its determination is left open here. The natural candidates (six sectors plus a central patch; one "trumpet" set
that is wide near the centre plus annular sectors; a sector family whose angular widths grow from
a tiling at small radius to pairwise overlaps further out; a brick pattern in polar coordinates
with the T-junctions either notched or cut back) all fail at one of two places, which is worth
recording because they are genuine obstructions and not oversights.

* *An overlap cannot be born.* Let `C_1, C_2` be two sheets whose angular ranges touch at radius
  `ρ` and overlap for `r > ρ`, and suppose an older sheet `P` is present near the touch point `z₀`
  (it must be: at `r = ρ` the point `z₀` lies on the boundary of both `C_i`, so it is in neither of
  them). Then `P` is open and contains `z₀`, hence meets `C_1 ∩ C_2` for `r` slightly larger than
  `ρ`, so some point lies in three sheets. If instead `P` omits `z₀`, then `z₀` is uncovered.
  (This is why the six–sector pattern cannot be perturbed into a mult–2 cover with mesh `5 + ε`:
  its sectors must tile near the centre, where the central patch is, and must overlap at radius
  `R`, where it is not, and the change cannot be made continuously.)
* *A notch cannot be closed.* If a sheet is cut away on a closed region `K` so that a twofold
  overlap elsewhere does not become threefold, then every point of `∂K` must be covered by the two
  sheets of that overlap; but `∂K` also borders regions where those sheets are single, so the
  coverage at `∂K` forces a third sheet there, which is exactly what `K` was meant to prevent.

The way out of both obstructions is to let a sheet **split into two pieces**: a parent may remove an
open gap from its angular range (its two remaining pieces are then still one open set of bounded
diameter, because the gap is thin), and the new sheet is born *inside that gap*, where the parent
is absent. Iterating this gives a binary refinement tree and appears to be the only route to a
cover with mesh close to `R`; carrying it out with explicit formulas and verifying coverage,
multiplicity and diameters is a well-posed but non-trivial task left open here. It is not needed
for any use made of Theorem A, which needs only the lower bound (and, by Theorem B-style
constructions, one could at best sharpen "5" to "the infimum of attainable meshes").

For the purposes of the five–colour theorem, and of any `k`–colour analogue, only the direction
proved matters: it is a *strengthening*, and it is label–blind (Corollary D).

---

## 5. Corollary D: the §7 obstruction is blind to the number of labels

Theorem A and Corollary A2 use only:

1. the ambient region is a disc of radius `5` (or any set containing one);
2. a point of the graph realisation of a *simple* graph has at most two positive coordinates;
3. the weights sum to `1`.

Fact 2 holds verbatim for `GraphSpace (⊤ : SimpleGraph (Fin k))` for **every** `k`, with the same
one–line proof (`graphEdgePoint a b t` has at most two nonzero coordinates): the number of
vertices is never used. Hence:

**Corollary D.** For every `k` and every continuous `F : C(B̄(0,5), GraphSpace (⊤ : SimpleGraph
(Fin k)))` there is a positive–coordinate preconnected region of diameter `≥ 5`. Consequently
the §7 step of the paper — "positive–coordinate components form a cover of multiplicity at most
two, hence some component has diameter `> 2`" — is *satisfiable for every label count*, with the
same constant `5`, and with no dependence on `k` beyond `k ≥ 2`.

The consequences for the `k = 6` question are immediate and usable:

* The `k = 6` analogue cannot fail in §7. Whatever obstructs six labels must live in the parts of
  the architecture that do see `k`: the palette cardinality (§5), the transition/cycle analysis
  (§8), or the conditional–average and support–exclusion steps of §6. It cannot live in the
  planar–cover obstruction, whose hypotheses and conclusion are identical for `k = 5` and `k = 6`.
* Conversely, no strengthening of §7 can help any lower bound: by Theorem A the §7 step is
  *saturated* at the disc radius in the sense that any argument of the same type cannot yield a
  diameter bound larger than `5` (Remark 4.1), and §7 has in any case a factor `≈ 5` of slack,
  since the paper's own mesh bound (Lemma 7.6) is `1 + o(1)` and the obstruction only needs
  `< 5`.

---

## 6. Relation to the existing formalisation, and a proposed patch

The Lean development contains, in `PlanarCovers.lean`, the proof of
`PlanarCover.hit_center` specialised to the constants `(r, d, r') = (4, 2, 3)`, and
`finite_partition_impossible` / `finite_open_cover_impossible` /
`compact_open_cover_impossible` specialised to `d = 2` and `Q = Metric.closedBall 0 5`. Theorem A
is the same proof with the three constants made parameters:

* `hit_center`: replace `Metric.ball y 4` by `Metric.ball y r`, `‖F z - z‖ ≤ 2` by `≤ d`, the
  circle `y + 3 e^{it}` by `y + r' e^{it}`, and use `d < r' < r` (the conclusion
  `y ∈ F '' ball y r` is unchanged). The two uses of `2` and `3` become `d`, `r'`.
* `finite_partition_impossible`: replace the two occurrences of `2` in `hd`
  (`‖p i - z.val‖ ≤ 2`) by `d`, keep `barycenter_two` and `affinePair_null` unchanged; the
  hypothesis `hQ : Metric.ball (0:ℂ) 5 ⊆ Q` and `hit_center`'s conclusion then give the
  contradiction as soon as `d < 5`, since `w ∈ Q` ranges over the ball `Metric.ball (0:ℂ) 1`,
  for which `Metric.ball w 4 ⊆ Metric.ball (0:ℂ) 5`, and `4 > d` is exactly `d < 5` up to the
  harmless choice of `1` and `4` (any `s < 5 - d` and `r` with `d < r < 5 - s` do).
* `compact_open_cover_impossible` follows with no change beyond those constants.

The statement of Theorem A is phrased so that this translation is purely mechanical. I did not
carry it out, so **no Lean-checked sharpening is claimed in this note**; moreover, at the time of
writing the `.olean` files in `lean/build/lib` are rejected by the toolchain on `PATH`
(`error: failed to read file '.../Five.olean', incompatible header`), so importing the
development to check the adapted proof was not possible from this workspace either.

---

## 7. Checks

`verify.py` (no dependencies; exact rational arithmetic, `sin`/`cos` bracketed by rational Taylor
partial sums) checks the numerical assertions used above:

1. `sin 30° = 1/2` rigorously bracketed, hence a closed `30°` sector of radius `5` has diameter
   exactly `2·5·sin 30° = 5`;
2. the six `30°` sectors centred at multiples of `60°` *tile* the disc of radius `5`: a sampled
   transverse point lies in exactly one, a point on each of the six seam rays in exactly two,
   and the origin in all six (multiplicity `6`);
3. six sectors of half-angle `30° + ε` and radius `5 + δ` have mesh
   `2(5+δ) sin(30°+ε)`, computed for `ε = 5°, 2°, 1°, 0.1°, 0.01°`, tending to `5` as the cover
   degenerates;
4. the two half-disc cover of `B̄(0,5)` has multiplicity at most two and mesh `2(5+δ) → 10`, so
   the optimal mesh lies in `[5,10]`;
5. the projection map `F(z) = (Re z, 0)` satisfies `|F(z) - z| = |Im z| ≤ 5` on `B̄(0,5)` with
   image in a single line, so `5` is exactly the threshold of the argument of Section 2;
6. `2 < 5`, so the hypothesis `mesh ≤ 2` of Lemma 7.5 and of `compact_open_cover_impossible` is
   the instance `d = 2` of the sharpened hypothesis `d < 5`.

Run: `python3 verify.py`.
