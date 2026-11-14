# The closed 60° cone condition on six cyclic interfaces:
# exact solution set, degenerate cases, and sharpness

*Solo computation + proof. Every numerical claim below is an exact statement about rational
multiples of $\pi$; all of them are re-checked in exact arithmetic by `cone_arc.py` in this
directory (Fractions only, no floating point, one process, ~5 s).*

---

## 0. Setting and the exact reading of the data

Colour set $C=\mathbb Z/6=\{0,\dots,5\}$. Slots $i\in\mathbb Z/6$ (indices always mod 6).
Cyclic interfaces
$$E_i=\{i,i+1\}\subseteq C .$$
Direction circle $T=\mathbb R/2\pi\mathbb Z$; data $v=(v_0,\dots,v_5)\in T^6$; $\operatorname{dist}$
is the circular distance on $T$ (values in $[0,\pi]$). Write $w=\pi/3$.

**Condition $\mathrm{CC60^{arc}}(v)$.** For every closed arc $A\subseteq T$ of angular length
exactly $w$,
$$\Big|\bigcup\{E_i : v_i\in A\}\Big|\le 3 . \tag{$\ast$}$$

*Why this is the continuous form of the six-direction grid.* In
`supervisor/solve-graphs/AC-CONE-SIX.md` the data are labels $q\in(\mathbb Z/6)^6$, the six
interfaces are the same $E_i=\{i,i+1\}$, and $q_i$ **is the direction of interface $E_i$**, in units
of $60^\circ$; the filter tested there is
$$(\dagger)\qquad \Big|\bigcup\{E_i : q_i\in\{d,d+1\}\}\Big|\le 3 \qquad (d\in\mathbb Z/6).$$
So the grid data are exactly $v_i=q_i\pi/3$, and the continuous generalisation replaces the
grid angle $q_i\pi/3$ by an arbitrary real angle $v_i$ — item (i) of the brief. Lemma 4 below shows
$(\ast)\iff(\dagger)$ on grid data, so $(\ast)$ is a faithful generalisation and not a different
condition. Arbitrary label data (an arbitrary family of interfaces, possibly with repetitions) is
covered by Proposition 2.

*Standing convention.* A "closed arc of length $w$" is a set $[a,a+w]$; "all $v_i$ lie in one closed
cone of width $w$" is the special case $S=\{0,\dots,5\}$ of $(\ast)$. Where the brief says "arcs of
length $\pi/3$", closedness of the endpoints is essential and is used (Corollary 3(c)).

---

## 1. Lemma 1 (combinatorial core)

> **Lemma 1.** For $S\subseteq\mathbb Z/6$:
> $$\Big|\bigcup_{i\in S}E_i\Big|\le 3 \iff S\subseteq\{a,a+1\}\ \text{for some } a\in\mathbb Z/6 .$$

*Proof.* ($\Leftarrow$) $\bigcup_{i\in S}E_i\subseteq E_a\cup E_{a+1}=\{a,a+1,a+2\}$.
($\Rightarrow$) Suppose $\big|\bigcup_{i\in S}E_i\big|\le 3$. If $|S|\ge 3$ pick distinct
$i,j,k\in S$; for any two of them $|E_i\cup E_j|\le 3<4=|E_i|+|E_j|$, so $E_i\cap E_j\ne\varnothing$.
But $E_i\cap E_j\ne\varnothing$ iff $j\equiv i\pm1 \pmod 6$. Hence $i,j,k$ are pairwise cyclically
adjacent, i.e. they form a triangle in the 6-cycle, which is triangle-free — contradiction. So
$|S|\le 2$, and for $S=\{i,j\}$ the same intersection argument gives $j\equiv i\pm1$, i.e.
$S\subseteq\{i,i+1\}$ after relabelling. $\blacksquare$

(The script checks all 64 subsets; e.g. $\big|\bigcup_{i\in\{0,2\}}E_i\big|=|\{0,1,2,3\}|=4$ and
$\big|\bigcup_{i\in\{0,1,2\}}E_i\big|=4$, while $|\{0,1\}|=3$.)

---

## 2. Proposition 2 (general exact form, arbitrary labels)

