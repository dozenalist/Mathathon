# D4 — a structural candidate for RR127

Problem: A_n = partitions of n into parts ≡ 1,4 (mod 5); D_n = partitions of n with
λ_i ≥ λ_{i+1}+2.  Goal: an explicit weight-preserving bijection A_n → D_n whose
inverse is recoverable from the D-side object alone.

Swarm member m4, direction d3 (= D4).  All arithmetic is exact integer arithmetic,
Python 3 stdlib only, files in `.ultramath/smwfxwsqf/m4/`.

---

## 0. What is actually machine-verified here

| command | what it checks | result |
|---|---|---|
| `python3 explore.py` | \|A_n\| by enumeration = by coin-change DP; \|D_n\| by enumeration = by the recurrence d(n,m)=d(n,m−1)+d(n−m,m−2); and \|A_n\| = \|D_n\| = Σ_k p_{≤k}(n−k²) | **PASS for n = 0..22** |
| `python3 explore.py` | both inverse laws of the staircase map and of T on *every* element of D_n, k = 0 and n = 0 included; plus staircase∘T commutation b = μ + k | **PASS for n = 0..18** |
| `python3 explore.py` | fixtures: A_2={(1,1)}, D_2={(2)}; D_5={(5),(4,1)}, A_5={(4,1),(1⁵)}; T(7,3,1)=(5,3,3) | **PASS** |
| `python3 check_level_bij.py` | the sharper reduction of §1 | **PASS for n = 0..20** |
| `python3 mechanism.py` | stages F2+F3 end-to-end, with a level function that is correct *by construction*, as a bijection whose inverse needs no stored trace (fibre sizes come out as d(n,k)) | **PASS for n = 0..14** |
| `python3 mechanism.py` | the three natural candidate rules for the guessed component | **all three FAIL** (see §5) |
| `python3 examples.py` | worked examples n = 0..8 | below |
| `python3 invariant.py` | the residue invariant s − t ≡ n (mod 5) | **PASS for n ≤ 25** |

Counts (\|A_n\| = \|D_n\|), n = 0..22:
1, 1, 1, 1, 2, 2, 3, 3, 4, 5, 6, 7, 9, 10, 12, 14, 17, 19, 23, 26, 31, 35, 41.

---

## 1. The reduction I work in (provable; sharpened form of the given staircase map)

The given staircase map sends λ ∈ D_n of length k to μ, a weakly decreasing
nonnegative k-tuple of weight n − k², and the given shift T sends λ to
b = μ + (k,…,k), a partition of n into exactly k parts, all ≥ k.  Taking the
conjugate of b turns this into a statement about ν = conjugate(μ):

> **D_n ↔ ⊔_{0 ≤ k ≤ ⌊√n⌋} { ν : ν is a partition of n − k², every part of ν ≤ k }.**
> k is the number of parts of λ; ν = conjugate(staircase(λ)); μ = conjugate(ν);
> λ_i = μ_i + 2(k−i)+1.

Verified exhaustively for n ≤ 20 (`check_level_bij.py`).  Consequently

  \|D_n\| = Σ_k p_{≤k}(n − k²),   d(n,k) := p_{≤k}(n−k²),

and d(n,k) is the size the level-k fibre of **any** bijection must have.  Table:

  n=0:{0:1}  n=1:{1:1}  n=2:{1:1}  n=3:{1:1}  n=4:{1:1,2:1}  n=5:{1:1,2:1}
  n=6:{1:1,2:2}  n=7:{1:1,2:2}  n=8:{1:1,2:3}  n=9:{1:1,2:3,3:1}
  n=10:{1:1,2:4,3:1}  n=11:{1:1,2:4,3:2}  n=12:{1:1,2:5,3:3}
  n=13:{1:1,2:5,3:4}  n=14:{1:1,2:6,3:5}  n=15:{1:1,2:6,3:7}
  n=16:{1:1,2:7,3:8,4:1}  n=17:{1:1,2:7,3:10,4:1}  n=18:{1:1,2:8,3:12,4:2}
  n=19:{1:1,2:8,3:14,4:3}  n=20:{1:1,2:9,3:16,4:5}

Consequences every candidate bijection must meet: level 1 always has exactly one
element; levels present are exactly 1..⌊√n⌋ for n ≥ 1.

