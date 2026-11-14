# RR127 claim ledger

Every row: exact statement and hypotheses, owner, reviewer, source, status,
evidence, unresolved obligations. Status vocabulary is the roadmap's:
PROPOSED | TESTED_FINITE | PROVED | LEAN_VERIFIED | REFUTED | BLOCKED.
Equal counts, a finite matching, a passing build or a fast implementation is
never used to promote anything above TESTED_FINITE.

## Current state table

| ID | Short statement | Status |
| --- | --- | --- |
| RR-C001 | Canonical interfaces and fixtures | PROVED (spec) + TESTED_FINITE |
| RR-C002 | `\|A_n\| = \|D_n\|` for `n <= 50`, six independent methods | TESTED_FINITE |
| RR-C003 | No weight-preserving bijection preserves the **length** | PROVED |
| RR-C004 | No weight-preserving bijection preserves the **largest part** | PROVED |
| RR-C005 | Staircase coordinates: order, nonnegativity, weight `n-k^2`, both laws | LEAN_VERIFIED |
| RR-C006 | Shift `T : D_n -> B_n` (smallest part >= length), both laws | TESTED_FINITE |
| RR-C007 | BZ82 reference map `A_n -> D_n`, proven inverse pair | TESTED_FINITE (n <= 50) |
| RR-C008 | BZ82 `psi` is an involution on `X(n) \\ {0} x A_n`, **all n** | **PROVED** |
| RR-C009 | BZ82 `phi` is an involution on `X(n) \ {0} x B_n` (reconstructed rule) | TESTED_FINITE (n <= 25) |
| RR-C010 | Equal largest-part cutoffs are **not** an identity (`n=5, m=4`) | PROVED (witness) |
| RR-C011 | BZ82 iteration length is Theta(n) empirically (max 646 at n=30) | TESTED_FINITE |
| RR-C012 | A "more natural" bijection meeting all criteria | OPEN |

## Details

### RR-C001 — interfaces and fixtures. Status: PROVED (definitional) + TESTED_FINITE.
Statement: the eight functions of D-1 with the stated domains; fixtures
`A_0=()`, `D_0=()`, `A_1=D_1={(1)}`, `A_2={(1,1)}`, `D_2={(2)}`,
`A_3={(1,1,1)}`, `D_3={(3)}`, `A_4=D_4` relation as tabulated in
`Literature/PROBLEM_SPEC.md`.
Owner M, reviewer X. Evidence: `Computation/rr_core.py`,
`Counterexamples/checker.py::check_regressions`, `Computation/results.json`
`fixtures`. Obligations: none; the table is definitional.

### RR-C002 — counts. Status: TESTED_FINITE.
Statement: for `0 <= n <= 50`, `|A_n| = |D_n|`, computed by (i) direct canonical
enumeration of `A_n`, (ii) direct canonical enumeration of `D_n`, (iii) unbounded
coin-change DP over allowed residues, (iv) the gap recurrence
`d(n,m)=d(n,m-1)+d(n-m,m-2)`, (v) the power series
`prod 1/((1-x^{5k+1})(1-x^{5k+4}))`, (vi) the series `sum_t x^{t^2}/(x;x)_t`;
plus (vii) a generic all-partitions filter for `n <= 20`. Methods (v) and (vi)
are independent of both recursions and are the analytic identity itself.
Owner C (worker m1, `smwfxwsqf`), reviewer M + X.
Evidence: `Computation/results.json` (`counts_all_agree = true`),
`.ultramath/smwfxwsqf/m1/d1_counts.tsv` (independent reproduction, identical).
First 31 values: 1,1,1,1,2,2,3,3,4,5,6,7,9,10,12,14,17,19,23,26,31,35,41,46,
54,61,70,79,91,102,117.
Obligations: none for the finite claim; **no all-n conclusion is drawn**.
Note: a widely quoted table value (55 at n=24) was checked and is wrong for this
family; all six methods agree on 54. Recorded to prevent a future regression to
the recalled table.

