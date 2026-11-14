# RR127 cycle 2 -- direction A (COMPUTATION)

Fresh transcription of BZ82's `phi` and `psi` from the printed paper, an
exhaustive audit of both involutions, and a comparison with the committed
`Computation/bz82.py`. Everything below is finite verification over an explicit
range. Nothing here is an all-`n` theorem and nothing here is a new bijection:
the Mathathon objective (a more natural, weight-preserving bijection with an
independently specified inverse) is **not** advanced by this file.

Written without looking at `Computation/bz82.py`: `bz82_audit.py` was
transcribed from `pdftotext -layout` of the original scan, quotations and OCR
notes in `SOURCE_EXCERPTS.md`. The scan's sha256 matches the digest already
recorded in `Literature/READING_NOTES.md`.

## 1. Files

| file | role |
| --- | --- |
| `bz82_audit.py` | the fresh implementation: `phi`, `psi`, `pi_iterate`, `T`, `Tinv`, state enumeration, plus the declared readings R1--R5 |
| `run_audit.py` | deliverables (i), (ii), (iii), (v); independent counting routes; writes `results_cycle2.json`, `traces_cycle2.txt` |
| `negative_control.py` | sensitivity tests: deliberately wrong readings of the same rules; writes `ctrl_cycle2_n18.json`, `ctrl_cycle2_n30.json` |
| `compare_bz82.py` | deliverable (iv), against `../bz82.py`; writes `compare_cycle2.json` |
| `SOURCE_EXCERPTS.md` | the printed lines `bz82_audit.py` was transcribed from, with OCR notes |
| `runlog_cycle2.txt` | the full console output of every command below |
| `traces_cycle2.txt` | the two labelled traces of (v) |
| `results_cycle2.json`, `compare_cycle2.json`, `ctrl_*.json` | machine-readable results |

## 2. Exact commands

```sh
cd RogersRamanujan/Computation/cycle2
python3 run_audit.py 30          # 15 s, exit 0
python3 negative_control.py 18   # 0.5 s
python3 negative_control.py 30   # 15 s
python3 compare_bz82.py 30       # 12 s, exit 0
python3 compare_bz82.py 40       # 97 s, exit 0
```

Python 3.12.14, stdlib only, no randomness, no network at run time.

Key output lines (verbatim from `runlog_cycle2.txt`):

```
states in X(n), n <= 30 : 67551
  phi domain 66658  (excluded 0 x B: 893)   psi domain 66658  (excluded 0 x A: 893)
  phi Case I / Case II (all states) = 33329 / 34222
  psi Ia/Ib/IIa/IIb = 29924/29924/3405/4298
  admissible set EMPTY : 893 (in domain 0)   [expected 0 / 0]
  z>=0 vs all-int z   : 0 disagreements
  example (1) phi ok=True   example (2) psi ok=True   example (3) pi((4,1)) ok=True
  OVERALL exhaustive checks passed: True   (0 failures)
compared: phi 66658, psi 66658, domains 67551+67551, forward 893, onto-D per weight 31/31
DISCREPANCIES: 0
compared: phi 541114, psi 541114, domains 544365+544365, forward 3251, onto-D per weight 41/41
DISCREPANCIES: 0
```

## 3. (i) The integer domain of `z` in `phi` Case II

The printed line is only `m = Max{z <= a+2j-2 : z + lam(a+2j-1-z) <= t+5j-2}`.
The domain used, stated explicitly as reading R1 in `bz82_audit.py`, is

```
z in Z,  0 <= z <= a + 2j - 2,  z + lam(a+2j-1-z) <= t+5j-2,
lam(x) = 0 for x > t.
```

`z >= 0` is the part-non-negativity half (`m` is a part) and `z <= a+2j-2` is
exactly index legality of `lam(a+2j-1-z)`. The set is finite, so *the maximum
exists iff the set is non-empty*; that is the test performed.

Over all of `X(n)`, `n <= 30` (67 551 states), the case split gives
**34 222 Case-II states**, of which **33 329 are in `phi`'s domain**.

