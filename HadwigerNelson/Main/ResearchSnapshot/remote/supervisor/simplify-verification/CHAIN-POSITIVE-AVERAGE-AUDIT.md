# One consumer chain, audited end to end: `agrees` → `positive_average` → support → unit-pair exclusion

Block 18, source-level only; no builds, no computation. Grades **[S]** source read, **[S+]** source read
and the step follows at the quoted line, **[P]** paper, **[C]** my reading. Timestamp of the block is in
`STATUS.json` (`updated_utc`, read from the clock).

## 0. A correction about the brief

There is **no `SmallArcs → FullApprox` chain** to audit: `SmallArcs` lives at
`lean/OAI/Analysis/PlaneSpectrum/SmallArcs.lean`, i.e. on the rigidity/spectral side, and is not imported by
`FullApproximation.lean` (whose only imports are `ContinuumLimits` and `GraphPatches`). The chain that exists
and does the work is the *Exclusion-type* one below, and it is the smallest substantive unaudited link in the
`FullApprox` consumption path.

## 1. The chain, with declarations and lines

| # | declaration | line | exact content |
|---|---|---|---|
| 1 | `structure FullApprox` field `agrees` | `FullApproximation.lean:264-265` | `∀ z : closedBall 0 5, z.val ∉ diskHoles disks → (map z).val = thresholdMap c ε α z.val` — **pointwise**, off a *stated* exceptional set, at this witness's own `ε` |
| 2 | `thresholdMap_pos` | `GraphRealization.lean:265-267` | `0 < thresholdMap c ε α q i ↔ α < diskAverage c ε i q`, from `thresholdTotal_pos` (`:249`), which needs `Measurable c`, `0 < ε` and `α < 1/5` |
| 3 | `FullApprox.positive_average` | `Mesh.lean:83-88` | `q ∉ diskHoles a.disks → 0 < (a.map q).val i → α < diskAverage c a.ε i q.val` — proof: `rw [a.agrees q hq] at hp` then `(thresholdMap_pos hc a.ε_pos hα q.val i).mp hp` |
| 4 | `support_of_positive_diskAverage_limit` | `Mesh.lean:37-…` | `Tendsto ε 0 → Tendsto a x → (∀ n, 0 < diskAverage c (ε n) i (a n)) → x ∈ spatialSupport c i`; proved via `Measure.mem_support_iff_forall`, a ball `ball (a n) (ε n) ⊆ U` and `diskAverage_area` |
| 5 | `diskAverage_unit_pair` | `DiskAverages.lean:63-69` | `‖q - z‖ = 1 → diskAverage c ε i q + diskAverage c ε i z ≤ 1`, from `colorFn_unit_pair` (the weak colouring) and a.e. monotonicity of the integral |
| 6 | consumer | `Mesh.lean:118-124` | uses 4 to get `p.1 ∈ spatialSupport c i`, then asserts `Disjoint (spatialSupport c i) (ball p.1 (1/8))` by `diskAverage_support_exclusion`, whose inner goal at `:142` is `diskAverage c (F (φ n)).ε i z ≤ 1 - α` |
| 7 | the two joins | `Mesh.lean:140-146` | `straddle_connected_unit (hK (φ n)) …` supplies a unit-distance pair `(q, z)` inside the connected region; `unit_from_hole_mem_annuli hh hunit` turns `q ∈ diskHoles` into `q ∈ holeAnnuli` (so `hqH : q ∉ diskHoles` follows from `z ∉ holeAnnuli`-type separation), then 3 gives `α < diskAverage … q`, then 5 + `linarith` gives `≤ 1 - α` |
| 8 | the contradiction | `Mesh.lean:147` | `Set.disjoint_left.mp hexc hasup (Metric.mem_ball_self (by norm_num))` — the support point sits in the ball the support is disjoint from |

## 2. Concluded statement (explicit)

> For a weak measurable 5-colouring `c`, `α < 1/5`, a sequence of `FullApprox c α (t n)` with `t n → 0`, and a
> connected region `K n` of diameter `> 2` on which the `i`-th coordinate is positive, the two limit points
> `p.1 ≠ p.2` cannot both lie in `spatialSupport c i`.
>
> `FullApprox.no_large_positive_sequence` (`Mesh.lean:92`): `False` — i.e. no such sequence exists.

