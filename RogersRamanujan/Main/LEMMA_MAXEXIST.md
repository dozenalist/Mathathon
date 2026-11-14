# Lemma MX: the Case-II maximum, all inputs

Status: **PROVED** (Main, cycle 3, 2026-11-14). Source of the argument: the
proposed outline in `SUPERVISOR_REVIEW_19046.md`, audited case by case by Main
against the definitions and re-checked against every Case-II state of weight
`<= 30`. Attribution: the case split is the supervisor's; the sharpening of the
`z`-range statement (Theorem MX.3 below) and the `a = mu` lemma are Main's, and
they correct errors in Main's own cycle-2 account.

This lemma is about **when the Case-II rule is defined**. It is not the whole
`phi` involution and does not by itself establish the reference bijection.

## Setting

Integer `j`, a positive descending partition `lambda` of length `t`, zero padding
`lam(x) = 0` for `x > t` (and `lam(0) = 0`). Define

```
a     = min { x >= 1 : 2j + x - lam(x) > 0 }     (exists: lam(x)=0 for x > t)
L     = lam(a)
k     = a + 2j - 1
mu    = k + 1 - L  =  2j + a - L
tstar = t + [a > t] + [mu > t]
R     = t + 5j - 2
```

**Lemma MX.0 (basic facts).** `0 <= L <= k`, `mu >= 1`, and `mu = 2j + a - L`.
*Proof.* Minimality of `a` gives `2j + a - lam(a) > 0`, i.e. `L <= k`, and `L >= 0`
since `lam >= 0`. Hence `mu = k+1-L >= 1`. QED

**Lemma MX.1 (monotonicity).** On the integers `0 <= z <= k-1` the map
`z |-> z + lam(k-z)` is strictly increasing (by at least 1 per step).
*Proof.* Increasing `z` by 1 decreases the index `k-z` by 1; `lam` is weakly
decreasing in its index (including the zero padding), so `lam(k-z-1) >= lam(k-z)`;
together with the `+1` from `z` this gives an increase of at least 1. QED

Consequently the admissible set `S = { z in Z : 0 <= z <= k-1, z + lam(k-z) <= R }`
is an initial segment of `{0,...,k-1}`, and

**Lemma MX.2 (criterion).** `S` is nonempty **iff** `k >= 1` and `lam(k) <= R`.
*Proof.* If `k <= 0` the interval is empty. If `k >= 1`, `z = 0` is admissible iff
`lam(k) <= R`, and by MX.1 that is the least element, so it suffices. QED

## Theorem MX.3 (where the printed maximum is defined) — CORRECTED in cycle 4

Let `S_Z = { z in Z : z <= k-1, z + lam(k-z) <= R }`, i.e. the printed rule read
literally: BZ82 p.314 prints the **upper** bound `z <= a+2j-2 = k-1` and no lower
bound, so `z` ranges over the integers below `k-1`.

1. **`S_Z` has a maximum on every state.** On `z <= k-1` the index `k-z` is `>= 1`,
   so both terms are in their positive range and `z |-> z + lam(k-z)` is
   *strictly* increasing (increase `z` by 1: `z` gains 1 and `lam(k-z)` is
   non-decreasing because its index falls). A strictly increasing function is
   bounded above by `k-1`, so the admissible `z` form a finite initial segment.
2. **On `phi`'s domain** some `z` with `0 <= z <= k-1` is admissible (Lemma MX.4),
   so the maximum of `S_Z` is attained in `{0,...,k-1}` and both created parts
   `m` and `t+5j-3-m` are `>= 0`.
3. **Off `phi`'s domain** (`{0} x B(n)`) the admissible `z` are all negative, the
   maximum of `S_Z` is negative, and `t+5j-3-m <= 0`, so the rule would create a
   non-positive part.

**Cycle-3 error corrected here, and the reason it mattered.** Cycle 3 stated that
`z |-> z + lam(k-z)` is "strictly increasing on **all** of `Z`, and it tends to
`+infinity` as `z -> +infinity`". The monotonicity claim is **false across
`z = k`**: at `z = k` the index is `0` and `lam(0) = 0`, so `f(k) = k` while
`f(k-1) = k-1 + lam(1)`, which is `> k` whenever `lam(1) >= 2`. Example: `k = 10`,
`lam(1) = 5` gives `f(9) = 14 > f(10) = 10`. Monotonicity holds only on `z <= k-1`,
where the indices are positive — which is exactly the printed range, so nothing is
lost by restricting, but the un-restricted claim was wrong. The worker m3 had in
fact flagged this boundary ("it steps DOWN past hi — the trap") in the cycle-3
swarm; cycle 3 recorded the trap in one place and asserted the false version in
another. Main's own m3 report noted it; the ledger did not follow.