| measurement | count |
| --- | --- |
| Case-II states, all of `X(n)`, `n <= 30` | 34 222 |
| ... in `phi`'s domain `X(n) \ {0}xB(n)` | 33 329 |
| admissible set **empty**, all Case-II states | **893** |
| admissible set **empty**, in-domain Case-II states | **0**  (the expected value) |
| `a+2j-2 < 0` | 1, namely `(0;())` -- and `() in B(0)`, so it is off-domain |
| in-domain states with `a+2j-2 < 0` | 0 |
| selected `m`: minimum / maximum | **0** / 6 |
| admissible set size `|S|`: minimum / maximum | 1 / 7 |
| distribution of `|S|` | 1:2605, 2:8403, 3:11317, 4:7974, 5:2691, 6:333, 7:6 |
| `z >= 0` vs "all integers `z <= a+2j-2`": differing `m` | **0** |

**Shape of the set, and a closed existence criterion.** Two further structural
facts were tested on all 34 222 Case-II states of `n <= 30`, 0 failures each:

* `S` is always a **prefix** `{0,1,...,m}` -- 0 holes -- so `|S| = m+1` always
  and `Max` is never a maximum over a non-convex set;
* `S` is non-empty **iff** `a+2j-2 >= 0` **and** `lam(a+2j-1) <= t+5j-2`
  (0 criterion mismatches over the same 34 222 states).

The criterion is not my derivation: member m1 of this swarm (direction B)
derived it from the monotonicity of `i |-> lam(i) - i`, which makes the
admissible `z`-set a down-set. I checked it and the prefix property against my
own independent state enumeration rather than accepting them, and the check is
in `run_audit.py::admissible_shape` (`results_cycle2.json`
`admissible_shape`). Its value is that "does the maximum exist for every `n`"
is thereby reduced from a max over an unexplained finite set to two explicit
inequalities -- and the empirical content of (i) is then exactly that both
inequalities hold on every in-domain Case-II state of `n <= 30`.

Two consequences worth stating separately.

* **The 893 empty sets are exactly the 893 states of `0 x B(n)`**, i.e. exactly
  the complement of `phi`'s domain (893 = `sum_{n<=30} |B(n)|` = `sum |D_n|`,
  and `|B(n)| = |D(n)| = |A(n)|` is *not* used: each empty case was checked
  directly to be `j = 0` with `() or lam(-1) >= len`). `run_audit.py` asserts
  this (`empty_iff_offdomain_off`) and it holds with 0 exceptions. So the
  printed rule is complete **on its domain**, and the cycle-1 "empty set"
  phenomenon is the domain boundary itself, not a defect. This is supervisor
  correction C1 as an exact iff, not just "never empty".
* **The smallest `z` actually selected is 0**, so the `z >= 0` half of the
  bound is attained and cannot be dropped; and relaxing the lower bound to all
  integers changes no maximum on this range, so R1 is stable.

## 4. (ii) `phi^2 = id` and `psi^2 = id` with domain closure

Range: **every state of `X(n)` for every `n <= 30`** -- 67 551 states, of which
66 658 lie in `phi`'s domain and 66 658 in `psi`'s domain. For each in-domain
state and each map `f`: output is a strictly positive descending tuple, the
weight `|lam| + P(j)` is preserved, `j` moves by `+-(1)` and therefore changes
parity, `f(s)` is again in `f`'s domain (closure), and `f(f(s)) = s`.
**0 failures** in every one of those checks, for both maps.

Coverage of the structural cases the audit had to touch (all counted over
`n <= 30`):

| case | count |
| --- | --- |
| `j > 0` / `j < 0` / `j = 0` | 22 063 / 16 859 / 28 629 |
| `j` even / `j` odd | 34 222 / 33 329 |
| empty partition `t = 0` | 7 (one per `j` with `P(j) = n`, `j = -3..3`) |
| repeated parts | 61 971 |
| `phi` Case I with a virtual zero at `a` / at `mu` | 2 605 / 3 |
| `phi` Case I / Case II (all states) | 33 329 / 34 222 |
| `psi` I(a) / I(b) / II(a) / II(b) (all states) | 29 924 / 29 924 / 3 405 / 4 298 |
| `psi` states with `t0 > 0` / with `m2 > 0` / with `m0 = 0` / with `m3 = 0` | 26 789 / 49 695 / 40 762 / 26 400 |
| `psi` II(b) that *creates* a part (`m0 = 0`) | 1 949 |
| `psi` II(a) with `nu = m3+5j-3 = 0` (part deleted) | 1 949 |

Two statements about `psi`'s case structure came out exact on this range, and
both are stronger than "the checks pass":

