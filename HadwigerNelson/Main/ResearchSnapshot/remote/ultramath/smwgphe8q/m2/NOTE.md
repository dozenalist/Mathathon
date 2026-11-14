# The angular-duality layer of CC60: what the strip lemmas really supply

**Claim of this note.** CC60's cone hypothesis enters at two logically separate points. The
strip/measure layer (Straddle, `outer_strip`, `inner_strip`, `finite_support_exclusion_ae`)
needs only **width $<\pi$**, and in fact supplies, for *every* subset of continua lying in one
closed cone of width $\le \pi/3$, an **open** angular window of length $\ge 2\pi/3$ together
with an annulus sector of **positive area** on which all the exclusions hold at once, off a
single null set. The constant $\pi/3$ therefore does **no** work in the geometric layer: it is
a purely combinatorial threshold. Two consequences are recorded below: the π/3 hypothesis is
strictly stronger than the geometry requires (so a proof that fails at width π/3 cannot be
blaming the geometry), and the "single shared radial side" of the OA120 construction is a
shorthand that is **only** valid because the strips are uniform in a neighbourhood — read
literally as an a.e. statement along a ray it would prove nothing.

Everything below is quoted from, or proved against, the source files
`lean/OAI/Geometry/PlaneColoring/AngularBoundary.lean`, `BoundaryTrace.lean`, `Palettes.lean`.
Every quantitative claim is reproduced exactly by `verify_dual_arc.py` (rational arithmetic
only; angles are exact rational multiples of π).

---

## 0. Setting and notation

$S^1=\{z\in\mathbb C:|z|=1\}$. For $u,v\in\mathbb C$ write $\langle u,v\rangle$ for the real
inner product of $\mathbb R^2$, so $\langle u,v\rangle=\|u\|\,\|v\|\cos\theta$ with $\theta$ the
angle from $u$ to $v$; thus $\langle u,v\rangle>0$ iff the angle between them is $<\pi/2$.

For a finite tuple $v_1,\dots,v_n\in S^1$ and $t\in S^1$ put

$$F(t)\;=\;\{\,i:\langle t,v_i\rangle>0\,\},\qquad
D(I)\;=\;\{\,t\in S^1: I\subseteq F(t)\,\}=\bigcap_{i\in I}H(v_i),\quad
H(v)=\{t:\langle t,v\rangle>0\}.$$

$H(v)$ is the **open** semicircle of directions within $\pi/2$ of $v$. A **closed arc** of $S^1$
means the image of a closed real interval of length $<2\pi$. For finite $V\subseteq S^1$ let

$$w(V)\;=\;\text{length of the smallest closed arc of }S^1\text{ containing }V ,$$

with $w(V)=0$ when $|V|\le 1$; and $w(I):=w(\{v_i:i\in I\})$. Equivalently $w(V)=2\pi-G(V)$
where $G(V)$ is the largest gap between cyclically consecutive points of $V$.

Quoted from the source, verbatim in content:

* `Straddle K` $=\{z:\exists p\in K,\ \exists q\in K,\ \mathrm{dist}(z,p)<1\ \wedge\ 1<\mathrm{dist}(z,q)\}$; it is open (`straddle_isOpen`).
* `ApproachingContinuum x K v`: $x\in K$, a sequence $r_n>0$ with $r_n\to0$, unit vectors $w_n\to v$, and $x+r_nw_n\in K$ for all $n$. So $v$ is a **signed** unit vector, not a line.
* `ApproachingContinuum.outer_strip`: if $\|e\|=1$ and $\langle e,v\rangle>0$ then there is $\delta>0$ with $x+re'\in\mathrm{Straddle}(K)$ for all unit $e'$ with $\|e'-e\|<\delta$ and all $r\in(1,1+\delta)$.
* `ApproachingContinuum.inner_strip`: if $\|e\|=1$ and $\langle e,v\rangle<0$ then there is $\delta>0$ with $x+re'\in\mathrm{Straddle}(K)$ for all unit $e'$ with $\|e'-e\|<\delta$ and all $r\in(1-\delta,1)$.
* `finite_support_exclusion_ae`: if $F_i\subseteq\mathrm{Fin}\,k$ with $\mathrm{spatialSupport}(c,j)$ disjoint from $\mathrm{Straddle}(K_i)$ for every $j\in F_i$, then $\forall^{\mathrm{a.e.}}z\ \forall i:\ z\in\mathrm{Straddle}(K_i)\Rightarrow c(z)\notin F_i$. **One** null set for all $i$ and all $j$ simultaneously.