**Two questions that cycle 3 ran together, kept apart now:**
* *Where is the printed maximum?* Always defined; attained in `{0,...,k-1}` iff the
  state is on `phi`'s domain.
* *When is some non-negative `z` admissible?* Exactly when `k >= 1` and
  `lam(k) <= R` (Lemma MX.2). This is the criterion an implementation needs, and
  it is the one the domain equivalence rests on.

*Verified:* over all 34 222 Case-II states of weight `<= 30`, `S_Z` has a maximum
in every case; on the 33 329 domain states the maximum lies in `{0,...,k-1}` and
both created parts are `>= 0`; on the 893 excluded states the maximum is negative
with `t+5j-3-m <= 0`, first witnesses `(0;())` giving `m = -2`, second part `-1`,
and `(0;(1))` giving `m = -1`, `-1`.

## Corollary MX.4 (the case analysis, and the excluded set)

Assume **Case II**, `L + lam(mu) < 5j + tstar`. Then exactly one of:

| case | hypothesis | conclusion | states (`weight <= 30`) |
| --- | --- | --- | --- |
| 1 | `a <= t`, `mu <= t` | `S` nonempty | 32 480 |
| 2 | `a <= t`, `mu > t` | `S` nonempty | 513 |
| 3 | `a > t+1` | impossible (contradicts Case II) | 0 |
| 4 | `a = t+1`, `j < 0` | impossible (contradicts Case II) | 0 |
| 5 | `a = t+1`, `j > 0` | `S` nonempty | 336 |
| 6 | `a = t+1`, `j = 0` | `S` empty; state is in `0 x B(n)` | 893 |

*Proof of each case.*
* **Case 1.** `a <= t` gives `L >= 1`; then `k - mu = L - 1 >= 0`, so `k >= mu`.
  `mu <= t` gives `tstar = t`, and Case II gives `lam(mu) <= t + 5j - L - 1 <= R`
  because `R - (t+5j-L-1) = L - 1 >= 0`. Since `k >= mu`, `lam` descending gives
  `lam(k) <= lam(mu) <= R`. By MX.2, `S` is nonempty.
* **Case 2.** `mu > t >= a`, so `2j = mu - a + L > t - a + L >= 1`, hence `j >= 1`;
  then `k >= mu > t` gives `lam(k) = 0` and `R = t+5j-2 >= 3 > 0`, so
  `lam(k) <= R` and `k >= mu >= 1`. By MX.2, `S` is nonempty.
* **Case 3.** Minimality at `a-1` with `a-1 > t` gives `lam(a-1) = 0` and
  `2j + a - 1 <= 0`, so `k <= 0`; but `a` minimal also gives `2j + a >= 1`, so
  `k = 0`, `mu = 1`, and `j <= -1`. If `t >= 1` then `a = 1-2j` and `a > t+1` give
  `t <= -2j-1`, so `tstar = t+1` and `5j + tstar = 5j + t + 1 <= 3j < 0`. If
  `t = 0` then `tstar = 2` and `5j + 2 <= -3 < 0`. Either way Case II would need
  `L + lam(mu) < 5j + tstar < 0` against `L + lam(mu) >= 0`. Contradiction.
* **Case 4.** `a = t+1 > t` gives `L = 0` and `k = t+2j`; `j < 0` gives
  `mu = k+1 <= t`. Minimality at `t` gives `2j + t - lam(t) <= 0`, i.e.
  `lam(t) >= k`; since `mu <= t`, `lam(mu) >= lam(t) >= k`. Case II with `L = 0`
  and `tstar = t+1` gives `lam(mu) <= 5j + t < t + 2j = k`. Contradiction.
* **Case 5.** `a = t+1`, `j > 0`: `k = t+2j > t`, so `lam(k) = 0`, and
  `k >= 1`, `R = t+5j-2 >= t+3 > 0`. By MX.2, `S` is nonempty.
* **Case 6.** `a = t+1`, `j = 0`: `k = t`, and minimality at `t` gives
  `lam(t) >= t` when `t > 0`, which with positivity is exactly the condition
  `lambda in B(n)`; conversely `lambda in B(n)` of length `t` with `j = 0` gives
  `lam(t) >= t`, so `a = t+1`. Then `lam(k) = lam(t) >= t > t-2 = R`, so by MX.2
  `S` is empty. For `t = 0` the interval is empty. QED

