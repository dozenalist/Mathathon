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
sphere with mutual distance `≥ 2` is positive-dimensional; Tammes-12 is the *optimiser* of the
minimum distance, not the solution set of `≥ 2`. Consequence: the failure set of `(M)` is much
larger than "the icosahedral 13-cluster", which is the second reason (after `K_{1,3}`) that
"exactly" is the wrong word at line 199.

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
almost every cell has volume *exactly* `V_dod`; it allows every cell to have volume
`V_dod + ε_v` with `ε_v → 0`. Step (3) then does not apply (it is an equality statement, not a
stability statement), so "every cell is a dodecahedron" does not follow, and neither does "every
centre has twelve contacts".

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

**What is unaffected:** Theorem C itself (line 352) is correct — I checked the split into internal
pairs and `U_B`, the two-sided volume estimate, `P_B ≤ |B|/2` hence `ρ ≤ 1/2`, and the final
division. `δ ≤ (4π/3)/(V_dod + δ₀ρ)` for `ρ > 0` stands. Only the *corollary* about the equality
case needs the stability input; the statement "the dodecahedral bound is never attained" may well
be true, but it is not proved by this argument.

---

## 7. The slack inequality at line 215 has the wrong coefficients, and the conclusion survives anyway

Line 211–217 offers the repair: allow `d_v ≥ 0` with `d_v + Σ_{e∋v}c_e = 1`, and displays

```
Σ_{v∈B} vol Ω(v)  ≥  √32|B| − (2√32 − 2V_dod)·Σ_{v∈B} d_v − √32 C_R .
```

Deriving it from the same split: with `Σ_{e∋v}c_e = 1 − d_v` on `B∖E_B`,

```
Σ_{v∈B}vol Ω(v) ≥ Σ_e c_e Σ_{v∈e∩(B∖E_B)}vol Ω(v)
                ≥ 2√32·Σ_{e⊆B∖E_B}c_e + V_dod·C_R'          (C_R' = exactly-one-endpoint sum)
                = √32(|B| − |E_B| − Σd_v − C_R') + V_dod C_R'
                = √32(|B| − |E_B| − Σ d_v) − (√32 − V_dod)·C_R' .
```

So the correct inequality has
- coefficient `√32` on `Σd_v`, not `2√32 − 2V_dod` (which is `0.213`, thirty times smaller), and
- coefficient `√32 − V_dod = 0.1066` on `C_R`, not `√32`,

and it is *weaker* than the displayed one. The displayed version is not what the split gives. Since
both `Σ_{v∈B}d_v` and `C_R` are `o(R³)` in the intended regime (density-zero unmatched set,
`C_R ≤ O(R²) + 12|E_B|`), **the conclusion is the same under either coefficient**, so this is a
derivation slip, not a broken argument — but a reader who checks line 215 against line 94 will not
be able to reproduce it, and the numbers are thirty-fold different in one case.

---

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
- **Newer main tip.** Between the audit target `a6f3935` and the current `c4134c2` Main rewrote the
  A15 row of the §5 table (E's `15.875` is the A–B pair at distance `√5 = 2.236`, not a contact;
  the B–B chain bonds at `a/2 = 2` give `129/8 = 16.125`). That is outside this audit's target and
  I have not re-derived `129/16` myself; I note it because it changes a number in the table above
  and because it is the second convention error in a worker's pair table.

## 9. Status changes this review asks for

