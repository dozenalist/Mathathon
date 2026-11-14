# §7 at six colours

**The cyclic locus of a weak measurable 6-colouring is non-empty and √2-dense;
the interface obstruction of §7 costs exactly one finiteness input, and every
other step of §7 transfers to k = 6 with no new geometry.**

Member m5, swarm `smwfo9zkl`. Direction d4: *nonemptiness of the cyclic locus at
k = 6*. Files: this document, `verify.py` (all checks), `hex_locus_check.py`
(non-vacuity on the known 7-colouring), `triangle_stratum.py` and
`cycle_strata.py` (exact stratification at a cyclic centre, k = 5 versus k = 6),
`paper/render.py` (rendered-page reader used for the formula checks).

---

## 0. Results

Throughout, `k >= 3`, `c : R² → I = {1,…,k}` is a **weak measurable**
colouring in the sense of Definition 1.2 of the paper (p. 2), `P_x(e)` is the
maximal palette of Definition 5.1 (p. 26), `Γ_x` is the transition graph of
Definition 6.1 (p. 34), and

```
L = L(c) = { x ∈ R² : Γ_x contains a cycle }.                                 (6.4)
```

**Theorem A (Theorem 4.1 below).** *For every `k >= 3` and every weak measurable
`k`-colouring, `L` meets every closed square of side `> 2`. Consequently `L` is
√2-dense in the plane: every closed disk of radius `> √2` meets `L`. In
particular `L ≠ ∅`.*

At `k = 6` this settles the nonemptiness half of the missing prerequisite
stated in the problem: **there is no 6-colouring, and no `k`-colouring at all,
whose transition graphs are acyclic everywhere.** Any counterexample to local
finiteness at `k = 6` must therefore be a colouring with `L` √2-dense and
accumulating.

**Theorem B (Theorem 5.1 below).** *Fix `k = 6`. Suppose*

  **(F)** *some closed square `Q₀` of side `> 2` meets `L` in finitely many points.*

*Then the conclusion of Proposition 7.1 (p. 42) holds at `k = 6`: there are
`ℓ ∈ {3,4,5,6}`, distinct labels `i₀,…,i_{ℓ−1} ∈ I`, a point `x ∈ L ∩ Q₀`,
a radius `ρ < side(Q₀)/2`, and for every edge `i_j i_{j+1}` a compact connected
`K_j ⊆ \overline{B(x,ρ)}`, a direction `v_j`, and a sequence `q_{j,k} → x` with
(i) `x ∈ K_j`, `K_j ∩ ∂B(x,ρ) ≠ ∅`; (ii) `(q_{j,k}−x)/|q_{j,k}−x| → v_j`;
(iii) `H_{i_j} ∩ Δ(K_j) = H_{i_{j+1}} ∩ Δ(K_j) = ∅`.*

So `§7` transfers to six colours **given (F) and nothing else**: no palette
bound, no binarity, no single-centre constraint, no `|P| ≤ 2`, no new geometry.
The implications among the candidate inputs are

```
local finiteness of L  ⟹  (F)
a point of L isolated at radius > √2  ⟹  (F)  ⟹  L ≠ ∅,
```

and no arrow reverses: (F) says nothing about `L` outside one small square, so
it is *strictly* weaker than local finiteness (take a colouring whose `L` is
locally finite inside one square and a continuum elsewhere); a point isolated at
radius `> √2` gives (F) by taking a closed square of side `> 2` inside its
isolating ball, and `(F) ⟹ L ≠ ∅` is not immediate from the definition but is
forced by Lemma 7.6's argument (§5, step 3). (F) is the precise weakening that
restores the paper's route; it is the Step-4 deliverable of the sprint brief.

**Theorem C (Theorem 3.1 below).** *If a closed square of side `s` has a
relatively open cover of multiplicity at most 2 and mesh at most `m`
(`m` = supremum of Euclidean diameters), then `s ≤ 2m`.*

This is Lemma 7.5 of the paper (p. 47) with its constants kept instead of
rounded to `s = 10, m = 2`. The invariance in `s` is what lets the §7 machine
run at an arbitrarily small scale, and hence what makes (F) — rather than
local finiteness — the right hypothesis. Proof: the printed Brouwer argument;
no new idea.

**Verdict on direction d4.** The question "is there a reduced palette model at
`k = 6` in which `Γ_x` is acyclic for every `x`?" is answered **no**, for every
`k`, by Theorem A. The answer is a theorem, not a construction, and it does not
depend on any of the fragile finite models.

**Two corrections to the record** (both verified against rendered pages):

1. `results/K6-BARRIER.md` §2 justifies the failure at `k = 6` with "a cover of
   the square by tiny disks has mesh tending to zero and multiplicity one".
   That is false: a relatively open cover of a *connected* space of
   multiplicity 1 is a one-member cover, and by Theorem C no cover of a square
   of side `s` with multiplicity `≤ 2` has mesh `< s/2`. The *conclusion*
   of that paragraph stands, for a different reason noted in Remark 2.3.
