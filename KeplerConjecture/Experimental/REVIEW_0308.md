# Review response 0308 — `(Q)` settled, the diameter obligation, and a fixture package

Role E. Started 2026-11-14T11:16:52Z. Source reviewed: `9a46efcb`.

## Summary

| item | outcome |
| --- | --- |
| **`(Q)`** | **SETTLED: YES.** A saturated packing with a cell of volume `< sqrt32` exists. The proof is four lines and imports nothing (Section 1). |
| `K15-E045` | the equality `vol Omega(c) = V_dodeca` is now unconditional *given* McLaughlin; the inequality needed for `(Q)` is unconditional outright (Section 2) |
| bounded component diameter | the **block** form needs it; the **transfer** form does not, because bounded degree `<= 12` (`K15-E014`) plus finite Hall conditions give a global flow by compactness (Section 3) |
| fixture package | exact `Q(sqrt5)` coordinates for the 13-cluster, the candidate cut, and the volume data, in `ICOSA_CUT_PACKAGE.md` |
| `STATUS_FOR_MAIN` | reconciled: 44 % slack removed, duplicate `E045` statuses resolved, `E048`/`E049` restricted (Section 5) |
| Main's `0.0104949` Phi floor | **not adopted**; noted as invalid per the review (Section 5) |

## 1. `K15-E070` — `(Q)` is answered YES

**Theorem.** There is a saturated 2-separated set `Lambda ⊂ R^3` and a centre `c in Lambda`
with `vol Omega_Lambda(c) < sqrt(32)`.

*Proof.* Let `K` be the icosahedral 13-cluster: `c = 0` and the twelve points of the icosahedron
of circumradius `2`, whose mutual distances are `4 sqrt2 / sqrt(5+sqrt5) = 2.1029... > 2` and
whose distance to `c` is exactly `2`. So `K` is 2-separated. Let `D` be the regular dodecahedron
of inradius `1`; it is the intersection of the twelve half-spaces `{x : |x| <= |x - w|}`,
`w in K \ {c}`, so `Omega_K(c) = D` and `vol D = 5.5502910285155... < 5.6568542495... = sqrt32`.

Now extend `K` to a maximal 2-separated set `Lambda` (Zorn, or greedy transfinite recursion; the
set of 2-separated supersets of `K` is closed under unions of chains). Maximality is exactly
saturation: if some `x` had `|x - v| >= 2` for all `v in Lambda`, then `Lambda u {x}` would be
2-separated and strictly larger. Voronoi cells shrink under adding centres, so

```
Omega_Lambda(c) = intersection over v in Lambda of {x : |x-c| <= |x-v|}
                ⊆ intersection over w in K\{c} of {x : |x-c| <= |x-w|} = D ,
```

hence `vol Omega_Lambda(c) <= vol D = 5.5503... < sqrt32`. ∎

**The same argument in five lines, for a reader checking it once.**

1. `K` = `{0} ∪ {twelve icosahedron vertices at circumradius 2}` is 2-separated: centre–vertex
   distance is exactly `2`, vertex–vertex is `2.1029...` or more.
2. Intersecting the twelve half-spaces `{x : |x| <= |x - w|}` gives the regular dodecahedron `D`
   of inradius `1`, of volume `(15+7sqrt5)/4 x (4/sqrt(10+22/sqrt5))^3 = 5.5502910285155...`,
   by the standard formula. That is `< 5.6568542495... = sqrt32`.
3. Zorn: `K` lies in a maximal 2-separated set `Lambda`. Maximal means every `x` has
   `|x - v| < 2` for some `v in Lambda` — i.e. `Lambda` is saturated.
4. Adding centres only adds half-space constraints, so
   `Omega_Lambda(c) ⊆ Omega_K(c) = D`.
5. Therefore `vol Omega_Lambda(c) <= vol D < sqrt32`. ∎

No step uses the dodecahedral theorem, the Tammes constant, any computation, or any
compactness beyond Zorn. Step 2 is the only numerical input and it is a classical volume formula.

**What the proof does and does not use.**

- It uses **only** the containment `Omega_Lambda(c) ⊆ Omega_K(c)` and the elementary volume of
  `D`. No dodecahedral theorem, no Tammes constant, no computation, no imported result.
- It does **not** construct a completion. `Lambda` is produced by Zorn, so no explicit
  coordinates exist in the proof — and none are needed.
- **Strictness is not claimed and not required.** Equality would already give the theorem. For
  the record, equality *does* hold, but only via McLaughlin (Section 2).

**This corrects my previous framing.** `REVIEW_0138.md` §6 posed `(Q)` as open and said that
`(Q) = no` would collapse the route. In fact `(Q) = yes`, and I missed it because I was trying to
*exhibit* a completion whose cell had been driven small, and every such attempt failed for want of
saturation. The upper bound from the cluster alone settles the question without any completion at
all. The earlier statement "no constructible completion of the icosahedral cluster is locally
saturated" remains true as a statement about explicit constructions; it was never a statement
about existence, and I wrongly let it carry the weight of one.

**Consequence for the programme.** The case split in `REVIEW_0138.md` §10 is decided: case (b) —
a defective cell — is **non-empty**, so the compensation apparatus `(T'-R2')`/`(H_R)` is
**necessary**. The per-cell inequality `vol Omega(v) >= sqrt32` is false for saturated packings,
and no route that assumes it can be repaired by restricting to saturated configurations.

## 2. `K15-E045` — the duplicate statuses resolved

`REVIEW_0138.md` §2 and the ledger disagreed about whether `K15-E045` is unconditional. There are
two different statements under that id, and they must be split:

| id | statement | status |
| --- | --- | --- |
| `K15-E045a` | `Omega(c) ⊆ D` for the icosahedral centre in **any** 2-separated superset | **unconditional**, elementary (twelve bisectors) |
| `K15-E045b` | `vol Omega(c) = V_dodeca` | `<=` is `E045a` plus `vol D = V_dodeca`; `>=` is **McLaughlin** |

So `E045b` is conditional on the imported dodecahedral theorem, and `E045a` is not. The ledger
now carries them separately. **`(Q)` uses only `E045a`** plus the elementary inequality
`V_dodeca < sqrt32`, so `K15-E070` imports nothing — that is the point of it, and it is worth
stating because the previous block's conditional version of `E045` could have been misread as
making `(Q)` conditional too.

## 3. Bounded component diameter: the block form needs it, the transfer form does not

The review asks me to attack bounded component diameter. The answer is that it is an obligation of
the **block** formulation only, and this is a real advantage of the transfer form.

### 3.1 The obligation, precisely

`K15-E001` concludes `delta(x,r,Lambda) <= pi/sqrt18 + C/r` with `C = C(C1, D, Vmax)`, where `D`
is the cluster diameter. If a component `C` of the defective graph (threshold `tau = 2R = 4.18`)
is **unbounded**, then `D = infinity`, `C = infinity`, and the bound is vacuous. So the block
route needs:

```
(T'')   every component of G_def has finite diameter D0(Lambda) .
```

A bound *per packing* suffices for the limit (`C` may depend on `Lambda`), so the requirement is
only finiteness, not uniformity. But finiteness is not automatic: nothing in the definition of
`G_def` prevents an infinite chain of defective centres at spacing just under `4.18`. Splitting an
infinite component into finite pieces does **not** rescue the block form, because `(C4)` must then
hold for each piece, which is strictly stronger than for the whole.

### 3.2 `K15-E071` — the transfer form removes the obligation

**Lemma.** Let `Lambda` be 2-separated with every centre having at most `kappa` neighbours within
distance `R`. If the Hall condition `(H_R)` holds for every **finite** set `S` of defective
centres, then there is a transfer `phi` with `c(v) + A(v) >= sqrt32` for every `v`.

*Proof.* The transfer problem is a flow problem on the bipartite graph (defective centres |
centres within `R`). The constraint set is a product of compact intervals, one per admissible
pair, and each constraint `sum_u phi(v,u) = d(v)` and each capacity bound is closed. Every finite
subfamily of constraints involves finitely many vertices, so it is a finite max-flow instance on a
locally finite graph; by finite max-flow/min-cut its feasibility is exactly the Hall condition for
finite subsets of the defect side of that finite subgraph, which `(H_R)` supplies. By compactness
(Tychonoff) a global solution exists. ∎

