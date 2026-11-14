# Review 0138 — withdrawal of K15-C029 and what replaces it

Source withdrawn-from: `6626714125c35292d78943cd0fe8d18ec0051b38`.
Reviewer finding (immediate, independent): the proof of `K15-C029` is invalid.
Main accepts it in full. This file records the withdrawal, the rejected text, the
correct estimate with the negative part, and what of the surrounding programme
survives.

## 1. What was wrong

`K15-C029` argued: `A(v) ≥ θ` on `D_θ`, and `Σ_{v∈Λ∩B(x,r)} A(v) ≤ C₁r²`, hence
`θ·#(D_θ ∩ B(x,r)) ≤ C₁r²`.

The middle step is false. Negligibility bounds a **signed sum**; the negative
terms of `A` outside `D_θ` can cancel the positive terms inside it, so the sum
carries no information about `#D_θ`. The proof silently assumed `A ≥ 0`, which is
not among the hypotheses — and is not true for the `A` Hales actually uses
(where `A` must be negative on cells larger than `√32`).

**Minimal illustration of the logical gap** (arithmetic, not a geometric packing
counterexample): let `Λ = 2ℤ³` and let `S ⊂ Λ` be a sublattice of density `δ`.
Set `A = θ` off `S` and `A = −θ(1−δ)/δ` on `S`. Then the mean of `A` is exactly
zero — `(1−δ)θ + δ·(−θ(1−δ)/δ) = 0` — while `A ≥ θ` on the full-density set
`Λ ∖ S`, so no bound of the form `#D_θ ≤ C₁r²/θ` can follow.
*(Correction, review 0138-local: the first version of this paragraph wrote
`A = −θ/δ` on `S`, whose mean is `−δθ`, not zero. The coefficient
`−θ(1−δ)/δ` is the one that gives zero mean; both versions satisfy the
one-sided negligibility bound — a negative mean is still `≤ C₁r²` — so the
illustration survives, but the stated arithmetic did not.)*
Whether such an `A` is *realizable* by a packing is a separate question; it does
not need to be, because the step being refuted is logical, not geometric.

## 2. Withdrawn text (kept as rejected evidence)

The full `K15-C029` entry remains in `Main/CLAIMS.md`, marked
`WITHDRAWN (proof invalid, review 0138)`. Nothing dependent on it may be cited.

Dependent statements withdrawn at the same time:

| Where | Statement withdrawn |
| --- | --- |
| `CLAIMS.md` K15-C029 (2) | "a proposed `A` uniformly positive on a positive-density set cannot be negligible" |
| `CLAIMS.md` K15-C029 (3) | "the average of `A` is `o(1)`, so `A` must be negative on a full-density set" |
| `CLAIMS.md` K15-C029 (4) | the "usable objective" containing "`A` must be negative on a set of vertices of full density" |
| `RESULTS.md` §2 item 5 | "defect density is zero" as a proved statement |
| `PROOF_GAPS.md` G7 | the falsification test derived from it |
| `PARTITION_SPEC.md` R3 | "K15-C029 applies: `A` must be positive at defect vertices and negative on a full-density set" |
| `PROGRESS.md` K15-MAIN-007 | the same claim in the block entry |

## 3. The correct estimate (K15-C029r, `PROVED`)

Same hypotheses: `Λ` saturated 2-separated, `vol Ω(v) + A(v) ≥ √32` for all `v`,
`Σ_{v∈Λ∩B(x,r)} A(v) ≤ C₁r²` for all `x`, `r ≥ 1`.

**Lemma.** For every `θ > 0`, every `x` and every `r ≥ 1`,
```
θ · #(D_θ ∩ B(x,r))  ≤  C₁ r²  +  N_A(x,r),        N_A(x,r) := Σ_{v∈Λ∩B(x,r)} max(−A(v), 0).
```
*Proof.* `Σ_{B} A = Σ_{D∩B} A + Σ_{B∖D} A ≥ θ·#(D∩B) − N_A`, since `A ≥ θ` on
`D` and `A ≥ −max(−A,0)` everywhere; combine with the negligibility bound. ∎

