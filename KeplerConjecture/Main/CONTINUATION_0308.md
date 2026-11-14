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

---

# Review `K15-REVIEW-0353-M-EVIDENCE` — repairs and integration

Received after the block's first push (`b42c8d1`). All four objections to `K15-C093` are
**confirmed against the text**; the three worker revisions are integrated by hash; one
further defect was found by Main while integrating them. **No new best packing bound is
established** by any of this, and `RESULTS.md` does not move.

## R1 — the cut/flow theorem: four defects, all real (`D18`)

`CUT_FLOW_THEOREM.md` is rewritten; the rejected wording is retained there in §6 and in the
ledger under `C093`, per the standing convention.

| # | Defect | Repair |
| --- | --- | --- |
| 1 | cut orientation **reversed**: the text said the infinite arcs make `X ⊇ N(U)∖F` optimal for `X = S∖F` | finite-capacity cuts have `X = ∅` — an outside vertex on the source side puts its infinite arc `w→t` across the cut, so outside vertices are forced onto the **sink** side and there is no minimisation. Conclusion `Σ_U b ≤ cap(U)` unchanged. **Both directed arcs now written out** (`v→w` and `w→v`, each with the full capacity) and the transfer is their net `ψ(v,w) = f(v→w) − f(w→v)`, so `|ψ| ≤ Φ_{vw}`; conversely every transfer arises this way |
| 2 | threshold formula divided by a **zero boundary**, and the example was wrong | `t* = +∞` if some `U ⊆ F` has `δ⁺(U) = ∅` and `Σ_U b > 0`; otherwise `max(0, sup_{δ⁺(U)≠∅} Σ_U b/|δ⁺(U)|)`. Hence `b = (4,−1,−1,−1)` is infeasible at **every** `Φ` (`Σ_F b = 1 > 0 = cap(F)`), not at a threshold `4/3`; the genuine threshold example is `b = (4,−4/3,−4/3,−4/3)` with `t* = 4/3`. `Φ ≥ 0` is now a stated hypothesis and the `max(0,·)` branch is what makes `Φ = 0` available when every cut has `Σ_U b < 0` |
| 3 | compactness assumed a **uniform bound** | `∏_e [−Φ_e, Φ_e]` is compact by Tychonoff from the compactness of each factor; `sup_e Φ_e < ∞` is **removed** as a hypothesis. A table now names where each remaining hypothesis is used: `Φ_e ≥ 0` (non-degenerate interval), `Φ_e < ∞` (compact factor), local finiteness (**only** so that `div` is a finite sum, hence continuous), `F_n` finite with `⋃F_n = V` |
| 4 | the density implication read as settling the strength | §4: `(C) ⟹ Kepler` (`C087`), no converse, **no equivalence**; `(C)` is at least as strong as Kepler |

**A second, independent proof of (⟸) was added** rather than only patching the first:
Farkas for `{Aφ ≥ b, |φ_e| ≤ Φ_e}` *keeping the box multipliers* gives the alternative
`∃y ≥ 0 : Σ_F y_v b(v) > Σ_e Φ_e|y_v − y_w|`, and the coarea identities
`Σ_F y_v b = ∫_0^∞ Σ_{U_t} b`, `Σ_e Φ_e|y_v − y_w| = ∫_0^∞ cap(U_t)` with
`U_t = {v : y_v > t}` then produce a cut violating `(C)`. This is the proof that survives
signed capacities, and it is what established that the cut condition is *exactly*
equivalent (not merely sufficient). The audit request for X is `AUDIT_REQUEST_X.md` item 5,
with a specific "try to break it" target: an instance where the two proofs disagree.

## R2 — the shell allowance's missing precondition (`K15-C098`)

Confirmed: `check(a, rho, eta, …)` accepted any `eta`. The count-price bound is licensed
only for `η ≥ 0`; for `η < 0` the correct statement replaces `η` by `max(η,0) = 0`, because
`f ≤ 0` off the shell already supplies the stronger hypothesis. So an `η < 0` call returned
a **smaller** number than the argument licenses for the parameter the caller believes it
passed. `check` now rejects `η < 0` with an explicit message and
`checker_adversarial.py` gains two cases (suite now 37 cases). **This is a precondition
validation, not a soundness argument**: generic checker soundness stays **SUSPENDED**
(`PN-4`), exactly as X asks.

