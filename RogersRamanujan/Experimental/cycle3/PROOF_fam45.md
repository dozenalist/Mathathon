# The family $(4^r,1^s)$: phi in closed form, all $r,s\ge 0$

Worker m1, direction D, cycle 3. Exact integer arithmetic throughout.
Everything below is checked against the committed `Computation/bz82.py` by
`fam45.py` (9/9 checks, 4.5 s); the finite checks are evidence, not proof, and
each theorem is proved independently of them.

## 0. Setup and notation (BZ82, cited not re-derived)

State $(j;\lambda)$, $P(j)=j(5j-1)/2$, $|\lambda|+P(j)=n$, $\lambda_x$ the
$x$-th part or $0$ for $x>t=\ell(\lambda)$,
$$a=\min\{x\ge1:2j+x-\lambda_x>0\},\quad L=\lambda_a,\quad
k=a+2j-1,\quad \mu=k+1-L=a+2j-L,$$
$t^*=t+[a>t]+[\mu>t]$, $R=t+5j-2$. **Case I** iff $L+\lambda_\mu\ge 5j+t^*$;
**Case II** otherwise, with
$m=\max\{0\le z\le k-1: z+\lambda_{k-z}\le R\}$ (the printed maximum permits
$z=0$), then subtract $1$ from every part, create $m$ and $t+5j-3-m$, discard
zeros, $j\mapsto j-1$. Case I deletes the slots at $a$ and $\mu$ (virtual $0$
outside $1..t$, both collected before removal), adds $1$ to every remaining
slot, inserts $L+\lambda_\mu-5j-t^*$ ones and sets $j\mapsto j+1$.

Family: $\mathrm{fam}(r,s)=(4^r,1^s)$, $r,s\ge0$, $t=r+s$, weight $4r+s$.
All parts are $1$ or $4 \pmod 5$, so $\mathrm{fam}(r,s)\in A_{4r+s}$ (C1:
2666 objects checked, 0 bad). Several objects share a weight (e.g. $n=20$:
$(r,s)=(5,0),(4,4),(3,8),(2,12),(1,16),(0,20)$), which the rays $(1^s)$ and
$(4^r)$ alone do not provide.

Throughout $j=0$, so $P(j)=0$, $n=4r+s$ and $k=a-1$.

## 1. Lemma 1 (local data on the whole family)

For $\lambda=(4^r,1^s)$, $j=0$:

| range | $a$ | $L$ | $\mu$ | $\lambda_\mu$ | $L+\lambda_\mu$ | $t^*$ |
|---|---|---|---|---|---|---|
| $r=0,s=0$ | 1 | 0 | 1 | 0 | 0 | 2 |
| $r=0,s\ge1$ | 2 | 1 | 1 | 1 | 2 | $s$ |
| $1\le r\le4$, $s\ge1$ | $r+1$ | 1 | $r$ | 4 | 5 | $t$ |
| $1\le r\le4$, $s=0$ | $r+1$ | 0 | $r+1$ | 0 | 0 | $r+2$ |
| $r\ge5$, $s\ge0$ | 5 | 4 | 1 | 4 | 8 | $t$ |

*Proof.* $2j+x-\lambda_x=x-\lambda_x$. For $x\le r$, $\lambda_x=4$, so
$x-\lambda_x=x-4\le0$ iff $x\le4$. At $x>r$, $\lambda_x=1$ for $x\le r+s$ and
$0$ beyond.
* $r=0$: $\lambda=(1^s)$; $x-\lambda_x=0$ at $x=1$ when $s\ge1$, and $>0$ at
  $x=2$ (either $\lambda_2=1$ if $s\ge2$, or $\lambda_2=0$). For $s=0$,
  $\lambda_1=0$ and $x>0$, so $a=1$.
* $1\le r\le4$: all $x\le r\le4$ give $x-4\le0$; at $x=r+1$,
  $(r+1)-\lambda_{r+1}=r\ge1$ when $s\ge1$; when $s=0$,
  $(r+1)-0=r+1>0$. So $a=r+1$; $L=1$ iff $s\ge1$; $\mu=a-L$; for $s\ge1$,
  $\mu=r$ and $\lambda_r=4$; for $s=0$, $\mu=r+1>t$, $\lambda_\mu=0$.
* $r\ge5$: $x-4\le0$ for $x\le4$ and $x-4=1>0$ at $x=5\le r$, so $a=5$,
  $L=4$, $\mu=1\le t$, $\lambda_1=4$.

$t^*$ then follows from $\mu\le t\iff$ never exceeding $t$ in the listed
non-degenerate ranges: for $r=0,s=0$, $a=1>0=t$ and $\mu=1>0$; for
$r=0,s\ge1$, $a=2>t\iff s=1$; for $1\le r\le4,s=0$, $a=\mu=r+1>r=t$. $\square$

