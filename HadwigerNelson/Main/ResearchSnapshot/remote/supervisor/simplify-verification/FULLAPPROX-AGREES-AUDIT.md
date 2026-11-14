# The `FullApprox.agrees` interface: assumption/conclusion map against paper Lemmas 7.4 and 7.8

Follow-up to `INTERFACE-WALL.md` §2, which named this interface as the earliest point where §7's
compiled chain stops certifying the paper. This note maps it exactly. **Nothing here is a claim that
the interface is wrong**: it separates (a) what is already proved in the tree, (b) what is proved but
which I have not audited, and (c) what the topology substitution would still have to be wired into.

Grades: **[K]** compiled in the tree as part of the 78-module build (prior report, statement read by
me); **[S]** statement read, proof body not audited; **[P]** paper text, read in
`attachments/here-are-three-files-ni5n/paper.pdf` via `paper-layout.txt` at the line numbers given.

## 1. The Lean object

```
structure FullApprox (c : ℂ → Fin 5) (α t : ℝ) where      -- FullApproximation.lean:255
  ε : ℝ;  ε_pos;  ε_lt : ε < t
  disks : Finset MarkedDisk
  positive  : ∀ d ∈ disks, 0 < d.radius
  disjoint  : pairwise disjoint closed balls
  sum_lt    : (∑ d ∈ disks, d.radius) < t
  map       : C(closedBall 0 5, GraphSpace (⊤ : SimpleGraph (Fin 5)))
  agrees    : ∀ z ∈ closedBall 0 5,  z.val ∉ diskHoles disks  →
                (map z).val = thresholdMap c ε α z.val      -- :264-265
```

`agrees` is the field in question. The field is produced, not assumed: `fullApprox_exists`
(`:330`) closes the structure from `hc`, `hw`, `0 < α < 1/5`, `t > 0` alone.

## 2. Assumption → conclusion map

| Lean item | paper counterpart | relation |
|---|---|---|
| `disks`, `positive`, `sum_lt`, `ε < t` | Lemma 7.4 preamble: "finite families `H_n` of open disks with pairwise disjoint closures such that their total radii tend to zero" **[P]** l. 2358–2360 | `sum_lt` is the "total radii tend to zero" budget at a single scale; `disjoint` is the closure-disjointness; `ε < t` is the scale's smallness relative to the budget |
| `disks` contains a disk about every cyclic centre (`L` finite, `hL`), plus `D = centerDisks A R` with `R ≤ s/4` and `hRsep` giving separation `2R < dist` | Lemma 7.4 (1): for each `x ∈ L₀` exactly one core disk `B_{n,x}`, contains `x`, different points different disks **[P]** l. 2361–2366 | same content; `L` plays `L₀`, and `fullApprox_exists` supplies `L` from `cyclicCore_compact_finite` (Theorem 6.5), which is **proved in the tree** **[K]** |
| `map : C(closedBall 0 5, GraphSpace ⊤)` | Lemma 7.4 (2)–(3): the map `q_{ε_n}` takes values in the graph `G` off the holes, and `g_n` is continuous on `Q` minus the core disks, **equal to `q_{ε_n}` outside all open disks of `H_n`** **[P]** l. 2367–2374 | `agrees` is exactly "equal to `q_ε` outside the holes"; `thresholdMap c ε α` is the tree's `q_ε` (barycentric threshold on the disk-average palette). That `thresholdMap` *is* the paper's `q_ε` is a definition-fidelity claim I have **not** audited — it is the one place where the interface's meaning depends on a comparison I did not check |
| `map`'s continuity | Lemma 7.4 (3) "obtained by filling the non-core disks through trees, preserving their boundary values" **[P]** | continuity is the whole point of the filling; `C(...)` carries it |
| homogeneity: `map` is defined on `closedBall 0 5`, `HoleApprox.map` on `closedBall 0 7 \ coreHoles` | Lemma 7.4 works on `Q` with `Q` the closed square / disk | in-tree restriction `7 → 5`; harmless for §7.4 whose cover lives on `closedBall 0 5` |

## 3. Which source theorems discharge each premise

Chain for `fullApprox_exists` (`:330-335`):

