# Amended all-`n` proof that `psi` is an involution on `X(n) \ {0} x A(n)`

RR127, cycle 2, direction B (proof audit), member m1.

This document **replaces** §3 of `Experimental/swarm_smwfxwsqf/m3/README.md`
(the cycle-1 written argument, incorporated into `Main/CLAIMS.md` RR-C008) as
the proof of record. It is written out in full rather than patched, because two
of the cycle-1 steps are false as stated and two more are true but unargued.
The executable counterpart is `psi_audit.py`; every numbered step below is
asserted there, state by state, on every state of `X(n)` for `n <= 30`.

Status vocabulary as in `Main/CLAIMS.md`. **Claim proved here: `psi` is a
well-defined involution of `X(n) \ {0} x A(n)` for every `n >= 0`.** The only
inputs not proved here are the three tie-break readings, which are *forced*
(cycle-1 evidence, RR-X006 / D-3a); step (d5) below isolates exactly where an
equality can occur, so the forcing is visible inside the proof.

---

## 0. The two errors in the cycle-1 argument, and what replaces them

**E1 (case stability, II(b)).** Cycle 1 wrote `t0' = t0 - 1` unconditionally.
False whenever `m0 = 0`: then no `0 (mod 5)` part is removed, a part
`mu = -5j-2 = 3 (mod 5)` is *created*, and `t0' = 0 = t0`. Witness
`(-1;()) -> (0;(3))`. As stated the claim is not merely false but impossible
(`t0 = 0` would give `t0' = -1`). Repair: Lemma 4(II(b)) below, split at
`m0 = 0`, with the stability inequality proved from `j <= -1`.

**E2 (branch inverse, II(a) with `nu = m3+5j-3 = 0`).** Cycle 1 wrote
`m3' <= m3 - 5`. False when the largest `3 (mod 5)` part is repeated: witness
`(0;(3,3)) -> (-1;(3))` retains `m3' = 3 = m3`. Sharp form (Lemma 6.2 below):
`m3' = m3` iff `m3` is repeated, and `m3' <= m3-5` holds only if `m3` is simple
*and* `m3 >= 8` (for `m3 = 3` simple one gets `m3' = 0 > -2`). Repair: the
weaker bound `m3' <= m3`, which suffices:
`m3' + 5(j-1) - 3 <= m3 + 5j - 8 = nu - 5 = -5 < 0 = m0'`.

**E3 (unargued, true).** Cycle 1's II(a) stability step says
"`m3+5j-3` is `= 0 (mod 5)` when positive". True only for `m3 > 0`; for
`m3 = 0` one has `nu = 5j-3 = 2 (mod 5)` and the *created* part would be
`2 (mod 5)`, destroying `m2' = 0`. It cannot happen, but that needs the
argument in Lemma 4(II(a)). Same for I(b): cycle 1's `k = (m2-N-5)/5` is
integral only because `m2 > 0` there, which also needs an argument
(Lemma 2.2). Both are supplied.

**E4 (arithmetic slip, cosmetic).** Cycle 1 wrote `<= -13` in the `nu = 0`
case of II(a); the correct value for the *false* bound is `-10`, and for the
*correct* bound `-5`. Recorded already in RR-C008; restated here so the numbers
in this file are self-consistent.

---

## 1. Notation and standing facts

`X(n) = {(j;lambda) : j in Z, lambda a partition (descending tuple of positive
integers), |lambda| + P(j) = n}` with `P(j) = j(5j-1)/2`. `()` is the partition
of 0. For a state `(j;lambda)` put

    t   = len(lambda),          lam(x) = lambda_x for 1 <= x <= t,  lam(x) = 0 for x > t,
    t0  = #{parts of lambda that are = 0 (mod 5)},
    m_r = max{part = r (mod 5)},  or 0 if there is no such part   (r = 0,2,3).

`A(n)` = partitions of `n` with all parts `= 1 or 4 (mod 5)`.
`Dom(n) := X(n) \ ({0} x A(n))`.

    F1:  P(j-1) = P(j) - (5j-3)          F2:  P(j+1) = P(j) + (5j+2)
    F3:  m_r = 0 or m_r = r (mod 5) and m_r >= 1
    F4:  if lambda has no part = r (mod 5) then m_r = 0

