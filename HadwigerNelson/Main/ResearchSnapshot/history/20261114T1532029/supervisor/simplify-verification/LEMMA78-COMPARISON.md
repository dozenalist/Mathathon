# `connected_escape_holes` vs paper Lemma 7.8 — they are not the same statement (mislabel retracted)

Block 16, analysis only. Grades: **[S]** source read; **[S+]** source read and the claim follows by the
cited lines; **[P]** paper; **[C]** my reading.

## 0. Retraction of my own earlier mapping

`INTERFACE-WALL.md` §2 and `FULLAPPROX-AGREES-AUDIT.md` §3 both listed
`connected_escape_holes` (`Mesh.lean:12`) as "the tree's counterpart of Lemma 7.8". **That is wrong**, and
the comparison asked for cannot be made as posed: the two statements have different objects, different
conclusions and different hypotheses. Details below. What survives is the answer to the real question —
*whether §7 needs Lemma 7.8 in the Lean at all* — which is section 3.

## 1. The two statements side by side

**Paper Lemma 7.8** (l. 2564–2569, statement read on the text):
> Let `B` be an open disk containing `x`, `B ⊂ B(x,ρ)`, `A = B(x,ρ) \ B`. Let `g : A → G` be continuous,
> `G` a finite connected simple graph, and suppose the image of the counterclockwise **inner boundary** has
> nonempty cyclically reduced word `W`. If `m` is the midpoint of an edge in `W`, then `g⁻¹({m})` has a
> **compact connected component meeting both boundary circles** of `A`.

Its proof uses: radial interpolation identifying `A` with a closed annulus, the fundamental group `≅ ℤ` via
winding, a compact-metric clopen partition argument, and a translated square grid whose cancelled boundary
yields a loop with nonzero winding, contradicting Lemma 7.7.

**Lean `connected_escape_holes`** (`Mesh.lean:9–13`, statement verbatim):
```
lemma connected_escape_holes {S : Finset MarkedDisk} {t : ℝ}
    (hS : ∀d∈S, 0≤d.radius)
    (hdis : (S : Set MarkedDisk).Pairwise (fun a b => Disjoint a.closedBall b.closedBall))
    (hsum : (∑d∈S, d.radius) < t) {K : Set ℂ} (hK : IsPreconnected K)
    {a b : ℂ} (ha : a∈K) (hb : b∈K) (hab : 2*t < dist a b) :
    ∃ a'∈K, a'∉diskHoles S ∧ dist a a' ≤ 2*t
```

| feature | Lemma 7.8 | `connected_escape_holes` |
|---|---|---|
| object | a continuous map `g` on an annulus | a **preconnected set** `K` and a disk family `S` |
| conclusion | `g⁻¹({m})` has a component meeting both boundary circles | a **point** `a' ∈ K` outside the holes, within `2t` of `a` |
| graph / word / winding | essential (reduced word `W`, winding number, Lemma 7.7) | none |
| annulus radii | `ρ` outer, inner boundary of `B`; conclusion is about both circles | no annulus; `t` is a **radius-sum budget**, and the displacement bound is `2t` |
| positivity | `ρ > r(θ) > 0` from the construction | `0 < t` is *derived*, `(Finset.sum_nonneg hS).trans_lt hsum`, not assumed |
| quantifier order | `∀ g, ∀ W ≠ ∅, ∃ component` (component depends on `g`) | `∀ S, ∀ t, ∀ K, ∀ a b, ∃ a'` — `a'` depends on everything, chosen after all data |
| role | feeds Proposition 7.1's continua `K_j` (l. 2622) | feeds the **mesh branch** of §7.4 |

So: not a weaker or stronger version of 7.8 — a different lemma that happens to be about holes.

## 2. Downstream trace of `connected_escape_holes` (as far as `Five.lean`)

```
connected_escape_holes                Mesh.lean:12
  ← used at Mesh.lean:102, :104        (inside no_large_positive_sequence, to push a and b
                                        out of the holes while keeping dist ≥ 3/2)
no_large_positive_sequence            Mesh.lean:92
  ← used at Five.lean:122             (the Mesh branch: a component of diameter > 2 at every
                                        scale contradicts the shrinking-budget theorem)
graph_map_large_positive              Five.lean:94   (the dichotomy that produces such a component)
  /  graph_map_small_mesh_impossible  Five.lean:22   (the other branch: cover obstruction)
no_measurable_weak_five_coloring      Five.lean:105
  → no_proper_five_coloring_algebraic Five.lean:130
```
Every step is a theorem with a proof term; the positivity and radius budget `t` enter as the *caller's*
choice (`t n = min (1/16) (1/(n+1))` at `Five.lean:106`), so `connected_escape_holes` never has to build a
sequence or a limit — it is used pointwise, once per scale.

