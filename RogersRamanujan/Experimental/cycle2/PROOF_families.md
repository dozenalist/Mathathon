# Infinite families under the BZ82 path: proved closed forms

Direction C (experimental), RR127 cycle 2.  Every statement below is a statement
about **BZ82's published map**, used here only as data source.  Nothing in this
file is a new bijection; it is a structural theorem about where the reference map
sends two parametric rays.

Notation exactly as in the task statement: `P(j) = j(5j-1)/2`, so
`P(-1) = 3`, `P(0) = 0`, `P(1) = 2`; `X(n) = {(j;lam) : |lam| + P(j) = n}`;
`lam(x) = lam_x` for `1 <= x <= t = len(lam)` and `0` otherwise;
`B(n) = {b : every part of b >= len(b)}`; `T(lam)_i = lam_i - k + 2i - 1`,
`Tinv(b)_i = b_i + k - 2i + 1`.

One fact used constantly: **phi Case II** changes `|lam|` by
`(t + 5j - 3) - t = 5j - 3` and sends `j -> j-1`; **phi Case I** deletes two
slots and increments `t*-2` of them, so it changes `|lam|` by
`(t* - 2) + (lam(a)+lam(mu)-5j-t*) - lam(a) - lam(mu) = -5j-2` and sends
`j -> j+1`.  Both equal `-(P(j') - P(j))`, so the weight is preserved in both
cases automatically.  The substance of what follows is *which case fires* and
*what the parts are*.

Every lemma below was machine-checked instance by instance by
`lemma_checks.py` (parameters up to `s <= 200`, `p <= 200`, `r <= 60`);
the proof is the case analysis, the script is the confirmation.

---

## Lemma 0 (one phi collapses the all-ones ray)

For every `s >= 3`:  `phi(0;(1^s)) = (-1;(s-3))`, the part `0` being dropped
when `s = 3`.  For `s in {0,1}` the start is already in `{0} x B`; for `s = 2`
the path is `(0;(1,1)) -> (1;()) -> (0;(2))`.

**Proof.**  `j = 0`, `lam = (1^s)`, `t = s`, so `lam(1) = lam(2) = 1` and
`lam(x) = 0` for `x > s`.  Then `x - lam(x) = 0` at `x = 1` and `= 1 > 0` at
`x = 2`, so `a = 2`, and `mu = 0 + 2 - lam(2) = 1`.  Hence
`lam(a) = lam(mu) = 1` and `t* = t = s` (both `a, mu <= s`).  Case I needs
`lam(a) + lam(mu) = 2 >= 5j + t* = s`, i.e. `s <= 2`.  So for `s >= 3` Case II
fires.  There `a + 2j - 2 = 0`, so the admissible set is `{0}` alone, and
`0 + lam(1) = 1 <= t + 5j - 2 = s - 2` holds exactly because `s >= 3`; thus
`m = 0` and the maximum exists.  Every part is `1`, so "subtract 1 from each of
the `t` parts" discards all of them, `m = 0` is discarded, and the only created
part is `t + 5j - 3 - m = s - 3`.  `j -> -1`.  QED

`s = 2` check: `a = 2, mu = 1, lam(a)+lam(mu) = 2 >= t* = 2`, Case I; deleting
slots `1,2` leaves nothing, `lam(a)+lam(mu)-5j-t* = 0` ones are inserted,
`j -> 1`, giving `(1;())`.  Then `psi` on `(1;())`: `t0 = m2 = 0`, `j = 1 > 0`
so Case I, `thr = 5*0+5*1-3 = 2 >= m2 = 0` so I(a), no part is `0 (mod 5)`,
part `2` is inserted, `j -> 0`: `(0;(2))`, and `(2) in B(2)`.  QED

Consequence: **the whole all-ones ray is one phi step away from a state with a
single part.**  All remaining work is psi on singletons, which Lemma 1 settles.

## Lemma 1 (psi on a singleton)

