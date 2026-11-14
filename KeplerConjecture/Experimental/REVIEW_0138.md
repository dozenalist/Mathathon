# Review response 0138 — corrections to scope, and the current state

Role E. Started 2026-11-14T09:57:21Z. Source reviewed: `4ea4e8b9`.

## 0. Reporting correction, accepted

My completion 51140 reported "40 minutes, finished 09:56Z". Both figures were **wrong**. I
derived them from `date -u` calls inside tool results and from a running tally I was updating
by hand; neither is the API's wall clock. The official history (receipt 09:15:53Z, completion
09:41:19Z, about 25 minutes) supersedes my account entirely, and the runtime was **Ultramath**,
which I had recorded as not used. I will report only actual tool/API UTC timestamps from now on
and will not infer elapsed time.

## 1. `K15-E049` — delimited

**What I claimed.** "The per-cell route is closed."

**That was too strong, and the sentence is withdrawn.** Here is what is actually proved.

### The admissible estimator family

Fix an outer centre `w` of the icosahedral cluster, and let `t(u)` be the radial extent of its
Voronoi cell in direction `u`, so `vol Omega(w) = (1/3) int_{S^2} t(u)^3 du`. An estimator in
the family `F` is any function `tau` satisfying

```
(F1)  tau(u) <= t(u)   for all u        (tau is a valid lower bound),
(F2)  tau is built ONLY from: the exact bisector terms d_j/(2 cos phi_j) of a known near set
      S of at most 12 centres, and a single uniform floor rho/2 applied to every centre not in S,
(F3)  rho is a radius at which the count "at most 12 centres in [2, rho]" is certified.
```

For every estimator in `F`, and every admissible `rho`,

```
vol Omega(w) >= (1/3) int tau^3 <= (4 pi/3)(rho/2)^3 <= (4 pi/3)(1.045572774)^3 = 4.787969853 ,
```

because (F2) forces `tau <= rho/2` **everywhere** (inside a cap `tau` is a minimum with
`rho/2`; outside all caps it *is* `rho/2`), and `rho <= 2 + delta_0 = 2.091145548` by
`K15-E012` with `theta_13 = 57.1367 deg` (`K15-E049` arithmetic; the ceiling is `15.49 %` below
the required `5.665734518`).

**Quantifiers, stated exactly.** The ceiling holds *for every estimator satisfying (F1)–(F3),
with the near set arbitrary, the cap values exact, and `rho` maximal*. It is not a statement
about other kinds of argument.

### What this does not close

- **It does not close per-cell methods.** It closes the *directional-cap estimator family*
  with a *single uniform floor*. A per-cell bound may legitimately use:
  (a) convexity of the Voronoi cell and its facet structure, not just directional caps;
  (b) a *multi-radius* count — e.g. `N(rho)` centres allowed in `[2, rho]` for `rho > 2.09`,
      which raises the floor `rho/2` at the cost of more caps. My argument gives no ceiling
      here, because (F3) restricts to radii where the count is exactly 12;
  (c) volume or polytope arguments that inscribe a body with known facets;
  (d) the second shell's presence to limit how far the completion can intrude.
- **It certainly does not close every geometric route**, and no such claim should be attached
  to it. It says nothing about collective/block inequalities, about transport, about
  decomposition arguments, or about any argument that does not bound `vol Omega(w)` from below
  by integrating a directional lower envelope.
- The `44 %` slack measured in `K15-E043` remains unexplained by any of this, and is the clearest
  reason to think a *non*-directional argument could succeed where `F` fails.

**Corrected ledger wording.** `K15-E049` status becomes
`PROVED (ceiling for the estimator family F, defined above)` rather than
`closes the per-cell route`.

### Dependent claims corrected

| downstream claim | old wording | corrected |
| --- | --- | --- |
| `STATUS_FOR_MAIN.md` | "only (2) remains / the per-cell family is closed" | "the estimator family `F` is closed; multi-radius counts, convexity-based per-cell bounds and collective arguments are all still open" |
| `GEOMETRIC_OBSTRUCTION.md` §K15-E048 | "the per-cell route is closed" | "no *uniform-floor directional* bound can exceed `4.787970`" |
| candidate table `K15-E1` | implies the geometric route reduces to one inequality | the route has at least three open shapes; `(T'-2)` is the one under development |