---

## 1. Lemma 1 (the dual arc)

> **Lemma 1.** Let $v_1,\dots,v_n\in S^1$ and $I\subseteq\{1,\dots,n\}$, $I\ne\emptyset$. Then
> $D(I)=\bigcap_{i\in I}H(v_i)$ is open, and
> $$\bigl|D(I)\bigr| \;=\; \max\bigl(0,\ \pi-w(I)\bigr),$$
> where $|\cdot|$ is angular length. If $w(I)<\pi$, $D(I)$ is a single open arc, of length
> $\pi-w(I)$, centred at the midpoint of the closed arc of length $w(I)$ that spans
> $\{v_i:i\in I\}$. In particular
> $$D(I)\neq\emptyset \iff w(I)<\pi \iff \{v_i:i\in I\}\text{ lies in an open semicircle.}$$

*Proof.* $D(I)=\bigcap_{i\in I}H(v_i)$ is open as a finite intersection of open sets.

*Case $|I|=1$.* $D(I)=H(v_1)$ is an open arc of length $\pi$ and $w(I)=0$; done.

*Case $|I|\ge2$ and $w(I)<\pi$.* Let $A$ be the closed arc of length $w=w(I)$ containing
$V=\{v_i:i\in I\}$, and let $a,b$ be its endpoints. Then $a,b\in V$ (otherwise $A$ could be
shortened), and $A$ is the arc from $a$ to $b$ going the long way round. Parametrise $S^1$ by
angle with the midpoint $\mu$ of $A$ at $0$, so $A=[-w/2,w/2]$ and $a,b$ sit at $\mp w/2$.
Every $v\in V$ lies in $[-w/2,w/2]$, hence at angular distance $\le w/2$ from $\mu$.

$(\supseteq)$ Let $t$ have angular distance $<\tfrac{\pi-w}{2}$ from $\mu$. For $v\in V$ the
angular distance from $t$ to $v$ is at most $\tfrac{\pi-w}{2}+\tfrac{w}{2}=\tfrac{\pi}{2}$,
with equality only if both inequalities are equalities; the first is strict, so
$\mathrm{dist}(t,v)<\pi/2$, i.e. $\langle t,v\rangle>0$. Hence $t\in D(I)$.

$(\subseteq)$ Let $t\in S^1$ have angular distance $\ge\tfrac{\pi-w}{2}$ from $\mu$; write $t$
for its signed representative with $|t|\le\pi$. If $t\ge\tfrac{\pi-w}{2}$ then
$|t-a|=t+\tfrac w2\ge\tfrac{\pi}{2}$ with $t+\tfrac w2\le\pi+\tfrac{\pi}{2}=\tfrac{3\pi}{2}$
because $w<\pi$ and $t\le\pi$; so the angular distance from $t$ to $a$ is $\ge\pi/2$ and
$\langle t,a\rangle\le0$, so $t\notin H(a)\supseteq D(I)$. The case $t\le-\tfrac{\pi-w}{2}$
is symmetric with $b$. Hence $D(I)$ is exactly the open arc of length $\pi-w$ about $\mu$. $\square$

*Case $w(I)\ge\pi$.* Then $V=\{v_i:i\in I\}$ is contained in no open semicircle: if
$V\subseteq U$ with $U$ an open arc of length $\pi$, then the minimal closed arc spanning $V$
lies in the closure of $U$, an arc of length $\pi$, and has length exactly $\pi$ only if it *is*
that closed semicircle, in which case $V$ contains both of its endpoints, which are antipodal and
so cannot both lie in the open arc $U$; hence $w(I)<\pi$, contradiction. Therefore for every
$t\in S^1$ the open semicircle $H(t)=\{z:\langle t,z\rangle>0\}$ fails to contain $V$, i.e.
$I\not\subseteq F(t)$, i.e. $t\notin D(I)$. So $D(I)=\emptyset$, which is
$\max(0,\pi-w(I))$ for $w(I)\ge\pi$.