> **Proposition 2.** Let $(E_i)_{i\in I}$ be any finite family of finite colour sets and
> $v:I\to T$. Then $(\ast)$ holds if and only if
> $$\Big|\bigcup_{i\in S}E_i\Big|\le 3\qquad\text{for every } S\subseteq I \text{ such that } \{v_i : i\in S\} \text{ lies in a closed arc of length } w.$$

*Proof.* Let $S_A=\{i:v_i\in A\}$. Since $S\mapsto S_A$ maps arcs to index sets and every index set
$S$ with $v_S\subseteq[a,a+d]$, $d\le w$, satisfies $S\subseteq S_{[a,a+w]}$, ranging over arcs of
length exactly $w$ is the same as ranging over those sets $S$. $\blacksquare$

(One reading note. If instead one allows the six directions to carry an *arbitrary* family of labels
$q_i\in\mathbb Z/6$, with $E_{q_i}$ the interface carried by $v_i$, then Proposition 2 applies
verbatim, and repeated labels only make the condition *weaker*: six copies of a single interface make
$(\ast)$ vacuous, since $|\bigcup_{i\in S}E_{q_i}|\le2\le3$ always. The nontrivial case — and the one
of AC-CONE-SIX and of the brief, where "all six $E_i$ must be realised near $x$" — is exactly the
present one, in which the six distinct interfaces $E_0,\dots,E_5$ are carried by the six slots. That
is why "all six realised" is load-bearing: it is what makes the prism constraints bite.)

Proposition 2 is what makes "an arc containing several $v_i$" harmless: the *only* data an arc
carries is its index set, and for the six cyclic interfaces those index sets are governed by
Lemma 1, i.e. by pairwise information. No condition involving three or more directions
simultaneously can be stronger than the pairwise one in this system.

---

## 3. Theorem 3 (exact solution set: the nine pairwise constraints)

Let
$$\mathcal P:=\binom{\mathbb Z/6}{2}\setminus\bigl\{\{i,i+1\}:i\in\mathbb Z/6\bigr\}$$
be the nine **non-consecutive** pairs (these are the edges of $K_6\setminus C_6$, the triangular
prism: triangles $\{0,2,4\}$, $\{1,3,5\}$ plus the matching $03,14,25$), and put
$$\mathcal V:=\Bigl\{v\in T^6:\ \operatorname{dist}(v_i,v_j)>w \ \text{ for all } \{i,j\}\in\mathcal P\Bigr\}.$$

> **Theorem 3.** For the six cyclic interfaces, $\mathrm{CC60^{arc}}(v)$ holds $\iff$ $v\in\mathcal V$.
> Equivalently the set of surviving direction data is *exactly*
> $$\mathcal V=\{v\in T^6:\ \min_{\{i,j\}\in\mathcal P}\operatorname{dist}(v_i,v_j)>\pi/3\},$$
> a set cut out by nine **strict** inequalities.

*Proof.* ($\Leftarrow$) Let $A$ be a closed arc of length $w$ and $S=\{i:v_i\in A\}$. Any two points
of $A$ are at distance $\le w$, so $\operatorname{dist}(v_i,v_j)\le w$ for all $i,j\in S$; by
hypothesis $S$ contains no non-consecutive pair, hence $|S|\le 2$ (three distinct slots in
$\mathbb Z/6$ always contain a non-consecutive pair) and $S\subseteq\{a,a+1\}$; Lemma 1 gives
$(\ast)$.
($\Rightarrow$, contrapositive) Suppose $\operatorname{dist}(v_i,v_j)\le w$ for some
$\{i,j\}\in\mathcal P$. The shorter arc between $v_i,v_j$ is a closed arc of length
$d=\operatorname{dist}(v_i,v_j)\le w<\pi$; since $2\pi>w$, it can be extended to a closed arc $A$ of
length exactly $w$ containing both. Then the index set $S=\{k:v_k\in A\}\supseteq\{i,j\}$ is not
contained in two consecutive slots, so by Lemma 1
$\big|\bigcup_{k\in S}E_k\big|\ge4$, i.e. $(\ast)$ fails. $\blacksquare$

So **the entire continuous content of CC60 for the six cyclic interfaces is nine scalar
inequalities**. In particular $\mathcal V$ is invariant under simultaneous rotation
$v\mapsto v+(t,\dots,t)$, and depends only on the multiset of pairwise circular distances on those
nine pairs.