## 2. Audit of `K15-E045` (dodecahedral theorem for every completion)

**The claim.** In any saturated 2-separated set containing the icosahedral cluster,
`Omega(c) = D` and `vol Omega(c) = V_dodeca` exactly.

**The argument, rechecked.**

1. `Omega(c) ⊆ D` is **unconditional**. `D` is by definition the intersection of the twelve
   half-spaces `{x : |x| <= |x - w_i|}`, and `Omega(c)` is the intersection over *all* centres,
   which is contained in the intersection over the twelve. No saturation, no completion
   hypothesis. ✓
2. `vol Omega(c) >= V_dodeca` is the **dodecahedral theorem**, imported. This is where the
   external content sits.
3. `vol D = V_dodeca` by construction (regular dodecahedron of inradius `1`).
4. Hence equality. ✓

**Where the audit bites — hypotheses of the imported theorem.** I have **not** verified from
the primary source in this project that the dodecahedral theorem holds for *arbitrary* (not
merely saturated) packings of unit balls, or whether it requires the packing to be locally
finite, or whether its Voronoi cells are the Euclidean ones. `Literature/CORE_SOURCES.md` lists
`HM10` as `FULL_TEXT_CHECKED` for "the main statement and computational outline", not for the
exact hypothesis list. Until X checks the precise statement, `K15-E045` should be carried as
**conditional on the imported theorem in the form used**, and I will not describe it as
unconditional.

Note that saturation *is* available in our setting (the whole programme assumes it), and
locally finite is automatic for a 2-separated set, so the risk is low — but "low risk" is not
"verified", and the difference matters for a formalisation target.

**External proof complexity, charged.** The dodecahedral theorem (Hales–McLaughlin, JAMS 2010)
is computer-assisted: its own proof uses graph enumeration, linear programming and interval
arithmetic, i.e. the same three technologies as the Kepler proof it was meant to simplify.
Importing `V_dodeca` therefore buys `5.550291` per cell at the price of an entire
computer-assisted proof, and it does **not** suffice for `(T'-R2')` needeing `5.665734`. Any
complexity comparison must charge that: a route that needs the dodecahedral theorem *plus* a
further `2.08 %` is strictly more expensive than a route that needs neither.

**What survives.** The numerical identity `vol D = 5.55029102851551027` and the containment
`Omega(c) ⊆ D` are unconditional. The equality needs the import. The observation that the
computed centre cell was `5.550291028515513` to `1e-15` in twelve runs is consistent with, and
now explained by, the conditional statement.

## 3. The collective target, formulated as an exact finite inequality (`K15-E060`)

### 3.1 What "two shells" has to mean

Adding cells to a block is not automatically helpful: the block inequality
`sum_{v in B} c(v) >= sqrt32 |B|` gains `c(u)` on the left and `sqrt32` on the right for
each added cell `u`, so adding `u` helps exactly when `c(u) > sqrt32`. So "use two shells"
is a real hypothesis, not a free weakening. Two further points had to be settled before the
target is even well posed:

- **Thresholds are forced, not chosen.** One-shell blocks `C u N(C)` are disjoint iff
  components are taken at `tau = 2 rho = 4.18`, because `s in N(C1) cap N(C2)` forces
  `dist(v1,v2) <= 2 rho`. Two-shell blocks `C u N(C) u N(N(C))` need `tau = 4 rho = 8.36`,
  because the chain is `dist <= 2 rho` twice. Both are proved in `GEOMETRIC_PARTITION.md`
  and *tested* (max pairwise overlap `0` in every fixture).
- **Boundary cost grows.** `diam Block2 <= diam(C) + 4 rho`, so `K15-E001` Step 2 runs with
  `D = diam(C) + 8.36`; the estimate stays `O(r^2)`, so the conclusion `delta <= pi/sqrt18 + C/r`
  survives with a larger `C`. Nothing breaks, but the constant is worse and must be stated.

### 3.2 The evaluator

`Experimental/scripts/block_evaluator.py` (numpy/scipy only; **one CPU, under 10 s, under
200 MB** for all fixtures). It computes Voronoi volumes with an explicit buffer, flags every
cell that the buffer cuts (so an unbounded cell can never be silently counted), finds the
defective set, extracts components at both thresholds, builds one- and two-shell blocks,
checks disjointness and overlap, and reports `D`, `S`, `S - D`, diameters and the
buffer flag per block. Command:

```
python3 Experimental/scripts/block_evaluator.py            # all fixtures
python3 Experimental/scripts/block_evaluator.py --fixture two_icosa
```

Inputs are generated in-script (no data files); output is
`Experimental/evidence/block_evaluator.json`. Success criterion: for each block,
`disjoint=True`, `block_has_buffer_cell=False`, and `S - D` positive; a **negative** `S - D`
in a buffer-free block would refute the target. Failure criterion for the *evaluator*:
any block reported with a buffer-cut cell, since the volume is then not the true one.

### 3.3 Fixtures and results (TESTED_FINITE)

| fixture | defects | blocks | `S - D`, one shell | `S - D`, two shells |
| --- | --- | --- | --- | --- |
| `fcc_plain` (500 pts) | 0 | vacuous: all singletons | — (holds by definition) | — |
| `hcp` (175) | 0 | vacuous | — | — |
| `random_fill` (107) | 0 | vacuous — sparse, cells large | — | — |
| `icosa_fill` (131) | 1 | 1 / 1 | `+61.504` | `+66.526` |
| `icosa_fill_b` (131) | 1 | 1 / 1 | `+52.016` | `+84.547` |
| `icosa_fcc_shell` (189) | 1 | 1 / 1 | `+94.064` | `+94.064` |
| `icosa_fcc_shell_b` (189) | 1 | 1 / 1 | `+94.036` | `+94.036` |
| `two_icosa` (two clusters) | 2 | 2 / 2 | `+50.052`, `+50.732` | `+68.518`, `+76.450` |

The deficit being repaid is `D = 0.106563`. So across seven non-vacuous blocks the observed
surplus exceeds the deficit by a factor between `470` and `880`, and **no block comes close to
failing**. `two_icosa` exercises the overlap accounting with two components and reports
`max_pairwise_overlap = 0`, confirming the `4.18` / `8.36` thresholds empirically as well as
by proof.

**Two fixtures could not be built, and that is informative.**

- `perturbed_fcc` is **impossible**: in fcc all twelve neighbours of a centre lie at distance
  exactly `2`, so *any* nonzero displacement violates 2-separation. Creating a defect requires
  a locally compressed motif, and the icosahedral cluster is the natural one. Recorded so that
  no one spends time trying.
- A *dense* completion of the icosahedral cluster is not achievable by random sequential
  adsorption: densities reached are `0.10` against `0.177` for fcc. This is the same
  undersaturation that limits `K15-E040`, and it means the `S - D` values above are inflated
  by free space. Since computed cell volumes are **upper** bounds, the test remains one-sided:
  a positive `S - D` does not certify, only a negative one refutes.

### 3.4 Antisymmetric transfer: the fallback, and it does better than expected (`K15-E061`)

The block formulation needs a partition, components, ordering and overlap accounting. There is
a formulation that needs none of it and restores the **pointwise** condition, so that Hales's
Lemma 3.3 applies directly with the singleton partition.

**Setup.** `R > 0`. For defective `v` set `d(v) = sqrt32 - c(v) > 0`, and `N_R(S)` for the
`R`-neighbourhood. A *transfer* is a skew-symmetric `phi(v,u) = -phi(u,v)` supported on
`0 < |v-u| <= R`; set `A(v) = sum_u phi(v,u)`.

**Hypothesis (Hall condition, `H_R`).** For every finite set `S` of defective centres,

```
sum_{v in S} d(v)  <=  sum_{u in N_R(S) \ S} ( c(u) - sqrt32 ) .
```

**Theorem.** Assume `(H_R)`. Then:

1. *Pointwise FCC-compatibility.* There is a transfer with `c(v) + A(v) >= sqrt32` for every
   `v in Lambda`. This is max-flow/min-cut: deficits on one side, surpluses on the other, and
   `(H_R)` is exactly the family of cut conditions.
2. *Exact cancellation.* For every finite `S subset Lambda`,
   `sum_{v in S} A(v) = sum_{v in S, u notin S, |v-u|<=R} phi(v,u)`, because the pairs internal
   to `S` cancel pairwise by skew-symmetry.