```
fullApprox_exists
  ← cyclicCore_compact_finite            CyclicCore.lean:269   [K]  (Theorem 6.5, per cycle length:
                                                                      threeCenter/fourCenter/fiveCenter_compact_finite)
  ← fullApprox_exists_of_finite_core     FullApproximation.lean:268
       ← finite_centers_separation       GraphPatches.lean:239
       ← holeApprox_exists               HoleApproximation.lean:291  [S]  (paper Lemma 7.4 (1)(2): ε, disks, map on
       │    ← small_hole_map                                            closedBall 0 7 minus core holes, agreeing off
       │                                                               diskHoles)
       ← HoleApprox.eventually_fill_cores FullApproximation.lean:206 [S]  (paper Lemma 7.4 (3): adds the centre disks,
       │                                                               re-budgets radii, produces F with the SAME
       │                                                               agreement, transported through diskHoles_union)
       ← MarkedDisk.separate              (enlarges/shrinks the disk family to be disjoint within t/4)
       ← disk_radius_sum_union_le, centerDisks_sum  (radius bookkeeping)
```

**[RETRACTED (block 16): `connected_escape_holes` is NOT the counterpart of Lemma 7.8 — see
`LEMMA78-COMPARISON.md`. It is a point-displacement lemma for a preconnected set; 7.8 itself has no Lean
counterpart and is made unnecessary by the dichotomy at `Five.lean:94`.]** And in the *other* §7.4 branch, `Mesh.no_large_positive_sequence` (`Mesh.lean:92`) uses
`connected_escape_holes` (`Mesh.lean:12`) and `straddle_connected_unit`
(`AngularBoundary.lean:156`) — these are the tree's counterparts of Lemma 7.8 ("a connected midpoint
preimage crosses the annulus", paper l. 2564) and of the connectedness sentence of (7.1).

**Status of the bodies.** Everything above exists as a theorem with a proof term in the tree; none of
them is a hypothesis or an `axiom`, and the tree is reported `sorry`-free with the three standard
axioms [K, prior report; I re-read the statements only]. I have **not** audited the proofs of
`small_hole_map`, `holeApprox_exists`, `HoleApprox.eventually_fill_cores`, `connected_escape_holes`,
or `MarkedDisk.separate`. So the honest label is:

* `agrees` is **proved, unaudited** — not an open mathematical gap, and not (by itself) evidence of a
  gap either;
* the audit that would settle it is statement-level: does each auxiliary's conclusion say what the
  paper's corresponding lemma says, at the same strength, or is it weakened on the way (e.g.
  agreement only off a larger exception set, only on a dense subset, or with `thresholdMap`'s
  parameters relaxed)?

## 4. What the topology substitution does and does not touch here

Nothing. `supervisor/simplify-topology/lean/CoverObstruction.lean` reproves paper **Lemma 7.5** (the
cover obstruction) with symbolic constants. Lemma 7.5 is consumed at `Five.lean:54` *inside*
`graph_map_small_mesh_impossible`, i.e. **downstream** of the palette bound and **independent** of the
`agrees` construction: the cover obstruction takes a continuous graph-valued map as given. Hence:

* compiling the substitution changes nothing about `agrees`, `small_hole_map`, `holeApprox_exists` or
  `eventually_fill_cores`;
* the substitution's own remaining integration work is the separate item already recorded in
  `TRANSFER-LEDGER.md` and `INTERFACE-WALL.md` §1: no module of `lean/` references
  `paper_lemma_7_5` / `compact_cover_obstruction_gen`, so §7's compiled content is still
  `PlanarCover.compact_open_cover_impossible`. A referee who wants the substitution *used* needs a
  source edit at `Five.lean:54` plus a rebuild of the 25-module cone.

## 6. The bounded definition/quantifier audit (block 8)

### 6.1 `thresholdMap` versus the paper's `q^ε` — definition level

Paper, p. 44, l. 2340–2346:

$$\pi^\varepsilon_i(q)=\frac{1}{\pi\varepsilon^2}\int_{B(0,\varepsilon)} a_i(q+v)\,dv,\qquad
q^\varepsilon_i(z)=\frac{(\pi^\varepsilon_i(z)-\alpha)^+}{\sum_{k\in I}(\pi^\varepsilon_k(z)-\alpha)^+}\qquad (7.4)$$

Lean (`GraphRealization.lean:243-248`):

```
def thresholdWeight c ε α q i := max (diskAverage c ε i q - α) 0
def thresholdTotal  c ε α q   := ∑ i, thresholdWeight c ε α q i
def thresholdMap    c ε α q i := thresholdWeight c ε α q i / thresholdTotal c ε α q
```

