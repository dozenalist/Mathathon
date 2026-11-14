# Integration note — hourly review 00:08 PST, 2026-11-14

> Supervisor publication note: the previously unavailable review artifacts below
> are now present at `b649a85` on the supervisor branch. The four subsequent
> worker checkpoints and bounded local checks are listed in
> [the hourly review](HOURLY_REVIEW_2026-11-14_0008.md). Historical statements
> about unavailable files refer to Main's earlier fetch of `0e28e09`.

Compact record of what this cycle integrated, from where, and what is still
unattached. Sources by full hash. Nothing here is a new packing theorem.

## Revisions read

| Source | Hash | What was taken |
| --- | --- | --- |
| `kepler15/main` (this branch, reviewed) | `0c3ee751254b1b61f16eb175d9bd8d571f842b18` | the ledger being repaired |
| `kepler15/setup-01a1d8c0` (supervisor) | `0e28e093fbe13fdc4e7aad684536547e3f539e06` | hourly-review protocol, `PROGRESS_SUMMARY.md`, `Main/CALLBACKS.md`, `Computation/Reviews/27616/` |
| Computation branch | `4b509e33fe1f5d50d37f7dd19b698d708312d35a` | control values `Δ = 0.779702445785607` (K=31/g1200), `0.779745768082807` (K=41/g4000); `TESTED_FINITE` |
| Computation K21 certification | `e681fbfddb8c5962333380c271d5f7a67f44a07b` → tip `633da8e9db3987ec8c56a7c1eb628f3d47402bc2` | **withdrawn** (K15-C017) |
| Experimental | `7cdec5deee2b3c60845be49c9c5cecc1f3592f78` | `K15-E001` cluster criterion (repaired as C015r), `K15-E003` monotonicity obstruction, `K15-E004` open question |
| Counterexamples | `6871b1083fb25fe76d9ac58c6d149744ecace635` | `X-C001`, `X-C002`, `X-C003`, `X-C005`–`X-C008`, source audits `X-SRC-01/02` |

**Not yet fetchable at this checkpoint:** `Main/HOURLY_REVIEW_2026-11-14_0008.md`
and `Computation/Reviews/48443/` are announced but absent from the fetched tips
(grep over `git ls-tree` of `0e28e09` finds only `Reviews/27616/`). Findings from
them are integrated from the assignment text and marked as such in K15-C017. They
must be re-anchored to their artifacts when pushed.

## What changed in the ledger

- `K15-C017` **new**: Computation's K21 certification is refuted — the checker's
  failure path is inside `if verbose` (its `[2, −1]` impossible input passes), and
  the rebuilt `q` has ten simple positive roots with
  `q(57955199/21687900) ≈ −3.876231892749308e−5`. No accepted bound near
  `0.78010544`. The π interval passes its own audit but its decimal upward
  rounding is unrepaired.
- `K15-C018` **new**: the shell-allowance benchmark, stated exactly:
  `f̂ ≥ 0`, `f ≤ η` on `[2, ρ]`, `f ≤ 0` beyond `ρ`, count 12 ⟹
  `δ ≤ (4π/3)(f(0) + 12η)/f̂(0)`. Proof is K15-C003 + K15-C002b; `ρ = 209/100`
  is **pending** a Tammes-13 enclosure and E's repaired radial argument.
  Attributed to the Cohn–Elkies truncation mechanism, DLOV14, and
  Musin–Tarasov's computer-assisted truncation. Explicitly *not* a three-point
  SDP.
- `K15-C005r` **corrected twice**: the lattice identity is
  `S_f = c Σ_{ξ∈L*} f̂(ξ) − f(0) ≥ c f̂(0) − f(0)` (equality only if `f̂` vanishes
  on `L* ∖ {0}`); and the conclusion is narrowed to pointwise-sign hybrids.
- `K15-C010r`: `− o(1)` removed; the Jensen estimate is finite.
- `K15-C013`: angular lemma scope `0 ≤ δ ≤ √5 − 1`; boundary count corrected.
- `K15-C015` **refuted as a universal statement** (singleton at the icosahedral
  vertex contradicts `vol Ω ≥ √32`) and repaired as a specified-partition
  statement. The geometric avenue stays open.
- X's Gaussian driver: factor-`π` density error and HiGHS "Model error" misread as
  infeasibility; exact feasible point `P = 2 − 2s/3`, `Q = 1 + 2v/3` exists.
- `D13` adds claim-admission rules; `D14` fixes the portfolio at one benchmark
  plus one geometric target.

## Status of the two live candidates

| Candidate | Status | Blocking dependency |
| --- | --- | --- |
| Shell allowance `ρ = 209/100`, `η ≥ 0` (K15-C018) | `PROPOSED` benchmark | rigorous Tammes-13 enclosure for `ρ`; a certified Sturm/Gram evaluation |
| Constructive partition route (E, `K15-E004` after C015r) | `PROPOSED` target | specified partition + boundary estimate; analytic cluster-volume lower bound (sampling cannot establish it, `K15-E003`) |

## What is not claimed

No new bound. No certified CE value: C's numbers are `TESTED_FINITE` with
`min f̂` of order `10⁻⁶`, and Main's own grid script carries a known bug
(K15-C014r). No worker claim is called independently verified on the strength of
its own label.
