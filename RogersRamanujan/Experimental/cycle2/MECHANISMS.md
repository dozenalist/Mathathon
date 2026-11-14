# Two explicit mechanisms, frozen conjectures, and what failed

Direction C (experimental), RR127 cycle 2.  The objective (a more natural
weight-preserving bijection `A_n -> D_n` with an independently specified
inverse) is **not** met here.  What is delivered: two fully specified mechanisms
with their exact admissible sets and their single blocking lemma, a proved
closed form for one infinite family (`PROOF_families.md`, Theorem F), and
frozen conjectures that were tested on held-out parameters and **failed**, with
the failures listed.

Nothing below edits any other folder.  The baseline `Computation/bz82.py` is
imported read-only; its rules are not changed or re-derived here.

---

## M1 --- collapse-and-singleton

**Forward rule.**  Domain `F1 = {(1^s) : s >= 0}` (one A-object per weight).
Given `(1^s)`, set `p = s - 3`, `r = p mod 5`, and read off `lam in D_s`:

| case | `lam(s)` |
|---|---|
| `s = 0` | `()` |
| `s = 1` | `(1)` |
| `s = 2` | `(2)` |
| `s = 4` | `(3,1)` |
| `s = 6` | `(4,2)` |
| `s = 3 mod 5`, `s >= 3` | `(s)` |
| `s = 2 mod 5`, `s >= 7` | `(s-2, 2)` |
| `s = 4 mod 5`, `s >= 9` | `(s-2, 2)` |
| `s = 1 mod 5`, `s >= 11` | `(s-4, 4)` |
| `s = 0 mod 5`, `5 <= s <= 25` | `(6 + s/5 - 2i)` for `i = 1..s/5` |

Every entry is *derived* from the printed `phi`/`psi` rules (one `phi` step,
then one `psi` step, or the six-step chain), not fitted; the derivation is
`PROOF_families.md` Lemmas 0-2 and Theorem F.

**Separately recoverable inverse.**  From `lam in D_n` alone: put `s = |lam|`
(the weight recovers the parameter, so no search is needed), compute the table
entry for `s`, and compare.  Equal -> return `(1^s)`; unequal -> "not in the
family".  No trace, no auxiliary `j`, no table over `A_n`.

**Admissible parameter set.**  `s = 0,1,2`; all `s >= 3` with `s != 0 mod 5`;
and `s in {5,10,15,20,25}`.  Excluded: `s = 0 mod 5` with `s >= 30`.
Boundary is *proved*, not empirical: Lemma 1(c) produces `b = (5^{s/5})`, and
`(5^k)` has `k` parts all equal to `5`, so it lies in `B(s)` iff `k <= 5`
iff `s <= 25`.  For `s >= 30` the rule's own output is not a legal `B`-state,
so the mechanism provably cannot close the family there.

**Invariant.**  Weight (`|lam(s)| = s`), and the `B`-side length is a function
of `s` alone (for `s >= 3`): `len = 1` for `s = 3 mod 5`; `len = 2` for
`s = 1,2,4 mod 5`; `len = s/5` for `s = 0 mod 5`, `s <= 25`.

**Termination measure.**  Explicit step count: `0` for `s in {0,1}`, `2` for
`s = 2` and for `s = 2,3,4 mod 5`, `2` for `s = 0 mod 5` with `s <= 25`, `6` for
`s = 1 mod 5` (`s >= 11`), `6` for `s = 4`.  **Bounded by 6 for every `s` in the
admissible set, with no growing range.**  This is the one place where the
mechanism is genuinely better than BZ82.

**The single lemma I cannot prove.**
> **L-M1.**  There is a closed-form description of `b(5k)`, the `B`-endpoint of
> `(0;(1^{5k}))`, valid for every `k >= 6`.

I cannot even state a candidate: see conjecture C2 below, refuted.  What I *can*
prove is that the natural continuation fails, and why (the `B`-membership
`5 >= k`).  So L-M1 is open, and it is the only gap in M1.

**Does M1 reach the objective?**  No.  It is a *partial* map: one A-object per
weight.  It saves the alternating path on that subfamily and nothing else.  It
is not a candidate for the objective; it is a proved structural fact about
BZ82 (its path on the all-ones ray has constant length in four of five residue
classes) that any later naturalness comparison can use.

## M2 --- free window (zero-orbit)

**Forward rule.**  `alpha in A_n` with `min(alpha) >= len(alpha)` (equivalently
`alpha in B_n`) is sent to `Tinv(alpha)`.  This is exactly what BZ82's iteration
does at step 0: such an object needs no `phi`, no `psi`, no signed state.

**Separately recoverable inverse.**  From `lam in D_n`: compute
`b = T(lam)`, i.e. `b_i = lam_i - k + 2i - 1`; return `b` iff `b in A_n`,
otherwise "not in the window".  Both directions are pure arithmetic on the
partition.