## R3 — three worker revisions integrated by hash (`K15-C097`)

**(a) C `4bcbd3a` — `C-DECOUPLE-001`.** For the icosahedral fixture the periodic graph is a
disjoint union of identical copies (centres within 2 of their copy origin, so copies are
`≥ 16 − 4 = 12` apart while `R ≤ 3`), so a finite `U` splits with **no cross edges** and the
ratio's maximum is attained inside one copy: `t* = 0.008880268414417` is exact for the
infinite packing, not a patch proxy. Accepted, with C's own caveat (dense packings have
period comparable to `R`). **Main adds two limits:** the fixture is **unsaturated**, so this
is a statement about an unsaturated periodic packing and **not** a floor for saturated ones;
that floor is independently valid from `K15-C081r` (Zorn extension to a saturated packing,
adding centres only shrinks `Ω(v₀)`, `deg(v₀) = 12` by `K15-C054`), giving the same number
`0.1065632/12 = 0.00888027…`.

**(b) E `82689ba` — the trend claim corrected.** The 30-centre search gives `6.494845` and
`6.968035`, *worse* than the 18-centre `6.263608`, so the sequence is not monotone and the
"margin halving at each step" framing is withdrawn by E itself. `(P′)` has survived every
legal test, best `6.263608` against a required `5.763417`; the evidence is **one-sided, so
not support**. Recorded `PROPOSED`, unproved — and Main states why plainly: **numerical
upper volumes cannot validate it**, since an upper bound on a computed volume is not a lower
bound on the true infimum and no interval arithmetic was used.

**(c) X `118ecd1` — `K15-X-C017`.** Both sides explicit: rational symmetric `6×6` `G,A,B`,
`m = 5`, `S = 8`; all PSD by exact rational LDL; `Q(A,B)` equals the Fourier image of `P`
exactly; `P(0)/Q(0) = 1.039899410072` hence `Δ ≤ 0.782267220134`; `Q ≥ 0` cross-checked by
exact Sturm. X also corrects its own earlier assumption that `G` had to be singular (`P =
−(s−4)H` gives `P(4) = 0` for any `H`). **`0.782267220134` is worse than the project's best
`0.779966216777`, so it is not an improvement.** Its value is methodological and it is
significant: **no sign predicate, no root isolation and no Sturm is needed anywhere — every
sign condition is a rational PSD test.** Given three unsound revisions of `shell_check.py`,
that is the trust profile the project should prefer, and it motivates

