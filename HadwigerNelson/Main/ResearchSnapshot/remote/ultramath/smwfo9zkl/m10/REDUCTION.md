# The two-centre palette CSP at six colours **is** the plane's unit-distance graph

Swarm `smwfo9zkl`, member m10, direction d3 ("translation-exclusion two-centre CSP at k = 6").
Everything below is proved here from the paper's own statements; every computation is exact and
has two independent decision procedures. Reproduction commands are in §9.

---

## 0. Result, in one paragraph

Formalise the **pointwise** two-centre palette system at level `k` (palettes are nonempty label
sets of size at most `k-3`; every exclusion of §5 becomes "two nodes whose `pi`-images are at
distance 1 get disjoint label sets", where `pi(x,e) = x+e` and `pi(p) = p`). Then, for every finite
configuration,

> **the system is satisfiable iff its conflict graph is `k`-colourable, and the conflict graph is
> the plane's unit-distance graph pulled back along `pi`.**

Two consequences, both one line each:

1. **The palette-cardinality freedom is invisible.** Sizes 1, 2, 3 all give the *same*
   satisfiability verdict, because `A |-> min A` turns any labelling into a proper colouring and
   singletons turn any colouring into a labelling. No "3-palette" can defeat a pointwise
   two-centre constraint system.
2. **Step 3 is not a relaxation of the problem — it is the problem.** A finite two-centre CSP that
   is UNSAT at `k = 6` exists **iff** a finite unit-distance graph with chromatic number at least
   seven exists. That is exactly the classical target, and no such graph is known. So the whole
   palette machinery of §5, used pointwise, can never decide the six-colour question.

What survives, and is exactly where the six-colour content must come from, are the paper's
**three non-exclusion palette facts**: the *containment* facts of Definition 5.1 / the state groups
of §6.3, the *non-containment* fact (6.2) at transition-graph edges (which rests on the area
measure of Definition 6.1), and the sector facts of Lemma 8.1. §6 shows, on the paper's own
Lemma 6.4 configuration, that the `k`-dependence of the five-colour argument sits entirely in the
first of these, and is the arithmetic statement `k-3 <= 2`.

Nothing below claims a lower bound for `chi(R^2)`. What is claimed is a complete proof that a
precise and currently active class of candidate arguments cannot produce one.

---

## 1. The paper's statements used, and how each was checked

`pdftotext -layout` drops fractions and radicals, so every displayed formula used here was
re-derived algebraically and checked numerically to 40 digits (`mpmath`), and, where it enters a
computation, verified **exactly** in `Q(sqrt 3, sqrt 11, ...)` by `sympy` radical arithmetic
(`twocentre.is_zero`, `unit_gap_exact`).

| paper item | statement used | check |
|---|---|---|
| Lemma 5.2 (1), display (5.2) | `c(x+e+v) ∉ P_x(e) ∪ P_x(v)` for a.e. independent pair `(e,v)` | used as stated |
| Lemma 5.2 (3), display (5.3) | `P_z(f) ∩ P_x(s(f)) = ∅` for `z+f = x+s(f)+t(f)`, `s,t` non-parallel unit, `s` a local diffeo | used as stated |
| Remark 5.3 | `t` may be constant; `(x+a)+f = x+f+a` is admissible off `f = ±a` | used as stated |
| Corollary 5.4, display (5.7) | `P_x(f) ∩ P_x(Rf) = ∅`, `R` = rotation by `pi/3` | used as stated |
| Lemma 5.5 | `Theta_d(t) = t + Im log(1+de^{-it})`, `alpha_pm = Theta_d(t) ± arccos(|d+e^{it}|/2)`, and `y + e^{it} = x + e^{i alpha_+} + e^{i alpha_-}` for `y = d`, `x = 0` | re-derived: `d+e^{it} = rho e^{i Theta}` with `rho = |d+e^{it}|`, so `e^{i alpha_+} + e^{i alpha_-} = rho e^{i Theta}`; max residual over `d ∈ {0.1,0.3,0.49}` and 40 values of `t` was `5.5e-41`; and **exactly** (`sympy`, no floating point) at `d = 1/2`, `cos t = 3/5` |
| Lemma 6.4 | `gamma = 2 arcsin(1/(2 sqrt 3))`, `cos gamma = 5/6`, `sin gamma = sqrt 11 / 6`; `z_j = x + e^{i(t+2j kappa)} + e^{i(t+pi+gamma+2j kappa)}` form an equilateral triangle of side 1 at distance `1/sqrt 3` from `x` | `cos gamma = 5/6` exactly; `\|1 - e^{i gamma}\|^2 = 1/3` exactly; the three vertices were built exactly in `Q(sqrt 3, sqrt 11)` and their three squared side lengths are exactly 1 (`probes.lemma64_points`) |
| Definition 5.1, Proposition 5.6 | palette is nonempty, `\|P_x(e)\| <= 2` at `k = 5`; at `k = 6` the bound `1 <= \|P\| <= 3` from `results/K6-BARRIER.md` §1 | the domain of a palette node |
| Definition 6.1, (6.1) | transition graph `Gamma_x` via the *area* condition `limsup D_ij(B,h)/\|h\| > 0` | **not** representable pointwise — see §6 |
| Lemma 6.2, display (6.2) | `ij ∈ Gamma_x => P_x(e) ⊄ {i,j}` a.e. | **not** an exclusion — see §6 |

Note in passing that the paper's `gamma` (Lemma 6.4) is the Moser-spindle angle: with
`cos gamma = 5/6`, `\|\sqrt 3 - \sqrt 3 e^{i gamma}\| = 1`, which is exactly the join that makes the
Moser spindle `K4`-free yet not 3-colourable. This is used in §7 as the calibration test.

---

## 2. The pointwise two-centre system

**Definition.** A *probe* is a finite set `V` of nodes, each of one of two kinds:

* a **colour node** `('c', p)` at a plane point `p`, with domain the singletons `{i}`, `i < k`;
* a **palette node** `('p', x, e)` at a centre `x ∈ R^2` and a unit vector `e`, with domain the
  nonempty subsets `A ⊆ {0,...,k-1}` with `|A| <= k-3`.

Write `pi('c',p) = p` and `pi('p',x,e) = x + e`. Two nodes `u,w` are **adjacent** iff
`|pi(u) - pi(w)| = 1`. A **labelling** assigns each node a member of its domain, and adjacent nodes
must receive **disjoint** sets.

Three remarks on faithfulness.

* A palette node is a palette `P_x(e)`; its domain is the paper's palette bound. The colour node is
  the actual colour at a point.
* **Every exclusion of §5 is an instance of the adjacency rule.** (5.2): `|(x+e+v)-(x+e)| = |v| = 1`.
  (5.3): `|(z+f)-(x+s)| = |t| = 1`. (5.7): `|f - Rf| = 2 sin(pi/6) = 1`. Properness of two typical
  points at unit distance: `|p-q| = 1`.
* The non-parallelism hypothesis of (5.3) is **automatic**: if `pi`-distance is 1 then
  `|s+t| = 1` with `|s| = |t| = 1`, so `cos angle(s,t) = -1/2` and `angle(s,t) = 2pi/3`.
* The *local-diffeomorphism* hypothesis of (5.3) was audited edge by edge (`branch_audit.py`): for
  every palette-palette edge of every probe used below, `max` over the two orientations of
  `|d alpha / d theta|` at the edge's free direction is at least `0.5`, so each edge is a genuine
  instance of (5.3) in at least one orientation. (Only one of the two branches of a sum can be
  degenerate at a given free direction, so this is the correct criterion.)

---

## 3. Theorem A (min-map): satisfiability is a colouring problem

**Theorem A.** For every probe and every `k >= 4`, the probe is satisfiable iff its conflict graph
`Pi(probe)` is `k`-colourable.

*Proof.* (`=>`) Given a labelling `L`, put `chi(v) = min L(v)`. If `u ~ w` then `L(u) ∩ L(w) = ∅`,
and two disjoint nonempty sets have different least elements, so `chi(u) != chi(w)`. Thus `chi` is a
proper `k`-colouring. ( `<=` ) Given a proper `k`-colouring `chi`, put `L(v) = {chi(v)}`. This is
nonempty, of size `1 <= k-3` (as `k >= 4`), and respects the colour-node domain; adjacent nodes get
different labels, hence disjoint sets. ∎

Two immediate corollaries.

**Corollary A1 (palette size is invisible).** Replacing the bound `|P| <= k-3` by `|P| <= m` for any
`1 <= m <= k-3` does not change satisfiability, for any probe, any `k >= 4`. In particular the
`1 / 2 / 3`-label alternatives at `k = 6` are equivalent. *This contains the m16 "shrink lemma"
(`(C1)-(C3)` implies `|Q_i| <= 2`) as the special case in which the probe is the six palettes of one
cyclic centre.* The reason the shrink lemma composes with "pair-satisfied" predicates is exactly
min-map.

**Corollary A2.** The verdict depends only on the finite point set `pi(probe)`: two probes with the
same `pi`-image have the same verdict, and adding palette nodes can only add points to that image.
The label sets themselves carry no information beyond their minima.

---

## 4. Theorem B (pullback): the conflict graph is the plane's unit-distance graph

Let `V_inf = R^2 × (S^1 ∪ {0})`, `pi(x,u) = x + u`, and let `Pi_inf` be the graph on `V_inf` with
`u ~ w <=> |pi(u) - pi(w)| = 1`. (Colour nodes are the slice `u = 0`; palette nodes are the slice
`u ∈ S^1`.)

**Theorem B.** `chi(Pi_inf) = chi(R^2)`. Indeed `Pi_inf` is the pullback of the plane's
unit-distance graph along the surjection `pi`.

*Proof.* (`>=`) The slice `u = 0` is an isomorphic copy of the plane's unit-distance graph, so a
`k`-colouring of `Pi_inf` restricts to a proper `k`-colouring of the plane. (`<=`) If `c` is a proper
`k`-colouring of the plane then `c ∘ pi` is a proper `k`-colouring of `Pi_inf`, since `Pi_inf`'s
edges are `pi`-pullbacks of unit-distance pairs. ∎

**Theorem C.** The full pointwise two-centre system at level `k` is satisfiable iff `chi(R^2) <= k`.

*Proof.* (`=>`) Theorem A applied to the full system, then restrict the resulting colouring to the
slice `u = 0`, which is the plane's unit-distance graph (Theorem B). ( `<=` ) The labelling
`v |-> {c(pi(v))}` of Theorem A. ∎

**Theorem D (the exact boundary of the route).** There is a finite probe that is UNSAT at level `k`
**iff** `chi(R^2) >= k+1`.

*Proof.* (`<=`) By de Bruijn–Erdős, `chi` of an infinite graph is the supremum of the chromatic
numbers of its finite subgraphs, so some finite point set `P` has unit-distance graph needing more
than `k` colours; take colour nodes at all points of `P`. ( `=>` ) An UNSAT probe's `pi`-image is a
finite point set whose unit-distance graph is not `k`-colourable. ∎

**Corollary D1.** At `k = 6`, a finite two-centre CSP that is UNSAT exists iff a finite
unit-distance graph with chromatic number `>= 7` exists. **No such graph is known**; its existence is
equivalent to `chi(R^2) >= 7`. Hence Step 3, in pointwise form, is *not* a relaxation of the problem.

**Corollary D2 (a non-constructive corollary of the five-colour theorem).** Since `chi(R^2) >= 6` is
proved (and machine-checked in this repo), de Bruijn–Erdős gives a **finite** unit-distance graph
that is not 5-colourable, hence a finite probe that is UNSAT at level 5. The paper's proof is
measure-theoretic (Lemma 5.5 and Lemma 6.4 are the places where the continuum does the work) and it
does not exhibit such a graph, so the framework correctly predicts an object that the route itself
cannot produce. That is the sharpest internal check on its faithfulness.

**Correction to a claim in the brief.** The brief states that "a pointwise finite two-centre system
collapses to the trivial bound `n <= k`". That is true only for a system consisting of `n` pairwise
disjointness constraints on `n` palettes (a clique). The faithful pointwise system also contains
the plane's own unit-distance graph (the colour-node slice, supplied by (5.2)), and then it does not
collapse: by Theorem D it decides the problem. The trivial bound and the exact reformulation are
different objects, and Step 3 must use the second.

---

## 5. What is *not* an instance of the rule

The reduction is exact for exclusions. The paper's palette argument also uses three facts that are
**not** of the form "two things are disjoint":

1. **Containment** (Definition 5.1 + the essential supports): at a direction in the state set `A`,
   the palette *contains* the represented state group: `{X} ⊆ P_x(a)` for a singleton state,
   `D ⊆ P_x(b)` for a pair state. The palette is an essential union of traces, so it is an upper
   bound on what the traces see, and the states give lower bounds.
2. **Non-containment at transition edges** (Lemma 6.2, display (6.2)): `ij ∈ Gamma_x` forces
   `P_x(e) ⊄ {i,j}`. This is a lower bound on `P_x(e)`, and `Gamma_x` is defined by the **area**
   condition (6.1) — `limsup_h D_ij(B,h)/|h| > 0` — which is not a pointwise property of a probe.
3. **Sectors** (Lemma 8.1): `P_i ∩ O_i ≠ ∅` and `P_i ∩ I_i ≠ ∅` for the six orbit directions at a
   cyclic centre; again lower bounds, derived from the ray geometry of §8.

Since `min` ignores lower bounds, Theorem A says nothing about systems containing them, and they are
the only possible source of extra power. §6 shows that at `k = 6` the first of them is exactly
where the five-colour contradiction stops.

---

## 6. Where Lemma 6.4 is a `k <= 5` argument, exactly

Take the paper's own Lemma 6.4 configuration: `x = 0`, `gamma` with `cos gamma = 5/6`,
directions `a_j = t + 2j pi/3`, `b_j = t + pi + gamma + 2j pi/3`, and the points
`z_j = e^{i a_j} + e^{i b_j}` — an equilateral triangle of side exactly 1 at distance `1/sqrt 3`
from `x` (verified exactly). Lemma 6.4 uses

* the pullback part: `colour(z_j) ∉ P_x(a_j) ∪ P_x(b_j)` (a (5.2) instance, `|z_j - x - a_j| = 1`)
  and `z_j, z_l` at unit distance;
* the state part: `{X} ⊆ P_x(a_j)` and `D = {1,2} ⊆ P_x(b_j)`, plus the size bound.

Decided exactly, with two procedures (`lemma64_diag.py`):

| constraint set | `k=5`, `|P|<=2` | `k=6`, `|P|<=3` | `k=7`, `|P|<=3` |
|---|---|---|---|
| pullback only | **SAT** | **SAT** | **SAT** |
| pullback + state containments | **UNSAT** | **SAT** | **SAT** |

The reason is arithmetic and complete: `colour(z_j)` must avoid `{X} ∪ D`, a set of size 3, so
`k-3` labels remain for three pairwise unit-distant points; the three points need three distinct
labels, so a contradiction needs `k-3 <= 2`, i.e. `k <= 5`. At `k = 6` the leftover set has size 3
and the triangle is properly 3-coloured. The explicit `k = 6` model is in `lemma64_diag.json`.

**Therefore the missing six-colour input, stated exactly, is:** a true constraint forcing
`|P_x(a) ∪ P_x(b)| >= 4` — with a common 2-element complement across the three `j` — for the
same-centre direction pairs `(t+2j pi/3, t+pi+gamma+2j pi/3)` at a cyclic centre. No pointwise
exclusion supplies it (§3–§4); it must come from the containment/measure facts of §5.

---

## 7. Decided computations

All exact (`sympy` radical arithmetic; every adjacency used in a certificate re-checked exactly);
two independent decision procedures (exact backtracking over label *sets*, and Glucose3 on the
colouring formulation); every SAT verdict proof-carrying (the labelling is re-verified against the
exact conflict graph, and `min` of it is re-verified to be a proper colouring).

### 7.1 Calibration (vacuity test)

The Moser spindle, built exactly in `Q(sqrt 3, sqrt 11)` with vertices `0`, `sqrt 3`,
`sqrt 3/2 ± i/2`, `sqrt 3 e^{i gamma}`, and the last two unit-circle intersections:

| `k` | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|
| verdict | UNSAT | **UNSAT** | SAT | SAT | SAT |

So the pipeline reproduces a known obstruction exactly — the Moser spindle has chromatic number 4 —
and, as it must, stops doing so at `k = 4`. The mechanism is sensitive at exactly the right place.

### 7.2 The paper's own configurations at `k = 6`

| probe | nodes / edges | `k=4` | `k=5` | `k=6` |
|---|---|---|---|---|
| Lemma 6.4 gamma-triad (3 sum points + 36 orbit palettes) | 39 / 129 | SAT | SAT | **SAT** |
| Lemma 5.5 two-centre pair `d = 1/2` (18 orbit palettes) | 18 / 20 | SAT | SAT | **SAT** |
| hexagonal-lattice patch, 9 centres x 6 directions + 9 colours | 63 / 276 | SAT | SAT | **SAT** |
| six palettes of one cyclic centre (the `(C1)+(C3)` half of the m5/m6 interface CSP) | 6 / 6 | SAT | SAT | **SAT** |

Every one is satisfiable at `k = 6`; the two procedures agree on all 17 records; every model is
verified. Note the last row: the *exclusion* half of the m5/m6 interface CSP is a 6-cycle, i.e.
2-colourable. That CSP's satisfiability at `k = 6` (177 of 7776 geometries at `(k,ell) = (6,6)`,
m16's `cal_csp_results.json`) therefore lives **entirely** in its non-exclusion constraints `(C2)` —
consistent with §5.

### 7.3 Two-centre sweep over the Lemma 5.5 geometry

27 exact probes: `d ∈ {1/10, 1/5, ..., 9/10}` times free directions
`t ∈ {(3,4), (5,12), (8,15)}` (Pythagorean, so `cos t, sin t` are exact rationals), each with both
branches `alpha_pm` computed exactly for every free direction, every direction at every centre
closed under the full `60°` orbit, and the (5.2) colour nodes at `x + alpha_+ + alpha_-` added.
Each probe has 84 nodes and 120 edges.

Result: **every one of the 27 conflict graphs is bipartite; `chi = 2`.** Hence the pointwise
two-centre system is satisfiable at `k = 4`, `5` and `6` for all of them, and (Corollary A1) for
every palette bound `m ∈ {1,2,3}`: 243 decisions, all SAT, both procedures agreeing, every model
verified.

Read against the theory: this is forced. A probe is only UNSAT at `k` if its point set is not
`k`-colourable, and a point set taken from two circles cannot be badly chromatic. The point of the
computation is the class it rules out, not the number: **no two-centre configuration of the paper's
Lemma 5.5 type, with six free directions and full orbit closure, carries any pointwise obstruction
at six colours.**

### 7.4 Validation of Theorem A

150 random probes (4 to 14 nodes, centres on a `Q(sqrt 3)` grid, directions from an exact
twelve-direction catalogue plus `gamma`), decided at `k = 4,5,6` and palette bounds `1,2,k-3`:
900 records, **0 disagreements** between the two procedures, **0 violations** of
size-independence, 0 UNSAT verdicts, every SAT verdict re-verified.

---

### 7.5 Third, fully independent check

`independent_check.py` re-derives the load-bearing numbers with nothing from `twocentre.py` —
plain `math`/`cmath` and a different colouring algorithm:

```
Lemma 5.5 identity: max residual = 6.087e-16        (float precision limit)
cos gamma = 0.833333333333333   (5/6 = 0.833333333333333)
Lemma 6.4: |z_j| = 0.577350269190 (x3)   side lengths = 1.000000000000 (x3)
Moser spindle: 7 points, 11 unit edges, chromatic number = 4 (exhaustive search)
two-centre probes that are NOT bipartite: none (27/27 bipartite)
```

---

---

## 8. What this does not do

* It does not decide `chi(R^2)`, and it does not prove or refute local finiteness at `k = 6`.
* It does not say that §7 cannot be transferred at six colours. It says that the part of the
  palette system expressible as pointwise disjointness cannot do it, and it names — §5, §6 — the
  three facts outside that class which any successful transfer must use.
* The sweep of §7.3 covers 27 configurations, not all of them; §3–§4 is what makes the negative
  conclusion general, and the computation is a check, not the argument.
* Theorem D's "iff" uses de Bruijn–Erdős for one direction. The other direction, and everything in
  Theorem A, is elementary and does not use choice.
* Theorems A–D are *exact*: no a.e. qualifier, no genericity, no measure theory. The reason is that
  the only direction that needs care is `chi <= k  =>  satisfiable`, and there the labelling
  `v |-> {c(pi(v))}` satisfies every constraint identically, not merely almost everywhere. So the
  a.e. structure of (5.2)/(5.3) adds no satisfiability power over the pointwise exclusions; what the
  paper's measure theory buys is the *density* consequences (Lemma 5.2(2)) and the transition-graph
  data, which are not exclusions at all (§5).

---

## 9. Reproduction

```
cd .ultramath/smwfo9zkl/m10
python3 probes.py             # §7.1, §7.2  -> probes_out.json
python3 sweep2.py             # §7.3        -> sweep2_out.json
python3 validate_theorem.py    # §7.4        -> validate_out.json
python3 lemma64_diag.py       # §6          -> lemma64_diag.json
python3 branch_audit.py       # §2, (5.3) local-diffeomorphism audit (= 0.5 minimum)
python3 independent_check.py   # §7.5, third code path, no shared library
```

Files: `twocentre.py` (geometry, adjacency, the two decision procedures, the verifier),
`probes.py`, `sweep2.py`, `validate_theorem.py`, `lemma64_diag.py`, `branch_audit.py`, and the four
`.json` outputs. Note on `k <= 3`: the palette bound `|P| <= k-3` is empty there, so every probe is
trivially UNSAT at `k <= 3`; Theorems A–D are stated for `k >= 4`, and the validation script
therefore runs `k >= 4`.
Dependencies: `sympy`, `mpmath`, `python-sat` (`Glucose3`), all present in the VM image.
