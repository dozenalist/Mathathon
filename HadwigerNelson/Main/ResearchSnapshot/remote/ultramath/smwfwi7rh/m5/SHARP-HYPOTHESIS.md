# The exact input of §7 at six colours, and why covering/content conditions on `L`
# cannot replace it

Member `m5`, swarm `smwfwi7rh`, direction **d2** ("weakest sufficient statement").
Deliverable type: **theorem + counterexample** (not a survey).  Companion files:
`verify.py` (all exact/numeric checks, runnable), `results.txt` (its output),
`LEAN-NOTE.md` (what is and is not machine-checked).

---

## 0. What is settled here

The record (`sprint/k6/REPORT.md`, `sprint/k6/WEAKEST.md`, `.ultramath/smwfo9zkl/m12/S7-INPUT.md`)
established that §7 of the paper runs at `k = 6` under the hypothesis

> **(W)** there are `y ∈ R²` and `R > 1` with `L ∩ B(y,R)` finite,

and left open (coordinator's lead, from `m15`) whether the *finiteness* in **(W)** can be
replaced by a **covering / content bound** — "zero upper `1`-dimensional Minkowski content of
`L` on compacts is enough for §7".  This note decides that question and locates the boundary
exactly:

| # | statement | status |
|---|---|---|
| **Thm 1** | a covering bound on `L₀ = L ∩ Q′` **is** enough for the *disk-removal* stage (Lemma 7.4), with holes of total radius `→ 0` | **proved** (§2) |
| **Prop 2** | the *printed* Lemma 7.4 (finite `H_n`, one distinct core disk per point of `L₀`) is satisfiable only for finite `L₀` | **proved** (§3) |
| **Thm 3** | at a *non-isolated* cyclic centre, **every** annulus around it contains another core disk, for every admissible hole family | **proved** (§4) |
| **Thm 3′** | the crossing lemma (paper Lemma 7.8) is **false** on a punctured annulus: explicit `g`, non-null inner word, no crossing component | **proved + exact certificate** (§5) |
| **Thm 4** | there is a closed, **perfect**, `1`-dense, porous set `L*` with **zero upper `1`-dimensional Minkowski content on every compact**, whose every ball of radius `> 1` meets it infinitely often | **proved** (§6) |
| **Thm 5** | the cover obstruction's threshold `inradius > mesh` is **sharp**: a disk admits a multiplicity-`2` cover of mesh `→ inradius` | **proved + exact certificate** (§7) |

**Consequence (§8).**  In the terminology of the record: the covering/content route buys
Lemma 7.4 and nothing else.  At a non-isolated cyclic centre the morphism `g_n` produced by
Lemma 7.4 is never defined on a whole annulus of positive radius, and by Theorem 3′ this is not
a defect of the printed proof but a genuine topological fact about punctured annuli.  Hence the
covering/content conditions, however strong, cannot supply **(W)**: no hypothesis that only
bounds the *size* of `L` (zero upper `1`-dim. Minkowski content, `σ`-finiteness, zero
`1`-dimensional Hausdorff measure, porosity, `1`-density) can imply it, because Theorem 4's set
satisfies all of them and has no isolated point at all.  The exact input of the printed
architecture is **isolation** of one cyclic centre, at radius `> 1`; the constant `1` is the
sharp threshold (Theorem 5 together with `m12`'s density theorem).

Scope, stated plainly.  Theorems 1, 2, 4, 5 are unconditional theorems about closed sets and
about the paper's own objects.  Theorem 3 is unconditional for closed `L`.  Theorem 3′ is a
statement of 2-dimensional topology, in the same category as Lemma 7.8; it shows that the
generalisation of Lemma 7.8 that a punctured annulus would require is *false*, so no argument
of the printed type can be run at a non-isolated centre.  It does **not** assert that
Proposition 7.1's conclusion is false for colourings with perfect `L` — that is precisely the
open problem, and §8 says what a proof would have to do instead.

---

## 1. Setting, and the two objects being compared

Everything below is in the paper's notation.  `c : R² → I`, `I = {1,…,k}`, is a weak measurable
`k`-colouring (paper Definition 1.2, Theorem 1.3); `Γ_x` is the transition graph of Definition
6.1 with edge condition (6.1); `L = {x : Γ_x contains a cycle}`; `H_i` is the closed spatial
essential support of the colour class `A_i`; `Δ(K) = {z : min_{q∈K}|z−q| < 1 < max_{q∈K}|z−q|}`
for nonempty compact `K` ((7.1)); `κ = π/3`, and `R` is the rotation by `κ`.

Two facts of the record that are used and not re-derived:

* **`L` is closed** (paper §6 for `k = 5`; `m12` Theorem A for every `k`).
* **`L` is `1`-dense** (`m12` Theorem D): `dist(y,L) ≤ 1` for every `y ∈ R²`; hence `L ≠ ∅` and
  every closed ball of radius `> 1` meets `L`.

The §7 transfer itself is `m12`'s Theorem B′ and is quoted, not reproved:

> **(B′)**  If `L ∩ B(y,R)` is finite for some `R > 1`, then Proposition 7.1 holds at `k = 6`
> (a cycle of common exclusion continua of length `ℓ ∈ {3,4,5,6}`).

The **hole families** of §7.2 are the objects I compare conditions against.  A hole family at
scale `n` is a finite family `H_n` of open disks with pairwise disjoint closures; a disk of
`H_n` is *core* if it belongs to the merger class of a disk that covers a point of `L₀`;
`g_n : Q \ ⋃{core disks} → G` is the graph-valued map of Lemma 7.4(3), equal to `q_{ε_n}`
outside all holes and obtained by filling the non-core holes through trees.

---

## 2. Theorem 1 — the disk-removal stage runs under a covering bound

The paper's §7.2 fixes `0 < α < 1/5` (at `k = 6`: `0 < α < 1/6`, so that
`Σ_{k∈I}(p_k^ε − α)_+ ≥ 1 − 6α > 0`, and `q^ε` of (7.4) is still a continuous map into the
simplex), then chooses a closed square `Q` with `∂Q ∩ L = ∅` and `L₀ = L ∩ Q′` **finite**.

> **Theorem 1.**  Let `Q ⊂ int Q′` be compact, `∂Q ∩ L = ∅`, `L₀ = L ∩ Q′`, and assume
>
> **(C)** for every `ε > 0` there is a finite family of open disks covering `L₀` whose radii sum
> to less than `ε`.
>
> Then there are `ε_n ↓ 0` and finite families `H_n` of open disks with pairwise disjoint
> closures and total radii tending to zero such that, for all large `n`,
>
> 1′. every point of `L₀` lies in the interior of a core disk of `H_n`; every core disk contains
>     a point of `L₀`; core disks meeting `Q` lie in `int Q`; core disks whose points of `L₀`
>     lie outside a `γ`-neighbourhood of `Q` are disjoint from `Q`, where `2γ = dist(∂Q, L) > 0`;
> 2.  `q_{ε_n}` takes values in the one-skeleton `G` on `Q \ ⋃_{B∈H_n} B`;
> 3.  there is a continuous `g_n : Q \ ⋃{core disks} → G` equal to `q_{ε_n}` outside all holes,
>     obtained by filling the non-core disks through trees.
>
> Hypothesis **(C)** holds in particular if `L₀` has upper `1`-dimensional Minkowski content
> zero: for a maximal `δ`-separated net of `L₀`, the balls of radius `δ` about its points cover
> `L₀` with total radius `δ·N`, and `N·πδ²/4 ≤ |N_{δ/2}(L₀)|`, so `δ·N ≤ 4|N_{δ/2}(L₀)|/(πδ) → 0`.

*Proof.*  The paper's proof of Lemma 7.4, with one substitution.  Fix `δ > 0`, put
`2γ = dist(∂Q, L) > 0` (positive because `∂Q` is compact, `L` is closed and the two are disjoint),
and let `{D_1,…,D_N}` be a finite cover of `L₀` by open disks of total radius `< min(δ, γ/2)`
(hypothesis **(C)**);
if a point of `L₀` lies on the boundary of some `D_i`, enlarge that disk by an arbitrarily small
amount and absorb the cost into `δ`.  Put `M = Q′ \ ⋃_i D_i`.  `M` is compact and disjoint from
`L₀ = L ∩ Q′`, hence `Γ_z` is a forest for every `z ∈ M` (including isolated vertices).  Now
copy §7.2 verbatim: each nonedge of `Γ_z` gets a ball on which the simultaneous threshold
violations admit finite open disk covers of total radius `o(1)` (Lemma 7.3); finitely many
nonedges give a radius `s_z > 0`; finitely many balls `B(z,s_z)` cover the compact `M`; let `λ`
be a Lebesgue number and mark the finitely many covering disks; their total radius
`m_{δ,ε} → 0` as `ε ↓ 0` for fixed `δ`.  Merge disks until closures are pairwise disjoint, with
total enlargement error `< η`; the total radius is at most
`Σ_i rad(D_i) + m_{δ,ε} + η < δ + m_{δ,ε} + η`, replacing the paper's `|L₀|δ + m_{δ,ε} + η`.
A final disk is core iff its merger class contains one of the `D_i`; every non-core final disk
with closure meeting `Q` lies outside all `D_i`, hence in `M`, has diameter below `λ`, and its
boundary maps into one component tree of the selected forest, which is contractible; the
boundary map therefore extends over the disk, and finite pasting gives (3).  Finally take
`δ_n ↓ 0`, fix the finite cover of `L₀` of total radius `< δ_n`, and choose `ε_n` and the merger
errors so that `m_{δ_n,ε_n} + η_n < min(1/n, λ_{δ_n}/3)`; the total radii tend to zero.  For the
positional assertion: every point of `L₀` is at distance `≥ 2γ` from `∂Q`, a core disk of radius
`< γ` containing `x` lies in `B(x,2γ)` and a disk of radius `r` containing `x` lies in `B(x,2r)`,
so no core disk meets `∂Q`; being connected it lies on the same side of `∂Q` as its point of
`L₀`, i.e. in `int Q` if the point is in `Q` and disjoint from `Q` if not.  (Keep the merger
errors `η_n` below `γ/2` too.)  ∎

**Remark.**  Theorem 1 is exactly `m15`'s suggestion, made precise and proved: the *removal* of
the cyclic centres, with holes of total radius tending to zero, does **not** need finiteness of
`L₀`.  In particular the sentence in `m12`'s §6 ("the disk removal of Lemma 7.4 cannot be
performed with holes of total radius tending to zero") is not correct as it stands; the
obstruction is further on, at §3–§5 below.

---

## 3. Proposition 2 — the printed form of Lemma 7.4 forces finiteness

> **Proposition 2.**  Let `L₀ ⊆ R²` be such that there are a finite family `H` of open disks with
> pairwise disjoint closures and an injection `L₀ → H`, `x ↦ B_x`, with `x ∈ B_x`.  Then `L₀` is
> finite.
>
> Consequently the printed Lemma 7.4 — "finite families `H_n`", "for each `x ∈ L₀` precisely one
> disk of `H_n` is designated the core disk `B_{n,x}`", "different points give different core
> disks" — is satisfiable only when `L₀` is finite, for every `n`.

*Proof.*  `|L₀| ≤ |H| < ∞`, since the injection is into a finite set.  ∎

So the two statements are the exact alternatives: with infinite `L₀` one may keep conditions
(2), (3) and "each cyclic centre in some core disk" (Theorem 1), and one must give up "one
distinct core disk per cyclic centre".  The paper's proof then also uses the discarded condition,
in one more place: "For large `n`, no final disk can contain two distinct points of `L₀`: its
diameter is smaller than their minimum positive separation" — a sentence that has no meaning for
infinite `L₀`.  At a perfect `L`, every core disk that contains a point `x ∈ L₀` also contains
other points of `L₀`, for every `n` (the disk is a neighbourhood of `x`).

---

## 4. Theorem 3 — no hole-free annulus at a non-isolated centre

This is where the route stops.

> **Theorem 3.**  Let `L ⊆ R²` be closed, `x ∈ L`, `ρ > 0`, and let `(H_n)` be any sequence of
> families of open disks with pairwise disjoint closures such that
>
> (i) every point of `L ∩ B(x,ρ)` lies in some disk of `H_n`, and
> (ii) `sup{rad(D) : D ∈ H_n} → 0`.
>
> Let `B_n ∈ H_n` be a disk containing `x`.  If `x` is not an isolated point of `L`, then for all
> sufficiently large `n` there is `D_n ∈ H_n`, `D_n ≠ B_n`, with `D_n ∩ (B(x,ρ) \ B_n) ≠ ∅`.
>
> Hence `g_n` of Lemma 7.4(3) is **never** defined on the whole closed annulus
> `A_n = closure(B(x,ρ)) \ B_n`, and paper Lemma 7.8 — whose hypothesis is a continuous map on
> the whole annulus — is inapplicable at **every** point `x` of a perfect `L`, for **every**
> radius `ρ` and every `n`.

*Proof.*  `x` is not isolated, so `L ∩ B(x,ρ) ∋ y ≠ x`; put `d = |y − x| > 0` (choose `y` with
`|y−x| < ρ`).  By (ii), for `n` large, every disk of `H_n` has radius `< d/3`; since `x ∈ B_n`,
`B_n ⊆ B(x, d/3)`, so `y ∉ B_n`.  By (i), `y ∈ D_n` for some `D_n ∈ H_n`; `D_n ≠ B_n`, and
`y ∈ D_n ∩ (B(x,ρ) \ B_n)`.  ∎

Two clarifications, because both are natural escape routes:

* **A "tiny annulus" repair does not give Proposition 7.1.**  One can always choose the largest
  hole-free annulus around `x`, `A_n = B(x,ρ_n) \ B_n` with
  `ρ_n = ½·min(ρ, dist(x, ∪{other holes in B(x,ρ)}))`, and apply Lemma 7.8 to it: it produces a
  continuum `K_n ⊂ A_n` meeting `∂B_n` and `∂B(x,ρ_n)`, on which both endpoint supports are
  excluded from `Δ(K_n)`.  But `ρ_n → 0`, so `K_n → {x}` in Hausdorff distance, `Δ(K_n)` is a
  shell of width `ρ_n` around the sphere of radius one, and the limiting object has
  `Δ({x}) = ∅`.  Proposition 7.1's conclusion requires a **fixed** `x, ρ > 0` and a fixed
  continuum `K_j` with `K_j ∩ ∂B(x,ρ) ≠ ∅`; §8 then consumes exactly that: Lemma 8.1 needs a
  fixed *positive* radial width of the excluded strip at radius one ("an open strip just outside
  radius one uses only `O(e)`", with "positive widths" intersected over finitely many edges).  A
  sequence of continua living on shells of width `ρ_n → 0` supplies no such width.  So the
  printed architecture needs a fixed-radius hole-free annulus, and by Theorem 3 that needs
  isolation.
* **Theorem 3 is about every hole family, not about the paper's construction.**  It uses only
  (i), (ii) and closedness of `L`, so it applies to any variant of Lemma 7.4 that keeps the
  points of `L` inside holes of vanishing radius, in particular to the content-based variant of
  Theorem 1.

---

## 5. Theorem 3′ — the crossing lemma is false on a punctured annulus

Theorem 3 says the annulus of Lemma 7.8 always has holes at a non-isolated centre.  One could
still hope that Lemma 7.8 is *true* with a hole in the annulus (after all, the annulus with a
puncture is still homotopy equivalent to a wedge of two circles, and the inner boundary is still
non-null there).  It is false.  This is the reason the annihilation obstruction cannot be
repaired inside the printed architecture.

> **Theorem 3′.**  Let `A = {z : 1 ≤ |z| ≤ 3}`, `K = {z : |z − 2| ≤ 1/4} ⊂ int A`,
> `G = C_5` (a `5`-cycle, a subgraph of the one-skeleton `K_6` used in §7), and let
> `ρ : S¹ → C_5` be a degree-one graph map.  Define
> `f(z) = (z/|z|)·conj(z−2)/|z−2|` on `A \ K` and `g = ρ ∘ f`.  Then
>
> * `g : A \ K → C_5` is continuous;
> * the counterclockwise inner boundary `∂B(0,1)` maps to a loop of degree `1`, so its cyclically
>   reduced word is the whole `5`-cycle `W = c_0c_1c_2c_3c_4`, a nonempty cyclically reduced word;
> * for `m = ρ(−i)`, an edge midpoint occurring in `W`, the compact set `g^{-1}({m})` equals
>   `({|z−1| = 1} ∩ (A \ K))`, which is a single arc; it joins the inner boundary circle
>   `{|z| = 1}` to the hole boundary `{|z−2| = 1/4}` and is at distance `≥ 1` from the outer
>   boundary `{|z| = 3}`.  In particular **no component of `g^{-1}({m})` meets both boundary
>   circles of `A`.**

*Proof.*  `f` is continuous on `A \ K` since `|z| ≥ 1` and `|z−2| ≥ 1/4` there.  For the level
set, write `z = x + iy`: `f(z) = −i` is equivalent to `z·conj(z−2) = −i|z||z−2|`; the right side is
purely imaginary, and
`Re(z·conj(z−2)) = x² + y² − 2x`, so the equation forces `x² + y² = 2x`, i.e. `|z − 1| = 1`
(exactly verified in `verify.py`, check A2a).  On that circle, writing `z = 1 + e^{iφ}` with
`φ ∈ (0,2π)`, one computes `z = 2cos(φ/2)e^{iφ/2}`, `z − 2 = 2i sin(φ/2)e^{iφ/2}`, hence
`f(z) = −i·sgn(cos(φ/2))`, which is `−i` exactly for `φ ∈ (0,π)` (checks A1, A2b).  Inside `A`
the condition `|z| ≥ 1` selects `φ ∈ (0, 2π/3]`, where `|z| = 2cos(φ/2) ∈ [1,2]` (check A2c,
A2d), so the level set in `A` is the arc from `z = 1/2 + i√3/2` to `z = 2`; removing the hole
`K` (which cuts the arc at `|z−2| = 1/4`, i.e. at `φ = 2arcsin(1/8)`, check A4′) leaves one arc
joining `|z| = 1` to `|z−2| = 1/4`, of distance `≥ 1` from `|z| = 3` (check A4).  Degrees:
`∂B(0,1) ∋ e^{it}` is mapped by `f` to `(1 − 2e^{it})/|1 − 2e^{it}|`, whose argument winds once
around `0` since the circle `|w − 1| = 2` encloses the origin, so the inner degree is `+1`
(check A3); on `|z−2| = 1/4` the degree is `−1` (check A3′).  ∎

Consequences, stated carefully.

* Lemma 7.8's proof uses in an essential way that `g` is defined on the whole annulus: the loop
  `∂V` with nonzero winding about `x` is then freely homotopic *inside the annulus* to a power of
  the inner boundary, so its image is freely homotopic to `W^d` and must meet `m` (Lemma 7.7).
  On the punctured annulus, a loop with winding `d` about `x` is homotopic to
  `(inner)^d·(hole)^k`, and in the example above the hole contributes exactly the cancelling
  `k = d`.  That is what happens: the level set escapes into the hole.
* The counterexample is a *general topological* one; it is not claimed that the specific maps
  `g_n` of §7 realise it.  What it shows is that no argument of the printed type — "the annulus
  is non-null, so some midpoint preimage crosses it" — can survive a hole, so the annihilation
  step is not a technicality of the paper's write-up.

---

## 6. Theorem 4 — a perfect, `1`-dense locus with zero `1`-dimensional content

The covering hypothesis of Theorem 1 is *strictly* weaker than **(W)**, in the strongest possible
way: it is compatible with `L` having no isolated point at all.  The following set is the
counterexample that direction d2 asks for ("zero content but breaks the annulus step").

Let `C ⊂ [0,1]` be the middle-thirds Cantor set, `s = log2/log3`, `ε_λ ∈ (0, 1/8)` for
`λ ∈ Λ = ½Z²` with `Σ_λ ε_λ^s < ∞` (e.g. `ε_λ = 2^{−1−|λ|²}`), and

> **L\* = ⋃_{λ ∈ Λ} (λ + ε_λ·(C × {0})) ⊂ R².**

> **Theorem 4.**  `L\*` has the following properties.
>
> (a) `L\*` is closed.
> (b) `L\*` is perfect: it is closed and has no isolated point.
> (c) `L\*` is `1`-dense: every closed disk of radius `> 1` meets it.  In fact every closed disk
>     of radius `≥ √2/4` does, because `0 ∈ C`, so `Λ ⊆ L\*`, and the covering radius of `½Z²`
>     is `√2/4`.
> (d) `L\*` has zero upper `1`-dimensional Minkowski content on every compact set: there is
>     `C_K < ∞` with `|N_δ(L\* ∩ K)| ≤ C_K·δ^{2−s}` for all `δ ∈ (0,1)`, hence
>     `|N_δ(L\* ∩ K)|/δ ≤ C_K δ^{1−s} → 0`.  Consequently `H¹(L\* ∩ K) = 0`, `L\*` is
>     `σ`-compact (`L\* = ⋃_k (L\* ∩ k·[-1,1]²)`), and `L\*` is porous.
> (e) every ball `B(y,R)` with `R > 1` meets `L\*` in infinitely many points; in particular
>     **(W)** fails for `L\*`, for every `y` and every `R`.

*Proof.*  (a) The family `{λ + ε_λ(C×{0})}` is locally finite (only the finitely many `λ` with
`dist(λ,K) ≤ 1/8` meet a compact `K`, because `ε_λ < 1/8`), so the union is closed.  (b) `0 ∈ C`, so `λ ∈ L\*`; every
point of `λ + ε_λ(C×{0})` is a limit of other points of that same piece, because a scaled Cantor
set is perfect.  (c) `Λ ⊆ L\*` and `½Z²` has covering radius `½·√2/2 = √2/4`.  (d) Let `K` be
compact and `δ ∈ (0,1)`.  `N_δ(L\* ∩ K) ⊆ ⋃_{λ ∈ K_δ} λ + N_δ(ε_λ(C×{0}))`, a union over the
finitely many lattice points `λ` with `dist(λ,K) ≤ δ + 1/8`.  A subset of a segment of length
`ε` whose `δ`-neighbourhood, intersected with the line, has length `ℓ`, has planar `δ`-neighbourhood
of area `≤ 2δ·ℓ` (the tube is contained in the `2δ`-neighbourhood of a segment).  Two regimes.

*If `ε_λ ≥ δ`*: covering `ε_λC` by `N` intervals of length `δ` and using the self-similarity of
`C` gives `N ≤ 3(ε_λ/δ)^s`, so
`|N_δ(ε_λ(C×{0}))| ≤ 2δ·2δ·N ≤ 12·δ^{2−s}·ε_λ^{s}`.

*If `ε_λ < δ`*: the piece is contained in a segment of length `ε_λ`, so its `δ`-neighbourhood is
contained in a rectangle of sides `ε_λ + 2δ ≤ 3δ` and `2δ`, of area `≤ 6δ²`.

Summing over the finitely many `λ` with `dist(λ,K) ≤ 1/8` (there are `N_K < ∞` of them, the
lattice `½Z²` being discrete) and using `Σ_λ ε_λ^s < ∞`:
`|N_δ(L\* ∩ K)| ≤ 6 N_K δ² + 12 δ^{2−s} Σ_{λ} ε_λ^s =: 6N_K δ² + C_K δ^{2−s}`, so
`|N_δ(L\* ∩ K)|/δ ≤ 6N_K δ + C_K δ^{1−s} → 0` because `s < 1`.  `σ`-compactness is immediate.  Porosity: `L\* ⊆ ⋃_{λ∈Λ} (λ + [-1/8,1/8]²)`, because every piece lies in the
segment `λ + ε_λ·[0,1]×{0}` with `ε_λ < 1/8`.  Hence for every `λ` the ball
`B(λ + (1/4,1/4), 1/8)` is disjoint from `L\*` (its centre is at distance `√2/8 > 1/8` from
`λ + [-1/8,1/8]²` and at distance `> 1/8` from every other lattice square), and these balls are
`√2/4`-dense.  For `0 < r ≤ 3/16` and `x` in the piece over `λ`, the ball of radius `r/4` centred
at `x + (r/2)e_y` is disjoint from `L\*` (`e_y` perpendicular to the piece, and all other pieces
are at distance `≥ 3/8 > r`); for `r ≥ 3/16` a ball of radius `1/8` from the family above lies in
`B(x,r)`.  So `L\*` is porous.  (e) A ball of radius
`> 1` contains a lattice point `λ` and, since each piece is a perfect set containing `λ`, it
contains infinitely many points of that piece.  ∎

**Corollary (no covering/content condition implies (W)).**  Any property `P` of closed sets that
is satisfied by `L*` — in particular "zero upper `1`-dimensional Minkowski content on every
compact", "`σ`-compact and content-zero", "`H¹`-null", "porous", "`1`-dense", "`L` is a
countable union of Cantor sets", "`L` has packing numbers `o(1/δ)`" — does not imply **(W)**:
`L*` satisfies `P` and every ball of radius `> 1` meets it infinitely often.  Since Theorem 1
shows `P` does yield the *disk-removal* stage, and Theorem 3 shows the extraction needs a
fixed-radius hole-free annulus, the covering/content programme cannot reach Proposition 7.1.

**Vacuity check.**  `L*` is not a vacuous object: it satisfies every property that the record
proved for `L` from the colouring side independently of finiteness — closed (paper §6 / `m12`
Thm A) and `1`-dense (`m12` Thm D) — and the extra smallness condition `m15` proposed.  What it
does not do is come from a colouring: whether a weak measurable six-colouring can have a perfect
cyclic locus is exactly the open problem (`REPORT.md` §8).  The corollary is therefore a
statement about which *hypotheses* can suffice, which is what a "weakest sufficient statement"
asks, and not a claim about six-colourings.

---

## 7. Theorem 5 — the cover threshold is sharp

`m12` §5.2 argues that `R > 1` cannot be improved "because the derived mesh bound `1 + o(1)`
cannot be lowered below the forbidden distance".  That argument is a statement about the printed
constants.  The following makes the sharpness intrinsic to the cover obstruction itself.

> **Theorem 5.**  Let `R > 0` and `m > R`.  The closed disk `B(0,R)` has a *relatively open*
> cover of multiplicity at most `2` and mesh at most `m`.
>
> Construction.  Fix `ε ∈ (0, (m−R)/4)` and define six sets:
>
> * `A_0` = (the upper half `{Im z ≥ 0}` of the disk `|z| < ε`) `∪` (the sector
>   `{ε ≤ |z| ≤ R, arg z ∈ [0, π/3)}`),
> * `A_1` = (the lower half `{Im z < 0}` of the disk `|z| < ε`) `∪` (the sector
>   `{ε ≤ |z| ≤ R, arg z ∈ [π/3, 2π/3)}`),
> * `A_k` = the sector `{ε ≤ |z| ≤ R, arg z ∈ [(k−1)π/3, kπ/3)}`, `k = 2,…,5`.
>
> Then `(A_k)_{k=0}^5` covers `B(0,R)`, its multiplicity is at most `2`, and
> `diam A_0 ≤ R + 2ε`, `diam A_k ≤ R` for `k = 1,…,5`.  Thickening each `A_k` by `ε₀/2`
> (see below) gives a relatively open cover with the same multiplicity and mesh `≤ R + 3ε ≤ m`.
>
> **Thickening lemma.**  Let `C_1,…,C_N` be a finite cover of a compact `X` with multiplicity at
> most `2`.  Then `U_i = {x : dist(x,C_i) < ε₀/2}` is a relatively open cover with `U_i ⊇ C_i` and
> multiplicity at most `2`, where `ε₀ = min_X g > 0` and `g(x)` is the third smallest of the
> numbers `dist(x,C_i)`.  Indeed at most two of those vanish at any `x`, so `g > 0`; `g` is
> continuous as an order statistic of continuous functions, and `X` is compact; and three
> memberships would give three distances `< ε₀/2`, hence `g < ε₀`.  ∎

*Proof of Theorem 5.*  Cover: a point with `|z| < ε` lies in `A_0` or `A_1` according to the sign
of `Im z`; a point with `|z| ≥ ε` lies in exactly one of the six half-open sectors, which is
attached to `A_0`, `A_1` or is one of `A_2,…,A_5`.  Multiplicity: the inner and outer layers are
radially separated (`|z| < ε` versus `|z| ≥ ε`), the two halves are disjoint, and the half-open
sectors are disjoint, so every point lies in exactly one `A_k`.  Diameters: `A_k` for `k ≥ 2` is an
annular sector of radius range `ε ≤ r ≤ R` and angle `π/3`; its extreme pairs are the two outer
arc endpoints, at distance `2R sin(π/6) = R`, and every pair involving an inner point is closer, so
`diam A_k = R`; `A_0` contains in addition a half-disk of radius `ε`, and the largest new distance
is from `(−ε,0)` to the outer arc endpoint at angle `π/3`, i.e.
`√((R/2+ε)² + 3R²/4) = √(R² + Rε + ε²) ≤ R + ε`, so `diam A_0 ≤ R + 2ε`.  The thickening lemma
converts the cover into a relatively open one at the cost of `ε₀ ≤ 2ε` in the mesh.  Checks
B1–B4 in `verify.py` confirm cover, multiplicity, and the two diameters on a `501×501` grid over
the disk, with `R = 1`, `ε = 1/100` (computed `diam A_0 = 1.0100…`, `diam A_k = 1.0000…`).  ∎

So the hypothesis `inradius(Q) > mesh` of the cover obstruction (the disk form of paper Lemma
7.5, `m12`'s Lemma 5.1) cannot be weakened to `inradius(Q) ≥ mesh`: *at* the threshold there are
relatively open multiplicity-two covers of the corresponding mesh, for every `R` and every
`m > R`.  Since the component cover of §7.3 has mesh `1 + o(1)`, a region of inradius `> 1` is
needed, and a region of inradius `≤ 1` admits such covers.  This is the intrinsic reason for the
constant `1` in **(W)** — and it matches `m12`'s density theorem, which shows that no ball of
radius `> 1` is ever free of cyclic centres.  In particular the constant `√2` in
`sprint/k6/WEAKEST.md` (an artefact of fitting a square of side `> 2` into the ball) is not
intrinsic: `1` is.  (For comparison, `m12` §5.3 proves the analogous sharpness for multiplicity
`3`, which is what makes the paper's multiplicity-two hypothesis essential.)

---

## 8. The exact boundary at six colours

Collecting §2–§7 with the record's Theorem B′.

**(8.1) Sufficient.**  `(W)`: `L ∩ B(y,R)` finite for some `R > 1` ⟹ Proposition 7.1 at `k = 6`
(`m12` Theorem B′, with the disk-form cover obstruction; `m12` also verifies that `§7` uses no
palette bound, and the only `k`-dependent constants are `α < 1/6` and `ℓ ≤ 6`).

**(8.2) The disk-removal stage uses much less.**  A covering/content bound **(C)** on `L₀`
(Theorem 1) suffices for Lemma 7.4, with holes of total radius `→ 0`, each cyclic centre inside a
hole.  So `(W)`'s *finiteness* is not what Lemma 7.4 needs.

**(8.3) The extraction uses exactly isolation.**  Theorem 3: at a non-isolated cyclic centre,
every annulus around it contains another hole, for every admissible hole family, at every scale.
So no fixed-radius hole-free annulus exists, Lemma 7.8 is inapplicable at every such centre, and
the "tiny annulus" variant degenerates (its continua shrink to `{x}`, and §8.1 needs a fixed
positive radial width).  Proposition 2 shows that, in the printed formulation, this is already
visible at the level of Lemma 7.4's counting.

**(8.4) The obstruction is topological, not a gap in the write-up.**  Theorem 3′: the natural
generalisation of Lemma 7.8 to a punctured annulus is false.  Holes are not a bookkeeping
problem: a non-null inner boundary can be "absorbed" by a hole.

**(8.5) No size condition can substitute.**  Theorem 4: a closed, perfect, `1`-dense, porous set
of zero upper `1`-dimensional Minkowski content on every compact exists.  So no hypothesis that
only measures how *small* `L` is can imply `(W)`; combining with (8.3), none can supply the
extraction either.  In particular the answer to `m15`'s suggestion is: **correct for Lemma 7.4
(Theorem 1), insufficient for Proposition 7.1 (Theorems 3, 3′, 4)**.

**(8.5′) One requirement is separate.**  Theorem 1 is stated for a region `Q` with
`∂Q ∩ L = ∅`, as in §7.2.  A covering bound **(C)** does not by itself produce such a `Q`: for a
closed null set `L` the set of translations `t` with `∂(Q+t) ∩ L ≠ ∅` can be all of the plane, so
content-zero does not make the boundary avoidable.  `(W)` does produce one: translate a fixed
closed square of side `> 2` inside `B(y,R)` so that its boundary avoids the finitely many points
of `L ∩ B(y,R)` (only finitely many translations are forbidden, since `∂Q ⊆ B(y,R)`).  So the
honest statement is: **(C) replaces the finiteness of `L₀` in Lemma 7.4, and nothing else**; the
clean-boundary requirement is weaker and independent.

**(8.6) The constant.**  Theorem 5: `R > 1` is the intrinsic threshold of the cover
obstruction; `R ≤ 1` gives no region on which the multiplicity-two component cover can be
contradicted, and `m12`'s density theorem shows that in general no ball of radius `> 1` is free.
So the sharp sufficient condition is `(W)` with `R > 1`, and the exact missing input is
**one isolated cyclic centre** (equivalently: a ball of radius `> 1`, or a closed square of side
`> 2`, meeting `L` finitely).

**(8.7) What a proof at a perfect `L` must do instead.**  By (8.3)–(8.4) such a proof cannot
extract continua from a fixed-radius annulus around one centre; it must use the accumulation
structure itself — e.g. a renormalisation/limit argument in which the continua are produced at
scales `ρ_n → 0` and a *new* argument converts the scale-`ρ_n` information at radius one into a
contradiction; or it must produce the `§8` strip restrictions (8.1) at a single centre without a
crossing lemma on a punctured annulus.  Nothing in the printed §7–§8 does either; the
"palette-level" and "strip-level" layers are already known to be powerless at `k = 6`
(`REPORT.md` §§4, 4b), and the present note closes the third layer, the topological one.

---

## 9. Files, and how to check everything

| file | content |
|---|---|
| `SHARP-HYPOTHESIS.md` | this note: Theorems 1, 3, 3′, 4, 5, Proposition 2, and §8 |
| `verify.py` | all exact/numeric checks: A (Theorem 3′), B (Theorem 5), C (Theorem 4), D (Theorem 1 bookkeeping) |
| `results.txt` | the output of `python3 verify.py` on this machine (`ALL CHECKS PASSED`) |
| `LEAN-NOTE.md` | what is machine-checked, what is not, and why |

Commands (from this directory):

```
python3 verify.py          # exits 0, prints PASS on all 20 checks
```

The paper's statements used here were read at two independent extractions and agree verbatim:
`pdftotext -layout` and `mutool draw -F txt` (Lemma 7.4 including "finite families `H_n`" and the
total-radius bound `|L₀|δ + m_{δ,ε} + η`; Lemma 7.6; Lemma 7.8; Proposition 7.1; §8.1's
"positive widths"; (7.1), (7.4), (7.6)).  The displayed formulas quoted in this note are (7.1),
(7.4) and the two displayed lines of Lemma 7.4's proof; both extractions give the same tokens.