### RR-C003 — length cannot be preserved. Status: PROVED.
`A_2 = {(1,1)}` and `D_2 = {(2)}`, so any weight-preserving bijection sends the
length-2 object to a length-1 object. Immediate; PROVED given RR-C001.

### RR-C004 — largest part cannot be preserved. Status: PROVED.
For `n >= 2`: `(1^n) in A_n`; any `lambda in D_n` with `lambda_1 = 1` is `(1)`
or `()`, of weight <= 1; so `(1^n)` has no partner with a preserved largest
part. Verified with minimal witnesses at every `n <= 14` in
`Counterexamples/REGISTRY.md`. Owner M/X, source: original to this project.

### RR-C005 — staircase bridge. Status: **LEAN_VERIFIED**.
Statement (`Lean/Staircase.lean`): with `Pos` and `Gap` as defined there,
`(a) head_bound : 2*len(rest)+1 <= a` (so subtraction never truncates),
`(b) addStair_subStair : addStair (subStair l) = l`,
`(c) subStair_addStair : subStair (addStair l) = l`,
`(d) sum_addStair : (addStair l).sum = l.sum + l.length * l.length`,
`(e) weight_subStair : (subStair lam).sum = n - len*len` when `lam.sum = n`,
`(f) subStair_nonneg`.
Evidence: `lean RogersRamanujan/Lean/Staircase.lean`, exit 0, 14.4 s, and
`#print axioms` giving `[propext, Quot.sound]` for every theorem — inside the
event's allowed set, no `sorryAx`, no `Classical.choice`.
Owner L (Main this cycle), reviewer M/X. Obligations: weak-decreasingness of
`subStair` is established by the checker (RR-C006) but **not** in Lean; the
`Nat.Partition` bridge is not done; `T` is not formalized (D-4).

### RR-C006 — shift T. Status: TESTED_FINITE.
Statement: `T(lambda)_i = lambda_i - k + 2i - 1` is a weight-preserving bijection
from `D_n` onto `B_n` = {length `k`, smallest part `>= k`}, inverse
`lambda_i = b_i + k - 2i + 1`, and `T(lambda)_i = mu_i + k`.
Evidence: `results.json` `staircase_and_T.ok = true` for `n <= 50` (every
`D_n` object), `T(7,3,1) = (5,3,3)` specifically checked.
Obligations: needs RR-C005-style Lean proof for LEAN_VERIFIED.

### RR-C007 — the BZ82 reference bijection. Status: TESTED_FINITE, `n <= 50`.
Statement: `forward : A_n -> D_n` and `inverse : D_n -> A_n` as implemented in
`Computation/bz82.py` are mutually inverse bijections for every
`0 <= n <= 50`; forward is injective, surjective onto `D_n`, deterministic and
weight-preserving. Source: BZ82 pp.313-315, implemented from the scan, with the
one reconstructed rule of D-3.
Evidence: `Computation/results.json` `bz82_bijection` (all per-weight rows
`ok`), `Counterexamples/checker.py 30` -> `PASS`, 0 fails.
Owner C (m4 direction) + M, reviewer X.
Obligations: **no all-n proof**. In particular the termination argument for the
iteration is empirical (RR-C011), and the source reconstruction is not verbatim
(D-3). This is a *new implementation of established mathematics*, not a new
correspondence.

