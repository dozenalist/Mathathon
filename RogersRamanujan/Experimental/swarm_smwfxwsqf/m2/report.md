# m2 — RR127: the largest-part refinement is not preservable

Swarm `smwfxwsqf`, direction **d4** (my registered direction). Object of study:
the **refinement obstruction** — not a count table (m1/d1) and not a proposed
mechanism (m4/d3). Question: can *any* weight-preserving bijection
$f\colon A_n \to D_n$ also preserve a simple statistic (largest part, etc.)?

Answer, below, for 30 of 31 statistics: **no**, each refuted by an explicit
witness at a specific $n$. The largest-part case is refuted for *every* $n\ge2$.

## Files

| file | content |
|---|---|
| `m2_check.py` | certificate: staircase/T inverse laws, $\lvert A_n\rvert=\lvert D_n\rvert$, fixtures, statistic battery |
| `results.txt` | its output (163 lines) |
| `m2_obstruction.py` | quantified obstruction, length law, coarsening scan, forced elements |
| `obstruction.txt` | its output (199 lines) |

## Commands run

```
$ cd .ultramath/smwfxwsqf/m2 && python3 m2_check.py > results.txt      # exit 0
$ cd .ultramath/smwfxwsqf/m2 && python3 m2_obstruction.py > obstruction.txt   # exit 0
```

Wall times: `FIX` 0.004 s, `INV` 0.021 s, `CNT` 0.001 s, total 0.034 s;
`m2_obstruction.py` 0.56 s. Both scripts end in `ALL CHECKS PASSED`.
Stdlib only (`sys`, `time`, `itertools.groupby`); exact integers; no floating point.

## 1. Certificates (all pass)

`[FIX]` sets, $n \le 6$. The two contract fixtures hold; I also checked my own
hand-derived expectations for the other $n\le6$ and they hold:

```
n=2  A_2={(1,1)}                  D_2={(2,)}            <- contract
n=5  A_5={(4,1),(1,1,1,1,1)}      D_5={(5),(4,1)}       <- contract
n=4  A_4={(4),(1,1,1,1)}          D_4={(4),(3,1)}
n=6  A_6={(6),(4,1,1),(1^6)}      D_6={(6),(5,1),(4,2)}
```

(My first run failed here: I had guessed $A_4=\{(4)\}$, $A_6=\{(4,1,1),(1^6)\}$
and forgotten $6\equiv1 \pmod 5$. The generator was right; the expectation was
mine and wrong. That is the one place the checker bit during development.)

`[INV]` both maps are two-sided bijections for every $n\le25$, **434** states of
$D$ traversed, **434** staircase pairs $(k,\mu)$ and **434** shift pairs
$b\in B_n$ tested — image membership, weight, weak-decrease/nonneg, both round
trips, injectivity and surjectivity, and the boundary cases:

```
length histogram k -> #parts : {0: 1, 1: 25, 2: 132, 3: 204, 4: 71, 5: 1}
k = 0 occurs 1 time(s) (n = 0 only); k = 1 25; k = 2 132
```

`k=0` is exercised exactly once (the empty partition of $0$), `k=1` at every
$n\in[1,25]$, `k=2` 132 times. No failure recorded.

`[CNT]` $\lvert A_n\rvert=\lvert D_n\rvert$ for all $n\le25$:

```
 n :   0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25
|A|:   1   1   1   1   2   2   3   3   4   5   6   7   9  10  12  14  17  19  23  26  31  35  41  46  54  61
```

## 2. Main result: the largest-part refinement fails for all $n\ge2$

`[STS]` For $n\le12$ the largest-part distributions agree only at $n=0,1$:

```
n= 2 |A|=1 |D|=1  DIFFER      largest part r :  1  2
                              A count        :  1  0
                              D count        :  0  1
```

**Smallest $n$: 2. Witness: $(1,1)\in A_2$ has largest part 1; $D_2=\{(2)\}$ is
the whole $D$-side and has largest part 2.** Smallest witness tuple in
lexicographic order on descending tuples: $(1,1)$ versus $(2)$.

The cause is uniform, not an accident of small $n$:

**Proposition.** For every $n\ge2$ and every weight-preserving bijection
$f\colon A_n\to D_n$, $f$ does not preserve the largest part.

*Proof.* $1^n=(1,\dots,1)$ is a partition of $n$ into parts $\equiv1\pmod 5$, so
$1^n\in A_n$; it is the unique element of $A_n$ with largest part $1$. If
$\lambda\in D_n$ has largest part $1$ then $\lambda=(1,\dots,1)$ has length $n$,
and gaps $\ge2$ force $n=1$. Hence $D_n$ has no element with largest part $1$
for $n\ge2$, and $f(1^n)$ must have largest part $\ge2$. $\square$

The same argument with "length" in place of "largest part" gives: $1^n$ is the
unique element of $A_n$ of length $n$, and a partition of length $n$ with gaps
$\ge2$ has weight $\ge n^2$, so $D_n$ has none for $n\ge2$. Both statements were
also confirmed mechanically for $n\le30$ (`[OBS]`, `counterexamples : []`).

## 3. Thirty statistics refuted, one survivor

`[SCAN]` 31 statistics, full distributions compared for $n\le12$. Each *banned*
entry comes with an explicit $n$ and witness, so those refutations are
rigorous (one counterexample suffices); only the *approved* list is empirical.