**Main's independent check.** All 25 assertions of MX.0–MX.4 (each inequality,
each case's conclusion, and exhaustiveness) were checked programmatically over
every Case-II state of weight `<= 30`: **0 failures**. Cases 3 and 4 have
**0 occurrences**, as the proof requires — they contradict Case II. Among the
in-domain states the counts are `32 480 + 513 + 336 = 33 329`, and the 893
excluded states are exactly Case 6, so Case 6 `iff` off-domain.

## Corollary MX.5 (`a = mu` is impossible in Case I)

Cycle 2 left an unexplained second-removal fallback in `phi` Case I for the
possibility `a = mu`. That possibility does not arise.

*Proof.* Suppose `a = mu`. If `a = mu <= t` then `L = lam(a) = lam(mu)` and
`tstar = t`; from `mu = a + 2j - L` and `a = mu` we get `2j = L`, so `j >= 0`,
while Case I gives `2L >= 5j + t`, i.e. `4j >= 5j + t`, i.e. `j <= -t`. Hence
`j = 0` and `t = 0`, contradicting `a = mu <= t`. If `a = mu > t` then `L = 0`,
so `2j = 0` and `j = 0`, `tstar = t+2`, and Case I gives
`0 >= 0 + t + 2`, impossible. QED

*Verified:* `a = mu` occurs on 6 458 states of weight `<= 30`, and **all of them
are Case II**; 0 occurrences in Case I. The fallback in
`Computation/bz82.py` is therefore unreachable and is retained only as an
assertion.

**Cross-check from an independent worker (cycle 3).** `smwg1kdjq`'s m3 wrote a
per-step skeleton auditor whose assertion P3 was the *stronger* claim "`a = mu`
implies `a > t` (both slots virtual)". P3 **fails**, with the minimal witness
`j = 1, lam = (2,)` (weight 4): there `a = mu = 1`, `L = 2 = 2j`, and `a = 1 = t`,
so the surviving slot is **real**. That witness is Case II
(`L + lam(mu) = 4 < 5j + t* = 6`), which is exactly what Lemma MX.5 allows: MX.5
constrains `a = mu` only **inside Case I**, where it forbids it. So the worker's
failed assertion does not threaten MX.5; it *confirms* the boundary, and it shows
that "`a = mu` implies both slots are virtual" is false in Case II. The correct
statement is the one MX.5 proves: `a = mu` never occurs in Case I, hence the
Case-I double deletion always acts on two distinct slots.

## What this does not do

Theorem MX.3 and Corollaries MX.4/MX.5 establish the **definedness** of the
Case-II branch and locate the excluded set. They do not prove:

* that the Case-I inserted count `L + lam(mu) - 5j - tstar` is a non-negative
  integer (it is non-negative only by the Case-I guard, which is by definition
  `>=`; integrality mod 5 must be shown);
* that Case I and Case II are mutually inverse as branches;
* case stability of `phi`;
* that `phi^2 = id`;
* anything about the alternating composition, its termination, or the endpoint;
* any statement about `A_n`, `D_n`, or the Mathathon objective.

## Lemma CI (the Case I → Case II transition)

Status: partly **PROVED**, partly **TESTED_FINITE**. Cycle 3, Main. This supplies
the first half of the case-stability obligation for `phi`; the reverse direction
(II → I) and both compositions remain open and are assigned to the cycle-3 proof
auditor.

Notation as above. Suppose **Case I** holds, `L + lam(mu) >= 5j + t*`, and let
`(j', lam') = phi(j, lam)` with `j' = j+1`. Recompute `a', L', mu'` from
`(j', lam')` by the same definitions.

**Lemma CI.1 (weight).** `|lam'| = |lam| - 5j - 2`, hence
`|lam'| + P(j') = |lam| + P(j) = n`.
*Proof.* The deleted slots carry total value `L + lam(mu)` (this is correct also
when `a > t` or `mu > t`, because then the slot is a virtual 0 and the
corresponding `lam` value is 0 by the padding convention). The remaining `t*-2`
slots each increase by 1, and `N = L + lam(mu) - 5j - t*` ones are inserted, so
`|lam'| = |lam| - L - lam(mu) + (t*-2) + N = |lam| - 5j - 2`. Then
`P(j+1) = P(j) + (5j+2)`. QED

