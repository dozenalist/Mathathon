# The null-set transfer lemma: boundary bookkeeping is unnecessary for an upper bound

**Verdict: VALID as a sufficient condition.** *(Revision note: an earlier version called (H)
"necessary", listed a half-plane as a counterexample, said a colouring of the complement "is" a cell
assignment, and graded compactness "essential" simpliciter. All four are corrected below, each marked
**CORRECTION**.)* Its consequence for this project is
that a proper 6-colouring of the plane *minus the honeycomb skeleton* — with no assignment to the
skeleton at all — already implies `chi(R^2) <= 6`. The earlier blanket requirement ("boundary
ownership must be constructed before any 6-upper-bound consequence") is **wrong and is withdrawn**
(§7). This is a conceptual implication only: **we have no positive global 6-colouring candidate**, so
nothing here establishes any numerical bound. No computation in this block; source review only.

## 1. The lemma

**Lemma (null-set transfer).** Let `k >= 1` and `Z ⊆ C` with

  **(H)** for every finite `F ⊆ C` there is `t ∈ C` with `(F + t) ∩ Z = ∅`.

Let `c : C \ Z → {1,…,k}` be **proper on `C \ Z`**: for all `x, y ∉ Z` with `|x - y| = 1`,
`c x ≠ c y`. Then `chi(R^2) <= k`, i.e. there is a proper `k`-colouring of the whole plane.

*Proof.*
*Step 1 (each finite configuration is coloured).* Let `F ⊆ C` be finite and `G_F` the unit-distance
graph on `F`. By (H) pick `t` with `F + t ⊆ C \ Z`, and put `d x := c (x + t)` for `x ∈ F`. If
`x, y ∈ F` and `|x - y| = 1` then `|(x+t) - (y+t)| = 1` with both points outside `Z`, so
`d x = c(x+t) ≠ c(y+t) = d y`. Hence `G_F` is `k`-colourable.
*Step 2 (all finite subgraphs).* The plane unit-distance graph `Γ` on `C` has, up to restriction, the
finite vertex sets of `C` as its finite vertex sets; by Step 1 every finite subgraph of `Γ` is
`k`-colourable.
*Step 3 (compactness, de Bruijn–Erdős).* A graph is `k`-colourable if all its finite subgraphs are
(the finite-intersection property in the compact product `∏_{v ∈ V} {1,…,k}`, Tychonoff). Hence `Γ`
is `k`-colourable. ∎

**What the conclusion is not.** The global colouring produced is *some* proper `k`-colouring of the
plane, obtained from the finite characterisation; there is no reason for it to agree with the supplied
`c` on `C \\ Z`, and the argument gives no control over that. In particular the lemma does not say that a
colouring of the complement "extends"; it says a plane colouring exists. Any use of it that needs
pointwise agreement on `C \\ Z` needs an extra argument, which this lemma does not supply.

*Choice.* Step 3 is Tychonoff's theorem

*Quantifier order matters.* `t` depends on `F`, and one cannot replace this by one global translate:
a `t` with `(C + t)` disjoint from `Z` needs `Z = empty`. Within **this** proof the compactness step is
therefore not removable, since the finite characterisation is the only device used to uniformise over `F`.

**CORRECTION.** An earlier version said compactness was "essential, not convenient", which grades it as
indispensable to any proof. That is not established and is not claimed: it is *used* here, and the one
alternative device tried here (a single global translate) is unavailable, but a different argument -
an explicit transfinite construction, or a definable/measurable selection - might avoid it entirely.


## 2. Hypothesis (H) holds for null sets, and the good translations are conull

If `Z` is Lebesgue-null then for finite `F`, `⋃_{x ∈ F} (Z - x)` is a finite union of null sets, hence
null, hence `≠ C`. So *almost every* `t` works, not merely one. The same argument goes through
verbatim for any `Z` with this finite-union property, e.g. `Z = Q^2` (dense, null): finite unions of
translates of `Q^2` are `Q^2 ≠ C`. So "closed", "thin" or "1-dimensional" are irrelevant; **null is
the operative hypothesis**.

**Some hypothesis is needed**, or the lemma is false: with `k = 1`, `Z = C` the complement is empty, so
the empty function is vacuously a proper 1-colouring of it, while `chi(R^2) <= 1` is false (`{0,1}`
is a unit edge).

**CORRECTION (second revision) - the embeddability reformulation was WRONG.** An earlier version
asserted the equivalence

    chi(R^2) <= chi(C \\ Z)   <=>   every finite unit-distance graph embeds as a subgraph of Gamma(C \\ Z).

**The necessity direction is false.** A chromatic inequality is a statement about a supremum of finite
chromatic numbers; it does not recover which subgraphs occur. A graph can have large chromatic number
while omitting a given small one: `chi` says nothing about embeddability. (Sufficiency of embeddability
does hold, trivially - embeddability into `Gamma(C \\ Z)` gives `chi(G_F) <= chi(C \\ Z)` - but that is the
wrong direction for the present purpose and is withdrawn as an equivalence.)

**The correct criterion is k-dependent and about colouring, not embedding** (de Bruijn-Erdos):

    chi(R^2) <= k   <=>   every finite unit-distance graph realisable in R^2 is k-colourable.

Both directions are valid in ZFC. The transfer argument delivers exactly the right-hand side, with
`k` the number of colours on the complement: a finite configuration `F` is translated into `C \\ Z`, the
global colouring restricts to it, and `F` is `k`-colourable. So the lemma gives `chi(R^2) <= k`; and
since `chi(C \\ Z) <= chi(R^2)` always (an induced subgraph), a domain satisfying (H) has
`chi(C \\ Z) = chi(R^2)`. That equality is a chromatic statement and is **not** an embeddability statement.

**H is only a sufficient *geometric* criterion**, and is used for one job: making the translation step
work. It is not necessary (a domain can satisfy the k-colourability criterion while failing (H)), and it
is not the content of the theorem. What is necessary and sufficient for `chi(R^2) <= chi(C \\ Z)` is the
k-colourability criterion above, at `k = chi(C \\ Z)`.

## 3. Applied to the honeycomb skeleton

Let `B` be the union of the boundaries of all cells of a regular honeycomb tiling. `B` is a countable
union of closed line segments, so `B` is null; by §2 hypothesis (H) holds, with the bad translations
forming a null set. Hence:

> If there is a proper 6-colouring of `C \ B`, then `chi(R^2) <= 6`.

`B` being a *regular* honeycomb is not used; any tiling by closed convex cells with null skeleton works.
Note `C \\ B` is the disjoint union of the cell interiors: a point in no cell boundary lies in exactly
one interior. So the *domain* of a colouring of the complement is that disjoint union, and no point of
the skeleton is ever coloured - no ownership rule is needed.

**CORRECTION - cell-constancy is an extra hypothesis.** An earlier version said such a colouring *is*
"an assignment of colours to cells, constant on each interior". False as stated: an arbitrary
colouring of the complement is an arbitrary function, and an interior, though connected, need not be
monochromatic. Cell-constancy must be assumed explicitly; only under it does the problem become the
Cayley graph of section 4. The lemma itself never uses cell structure, so it applies either way.

## 4. The equivalence that makes this usable (and the within-cell condition)

For a cell-constant assignment `gamma : cells → {1,…,k}` with `k >= 2`:

  `gamma` is proper on `C \ B`  ⟺  (i) `diam(C) <= 1` (`2a <= 1` for hexagon circumradius `a`), and
                                   (ii) `gamma(mu) ≠ gamma(nu)` for every pair with
                                        `dmin(nu - mu) < 1 < dmax(nu - mu)` **strictly**.

*Proof.* (⟸) Take `x ∈ int C_mu`, `y ∈ int C_nu` with `|x - y| = 1`. If `mu = nu` then (i) forbids it:
the interior distance set of a convex cell of diameter `D` is `(0, D)`, and the maximum `D` is attained
only at vertices, hence on the boundary — so `2a <= 1` gives `1 ∉ (0, 2a)`. If `mu ≠ nu` then `1` lies
in the interior-to-interior distance set, whose closure is `[dmin, dmax]` and which contains every
value strictly between; so `dmin < 1 < dmax`, and (ii) applies. (⟹) conversely a strict-forced pair has
interior points at distance exactly `1`, which properness of `gamma` must separate. ∎

So the constraint graph on cells is **exactly** `Cay(Z^2, F_strict)` with `F_strict = {v : dmin(v) <
1 < dmax(v)}` — the graph used in every certificate in this directory. In particular:

* **Within-cell pairs are handled by `2a <= 1`**, not by an extra edge type. At `2a = 1` exactly (the
  endpoint `a = 1/2`) the interior distance set is `(0,1)` and `1` is *not* attained, so `a = 1/2` is
  admissible — consistent with `CELL-NOGO-v2.md`.
* **Non-strict "tangency" edges must not be reintroduced.** A pair with `dmin = 1` or `dmax = 1` has
  its unit pairs only on the skeleton, which is uncoloured, so it imposes *no* constraint. The weak
  (closed-cell) criterion `dmin <= 1 <= dmax` used by the retiring rectangle worker would
  over-constrain. At `a = 1/5` this is exactly ring 3 (`N = 3`, `dmax = 1`), and our certificates use
  the strict graph, so nothing needs re-deriving.

## 5. The distinction the supervisor asked for: all interiors vs one finite patch

* **A colouring of ALL cells** — e.g. a genuinely SAT periodic quotient, which colours every coset of
  `Z^2`, hence every cell — is a colouring of the whole of `C \ B`, so by §3 it gives `chi(R^2) <= 6`
  **with no further work**. The "interior labels only" caveat I attached to such a result was wrong
  (§7); there is no residual boundary step to perform.
* **A SAT colouring of ONE finite patch does not suffice.** The patch colours the interiors of finitely
  many cells, i.e. a bounded region. In Step 1 the translate `F + t` must land inside the coloured
  region; for a patch of diameter `D_p` that is impossible for any unit-distance graph of diameter
  `> D_p` — and such graphs exist at every size (a chain of `n` unit edges has diameter `n`). So Step 1
  fails for all large graphs and no compactness conclusion follows. A finite patch establishes only
  "these cells can be coloured", which is why `PATCH-PREREGISTRATION.md` and `A-QUARTER.md` were
  careful to claim nothing beyond the family.
* **CORRECTION - a half-plane does not fall to that objection.** An earlier version listed a half-plane
  alongside a strip; that was wrong. A closed half-plane `H` satisfies (H): for finite `F`, translate far
  enough along the inward normal and `F + t` lies in `H`. So by section 1 a proper 6-colouring of a
  *half-plane* would also give `chi(R^2) <= 6`. The lemma is not about thinness.
* **CORRECTION (third revision) - the strip case, done properly.** Two errors to remove. First, an
  early version blamed diameter ("graphs of larger diameter cannot be translated in"); that is wrong,
  because a chain can be laid flat along the axis. Second, the repair I gave next was also wrong-headed:
  it asked whether some *realisation* of a graph fits in the strip, and invoked rigidity of a
  triangulated patch. **That is a different criterion.** `(H)` is about translating each *given* finite
  point set, with its coordinates fixed, by a translation only - no rotations, no re-realisation. So the
  question is never "can this graph be realised inside the strip"; it is "does every finite point set
  have a translate inside the strip".

  With that read, a fixed-width strip fails `(H)` **trivially**, with no edges and no rigidity. Let
  `S = {z : |Im z| <= w/2}` and take the two-point set `F = {0, (w+1) i}`. A translate of `F` has the
  same vertical separation `w+1`, so `F + t` can never lie in `S`. Hence `(H)` fails for every
  fixed-width strip, by a counterexample of two points at distance `w+1` (a unit-distance graph with
  two vertices and no edges, so it is admissible).

  The rigidity claim about triangulated triangular-lattice patches is **withdrawn entirely**: it is
  unsupported here (I gave no proof that all its unit-distance realisations are congruent), and it is
  not needed for anything.



## 6. The asymmetry, which matters strategically

For the honeycomb family the lemma gives an asymmetric transfer:

* **Negative (UNSAT) result ⟹ nothing about `chi(R^2)`.** This is why every exclusion in this
  directory is labelled a *restricted family* result. Correct and unchanged.
* **Positive (SAT) result ⟹ the full upper bound.** A proper colouring of the *forced graph on all
  cells* at any admissible `a` gives `chi(R^2) <= 6` outright.

So the honeycomb cell family is not merely "a restricted family" for the upper-bound programme: it is
a **sufficient** family. It is not necessary, of course. Concretely, a 6-colouring of
`Cay(Z^2, F_strict(a))` for any `a <= 1/2` would settle `chi(R^2) <= 6` — and by the certificates in
this directory no such `a` lies in the accepted no-go interval `(1/sqrt28, 1/2]`, so the only
untried range is `a <= 1/sqrt28`.

**Interval status.** The accepted honeycomb family no-go is now
`(1/sqrt28, 1/2] = (0.188982, 0.5]`. It is assembled from three parts: the two certified 73-cell patches
at `a = 1/5` and `a = 1/4`, covering `(1/sqrt28, 1/sqrt12)`; and, per the geometry chat's `K_7` audit
received this block, the older `T^2`-clique extension through `a = 1/2`, now accepted with properness
stated explicitly. Above `a = 1/2` the family is vacuous (a cell interior then contains a unit pair).
So the only untested range is `a <= 1/sqrt28`, and that is the sliver referred to in section 6.

## 7. Repair: the withdrawn requirement

`CELL-NOGO-v2.md` §1 stated: *"A positive result ... additionally requires colouring the 1-skeleton so
that no boundary point is at distance 1 from a point of its own colour — a separate step, unproven
here."* By §1 that step **does not exist**. The requirement is withdrawn in place (banner added), and
the same repair is applied to `RECOVERY.md`'s "still owes an ownership rule on the 1-skeleton".

What a positive cell-family result would now need is exactly: `2a <= 1`, a colouring of **all** cells,
and separation on the **strict** forced pairs. Nothing else. (The interior criterion is not merely
sound but, by §4, exactly the right one.)

## 8. What is already machine-checked, and what a formalisation would cost

Both halves of the mechanism are already in the tree, wired the other way round:

* `lean/OAI/Geometry/PlaneColoring/Converse.lean`, `exists_properColoring_of_finset`: *"if every finite
  set of points admits a proper colouring, then the whole plane does (Tychonoff compactness in
  `C → Fin k`)"* — this is Step 3, at exactly the generality needed.
* `lean/OAI/Geometry/PlaneColoring/NullSetRobust.lean`, `not_proper_five_coloring_compl_null`: its
  proof contains precisely Step 1's mechanism — *"every finite configuration can be translated off
  `Z` (the bad translations form a finite union of null sets), so a 5-colouring of `C \ Z` would give
  one of every finite configuration, hence — by compactness — one of the plane"* — but it is used
  **contrapositively**, to prove a *lower* bound.

So the lemma is not new mathematics: it is those two lemmas re-assembled with the contradiction
removed and `Fin 5` replaced by `Fin k`. A formalisation would be a short corollary in the
`PlaneColoring` namespace (`proper_coloring_compl_null_of_null : volume Z = 0 → (proper k-colouring of
`C \ Z`) → ∃ c, ProperColoring k c`), reusing `finite_density_realization` /
`measure_preimage_add_right` and `exists_properColoring_of_finset`. **Not attempted in this block** (no
Lean builds). I have read those two files this block but have not re-checked their proofs line by line,
and I make no claim about their axiom dependencies beyond what `results/VERIFICATION.md` already
records.

## 9. Evidence grades

| item | grade |
|---|---|
| Lemma, Steps 1–3, and the necessity of (H) | **proof** (elementary, ZFC via Tychonoff) |
| (H) holds for null `Z`, with a conull set of good translations | **proof** (finite union of null sets is null) |
| `C \ B = ⊔ int C`, so a colouring of `C \ B` is a cell assignment | **proof** (tiling: disjoint interiors, union the plane) |
| §4 equivalence, including `2a <= 1` and `a = 1/2` admissible | **proof**; the interval-image fact is Lemma 1(1) of `CELL-NOGO-v2.md`, whose exact endpoint behaviour was certified computationally earlier |
| `exists_properColoring_of_finset` states the compactness step | **source read this block**; not built or re-checked |
| "a positive colouring would give `chi(R^2) <= 6`" | **conditional implication** — the antecedent is currently FALSE for `a` in the accepted no-go interval `(1/sqrt28, 1/2]` by our certificates and the `K_7` audit, and has no candidate elsewhere |
| any numerical bound on `chi(R^2)` | **none is established here** |
