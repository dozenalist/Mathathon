# RR127 — direction D3: the Bressoud–Zeilberger (1982) involution ψ

Member m3, swarm smwfxwsqf.  Everything below is exact integer arithmetic,
`python3` standard library only, no network, no git.

Files

| file | contents |
|---|---|
| `bz.py` | the map ψ (all four branches), the state enumeration, two independent counting routines for `A_n` and `D_n` |
| `run_tests.py` | test driver; `python3 run_tests.py 15` (contract range) or `python3 run_tests.py 30` |
| `results_n15.txt` | full output for n = 0..15 |
| `results_n30.txt` | full output for n = 0..30 (extension) |

---

## 1. The object

```
X(n)  = { (j; λ) : j ∈ Z, λ a partition (descending tuple of positive ints),
                  |λ| + j(5j−1)/2 = n }
ψ     : X(n) \ F(n) → X(n) \ F(n),     F(n) = { (0; λ) : λ ∈ A_n }
```
`j(5j−1)/2` = 0,2,3,9,11,21,24,… for j = 0,1,−1,2,−2,3,−3 (the 5-pentagonal
numbers).  `A_n` = partitions of n with all parts ≡ 1 or 4 (mod 5), as in the
contract.  Partitions are written as descending tuples, `()` is the partition
of 0; multiplicities are kept.  `t_0` = number of parts ≡ 0 (mod 5),
`m_r` = largest part ≡ r (mod 5) (`0` when there is none), r = 0,2,3.
Put `N := 5t_0 + 5j − 3` (so `N ≡ 2 (mod 5)`), the part that Case I inserts.

The four branches are exactly the ones quoted in the task contract.  Nothing
else was changed.

## 2. Tie-break decisions (documented; each is *forced*, see §5)

| # | ambiguity | decision |
|---|---|---|
| 1 | Case I with `N = m_2` | **I(a)** — the guard is `N ≥ m_2`, equality goes to I(a) |
| 2 | Case II with `m_3 + 5j − 3 = m_0` | **II(a)** — guard `m_3 + 5j − 3 ≥ m_0`, equality goes to II(a) |
| 3 | `m_3 + 5j − 3 = 0` | **the part disappears**: II(a) removes `m_3` instead of writing a part 0. (Necessarily `m_0 = 0` here, since the II(a) guard gives `0 ≥ m_0`.) |

Note that decision 3 is not independent of decision 2: if `m_3+5j−3 = 0` then
`m_0 = 0`, so the "= 0" case is exactly the equality case with `m_0 = 0`.

Working with these three decisions, **ψ is a genuine involution on its domain
for every n, with no exception** — proved in §3, verified exhaustively for
n ≤ 30 in §4.

## 3. Proof that ψ is an involution on `X(n) \ F(n)` (all n)

Write `P(j) = j(5j−1)/2`.  Two arithmetic facts used throughout:

    P(j−1) = P(j) − (5j−3),        P(j+1) = P(j) + (5j+2).

**(a) Weight.**  Each branch changes `|λ|` by the negative of the change of `P`:

| branch | change of λ | change of `|λ|` | change of `P(j)` |
|---|---|---|---|
| I(a) | −5 from each of the `t_0` parts ≡0, insert `N` | `−5t_0 + N = 5j−3` | `−(5j−3)` |
| I(b) | delete `m_2`, +5 to each of the `t_0` parts ≡0, add `k=(m_2−5j−2−5t_0)/5` copies of 5 | `−m_2+5t_0+5k = −5j−2` | `+(5j+2)` |
| II(a) | replace `m_3` by `m_3+5j−3` | `5j−3` | `−(5j−3)` |
| II(b) | replace `m_0` by `m_0−5j−2` | `−5j−2` | `+(5j+2)` |

So `|λ| + P(j) = n` is preserved in every branch.  Positivity of the new parts:
in I(a), either `t_0+j ≥ 1` gives `N ≥ 2`, or `m_2 > 0` with `N ≥ m_2 ≥ 2`;
in I(b), `k ≥ 0` because `N < m_2` gives `5k = m_2−5j−2−5t_0 > −5`; in II(a),
`ν := m_3+5j−3 ≥ m_0 ≥ 0`; in II(b), `ν = m_0−5j−2` and `j ≤ −t_0 ≤ 0`, so
`ν ≥ 3` whenever `m_0 > 0` (then `m_0 ≥ 5`), and `ν = −5j−2 ≥ 3` when
`m_0 = 0, j ≤ −1`.  Also `N ≡ 2`, `ν_{II(a)} ≡ 0`, `ν_{II(b)} ≡ 3 (mod 5)`.