**Lemma CI.2 (`a' = a-1`).** If Case I holds, `a' = a - 1`.
*Proof sketch.* The slots at `a` and `mu` are deleted and every surviving slot is
incremented, so the part that ends at position `a-1` has value `lam(a+1)+1`
(for `a <= t`) or `1` (when a phantom 0 at `a` is deleted); in either case the
smallest index where `2j' + x - lam'_x > 0` is `x = a-1`. QED (This is BZ82's
`abar = a-1`; it is verified below.)

**Lemma CI.3 (the printed strict inequality `mu' > mu` is FALSE; the correct
statement is `mu' >= mu`).**
With `j' = j+1`, `a' = a-1` (CI.2) and `lam'(a-1) = lam(a+1)+1` (BZ82 p.314),

```
mu' = 2j' + a' - lam'(a') = 2j + a - lam(a+1),
mu' - mu = lam(a) - lam(a+1) = L - lam(a+1) >= 0,
```

with equality **iff** `lam(a+1) = lam(a)`, i.e. iff the value at the deletion slot
`a` is repeated.

**The clean witness (cycle 4), on a real slot.** `j = 0, lam = (4,1,1)`:
`a = 2` (a **real** slot, since `a <= t = 3`), `L = 1`, `k = 1`, `mu = 1`, and
`phi(0;(4,1,1)) = (1;(2,1,1))`, at which `a' = 1`, `mu' = 1 = mu`. So the printed
strict inequality fails on a state where both slots are genuine parts — not only
in virtual-slot cases. Cycle 3's example `(-1;())` was a virtual-slot instance;
this one is stronger and should be quoted in preference.

**Source caveat, stated properly (cycle 4).** BZ82 p.314, in the paragraph
following the Case I definition, prints the conclusion
`mu_bar = 2j + a - lam(a+1) > mu` as part of its involution check. **Two separate
claims must not be conflated:** (i) *mathematically*, the strict inequality is
false, with the counterexample above and 5 844 further states at `weight <= 26`
where `mu' - mu = 0`; (ii) *as a reading of the source*, the statement sits in a
three-page note whose OCR corrupts several inequality symbols, and the symbol at
that point has **not** been visually re-verified against a rendered image of
p.314. Main asserts (i) only. The measured distribution of `mu' - mu` over the
10 285 Case-I states of `weight <= 26` is
`0 (5 844), 1 (2 918), 2 (1 087), 3 (344), 4 (80), 5 (12)`.

Nothing is broken by this: the conclusion BZ82 actually needs is that Case II is
selected at the image, and that holds in **all 10 285** states with no exception.

**Verified (TESTED_FINITE, `weight <= 26`):** every Case-I state maps to a state
selecting Case II (10 285 / 10 285); `a' = a-1` (10 285 / 10 285); `mu' >= mu`
(10 285 / 10 285).

## Lemma CII (the Case II → Case I transition)

Status: **TESTED_FINITE** (`weight <= 26`). Cycle 3, Main. This is the other half
of case stability, and it is the piece BZ82 dismisses with "similarly". It is
*not* yet a proof; the empirical content below is what a proof must explain.

Suppose **Case II** holds (so `L + lam(mu) < 5j + t*`), and let
`(j', lam') = phi(j, lam)`, i.e. `j' = j-1`, `lam'` obtained by subtracting 1 from
each of the `t` parts and inserting `m` and `t+5j-3-m`.

**Measured, over all 10 285 Case-II states of weight `<= 26`:**
* the image **always** selects Case I — 10 285 / 10 285, no exception. So
  `phi` toggles the case, in both directions, with no overlap;
* at the image, the recomputed minimal index satisfies **`a' = a + 1`** in
  10 285 / 10 285 states.

Together with CI.2 (`a' = a-1` for Case I → Case II) this gives the clean
symmetry that makes `phi` an involution plausible:

| transition | `a` shift | occurrences |
| --- | --- | --- |
| Case I -> Case II | `a' = a-1` | 10 285 / 10 285 |
| Case II -> Case I | `a' = a+1` | 10 285 / 10 285 |

So the two branches are inverse *at the level of the index `a`*, which is the
structural reason `phi(phi(s)) = s`. A proof should proceed by showing the
Case-II construction recreates exactly the slot pair that Case I deleted, and the
`a`-shift is the visible shadow of that.

**What is still missing** (and is the honest statement of the gap):
`t' - t` is *not* a simple function — measured values range over
`-24 .. +2` with a spread distribution — because the two created parts `m` and
`t+5j-3-m` may be `1`s while decremented parts may vanish, so the length is not
preserved and cannot be used as a progress measure. A proof of `phi^2 = id` must
therefore track the multiset of values, not the length. That is the concrete
difficulty, stated precisely.