* on the **domain**, the branch pairs are exactly `I(a) <-> I(b)` and
  `II(a) <-> II(b)`: 29 924 states in `I(a)` all land in `I(b)` and 29 924 in
  `I(b)` all land in `I(a)`; 3 405 `II(a)` land in `II(b)` and 3 405 `II(b)` in
  `II(a)`. No other branch pair occurs.
* all **893** off-domain states (`0 x A(n)`) fall in branch **II(b)**, with
  `t0 = 0`, `m2 = 0`, `m3 = 0`, `m0 = 0`, `j = 0` -- which is exactly the
  "II(b) selected with `m0 = 0` and `j = 0`" configuration of RR-C008 step (b).
  In-domain, `psi` II(b) with `m0 = 0` never creates a non-positive part
  (0 occurrences of `m0-5j-2 <= 0`).

Two other exact facts used by the transcription:

* **`a = mu` never happens in Case I.** 6 458 states of `n <= 30` have
  `a = mu`, and all 6 458 are Case II. So the ambiguity in "delete the parts
  `lam(a)` and `lam(mu)`" when `a = mu` is vacuous for `phi`, and the guard for
  it in `bz82.py` (`if drop:`) is dead code. Proof in `bz82_audit.py` docstring
  R2 (from `lam(a) = 2j` and `4j >= 5j + t*`, i.e. `t* <= -j < 0`).
* **Reading R5.** "Delete the parts `lam(a)` and `lam(mu)`" has to be a
  *value* deletion: remove one copy of the value `lam(a)` and one of `lam(mu)`,
  skipping zeros. Then the number of surviving parts is
  `t - [lam(a)>0] - [lam(mu)>0] = t* - 2` identically and the weight identity
  holds unconditionally. The competing "position" reading (pad the sequence to
  length `t*` and delete positions `a`, `mu`) agrees exactly when
  `max(a,mu) <= t*` and fails otherwise -- 371 in-domain Case-I states of
  `n <= 30`. First witness: `(-1;())` of weight 3, where `a = 3`, `mu = 1`,
  `t = 0`, `t* = 2`; the position reading gives `(0;1,1,1,1)` (weight 4) while
  the value reading gives `(0;1,1,1)` (weight 3) and
  `phi(0;1,1,1) = (-1;())` recovers it. See section 9.

## 5. (iii) The three printed examples of p. 315

All three reproduce exactly, and the paper's own labels `a = 4`, `mu = 1`,
Case I; `t0 = 3`, `m2 = 2`, Case I(a) are the values my code computes, not
looked-up ones.

1. `phi(2; 11,9,8,7,6,1,1,1) = (3; 10,9,7,2,2,2)`, with `a = 4`, `mu = 1`,
   Case I (verdict: match).
2. `psi(-2; 15,14,9,9,8,8,8,5,5,4,3,2,1) = (-3; 14,10,9,9,8,8,8,4,3,2,2,1)`,
   with `t0 = 3`, `m2 = 2`, Case I(a) (verdict: match).
3. `pi((4,1)) = (3,2)`, and the **nine-state chain matches state by state**:

```
(0;4,1) -phi-> (1;1,1,1) -psi-> (0;2,1,1,1) -phi-> (-1;1,1) -psi-> (0;3,1,1)
-phi-> (1;2,1) -psi-> (0;2,2,1) -phi-> (1;3) -psi-> (0;3,2)
```

with branches `I, I(a), II (m=0), II(b) (nu=3), I, I(a), I, I(a)` and
`T^{-1}(3,2) = (4,1)`, i.e. this example is a fixed point of the composed
`A_n -> D_n` map. Note the printed OCR `(m3,1,1)` is `(0;3,1,1)`; I record that
in `SOURCE_EXCERPTS.md` rather than silently "correcting" it in the report.

## 6. (iv) Comparison with the committed `Computation/bz82.py`

`compare_bz82.py` imports both implementations and compares, state by state:
`phi` on every state of `phi`'s domain, `psi` on every state of `psi`'s domain,
the two domain predicates on every state of `X(n)`, and the composed
`forward = Tinv . pi` on every object of `A_n` together with injectivity and
surjectivity onto `D_n` per weight, plus the three examples through the
committed code.