> **Corollary 1.1.** If $I$ lies in one closed cone of width $\le\pi/3$, i.e. $w(I)\le\pi/3$,
> then $D(I)$ is a **nonempty open** arc of length $\ge\pi-\pi/3=2\pi/3$, and the bound is
> attained exactly when $w(I)=\pi/3$.
>
> **Corollary 1.2 (the threshold is $\pi$, not $\pi/3$).** For a subset of continua the joint
> strip argument is available whenever $w(I)<\pi$; it *fails* exactly at $w(I)=\pi$. So
> CC60's hypothesis $w\le\pi/3$ is strictly stronger than the geometry requires.

Verified exactly (`verify_dual_arc.py`, groups C1–C4, C9) on six rational batteries - the
60° grid, a generic non-grid six-tuple with spacing $\pi/3$, an irregular tuple, two tuples
with repeated directions, an antipodal tuple and a closed-semicircle tuple - over all $6\times64$
subsets: $|D(I)|=\max(0,\pi-w(I))$ in every case, $D(I)\ne\emptyset\Leftrightarrow w(I)<\pi$
in every case, and $\min_{w(I)\le\pi/3}|D(I)|=2\pi/3$ with equality exactly at $w(I)=\pi/3$.

---

## 2. Lemma 2 (positive-measure shared sector; one null set)

> **Lemma 2.** Let $K_1,\dots,K_n$ be continua with `ApproachingContinuum` $x\,K_i\,v_i$, let
> $I$ be a nonempty finite index set with $w(I)<\pi$, and let $\beta\in D(I)$. Then there are
> $\delta>0$ and $\eta>0$ such that
> $$S\;:=\;\{\,x+re^{i\theta}\ :\ 1<r<1+\delta,\ |\theta-\beta|<\eta\,\}\;\subseteq\;\bigcap_{i\in I}\mathrm{Straddle}(K_i),$$
> and $S$ is a nonempty open annulus sector of Lebesgue area $\delta(2+\delta)\,\eta>0$.
> Consequently $\bigl|\bigcap_{i\in I}\mathrm{Straddle}(K_i)\bigr|>0$, and the six (or $n$)
> support exclusions hold **simultaneously at one point** for a.e. point of the intersection,
> the exceptional set being a single null set.

*Proof.* Fix $e_\beta=e^{i\beta}$. Since $\beta\in D(I)$, $\langle e_\beta,v_i\rangle>0$ for all
$i\in I$. `outer_strip` gives $\delta_i>0$ with $x+re'\in\mathrm{Straddle}(K_i)$ for every unit
$e'$ with $\|e'-e_\beta\|<\delta_i$ and every $r\in(1,1+\delta_i)$. Replacing $\delta_i$ by
$\min(\delta_i,1)$ (harmless: the conclusion is monotone in $\delta$) and then putting
$\delta=\min_{i\in I}\delta_i\in(0,1]$ (a finite minimum of positive reals; this is
`finite_positive_lower_bound` in the source), we get $x+re'\in\bigcap_{i\in I}\mathrm{Straddle}(K_i)$
for every unit $e'$ with $\|e'-e_\beta\|<\delta$ and every $r\in(1,1+\delta)$.

Since $\delta\le1$, $\eta:=2\arcsin(\delta/2)\in(0,\pi]$ is defined and positive, and
$|\theta-\beta|<\eta$ implies $|e^{i\theta}-e^{i\beta}|=2|\sin\tfrac{\theta-\beta}{2}|<\delta$.
Then
$S=\{x+re^{i\theta}:1<r<1+\delta,|\theta-\beta|<\eta\}\subseteq\bigcap_i\mathrm{Straddle}(K_i)$.
$S$ is open (polar coordinates are a homeomorphism onto $\mathbb C\setminus\{x\}$ and $S$ is the
image of the open rectangle $(1,1+\delta)\times(\beta-\eta,\beta+\eta)$), nonempty because
$\delta,\eta>0$, and by Fubini in polar coordinates
$$|S|=\int_{1}^{1+\delta}\!\!\int_{\beta-\eta}^{\beta+\eta} r\,d\theta\,dr=\frac{(1+\delta)^2-1}{2}\cdot2\eta=\delta(2+\delta)\eta>0 .$$
Since $S\subseteq\bigcap_i\mathrm{Straddle}(K_i)$ and $|S|>0$, the intersection has positive
measure. Finally `finite_support_exclusion_ae` produces a single null set $N$ with
$z\notin N,\ z\in\mathrm{Straddle}(K_i)\Rightarrow c(z)\notin F_i$ for all $i$ and all
$j\in F_i$; so for a.e. $z\in\bigcap_i\mathrm{Straddle}(K_i)$, no $F_i$ contains $c(z)$.
$\square$

