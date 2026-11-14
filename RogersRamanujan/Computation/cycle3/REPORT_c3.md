# Cycle 3, direction C — computation regression

Worker m3, swarm `smwg1kdjq`. Everything below is exact-integer, python3 stdlib
only, no network, no git. Files are confined to
`RogersRamanujan/Computation/cycle3/`; nothing outside it was edited.

## Deliverables

| file | what it is |
| --- | --- |
| `phi_skeleton_c3.py` | corrected skeleton auditor of BZ82's `phi`, assertions P0–P9, all of `X(n)` for `n <= 30` |
| `regression_c3.py` | one self-contained fast regression against the committed `Computation/bz82.py`, 8 checks, **0.41 s** |
| `slab_c3.py` | a `(j, lambda)` slab decoupled from weight (`|j| <= 30`, `|lam| <= 30`, 1 746 369 states) — a wider screen than any weight slice can give |
| `proofcheck_c3.py` | machine check of each *step* of the written proof of obligation (i) (Finding 2) |
| `results_skeleton_c3.json`, `results_regression_c3.json`, `results_slab_c3.json` | machine-readable results (JSON, no YAML), aggregates only |
| `results_proofcheck_c3.json` | its aggregates |
| `log_skeleton_n30.txt`, `log_regression.txt`, `log_slab_30_30.txt`, `log_proofcheck.txt` | captured stdout |

Exact commands (each from `RogersRamanujan/Computation/cycle3/`):

```
python3 phi_skeleton_c3.py 30 --json results_skeleton_c3.json
python3 regression_c3.py
python3 slab_c3.py 30 30
python3 proofcheck_c3.py 40 22
```

Key output line of the last one:

```
s0 R >= 0 fails 0   s1 k >= 1 fails 0   s2 f not increasing on [0,hi] 0
s4 case (a) k <= t: 15187 states (R <= hi: 0, R > hi: 15187), branch argument fails 0, m <= R-1 fails 0
s5 case (b) k > t: 166804 states, j < 1 0, a > t+1 0, R < k 0
s6 (p2>=0) <=> (R>=k) fails 0   s7 lemma m <= R-1 fails 0
TOTAL: PASS  (0 step failures, 1.7 s)
```

`R <= hi` occurs 0 times in case (a), which is itself the argument above: if
`R <= hi` then `f(R) >= f(0)+R >= R+1 > R` contradicts admissibility of `R`.

## Job 1 — the repaired skeleton auditor

Key output lines of `python3 phi_skeleton_c3.py 30`:

```
states in X(n): 67551  in phi domain: 66658  excluded {0}xB(n): 893
Case I: 33329   Case II: 33329
a == mu: 6458  (a <= t: 5565, a > t: 893)   a == mu AND Case I: 0
Case II: p2 = 0 in 3, m = 0 in 2605, m = hi in 22527, m < hi in 10802, image lost a 1 in 22759
p2 certificate: C-a only 10805, C-b only 0, both 22524, neither 0
P0..P9 PASS (12916–135102 assertions each)
cross-check vs Computation/bz82.py: 66658 states, 0 mismatches
TOTAL: PASS  (0 failed assertions, 0 cross-check mismatches, 1.3 s)
```

What P0–P9 assert is listed in the module docstring; in one line each: P0 the
domain is exactly `X(n) \ {0}xB(n)`; P1 `a` exists, is minimal, and
`a <= max(t+1, 1-2j)`; P2 `1 <= mu <= a+2j` and `mu = k+1-L` with `0 <= L <= k`;
P3 `a == mu <=> L = 2j` **and** `a == mu` never meets Case I; P4 weight and
positivity in both cases; P5 the Case-II z-set is the down-set `0..m` with
`a+2j-2 >= 0` and `t+5j-3-m >= 0`, plus a recorded certificate for the second
inequality; P6 `r = L+lam(mu)-5j-t* >= 0` and the slot inventory has size `t*`;
P7 Case I ↔ Case II and the image stays in the domain; P8 `phi^2 = id`;
P9 `j` flips parity and `|lam| + P(j)` is invariant.

### Repair of the cycle-2 skeleton

`Counterexamples/cycle2/phi_skeleton.py` **as it stands in this working tree does
not reproduce the reported failure.** `python3 phi_skeleton.py 2` exits 0 with
`0 failures`, and `python3 phi_skeleton.py 30` exits 0 with
`domain states 66658, excluded {0}xB(n) 893 / Case I 33329, Case II 33329 /
states with a = mu: 6458 (all Case II: True)`. Those five numbers are
identical to mine, computed by an independent transcription, so the reported
`KeyError: 'a==mu'` and the vacuous-`case_of` defect belong to the **exported
checkpoint**, not to the file now in the tree. What I can and do report is which
of its checks are load-bearing and which are not, and add the ones it lacks:

* its `P3` already asserts `a = mu => not Case I` finitely; it is now **proved**
  (Finding 1), so the assertion is a regression guard rather than evidence;
