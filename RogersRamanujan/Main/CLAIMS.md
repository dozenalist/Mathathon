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
| RR-C002 | Equality `|A_n| = |D_n|` for `n <= 50`; method independence stated honestly | TESTED_FINITE |
| RR-C003 | No weight-preserving bijection preserves the **length** | PROVED |
| RR-C004 | No weight-preserving bijection preserves the **largest part** | PROVED |
| RR-C005 | Staircase **equivalence**: order, both inverse laws on the correct subtypes, length retained, padding explicit | **LEAN_VERIFIED** (4.35.0 for the base module; order module on 4.33.1 only) |
| RR-C006 | Shift `T : D_n -> B_n` (smallest part >= length): **bijection**, both laws | **LEAN_VERIFIED** (4.33.1; pin pending) |
| RR-C007 | BZ82 reference map: our implementation is a bijection `A_n -> D_n` | TESTED_FINITE (n <= 50); BZ82's theorem is PROVED in the literature |
| RR-C008 | BZ82 `psi` involution on `X(n) minus {0} x A_n`, **all n** | **PROVED (amended, independently audited, gap list empty)** |
| RR-C009 | BZ82 `phi` involution on `X(n) minus {0} x B_n`; **faithful transcription, no reconstruction** | TESTED_FINITE (`n <= 30`) |
| RR-C010 | Equal largest-part cutoffs are **not** an identity (`n=5, m=4`) | PROVED (witness) |
| RR-C011 | BZ82 alternating-path lengths: raw max/mean per weight, extremal objects | TESTED_FINITE (no growth class claimed) |
| RR-C013 | **Theorem F**: closed form for the all-ones ray $(1^s)$ under BZ82, 4 of 5 residue classes | **PROVED** (written case analysis; endpoints verified `s<=60` by Main) |
| RR-C014 | **Theorem G**: closed forms for the all-fours ray $(4^r)$ | **PROVED** (same caveat) |
| RR-C015 | $(1^s)$ with $s\equiv0\ (5)$, $s\ge30$: **provably** not closable in 2 steps; measured path lengths 44–672 | **PROVED** (lower bound) + TESTED_FINITE (lengths) |
| RR-C016 | Candidate mechanisms M1 (collapse-and-singleton), M2 (free window) | OPEN; neither meets the objective |
| RR-C018 | **Lemma CI**: `phi` Case I maps into Case II; `a' = a-1`; `mu' >= mu` | PROVED (weight, `a'=a-1`) + TESTED_FINITE (`weight<=26`) |
| RR-C019 | BZ82's printed `mu_bar > mu` is **false**; the correct statement is `>=`, equality iff `lam(a)=lam(a+1)` | **REFUTED** (5 844 of 10 285 Case-I states, first `(-1;())`) |
| RR-C020 | **Theorem 1/2/3**: `phi` and `psi∘phi` closed forms on the **whole** family `(4^r,1^s)`, plus Lemma 2 (excluded set) | **PROVED** |
| RR-C021 | **R2 slot identities** (R2.1 multiset, R2.2, and both Case-I duals) verified; all-input proof open | TESTED_FINITE (widened in cycle 4) |
| RR-C022 | `phi` obligations: `N >= 0`, both deletions valid, `a != mu` in Case I, `p2 >= 0` (**sharp**: attained), weight identity | **PROVED** (all `n`) |
| RR-C026 | Dead code retired: `phi` Case I never deletes one slot twice | **PROVED** (2 routes) + 0 hits in 1 746 369 states |
| RR-C023 | `(4^r,1^s)` cost: 21 of 80 parameters exceed a 20 000-step cap (finite chains to 18 702) | TESTED_FINITE |
| RR-C024 | Conjecture P2: `b(4^2,1^s)` shape for `s≡2 (5)` | CONJECTURE (80 parameters, 0 failures) |
| RR-C025 | P3 shape at `r=3` | **REFUTED** (fails at `s=62`, corrected witness) |
| RR-C012 | A "more natural" bijection meeting all criteria | **OPEN** |

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
plus (vii) a generic all-partitions filter for `n <= 20`.