| range | `phi` compared | `psi` compared | `forward` compared | onto-`D_n` per weight | discrepancies |
| --- | --- | --- | --- | --- | --- |
| `n <= 30` | 66 658 | 66 658 | 893 | 31/31 | **0** |
| `n <= 40` | 541 114 | 541 114 | 3 251 | 41/41 | **0** |

The discrepancy list is therefore **empty**, and the minimal list is empty:
there is no state, no weight and no example on which the two readings differ.
Two remarks about what that does and does not establish.

* It does establish that the committed implementation is a faithful
  transcription of the printed rules *as I independently read them*, including
  the `z >= 0` domain, the `>=` tie-breaks in I(a) and II(a), and the placement
  of the virtual zero slot at the exact index `a` (resp. `mu`) rather than at
  the end of the sequence. That placement is the one substantive detail where
  the two codes had to agree and could have disagreed (section 4, R5).
* It does **not** establish that the transcription is right. Two independent
  readers can share a misreading; the guard against that is the paper's own
  three examples and the internal consistency of the weight identity, and those
  are the checks that caught the R5 reading in the first place.

## 7. (v) Per-weight statistics of the alternating path

`pi` as implemented applies `phi`, then `psi`, then `phi`, from the start state
`(0;lam)` with `lam in A_n`, and stops the first time the state is `(0;mu)` with
`mu in B(n)`. "steps" = number of applications. The mean is over all objects of
`A_n`, reported exactly and as a decimal.

| n | \|A_n\| | max steps | mean steps (exact) | mean | extremal A_n object | # extremal |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 0 | 0.000 | `()` | 1 |
| 1 | 1 | 0 | 0 | 0.000 | `1,` | 1 |
| 2 | 1 | 2 | 2 | 2.000 | `1,1,` | 1 |
| 3 | 1 | 2 | 2 | 2.000 | `1,1,1,` | 1 |
| 4 | 2 | 6 | 3 | 3.000 | `1,1,1,1,` | 1 |
| 5 | 2 | 8 | 5 | 5.000 | `4,1,` | 1 |
| 6 | 3 | 10 | 4 | 4.000 | `4,1,1,` | 1 |
| 7 | 3 | 14 | 8 | 8.000 | `4,1,1,1,` | 1 |
| 8 | 4 | 16 | 7 | 7.000 | `4,1,1,1,1,` | 1 |
| 9 | 5 | 16 | 6 | 6.000 | `4,4,1,` | 1 |
| 10 | 6 | 10 | 13/3 | 4.333 | `6,1,1,1,1,` | 1 |
| 11 | 7 | 42 | 88/7 | 12.571 | `4,4,1,1,1,` | 1 |
| 12 | 9 | 58 | 142/9 | 15.778 | `9,1,1,1,` | 1 |
| 13 | 10 | 42 | 18 | 18.000 | `6,6,1,` | 1 |
| 14 | 12 | 90 | 62/3 | 20.667 | `11,1,1,1,` | 1 |
| 15 | 14 | 124 | 148/7 | 21.143 | `9,4,1,1,` | 1 |
| 16 | 17 | 128 | 456/17 | 26.824 | `6,4,4,1,1,` | 1 |
| 17 | 19 | 140 | 600/19 | 31.579 | `9,4,1,1,1,1,` | 1 |
| 18 | 23 | 110 | 788/23 | 34.261 | `4,4,4,1,1,1,1,1,1,` | 1 |
| 19 | 26 | 196 | 502/13 | 38.615 | `11,6,1,1,` | 2 |
| 20 | 31 | 224 | 1280/31 | 41.290 | `11,6,1,1,1,` | 1 |
| 21 | 35 | 208 | 1656/35 | 47.314 | `14,6,1,` | 1 |
| 22 | 41 | 228 | 2192/41 | 53.463 | `11,9,1,1,` | 1 |
| 23 | 46 | 344 | 1381/23 | 60.043 | `14,6,1,1,1,` | 1 |
| 24 | 54 | 300 | 1780/27 | 65.926 | `4,4,4,4,1,1,1,1,1,1,1,1,` | 1 |
| 25 | 61 | 466 | 4498/61 | 73.738 | `14,4,4,1,1,1,` | 1 |
| 26 | 70 | 592 | 2801/35 | 80.029 | `6,6,4,4,1,1,1,1,1,1,` | 1 |
| 27 | 79 | 390 | 7004/79 | 88.658 | `14,6,4,1,1,1,` | 1 |
| 28 | 91 | 416 | 8780/91 | 96.484 | `9,6,6,6,1,` | 1 |
| 29 | 102 | 560 | 5419/51 | 106.255 | `11,11,1,1,1,1,1,1,1,` | 1 |
| 30 | 117 | 646 | 4468/39 | 114.564 | `4,4,4,4,4,4,4,1,1,` | 1 |