* its Case-I deletion deletes "any slot whose position is `a` or `mu`" and has
  no representation of a slot collision. In `phi_skeleton_c3.py` the inventory is
  an explicit list of `(pos, value)` of size `t*`, and each of the two deletions
  must consume a **distinct** entry; a collision raises instead of being resolved
  by set semantics (BUG-3). Provably unreachable (Finding 1), so this changes no
  number — it makes the impossibility visible;
* `P5` there records only `m` and the value of `p2`. Here it records which
  *argument* certifies `p2 >= 0` and splits `m = hi` from `m < hi` (Finding 2);
* every counter here is a pre-declared fixed-key dict and `Census.bump` raises on
  an unknown key, so a counter read before it is written is a loud failure
  instead of a silent `0` (BUG-1);
* `P7` here consumes the record `phi` returns and asserts `branch in ('I','II')`
  before using it, so it cannot pass vacuously (BUG-2);
* the auditor additionally runs every in-domain state through the committed
  `bz82.py` and compares images: **66 658 states, 0 mismatches**.

## Findings

**Finding 1 (proved, closes the `a = mu` half of obligation (iii)).**
`a = mu` **implies Case II**; the slot at position `a` therefore never has to be
deleted twice, and no second-removal fallback is needed anywhere in Case I.

* If `a <= t`: `L = lam(a) = 2j` and `L >= 1`, so `j >= 1`. Also `mu = a <= t`,
  so `lam(mu) = L = 2j` and `a, mu <= t` give `t* = t`. Case I would require
  `L + lam(mu) = 4j >= 5j + t* = 5j + t`, i.e. `j + t <= 0`, contradicting
  `j >= 1`, `t >= 0`.
* If `a > t`: `L` is the padded zero, so `2j = 0`, i.e. `j = 0`. Then `mu = a > t`
  too, so `lam(mu) = 0` and `t* = t + 2`. Case I would require
  `0 >= 5j + t* = t + 2 >= 2`. Contradiction.

Consequence for the committed code: the `if drop:` fallback at the end of Case I
in `Computation/bz82.py` is unreachable. It is dead code that looks like a rule
— the same failure mode as RR-X005 and RR-C017. **Proposed change to Main:**
replace it by `assert not drop` (or delete it) with a pointer to this note. It is
exercised 0 times over 1 746 369 states.

**Finding 2 (obligation (i) — BOTH parts now proved).**

Part one, `m >= 0`, is immediate: `m` is the maximum of a nonempty set of
nonnegative integers.

Part two, `p2 = t+5j-3-m >= 0`, is **proved for all in-domain Case-II states**;
no computation is needed. Write `R = t+5j-2`, `k = a+2j-1`, `hi = k-1`,
`f(z) = z + lam(k-z)` with zero padding, `S = {0 <= z <= hi : f(z) <= R}`,
`m = max S`. Case II contributes exactly one hypothesis: `S` is nonempty.

* `f` is **strictly increasing on `[0, hi]`**: for `0 <= z <= hi-1` both indices
  `k-z` and `k-z-1` lie in `[1,k]`, so
  `f(z+1) - f(z) = 1 + lam(k-z-1) - lam(k-z) >= 1` by weak decrease of `lam`.
  (It is **not** increasing past `hi`, where the padded index `0` is reached and
  `f(z+1)-f(z) = 1 - lam(1)` may be very negative. Extending the monotonicity
  argument beyond `hi` — as a careless reading of "`z + lam(k-z)` increases"
  invites — is the one trap here; `S` only ever lives on `[0,hi]`, so nothing is
  lost.)
* `S` nonempty gives `R >= 0`, since `f >= 0` on `[0,hi]`.
* **Case (a), `k <= t`.** Then `k >= 1` (as `S ⊆ [0,k-1]` is nonempty) and
  `lam(k) >= 1`. If `R <= hi` then `f(R) >= f(0) + R = lam(k) + R >= R+1 > R`,
  so `z = R` is inadmissible and `m <= R-1`. If `R > hi` then
  `m <= hi <= R-1`.
* **Case (b), `k > t`.** Then `j >= 1`: if `a <= t` then
  `k = a+2j-1 > t` forces `2j-1 >= k-a > t-a >= 0`, and if `a > t` then
  `k = a+2j-1 >= t+2j > t`. With `j >= 1`, `a <= max(t+1, 1-2j) = t+1`. So either
  `a <= t` and `R - (k-1) = t+3j-a >= 3j >= 3`, or `a = t+1` and
  `R - (k-1) = 3j-1 >= 2`. Hence `R >= k = hi+1` and `m <= hi <= R-1`.

**Sharp form (also proved, and it explains why the naive route fails):**
`p2 >= 0` **iff** `R >= k`. `z = R` is admissible whenever `0 <= R <= hi`, since
`f(R) >= R`; so if `R < k` then `R <= hi`, `m >= R` and `p2 <= -1`. Conversely
`R >= k` forces `hi <= R-1`. So the whole obligation is the single inequality
`a <= t+3j-1`, which the two cases above establish.