Note $a\ne\mu$ in every range of Lemma 1, so the Case-I deletion is never at a
doubled slot on this family (obligation (iii) is vacuous here).

## 2. Lemma 2 (which members are excluded)

$\mathrm{fam}(r,s)$ lies in $0\times B(n)$, i.e. phi is undefined on it, iff
$(r,s)\in\{(0,0),(0,1),(1,0),(2,0),(3,0),(4,0)\}$.

*Proof.* With $j=0$ and $t=\ell(\lambda)$ the excluded set is
$\{$all parts $\ge t\}$, vacuous for $t=0$. If $s=0$ this is $4\ge r$, i.e.
$r\le4$. If $s\ge1$ the smallest part is $1$, so $t\le1$, i.e. $(0,1)$ or
$(1,0)$; the second is already in the $s=0$ list. $\square$ (C2 confirms: the
excluded set computed from `bz82.phi_domain` equals this six-element set over
all $3315$ states of weight $\le160$.)

## 3. Theorem 1 (phi in closed form, all $r,s\ge0$)

For $\mathrm{fam}(r,s)$ outside the six excluded pairs, $\varphi(0;\lambda)$ is,
with $t=r+s$ and $\mathrm{desc}$ sorting the positive entries descending,

1. $r=0,\ s=2$: $\;(1;())$;
2. $r=0,\ s\ge3$: $\;(-1;(s-3))$ (the part is discarded when $s=3$);
3. $1\le r\le4,\ s\ge1,\ t\le5$: $\;(1;(5^{r-1},2^{s-1},1^{5-t}))$;
4. $1\le r\le4,\ s\ge1,\ t\ge6$: $\;(-1;\mathrm{desc}(3^{r},\ m,\ t-3-m))$,
   $m=\min(r-1,t-6)$;
5. $r\ge5,\ t\le8$: $\;(1;(5^{r-2},2^{s},1^{8-t}))$;
6. $r\ge5,\ t\ge9$: $\;(-1;(t-6,3^{r+1}))$.

*Proof.* Case I test: $L+\lambda_\mu\ge 5j+t^*=t^*$ (Lemma 1).

*Case 1/2 ($r=0$).* $L+\lambda_\mu=2$, $t^*=s$ for $s\ge1$, so Case I iff
$s\le2$; with $s\ge2$ (not excluded) that is $s=2$. Case I at $s=2$: $t=2$,
$a=2$, $\mu=1$ are both real slots, so deleting them leaves nothing;
$L+\lambda_\mu-5j-t^*=2-2=0$ ones inserted; $j\mapsto1$: $(1;())$.
Case II at $s\ge3$: $k=a-1=1$, so $z$ ranges over $0\le z\le k-1=0$, i.e.
$z=0$ alone. Admissibility there reads $0+\lambda_{k}=\lambda_1=1\le R=t-2=s-2$,
true exactly for $s\ge3$; hence $m=0$ and $p_2=t-3-m=s-3\ge0$. Every part
satisfies $\lambda_i-1=0$ and is discarded, so the image is
$(-1;\mathrm{desc}(s-3))$, i.e. $(-1;(s-3))$ for $s\ge4$ and $(-1;())$ at
$s=3$.

*Case 3/4 ($1\le r\le4,\ s\ge1$).* Case I iff $5\ge t$.
Case I: slots $1..r$ hold $4$, slots $r+1..t$ hold $1$; $a=r+1$ and $\mu=r$
are both real and distinct, so after deleting them and adding $1$ the
multiset is $5^{r-1},2^{s-1}$, and
$L+\lambda_\mu-5j-t^*=5-t$ ones are inserted (nonnegative because $t\le5$).
Case II ($t\ge6$): $k=a-1=r$, so $0\le z\le r-1$; $a-1-z=r-z\in[1,r]$, where
$\lambda=4$, so admissibility is $z\le t-6$. As $t-6\ge0$,
$m=\min(r-1,t-6)\ge0$; $p_2=t-3-m\ge t-3-(t-6)=3>0$. Subtracting $1$ from
$4$ gives $3$ ($r$ times) and from $1$ gives $0$ (dropped). $\square$ for
this case.

*Case 5/6 ($r\ge5$).* Case I iff $8\ge t$ (and $t\ge5$). Case I: $a=5,\mu=1$
are both real and distinct; slots $2,3,4$ and $6..r$ hold $4$ (count $r-2$),
slots $r+1..t$ hold $1$ (count $s$); $5-t$… precisely
$8-t$ ones are inserted. Case II ($t\ge9$): $k=a-1=4$, $0\le z\le3$,
$a-1-z=4-z\in[1,4]$, where $\lambda=4$, so admissibility is $z\le t-6$; since
$t-6\ge3$, $m=3$ and $p_2=t-6\ge3$. The parts $4-1=3$ occur $r$ times and
$m=3$ merges into that block: $3^{r+1}$, with $t-6\ge3$ first. $\square$