2. §7 contains three `k`-dependent constants, listed in §2 below; one of them
   (`α < 1/5`) is a genuine numerical error at `k = 6` and must become
   `α < 1/6`. This does not appear in the barrier document.

---

## 1. The objects at `k = 6`, written out

Taken verbatim from the paper, specialised to `k = 6` and `I = {1,…,6}`; I
checked each displayed formula against a rendered page (`paper/render.py`, a
`mutool -F stext` reader that reports baseline shifts and font-size changes, so
that sub/superscripts and stacked fractions are visible; see §7).

* `S = S¹` with normalized arc measure `σ`; `A_i = c^{-1}(i)`; `R` = rotation by
  `κ = π/3`; `J` = rotation by `π/2`. Directions `e, v` are *parallel* if
  `v = ±e`.
* **Typical point**: a point of density one of its own colour (conull). By
  Lemma 4.3 (p. 25) *no unit pair of typical points has the same colour*; the
  lemma is stated for a weak measurable `k`-colouring with arbitrary `k`.
* **Traces and palettes** (Definition 5.1, p. 26): `W_x ⊆ L^∞(S; R⁶)` is the
  weak-\* closed set of limits of `(a_i(y_n + r_n e))_{i∈I}` along typical circle
  samplings `y_n → x`, `r_n → 1`. `D_{x,i} = ess⋃_{b∈W_x}{b_i > 0}` and
  `P_x(e) = {i : e ∈ D_{x,i}}`, defined up to angular null sets.
  `1 ≤ |P_x(e)|` a.e. (any trace sums to 1). At `k = 6` the established
  general-`k` bound `|P_x(e)| ≤ k−3 = 3` holds (`results/K6-BARRIER.md` §1);
  **Theorem A and Theorem B do not use it.**
* **Transition graph** (Definition 6.1, p. 34): with
  `D_{ij}(B,h) = |{q ∈ B : (c(q), c(q+h)) ∈ {(i,j),(j,i)}}|` and `B` ranging over
  balls centred at `x`,
  ```
  ij ∈ Γ_x  ⟺  ∀B  limsup_{h→0, h≠0} D_{ij}(B,h)/|h| > 0.                   (6.1)
  ```
  Edge-presence loci are closed (paper, p. 34), so `L` is closed.
* **An edge has an avoiding trace** (Lemma 6.2, p. 35): `ij ∈ Γ_x` implies
  `P_x(e) ⊄ {i,j}` for a.e. `e`. This is the only place the graph meets the
  palettes, and it is label-blind.
* `H_i = {q : |A_i ∩ B(q,r)| > 0 ∀r > 0}`; `ij ∈ Γ_x ⟹ x ∈ H_i ∩ H_j`.

---

## 2. Hypothesis audit: what §7 actually uses, and its status at `k = 6`

`§7` occupies pp. 42–50. Every ingredient, with what it needs and whether `k`
enters:

| paper step | page | what it uses | status at `k = 6` |
|---|---|---|---|
| Definition 1.2, Lemma 4.3 | 2, 25 | weak measurability, unit-distance properness of typical points | stated for arbitrary `k`; unchanged |
| (7.1) straddling region `Δ(K)` | 42 | connectedness of `K` | none; unchanged |
| Lemma 7.2 `p^ε_i(q)+p^ε_i(z) ≤ 1` | 43 | disk averages, Lemma 4.3 | none; unchanged |
| Lemma 7.3 missing edge ⇒ small overlap | 44 | (6.1)'s negation, circle-average Fourier bound (6.3), Cauchy–Schwarz | none: the label set is never counted; unchanged |
| (7.4) `q^ε_i = (p^ε_i − α)_+ / Σ_k (p^ε_k − α)_+` | 45 | **`0 < α < 1/5`** because "the five probabilities sum to one" | **becomes `0 < α < 1/6`**: `Σ_k (p_k−α)_+ ≥ 1 − 6α > 0`. Also `R⁵ → R⁶` |
| `G` = one-skeleton of the simplex | 45 | **"complete graph on its five vertices"** | complete graph on **6** vertices; still finite, simple, connected — exactly Lemma 7.7/7.8's hypotheses |
| Lemma 7.4 (1) core disks at `L₀` | 45 | `L₀ = L ∩ Q'` **finite** (Theorem 6.5) | **not available at `k = 6`** — this is the only gap |
| Lemma 7.4 (2) `q^ε` graph-valued on `Q ∖ ⋃H` | 45 | "finitely many nonedges"; positive coordinates form a clique in a forest, "therefore number at most two, and a two-element set is a forest edge" | **label-blind**: a forest has no 3-clique for every `k`; unchanged |
| Lemma 7.4 (3) tree filling | 45–46 | connected boundary image lies in one component *tree*; a finite tree is contractible | label-blind; unchanged |
| Lemma 7.4 total radii `|L₀|δ + m + η` | 46 | **finiteness of `L₀`** (via `|L₀|`) | the second use of the same gap |
| Lemma 7.5 cover obstruction | 47 | pure topology (Brouwer) | **true for every `k`**; sharpened in Theorem C |
| Lemma 7.6 non-null core loop | 47 | components of `{g̃_i > 0}`, multiplicity ≤ 2 because "every point of `G` has at most two positive coordinates"; mesh `≤ 1+o(1)` | label-blind; unchanged. Its last sentence, "This argument also rules out the possibility of having no core disks in `Q`", is the seed of Theorem A |
| Lemmas 7.7, 7.8 | 48 | finite connected simple graphs, reduced words, annulus topology | none; unchanged |
| Prop. 7.1 proof | 49–50 | "finitely many simple cycles in the complete graph on five vertices … `ℓ ∈ {3,4,5}`"; midpoint coordinates `1/2 > α`; `x ∈ L₀ ∩ int Q`; `ρ` with `B(x,ρ) ⊂ int Q` free of other points of `L₀` | `ℓ ∈ {3,4,5,6}`; `α < 1/6` gives `1/2 > α`; the last two again need `L₀` finite |