```
statistic                        n   A-witness (value)     D-witness (value)
largest part                     2   (1,1)    1            (2)      2
smallest part                    2   (1,1)    1            (2)      2
number of parts                  2   (1,1)    2            (2)      1
number of distinct parts         4   (4)      1            (3,1)    2
parity of number of parts        2   (1,1)    0            (2)      1
number of parts mod 5            2   (1,1)    2            (2)      1
parity of largest part           2   (1,1)    1            (2)      0
largest part mod 5               2   (1,1)    1            (2)      2
number of parts equal to 1       2   (1,1)    2            (2)      0
number of parts = 0 mod 5        5   (4,1)    0            (5)      1
number of parts = 1 mod 5        2   (1,1)    2            (2)      0
number of parts = 2 mod 5        2   (1,1)    0            (2)      1
number of parts = 3 mod 5        3   (1,1,1)  0            (3)      1
number of parts = 4 mod 5        7   (4,1,1,1) 1           (7)      0
number of distinct residues mod5 4   (4)      1            (3,1)    2
max multiplicity                 2   (1,1)    2            (2)      1
repeated part? 0/1               2   (1,1)    1            (2)      0
number of odd parts              2   (1,1)    2            (2)      0
number of even parts             2   (1,1)    0            (2)      1
spread largest-smallest          4   (4)      0            (3,1)    2
largest minus 1                  2   (1,1)    0            (2)      1
number of parts >= 2             2   (1,1)    0            (2)      1
number of parts >= 5             5   (4,1)    0            (5)      1
sum of parts = 1 mod 5            2   (1,1)    2            (2)      0
sum of parts = 4 mod 5            7   (4,1,1,1) 4           (7)      0
sum of parts = 0 mod 5            5   (4,1)    0            (5)      5
multiplicity of the largest part 2   (1,1)    2            (2)      1
number of parts in a run >= 2    2   (1,1)    2            (2)      0
second largest part              2   (1,1)    1            (2)      0
largest - second largest         2   (1,1)    0            (2)      2
```

Reading: at that $n$ the A-witness carries a statistic value that occurs more
often in $A_n$ than in $D_n$ (so it cannot be matched), and the D-witness is an
unmatched value on the other side. The **only** consistent statistic is the
trivial control `weight mod 2`, which equals $n\bmod 2$ by construction.

Consequence for a candidate mechanism (m4): do not claim preservation of the
largest part, the smallest part, the length, the number of distinct parts, the
multiplicity profile, or any 5-residue count. Every such claim is already false
at the $n$ listed.

## 4. How badly it fails: minimum block count

`[COARS]` If one insists on *some* monotone recoding of the largest part,
how many contiguous blocks of the value line must be merged? A cut after value
$r$ is admissible iff $\sum_{r'\le r}(p_A(r')-p_D(r'))=0$. Writing
min / number of levels present:

```
 n   largest part      number of parts
     min/levels        min/levels
 0     1 / 1            1 / 1
 2     1 / 2            1 / 2
 4     2 / 3            2 / 3
 6     2 / 4            2 / 4
 7     1 / 5            1 / 4
 9     2 / 7            2 / 6
10     1 / 7            1 / 7
12     1 / 9            1 / 8
```

At $n=12$ the minimum is 1 while 9 levels occur: **no recoding of the largest
part into $\ge2$ contiguous classes has matching distributions at $n=12$**. The
largest part is not merely unpreservable, it is incompatible with every monotone
shadow of itself.

## 5. Two facts a candidate *can* use (verified)

`[DICT]` The two contract reductions are the same map up to the constant $k$:
with $\mu$ the staircase image and $b=T(\lambda)$, for all $\lambda\in D_n$,
$n\le25$ (**434** partitions, no failure):

$$\mu_i = b_i - k \quad (i=1..k),\qquad \mu_1=\lambda_1-2k+1,\ \mu_k=\lambda_k-1,\qquad b_1=\lambda_1-k+1,\ b_k=\lambda_k+k-1\ge k .$$

`[LEN]` Conversely, the length distribution of $D_n$ is forced by the $(k,\mu)$
reduction:

$$\#\{\lambda\in D_n:\ \ell(\lambda)=k\}\;=\;p\bigl(n-k^2 \text{ into at most } k \text{ parts}\bigr).$$

Verified for all **351** pairs $(n,k)$ with $n\le25$ — no violation. So a
candidate $f\colon A_n\to D_n$ must split $A_n$ into blocks of exactly these
sizes; this is a hard, cheap sanity check on any proposed mechanism.

`[FORCED]` Elements of $A_n$ whose largest part never occurs as a largest part in
$D_n$ — these must move *off* their largest part under every candidate:

```
 n  |A_n|  #forced   examples
 2    1      1       (1,1)
 4    2      1       (1,1,1,1)
 7    3      2       (4,1,1,1), (1^7)
 9    5      3       (4,4,1), (4,1,1,1,1,1), (1^9)
12    9      4       (4,4,4), (4,4,1,1,1,1), (4,1^8), (1^12)
```

## 6. Honest limits

* The 30 refutations are rigorous (explicit witness each). The statement "no
  *natural* statistic is preserved" is **not** a theorem: it is a finite scan of
  31 statistics plus 425 binary coarsenings (36 coarsenings agree for $n\le12$,
  e.g. `largest part == 9`, `spread largest-smallest <= 9`; these are
  coincidences at specific $n$, not structural — none is a function of $n$
  alone except the trivial control).
* The two Prop-style statements in §2 are complete proofs, nothing guessed.
* I did **not** search the literature; no external claim is made about what is
  known. Everything above is computed in this VM by the two scripts listed.
* I did not attempt to construct a bijection — that is d3/m4's direction.
* The scripts intentionally recompute from scratch (own generators, own DP-free
  enumeration); they share no code with m1's.