**`K15-C099` (proposal, needs the person's sign-off):** make "both sides, all sign
conditions rational PSD" the *acceptance* criterion for certificates, and mark any
certificate needing `shell_check` as `PENDING` until the soundness argument of `PN-4`
exists. It costs nothing numerically (no candidate is competitive with published values)
and it removes the project's most-repeated failure. Reverse if `PN-4` lands and X accepts it.

## R4 — the 13-cluster: X's flag confirmed, with the exact numbers

X flagged that C's sparse periodic 13-cluster is unsaturated and that `build_13(2.1029)` adds
ring edges below the true separation. **Both confirmed**, and Main found the closed form is
also mis-stated:

- the exact ring (outer-icosahedron edge) at circumradius 2 is
  `4/√(1+φ²) = 4√2/√(5+√5) = 2√(2 − 2/√5) = 2.102924448476534…`;
- C's comment gives `2√(1 − 1/√5) = 2.1029`, which evaluates to `1.48699` — **it is missing
  a factor `√2`**; and the decimal `2.1029` is short by `2.4448e−5`;
- `build_13` gates on `distance_R >= 2.1029 − 1e−9`, so at the scanned row `R = 2.1029` the
  graph gains 30 ring edges whose actual separation `2.102924448…` **exceeds** `R`.

*Consequences, stated at their true size.* The affected row is mislabelled — its reported
`t*` is the value at `R ≥ 2.1029244`, not at `R = 2.1029` — and the qualitative conclusion
(the singleton cut binds, threshold unchanged) is unaffected because it is driven by the
singleton. But **no finite scan from that fixture is promoted here**, the fixture is not used
as a saturated witness anywhere in `Main/`, and exact geometric validation
(`validate_icos_fixture` extended to the ring-edge threshold, with the closed form above)
is requested before any of its rows is quoted.

## R5 — Barlow work continues after the repairs

The Barlow programme was not blocked by any of the above and is unaffected: `K15-C094`
(every Barlow cell `√32`, proof + 346 layer analyses), `K15-C095` (the crack packing:
infinite closed components, `b = −1.3285` at the faces, a second equality case of Kepler's
bound), `K15-C096` (singleton closed components reduced to `V(2.09) ≥ √32`, sharp threshold
`ρ* = 2.012718662`, margin `12%` under conjecture `(S)`). The repair discipline of `D18`
was applied to them as well: `C094`'s step 2 has an equality/tangency case that the
numerics check explicitly (`slack = 0` to `1e−16`, not `< 0`), and `C095`'s two analytic
bounds (`H ≤ d ≤ 2H`) are stated as inequalities rather than as sampled values.

**Still not established: any new bound on the density of a packing in `R³`.** The record
bound to beat analytically remains Hales–McLaughlin's `0.754697399337`.

---

# R6 — Barlow / complexity work continued after the repairs (`K15-C100`–`C102`)

Three further results, all obtained after the review's repairs and none of them requiring any
tool the review put in doubt.

**`K15-C100` — the cost scorecard** (`Main/COMPLEXITY.md`). The two numbers that decide the
project's goal: the **lattice-restricted** three-point bound is `0.741506` against the truth
`0.740480489693` — a gap of `+0.00103`, i.e. **`0.14%`** — while the **general** three-point
bound is `0.770271`, a gap of `4.0%`. So the lattice restriction is worth `0.029` of density,
and every non-computational object within `0.14%` of the truth is three-point-and-lattice.
Since the plain two-point LP is *proved* not sharp in `d = 3` (Li 2024, Thm 6.1) and
`K15-C095` exhibits the mechanism concretely (any planar fault is an equality case, so a
sharp certificate needs `f` to vanish on a continuum of shell radii), the analytic route
cannot be a shortcut below level 3; and the transfer route is at least as strong as the
theorem (`C087`) with no slack at the extremal family (`C094`). **The one well-posed
improvement target with this project's tools is a pointwise cell inequality strictly better
than `0.754697399337`.**

**`K15-C101` — `(S)` splits at the Tammes-13 threshold.** `2.09` is the Tammes-13 threshold
rounded down: 13 points on a sphere of radius `ρ` with mutual `≥ 2` exist iff
`ρ ≥ 2.091145548`, and at `ρ = 2.09` the required separation is `57.1709° > θ₁₃ = 57.1367°`,
so at radius exactly `2.09` **every admissible configuration has at most 12 points**. That
splits `V(2.09) ≥ √32` into case **(A)** (all at radius `ρ`: scaling maps it to the `ρ = 2`
problem, giving the icosahedral `V_dod(ρ/2)³ = 6.333804106 = 1.1197·√32`, settled at `12%`
margin modulo Tammes-12 and spread monotonicity) and case **(B)** (`some` point farther out:
exactly "mixed radii do not help", the open case). Also: the trivial inball bound
`4π/3(ρ/2)³ = 4.78011` beats `V_dod` only for `ρ > 2.1967`, so `(S)` must be a stability
statement and cannot be replaced by a ball estimate.

**`K15-C102` — no extra centre ever cuts the icosahedral cell.** Redundancy is per
half-space, so case (B) at a fixed base is decided by the single-point question, and that
question has a closed form (`r₊ = ⟨u,x⟩ + √(⟨u,x⟩² − (ρ²−4))`). Over `2×10⁶` directions plus
refinement from all 24 icosahedral/dodecahedral directions, the nearest admissible extra
centre is at

```
|p| = 3.206870905…   (edge-midpoint direction)   vs   2·R_cell = 2.955706345,
```

a margin of `8.5%`. Hence `V(2.09) ≤ V_dod(1.045)³ = 6.333804106` **with equality** at the
icosahedral configuration, and — the part that matters for the ledger —
`CLOSED_COMPONENT.md`'s **A1 is upgraded**: `6.333804` is the *true* cell volume of the
pushed-out icosahedral vertex, so its deficit `b = −0.677` is true, not an estimate. The
natural singleton candidate fails by `12%` as a matter of fact rather than under an
assumption.

**A by-product worth having** (`BARLOW_CELLS.md`, Lemma 3): the exact truncation criterion
`|p−v| ≥ 2h_Ω(p−v)` (support function), which makes every "centres within `2R_cell`" claim in
the project rigorous, and which explains a number the numerics produced: for a Barlow packing
`R_cell = √2`, so the truncation radius is `2√2` — **exactly the next distance** — which is
why the far-centre slack is `0` to `1e−16` (tangency) and not negative. Step 2 of `C094`
therefore cannot be sharpened to a strict inequality.

**Status unchanged: no new bound on the density of a packing in `R³`.**

---

# R7 — review 0438 integration (what in this document is now superseded)

This document was written for block `0308`. Two later blocks changed its content, and this
section is the pointer so a reader does not work from a superseded page. Nothing above is
deleted: the earlier text is the record of what was believed then.

**1. Task 3's theorem was proved on a flawed lemma, and is now proved on a repaired one.**
§"Task 3" rests on `BARLOW_CELLS.md` Lemma 1, which was **circular** — E's `K15-E083` found it
and `K15-C104` repairs it: redundancy of a non-contact half-space needs `K ⊆ H_c` for the
*contact-only* polytope, not `Ω ⊆ H_c`. The theorem (`C094`) is unchanged and its acceptance is
restored on the repaired proof, whose load-bearing step is an exact two-polytope computation that
Main re-derived independently (`Computation/contact_cell_exact.py`). Consequences of the repair:
`(F3)` is no longer used by the theorem, and the chain is shorter.

**2. `GAP_FIXTURE`'s saturation range was overstated.** "For `d > 1.633` … saturated" needs the
upper bound `d ≤ 2H = 3.266`; corrected in `GAP_FIXTURE.md` (E caught it).

**3. The block's rhetoric about the cut route was wrong, and is withdrawn.** `C105`: a
**sufficient** criterion is not circular because it implies the target. `C087`'s one-way arrow
forbids only the reading "the cut form is a weaker target than Kepler"; it does not disqualify
the route. The phrase "a reorganisation, not a simplification" is withdrawn from `ACCEPTED.md`,
`C087` and `COMPLEXITY.md`.

**4. The chosen geometric target has changed (`D19`).** This document's Task 2 and the
`PACKAGE_CUT`/`NEXT_PACKAGE` material target the **cut condition**. That route is not wrong, but
`D19` records that it is no longer the live one, for two reasons established at `0438`:

- the *pointwise* cell route is **closed by sharpness** — `vol Ω ≥ V_dod` is attained, and the
  retained literature records that the whole per-point family is capped at `8/V_dod`
  (`Literature/sharp-bounds-in-dimension-3.md` §5.3(i)), so beating it *requires* a multi-cell
  inequality;
- the **pair route** is that inequality: `vol Ω(v) + vol Ω(w) ≥ 2√32` (`GEOMETRIC_LEMMA_0438.md`,
  `C106`–`C108`), with a bridge to the density bound and a proof of its qualitative form.

So a reader looking for the current target should read `GEOMETRIC_LEMMA_0438.md` and
`REVIEW_0438.md` §5 (package `PN-C`/`PN-E`/`PN-X`), not `NEXT_PACKAGE.md`, which remains as the
statement of the cut route's inequality.

**5. Task 4's audit was revised.** `C088`'s "no compact reduction exists" is now scoped to "none
available *for the cut formulation as stated*"; and `C002b`'s status token (`PROPOSED`) was
inconsistent with three files treating it as audited — now `AUDITED` with `G1` outstanding.

**Still true from this document:** the four-task results, the covering lemma (`C092`), the
cut/flow theorems (`C093`, repaired at `D18`), and the six-stacking table (`C091`, upgraded to
`PROVED` by `C094`).