**Cross-check against RR-C011.** The sequence of maxima here,
`0,0,2,2,6,8,10,14,16,16,10,42,58,42,90,124,128,140,110,196,224,208,228,344,
300,466,592,390,416,560,646`, is **identical** to the list recorded in
`Main/CLAIMS.md` RR-C011, and the mean at `n = 30` is `4468/39 = 114.564`
(RR-C011: "114.6"). An independent implementation of the same printed rules
reproduces the committed step counts exactly. No growth rate is asserted here:
the table is raw data and a single extremal object per weight, per supervisor
correction C4.

The two complete labelled traces are in `traces_cycle2.txt`:

* long: `(4,4,4,4,4,4,4,1,1) in A_30`, **646** applications, 647 states, ending
  at `(0;8,8,7,7) in B_30`, hence `T^{-1}(8,8,7,7) = (11,9,6,4) in D_30`;
* short: `(1,1) in A_2`, 2 applications, `(0;1,1) -phi-> (1;()) -psi-> (0;2)`,
  hence `T^{-1}(2) = (2) in D_2`.

Each line is labelled with the step number, the map applied, `j`, the partition,
and the printed branch with the quantities the paper names (`a`, `mu`, `m`,
`nu`).

## 8. (vi) Which checks are logically independent of which

Honest inventory. "Independent" below means: neither check can be derived from
the other within this artifact.

**Genuinely independent of each other:**

1. `phi^2 = id` and `psi^2 = id`. Different rules, disjoint code, and neither
   implies the other. Both were run over the same state set, which makes them
   *correlated* (a shared state-enumeration bug would hit both) but not
   dependent.
2. The three counting routes in `run_audit.py::independent_counts`: (a) direct
   enumeration of `A_n` by the residue predicate, (b) direct enumeration of
   `D_n` by the gap predicate, (c) the Jacobi triple-product sum
   `sum_{j in Z} (-1)^j p(n - P(j))` computed from the ordinary partition
   numbers `p(m)` via Euler's pentagonal recurrence. (a) and (b) share the
   partition generator but share no predicate; (c) uses neither `A`-parts nor
   `D`-parts at all. All three agree for every `n <= 30` (31/31).
   Following supervisor correction C3, I do **not** claim six methods: the
   power-series product, the coin-change DP, the gap recurrence and the
   `sum_t x^{t^2}/(x;x)_t` series in cycle 1 collapse to two recurrences, and
   the only genuinely separate routes there are the two enumerations and the
   Jacobi sum. Counting is in any case not evidence for the objective.
3. The Case-II admissibility test of (i) and the involution test of (ii). A
   rule can have `m` always defined and still fail `phi^2 = id` -- variant
   `PHI-1` in section 9 is exactly such a rule (0 raises, 1 113 defects).
   Within (i), the prefix test and the criterion test of section 3 are also
   independent of each other: the last admissible integer is in the set by
   construction, so a hole would move the maximum without emptying the set.
4. The comparison with `bz82.py` is independent of my implementation in the
   sense that the two programs were written separately from the same source;
   it is *not* independent evidence about the source.
5. The negative controls of section 9 are independent of the audit and are the
   reason the audit's zeros mean something.

**Not independent (do not count these twice):**

6. The three p.315 examples are instances inside the exhaustive range, so they
   are *implied* by the `n <= 30` census. Their separate value is source
   fidelity and nothing else: they are the only external check on the
   transcription, and they were verified by hand against the printed page
   before the code was run.
7. `forward` being injective, surjective and weight-preserving on `A_n -> D_n`
   is a corollary of `phi^2 = psi^2 = id` on the same range; it is the same
   information, aggregated.
8. The agreement of the `n <= 40` comparison with the `n <= 30` comparison is
   a monotone extension of the same check, not new evidence.
9. The identity `|A_n| = |D_n|` is *not* independent evidence for anything about
   the bijection: equal counts prove nothing, as the contract says.