`psi` is the four-branch rule quoted in the brief. `Case I` means
`t0 + j > 0 or m2 > 0`; `Case II` means `t0 + j <= 0 and m2 = 0`.

**Lemma 1.1 (Case II forces `j <= 0`).** `t0 >= 0`, so `t0 + j <= 0` gives
`j <= -t0 <= 0`. In particular `5j - 3 <= -3` and `-5j >= 0`.

**Lemma 1.2 (signed weight).** In each of the four branches `|lambda|` changes by
exactly **`5j-3`** (I(a), II(a)) or **`-5j-2`** (I(b), II(b)), i.e. by
`-(P(j')-P(j))` where `P(j) = j(5j-1)/2`. Hence the **signed** weight
`|lambda| + P(j)` is preserved.

*[Amended by Main, cycle 3: the cycle-2 statement printed `-5j+3` for
I(a)/II(a), which contradicts the lemma's own calculation (`-5t0` from the
dropped multiples of 5 plus `+N = 5t0+5j-3` gives `+5j-3`) and contradicts
`-(P(j-1)-P(j)) = +(5j-3)`. Statement corrected; the proof text was already
right. The heading is also corrected from "weight" to "signed weight", because
`|lambda'|` alone is not `n` after a `j`-changing step.]*

*Proof.* I(a): every part `= 0 (mod 5)` loses 5, those equal to 5 are dropped,
which is a loss of `5t0`; the inserted part is `N = 5t0+5j-3`. Net `5j-3`.
I(b): one copy of `m2` is deleted (`-m2`), each of the `t0` parts `= 0 (mod 5)`
gains 5 (`+5t0`), and `k = (m2-5j-2-5t0)/5` copies of 5 are created (`+5k`);
net `-m2+5t0+(m2-5j-2-5t0) = -5j-2`. II(a) with `m3 >= 1`:
`+nu - m3 = 5j-3`. II(a) with `m3 = 0`: `+nu = 5j-3` (unreachable, Lemma 4).
II(a) with `nu = 0`: `-m3 = 5j-3`. II(b) with `m0 > 0`: `+mu - m0 = -5j-2`.
II(b) with `m0 = 0`: `+mu = -5j-2`. Compare with F1, F2. QED

## 2. Where the rules can fail: the domain is derived, not imposed

**Lemma 2.1 (positivity).** All parts produced by I(a), I(b), II(a) are
`>= 1`, and by II(b) except in the single configuration `m0 = 0, j = 0`.

*Proof.* I(a): `N = 5(t0+j)-3 = 2 (mod 5)` and the guard is `N >= m2 >= 0`, so
`N >= 2`; reduced parts that would reach 0 are dropped. I(b): `m2 >= 2`
(Lemma 2.2), the deleted part is `m2 >= 2`, and other parts only grow.
II(a): `nu >= m0 >= 0` and `nu = 0` means deletion, not a part 0. II(b):
`mu = m0-5j-2`. If `m0 > 0` then `m0 = 0 (mod 5)` forces `m0 >= 5`, so by
Lemma 1.1 `mu >= 3-5j >= 3`. If `m0 = 0` then `mu = -5j-2`, which is `>= 3` for
`j <= -1` and `-2` for `j = 0`. QED

**Lemma 2.2 (I(b) never runs with `m2 = 0`, and `k` is a non-negative
integer).** If I(b) is selected then `m2 >= 2` and `k = (m2-N-5)/5 >= 0`.

*Proof.* I(b) means Case I and `N < m2`. If `m2 = 0` this reads
`5(t0+j)-3 < 0`, i.e. `t0+j <= 0`, i.e. Case II — contradiction. So `m2 >= 2`,
and by F3 `m2 = 2 (mod 5)`; also `N = 2 (mod 5)`. Hence `m2-N` is a positive
multiple of 5, so `m2-N >= 5` and `k = (m2-N-5)/5 >= 0`. (This is the
integrality argument cycle 1 omitted; it is exactly why the `m2 = 0` case of
I(b) is empty.) QED