**Summary of the audit.** Of §7's inputs, exactly one is `k`-dependent in a way
that is not a constant to be changed: **the finiteness of `L ∩ Q'`**. Everything
else is either label-blind or a numerical constant (`α < 1/6`, six vertices,
`ℓ ≤ 6`). In particular

> §7 uses neither the palette bound `|P_x(e)| ≤ k−3`, nor Proposition 5.6, nor
> Lemma 5.5, nor binarity, nor any single-centre constraint.

**Remark 2.3 (why `k = 6` breaks §7 but not the cover lemma).** At `k = 6` a
palette may carry three labels, so `q^ε` is a map into the *2-skeleton* of the
6-simplex. The multiplicity-2 hypothesis of Lemma 7.5 then becomes multiplicity
3, and a multiplicity-3 cover of a square by sets of arbitrarily small diameter
does exist — that is the Lebesgue covering dimension of the plane being 2. The
correct statement of the failure is therefore: *the multiplicity bound is what
`k = 6` destroys*, not the mesh bound. The mesh bound `1 + o(1)` is twice the
unit distance and cannot be improved at any `k`.

---

## 3. Theorem C: the cover obstruction in scale-invariant form

**Theorem 3.1.** Let `Q ⊂ R²` be a closed square of side `s > 0`, and let
`{U_a}` be a relatively open cover of `Q` with multiplicity at most 2 and mesh
at most `m`, where mesh is the supremum of the Euclidean diameters of the
members. Then `s ≤ 2m`.

The paper (Lemma 7.5, p. 47) proves the special case `s = 10, m = 2`:
`10 ≤ 4` is false, so no such cover exists. The proof below is the printed one
with the two constants kept rather than instantiated. I reproduce it because
the invariance in `s` is the whole point for `k = 6`.

*Proof.* By compactness pass to a finite subcover `U_1,…,U_N` with the same
bounds. Choose `z_a ∈ U_a`. Since `s > 2m ≥ m` with `m ≥ 0`, we have
`diam Q = s√2 > s > m`, so no `U_a` equals `Q`, so `dist(z, Q∖U_a)` is defined; normalise these distances
to a continuous partition of unity `φ_a`, so that `φ_a(z) > 0 ⟹ z ∈ U_a`. Put

```
F(z) = Σ_a φ_a(z) z_a .
```

`F(Q) ⊆ Q` by convexity. At each `z` at most two weights are positive
(multiplicity ≤ 2), so `F(z)` lies in the segment `[z_a, z_b]` (or at a vertex
`z_a`) for the at most two members containing `z`; hence

```
F(Q) ⊆ ⋃_{a≤b} [z_a, z_b],  a finite union of closed segments,           (3.1)
|F(z) − z| ≤ Σ_a φ_a(z) |z_a − z| ≤ m   (z ∈ U_a ⟹ |z_a − z| ≤ diam U_a ≤ m).  (3.2)
```

Take `y ∈ Q` with `dist(y, ∂Q) > m`. By (3.2), the continuous map
`h(z) = y + z − F(z)` satisfies `|h(z) − y| = |z − F(z)| ≤ m`, so `h(Q) ⊆ B(y,m)
⊆ Q`; the Brouwer fixed point theorem in the plane gives `z` with `h(z) = z`,
i.e. `F(z) = y`. Therefore

```
{ y ∈ Q : dist(y, ∂Q) > m } ⊆ F(Q) ⊆ (a finite union of segments).
```

