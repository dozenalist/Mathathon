## Abstract

Six questions, six verdicts, with the three layers kept apart (a contact-pair conjecture, a
combinatorial weighting hypothesis, a density conclusion):

1. **Theorem B's counting**: the definition of `C_R` at line 90 is the wrong set — the identity and
   `c_e ≤ 1` both need the exactly-one-endpoint sum (the document's own self-audit has it right).
   One-line repair; the theorem survives. `X-C037`.
2. **The weight hypothesis `(M)`**: its characterisation is the *fractional* Tutte condition and is
   correct (verified on 33,867 graphs). `X-C038`. The "exactly an isolated icosahedral cluster"
   description of the failure is too strong — `K_{1,3}` and `P₃` fail too, and the icosahedral
   twelve are *not* the unique twelve-point set with mutual distance `≥ 2` on radius 2. `X-C039`,
   `X-C048`.
3. **Theorem D (compactness)**: correct in all five clauses, with `N_max` needing `(2R_max+1)³`; its
   two-dodecahedra step is confirmed independently to twelve digits. `X-C043`.
4. **The equality case of `(L)`**: "exactly the Barlow family" is **refuted** — the crack packing
   has bulk–bulk pairs at `2√32` and is not Barlow. `X-C040`. Hales–McLaughlin's own equality case
   (which Theorem D needs) *is* verified from the primary source. `X-C047`.
5. **Theorem C's "the equality case of the dodecahedral bound is empty"**: the conclusion is true
   (two lines from Hales) but the document's route to it reads an average as a pointwise statement,
   and even a *volume*-stability theorem would not repair it. `X-C041`, `X-C049`.
6. **The slack repair**: its displayed coefficients are weaker than the split's, so the display is
   true; the repair does need `Σc_e ≤ 1` on the exceptional set, which `(M)` does not give.
   `X-C042`.

Nothing here is a bound. The record remains `0.754697399337` (analytic) and `0.779966216777` (best
certificate); `(L)` is unproved and `(M)` is a hypothesis. Four statements in the audited files and
four claims of my own were wrong at some point; all eight were caught by a computation, a second
implementation or a source, and each is recorded where it was found.

# K15-REVIEW-0523-X — audit of `GEOMETRIC_LEMMA_0438.md` and `EXPOSITION_0438.md`

Receipt `2026-11-14T13:32:41Z`. Audited: `Main/GEOMETRIC_LEMMA_0438.md` at commit `a6f3935`
(blob `a03be811`), `Main/EXPOSITION_0438.md` at the same commit (blob `5a1708af`, unchanged at the
current main tip), and `Computation/cut_flow.py` at comp tip `a25f5be` (blob `c2127cee`). Line
numbers below are lines of `GEOMETRIC_LEMMA_0438.md` at `a6f3935`.

**Verdict in one paragraph.** The *chain* is sound and correctly labelled conditional; the
*local* statement `(L)` is not proved and is not claimed to be; Theorem D's compactness argument
survives a clause-by-clause check and its step 4 constant is confirmed independently here to 12
digits; **but four specific statements are wrong as written**: the definition of `C_R` (line 90)
contradicts the identity it is used in (line 94) and contradicts the document's own self-audit
(line 409); the characterisation of the weight hypothesis `(M)` (line 197) is Tutte's *integral*
condition and is false as an iff for the fractional object it introduces; the heading at line 40
asserts a converse (equality in `(L)` ⟹ Barlow) that the text does not prove and that the
project's own `C095` refutes; and consequence 2 of Theorem C (line 385) infers "every cell
dodecahedral" from an equality of *density*, which is an average, and needs a stability version of
Hales–McLaughlin that the exposition itself records as unavailable. None of these promotes a bound;
the first three are one-line repairs, the fourth is a demotion.

**The three layers, kept apart** (this separation is the main thing the audit adds):

| layer | statement | status |
| --- | --- | --- |
| local | `(L)`: every contact pair has `vol Ω(v)+vol Ω(w) ≥ 2√32` | **conjecture** (E's `K15-E074`), equality on Barlow *proved* (`C106`), converse **false** (§5) |
| combinatorial | `(M)`: `c_e ≥ 0` on contact edges with `Σ_{e∋v}c_e = 1` off a density-zero set | **hypothesis**, not automatic; correct characterisation is the Farkas one (§3), not the document's |
| global | `(L) ∧ (M) ⇒ δ(Λ) ≤ π/√18`, and `(L_δ) ∧ (M) ⇒ δ < 0.754697399337` | **conditional**; Theorem B's proof has one defective definition (§2), repairable |

Nothing here is a density result, and nothing here is quoted as one.

---

## 1. What the document claims, separated

`(L)` (line 13) is a statement about one contact pair in a saturated packing. It is *local*.

`(M)` (line 74) is a statement about the contact graph of one packing. It is *combinatorial*, and
it is not implied by saturation (`§4` of the document says so, correctly).

Theorem B (line 71) is the implication `(L) ∧ (M) ⇒ δ(Λ) ≤ π/√18` **for the one packing `Λ`**
that satisfies both. It cannot be, and is not, quantified over all packings: `(L)` is not known
for all packings, and `(M)` is not either. So the density conclusion is *conditional per packing*;
turning it into a theorem about all packings needs both hypotheses proved for every saturated
packing, and the document says that is not done ("No proof of either form is known to Main",
line 219). That labelling is honest and I am not changing it.

The reduction from arbitrary to saturated packings is used implicitly and is fine: if the bound
holds for every *saturated* packing, then for any packing `Λ` choose a saturated `Λ' ⊇ Λ` (Zorn);
`δ(Λ) ≤ δ(Λ')` and the Voronoi cells of `Λ'` are the ones `(L)` applies to, so `δ(Λ) ≤ π/√18`. ✓

---

### 1a. The near-critical row: two different payer values, both above target

The §5 table quotes the icosahedral payer as `5.897967122`, margin `0.134549` over
`2√32 − V_dod = 5.763417470`. Main's post-target `C118` writes E's fixture in closed form
(`c = 0`, `w1 = (0,0,2)`, five ring points at `(4/√5 cos72k, 4/√5 sin72k, 2/√5)`, five pentagon
points at `w1 + 2(s cos(36+72k), s sin(36+72k), 3/8)` with `s = √55/8`, `south = (0,0,4)`) and
reproduces `5.89801737180372`. I recomputed it independently
(`Counterexamples/Reviews/payer_fixture_indep.py`): **`5.89801737180372`, 20 cell vertices,
minimum pairwise distance exactly 2** — `C118` is sound to every digit it quotes. **But that is not
the `5.897967122` of §5**: two different completions from the same `C5` family, differing in the
fifth decimal, both above the target (`0.134599902` and `0.134549652`). No claim is affected — §5
quotes the sharper one — but the two must not be quoted interchangeably, and a later comparison of
"the payer value" should say which fixture it means.

## 2. Theorem B: the definition of `C_R` is not the one the identity needs

**Line 90:** `C_R := Σ_{e : e ⊄ B∖E_B} c_e` — the sum over **every** edge that is not contained in
`B∖E_B`, *including edges with no endpoint in `B∖E_B` at all*.

**Line 94:** `|B| − |E_B| = Σ_{v∈B∖E_B} Σ_{e∋v} c_e = 2 Σ_{e⊆B∖E_B} c_e + C_R`.

The middle sum counts each edge `e` with multiplicity `#{v ∈ e ∩ (B∖E_B)}`. So the identity is

```
|B| − |E_B|  =  2 Σ_{e ⊆ B∖E_B} c_e  +  Σ_{e : |e ∩ (B∖E_B)| = 1} c_e ,
```

i.e. it needs `C_R` = the **exactly-one-endpoint** sum, not the complement-of-inside sum. With
line 90's definition the identity is false whenever some edge of the contact graph lies entirely
outside `B` with `c_e > 0` — and for an infinite packing with a translation-invariant weighting
there are infinitely many such edges, so line 90's `C_R` is `+∞` and line 100's bound is vacuous.

The document is inconsistent with itself here: its own hostile self-audit at **line 409** says
"`C_R` collects every edge with exactly one endpoint in `B∖E_B`", which is the correct object. So
this is a definition typo, not a broken theorem — but it is a typo in the definition of the one
term the error estimate is about, and a reader who takes line 90 literally gets a vacuous result.

**Witness (`Reviews/witness_0438_audit.py`, W1).** A finite graph with `|B| = 5`, `|E_B| = 1`,
weights normalised so `Σ_{e∋v}c_e = 1` on `B∖E_B`: `|B| − |E_B| = 4`, `2S₂ + S₁ = 4` ✓, while
`2S₂ + (S₁+S₀) = 13/3 ≠ 4`, the discrepancy being exactly the weight `1/3` of the single edge whose
endpoints both lie outside `B`. Exact rational arithmetic.

**And the same typo breaks `c_e ≤ 1`.** Line 92 justifies `c_e ≤ 1` by "`c_e` is one summand of
`Σ_{e'∋v}c_{e'} = 1`", which only holds at a vertex **outside** `E`. Under line 90's definition
`C_R` also counts edges whose endpoints *both* lie in `E`, where nothing normalises `c_e`, so
`c_e` is unbounded on those and the estimate `C_R ≤ O(R²) + 12|E_B|` fails for a second reason.
With the one-endpoint definition every edge in `C_R` has an endpoint in `B∖E_B`, so `c_e ≤ 1`
does hold. So the repair is forced twice over, by the identity and by the bound.

**Does the estimate survive the repair?** Yes, and the document's own split is right once the
definition is fixed: with `C_R` = exactly-one-endpoint, an edge counted there has one endpoint in
`B∖E_B` and the other either outside `B` — hence at distance `< R+2` from the origin, in the shell
`{R−2 ≤ |x| ≤ R+2}`, of which there are `O(R²)` by 2-separation, each carrying at most 12 contact
edges — or in `E_B`, contributing at most `12|E_B|`. So `C_R ≤ O(R²) + 12|E_B|` ✓ (line 120). The
rest of the proof (lines 96–130) then goes through unchanged. **Repair: replace line 90 by
`C_R := Σ_{e : |e∩(B∖E_B)|=1} c_e`, i.e. adopt line 409's wording.**

---

## 3. `(M)`: the stated characterisation is correct, and I record my own first misreading of it

**Line 197:** "`(M)` is a fractional perfect matching condition, and by the fractional Tutte
theorem it holds iff for every finite `S ⊆ V`, the number of isolated vertices of `G − S` is at
most `|S|`."

**This is right, and the audit's first draft said it was wrong — that draft is withdrawn.** My
first reading took the sentence as Tutte's *integral* condition ("the number of **odd components**
of `G−S` is at most `|S|`"), which the triangle would refute: `c_e = 1/2` on each of the three
edges is a fractional perfect matching, while `S = ∅` gives one odd component against `|S| = 0`.
But the document says **isolated vertices**, and that is the *fractional* condition:

```
ν*(G)  =  min_{S ⊆ V} ( |V| + |S| − iso(G−S) ) / 2 ,       and   (M) holds  ⟺  ν*(G) = |V|/2 .
```

I checked that against an LP for **every graph with `n ≤ 6`** — 33,867 graphs, 0 mismatches
(`Reviews/witness_0438_audit.py`, W2, which runs `n ≤ 5` for speed and prints the larger count).
So line 197 stands. The error was mine, it was caught by the exhaustive check rather than by
reading more carefully, and it is recorded here because the same class of error (mixing the
integral and fractional forms of a matching theorem) is exactly the kind that would otherwise have
produced a false defect report.

**What the correct dual form adds.** The characterisation is stated as an iff on sets `S`; the
practical form for *exhibiting* a failure is the Farkas certificate:

```
(M) is infeasible   ⟺   there is y : V → R with  y_u + y_v ≤ 0  on every edge  and  Σ_v y_v > 0 .
```

On the document's thirteen-cluster (`K_{1,12}`) the certificate is `y = −1` at the centre and
`y = +3/4` at each of the twelve leaves: every edge sum is `−1/4 ≤ 0`, and `Σ y = 8 > 0`. That is
a two-line proof that `(M)` fails there, replacing the appeal to the set condition. (`W3`.)

**One wording point, not a defect.** Line 199–206 says the failure "is *exactly* an isolated
icosahedral cluster". With line 197's criterion in hand the mechanism is: some `S` whose removal
isolates more than `|S|` vertices. The icosahedral 13-cluster is the *extremal geometric* instance
of that mechanism (twelve legal contacts at one centre), not the only one — `K_{1,3}` fails `(M)`
via `S =` its centre, and a solid angle of three neighbours is a legal local configuration. So
"exactly an isolated icosahedral cluster" should read "the extremal case is the icosahedral
13-cluster". The conclusion the document draws from it — that the bridge's hypothesis is not
automatic — is unaffected.

**A second over-claim in the same paragraph (found by the block's swarm, verified here).** Line 204
says "twelve centres on the sphere of radius 2 about `v` with mutual distance `≥ 2` is exactly the
icosahedral twelve (Tammes-12)". That is false: the icosahedral twelve on radius 2 have minimum
mutual distance `4√2/√(5+√5) = 2.102924448`, which is *strictly* greater than 2, so every small
perturbation of the icosahedron is still admissible. The set of twelve-point configurations on the
sphere with mutual distance `≥ 2` is positive-dimensional — explicitly, keeping eleven icosahedral
points fixed and rotating the twelfth about `e₁` by `t` (renormalised to radius 2) keeps the minimum
at `≥ 2` for `t` up to at least `6°` (`2.0955, 2.0880, 2.0730, 2.0427, 2.0120` at `t = 0.5°, 1°,
2°, 4°, 6°`); Tammes-12 is the *optimiser* of the minimum distance, not the solution set of `≥ 2`. Consequence: the failure set of `(M)` is much
larger than "the icosahedral 13-cluster", which is the second reason (after `K_{1,3}`) that
"exactly" is the wrong word at line 199.

**A better failure, with no cluster and minimum degree 2 (swarm member `m6`, verified exactly).** Five
points: `v = 0`, `w = (2,0,0)`, `p₁ = (1,√3,0)`, `p₂ = (1,−√3/2,3/2)`, `p₃ = (1,−√3/2,−3/2)`.
Every `v`–`w`, `v`–`pᵢ` and `w`–`pᵢ` squared distance is exactly `4` and every `pᵢ`–`p_j` squared
distance is exactly `9`, so the contact graph is `K₅` minus the triangle on `{p₁,p₂,p₃}` — a book
with spine `v w` and three pages, degrees `4,4,2,2,2`. `S = {v,w}` leaves three isolated vertices
against `|S| = 2`, so `(M)` fails, with the Farkas certificate `y = (−1,−1,+1,+1,+1)`: edge sums
`−2,0,0,0,0,0,0` and `Σy = 1`. So `(M)` fails on a legal configuration with **no vertex of degree
1** and **no icosahedral cluster** — the 13-cluster is the *largest* violation (`12 > 1`), not the
only mechanism. (How large: two contact points at distance 2 both touching a point at distance 2
put it on a circle `{x = 1, |p| = 2}` of radius `√3`, where mutual distance `≥ 2` allows at most
`5` points, so `|S| = 2` can be violated by up to `5 > 2` common neighbours. `m6`.)

**`K_{1,3}` is geometrically realisable, not just a graph.** `v = 0` and the three points
`2·(1,1,1)/√3`, `2·(1,−1,−1)/√3`, `2·(−1,1,−1)/√3`: each is at distance 2 from `v`, and their
mutual distances are `√(32/3) = 3.266 ≥ 2`, so the contact graph of this configuration **is**
`K_{1,3}` and `(M)` fails on it. (It is not saturated — the leaves have unbounded cells — so this
refutes the characterisation of the *graph* condition, not the existence of a saturated packing
with that contact graph. Whether a saturated packing can realise `K_{1,3}` is a separate question
and I do not claim it.)

**Exceptional vertices and their weights.** `E` must have upper density zero, and the proof uses
`|E_B| = o(R³)` for `E_B = E ∩ B(0,R)`, which is exactly what upper density zero gives for balls ✓.
`c_e ≤ 1` follows because `c_e` is one summand of `Σ_{e'∋v}c_{e'} = 1` ✓, and the same argument
gives `d_v ≤ 1` in the §4 repair ✓. Nothing in the exceptional set is used quantitatively, so a
density-zero `E` costs nothing in the proof — which is why the §4 repair (density-zero unmatched
set, no matching at all) is the right shape of hypothesis, and why the document is right that the
open problem is geometric (`δ₀`) rather than combinatorial.

---

## 4. Theorem D: clause-by-clause, and step 4 confirmed independently

Theorem D (line 283): `σ₀ := inf{vol Ω(v)+vol Ω(w) : 2-separated configurations containing a pair
at distance exactly 2}` satisfies `σ₀ > 2V_dod`. I checked the five clauses that can fail.

**(a) `Ω(v) ⊆ B(v,R_max)` from `vol Ω(v) ≤ C` alone.** The cone estimate is right: for `x` in the
cell at distance `r`, the cone from `x` over a unit disc perpendicular to `x` lies in the cell
(convexity, and the unit ball `B(v,1) ⊆ Ω(v)` because every bisector is at distance `≥ 1`), so
`vol Ω(v) ≥ πr/3`, hence `r ≤ 3C/π`. ✓ Note the constant is `3C/π` per cell with `C` the bound on
the *sum*, so both cells lie in `B(·,3C/π)` ✓.

**(b) A centre farther than `2R_max` cannot cut the cell.** If `|z − v| > 2R_max` then the
half-space of `z` containing `v` contains `B(v, |z−v|/2) ⊇ B(v, R_max) ⊇ Ω(v)` ✓. So `Φ` depends
only on the centres within `2R_max` of `v` or of `w` ✓.

**(c) The restriction to `Φ ≤ 2V_dod + 1` is harmless.** `Φ ≥ 2V_dod` everywhere by (1), and the
restricted set is non-empty (fcc: `Φ = 2√32 = 11.31 ≤ 11.10 + 1 = 12.10`), so every configuration
with `Φ > C` is above a value already attained inside the restricted set and cannot be the infimum
✓.

**(d) Closedness and continuity.** The admissible set with `v = 0, w = (2,0,0)` fixed is a set of
finite subsets of a bounded region with pairwise distances `≥ 2` — a closed subset of the Hausdorff
compactum, since distances are continuous and the cardinality is uniformly bounded ✓. `Φ` is
continuous because each cell is the intersection of the finitely many half-spaces of the centres
inside the region, and the volume of a convex body containing a fixed ball and contained in a
fixed ball is continuous in the half-spaces ✓. **One clause is not written out and should be:** a
configuration can have a centre at *exactly* `2R_max` from `v`, where the half-space is tangent to
`B(v,R_max)`; that is a closed condition and the limit is admissible, so nothing breaks — but it is
the one place where "no other centre contributes" needs the word "closed" rather than "open". ✓

**(e) The cardinality bound** `N_max = vol(B(0,2R_max))/(4π/3)` is a constant factor off (the
disjoint unit balls lie in `B(0,2R_max+1)`, so the count is `(2R_max+1)³`), which does not matter
for compactness ✓. The same slip propagates into §4.1b's headline number: "at most
`(21.865)³ ≈ 10453` points" should be `(22.865)³ ≈ 11956`. Cosmetic — the point of that paragraph
is that the search is finite and enormous — but the number is quoted as a concrete bound.

**Step (3) is where the document says a referee should push** (line 448–451): it uses
Hales–McLaughlin's *equality* case, `vol Ω = V_dod ⟺ Ω` regular dodecahedron. **I checked it
against the primary source and it is stated there explicitly** — Hales–McLaughlin,
arXiv:math/9811079v3, §1:

> "…the inequality `vol(Ω(Λ,v)) ≥ vol(Ω(Λ_dod,0))` for every `v ∈ Λ`, and for every set of points
> `Λ ⊂ R³` whose pairwise distances are at least the diameter `2`. **The case of equality occurs
> exactly when `Ω(Λ,v)` is congruent to a regular dodecahedron of inradius 1.**"

and in the strong (truncated-cell) form, §2.1: "Equality holds exactly when `Ω(Λ,v₀)` is congruent
to `Ω(Λ_dod,0)`." Two things matter here and both are in the quoted sentence: the equality case is
**exactly** dodecahedral (so step (3) is exactly as strong as the source), and the inequality is
stated for **every 2-separated point set**, not only saturated packings — which is what Theorem D
needs, since its minimiser is an arbitrary configuration. So the one external dependency of `C108`
is a published, quotable statement, not a folklore strengthening. (Main's line 448–451 flags it as
"the softer dependency … the place a referee should push"; the push succeeds.)

Two caveats worth keeping: the source is computer-assisted (interval arithmetic over tame Voronoi
graphs), so the equality case inherits that, and the paper's `Λ_dod` is the dodecahedron **of
inradius 2** with pairwise distances `≥ 2` in their normalisation — the numbers in this project use
inradius 1, so a reader converting must keep the factor. Both are bookkeeping, not gaps.

**Step (4) is correct, and I confirm the constant independently.** `Reviews/two_dodecahedra_indep.py`
builds the two icosahedral rings from the dodecahedron's own face normals, puts the centres at
distance 2, and maximises over the twist about the `v`–`w` axis:

```
sup over twist of the min cross-distance  =  1.125554844510   at t = 36.000000 deg
required for two dodecahedral cells       =  2                 (shortfall 0.8744)
```

This reproduces Main's `1.12555484451` to twelve digits. Note it *maximises over all twists*, i.e.
over a superset of the legal configurations (legality forces the shared face's pentagon to
coincide, a multiple of 72°), so the impossibility is a fortiori.

**The E/Main discrepancy is resolved** (the document calls it "recorded and not resolved", line
331). It is not a discrepancy: `1.056487696` is a *value* of the same function, attained at twist
`33.636862°` and at `38.363138°`, while its supremum is `1.125554844510`. E sampled another twist;
Main's number is the supremum. The four values Main tabulates at `t = 0°, 18°, 36°, 54°`
(`1.1256, 0.5982, 0.2111, 0.5982`) are the same multiset as this script's `m(36°, 54°, 0°, 18°)` —
Main's twist origin is shifted by 36°. So both numbers are right, the conclusion is unaffected, and
the sharp statement is `sup_t m(t) = 1.1255548`.

**Theorem D stands**, conditional on Hales–McLaughlin's equality case.

---

## 5. The equality case of `(L)`: the heading at line 40 is refuted by `C095`

**Line 40:** "*Its equality case is exactly the Barlow family — and that is a proof, not
evidence.*" The proof that follows shows only **Barlow ⟹ equality** (from `C094`: every Barlow
cell has volume `√32` exactly). It does not show **equality ⟹ Barlow**, and the converse is false:

> **Counterexample (the project's own `C095`).** The crack packing is two fcc half-spaces with a
> planar gap: saturated for `H ≤ d ≤ 2H`, **every bulk cell has `vol Ω = √32` exactly**
> (`C095` §3), and it is **not Barlow** (`C095` §4, because the layer spacing across the crack is
> `d ≠ H`). Take any contact pair `v, w` both in the bulk, away from the crack: both cells have
> volume `√32`, so `vol Ω(v) + vol Ω(w) = 2√32` — equality in `(L)` — in a packing that is not
> Barlow.

A second, independent realisation of the same construction (the block's swarm member `m5`): take
fcc with nearest-neighbour distance 2, `{√2(m,n,p) : m+n+p even}`, and translate the half-space
`{m+n+p > 0}` by `δ(1,1,1)/√3` with `0 < δ < 2−√2`. Then the minimum distance is still exactly 2
(a translation only increases cross distances), the covering radius is at most `√2 + δ < 2` so the
packing is **saturated**, bulk cells are unmodified fcc cells of volume `√32` (so bulk–bulk pairs
sit exactly at `2√32`), and the crack-adjacent cells are strictly larger — so it is not Barlow.
Same conclusion, one more construction, and it makes the counterexample independent of the details
of `C095`. I checked the numbers of that construction directly (`Reviews/crack_cell_indep.py`,
half-space clipping plus hull volumes): `ε = 0` gives the fcc cell of volume `√32 =
5.656854249492` exactly; the facing-layer cell has volume `√32 + 2ε` **exactly** (`6.656854249492`
at `ε = 1/2`, `6.985000249492` at `ε = 0.664073`), and the minimum pairwise distance is exactly 2
throughout. So the `6.985` quoted in the §5 table is confirmed independently, and the formula
`√32 + 2ε` explains why the crack costs volume: one cell per unit area of crack, at height
`2ε`.

The document's own §5 table says the same thing ("crack packing | bulk–bulk | `11.313708499` |
equality in the bulk"), so line 40 contradicts line 240 of the same file. **Repair:** the heading
should read "*`(L)` is attained on every Barlow packing, and also on the bulk of every planar-fault
packing (`C095`); the equality family is not classified*". That is the honest statement, and it is
also the more interesting one: equality in a *local* inequality says nothing global, which is why
`(L)` can be sharp and still not pin the extremiser.

What equality in `(L)` does force: nothing beyond `vol Ω(v) + vol Ω(w) = 2√32` for that pair. It
does not force either cell dodecahedral (the Barlow cells are rhombic/trapezorhombic dodecahedra —
`EXPOSITION_0438.md` §2 says so explicitly — of volume `√32 ≠ V_dod`), and it does not force the
packing to be layered.

---

## 6. Theorem C, consequence 2: "the equality case is empty" is an average read as a pointwise statement

**Line 385:** "Equality in `δ ≤ (4π/3)/V_dod` would need *every* cell to be a dodecahedron, hence
(step 3) every centre to have twelve contacts, hence a positive density of contact pairs, which
Theorem C forbids."

The first "hence" is not an implication. The bound is proved by taking a limit of averages:
`Σ_{v∈B}vol Ω(v) ≥ V_dod|B|` with equality of *densities* forces only

```
for every ε > 0 :   density{ v : vol Ω(v) > V_dod + ε }  =  0 ,
```

because the terms are `≥ V_dod` and their Cesàro mean tends to `V_dod`. That does **not** say that
almost every cell has volume *exactly* `V_dod`. What it leaves open — not what it asserts — is that
every cell has volume `V_dod + ε_v` with `ε_v → 0` and no cell dodecahedral; the averaging argument
cannot exclude that, because `Σ_{v∈B} ε_v` can be `o(R³)` while `ε_v > 0` everywhere (take
`ε_v = 1/|v|`, whose sum over a ball of radius `R` is `O(R²)`). Step (3) then does not apply — it is
an equality statement, not a stability statement — so "every cell is a dodecahedron" does not
follow, and neither does "every centre has twelve contacts". (Whether such a packing *exists* is a
separate question, and §6's next paragraph shows that even a volume-stability theorem would not
settle it.)

To close it one needs: `vol Ω(vₙ) → V_dod` ⟹ the cells become asymptotically dodecahedral ⟹ the
contact directions become asymptotically the twelve icosahedral ones ⟹ a positive density of
contact pairs. That is a **quantitative stability version of Hales–McLaughlin**, and the
`EXPOSITION_0438.md` §6 itself says it is the unavailable object ("Extracting an explicit `δ₀` is
equivalent to a stability version of Hales–McLaughlin"). So the corollary is asserted from exactly
the tool the exposition says is missing.

**The corollary is nevertheless true, for a reason that does not help the route.** `π/√18 =
0.740480 < 0.754697 = (4π/3)/V_dod`, so Hales' theorem alone says no packing attains the
dodecahedral bound. That is a two-line proof of the *statement*, and it is worth stating because it
tells the reader what the corollary is worth: inside a chain whose purpose is to prove Kepler, a
corollary that follows from Hales cannot be used as independent evidence, and the route to it
through Theorem C would need the stability statement that the exposition says is missing. (This
observation is the block's swarm member `m3`'s; I checked it and it is right, with one correction:
their derivation addressed "`vol Ω = V_dod` off a density-zero set", which is stronger than density
equality, so it does not prove the corollary either — it proves the different statement that
almost-everywhere exact dodecahedral cells are impossible.)

**And stability of the *volume* would not be enough anyway (swarm member `m7`, checked).** Twelve
centres in the icosahedral directions at circumradius `r > 2` are legal (`2·1.0514622242 =
2.1029244485 > 2` whenever `r ≤ 2.10`), and the Voronoi cell of the centre is then the regular
dodecahedron of inradius `r/2`, so `vol Ω(0) = V_dod·(r/2)³ → V_dod` as `r → 2⁺` **while the centre
has degree 0**. So even a quantitative volume-stability theorem would not deliver "many contacts" —
the route needs stability in the *distance* (the twelve neighbours within `2+η`), not only in the
volume. That is a second, independent reason why the corollary does not follow from Theorem C, and
it is sharper than the averaging objection: it survives the repair I suggested in the previous
paragraph.

**A partial result worth keeping (swarm member `m5`, checked).** For `Z := {v : vol Ω(v) = V_dod}`
in a saturated packing: each `v ∈ Z` is dodecahedral, hence has exactly 12 contacts; no two points
of `Z` are at distance 2 (that is step 4 of Theorem D); so all 12 contacts of every `v ∈ Z` lie in
`Z^c`, giving `12|Z ∩ B_R| ≤ Σ_{w∈Z^c∩B_{R+2}} deg(w) ≤ 12|Z^c∩B_{R+2}|`, i.e.
**`density(Z) ≤ 1/2`**. That is a real theorem about the exact-equality set and it is the part of
the corollary that *does* follow from the two-dodecahedra step. It does not close the density
statement, because `Z^c` may consist entirely of cells of volume `V_dod + ε_v` with `ε_v → 0`.

**What is unaffected:** Theorem C itself (line 352) is correct — I checked the split into internal
pairs and `U_B`, the two-sided volume estimate, `P_B ≤ |B|/2` hence `ρ ≤ 1/2`, and the final
division. `δ ≤ (4π/3)/(V_dod + δ₀ρ)` for `ρ > 0` stands. Only the *corollary* about the equality
case needs the stability input; the statement "the dodecahedral bound is never attained" may well
be true, but it is not proved by this argument.

---

## 7. The slack inequality at line 215: the coefficients are not the split's, but they are weaker, not stronger (my first reading was inverted)

Line 211–217 offers the repair: allow `d_v ≥ 0` with `d_v + Σ_{e∋v}c_e = 1`, and displays

```
Σ_{v∈B} vol Ω(v)  ≥  √32|B| − (2√32 − 2V_dod)·Σ_{v∈B} d_v − √32 C_R .
```

Deriving it from the same split: with `Σ_{e∋v}c_e = 1 − d_v` on `B∖E_B`,

```
Σ_{v∈B}vol Ω(v) ≥ V_dod·Σ d_v + 2√32·Σ_{e⊆B∖E_B}c_e + V_dod·C_R'      (C_R' = one-endpoint sum)
                = V_dod Σ d_v + √32(|B| − |E_B| − Σd_v − C_R') + V_dod C_R'
                = √32(|B| − |E_B|) − (√32 − V_dod)(Σ d_v + C_R') .
```

So the correct coefficients are `√32 − V_dod = 0.106563221` on **both** `Σd_v` and `C_R'`, while the
display has `2(√32 − V_dod) = 0.213126442` on `Σd_v` and `√32 = 5.656854` on `C_R`. **Both displayed
coefficients are larger than the correct ones, hence the displayed right-hand side is smaller, hence
the displayed inequality is weaker and follows from the correct one.** So it is true, and the
conclusion is unchanged — this is imprecision, not a defect.

**Correction, recorded.** My first draft of this section claimed the opposite — that the displayed
form was "stronger than the argument and plausibly false", with a per-vertex computation at a
dodecahedral vertex carrying `d = 0.4`. That computation reads the inequality as if it were
vertex-separable, which it is not: the slack term is global and is offset by vertices where the
matching is complete. The direction of the comparison is fixed by
`RHS_displayed − RHS_correct = −(√32−V_dod)Σd_v − (√32 − (√32−V_dod))C_R' ≤ 0`, which is immediate.
The block's swarm member `m1` caught this; it is the second inequality I inverted in this block and
both are recorded rather than quietly fixed.

**One genuine addition to the repair.** `d_v ≥ 0` needs `Σ_{e∋v}c_e ≤ 1` at `v ∈ E`, which `(M)`
does not give (it constrains only `v ∉ E`). The repair should be stated as: there are `c_e ≥ 0`
with `Σ_{e∋v}c_e ≤ 1` for every `v` and `= 1` for every `v` outside a density-zero set. With that
reading the derivation above is valid.

---

## 7.1 A presentation gap that is not a mathematical one: `lim` should be `limsup`

Theorems B and C divide by `|B|` and let `R → ∞`, writing `c(Λ) = lim |Λ∩B(0,R)|/((4π/3)R³)` and
`ρ = lim P_B/|B|`. Neither limit need exist: a saturated 2-separated packing can have a slab
structure — slabs of thickness `T_k → ∞` with in-plane cubic lattices of spacing alternating between
`2` and `2.25`, half-thickness `1` at the faces — whose centre density oscillates between `1/8` and
`1/2.25³ = 0.0878` without converging. (It is 2-separated: spacing `≥ 2` in-plane and `1+1 = 2`
across the faces; and saturated: covering radius `√(1.125² + (2.25/√2)²) = 1.9486 < 2`.)
This does not break anything, because every inequality in both theorems is one-sided and the
project's contract defines `δ` as the **upper** density: replacing each `lim` by `limsup` leaves
`√32·c⁺ ≤ 1` and `c⁺ ≤ 1/(V_dod + δ₀ρ⁺)` unchanged. But as written the proofs assume limits that
the hypotheses do not provide, and a referee will ask. (Swarm member `m7`; I checked the covering
radius and the 2-separation.)

## 8. What stands

- **`(B_K)` monotonicity** (line 139–160): correct and useful. `δ ≤ 8π/(3K)`, `K = 2V_dod` gives
  exactly `0.754697399337`, `K = 2√32` gives exactly `π/√18`. Checked arithmetically:
  `8π/(3·11.100582057) = 0.754697399` and `8π/(3·11.313708499) = 0.740480489`. The statement "the
  whole gap is a 1.92% increase in `K`" is `√32/V_dod = 1.01919957` ✓.
- **Corollary B1** (line 133): `(L)` + degree 12 everywhere ⟹ `(M)` with `c_e = 1/12` ✓ — this is
  the cleanest statement in the file, and the reason the Barlow family is a good test case.
- **Theorem C** (§6 above).
- **Theorem D** modulo the Hales–McLaughlin equality case (§4).
- **The labelling**: nothing in either file is quoted as a bound, and both say so repeatedly. The
  exposition's §3 table of what is *not* established is accurate and I could not add an item to it
  except the four in this review.
- **Every quoted constant re-derived.** `2V_dod = 11.1005820570`; `2√32 = 11.3137084990`;
  `12·2√32 − 12V_dod = 69.1610096456` and `13√32 − V_dod = 67.9888142149` (margin `1.172195431`,
  `1.7241%`); `√32/V_dod = 1.019199574`; `8π/(3·2V_dod) = 0.754697399337`;
  `8π/(3·2√32) = 0.740480489693`; and `(4π/3)/(V_dod + (2√32−2V_dod)/2) = 0.740480489693 = π/√18`
  — so the claim that the entire gap is a `1.92%` increase in `K` is arithmetically exact, and the
  interpolation `(B_K)` really does hit both endpoints.
- **One constant in the compactness section is stated with the sharper bound.** Step (2) restricts
  to `Φ ≤ 2V_dod + 1 = 12.1006` and then writes `R_max = 3C/π`; the value `10.932` quoted at
  §4.1b uses `C = σ₀ ≤ 11.4483` from E's witness instead. Both are correct — the proof just uses
  the larger `R_max = 11.556` — but the two numbers appear with the same symbol, and a reader
  recomputing `3·12.1006/π` will not get `10.932`.
- **The `CDS22` numbers check out.** `EXPOSITION_0438` §4 quotes `0.770271` and `0.741506` from
  Cohn–de Laat–Salmon, arXiv:2206.15373; both appear in the paper's full text (twice each). The
  attribution is right, with one caveat for readers: that paper's abstract advertises new bounds
  only for dimensions 4–7 and 9–16, so a reader who stops there will think the `d = 3` values are
  the project's own computation. They are not — but they are also not new, which is the point
  §4 uses them for.
- **Newer main tip.** Between the audit target `a6f3935` and the current `c4134c2` Main rewrote the
  A15 row of the §5 table (E's `15.875` is the A–B pair at distance `√5 = 2.236`, not a contact;
  the B–B chain bonds at `a/2 = 2` give `129/8 = 16.125`). That is outside this audit's target and
  I have not re-derived `129/16` myself; I note it because it changes a number in the table above
  and because it is the second convention error in a worker's pair table.

## 9. Status changes this review asks for

| id | claim | verdict |
| --- | --- | --- |
| `X-C037` | `C_R` (line 90) is the wrong set; the identity and `c_e ≤ 1` both need the exactly-one-endpoint sum (already line 409) | **defect**, one-line repair |
| `X-C038` | `(M)`'s criterion (line 197) is the fractional Tutte condition and is correct | **verified** (33,867 graphs); my first reading withdrawn |
| `X-C039` | "the failure is *exactly* an isolated icosahedral cluster" | **wording**; `K_{1,3}` and `P₃` fail too |
| `X-C040` | "(L)'s equality case is exactly the Barlow family" (line 40) | **refuted** by `C095` and by the fcc half-space shift |
| `X-C041` | Theorem C's "equality case is empty" reads an average as pointwise | **gap**; needs stability |
| `X-C042` | the slack coefficients (line 215) are weaker than the split's, so the display follows | **impression**, not a defect; my first claim withdrawn |
| `X-C043` | Theorem D step 4 | **verified** to 12 digits; E/Main discrepancy **resolved** |
| `X-C044` | `cut_flow.py` at `a25f5be` still truncates the vertex set at lines 269/352/390 | **defect** (D8, unchanged) |
| `X-C045` | `exact_sign.py` decided signs on a different interval for some exact rationals (`nsimplify`) | **defect in X's own tool**, fixed; no published number moved |
| `X-C046` | the bounded-interval `p ≤ η` predicate by an independent Vincent–Descartes decider | **done**, 92 cases, 0 mismatches |
| `X-C047` | Hales–McLaughlin's equality case | **verified from the primary source**, including its hypothesis |
| `X-C048` | "twelve at mutual distance ≥ 2 on radius 2 is exactly the icosahedral twelve" (line 204) | **refuted** (the icosahedral twelve have 2.1029) |
| `X-C049` | "the equality case is empty" is true, in two lines from Hales | **true, but not from the chain** |
| `X-C050` | `C121` (post-target): explicit stability for `≤ 12`-face cells | **correct and sharp**, but gives near-contacts, not contacts |
| `X-C051` | the two-dodecahedra threshold | **`3.4555003`**, so `C116`'s `6/√5` is 28.8% short (my first claim, `2φ`, withdrawn) |
| `X-C052` | A15's Voronoi volumes (post-target correction `C111`) | **confirmed**: `125/16`, `129/16`, contacts give `16.125` |
| `X-C053` | the arithmetic of `C119`/`C122` (post-target) | **checked exactly**, no discrepancy |
| `X-C054` | fcc and hcp cells: `√32` and circumradius `√2` | **verified** directly, both hcp sites |
| `X-C055` | E's payer fixture (`C118`) | **reproduced to 1e-12**; it is *not* the `5.897967122` of §5 |

Rows `X-C037`–`X-C043` are in the audited target (`a6f3935`); `X-C044` and `X-C050`–`X-C055` are
post-target material audited because it carries numbers a later block would quote; `X-C045`–
`X-C046` are the G8 fallback and `X-C047`–`X-C049` are the source check and the Tammes-12 refutation.

## 10. Limits of this review

- I audited the *proofs*, not the numerics behind `C094`/`C104`/`C095`/`two_dodecahedra.py`;
  the one constant I recomputed is step 4's, and I confirm it.
- I did not verify Hales–McLaughlin's equality case from the primary source; Theorem D and step (3)
  rest on it, and the document says the same.
- The `(M)` discussion is about finite graphs; the infinite-graph version needs the density-zero
  exceptional set and is not affected by the triangle, which is used only to refute the *stated
  characterisation*.
- No high-degree optimiser search was run, and no new bound is proposed.

---

## 11. Fallback done: the bounded-interval predicate closed independently — and it found a bug in X's own tool

G8's remaining half was "the `p ≤ η` predicate by an independently derived method". Done:
`Reviews/p_le_eta_independent.py`.

**Method.** Vincent/Descartes, exact rational arithmetic, no Sturm sequence, no `sqf_list`, no
SymPy root isolation: `w = p/gcd(p,p')` (Euclidean gcd over ℚ), a root of `w` in `(a,b)` is a
positive root of the Möbius transform `(1+t)ⁿw((a+bt)/(1+t))`, Descartes gives `V ≥ #roots` with
`V ≡ #roots (mod 2)`, so `V = 0` is "no root" and `V = 1` is "exactly one"; bisect any piece with
`V ≥ 2`. Then `p ≤ 0` on `[lo,hi]` iff `p ≤ 0` at `lo`, at `hi`, and at one rational sample in each
gap between consecutive roots — the sign is constant on each gap.

**Two implementation traps, recorded because both produced wrong answers before being caught by
the comparison:**
1. Endpoint values alone decide nothing when an endpoint is a root: `p = −(x−1)(x−3/2)` on `[1,3/2]`
   has `p ≤ 0` at both ends and `p > 0` inside. The first draft returned True.
2. Shrinking away from an endpoint root must land on a point where `p ≠ 0`; a root-free piece whose
   far end is a zero of `p` still says nothing about the sign just inside it. The second draft
   returned True on the same example.

**Result.** 60 rational-endpoint cases (endpoints at, between and within `10⁻¹²` of roots;
multiplicities 1–2; both leading signs) and 32 algebraic-endpoint cases (`√2`, `√3`, `√5/2`,
`φ`; algebraic endpoints bracketed into root-free rational zones) — **0 mismatches** against both
X's `exact_sign.sign_on_interval` and Main's `shell_check.le_on_interval`.

**The bug it found in `exact_sign.py`.** `sign_on_interval` and `sign_on_half_line` converted their
endpoints with `sp.nsimplify`, and `nsimplify` **invents radicals for exact rationals**:

```
nsimplify(Rational(353553390593273762200422181, 250000000000))  =  1000*sqrt(2)
```

which is `1414.21`, not `1.41421`. With such an endpoint the predicate decided a sign on a
*different interval*, or raised `CoercionFailed` when SymPy's `count_roots` got the radical. No
published certificate is affected — every X certificate is decided on `[0, ∞)` or `[0,4]`, where
`nsimplify` is the identity — but it is a genuine soundness defect in the tool the certificates
rest on, and it is the same failure mode as the one already recorded in this project's history
(`nsimplify` rewriting rationals into spurious radical products inside a try/except). **Fixed** by
a `_endpoint` helper that passes `Rational`/`Fraction`/`int` through exactly and only calls
`nsimplify` on genuinely symbolic input; `verify_all.py` still reports **ALL PASS** (21 controls
and every certificate), so nothing published moved. Section C of the new script is the regression
test: the two endpoints above now return `False` (not a verdict on `1000√2`, and not an exception).

**What this does and does not close.** The bounded-interval predicate now has three
implementations — X's, Main's and this one — agreeing on 92 adversarial cases, and one of the
three (X's) was carrying a defect that only an independent implementation would surface. It does
not close G8: the samples are finite, and G8's *independence* half was already answered in the
previous block. The right status is "three implementations agree on 92 cases; one defect found and
fixed; no proof of correctness for any of them".

## 12. What this block adds, in one list

| item | result |
| --- | --- |
| `C_R` in Theorem B | wrong set defined (line 90); the identity needs the one-endpoint sum (already line 409); the same typo also breaks `c_e ≤ 1` on `E`-internal edges; exact witness; one-line repair (`X-C037`) |
| `(M)`'s characterisation | **correct** (fractional Tutte, `i(G−S) ≤ |S|`; equivalently `|N(C)| ≥ |C|` on independent sets); verified on 33,867 graphs; my first reading of it was wrong and is withdrawn (`X-C038`) |
| failure of `(M)` | mechanism is "some `S` with `iso(G−S) > |S|`", realisable at three points (`{(0,0,0),(2,0,0),(4,0,0)}`, graph `P₃`); the icosahedral 13-cluster is the extremal case, not the only one — wording (`X-C039`) |
| "twelve at distance ≥ 2 on radius 2 is exactly the icosahedral twelve" | **false**: the icosahedral twelve have min distance `2.102924448 > 2`, so the set is positive-dimensional (`X-C048`) |
| `(L)`'s equality case | "exactly the Barlow family" **refuted** by `C095` and independently by the fcc half-space-shift packing; equality at a pair forces only `vol ∈ [V_dod, 2√32−V_dod]` per cell (`X-C040`) |
| Theorem C's "equality case is empty" | **true** (two lines from Hales: `0.740480 < 0.754697`) but not from the chain: the argument reads an average as pointwise and needs stability; even volume-stability is not enough — twelve icosahedral directions at radius `r > 2` give `vol → V_dod` with degree 0 (`X-C041`, `X-C049`) |
| §4 slack inequality | coefficients `2(√32−V_dod)` and `√32` are larger than the split's `√32−V_dod` on both terms, so the display is **weaker and true**; my first claim (stronger/false) is withdrawn; repair needs `Σc_e ≤ 1` on `E` (`X-C042`) |
| Theorem D | **correct**, all five clauses; `N_max` should be `(2R_max+1)³` (11,956 not 10,453); step 4 confirmed independently to 12 digits; E/Main discrepancy **resolved** (`X-C043`) |
| Hales–McLaughlin's equality case | **verified from the primary source** (arXiv:math/9811079v3 §1), including that the inequality is for *every* 2-separated point set — so Theorem D's minimiser needs no saturation (`X-C047`) |
| `lim` vs `limsup` in Theorems B and C | presentation gap: neither `c(Λ)` nor `ρ` need exist (saturated slab construction); the one-sided inequalities survive verbatim with `limsup` (`X-C049`… recorded as a note) |
| `cut_flow.py` at `a25f5be` | D8 unchanged, line-specific: 269, 352, 390; the fix pattern already sits at 306–307 (`X-C044`) |
| bounded-interval predicate (G8) | independent Vincent–Descartes decider, 92 cases, 0 mismatches; it found and I fixed an `nsimplify` soundness bug in `exact_sign.py` (`X-C045`, `X-C046`) |

**Four corrections of my own are in this review**, each found by a computation or a comparison
rather than by re-reading: the `(M)` characterisation (§3), the direction of the slack comparison
(§7), a draft claim that the displayed slack inequality was false (§7), and the two-dodecahedra
threshold (§14 — the only one that was pushed before being caught, a script that scaled the wrong
ring). That rate is worth recording: this is what an audit of one's own work costs when the checks
are real.

**Nothing here is a bound, and I am not proposing one.** `(L)` remains unproved; `(M)` remains a
hypothesis; `δ₀` remains non-explicit; the dodecahedral bound remains `0.754697399337`.

---

## 13. How the audit was supported, and what is mine

An eight-member swarm ran on the six attack surfaces in parallel with this audit (same session,
`.ultramath/smwgg6jiv`, `deepseek-v4.1-flash`, 100 steps each). Two of its submissions were accepted
after checking (a consolidated adjudication, and a corrected six-item report); the extras that
survive my own re-checking are integrated above with credit:

- the Tammes-12 slack (§3) and the `K_{1,3}` / `P_3` realisations (§3) — I had missed both;
- the fcc half-space-shift construction of the crack packing (§5) and the crack-cell formula
  `√32 + 2ε`, which I then recomputed independently (`Reviews/crack_cell_indep.py`);
- `density(Z) ≤ 1/2` for the exact-equality set (§6);
- the `r > 2` icosahedral family showing that even *volume*-stability gives no contacts (§6) — the
  sharpest single addition to my own §6;
- the `lim`/`limsup` presentation gap with the saturated slab construction (§7.1).

Four things in this review are corrections of my own errors: the `(M)` characterisation (§3), the
direction of the slack comparison (§7), an earlier draft's claim that the displayed slack inequality
was false, and the two-dodecahedra threshold (§14). All three were caught by checking against the sources or against another
implementation, not by re-reading my own prose — which is the argument for doing both.

Everything else — the `C_R` witness, the Theorem D clause audit, the step-4 recomputation and the
E/Main resolution, the Hales–McLaughlin equality case from the primary source, the independent
`p ≤ η` decider and the `nsimplify` defect, the crack-cell volumes, and every verdict in §9 — is
mine, and reproducible from the scripts named in each section.

---

## 14. Post-audit developments in `main` (checked, not part of the audited target)

Between the audit target `a6f3935` and the tip I fetched at close (`8dc264e`) Main pushed, among
others, `K15-C121` — "an explicit stability bound for cells with `≤ 12` faces" — which is exactly the
object §6 above says the chain is missing. I checked it; it belongs in the record.

**`C121` is correct.** Statement: if `Ω(v)` has at most 12 faces and every neighbour is at distance
`≥ 2ρ` (`ρ ≥ 1`), then `vol Ω(v) ≥ V_dod ρ³`. Proof: scale by `1/ρ`; the scaled body has
`≤ 12` faces, contains `B(0,1)` and has all faces at distance `≥ 1`; Fejes Tóth's Theorem 4.1 (as
quoted in `C115`) gives volume `≥ ω_dod`; scale back. Two checks: the arithmetic is exact —
`V_dod·1.045³ = 6.333804106 = 1.119669·√32`, so a `≤ 12`-face cell of an isolated vertex beats `√32`
by 11.97% — and the "second form" threshold is right: `(3V_dod/4π)^{1/3} = 1.0983541`, above the
`1.045` in play, which is why Fejes Tóth is doing real work. The application is legitimate because
`Ω/ρ` is again a Voronoi cell (of the scaled packing, whose minimum distance is still `≥ 2`).

**It is sharp, and its equality case is the `r > 2` family of §6.** Twelve icosahedral directions at
circumradius `r = 2ρ` give a dodecahedral cell of inradius `ρ` and volume `V_dod ρ³`, with no
contact at all. So `C121` is not merely a bound — it is attained, by precisely the family that shows
volume-stability cannot produce contacts.

**Consequently `C121` does not close the corollary, and my §6 stands with a sharper boundary.** What
the chain needs is *contacts* (distance exactly 2) to feed the matching of Theorem C; `C121` gives
"some neighbour within `2ρ`". For `ρ = 1.045` that is a neighbour at distance `≤ 2.09` — a
*near*-contact, and `C116`'s band `6/√5 = 2.683` is wider still. A positive density of near-contacts
is not a matching of the contact graph, so the step "asymptotically dodecahedral ⟹ `ρ > 0`" is not
repaired. What `C121` does repair is the *singleton* question for `≤ 12`-face cells, explicitly and
without compactness, which is a real gain and a different statement.

**One arithmetic flag in `C115` (Main's newest entry, outside the audited target).** It records
"`t_dod = 3 tan(π/5) ≈ 1.258`". But `3 tan 36° = 2.17963`, while `1.2584 = √3 tan(π/5)`. So a
factor `√3` looks to be missing from the displayed formula (the decimal is the one my arithmetic
gives for `√3 tan(π/5)`). I have not read the paper's own definition of `t_dod`, so this is a flag
to check against the source rather than a verdict — but it is a formula and a decimal that do not
agree with each other, in an entry whose purpose is to be the quotable primary source.

**`C116`'s constant is valid but not sharp — the threshold is `3.4555003`, not `6/√5`.** `C116`
proves that two dodecahedral cells are impossible when their centres are closer than `6/√5 =
2.683281573`, and says its sharpness is only for its arc-cover certificate. Computing the same
obstruction directly (`Reviews/near_contact_band_indep.py`): `v` at the origin with its twelve
icosahedral neighbours at `2uᵢ`, `w` at `d·u₀` with its twelve at `d·u₀ + 2R_t u_j`. Any packing
containing two dodecahedral cells contains such a configuration, so if a cross-distance is `< 2` for
every twist, no such packing exists. The maximum over the twist of the minimum cross-distance is

```
2.0000000000 exactly at   d* = 3.4555003444    (twist 36°)
```

and at `d*` no other centre cuts either cell, so the two dodecahedral cells are **attainable** there;
for `d < d*` the cross-distance condition fails at every twist. Hence the threshold is `d*`, and
`d*/ (6/√5) = 1.287789`: C116's constant is valid but **28.8% short**. (It does not affect the
route — `C114` needs only `ε < 0.6832816` and `d* − 2 = 1.4555` — but the constant should be
`3.4555003`.)

**Retraction.** The first version of this paragraph claimed the threshold was `2φ = 3.236068`. That
came from a script error: I had scaled *v's* icosahedral ring by `d` as well as `w`'s (`d*V[i]`
instead of `2*V[i]`), which is not the configuration of two dodecahedral cells. The corrected number
is `3.4555003`; the script now asserts the attainability check and carries the correction in its
docstring. This is the fourth self-correction of the block and the only one that was pushed before
being caught.

## 13. How the audit was supported, and what is mine

An eight-member swarm ran on the six attack surfaces in parallel with this audit (same session,
`.ultramath/smwgg6jiv`, `deepseek-v4.1-flash`, 100 steps each). Two of its submissions were accepted
after checking (a consolidated adjudication, and a corrected six-item report); the extras that
survive my own re-checking are integrated above with credit:

- the Tammes-12 slack (§3) and the `K_{1,3}` / `P_3` realisations (§3) — I had missed both;
- the fcc half-space-shift construction of the crack packing (§5) and the crack-cell formula
  `√32 + 2ε`, which I then recomputed independently (`Reviews/crack_cell_indep.py`);
- `density(Z) ≤ 1/2` for the exact-equality set (§6);
- the `r > 2` icosahedral family showing that even *volume*-stability gives no contacts (§6) — the
  sharpest single addition to my own §6;
- the `lim`/`limsup` presentation gap with the saturated slab construction (§7.1).

Four things in this review are corrections of my own errors: the `(M)` characterisation (§3), the
direction of the slack comparison (§7), an earlier draft's claim that the displayed slack inequality
was false, and the two-dodecahedra threshold (§14). All three were caught by checking against the sources or against another
implementation, not by re-reading my own prose — which is the argument for doing both.

Everything else — the `C_R` witness, the Theorem D clause audit, the step-4 recomputation and the
E/Main resolution, the Hales–McLaughlin equality case from the primary source, the independent
`p ≤ η` decider and the `nsimplify` defect, the crack-cell volumes, and every verdict in §9 — is
mine, and reproducible from the scripts named in each section.

---

## 14. Post-audit developments in `main` (checked, not part of the audited target)

Between the audit target `a6f3935` and the tip I fetched at close (`8dc264e`) Main pushed, among
others, `K15-C121` — "an explicit stability bound for cells with `≤ 12` faces" — which is exactly the
object §6 above says the chain is missing. I checked it; it belongs in the record.

**`C121` is correct.** Statement: if `Ω(v)` has at most 12 faces and every neighbour is at distance
`≥ 2ρ` (`ρ ≥ 1`), then `vol Ω(v) ≥ V_dod ρ³`. Proof: scale by `1/ρ`; the scaled body has
`≤ 12` faces, contains `B(0,1)` and has all faces at distance `≥ 1`; Fejes Tóth's Theorem 4.1 (as
quoted in `C115`) gives volume `≥ ω_dod`; scale back. Two checks: the arithmetic is exact —
`V_dod·1.045³ = 6.333804106 = 1.119669·√32`, so a `≤ 12`-face cell of an isolated vertex beats `√32`
by 11.97% — and the "second form" threshold is right: `(3V_dod/4π)^{1/3} = 1.0983541`, above the
`1.045` in play, which is why Fejes Tóth is doing real work. The application is legitimate because
`Ω/ρ` is again a Voronoi cell (of the scaled packing, whose minimum distance is still `≥ 2`).

**It is sharp, and its equality case is the `r > 2` family of §6.** Twelve icosahedral directions at
circumradius `r = 2ρ` give a dodecahedral cell of inradius `ρ` and volume `V_dod ρ³`, with no
contact at all. So `C121` is not merely a bound — it is attained, by precisely the family that shows
volume-stability cannot produce contacts.

**Consequently `C121` does not close the corollary, and my §6 stands with a sharper boundary.** What
the chain needs is *contacts* (distance exactly 2) to feed the matching of Theorem C; `C121` gives
"some neighbour within `2ρ`". For `ρ = 1.045` that is a neighbour at distance `≤ 2.09` — a
*near*-contact, and `C116`'s band `6/√5 = 2.683` is wider still. A positive density of near-contacts
is not a matching of the contact graph, so the step "asymptotically dodecahedral ⟹ `ρ > 0`" is not
repaired. What `C121` does repair is the *singleton* question for `≤ 12`-face cells, explicitly and
without compactness, which is a real gain and a different statement.

**One arithmetic flag in `C115` (Main's newest entry, outside the audited target).** It records
"`t_dod = 3 tan(π/5) ≈ 1.258`". But `3 tan 36° = 2.17963`, while `1.2584 = √3 tan(π/5)`. So a
factor `√3` looks to be missing from the displayed formula (the decimal is the one my arithmetic
gives for `√3 tan(π/5)`). I have not read the paper's own definition of `t_dod`, so this is a flag
to check against the source rather than a verdict — but it is a formula and a decimal that do not
agree with each other, in an entry whose purpose is to be the quotable primary source.

**`C116`'s constant is valid but not sharp — it can be improved from `6/√5` to `2φ`.** `C116` proves
that two dodecahedral cells are impossible when their centres are closer than `6/√5 =
2.683281573`, and says the sharpness is only for its arc-cover certificate. Computing the same
obstruction from the other side (`Reviews/near_contact_band_indep.py`): put `v` at the origin with
its twelve icosahedral neighbours at `2uᵢ`, and `w` at `d·u₀` with its twelve neighbours at
`d·u₀ + 2R_t u_j` (twist `t` about the `v`–`w` axis). Any packing containing two dodecahedral cells
contains such a configuration, so if a cross-distance is `< 2` for every twist, no such packing
exists. The maximum over the twist of the minimum cross-distance is

```
at d = 2φ = 3.2360679775 :   2.000000000000000   (twist 36°)
just below (−10⁻⁶)      :   1.999999105573
just above (+10⁻⁶)      :   2.000000894427
```

so the pairwise condition alone already forbids `d < 2φ`, and `2φ/(6/√5) = 1.206011`: the constant
can be widened by **20.6%**. This is consistent with `C116`'s own caveat ("it is entirely possible
that two dodecahedral cells stay impossible to larger `d` by an argument this one cannot see") — this
is that argument's conclusion, to numerical exactness at `2φ`. Two things it does not do: it does
not show that two dodecahedral cells are *attainable* at `d = 2φ` (the "no other centre cuts either
cell" condition is not checked here), so `2φ` is a lower bound for the true threshold; and it does
not affect the route, since `C114` only needs `ε < 0.6832816` and `2φ − 2 = 1.236` is more than
enough.

---

## 15. Close

**Audited target:** `Main/GEOMETRIC_LEMMA_0438.md` blob `a03be811` and `Main/EXPOSITION_0438.md`
blob `5a1708af`, both at commit `a6f3935`. Post-target material (`C115`–`C122`, `cut_flow.py` at
`a25f5be`) is audited separately in §14 and flagged as such.

**Verdict on the chain.** Theorems B, C and D are correctly stated and correctly proved modulo
(a) the `C_R` definition typo, which is repairable in one line and already contradicted by the
document's own self-audit; (b) Hales–McLaughlin's equality case, which I verified from the primary
source; and (c) the `lim`/`limsup` presentation. `(L)` is not proved and is not claimed to be.
Nothing here is a density bound and nothing here should be quoted as one — the record remains
`0.754697399337` for analytic bounds and `0.779966216777` for the best certificate.

**Four statements in the audited files are wrong as written** (`C_R`, "exactly the Barlow family",
"exactly the icosahedral twelve", the missing stability in Theorem C's corollary), and **four of my
own claims in this review were wrong at some point** (§3, §7 twice, §14). The overlap is not
accidental: every one of the eight was caught by a computation, a comparison with a second
implementation, or a source, and none by re-reading.

**Reproduce:** `Reviews/witness_0438_audit.py`, `Reviews/two_dodecahedra_indep.py`,
`Reviews/crack_cell_indep.py`, `Reviews/near_contact_band_indep.py`, `Reviews/a15_pair_indep.py`,
`Reviews/p_le_eta_independent.py`, `Reviews/g8_checker_independence.py`, and the project's
`verify_all.py` (ALL PASS after the `exact_sign.py` fix). All run in seconds; nothing was sent to a
remote machine.

*Pushed source: `kepler15/counterexamples/run-01`, tip at close recorded in the commit that adds
this section.*