**Lemma 2.3 (the domain is exactly `X(n) \ {0} x A(n)`).** `psi` produces a
valid signed state of the **same signed weight** `|lambda| + P(j) = n` on a state
`s` iff `s` is not of the form `(0;lambda)` with `lambda in A(n)`.

*[Amended by Main, cycle 3: the cycle-2 wording said the output is "a partition
of weight n". That is the wrong invariant: after `j -> j+1` the partition alone
has weight `n - P(j+1)`, not `n`. The correct statement, which the proof below
actually establishes via Lemma 1.2, is preservation of the signed weight
`|lambda| + P(j)`, together with validity (all parts positive).]*

*Proof.* By Lemmas 1.2 and 2.1 the only failing configuration is II(b) with
`m0 = 0, j = 0`. Then `t0 = 0` (as `m0 = 0`), `m2 = 0` (Case II), and II(b)
selected gives `nu = m3+5j-3 = m3-3 < m0 = 0`, so `m3 <= 2`, and by F3
`m3 = 0`. So `lambda` has no part `= 0, 2, 3 (mod 5)`, i.e. every part is
`= 1 or 4 (mod 5)`, i.e. `lambda in A(n)`; and `j = 0`. Conversely if
`s = (0;lambda)`, `lambda in A(n)`, then `t0 = m2 = m0 = m3 = 0`, Case I fails,
`nu = -3 < 0 = m0` so II(b) is selected, and `mu = -2`. QED

## 3. Case stability

**Lemma 3.** For `s in Dom(n)`, `psi(s) in Dom(n)` lies in the same top-level
case as `s`.

*Proof, branch by branch.*

**(i) I(a) -> Case I.** `N = 2 (mod 5)` is a created part and `N >= 2`, so
`m2' >= N > 0`. QED

**(ii) I(b) -> Case I.** `t0' = t0 + k` (the `t0` parts `= 0 (mod 5)` stay so
and the `k` created 5s are `= 0 (mod 5)`; `m2 = 2 (mod 5)` is not), `j' = j+1`,
so `5(t0'+j') = 5t0+5k+5j+5 = m2+3 > 0` since `m2 >= 2` (Lemma 2.2). Hence
`t0'+j' >= 1`. QED

**(iii) II(a) -> Case II.** First, `m3 >= 1`: else `nu = 5j-3 >= m0 >= 0`
gives `j >= 1`, contradicting Lemma 1.1. Hence `nu = (mod 5)` value
`m3+2 = 0`, so the part created when `nu > 0` is `= 0 (mod 5)`, and the part
deleted when `nu = 0` is `m3 = 3 (mod 5)`. Therefore `t0' = t0 + [nu>0]`, and
`t0' + j' <= t0+1+j-1 = t0+j <= 0`. Also no part `= 2 (mod 5)` is created or
destroyed, so `m2' = m2 = 0`. QED *[This is E3: the parenthetical of cycle 1
is false for `m3 = 0`; the case is excluded here, not assumed.]*

**(iv) II(b) -> Case II.**
*Sub-case `m0 > 0`.* One copy of `m0` is replaced by `mu = 3 (mod 5)`, so
`t0' = t0-1`; `j' = j+1`; hence `t0'+j' = t0+j <= 0`; nothing `= 2 (mod 5)` is
created, so `m2' = 0`. QED
*Sub-case `m0 = 0`. [E1, Repair 1]* Then `t0 = 0` and no part `= 0 (mod 5)` is
created (`mu = 3 (mod 5)`), so `t0' = 0 = t0` — **not** `t0-1`. Thus
`t0'+j' = j+1`, and the needed inequality is `j <= -1`. Suppose `j = 0`. Case II
holds (`t0+j = 0 <= 0`, `m2 = 0`); II(b) selected means `nu = m3-3 < m0 = 0`,
so `m3 = 0`; then `lambda` has no part `= 0,2,3 (mod 5)`, i.e.
`lambda in A(n)`, and `j = 0`, i.e. `s in {0} x A(n)`, excluded. Hence on
`Dom(n)`, `j <= -1` and `t0'+j' = j+1 <= 0`. `m2' = 0` as nothing
`= 2 (mod 5)` is made. QED