Let `p >= 0` and take `(j;lam) = (-1;(p))` (empty `lam` when `p = 0`).  Put
`r = p mod 5`.

| `p` | `psi(-1;(p))` | terminal in `B`? |
|---|---|---|
| `p = 0` | `(0;(3))` | yes |
| `r = 0, p >= 5` | `(0;(p+3))` | yes |
| `r in {1,4}` (with `p >= 6` resp. `p >= 4`) | `(0;(p,3))` | yes |
| `r = 2, p >= 2` | `(0;(5^k))`, `k = (p+3)/5` | iff `k <= 5` |
| `r = 3, p = 3` | `(0;(3,3))` | yes |
| `r = 3, p >= 8` | `(-2;(p-8))` | no (`j != 0`) |

**Proof, common part.**  `t = [p > 0]`, and the residue data are
`t0 = [r = 0]` (`t0 = 0` for `p = 0`), `m0 = p` if `r = 0` else `0`,
`m2 = p` if `r = 2` else `0`, `m3 = p` if `r = 3` else `0`.

*`r = 0`.*  `m2 = 0` and `t0 + j = t0 - 1 <= 0`, so Case II (for `p = 0` also
Case II since `t0 + j = -1`, `m2 = 0`).  There `thr = m3 + 5j - 3 = -8` and
`-8 >= m0 = p` is false for every `p >= 0`, so II(b) fires:
`new = m0 - 5j - 2 = p + 5 - 2 = p + 3 > 0`, the part `m0 = p` is deleted when
`p > 0` (nothing is deleted when `p = 0`), `p+3` is created, `j -> 0`.  For
`p > 0` the result is `(0;(p+3))`; for `p = 0` it is `(0;(3))` because
`0 - 5(-1) - 2 = 3`.  A one-part partition is always in `B`.  QED

*`r in {1,4}`.*  `t0 = m0 = m2 = m3 = 0`, `t0 + j = -1 <= 0`, so Case II;
`thr = -8 < 0 = m0`, so II(b): `new = 0 - 5(-1) - 2 = 3 > 0`, nothing is
deleted, `3` is created, `j -> 0`, giving `(0;(p,3))` after sorting.  This is a
partition iff `p >= 3`, i.e. `p >= 4` in class `4` and `p >= 6` in class `1`, and
then `len = 2` with `min = 3 >= 2`, so it lies in `B`.  (For `p = 1` the sorted
result is `(3,1)`, which is **not** in `B(4)` because `1 < 2`; that single value
is the exception recorded in Theorem F.)  QED

*`r = 2`.*  `m2 = p > 0`, so Case I.  `thr = 5t0 + 5j - 3 = 0 - 5 - 3 = -8` and
`-8 >= m2 = p` is false since `p >= 2`, so I(b) fires: the part `m2 = p` is
deleted, `5` is added to every part `= 0 (mod 5)` (there are none, `t0 = 0`), and
`(m2 - 5j - 2 - 5t0)/5 = (p + 3)/5 = k` copies of `5` are created, `j -> 0`.
Result `(0;(5^k))`.  A partition of `k` parts, all equal to `5`, lies in `B` iff
`5 >= k`.  QED

*`r = 3`.*  `t0 = m0 = m2 = 0`, so Case II; `thr = m3 + 5j - 3 = p - 8`, and
II(a) fires iff `p - 8 >= m0 = 0`, i.e. `p >= 8`.  For `p = 3`, II(b) gives
`new = 3`, appended, `j -> 0`: `(0;(3,3))` with `len = 2`, `min = 3 >= 2`, so in
`B`.  For `p >= 8`, II(a) replaces the part `m3 = p` by `p - 8` (deleting it when
that is `0`, i.e. at `p = 8`) and sets `j -> -2`: `(-2;(p-8))`.  QED

## Lemma 2 (the six-step chain, `p = 3 mod 5`, `p >= 8`)

```
(-1;(p)) --psi--> (-2;(p-8)) --phi--> (-1;(1^p)) --psi--> (0;(3,1^p))
         --phi--> (-1;(p-2,2)) --psi--> (0;(p-2,5)) in B(p+3).
```