---

## 4. Corollary 3 (all degenerate cases, explicitly)

Throughout, $v\in\mathcal V$ and $w=\pi/3$.

**(a) Two equal directions.** $v_i=v_j$ is admissible **iff** $\{i,j\}$ is cyclically consecutive.
If $\{i,j\}\in\mathcal P$ and $v_i=v_j$, then any closed arc of length $w$ through that common
direction contains both, and its index set spans $\ge4$ colours: $(\ast)$ fails. Consecutive
coincidences are free: the grid-A point $(0,0,\tfrac{2\pi}3,\tfrac{2\pi}3,\tfrac{4\pi}3,\tfrac{4\pi}3)$
has $v_0=v_1$, $v_2=v_3$, $v_4=v_5$ and survives (checked exactly); six pairwise **distinct**
directions also survive (§5), so multiplicity is completely unconstrained.

**(b) Antipodal pairs.** $\operatorname{dist}=\pi>w$ always, so an antipodal pair never violates
anything, whatever its slot pair. Example surviving exactly: $v=(0,\pi,\tfrac\pi2,\tfrac{3\pi}2,\tfrac{7\pi}5,0)$
(script, case "antipodal pair").

**(c) Distance exactly $\pi/3$ and closed endpoints.** $\operatorname{dist}(v_i,v_j)=w$ for
$\{i,j\}\in\mathcal P$ is a **violation**: the inequality in Theorem 3 is strict, and the reason is
precisely that arcs are closed — $[v_i,v_i+w]$ contains both $v_i$ and $v_j$. Hence
$\mathcal V$ is open in $T^6$ and
$$\partial\mathcal V=\Bigl\{v:\ \exists\{i,j\}\in\mathcal P,\ \operatorname{dist}(v_i,v_j)=\pi/3\Bigr\}.$$
So *no* boundary point of the constraint set satisfies CC60; openness is a genuine feature of the
closed-arc formulation, not an artefact. Example failing with witness arc:
$v=(0,\tfrac\pi3,\tfrac\pi3,\pi,\tfrac{4\pi}3,\tfrac{5\pi}3)$, pair $\{0,2\}$ at distance exactly
$\pi/3$, offending arc $[0,\pi/3]$ with index set $\{0,1,2\}$.

**(d) Arcs containing several directions.** A closed arc of length $w$ contains **at most two** of
the six directions, and if it contains two they occupy consecutive slots. (Three distinct slots
always contain a non-consecutive pair; then the arc would violate Theorem 3.) Consequently an arc of
length exactly $w$ spans
* $0$ or $1$ directions $\Rightarrow |\bigcup E_i|\le 2$,
* exactly the consecutive pair $\{a,a+1\}\Rightarrow \big|\bigcup E_i\big|=3$ — **equality**.

So "sharp equality at cone width $\pi/3$" in the arc sense is the generic case: it occurs exactly for
arcs whose direction set is a consecutive pair, and it is compatible with an open set of data
(§5). The $\pi/3$ width is *not* where $(\ast)$ saturates; see Theorem 6.

**(e) Monotone variants.** Replacing "length exactly $w$" by "length $\le w$" changes nothing
(containment of closed arcs). Weakening the width to $\theta<w$ gives, by the same proof, the weaker
set $\{v:\operatorname{dist}> \theta \text{ on }\mathcal P\}\supseteq\mathcal V$; strengthening it is
treated exactly in Theorem 6.

---

## 5. Theorem 3, Corollary: the survivor set is open and full-dimensional (answer to (ii))

**(i) Openness and dimension.** By Theorem 3 and Corollary 3(c), $\mathcal V\subseteq T^6$ is open;
hence it is **not** a finite union of grid points or of any finitely many grid-like strata. If
nonempty it is a 6-dimensional open semialgebraic (in fact piecewise-linear-on-the-cover) set. The
six grid survivors of AC-CONE-SIX are interior points of $\mathcal V$ (each has all nine constrained
distances $\ge 2\pi/3>\pi/3$).