**Remark 3.4 (`psi(s')` is defined).** By Lemma 2.3 it is enough that
`s' = psi(s)` is not in `{0} x A(n)`. A state of `{0} x A(n)` has `j = 0`,
`t0 = 0`, `m2 = 0`. After I(a), I(b) we are in Case I, which no such state is,
so `s'` is not in the excluded set. After II(a), `j' = j-1 <= -1`. After II(b),
`lambda'` always contains the part `mu = 3 (mod 5)` (equal to `-5j-2` when
`m0 = 0`, to `m0-5j-2 >= 8` when `m0 > 0`), and `A(n)` contains no part
`= 3 (mod 5)`, so `lambda'` is never in `A(n)`. QED

## 4. The four branches are mutually inverse

Throughout, `s = (j;lambda) in Dom(n)` and `s' = psi(s) = (j';lambda')`.

**4.1 I(a) -> I(b).** Let `N = 5t0+5j-3` and `s5 = #{copies of 5 in lambda}`.
By I(a), `lambda'` = (the `t0` parts `= 0 (mod 5)` each minus 5, the `s5`
copies that reach 0 dropped) together with `N`. Hence `t0' = t0 - s5` and
`m2' = N` (the parts `= 2 (mod 5)` of `lambda` are `<= m2 <= N`, and `N`
itself is present with `N = 2 (mod 5)`). Apply `psi` to `s'`: Case I by
Lemma 3(i). `N' := 5t0'+5j'-3 = 5(t0-s5)+5(j-1)-3 = N - 5s5 - 5 < N = m2'`, so
**I(b)** is selected. I(b) deletes the copy of `N`, adds 5 to each of the
`t0' = t0-s5` parts `= 0 (mod 5)` (restoring the ones that survived), creates
`k' = (m2'-N'-5)/5 = (N-(N-5s5-5)-5)/5 = s5` copies of 5 (restoring the ones
that were dropped), and sets `j'' = j-1+1 = j`. Result: `lambda`. QED

**4.2 I(b) -> I(a).** `N = 5t0+5j-3 < m2`. `lambda'` = `lambda` minus one copy
of `m2`, every part `= 0 (mod 5)` increased by 5, plus `k` copies of 5 where
`k = (m2-5j-2-5t0)/5 >= 0` (Lemma 2.2). So `t0' = t0+k` and `m2' <= m2` (only
`= 2 (mod 5)` parts of `lambda` survive, one `m2` removed). Apply `psi` to
`s'`: Case I by Lemma 3(ii), and
`N' = 5t0'+5j'-3 = 5t0+5k+5j+5-3 = m2 >= m2'`, so **I(a)** is selected.
*(4.2a: equality `N' = m2'` occurs exactly when `m2` is repeated in `lambda`;
the `>=` reading of decision 1 handles equality; either way I(a) is selected,
so 4.2 needs only `N' >= m2'`.)*
I(a) subtracts 5 from each part `= 0 (mod 5)` of `lambda'`: the `k` copies of 5
vanish, the `t0` originals return to their `lambda` values; and it inserts
`N' = m2`. So `lambda` is restored and `j'' = j+1-1 = j`. QED