## 3. The inequalities actually needed, and who discharges them

| inequality | where needed | discharged by |
|---|---|---|
| `0 < ε` | 2, 5 | `FullApprox.ε_pos`; `(F (φ n)).ε_pos` at `:144` |
| `α < 1/5` (strict) | 2 via `thresholdTotal_pos` (`1 - 5α > 0`) | `hα'` at `Mesh.lean:119, 143`; supplied as `1/10` with `by norm_num` at `Five.lean:105-107` |
| `0 < (map q).val i` | 3 | `hprob _ _ hq` — the *large positive region* hypothesis, pointwise in the region |
| `q ∉ diskHoles disks` | 3 | `hqH`, from `unit_from_hole_mem_annuli`: hole membership plus unit distance would put `q` in the annuli, against the separation |
| `diskAverage_i(q) + diskAverage_i(z) ≤ 1` | 5 | `diskAverage_unit_pair`, which is a.e. in the *weak colouring* (`colorFn_unit_pair`) |
| `α < diskAverage_i(q)` ⇒ `diskAverage_i(z) ≤ 1 - α` | 6 | `linarith` on the previous two |

**Quantifier discipline.** Steps 1-3 are **pointwise**: one centre `q`, one label `i`, one witness (hence one
scale `ε`). No a.e. qualifier and no measure appears. The only a.e. input is the *weak colouring* inside
`diskAverage_unit_pair`, and it is consumed through `diskLaw_absolutelyContinuous` — i.e. it is pushed to an
a.e. statement about the **law** `diskLaw ε`, not about the plane. Step 4 is where a limit enters, and it is a
`Tendsto` in `ℕ`, not an a.e. statement.

**Centre/scale discipline.** The scale is always `(F (φ n)).ε` — the *same* `ε` on both sides of step 2 (no
scale shift, no `ε/2`), and the centre is `q.val` in `diskAverage` and `q` in the subtype at once. So the chain
needs no radius bookkeeping beyond `ε < t` (`ε_lt`), and the "angular" content is entirely inside
`diskAverage` (an average over `ball 0 ε`, converted by `diskAverage_area` to `volume (ball q ε ∩ {c = i}) /
volume (ball 0 ε)`).

**Where the annuli enter (and their radius).** Not through `positive_average` but at `:141`:
`unit_from_hole_mem_annuli` maps "`q` is in a hole and at unit distance from `z`" into `holeAnnuli`, and
`diskAnnulus d = closedBall c (1 + r) \ ball c (1 - r)` has area `4πr` (`volume_diskAnnulus`), which is the
per-disk charge in the shrinking budget. So the `1 ± r` radii are used *only* for the measure estimate, never
for a pointwise claim.

## 4. Genuinely unsupported premise?

**None.** Each premise of each step is discharged at the cited line. Two boundary conditions are worth naming
because they are hypotheses rather than consequences:

1. `support_of_positive_diskAverage_limit` requires `∀ n, 0 < diskAverage c (ε n) i (a n)` — positivity at
   **every** index, not eventually. In this chain that holds because the region hypothesis is `∀ n`
   (`hbad : ∀ n, …`). A variant giving positivity only eventually would need the sequence restricted to a
   tail first; nothing in the tree does that, so no obligation is open.
2. `positive_average` needs `q ∉ diskHoles a.disks` **at that witness's own disk family** — the exceptional
   set is per-witness, and it is supplied per-witness at `:143`. There is no "one exceptional set for all
   scales" claim anywhere, consistent with the paper's own remark that the null sets are those of a single
   application.

Verdict: **the chain is sound at source level**, with the caveat that "sound" here means *this* chain; it is
not a statement about the paper's §7.4 as a whole, and it establishes no new topological result. Everything in
it is inherited source.

## 5. Retained

`initialDisks`' L-part carries `core := true` (the paper's core family); `centerDisks` is a separate family
with `core := false`. `diskAnnulus = closedBall c (1+r) \ ball c (1-r)`, area `4πr`.