**Reading.** The defect count is controlled by the *negative mass* of `A`, not by
`C₁` alone. Any use of this lemma must supply a bound on `N_A`. Two ways:

1. **Conditional lemma, `A ≥ 0`** (recorded separately, since it is what the old
   entry actually proved): if in addition `A ≥ 0` pointwise, then `N_A = 0` and
   `#D_θ ∩ B(x,r) ≤ C₁r²/θ`. This is true and may be cited *with that
   hypothesis*. It is not Hales' situation.
2. **Bounded-range transfers** (`K15-C035` below): if `A` comes from an
   antisymmetric transfer of range `R` and bound `Φ`, then
   `N_A ≤ Φ·k_R·#(Λ∩B(x,r))`, and the lemma becomes a *relative* bound: the
   density of `D_θ` is at most `(Φ k_R/θ)·c(Λ)`. That is the form in which the
   estimate is usable, and it is what the transfer construction supplies.

## 4. What survives, and what does not

- **Survives:** Lemma 3.3 itself (which needs only one-sided negligibility,
  because it combines it pointwise with fcc-compatibility). `K15-C002b`,
  `K15-C003r`, `K15-C004`, the verified certificate `K15-C023`, the interface and
  the checkers are untouched by this withdrawal.
- **Does not survive:** any statement that fcc-compatibility plus negligibility
  forces the small-cell set to have density zero, or that `A` must be negative on
  a full-density set. Those were the "usable objective" of the last block; the
  objective is now the weaker and correct one in §3.
- **Scope retraction (second review point).** The last block's claim that the
  shell and two-point families are "closed" is narrowed: finite-optimiser
  failures and one fixture support only the tested scope. `K15-C028`'s fixture
  shows the allowance is unprofitable *at degree 3 in that family*, and C's
  saturation is a statement about *that certifier*; neither is an impossibility
  theorem. The word "closed" is replaced by "no gain found in the tested scope".

## 5. Integration log for this block

Read at receipt (`2026-11-14T09:42:58Z`): supervisor `3c8ea4b0…`, Computation
`5c102677…`, Experimental `4ea4e8b9…`, Counterexamples `e3a63a18…`. Nothing was
merged; artifacts are imported by reference with full hashes in
`Main/SOURCE_MANIFEST.md`, and no unrelated history was deleted.

| Artifact | Disposition |
| --- | --- |
| X `Reviews/audit_shell_check.py` | **run**; quadrature confirms Main's Fourier map to `4.9e−15` (K15-C041). Two defects in the script reported. |
| C `shell_sos.py`, `shell_propose.py` | read; proposer-only, all verdicts `null` (K15-C046) |
| E `verify_all_claims.py` | **run**; 23/23 consistent (K15-C047), not independent |
| E `TAMMES13_ENCLOSURE.md` | audited last block (K15-C027); unchanged verdict |
| E `outer_cell_angular_bound.py`, `K15-E048` | imported with scope (K15-C042); one constant `5.665735` queried |

Block content beyond the withdrawal: `K15-C029r` (correct signed estimate),
`K15-C029c` (conditional), `K15-C035` (transfer ⇒ negligibility, explicit
`C₁ = 3ΦR(R+1)⁵` — factor `R` restored in review 0223), `K15-C036` (no finite fixture can decide), `K15-C037` (C002b
audit), `K15-C038`/`C039` (transfer and cluster fixtures, both with the
monotonicity lesson), `K15-C043` (Lemma 3.3 chain re-derived), `K15-C044`
(transfer feasibility, corrected in-block), `K15-C045` (structural synthesis),
`K15-C040` (Lean volume module + request `M-LEAN-002`).

## 6. Second finding, received mid-block: the sign predicates were unsound