## 3. Does §7 need Lemma 7.8 in the Lean? Apparently not — that is the architectural substitution

* There is **no** formal counterpart of 7.8, nor of 7.7's winding/word machinery: a grep for
  `winding`, `reducedWord`, `free_homotopic` over `lean/OAI/**/*.lean` returns **nothing** [S].
* The word "annulus" in the Lean means something else. **Corrected (block 17):** the actual definition is
  `diskAnnulus d = closedBall d.center (1 + d.radius) \ ball d.center (1 - d.radius)`
  (`HoleApproximation.lean:210-211`) — the closed band of points at distance in `[1 - r, 1 + r]` from the
  centre — and for `0 ≤ r ≤ 1` its area is `4πr` (`volume_diskAnnulus`, from `π(1+r)² - π(1-r)²`). My earlier
  description ("`ball(c, r+1)` minus `closedBall(c, r)`, a unit-thick rim") was wrong at **both** endpoints.
  Its purpose is the *exception set for exact unit distances*: `unit_from_disk_mem_annulus` proves
  `q ∈ d.closedBall → dist z q = 1 → z ∈ diskAnnulus d`, so the annuli charge area `4πr` per disk for the
  unit-circle contributions. It is not the paper's annular domain `B(x,ρ) \ B` [S].
* Instead of extracting continua via 7.4–7.8 and Proposition 7.1, the tree splits §7.4 into a
  **dichotomy** at `Five.lean:94`: either every positive-coordinate component has diameter ≤ 2 — then
  `PlanarCover.compact_open_cover_impossible` applies to the components — or some component has diameter
  > 2, and then `no_large_positive_sequence` kills it with `connected_escape_holes`. Both branches are in
  the tree; neither uses 7.6/7.7/7.8 [S].

**Consequence.** The earlier framing "Lemma 7.8 is the remaining uncompared §7 statement" is void: it is not
*fomalised-but-uncompared*, it is **not needed by the Lean's route**. Whether the paper's continua are needed
for anything the Lean does not do (they are not: the Lean reaches `no_measurable_weak_five_coloring`) is a
question about the paper's exposition, not about the development.

## 4. Mismatch with a consequence — stated exactly, once

One concrete difference does have a consequence, and it is the one worth recording:

> Paper 7.8's conclusion is about a **component of a preimage**, which is automatically closed in `A` and
> therefore compact there; the Lean lemma's object is an arbitrary **`IsPreconnected` set given as a
> hypothesis**, with no closedness assumed.

That is *not* a weakening for the Lean's use: `IsPreconnected` is exactly the hypothesis `graph_map_large_positive`
supplies (a connected component of a positive-coordinate set), and the escape conclusion needs no closedness
because it only moves a point inside `K`. If a future proof wanted 7.8's conclusion (a component meeting both
boundaries) it would need `K` to be a maximal connected component *and* closedness — neither is available from
`IsPreconnected` alone. So the gap is confined to a use the tree does not make.

## 5. The smallest check, run (source-level, no build) — and its outcome

**Check.** Is the continuum machinery in the dependency cone of `Five.lean`, and does anything play
Proposition 7.1's role?

**Result [S], import graph computed over `lean/OAI`:**

* the `OAI` import cone of `OAI.Geometry.PlaneColoring.Five` has **70 modules**; `Mesh`, `FullApproximation`
  and `ContinuumLimits` are all in it;
* `ContinuumLimits` is imported by **`FullApproximation.lean` alone**, and its declarations are analytic
  support, not continua: `ae_frequently_notMem_of_measure_tendsto_zero`, `ae_ne_one_of_eventual_bound`,
  `colorFn_locallyIntegrable`, `diskAverage_eq_average_ball`, `diskAverage_ae_tendsto`,
  `support_disjoint_open_of_ae`, `diskAverage_support_exclusion`, …
* nothing in the tree states an "exclusion continuum" or a component-meets-both-boundaries conclusion; the
  grep for `winding`/`reducedWord`/`free_homotopic` is still empty.

**Conclusion.** The module *named* `ContinuumLimits` contains no Proposition 7.1 counterpart — the name is
misleading. So the dichotomy at `Five.lean:94` is the only §7 route in the tree, and Lemma 7.8 (with 7.6 and
7.7) is **formally unnecessary rather than missing**. That is the architectural substitution, and it should be
said that way in any report, not as "§7 is proved modulo Lemma 7.8".

**What remains genuinely unchecked.** Whether the *paper's* Proposition 7.1 is needed for anything the Lean
does not prove — it is not, since the Lean reaches `no_measurable_weak_five_coloring` — and whether the paper's
exposition can therefore drop 7.6–7.8 in favour of the dichotomy. That is a paper-level editing question, [P],
and I have not attempted it.
