# D1 EXACT ENUMERATION — SAIR Mathathon RR127 (swarm smwfxwsqf, member m1)

Definitions taken from the contract, unchanged:
A_n = partitions of n with every part = 1 or 4 (mod 5), multiplicities allowed;
D_n = partitions of n with lambda_i >= lambda_{i+1} + 2 for every i;
() is the unique partition of 0.

## Methods — two independent counters per side (plus a third, unrequested check)

Script `d1_enum.py`, NMAX = 30, Python 3.12 stdlib only, exact integer arithmetic.

1. **A, method (i), direct generation** (`gen_A_direct`): recursive enumeration
   of canonical **descending** tuples over `allowed = [p <= n : p mod 5 in {1,4}]`
   taken in decreasing order, `t` copies of each part, hard size cap
   `t*p <= remaining`. Every tuple is asserted to have sum exactly n, all parts
   = 1 or 4 mod 5, and no duplicate tuples appear.
2. **A, method (ii), DP** (`dp_A`): unbounded coin change —
   `a[0]=1`; for `p = 1..N` with `p mod 5 in {1,4}`, for `v = p..N`:
   `a[v] += a[v-p]`. Answer `a[n]`.
3. **D, method (i), direct generation** (`gen_D_direct`): recursive enumeration
   of canonical descending tuples with adjacent gap >= 2 and size cap
   (`p <= min(maxpart, remaining)`; after choosing p the cap becomes p-2).
   Every tuple is asserted to have sum exactly n, all gaps >= 2, no duplicates.
4. **D, method (ii), DP** (`dp_D`): memoised
   `d(n,m) = d(n,m-1) + d(n-m,m-2)`, with `d(0,m) = 1` for **all** m (including
   m <= 0), `d(n,m) = 0` for `n < 0`, and `d(n,m) = 0` for `n > 0 and m < 1`.
   Answer `d(n,n)`.
5. **Third check (extra)**: brute force over *all* partitions of n (5604 of them
   at n = 30), filtering by "all parts 1 or 4 mod 5" respectively "all gaps >= 2".

### The m = 1 / m = 2 boundary (explicitly checked, as demanded)

`d(n,1) = d(n,0) + d(n-1,-1)` under the rules above, so

| call | value | meaning |
|---|---|---|
| d(1,1) | **1** | `d(1,0)=0`, `d(0,-1)=1` — the single part 1 survives |
| d(2,1) | 0 | `(1,1)` correctly excluded |
| d(3,1) | 0 | |
| d(2,2) | 1 | the part 2 |
| d(0,0) | 1 | the empty partition |
| d(1,0) | 0 | |
| d(2,0) | 0 | |
| d(0,-5) | 1 | `|λ|=0` base case wins over `m<0` |

If the `m<1` rule were allowed to kill `d(1,1)`, then `|D_1|` would come out 0
and the table would already fail at n = 1. Values printed by the script under
key `d_boundary` in `d1_counts.json`.

## Counts for n = 0..30 (all four counters)

| n | |A_n| | |D_n| | A-dp | A-brute | D-dp | D-brute |
|---|------|------|------|---------|------|---------|
| 0 | 1 | 1 | 1 | 1 | 1 | 1 |
| 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 2 | 1 | 1 | 1 | 1 | 1 | 1 |
| 3 | 1 | 1 | 1 | 1 | 1 | 1 |
| 4 | 2 | 2 | 2 | 2 | 2 | 2 |
| 5 | 2 | 2 | 2 | 2 | 2 | 2 |
| 6 | 3 | 3 | 3 | 3 | 3 | 3 |
| 7 | 3 | 3 | 3 | 3 | 3 | 3 |
| 8 | 4 | 4 | 4 | 4 | 4 | 4 |
| 9 | 5 | 5 | 5 | 5 | 5 | 5 |
| 10 | 6 | 6 | 6 | 6 | 6 | 6 |
| 11 | 7 | 7 | 7 | 7 | 7 | 7 |
| 12 | 9 | 9 | 9 | 9 | 9 | 9 |
| 13 | 10 | 10 | 10 | 10 | 10 | 10 |
| 14 | 12 | 12 | 12 | 12 | 12 | 12 |
| 15 | 14 | 14 | 14 | 14 | 14 | 14 |
| 16 | 17 | 17 | 17 | 17 | 17 | 17 |
| 17 | 19 | 19 | 19 | 19 | 19 | 19 |
| 18 | 23 | 23 | 23 | 23 | 23 | 23 |
| 19 | 26 | 26 | 26 | 26 | 26 | 26 |
| 20 | 31 | 31 | 31 | 31 | 31 | 31 |
| 21 | 35 | 35 | 35 | 35 | 35 | 35 |
| 22 | 41 | 41 | 41 | 41 | 41 | 41 |
| 23 | 46 | 46 | 46 | 46 | 46 | 46 |
| 24 | 54 | 54 | 54 | 54 | 54 | 54 |
| 25 | 61 | 61 | 61 | 61 | 61 | 61 |
| 26 | 70 | 70 | 70 | 70 | 70 | 70 |
| 27 | 79 | 79 | 79 | 79 | 79 | 79 |
| 28 | 91 | 91 | 91 | 91 | 91 | 91 |
| 29 | 102 | 102 | 102 | 102 | 102 | 102 |
| 30 | 117 | 117 | 117 | 117 | 117 | 117 |