If `s > 2m`, the left-hand side contains the open square of side `s − 2m > 0`
concentric with `Q`, which is non-empty and open. But a closed segment has
Lebesgue measure zero in `R²`, so a finite union of them is null and cannot
contain a non-empty open set. Hence `s > 2m` is impossible, i.e. `s ≤ 2m`. ∎

The mesh bound supplied by Lemma 7.6 is `≤ 1 + o(1)`, so Theorem 3.1 gives
`s ≤ 2 + o(1)`: **the §7 machine needs a closed square of side `> 2`, and no
larger.** The constant cannot be lowered by this route, because the bound `1` in
the mesh estimate is the unit distance itself (Lemma 7.2 forces
`p^ε_i ≤ 1 − α` at a point at distance 1 from a point where `p^ε_i > α`).

---

## 4. Theorem A: the cyclic locus is √2-dense

**Theorem 4.1.** Let `k >= 3`, let `c` be a weak measurable `k`-colouring, and
let `L` be given by (6.4). Then every closed square of side `> 2` meets `L`.
Hence `L` is √2-dense.

The only requirement on `k` in the proof is that the 1-skeleton of the simplex
on `I` is connected, i.e. `k ≥ 2`; the argument never counts labels otherwise,
and it uses no palette bound.

*Proof.* Suppose for contradiction that `Q₀` is a closed square of side `s > 2`
with `L ∩ Q₀ = ∅`. Choose a closed square `Q ⊂ int Q₀` of side `s'` with
`2 < s' < s`, and put `Q' = Q₀`. Then `L ∩ Q' = ∅`, so for every `z ∈ Q'` the
graph `Γ_z` is a forest; in particular `L₀ := L ∩ Q' = ∅`.

*Step 1: the graph-valued approximation.* Apply Lemma 7.4 (p. 45) with `L₀ = ∅`
and the `α ∈ (0, 1/6)` of §2. Its proof runs verbatim: `M_δ = Q' ∖ ∅ = Q'` is
compact and every `Γ_z`, `z ∈ M_δ`, is a forest; for each nonedge of `Γ_z`
Lemma 7.3 supplies a ball on which the simultaneous threshold violations are
covered by finitely many disks of total radius `o(1)`; finitely many balls
`B(z, s_z)` cover `M_δ`. At any point of `M_δ` outside the marked disks, the
positive coordinates of (7.4) form a clique in the forest of each selected ball
containing that point — **a clique in a forest has at most two vertices, and a
2-element clique is an edge of that forest** — so `q^ε` takes values in the
1-skeleton `G` of the simplex on `I`, which is the complete graph on `k` vertices.

Merging disks as in the paper (the number of disks is finite, so the enlargement
errors sum to less than any prescribed `η`), we obtain finite families `H_n` of
open disks with pairwise disjoint closures, total radii

```
|L₀| δ_n + m_{δ_n,ε_n} + η_n = m_{δ_n,ε_n} + η_n ⟶ 0,                      (4.1)
```

and, for all large `n`, a continuous map

```
g_n : Q ∖ ⋃_{x ∈ L₀ ∩ Q} B_{n,x} = Q ⟶ G                          (7.5 for k = 6)
```

equal to `q^{ε_n}` outside all open disks of `H_n`, and graph-valued there.
This is Lemma 7.4's assertion (3) with the index set `L₀ ∩ Q` empty; the one
`k`-dependent constant was `α`, already replaced by `α < 1/6`.

*Step 2: no null homotopy is possible.* Lemma 7.6 (p. 47) states that for all
large `n` some core disk in `Q` has a boundary loop whose `g_n`-image is not
null homotopic in `G`. Its proof assumes the contrary. Here there are no core
disks at all, so the assumption "all core boundary loops are null homotopic" is
vacuous and the proof applies with `g̃_n = g_n : Q → G` (no extension needed).
The paper records the conclusion explicitly: *"This argument also rules out the
possibility of having no core disks in `Q`."*

Concretely: for `i ∈ I` let `U_{n,i}` be the components of the relatively open
set `{z ∈ Q : (g_n(z))_i > 0}`. These are open and path connected, and they
cover `Q` with **multiplicity at most 2**, because every point of the 1-skeleton
has at most two positive barycentric coordinates — for every `k`. The mesh of
this cover is at most `1 + o(1)`: if two points `a_n, b_n` of one component
`U_{n,i}` were at distance `> 1 + c`, the path between them must cross a point at
exact distance one from a limiting point `a ∈ H_i` outside the (vanishing) holes;
Lemma 7.2 then gives `p^{ε_n}_i ≤ 1 − α` there, whence
`α |A_i ∩ U| ≤ ‖p^{ε_n}_i − a_i‖_{L¹(U)} + α|E_n ∩ U| → 0`, contradicting
`a ∈ H_i`. (This is the printed proof; `E_n` is the union (7.6) of the annuli
of the holes, `|E_n| ≤ 4π Σ r → 0`.)