**4.3 II(a) -> II(b).** `nu = m3+5j-3 >= m0`, `m3 >= 1` (Lemma 3(iii)), so
`nu = 0 (mod 5)`.
*Case `nu > 0`.* `lambda'` = `lambda` with one copy of `m3` replaced by `nu`.
Then `m0' = nu` (the parts `= 0 (mod 5)` of `lambda` are `<= m0 <= nu`) and
`m3' <= m3` (one copy of the largest part `= 3 (mod 5)` was removed; the bound
`m3' <= m3-5` used in cycle 1 is **false**, see 6.2). Apply `psi` to `s'`:
Case II by Lemma 3(iii) and
`m3'+5j'-3 = m3'+5(j-1)-3 <= m3+5j-8 = nu-5 < nu = m0'`, so **II(b)** is
selected. II(b) replaces `m0' = nu` by `nu-5j'-2 = (m3+5j-3)-5(j-1)-2 = m3`,
restoring `lambda`, and `j'' = j-1+1 = j`. QED
*Case `nu = 0`. [E2, Repair 2]* Then `m3 = 3-5j = 3 (mod 5) >= 1`, and
`nu >= m0` gives `m0 = 0`. `lambda'` = `lambda` minus one copy of `m3`; hence
`m0' = 0`, `m2' = 0` (Lemma 3(iii)), and `m3' <= m3`, with equality exactly
when `m3` is repeated. Apply `psi` to `s'`: Case II by Lemma 3(iii), and
`m3'+5j'-3 <= m3+5j-8 = (3-5j)+5j-8 = -5 < 0 = m0'`, so **II(b)** is selected.
Here `m0' = 0`, so II(b) *creates* the part `m0'-5j'-2 = -5(j-1)-2 = 3-5j = m3`,
restoring `lambda`, and `j'' = j`. QED

**4.4 II(b) -> II(a).** `nu = m3+5j-3 < m0`. Put `mu = m0-5j-2`; then
`mu > m3-5` (from the guard) and `mu = 3 (mod 5) = m3 (mod 5)` when `m3 > 0`,
so `mu >= m3` always (if `m3 = 0` this is `mu >= 3 > 0`).
*Sub-case `m0 > 0`.* `lambda'` = `lambda` with one copy of `m0` replaced by
`mu`. So `m3' = mu` (parts `= 3 (mod 5)` of `lambda` are `<= m3 <= mu`, and
`mu` is present) and `m0' <= m0`. Apply `psi` to `s'`: Case II by
Lemma 3(iv), and `m3'+5j'-3 = mu+5(j+1)-3 = (m0-5j-2)+5j+5-3 = m0 >= m0'`, so
**II(a)** is selected. *(4.4a: equality `m0 = m0'` occurs exactly when `m0` is
repeated; the `>=` reading of decision 2 handles it.)* II(a) replaces
`m3' = mu` by `mu+5j'-3 = mu+5(j+1)-3 = m0 > 0` (no deletion), restoring
`lambda`, and `j'' = j+1-1 = j`. QED
*Sub-case `m0 = 0`.* Then `t0 = 0`, `j <= -1` (Lemma 3(iv)), and `lambda'` =
`lambda` plus the created part `mu = -5j-2 >= 3`; so `m0' = 0`, `m2' = 0`,
`m3' = mu` (as `mu >= m3`). Apply `psi` to `s'`: Case II since
`t0'+j' = j+1 <= 0` by `j <= -1`, and
`m3'+5j'-3 = mu+5(j+1)-3 = 0 >= 0 = m0'`, so **II(a)** is selected, with
`nu' = 0`; II(a) then deletes `m3' = mu` (the "delete it when that is 0"
clause), restoring `lambda`, and `j'' = j`. QED

## 5. Conclusion

**Theorem 5.1.** For every `n >= 0`, `psi` is a well-defined involution of
`Dom(n) = X(n) \ ({0} x A(n))`.

*Proof.* For `s in Dom(n)`, Lemma 2.3 gives `psi(s) in X(n)` (weight `n` by
Lemma 1.2). Lemma 3 gives that `psi(s)` is in `Dom(n)` (Remark 3.4) and in the
same top-level case. Section 4 then identifies `psi(psi(s)) = s` in each of the
four branches. QED

**Corollary 5.2.** `X(n) = ({0} x A(n)) ⊔ (2-element psi-orbits)`, each orbit
with opposite signs, whence `sum_{j in Z} (-1)^j p(n - j(5j-1)/2) = |A_n|`.
(Not used below; recorded because it is the arithmetic payload of the theorem.)

**n = 0.** `P(j) = 0` only for `j = 0`, so `X(0) = {(0;())}`; `() in A(0)`, so
`Dom(0) = {}` and the theorem is vacuous. Note `(0;())` is exactly the excluded
set, so `psi` has *no* legal input at `n = 0`; a proof obligation at `n = 0`
would be vacuous, not missing.

## 6. The complete virtual-zero and multiplicity census

