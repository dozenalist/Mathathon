# Cycle 3, direction A': BZ82 `phi` — obligation (i),(ii),(iii) proved; (iv),(v) reduced

Author: worker m4 (swarm `smwg1kdjq`), cycle 3.  Deliverable of direction A'.
Proposed destination in the project tree:
`RogersRamanujan/Counterexamples/cycle3/PROOF_PHI_OBLIGATIONS.md` (Main to copy;
this worker does not write outside its own directory).

**Honest status.**

| obligation | status |
|---|---|
| (i) Case-II created parts `m >= 0` and `t+5j-3-m >= 0` | **PROVED** for all inputs (Lemmas 3, 4) |
| (ii) Case-I inserted count `N = L + lam(mu) - 5j - t* >= 0`, integral | **PROVED** for all inputs (Lemma 2; it is exactly Case I's defining inequality) |
| (iii) the deletions at `a` and `mu` are valid, incl. `a = mu` | **PROVED** for all inputs (Lemma 1 for `a != mu`; Lemma 0 for `mu >= 1` and the slot count `t*`) |
| (iv) case stability `I -> II` and `II -> I` | **NOT PROVED**; reduced to R1 (two explicit inequalities), 0 failures finitely |
| (v) both compositions are the identity | **NOT PROVED**; reduced to R2 (slot-level inverse recipe), 0 failures finitely |

Also **PROVED** here: weight preservation in both branches as an identity in the
parameters (Lemma 5), positivity/partition-hood of both outputs (Lemma 6).
No claim of an all-`n` involution proof is made anywhere below.

## 0. Setting and cited facts (not re-derived here)

`j in Z`, `lam` a descending tuple of positive integers of length `t` (possibly
`t = 0`), zero padding `lam(x) = lam_x` for `1 <= x <= t` and `0` for `x > t`.
`P(j) = j(5j-1)/2`; a signed state `(j;lam)` lies in `X(n)` iff
`|lam| + P(j) = n`.  BZ82 p.314 parameters:

    a   = min{ x >= 1 : 2j + x - lam(x) > 0 },   L = lam(a)
    k   = a + 2j - 1,      mu = k + 1 - L = a + 2j - L
    t*  = t + [a > t] + [mu > t],                R = t + 5j - 2
    Case I  iff  L + lam(mu) >= 5j + t*
    Case II otherwise:  m = max{ z in Z : 0 <= z <= k-1, z + lam(k-z) <= R }

`phi`: Case I deletes the slots at `a` and `mu`, adds 1 to every remaining slot,
inserts `N = L + lam(mu) - 5j - t*` parts equal to 1, and sends `j -> j+1`;
Case II subtracts 1 from each of the `t` parts, creates parts `m` and
`t+5j-3-m` (discarding zeros), and sends `j -> j-1`.  Domain:
`X(n) \ ({0} x B(n))` where `B(n)` = partitions of length `k` with smallest
part `>= k`.

Cited without re-derivation (Main's proved results, per the cycle-3 brief):

* **E1** (Case-II maximum existence).  Inside Case II the admissible set `S` is
  nonempty **iff** `k >= 1` and `lam(k) <= R`; it is empty exactly on
  `{0} x B(n)`; `z + lam(k-z)` is nondecreasing in `z`, so `S` is an initial
  segment and `m = max S` is uniquely determined.
* **E2** (the supervisor's cases 3 and 4 do not occur in Case II): `a > t+1`
  never occurs, and `a = t+1` with `j < 0` never occurs.  Consequently every
  in-domain Case-II state has **either `a <= t`, or `a = t+1` with `j >= 1`**
  (the remaining sub-case `a = t+1, j = 0` is `{0} x B(n)`, i.e. outside the
  domain).
* **E3** `psi` is an involution on `X(n) \ ({0} x A(n))` for all `n`
  (`Counterexamples/cycle2/AMENDED_PROOF.md`) — not used below.
* The two-slot rule of Case I: **collect both slots before removing either.**

## 1. Lemma 0 (parameters). *Proved.*

*(a)* The set defining `a` is nonempty: for `x > t` we have `lam(x) = 0`, so
`2j + x - lam(x) = 2j + x > 0` once `x > -2j`.  Hence `a` exists, `a >= 1`.

*(b)* `mu >= 1`: `mu = 2j + a - L` and `2j + a - L > 0` is exactly the defining
property of `a`; as an integer `mu >= 1`.  Equivalently `L <= k`.

*(c)* The padded list of Case I has exactly `t*` slots: the `t` real slots
`1..t` together with one virtual slot of value `0` at `a` if `a > t`, and one at
`mu` if `mu > t`.  In particular `a` and `mu` are positions **of that list** by
construction, and `t* = t + #{x in {a,mu} : x > t}`. ∎

Note `L = 0` happens only when `a > t`; virtual slots are the only slots that
can hold the value `0`.

## 2. Lemma 1 (`a != mu` in Case I). *Proved — the obligation of (iii).*

Assume the state is in the domain and in Case I.

*Step 1: `a > t` forces `j = 0`.*  If `a > t` then `L = lam(a) = 0`, hence
`mu = k + 1 - L = a + 2j`, and `a = mu` would give `2j = 0`, i.e. `j = 0`.
Suppose for contradiction `j = 0` and `a > t`.  By minimality of `a`,
`2j + x - lam(x) = x - lam(x) <= 0` for all `1 <= x <= t`, i.e. `lam_x >= x`;
in particular `lam_t >= t`.  Since `lam` is descending, every part of `lam` is
`>= t = length(lam)`, so `lam in B` and `(0;lam) in {0} x B(n)`, which is
outside the domain.  Contradiction.  Hence on the domain the conjunction
`a = mu` and `a > t` is impossible, so `a = mu` forces `a <= t`.

*Step 2: `a <= t` contradicts Case I.*  With `a <= t` we have `L = lam(a) >= 1`
and `t* >= t >= a >= 1`.  From `a = mu = a + 2j - L` we get `L = 2j`, so
`2j >= 1` and `j >= 1`.  Also `mu = a`, so `lam(mu) = lam(a) = L = 2j`.  Case I
then reads

    4j = L + lam(mu) >= 5j + t*  =>  t* <= -j <= -1,

contradicting `t* >= 1`.  ∎

**Consequence for the code.**  `Computation/bz82.py`, Case I, contains the
fallback `if drop: ...` which removes a second copy of the value at `a` when
`a = mu`.  Lemma 1 proves that branch is **unreachable** on the domain, so it can
be replaced by an assertion (proposed change to Main; this worker does not edit
outside its own directory).  The fallback is also the only place in `phi` where a
"second-removal" convention could silently change the map, so removing it removes
that risk.

## 3. Lemma 2 (inserted count). *Proved — obligation (ii).*

`t*`, `j` are integers and `L, lam(mu)` are integers, so
`N = L + lam(mu) - 5j - t*` is an integer.  Case I is *defined* by
`L + lam(mu) >= 5j + t*`, which is exactly `N >= 0`.  So nonnegativity needs no
estimate: it is the branch condition, and Case II is its strict complement.  In
particular `N = 0` occurs (26 417 of the 270 557 Case-I states of weight
`<= 40`); Case I inserts no ones at all in those states, so "insert N ones" must
be read as an insertion of a possibly empty multiset. ∎

## 4. Lemma 3 (`m` is a legitimate part). *Proved — first half of (i).*

Assume Case II and (by **E1**) `S != {}`.  Then `S` is a nonempty finite subset
of the integer interval `[0, k-1]`, so `m = max S` exists and
`0 <= m <= k-1`.  In particular the first created part `m` is a nonnegative
integer, and it is `0` only when `0 in S` and `1, ..., k-1` all fail. ∎

## 5. Lemma 4 (second created part). *Proved — second half of (i).*

**Statement.**  For every state in the domain in Case II,
`p2 := t + 5j - 3 - m >= 0`.

*Proof.*  Since `m in S`, `m + lam(k-m) <= R` with `lam(k-m) >= 0`, hence

    (1)   m <= R = t + 5j - 2,

i.e. `p2 >= -1`.  So it suffices to exclude `m = R`.

**Assume `m = R`** and derive a contradiction.

From `m <= k-1` (`Lemma 3`) and `m = R`:

    (2)   t + 5j - 2 <= a + 2j - 2,   i.e.   a >= t + 3j.

From `m = R in S`:

    (3)   R + lam(k-R) <= R,  hence  lam(k-R) = 0,

and by (2) the index `x0 := k - R = a + 2j - 1 - (t + 5j - 2) = a - 3j - t + 1`
satisfies `x0 >= (t+3j) - 3j - t + 1 = 1`.  Combining `x0 >= 1` with (3):

    (4)   lam(x0) = 0 and x0 > t.

Now split by **E2**, which leaves exactly two possibilities.

*Case B: `a = t+1` and `j >= 1`.*  By (2), `t + 1 = a >= t + 3j >= t + 3`, a
contradiction.  So `m = R` cannot occur here.

*Case A: `a <= t`.*  Then `L = lam(a) >= 1`.
By **E1** and `S != {}` we have `lam(k) <= R`; as `lam(k) >= 0` this gives
`R >= 0`, i.e.

    (5)   t >= 2 - 5j.

  *Sub-case `j >= 1`.*  (2) gives `a >= t + 3j > t`, contradicting `a <= t`.
  *Sub-case `j = 0`.*  (2) gives `a >= t`, so with `a <= t`: `a = t`.  Then
  `x0 = a - 3j - t + 1 = 1`, and (4) demands `x0 > t`, i.e. `t = 0`; but
  `a <= t` with `a >= 1` gives `t >= 1`.  Contradiction.
  *Sub-case `j <= -1`.*  By (5), `t >= 2 - 5j > -2j` (since `j <= 0`), so
  `x0 > t > -2j`.  By minimality of `a`, every `1 <= x < a` satisfies
  `2j + x - lam(x) <= 0`, i.e. `lam(x) >= x + 2j`.  If `x0 < a` this gives
  `lam(x0) >= x0 + 2j > 0`, contradicting (4).  Hence `x0 >= a`, i.e.
  `a - 3j - t + 1 >= a`, so `t <= 1 - 3j`.  With (5),
  `2 - 5j <= t <= 1 - 3j`, i.e. `1 <= 2j`, contradicting `j <= -1`.

All cases contradict, so `m < R`, i.e. `m <= R - 1 = t + 5j - 3` and
`p2 >= 0`. ∎

**Sharpness.**  `p2 = 0` is attained, so the lemma is sharp and the "discard a
created part that is 0" convention is needed.  The complete list of Case-II
states of weight `<= 30` with `p2 = 0` is

    (0; (1,1,1))   -> m = 0, p2 = 0, image (-1; ())
    (-1; (1^8))    -> m = 0, p2 = 0, image (-2; ())
    (-2; (1^13))   -> m = 0, p2 = 0, image (-3; ())

so at `(0;(1,1,1))` **both** created parts vanish and `phi` maps to the empty
partition.  The minimal witness is `(0;(1,1,1))`, weight 3.  `m = R` (i.e.
`p2 = -1`) never occurs: 0 of the 270 557 Case-II states of weight `<= 40`, and 0
of 116 081 random Case-II states of weight up to 9624.

## 6. Lemma 5 (weight is preserved as an identity). *Proved.*

*(a)* `P(j+1) = P(j) + 5j + 2` and `P(j-1) = P(j) - (5j - 3)` (both are one-line
expansions of `P(j) = j(5j-1)/2`).

*(b) Case I.*  The `t*` slots lose the two deleted values `L` and `lam(mu)`, the
other `t* - 2` slots gain 1 each, and `N` ones are added:

    |lam'| = |lam| - L - lam(mu) + (t* - 2) + N
           = |lam| - L - lam(mu) + (t* - 2) + (L + lam(mu) - 5j - t*)
           = |lam| - 5j - 2 = |lam| - (P(j+1) - P(j)),

so `|lam'| + P(j+1) = |lam| + P(j) = n`.  The length is `t* - 2 + N`.

*(c) Case II.*  The `t` parts each lose 1 (a part equal to 1 disappears), and the
two created parts are `m`, `p2` with `m + p2 = t + 5j - 3`:

    |lam'| = |lam| - t + m + p2 = |lam| + 5j - 3 = |lam| + (P(j) - P(j-1)),

so `|lam'| + P(j-1) = n`.  The length is `#{i : lam_i >= 2} + [m>0] + [p2>0]`. ∎

Both branches flip the parity of `j`, hence swap `X^e(n)` and `X^o(n)`.

## 7. Lemma 6 (both outputs are partitions; output lengths). *Proved.*

The `i`-th slot keeps a value `>= 0` (real slots are `>= 1`, virtual slots are
`0`), so after `+1` every kept slot is `>= 1`; Case-II survivors `lam_i - 1` are
`>= 0` and the non-positive ones are discarded, while `m >= 0`, `p2 >= 0` by
Lemmas 3 and 4.  Sorting the resulting multiset yields a descending positive
tuple, i.e. a partition.  No monotonicity needs to be tracked through the
deletion, because a partition here *is* a descending tuple, i.e. a sorted
multiset. ∎

Note: the only case where `phi`'s **domain** condition can bite on the output is
`j' = 0`, i.e. `j = -1` (Case I) or `j = 1` (Case II); this is the part of R1(a)
below.

## 8. Obligations (iv) and (v): reduced, not proved

### R1 (case stability).  Not proved here.

*R1(a)* `phi` maps the domain `X(n) \ ({0} x B(n))` into itself.
*R1(b)* the Case-I image satisfies Case II's inequality
`L' + lam'(mu') < 5j' + t*'` (primes = parameters recomputed from the image),
and the Case-II image satisfies Case I's inequality
`L' + lam'(mu') >= 5j' + t*'`.

Why this is harder than `psi`'s case stability: the census of Case-I states by
`(a vs t) x sign(j)` at weight `<= 30` is

    (a<=t, j<=-1) 12167   (a<=t, j==0) 15051   (a<=t, j>=1) 3506
    (a=t+1, j<=-1) 2234   (a>t+1, j<=-1)  371

(all three `j >= 0` cells with `a >= t+1` are empty; that is a short corollary of
the Case-I inequality: if `a > t` then `L = 0` and `mu = a + 2j > t` whenever
`j >= 0`, so `lam(mu) = 0` and Case I reads `0 >= 5j + t*`, which is impossible
since `t >= 1` gives `t* >= 1` and `t = 0` gives `t* = 2`).  So the
Case-I side needs **three** sub-cases, one of which (`a > t+1`, only 371 states
at weight `<= 30`) has no counterpart in the established Case-II analysis and is
where a proof of R1(b) has to do new work.  R1(a) is a two-case statement
(`j = +-1`).

### R2 (the inverse branches, derived from the inequality).  Not proved here.

Reversing the rules by *inequality* rather than by formula gives the following,
which is what (v) has to verify.  Let `s = (j;lam)` be in the domain with
parameters `(a,L,k,mu,t*,R)`.

*If `s` is in Case II*, with `m = max S`, `p2 = t+5j-3-m`, the image is
`s' = (j-1; lam')`, `lam'` = sorted `({lam_i - 1 : lam_i >= 2} u ({m,p2} - {0}))`.
The inverse operation is Case I applied to `s'` with parameters recomputed from
`lam'`, and the content of (v) is the **three slot identities**

    (R2.1)  { pad(lam', a'), pad(lam', mu') } = { m, p2 }   (as multisets),
    (R2.2)  N' := L' + lam'(mu') - 5j' - t*' = #{ i : lam_i = 1 },
    (R2.3)  { pad(lam', x) - 1 : x a surviving slot } = { lam_i - 1 : lam_i >= 2 }.

(R2.1) is the substantive one: it says that the two slots Case I deletes from the
image are exactly the two parts Case II created, and — because a created part may
be `0` — that a created `0` is represented by a **virtual slot**, cf. the witness
`(0;(1,1,1)) -> (-1;())` where both created values vanish and Case I on `(-1;())`
deletes the two virtual slots at `a' = 1, mu' = 2`.
*If `s` is in Case I*, the dual identities hold: with image
`s' = (j+1; lam')` (length `t* - 2 + N`),

    (R2.1') { m', p2' } = { L, lam(mu) }  (as multisets),
    (R2.2') #{ x in lam' : x = 1 } = N,
    (R2.3') { lam'_i - 1 : lam'_i >= 2 } = the surviving slot values of `s`.

**Sharpening found by the audit (a strictly stronger, and better, proof target;
evidence only).**  The slot identity is not merely a multiset identity and needs
no swap: positionally,

    (R2.1'')  Case II -> I:  lam'(a') = m   and  lam'(mu') = p2,
              Case I  -> II: m' = L         and  p2' = lam(mu)

with 0 exceptions over the 541 114 in-domain states of weight `<= 40` and the
296 795 random in-domain states (assertions `P10'`/`P11'` in the auditor).  This
is the statement a proof of (v) should aim at: it names *which* of the two
positions `a'`, `mu'` carries which created part.  It also shows that a created
part equal to `0` is carried by a virtual slot at exactly that position, cf.
`(0;(1,1,1)) -> (-1;())`.

**Finite certification of R1 and R2** (evidence, *not* proof): all of
P8 (R1(b)), P9 (`phi(phi(s)) = s`), P10/P11/P10'/P11' (R2.1-3, checked slot by slot rather
than only net) hold with **0 failures** over

* all 66 658 in-domain states of weight `<= 30` (P0-P9, plus P10/P11;
  `out_weight30.txt`),
* all 541 114 in-domain states of weight `<= 40` (same checks;
  `out_weight40.txt`),
* 296 795 random in-domain states (weights up to 9624, `|j|` up to 60),
  `stress.py`.

The counts `Case I = Case II = 33 329` (resp. `270 557`) are consistent with
`phi` being an involution, but by themselves prove nothing.

## 9. Exact commands and key output lines

    $ python3 cycle3/phi_obligations.py 30 --compare     # 1.6 s
    P0-P11 ALL PASS over every in-domain state of weight <= 30
    signed states total      : 67551
    excluded (0 x B(n))      : 893
    in-domain                : 66658
      Case I                 : 33329  -> Case II outputs: 33329
      Case II                : 33329  -> Case I outputs: 33329
    a == mu occurrences (P2): 0
    m == R occurrences       : 0
    disagreements with bz82  : 0

    $ python3 cycle3/phi_obligations.py 40 --compare     # 32 s
    in-domain                : 541114
      Case I                 : 270557  -> Case II outputs: 270557
      Case II                : 270557  -> Case I outputs: 270557
    a == mu occurrences (P2): 0
    m == R occurrences       : 0
    disagreements with bz82  : 0

    $ python3 cycle3/stress.py                            # 15 s
    stress: trials 300000, in-domain 296795 (Case I 180714, Case II 116081), max weight 9624
    stress: P0-P11 ALL PASS (0 failures)

The auditor is an **independent** implementation of the printed recipe (written
from the task statement, not from `bz82.py`); `--compare` additionally requires
object-for-object agreement with the committed `Computation/bz82.py`, which is
what the `disagreements: 0` lines report (transcription fidelity, not proof).

## 10. What is still missing, precisely

1. **R1(b)** for the three Case-I sub-cases, and **R1(a)** for `j = +-1`.
2. **R2.1-R2.3** (and duals): these are the identities that make (v) more than
   "the net effect is the identity".  `R2.1` is where the `a = mu` question could
   in principle resurface: it asserts that the two deleted positions of the image
   are *distinct* — for the image, Lemma 1 supplies that, since the image is in
   Case I.
3. Nothing here proves `phi^2 = id` for all `n`, and no step above assumes it.

## 11. Files

* `phi_obligations.py` — independent `phi` + auditor (assertions P0-P11), CLI
  `python3 phi_obligations.py <maxweight> [--compare]`, JSON on the last line.
* `out_weight30.txt`, `out_weight40.txt` — captured output.
* `probe_slots.py` — positional slot identity of section 8 (R2.1'').
* `stress.py` — randomised stress test.
* `probe.py` — witnesses and the sub-case census of section 8.