| paper | Lean | verdict |
|---|---|---|
| $(x)^+$ | `max x 0` | identical |
| $\pi^\varepsilon_i(z)-\alpha$ | `diskAverage c ε i q - α` | identical, *given* `diskAverage` = $\pi^\varepsilon$ |
| $\pi^\varepsilon_i(q)=\frac{1}{\pi\varepsilon^2}\int_{B(0,\varepsilon)}a_i(q+v)dv$ | `diskAverage c ε i q = ∫ v, colorFn c i (q+v) ∂diskLaw ε` (`DiskAverages.lean:33`) | **the one sub-link not closed**: `diskLaw ε` must be the normalised uniform law on `B(0,ε)`. Its normalisation is consistent with the proved `diskAverage_sum`/`diskAverage_le_one`, but I did not read `diskLaw`'s definition |
| denominator positive because the probabilities sum to one | `thresholdTotal_pos` (`GraphRealization.lean:249`, from `1-5α ≤ Σ` and `α<1/5`) | same estimate, same hypothesis `α < 1/5` |
| "$q^\varepsilon$ is a continuous map into the simplex" | `thresholdMap_sum` ($\sum_i = 1$) and `thresholdMap_nonneg` | identical |
| "In particular $q^\varepsilon_i(z)>0$ iff $\pi^\varepsilon_i(z)>\alpha$" | `thresholdMap_pos : 0 < thresholdMap c ε α q i ↔ α < diskAverage c ε i q` (`:265`) | identical, same direction |
| "$G$ = one-skeleton of the simplex" | `graphRealization G := {p ∣ ∃ i j, (i=j ∨ G.Adj i j) ∧ ∃ t ∈ Icc 0 1, p = graphEdgePoint i j t}` (`:93`); for `G = ⊤` this is "supported on at most two vertices, weights summing to 1" | identical. In particular "the map takes values in $G$" is *not* a free statement: it is membership in `graphRealization`, which is exactly "at most two coordinates are positive", i.e. the conclusion of the missing-edge overlap bound (paper Lemma 7.3). In the tree that membership is carried by the **codomain type** `GraphSpace ⊤` of `FullApprox.map`/`HoleApprox.map`, and its discharge is inside `small_hole_map` (unaudited). |

So at the definition level the two `q`'s are the same formula, with one open sub-link (`diskLaw`'s
normalisation) and one structural translation ("takes values in G" = `graphRealization ⊤` membership =
"≤ 2 positive coordinates").

### 6.2 The quantifiers, stated explicitly

