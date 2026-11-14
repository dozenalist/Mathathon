# d3 five-cycle-finite-core — verdict: the finite claim is TRUE but the paper's `j in {1,4}` is not the strongest conclusion

Setup exactly as in the task. $D_i=\{i,i+2\}\subset\mathbb Z/5\mathbb Z$, a list $L\ne\varnothing$ is
**valid** iff $\bigcap_{i\in L}D_i=\varnothing$. Positions $r\in\mathbb Z/6\mathbb Z$; adjacent
position lists disjoint; every $i\in S(r)$ has a neighbour $(i\pm1)$ in $S(r+1)$ and $S(r-1)$.
All verdicts by exhaustive integer set arithmetic (`frozenset`s in `fivecycle.py`, bitmasks in
`check2.py`), no floats, no sympy.

Commands (from `.ultramath/smwfycy1c/m3/`):

    python3 fivecycle.py > out.json      # raw enumeration, JSON dump
    python3 check2.py                    # independent implementation, 15 asserts, exit 0

## 0. Support lists

21 of the 31 nonempty subsets of $\mathbb Z/5\mathbb Z$ are valid (the 10 invalid ones are the 5
singletons and the 5 pairs $\{i,i+2\}$). Every valid list contains an adjacent index pair, as the
paper says. Crucially $\{2,4\}$ is **not** valid ($D_2\cap D_4=\{4\}$), while $\{2,3,4\}$ is, and
$\{2,3,4\}$ is the *only* valid list containing $2,4$ and avoiding $0,1$.

## 1. All triples $(S_0,S_1,S_5)$ — the hypothesis set is NOT empty, it has exactly one element

$$\#\text{triples}=1,\qquad (S_0,S_1,S_5)=\big(\{0,1\},\{2,3,4\},\{2,3,4\}\big).$$

So the hypothesis set is non-empty and the claim is **not** vacuous. Strongest forced conclusion
(over all triples, forced = possible in every coordinate):

$$S_1=S_5=\{2,3,4\}\ \text{exactly},\qquad\text{and}\qquad S_0=\{0,1\}\ \text{exactly}.$$

The paper's "$2,4\in S^{(1)}\cap S^{(5)}$" is correct but strictly weaker: disjointness from
$S_0\ni 0,1$ gives $S_1\subseteq\{2,3,4\}$, and validity then forces $3\in S_1$ as well, because
$\{2,4\}$ alone is invalid.

## 2. The $j$ step, both readings

$S_3$ is valid, hence contains an adjacent pair $\{j,j+1\}$; the neighbour rule gives
$j-1,j+2\in S_2$ (and $\in S_4$), $S_2$ valid, $S_2\cap S_1=\varnothing$.

| reading | constraint used | surviving $j$ |
|---|---|---|
| **W** (paper: only $2,4\in S_1$, i.e. $S_2\cap\{2,4\}=\varnothing$) | $j-1,j+2\notin\{2,4\}$ | $\{1,4\}$ |
| **S** (full force $S_1=\{2,3,4\}$, i.e. $S_2\cap\{2,3,4\}=\varnothing$) | $S_2\subseteq\{0,1\}$ | $\varnothing$ |

W witness for both survivors: $S_2=\{0,1,3\}$ (valid). In W the paper's
"only $j\in\{1,4\}$ survive" is reproduced. In S nothing survives: $S_2\subseteq\{0,1\}$ would
have to contain the two distinct indices $j-1\ne j+2$, i.e. $\{j-1,j+2\}=\{0,1\}$, which needs
$j=1\wedge j=4$ or $j=2\wedge j=3$ — impossible. A hypothesis-faithful search over
$(S_1,S_2,S_3)$ (no hand-derived $j-1,j+2$) agrees: empty for every $j=0,\dots,4$.

**So the paper's $\{1,4\}$ is not the strongest available; the full force of $S_1$ kills every $j$.**

## 3. Stronger still: the whole Sec. 6.3.4 hypothesis set is empty

Exhaustive search over all 6-tuples $(S_0,\dots,S_5)$ of valid lists, adjacent disjoint, full
neighbour rule, $0,1\in S_0$: **0 configurations**. Kernel of the contradiction (paper's rule
"each $i\in S(a)$ has an adjacent index in $S(Ra)$ and $S(R^{-1}a)$", stated at *every* direction,
hence mutual across an adjacent pair):

* $0,1\in S_0\Rightarrow\{2,4\}\subseteq S_1\Rightarrow S_1=\{2,3,4\}\Rightarrow S_0\subseteq\{0,1\}\Rightarrow S_0=\{0,1\}$;
* but $3\in S_1$ has neighbours $2,4$, both in $S_1$, so $3$ has **no** neighbour in $S_0$ — contradicting the rule at direction $Ra$.

With only the one-directional rule ($i\in S_0$ needs a neighbour in $S_1$) the prefix $(S_0,S_1)$
is satisfiable and the prefix $(S_0,S_1,S_2)$ is already empty ($3\in S_1$ needs $2$ or
$4\in S_2\subseteq\{0,1\}$). So the accumulation contradiction of Sec. 6.3.4 is available after
**two** positions, not after six; the $j$ analysis and the Lemma 6.7 step bans are redundant.

**Verdict.** The finite claim is TRUE and non-vacuous at the literal 3-list level (exactly one
triple), and the paper's conclusion (no accumulation in the five-cycle locus) is unaffected — the
contradiction is reached, only far later than necessary. Stateable strengthening: from
$0,1\in S(a)$ alone the hypothesis set collapses, so "only $j\in\{1,4\}$ survive" can be replaced
by "no $j$ survives".

Files: `fivecycle.py` (frozenset enumeration, JSON), `check2.py` (bitmask re-implementation,
15 assertions, exit 0), `out.json` (raw output), `../m3/RESULTS.txt` (machine summary).