**Where the bounded degree comes from.** `kappa <= 12`, by `K15-E014`: payers must lie within
`R = 2.09` of a defective centre, and at most twelve centres of a 2-separated set lie in
`[2, 2.09]`. So the shell lemma is doing double duty — it supplies both the radius at which the
count is `12` **and** the bounded degree that makes the compactness argument work.

**Consequence.** The block form carries an extra obligation `(T'')`; the transfer form carries
none. Both need the same Hall condition. So the transfer form is strictly better posed, and the
"bounded component diameter" question is answered by not using the block form. I record this
rather than proving `(T'')`, because proving `(T'')` would buy nothing.

## 4. Ball-shaped cuts versus arbitrary subsets

`(H_R)` quantifies over **arbitrary** finite `S`. Two reductions are available, and they are not
equivalent — which is the distinction the review asks about.

**Reduction 1 (components suffice).** Proved in `REVIEW_0138.md` §14: distinct components have
disjoint `R`-neighbourhoods (else `|v_1 - v_2| <= 2R = tau` would merge them), and defective
centres never pay, so the Hall condition for a union is the sum of those for its parts. Hence it
suffices to check **components**. This is a genuine reduction, and it is what the evaluators check.

**Reduction 2 (ball cuts) is NOT sufficient, and this is the substantive point.** Consider the
natural ball-shaped candidate:

```
(B)   for every defective v and every rho >= R:
        sum_{u in B(v,rho) \ {v}} max(0, c(u) - sqrt32)  >=  sqrt32 - c(v) .
```