*Step 3: the obstruction.* For all large `n` the cover `{U_{n,i}}` of `Q` is
relatively open, of multiplicity at most 2, and of mesh at most `m_n` with
`m_n → 1`. By Theorem 3.1, `s' ≤ 2 m_n`; letting `n → ∞`, `s' ≤ 2`. But
`s' > 2`. Contradiction. Hence no closed square of side `> 2` is disjoint from
`L`. ∎

**Corollary 4.2.** `L ≠ ∅`, and for every `p ∈ R²` and every `ρ > √2` the disk
`B(p,ρ)` meets `L`; equivalently `dist(p, L) ≤ √2`.

*Proof.* A closed disk of radius `ρ` contains a closed square of side `ρ√2`, and
`ρ√2 > 2 ⟺ ρ > √2`. ∎

**Corollary 4.3 (six colours).** Every weak measurable 6-colouring has a
non-empty, √2-dense cyclic locus. By Theorem 1.3 of the paper (p. 2, valid for
every `k`) a proper 6-colouring of `R²` exists iff a weak measurable 6-colouring
does, so: **if the plane is 6-colourable, then some 6-colouring has a cyclic
centre within distance √2 of every prescribed point.** No 6-colouring can have
`Γ_x` acyclic everywhere.

(One caveat on the shape of the statement, since `Γ_x` is defined through
circle averages: `Γ_x` and `L` are objects attached to a *weak measurable*
colouring, and Theorem 1.3 is an existence transfer, not a per-colouring one.
So Theorem 4.1 is a theorem about weak measurable colourings, exactly like
Theorem 1.4 of the paper, and Corollary 4.3 is the corresponding statement for
proper 6-colourings.)

**Remark 4.4 (the constant).** `√2` is what the method gives: the mesh bound
`1` of Lemma 7.6 comes from Lemma 7.2's inequality at the unit distance, and
Theorem 3.1 converts a mesh bound `m` into the square side `2m`. It is *not*
sharp for any particular colouring: for the hexagonal 7-colouring `L` is a discrete lattice of mesh
`√3·(2/5) = 0.693` (§6). So Theorem 4.1 is a universal statement of the right
order of magnitude, not an optimal one.

**Remark 4.5 (what this does and does not settle).** Corollary 4.2 answers
"does a 6-colouring have a cyclic centre?" in the affirmative, for every `k`.
It does *not* produce a locally finite `L`, nor even an isolated point of `L`;
and Theorem 5.3 shows that finiteness, not non-emptiness, is what §7 needs. So
the sprint brief's "single missing prerequisite" should be restated: the
missing prerequisite is **not** non-emptiness of `L`, it is (F) of Theorem B.

---

## 5. Theorem B: exactly which finiteness input §7 needs

**Definition 5.0.** For a closed `L ⊆ R²`, say **(F)** holds if some closed
square `Q₀` of side `> 2` meets `L` in finitely many points.

**Theorem 5.1 (transfer of §7 to six colours).** Let `c` be a weak measurable
6-colouring and assume (F) for its locus `L`. Then the conclusion of
Proposition 7.1 holds at `k = 6`, with `ℓ ∈ {3,4,5,6}` and `α ∈ (0,1/6)`; the
constants `2` in the side of `Q₀` and `ρ < side(Q₀)/2` are the only changes to
the printed statement.

*Proof.* Run the printed proof of Proposition 7.1 (pp. 49–50) on the pair
`Q ⊂ int Q₀`, where `Q` is a closed square of side `s'` with `2 < s' < s`; the
substitutions are exactly the audit of §2:

1. `α ∈ (0, 1/6)` so that (7.4)'s denominator `≥ 1 − 6α > 0`;
2. `I = {1,…,6}`, `W_x ⊆ L^∞(S; R⁶)`, `G` the complete graph on 6 vertices;
3. `L₀ = L ∩ Q₀` is finite and non-empty by (F) and Lemma 7.6, so Lemma 7.4
   gives `ε_n ↓ 0` and the disks `B_{n,x}`, `x ∈ L₀`, with total radii `→ 0`
   and `g_n` continuous on `Q ∖ ⋃_{x ∈ L₀∩Q} B_{n,x}` with values in `G`;
4. Theorem 3.1 replaces Lemma 7.5, and is applied with `s'` in place of `10`;
5. in the final step "there are only finitely many simple cycles in the complete
   graph on five vertices" becomes "on six vertices", and the cycle lengths are
   `ℓ ∈ {3,4,5,6}`; the midpoint of an edge of `G` has two coordinates `1/2 > α`.