Local reproduction at source `6626714` found that `Computation/shell_check.py`
accepted three impossible inputs (`u(1−u) ≤ 0` on `[0,1]` with value `+1/4` at
`1/2`; `u(u−1) ≥ 0` on `[0,∞)` with `−1/4`; `u(1−u) ≤ 0` on `[0,∞)`). Root
cause: Sturm's `V(a) − V(b)` counts roots in `(a, b]`, the code subtracted a root
at `lo` instead of `hi`, and testing only endpoints is invalid when both endpoints
are roots. `K15-C049` records the general repair (root isolation plus one test
point per constant-sign gap), the regressions now kept permanently (19 cases), and
the re-verification: the K33b certificate still `ACCEPT` with the identical ratio,
the fixture value unchanged, the `exactcert` cross-run unchanged. General
soundness claims are suspended until X audits the repaired file.

This is the second withdrawal of the block (the first was `K15-C029`) and the
lesson is the same in both: a claim was supported by *tests that could not have
failed*. The countermeasures are now mechanical — `Computation/run_all_checks.py`
(8 checks, one command) and the fuzz script `K15-C050`.

## 7. Method note carried forward

The two defects found this block (`K15-C029`'s implicit `A ≥ 0`, and the sign
predicates of `K15-C049`) have the same shape: a claim whose *tests* could not
fail. E's `interval_selfaudit.py` is the model to copy — it checks soundness
*and* that a deliberately corrupted primitive is detected (`K15-C057`).
`Computation/run_all_checks.py` (`K15-C053`) is Main's version of the same idea,
and `predicate_fuzz.py` / `predicate_crosscheck.py` are the independent supports
for the repair. Any future checker in this project should ship with all three.

## 8. Third finding, received near the end of the block: the first repair was wrong too

`K15-C049`'s algorithm (odd part plus three probes) accepted three *new*
impossible inputs, all perfect squares — `[u(u−1/2)(u−1)]² ≤ 0` on `[0,1]` (value
`+9/4096` at `1/4`), `−[u(u−1)(u−1/2)(u−2)]² ≥ 0` (value `−441/65536`) and
`[u(u−1)(u−2)]² ≤ 0` on `[0,∞)` (value `+9/64`). The odd part of a square is a
constant, so the count was zero and the three probes landed on roots.

The algorithm is now changed rather than patched: test points come from the
polynomial's own roots, one per constant-sign gap, with the odd part removed from
the code. `K15-C058` records this; the suite is at 24 cases and includes all six
witnesses. **Every general soundness claim about the checker remains suspended**,
and the block's own record now contains three of them (C029, C049, C058) — the
reason the project's summary asks for X's audit before any of it is relied upon.

Two further corrections from the same evidence round: the signed toy example in
§1 had the wrong coefficient for a zero mean (`−θ(1−δ)/δ`, not `−θ/δ`; corrected
in place), and the cluster fixture's completions were **not packings** until a
cross-distance filter against the core was added (`K15-C039`, updated).

## 9. Block summary (for the supervisor)

Block `K15-REVIEW-0138-M`, receipt `2026-11-14T09:42:58Z`.

**Withdrawn:** `K15-C029` (invalid proof, the reason the block exists),
`K15-C049`'s algorithm (superseded), `K15-C014` (earlier block, still documented).
**Added and proved:** `C035` (transfers ⇒ negligibility, explicit constant),
`C036` (no finite fixture can verify the pointwise inequality), `C043` (Lemma 3.3
chain re-derived), `C044` (cut condition, corrected in-block), `C045` (synthesis),
`C054` (transfer graph has degree ≤ 12 at `R ≤ 2.09`), `C029r`/`C029c` (signed
estimate and its conditional form), `C037` (C002b audited), `C024` (normalisation).
**Verified:** `C023`, `C031`, `C041`, `C048`, `C052`, `C055`, `C056` (the K33 pair
under a repaired checker and three implementations).
**Fixtures:** `C038`, `C039` (corrected twice), `C028` (+ two addenda), `C051`
(negative search), `C053` (one-command runner), `C030` and `C058`'s 24 cases.
**Lean:** `C040` — statement frozen, no proof, `M-LEAN-003` filed.
**Suspended:** every general soundness claim about the checker, until X audits
`Main/AUDIT_REQUEST_X.md`'s four questions.
