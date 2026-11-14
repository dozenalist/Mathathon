# K15-REVIEW-0138 — X independent review (block 2)

Receipt `2026-11-14T10:04:35Z`; earliest finish `11:04:35Z`. Runtime: Ultramath (supervisor
verified). Branch `kepler15/counterexamples/run-01`. Audited tips: main `9461aae`, setup
`3c8ea4b`, experimental `ec66012`, comp `447da32`; target commits `96419eaa`, `4ea4e8b9`,
`6626714`.

## 1. Main's repaired `shell_check` — ACCEPTED on an independent 23-test battery

`Computation/shell_check.py` at `9461aae` is blob **`5619c1defd998d175d4ae2bea3ecb64b69c08f9a`**
(the defective revision at `6626714` was `a8526a8c322fc350c27557656d655e28a371a62b`). The repair
**is** pushed, and it rejects all three reported witnesses:
`le_on_interval([0,1,−1],0,0,1)`, `nonneg_on_half_line([0,−1,1])`, `_ray([0,1,−1],0)` all return
`False`, correct since `u−u² = +1/4` and `u²−u = −1/4` at `u = 1/2`.

**Mechanism, verified against the symptom.** Their `_count_roots_open` docstring says the old code
subtracted a root at `lo` instead of at `hi` when converting Sturm's `(a,b]` count to `(a,b)`.
That is exactly the reported failure: `u²−u = u(u−1)` has its root at `lo = 0`, so the erroneous
subtraction removed the *only* interior root and left the count at 0. The repaired version
additionally decides the sign with `P.intervals(eps=1e-8)` isolating intervals plus one rational
point in each gap between consecutive intervals — complete, because the sign is constant on each
gap and the interval endpoints are exact rationals.

**My battery** (`Reviews/x_adversarial_shellcheck.py`, reproduction below) — 23 tests, **0
mismatches**:

| family | cases | result |
| --- | --- | --- |
| the three reported witnesses | `u−u²`, `u²−u` on `[0,1]` / `[0,∞)` | correct (reject) |
| same shapes, true statements (over-rejection check) | `u²−u ≤ 0` on `[0,1]`; `−(u−1)² ≤ 0`; `−(u−5)² ≤ 0` on `[5,∞)` | correct (accept) |
| touching from **above** (must reject) | `(u−1)² ≤ 0` on `[0,2]`; `(u−5)² ≤ 0` on `[5,∞)` | correct (reject) |
| **irrational roots** | `u²−2` on `[0,1]` (accept) / `[0,2]` (reject) / `[3/2,2]` (reject); `2−u²` on `[0,∞)`; `u²−2` on `[2,∞)`; `(u²−2)²` (accept) | all correct |
| repeated roots | `(u−1)³`, `−(u−1)³` on `[0,2]` | correct |
| zero polynomial / constants | `0 ≤ 0` (accept), `−1 ≥ 0` (reject), `0 ≤ 0` on a ray | correct |

**A methodological point that cost me four wrong expectations.** While writing the battery I
mis-predicted four cases, all by confusing *"has a double root"* with *"satisfies ≤ 0"*: `(u−1)²`
touches zero from **above**, so it is `1` at `u = 0` and is **not** `≤ 0` on `[0,2]`; likewise
`−(u−1)³ = +1` at `u = 0`; and `u²−2 > 0` on `[3/2,2]` because `√2 < 3/2`. Every one of those was
my error and Main's code was right. The battery therefore now **verifies every "False"
expectation against an explicit witness value** before trusting it (see the automatic witness
block in the script). This is the same class of mistake that produced my earlier unsound
predicate and Main's earlier endpoint defect: the failure mode is human, and the mitigation is
witness-anchored expectations rather than intuition.

**Scope statement, which the review rightly insisted on.** Accepting `5619c1d` certifies *the
predicate implementations* on the families above. It does **not** make the K33 bound rest on
checker agreement: `K33`/`K33b` are valid because Computation's strict and independent SymPy
checks passed locally **and** because their sign structure is decidable by hand
(`p` has one real root below `8π`, `q` has one real root, negative). **Particular valid K33
coefficients are one thing; generic checker soundness is another, and I keep them separate.**

Reproduction: `cd KeplerConjecture/Counterexamples/Reviews && python3 x_adversarial_shellcheck.py
shell_check_9461aae.py` (exit 0 iff 0 mismatches).