**Independence, corrected in cycle 2.** Cycle 1 called these "six independent
methods", which overstates it. (iii) and (v) are the *same* recurrence (same
objects, same order of summation), so they cross-check transcription, not
mathematics. The genuinely independent groups are: {direct enumeration of `A_n`
and of `D_n` — different families, different generators}, {(iii)=(v)}, {(iv)},
{(vi)}, {(vii)}. The comparison that carries real mathematical content is
`(v) = (vi)`, whose equality *is* the Rogers--Ramanujan first identity, checked
coefficient by coefficient; and (vii), which enumerates unconditionally and then
filters. Note also that (vi) counts the `B_n` side, so agreement of (vi) with
(i)-(iv) is the identity, not a tautology.
Owner C (worker m1, `smwfxwsqf`), reviewer M + X.
Evidence: `Computation/results.json` (`counts_all_agree = true`),
`.ultramath/smwfxwsqf/m1/d1_counts.tsv` (independent reproduction, identical).
First 31 values: 1,1,1,1,2,2,3,3,4,5,6,7,9,10,12,14,17,19,23,26,31,35,41,46,
54,61,70,79,91,102,117.
Obligations: none for the finite claim; **no all-n conclusion is drawn**.
Cycle-2 correction: cycle 1 asserted that a "widely quoted" table value (55 at
`n = 24`) is wrong. That assertion had no source and is withdrawn. What is true
is narrower and verifiable: the hand-recalled array that cycle 1 carried inside
`rr_core.py` as a cross-check disagrees with every method implemented here, and
that array has been **retired** rather than corrected, because this project has
no citation for the sequence's offset or convention. No remembered table is used
as an oracle anywhere in the code now.

### RR-C003 — length cannot be preserved. Status: PROVED.
`A_2 = {(1,1)}` and `D_2 = {(2)}`, so any weight-preserving bijection sends the
length-2 object to a length-1 object. Immediate; PROVED given RR-C001.

### RR-C004 — largest part cannot be preserved. Status: PROVED.
For `n >= 2`: `(1^n) in A_n`; any `lambda in D_n` with `lambda_1 = 1` is `(1)`
or `()`, of weight <= 1; so `(1^n)` has no partner with a preserved largest
part. Verified with minimal witnesses at every `n <= 14` in
`Counterexamples/REGISTRY.md`. Owner M/X, source: original to this project.