**Consequences (the obligations the brief lists for direction A, on this
subfamily).** (i) every created part is nonnegative — read off the proof
(Case 3/4: $5-t\ge0$; Case 6: $t-6\ge3$; Cases 1/2: $s-3\ge0$ or a discarded
zero); (ii) the inserted count $L+\lambda_\mu-5j-t^*$ is a nonnegative integer
in each Case-I line; (iii) the two deleted slots are always distinct and real
($a=\mu$ never occurs on this family); (iv) case stability is visible in the
closed form: the Case-I images $(1;\cdot)$ and the Case-II images
$(-1;\cdot)$ are separated by a threshold on $t$ only.

## 4. Theorem 2 ($\psi\circ\varphi$ in closed form, Case I, $r\ge1$)

In the Case-I ranges of Theorem 1 the phi-image is $(1;(5^A,2^B,1^C))$ with
$A=r-1,B=s-1,C=5-t$ (for $1\le r\le4$) or $A=r-2,B=s,C=8-t$ (for $r\ge5$). Then
$\psi$ selects **I(a)** and
$$\psi\varphi(0;(4^r,1^s))=(0;\mathrm{desc}(5A+2,2^B,1^C)),$$
i.e. $(0;(5r-3,2^{s-1},1^{5-t}))$ resp. $(0;(5r-8,2^{s},1^{8-t}))$.

*Proof.* $\psi$'s residue data: no part is $\equiv2,3\pmod5$ except possibly the
$2$'s, so $m_2=2$ iff $B\ge1$; parts $\equiv0\pmod5$ are exactly the $A$
fives, $t_0=A$; $j=1$, so $t_0+j=A+1>0$ and Case I of $\psi$ is selected. The
threshold is $5t_0+5j-3=5A+2\ge2\ge m_2$, so branch I(a) is taken: every part
$\equiv0\pmod5$ loses $5$ (each $5$ becomes the discarded $0$), every other
part is kept, the part $5A+2$ is appended and $j\mapsto0$. $\square$

So the $5$-block created by phi is *cancelled exactly* by $\psi$ in one step,
and the two-step image is again a $j=0$ state with the same weight. (C3: 20
Case-I states, 0 mismatches.)

## 5. Theorem 3 (full BZ82 endpoint for $r=1$, three residue classes)

Let $b(\lambda)$ denote the B-side endpoint of the alternating chain, i.e. the
first state $(0;\cdot)$ reached with all parts $\ge$ the length
(`bz82.pi_forward`). For $r=1$:

| $s$ | $b(4,1^s)$ | steps |
|---|---|---|
| $s\equiv1\pmod5$, $s\ge6$ | $(s-2,3,3)$ | 2 |
| $s\equiv2\pmod5$, $s\ge7$ | $(s+1,3)$ | 2 |
| $s\equiv3\pmod5$, $s\ge8$ | $(s-2,3,3)$ | 2 |
| $s=5$ | $(3,3,3)$ | 1 |
| $s=9$ | $(5,5,3)$ | 2 |

*Proof.* By Theorem 1 (case 4 with $r=1$, valid for $s\ge5$) the first step is
$\varphi(0;(4,1^s))=(-1;(K,3))$, $K=s-2$. Put $j=-1$ and $\lambda=(K,3)$ and
apply $\psi$; $K$ is the only part that can vary in residue.
* $K\equiv0$ ($s\equiv2$): $t_0=1$, $m_0=K$, $m_2=0$, so $\psi$ takes Case II
  ($t_0+j=0$) and $\mathrm{thr}=m_3+5j-3=-5<m_0$, so II(b): remove $K$, create
  $m_0-5j-2=K+3=s+1$, $j\mapsto0$: $(0;(s+1,3))$, length $2$, smallest $3\ge2$,
  so the chain stops.
* $K\equiv1$ ($s\equiv3$): $m_0=m_2=0$, $m_3=3$, Case II, $\mathrm{thr}=-5<0=m_0$,
  II(b) creates $3$ with nothing to remove: $(0;(K,3,3))$, length $3$, smallest
  $3\ge3$: stop.
* $K\equiv4$ ($s\equiv1$): identical to the previous line ($K\equiv4$ is still
  neither $0$ nor $2$ mod $5$): $(0;(K,3,3))$.