> **Corollary 2.1 (why a single radial ray is not enough).** If the region replaced by the ray
> $R=\{x+re^{i\beta}:1<r<1+\delta\}$ then $|R|=0$, and the statement
> "$\forall^{\mathrm{a.e.}}z\in R:\ c(z)\notin F_i$" is **vacuously true** for every $F_i$: it
> carries no information. The OA120 description "$q(s)=x+s\,e^{i\beta}$ has modulus exactly
> $s>1$, so the outer strip applies at every $s$" is therefore correct only as a shorthand for
> the *uniform* statement over the sector; the ingredient that makes it work is that
> `outer_strip` is uniform in a neighbourhood of $(1,e_\beta)$, not that the ray is long.

> **Corollary 2.2 (a.e. quantifiers survive, pointwise ones do not).** The $n$ exclusions are
> combined on one null set, so no diagonal argument is needed and no measure is lost. What is
> lost is any pointwise or anglewise claim: by Lemma 1 the two endpoints of $D(I)$ are exactly
> the critical angles where some $\langle t,v_i\rangle=0$, and at those `outer_strip`'s strict
> hypothesis fails.

---

## 3. Lemma 3 (signedness: outer/inner pairing and antipodal pairs)

> **Lemma 3.** Let $v\in S^1$.
> (a) $H(v)=\{t:\langle t,v\rangle>0\}$ and $H(-v)=\{t:\langle t,v\rangle<0\}$ are the two open
> semicircles; each is exactly the set of angles at which `outer_strip` (resp. `inner_strip`)
> applies to a continuum approaching in direction $v$.
> (b) $H(v)\sqcup H(-v)=S^1$ up to the two critical points $\pm iv$; and
> $F(t+\pi)=S^1\setminus F(t)$ up to the measure-zero critical set. Hence `outer_strip` alone
> constrains a continuum on exactly one open semicircle of angles, and `outer_strip` together
> with `inner_strip` constrains it at **every** angle.
> (c) If $v_j=-v_i$ then $D(\{i,j\})=\emptyset$; the two outer strips of an antipodal pair are
> never applicable at a common point, so the *joint* constraint on that pair is vacuous. This is
> consistent with Lemma 1 since $w(\{i,j\})=\pi$.
> (d) A closed cone of width $\le\pi/3<\pi$ therefore contains no antipodal pair, and indeed
> every subset of it has width $\le\pi/3$.

*Proof.* (a) is the definition of $\langle\cdot,\cdot\rangle$. For (b): $\langle-t,v\rangle=-\langle t,v\rangle$, so $t\in H(v)\Leftrightarrow t+\pi\in H(-v)$; and
$H(v)\cup H(-v)=\{t:\langle t,v\rangle\neq0\}$ is the complement of the two antipodal critical
points $\{iv,-iv\}$, a null set for angular measure. (c) $\langle t,-v_i\rangle=-\langle t,v_i\rangle$, so the two are never both positive; equivalently $v_j$ lies exactly at angular distance $\pi$ from $v_i$, so $w=\pi$ and Lemma 1 gives $D=\emptyset$. (d) is immediate: $w(I)\le$ the width of the cone $\le\pi/3<\pi$. $\square$

> **Corollary 3.1 (single continua carry no angular information).** For $I=\{i\}$, Lemma 2
> applied to `outer_strip` and to `inner_strip` with the *same* hypothesis
> ($c\in J$ a.e. on $\mathrm{Straddle}(K_i)$) yields the same conclusion on $H(v_i)$ and on
> $H(-v_i)$, whose union is everything up to a null set. So a single continuum gives an
> angle-free constraint; **all** angular information in CC60 comes from subsets of size $\ge2$.

