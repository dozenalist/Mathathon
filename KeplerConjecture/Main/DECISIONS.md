# Decision record — Kepler problem 15

Each entry: what was decided, the evidence, and what would reverse it. Main keeps
this file; workers may propose entries in their own branches.

## D1 — Freeze one mathematical contract (2026-11-14, M)

Adopt unit balls (radius 1), minimum separation 2, `δ` = occupied-volume upper
density, `c = 3δ/(4π)`, `f̂(t) = ∫f(x)e^{−2πi⟨x,t⟩}dx`, and quote CDS/higher-point
numbers in occupied-volume units with the centre-density equivalent alongside.
**Reason.** The recovered material mixes three conventions (radius 1/2 with
separation 1 and number density; CE "table units"; occupied volume), and
`Literature/PRIOR_WORK.md` records a dual-shell enumeration bug that was a pure
normalisation error. **Reverse if** a source theorem can only be cited in its
native scale — then convert in the same paragraph (K15-C007), do not re-freeze.

## D2 — Ordinary Cohn–Elkies is a control, not a target (M)

No effort goes into searching for a single admissible `f` that proves
`π/√18`. By Li (Adv. Math. 460 (2024) 110043, Thm 6.1) the CE optimum in `d=3`
is `> 0.18398089` in centre units against `2^{−5/2} = 0.176776695…`
(K15-C006). Two-point function searches stay useful only as (i) reproducibility
controls, (ii) components of a hybrid that carries extra geometric information.
**Reverse if** someone exhibits a proof that Li's bound is misquoted in this
range — the local reproduction of `0.18398089` is still pending.

## D3 — Re-anchor "better" to 0.754697399337 (M)

The comparison target is the dodecahedral bound `(4π/3)/V_HM` (K15-C008), not
the Fourier-family record `0.770271`. A new analytic or hybrid bound counts as
progress only below `0.754697399337`, or as a materially shorter proof of a
bound at least that strong. **Reason.** ROADMAP §5 lists the CDS values but the
frontier is set by Hales–McLaughlin; without this anchor the team would present
a `0.7703` re-derivation as state of the art. **Reverse if** X establishes that
a stronger published non-Kepler bound exists.

## D4 — A local-count price is proved; an integral tail is not excluded (M)

The earlier brief's "positive tail `I = ∫_{|x|>R} f`" interface has no proof.
Theorem B / K15-C003 supplies a proved replacement: it charges `n·max(M,0)`
where `n` is a contact number of the region where `f > 0`.
**Narrowing (review objection 10):** this does *not* show that integral tail
estimates are impossible. An integral estimate combined with a proved counting
envelope (K15-C013) is a legitimate route and is not excluded here.
**Evidence.** `smwg019eu` m2 §3: the integral form is equivalent to a global
equidistribution statement about the tail; a purely local argument loses a
factor `1/(c·vol B_1) = 1.3505`, and any refutation of the integral form must
beat the two-point optimum by `5.30%` (`f̂(0)/f(0) = 5.3719879` at the CE
optimum). **Reverse if** someone proves the equidistribution inequality for a
class of packings — then the integral form is available again on that class.

## D5 — Contact-sphere relaxation is closed (M, m2; restored)

"Let `f > 0` on `{|x| = 2}`, price it with the kissing number 12" is vacuous
(K15-C004). **Reverse if** the relaxation set has interior — which means a
genuine tolerance in the kissing problem, i.e. a new local theorem (see
K15-C013 and T5). That would be a result in its own right and would re-open the
route.

## D6 — Additive two-point corrections to Voronoi volume: RE-OPENED (M)

The checkpoint-1 closure was based on an inequality read backwards and is
withdrawn (K15-C005). The route is open: what is missing is a statement
controlling how often near-icosahedral cells occur in a packing, since
negligibility controls `Σ_v A(v)` only from above. **Status:** open, unowned.
**Note:** whoever revives it must freeze the sign convention first
(`score = vol Ω + A ≥ V_0`), and must not reuse Main's checkpoint-1 text.

## D7 — Sharpness and uniqueness claims must survive zero-density defects (M)

Any statement of the form "every maximal-density packing is …" must state how
zero-density regions (holes, unbounded defects, non-ergodic mixtures) are
handled. The recovered `smwfyzz1k` material contains uniqueness-flavoured
claims; they are `PENDING_REVIEW` (K15-R001…R005) and may not be cited.
Likewise the retracted "every smooth sharp certificate must vanish" argument
(PRIOR_WORK) stays retracted; Viazovska's `g` in `d=8` is a counterexample to
the blanket form.

## D8 — Lean scope: definitions and finite lemmas only (M)