Every other line of the printed proof is label-blind and is quoted unchanged:
Lemma 7.6 (a core disk in `Q` has a non-null boundary loop), the choice of
`x ∈ L₀ ∩ int Q` and `ρ > 0` with `B(x,ρ) ⊂ int Q` free of other points of `L₀`
(possible by finiteness of `L₀`), the annulus
`A_n = B(x,ρ) ∖ B_{n,x}`, Lemmas 7.7 and 7.8 (`g_n` restricted to `A_n` has a
non-null inner boundary word; every edge midpoint of a reduced circuit has a
connected preimage component crossing the annulus), the Hausdorff limits
`K_{n,j} → K_j`, and the support exclusions via (7.2) and Lemma 7.2. ∎

**Corollary 5.2 (local finiteness suffices).** If `L` is locally finite then (F)
holds for every square, so §7 transfers to `k = 6` in full. In particular, the
paper's architecture is available at six colours as soon as `L` itself — *all*
cycle lengths at once — is shown finite in one square of side `> 2`. A
local-finiteness proof for a single cycle length is not by itself enough: `L` is
the union over `ℓ ≥ 3` of the `ℓ`-cycle loci, so (F) needs the accumulation
behaviour of every cycle length inside that square.

**Theorem 5.3 (non-emptiness is strictly weaker than (F)).** Closed sets that
are √2-dense but satisfy neither the square form of Theorem 4.1 nor (F) exist,
so neither Theorem 4.1 nor any density statement implies (F). Example: the two
families of parallel lines `L = {x = 2√2 k : k ∈ Z} ∪ {y = 2√2 k : k ∈ Z}`.
It is closed; every point of the plane is at distance `≤ √2` from it (the cell
centre `(√2, √2)` is at distance exactly `√2`), so it meets every closed disk of
radius `> √2`; it is perfect, so it has no isolated point; and the closed square
`[√2 − 1.05, √2 + 1.05]²` of side `2.1` lies strictly inside the open cell and
meets it in no point. Hence `L` misses a closed square of side `2.1 > 2`, so even
the conclusion of Theorem 4.1 fails for this `L` whereas the density corollary
holds; and `L ∩ Q` is a continuum for every square `Q` that does meet it, so (F)
fails. (`verify.py` check [6] verifies the three numerical assertions.)

*Proof.* All assertions are immediate from the spacing `2√2`; see `verify.py`.
∎

Consequently the *square* form of Theorem 4.1 — "every closed square of side
`> 2` meets `L`" — is strictly stronger than √2-density, and the constant `2`
in it is not implied by density alone. This is the sense in which Theorem 4.1
comes close to the scale at which §7 can run (Theorem 3.1 needs side `> 2`) but
still falls short of what §7 consumes (finiteness, (F)).

**Remark 5.4 (exactly where the printed proof uses finiteness, and why nothing
weaker will do).** Three places, all in Lemma 7.4 and the last step of
Proposition 7.1:

* the total-radius bound (4.1): with `|L₀| = ∞` the term `|L₀| δ` is useless and
  the union of core disks need not have small total radius;
* "for large `n`, no final disk can contain two distinct points of `L₀`: its
  diameter is smaller than their minimum positive separation" — a minimum
  separation is a finiteness statement;
* the pasting in (7.5) is over a finite family of disks with pairwise disjoint
  closures.

So (F) — finiteness in *one* square — is the exact shape of the input, and it is
the weakest form in which the printed method can consume Theorem 6.5. Whether
(F) holds at `k = 6` is open; Theorem A shows it is not refuted by emptiness of
`L`, and the exhaustive computation of §6 shows it is not refuted by the
palette structure at a triangle interface either.