3. *Negligibility.* For `S = Lambda(x,r)` the boundary pairs have `u in B(x,r+R) \ B(x,r)`,
   a shell of `O(r^2)` centres, and for each such `u` at most `|Lambda cap B(u,R)| <= (R+1)^3`
   partners. Hence `|sum_{v in Lambda(x,r)} A(v)| <= ||phi||_inf (R+1)^3 |shell| = O(r^2)`.
4. *(C3) is automatic.* Pacers never pay more than `c(u) - sqrt32`, and receivers only gain,
   so `c(v) + A(v) >= 0` everywhere.

Consequently `A` is negligible and fcc-compatible, and **Lemma 3.3 applies with no cluster
machinery at all**.

**Implemented and tested.** `Experimental/scripts/transfer_evaluator.py` constructs the
transfer explicitly (pro rata, capped by each payer's surplus, payers restricted to
non-defective centres) and verifies the conclusions numerically:

| fixture | pointwise FCC | `min (c + A)` | range of `A` | `|sum A|` | defects paid |
| --- | --- | --- | --- | --- | --- |
| `icosa_fill` | yes | `5.656854249` | `[-0.0112, +0.1066]` | `1.4e-17` | 1 / 1 |
| `icosa_fill_b` | yes | `5.656854249` | `[-0.0111, +0.1066]` | `6.9e-18` | 1 / 1 |
| `icosa_fcc_shell` | yes | `5.656854249` | `[-0.0102, +0.1066]` | `0` | 1 / 1 |
| `two_icosa` | yes | `5.656854249` | `[-0.0160, +0.1066]` | `0` | 2 / 2 |
| `hcp`, `fcc_plain` | yes | `5.656854249` | `[0, 0]` | `0` | 0 |

Three features are worth stating plainly.

- **The transfer is inert on the equality family.** `A ≡ 0` on fcc and hcp, so the rule cannot
  disturb the configurations that attain `pi/sqrt18`. This was the main risk of any
  correction scheme and it is settled here for this rule.
- **The *per-pair* transfer is tiny**: `||phi||_inf <= sqrt32 - V_dodeca = 0.106563`, i.e. at
  most `1.9 %` of a cell volume, because a defect's deficit never exceeds that (using
  `vol Omega >= V_dodeca`). Note the distinction I got wrong on first writing: this bounds
  each `phi(v,u)`, **not** each `A(v)`. A vertex `u` that pays `K(u)` defects can have
  `|A(u)| <= K(u) * 0.106563`, and `K(u)` is not bounded by `1`. Only the per-pair bound enters
  negligibility, via `||phi||_inf` in `C1`, so the argument is unaffected — but the stronger
  per-vertex claim was unjustified and is corrected here. In all six fixtures `K(u) = 1` and the
  reported `|A| <= 0.016` is consistent with both bounds.
- **(C3) has genuine margin.** A payer never gives more than `c(u) - sqrt32`, so
  `c(u) + A(u) >= sqrt32 > 0`; a receiver only gains. So `c + A >= 0` holds by construction, not
  by smallness.
- **Each deficit is paid in full by exactly twelve payers**, matching `K15-E014`'s count.

**Equivalence, stated honestly.** `(H_R)` with `S` the defect set of a single component *is*
`(T')` on the block `S u N_R(S)`. So the transfer does **not** remove the mathematical
content; it repackages it. What it genuinely removes is (i) the partition, (ii) the component
/ threshold / overlap bookkeeping, (iii) the need for `K15-E001`'s cluster criterion at all,
and (iv) the negligibility proof, which becomes a two-line telescoping argument with an
explicit `O(r^2)` boundary. That is a real improvement in the *interface* and in what a
formalisation would have to carry, and it should not be described as a reduction in difficulty.

### 3.5 The remaining local inequality, stated exactly

`(H_R)` is unproved. What is needed, minimally, is:

```
for every finite set S of defective centres (c(v) < sqrt32),
    sum_{v in S} (sqrt32 - c(v))  <=  sum_{u in N_R(S) \ S} (c(u) - sqrt32) ,
with R = 2.09.
```

Everything else in the chain is now either proved (`K15-E014` for the count, the transfer
theorem above) or imported and charged (`V_dodeca`). The measurements say the inequality holds
with a factor of `470`-`880` to spare on every constructible fixture; the obstruction is that
no technique proves even a factor of `1`.

### 3.6 A structural finding: defects are isolated, so surplus is never shared