> **Corollary 3.2 (the source supplies signed directions).** `ApproachingContinuum` carries
> $v\in S^1$ with $w_n\to v$, and both strips are stated separately, so $v$ is an oriented unit
> vector. Replacing $v_i$ by $-v_i$ leaves Corollary 3.1 unchanged (the two strips swap), but
> changes the joint structure: $D$ is invariant under a *simultaneous* negation
> ($D(-I)=D(I)+\pi$) and not under a single one. Negating one member of a pair is exactly the
> antipodal degeneration of Lemma 3(c). Hence every joint constraint of CC60 must be stated for
> the signed tuple $(v_i)$, and no unsigned-line formulation is equivalent.

---

## 4. Lemma 4 (repeated directions are invisible at this layer)

> **Lemma 4.** If $v_i=v_j$ then $H(v_i)=H(v_j)$, hence $D(I)$ depends only on the *set*
> $\{v_i:i\in I\}$ and not on the multiplicities. In particular $v_i=v_j$ produces neither an
> obstruction nor an extra constraint at the strip layer; and the arc condition
> "$|\bigcup_{i:v_i\in A}E_i|\le3$ for every closed $A$ of length $\pi/3$", being a function of
> the multiset of directions, is identically blind to it.

*Proof.* $H$ is a function of the point $v$ alone; $D(I)=\bigcap_{i\in I}H(v_i)$ is therefore
unchanged when the index set is replaced by the set of distinct values of $v$ on $I$. The last
assertion is the definition of the arc condition. $\square$

> **Remark.** Lemma 4 is a *limitation*, not a defect: it says that two continua approaching in
> the same signed direction contribute the same angular window. Any use of their two distinct
> interface roles must come from the exclusion sets $F_i, F_j$ or the shapes $K_i,K_j$, i.e.
> from hypotheses outside the direction datum. A "surviving" or "forbidden" configuration that is
> justified only by directions therefore cannot use equality of directions as a resource.

---

## 5. Audit: the four questions, answered

**(Q1) Which six-interface realisations are actually produced by a weak colouring with the
source exclusions?** All of them that the arc condition admits. By Corollary 1.1, any set $I$ of
continua lying in one closed arc of angular length $\pi/3$ has $w(I)\le\pi/3$, hence by Lemma 1
an open dual arc of length $\ge2\pi/3$, hence by Lemma 2 a positive-measure annulus sector on
which every exclusion in $I$ holds at once off a single null set. So the geometry never blocks a
subset that the arc condition can select. The binding content of CC60 is therefore **entirely
combinatorial**: formulation (i) of the target is geometrically sound, and any failure of a
proposed strengthening is a failure of the (v,q) combinatorics, not of the strips.

**(Q2) Is the single shared radial side forced by the interface structure?** Neither forced nor
sufficient. The correct object is the pair (open dual arc $D(I)$, radial window $(1,1+\delta)$),
i.e. the annulus sector $S$ of Lemma 2, whose existence is *equivalent* to $w(I)<\pi$ (Lemma 1
plus Lemma 2). A single ray is a set of area zero and Corollary 2.1 shows the a.e. exclusion on
it is vacuous. So the radial side is supplied by the cone hypothesis (any $\beta$ in the
interior of the dual arc), not by the interface structure, and the interface structure supplies
nothing here.

**(Q3) Signed directions or unsigned lines?** Signed (Corollary 3.2). Single-continuum
statements are sign-blind (Corollary 3.1); joint statements are not; the antipodal pair is the
exact degeneration (Lemma 3(c)) and is automatically excluded by $w\le\pi/3<\pi$.

**(Q4) Do the a.e. quantifiers survive?** Yes, and in the strongest available form
(Corollary 2.2): one null set serves all continua and all colours, and the region where it bites
has positive measure. What does *not* survive is pointwise evaluation: the angular conclusion
holds on the **open** dual arc only, its endpoints being exactly the critical angles
$v_i\pm\pi/2$, and the six critical angles of the grid model are precisely that null set.