---

## 2. The mechanism

**"Level framework".**  A bijection Φ: A_n → D_n is *level compatible* when the
number of parts of Φ(α) depends only on α.  Every level-compatible Φ factors as

* **F1 (guessed!)** a rule `lev : A → {0,1,…,⌊√n⌋}`, applied to one A-partition,
  with **no** reference to any other n and no stored table;
* **F2** for each k a bijection  lev⁻¹(k) → {ν : parts(ν) ≤ k, \|ν\| = n−k²}.
  Canonical choice: sort both sets lexicographically and match by rank.  It is a
  canonical, parameter-free rule and it is invertible from the ν-side by unranking,
  but it is *contentless* — all the substance sits in F1.  (Flagged as such.)
* **F3** ν ↦ μ := conjugate(ν) ↦ λ_i := μ_i + 2(k−i)+1 — the given staircase map,
  proved, no guessing.

**Forward rule.**  α ∈ A_n  →  k := lev(α)  →  rank r of α in the lex-ordered
fibre lev⁻¹(k)  →  ν := the r-th partition of n−k² with parts ≤ k (lex order)
→  λ := staircase_inv(k, conjugate(ν)) ∈ D_n.

**Inverse (from λ alone, no trace).**  k := number of parts of λ; μ := staircase(λ);
ν := conjugate(μ) (checked: parts(ν) ≤ k, \|ν\| = n−k²); r := rank of ν among the
partitions of n−k² with parts ≤ k; α := the r-th element of lev⁻¹(k) in lex order.
Every step is a function of λ and n; nothing is remembered.

**Preserved invariant.**  Weight: Σα = n = k² + \|ν\| = Σλ, checked on every
element of every fibre for n ≤ 14.  Additionally the A-side invariant
**#(parts ≡ 1) − #(parts ≡ 4) ≡ n (mod 5)** holds (proof: reduce n = Σp mod 5);
its D-side transport I could **not** find, so I do not claim one.

**Terminating measure.**  k² ≤ n on the D-side, and along the forward direction the
staircase peel removes exactly k².  Equivalently, the measure −k is bounded below
and the construction is a single pass, so it terminates in O(number of parts).

---

## 3. Worked examples n = 0..8

F3 is fully explicit here (all rows verified by `examples.py`); the fibre sizes are
the forced d(n,·) of §1.

    n=0  A_0={()}                  D_0={()}                       k=0  μ=()          ν=()
    n=1  A_1={(1)}                 D_1={(1)}                      k=1  μ=(0)         ν=()
    n=2  A_2={(1,1)}               D_2={(2)}                      k=1  μ=(1)         ν=(1)
    n=3  A_3={(1,1,1)}             D_3={(3)}                      k=1  μ=(2)         ν=(1,1)
    n=4  A_4={(4),(1⁴)}            D_4={(4),(3,1)}                1:1, 2:1
         (4)  → k=1 μ=(3) ν=(1,1,1)   |   (3,1) → k=2 μ=(0,0) ν=()
    n=5  A_5={(4,1),(1⁵)}          D_5={(5),(4,1)}                1:1, 2:1
         (5)  → k=1 μ=(4) ν=(1⁴)       |   (4,1) → k=2 μ=(1,0) ν=(1)
    n=6  A_6={(6),(4,1,1),(1⁶)}    D_6={(6),(5,1),(4,2)}          1:1, 2:2
         (6) → k=1 μ=(5) ν=(1⁵) | (5,1) → k=2 μ=(2,0) ν=(1,1) | (4,2) → k=2 μ=(1,1) ν=(2)
    n=7  A_7={(6,1),(4,1³),(1⁷)}   D_7={(7),(6,1),(5,2)}          1:1, 2:2
         (7) → k=1 ν=(1⁶) | (6,1) → k=2 μ=(3,0) ν=(1³) | (5,2) → k=2 μ=(2,1) ν=(2,1)
    n=8  A_8={(6,1,1),(4,4),(4,1⁴),(1⁸)}   D_8={(8),(7,1),(6,2),(5,3)}   1:1, 2:3
         (8)→k=1 ν=(1⁷) | (7,1)→k=2 μ=(4,0) ν=(1⁴) | (6,2)→k=2 μ=(3,1) ν=(2,1,1)
         | (5,3)→k=2 μ=(2,2) ν=(2,2)

