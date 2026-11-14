# Block `K15-REVIEW-0438-M` — reconciliation, one repaired proof, and one new bridge

Started `2026-11-14T12:42:16.523Z` on delivery of `K15-REVIEW-0438-M`. Sources reconciled:
C `6fbd0a1bf214a92b625cee84e8ee95ac5da4b8d9`, E
`498cfc3c0ce8d023fbf29b5810d06be115ac256b`, X `d64de362da7b6f52bd494d15364e67783a3b184b`,
plus the local evidence in `K15-REVIEW-0438-M-LOCAL`. Work continued from `7ba7146425`.

## 1. The one thing that was actually broken: `C094`'s Lemma 1

E's `K15-E083` found it, the supervisor's `K15-REVIEW-0438-M-LOCAL` asked for it to be checked
before `C094` is accepted, and **it was real**. `C094`'s Lemma 1 argued that a non-contact
half-space `H_c` contains `B(v,√2) ⊇ Ω(v)`, "hence is redundant". That is circular: `Ω ⊆ H_c`
holds *by definition* for every half-space in the intersection defining `Ω`. Redundancy needs
`K ⊆ H_c` for the **contact-only** polytope `K`.

**Repair (`C104`).** Two steps: (1) `K ⊆ B(v,√2)`, an exact finite statement about the contact
polytope that never mentions `Ω`; (2) for `x ∈ K` and a non-contact `c`,
`|x−c| ≥ |c−v| − |x−v| ≥ 2√2 − √2 = √2 ≥ |x−v|`, so `K ⊆ H_c`, hence `Ω = K`.

**Main re-verified the contact bound independently** (`Computation/contact_cell_exact.py`), from
E's *statement* and not E's code: exact arithmetic in `Q(√2,√3)` as 4-tuples over `Fraction`,
Cramer solves, exact feasible-set tests, rigorous interval sign decisions. Both local types:
14 vertices, `|x|² ∈ {3/2 (×8), 2 (×6)}`, `max = 2`, Euler `14−24+12 = 2`. This is the
exactness `C094` now rests on — see §2 for why it is not E's script.

`C094`'s acceptance is **restored on the repaired proof**, and the theorem is unchanged.
`(F3)` is no longer used by it, so the repaired chain is shorter.

## 2. Corrections to worker material (and one to Main's own)