### RR-C005 — staircase bridge. Status: **LEAN_VERIFIED** (pinned compiler, externally re-checked).
Statement (`Lean/Staircase.lean`): with `Pos` and `Gap` as defined there,
`(a) head_bound : 2*len(rest)+1 <= a` (so subtraction never truncates),
`(b) addStair_subStair : addStair (subStair l) = l`,
`(c) subStair_addStair : subStair (addStair l) = l`,
`(d) sum_addStair : (addStair l).sum = l.sum + l.length * l.length`,
`(e) weight_subStair : (subStair lam).sum = n - len*len` when `lam.sum = n`,
`(f) subStair_nonneg`.
Evidence, primary: the supervisor compiled the identical file (SHA256
`C7ACBCD74866958596ACC458A7231939EBE01969A0723179BFDAAF263CBEB280`) with the
**pinned** Lean 4.35.0 executable (commit `eb6cafb7290e8bd5f2937522d8d804f58f02bafc`),
exit 0, and reports the exact axiom output: `subStair_addStair` uses
`[propext]`; `head_bound`, `addStair_subStair`, `sum_addStair`,
`weight_subStair`, `subStair_nonneg` use `[propext, Quot.sound]`. This is inside
the event's allowed set, with no `sorryAx`. Main's own local check used Lean
4.33.1 (the VM's executable) and gave the same axiom sets; the toolchain
mismatch is therefore resolved in favour of the pinned compiler, and the `4.33.1`
caveat is retired.
**Scope, corrected in cycle 2.** These six declarations do **not** constitute a
staircase *equivalence*. Two things were overstated in cycle 1:
(i) weak-decreasingness of `subStair` is still missing in Lean — it is verified
only computationally (RR-C006) — so "the staircase coordinates form a partition"
is not yet kernel-checked;
(ii) `subStair_nonneg` proves `0 <= x` for a `Nat`, which is automatic and
carries no content; the substantive non-truncation evidence is `head_bound`
together with `addStair_subStair`, not nonnegativity.
Owner L (Main cycle 1), reviewer: the supervisor's independent compilation, plus
X. Obligations: the order lemma; `T`; the `Nat.Partition` bridge (D-4); and a
named build target so these modules are actually compiled by the reported build.

### RR-C006 — shift T. Status: **LEAN_VERIFIED** (Lean 4.33.1; pinned-4.35.0 run pending).
Statement: `T(lambda)_i = lambda_i - k + 2i - 1` is a weight-preserving bijection
from `D_n` onto `B_n` = {length `k`, smallest part `>= k`}, inverse
`lambda_i = b_i + k - 2i + 1`, and `T(lambda)_i = mu_i + k`.
Evidence, computational: `results.json` `staircase_and_T.ok = true` for `n <= 50`
(every `D_n` object), `T(7,3,1) = (5,3,3)` checked.

**Formalized in cycle 3** (`Lean/ShiftT.lean`, integrated by Main from cycle-3
worker m2's `Lean/cycle3/`). Encoding: `shiftT l = (subStair l).map (· + l.length)`
and `shiftInv l = (addStair l).map (· - l.length)`, i.e. `T(lam)_i = mu_i + k`
*by construction*, so that obligation is definitional; faithfulness to the
contract's formula `T(lam)_i = lam_i - k + 2i - 1` is checked against Python, not
assumed. Main's own verification:
* `lean RogersRamanujan/Lean/ShiftT.lean` exit 0, 0 errors, **no `sorryAx`**;
  the worker's 41 `#print axioms` directives print 40 results — 33 with axioms
  (`[propext]` 7, `[propext, Quot.sound]` 26) and 7 with none — all inside the
  event's allowed set;
* `python3 Lean/cycle3/check_encoding.py` exit 0, **10 checks, 0 FAIL**,
  197 `D`-objects and 197 `B`-objects at `n <= 20`. Key rows: `shiftT` equals the
  integer formula on all of `D_n`; image `⊆ B_n`; weight preserved; injective;
  both inverse laws; and **`T(D_n) = B_n` as sets for every `n <= 20`** — i.e.
  surjectivity, so this is a bijection and not merely an injection;
* Main **kernel-checked the three hypothesis-necessity witnesses** in a separate
  file: `(shiftT [1,3]).sum ≠ 4` with `[1,3]` `Pos` but not `Gap` (so `Gap` is
  needed for weight preservation); `shiftT [0] = shiftT [1]` (so `Pos` is needed
  for injectivity); and `shiftInv [2,5] = [3,4]` which is `¬ Gap`, with `[2,5]`
  `¬ WeakDec` (so the entry bound alone does not land in `D_n`). All exit 0.
* Also present: `weakDec_shiftT`, `shiftInv_pos`, `shiftInv_gap`, and the subtype
  bijection `toB : DGap -> BSmall` with `toD_toB`, `toB_toD`, `weight_toB`.

**Toolchain, stated precisely:** this module is verified on the VM's Lean
**4.33.1** only. The pinned 4.35.0 is not installed here. So RR-C006 is
**LEAN_VERIFIED modulo the pin**, i.e. Lean-conditional on running this file on
4.35.0, exactly as RR-C005's `StaircaseOrder` module was until the supervisor
compiled it. `lake build RogersRamanujan` with this module has **not** been run
(no `.lake` checkout in this container).
**Note:** `ShiftT.lean` as delivered inlined a verbatim copy of `Staircase.lean`,
which would make it unimportable alongside the original; Main replaced that with
`import RogersRamanujan.Lean.Staircase` and added it to the aggregator
`RogersRamanujan.lean`, which now compiles exit 0.

### RR-C007 — the BZ82 reference bijection. Status: TESTED_FINITE for our
implementation, `n <= 50`; the underlying theorem is PROVED in the literature
(BZ82 p.314) and is attributed, not claimed.

Three distinct things, kept separate in cycle 2 (cycle 1's "proven inverse pair"
blurred them): (1) **BZ82's theorem** that the alternating composition is a
bijection — established mathematics, cited, not ours; (2) **our implementation**
of it, verified as a bijection over a finite range — TESTED_FINITE; (3) a
**source-faithfulness proof** — cycle 2 supplies the missing independent evidence:
worker m3 wrote a separate implementation from the scan **without reading
`bz82.py`**, and `compare_bz82.py 30` reports `phi 66658, psi 66658, domains
67551+67551, forward 893, onto-D 31/31, examples 3` with **DISCREPANCIES: 0**.
Two independent readings of the same three-page note therefore agree
object-for-object across 66 658 states in each involution and all 31 weights.
(Also confirmed at `n <= 40`: 541 114 states, 0 discrepancies.) This is strong
but still finite evidence — it is not a written proof that the code implements
the rules on all inputs, so RR-C007 stays TESTED_FINITE with the independence
now documented rather than asserted.
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
AMENDED AND AUDITED IN CYCLE 2. The supervisor found two real boundary errors in
the cycle-1 argument; worker m1 (direction B) wrote the amended all-`n` proof in
full (`Counterexamples/cycle2/AMENDED_PROOF.md`) and Main refereed it, re-deriving
every new lemma by machine. **The gap list is empty.** Four items beyond the
supervisor's two:
 * **E3** `II(a)` is never selected with `m3 = 0`: the guard would give
   `nu = 5j-3 >= m0 >= 0`, i.e. `j >= 1`, against `j <= 0` (Lemma 1.1). So
   "replace the part `m3`" always acts on a real part, and `nu` is a
   `0 (mod 5)` value, hence `m2' = m2 = 0`. **Verified: 0 occurrences.**
 * **E3'** `I(b)` is never selected with `m2 = 0`, which makes its multiplicity
   `k = (m2-N-5)/5` a non-negative integer. **Verified: 0 occurrences.**
 * **Sharp forms**: `t0' = t0-1` **iff** `m0 > 0`; `m3' = m3` **iff** `m3` is
   repeated; and `m3' <= m3-5` also fails for `m3 = 3` simple, not only for
   repeated maxima — so the corrected bound `m3' <= m3` is the right one.
 * A 14-row census of every virtual-zero and multiplicity case ships with the
   proof (`psi_audit.py`, 0 failures over the domain for `n <= 30`: `Dom` 66 658,
   `I(a) = I(b) = 29 924`, `II(a) = II(b) = 3 405`, `II(b)` with `m0 = 0` in
   1 949, `II(a)` with `nu = 0` in 1 949 of which 980 have `m3` repeated).
 * Repair 1 (case stability, II(b)). `t0' = t0 - 1` is **false when `m0 = 0`**:
   then no part is removed, a part `= 3 (mod 5)` is created, and `t0' = t0 = 0`,
   e.g. `(-1;()) -> (0;(3))`. Separate argument for that case: `m0 = 0` gives
   `t0 = 0`, and Case II gives `t0 + j <= 0`, i.e. `j <= 0`. If `j = 0` then
   `m0 = m2 = 0`; II(b) selected means `m3 - 3 < 0`, so `m3 = 0`; hence `lam`
   has no part `= 0,2,3 (mod 5)` and the state is in the excluded set. So on the
   domain `j <= -1`, and `t0' + j' = 0 + (j+1) <= 0` as required.
 * Repair 2 (branch inverse, II(a) with `nu = m3+5j-3 = 0`). The bound
   `m3' <= m3 - 5` is **false when the largest `3 (mod 5)` part is repeated**:
   `(0;(3,3)) -> (-1;(3))` keeps `m3' = 3`. The weaker bound `m3' <= m3`
   suffices: `m3' + 5(j-1) - 3 <= m3 + 5j - 8 = nu - 5 = -5 < 0 = m0'`, so II(b)
   is selected, and it creates `m0' - 5(j-1) - 2 = 3 - 5j = m3`, restoring the
   part. Multiplicity variants of both witnesses are exercised in the audit.

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
The tie-breaks themselves are **forced**: flipping any one of them gives 1120 or
374 failures at `n <= 18` with explicit witnesses (RR-X006, DECISIONS D-3a). That
is what makes step (d) a statement about BZ82's map and not about a variant.
Phrasing correction: the orbits are 2-cycles and never reach `{0} x A_n`; the
correct claim is the decomposition `X(n) = ({0} x A_n) ⊔ 2-cycles`.
Recorded correction to the worker's text: in II(a) with `nu = 0` the printed
bound `-13` is arithmetically `-10`; the conclusion still holds.
What this does **not** give: the analogous statement for `phi` (RR-C009), and any
conclusion about BZ82's endpoint map beyond `n <= 50`.

### RR-C009 — `phi` is an involution on `X(n) \ {0} x B_n`. Status: TESTED_FINITE, `n <= 30`.
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

### RR-C011 — alternating-path lengths. Status: TESTED_FINITE. No growth class claimed.
Cycle 1 wrote "`Theta(n)` empirically" and "roughly linearly". Both are withdrawn:
a maximum of 646 steps at `n = 30` over 31 data points cannot support a growth
class, and the mean is not a linear function of `n` (it is not even monotone in
the max, e.g. max falls from 16 at `n=9` to 10 at `n=10`, and from 592 at `n=26`
to 390 at `n=27`). What is recorded is raw data only:

* max steps for `n = 0..30`: 0,0,2,2,6,8,10,14,16,16,10,42,58,42,90,124,128,140,
  110,196,224,208,228,344,300,466,592,390,416,560,646;
* mean steps for `n = 0..30`: 0,0,2,2,3,5,4,8,7,6,4.333,12.571,15.778,18,20.667,
  21.143,26.824,31.579,34.261,38.615,41.29,47.314,53.463,60.043,65.926,73.738,
  80.029,88.658,96.484,106.255,114.564;
* extremal `A_n` objects (longest path): `n=10` `(6,1,1,1,1)`; `n=20`
  `(11,6,1,1,1)`; `n=30` `(4,4,4,4,4,4,4,1,1)`.

**Correction (cycle 3).** Cycle 2 wrote that both of the last two "start in the
two-parameter family `(4^r,1^s)`". Checked: `(4,4,4,4,4,4,4,1,1) = (4^7,1^2)` **is**
in that family, but `(11,6,1,1,1)` is **not** — it lies in `A_20` and is a
genuine extremizer, but it is not of the form `(4^r,1^s)`. So the `n = 30`
extremizer alone motivates that family; inferring a common parametric family
from two extremizers was unjustified. A second valid family to test is
`(6^r,1^s)` (weight `6r+s`), which contains `(6,1,1,1,1)`. PAK06's exercise on
worst-case growth stays open. Two complete
labelled traces (longest and shortest at `n = 12` and `n = 20`, with the
involution applied at each step) are in `results.json` under `extremal_traces`.

### RR-C012 — the objective. Status: OPEN.
No candidate has been exhibited that improves on BZ82 on the project's
naturalness criteria (rule count, auxiliary state, inverse recoverability,
termination, intermediate size, structural consequence). Remaining gap stated
precisely in `Main/RESULTS.md` section 5.

### RR-C013 — Theorem F: a closed form for the all-ones ray. Status: **PROVED**
(cycle-2 worker m4, `Experimental/cycle2/PROOF_families.md`), with a stated caveat.

For $s\ge3$ one application of $\varphi$ collapses the ones-ray:
`varphi(0;(1^s)) = (-1;(s-3))`. All remaining work is `psi` on a *singleton*,
which is closed form in all five residue classes of $p \bmod 5$ (Lemma 1), with
one class needing a six-step chain (Lemma 2). The D-side images

$$b(1^s)=\begin{cases}(s) & s\equiv3\\ (s-2,2) & s\equiv2,4\\ (s-4,4) & s\equiv1,\ s\ge11\\ (6+k-2i),\ k=s/5 & s\equiv0,\ s\le25\end{cases}$$

with exceptions $s=4\mapsto(3,1)$, $s=6\mapsto(4,2)$ and $s=2\mapsto(2)$.

**Scope of the length bound (corrected in cycle 3).** Path length `<= 6` is
claimed only for the residue classes in which the closed form is *derived*, i.e.
`s = 1,2,3,4 (mod 5)`. It is **not** a claim about `s = 0 (mod 5)`, where the
measured lengths are 2 for `s <= 25` but 220, 574, 124, 452, 44, 454, 672 for
`s = 30,35,40,45,50,55,60`. Cycle 2 stated a blanket "`<= 6` throughout" for
`s <= 60`, which contradicts its own multiples-of-five table; that blanket claim
is withdrawn.

**Main's independent verification.** Computed `forward((1^s))` for every
$s\le60$ with the committed `bz82.py` and compared to the formula: **every value
matches**. Path lengths are 2 for the generic classes and 6 for $s\equiv1\ (5)$,
$s\ge11$.
**Correction to the worker's report:** the $s\equiv2,4$ formula also fails at
$s=2$ (actual image `(2)`); the report lists only $s=4,6$ as exceptions, so the
prose exception list is incomplete even though their harness reports 0
mismatches to $s=120$.
**Scope caveat, stated rather than implied:** I verified the *endpoint values*
and read the case structure; I did **not** referee each QED of Lemmas 0–2 line by
line. So PROVED here means "written residue-class case analysis, independently
value-checked", not "fully refereed".

### RR-C014 — Theorem G: the all-fours ray. Status: **PROVED** (same caveat).
`varphi(0;(4^r))` is undefined for $r\le4$ — because $(4^r)\in 0\times B(n)$, since
its smallest part 4 is at least its length — then equals
`(1;(5^{r-2},1^{8-r}))` for $5\le r\le8$ and `(-1;(r-6,3,3^r))` for $r\ge9$.
Verified exactly for $r\le12$ by Main, including the merge of the leading $r-6$
into the threes at $r=9$.

### RR-C015 — where BZ82's cost actually lives. Status: PROVED lower bound + measured.
For $s\equiv0\ (5)$ the two-step output is $(5^{s/5})$, which lies in $B(n)$ iff
$5\ge s/5$, i.e. **iff $s\le25$**. So for $s\ge30$ in this class the endpoint is
**not reached in two steps**.

**Exact statement, and what it is not (cycle 3).** The proved content is a
*$>2$ lower bound* on the path length for `s = 5k, k >= 6`. It is **not** a claim
that the length is asymptotic to anything, superconstant, or growing at any
particular rate. The measured lengths
`220, 574, 124, 452, 44, 454, 672` for `s = 30,35,40,45,50,55,60` are *data*, and
they are non-monotone, so no growth statement is supported. Measured lengths for
the other classes are `<= 6` up to `s = 60`; that is likewise a finite
observation about those classes, and the `<= 6` bound is only *derived* for
`s = 1,2,3,4 (mod 5)`.

The honest summary: the all-ones ray has a proved closed form with path length
`<= 6` in four residue classes, and in the fifth the two-step route is provably
blocked from `s = 30` on, with the endpoint then reached by other routes at
measured lengths between 44 and 672. Where the truth lies in that fifth class is
**open**. This is the first result in the project that locates BZ82's cost
structurally rather than tabulating it: the all-ones ray is closed-form and cheap
in four classes and provably expensive in the fifth. It does **not** give a new
bijection and does not bear on the objective directly.

### RR-C016 — candidate mechanisms. Status: OPEN, neither meets the objective.
M1 (collapse-and-singleton) and M2 (free window, reaching 7.8% of $A_n$ objects)
each have a forward rule, recoverable inverse, admissible set, invariant and
termination measure, and each is blocked by one named lemma (L-M1: the natural
continuation fails on $B$-membership `5 >= k`). Worker m4 states plainly that
neither meets the objective; that assessment is accepted. Also **refuted** on
held-out parameters: $b(5k)=(5^k)$ for $k\ge6$ (7/7 fail), $b(5k)$ affine in
$k$, $\mathrm{len}(b(4^r))\le2$ (fails at `r=7`), and $\kappa$ a function of
$s\bmod5$. No rule was found for `(4^r,1^s)`. Also corrected: `(5^k)` is **not**
in `A_n` for `k > 0` (since `5 = 0 (mod 5)`), so it is not a residue family to
test; it appears only as an *intermediate* state on the all-ones ray.

### RR-C017 — Implementation trap in `phi` Case I: the two deletions are indexed against the original list.
Status: **PROVED by witness** (cycle-2 worker m3, F2; confirmed and quantified by Main).

BZ82 says "delete the parts `lambda(a)` and `lambda(mu)`". A natural
implementation deletes position `a`, then position `mu` — but the list has
shortened, so the second index is stale and a different part is removed. This
silently breaks weight preservation: Main implemented the trap and found 172
differing states at `weight <= 25`, **every one of them with weight broken**,
first witness `(-1;())` giving `(0;(1,1,1,1))` instead of the correct `(0;(1,1,1))`.
Worker m3 reports 371 witnesses (presumably over `weight <= 30`); the phenomenon
and the minimal witness agree.

Recorded because it is the second time in this project that a plausible local
operation was a silent error — the first was Main's own `z >= 1` restriction in
`phi` Case II (RR-X005). Both are the same failure mode: a local operation that
looks forced but is not, with the damage showing up only in weight or an
involution law. `Computation/bz82.py` collects both slots before removing them,
which is why it was never affected.

### RR-C021 — the slot identities R2. Status: **TESTED_FINITE**.
**This row said PROVED in cycle 3 and that was wrong.** Two independent reasons,
both Main's error rather than the worker's:

1. **The worker never claimed it proved.** `Counterexamples/cycle4/PROOF_PHI_OBLIGATIONS.md`
   (verbatim copy of the cycle-3 artifact, now committed) states for obligation
   (v): "**NOT PROVED**; reduced to R2 (slot-level inverse recipe), 0 failures
   finitely", and its section 8 heading reads "R2 ... Not proved here". Main
   promoted it to PROVED on the strength of its own 10,285-state check alone.
2. **Main checked only a fragment.** The full R2 is three multiset identities plus
   their Case-I duals:
   ```
   (R2.1)  { pad(lam',a'), pad(lam',mu') } = { m, p2 }        (multisets)
   (R2.2)  N' := L' + lam'(mu') - 5j' - t*' = #{ i : lam_i = 1 }
   (R2.3)  { pad(lam',x) - 1 : x a surviving slot } = { lam_i - 1 : lam_i >= 2 }
   (R2.1') { m', p2' } = { L, lam(mu) }                       (Case I -> II dual)
   (R2.2') #{ x in lam' : x = 1 } = N
   (R2.3') { lam'_i - 1 : lam'_i >= 2 } = surviving slot values of s
   ```
   What Main verified is the worker's *sharpenings* `R2.1''` — positionally,
   `lam'(a') = m` and `lam'(mu') = p2` — over all 10 285 Case-II states of
   `weight <= 26`. That is one inequality pair inside R2.1; it does not establish
   R2.2, R2.3, or any of the Case-I duals, and it does not name the multiset
   identity with its `0`-entry and virtual-slot cases.
   The worker had already checked `R2.1''` more widely (541 114 states at
   `weight <= 40`, plus 296 795 random in-domain states), so Main's check was a
   weaker re-run, not independent confirmation of the whole.

**What the `0`-entry issue is.** `(R2.1)` must be a *multiset* identity because a
created part can be `0`, and a created `0` is carried by a **virtual slot**: the
witness `(0;(1,1,1)) -> (-1;())` has both created values `0`, and Case I applied
to `(-1;())` deletes the two virtual slots at `a' = 1, mu' = 2`. A statement only
about positive parts misses this case entirely.

**Dependency, stated so the circle is visible.** `R2.1''` refers to `a'` and
`mu'`, which are defined by recomputing the parameters at the image; and the
`a`-shift facts (Lemma CI.2 and CII, themselves TESTED_FINITE) are stated in terms
of `a'`. So R2 and the shift currently cite each other's vocabulary. Breaking that
circle — defining `a'` intrinsically at the image rather than through the shift —
is part of what a proof of R2 must do.
**Cycle-4 widening of the finite evidence.** Beyond the `R2.1''` fragment above,
Main has now checked, over all in-domain states of `weight <= 23` (6 224 Case-II and
6 224 Case-I states, 0 failures in each group):
* **(R2.1) as a multiset**, with virtual slots (`pad(lam',x) = lam'_x` for
  `x > len(lam')`): `{pad(lam',a'), pad(lam',mu')} = {m, p2}`;
* **(R2.2)**: `N' = L' + lam'(mu') - 5j' - t*'` equals `#{i : lam_i = 1}`;
* **(R2.1')**: `{m', p2'} = {L, lam(mu)}` for the Case-I image, recomputing `m', p2'`
  from the image;
* **(R2.2')**: `#{x in lam' : x = 1} = N`.
So the whole of R2.1/R2.2 in both directions is now supported finitely, not just one
inequality pair. (R2.3 and R2.3' were not re-checked here.)

**Why the multiset form is the right one — a proof hint, not a proof.** A created
part may **tie** with a decremented part (e.g. `lam_i - 1 = m`), and it may be `0`
and live in a virtual slot. A positional statement then has to say *which copy* sits
at `a'`, which is ill-defined under ties. The multiset statement is invariant under
that ambiguity, so it is exactly the form that survives ties; and since Case I
deletes **both** slots, order is irrelevant to the involution. This suggests the
proof should proceed through the multiset and never through sorted positions — and it
explains why the positional sharpening `R2.1''` is a *consequence* on the tested
range rather than the natural hypothesis.
**Obligation:** an all-input proof of (R2.1), (R2.2) and their duals, plus R2.3/R2.3',
with the tie and virtual-slot cases handled as above, independently reviewed.

### RR-C022 — `phi`'s definedness obligations. Status: PROVED for all `n`.
From cycle-3 worker m4, with Main's checks:
* the Case-I inserted count `N = L + lam(mu) - 5j - t*` is `>= 0` *by Case I's own
  guard*, so no separate argument is needed;
* both deletions are valid, and `a != mu` in Case I. Proof (m4's, cleaner than
  Main's MX.5): if `a = mu` then `2j = L`; `a <= t` gives `L >= 1` so `j >= 1`,
  while Case I with `lam(mu) = L = 2j` gives `4j >= 5j + t*`, i.e. `t* <= -j <= -1`,
  contradicting `t* >= 1`. If `a > t` then `L = 0`, `mu = a+2j`, and `a = mu` forces
  `j = 0`, which with `a > t` makes `lam` lie in `B` and hence off the domain.
  **Caveat that matters:** `a = mu` *does* occur in Case II (6 458 states at
  `weight <= 30`, e.g. `j=1, lam=(2,)`); the restriction to Case I is essential.
* `p2 = t+5j-3-m >= 0` follows from `m <= R` (because `m + lam(k-m) <= R` and
  `lam >= 0`) together with the Case-II dichotomy excluding `m = R`;
* signed weight is preserved by an explicit identity (Lemma CI.1).
**Not proved:** case stability and `phi^2 = id`, now reduced to R1 (explicit
inequalities) plus RR-C021.

**RR-C022(i) in full, and why it is short** (cycle-3 worker m3, propositions
checked by Main over 13 124 in-domain Case-II states — 9 assertions, 0 failures).
Since `t+5j-3 = R-1`, obligation (i) is exactly `m <= R-1`. Put
`f(z) = z + lam(k-z)` on `0 <= z <= k-1`. Both indices lie in `[1,k]`, so `f` is
strictly increasing there — but `f` **steps down at `z = k`** because `lam(0) = 0`,
so the interval cannot be extended; that is the trap in any slicker argument.
* If `k <= t` then `lam(k) >= 1`. If `R <= k-1` then `f(R) >= f(0) + R >= R+1 > R`,
  so `R` is not admissible, and neither is any `z > R`; hence `m < R`.
* If `k > t` then `j >= 1` (from `a <= max(t+1, 1-2j)`). With `a <= t` one gets
  `R-(k-1) = t+3j-a >= 3`; with `a = t+1` one gets `3j-1 >= 2`. Either way
  `m <= k-1 <= R`.
So `m <= R-1` and `p2 = R-1-m >= 0`.
**The bound is sharp**, not slack: `slab_c3.py` finds `p2 = 0` attained at
`j=-4, lam=(1^23)`.

**RR-C026.** `a = mu` cannot occur in Case I, so the two deletions always act on
distinct slots. Two independent arguments (Main's MX.5; the worker's shorter route
via `2j = L`) and two independent censuses (Main's 6 458 hits all in Case II;
the worker's 0 hits in 1 746 369 states) agree. The defensive fallback in
`Computation/bz82.py` Case I was therefore dead code and is now an **assertion**.

### RR-C020 — closed forms on the whole `(4^r,1^s)` family. Status: PROVED.
Cycle-3 worker m1. `t = r+s`, `j = 0`, and `phi` is closed form on all four regimes
(`r = 0`; `1 <= r <= 4` split at `t <= 5`; `r >= 5` split at `t <= 8`), with
`a != mu` throughout, created parts nonnegative, and inserted count nonnegative;
`psi ∘ phi` is closed form on the complete 20-element Case-I parameter set; and for
`r = 1` the full endpoint is reached in two steps.

**Main's independent check:** re-implemented all four regimes and compared with the
committed `bz82.py` for `r <= 10`, `s <= 25` — **280 of 280 agree**. (A first pass
showed one mismatch at `r=0, s=3`; that was Main's encoding slip — the tuple `(0,)`
against BZ82's zero-part convention — so the statement is right but the proof text
should state the vanishing-part convention explicitly.) Lemma 2 is confirmed
exactly: `()`, `(1)`, `(4^r)` for `1 <= r <= 4` are outside `phi`'s domain, `(4^5)`
is inside — so RR-C014's `r <= 4` is *derived*, not assumed.

### RR-C023 / RR-C024 / RR-C025 — cost, conjecture, refutation.

**B versus D: the distinction this section must preserve.** `B_n` is the set of
partitions whose *smallest part is at least their length*; `D_n` is the set with
*successive gaps at least 2*. They are different sets and `B_n` is **not**
`D_n`; `T : D_n -> B_n` (RR-C006) is what connects them. A `B`-object need not
have any gap property: `(25,17,8,8,8,8)` has adjacent differences
`8,9,0,0,0` and is a perfectly valid member of `B_74` (length 6, smallest part
8 >= 6). Every claim below names which side it is on.

* **RR-C023 (cost, TESTED_FINITE).** On the family `(4^r,1^s)` — the first family
  with more than one object per weight — BZ82 is expensive in some classes but not
  all: for `r = 1`, `s ≡ 0,4 (5)`, 21 of 80 parameters exceed a 20 000-edge cap,
  with the largest *finite* measured traces 18 702 and 15 452
  **involution edges** (states = edges + 1). Some classes are cheap (the
  `r = 1`, `s ≡ 1,2,3 (5)` formulas take two edges). So the correct statement is
  that cost varies enormously across the family and is *not* uniformly high;
  every number here is a measured trace length under a cap, not a complexity
  bound, and a cap is an unresolved case, not a proof of non-termination.
* **RR-C024 (CONJECTURE, not theorem).** `b(4^2,1^s) = (s-1,6,3)` for `s ≡ 2 (5)`
  — in **B-space**. 80 held-out parameters to `s = 402`, 0 failures, trace length
  8 edges. Recorded as a conjecture.
* **RR-C025 (REFUTED, and the worker's witness stands).** The analogous shape at
  `r = 3`, again **in B-space**: it holds at `s = 27,32,37,42,47,52,57`, where the
  `B`-endpoint is `(s+2,7,3)` reached in **30 edges / 31 states**, and it **fails
  at `s = 62`**, where the `B`-endpoint is `(25,17,8,8,8,8)` reached in
  **1 910 edges / 1 911 states**; it also fails at `s = 67,72,77`
  (`(33,27,7,6,6)`, `(30,24,18,6,6)`, `(47,16,9,9,8)`).

**Cycle-4 correction of Main's own cycle-3 error. Preserved deliberately.**
In cycle 3 Main "corrected" this witness, reporting that the committed map gives
`(30,20,9,7,5,3)` in "5 steps" and that `(25,17,8,8,8,8)` "has adjacent
differences 8,9,0,0,0 so it is not a gap partition and cannot be an image at
all". **Both parts of that correction were wrong.**

1. `(25,17,8,8,8,8)` is the **`B`-endpoint** returned by `pi_forward`; it is a
   valid `B_74` object and was never required to have gaps. Main applied the `D_n`
   test (`is_gap`) to a `B`-object: the exact B/D confusion this project has been
   warned about repeatedly. `(30,20,9,7,5,3)` is the **`D`-image** returned by
   `forward = T^{-1} ∘ pi_forward`, and `T^{-1}(25,17,8,8,8,8) = (30,20,9,7,5,3)`
   entry by entry (`b_i + 6 - 2i + 1`). Both tuples are correct; they live on
   different sides of `T`.
2. The "5 steps" figure was a **measurement bug**: the check unpacked
   `tr, _ = pi_forward(p)` when the function returns `(endpoint, trace)`, so
   `len(tr) - 1` was the number of parts of the *endpoint* minus one. The true
   figure is 1 910 edges / 1 911 states. The earlier scripts that printed
   "steps" for several `s` were therefore all mislabelled; the values that looked
   plausible did so by coincidence (a 2-edge path's endpoint happened to have 3
   parts).

So the worker m1's P3 refutation was correct in substance and in witness; Main's
rejection of it is **retracted** (recorded here rather than deleted). The worker
did conflate "steps" with states in its own prose — the honest figure is 1 911
*states*, i.e. 1 910 *edges* — and that distinction is now stated everywhere.

Correct methodology note, since this error had two independent causes: when a
claim mixes `B` and `D`, test it on the side named; and when reporting a path
length, print `len(trace)` and `len(trace)-1` explicitly rather than a derived
quantity whose meaning depends on an unpacking order.