**(ii) An explicit genuinely non-grid survivor with a certificate.**
$$v^\star=\frac{\pi}{20}\,(1,\,5,\,14,\,18,\,28,\,32)
\quad\text{i.e.}\quad (9^\circ,45^\circ,126^\circ,162^\circ,252^\circ,288^\circ).$$
All six directions are distinct and none is a multiple of $60^\circ$. The nine constrained distances
are, exactly,
$$\operatorname{dist}(v^\star_0,v^\star_2)=\tfrac{13}{20}\pi,\ \
\operatorname{dist}(v^\star_0,v^\star_3)=\tfrac{17}{20}\pi,\ \
\operatorname{dist}(v^\star_0,v^\star_4)=\tfrac{13}{20}\pi,$$
$$\operatorname{dist}(v^\star_1,v^\star_3)=\tfrac{13}{20}\pi,\ \
\operatorname{dist}(v^\star_1,v^\star_4)=\tfrac{17}{20}\pi,\ \
\operatorname{dist}(v^\star_1,v^\star_5)=\tfrac{13}{20}\pi,$$
$$\operatorname{dist}(v^\star_2,v^\star_4)=\tfrac{7}{10}\pi,\ \
\operatorname{dist}(v^\star_2,v^\star_5)=\tfrac{9}{10}\pi,\ \
\operatorname{dist}(v^\star_3,v^\star_5)=\tfrac{7}{10}\pi,$$
the minimum being $\tfrac{13}{20}\pi$, with slack $\tfrac{13}{20}\pi-\tfrac{\pi}{3}=\tfrac{19}{60}\pi$
over the threshold $\pi/3$. **Full-dimensional certificate:** moving both endpoints of a pair by at
most $\rho$ changes their circular distance by at most $2\rho$, so the sup-norm ball
$$B=\{v\in T^6:\ \max_i\operatorname{dist}(v_i,v^\star_i)<\rho\},\qquad \rho=\tfrac{19}{180}\pi=19^\circ$$
satisfies $\operatorname{dist}\ge \tfrac{13}{20}\pi-2\rho=\tfrac{79}{180}\pi>\pi/3$ on all nine pairs,
i.e. $B\subseteq\mathcal V$. The set of grid rotations is a countable (here finite, 36-element)
nowhere-dense set, so $B$ minus it is an open set of **genuinely non-grid** survivors. All 64 corners
of the box plus random interior points are verified exactly by the script.

**(iii) A four-parameter family whose corner is the grid-A point.** For
$0\le\alpha,\beta,\gamma\le \pi/4$ and any $t\in T$,
$$v(\alpha,\beta,\gamma;t)=t+\Bigl(0,\ \alpha,\ \tfrac{2\pi}3,\ \tfrac{2\pi}3+\beta,\ \tfrac{4\pi}3,\ \tfrac{4\pi}3+\gamma\Bigr).$$
*Proof that $v(\alpha,\beta,\gamma;t)\in\mathcal V$:* rotation invariance reduces to $t=0$, and then
the nine constrained distances are $2\pi/3$ for the pairs $\{0,2\},\{0,4\},\{2,4\}$, and
$$\tfrac{2\pi}3+\beta,\quad \tfrac{2\pi}3+\beta-\alpha,\quad \tfrac{2\pi}3+\alpha,\quad
\tfrac{2\pi}3+\gamma,\quad \tfrac{2\pi}3-\gamma+\alpha,\quad \tfrac{2\pi}3+\gamma-\beta$$
for $\{0,3\},\{1,3\},\{1,4\},\{2,5\},\{1,5\},\{3,5\}$ respectively; every expression lies in
$[\tfrac{5}{12}\pi,\tfrac{11}{12}\pi]\subset(0,\pi)$, so it *is* the circular distance, and it is
$>\pi/3$. $\blacksquare$
At $(\alpha,\beta,\gamma)=(0,0,0)$ this is the grid-A point $(0,0,\tfrac{2\pi}3,\tfrac{2\pi}3,\tfrac{4\pi}3,\tfrac{4\pi}3)$,
so **the grid-A configuration is not isolated: it is the corner of a 4-parameter family of
genuinely non-grid survivors** (already $\alpha=\beta=\gamma=\pi/4$ gives six distinct non-grid
angles). The script verifies 500 exact parameter points.