| # | who | finding | disposition |
| --- | --- | --- | --- |
| 1 | C, `STATUS.md` item 1 | `shell_check.py` "at `6626714` is unsound", three witnesses falsely accepted | **Stale revision of Main's own branch.** `6626714` is an ancestor of `kepler15/main` that predates the `C058`/`C068` repairs and still contains `_odd_part`. Main ran all three witnesses against the current file: `le_on_interval([0,1,−1],0,0,1)`, `nonneg_on_half_line([0,−1,1])`, `_ray([0,1,−1],0)` all return **False** (correctly; `u−u² = 1/4 > 0` at `u = 1/2`). Already fixed. Generic checker soundness nonetheless stays **SUSPENDED** — C's advice is right in form, wrong in reason. |
| 2 | E, `K15-E083` | Main's `C094` Lemma 1 is circular | **Confirmed**, repaired `C104`. |
| 3 | E, `INTEGRATION_0353` | `GAP_FIXTURE` overstates: "for `d > 1.633` … saturated" needs `d ≤ 2H` | **Confirmed**, corrected to `1.633 < d ≤ 2H = 3.265986`. |
| 4 | supervisor, `LOCAL` | `barlow_contact_cell.py` admits vertices by `sp.N(...,30) > 1e-25` and compares radii numerically; not fully exact. C5 geometry also numeric | **Accepted.** `C094` now rests on Main's exact re-derivation, not on E's script; the file states this. E's script is not advertised as exact anywhere in `Main/`. |
| 5 | supervisor, `LOCAL` | universal lower-volume claims must stay unaccepted | **Accepted.** `(L)`, `σ₀`, `δ₀` are `PENDING_REVIEW`; `C108` is a strictness statement and no number moves. |
| 6 | Main | first draft of Theorem C wrote `ρ = 1`, impossible for a matching (`P_B/|B| ≤ 1/2`), making the formula return `0.7268 < π/√18` | **Caught by `constants_check.py`**, corrected to `ρ ≤ 1/2`; recorded in `C108`. |
| 7 | Main | first version of `two_dodecahedra.py` removed the wrong pole for `w` (the shared contact lies at `−2` in `w`'s frame) — the same bug E records | **Fixed**; the pole convention is now explicit in the script. |
| 8 | Main | E's `K15-E075` quotes `1.056487696`, Main gets `1.12555484451` | **Recorded, not resolved.** Both `< 2`; conclusion identical; Main cites its own value. |
| 9 | Main | E's A15 row (`15.875`) is the **A–B** pair at distance `2.236`, not a contact pair; A15's contact pairs are B–B at `a/2 = 2`, summing to `129/8 = 16.125` | **Confirmed by exact computation** (`C111`): `vol_A = 125/16`, `vol_B = 129/16`, weighted sum `= a³ = 64` exactly. Nothing refuted (both exceed `2√32`); the row is corrected. This is the second convention error in the workers' pair tables, after E's pole convention in `E075`. |
| 10 | Main's rhetoric | "the cut condition implies Kepler, so the route is a reorganisation, not a simplification" | **Withdrawn** (`C105`). A sufficient criterion is not circular because it implies the target; only the "weaker target" reading is forbidden. Corrected in `ACCEPTED.md`, `C087`, `COMPLEXITY.md`. |

**Also recorded:** Astra verified original X-C017 at `< 0.782267220134` and the 37 repaired
checker regressions; the smaller C017 certificate gives strict `< 0.782267254857` (very slightly
weaker) with maximum rational entry 41 characters, and remains `PENDING_REVIEW` here. C's
repaired dodecahedron enclosure, both edge-threshold controls and the FCC constructor are
verified locally. E's C5 seed-0 pilot found `5.898007181` with no improvement; seven further
seeds are pending, so **no universal lower-volume claim is accepted**.

## 3. The research: the highest-value geometric lemma, and the bridge it was missing

Full statement, proofs and witness table in `Main/GEOMETRIC_LEMMA_0438.md`; ledger `C106`,
`C107`, `C108`.

**The lemma chosen.** E's pair conjecture `(P′)`: `vol Ω(v) + vol Ω(w) ≥ 2√32` for every contact
pair. It clears the brief's bar — with the bridge it yields `δ ≤ π/√18` exactly, not
`0.754697…` — and it is strictly stronger than the published dodecahedral bound because
`2V_dod = 11.100582 < 11.313708 = 2√32` and E's `E075` shows `2V_dod` is unattainable for a
contact pair. **New here: `(P′)` holds with equality on every Barlow packing**, from `C094`, so
its equality family is exactly the known extremal one.

**What was missing.** E's warrant for `(P′)` is "it implies the cut with `1.72%` margin"; that
arithmetic is right but it is the 13-cluster cut only. A cut at one `U` is not a density bound.

**The bridge (`C106`).** `(P′)` + a fractional perfect matching of the contact graph off a
density-zero set ⟹ `δ ≤ π/√18`; with `deg ≡ 12` the matching is free, which covers every Barlow
packing. Proof by summing cell volumes against the matching weights over a ball, with the
crossing edges `O(R²)` by 2-separation and the tiling `(4π/3)R³ + O(R²)` from saturation.

**The quantitative point (`C107`), and the sharpest number this project has produced about its
own gap.** The bridge is monotone: any pair constant `K` gives `δ ≤ 8π/(3K)`. Then

```
K = 2V_dod  = 11.100582057  →  δ ≤ 0.754697399337   (exactly the dodecahedral bound)
K = 2√32    = 11.313708499  →  δ ≤ 0.740480489693   (exactly π/√18)
```

So the route has **no sharpness barrier**: any `K > 2V_dod`, however small the excess, beats
`0.754697399337`, and the **entire remaining gap is a `1.92%` increase in one two-cell
constant** (`√32/V_dod = 1.01919957`). Contrast the two routes already closed here: pointwise
cell bounds are dead because `V_dod` is *attained*, and the plain two-point LP is dead by Li's
obstruction. The pair functional has room.

**`(L_δ)` is true (`C108`).** `σ₀ := inf` of the pair sum satisfies `σ₀ > 2V_dod`, by
compactness: a cell of volume `≤ C` lies in `B(·,3C/π)`, so for bounded `Φ` the local
configuration is compact; at a minimiser with `σ₀ = 2V_dod` both cells have volume exactly
`V_dod`, hence by ML's equality case both are regular dodecahedra, which Main re-verified to be
impossible for adjacent centres (`1.1255548 < 2`, a `44%` shortfall). With a **maximal**
matching this gives, unconditionally and with no fractional matching,

```
δ(Λ) ≤ (4π/3)/(V_dod + δ₀ρ)  <  0.754697399337   whenever ρ > 0,
```

where `ρ ≤ 1/2` is the matching density and `δ₀ = σ₀ − 2V_dod > 0` is **not explicit**. Two
corollaries worth having: any saturated packing with a positive density of contact pairs is
*strictly* below the dodecahedral bound, and **the equality case of the dodecahedral density
bound is empty**.

**What this is not.** Not a number. `δ₀` is non-explicit, so `RESULTS.md` does not move, and no
universal lower-volume claim is accepted pending review.

## 4. Reconciliation of the claim files

- `CLAIMS.md`: `C091` restatused, `C093` repaired (`D18`), `C094` repaired (`C104`), `C087`
  direction corrected (`C105`), `ACCEPTED`/`COMPLEXITY` rhetoric corrected (`C105`); new
  `C100`–`C108`.
- `ACCEPTED.md`: cut-condition row corrected and a standing caution added on one-way arrows;
  the Barlow row now says "repaired at `C104`"; the pair route added as `PROPOSED`.
- `RESULTS.md`: **unchanged in every number.** The bound to beat analytically is still
  Hales–McLaughlin's `0.754697399337`; nothing here is quoted as a bound.
- `PROOF_GAPS.md`: `G5` unchanged; new gap recorded as the explicit `δ₀` ("payer") and the
  matching density `ρ`.
- `DECISIONS.md`: `D18` (repair discipline: two proofs, rejected text retained, hypotheses
  itemised), `D19` (pair route is the live geometric route; pointwise is closed by sharpness).

## 4a. A hostile self-audit of the two new theorems

Written because a referee looks here first; the details are `GEOMETRIC_LEMMA_0438.md` §4.1a.

- **Theorem B** survives: the sum swap is finite, both factors non-negative, the counting
  identity `|B| − |E_B| = 2Σ_{internal}c_e + C_R` is an identity and not an estimate, and the
  tiling step is the only place saturation is used. **Saturation is the bridge's single point of
  failure**, which is why B is stated for saturated packings.
- **Theorem C had a wording defect, now fixed**: the first version said "unmatched" where the
  correct split is "not in an *internal* pair" — a vertex matched to a partner outside `B`
  contributes only `V_dod`. The inequality is unaffected; the justification is now right.
  Also recorded: **maximality is not doing analytic work**, only bookkeeping on `ρ`.
- **Theorem D** survives its own audit, with one flagged dependency: it needs the *equality
  case* of Hales–McLaughlin ("`vol Ω = V_dod` iff the regular dodecahedron"). That is standard,
  and it is **not** re-derived here — **it is the softest link in the chain and the place a
  referee should push.**
- **A negative result recorded rather than hidden.** The compressed symmetric pair family
  (`C109`) is too sparse to probe `(L)`: it gives pair sums `20.99`–`30.02`, far *above*
  `2√32`, and since computed volumes are upper bounds it is neither support nor counterexample.
  It is reported as what it is.

## 5. Next package for the three workers

**Resource discipline for every request below.** All inputs are pushed on `kepler15/main`;
the revision to quote in any request is the tip **at the time of dispatch**, which after this
block's final push is the hash recorded in `SOURCE_MANIFEST.md`. Every computation is
single-process, `≤ 1 CPU`, `≤ 1 GiB`, `≤ 300 s`, stdlib plus `numpy`/`scipy`/`sympy` only, and
must exit non-zero on any internal inconsistency. Any Lean request additionally needs a
narrow-import file and the `≤ 1 GiB` cap honoured (`M-LEAN-002` already failed at 60 s / 715 MB
with a broad `Mathlib` import, so broad imports are not to be requested again).


**PN-C — the pair constant by construction.** C owns the fixture machinery. Ask: for the
two-centre model (centres at distance `d ∈ [2, 2.2]`, explicit local neighbourhoods, *validated*
2-separation over all pairs), compute `vol Ω(v) + vol Ω(w)` and report whether the minimum over
that family is bounded away from `2V_dod`, with the binding configuration named.
*Acceptance:* a validated configuration table, a minimum, and the margin over `2V_dod`; **no
claim that the minimum is the global one.** Portability: one file, stdlib only, `≤ 1 CPU`,
`≤ 1 GiB`, `≤ 300 s`, exact or interval arithmetic for every inequality, exit non-zero on any
validation failure.

**PN-E — the payer bound, which is now the whole geometric content.** E's own statement of what
it owes. Ask: a lower bound `vol Ω(w) ≥ 5.763417470` for the partner of a dodecahedral cell, or
*any* explicit `δ₀ > 0` for the pair functional — the latter is strictly weaker and already
sufficient (`C107`, `C108`).
*Acceptance:* a proof, or an explicit legal configuration with pair sum `< 2V_dod + 0.213126`
(which would bound `δ₀` and is itself valuable), or a documented obstruction. **Priority: the
weak form.** Caps: `≤ 1 CPU`, `≤ 1 GiB`, `≤ 300 s` per run; a sweep may be a batch of such runs
but each must validate the minimum separation over **all** pairs, including core–background.

**PN-X — audit three things, in this order.** (i) `C104`: that `K ⊆ B(v,√2)` is what Lemma 1
needs and that Main's exact script settles it; (ii) `C106`/`C108`: the bridge's counting
identity and the `ρ ≤ 1/2` range; (iii) the two-dodecahedra computation, including the
discrepancy with E's `1.056487696`.
*Acceptance:* a written verdict per item; the standing `shell_check` soundness argument
(`AUDIT_REQUEST_X.md` item 5) is still outstanding and is the only thing keeping generic
soundness suspended. `AUDIT_REQUEST_X.md` item 7 is the new pair-route request and names the
softest link explicitly (the Hales–McLaughlin equality case).

## 6. Honest accounting for this block

**Repaired:** one circular proof (`C094`'s Lemma 1), one rhetorical overstatement (sufficient ⇏
circular), one scope overstatement (`GAP_FIXTURE`'s saturation range), two of Main's own
implementation bugs, and the `ρ = 1` error in Theorem C. **Reconciled:** three worker revisions
plus the local evidence, with the `shell_check` report shown to be against a stale revision.
**New mathematics:** the bridge (`C106`), the monotone `8π/(3K)` payoff and the `1.92%`
quantification (`C107`), and `(L_δ)` by compactness with an unconditional strictness corollary
(`C108`). **Not achieved:** any number, any improvement over `0.754697399337`, and any progress
on the sharp `2√32`; the payer bound remains open and is now the single geometric item blocking
the route.

**Wall clock, honestly.** This block delivered twelve commits between `12:42:16Z` and `13:27Z`,
i.e. about `45` minutes of real time for the work above, and reached its final push at `13:29Z`
(`≈47` minutes). Roughly `25` of those minutes were consumed by **two timed-out attempts at the
A15 computation** — the first enumerated `C(1000,3)` half-spaces and the second used a full point
set without truncation; the third attempt, with the adaptive truncation of Lemma 3, ran in
`0.3 s`. That is the honest accounting, and the lesson is worth recording next to it: the
support-function truncation of `BARLOW_CELLS.md` Lemma 3 is not a nicety, it is what makes any
dense fixture computable at all, and a fixture script that ignores it does not merely run slowly,
it does not terminate.