**Proof.**  Step 1 is Lemma 1, `r = 3`.  For the remaining four steps write
`q = p - 8 >= 0`; note `q = 0 mod 5`.

*Step 2: `phi(-2;(q)) = (-1;(1^p))`.*  `j = -2`, `lam = (q)` (empty if `q = 0`),
`t = [q > 0]`, `lam(1) = q`, `lam(x) = 0` for `x >= 2`.  At `x = 1` the test
value is `-4 + 1 - q = -3 - q < 0`; at `x in {2,3,4}` it is `-2,-1,0`; at `x = 5`
it is `-4 + 5 - 0 = 1 > 0`.  So `a = 5` and `mu = -4 + 5 - 0 = 1`; `a > t`
always and `mu > t` iff `q = 0`.  Hence `lam(a) = 0`, `lam(mu) = q` and
`t* = t + 1 + [q = 0]`, so `t* <= 2`.  Case I needs
`lam(a) + lam(mu) = q >= 5j + t* = -10 + t*`, i.e. `q >= -8`; true.  Case I
deletes the slots at `5` (virtual) and at `1` (the real part `q`, when `q > 0`),
adds `1` to every remaining slot (there are none), and inserts
`lam(a) + lam(mu) - 5j - t* = q + 10 - t*` ones, with `j -> -1`.  For `q > 0`:
`t = 1`, `t* = 2`, so `q + 8 = p` ones and the part `q` is gone.  For `q = 0`:
`t = 0`, `t* = 2`, so `10 - 2 = 8 = p` ones.  Either way `(-1;(1^p))`.  QED

*Step 3: `psi(-1;(1^p)) = (0;(3,1^p))`.*  All parts are `1`, so
`t0 = m0 = m2 = m3 = 0`; `t0 + j = -1 <= 0` and `m2 = 0`, so Case II;
`thr = -8 < 0 = m0`, so II(b): `new = 3`, nothing deleted, `3` created,
`j -> 0`.  QED

*Step 4: `phi(0;(3,1^p)) = (-1;(p-2,2))`.*  `j = 0`, `t = p+1`, `lam(1) = 1`,
`lam(2) = 1` (`p >= 8`), `lam(3) = 3`.  `1 - lam(1) = 0` and
`2 - lam(2) = 1 > 0`, so `a = 2`, `mu = 0 + 2 - 1 = 1`,
`lam(a) = lam(mu) = 1`, `t* = t = p+1`.  Case I needs `2 >= p+1`, false for
`p >= 8`, so Case II.  There `a + 2j - 2 = 0`, so `z = 0` only, and
`0 + lam(1) = 1 <= t + 5j - 2 = p - 1` (true), hence `m = 0`.  Subtracting `1`
from every part leaves `(2)` (the `1`s vanish), `m = 0` is discarded,
`p - 2 = t + 5j - 3 - m` is created, `j -> -1`.  QED

*Step 5: `psi(-1;(p-2,2)) = (0;(p-2,5))`.*  `p = 3 mod 5` gives `p - 2 = 1 mod 5`,
so the parts are `= 1,2 (mod 5)`; hence `t0 = m0 = m3 = 0` and `m2 = 2 > 0`.
Case I fires (`m2 > 0`).  `thr = 0 - 5 - 3 = -8 < m2 = 2`, so I(b): the part `2`
is deleted, `5` is added to every part `= 0 (mod 5)` (none), and
`(2 - 5(-1) - 2 - 0)/5 = 1` copy of `5` is created, `j -> 0`.  Result
`(0;(p-2,5))`, which has two parts, the smaller `5 >= 2`, so it lies in `B`.
QED

## Theorem F (the all-ones ray, closed form)

Write `b(s)` for the `B`-endpoint of `(0;(1^s))` and
`lam(s) = Tinv(b(s)) in D_s`.