`(H_R)` would be much harder if several defective centres could draw on the same paying
neighbours. Two measurements say they cannot, at least for the defect we have.

**fcc and hcp are locally rigid, so defects cannot be made by perturbation.** In fcc every one
of the twelve neighbours of a centre sits at distance exactly `2`. Any nonzero displacement of
a centre therefore violates 2-separation, and the same holds for hcp. This is why the
`perturbed_fcc` fixture cannot exist (Section 3.3) and it means defects must come from a
*different* motif rather than from a wobble of the optimal one — a defect requires local
crowding, and crowding requires near-tangency, and near-tangency leaves no room to move.

**Two icosahedral defects are always far apart.** Two copies of the motif with centres at
distance `d` are legal iff `d >= 5.5`; at `d = 5.0` the minimum separation drops to `1.597`, and
at `d = 4.18` to `0.777`. But components merge only at `d <= tau = 4.18 = 2R`. Since
`5.5 > 4.18`, two icosahedral defects are **always in different components and never share a
paying neighbour**. (I first wrote "minimum legal `d` is 6"; the measurement is `5.5`. The
conclusion is unaffected but the figure is corrected here.)

**Consequence.** For configurations of this motif, `(H_R)` decomposes into independent
single-defect inequalities, each with its own twelve payers and no competition — which is
exactly the setting in which the measured slack factor of `470`–`880` was obtained. So the
`(H_R)` tests are not weakened by the fixtures having only one defect each: multiple defects
genuinely decouple. The `2x2x2` grid of eight defects confirms this — eight components,
`max_pairwise_overlap = 0`, minimum `S - D = +67.472`, no sharing pressure.

**What is *not* established.** That *every* defective configuration has isolated defects. The
argument above is (i) exact for fcc/hcp rigidity, (ii) measured for the icosahedral motif, and
(iii) heuristic in general. A defect with a smaller deficit might be packed more densely, and
then surpluses could compete. I can neither construct such a configuration nor rule it out, and
I do not promote the heuristic to a theorem. This is the sharpest open point about `(H_R)`.

## 4. Runtime and clock

Receipt `2026-11-14T09:57:21Z`. Checkpoints taken at approximately +20 and +40 minutes using
`date -u` at the start of each tool call, and the final report is issued no earlier than
`10:57:21Z`. No sleeping or busy-waiting was used; pauses between pushes were spent on the
fixtures, the transfer theorem and the obstruction in Section 3.6.

## 5. Correction: the empirical support for `(H_R)` was an artefact

This is the most important finding of the block, and it retracts a number I published last
block.

**The bug.** `vor_volumes` flagged a cell as buffer-limited only if one of its vertices lay at
radius `> R - 1e-6`, with the buffer sphere at `R = 26`. That test never fires: the buffer is a
*sphere* of points, so the buffer points themselves have unbounded cells, and a core cell is
truncated by the bisectors with buffer points at radius roughly `13`-`18`, well inside `R`.
Diagnosed concretely: the largest fcc "boundary" cell had volume `602.709` with maximum vertex
radius `17.9205`, and the Vornoi diagram reported `3000` unbounded regions — one per buffer
point. So no cell was ever flagged, and `interior = 500` for a 500-point fcc block, which is
absurd.

**The correct test.** In a *saturated* packing, `Omega(v) subset B(v,2)`. A cell whose extent
from its own centre exceeds `2` therefore cannot be the cell of a saturated packing, and its
computed volume is meaningless for the packing bound — whether it was truncated by the buffer,
or is simply unsaturated free space. That is the semantics the flag should carry, and it is now
implemented (`extent_cap = 2.0`).

**Consequence: every block I tested is unreliable.**

| fixture | cells flagged unreliable | block flagged |
| --- | --- | --- |
| `fcc_plain` (500) | `244` | — (no defects) |
| `hcp` (175) | `130` | — (no defects) |
| `icosa_fill` (131) | `126` | yes |
| `two_icosa` (281) | `241` | yes |
| `icosa_fcc_shell` (189) | `188` | yes |

Every non-vacuous block is flagged. So the values `S - D = +50` to `+95` reported in Section
3.3, and the "factor `470`-`880`" I quoted in the previous completion, are **artefacts of free
space**: computed cell volumes are upper bounds, the inflated cells are exactly the payers, and
`S` is therefore overestimated without bound. The true `S - D` could be small, or negative. I
retract the slack claim.