**(b) The only undefined case.**  By the above, the rules return a non-partition
only when II(b) is selected with `m_0 = 0` and `j = 0`, giving the part `−2`.
Since Case II forces `j ≤ −t_0 ≤ 0`, this means `j = 0, t_0 = 0` (⟺ `m_0 = 0`)
and `m_2 = 0`, and II(b) (not II(a)) is selected, i.e. `m_3 − 3 < 0`, i.e.
`m_3 = 0`.  So the rules are undefined exactly on
`{(0; λ) : λ has no part ≡ 0,2,3 (mod 5)} = {(0; λ) : λ ∈ A_n} = F(n)`. ✔

**(c) Case stability.**  For `s ∈ Dom(n)`, ψ(s) lies in the same top-level case:

* I(a): the new part `N ≡ 2 (mod 5)` is present, so `m_2' ≥ N > 0` ⟹ Case I.
* I(b): `5(t_0' + j') = 5t_0 + (m_2−5j−2−5t_0) + 5(j+1) = m_2 + 3 > 0`
  (as `m_2 ≡ 2`, `m_2 ≥ 2`) ⟹ Case I.
* II(a): `j' = j−1`, `t_0' ∈ {t_0, t_0+1}` (the value `m_3+5j−3` is ≡0 mod 5 when
  positive), so `t_0'+j' ≤ t_0+j ≤ 0`, and `m_2' = m_2 = 0` ⟹ Case II.
* II(b): `t_0' = t_0−1`, `j' = j+1` ⟹ `t_0'+j' = t_0+j ≤ 0`; the new part is
  ≡3 mod 5 so `m_2' = 0` ⟹ Case II.

**(d) Branch pairs are mutually inverse.**  Let `s=(j;λ)`, and in I(a) let
`s = #{parts of λ equal to 5}`.

*I(a) → I(b).*  In ψ(s) the parts ≡0 mod 5 number `t_0−s` and `m_2' = N`
(`N` is present and `N ≥ m_2`).  Hence `5t_0' + 5j' − 3 = 5t_0−5s+5(j−1)−3
= N −5s−5 < N = m_2'`, so I(b) is selected.  I(b) deletes the copy of `N`,
adds 5 to every part ≡0 (restoring the old ones) and creates
`(N − 5(j−1) − 2 − 5t_0')/5 = (5t_0 − 5t_0')/5 = s` copies of 5, and sets
`j'' = j`: that is λ again.

*I(b) → I(a).*  In ψ(s) we have `t_0' = t_0 + k`, so
`N' = 5t_0'+5(j+1)−3 = 5t_0+5k+5j+2 = m_2`, while `m_2' ≤ m_2` (the parts ≡2 of
ψ(s) are the parts ≡2 of λ, with one copy of `m_2` deleted).  Hence `N' ≥ m_2'`
— **this is where decision 1 is needed** (equality occurs exactly when `m_2` is
repeated) — I(a) is selected, and it reverses I(b) by the same computation.

*II(a) → II(b).*  Let `ν = m_3+5j−3`.
If `ν > 0`: `ν` is a part of ψ(s) with `ν ≡ 0 (mod 5)` and `ν ≥ m_0`, so
`m_0' = ν`; and `m_3' ` (largest part ≡3 of ψ(s)) is at most `m_3`, so
`m_3' + 5(j−1) − 3 ≤ m_3+5j−8 = ν−5 < ν = m_0'` ⟹ II(b) is selected, and it
replaces `m_0'=ν` by `ν − 5(j−1) − 2 = m_3`, restoring `m_3` and `j`.
If `ν = 0` (decision 3): the part `m_3 = 3−5j` was removed and `m_0' = m_0 = 0`
(note `m_2' = 0`); then `m_3'+5(j−1)−3 ≤ (m_3−5)+5j−8 = −13 < 0 = m_0'`
⟹ II(b) is selected and it *creates* the part `0 − 5(j−1) − 2 = 3−5j = m_3`,
again restoring `m_3` and `j`.