**Admissible parameter set.**  `A_n cap B_n`; membership test `min >= len`,
explicit for every `n`.  It is **empty for `n in {2,3,5,7}`** and nonempty for
every other `n <= 40` (`DATA.md` F4); e.g. `()` at `n = 0`, `(4^r)` at `n = 4r`
with `r <= 4`, `(1)` at `n = 1`, `(8)` at `n = 8`.  So the mechanism is a
*partial* map, as its name says.

**Invariant.**  Weight only.  No auxiliary invariant is needed, which is the
point of the window.

**Termination measure.**  `0` alternating steps.

**The single lemma I cannot prove.**
> **L-M2.**  There is a rule on the complement `A_n \ B_n` with the same
> character --- deterministic, defined by a formula on `alpha` alone, inverse a
> formula on `lam` alone, no signed state and no auxiliary data --- which is a
> bijection onto `D_n \ Tinv(A_n cap B_n)`.

I cannot prove existence, and I have no candidate.  I can quantify why the
window cannot be enough: over `0 <= n <= 40` the window has **255** elements
against **3251** in the union of the `A_n` (`DATA.md` F4), a fraction `0.078`.
So any mechanism of this shape leaves ~92% of the objects to a rule that is not
of this shape.

**Does M2 reach the objective?**  No, for the reason just stated.

---

## Frozen conjectures, and their failures

Protocol used: state the conjecture, fix the parameter range on which it is
*derived* (never fitted), then run it on strictly larger parameters and report
every mismatch.  Script: `family_rules.py`.

**C1 (proved on `k <= 5`, tested on `k = 6..12`).**  `b(5k) = (5^k)` for all
`k >= 1`.  *Failed: 7 of 7 held-out values.*
```
k= 6  pred (5,5,5,5,5,5)           got (14,11,5)
k= 7  pred (5,5,5,5,5,5,5)         got (15,9,6,5)
k= 8  pred (5^8)                   got (25,12,3)
k= 9  pred (5^9)                   got (12,10,9,7,7)
k=10  pred (5^10)                  got (35,11,4)
k=11  pred (5^11)                  got (16,12,11,8,8)
k=12  pred (5^12)                  got (23,17,9,6,5)
```
The failure is *explained*, not mysterious: `(5^k) !in B(5k)` for `k >= 6`.

**C2 (refuted outright).**  `b(5k)` is coordinatewise affine in `k`, with the
length eventually constant --- the only shape that would make L-M1 provable by
linear algebra.  Lengths for `k = 1..12`: `1,2,3,4,5,3,4,3,5,3,5,5`, not
eventually constant.  First coordinates: `5,5,5,5,5,14,15,25,12,35,16,23`;
successive differences `0,0,0,0,9,1,10,-13,23,-19,7`, not monotone.  Refuted.

**C3 (observed at `r = 5,6`, tested on `r = 7..20`).**  `b(r)` for the
all-fours ray has at most two parts.  *Failed at `r = 7`*: `b(7) = (14,11,3)`
(and `r <= 4` is no evidence, since there `b(r) = (4^r)` has `r` parts).  Later
values include `(17,14,8,7,7,7)` at `r = 15` (six parts).  Refuted.

**C4 (refuted).**  The `B`-side length `kappa(s)` of the all-ones ray depends
only on `s mod 5`.  For `s = 0 mod 5` it equals `s/5` for `s <= 25` but `3,4,3,
5,3,5,5` for `s = 30,35,40,45,50,55,60`; so it is neither `s/5` nor a function
of the residue class alone.  Refuted.

## The two-parameter family `(4^r,1^s)` --- no compression found

Raw B-endpoints for `0 <= r <= 8`, `0 <= s <= 12` are tabulated in `DATA.md` F3
(117 parameter pairs, more than the 12 required).  Observations, all exact:

* Endpoint length (the "level") takes every value in `1..6` and is not monotone
  in either parameter: `len(b(1,s)) = 2,2,2,2,3,3,2,3,3,2,3,2` for `s = 1..12`.
* Path length is not monotone either: `(4^4,1^1)` takes 2 steps to `(17)` while
  `(4^4,1^2)` takes 52 to `(14,3,1)`; `(4^7,1^2)` takes 646 steps to
  `(11,9,6,4)`.
* No row or column is eventually an arithmetic progression, and no two rows are
  related by a shift of `s`.  I could not extract a rule, so I state no
  conjecture for this family.  Reported as a failure, not smoothed over.

## Which of these checks are genuinely independent

* The Lemma proofs are case analyses on the printed rules; `lemma_checks.py`
  instantiates them.  That is a transcription check, not a proof.
* `family_rules.py` compares the derived table against the **committed**
  `Computation/bz82.py`, so a slip in either transcription appears as a
  mismatch.  This is the strongest cross-check in the folder.
* `Tinv` is recomputed from its closed formula in `family_rules.py` and
  `make_data.py` rather than imported from `rr_core`, so the D-side column is a
  second route.
* Nothing here uses `|A_n| = |D_n|`; no claim rests on the counting identity.