### RR-C008 — `psi` is an involution on `X(n) \ {0} x A_n` for **every** `n`. Status: **PROVED**.
Owner: C (worker m3, `smwfxwsqf`), reviewer M (refereed the written argument, not
only the run). Source: BZ82 p.314 with the three forced tie-breaks of D-3
(equality in I(a) -> I(a); equality in II(a) -> II(a); II(a) with value 0 ->
the part is deleted). Evidence: `.ultramath/smwfxwsqf/m3/README.md` §3 plus
Main's independent re-derivation.
Written argument, in outline. Put `P(j) = j(5j-1)/2`, so `P(j-1) = P(j)-(5j-3)`
and `P(j+1) = P(j)+(5j+2)`. (a) Each of the four branches changes `|lam|` by
exactly `-(change in P(j))`, so `|lam|+P(j) = n` is invariant, and every created
part is positive. (b) The rules fail to return a partition in exactly one
configuration: II(b) selected with `m0 = 0` and `j = 0`. Case II forces
`t0+j <= 0`, so `m0 = 0` means `t0 = 0` and `j <= 0`; with `j = 0` and II(b)
selected, `m3 < 3`, hence `m3 = 0`. Thus `lam` has no part `= 0,2,3 (mod 5)`,
i.e. `lam in A_n` — so the **domain is derived, not imposed**: it is precisely
`X(n) \ {0} x A_n`. (c) Each branch stays in its top-level case. (d) The branch
pairs `I(a)/I(b)` and `II(a)/II(b)` are mutually inverse; the two tie-breaks are
*forced* here, since equality occurs exactly when `m2` (resp. `m0`) is repeated.
Corollary (recorded, classical): since every orbit is a 2-element set with
opposite `(-1)^j` and the leftover states are exactly `A_n`,
`sum_{j in Z} (-1)^j p(n - j(5j-1)/2) = |A_n|`.
Main's independent confirmation of the same three tie-breaks: `psi^2 = id` with
0 defects over all 3198 in-domain states for `n <= 18` and over all in-domain
states for `n <= 25`; BZ82's three printed examples reproduce exactly.
Recorded correction to the worker's text: in II(a) with `nu = 0` the printed
bound `-13` is arithmetically `-10`; the conclusion still holds.
What this does **not** give: the analogous statement for `phi` (RR-C009), and any
conclusion about BZ82's endpoint map beyond `n <= 50`.

### RR-C009 — `phi` is an involution on `X(n) \ {0} x B_n`. Status: TESTED_FINITE, `n <= 25`.
`psi` is an involution with `psi^2 = id` and closure on `X(n) \ {0} x A_n` for
every such state with `n <= 25`; likewise `phi` on `X(n) \ {0} x B_n` under D-3.
Also both preserve the invariant `|lam| + j(5j-1)/2` and flip the parity of `j`
by construction. Evidence: `results.json` `involution_structure`, and the
2 692-defect negative control for the literal printed rule (D-3).
Obligations: an all-n proof of the involution property would settle RR-C007.

### RR-C010 — equal largest-part cutoffs are not an identity. Status: PROVED (witness).
At `n = 5`, cutoff `m = 4`: `{|lambda in A_5 : lambda_1 <= 4|} = 2`
(`(4,1)` and `(1,1,1,1,1)`) but `{|lambda in D_5 : lambda_1 <= 4|} = 1` (`(4,1)`).
So no refinement at equal largest-part cutoff can be proved by counting; it
needs its own correct boundary conditions. Confirms the roadmap's warning.

### RR-C011 — iteration length. Status: TESTED_FINITE (empirical only).
The number of `phi`/`psi` applications needed by the BZ82 map, per weight, has
max 0,0,2,2,6,8,10,14,16,16,10,42,58,42,90,124,128,140,110,196,224,208,228,344,
300,466,592,390,416,560,646 for `n = 0..30`, and mean growing roughly linearly
(114.6 at `n = 30`). This is measured, **not** proved; no lower bound is claimed
and PAK06's exercise about worst-case growth stays open here.

### RR-C012 — the objective. Status: OPEN.
No candidate has been exhibited that improves on BZ82 on the project's
naturalness criteria (rule count, auxiliary state, inverse recoverability,
termination, intermediate size, structural consequence). Remaining gap stated
precisely in `Main/RESULTS.md` section 5.