Every configuration in which one of `m0, m2, m3` is `0` ("virtual zero"), or in
which a largest part is repeated, is listed. `psi_audit.py` counts the last
column over all of `X(n)`, `n <= 30` (`66 658` domain states).

| # | configuration | verdict | how | count n<=30 |
|---|---|---|---|---|
| 1 | I(b) with `m2 = 0` | **impossible** | Lemma 2.2 (`N<m2=0` forces Case II) | 0 |
| 2 | I(b) with `m2` repeated | possible | `m2' = m2`, equality `N'=m2'` -> I(a) by decision 1 (4.2a) | — |
| 3 | I(a) with `m2 = 0` | possible | guard `N >= 0` is then vacuous; `N >= 2` always | — |
| 4 | I(a), `t0 = 0` | possible | `s5 = 0`, `k = s5 = 0`; only `N` is created | — |
| 5 | I(a) with a part equal to 5 | possible | `s5 > 0`; these are exactly the parts refilled by I(b) | — |
| 6 | II(a) with `m3 = 0` | **impossible** | `nu = 5j-3 >= m0 >= 0` forces `j >= 1`, Lemma 1.1 gives `j <= 0` | 0 |
| 7 | II(a) with `nu = 0` | possible | then `m0 = 0`; part deleted | 1 949 |
| 8 | II(a)/`nu=0` with `m3` **repeated** | possible | `m3' = m3`; **kills the cycle-1 bound** (6.2) | 980 |
| 9 | II(a)/`nu=0` with `m3` simple | possible | `m3' <= m3-5` or `m3' = 0` | 969 |
| 10 | II(a) with `m0 = 0` | possible | `m0' = nu` | — |
| 11 | II(b) with `m0 = 0` | possible | **Repair 1**: `t0' = t0 = 0`, `j <= -1` | 1 949 |
| 12 | II(b) with `m0` repeated | possible | `m0' = m0`; equality -> II(a) by decision 2 (4.4a) | — |
| 13 | II(b) with `m3 = 0` | possible | `mu >= 3 > m3`, so `m3' = mu`; 4.4 works verbatim | — |
| 14 | `lambda = ()` (`t = t0 = 0`, all `m_r = 0`) | possible | `j > 0` -> I(a); `j = 0` excluded; `j <= -1` -> II(b) | — |

**6.2 (sharp form of E2).** In II(a) with `nu = 0`: `m3' = m3` iff `m3` is
repeated; if `m3` is simple then `m3' = 0` or `m3' <= m3-5`. So the cycle-1
bound `m3' <= m3-5` fails in *two* ways — repeated `m3`, and `m3 = 3` simple
(where `m3' = 0 > 3-5`). Measured over `n <= 30`: it fails on 1 721 of the
1 949 states with II(a)/`nu=0`, of which 1 138 have `m3` repeated. The bound
`m3' <= m3` holds on all of them, which is all step 4.3 needs.

**6.3 (sharp form of E1).** In II(b), `t0' = t0-1` iff `m0 > 0`, and
`t0' = t0 = 0` iff `m0 = 0`. Measured over `n <= 30`: 0 violations.

## 7. What `psi_audit.py` checks (and what it does not)

`python3 psi_audit.py 30` re-implements `psi` from the brief (not from
`Computation/bz82.py`) and asserts, for every state of `X(n)`, `n <= 30`:

* Lemma 2.3 literally (the undefined set *is* `{0} x A(n)`, in both directions);
* Lemma 1.2 (weight) and positivity of every produced part;
* Lemma 3 for each branch, including every intermediate count and congruence
  (`t0'`, `m0'`, `m2'`, `m3'`, `N`, `nu`, `mu`, `k`, `s5`);
* 4.1-4.4 actively: `m3' <= m3`, `m3'+5j'-3 < m0'` (resp. `>= m0'`), the
  restoration `mu' = m0'` / `m3`, and `psi(psi(s)) = s`.

Total: 67 551 states, 66 658 in the domain, `I(a)=29 924`, `I(b)=29 924`,
`II(a)=3 405`, `II(b)=3 405`, **0 assertion failures**. This is a check of the
*proof steps*, not of the theorem alone; a wrong intermediate claim is reported
with its first witness rather than absorbed.

