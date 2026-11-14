# The null-set transfer lemma: boundary bookkeeping is unnecessary for an upper bound

**Verdict: VALID**, with the hypothesis stated precisely below. Its consequence for this project is
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

*Choice.* Step 3 is Tychonoff's theorem for a product of continuum many finite discrete spaces: a
theorem of ZFC, no extra hypotheses. Nothing else uses choice.

*Quantifier order matters.* `t` depends on `F`. It is **not** possible to replace this by one global
translate: a single `t` with `(C + t) ∩ Z = ∅` needs `Z = ∅`. So the compactness step is not a
convenience — without it there is no way to pass from "the colouring misses `Z`" to a plane colouring.

## 2. Hypothesis (H) holds for null sets, and the good translations are conull

If `Z` is Lebesgue-null then for finite `F`, `⋃_{x ∈ F} (Z - x)` is a finite union of null sets, hence
null, hence `≠ C`. So *almost every* `t` works, not merely one. The same argument goes through
verbatim for any `Z` with this finite-union property, e.g. `Z = Q^2` (dense, null): finite unions of
translates of `Q^2` are `Q^2 ≠ C`. So "closed", "thin" or "1-dimensional" are irrelevant; **null is
the operative hypothesis**.

**The hypothesis is necessary.** Take `k = 1`, `Z = C`. Then `C \ Z = ∅` and the empty function is
vacuously a proper 1-colouring of `C \ Z`, but (H) fails, and the conclusion `chi(R^2) <= 1` is false
(`{0, 1}` is a unit edge). Any statement of the lemma without (H) is false.

## 3. Applied to the honeycomb skeleton

Let `B` be the union of the boundaries of all cells of a regular honeycomb tiling. `B` is a countable
union of closed line segments, so `B` is null; by §2 hypothesis (H) holds, with the bad translations
forming a null set. Hence:

> If there is a proper 6-colouring of `C \ B`, then `chi(R^2) <= 6`.

`B` being a *regular* honeycomb is not used; any tiling by closed convex cells with null skeleton
works. Note `C \ B = ⊔_cells int(C)`: a point in no cell boundary lies in exactly one interior, so a
colouring of `C \ B` **is** an assignment of colours to cells, constant on each interior. No point of
the skeleton is ever coloured, so no ownership rule is ever needed.

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
* The same objection kills a colouring of a *strip*, a *half-plane* or any proper region: the
  translation must be free to place `F + t` anywhere.

## 6. The asymmetry, which matters strategically

For the honeycomb family the lemma gives an asymmetric transfer:

* **Negative (UNSAT) result ⟹ nothing about `chi(R^2)`.** This is why every exclusion in this
  directory is labelled a *restricted family* result. Correct and unchanged.
* **Positive (SAT) result ⟹ the full upper bound.** A proper colouring of the *forced graph on all
  cells* at any admissible `a` gives `chi(R^2) <= 6` outright.

So the honeycomb cell family is not merely "a restricted family" for the upper-bound programme: it is
a **sufficient** family. It is not necessary, of course. Concretely, a 6-colouring of
`Cay(Z^2, F_strict(a))` for any `a <= 1/2` would settle `chi(R^2) <= 6` — and by the certificates in
this directory no such `a` lies in `(1/sqrt28, 1/2]`, so the only untried range is the sliver
`a <= 1/sqrt28`.

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
| "a positive colouring would give `chi(R^2) <= 6`" | **conditional implication** — the antecedent is currently FALSE for `a in (1/sqrt28, 1/2]` by our certificates, and has no candidate elsewhere |
| any numerical bound on `chi(R^2)` | **none is established here** |