**(iv) Conclusion for (ii).** The common-interface topology (six interfaces, consecutive ones
sharing a label, all six carried by directions near $x$) does **not** force an excluded arc and does
not force the directions into any grid: the exact solution set of the complete combinatorial content
of CC60 is the open, full-dimensional $\mathcal V$, with non-grid points in its interior. Any further
constraint on the directions must come from the *geometric* input (the source's exclusion structure
$H_i$ at the continua $K_i$), not from the interface combinatorics. The precise extra hypothesis
under which the grid *is* forced is isolated in Theorem 7.

---

## 6. Lemma 4 (grid specialisation: the generalised condition agrees with AC-CONE-SIX)

> **Lemma 4.** For grid data $v_i=q_i\pi/3$, $q\in(\mathbb Z/6)^6$, the arc condition $(\ast)$ is
> equivalent to the six tests $(\dagger)$.

*Proof.* The six grid points $d\pi/3$ are spaced exactly $w$ apart, so every closed arc of length
exactly $w$ contains at least one grid point and at most two, and two only if they are consecutive:
$$A\mapsto \{i:v_i\in A\}\in\Bigl\{\{i:q_i=d\},\ \{i:q_i\in\{d,d+1\}\}\ :\ d\in\mathbb Z/6\Bigr\}.$$
The pair cases are exactly $(\dagger)$; and a singleton case is dominated by a pair case, because
$\bigcup_{q_i=d}E_i\subseteq\bigcup_{q_i\in\{d-1,d\}}E_i$, so $(\dagger)\Rightarrow(\ast)$; the
converse is immediate since $(\dagger)$ is the $d,d+1$ instance of $(\ast)$. $\blacksquare$

**Consistency check.** Applying Theorem 3 to all $6^6=46656$ grid data gives exactly $36=6\times6$
survivors (six rotation orbits of six), and imposing $q_0=0$ gives exactly the six AC-CONE-SIX
survivors
$$(0,0,2,2,4,4),\ (0,0,4,4,2,2),\ (0,1,2,3,4,5),\ (0,2,2,4,4,0),\ (0,4,4,2,2,0),\ (0,5,4,3,2,1).$$
The script recomputes this from scratch.

---

## 7. Theorem 6 (sharp threshold: the $\pi/3$ bound has a factor-2 margin)

For $\theta\in(0,\pi)$ let $\mathrm{CC60^{arc}_\theta}$ be $(\ast)$ with $w$ replaced by $\theta$, and
$\mathcal V_\theta$ its solution set.

> **Theorem 6.** $\mathcal V_\theta\ne\varnothing \iff \theta<\tfrac{2\pi}3$.

*Proof.* ($\Leftarrow$) Three double clusters: for $0<\varepsilon<\tfrac{2\pi}3-\theta$ put
$$v=\Bigl(0,\ \varepsilon,\ \tfrac{2\pi}3,\ \tfrac{2\pi}3+\varepsilon,\ \tfrac{4\pi}3,\ \tfrac{4\pi}3+\varepsilon\Bigr).$$
The constrained pairs are exactly those whose slots lie in different clusters (within a cluster the
slot pairs are consecutive), so every constrained distance is either exactly $\tfrac{2\pi}3$ (the
pairs at slot distance $2$) or one of $\tfrac{2\pi}3\pm\varepsilon$ (pairs at slot distance $3$), and
all of these are $>\theta$.
($\Rightarrow$) Suppose $\theta\ge\tfrac{2\pi}3$ and all nine constrained distances are $>\theta$. In
particular the triangle $\{0,2,4\}$ is pairwise farther than $\theta$. Three points of $T$ cut $T$
into three closed arcs of lengths $g_1,g_2,g_3\ge0$ with $g_1+g_2+g_3=2\pi$, and the distance between
the pair bounding the $k$-th arc is $\min(g_k,2\pi-g_k)$. Each is $>\theta$, hence $g_k>\theta$ for
each $k$, hence $2\pi=\sum_kg_k>3\theta\ge2\pi$ — contradiction. $\blacksquare$

So the closed sixty-degree cone is **safe by a factor of two**: the six-interface system survives any
cone width up to (but not including) $120^\circ$. At $\theta=2\pi/3$ the only limits of solutions are
the three antipodal clusters $\{0,2\pi/3,4\pi/3\}$ doubled, with cluster diameter $\to0$; they are not
solutions, the inequalities being strict. Consequently no strengthening of CC60 of the form "widen
the cone to $\theta$" can hold for $\theta\ge2\pi/3$, and — importantly for the adversarial
direction — *no direction configuration spread out over up to $120^\circ$ can be excluded by the
arc condition alone*.