## 9. Negative controls: the zeros are not vacuous

`negative_control.py` reruns the same harness with one disputed line changed.
Same states, same code path.

| variant | `n <= 18` defects | `n <= 30` defects | first failing state |
| --- | --- | --- | --- |
| baseline (correct reading) `phi` | **0** of 3 198 | **0** of 66 658 | -- |
| `PHI-1` Case I deletes *positions*, padded at the end | 141 | 1 113 (371 weight + 742 involution) | `(-1;())`: `(0;1,1,1,1)` instead of `(0;1,1,1)` |
| `PHI-2` Case II `z >= 1` with fallback `m = 0` | **0** | **0** | -- |
| `PHI-3` Case II `z >= 1`, no fallback | 510 (255 raises) | 5 210 (2 605 raises) | `(-1;())` at `n = 3` |
| baseline (correct reading) `psi` | **0** of 3 198 | **0** of 66 658 | -- |
| `PSI-1` flip the I(a) tie (`>=` -> `>`) | **1 120** | 23 836 | `(0;2,2)` at `n = 4`, I(b) needs `k = -1` copies of 5 |
| `PSI-2` flip the II(a) tie (`>=` -> `>`) | 539 (= 165 weight + **374** involution) | 5 473 | `(0;3)` at `n = 3` (weight), `(-1;())` (involution) |
| `PSI-3` II(a) with `nu = 0` keeps a part of 0 | **374** | 3 898 | `(-1;()) -> (0;3) -> (-1;0)` |

The three numbers `1 120`, `374`, `374` at `n <= 18` are **exactly** the ones
recorded in `Main/DECISIONS.md` D-3a for the same three flips, with the same
first witnesses, obtained here from a separate implementation and a separate
harness. That is the evidence that the audit's zeros are sensitive rather than
vacuous.

`PHI-2` is also an independent confirmation of supervisor correction C2: the
cycle-1 rule (`z >= 1`, falling back to 0 when empty) agrees with the printed
`z >= 0` rule on **every** in-domain Case-II state of `n <= 30` (0 differing
`m`), because the fallback fires exactly on the 2 605 in-domain states where
only `z = 0` is admissible and there the fallback value *is* the maximum. What
was wrong in cycle 1 was the diagnosis, not the code -- as C2 says.

Not reproduced: D-3's figure of "2 692 defects at `n <= 18`" for the literal
printed rule. `PHI-3` gives 255 raising states, i.e. 510 counted defects when
both directions are counted. The gap is a convention difference (which states
are in the denominator, and whether a raise is counted once or twice); I record
my own figure and the convention behind it rather than adopt the old number.

## 10. Findings for Main, and proposed changes I did not make

I have write access only to `Computation/cycle2/`, so the following are
proposals, not edits.

* **F1 (sharpens C1 to an iff).** Over `n <= 30` the `phi` Case-II admissible
  set is empty on exactly 893 states, and those are exactly the states of
  `0 x B(n)`, i.e. exactly `X(n) \ dom(phi)`. In-domain the count is 0. So the
  printed rule is complete on its domain and the cycle-1 "empty set" is the
  domain boundary. *Proposed:* restate `Main/DECISIONS.md` D-3's first bullet
  ("its admissible set is empty at `(0;(2,1,1,1))`") -- that state is in
  `phi`'s domain and the `z >= 0` set there is `{0}`, non-empty, with `m = 0`.
  The counterexample in D-3 does not exist. D-3 is already retracted by C1;
  this supplies the replacement statement.
* **F2 (new, about the source, not the code).** `phi` Case I's "delete the
  parts `lam(a)` and `lam(mu)`" must be a *value* deletion. The position
  reading differs on 371 in-domain Case-I states of `n <= 30` and breaks the
  weight identity; first witness `(-1;())` at `n = 3`. The supervisor's
  phrasing "a slot beyond `t` holds a virtual 0" is correct only if that
  virtual zero is placed at index `a` (resp. `mu`), not appended. `bz82.py`
  places it correctly. *Proposed:* add reading R5 to `Literature/READING_NOTES.md`
  RR-L004 and to the `bz82.py` docstring, which currently says "one phantom
  slot of value 0 at each of `a`, `mu` that exceeds `t`" without saying where
  the phantom sits when both `a` and `mu` exceed `t` by different amounts (it
  is correct, but a future editor could break it silently; `PHI-1` is the
  measured cost, 1 113 defects).