| id | claim | what this review found |
| --- | --- | --- |
| `X-C037` | Line 90's `C_R` is the wrong object; the identity needs the exactly-one-endpoint sum (already the wording at line 409) | **DEFECT (definition), one-line repair**; witness W1, exact |
| `X-C038` | Line 197's criterion for `(M)` is the **fractional** Tutte condition and is **correct**: verified against an LP on all 33,867 graphs with `n ≤ 6`, 0 mismatches. (An earlier draft of this review called it the integral condition and "refuted" it with the triangle; that reading was wrong and is withdrawn.) The Farkas form `y_u+y_v ≤ 0`, `Σy > 0` is the practical certificate form | **VERIFIED** (and my own error recorded); witness W2 |
| `X-C039` | "the failure is *exactly* an isolated icosahedral cluster" — the mechanism is "some `S` with `iso(G−S) > |S|`"; the 13-cluster is its extremal geometric case, not the only one (`K_{1,3}` fails too) | **Wording**, not a defect; witness W3 |
| `X-C040` | Line 40's "equality case is exactly the Barlow family" asserts an unproved converse that `C095`'s crack packing refutes (bulk–bulk pairs at equality, packing not Barlow) | **REFUTED as stated**; demote the heading |
| `X-C041` | Theorem C consequence 2 ("the equality case is empty") infers a pointwise statement from an average and needs a stability version of Hales–McLaughlin that the exposition says is unavailable | **GAP (not refuted)**; the corollary may be true, the argument is not a proof |
| `X-C042` | Line 215's coefficients (`2√32−2V_dod` on `Σd_v`, `√32` on `C_R`) are not what the split gives (`√32`, `√32−V_dod`); conclusion unaffected | **DEFECT (derivation)**, cosmetic |
| `X-C043` | Theorem D step 4 confirmed independently: `sup_t m(t) = 1.125554844510 < 2`; and E's `1.056487696` is `m` at twist `33.636862°`/`38.363138°`, so the "unresolved discrepancy" is resolved in Main's favour | **VERIFIED / RESOLVED** |
| `X-C048` | Line 204's "twelve centres on the sphere of radius 2 with mutual distance ≥ 2 is exactly the icosahedral twelve" is **false**: the icosahedral twelve have min distance `2.102924448 > 2`, so the admissible set is positive-dimensional; `K_{1,3}` is realisable at `2·(±1,±1,±1)/√3`, so the failure set of `(M)` is much larger than "the 13-cluster" | **REFUTED (over-claim)**; verified |
| `X-C049` | Theorem C's corollary "the equality case is empty" is **true** but follows in two lines from Hales (`π/√18 = 0.740480 < 0.754697 = (4π/3)/V_dod`), so it cannot be evidence inside a chain meant to prove Kepler; the route through Theorem C needs the missing stability statement | **TRUE but not from the chain** (`X-C041` stands as the gap) |
| `X-C044` | `cut_flow.py` at `a25f5be` (blob `c2127cee`) still infers the vertex set from the edge list at lines 269 (`find_violating_cut`), 352 (`feasible_flow`), 390 (`verify_flow_exact`); `exhaustive_cut_scan` already has the fix at 306–307 (`n = max(n, len(b_lo))`) but it was not propagated | **DEFECT (D8, unchanged)** |

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
| `C_R` in Theorem B | wrong set defined (line 90); identity needs the one-endpoint sum (line 409); exact witness; one-line repair (`X-C037`) |
| `(M)`'s characterisation | **correct** (fractional Tutte, verified on 33,867 graphs); my first reading of it was wrong and is withdrawn; Farkas form supplied (`X-C038`) |
| failure of `(M)` | mechanism is "some `S` with `iso(G−S) > |S|`"; the 13-cluster is the extremal case, not the only one — wording (`X-C039`) |
| `(L)`'s equality case | "exactly the Barlow family" **refuted by `C095`** (crack packing, bulk–bulk pairs at equality, not Barlow) (`X-C040`) |
| Theorem C's "equality case empty" | average read as pointwise; needs a stability version of Hales–McLaughlin that the exposition says is unavailable — gap, not refutation (`X-C041`) |
| §4 slack inequality | displayed coefficients not what the split gives (`√32`, `√32−V_dod` vs `2√32−2V_dod`, `√32`); conclusion unaffected (`X-C042`) |
| Theorem D step 4 | **confirmed independently to 12 digits**; E/Main "unresolved discrepancy" **resolved** (E's value is another twist) (`X-C043`) |
| `cut_flow.py` at `a25f5be` | D8 unchanged, line-specific: 269, 352, 390; the fix pattern already sits at 306–307 (`X-C044`) |
| bounded-interval predicate | independent Vincent–Descartes decider, 92 cases, 0 mismatches; found and fixed an `nsimplify` soundness bug in `exact_sign.py` (`X-C045`, `X-C046`) |

**Nothing here is a bound, and I am not proposing one.** `(L)` remains unproved; `(M)` remains a
hypothesis; `δ₀` remains non-explicit; the dodecahedral bound remains `0.754697399337`.