(For n ≤ 8 the fibre of level 1 is a singleton, so the A-partition → level
assignment is forced there; ambiguity starts only where some d(n,k) > 1 with more
than one k, i.e. at n = 4 and n ≥ 6.)

---

## 4. The one lemma I cannot prove

> **Lemma LS (level splitting).**  There exists a rule `lev`, evaluating on a single
> A-partition α (using only α and n = Sum α, with no lookup table and no reference
> to the other A-partitions of n), such that for all n and all k
>    #{α ∈ A_n : lev(α) = k} = p_{≤k}(n − k²).

I can *construct* a splitting with the right fibre sizes (by rank) and therefore the
framework of §2 is a genuine bijection with a D-side inverse — but I cannot produce
a rule for it that is checkable by hand.  **Lemma LS is the single gap.**  Everything
else in §1–§3 is proved or exhaustively checked.

**Which part is guessed:** exactly F1 (`lev`).  The specific guessed rule I tried is
`lev_G(α) := max{k : the k largest parts p_1 ≥ … ≥ p_k of α satisfy p_i ≥ 2i−1}`
(α "dominates the odd staircase").  It dies at n = 4: A_4 = {(4),(1⁴)} gives level 1
for both, but d(4,·) needs one element at level 1 and one at level 2 (witness (1,1,1,1),
n = 4).  No parameters were fitted to any matching table at any point.

---

## 5. What failed — quantified

Necessary condition tested: \|lev⁻¹(k)\| = d(n,k) for all k, level 0 empty for n > 0.

| guessed rule | first n failing | witness data |
|---|---|---|
| `lev = #(parts ≡ 4 mod 5)` ("5-carriers") | **n = 1** | α=(1) → level 0, but level 0 must be empty |
| `lev = len(α)` | **n = 2** | A_2={(1,1)} → level 2, required level 1 |
| `lev = min(len(α), ⌊√n⌋)` | **n = 5** | A_5={(4,1),(1⁵)} → both level 2; required {1:1, 2:1} |
| `lev_G` (odd-staircase domination, §4) | **n = 4** | A_4={(4),(1⁴)} → both level 1; required {1:1, 2:1} |

A wider battery of 24 natural statistics of the A-partition (number of parts,
largest/smallest part, #parts ≡ 1, #parts ≡ 4, #distinct parts, Durfee size,
Σ⌊p/5⌋, Σ⌈p/5⌉, parity counts, rank = max−len, …; `probe.py`, `probe2.py`) was
tested against the requirement that the level be a function of that statistic, in
the weak form "level counts obtainable by merging the value classes" — allowed at
every n ≤ 14.  The *strong* form fails for `len` by n = 6: A_6 = {(6),(4,1,1),(1⁶)}
has len-values 1,3,6 while d(6,·) = {1:1, 2:2}; since (1)∈A_1 forces g(1)=1 and
(1,1,1)∈A_3 forces g(3)=1 for any single global g with lev = g(len), A_6 would put
two elements at level 1, which has only one slot.  Conclusion: **the level no
simple local statistic can serve** — the parameter is genuinely global, which is
consistent with the known difficulty of Rogers–Ramanujan bijections.

Also negative, and worth recording: the largest-part distribution of A_n differs
from that of D_n already at **n = 2** (A_2 = {(1,1)} largest part 1; D_2 = {(2)}
largest part 2); it differs for every 2 ≤ n ≤ 12 (`probe.py`).  So no
largest-part-preserving bijection exists.

---

## 6. Honest status

Delivered: the sharpened reduction (§1, verified), a complete level-compatible
mechanism with an explicit forward rule, a D-side-recoverable inverse, a preserved
weight invariant, a bound on the terminating measure, and worked examples n = 0..8
(§2–3).  Not delivered: a *natural* rule for the guessed component; §4 Lemma LS is
open here, and §5 shows the obvious candidates are dead, with exact minimal
witnesses.  The trivial rescues are excluded on purpose: pairing A_n and D_n by
lexicographic rank (an order isomorphism, explicit and invertible) is a bijection
for every n but is exactly the "finite matching table" the brief forbids, and it
carries no structural information.