| `s` | `b(s)` | `lam(s)` |
|---|---|---|
| `0` | `()` | `()` |
| `1` | `(1)` | `(1)` |
| `2` | `(2)` | `(2)` |
| `4` | `(2,2)` | `(3,1)` |
| `6` | `(3,3)` | `(4,2)` |
| `s = 3 mod 5`, `s >= 3` | `(s)` | `(s)` |
| `s = 2 mod 5`, `s >= 7` | `(s-3, 3)` | `(s-2, 2)` |
| `s = 4 mod 5`, `s >= 9` | `(s-3, 3)` | `(s-2, 2)` |
| `s = 1 mod 5`, `s >= 11` | `(s-5, 5)` | `(s-4, 4)` |
| `s = 0 mod 5`, `5 <= s <= 25` | `(5^{s/5})` | `(6 + s/5 - 2i)_{i=1..s/5}` |
| `s = 0 mod 5`, `s >= 30` | **no closed form claimed** | --- |

**Proof.**  For `s >= 3` Lemma 0 gives `(-1;(s-3))`, so apply Lemma 1 with
`p = s - 3`.
* `s = 3 mod 5` iff `p = 0 mod 5`: Lemma 1 gives `(0;(p+3)) = (0;(s))`, in `B`.
* `s = 2 mod 5` iff `p = 4 mod 5`: `p >= 4` iff `s >= 7`; Lemma 1(b) gives
  `(0;(p,3)) = (0;(s-3,3))`, in `B`.
* `s = 4 mod 5` iff `p = 1 mod 5`: `p >= 6` iff `s >= 9`; `(0;(s-3,3))`.  The
  excluded value `p = 1` (`s = 4`) is the computed exception `(2,2)`.
* `s = 1 mod 5` iff `p = 3 mod 5`: for `p >= 8` (`s >= 11`) Lemma 2 gives
  `(0;(p-2,5)) = (0;(s-5,5))`, in `B`.  The excluded value `p = 3` (`s = 6`) is
  the computed exception `(3,3)`.
* `s = 0 mod 5` iff `p = 2 mod 5`: Lemma 1(c) gives `(0;(5^{(p+3)/5}))` with
  `(p+3)/5 = s/5`, in `B` iff `s/5 <= 5`, i.e. `s <= 25`.  For `s >= 30` the
  two-step output is provably **not** in `B` (it has `s/5 > 5` parts, all equal
  to `5`), so the mechanism of Lemmas 0-1 cannot close there; no other closed
  form is claimed.
The D-side column is `Tinv` applied to the `B`-side column:
`Tinv((s)) = (s)`; `k = 2`, `b = (s-3,3)` gives `(s-3+1, 3-1) = (s-2,2)`;
`k = 2`, `b = (s-5,5)` gives `(s-4,4)`; `k = s/5`, `b = (5^k)` gives
`5 + k - 2i + 1 = 6 + k - 2i`.  QED

**What Theorem F does and does not say.**  It pins the endpoint of one A-object
per weight, with a proof that is uniform in `s` (no finite range) for four of
the five residue classes.  It does **not** give a bijection, and it does not
cover the fifth class beyond `s = 25`.  The list of `b` for `s = 0..60` is in
`DATA.md` F1; the fifth class is where BZ82's orbit suddenly lengthens
(`steps = 2` for `s <= 25`, then `220, 574, 124, 452, 44, 454, 672` for
`s = 30,35,...,60`).

## Theorem G (the all-fours ray)

| `r` | statement | status |
|---|---|---|
| `0 <= r <= 4` | `(4^r) in B(4r)`, `b(r) = (4^r)`, `lam = Tinv((4^r)) = (r+5-2i)_{i=1..r}`, 0 steps | PROVED |
| `5 <= r <= 8` | `phi(0;(4^r)) = (1;(5^{r-2},1^{8-r}))` | PROVED (first step only) |
| `r = 8` | `psi(1;(5^6)) = (0;(32))`, so `b(8) = (32)` in 2 steps | PROVED |
| `r >= 9` | `phi(0;(4^r)) = (-1;(r-6,3,3^r))` | PROVED (first step only) |