*II(b) → II(a).*  Put `ν = m_0−5j−2` (≡3 mod 5).  The II(b) guard
`m_3+5j−3 < m_0` gives `ν > m_3−5`, hence `ν ≥ m_3` because both are ≡3 (mod 5);
so the largest part ≡3 of ψ(s) is exactly `ν`.  Also `m_0' ≤ m_0` (the largest
remaining part ≡0).  Then `ν + 5(j+1) − 3 = m_0 ≥ m_0'` ⟹ II(a) is selected —
**this is where decision 2 is needed** (equality occurs exactly when `m_0` is
repeated) — and it replaces `ν` by `ν+5(j+1)−3 = m_0`, restoring `m_0` and `j`.

Combining (a)–(d): ψ is a well-defined map `Dom(n) → Dom(n)` and
`ψ∘ψ = id` on `Dom(n)`, for every n. ∎

Unrolling the proof: every `ψ`-orbit is a 2-element set whose two states carry
opposite signs `(−1)^j`, and the states left over are exactly `F(n) = {0}×A_n`.
Hence

    Σ_{(j;λ) ∈ X(n)} (−1)^j  =  |A_n|,     i.e.   Σ_{j∈Z} (−1)^j p(n − j(5j−1)/2) = |A_n|.

## 4. Results (verbatim numbers from `results_n15.txt` / `results_n30.txt`)

Answers to the three questions asked:

**(i) Is ψ an involution (ψψ = id) on its declared domain?**  **Yes.**
0 failures over **1371** states of `X(n)` and **1290** states of `Dom(n)` for
n = 0..15; and 0 failures over **67551** states / **66658** domain states for
n = 0..30.  Also verified on that domain: weight preserved, sign reversed,
no fixed point, output always a partition with positive parts.

```
states tested (all of X(n), n=0..15): 1371
states tested in Dom(n):               1290
fixed set F(n) == {(0,lam): lam in A_n} for all n : YES
psi total on Dom (returns a partition with positive parts): YES
weight |lam| + j(5j-1)/2 preserved on all of Dom:            YES
sign (-1)^j reversed on all of Dom:                         YES
psi has no fixed point inside Dom:                          YES
psi(psi(s)) == s for every s in Dom (n=0..15):               YES (0 failures)
case stability  (Case I maps to Case I and Case II to Case II): YES
domain states per branch: I(a)=528 I(b)=528 II(a)=117 II(b)=117
domain states in Case I / Case II: 1056 / 234
```
(the n ≤ 30 run prints 29924 / 29924 / 3405 / 3405 and 59848 / 6810, again
`I(a)` and `I(b)` counts equal and `II(a)`, `II(b)` counts equal — which they
must be, since the branches are mutually inverse.)

Per-n (n = 0..15): `|X(n)|` = 1,1,3,5,8,12,19,27,40,57,80,111,153,206,278,370;
`|F(n)| = |A_n|` = 1,1,1,1,2,2,3,3,4,5,6,7,9,10,12,14;
`|Dom(n)|` = 0,0,2,4,6,10,16,24,36,52,74,104,144,196,266,356 — always even, and
`|Dom(n)|/2` 2-cycles.