* $K\equiv2$ ($s\equiv4$): $m_2=K>0$, so $\psi$ takes Case I; the threshold
  $5t_0+5j-3=-8<K=m_2$, so I(b): remove $K$, keep $3$, create
  $K-5j-2-5t_0=K+3=s+1$ copies of $5$ ($s\equiv4\Rightarrow5\mid s+1$),
  $j\mapsto0$: $(0;(5^{(s+1)/5},3))$. This is in $B$ iff
  $3\ge(s+1)/5+1$, i.e. iff $s\le9$: the chain stops only at $s=9$.
* $K\equiv3$ ($s\equiv0$): $m_3=K$, $m_0=m_2=0$, Case II. For $s=5$, $K=3$ and
  $\mathrm{thr}=3-8<0=m_0$, so II(b) creates $3$: $(0;(3,3,3))$, stop. For
  $s\ge10$, $K\ge8$, so $\mathrm{thr}=K-8\ge0=m_0$ and II(a) is taken: remove
  $K$, create $K-8$ (discarded if $0$, i.e. at $s=10$), $j\mapsto-2\neq0$: the
  chain continues. $\square$

The last line is exactly the "expensive" behaviour: at $s=9$ the observation
that the Case-I(b) output $(5^{(s+1)/5},3)$ sits *on* the membership boundary
length $=$ smallest part is what separates the closed class $s\equiv4$ at
$s=9$ from the open class $s\ge14$.

## 6. Data: the whole endpoint table, weight $\le40$

`results_fam45.json` key `endpoint_table_weight_le_40`: all 231 pairs
$(r,s)$ with $4r+s\le40$, each with $\mathrm{lam}$, the Theorem-1 phi image
(or `excluded`), the B-side endpoint `b`, the D-side image `Tinv(b)` and the
number of alternating steps (225 members have a chain; 6 are excluded).
Path lengths range from $0$ to $699$ already at this weight, so no closed form
is to be expected from the table alone; sections 3 and 5 are where structure
lives.

## 7. Frozen conjectures and their exact fate

**P2 (open).** $b(4^2,1^s)=(s-1,6,3)$ for every $s\equiv2\pmod5$, $s\ge7$.
Frozen after seeing $s\le40$; tested on the held-out range $s=7..402$ (80
parameters, weights $\le410$): **0 failures, and the chain has length exactly
8 steps for all 80**. The proposition is not proved: the missing lemma is a
closed $8$-step local cycle on $(-1;(3,3,1,s-2))$. Smallest parameters that
would settle it: a counterexample at $s=407$ ($n=415$); for a proof, the
stabilised 8-step cycle.

**P3 (REFUTED).** The pattern of P2 does *not* continue to $r=3$:
$b(4^3,1^s)=(s+2,7,3)$ holds for $s=27,32,\dots,57$ ($31$ steps) and **fails at
$s=62$** ($n=74$), where the true image is $(25,17,8,8,8,8)$ after $1911$
alternating steps; it also fails at $s=67,72,77$. This is reported as a
refutation, not a near miss: the step count jumps from $31$ to $1911$ exactly
where the closed form dies.

**r = 1, classes $s\equiv0,4\pmod5$ (no closed form).** With a $20000$-step
cap, $6$ of $40$ parameters in class $0$ and $15$ of $40$ in class $4$ exceed
the cap (largest finite chains observed: $18702$ and $15452$ steps); e.g.
$b(4,1^{150})$ exceeds $10^6$ steps under the committed safeguard. Compare the
whole-family maximum $672$ quoted for the ones-ray in RR-C015: on this
two-parameter family BZ82's cost is far larger.

## 8. One precise extension question

**Q.** Is $b(4,1^s)$'s largest part ever $\equiv0\pmod5$ in the open class
$s\equiv4\pmod5$, $s\ge14$? Equivalently: after $\psi$'s I(b) creates the block
$5^{(s+1)/5}$ at $s=9$ (where it cancels *exactly* against the length
constraint), does the chain for $s\ge14$ ever return to a state whose largest
part is a multiple of $5$? The tested range $s=14,19,24,29,34$ says no
($(9,5,4),(11,7,5),(8,7,7,6),(17,16),(17,17,4)$: largest part never
$\equiv0$). Smallest parameters that settle the first open case: $s=39$
($n=43$) and $s=44$ ($n=48$); a proof would need a measure that strictly
decreases the multiplicity of the $5$-block modulo the length constraint, which
is the missing lemma.

## 9. What is not claimed

* Nothing here bears on the Mathathon objective (RR-C012): BZ82's map is used,
  not improved on.
* Theorems 1--3 are stated for the **family only**; the general all-input phi
  obligations (RR-C009) are untouched.
* P2 is a conjecture with 80 confirming parameters; that is evidence, not
  proof. P3 is a refutation and is exact.