**Proof of the `r <= 4` row.**  `(4^r)` has `r` parts, the smallest `4 >= r`;
so it is in `B(4r)` and the iteration stops at step `0`.  Then
`Tinv((4^r))_i = 4 + r - 2i + 1 = r + 5 - 2i`, which is positive for
`i <= r <= 4`, so it is a partition, and it is a gap partition because
consecutive entries differ by `2`.

**Proof of the `r in [5,8]` row.**  `j = 0`, `lam = (4^r)`, `t = r >= 5`, so
`lam(x) = 4` for `1 <= x <= r`.  `1 - 4, 2 - 4, 3 - 4, 4 - 4` are `<= 0` and
`5 - lam(5) = 1 > 0`, so `a = 5` and `mu = 0 + 5 - lam(5) = 1`.
Both `a, mu <= t`, so `t* = t = r`; `lam(a) + lam(mu) = 4 + 4 = 8`, and Case I
needs `8 >= r`.  Deleting the slots at `5` and `1` (both real, both `4`) leaves
`r - 2` parts `4`, each incremented to `5`, and
`8 - r` ones are inserted, `j -> 1`:
`(1;(5^{r-2},1^{8-r}))`.  QED

**Proof of the `r = 8` row.**  `(1;(5^6))`: `t0 = 6`, `j = 1`, `m2 = 0`, so
Case I (`t0 + j = 7 > 0`); `thr = 30 + 5 - 3 = 32 >= m2 = 0`, so I(a): the six
parts `5` each lose `5` and are dropped, `32` is inserted, `j -> 0`.  QED

**Proof of the `r >= 9` row.**  `a = 5`, `mu = 1`, `lam(a) = lam(mu) = 4`,
`t* = r`, so Case I needs `8 >= r`: false.  Case II fires with
`a + 2j - 2 = 3`; for `0 <= z <= 3` the index `4 - z` lies in `{1,2,3,4} <= t`
and `lam(4-z) = 4`, so the constraint is `z + 4 <= t + 5j - 2 = r - 2`, i.e.
`z <= r - 6`, which holds for all `z <= 3` exactly when `r >= 9`.  So the
admissible set is the whole range and the maximum is `m = 3`.  Subtracting `1`
from the `r` parts gives `3^r`; the created parts are `m = 3` and
`r - 6` (`= t + 5j - 3 - m = r - 3 - 3`), both positive for `r >= 9`, and
`r - 6 >= 3`, so the descending order is respected.  QED

**What Theorem G does not say.**  For `5 <= r <= 7` the after-`phi` state is
`(1;(5^{r-2},1^{8-r}))`, which is not in `B` (it has `1`s), and I have no
closed form for the rest of the path.  For `r >= 9` I have only the first
step, and the endpoints `(12,8), (19,5), (14,11,3), (15,11,6,4), ...` show no
pattern: first coordinates for `r = 5..20` are
`12,19,14,32,15,15,25,30,36,30,17,23,20,17,18,35` and lengths
`2,2,3,1,4,4,3,2,3,5,6,5,5,5,5,3`.  No monotone, periodic or affine law
survives; that is reported as a failure, not smoothed over.

## Which checks are independent

* The proofs are case analyses on the printed rules; the scripts instantiate
  them, so `lemma_checks.py` is a check of *transcription*, not of the case
  analysis.  The case analysis is the mathematical content and is written above.
* `Theorem F end-to-end` in `lemma_checks.py` uses the committed
  `Computation/bz82.py`, i.e. a second implementation, so an error in one
  transcription shows up as a mismatch.  That is the strongest cross-check here.
* `family_rules.py` recomputes `Tinv` from the closed formula instead of calling
  `rr_core.Tinv`, so the D-side column is a second route.
* The counts `|A_n| = |D_n|` are **not** used anywhere in this file; nothing
  here rests on the counting identity.