* **F3 (`a = mu` in Case I is vacuous).** 6 458 states of `n <= 30` have
  `a = mu`; all are Case II. A proof is in `bz82_audit.py` R2. *Proposed:* the
  `if drop:` block in `bz82.py::phi` is unreachable dead code; keeping it is
  harmless but it should not be cited as evidence that the `a = mu` case was
  settled by testing.
* **F4 (`psi`'s branch pairing is exact).** On the domain the pairs are exactly
  `I(a)<->I(b)` and `II(a)<->II(b)` (29 924 and 3 405 states each way,
  `n <= 30`). This is a stronger statement than "the branches are mutually
  inverse" and it is what `RR-C008` step (d) actually needs. *Proposed:* state
  it in `CLAIMS.md` RR-C008 as an exact branch-pairing lemma with the numerical
  support and the (still missing) written proof.
* **F5 (C5 support).** Independent enumeration gives `|A_24| = 54`, and the
  Jacobi sum `sum_j (-1)^j p(24 - P(j))` also gives 54. The recalled
  `A003114` tail value 55 is inconsistent with the *definition* of `A_n` in the
  contract, so it cannot be a mis-implementation. *Proposed:* retire
  `rr_core.A003114` or replace it with the computed first 31 values and a note
  that the identification with `A003114` is unverified here (I did not consult
  OEIS; the claim is only that 55 is wrong *for this family*).
* **F7 (cross-direction, confirmed independently).** Direction B's `z`-set
  down-set lemma, and its criterion `nonempty iff a+2j-2 >= 0 and
  lam(a+2j-1) <= t+5j-2`, hold on all 34 222 Case-II states of `n <= 30` when
  tested against my state enumeration (0 failures, `admissible_shape` in
  `results_cycle2.json`), as does the stronger statement that the set is always
  a prefix `{0,...,m}`. *Proposed:* record in `CLAIMS.md` RR-C009 that
  `phi`'s Case-II existence question is settled *per state* by two
  inequalities, and that the only remaining content is proving those two for
  every in-domain state -- not an existence question about a maximum.
* **F6 (C6 blind spot).** In this artifact the generic-filter route is not a
  separate method at all: `independent_counts` uses `A`-enumeration,
  `D`-enumeration and the Jacobi sum, all three of which enter the agreement
  test. I have nothing to say about `run_checks.py` beyond C6's own finding
  because I did not modify it (outside my folder).

## 11. What failed, and what is not verified

* **A transcription error of mine, found by the audit itself.** My first
  `phi` Case I implementation deleted positions in a sequence padded at the end
  to length `t*`. It passed the p.315 examples and `n <= 10` and failed at
  `(-2;())`, `n = 11` (weight 12 instead of 11). That is the origin of finding
  F2 and of the `PHI-1` control. It is reported rather than quietly fixed
  because it is the one place where the printed rule is genuinely ambiguous.
* **No all-`n` result.** Nothing here proves `phi^2 = id`, `psi^2 = id`,
  termination of the iteration, or correctness of the composed map for any
  `n > 40`. The strongest thing said is a finite conjunction over `n <= 40` for
  the comparison and `n <= 30` for the involution audit.
* **Termination is not proved and is not measured beyond `n <= 30`.**
  `pi_iterate` uses a repeated-state detector as a failure guard, not as a
  proof.
* **States in the other map's excluded set are reached, but never where the
  next map would be undefined.** 1 588 such events were recorded, 794 of
  `phi(s) in 0 x A(n)` (where `psi` is not defined) and 794 of
  `psi(s) in 0 x B(n)` (where `phi` is not defined). But in none of those
  events did the alternation have to apply the missing map: all 893 runs of
  `pi_iterate` completed, and `pi_iterate` raises if it is ever asked to apply a
  map outside its domain. But this is an empirical fact about the iteration on
  `n <= 30`, and BZ82 do not state it; the paper's "last well-defined element"
  phrasing is doing real work here and it is the one place in the p.314
  argument where I could not see an a priori reason that it cannot happen.
  *This is the most interesting unresolved point I found, and it is not a defect
  in the rules.*
* I did not read `Counterexamples/`, `Experimental/` or `Lean/`, did not run
  `Computation/run_checks.py`, and did not touch `rr_core.py` or `bz82.py`.