---

## 6. Sharpness: two exact counterexamples

**(E1) Width $\pi$ kills the joint constraint, and cannot be repaired.** Take
$v_1=1$, $v_2=-1$. Then $w=\pi$, $D(\{1,2\})=\emptyset$ (Lemma 1; exactly checked: no rational
$t=k/720$ in a $1440$-point grid has both inner products positive), while each singleton still
has $|D|=\pi$. So the threshold in the strip layer is exactly $\pi$: the joint constraint exists
for $w<\pi$ and vanishes for $w\ge\pi$. CC60 with $\pi/3$ sits a factor three inside this
threshold.

**(E2) The strict inequality $\langle e,v\rangle>0$ cannot be weakened to $\ge0$.**
Let $K=\{is:0\le s\le1\}$ (a compact connected set, i.e. a continuum), $x=0$, $v=i$. Then
$x\in K$ and with $r_n=1/(n+1)$, $w_n=i$ we have $x+r_nw_n=i/(n+1)\in K$ and $w_n\to v$, so
`ApproachingContinuum` $0\,K\,i$ holds. Take $e=1$: then $\langle e,v\rangle=0$. For every
$r>1$ and every $s\in[0,1]$,
$$\|r-is\|^2=r^2+(1-s)^2\ \ge\ r^2\ >\ 1,$$
so $r\cdot e=r$ has **no** point of $K$ at distance $<1$, whence $r\notin\mathrm{Straddle}(K)$.
Thus the conclusion of `outer_strip` fails at the boundary angle. Verified exactly on $2884$
rational samples `(r,s)` (group C10).

**Consequence.** The closed-π/3 cone is nevertheless safe: for $\beta$ the centre of the cone,
$\langle e_\beta,v_i\rangle\ge\cos(\pi/6)=\sqrt3/2>0$ for every $i$, so strictness holds with
room to spare, and the dual arc is open of length $\ge2\pi/3$. It is the *angular* variable $t$,
not the *direction* variable $v_i$, whose arc must be treated as open.

---

## 7. Candidate strengthenings and why each is blocked

| candidate strengthening / failure mode | verdict | blocked by |
|---|---|---|
| CC60 holds for cones of width $<\pi$ (unsaturated direction cone) | **open** — geometry allows it | not blocked by Lemmas 1–4; only the combinatorial step can block it. This is where d1's characterisation bites. |
| The arc condition is unrealisable because a $\pi/3$ cone cannot supply a common radial side | **false** | Lemmas 1 + 2: every $w\le\pi/3$ subset gets an open dual arc of length $\ge2\pi/3$ and a sector of positive area |
| Two equal directions $v_i=v_j$ break the argument | **false / inert** | Lemma 4: equal directions are invisible; no obstruction and no extra constraint |
| An antipodal pair is a counterexample to the joint form | **not applicable** | Lemma 3(c) + $w\le\pi/3$: antipodal pairs are excluded by the hypothesis, and they are exactly the degeneration where the joint constraint is vacuous |
| Closed endpoints of arcs of length exactly $\pi/3$ break the a.e. statement | **harmless in $v$, real in $t$** | Corollary 1.1: a closed direction cone of width exactly $\pi/3$ still gives an open dual arc; but the dual arc's endpoints are critical angles, so no pointwise claim at them |
| A single shared radial ray suffices | **false** | Corollary 2.1: zero area, a.e. exclusion vacuous |
| The a.e. quantifier degrades when six exclusions are combined | **false** | Corollary 2.2: one null set, positive-measure region |

---

## 8. What this note does not do

It does not decide the combinatorial arc condition on $(v,q)$ — that is d1's direction — and it
makes no statement about the plane, the chromatic number of the plane, or the truth of CC60.
It makes no claim at the six critical angles or at the endpoints of dual arcs. No claim here
depends on a numerical approximation: the verifier uses `fractions.Fraction` only, and every
sign test reduces to the exact rational predicate $\mathrm{cdist}(t,a)<1/2$.

## 9. Reproduce

```
python3 verify_dual_arc.py      # 6 batteries x 64 subsets, exact, ~0.3 s, one process
```