**Paper Lemma 7.4** (l. 2358–2374):
$$\exists (\varepsilon_n)_{n},\ \varepsilon_n\downarrow 0,\quad \exists (H_n)_n \text{ finite families of open disks},\quad \forall^{\text{a.e. } n}\Big[(0)\ \partial B \text{ pairwise disjoint},\ (0')\ \textstyle\sum_{B\in H_n}\mathrm{rad}(B)\to 0,\ (1)\ \text{core disks},\ (2)\ q^{\varepsilon_n}\text{ lands in }G\text{ off }\textstyle\bigcup H_n,\ (3)\ \exists g_n \text{ continuous},\ g_n=q^{\varepsilon_n}\text{ off }\bigcup H_n\Big].$$

The "for all sufficiently large $n$" is the quantifier $\forall^{\text{a.e.}} n$ — *not* $\forall n$, and the objects $(\varepsilon_n)$, $(H_n)$ are chosen **before** it.

**Lean** (`fullApprox_exists`, `:330`):
$$\forall \alpha\in(0,1/5),\ \forall t>0,\quad \mathrm{Nonempty}\,\big(\mathrm{FullApprox}\ c\ \alpha\ t\big),$$
i.e. **one scale per budget**, with the fields $\varepsilon<t$, $\sum\mathrm{rad}<t$, and the agreement holding **for all** $z\in\overline B(0,5)$ off the holes — no $n$, no eventual quantifier, and the scale $\varepsilon$ is existentially quantified inside the structure rather than chosen first as a sequence.

### 6.3 Are they interchangeable? Yes, in the direction the argument uses — and here is the selection

* **Paper ⇒ Lean ("one scale from an eventually-true sequence").** Let $t>0$. Since $\varepsilon_n\downarrow 0$, the set $\{n : \varepsilon_n<t\}$ is **cofinal** (indeed all $n\ge N$). Intersect with the cofinite set on which Lemma 7.4's items hold; the intersection is nonempty. Take such an $n$: its $(\varepsilon_n,H_n,g_n)$ is a `FullApprox` at budget $t$. *No diagonal and no choice beyond picking one integer*; cofinality of $\{n : \varepsilon_n<t\}$ inside the eventual set is the whole selection lemma. Monotonicity of $(\varepsilon_n)$ is discarded and not used.
* **Lean ⇒ Paper ("sequence from per-scale existence").** Put $t_n:=\min(1/16,1/(n+1))>0$; by the Lean form each $\mathrm{FullApprox}\ c\ \alpha\ t_n$ is nonempty; `Classical.choice` selects one per $n$. Then $\varepsilon_n<t_n\to 0$, and every item holds for **all** $n$, so in particular for all sufficiently large $n$. This is countable choice (the standard `Classical.choice` of the tree), instantiated in-tree at `Five.lean:105–113`, where exactly this $t$ is used and `no_large_positive_sequence` consumes the resulting sequence with `Tendsto t atTop (𝓝 0)` and $t_n\le 1/16$.

**Outcome.** The two forms are interchangeable modulo one genuine difference:

> **[RETRACTED in §7.2.]** The paragraph below claimed that the Lean form does not give a
> monotone decreasing $(\varepsilon_n)$ and that "monotonicity cannot be restored for free". That is
> wrong: shrinking $\varepsilon$ blocks *modifying a witness*, not *selecting among witnesses*, and
> §7.2 gives two constructions (strictly decreasing subsequence; recursive budgets
> $t_k=\min(1/(k+1),\varepsilon_{k-1}/2)$) that carry the whole $(H_n,g_n)$ and every witness. The
> original text is kept as the record of the error.
>
> ~~Extra hypothesis / loss.~~ The Lean form does **not** give a *monotone decreasing*

Nothing else differs at the quantifier level. Two non-quantifier instance differences already recorded: the paper works on a closed square $Q$ of side ten with $\partial Q\cap L=\varnothing$ and a larger $Q'$, the Lean on $\overline B(0,5)$ with $\overline B(0,7)$/$(0,8)$ for the core; and the paper's $L_0=L\cap Q'$ finite by Theorem 6.5 versus the Lean's `L` from `cyclicCore_compact_finite` — same content, different ambient sets.

### 6.4 What this audit changes

* `thresholdMap` = paper's $q^\varepsilon$ at the definition level, with **one** open sub-link (`diskLaw`'s normalisation) — so the interface's *meaning* is pinned; this was §2's dangling comparison.
* The quantifier shapes are not merely "similar": the implication in the used direction is a one-line cofinality argument, and the reverse is countable choice, already instantiated in the tree. So the paper's "for all sufficiently large $n$" and the Lean's "one scale per $t$" **are** interchangeable, with the single recorded loss of monotonicity.
* Neither of these is a mathematical gap. They are two comparisons that a referee can now check by reading §6.1–§6.3 against the cited lines; the bodies of `small_hole_map`, `holeApprox_exists`, `eventually_fill_cores` remain **proved in tree, unaudited**.

## 7. Closing the two open items (block 9)

### 7.1 `diskLaw` — the sub-link is CLOSED

`DiskAverages.lean:9-17`:

```
def diskLaw (ε : ℝ) : Measure ℂ := (volume (Metric.ball (0:ℂ) ε))⁻¹ • volume.restrict (Metric.ball 0 ε)
lemma diskLaw_probability {ε} (hε : 0<ε) : IsProbabilityMeasure (diskLaw ε)
def colorFn (c) (i) (z) : ℝ := if c z = i then 1 else 0
def diskAverage (c) (ε) (i) (q) : ℝ := ∫ v, colorFn c i (q+v) ∂diskLaw ε      -- :33
```

So `diskLaw ε` is the **normalised** Lebesgue measure on `B(0,ε)` — `diskLaw_probability` closes the
normalisation at `ε > 0` — and `colorFn c i` is the indicator of the colour-`i` set. Hence

$$\texttt{diskAverage}\ c\ \varepsilon\ i\ q=\frac{1}{\mathrm{vol}\,B(0,\varepsilon)}\int_{B(0,\varepsilon)}\mathbf 1_{\{c=i\}}(q+v)\,dv,$$

which is the paper's $\pi^\varepsilon_i(q)=\frac{1}{\pi\varepsilon^2}\int_{B(0,\varepsilon)}a_i(q+v)dv$
(l. 2342) as soon as $\mathrm{vol}\,B(0,\varepsilon)=\pi\varepsilon^2$. Two remarks, neither a gap:

* the Lean writes the normaliser as a measure of the ball, not as $\pi\varepsilon^2$, and **never needs
  the numeric value**: only normalisation (`diskLaw_probability`) and absolute continuity
  (`diskLaw_absolutelyContinuous`) are used. So the identification is at the level of *meaning*, and
  any argument in the tree is insensitive to the constant.
* the Lean assumes `Measurable c` where the paper's weak colouring is measurable only modulo null sets
  (Definition 1.2 and the remark after it). That convention difference is already carried elsewhere in
  the project (`AEMeasurable` in `WeakColoring`); it does not affect $\pi^\varepsilon$.

With §6.1, the definition-level audit of `thresholdMap` against $q^\varepsilon$ is now **complete**:
same formula, same three consequences, same "one-skeleton" reading, same averaging kernel.

### 7.2 RETRACTION: monotonicity of $(\varepsilon_n)$ is *not* lost

> **Retracted.** §6.3 called "no monotone decreasing $\varepsilon_n$" the single loss of the
> interchange. That is wrong. The obstruction I had in mind — shrinking $\varepsilon$ changes
> $\pi^\varepsilon$ and hence the disk family and the agreement map — bars *modifying a witness*, not
> *selecting among witnesses*. Both of the following give strict monotonicity along with the entire
> associated data.

**(a) Subsequence selection.** Any sequence with $\varepsilon_n>0$ and $\varepsilon_n\to0$ has a
strictly decreasing subsequence: put $n_0:=0$ and, given $n_k$, choose $n_{k+1}>n_k$ with
$\varepsilon_{n_{k+1}}<\varepsilon_{n_k}/2$; this is possible because $\varepsilon_n\to0$ and
$\varepsilon_{n_k}>0$. Then $n_k\to\infty$ and $\varepsilon_{n_k}$ is strictly decreasing. The whole
family $(H_{n_k}, g_{n_k})$ and every witness travels with the index, and each item of Lemma 7.4 holds
at $n_k$ for all large $k$ because the set of good indices is cofinite.

**(b) Recursive budgets, directly from the Lean form.** With $\varepsilon_{-1}:=1$, define
$t_k:=\min\big(1/(k+1),\ \varepsilon_{k-1}/2\big)>0$ and choose
$A_k:\mathrm{FullApprox}\ c\ \alpha\ t_k$. Then $\varepsilon_k<t_k\le\varepsilon_{k-1}/2$ — strictly
decreasing — and $\varepsilon_k<1/(k+1)$, so $\varepsilon_k\to0$. This uses only the field
`FullApprox.ε_lt` and `ε_pos`, i.e. exactly the "$\varepsilon<t$" the supervisor pointed to.

### 7.3 Do the extra indexed bounds survive reindexing? All of them, and why

| bound, with its exact source | shape | under $n\mapsto n_k$ |
|---|---|---|
| `FullApprox.ε_lt : ε < t` (`FullApproximation.lean:258`) | per-index, budget-relative | preserved: $t_k$ is the budget actually chosen |
| `FullApprox.sum_lt : Σ_{d∈disks} rad d < t` (`:263`) | per-index, budget-relative | preserved; gives $\Sigma_k\to0$ since $\Sigma_k<t_k\to0$. **Monotone decrease of the sums is not obtained and not used** — the paper asks only that they tend to zero (l. 2359) |
| `hsmall : ∀n, t n ≤ 1/16` (`Five.lean:110`) | uniform constant | preserved |
| `huR : ∀n, 2*u n < R`, `hult : u n < 1/2`, `hut : u n < t` (`FullApproximation.lean:295-299`) | per-index, fixed constants from the budget | preserved |
| `L`, `A := activeCenters L`, `R ≔ min (s/4) …` (`:273-274`) | fixed once, not indexed by $n$ | untouched: reindexing does not change $L$; the paper likewise fixes $L_0=L\cap Q'$ once (l. 2352) |
| `2*t n < dist (x n) (y n)` (`Mesh.lean` `hxy'`) | derived per index from $2<\mathrm{dist}$ and $t_n\le1/16$ | preserved |
| `Tendsto t atTop (𝓝 0)` (`Five.lean:106`) | asymptotic | preserved under composition with strictly increasing $\varphi$; instantiated in-tree as `ht.comp hφ.tendsto_atTop` |
| paper's "$\forall^{\text{a.e.}}n$" / cofinite good set | cofinite | preserved: a cofinite set meets a cofinal subsequence in a cofinal set |
| paper's non-nesting of core disks across $n$ (item (1): "for each $x\in L_0$ precisely **one** disk $B_{n,x}$", nothing about $n$-to-$n+1$) | no cross-index constraint | nothing to preserve |
| `HoleApprox.eventually_fill_cores` (`:206`) takes the **whole sequence** `a : ∀n, HoleApprox c α L (u n)` and returns one index $n$ | sequence-level hypothesis | apply it to $a\circ\varphi$; its hypotheses ($u\circ\varphi\to0$, per-index bounds) hold as tabled above. **No adjacency or consecutive-index use anywhere**, so this is not an obstruction |

The one thing a reader must accept is the choice principle: pointwise `Nonempty` ⇒ sequence is
countable choice, and the recursive form is dependent choice; both are `Classical.choice`, and the
tree already performs exactly this step at `Five.lean:105-113`.

### 7.4 Corrected quantifier chain

```
PAPER (Lemma 7.4, l. 2358-2374):   ∃ (ε_n)↓0, ∃ (H_n), ∀ᶠ n, [P(n) : (1) core, (2) lands in G off ⋃H_n, (3) g_n = q^{ε_n} off ⋃H_n]
LEAN  (fullApprox_exists, :330):   ∀ t > 0, ∃ ε<H,g>, P at budget t     [ε<t, Σrad<t, agreement for ALL z off holes]

LEAN ⇒ PAPER   : 7.2(b) with t_k = min(1/(k+1), ε_{k-1}/2); P holds at every k, so a fortiori ∀ᶠ k; ε_k strictly ↓.
PAPER ⇒ LEAN   : given t>0, cofinality of {n : ε_n<t} within the cofinite good set gives one n; that witness is a FullApprox at budget t.
ROUND TRIP     : reindex by the subsequence of 7.2(a); P is preserved by 7.3's table.
VERDICT        : interchangeable, INCLUDING strict monotonicity. Cost: countable/dependent choice and one reindexing.
```

**No obstruction is isolated**, because there is none: every constraint the paper attaches to the
index is either per-index with a uniform constant, budget-relative, asymptotic, or about a set fixed
once. The earlier "single loss" was my error and is retracted in place (§6.3 now points here).

## 8. Does selecting on ε also give the budget and the radii? (block 12)

**The point raised.** `FullApprox` gives `ε < t` (`ε_lt`) and `Σ_{d∈disks} rad d < t` (`sum_lt`). It
does **not** give `t ≤ C·ε`. So a sequence whose *ε* tends to zero carries no information about the
budget `t`, nor about the total radii — which is what the paper's Lemma 7.4 actually asks for
("their total radii tend to zero", l. 2359). A selection theorem stated on ε alone would therefore be
applied to the wrong quantity.

**CORRECTION (block 13).** §8 as first written then slid between two different recursions: it said to
instantiate with `scale := t` and then wrote the rule `t_n := min(ε_{n-1}/2, 1/(n+2))`. Those are not
the same recursion. With `scale := t` the generic lemma's rule reads

$$t_n=\min\big(t_{n-1}/2,\ 1/(n+2)\big),$$

i.e. the next budget depends on the previous **budget**, not on the previous `ε` — and it gives *no*
information about the ordering of the `ε_n`: each `ε_n` is merely some number in `(0, t_n)` and may move
up and down. What is true, and what is enough for everything except the monotone-`ε` form, is:

> `t_n → 0`, `0 < ε_n < t_n`, `Σ rad_n < t_n` ⟹ `ε_n → 0` **and** `Σ rad_n → 0`.

Two legitimate routes, each a literal instantiation of the *same* generic lemma; they must not be mixed.

### Route A — `scale := t` (budget-driven), then one reindexing

1. `W := Σ (t : ℝ), FullApprox c α t`, `scale ⟨t, A⟩ := t`, `P := True`.
2. `hsmall` here is verbatim `fullApprox_exists : ∀ t > 0, Nonempty (FullApprox c α t)`
   (`FullApproximation.lean:330`).
3. Generic conclusion: `(∀ n, 0 < t_n) ∧ (∀ n, t_{n+1} < t_n) ∧ (∀ n, t_n < 1/(n+1)) ∧ Tendsto t 0`.
4. **Inherited, per index, from the fields**: `ε_n < t_n < 1/(n+1)` and `Σ rad_n < t_n < 1/(n+1)`;
   with nonnegativity (`ε_pos`, `Finset.sum_nonneg`) both tend to `0` by squeeze.
5. **Not inherited**: `ε_{n+1} < ε_n`.
6. **To get monotone `ε`, reindex.** From `ε_n → 0` and `ε_n > 0`, for every `n` the set
   `{m > n : ε_m < ε_n/2}` is nonempty (convergence to `0` makes `{m : ε_m < ε_n/2}` cofinite, and a
   cofinite set meets `{m > n}`). Dependent choice gives `φ` strictly increasing with
   `ε_{φ(n+1)} < ε_{φ(n)}/2`; then `ε_{φ(n)}` is strictly decreasing and, since `φ(n) ≥ n`,
   `t_{φ(n)} < 1/(φ(n)+1) ≤ 1/(n+1)` and `Σ rad_{φ(n)} < t_{φ(n)}`, so the reindexed sequence keeps
   budget convergence, radius convergence and `t`-monotonicity. Whole witnesses are carried; nothing is
   rebuilt.

### Route B — RETRACTED as written (block 14)

> **Retracted.** The claim was that instantiating the generic lemma at `scale := ε` with
> `hsmall s := "a witness at budget s/2"` yields per-index budgets `t_n = s_n/2`. It does not:
> `pickAt` returns `⟨Classical.choose (hsmall s hs), _⟩`, and `Classical.choose_spec` supplies **only**
> `Good scale P w ∧ scale w < s` — the field `t` of the returned witness is whatever `hsmall` produced,
> with **no** recorded relation to `s/2`. My proof *exhibited* a witness at budget `s/2`; that does not
> make the chosen witness equal to the exhibited one, so no bound on `t_n` follows.

Two ways to salvage it, neither carried out here:

1. **Strengthen the choice specification.** Replace `hsmall`'s conclusion by
   `∃ w, Good scale P w ∧ scale w < s ∧ t w ≤ s/2` (i.e. carry the budget bound inside the witness type or
   as an extra conjunct of `P`). Then `pickAt`'s specification retains the budget bound and
   `t_n ≤ s_n/2 ≤ 1/(2(n+2)) → 0` goes through unchanged. This needs the generic lemma stated with the
   extra conjunct — i.e. `P` must be *the budget bound itself*, `P w := t w ≤ s/2`, which is not available
   inside a single generic statement because `s` changes with the step.
2. **A separate concrete choice.** Define the per-step object directly (not through `pickAt`):
   `stepB n prev := ⟨min (ε prev/2) (1/(n+2)) / 2, Classical.choose (fullApprox_exists (that/2))⟩`, and
   prove `(stepB n prev).1 ≤ 1/(2(n+2))` and `ε (stepB n prev) < (stepB n prev).1` by construction. This is
   a *different* recursion from the generic lemma's, as the objection says, and would need its own file.

**Consequence.** Route A stands alone as the correct direction: select whole witnesses by the **budget**,
`t_n = min(t_{n-1}/2, 1/(n+2))`-driven, get `t_n → 0`, hence `ε_n → 0` and `Σ rad_n → 0`, and then take a
strictly increasing subsequence making `ε` strictly decreasing — that step needs no choice inside the
witness (it reindexes the already-built sequence), which is why it is not exposed to this retraction.

Also corrected, in both routes: the selected scale is **strictly below** `min(previous/2, 1/(n+2))`
(`sel_step_lt` gives `<`, from `pickAt_lt`), never equal to it. Every bound derived from it therefore
holds with `<` and the inequalities used downstream are unaffected.

**Which suffices?** One single-scale lemma suffices for both routes; **no two-scale witness lemma is
needed**. Route A is the cheapest instantiation (its `hsmall` is literally the tree's theorem) and gives
everything after one reindexing; Route B gives monotone `ε` for free at the cost of a two-line
`hsmall` construction. Selecting on `ε` **without** the `s/2` step (i.e. pretending `ε` is arbitrarily
small while the budget floats) would leave `t` and the radii free — that is the error the objection
identifies and neither route commits it.

**Scope, stated to prevent promotion.** This is a statement about how to *instantiate* a selection
principle inside `fullApprox_exists`. It does not formalise the analytic bridge: the generic lemma says
nothing about `H_n`, `g_n`, `diskHoles`, `thresholdMap` or the cover obstruction, and nothing here
upgrades §7's status. The paper's Lemma 7.4 items (1)–(3) still rest on `small_hole_map`,
`holeApprox_exists` and `eventually_fill_cores` — **proved in tree, unaudited** — and Lemma 6.7 is
untouched.

## 9. Lemma 7.4 items (1),(2): source-to-paper comparison (block 13)

Paper Lemma 7.4 items (1)-(2), l. 2361-2368, and the Lean objects that carry them.

**Item (1).** Paper: *"For each `x ∈ L₀`, precisely one disk of `H_n` is designated the core disk
`B_{n,x}` and contains `x` in its interior. Different points give different core disks. If `x ∈ Q`,
then `B_{n,x} ⊂ int(Q)`; if `x ∉ Q`, then `B_{n,x} ∩ Q = ∅`."*

Lean counterparts (`DiskExtension.lean`):
```
structure MarkedDisk where  center : ℂ;  radius : ℝ;  core : Bool
def MarkedDisk.Valid (L : Set ℂ) (d) := 0 < d.radius ∧ (d.core = true → ∃ x ∈ L, x ∈ d.ball)
def coreHoles  (S : Finset MarkedDisk) := ⋃ d∈S, ⋃ (_ : d.core = true), d.ball
def diskHoles  (S : Finset MarkedDisk) := ⋃ d∈S, d.ball
def MarkedDisk.noncoreCost (d) := if d.core then 0 else d.radius
```
with `HoleApprox.valid : ∀ d ∈ disks, d.Valid (L : Set ℂ)` (`HoleApproximation.lean:285`) and
`HoleApprox.sum_lt : (∑ d ∈ disks, d.radius) < t` (`:287`).

| paper clause | Lean | verdict |
|---|---|---|
| a core disk contains its point `x ∈ L₀` in its interior | `Valid`: `core = true → ∃ x ∈ L, x ∈ d.ball` | **weaker**: existence, not "contains *this* `x`"; no injectivity of `x ↦ B_{n,x}`; no "precisely one" |
| different points give different core disks | — | **not stated** in the Lean |
| `B_{n,x} ⊂ int Q` for `x ∈ Q`, `B_{n,x} ∩ Q = ∅` for `x ∉ Q` | — | **not stated**; the Lean instead fixes the ambient ball `𝓑(0,7)` and separates disks by `MarkedDisk.separate` |
| total radii of the disks tend to zero | `sum_lt` bounds the **total** radius sum, while `noncoreCost` exempts core disks — the core disks are the ones the paper keeps at fixed scale | same content, different bookkeeping |

So item (1) is the one place where the Lean is *strictly weaker than the paper*: it records "a core disk
meets `L`" rather than "one core disk per point of `L₀`, injectively, inside `Q`". Grade **[S]**, and the
honest label is **a statement-level difference, not a proved equality**. Whether it is harmless is a
separate question (the argument uses item (1) only to keep the cores fixed while the other disks shrink;
`noncoreCost` is exactly that), but it is not something I have verified — so it is recorded as an open
audit item, not as a gap in the proof.

**Item (2).** Paper: *"The map `q_{ε_n}` takes values in `G` on `Q ∖ ⋃_{B∈H_n} B`."*

Lean: `HoleApprox.map : C(↥(closedBall 0 7 ∖ coreHoles disks), GraphSpace ⊤)` (`:288`) — the codomain
`GraphSpace ⊤ = graphRealization ⊤` *is* "values in `G`", and the domain already omits the **core** holes
— together with `HoleApprox.agrees` (`:289`): off `diskHoles disks` the map equals `thresholdMap c ε α`.
Since `coreHoles ⊆ diskHoles`, off **all** holes the map both equals `q^ε` and lands in `G`, which is
item (2) verbatim (the map is extended over the non-core holes by the tree filling, exactly as the
paper's item (3) says). Grade **[S]**: item (2) is reproduced, derived from codomain + `agrees`.

**Does the subsequence preserve items (1),(2)?** Yes, and for a structural reason worth stating: every
clause of items (1),(2) (and of (3), and of the fields `valid`, `disjoint`, `sum_lt`, `ε < t`) is a claim
about the *single index* `n` — there is no clause relating `n` to `n+1` (in particular the paper nowhere
requires the disk families to be nested, nor the maps to be compatible between scales). The only
cross-index quantifier in Lemma 7.4 is "for all sufficiently large `n`", which a cofinal subsequence
preserves. Hence reindexing by any strictly increasing `φ` with `φ(n) ≥ n` keeps items (1)-(3) and every
field, while inheriting the bounds `ε_{φ(n)} < 1/(n+1)`, `Σ rad_{φ(n)} < t_{φ(n)} < 1/(n+1)` from §8.
The one thing reindexing cannot fix is the *weakening* in item (1) — that is a statement-level gap in the
Lean, independent of any subsequence.

## 5. What would make the §7 claim referee-proof

1. `Five.lean:54` re-pointed at the substitution (or a note saying the substitution is a parallel
   statement and the tree's lemma is the one in force).
2. A statement-level comparison, paper Lemma 7.4 ↔ `HoleApprox` fields + `eventually_fill_cores`
   conclusion, at fixed quantifiers: the paper quantifies `n` and asks for the properties "for all
   sufficiently large `n`"; the Lean fixes one scale `t` and one `HoleApprox` per scale, with
   `u n → 0` supplied by the caller. That is the same content at a different quantifier shape, and
   saying so is the deliverable.
3. The same for Lemma 7.8 ↔ `connected_escape_holes`, including the annulus radii, which the paper's
   statement pins and the Lean's parameters I have not matched.

None of these is attempted here; each is a bounded, purely textual comparison once someone reads the
two proofs.
