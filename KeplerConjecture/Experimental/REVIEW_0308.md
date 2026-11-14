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
ten remaining... sorry, on the twelve payer cells that exceeds `V_dodeca` in total by
`1.385321873`, using the actual neighbour data — which for a payer is: one neighbour at exactly
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