Explicit sequence (identical for A and D, i.e. the Rogers–Ramanujan values):

```
n= 0.. 9 : 1 1 1 1 2 2 3 3 4 5
n=10..19 : 6 7 9 10 12 14 17 19 23 26
n=20..29 : 31 35 41 46 54 61 70 79 91 102
n=30     : 117
```

## Agreement of the methods (for every n = 0..30)

```
CHECK A direct == A dp: True
CHECK D direct == D dp: True
CHECK A direct == A brute: True
CHECK D direct == D brute: True
CHECK |A_n| == |D_n| (RR): True
```

These five booleans are asserted inside the script, so any disagreement would
abort with a non-zero exit; the run above exited 0. Full log: `d1_enum.log`.

## Fixtures required by the task — reproduced

* `|A_2| = 1 = |D_2|`, with `A_2 = {(1,1)}`, `D_2 = {(2)}`.
* `D_5 = {(5), (4,1)}` and `A_5 = {(1,1,1,1,1), (4,1)}` — exactly the stated
  fixtures.

## Sets for n <= 6 (generator output, canonical descending tuples)

```
A_0 = [()]                                 D_0 = [()]
A_1 = [(1,)]                               D_1 = [(1,)]
A_2 = [(1, 1)]                             D_2 = [(2,)]
A_3 = [(1, 1, 1)]                          D_3 = [(3,)]
A_4 = [(1,1,1,1), (4,)]                    D_4 = [(4,), (3, 1)]
A_5 = [(1,1,1,1,1), (4,1)]                 D_5 = [(5,), (4, 1)]
A_6 = [(1,1,1,1,1,1), (4,1,1), (6,)]       D_6 = [(6,), (5, 1), (4, 2)]
```

All n = 0..30 listings (893 tuples per side) are dumped machine-readably in
`d1_sets_n0_30.json` (36 kB), so a proposed bijection can be checked by
`sorted(map(tuple, f(A_n_listing))) == sorted(D_n_listing)`.

## Wall times (CPython 3.12.14, this VM)

Whole-process wall clock, `/usr/bin/time -f "%e s"`, three consecutive runs of
`python3 d1_enum.py` (which does *all* of: direct generation n=0..30 both sides,
both DPs, both brute-force filters over all partitions of n, and both 6-element set
listings):

```
d1_enum wall=0.49 s
d1_enum wall=0.24 s
d1_enum wall=0.59 s
```

`d1_refine.py` (k-spectra, n <= 30): 0.12 s and 0.11 s.
`d1_sets.py` (all exact sets n = 0..30, 893 tuples per side, 36 kB written): 0.074 s.

Component times from inside the script (`time.perf_counter`), one representative
run that produced both `d1_enum.log` and `d1_counts.json` (`times_s`); these are
millisecond-scale and noisy, so treat them as orders of magnitude:

| component | representative | range seen over runs |
|---|---|---|
| method (i) direct generation, all n = 0..30, A+D | 0.0028 s | 0.0021 – 0.0116 s |
| DP for A, all n <= 30 | 7.5e-06 s | < 1e-5 s |
| DP for D, all n <= 30, memoised | 0.0051 s | 0.0008 – 0.010 s |
| brute force over all partitions, n = 0..30 (p(30)=5604) | 0.135 s | 0.07 – 0.34 s |

The slowest single n for direct generation wanders between n = 29 and n = 30
from run to run (< 0.9 ms for A and D together in every run observed) — the
per-n numbers at this size are dominated by interpreter noise, not by the
algorithm. Everything here is tiny: n = 40 would still be milliseconds.