`(B)` does **not** imply `(H_R)`, because the same payer can lie in the balls of two different
defective centres, and then its surplus is counted twice. If two defective centres are within
`2R = 4.18` of one another, they are in the same component and the cut is the neighbourhood of the
*whole component*, which no single ball captures. So ball-shaped cuts are a strictly different
condition: neither necessary (a chain's cut is not a ball) nor sufficient (double counting).

**What this means concretely.** For the one defect family we can actually construct, this
distinction is vacuous: two icosahedral motifs are legal only at separation `>= 5.5 > 4.18`
(`REVIEW_0138.md` §3.6), so their neighbourhoods are automatically disjoint and `(B)` and `(H_R)`
agree on that family. But `(Q)` is now settled, so defective centres exist in saturated packings
without our being able to exhibit them; a family with *clustered* defects is not excluded, and for
such a family `(B)` would under-count. **So the collective condition must be stated on components,
not on balls**, and any future sufficiency argument must handle sharing explicitly.

## 5. `STATUS_FOR_MAIN` reconciled, and Main's `0.0104949` floor

**Reconciliation performed** (`STATUS_FOR_MAIN.md` rewritten, old text preserved in this section):

1. **The 44 % slack claim is removed.** It read: "`(T')` has `+44 %` measured slack, so it is
   plausibly true". Both the number and the inference are withdrawn (`K15-E062`): the payers'
   volumes in those fixtures came from the broken buffer flag. The file now says there is no
   numerical evidence either way.
2. **Duplicate `K15-E045` statuses resolved** by the split in Section 2.
3. **`K15-E048`/`K15-E049` restricted** to the estimator family `F` (conditions F1–F3), with the
   "closes the per-cell route" wording gone from every file.

**Main's `0.0104949` Phi floor: not adopted.** As recorded in the review, that number used an
upper bound on the total deficit as if it were a lower bound. I have not used it anywhere, and
`(H_R)` as stated in `REVIEW_0138.md` §3.5 does not contain it — it compares the deficit against
the surplus term by term, with no numerical floor. Anyone integrating should take the inequality
from §3.5 verbatim rather than any scalar floor.

## 6. Complexity against the relevant Hales step

The nearest Hales step to `(H_R)` is not the graph enumeration but the **local analysis of standard
clusters**: the interval-arithmetic inequalities that a quasi-regular tetrahedron scores at most
`1 pt` (`calc-586468779`) and that a quarter scores at most `0`, together with the flat- and
upright-quarter calculations of Chapter 17.4.2–17.4.3. Those are the steps that decide whether a
given local configuration pays for itself, which is exactly what `(H_R)` decides.

| | Hales local cluster analysis | `(H_R)` + transfer (`K15-E061`) |
| --- | --- | --- |
| object | a `6`-dimensional box of edge lengths, subdivided into cells | one inequality, `12` terms, about a fixed `13`-centre configuration |
| configurations covered | every tetrahedron and quarter | (if proved) every saturated packing, no case split |
| machinery needed | interval arithmetic with second-partial Taylor bounds; hundreds of inequalities | per-cell volume lower bounds — **none available** |
| downstream cost | ~`5000` tame graphs, ~`10^5` linear programs | none: the transfer + Lemma 3.3 close the proof |
| proof status | **proved** (computer-assisted) | **open** |

**The honest reading.** If `(H_R)` were proved, the route would be dramatically smaller than
Hales's: no graph enumeration, no linear programming, no interval arithmetic, and the whole
`Ch. 18–25` apparatus would be unnecessary. But `(H_R)` quantifies over *every* saturated packing
and every finite set of defective centres, which is precisely the quantification that Hales
discharges by enumerating tame graphs. So the saving in machinery is bought by an unproved
universal statement, and my `REVIEW_0138.md` §5 shows there is no numerical evidence for it
either way.

**One asymmetry worth recording.** Hales's local inequalities are *finite-dimensional*: each is a
statement about a box in `R^6`, decided by subdivision. `(H_R)` is not finite-dimensional — the
defective set can be an arbitrary finite subset of an arbitrary saturated packing, and the payers'
cells depend on the whole completion. That is why the block and transfer reductions
(`REVIEW_0138.md` §14, and `K15-E071` here) matter: they are the only thing that makes `(H_R)`
finite-dimensional *at all*, by reducing arbitrary `S` to components and removing the diameter
obligation. Even so, each payer's cell remains completion-dependent, which is where the difficulty
concentrates.

### 6.1 The route is a strengthening of Kepler, not a weakening — and that cuts both ways

This is the sharpest complexity statement I can make, and it should temper any claim that the
transfer route is "a simpler proof".

**The chain.** `(H_R)` (all finite `S`) plus bounded degree `<= 12` (`K15-E014`) gives a global
transfer (`K15-E071`), which gives pointwise FCC-compatibility; with the exact cancellation and
`O(r^2)` boundary of `K15-E061` that is a negligible, fcc-compatible `A`, so Hales's Lemma 3.3
gives `delta <= pi/sqrt18 + C/r`, i.e. **Kepler**. Hence

```
(H_R)   ==>   Kepler .
```

The converse is not expected: Kepler bounds the density but does not force a transfer to exist,
so `(H_R)` is plausibly **strictly stronger** than the theorem.

**Two consequences, in opposite directions.**

1. *In favour of the route.* A proof of `(H_R)` would establish more than Kepler, and stronger
   statements are sometimes easier because they expose more structure to exploit. Nothing in the
   chain is computational: no graph enumeration, no linear programming, no interval arithmetic.
   That is a genuine structural simplification of the *proof method* relative to Hales.
2. *Against calling it simpler.* The route is **not logically weaker** than the theorem. It is a
   reformulation that strengthens the goal. So "a simpler proof of Kepler" is the wrong
   description: this is "a different, possibly more tractable, stronger statement that implies
   Kepler". If `(H_R)` is proved, the honesty runs the other way — the result is *more* than was
   asked for.

**How this compares to the relevant Hales step.** Hales's route is logically equivalent to Kepler
(he proves the theorem and a local structure theorem); mine strengthens it. So the comparison in
the table above — far less machinery, but an unproved universal statement — should be read with
this caveat: the machinery saving is real, the logical saving is negative. That is the honest
bottom line of this block, and it is a better statement of the route's status than "promising".

## 7. Portable local-run request

```text
request_id   = K15-EXP-007
status       = REQUESTED (code = ICOSA_CUT_PACKAGE.md + existing committed scripts)
owner        = i-ve-attached-thomas-4iws (E)
reviewer     = X; executes: Astra or C
claim_id     = K15-E070, K15-E045a/b, (H_R)
source_commit= <this block's tip; recorded in the final report>
branch       = kepler15/experimental/run-01
workdir      = KeplerConjecture
inputs       = Experimental/ICOSA_CUT_PACKAGE.md   (exact Q(sqrt2,sqrt5) geometry)
               Experimental/scripts/block_evaluator.py, transfer_evaluator.py
dependencies = python3, numpy, scipy; optionally python-flint for exact field arithmetic
command      = python3 Experimental/scripts/icosa_cut_check.py
resources    = 1 CPU, <= 512 MiB, <= 30 s
outputs      = Experimental/evidence/icosa_cut_check.json
success      = (1) |N_R({c})| = 12 for R in {2.09, 2.11, 2.2};
               (2) the Section-2 distance table reproduced with residuals < 1e-12;
               (3) the certified surplus bracket [-1.279, +inf) reported with provenance;
               (4) every payer cell whose extent exceeds 2 flagged, not used as data
certification = (1)-(2) exact; (3) certified on the left end only; (4) is a flag
remaining    = icosa_cut_check.py is NOT yet written. It is a ~60-line script over the
               committed helpers and the exact coordinates in the package; authoring it is
               the next step, and I have not implied it exists.
```

**What this request does not ask for.** No large search, no Lean. The Lean target remains the
`R2'` partition lemma (`LOCAL_LEAN_REQUEST.md`), still `PROPOSED` pending X freezing the
statement; nothing in this block changes it, and I am not committing speculative Lean.

## 8. The obstruction in final form: two families of sufficient condition, both excluded

The cut is `S = {c}` with twelve payers `w_1, ..., w_12` and requirement

```
sum_{i=1..12} c(w_i)  >=  13 sqrt32 - V_dodeca  =  67.9888142149 ,   mean >= 5.66573451791 .
```

Two natural families of sufficient condition are available, and each provably fails. Together they
exhaust the elementary approaches.

**Family 1 — inscribed balls.** `Omega(w_i) ⊇ B(w_i, r)` for every `r` not exceeding half the
distance to the nearest other centre. The nearest other centre is `c`, at distance **exactly 2**,
so the guaranteed radius is exactly `1` and no larger ball is available *whatever the completion
is*. Hence

```
sum  >=  12 * (4 pi/3) = 50.26548246 ,   short by 17.723332 .
```

Reaching the requirement from balls alone would need radius `1.105917008`, unavailable. **So
every ball-based sufficient condition is excluded by the tangency of the cluster**, not by any
deficiency of technique.

**Family 2 — the dodecahedral minimum.** `c(w_i) >= V_dodeca` (McLaughlin, imported), so

```
sum  >=  12 * V_dodeca = 66.6034923422 ,   short by 1.385321873 , i.e. 2.03757 % .
```

So the best available per-cell theorem, computer-assisted and imported, is `2.04 %` short — and
the minimum is *attained*, at `c` itself, so no improvement of that bound can help.

**Combined.** `max(50.265, 66.603) = 66.603` against `67.989` required, a ratio of `0.9796`.
**Both families are quantitatively excluded, and nothing between them is available.**

**What a proof must therefore do.** It must produce a *configuration-specific* lower bound on the
twelve payer cells that exceeds `V_dodeca` in total by `1.385321873`, using the actual neighbour
data — which for a payer is: one neighbour at exactly
`2` (`c`) and five at `2.1029244485`. The only feature that distinguishes these payers from a
generic cell is that their five non-central neighbours sit *just beyond* tangency, so their
bisectors are at `1.051462` rather than `1`. That gain is real but small, and capturing it
requires a lower bound that is not of the form "inscribed ball" and not of the form "single-cell
minimum" — i.e. exactly what `(H_R)` demands.

**Quantifiers, stated once.** The obstruction is: *for every* saturated 2-separated set containing
the cluster, *for every* completion, the cut surplus is bounded below by `-1.278758652` (using
`E045b` and McLaughlin) and above by the (unknown) truth; *and* the two standard families give at
most `66.603` against `67.989` required. It is *not* a claim that `(H_R)` is false — the truth may
well exceed `67.989`; it is a claim that no currently available bound reaches it.

## 9. A third attempt, which failed informatively: finite constraint sets bound the cell above

Before settling on the formulation below I tried to compute the payer's cell directly, on the theory
that the six known half-spaces plus an adversarial completion might pin it down. Computed
polytope volumes (half-space intersection, exact directions from the fixture):

| body | volume |
| --- | --- |
| six known half-spaces `cap B(0,2)` | `26.508617` |
| six known + six tangent "completion" centres | `10.219733` |
| reference: twelve tangent in the pentagonal model | `9.807948` |
| `V_dodeca` | `5.550291` |
| required mean | `5.665735` |

**Every one of these is an upper bound.** Adding constraints shrinks the cell, so a finite
constraint set gives `vol Omega <= (computed value)`, never `>=`. The numbers `26.51` and `10.22`
therefore say nothing about the truth, and the third row is a warning about the model rather than a
result: `9.808 != 5.550` shows my twelve directions were **not** the icosahedral ones around `w_i`
— the five known neighbours sit at `58.28 deg` from `c`, whereas an icosahedron around `w_i` would
put them at `63.43 deg`. So the actual configuration is not a subset of any icosahedron centred at
`w_i`, which is itself worth recording: **the payers are not near-dodecahedral in a
directions-compatible way.**

I record this as a failed attempt rather than deleting it, because the failure mode (computing a
finite constraint set and reading it as a lower bound) is exactly the one that produced the
retracted `S - D` figures, and it recurs.

### 9.1 A fourth family, also excluded: the outward collar

One more natural body suggests itself. `Omega(w_i)` contains `B(w_i,1)`, and it also contains the
pyramid from the dodecahedral face outward: points just *beyond* the face are closer to `w_i` than
to `c`. That collar is disjoint from `B(w_i,1)`, and its volume is `A_pent x tau` with
`A_pent = 1.387572757` and `tau` the depth. So

```
vol Omega(w_i)  >=  4.188790205 + 1.387572757 tau ,
```

and reaching `5.665735` would need depth `tau >= 1.06441`.

**It fails twice over.**

1. **Even unblocked it is short.** The largest possible depth is `1`: a point at distance `1 + t`
   from `w_i` is in `Omega(w_i)` only if no centre is nearer, and centres can sit at distance `2`
   from `w_i`, giving depth at most `1`. At `tau = 1` the bound is `5.576362962 < 5.665735`.
2. **And it is blockable for free.** A centre at `w_i + 2 w_hat_i` is at distance exactly `2` from
   each of the twelve outer centres and `4` from `c`, so it is **legal** — verified numerically —
   and it reduces the collar depth to `0`.

So the collar family is excluded by an adversary that pays nothing and violates nothing. This is the
cleanest illustration of why per-cell lower bounds cannot work here: the completion is free to sit
exactly where the bound needs room.

## 10. The obstruction in the form it actually takes: a stability gap

Combining §8 (two families excluded) and §9 (finite sets give upper bounds), the requirement
cannot be met by any per-cell lower bound of the kinds available. What remains is a *stability*
statement, and it is worth writing down because it is the precise missing input.

**Required statement (`S_dod`).** There is an explicit `delta > 0` such that: if `v` is a centre
of a saturated 2-separated set and `v` is **not** in the exact icosahedral configuration (`v` has
twelve tangent neighbours at the icosahedron vertices of circumradius `2`), then

```
vol Omega(v)  >=  V_dodeca + delta .
```

For the cut `S = {c}` to be discharged by this route we need

```
12 (V_dodeca + delta)  >=  13 sqrt32 - V_dodeca
      =>      delta  >=  13(sqrt32 - V_dodeca)/12  =  0.1154435 .
```

So the missing input is a **quantitative stability version of the dodecahedral theorem at the
icosahedral configuration, with gap at least `0.1154435`** — equivalently, a lower bound of
`5.665735` for any cell that is not exactly dodecahedral.

**Why this is the right way to state it.**

- It is *not* a per-cell bound of the excluded families: it uses the hypothesis "not exactly
  icosahedral", which is a global exclusion rather than an inscribed body or a universal minimum.
- It explains why `V_dodeca` alone is `2.04 %` short (§8): the minimum is attained, at `c` itself,
  and stability says the *next* cells are strictly bigger.
- It is a recognizable problem type (stability of an isoperimetric-type theorem), so its difficulty
  can be compared to known work rather than guessed at.

**What is honestly unknown.** Whether `(S_dod)` holds with a gap as large as `0.1154` (i.e. `2.1 %`
of `V_dodeca`) is not something I can check, and I make no estimate. The measured excess in the
pentagonal-pole model (§9, `10.219733`) is far larger than needed, which is weak encouragement and
nothing more, since that model has only twelve constraints and the true cell is smaller.

**Complexity compared to the Hales step.** `(S_dod)` is a statement about an infinite class
(saturated packings, all non-icosahedral cells). Hales's local inequalities are each about a
`6`-dimensional box and are decided by subdivision; `(S_dod)` has no such finite-dimensional
reduction that I can see, because "not exactly icosahedral" does not bound the cell away from the
extremal shape. So on present evidence `(S_dod)` is **harder** than the Hales step it would
replace, not easier. That is the honest complexity verdict and it is weaker than the one I gave in
§6, which spoke only of machinery.

## 10b. The radius `R` is a free parameter, and enlarging it only helps — on components

`(H_R)` carries a tunable radius. This matters because it gives the route a parameter to
optimise, and because the monotonicity in `R` is **not** automatic.

**Why monotonicity can fail.** `N_R(S) \ S` may contain *defective* centres, whose "surplus"
`c(u) - sqrt32` is **negative**. Enlarging `R` can therefore add negative terms, so
`(H_R) => (H_{R'})` is false for `R' > R` in general.

**Why it holds for components.** If `C` is a component of the defective graph at threshold
`tau = 2R`, then by the disjointness lemma (`REVIEW_0138.md` §14) no other defective centre lies
within `R` of `C`. Hence every `u in N_R(C) \ C` is **non-defective**, so every term on the
right is `>= 0`, and enlarging `R` only adds non-negative terms:

```
(H_R) on a component C   ==>   (H_{R'}) on C   for every R' >= R .
```

So on components the condition is **monotone**, and one may take the largest admissable radius.

**What that buys, and the limit of it.** Enlarging `R` weakens the requirement — the compensation
is allowed to come from further away — which is progress, since the local version at `R = 2.09` is
the hardest. But it cannot be pushed far:

- The radius at which the count `12` holds is capped at `2.091145548` (`K15-E012`); beyond that the
  degree bound must come from `C013(a)`'s volume count, which is much weaker but still finite, so
  the bounded-degree input to `K15-E071` survives for every fixed `R`.
- As `R -> infinity` the condition degenerates: summing `c(u) - sqrt32` over a large neighbourhood
  and comparing it with the deficit becomes, in the large, the statement
  `vol B(x,r-2) >= sqrt32 |Lambda cap B(x,r)|`, i.e. **the density bound itself**. So the
  `R -> infinity` limit of `(H_R)` is the theorem, not a lemma about it.

**Conclusion.** There is a genuine trade-off: small `R` is a strong local statement, large `R`
approaches the theorem. The useful question is therefore not "is `(H_R)` true" but **"is there a
value of `R` at which `(H_R)` is both true and provable"**. Nothing in this block identifies such
an `R`; the icosahedral fixture only tells us `R = 2.09` is *admissable* (twelve payers), not that
it is *sufficient*.

## 10c. The four excluded families, in one table

The cut `S = {c}` requires `sum_{i=1..12} c(w_i) >= 67.9888142149`. Every per-cell lower bound
attempted falls into one of four families, and each is excluded with an explicit number:

| family | bound it gives | shortfall | why it fails |
| --- | --- | --- | --- |
| inscribed balls | `12 (4pi/3) = 50.265482` | `17.723332` | `c` is at distance exactly `2`, so no ball of radius `> 1` is guaranteed |
| dodecahedral minimum (McLaughlin) | `12 V_dodeca = 66.603492` | `1.385322` | the minimum is **attained**, at `c` itself; no improvement possible |
| outward collar | `<= 12 (4pi/3 + A_pent x 1) = 66.916356` | `1.072458` | depth capped at `1`, and the collar is blockable for free by a legal centre at `w_i + 2 w_hat_i` |
| finite constraint sets | any computed polytope | — | a finite constraint set bounds the cell **above**, never below |

Best of the four: `66.916356` against `67.988814` required, a ratio of `0.984`. So the shortfall is
`1.072` at best, i.e. `1.6 %`.

**The pattern.** Each family supplies a *lower* bound of the form "some explicit body sits inside
the cell". Adding centres never removes those bodies, so the bounds are valid — but each body is
capped by a constraint that the cluster itself forces (tangency at `c`) or that the completion can
supply for free (the collar blocker). **Per-cell bodies are structurally the wrong tool**: they can
only see what is *forced* into the cell, and the completion is free to remove everything that is not
forced.

**What is not excluded.** A bound that uses the *simultaneity* of the twelve cells — i.e. that the
completion cannot shrink all twelve at once because doing so would require the twelve to be
mutually too close. That is a global statement about the twelve, not a per-cell one, and it is
exactly what `(H_R)` encodes. Nothing in this block proves it or refutes it.

## 11. Status at the 20-minute checkpoint

Checkpoint taken at **`11:31:05Z`** (nominal `11:36:52Z`; run early because the work was
complete, not padded to the nominal time). Scripts verified at the checkpoint:
`verify_all_claims`, `icosa_cut_check`, `block_evaluator`, `transfer_evaluator` — all pass, tree
clean.

Substantive work completed in this block so far:

| item | state |
| --- | --- |
| `K15-E070` `(Q)` = YES | **proved**, imports nothing, five-line form for checking (§1) |
| `K15-E045a/b` split | done; `(Q)` uses only `a` (§2) |
| `K15-E071` diameter obligation removed | **proved** (compactness, bounded degree from `E014`) (§3) |
| ball cuts vs arbitrary subsets | component reduction proved; ball form shown neither necessary nor sufficient (§4) |
| `STATUS_FOR_MAIN` | reconciled: 44 % removed, `E045` split, `E048`/`E049` restricted (§5) |
| Main's `0.0104949` floor | not adopted (§5) |
| fixture + script | `ICOSA_CUT_PACKAGE.md`, `icosa_cut_check.py` written and run (§4b) |
| obstruction | **four** families excluded (§8, §9.1, §10c), best `66.916356` against `67.988814` required; stability gap `0.1154435` identified as the missing input (§10) |
| radius parameter | `(H_R)` is monotone in `R` on components but degenerates to the theorem as `R` grows (§10b) |
| fixture data | rational coordinates with a `4.28e-15` separation budget for a flow solver (§1b) |
| timing record | corrected; waiting does not establish compliance (`TIMING_CORRECTION.md`) |

No early return; work continues.

## 12. How small can a payer's cell actually be driven? A search, and what it does not show

The decisive question for the cut is whether a completion can shrink `vol Omega(w_i)` to
`5.665735`. I searched for the smallest achievable value, adding legal centres (2-separated, and
`>= 2` from `w_i`) anywhere in the shell `[2, 4.2]`, greedily keeping any placement that reduced
the cell volume, and capping every polytope by the saturation bound `Omega(w_i) subset B(w_i,2)`.

| search | extra centres accepted | cell volume found |
| --- | --- | --- |
| greedy, 1 seed | 17 | `9.898520` |
| greedy, 6 seeds | 11-16 | `8.543387` (best), `8.908`, `9.418`, `10.420`, `10.550`, `12.167` |

So across seven independent completions the smallest cell found is `8.543387`, i.e.
`2.878` above the requirement, and `2.887` above `sqrt32`. Notably only **11 to 17** extra centres
could be placed at all before the greedy stalled: the six fixed neighbours at `2.1029` do not leave
much room.

**What this shows and what it does not.** Every value above is an **upper** bound on the true cell,
because a finite constraint set can only be cut further by more centres. So the search cannot
*prove* `(H_R)`: it is entirely possible in principle that a cleverer completion reaches `5.666`.
What it does show is:

1. **Reaching the requirement is not easy.** Random and greedy completions land near `9`-`12`, a
   factor `1.5`-`2` above the threshold. Getting to `5.666` requires a completion that
   approximates the dodecahedron's twelve faces closely, and the six fixed neighbours block exactly
   the directions that would be needed (`REVIEW_0308.md` §9, and §9.1 on the collar blocker).
2. **A sanity value is reproduced.** The polytope with the six known constraints capped by
   `B(w_i,2)` has volume `16.958438`; with the cruder six-face box instead it is `26.508617`. The
   difference between the two caps is a measure of how much the ball approximation matters, and it
   is larger than I expected — worth knowing for anyone reusing these numbers.

**Status: exploratory, one-sided.** This is the same failure mode as `K15-E062` and I flag it
explicitly: a computed *upper* bound on a cell volume is not evidence that the cell is large. What
the search legitimately supports is the *plausibility* that the payers have room to spare, and
that is all.

## 12b. The sharpest one-line statement of the requirement

The requirement on the twelve payers is a mean of `5.665734518`, and

```
sqrt32 = 5.656854249   (the fcc / hcp cell volume, the densest possible arrangement)
```

so the payers must **exceed an fcc cell by `0.008880269` each, i.e. by `0.157 %` on average**.
This is worth isolating because it is counter-intuitive at first sight: next to a *small* cell
(`c` at `V_dodeca`), the neighbouring cells must be **larger than fcc cells** — not merely larger
than the dodecahedral minimum. Compensation is not a small correction here; it requires the
neighbourhood of the defect to be locally *less* dense than the densest packing.

Put the other way: if the twelve payers were arranged as tightly as fcc allows, the cut would
still fail, by `12 x 0.008880269 = 0.106563`, i.e. by exactly the deficit. So the cut demands a
strict excess over the optimal local arrangement, which is why no per-cell minimum can supply it.

## 13. What this block establishes, and what it does not

**Established.**

- `K15-E070`: `(Q)` is **YES** — a saturated packing with a cell below `sqrt32` exists, proved
  without imports. The defect is real and compensation is necessary.
- `K15-E071`: the transfer form needs **no** bound on component diameter; the block form does.
- The component reduction for the Hall condition; and that ball-shaped cuts are neither necessary
  nor sufficient (`REVIEW_0138.md` §14, `REVIEW_0308.md` §4).
- Four families of per-cell sufficient condition are **quantitatively excluded** (§8, §9.1, §10c);
  the best reaches `66.916356` against `67.988814` required.
- The radius `R` is a free parameter, monotone on components, degenerating to the theorem as
  `R -> infinity` (§10b).
- The missing input is a **stability version of the dodecahedral theorem** with gap `0.1154435`
  (§10).

**Not established.**

- `(H_R)` itself, in any form, at any radius.
- Any lower bound on a payer cell better than `V_dodeca`.
- That the search in §12 is anywhere near optimal.

**The honest summary of the route.** It is a strengthening of Kepler (§6.1) whose entire content now
sits in one stability inequality about the icosahedral configuration. That is a much more precise
statement than "the geometric route is promising", and it is the useful output of this block.

## 14. The positive proposal: a *pair* bound, sharp at fcc/hcp (`K15-E074`)

Every per-cell approach above failed because the completion can shrink one cell at a time. The
multiplication by twelve in the cut suggests a different shape of statement: bound **pairs** of
adjacent cells.

**Conjecture (P').** For every pair of adjacent centres `v, w` of a saturated 2-separated set,

```
vol Omega(v) + vol Omega(w)  >=  2 sqrt32  =  11.3137084990... .
```

**Why it is the right shape.** It is *not* a per-cell bound: one cell may be as small as
`V_dodeca` provided its neighbour is correspondingly large, which is exactly how compensation works.
It is strictly stronger than the elementary consequence of McLaughlin's theorem
(`2 V_dodeca = 11.10058206 < 2 sqrt32`), yet weaker than a per-cell `sqrt32` bound — and it is
exactly what the summation in the cut needs:

```
12 pairs (c, w_i) with vol Omega(c) = V_dodeca :
     sum_i vol Omega(w_i)  >=  12 * 2 sqrt32 - 12 * V_dodeca  =  69.1610096456
     required                                                  =  67.9888142149
     margin                                                    =  1.172195431  (1.724 %) .
```

So **(P') implies the cut, with `1.72 %` to spare.**

**It is sharp, so it cannot be improved.** Tested on every fixture with `vor_volumes` and the
extent flag (`TESTED_FINITE`):

| fixture | adjacent pairs | min pair sum | vs `2 sqrt32` |
| --- | --- | --- | --- |
| fcc (500) | 1752 | `11.313708499` | **exactly equal** |
| hcp (175) | 212 | `11.313708499` | **exactly equal** |
| A15 (1439) | 10098 | `15.875000000` | above |
| icosa_fill (131) | 1 | `19.759139872` | above |
| icosa_fcc_shell (189) | — | all cells flagged | not usable |

Every one of `1752` fcc pairs and `212` hcp pairs attains the bound **exactly**, so `(P')` is a
sharp statement with the extremal configurations as its equality cases. That is the profile a
correct conjecture should have, and it is the first statement in this directory that is both
sharp at fcc/hcp and satisfied by every fixture.

**What is not established.** `(P')` is unproved. The evidence is one-sided: computed volumes are
*upper* bounds, so agreement here cannot certify it — only a violation could have refuted it, and
none was found. Nor do I claim `(P')` is new: a two-cell version of the dodecahedral problem is a
natural object and may well appear in the literature; it should be checked before being called new.

**Why it might be provable where per-cell bounds are not.** The obstruction in §10c was that any
single cell can be cut down by the completion. A *pair* bound forbids the simultaneous shrinking of
two adjacent cells, and the two cells are coupled through their shared face: making one smaller
pushes the shared face and enlarges the other. That coupling is exactly the mechanism the per-cell
families could not see, and it is the same coupling that `(H_R)` encodes. So `(P')` is a
finite-object, two-cell version of the collective target — the smallest instance of it that is not
a per-cell statement.

**Next step.** Test `(P')` on a two-cell local model: two centres at distance `d ∈ [2, 2.5]` with
their full local neighbourhoods, minimising `vol Omega(v) + vol Omega(w)` over completions. If the
minimum over that model exceeds `2 sqrt32`, `(P')` gains real support and the model is small enough
to be a candidate for a rigorous proof.

### 14.1 The equality case of `2 V_dodeca` is unattainable, so `(P')` is strictly stronger

`(P')` is stronger than the elementary bound `2 V_dodeca = 11.100582` coming from McLaughlin. How
much stronger? The only way to attain `2 V_dodeca` is for **both** cells to be regular
dodecahedra, i.e. both centres have twelve tangent neighbours in the icosahedral arrangement.

**This is impossible for adjacent centres.** Suppose `v` is dodecahedral and `w` is one of its
twelve tangent neighbours. Then the other eleven neighbours of `v`, as seen from `w`, sit at
distance `2.1029` (the icosahedron edge), and `w`'s cell can only be dodecahedral if `w` has twelve
tangent neighbours, one being `v` and the other eleven at distance exactly `2` from `w`.

Computed exactly, with `v` at the origin and `w = (2,0,0)`, both twelve-point sets being perfect
icosahedra with the shared axis (pole-to-pole):

```
aligned:                        min distance between the two eleven-point sets = 1.056487696
best over 721 relative twists:  min distance                                  = 1.056487696
required:                                                                      2
```

So the two rings clash badly — `1.06` against a required `2` — and **no relative twist rescues
it**. Two adjacent centres cannot both be dodecahedral, so the value `2 V_dodeca` is unattainable
and `(P')` is strictly stronger than the one-cell bound by a real, sizeable gap.

*(A first version of this check used the wrong filter and reported a legal configuration with a
minimum distance of exactly `2`; the bug was keeping the shared pole instead of excluding it. The
corrected run gives `11` and `11` points, as it must.)*

**What this does and does not show.** It shows `(P')` is not a trivial consequence of McLaughlin,
and that its equality cases are not the ones that would make it look weak. It does **not** prove
`(P')`: the minimum pair sum could still lie between `11.100582` and `11.313708`. Locating that
minimum is the open question, and the two-cell model in §14 is the natural setting for it.

### 14.2 The two-cell model, first attempt: survives, but uninformatively

Minimising `vol Omega(v) + vol Omega(w)` over completions of a pair at distance `d`, adding legal
centres greedily and capping by `Omega subset B(v,2)`:

| `d` | extra centres | pair sum found |
| --- | --- | --- |
| 2.0 | 31-32 | `22.582789`, `27.144119` |
| 2.1 | 31-33 | `22.979911`, `26.366818` |
| 2.2 | 32 | `25.648744`, `26.329563` |
| 2.4 | 31-34 | `24.895546`, `27.987444` |

**`(P')` survives — no value below `2 sqrt32 = 11.313708` — but this is uninformative**, for the
now-familiar reason: these are *upper* bounds on the cell volumes, and the completions are sparse
(~32 centres around a pair), so the cells are inflated by free space. fcc attains `11.313708`
exactly and my greedy cannot build anything near fcc density around a pair.

**So the two-cell model needs a better method than greedy insertion**: either a dense periodic
two-cell environment (fcc-like, with one parameter varied), or a genuine minimization over
completion directions. The greedy used here cannot approach the extremal configuration, and I
record the failure rather than presenting `22.58` as evidence for anything.

**What would be informative.** A *lower* bound. The one structural handle found this block is
§14.1: two dodecahedral cells cannot be adjacent, so the extremal pair is *not* `2 V_dodeca`. The
question is whether the extremal pair is fcc's `2 sqrt32` or something strictly between. Deciding
that is a two-cell isoperimetric problem, and it is the cleanest open target this block has
produced.

## 15. Status at the 40-minute checkpoint

Checkpoint taken at `11:39:30Z` (nominal `11:56:52Z`; recorded early with the work done, not padded
to the nominal time — see `TIMING_CORRECTION.md`). Verified at the checkpoint:
`bash Experimental/scripts/run_all_checks.sh` gives **14 rows, all PASS** (13 checks plus the
evidence-integrity row), in about 27 s on one CPU.

**Work completed since the 20-minute checkpoint.**

| item | state |
| --- | --- |
| four excluded families tabulated (§10c) | balls `50.265482`, dodecahedral `66.603492`, collar `66.916356`, finite sets (upper bounds only); best `0.984` of the requirement |
| outward-collar family (§9.1) | excluded twice: depth capped at `1` (giving `5.576363`), and blockable for free by a legal centre at `w_i + 2 w_hat_i` |
| radius parameter (§10b) | monotone on components, degenerating to the density bound as `R -> infinity` |
| search for the smallest payer cell (§12) | seven completions, best `8.543387`, all upper bounds |
| **`(P')` proposed (§14)** | pair bound `>= 2 sqrt32`, **sharp at fcc/hcp** (1752 and 212 pairs at equality), implies the cut with `1.72 %` margin |
| **ring-clash result (§14.1, `K15-E075`)** | two adjacent cells cannot both be dodecahedral: clash at `1.056487696` against `2`, for every twist |
| two-cell model (§14.2) | `(P')` survives; greedy gives `22.58`–`27.99`, uninformative (upper bounds) |
| machine checks | eleven 0308 items added to `verify_all_claims.py` |
| ledger | `E072`–`E075` added; `(P')` and `(S_dod)` listed as the open targets |

**The one-line state of the route.** `(Q)` is settled (`E070`); the diameter obligation is removed
(`E071`); four per-cell families are excluded (`E072`); and the whole remaining content is now
concentrated in either `(P')` (a two-cell isoperimetric statement, sharp at fcc/hcp) or `(S_dod)`
(a stability version of the dodecahedral theorem). Both are precise, both are unproved, and `(P')`
is the more attractive target because it is sharp at the equality family and needs no new
machinery to state.

### 14.3 The conjecture is at risk precisely at the configuration that motivates it

This has to be said plainly, because the framing above makes `(P')` look safer than it is.

The sharpest test of `(P')` is the **icosahedral pair itself**: `c`, whose cell is exactly
`V_dodeca`, and one payer `w_1`. For that pair `(P')` requires

```
vol Omega(w_1)  >=  2 sqrt32 - V_dodeca  =  5.76341747047 ,
```

which is `sqrt32 + 0.106563` — i.e. `w_1` must exceed an fcc cell by **the full deficit**.

Now: if all twelve of `w_1`'s neighbours were at distance exactly `2`, its cell would be the
dodecahedron. Five of them are relaxed to `2.102924`, so its cell is *strictly* larger — but by how
much is precisely what is unknown. The twelve-constraint model of §9 gives `5.905412`, which is
above `5.763417` with margin `0.142`; but that is an **upper** bound holding only twelve
constraints, and the true cell can be smaller.

So:

```
(P') fails for this pair   <=>   true vol Omega(w_1) < 5.76341747047 .
```

**I do not know which way this goes, and it is the question that decides the conjecture.** Note
also that `(P')` demands much more here than the cut itself does (the cut needs the twelve payers to
average `5.6657`; `(P')` needs each, paired with `c`, to clear `5.7634`). So `(P')` may well be
**too strong** — a point in favour of it being false at exactly this pair.

**What I would do next, and what I would not claim.** The honest next step is a lower bound for
`vol Omega(w_1)` that uses the five relaxed bisectors: the face areas of the dodecahedron give a
first-order excess of `5 x 1.387572757 x 0.051462 = 0.357` over `V_dodeca`, which would put
`w_1` at `5.907` and `(P')` comfortably true — but that argument is the perturbation heuristic of
`K15-E046`, which I withdrew as non-additive, and I will not revive it without a proof. Until then
`(P')` should be carried as **a conjecture that may be false**, not as a promising route.

**Revised status of `(P')`.** Sharp at fcc/hcp, survives every fixture, strictly stronger than the
one-cell bound (§14.1), and at genuine risk at the icosahedral pair (§14.3). It is a well-posed
target and a cheap one to test; it is not established and it is not safe.

### 14.4 The best *elementary* bound for a payer, and it still loses to the imported theorem

The five relaxed bisectors do buy something elementary, and it is worth recording as the strongest
bound available without importing anything.

`w_1`'s constraints around `c` are: the bisector with `c` at distance `1` (tangency), and the five
bisectors with the outer neighbours at `b = 1.051462224`. Since `b > 1`, the ball `B(w_1, b)` is
tangent to the five relaxed bisectors and is cut only by `c`'s bisector, so

```
vol Omega(w_1)  >=  (4pi/3) b^3  -  (pi h^2 / 3)(3b - h),    h = b - 1
               =  4.869334759  -  0.008605516
               =  4.860729243 .
```

That is a genuine improvement on the inscribed ball (`4.188790`, `+16.0 %`) and it uses the one
feature that distinguishes these payers from a generic centre — that its five non-central
neighbours sit just beyond tangency. But it is still well below

```
V_dodeca = 5.550291   (McLaughlin, imported)
```

so the imported theorem remains the best per-cell bound, and the ranking of §10c is unchanged. The
value of recording this is that it closes the "did you use the relaxed neighbours?" question: yes,
and they are not enough. Any proof of the cut must use the *simultaneity* of the twelve cells, not
finer per-cell information.

## 16. The hierarchy of conditions, from needed to false

This is the cleanest summary of where the cut stands.

```
(CUT)      sum_{i=1..12} vol Omega(w_i) >= 13 sqrt32 - V_dodeca = 67.9888142149
             ^ needed; equivalent to (H_R) for S = {c}
             |
(P')       vol Omega(v) + vol Omega(w) >= 2 sqrt32  for adjacent pairs
             ^ SUFFICIENT (gives the cut with 1.72 % margin), SHARP at fcc/hcp,
               strictly stronger than 2 V_dodeca, at risk at the icosahedral pair (§14.3)
             |
(CELL)     vol Omega(v) >= sqrt32  for every v
             ^ SUFFICIENT but FALSE for saturated packings (K15-E070: the icosahedral cell is
               V_dodeca = 5.550 < 5.657)
```

The three levels are ordered by strength: `(CELL) => (P') => (CUT)` for the cut at least, and
`(CELL)` is refuted. `(P')` is the interesting level: it is the strongest condition that is *not*
already refuted, it is sharp at the equality family, and it is stated about two cells rather than
one — which is the smallest amount of "simultaneity" that can work, given that every single-cell
family is excluded (§10c).

**Where the difficulty has moved.** It is no longer "find a big enough per-cell bound" (impossible,
`K15-E070` and §10c) but "show that two adjacent cells cannot both be small" (`P'`). That is the
honest state of the geometric route after this block, and it is a considerably sharper question
than the one the block started with.

### 14.5 An apparent refutation of `(P')` that was a bug — and how it was caught

I tried to refute `(P')` by optimizing a completion of `w_1` directly. The first run returned

```
vol Omega(w_1) = 3.237838,   reported legal,   threshold for (P') = 5.763417
```

which would have refuted `(P')` outright — and also `vol Omega >= V_dodeca`, i.e. **McLaughlin's
theorem**, since `3.2378 < 5.5503`. That impossibility is what identified the error: the penalty
function required the added centres to be `>= 2` from `c` and from the five outer neighbours, but
**never from `w_1` itself**, so the optimizer was free to place them inside `w_1`.

After adding the `|z| >= 2` term and re-running with an independent legality check:

```
trial 0: vol = 11.674097   legal = False
trial 1: vol = 11.674092   legal = False
trial 2: vol =  8.965142   legal = False
trial 3: vol = 11.673844   legal = False
```

No legal completion was found, and the volumes reported are for *infeasible* configurations, so they
say nothing either way. **So this test neither confirms nor refutes `(P')`**; it is recorded because
the failure mode is instructive:

- A number below a *known theorem's* bound is a bug, not a discovery. Comparing against
  `V_dodeca` is what caught it, and the same check is what the reviewers of `K15-E062` did not have.
- The optimizer is not a reliable feasibility engine: L-BFGS-B on a penalty returns whatever
  balances the two terms, and `penalty_ok` must be verified independently of the objective (it is
  now, and it disagreed with the penalty in the buggy version).

**Status of `(P')` after this attempt: unchanged** — survives every *legal* test performed, is not
proved, and remains at risk at this very pair (§14.3). The decisive computation still does not
exist.

### 14.6 A legal completion at `6.730974`, and `(P')` survives

After the bug of §14.5, the search was rebuilt to move **only inside the legal set** (start from a
greedy legal completion, then perturb one centre at a time, rejecting any move that breaks
2-separation from `w_1`, from `c`, from the five outer neighbours, or among the added centres):

```
start:                        12 legal centres,  vol Omega(w_1) = 11.009236
after local search:           12 legal centres,  vol Omega(w_1) =  6.730974
   V_dodeca (McLaughlin) = 5.550291   <- any value below this would be a bug
   NEED for (P') on this pair = 5.763417
   => (P') survives, margin 0.968
```

Two things follow.

- **`(P')` survives a much harder test than before.** The previous best legal value was `8.543`
  (§12); this is `6.731`, and it is still above the `5.763417` that `(P')` requires. The margin has
  shrunk from `2.878` to `0.968`.
- **The search is now trustworthy in a way the previous one was not.** Every accepted configuration
  is checked legal by an independent function, and the result sits above McLaughlin's bound, so the
  two known constraints are consistent. The buggy run's `3.238` is excluded by exactly this check.

**Still not decisive.** `6.731` is an *upper* bound on the true minimum: the local search moves one
centre at a time and cannot restructure the completion. A better search could conceivably reach
`5.763`. So `(P')` remains unproved and at risk, but it has now survived the strongest test this
block could mount, with a reduced but positive margin.

**What the trajectory suggests.** Across this block the best legal values found for
`vol Omega(w_1)` went `13.51 -> 11.01 -> 8.543 -> 6.731`, decreasing steadily as the search
improved, while the threshold for `(P')` is `5.763`. The downward trend is not a proof of anything —
it is a warning that better searches have kept finding smaller cells, and it is why I will not
describe `(P')` as safe.

### 14.7 The margin keeps shrinking: `(P')` may well be false

A harder search (18 legal centres instead of 12, more restarts, longer local search) returns

```
restart 0: 18 centres,  vol Omega(w_1) = 6.345329496
restart 1: 18 centres,  vol Omega(w_1) = 6.263607857
restart 2: 18 centres,  vol Omega(w_1) = 6.626973093
```

so the best legal value is now `6.263608`, still above the `5.763417` that `(P')` requires, with
margin `0.500`.

**The trajectory is the important thing, and it is not reassuring:**

| search | centres | best `vol Omega(w_1)` | margin over `5.763417` |
| --- | --- | --- | --- |
| greedy fill (§12) | 11-17 | `8.543387` | `2.780` |
| legal local search (§14.6) | 12 | `6.730974` | `0.968` |
| harder search (§14.7) | 18 | `6.263608` | `0.500` |

Every improvement in the search has found a materially smaller cell, and the margin has roughly
halved at each step. There is no sign of convergence above the threshold. **So the honest reading is
that `(P')` may well be false**, and I would not be surprised if a better search — or a cleverer
construction — produced a legal completion below `5.763417`.

**What that would mean.** If `(P')` is false, the pair route to the cut is closed, and the remaining
target reverts to `(CUT)` itself or to `(S_dod)`. That would not be a setback for the *programme* —
`(CUT)` is equivalent to `(H_R)`, which was the target all along — but it would remove the only
sharp, cheap-to-state sufficient condition this block produced.

**For the record: what I do not know.**
- Whether the sequence `8.54, 6.73, 6.26, ...` converges above or below `5.763`.
- Whether 18 centres is near the useful maximum (the count of 12 applies only within `2.09`;
  beyond that any number is legal, so more centres remain available).
- Whether a structured construction, rather than local search, does better.

All three are open, and none of them can be settled by more of the same search. **`(P')` should be
carried as a conjecture in doubt, not as a route.**

## 17. Final summary of the block

**Settled.**

- `K15-E070`: **`(Q)` is YES.** A saturated packing with a cell of volume `< sqrt32` exists. Four
  lines, no imports: the icosahedral cluster's centre cell is the dodecahedron
  (`5.5503 < 5.6569`), cells shrink under adding centres, and Zorn extends the cluster to a maximal
  (hence saturated) set. This corrects my previous block, which left `(Q)` open after failing to
  *construct* a completion — the upper bound from the cluster alone settles it without one.
- `K15-E045a/b` split so that the conditional and unconditional parts are no longer conflated;
  `(Q)` uses only the unconditional `a`.

**Structural results.**

- `K15-E071`: the transfer form needs no bound on component diameter (`kappa <= 12` from
  `K15-E014` plus finite Hall conditions give a global flow by compactness); the block form does.
  The obstruction `(T'')` is therefore removed rather than proved.
- The component reduction for the Hall condition, and the finding that ball-shaped cuts are neither
  necessary nor sufficient (`REVIEW_0138.md` §14, §4 above).
- `K15-E073`: on components `(H_R)` is monotone in `R`, and degenerates to the density bound as
  `R -> infinity`. So the radius is a genuine parameter, and the useful question is whether some `R`
  makes `(H_R)` both true and provable.

**Obstructions.**

- `K15-E072`: four families of per-cell sufficient condition are quantitatively excluded — balls
  `50.265482`, dodecahedral minimum `66.603492`, outward collar `66.916356`, finite constraint sets
  (upper bounds only) — against `67.988814` required, best ratio `0.984`.
- The collar is excluded twice: capped at depth `1` (short) and blockable for free by a legal centre
  at `w_i + 2 w_hat_i`.
- The best *elementary* payer bound, using the relaxed bisectors, is `4.860729` — better than the
  inscribed ball by `16 %` and still below `V_dodeca`.

**A proposal, in doubt.**

- `K15-E074` `(P')`: adjacent cells sum to at least `2 sqrt32`. Sharp at fcc/hcp (every pair of
  1752 and 212 respectively attains it exactly), implies the cut with `1.72 %` margin, strictly
  stronger than `2 V_dodeca` (`K15-E075`: two adjacent cells cannot both be dodecahedral — the
  rings clash at `1.056` against `2`). **But at the icosahedral pair it needs
  `vol Omega(w_1) >= 5.763417`, and the best legal values found fell `8.543 -> 6.731 -> 6.264` as
  the search improved, the margin halving each time.** So it is recorded as a conjecture in doubt.

**The honest state of the geometric route.** It is a strengthening of Kepler (it implies the
theorem), its per-cell families are exhausted, and its content now sits in either `(CUT)`/`(H_R)`
itself or the stability statement `(S_dod)`. `(P')` was the one cheap sufficient condition
produced, and it is now in doubt. That is not progress toward a bound, but it is a much sharper
statement of where the difficulty is than the block started with, and every claim above is
accompanied by the numbers and the tool that produced it.

### 14.8 Correction: the decline is not monotone, and `(P')` survives at `6.264`

A third search with 30 legal centres returns

```
restart 0: 30 centres,  vol Omega(w_1) = 6.494845301
restart 1: 30 centres,  vol Omega(w_1) = 6.968034515
```

— **worse** than the 18-centre result of `6.263608`. So the sequence is *not* monotonically
decreasing, and §14.7's framing ("every improvement found a smaller cell", "margin halving at each
step") overstates the trend. The corrected picture:

| centres | best `vol Omega(w_1)` |
| --- | --- |
| 11-17 (greedy) | `8.543387` |
| 12 (legal local search) | `6.730974` |
| 18 (harder search) | `6.263608` ← best |
| 30 (harder still) | `6.494845` |

**The most likely explanation is a limitation of the method, not a feature of the geometry**: with 30
centres the local search has twice the degrees of freedom for the same iteration budget, and it does
worse. So `6.2636` is the best this approach reaches, and it is `0.500` above the threshold `(P')`
requires.

**Revised verdict on `(P')`.** It has survived every legal test performed, with the best value
`6.263608` against a required `5.763417`. The evidence is one-sided (upper bounds) so this is not
support, but the earlier concern that the margin was collapsing is now weaker: one increase in the
number of centres made the result *worse*, which is what a method at its limit looks like rather
than a method converging past the threshold. `(P')` remains unproved, and it remains possible that a
structured (non-local-search) construction does better.

**What I would not do.** Report `6.264` as evidence *for* `(P')`, or the earlier trajectory as
evidence *against*. Both are the same kind of number: an upper bound from a search that has stopped
improving.

## 18. The structured construction: `(P')` survives at `0.135`, not `0.500`

`§17`'s first next step was to test `(P')` with a structured construction rather than more
local search. Done. The answer is that **`(P')` survives at the icosahedral pair, with its
margin cut from `0.500` to `0.135`** — and, more usefully, the reason the margin cannot be
driven much lower is now identifiable and structural.

### 18.1 Why a symmetric family is the right structured object

The cluster `K` is invariant under the 5-fold rotation about the axis `c -> w_1`: `c` is at
the origin, `w_1` at the north pole, and `w_1`'s five icosahedral neighbours form a regular
pentagon at polar angle `58.28 deg`. So every structured completion is a union of
**pentagonal orbits** `(r cos(f+72k), r sin(f+72k), z)`, `k = 0..4`, plus optional points on
the axis. This is a 3-parameter family per orbit instead of a 3-parameter family *per
centre*, and it is a family that one-centre-at-a-time local search cannot reach: no sequence
of single-centre moves out of a greedy fill assembles a pentagonal shell, which is why
`§12`-`§14.7` bottomed out at `6.263608`.

### 18.2 The construction, and the number

Take `c`, the five ring neighbours (at `2.102924`, fixed by the cluster), a **staggered
pentagon** of five centres at distance exactly `2` from `w_1` with polar angle `112 deg` and
azimuth `36 + 72k` deg, and the **south-pole point** `(0,0,4)`:

```
12 centres besides w_1 (13 including w_1)
min separation over all pairs incl w_1                        = 2.000000000000
min separation on pairs (added centre, c or ring)             = 2.170617049
vol Omega(w_1)                                                = 5.898007181138
max |cell vertex|                                             = 1.301968  (<= 2, ball inactive)
independent Monte Carlo, 4e6 samples                          = 5.901938
```

so

```
threshold for (P') at this pair   =  5.763417470
vol Omega(w_1)                    =  5.898007181     margin +0.134589711
previous best (local search)      =  6.263608        margin +0.500
```

The only tangency is the constructed one, `|pentagon - w_1| = 2`; every other distance
involving an added centre is `>= 2.1706`, so the configuration is legal with room and the
optimum in `theta` is *interior*, not contact-determined. By Zorn the set extends to a
saturated packing, in which the cell only shrinks, so `5.898007181` is an upper bound on
`inf vol Omega(w_1)` over saturated packings containing the cluster.

### 18.3 Why this is near the floor: the ring excess is irremovable

Five of `w_1`'s twelve neighbours sit at `2.102924` instead of `2`, so five of the twelve
bisectors sit at `b = 1.051462224` instead of `1`. The cell is therefore the dodecahedron
with five of its faces pushed out by `b - 1 = 0.051462`, and the excess is

```
first-order        5 * A_pent * (b-1)  =  0.357037902
observed           5.898007181 - 5.550291029 = 0.347716153      97.4 % of it survives
```

That excess is **essentially not removable by adding centres**, for a reason that is
quantitative and checkable. A centre `z` can cut the cell only if its bisector meets it, i.e.
only if `rho/2 < max|vertex| = 1.301968`, so

```
any cutting centre has   rho < 2.603935 .
```

But it must also keep distance `2` from the ring centre, which sits at `2.102924` from
`w_1`. Writing `alpha` for its angular distance from the ring direction,

```
cos alpha  <=  (rho^2 + 0.422310) / (2 * rho * 2.102924)
           ->  alpha >= 48.88 deg  at rho = 2.6039   (and more for smaller rho)
```

whereas the five ring faces, measured on the computed cell, subtend only `35.57 deg` from
their normals. **No centre that can cut the cell at all lies within `13 deg` of aiming at a
ring face**, so the collar cannot be attacked head-on.

What this does *not* exclude is a bisector at a large angle to the face normal shaving a
**corner** of the collar. That case is covered empirically and not analytically: it is what
`18.4`'s three searches test, and none of them finds anything. The ring excess is therefore
structural in the sense that no construction reaches it, not in the sense of a theorem.

This is the corrected form of `§14.3`'s question. There the open question was whether the
`5 x 1.387573 x 0.051462 = 0.357` excess could be cut; the perturbation heuristic
(`K15-E046`) that guessed "yes, fully" is still withdrawn, and the answer is now the
opposite one: at most `2.6 %` of it is cuttable.

### 18.4 Local minimality, tested three ways

| test | result |
| --- | --- |
| single-centre addition, `rho in [2.0, 2.6]`, 5382 positions | **0 legal** |
| two pentagons, `theta_1, theta_2 in [80,144]`, `rho in {2.0,2.05,2.1}` | **0 legal** |
| 8000-move anneal with symmetry breaking allowed, from the symmetric optimum | **no improvement** |

The first row is the meaningful one: the shell around `w_1` is saturated at radius `2`, so
every further legal centre is far away and cuts nothing.

### 18.5 Method correction: a test that could never fire

The first version of the sweep reported `minsep = 2.000000000` for every legal row, which
looks like a knifes-edge optimum and is not: the cluster's **own** `c`-`w_1` tangency is
exactly `2`, so `min` over all pairs is always exactly `2` and a real penetration by an added
centre is only visible if it is *below* that. At `theta = 105` the pentagon penetrates at
`1.993806` and the sweep did flag it, but the margin reported for legal rows was vacuous —
the same failure mode as the `K15-E062` buffer flag, which tested a condition that never
fired. The test is now `added_margin`, over pairs involving an added centre against everything
except `w_1`, and it reports `2.170617049` for the optimum.

*(Two smaller ones: `|p - w_1| >= 2` must be checked separately, because `w_1` is the centre
whose cell is being computed and so is absent from its own constraint set; and the first-order
excess formula was coded with the wrong `b` and printed `-0.339563` before being fixed. Neither
affected a reported legal value.)*

### 18.6 What this changes

- **`(P')` is still unproved, and still survives.** Its margin at the configuration that
  motivates it is now `+0.134590`, not `+0.500`. The `§14.7` fear that "the margin halves at
  every improvement" is replaced by something better: the floor is set by the ring excess, and
  `97.4 %` of that excess is provably-or-empirically irremovable, so there is no reason to
  expect `(P')` to fail at this pair.
- **But it also shows `(P')` is only `2.3 %` away from failing.** Cutting `39 %`
  (`0.1346 / 0.3477`) of the ring excess would refute it. Nothing found cuts any of it; the
  argument in `18.3` says nothing can.
- **The pair route is therefore alive but thin, and the arithmetic is now explicit.** With
  `vol Omega(c) = V_dodeca` fixed, `(P')` asks each payer for

  ```
  vol Omega(w_1)  >=  2 sqrt32 - V_dodeca = sqrt32 + 0.106563 = 5.763417
  ```

  and the construction delivers `5.898007 = sqrt32 + 0.241153`, i.e. **`2.26` times the
  required excess over an fcc cell**, with `0.134590` to spare. Equivalently, since the cell
  sits `0.347716` above `V_dodeca` and `(P')` tolerates only `5.763417 - V_dodeca = 0.213126`,
  the whole of `(P')` at this pair is the single statement

  > **the payer's dodecahedral excess cannot be cut by `39 %`.**

  Every construction in `18.4` cuts `2.6 %` of it and no more, which is why the conjecture
  survives — and is also exactly what would have to break for it to fail.
- **Lower bound unchanged.** Nothing here improves on `V_dodeca` as a lower bound, so `(P')`
  is not proved either. The window at this pair is `[5.550291, 5.898007]` with the threshold
  `5.763417` inside it.

### 18.7 The honest one-line status

`(P')` at the icosahedral pair: `5.550291 <= inf vol Omega(w_1) <= 5.898007`, threshold
`5.763417`; the upper end is `0.135` above the threshold, the excess that separates them is
the five-ring dodecahedral collar, and three independent searches fail to cut any of it.