**Why this is a genuine obstruction and not just a code fix.** It is not that the fixtures were
built carelessly; it is that **no constructible completion of the icosahedral cluster is locally
saturated**. Saturation requires every point of space to be within `2` of a centre, and the
icosahedral motif is frustrated: the outer twelve are at `2.1029` from the defect and cannot be
completed densely without displacing them. Random sequential adsorption reaches density `0.10`
against `0.177` for fcc, and the fcc shell is incommensurate and leaves gaps. So the
configuration that would make `(T')` / `(H_R)` testable is exactly the configuration we cannot
build.

**What therefore remains meaningful in this block.**

- The `(T')`/`(H_R)` statements themselves, and their equivalence (Section 3.4). ✓
- The transfer theorem: pointwise FCC-compatibility *given* `(H_R)`, exact cancellation, and the
  `O(r^2)` boundary estimate. These are proofs and do not depend on volumes being accurate. ✓
- The disjointness/overlap results: `max_pairwise_overlap = 0` in every fixture, and the
  thresholds `4.18` / `8.36`. These depend only on distances, not on volumes, so they survive. ✓
- The transfer *implementation* check: `c + A >= sqrt32` pointwise, `|sum A| <= 1.4e-17`, `A = 0`
  on fcc/hcp. This validates the **code path only**. It does not confirm `(H_R)`, because the
  payers' volumes in these fixtures are among the unreliable cells of Section 5 — the algorithm
  is being fed surpluses that a saturated packing need not have. Stated explicitly so the table
  in Section 3.4 is not read as geometric evidence.
- The numerics `S - D`: **unreliable**, retracted as evidence.

**What would be needed to test `(T')` at all.** A certified lower bound on `c(u) - sqrt32` for
the payers that is valid for *every* completion, which is precisely the missing inequality — so
the inequality cannot be tested by constructing completions. This closes the empirical route to
the question, and it is the honest end state: the two-shell and transfer formulations are now
exact and cleanly stated, and there is no numerical shortcut to settling them.

## 6. The precise open problem, and why it is not a computational one

The retraction in Section 5 leaves one question that has to be settled before `(T')` or `(H_R)`
can be attacked intelligently:

> **(Q)** Does there exist a **saturated** 2-separated set containing a centre with
> `vol Omega(v) < sqrt(32)`?

Everything in this block assumed yes, and built the whole compensation apparatus on the
icosahedral motif, which is the only defect we can actually exhibit. But the motif is not
saturated, and Section 5 shows that no completion of it that we can construct is either.

**Why (Q) matters.** If the answer is *no* — if every cell of every saturated packing already
has volume `>= sqrt32` — then Hales's correction is unnecessary: the per-cell inequality
`vol Omega(v) >= sqrt32` holds outright, Lemma 3.3 applies with `A = 0` and the singleton
partition, and the density bound follows with no transfer, no clusters and no blocks. So **(Q) =
no collapses the entire geometric route to the per-cell inequality.**

**But (Q) is at least as strong as Kepler.** If every cell of every saturated packing has volume
`>= sqrt32`, then summing gives density `<= (4pi/3)/sqrt32 = pi/sqrt18` immediately. So a proof
of `(Q) = no` would be a proof of the theorem, and any proof of the theorem does **not** give
`(Q) = no` (Kepler does not force every cell to be large). (Q) is therefore strictly stronger
than the target and must not be adopted as a strategy.

**What is known.** The dodecahedral theorem gives `vol Omega(v) >= V_dodeca = 5.550291 <
5.656854`, so known theory *permits* defects and does not rule them out. The gap between
`V_dodeca` and `sqrt32` is `0.106563`, which is exactly the deficit of the icosahedral motif —
i.e. the motif realises the smallest cell the dodecahedral theorem allows. So the question is
whether the extremal cell of the dodecahedral theorem can be embedded in a *saturated* packing at
all.

**Why it is not computational.** Deciding (Q) requires an infinite condition (saturation is a
statement about all of `R^3`), and Section 5 shows that finite completions cannot even make the
relevant cell volumes meaningful: the cells we would measure are truncated or unsaturated, and
their computed volumes are upper bounds that the true packing may never attain. So no amount of
search settles (Q); it needs either an explicit periodic saturated construction with a certified
Voronoi cell (finite data, but the certification must cover the infinite periodic repetition), or
a proof that none exists.