## Bonus refinement: number of parts (k-spectra)

Script `d1_refine.py`, output `d1_by_length.json`. `specA[n][k]` = number of
λ in A_n with exactly k parts, likewise `specD`. Totals re-checked against
`d1_counts.json` for n = 0..30.

```
 n | k: |A_n^(k)|                    | k: |D_n^(k)|
 0 | {0: 1}                         | {0: 1}
 1 | {1: 1}                         | {1: 1}
 2 | {2: 1}                         | {1: 1}
 3 | {3: 1}                         | {1: 1}
 4 | {1: 1, 4: 1}                   | {1: 1, 2: 1}
 5 | {2: 1, 5: 1}                   | {1: 1, 2: 1}
 6 | {1: 1, 3: 1, 6: 1}             | {1: 1, 2: 2}
 7 | {2: 1, 4: 1, 7: 1}             | {1: 1, 2: 2}
 8 | {2: 1, 3: 1, 5: 1, 8: 1}       | {1: 1, 2: 3}
 9 | {1: 1, 3: 1, 4: 1, 6: 1, 9: 1} | {1: 1, 2: 3, 3: 1}
10 | {2: 2, 4: 1, 5: 1, 7: 1, 10: 1} | {1: 1, 2: 4, 3: 1}
11 | {1: 1, 3: 2, 5: 1, 6: 1, 8: 1, 11: 1} | {1: 1, 2: 4, 3: 2}
12 | {2: 2, 3: 1, 4: 2, 6: 1, 7: 1, 9: 1, 12: 1} | {1: 1, 2: 5, 3: 3}
```

**Negative fact, useful to the bijection directions:** the k-spectra differ
already at **n = 2** — A_2 = {(1,1)} has 2 parts, D_2 = {(2)} has 1. Hence

> **no bijection A_n → D_n can preserve the number of parts**, for n >= 2.

In particular the composition with T (which preserves the length of a D-partition)
cannot be a length-preserving correspondence, and the staircase reduction's k
(A-side length vs D-side length) is not what gets matched. Any candidate
mechanism must genuinely move weight between parts.

## Exact commands run (from `.ultramath/smwfxwsqf/m1`)

```
timeout 300 python3 d1_enum.py            # exit 0; table + five CHECK ... True lines + d_boundary
timeout 300 python3 d1_refine.py          # exit 0; k-spectra, first n with different spectra: 2
timeout 300 python3 d1_sets.py            # exit 0; wrote d1_sets_n0_30.json (36 kB), wall 0.0736 s
```

Key output lines (verbatim):

```
CHECK A direct == A dp: True
CHECK D direct == D dp: True
CHECK A direct == A brute: True
CHECK D direct == D brute: True
CHECK |A_n| == |D_n| (RR): True
d-boundary: {'d(1,1)': 1, 'd(2,1)': 0, 'd(2,2)': 1, 'd(0,0)': 1, 'd(1,0)': 0, 'd(3,1)': 0, 'd(2,0)': 0, 'd(0,-5)': 1}
first n with different k-spectra: 2
spectra totals match d1_counts.json for n=0..30: True
```

## Files (all in `.ultramath/smwfxwsqf/m1/`)

* `d1_enum.py` — the four counters + brute force + assertions (stdlib only).
* `d1_enum.log` — full stdout of the final run (exit 0), same run as `d1_counts.json`.
* `d1_counts.json` — counts, per-method arrays, wall times, check booleans,
  d-boundary values, fixtures, n <= 6 sets.
* `d1_counts.tsv` — the table, tab separated.
* `d1_refine.py`, `d1_refine.log`, `d1_by_length.json` — k-spectra refinement.
* `d1_sets.py`, `d1_sets.log`, `d1_sets_n0_30.json` — exact sets n = 0..30.
* `d1_results.md` — this note.

## Scope, and what is NOT claimed

This direction only tabulates and cross-checks. It does **not** construct or
verify a bijection, does not test the staircase or T inverse laws (those are
other directions' assignments), and does not use the web. What it does
establish, independently of anyone else's code, is that |A_n| = |D_n| for
n = 0..30 by three mutually independent algorithms per side, with every
generated tuple validated, plus the exact reference sets needed to test a
bijection. (The 31 values also agree, term for term, with the Rogers-Ramanujan
sequence as I recall it from OEIS A003114 - recollection only, not fetched: the
RULES forbid network access, so no online check was made and none is claimed.)