**Not** checked here (deliberately): the forcing of the three tie-breaks
(cycle-1 evidence, D-3a) and `phi` (below, and direction A).

## 8. Skeleton audit of `phi` (the other half of BZ82 p.314)

`phi` has **no** all-`n` proof in this repository: RR-C009 is TESTED_FINITE only.
What is proved here, and what is still missing, is the following. Notation:
`a = min{x >= 1 : 2j + x - lam(x) > 0}` (minimum over a non-empty set, see P1),
`mu = 2j + a - lam(a)`, `t* = t + [a>t] + [mu>t]`.

**P1 (existence of `a`), PROVED.** `x0 = max(t+1, 1-2j)` satisfies `x0 > t`
(so `lam(x0) = 0`) and `2j+x0 >= 1 > 0`; hence `a` exists and
`a <= max(t+1, 1-2j)`. Uniqueness is `min` of a set of positive integers.

**P2 (`mu >= 1`), PROVED.** `mu = 2j + a - lam(a) > 0` is exactly the
defining property of `a`; `mu` is an integer.

**P3 (`a = mu` never occurs in Case I), PROVED — this disposes of the
"removal multiplicities when `a = mu`" question.** `a = mu` iff `lam(a) = 2j`.
If `a <= t` then `lam(a) >= 1`, so `j >= 1`, and the Case I test reads
`2 lam(a) = 4j < 5j + t*` (as `t* >= 1`), so Case II. If `a > t` then
`lam(a) = 0`, so `j = 0` and `t* = t+2`, and the test reads `0 >= t+2`, false,
so Case II. Hence in Case I the two deleted slots are always *distinct*, the
slot count is `t*-2` and the printed count `lam(a)+lam(mu)-5j-t*` of inserted
1s is unambiguous. Verified: `a = mu` on 6 458 states of weight `<= 30`, all
Case II. (The committed `bz82.py` carries a tie-break for `a = mu`; P3 shows it
is unreachable in Case I.)

**P4 (weight), PROVED, both cases.** Case I: slot set = the `t` real slots plus
one virtual slot at each of `a`, `mu` that exceeds `t` (size `t*`); deleting
slots `a`,`mu` leaves `t*-2` slots, all real (`a`, `mu` are the only virtual
ones), so `|lambda'| = |lambda| - lam(a) - lam(mu) + (t*-2) +
(lam(a)+lam(mu)-5j-t*) = |lambda| - 5j - 2 = |lambda| - (P(j+1)-P(j))` by F2.
Case II: `|lambda'| = |lambda| - t + delta1 + delta2` where
`delta_k = part if positive else 0`, for the parts `m` and `t+5j-3-m`. If both
are positive the sum is `t+5j-3`; if exactly one is 0 the other is `t+5j-3`; if
both are 0 then `t = 3-5j` and `-t = 5j-3`. In every case
`|lambda'| = |lambda| + 5j-3 = |lambda| - (P(j-1)-P(j))` by F1. **Note the
reading needed:** a virtual zero *outside* `{a,mu}` is never incremented, which
is what makes Case I weight-preserving; the padded range `1..a+2j-1` appears in
Case II only.

**P5 (existence of `m` in Case II) — MONOTONICITY LEMMA, PROVED; the residual
inequality is NOT proved.** `i |-> lam(i) - i` is non-increasing on `i >= 1`
(`lam` is weakly decreasing, `-i` strictly), so
`lam(i) - i <= t+3j-a-1` is an **up-set** in `i`; substituting
`i = a+2j-1-z` (which maps `0 <= z <= a+2j-2` onto `1 <= i <= a+2j-1`)
the admissible `z`-set is a **down-set**, i.e. exactly `{0,1,...,m}`. Therefore

> **`m` exists `<=>` `a+2j-2 >= 0` and `z = 0` is admissible
> `<=>` `a+2j-2 >= 0` and `lam(a+2j-1) <= t+5j-2`,**