---

## 8. Theorem 7 (sharp equality at $\pi/3$: maximal confinement forces the alternating grid)

> **Theorem 7.** Let $v\in\mathcal V$ and suppose in addition that every *consecutive* pair is
> confined: $\operatorname{dist}(v_i,v_{i+1})\le\pi/3$ for all $i\in\mathbb Z/6$. Then
> $$v_i=t+i\tfrac{\pi}3\quad\forall i,\qquad\text{or}\qquad v_i=t-i\tfrac{\pi}3\quad\forall i$$
> for some $t\in T$. Both alternatives do lie in $\mathcal V$.

*Proof.* For each $i$ choose $s_i\in[-\pi/3,\pi/3]$ with $v_{i+1}=v_i+s_i$ on $T$ (possible by
confinement; when $\operatorname{dist}=\pi/3$ either sign may be chosen). Extend $s$ periodically,
$s_{i+6}=s_i$, and lift: $u_0=0$, $u_{i+1}=u_i+s_i$, so $u_i=\sum_{j<i}s_j$ and $v_i\equiv u_i$
mod $2\pi$; then $u_{i+6}-u_i=\sum_{j=0}^{5}s_j=:2\pi m$ with $m\in\mathbb Z$ and
$|2\pi m|\le 6\cdot\tfrac{\pi}3=2\pi$, so $m\in\{-1,0,1\}$.
For a slot pair at distance $2$, say $\{i,i+2\}$ (indices taken in $\mathbb Z$ with the periodic
extension), the circular distance is
$$\min_{k\in\mathbb Z}|u_{i+2}-u_i-2\pi k|=\min_k|s_i+s_{i+1}-2\pi k|=|s_i+s_{i+1}|,$$
the last equality because $|s_i+s_{i+1}|\le\tfrac{2\pi}3<\pi$. So $\mathcal V$ gives
$$\sigma_i:=s_i+s_{i+1}>\tfrac{\pi}3\qquad\text{for all } i.\tag{7.1}$$
*Step 1 (adjacent sums never change sign).* If $\sigma_i>\tfrac{\pi}3$ and
$\sigma_{i+1}<-\tfrac{\pi}3$ then $s_i>\tfrac{\pi}3-s_{i+1}$ and
$s_{i+2}<-\tfrac{\pi}3-s_{i+1}$. If $s_{i+1}\ge0$ then
$s_{i+2}<-\tfrac{\pi}3-s_{i+1}\le-\tfrac{\pi}3$, contradicting $s_{i+2}\ge-\tfrac{\pi}3$. If
$s_{i+1}<0$ then $s_i>\tfrac{\pi}3-s_{i+1}>\tfrac{\pi}3$, contradicting $s_i\le\tfrac{\pi}3$. By
connectedness of the 6-cycle all $\sigma_i$ thus have one sign; say all $>\tfrac{\pi}3$ (otherwise
negate everything).
*Step 2 (all steps the same sign).* From $s_i>\tfrac{\pi}3-s_{i+1}\ge\tfrac{\pi}3-\tfrac{\pi}3=0$ we
get $s_i>0$ for every $i$.
*Step 3 (rigidity).* Then $0<\sum_is_i\le2\pi$, so $m=1$ and $\sum_i s_i=2\pi$; with each
$s_i\le\tfrac{\pi}3$ this forces $s_i=\tfrac{\pi}3$ for all $i$. In the negated case likewise
$s_i=-\tfrac{\pi}3$ for all $i$. $\blacksquare$
(The two alternatives have constrained distances $2\pi/3$ and $\pi$, so they do satisfy $\mathcal V$;
the script checks both orientations at several rotations.)

**Corollary 7'.** For $v\in\mathcal V$, the six consecutive distances are never *all* $<\pi/3$:
otherwise $|s_i|<\pi/3$ and Steps 1–2 still give all $s_i$ of one sign, so
$\sum_is_i\ne0$ while the winding needs $\sum_i s_i=2\pi m$ with $|\sum_is_i|<2\pi$, i.e. $m=0$.
Hence the *unique* way all six chain links saturate the cone is the alternating grid.