No analysis formalisation. The two candidates worth compiling are
(1) the exact dodecahedral constant `V_HM` including `π`-free algebra
(`K15-COMPUTE-002`) and (2) the density-conversion identity `δ = (4π/3)c`
together with the finite count `n(δ) = ⌊(3+δ)³⌋−1` of K15-C003 Cor. 2.3.
Both are stable, small, and serve a concrete dependency. Everything else waits.

## D9 — Keep recovered drafts verbatim, supersede by ledger (M)

`Roadmaps/dim-3-analytic-bound-prompt.md` and `Roadmaps/sharp-bound-in-three-dimensions.md`
are committed unchanged, with checksums, and are marked superseded. Editing them
would destroy the audit trail for K15-C009 and D4. Corrections live in
`Main/CLAIMS.md`.

## D10 — K15-C014 withdrawn; grids are exploratory, Sturm is the acceptance test (M)

The submitted grid LP never imposed Fourier positivity and used a coefficient box.
The universal conclusion drawn from it is withdrawn (K15-C014r). Standing rule:
a candidate in the univariate Laguerre–Gaussian family is accepted only with an
exact sign decision (Sturm) on both half-lines, as in X-C008; anything else is
`TESTED_FINITE` at best. **Reverse if** a rigorous interval/ball-arithmetic
certificate covering both half-lines is produced with its driver.

## D11 — The lead local route is cluster-averaged, with its cost priced (M, E)

