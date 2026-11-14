# Block `K15-REVIEW-0308-M-CONTINUE` — the four-task continuation

Answers the four-item queue in `Main/TASKS.md` / the block receipt
`K15-REVIEW-0308-M-CONTINUE`. Every item is reported with what was *proved*, what was only
*checked*, and what failed. Nothing here is a new density bound; the target of the project
is unchanged.

## One-paragraph summary

The block produced **two new theorems** and **three corrections**. The theorems are
`K15-C094` (every Voronoi cell of every Barlow packing has volume `√32` — closing the
uniformity that `K15-C091` had only as numerical evidence) and `K15-C095` (the "crack
packing": a saturated 2-separated packing with two infinite closed components, which is
also a second equality case of Kepler's bound and is **not** Barlow). The corrections are
`C088` (softened: no compact reduction *for the cut formulation as stated*, not "none
exists"), `C089` (the closed-component obstruction needs **bounded** `C`), and the bridge
audit (`BRIDGE_AUDIT.md` §6: the `12/S` loss cancels in the limit, so the bridge is exact
for its purpose — contrary to what `C083` implied). Task 3 is therefore finished; task 1 is
finished for singletons (reduced to the explicit inequality `V(2.09) ≥ √32`, with a `12%`
margin under a stated conjecture, `K15-C096`) and still open for `|C| ≥ 2`; task 4 is done.

---

## Task 1 — the closed-component question

**Asked:** can a saturated 2-separated packing in `R³` have a closed component of the
`2.09`-graph with positive signed deficit `Σ_C b > 0`?

**Carried in:** `Main/CLOSED_COMPONENT.md`, `K15-C092` — the covering lemma (an isolated
vertex of a saturated packing has `≥ 5` centres in `(2.09, 4]`) and four documented failed
constructions `A1`–`A4`.

**New this block.** Three things, all of them corrections or reductions rather than a
resolution.

1. **"Closed" must mean "bounded"** (`K15-C095`, `Main/GAP_FIXTURE.md`). The crack packing
   — two fcc half-spaces cut at `z = 0`, the upper one raised by `d` and shifted sideways
   by `T` — is a saturated 2-separated packing for `H ≤ d ≤ 2H`, and for `d > 1.633` its
   minimum cross-crack distance is `> 2.09`, so its `2.09`-graph has **two closed infinite
   components**. So closed components are not exotic. They are also harmless, because every
   *finite* `U ⊆ C` has out-edges into `C∖U`. `K15-C089`'s "a closed component gives
   `t* = ∞`" is therefore correct only for bounded `C`, and is amended.
2. **Voids are never the counterexample** (same entries). In the crack packing at `d = 2.4`
   every crack-face cell has `vol Ω = 6.985349063`, i.e. `b = −1.328495`, and every bulk
   cell has `vol Ω = √32` exactly. Cells next to a hole are *larger*, so `b < 0` and the
   cut condition holds for free. Only compression can produce `b > 0`. This closes off a
   natural but wrong search direction (vacancies, gaps, surfaces, amorphous layers).
3. **The singleton case is reduced to one explicit inequality** (`K15-C096`). `C = {v₀}`
   closed with `Σ_C b > 0` is exactly: every other centre is at distance `≥ 2.09` from
   `v₀`, **and** `vol Ω(v₀) < √32`. Define

   ```
   V(ρ) = min{ vol Ω(0) : C 2-separated, every |c| ≥ ρ },     V(2) = V_dod (Hales–McLaughlin)
   ```

   Then the singleton case is closed iff `V(2.09) ≥ √32`. The relevant numbers:

   | quantity | value |
   | --- | --- |
   | `V_dod` | `5.550291028515510` |
   | `ρ* = 2(√32/V_dod)^{1/3}` — where the scaled dodecahedral cell reaches `√32` | **`2.012718662…`** |
   | `V_dod(1.045)³` — the icosahedral twelve at `ρ = 2.09` | `6.333804106` = **`1.1197·√32`** |

   So under the natural conjecture `(S)` — `V(ρ) = V_dod(ρ/2)³` on `[2, ρ_c]`, which is
   exactly the stability version of Hales–McLaughlin that `A2` asked for — the cheapest
   isolated-vertex configuration clears `√32` by **12%**, and the sharp threshold is only
   `0.64%` above 2 (versus a graph radius `4.5%` above 2). A probe over the 20 icosahedral
   holes at `ρ = 2.0127, 2.09, 2.2`, an extra point at every radius in `[ρ,4]`, finds **no
   admissible extra point that cuts the cell at all**.

**Status.** Singleton: reduced, open, not marginal. `|C| ≥ 2`: untouched, open, no
construction and no obstruction — a member of `C` has neighbours *inside* `C` at distance
2, so `(S)` does not apply to it. **No claim that the question is settled.**

## Task 2 — the finite-to-infinite cut/flow theorem

**Delivered:** `Main/CUT_FLOW_THEOREM.md` + `K15-C093`, committed as `e70dd10` and pushed
to `kepler15/main` (verified against the remote, which had been left at the parent
`a3638a9`; the interrupted step's push had not landed).

Content: Theorem 1 (finite graph, demands on `F ⊆ V` only, transfer exists **iff**
`Σ_U b ≤ cap(U)` for all `U ⊆ F`) — the *free boundary* is what makes the reduction to
Gale–Hoffman go through; Theorem 2 (locally finite infinite graph, exhaustion, bounded
capacities) by Tychonoff on `∏_e[−Φ₀,Φ₀]` and the finite intersection property, with the
refinement that **compactness alone needs no degree bound** — local finiteness is needed
only for `div` to be a finite sum (correcting `K15-C067`, which conflated the two). Worked
signed examples: the dumbbell `b = (1,−⅓,−⅓,−⅓)` with `t* = ⅓` and a tight singleton cut
as the dual witness; the same graph at `b(a) = 4` infeasible at `Φ = 1` with the violating
cut `{a}`; and a two-hop path `(+1,0,0,−1)` with `t* = 1`, a unique flow, and three tight
prefix cuts.

Nothing in task 2 needed repair this block.

## Task 3 — Barlow cell volumes (finished)

**Delivered:** `Main/BARLOW_CELLS.md` + `K15-C094`. `K15-C091` had the average `√32` proved
and the uniformity only as numerical evidence over six stackings. The uniformity is now
proved, and the earlier framing of the problem was wrong in an instructive way.

**The theorem.** *Every Voronoi cell of every Barlow packing has volume `4√2 = √32`.*

**The proof** (four steps, no interval arithmetic):

1. **Distances.** Exactly twelve centres at distance 2 — six in-layer, three in each
   adjacent layer, the latter because `T = (a₁+a₂)/3` is the centroid of the equilateral
   triangle `{0,a₁,a₂}`, so `|T| = 2/√3` and `|T|² + H² = 4` — and every other centre at
   distance `≥ 2√2` (next in-plane distance in an adjacent layer is `4/√3`, giving
   `√(16/3 + 8/3)`).
2. **The cell is the contact cell.** Every point of space is within `√2` of a centre: a
   layer plane is within `H/2` of any point, the triangular lattice has covering radius
   `2/√3`, and `(2/√3)² + (H/2)² = 2`. So `Ω(v) ⊆ B(v,√2)`; a non-contact `c` has
   `|c−v| ≥ 2√2`, so its half-space contains `B(v,√2) ⊇ Ω(v)` and is redundant.
3. **Exactly two shapes.** The six in-layer contacts are a regular hexagon. The three upper
   contacts lie in the coset `δ₊T + Λ` and the three lower in `−δ₋T + Λ`; the two non-zero
   cosets of `Λ` in `(1/3)Λ` give azimuth classes `𝒜 = {30°,150°,270°}` and
   `ℬ = 𝒜+60°`. So the contact set is determined by `δ₊ = δ₋` (**fcc** configuration) or
   `δ₊ = −δ₋` (**hcp** configuration); a `60°` rotation and `z ↦ −z` collapse the four sign
   combinations to these two.
4. **Both volumes are `√32`.** The average cell volume is `2√3·H = 4√2` in *every* Barlow
   packing. `ABC…` is fcc-configured in every layer, so `A_fcc = 4√2`; `ABA…` is
   hcp-configured in every layer, so `A_hcp = 4√2`. Every cell is one of the two. ∎

**What the numerics test** (`Computation/barlow_cells.py`, `--sweep 6`): 9 named stackings
plus `48` random legal stackings of period 3–10, `346` layer analyses, **0 violations**,
exit 0. Per layer: `#`centres at distance 2 `= 12`; next distance `2√2`; volume from the
12 contacts **equals** volume from all centres within radius 5 (to `1e−12`); circumradius
`√2`; 12 quadrilateral faces, 14 vertices; and the non-contact half-space slack is `0` to
`1e−16`, i.e. the far half-spaces are **tangent** — the equality case in step 2, which is
the thing a naive reading gets wrong. The fcc and hcp cells have **different** face-normal
dot-product fingerprints (`−½` only versus `−5/6, −1/3` as well), so they are *not
congruent*: the result is a volume statement about a two-element family, not a shape
statement about one polyhedron. **"Every Barlow cell is a rhombic dodecahedron" is false**,
which is worth knowing because that was the natural guess.

**The consequence that costs something.** `b ≡ 0` on every Barlow packing, so every cut is
*tight* (`Σ_U b = 0 = Φ|δ⁺_R(U)|` with `Φ = 0`): the cut condition has **zero margin** at
the extremal configurations. Any proof strategy of the form "produce a positive margin on a
compact class, then use `C087` for large cuts" therefore fails exactly where it matters.
This is the transfer-route analogue of Hales' §17.2 remark that pure subdivision fails at a
tight point, and it is recorded as a **cost**, not a gain.

## Task 4 — the bridge audit, the implication audit, and the complexity comparisons

Four deliverables.

1. **`K15-C002b` audited line by line against Cohn–Elkies Appendix A**
   (`BRIDGE_AUDIT.md` §5, new). Five CE moves mapped to `C002b`'s four items; two of CE's
   moves (translation-invariance of the density limit, passage to a compact set) are simply
   *not used*, and `C002b` replaces Groemer's "uniformly dense extremal packing" with a
   maximal-tile counting argument plus an explicit `O(R²S)` boundary count. Two defects
   recorded: the **counting-to-volume step is implicit** (a reader of `C002b` alone cannot
   see it), and the ledger's own **status token said `PROPOSED`** while `RESULTS.md`,
   `ACCEPTED.md` and `C037` treated it as audited. Token corrected to `AUDITED` (Main,
   `C037`) with the outside check still outstanding as `G1`.
2. **The bridge's exact logical form — the `12/S` cancels** (`BRIDGE_AUDIT.md` §6, new).
   `(P)`: the bound holds for periodic packings. `(B)`: for every `Λ` and `S ≥ 10` there is
   periodic `Π_S` with `δ(Π_S) ≥ δ(Λ)(1−12/S)`. Then
   `δ(Λ) ≤ δ(Π_S)/(1−12/S) ≤ bound·(1+O(1/S))` for every `S`, and the left side does not
   depend on `S`, so `S → ∞` gives `(G)`: the bound for **every** packing, with no `12/S` in
   the conclusion. `K15-C083`'s "the bridge says nothing quantitative at any computable
   scale" is true only of a different ambition (a finite-`S` error term) and is false as a
   statement about `(G)`. Also noted: no uniformity in `Λ` is needed, `S` being chosen after
   `Λ`.
3. **`C087`'s implication is one-directional, and its error term needs saturation**
   (ledger amendment). `C087` proves *cut condition ⟹ `δ ≤ π/√18`*; the converse is not
   available, so the cut condition is **at least as strong as** Kepler — the opposite of a
   shortcut. Two unstated hypotheses in the `O(r²)` term: (i) `Σ_U vol Ω = vol B(x,r) +
   O(r²)` needs `Ω(v) ⊆ B(v,2)`, which is a **saturation** property (and fails for
   unsaturated packings, whose cells can be unbounded — the crack packings show this
   directly); (ii) `|U| = c(Λ)(4π/3)r³ + O(r²)` uses the **centre** density, with
   `√32c − 1 = 0` at `c = 1/√32`. Neither affects the conclusion.
4. **`ACCEPTED.md` extended, and a one-way-implications table added.** Five arrows listed
   with their converses: `(T')`⟹cut (one-way), cut⟹Kepler (one-way), `b ≡ 0` on Barlow
   (one-way), 12-contacts⟹layered (**not verified here**), transfer⟺cut (**both ways** —
   the only genuine equivalence, and it is pure graph theory). Writing them down together
   was worth it: three of the five have already been read as equivalences somewhere in this
   ledger.

**`C088` softened** as requested: it now says no compact reduction is available *for the
cut formulation as stated*, and explicitly withdraws "none exists" — nothing rules out a
`DS`-analogue for the cut form, and Hales' own `DS` was introduced *after* his accounting.

---

## Corrections made this block

| # | Where | Was | Now |
| --- | --- | --- | --- |
| 1 | `C088` | "no compact reduction is available" | "none available **for the cut formulation as stated**"; the stronger claim is withdrawn |
| 2 | `C089`, `CLOSED_COMPONENT.md` | a closed component gives `t* = ∞` | only a **bounded** closed component does; infinite ones exist (`C095`) and are harmless |
| 3 | `C091` | `TESTED_FINITE`, uniformity open | `PROVED` via `C094`; the finite evidence is retained as evidence |
| 4 | `C002b` status token | `PROPOSED` | `AUDITED` (Main, `C037`); outside check outstanding (`G1`) |
| 5 | `C083` | "the bridge says nothing quantitative at any computable scale" | the `12/S` **cancels**; `(G)` is exact (`BRIDGE_AUDIT.md` §6) |
| 6 | `C087` | `O(r²)` term presented as free | needs saturation (`Ω(v) ⊆ B(v,2)`) and the centre-density substitution; both now stated |
| 7 | step 3's framing | "is every Barlow cell a rhombic dodecahedron?" | **false**; there are two shapes, both of volume `√32` |

## Concrete next package

Ordered by value per unit work. Each item names its artifact and its acceptance test, so
"done" cannot be claimed without one.

**PN-1 — decide `V(2.09) ≥ √32` (`K15-C096`).** The sharpest open item in the project, and
the only one whose *refutation* would be decisive. Prove `(S)`: `V(ρ) = V_dod(ρ/2)³` on
`[2, ρ_c]`, or any `V(ρ) ≥ V_dod(1 + 0.2133(ρ−2))` on `[2, 2.09]`.
*Acceptance:* either a proof of `(S)` on `[2,2.09]`, or a certified enclosure
`V(2.09) ≥ √32` from interval arithmetic over configurations. **A refutation is an explicit
2-separated configuration with every `|c| ≥ 2.09` and `vol Ω(0) < √32` — that is a
counterexample to the transfer route and must be reported immediately, with the minimum
separation checked over all pairs including core–background.** Highest value item; hand to
Astra with the `rho_probe.py` output as the starting point.

**PN-2 — the `|C| ≥ 2` closed-component case.** No reduction is known. Search for a bounded
closed component with `Σ_C b > 0`, using the two facts that make the search cheap: `b > 0`
requires compression (never voids, `C095`), and `Ω(v)` is determined by centres within 4.
*Acceptance:* either a validated construction (min separation `≥ 2` over all pairs, every
cell volume, `δ⁺_{2.09}(C) = ∅` verified) or an obstruction list in the style of A1–A4.
Owner: E. **Do not** report "no example found" as progress.

**PN-3 — checker soundness, still suspended.** Three repairs (`C049`, `C058`, `C068`) each
found by outside reproduction. What X is asked to audit is a *soundness argument*, not a
battery. Main's side owes the written argument: (i) the isolating-interval refinement
terminates; (ii) "one test point per constant-sign gap" is complete for the roots of the
polynomial itself; (iii) the `function_range` fallback is sound where the gap rule returns
inconclusive; (iv) no decision path inspects only the odd part or samples between touching
intervals. *Acceptance:* a written proof that the accepted set `{p : check(p) = true}` is
contained in `{p : p ≤ 0 on the region}`. Until then, generic checker soundness stays
suspended and only the certificate path (no roots on sign regions) is relied on.

**PN-4 — `sup_Λ t*(Λ) ≤ Φ₀` for ball cuts only.** `PACKAGE_CUT.md` step 1, with the
explicit boundary `3k_RRr²`. Two facts sharpen it: `Φ = 0` is **attained** by a non-Barlow
class (`C095`'s crack packings) and is **false** in general (`C069`), so the ball-cut case
must be proved for every `Φ > 0` and no slack argument can work (`C094`). Step 0 is PN-1.

**PN-5 — the strategic question, stated plainly, for the person to decide.** `C087` says
the cut condition implies Kepler and is not implied by it, so the geometric route is a
*reorganisation*, not a simplification: its price is that the geometric content reappears at
full strength, and its dividend (negligibility for free, `C035`) is something Hales also
gets cheaply (Thm 7.11, no computation). `C095` adds that the equality case of Kepler's
bound is far larger than the Barlow packings (any planar fault is an equality case), so no
sharp certificate can rest on a unique extremiser. If the goal is strictly "a simpler proof
of `δ ≤ π/√18`", the honest summary is: **no shortcut is known in this project, and the two
routes explored here are each at least as strong as the theorem they would prove.**

## What was not done

- **No new density bound.** No number in `RESULTS.md` moves.
- **The closed-component question is not settled** for any `|C| ≥ 1`: reduced for `|C| = 1`,
  open for `|C| ≥ 2`.
- **No Lean.** `M-LEAN-002` closed `FAILED on resources` (broad `import Mathlib` hit 60 s /
  715 MB); `M-LEAN-003` (narrow-import `CubeDiff.lean`) is untouched this block.
- **No worker-branch merge.** Integration stays by reference; `C-CUT-001` was not run here
  (it belongs to C) and no `t*` was computed for any new packing.
- **`C096`'s conjecture `(S)` is not proved**, and the `13`-point search is not exhaustive —
  it probes the natural positions only.