**Remark 5.5 (comparison with the alternatives in the brief).** Of the three
weakenings the brief lists — non-emptiness, a continuum of centres, a single
non-null loop — the first is a theorem (Corollary 4.2) and does not suffice; the
third *is* what (F) produces (Lemma 7.6's non-null core loop), but it cannot be
had without the removal of `L` from a whole square; "a continuum of centres" is
implied by Theorem 4.1 and is likewise insufficient. The operative statement is
(F), i.e. **one small square on which `L` is finite**.

---

## 6. Non-vacuity, sharpness, and the exact decision at a triangle interface

### 6.1 The known 7-colouring (`hex_locus_check.py`)

Theorem 4.1 is proved for every `k >= 3`, so it must survive the one case where
a colouring is known to exist: `k = 7`. I computed `Γ_x` from (6.1) for the
hexagonal colouring (hexagons of circumradius `r = 2/5`, Voronoi cells of the
triangular lattice `√3 r Z[ω]`, coloured by the cosets of `(2−ω)Λ`, i.e.
`colour(m + nω) = m + 2n mod 7`), by grid quadrature of
`|D_{ij}(B,h)|/|h|` on a ball `B` of radius `0.05` for `|h|` down to `0.0025`.
Output of `python3 hex_locus_check.py`:

```
[0] centre (0,0): colour 0, six neighbour colours [1,2,3,4,5,6], all distinct: True
    min distance between equal-colour centres 1.8330; points of two such
    hexagons are >= 1.0330 > 1 apart => proper 7-colouring
[1] centres 0, 1, -w : mutual distances [0.69282]
    vertex (0.3464-0.2000j), |.| = 0.400000 (= r), cell colours [0, 1, 5]
    |h| = 0.0200: 3 edges, triangle present: True
    |h| = 0.0100: 3 edges, triangle present: True
    |h| = 0.0050: 3 edges, triangle present: True
    |h| = 0.0025: 3 edges, triangle present: True
    ratios: (0,1):0.050, (0,5):0.028, (1,5):0.029
[2] centre of hexagon (0,0): edges of Gamma: [] (expect none)
[3] side midpoint 0|1: edges of Gamma: ['(0, 1):0.098'] (expect exactly one edge)
[4] points at distance 0.2 from a centre: 0 edges
```

So for the 7-colouring, `Γ_x` is empty at cell centres, a single edge (= a tree)
on the relative interior of a hexagon side, and a **triangle** at every Voronoi
vertex. The ratios at the vertex are bounded away from zero as `|h| ↓ 0`, which
is (6.1)'s `limsup > 0`. Hence

```
L_7 = { Voronoi vertices } = the vertices of the triangular tiling,
```

a discrete lattice of mesh `√3·(2/5) = 0.6928`, locally finite, and far denser
than the `√2 = 1.414` that Theorem 4.1 guarantees (and than the `5√2 = 7.07`
that the paper's own constants, taken at face value, would give). So the §7
machinery is not killed by a colouring that exists, and Theorem 4.1 is
non-vacuous.

The exact argument, not just the computation: if two colours have a common
boundary segment of positive length through `x`, then `|D_{ij}(B,h)| ≥
c|h|` for `h → 0` in a direction transverse to the boundary and every ball `B`
about `x` that the segment crosses, so `ij ∈ Γ_x`; if a colour does not occur in
some neighbourhood of `x` then `D_{ij}(B,h) = 0` for that ball, so `ij ∉ Γ_x`.
At a tiling vertex three cells meet, pairwise along three segments of positive
length, and no fourth colour occurs nearby; on the relative interior of a
hexagon side exactly two colours occur, meeting along that side; in the interior
of a cell exactly one colour occurs. Hence `Γ_x` is a triangle at the vertices,
a single edge on the open sides, and edgeless at cell centres.

### 6.2 The triangle interface: `k = 5` versus `k = 6` (`triangle_stratum.py`)

At a centre whose `Γ_x` contains the triangle `T = {a,b,c}`, Lemma 6.2 gives
`P_x(e) ⊄ {i,j}` for each edge `{i,j}` of `T`, a.e. `e`. Combining with the
palette bound `1 ≤ |P| ≤ k−3` decides the whole palette stratum. Exhaustive
enumeration over all subsets:

* `k = 5`: `|P| ≤ 2`; a non-empty subset of `T` of size `≤ 2` lies in some edge
  of `T`, so `P_x(e) ⊄ T`; hence `P_x(e)` meets the two-element outsider set
  a.e., and (5.7) `P_x(f) ∩ P_x(Rf) = ∅` makes the intersection a singleton
  alternating under `R`. So `x` is **binary for the fixed outsider pair**,
  Lemma 5.5 applies, and the triangle locus is locally finite — the paper's
  first case of Theorem 6.5.
* `k = 6`: `|P| ≤ 3`; the admissible palettes are 35 in number and include
  `P = T` itself (so `A(e) = P_x(e) ∩ (I∖T)` may be **empty**), every palette
  of the form `{t} ∪ (2-subset of outsiders)` (so `|A| = 2`), and the whole
  outsider triple (so `|A| = 3`). No fixed pair and no fixed outsider is forced.

The counts `9` and `35` are produced twice, by two independent code paths in
`triangle_stratum.py`: brute-force enumeration over all subsets, and the
inclusion–exclusion formula
`Σ_{j=1}^{k−3} C(k,j) − 3·(2 + [k−3 ≥ 2]) + 3` (two edges of `T` meet in one
vertex, three meet in nothing). They agree at both `k`.

So at `k = 6` the triangle locus receives **no binarity** and Lemma 5.5 gives
nothing: the printed triangle case of Theorem 6.5 has no six-colour analogue,
independently of any finite-model search. This is why the `k = 6` problem is a
*finiteness* statement about `L` (Theorem B) rather than a binarity statement,
and it is the exact sense in which the sprint brief's "palette bound 3,
triangle-interface outsider set of size 2 of 3" bites.

Both enumerations are exact and exhaustive; the only inputs are (6.2) of the
paper and the palette bound. Certificate: the tables printed by
`python3 triangle_stratum.py`.

### 6.3 Every cycle length at a cyclic centre (`cycle_strata.py`)

The same enumeration for every simple cycle length `ℓ` gives the complete
single-centre stratum, with two independent counts again (brute force and the
closed form `Σ_{j=1}^{k−3} C(k,j) − 2ℓ`, since only singletons and pairs can sit
inside an edge and a cycle's edges are distinct):

| `k` | `ℓ` | admissible palettes | of which singletons | of which pairs | of which triples |
|---|---|---|---|---|---|
| 5 | 3 | 9 | 2 (the outsiders) | 7 | – |
| 5 | 4 | 7 | 1 (the extra label) | 6 | – |
| 5 | 5 | 5 | 0 | 5 (the diagonals `{i,i+2}`) | – |
| 6 | 3 | 35 | 3 | 12 | 20 |
| 6 | 4 | 33 | 2 | 11 | 20 |
| 6 | 5 | 31 | 1 | 10 | 20 |
| 6 | 6 | 29 | 0 | 9 (6 at distance 2, 3 at distance 3) | 20 |

At `k = 6` the two structural facts are: **(a)** no palette of size 3 is ever
excluded, because an edge of a cycle has only two endpoints — so *no*
single-centre palette constraint can forbid a cycle of any length at six
colours; **(b)** if all palettes were of size `≤ 2` (the `k = 5` situation), the
admissible pairs would be exactly the diagonals of the cycle, and at `ℓ = k` the
palette would have to be a non-edge of the cycle — at `k = 5, ℓ = 5` that is the
5-periodic diagonal structure of the paper's §6.3.3.

Consequence for the `k = 6` cycle cases: the single-centre content is vacuous
at every cycle length, so every exclusion of a cycle case at six colours must
use the two-centre transport (5.3), not the palette bounds. This is the
palette-side counterpart of Theorem B: the same reason (three labels are free)
that kills binarity at the triangle also kills every other palette-based route.

---

## 7. How the formula checks were made

`pdftotext -layout` drops stacked fractions and radicals. To read displayed
formulas I converted the PDF to `mutool -F stext` XML (per-glyph `x`, baseline
`y`, font size, glyph) and reconstructed lines with baseline shifts and
font-size changes marked, which exposes sub- and superscripts and shows stacked
fractions inline in reading order. `paper/render.py` does this;
`python3 paper/render.py 'paper/pg%d.xml' 42 43 45 46 47` reproduces the pages
used here. Checked this way and found faithful to the extraction:
Proposition 7.1 (p. 42), Lemma 7.2 (p. 43), Lemma 7.3 (p. 44), (7.4) with
`0 < α < 1/5`, "the complete graph on its five vertices", and Lemma 7.4 with
`| L₀ | δ + m_{δ,ε} + η` (p. 45–46), Lemma 7.5 and Lemma 7.6 (p. 47).

---

## 8. What is not proved

1. **(F) at `k = 6`.** Not proved, not refuted. Theorems A and B reduce the
   entire §7 step to it; §6.2 shows the printed route to it (binarity) is closed
   at `k = 6`.
2. **Local finiteness of `L` at `k = 6`.** Not addressed except as the strongest
   sufficient condition for (F) (Corollary 5.2); the per-cycle-case work is
   other members' directions.
3. **`§8` at `k = 6`.** Untouched. Theorem 5.1 delivers the hypothesis of §8
   (the cycle of exclusion continua with its sliver data `v_j`), not its
   conclusion; the six-cycle case has no printed argument at all.
4. **Sharper density than `√2`.** Theorem 4.1's constant is what the printed
   machinery yields and is close to optimal *for the method* (§3); no attempt was
   made to improve it by a different argument.
5. **Lean.** No formalisation. The claims are analytic; the only machine-checked
   parts are the two computations of §6 and the rendered-page formula audit of
   §7.

---

## 9. File list and how to check

| file | what it is |
|---|---|
| `K6-CYCLIC-LOCUS.md` | this document: Theorems A, B, C with all proofs and the hypothesis audit of §2 |
| `verify.py` | elementary checks: the identity `{y : dist(y,∂Q) > m}` = concentric square of side `s−2m` and the instances `s ≤ 2m`; the clique-in-a-forest step exhaustively over all 33 867 graphs on `≤ 6` vertices; the `α < 1/6` denominator in exact rationals; disk/square; the strictness example of Theorem 5.3 |
| `hex_locus_check.py` | §6.1: `L_7` for the hexagonal 7-colouring (non-vacuity of Theorem 4.1) |
| `triangle_stratum.py` | §6.2: exhaustive palette strata at a triangle interface, `k = 5` versus `k = 6` |
| `cycle_strata.py` | §6.3: the same for every cycle length `ℓ = 3..6`, `k = 5` and `6` |
| `paper/render.py` | rendered-page formula reader; `paper/pg*.xml` its input |

```
python3 verify.py && python3 hex_locus_check.py && python3 triangle_stratum.py \
  && python3 cycle_strata.py
```

All three exit 0 and print the tables quoted above; a run is recorded in
`logs/all-checks.log`.