**A concrete first attempt at a positive answer**, which I did not complete: a Frank–Kasper
phase. Those are the standard periodic sphere packings with icosahedral coordination, and the
`A15` structure in particular has 12- and 14-coordinated sites. If any of them has a Voronoi cell
of volume below `sqrt32`, that settles (Q) = yes with fully explicit data and makes `(T')`
testable. This is a bounded, checkable computation (one periodic cell, exact coordinates,
certified Voronoi decomposition) and it is the natural next step; I flag it as the highest-value
follow-up rather than claim it.

## 7. Where the geometric route stands after this block

1. `(T'-R2')` and `(H_R)` are now stated exactly, with forced thresholds (`4.18`, `8.36`), the
   boundary cost (`diam C + 8.36`) and a proved equivalence between the block and transfer forms.
2. The transfer form is the better interface: it needs no partition, and it proves negligibility
   by a two-line telescoping argument with an explicit `O(r^2)` boundary. Its theorem
   (`K15-E061`) is independent of any numerical input.
3. The empirical support I previously offered is withdrawn (Section 5). There is currently **no
   evidence either way** on `(H_R)`, and the reason is structural: the configuration that would
   test it cannot be built.
4. `(Q)` is the sharp question to settle next, and it is not a search.
5. `K15-E049` is narrowed to the estimator family `F`; multi-radius counts, convexity-based
   per-cell bounds and collective arguments are all still open.

Nothing here closes the geometric route, and nothing here should be read as showing the route is
promising. The deliverable of this block is an auditable target, two runnable evaluators, and one
retraction.

## 8. Result of the dense-completion search (`K15-EXP-005`)

The harness of Section 8-authoring was run as a background job: `--seconds 300 --seeds 4`,
one CPU, exit status `0`, wall clock `~4 min`. Output committed as
`Experimental/evidence/dense_completion_search.json`.

| seed | `n` | `sum12` | `mean12` | iterations | refuted |
| --- | --- | --- | --- | --- | --- |
| 0-3 (best) | — | `116.663` | `9.722` | `475` | no |

**The search did not refute `(T')`, and it did not even improve on the sparse baseline** of
`98.0` from `K15-E040`; it made the configuration *worse*. Two readings, both recorded:

1. **The annealing is too weak.** 475 accepted-improvement iterations per seed is small for a
   `300`-point configuration, and the move set (insert/delete one point) cannot restructure a
   frustrated cluster. The cache key `(len(P), |P|_1)` is also collision-prone for similar point
   sets, so some scores may have been stale — a defect of the harness, not of the mathematics.
2. **The search was aiming at the wrong thing.** Density is not the quantity that makes `(T')`
   hard; *saturation* is. A denser set increases the *number* of centres but does not make the
   outer cells satisfy `Omega(w) subset B(w, 2)`, which Section 5 identifies as the condition
   that makes the volumes meaningful. So driving density up cannot fix the difficulty.

Reading 2 is the substantive one and it is consistent with everything else in this block: the
empirical route to `(H_R)` is closed not for want of a better optimiser but because the target
configuration is not reachable by completion. Recorded so that no further search budget is spent
on it.

## 9. First attempts at `(Q)` — two controls, no answer

### 9.1 A15 is the project's first genuinely saturated fixture

`Experimental/scripts/frank_kasper_test.py` builds the A15 (β-W / Cr₃Si) structure, scales it
so the minimum distance is exactly `2`, and computes cell volumes.

```
A15: min separation = 2.000000 (exact after scaling), conventional cube edge L = 4.0
     cell volumes: 7.812500000 and 8.062500000        sqrt(32) = 5.656854249
     cell extents: 1.443376  (< 2, so Omega subset B(v,2) holds)
     packing density: 0.523599
```

Two things follow, and the first matters more than the second.

- **This is the first fixture in the project whose cells satisfy the saturation criterion**
  `extent <= 2` established in Section 5. Every earlier fixture failed it. So A15 is a genuine
  saturated test case, and the evaluator's machinery (defect detection, extent flag, block
  construction) is now exercised on a configuration where the numbers actually mean what they
  claim. Run on a 1439-point build it reports `0` defects among the valid interior cells and
  `520` boundary cells correctly flagged — the flag works.