Both bounds are attained, so they are sharp:

* `min p2 = 0` at `j = -5, lam = (1^28)`, `n = 93`, `m = 0`, `p2 = 0`;
* `min r = 0` at `j = -5, lam = (2,2,1^26)`.

Finite confirmation of every step of the proof is `proofcheck_c3.py`: 0 step
failures over 181 991 in-domain Case-II states with `S` nonempty, `|j| <= 40`,
`|lam| <= 22` — `f` strictly increasing on `[0,hi]`, `R >= 0`, `k >= 1`, the
case-(a) argument in both sub-branches, case (b) `j >= 1`, `a <= t+1`, `R >= k`,
the sharp form, and `m <= R-1`. The script also reports, as a non-failure, that
`f` steps *down* at `hi+1` in 181 951 of 181 991 states: that is the trap, and it
is why the monotonicity is only ever used on `[0,hi]`.

**Finding 3 (obligation (iii) beyond the collision, and the domain, on a wider domain).**
`slab_c3.py 30 30` sweeps 1 746 369 states with `|j| <= 30` and `|lam| <= 30`,
which is *not* a weight slice (a weight slice couples `j` to `|lam|` through
`P(j)`). Over it: `a == mu` 33 723 times, **Case I 0**; `p2 < 0` **0**;
`C-a` failure **0**; `r < 0` **0**; the sharp maximum-existence criterion
(`nonempty <=> k >= 1 and lam(k) <= R`) violated **0** times over 870 782
Case-II states; and the admissible set is empty **exactly** on `{0}xB(n)`
(892 excluded states, 0 in-domain). The equivalence
"Case-II admissible set empty ⟺ `{0}xB(n)`" was previously finite only for
`n <= 30`; it now also holds on a slab reaching weight
`P(30) + 30 = 306` and `|j|` up to 30 with tiny partitions. Still finite
evidence, not a proof.

## Job 2 — the fast regression

`python3 regression_c3.py` — **8/8 PASS in 0.41 s** (budget 20 s):

```
EX-1   PASS  BZ82 p.315 example (1), phi: a=4 mu=1 Case I  (a=4 mu=1)
EX-2   PASS  BZ82 p.315 example (2), psi: t0=3 m2=2 Case I(a)
EX-3   PASS  BZ82 p.315 example (3), nine-state chain, pi((4,1))=(3,2)  (steps=8)
PHI    PASS  phi^2 = id and closure on X(n)\{0}xB(n), n <= 18  (checked=3198)
PSI    PASS  psi^2 = id and closure on X(n)\{0}xA(n), n <= 18  (checked=3198)
BIJ    PASS  forward/inverse are mutually inverse bijections A_n <-> D_n, n <= 18  (objects=140)
C2MAX  PASS  Case-II maximum exists iff k>=1 and lam(k)<=R, n <= 30  (checked=34222)
C2BOX  PASS  created parts/inserted ones are nonnegative, n <= 30  (case_II=33329 case_I=33329)
TOTAL: PASS  8/8 checks passed in 0.41 s
```

`BIJ` checks all five laws (into `D_n`, injective, weight, surjective with
`|A_n| = |D_n|`, and both compositions the identity), not just the object count.
`C2MAX` checks the down-set property, the sharp criterion, and that emptiness is
exactly `{0}xB(n)`. The JSON at
`Computation/cycle3/results_regression_c3.json` holds one aggregate row per
check plus one row per weight, and no per-state rows.

**Three of my own first-pass assertions were wrong and the committed code was
right.** Recorded because the project's rule is that local expectations must be
checked against the source, not the other way round:

1. example (1) inserts **0** ones (`r = 0`), not 2 — deleting slots 1 and 4 of
   the eight slots and incrementing the rest already gives the six-part image;
2. example (2) has `m3 = 8`, not `m3 = 0`; only `t0`, `m2` and the sub-case are
   what the source prints;
3. `forward((4,1)) = (4,1)`, not `(3,2)`: `forward = T^{-1} . pi` with
   `pi((4,1)) = (3,2)` and `T^{-1}(3,2) = (4,1)`. This agrees with
   `Main/RESULTS.md` ("the map fixes `(4,1)`"); my expectation had dropped the
   final `T^{-1}`.

## What is not done, and one unrelated defect

* Obligation (i) is **closed** (Finding 2), by a written proof, not by the run.
* Obligation (v) is **not** proved. `P8` is a finite check over 66 658 states and
  is labelled as evidence in the code, not as a proof.
* `Computation/rr_core.py` cannot be run as a script: its `__main__` block
  references `A003114`, which is not defined anywhere in the file
  (`NameError: name 'A003114' is not defined`). The table was retired in cycle 2
  but the block that reads it was not. Not mine to edit — **proposed change to
  Main:** delete the `A003114[n]` comparison from that block (the other five
  columns are still a useful smoke test).