**Consequence: the grid is a rigid, measure-zero, maximally-confined circumstance.** Theorem 7 is
exactly the extra hypothesis under which the AC-CONE-SIX grid is forced; without it the survivor set
is the open $\mathcal V$ of §5. It also explains the orbit split of AC-CONE-SIX §2 structurally:
* *orbit A* $\{(0,0,2,2,4,4),\dots\}$ — consecutive distances $(0,\tfrac{2\pi}3,0,\tfrac{2\pi}3,0,\tfrac{2\pi}3)$,
  i.e. three double clusters — is the **corner of the 4-parameter family** of §5(iii);
* *orbit B* $\{(0,1,2,3,4,5),(0,5,4,3,2,1)\}$ — all consecutive distances exactly $\pi/3$ — is
  **rigid**: its only continuous freedom is the global rotation $t$. So the two orbits that survive
  the cone filter are precisely "the flexible cluster stratum" and "the rigid confined chain".

---

## 9. What is and is not claimed

**Claimed and proved here.**
1. Theorem 3: the exact solution set $\mathcal V$ of the closed-arc CC60 condition for the six cyclic
   interfaces is nine strict pairwise constraints (prism edges), with Lemma 1 as the combinatorial
   core and Proposition 2 as the general (arbitrary-label) form.
2. Corollary 3: complete treatment of equal directions, antipodal pairs, distance exactly $\pi/3$,
   closed endpoints, arcs containing several directions ($\le2$ directions per closed $\pi/3$-arc,
   equality = consecutive pair), and monotone variants.
3. §5: $\mathcal V$ is open and full-dimensional, so the survivor set is **not** a finite union of
   grid-like strata; explicit exact non-grid certificates ($v^\star$ with a $19^\circ$ sup-norm box;
   the 4-parameter family through grid A). This answers (ii): no excluded arc is forced by the
   interface combinatorics.
4. Theorem 6: the exact width threshold $2\pi/3$ (only strictly below it are there solutions).
5. Theorem 7 and Corollary 7': the exact rigid configuration at cone width $\pi/3$ — maximal
   confinement forces the alternating grid, and nothing weaker does.

**Not claimed.** No statement about the plane, about colourings, or about any chromatic number. No
claim that the source's geometric hypotheses really deliver $(\ast)$ for every cone position, nor
that they deliver the confinement hypothesis of Theorem 7 — those are hypotheses about the
source's exclusion lemmas, not combinatorial consequences (this is the adversarial member's
direction). Not claimed: connectedness of $\mathcal V$; and of the 64 "close-pattern" cells
$W_K=\{v:\operatorname{dist}<w \text{ on } K\subseteq C_6,\ \operatorname{dist}>w \text{ otherwise}\}$
only two are settled here — $W_\varnothing=\varnothing$ (six pairwise-far points would cut $T$ into six
gaps each $>w$, whose sum must be $2\pi=6w$ while it is $>6w$ — impossible) and $W_{C_6}=\varnothing$ (Corollary 7'), while
$W_{\{(0,1),(2,3),(4,5)\}}$ is a nonempty 6-dimensional open cell (grid A is interior to it, by §5(iii)). Deciding
which of the remaining cells are nonempty is a finite exact problem, not needed for the statements
above.

---

## 10. Reproduction

```
cd .ultramath/smwgphe8q/m1 && python3 cone_arc.py
```
Exact arithmetic only (`fractions.Fraction`; angles are rational multiples of $\pi$; distances are
rationals in $[0,\pi]$). Output ends with `ALL 105635 CHECKS PASSED` (≈5 s, one process, one thread).
Sections of the script: [1] Lemma 1 over all 64 subsets; [2] Theorem 3 against a *direct*
arc-enumeration implementation on 46875 exhaustive rational 6-tuples plus 4000 random ones plus seven
degenerate cases with independently known verdicts; [3] independent brute-force re-validation of every
witness arc; [4] the $6^6$ grid and the six AC-CONE-SIX survivors; [5] the $v^\star$ certificate with
all nine distances, the slack, and all 64 box corners; [6] the 4-parameter family and its
$5\pi/12$ bound; [7] the width threshold; [8] the rigidity steps of Theorem 7.