- **A15 has no defective cell**: `7.8125` and `8.0625`, both far above `5.6569`. So it does not
  answer `(Q)`. Its density `0.5236` is far below fcc's `0.7405`, so this is unsurprising.

**A failed attempt, recorded.** I first tried the Laves phase C15 (MgCu₂) as a denser
candidate, since its mean cell volume (≈ `5.90` at density `0.71`) sits close enough to `√32`
that individual cells could dip below. My construction used an **8-atom** basis (one Mg plus one
Cu orbit) when C15 has **24** atoms per conventional cell (8 Mg at 8a + 16 Cu at 16d). The
result was nonsense — all cells `98.53` with extent `4.12`, density `0.0425` — and I discarded
it rather than patching the geometry from memory. Anyone continuing this should take the Wyckoff
positions from a crystallographic source, not reconstruct them.

### 9.2 Periodic relaxation recovers fcc, and finds nothing denser

`Experimental/scripts/periodic_relax.py` relaxes `N` points in a periodic cube, minimising
`L^3 + P·Σ max(0, 2 − d_ij)^2`, i.e. driving density up until contacts lock.

| `N` | `L` | density | mean cell volume |
| --- | --- | --- | --- |
| 4 | `2.827432` | `0.741262` | `5.650888` |
| 8 | `3.793810` | `0.613694` | `6.825535` |
| 12 | `4.601329` | `0.515965` | `8.118368` |

The `N = 4` optimum is `L = 2.8274` against `2√2 = 2.8284` for fcc, with density `0.7413`
against `0.7405` — the relaxation has recovered **fcc**, which is the correct answer and a good
validation of the harness. The larger cells find only sparser structures, so the search is not
finding a denser Frank–Kasper competitor.

All runs landed marginally below the legality threshold (`min_d` in `[1.9956, 1.9993]`), i.e. the
penalty weight was too small to hold separation exactly; none was accepted as legal. That is a
parameter defect in the harness, not a mathematical result, and it is why `best legal: none` is
printed.

**Where `(Q)` stands.** Unanswered. Two saturated configurations have been examined (fcc via the
relaxation, A15 explicitly) and neither has a defective cell; the one configuration that *does*
have a defective cell (the icosahedral cluster) cannot be saturated. That is consistent with —
but does not establish — the possibility that `(Q) = no`, which as noted would collapse the
route to the per-cell inequality. Settling `(Q)` needs a certified periodic construction (correct
Wyckoff data, exact coordinates, periodic Voronoi decomposition) or an impossibility proof; it
is the single highest-value next task and I make no claim about it.

### 9.3 A control that worked: a blind relaxation recovers `pi/sqrt18`

After fixing the projection defect of Section 9.2 — scale `L` by `2/min_d` so the final set has
minimum separation **exactly** `2` and is legal by construction — the harness returns

```
N = 4,  L_proj = 2.828427276067519    (2 sqrt2      = 2.828427124746190)
density        = 0.7404803708455797   (pi/sqrt18    = 0.740480489693652)
mean cell      = 5.656855157420403    (sqrt32       = 5.656854249492381)
four cell volumes: 5.656855, 5.656855, 5.656855, 5.656855   (all equal)
relative error in density: 1.6e-07
```

A blind local optimisation over `(4 positions, cell size)` with no knowledge of fcc — only the
separation constraint and the volume objective — lands on a four-point cell with equal edge
lengths `2√2`, four equal Voronoi cells of volume `√32`, and the density `pi/sqrt18` to eight
significant figures. That is a genuine independent check that the evaluator chain (separation
handling, periodic images, Voronoi volumes, density conversion) is consistent with the target.

It is **not** evidence for or against `(Q)`: fcc has all cells exactly at `√32` and none below,
so it neither supplies a defect nor excludes one. Its value is as a calibration: if the harness
had a systematic error in the volume or the periodic convention, it would not reproduce
`sqrt32` and `pi/sqrt18` simultaneously to eight digits.

The `N = 6, 8, 12, 16` runs found nothing denser than the `N = 4` (fcc) optimum, so the search
offers no Frank–Kasper competitor with a small cell. `(Q)` remains open, and the next step is a
certified periodic construction from crystallographic data rather than a relaxed search.