and whenever it exists it is the largest of an initial segment, so no "max of a
non-convex set" difficulty exists at all. Both properties hold on all 33 329
Case-II states of weight `<= 30` (`phi_skeleton.py`, assertion `P5`). The
remaining gap is exactly one inequality, stated above, for all `n`.

**P6 (Case I produces a partition), PROVED given P1-P3.** The guard
`lam(a)+lam(mu) >= 5j+t*` is exactly `r >= 0`, and every produced part is
either `>= 2` (an incremented real part) or `1`.

**P7 (case stability), measured not proved.** Over `n <= 30`, `phi` maps every
Case I state to a Case II state and conversely (33 329 each way). No written
argument for this is known to me.

**P8, P9.** `phi(phi(s)) = s` and the parity flip of `j` hold on all 66 658
domain states of weight `<= 30` under this transcription; this is finite
evidence only, and direction A owns the exhaustive census.

### Exact gap list for `phi`

1. **(G1)** The inequality `a+2j-2 >= 0` and `lam(a+2j-1) <= t+5j-2` on every
   Case-II state, all `n`. By P5 this is the *whole* of the `m`-existence
   problem. **OPEN here**; finite for `n <= 30`.
2. **(G2)** P7 (case stability) has no all-`n` argument. **OPEN.**
3. **(G3)** P8 (`phi^2 = id`) has no all-`n` argument: it needs the index
   bookkeeping of `phi`'s inverse pair, which is not written anywhere in this
   repository. **OPEN.**
4. **(G4)** The printed `t*` is exactly `t + [a>t] + [mu>t]` only under the
   reading of P4 (slot set = real slots + one virtual slot at each of `a`,`mu`
   that exceeds `t`). Under the alternative reading "pad `lambda` to length
   `t*` and increment every non-deleted slot", `phi` Case I does *not* preserve
   weight: `(-1;())` would go to `(0;(1,1,1,1))` of weight 4 instead of 3.
   The two readings differ whenever `a > t+1`; the committed `bz82.py` uses the
   P4 reading (phantom slots only at `a`, `mu`). **This is a specification
   ambiguity that must be stated wherever `t*` is quoted, not a defect.**

For `psi` the gap list is **empty**: 1-5 and 7 above close E1-E4 and every case
in §6, on the strength of Lemmas 1-3 and 4.1-4.4.

## 9. Anchoring: the transcription is the same map as the reference code

Both maps used here were written from the brief in `Main/CLAIMS.md`, not from
`Computation/bz82.py`. `crosscheck.py` then compares them with the committed
reference implementation state by state, including *which* states each refuses:

```
$ python3 crosscheck.py 26
n = 0..26, 26752 states of X(n), 26248 in the psi domain
psi: domain disagreements 0, value disagreements 0
phi: domain disagreements 0, value disagreements 0
VERDICT: identical maps on the tested range
```

So the distinction drawn in §7 between "the map" and "the proof of the map"
is real: the maps coincide, and what changed is the argument.

## 10. Commands and key output lines

```
$ cd RogersRamanujan/Counterexamples/cycle2
$ python3 psi_audit.py 30      # 5 s
0 failures: every step of the amended proof (a)-(d), every branch,
every virtual-zero case and every multiplicity case, holds on every state.
states in X(n):   67551
states in Dom(n): 66658   (F(n) = {0}xA(n): 893)
branch counts:    I(a)=29924 I(b)=29924 II(a)=3405 II(b)=3405
  II(a) selected with nu = 0, m3 repeated     : 980 states
  II(a) selected with nu = 0, m3 not repeated : 969 states
  II(b) selected with m0 = 0                  : 1949 states
  states where the committed bound m3' <= m3-5 is FALSE : 1721
     of which m3 is repeated                              : 1138

$ python3 phi_skeleton.py 30   # 6 s
domain states 66658, excluded {0}xB(n) 893
Case I 33329, Case II 33329
states with a = mu: 6458  (all Case II: True)
0 failures on every skeleton step P0-P9 over the whole range.

$ python3 crosscheck.py 26     # 2 s   -> identical maps on the tested range
```

Logs: `log_psi_30.txt`, `log_phi_30.txt`.