**(ii) Does the orbit of every state reach `{j=0} × A_n`?**  **No, and it
cannot**: ψ is an involution, so every orbit is a 2-element set contained in
`Dom(n)`, and `F(n)` is never reached by an iterate (the column "reachable
F(n)" in `results_n15.txt` is 0 for every n).  The correct structural statement,
which is what makes the sign-reversing argument work, is the disjoint union

    X(n)  =  F(n)  ⊔  (2-element ψ-orbits),      F(n) = {0} × A_n,

verified literally for n ≤ 30 (counts: `|X(n)| = |F(n)| + 2·#orbits`, e.g.
n = 8: 40 = 4 + 2·18; n = 30: 13655 = 117 + 2·6769).  `n = 0` is the empty
domain case: `X(0) = {(0;())}` and `() ∈ A_0`, so `Dom(0) = ∅`.

**(iii) Is the map single-valued / consistent?**  **Yes.**  The guards are
functions of the state alone, so ψ is a function by construction; the
substantive requirement is case stability (§3(c)), verified for every domain
state: Case I → Case I, Case II → Case II, 0 exceptions.  Equality is taken by
I(a) and by II(a) consistently at every n.

### Tie-breaks are forced (variant test, n ≤ 15)

| decisions | involution failures (of 1290 domain states) | smallest witness |
|---|---|---|
| I(a), II(a), delete **(chosen)** | **0** | — |
| I(b), II(a), delete | 219 | n=4: `s=(0;2,2)`, `ψ(s)=(1;2)`, `ψ(ψ(s))` undefined (I(b) would need `k=−1` parts of 5) |
| I(a), II(b), delete | 100 | n=3: `s=(−1;())`, `ψ(s)=(0;3)`, `ψ(ψ(s))` undefined (needs the part `−2`) |
| I(a), II(a), part-0-kept | 100 | n=3: `s=(−1;())`, `ψ(s)=(0;3)`, `ψ(ψ(s))` undefined (same witness) |
| I(b), II(b), part-0-kept | 319 | n=3: `s=(−1;())`, ... |

(`results_n30.txt` gives the same picture with 0 / 11918 / 2487 / 2405 / 14405.)
The failure counts are additive (219+100 = 319), so the two equality decisions
break disjoint sets of orbits — each is independently forced.

### The arithmetic consequence (`results_n15.txt`, §(7); also n ≤ 30)

```
  n   |X(n)|   signed    |A_n|    |D_n|
  0        1        1        1        1
 ...
  8       40        4        4        4
 ...
 15      370       14       14       14
 30    13655      117      117      117
signed sum == |A_n| == |D_n| for all n=0..30 : True
```
`|A_n|` and `|D_n|` were computed twice each (unbounded coin change over
parts ≡1,4 mod 5 and the recurrence `f(n,k) = f(n,k−1) + f(n−k,k−2)` with
`f(0,k)=1`, `f(n,k)=0` for `n>0, k<1`; and again by brute-force generation of
all partitions, agreement asserted).  By §3 the equality `signed = |A_n|` is
not a coincidence: it is exactly the orbit decomposition.

Worked orbits (`results_n15.txt`, section "worked examples"), e.g.

```
n = 4   |X|=8  fixed F={(0; 1,1,1,1) (0; 4)}
     (-1; 1)        --II(b)--> (0; 3,1)     --II(a)--> (-1; 1)
     (0; 2,1,1)     --I(b)-->  (1; 1,1)     --I(a)-->  (0; 2,1,1)
     (0; 2,2)       --I(b)-->  (1; 2)       --I(a)-->  (0; 2,2)
n = 5   |X|=12 fixed F={(0; 1,1,1,1,1) (0; 4,1)}
     (-1; 2)        --I(b)-->  (0; 5)       --I(a)-->  (-1; 2)
     (0; 3,2)       --I(b)-->  (1; 3)       --I(a)-->  (0; 3,2)
```

## 5. What this map does and does not give for RR127

* It gives a **combinatorial proof of the product side**: `Σ_n |A_n| q^n`
  `= (Σ_j (−1)^j q^{j(5j−1)/2}) / (q;q)_∞ = Π_{k≥0} 1/((1−q^{5k+1})(1−q^{5k+4}))`
  (the last step is the Jacobi triple product, not checked here).
* It gives **no bijection `A_n → D_n`**.  The survivors of the involution are
  the states `(0; λ)` with `λ ∈ A_n`; nothing in the map refers to `D_n`.  The
  count identity `|A_n| = |D_n|` needs, in addition, the *sum* side
  `Σ_k q^{k²}/(q;q)_k` for `D`, i.e. the staircase + shift bijection of the
  contract plus a `q`-identity.  So the Bressoud–Zeilberger map is a reference
  point for RR1, **not** the sought explicit `A_n ↔ D_n` bijection.

## 6. Exact commands and key output lines

```
$ python3 run_tests.py 15            # contract range, 0.40 s
states tested (all of X(n), n=0..15): 1371
states tested in Dom(n):               1290
fixed set F(n) == {(0,lam): lam in A_n} for all n : YES
psi(psi(s)) == s for every s in Dom (n=0..15):               YES (0 failures)
case stability  (Case I maps to Case I and Case II to Case II): YES
signed sum == |A_n| == |D_n| for all n=0..15 : True
wall time: 0.40 s

$ python3 run_tests.py 30            # extension, ~23 s
states tested (all of X(n), n=0..30): 67551
states tested in Dom(n):               66658
psi(psi(s)) == s for every s in Dom (n=0..30):               YES (0 failures)
domain states per branch: I(a)=29924 I(b)=29924 II(a)=3405 II(b)=3405
signed sum == |A_n| == |D_n| for all n=0..30 : True
```

No failure was found, so there is no failure witness to report.  The only
inputs that had to be supplied are the three tie-break decisions of §2; each is
forced by the involution requirement, with the witnesses listed in §4.