Adopt K15-C015 (E's `K15-E001`) as the project's local-geometric candidate: it
strictly relaxes Lemma 3.3 to cluster averages. Adopt E's `K15-E003` with it: the
criterion cannot be established by finite computations, so the next proof
obligation is an analytic cluster-volume lower bound (Rogers-simplex/Fejes Tóth
type), starting from the icosahedral 13-cluster. **Reverse if** the cluster
inequality fails on an explicit cluster (that would be a refutation, and E's
fixture is the first test).

## D12 — One hybrid score, frozen (M)

Any future hybrid must state which of the two scores it uses, with the self-term
in or out: (S1) `σ₁ = vol Ω + κ·Σ_μ f(v−μ)`, (S2) `σ₂ = vol Ω + κ·Σ_{μ≠v} f(v−μ)`.
No further hybrid obstruction or promotion may be discussed without naming the
score and its Poisson mean. K15-C005r settles both: (S1) degrades the bound by
`κf(0)`, (S2) is capped at `V_dod`.

## D13 — Claim-admission rules (M, after K15-C017)

A computational bound may enter `Main/CLAIMS.md` only with: (i) failure reporting
that is on by default — never inside a verbosity conditional; (ii) an exact
verdict at an adversarial witness point (a rational input that *must* fail);
(iii) the hash of the exact source that produced it, and a re-run of that source
by someone other than its author. A difficulty reported by a solver (for example
HiGHS "Model error") is a fault of the formulation until proven otherwise; it is
never evidence of infeasibility. **Reverse if** Astra's environment requires a
different reporting channel — then record the equivalent check explicitly.

## D14 — Two candidates, one benchmark, one target (M)

After this review the project carries exactly: (a) the **benchmark** of
K15-C018 (shell allowance, `ρ = 209/100` pending, `η ≥ 0`, count 12) as the
analytic candidate to evaluate, and (b) E's **constructive partition route** as
the geometric target, with K15-C015r's specified-partition formulation. The
exact-Sturm Laguerre family (X-C008) remains the only certification mechanism.
No third route is opened this cycle; no route is closed on the strength of a
wrong universal quantifier.

## D15 — `ρ = 2.05` is the first shell width to certify; `2.09` is the tight target (M)

K15-C019 turns the shell count into a single Tammes inequality. At `ρ = 2.09`
the required enclosure accuracy is 0.03°, which no artefact in this project can
currently support; at `ρ = 2.05` it is 1.26°. Certify `2.05` first, then tighten
only if E's enclosure supports it. **Reverse if** a published rigorous Tammes-13
enclosure with a stated margin arrives, in which case 2.09 costs nothing extra.

## D16 — One checker, used by everyone (M)

`Computation/shell_check.py` is the acceptance test for any shell-allowance
candidate: rational input, failure reporting unconditional, exact Sturm verdicts,
directed `π`. A number that has not passed it is `TESTED_FINITE` regardless of the
tool that produced it. **Reverse if** X's audit finds an error in it, in which
case the corrected file is the acceptance test and the old one is preserved.

## D17 — Next target: E's `(H_R)` in cluster-average form, not `(Q)` and not 3-point (M)

`K15-C069` refutes `(Q)` (a saturated packing *does* contain a cell below `√32` —
the dodecahedral one), so no pointwise cell statement can be the target. C's exact
SOS family plateaus at `Δ ≈ 1.99` and its higher-degree exact certificates at
`0.77996622`, so the two-point route has no slack left; the three-point
specification has never been implemented and there is no evidence it would pay
within the remaining budget. The target is therefore `Main/NEXT_PACKAGE.md`:
`Σ_U vol Ω ≥ √32|U| − O(Φ|U|^{2/3})` with `Φ` from `K15-C044`, plus E's `(H_R)`
as its formal version. **Reverse if** a worker produces a 3-point certificate
whose exact value beats `0.77996622`.

## D18 — the cut/flow theorem is repaired, not re-argued (M, after review `K15-REVIEW-0353-M-EVIDENCE`)

The reviewer found four defects in `K15-C093`/`CUT_FLOW_THEOREM.md`; all four were
confirmed against the text and are repaired in place with the rejected wording retained
(`CUT_FLOW_THEOREM.md` §6, ledger `C093`). The decision this records is *how* they were
repaired, because the tempting repair was the wrong one.

1. **Established convention now: a theorem gets two independent proofs before it is used
   as load-bearing.** The cut/flow theorem is now proved twice — once by max-flow on an
   explicit directed network (constructive, gives the algorithm) and once by LP duality
   plus the coarea formula (gives the exact dual, and is the one that survives signed
   capacities). The second proof is what found that the cut condition is *exactly*
   equivalent to feasibility and not merely sufficient.
2. **A rejected example is not deleted; it is replaced by the correct one.** `b =
   (4,−1,−1,−1)` is retained as rejected evidence with its actual status (infeasible at
   every capacity, `Σ_F b = 1 > 0 = cap(F)`), and the threshold example it was meant to be
   is added as `b = (4,−4/3,−4/3,−4/3)`, `t* = 4/3`.
3. **Empty boundaries are a separate case by default.** Any statement of the form
   `Σ_U b ≤ Φ|δ⁺(U)|` must say what happens at `δ⁺(U) = ∅`; here that case is an
   obstruction at every `Φ` and is capacity-free. This is now the standing rule for cut
   statements in this project.
4. **Hypotheses are audited for use.** `sup_e Φ_e < ∞` was in the theorem and is not used
   (Tychonoff needs only per-factor compactness). Any hypothesis in a `PROVED` claim must
   now name where it is used, as the table in `CUT_FLOW_THEOREM.md` §2 does.

**Reverse if** X's independent audit of the repaired statement finds a further defect; in
that case the pattern above (two proofs, rejected text retained, hypotheses itemised) is
still the right one, and the fix goes into the same two places.

## D19 — the pair route is the live geometric route; the pointwise route is closed by sharpness (M, review 0438)

The two facts established this block point in opposite directions for the *pointwise* route and
the *same* direction for the pair route, so this records the split.

- **Pointwise is closed, not merely stuck.** `vol Ω(v) ≥ V_dod` is *attained* — the dodecahedral
  cell of the 13-cluster embeds in a saturated packing (`C069`, `C095`). So no pointwise
  strengthening exists, and the dodecahedral bound `δ ≤ 0.754697399337` is the exact limit of
  that class. Continuing to look for pointwise improvements is a category error.
- **The pair functional has room.** `2V_dod = 11.100582` is *unattainable* for a contact pair
  (E's `E075`, re-verified here at `1.1255548 < 2`), while `2√32 = 11.313708` is attained on
  every Barlow packing (`C106`). The true infimum lies strictly between, and by `C107` **every**
  improvement of the pair constant improves the density bound, with no threshold to clear.
- **The payoff is `(4π/3)/(V_dod + δ₀ρ)`** (`C108`), so the pair route needs exactly two
  numbers: a geometric `δ₀ > 0` and a combinatorial matching density `ρ > 0`. Neither is a
  sharpness barrier.

**Decision.** Keep one geometric route active and make it this one. State the target in the
monotone weak form `(L_δ)` (`C107`), not the sharp `2√32`, because any positive `δ₀` suffices
and the sharp constant is a bonus. Do **not** open new pointwise targets. Keep the local
statement (the pair bound) and the global bridge (matching + counting) as *separate*
deliverables with separate owners, since they fail for different reasons.

**Reverse if** E's payer bound is proved with an explicit constant and the resulting number does
not beat `0.754697399337` (which cannot happen by `C107` unless `ρ = 0`, so the real reversal
condition is: if `ρ = 0` turns out to be compatible with high density, the bridge is vacuous and
the route needs a different global device).
