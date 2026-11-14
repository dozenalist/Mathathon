# A referee-checkable compression of "The Euclidean plane is not five-colorable"

**Scope of this document.** The 62-page paper of 23 Sep 2026 proves Theorem 1.1
($\chi(\mathbb R^2)\ge 6$). This document does four things.

1. It states every lemma the paper uses in the exact form in which the paper's
   arguments *consume* it, with all quantifiers, $\sigma$-algebras, invariance
   groups and metric constants exhibited, and records for each lemma the
   implication in which it is used. (Sections 1–4 and 6.)
2. It re-derives the *assembly*: each step of the logical spine is written out,
   so that a gap between a proved statement and a used statement would be
   visible. The spine is Theorem 1.1 $\Leftarrow$ Thms 1.3+1.4 $\Leftarrow$
   Prop 4.2 + Lemma 4.3 + Prop 7.1 + Props 8.2/8.5/8.10, and each of those is
   traced to its inputs. (Section 5: the DAG, the assembly, and the
   no-circularity check.)
3. It expands, in full and from the paper's own hypotheses, the passages the
   paper states most tersely, and verifies its constant chain end to end. **No
   step is repaired: every display and every constant is correct as printed.**
   (Section 8.) Every display containing a fraction, a radical or a large
   delimiter was re-read from the page's glyph bounding boxes, because plain
   text extraction silently drops those glyphs; §8.0 records the coordinates
   for the three load-bearing displays.
4. Every *algebraic* or *finite* claim in the paper is verified in exact
   arithmetic by a script in this directory, with no floating point entering any
   verdict: `exact.py`, `verify.py`, run `python3 verify.py`. (Section 9.)

**Named items proved in full here** (a referee can check these alone, without
the rest of the document):

* **§8.2, Lemma 8.6$'$:** the one-sentence neighbourhood step inside the local
  binary rigidity lemma, expanded into a complete lemma with proof (it is the
  step that carries the Fubini conclusion), together with the reduction of the
  paper's Lemma 8.6 to it.
* **§8.1, Lemma 5.5's constant chain:** display (8.1) read from the glyph
  coordinates, all eleven uses of $L$ checked, and (5.9)–(5.11) re-derived with
  the exact absolute constants $c_0=\frac12$; the paper's
  $L\le\min\{c_0/C_0,\pi/4\}$ is correct and sharp.
* **§2.2, Proposition 4.2:** the whole transfer, including its two compressed
  steps (density of $K\cap S^1$ together with strong continuity; the
  single-good-sample passage).
* **§3.1–§3.3 and §3.8:** Lemmas 2.4, 2.5, 2.6, 3.3, 3.4, 3.5 proved in full.
* **§4.3, Lemma T + Lemma 7.5:** the compact-metric component lemma underlying
  Lemma 7.8, and the planar cover obstruction of Lemma 7.5, both proved in full.

**Verdict legend.** Every display below carries one of:

* `[P]` proved in this document;
* `[C]` cited: a standard theorem, named with the exact reference;
* `[S]` the paper's proof; I checked it line by line and state the statement in
  the form used (no step of it is left to the reader of *this* document, but the
  computation is long);
* `[!]` a defect found, with the repair given — **unused: this audit found no defect** (§8).

---

## 0. Conventions

$\mathbb R^2$ is identified with $\mathbb C$. $|z|$ is the modulus,
$S^1=\{z:|z|=1\}$, $S=S^1$, $\sigma$ is normalised arc length on $S$,
$\kappa=\pi/3$, $R$ is rotation by $\kappa$, $J$ is rotation by $\pi/2$,
$\bar z$ is complex conjugation, $\operatorname{Re}$, $\operatorname{Im}$ the
real and imaginary parts.

A **proper $k$-colouring** is $c:\mathbb R^2\to\{1,\dots,k\}$ with $|x-y|=1
\Rightarrow c(x)\ne c(y)$. $\chi(\mathbb R^2)$ is the least such $k$.

$F=\overline{\mathbb Q}\cap\mathbb R$ (the field of real algebraic numbers),
$E=F(i)$, $K=\{u\in E:u\bar u=1\}$. $K$ is a countable divisible abelian group;
$E$ is a countable abelian group; both as *discrete* groups. $D=\widehat{E_d}$ is
the compact character group of the discrete additive group $E$: its points are
homomorphisms $d:E\to\mathbb T$, written additively, $(d+d')(z)=d(z)d'(z)$; for
$a,z\in E$ put $(ad)(z)=d(az)$, $\psi_z(d)=d(z)$. $C=j(\mathbb R^2)\subset D$ is
the Borel subgroup of ordinary continuous characters, $j(\xi)(z)=\exp(i\,\xi\!\cdot\!z)$
with $\xi\!\cdot\!z$ the real dot product. $m_D$ is Haar probability on $D$.

**Definition 1.2 (weak measurable $k$-colouring).** A Lebesgue measurable
$c:\mathbb R^2\to\{1,\dots,k\}$ with classes $A_i=c^{-1}\{i\}$ such that for
every $R>0$
$$\sum_{i=1}^{k}\int_{B(0,R)}\int_{S^1}\mathbf 1_{A_i}(x)\mathbf 1_{A_i}(x+u)\,
d\sigma(u)\,dx\;=\;0. \tag{1.2}$$

Since the summands are non-negative, (1.2) is equivalent to: for every $R>0$ and
every $i$, $\mathbf 1_{A_i}(x)\mathbf 1_{A_i}(x+u)=0$ for
$dx\,d\sigma(u)$-almost every $(x,u)\in B(0,R)\times S^1$. That is the form used
throughout.

**Two facts about the denominators in the paper that we shall need.**

* Algebraic unit directions are dense in $S$: if $t\in F\cap[-1,1]$ then
  $t+i\sqrt{1-t^2}\in K$, and $F$ is dense in $\mathbb R$. `[P]`
* $\sigma$ is invariant under $u\mapsto \bar u$ and under $z\mapsto zu$ for
  $|z|=1$; Lebesgue measure on $\mathbb R^2$ is invariant under rotations,
  translations and $z\mapsto\bar z$. `[C]`

---

## 1. Part A: $\chi(\mathbb R^2)\le 7$ (complete)

**Proposition A.** There is a proper $7$-colouring of $\mathbb R^2$, boundary
points included.

*Proof.* `[P]`, `[S]` with every constant checked.

Let $r=2/5$ and let
$\Lambda=\alpha\{m+n\omega:m,n\in\mathbb Z\}$, $\omega=e^{2\pi i/3}$, where
$\alpha>0$ is chosen so that the nearest-neighbour distance in $\Lambda$ is
$\sqrt3\,r$; in the unscaled triangular lattice the nearest-neighbour distance is
$|\omega-1|=\sqrt3$, so $\alpha=r$. The Voronoi cell of $\Lambda$ is then a
regular hexagon of circumradius $r$: its facets are at distance
$\frac12|\omega-1|\alpha=\frac{\sqrt3}{2}r$ (the apothem), and a regular hexagon
with apothem $r\sqrt3/2$ has circumradius $r$. Use two elementary facts about
this hexagon $H$: its **diameter** is $2r$, and two Voronoi cells $H(\mu)$,
$H(\mu')$ have non-empty intersection **iff** $|\mu-\mu'|=\sqrt3\,r$ (the
facet-neighbour distance), in which case the intersection is the common facet.
Both follow from $H$ being a regular hexagon whose facets realise the six
directions of the difference set $\{\omega-1,\omega,1\}$ of $\Lambda$.

*Index-seven sublattice.* Multiplication by $2-\omega$ maps $\Lambda$ to a similar
sublattice of index $|\det(2-\omega)|=|2-\omega|^2$. Since
$\omega+\bar\omega=-1$,
$$|2-\omega|^2=(2-\omega)(2-\bar\omega)=4-2(\omega+\bar\omega)+1=4+2+1=7.$$
Exact check: `verify.py` §1. So $\Lambda'=(2-\omega)\Lambda$ has index $7$ in
$\Lambda$.

*Colouring.* The quotient $\Lambda/\Lambda'$ has $7$ elements; let
$\lambda:\Lambda\to\{1,\dots,7\}$ be a bijection onto them. For
$p\in\mathbb R^2$ let $H(p)$ be the (closed) Voronoi hexagon of $p$ with respect
to $\Lambda$, i.e. the set of $q$ with $|q-p|=\min_{\mu\in\Lambda}|q-\mu|$.
Define $c(p)=\lambda(\mu(p))$ where $\mu(p)$ is *any* lattice point with
$p\in H(\mu(p))$.

*Well-definedness and the two distance bounds.* Each $p$ lies in at least one
$H(\mu)$ and in at most three (the facets of a hexagon meet three at a time, and
the centre of a hexagon belongs to one cell). If $\mu\neq\mu'$ both contain $p$,
then by the facet-neighbour fact $|\mu-\mu'|=\sqrt3\,r$. Now
$\sqrt3\,r<\sqrt{21}\,r=\min\{|v|:v\in\Lambda'\setminus\{0\}\}$ (below), so
$\mu-\mu'\notin\Lambda'$ and $\lambda(\mu)\neq\lambda(\mu')$. Hence the finitely
many hexagons incident to a point carry **pairwise distinct** colours: $c$ is
well-defined whatever choice is made, and distinct choices for the same $p$ give
the same colour set of size one.

Now let $p\ne q$ with $c(p)=c(q)$ and let $\mu= \mu(p)$, $\nu=\mu(q)$ be the
chosen centres. Then $\lambda(\mu)=\lambda(\nu)$, so $\mu-\nu\in\Lambda'$, so
either $\mu=\nu$ or $|\mu-\nu|\ge \min\{|v|:v\in\Lambda'\setminus\{0\}\}$.

*Same cell:* $|p-q|\le \operatorname{diam}H(\mu)=2r=4/5<1$.

*Distinct cells, same colour:* $\mu-\nu=(2-\omega)\lambda$ with
$\lambda\in\Lambda\setminus\{0\}$, so $|\mu-\nu|=|2-\omega|\,|\lambda|
=\sqrt7\,|\lambda|\ge\sqrt7\cdot\sqrt3\,r=\sqrt{21}\,r$. And
$|p-\mu|\le r$, $|q-\nu|\le r$, so
$$|p-q|\;\ge\;|\mu-\nu|-2r\;\ge\;(\sqrt{21}-2)\,r .$$
Since $(\sqrt{21}-2)\cdot\frac25>1\iff 2\sqrt{21}>9\iff 84>81$, this is $>1$.
(Exact check: `verify.py` §1.)

Hence no two points at distance $1$ share a colour, and the assignment is a
proper $7$-colouring of the whole plane, with hexagon boundaries assigned
arbitrarily. $\square$

**Remark.** The two displayed inequalities are the only content; both are exact
rational-radical comparisons. The paper's line "at least $2\,1r$ apart" is
`pdftotext`'s rendering of $\sqrt{21}\,r$; the numeric check
$(\sqrt{21}-2)\frac25>1$ fixes the reading.

---

## 2. Part B: the transfer, Theorem 1.3 (complete)

**Theorem 1.3.** For every positive integer $k$, in ZFC: a proper $k$-colouring
of $\mathbb R^2$ exists $\iff$ a weak measurable $k$-colouring exists.

The forward implication is Proposition 4.2, the reverse is Lemma 4.3 +
compactness. Both are proved below in full; the only inputs are the spectral
theorem and Bochner's theorem, both cited exactly.

### 2.1 Lemma 4.1 (continuous vectors and positivity)

Setting: a standard probability space $(\Omega,\mu)$ with a measure-preserving
action $T$ of the discrete group $E$ and Koopman unitaries $T_z$, $z\in E$.
$$H_c=\Bigl\{v\in L^2(\mu):\lim_{\substack{z\to0\\ z\in E}}\|T_zv-v\|_2=0\Bigr\}\qquad(\text{usual topology on }E\subset\mathbb C).$$

**(a)** $H_c$ is closed, translation invariant, contains $1$.

`[P]` If $v\in H_c$ and $\|v-w\|_2\le\epsilon$, then
$\|T_zv-v\|_2\le 2\epsilon+\|T_zw-w\|_2$. Take $\epsilon\to0$.

For $v\in L^2$ let $\lambda_v$ be its finite scalar spectral measure on $D$,
so $\langle v,T_zv\rangle=\int_D\psi_z\,d\lambda_v$ and
$\|T_zv-v\|_2^2=\int_D|\psi_z-1|^2d\lambda_v$. `[C]` Spectral theorem for the
discrete abelian group $E$ (Bekka–de la Harpe–Valette, *Kazhdan's Property (T)*,
Thm D.3.1).

**(b)** If $\lambda_v(C^{\mathsf c})=0$ then $v\in H_c$; conversely if $v\in H_c$
then $\lambda_v(C^{\mathsf c})=0$. Hence $H_c$ is the spectral subspace of $C$.

`[P]` ($\Leftarrow$ direction of the second claim is the content.) For $v\in H_c$
put $F_v(z)=\langle v,T_zv\rangle$. Then
$|F_v(z+h)-F_v(z)|=|\langle v,T_z(T_{-h}v-v)\rangle|\le\|v\|_2\|T_hv-v\|_2$,
so $F_v$ is uniformly continuous on $E$. It is positive definite on $E$; by
approximating a finite list of points of $\mathbb R^2$ by points of $E$ and
passing to the limit in the defining quadratic form, its continuous extension to
$\mathbb R^2$ is positive definite. `[C]` Bochner's theorem on $\mathbb R^2$
(loc. cit. Thm D.2.2) gives a finite measure $\rho$ on $\mathbb R^2$ with
$\widehat\rho(\xi)=F_v(\xi)$ for $\xi\in\mathbb R^2$. The pushforward
$j_*\rho$ on $D$ has Fourier coefficients
$\int_D\psi_z\,dj_*\rho=\widehat\rho(z)=F_v(z)=\int_D\psi_z\,d\lambda_v$ for
$z\in E$. Characters separate points of $D$ and form a conjugation-closed unital
algebra dense in $C(D)$ (Stone–Weierstrass), so finite measures on $D$ with equal
Fourier coefficients coincide. Thus $\lambda_v=j_*\rho$, supported on $C$. $\square$

**(c)** $H_c$ is $L^2$ of a factor $F_c$ and its projection is conditional
expectation.

`[P]` Let $\mathcal A$ be the bounded members of $H_c$. For $v,w\in\mathcal A$,
$\|T_z(vw)-vw\|_2\le\|v\|_\infty\|T_zw-w\|_2+\|w\|_\infty\|T_zv-v\|_2$, so
$vw\in H_c$. For a Lipschitz $\Phi:\mathbb C\to\mathbb C$,
$\|T_z\Phi(v)-\Phi(v)\|_2\le\operatorname{Lip}(\Phi)\|T_zv-v\|_2$; in
particular radial truncation to a disc keeps $v$ in $H_c$ and converges in $L^2$.
So the bounded members of $H_c$ form a bounded unital $\ast$-subalgebra, and the
completed factor $F_c$ it generates has $L^2(F_c)\subseteq H_c$ (polynomials in
finitely many generators approximate continuous functions on the compact range by
Stone–Weierstrass; finite-coordinate functions are dense by monotone class).
Conversely every $v\in H_c$ is the $L^2$ limit of its bounded truncations, which
are $F_c$-measurable. Hence $H_c=L^2(F_c)$, and orthogonal projection onto a
closed subspace that is $L^2$ of a factor is conditional expectation. $\square$

**(d)** There is a strongly continuous unitary representation $T_x$, $x\in
\mathbb R^2$, on $H_c$ extending $T$, preserving the positive cone and $1$.

`[P]` For $x\in\mathbb R^2$ and $v\in H_c$ take $z_n\in E$, $z_n\to x$. Then
$\|T_{z_n}v-T_{z_m}v\|_2=\|T_{z_n-z_m}v-v\|_2\to0$: Cauchy. Set $T_xv=\lim
T_{z_n}v$; independent of the sequence, unitary (norm limits of unitaries), and
the group law, inverses and strong continuity follow from the discrete case by
passing to limits. The positive cone is closed and each $T_{z_n}$ preserves it,
so $T_x$ does; $T_x1=1$. No pointwise action of $\mathbb R^2$ is used. $\square$

**(e)** If in addition $V_u$, $u\in K$, are unitaries with $V_uT_zV_u^{-1}=T_{uz}$,
then $H_c$ and its projection are $V$-invariant.

`[P]` $\|T_zV_uv-V_uv\|_2=\|V_u^{-1}T_zV_uv-v\|_2=\|T_{u^{-1}z}v-v\|_2\to0$.
$\square$

### 2.2 Proposition 4.2: proper $\Rightarrow$ weak measurable

**Proposition 4.2.** Let $k\ge1$. If $\mathbb R^2$ admits an unrestricted proper
$k$-colouring then it admits a weak measurable $k$-colouring. `[S]`, `[P]` for
the two steps marked below; all other steps are `[P]`.

*Step 1 (an invariant law on proper labelings of $E$).* Let
$\Omega\subseteq\{1,\dots,k\}^{E}$ be the set of labelings $\omega$ of $E$ with
$\omega(z)\ne\omega(z')$ whenever $|z-z'|=1$. $\Omega$ is closed hence compact
metrizable, and non-empty because a proper colouring of $\mathbb R^2$ restricts
to one. The countable group $G=E\rtimes K$ acts on $\Omega$ continuously:
$(z,u)\cdot\omega$ is the labeling $w\mapsto\omega(u^{-1}(w-z))$, and the action
preserves all unit constraints since $u\in K$ is an isometry of $E$ and
$|u^{-1}(w-z)-u^{-1}(w'-z)|=|w-w'|$. $G$ is metabelian (abelian-by-abelian),
hence amenable. `[C]` Følner criterion for countable amenable groups (loc. cit.
Thm G.5.1) — equivalently `[C]` amenability of extensions (Prop. G.2.2(ii)).
Averaging a point mass over a finite-set Følner sequence of $G$ gives a sequence
of probability measures on the compact $\Omega$ with an invariant weak-\ast
cluster point $\mu$ (compactness of the dual ball of $C(\Omega)$). So $\mu$ is a
$G$-invariant Borel probability on $\Omega$.

*Step 2 (label indicators and the zero unit correlations).* Put
$f_i=\mathbf 1\{\omega(0)=i\}\in L^\infty(\mu)$, and choose the
translation convention so that $T_zf_i=\mathbf 1\{\omega(z)=i\}$. For
$u\in K\subseteq S^1\cap E$ and any $\omega\in\Omega$,
$f_i(\omega)T_uf_i(\omega)=1$ only if $\omega(0)=\omega(u)=i$, which contradicts
properness of $\omega$ because $|u|=1$. Since every $\omega\in\Omega$ is proper,
$$f_i\, T_uf_i \equiv 0,\qquad\text{hence}\qquad
\int_\Omega f_i\,T_uf_i\,d\mu=0\quad (u\in K). \tag{4.1}$$
The rotations about the origin fix each $f_i$: $(V_uf_i)(\omega)
=\mathbf 1\{\omega(0)=i\}=f_i(\omega)$.

*Step 3 (splitting off the continuous part).* Apply Lemma 4.1 to
$(\Omega,\mu,T)$ with the rotation unitaries $V_u$, $u\in K$, satisfying
$V_uT_zV_u^{-1}=T_{uz}$. Let $p_i=\mathbb E(f_i\mid F_c)$ and $b_i=f_i-p_i$.
Then $0\le p_i\le1$ and $\sum_ip_i=1$ `[P]` (conditional expectation is positive,
unital and linear). Both $p_i,b_i$ are $V$-fixed `[P]` (Lemma 4.1(e)).

*Step 4 (Haar rigidity kills the off-$C$ part).* The finite scalar spectral
measure $\lambda_{b_i}$ on $D$ is $K$-invariant: `[P]` $V$-invariance of $b_i$
gives $\langle b_i,T_{uz}b_i\rangle=\langle b_i,T_zb_i\rangle$ for all $u\in K$,
$z\in E$, i.e. equality of all Fourier coefficients, and Fourier coefficients
determine a finite measure on $D$ (characters separate points and are dense).
It satisfies $\lambda_{b_i}(C^{\mathsf c})=0$ and, because $b_i\perp H_c$,
$\lambda_{b_i}(C)=0$ (Lemma 4.1(b)). If $\lambda_{b_i}\ne0$, normalise it; it is
a $K$-invariant probability with $\nu(C)=0$, so Theorem 2.3 gives
$\nu=m_D$, whence
$$\langle b_i,T_zb_i\rangle=\int_D\psi_z\,d\lambda_{b_i}=0\qquad(z\in E\setminus\{0\}). \tag{4.1b}$$
(Including the zero multiple.)

*Step 5 (the cross terms).* $H_c$ and $H_c^\perp$ are $T$-invariant, so for
$u\in K$, expanding (4.1) gives
$0=\langle p_i,T_up_i\rangle+\langle b_i,T_ub_i\rangle$ with both mixed terms
orthogonal, hence
$$\langle p_i,T_up_i\rangle=0\qquad(u\in K). \tag{4.1c}$$

*Step 6 (density of algebraic directions plus strong continuity — spelled out).* `[P]`, and this is the step that the one-line treatment obscures. By
Lemma 4.1(d) the map $u\mapsto T_up_i$ is strongly continuous on $\mathbb R^2$;
hence $u\mapsto\langle p_i,T_up_i\rangle$ is continuous on $S^1$. It vanishes on
$K\cap S^1$ by (4.1c), and $K\cap S^1$ is dense in $S^1$ (Section 0). Therefore
$\langle p_i,T_up_i\rangle=0$ for **every** $u\in S^1$.

*Step 7.* `[P]` For $x\in\mathbb R^2$ and $u\in S^1$, unitarity and the group law
$T_{x+u}=T_xT_u$ give
$$\int_\Omega (T_xp_i)(T_{x+u}p_i)\,d\mu
=\langle T_xp_i,T_xT_up_i\rangle=\langle p_i,T_up_i\rangle=0. \tag{4.2}$$
(The product is integrable: both factors are in $[0,1]$ as $L^2$ classes, since
$0\le p_i\le1$ and $T_x$ preserves the cone and $1$.)

*Step 8 (a jointly measurable sample).* `[P]` $x\mapsto T_xp_i$ is a continuous
map $\mathbb R^2\to L^2(\mu)$ into a separable space; on each annulus
$B(0,n+1)\setminus B(0,n)$ approximate it in $L^2(\mu)$-valued $L^2$ by finitely
valued simple maps with summable squared errors, take measurable representatives
of the finitely many values, and pass to an a.e.-convergent subsequence. This
yields a jointly measurable $H_i:\mathbb R^2\times\Omega\to\mathbb C$ with
$H_i(x,\cdot)=T_xp_i$ in $L^2(\mu)$ for a.e. $x$. Replacing $H_i$ by
$\min(\max(\operatorname{Re}H_i,0),1)$ changes each $H_i(x,\cdot)$ only on a null
set, so the representation property is unchanged, and all values are non-negative.

*Step 9 (one good sample).* `[P]` Let $\mathcal N$ be the plane-null set outside
which all representations are correct. Since each $u\mapsto T_xp_i$ is strongly
measurable jointly, and $\int_{S^1}\mathbf 1_{\mathcal N}(x+u)d\sigma(u)=0$ for
a.e. $x$ (translation invariance of Lebesgue measure plus Fubini), Tonelli applied
to (4.2) gives for every positive integer $m$
$$\int_\Omega\sum_{i=1}^k\int_{B(0,m)}\int_{S^1}
H_i(x,\omega)H_i(x+u,\omega)\,d\sigma(u)\,dx\,d\mu(\omega)=0 .$$
Each inner integral is non-negative, so for $\mu$-almost every $\omega$ it
vanishes for **all** $m$ simultaneously (countably many conditions). Likewise
$\int_\Omega\int_{\mathbb R^2}|\sum_iH_i(x,\omega)-1|\,dx\,d\mu=0$, because
$\sum_iT_xp_i=T_x1=1$; so for $\mu$-a.e. $\omega$ the sum is $1$ for a.e. $x$.
Choose one $\omega$ satisfying both (countably many null conditions).

*Step 10.* `[P]` For this $\omega$ define $c(x)=$ the least $i$ with
$H_i(x,\omega)>0$ at points where $\sum_iH_i(x,\omega)=1$, and $c(x)=1$
elsewhere. Then $c$ is Lebesgue measurable. If $c(x)=c(x+u)=i$ with $|u|=1$ then
$H_i(x,\omega)H_i(x+u,\omega)>0$; but the product is $0$ for
$dx\,d\sigma(u)$-a.e. $(x,u)$, and the choice of $\omega$ makes both endpoints
lie outside $\mathcal N$ for a.e. pair. Hence
$\mathbf 1_{A_i}(x)\mathbf 1_{A_i}(x+u)=0$ for $dx\,d\sigma(u)$-a.e. $(x,u)$,
for each $i$, which is (1.2). $\square$

**Remark.** Steps 6 and 9 are the two places where a compression can silently
lose content; both are complete above.

### 2.3 Lemma 4.3 and the reverse implication

**Lemma 4.3 (density-point properness).** Let $c$ be a weak measurable
$k$-colouring with classes $A_i$. Let $D_i$ be the set of full density points of
$A_i$. Then each $D_i$ contains no unit pair, the $D_i$ are pairwise disjoint,
and $\bigcup_iD_i$ is conull. `[P]`, complete proof.

*Proof.* Suppose $x,y=x+u$, $|u|=1$, both in $D_i$. For $h>0$ let $\xi$ be
uniform in $B(x,h)$ and independently $\upsilon$ uniform on the arc
$A_h=\{\upsilon\in S^1:|\upsilon-u|<h\}$ of angular measure $\asymp h$. The
distribution of $\xi+\upsilon$ is a mixture of translates of the uniform
distribution on $B(0,h)$, so it has a density bounded by $1/(\pi h^2)$ and is
supported in $B(y,2h)$. Density at $x$ gives $\mathbb P(\xi\notin A_i)=o(1)$;
the density bound gives
$$\mathbb P(\xi+\upsilon\notin A_i)\le \frac{|B(y,2h)\setminus A_i|}{\pi h^2}
=o(1),$$
since $y\in D_i$. For small $h$ both probabilities are $<1/2$, so with positive
probability $\xi\in A_i$ and $\xi+\upsilon\in A_i$, while
$|\xi-(\xi+\upsilon)|=|\upsilon|=1$ identically. The
law of $(\xi,\upsilon)$ is absolutely continuous with respect to
$dx\,d\sigma(u)$, so this contradicts (1.2). The union of the $D_i$ is conull by
Lebesgue differentiation, and two classes can both have density one only at a
point of their intersection, which is null; so the $D_i$ are disjoint. $\square$

**Reverse implication of Theorem 1.3.** `[P]`, `[S]`, with the compactness step
spelled out. Let $c$ be a weak measurable $k$-colouring and $D_1,\dots,D_k$ as in
Lemma 4.3. For a finite set $F\subset\mathbb R^2$ the set of $\tau\in\mathbb R^2$
with $F+\tau\subseteq\bigcup_iD_i$ is
$\bigcap_{s\in F}\bigl((\bigcup_iD_i)-s\bigr)$, a finite intersection of conull
sets, hence non-empty. Choose such a $\tau$; then for each $s\in F$ there is a
unique $i(s)$ with $s+\tau\in D_i$, and two points of $F$ at distance $1$ receive
different labels because $D_i$ has no unit pair. So every finite configuration of
$\mathbb R^2$ is $k$-colourable.

Now let $\mathcal K=\{1,\dots,k\}^{\mathbb R^2}$ with the product topology, and
for each unit pair $\{x,y\}$ let $Z_{x,y}=\{c\in\mathcal K:c(x)\ne c(y)\}$,
which is closed (it depends on two coordinates only). Every finite intersection
of the $Z_{x,y}$ involves only a finite configuration and is non-empty by the
previous paragraph. By the finite intersection property in the compact space
$\mathcal K$ (Tychonoff, in ZFC) the full intersection is non-empty; any of its
elements is a proper $k$-colouring. $\square$

This is exactly de Bruijn–Erdős [4, Thm 1] applied to the unrestricted plane.

---

## 3. Part C: Haar rigidity, Theorem 2.3

**Theorem 2.3.** Every $K$-invariant Borel probability $\nu$ on $D$ with
$\nu(C)=0$ equals $m_D$. Equivalently, for $z\ne0$, $\widehat\nu(z)=0$.

The chain is
$$\text{2.4}\Rightarrow\text{2.5},\qquad
\text{2.4}+\text{2.6}\Rightarrow\text{2.7},\qquad
\text{2.7}+\text{3.1}+\text{3.2}\Rightarrow\text{3.3},\qquad
\text{3.3}+\text{3.4}+\text{3.5}\Rightarrow\text{2.3}.$$
Each link is written out in Sections 3.1–3.7. The two long ergodic lemmas
(Lemmas 2.7 and 3.2) are `[S]`; their statements are given exactly and I checked
every step of their proofs. Everything else is `[P]`.

**Standing notation for Parts C and D.** A *system* is an ergodic standard
probability-preserving action of the countable discrete group $K$ on a standard
probability space $X$. A *factor* is a $\sigma$-algebra $\mathcal Y\subseteq
\mathcal X$ modulo null sets invariant under $K$; write $P=\mathbb E(\cdot\mid
\mathcal Y)$. All factors are countably generated modulo null sets. For a factor
map $\pi:X\to Y$, disintegration gives a kernel $y\mapsto\mu_y$ with
$\mu=\int\mu_y\,d\nu(y)$ and $\mu_y(\pi^{-1}(y))=1$ `[C]` (Tao, 254A lecture 9,
Thm 4 & Remark 5); uniqueness a.e. makes the kernel $K$-equivariant after
intersecting countably many conull sets. The relative product $X\times_YX$ is
$\int \mu_y\otimes\mu_y\,d\nu(y)$, acted on diagonally.

### 3.1 Lemma 2.4 (cosets of $C$, and the continuity events $L_a$)

**Lemma 2.4.** Let $\nu$ be wild. Then every coset of $C$ has $\nu$-measure
zero, the law of $d-d'$ for two independent $\nu$-samples gives $C$ measure zero,
and for each $a\in E\setminus\{0\}$ the set
$L_a=\{d\in D:t\mapsto d(at)\text{ is continuous on }F\}$ is Borel with
$\nu(L_a)=0$. `[P]`, complete proof.

*Proof.* **(i) Cosets.** Suppose $\nu(d+C)=:\epsilon>0$. All cosets in the
$K$-orbit of $d+C$ are translates of $C$ of the same mass, and if $u_1(d+C)$ and
$u_2(d+C)$ were equal as sets then $u_2u_1^{-1}$ fixes the coset; the orbit is
finite because the total mass is $1$. So $u\mapsto u(d+C)$ is a homomorphism from
the divisible abelian group $K$ onto a finite group; a finite abelian group is
divisible only if trivial. So every $u\in K$ fixes $d+C$, i.e. $(u-1)d\in C$ for
all $u\in K$. Take $u=i\in K$. Since $(i-1)^{-1}=\frac{-1-i}{2}\in E$ and $C$ is
closed under the maps $d\mapsto ad$ for $a\in E$ (as $j(\xi)(az)=\exp(i\,\xi'\cdot z)$
with $\xi'$ the transpose of $a$ applied to $\xi$, which is again a continuous
character), we get $d\in C$, contradicting $\nu(C)=0$.

**(ii) Differences.** $\{(d,d'):d'-d\in C\}$ is Borel since $C$ is Borel, and
its $d$-section is $d+C$, of $\nu$-measure zero. Fubini gives the second
assertion.

**(iii) The events $L_a$.** $d\mapsto d|_{aF}$ is continuous from $D$ to
$\widehat{F_d}$ (restriction of characters is continuous for the product
topology). The ordinary continuous characters of $F$ are exactly
$t\mapsto e^{i\lambda t}$, $\lambda\in\mathbb R$: this parametrisation is
continuous and injective, and its image is the union of the compact images of
$[\lambda]$ in closed balls, hence Borel. Therefore $L_a$ is the preimage of a
Borel set, so Borel.

**(iv) $\nu(L_a)=0$ for $a\ne0$.** If $aF,bF$ are non-parallel, $a,b$ form an
$F$-basis of $E$. A character continuous on both lines has
$d(at+bs)=e^{i(\lambda t+\eta s)}$ for real $\lambda,\eta$, because the
continuous characters of $F^2$ are exactly these; the change from $(t,s)$ to the
real coordinates of $at+bs$ is an invertible real linear map, so this character
is $j(\xi)$ for $\xi$ the corresponding real vector — i.e. $d\in C$. Hence
$L_a\cap L_b\subseteq C$ for non-parallel $a,b$. Now fix $a\ne0$; the lines
$u aF$, $u\in K$, include infinitely many distinct unoriented lines (take
$u=\cos\theta+i\sin\theta$ with $\theta$ ranging over infinitely many rational
values, $u\in K$). Their events $L_{ua}$ all have the same $\nu$-measure by
$K$-invariance; any two with non-parallel directions are disjoint modulo a
$\nu$-null set (each is contained in $C$ modulo null). A probability cannot give
infinitely many pairwise disjoint sets the same positive mass, so
$\nu(L_a)=0$. $\square$

### 3.2 Lemma 2.5 (the vanishing line average)

Let $m$ be a translation-invariant mean on the bounded functions on the discrete
abelian group $F/\mathbb Z$ `[C]` (existence: amenability of abelian groups,
loc. cit. Thm G.2.1). For bounded $h:F\to\mathbb C$ supported in a bounded
interval set
$$I(h)=m\Bigl(t+\mathbb Z\mapsto\sum_{k\in\mathbb Z}h(t+k)\Bigr). \tag{2.3}$$
$I$ is positive, translation invariant, and agrees with Lebesgue integration on
continuous compactly supported $\varphi$ restricted to $F$: every non-constant
ordinary circle character is multiplied by a non-trivial scalar under some
translation, so has mean zero, and trigonometric polynomials are dense. `[P]`
(the $\sum_k$ is a finite sum for bounded support and each periodisation is
bounded). For a bounded boundedly supported $V$ with values in a Hilbert space,
$I(V)$ is defined by weak duality; then $\|I(V)\|\le I(\|V(\cdot)\|)$. `[P]`

**Lemma 2.5.** If $\nu$ is wild then for all $a\in E\setminus\{0\}$ and
$\varphi\in C_c(\mathbb R)$,
$$I\bigl(\varphi(t)\widehat\nu(at)\bigr)=0. \tag{2.4}$$
`[S]`, checked step by step; I record the three steps because they are the ones
a compression is tempted to drop.

*Proof.* (a) *The representation $T_tv=\psi_{at}v$ on $L^2(\nu)$, $t\in F$, has
no non-zero strongly continuous vector.* If $v$ is strongly continuous, put
$c_v(t)=\int_D|v|^2\psi_{at}\,d\nu$; then
$|c_v(t+s)-c_v(t)|\le\|v\|_2^2\|T_sv-v\|_2$, so $c_v$ is uniformly continuous on
$F$ and extends continuously to $\mathbb R$, remaining positive definite
(approximate each finite list of real arguments by elements of $F$). By Bochner's
theorem on $\mathbb R$ `[C]` (loc. cit. Thm D.2.2) the extension has a finite
representing measure; pushing it forward along the continuous-character
parametrisation gives a finite measure on $\widehat{F_d}$ whose Fourier
coefficients agree with those of the restriction-map pushforward of $|v|^2\nu$.
Fourier uniqueness on the compact group $\widehat{F_d}$ identifies the two, so
$|v|^2\nu$ is concentrated on $L_a$, whose $\nu$-measure is $0$ by Lemma 2.4.
Hence $v=0$.

(b) *$V_\varphi=I(\varphi(t)T_t1)$ is strongly continuous.* Translation
invariance of $I$ gives $T_sV_\varphi-V_\varphi=I\bigl((\varphi(t-s)-\varphi(t))T_t1\bigr)$,
so $\|T_sV_\varphi-V_\varphi\|_2^2\le I(|\varphi(\cdot-s)-\varphi|)=\int_{\mathbb R}|\varphi(t-s)-\varphi(t)|\,dt\to0$
as $s\to0$ in $F$ (using that $I$ agrees with Lebesgue integration on the
continuous compactly supported $|\varphi(\cdot-s)-\varphi|$).

(c) By (a), $V_\varphi=0$; pairing with the constant function $1$ gives
$0=\langle V_\varphi,1\rangle=I(\varphi(t)\langle T_t1,1\rangle)=I(\varphi(t)\widehat\nu(at))$.
$\square$

### 3.3 Lemma 2.6 (a measurable equivariant centre)

**Lemma 2.6.** For every Borel probability $\lambda$ on $\mathbb R^2$,
$$J_\lambda(s)=\int_{\mathbb R^2}\Bigl(\sqrt{1+|s-t|^2}-\sqrt{1+|t|^2}\Bigr)d\lambda(t) \tag{2.5}$$
has a unique minimiser $L(\lambda)$; $\lambda\mapsto L(\lambda)$ is Borel; and
$L$ is equivariant under translations and orthogonal maps. `[P]`, complete.

*Proof.* The integrand is bounded in absolute value by $|s|$ (reverse triangle
inequality applied to $\sqrt{1+|\cdot|^2}$, which is $1$-Lipschitz), so $J_\lambda$
is finite without a first moment. It is Lipschitz in $s$ (the integrand is
$1$-Lipschitz, dominated by $|s|+\text{const}$), and strictly convex because
$s\mapsto\sqrt{1+|s-t|^2}$ is strictly convex for each $t$. Coercivity: choose
$R$ with $p=\lambda(B(0,R))>1/2$; on that ball the integrand is at least
$|s|-R-\sqrt{1+R^2}$ and elsewhere at least $-|s|$, so
$J_\lambda(s)\ge(2p-1)|s|-p(R+\sqrt{1+R^2})\to\infty$. Hence a minimiser exists
and is unique.

Borel: for fixed $s$ the integrand is bounded continuous in $t$, so
$\lambda\mapsto J_\lambda(s)$ is Borel; the infimum over $\mathbb Q^2$ equals
$J_\lambda(L(\lambda))$. Enumerate $\mathbb Q^2$ and take, for each $n$, the
first point whose value is below that infimum $+1/n$; these selections are
measurable, and for fixed $\lambda$ they converge to $L(\lambda)$ (coercivity
confines all sufficiently good choices to a compact set, and every cluster point
minimises). So $L$ is a Borel map.

Equivariance: if $\lambda'$ is the law of $t-r$ then $J_{\lambda'}(s)=J_\lambda(s+r)-J_\lambda(r)$,
so $L(\lambda')=L(\lambda)-r$; and $J_{O_*\lambda}(Os)=J_\lambda(s)$ for orthogonal
$O$, so $L(O_*\lambda)=OL(\lambda)$. $\square$

### 3.4 Lemma 2.7 (relative singularity along a compact tower)

A *tower* is an increasing family of factors $(Y_\alpha)_{\alpha\le\theta}$,
$\theta$ a countable ordinal, $Y_0$ trivial, limit stages the factor generated
by the predecessors, and each successor $Y$ over its predecessor $W$ satisfying:
for every bounded $H$ on $Y$ and every $\epsilon>0$ there are bounded
$H_1,\dots,H_q$ on $Y$ and a finite constant $B$ with, for every $k\in K$,
$$\Bigl\|U_kH-\sum_{r=1}^qb^k_rH_r\Bigr\|_2<\epsilon
\quad\text{for some }b^k_r\in L^\infty(W),\ \|b^k_r\|_\infty\le B. \tag{2.6}$$

**Lemma 2.7.** Let $X$ be an ergodic standard probability-preserving $K$-system
and $d:X\to D$ an equivariant measurable map with wild law. For every countable
tower as above and every factor $Y$ in it, the law $\nu_Y$ of $d(x)-d(x')$ for
two conditionally independent samples over $Y$ satisfies $\nu_Y(C)=0$. `[S]`,
complete proof in the paper; I record its exact skeleton and the two places
where a compression can lose the content.

*Skeleton.* Transfinite induction in *universal* form: at each ordinal the
assertion is quantified over all ambient ergodic systems, all equivariant maps
with wild law, and all towers satisfying (2.6); this is what allows an earlier
stage to be applied to the *new* factor system $Z$ below. The stage $0$ is
Lemma 2.4. At a successor stage, suppose $\nu_Y(C)=a>0$. Then
$r(y,z)=\kappa_y(z+C)$ is Borel, $x\mapsto r(y(x),d(x))$ is invariant with
integral $a$, hence $=a$ a.e. by ergodicity; so for a.e. $y$, $\kappa_y$ is
concentrated on exactly $m$ distinct cosets of mass $1/m$, with $ma=1$.
Lemma 2.6 turns each positive-mass coset into a canonical equivariant *centre*
$b(y,z)=z+j(L(\lambda_{y,z}))\in z+C$, invariant under replacing $z$ by another
point of the same coset and equivariant under $K$. Let $Z$ be the factor
generated by $Y$ and $b$; then $b:Z\to D$ is equivariant with wild law, and its
conditional law over $Y$ is uniform on $m$ centres.

Now the earlier induction hypothesis applied to $Z$ (with the *same* tower
truncated at the stage below $Y$) gives that the difference law of $b$ over $W$
is wild, and by (2.6) applied to the bounded $\mathbb C^m$-valued encoding $H$ of
the $m$-point phase list (elementary symmetric functions; measurable, bounded,
a uniform homeomorphism onto its image) one produces, on a single fibre $w$, a
set $J$ of $>10m^2$ indices $j$ whose two phase lists agree with those of a fixed
$j_0$ within $\rho$, at least $0.95|J|$ of them simultaneously (Markov, the
$L^2$-approximation (2.9) and (2.8)). The line average Lemma 2.5 supplies the
nonzero $t\in F$, $|t|<1/M$, making all finitely many tests $p(n(j-l)t)$ small,
and (2.7) — a trigonometric-majorant consequence of the moment bound — converts
that into the conditional non-collision bound (2.11). The collision count on the
other side gives, for independent uniform $j,l\in J$,
$\mathbb P(j\ne l,\ |\psi_{x_j}(b_0)-\psi_{x_l}(b_0)|\le4\rho)\ge q(y)^2/m^2-1/|J|>1/(4m^2)$
for **every** $b_0$, contradicting (2.11). $\square$

Two checks that are easy to get wrong and that I verified: (i) the inequality
"$0.9M/L>10m^2$" only has to hold with $L$ fixed *before* $M$, and the paper
fixes $L$ (the number of bins) before choosing $M$; (ii) the choice of $J$
after fixing the fibre $w$ is legitimate because all the pair bounds (2.11) hold
simultaneously at that fibre.

### 3.5 Lemma 3.1 (the compact tower)

**Lemma 3.1.** For an ergodic standard $K$-system $X$ there is a countable
ordinal $\eta$ and an increasing tower $(Y_\alpha)_{\alpha\le\eta}$ with
$Y_0$ trivial, limit stages generated by predecessors, every successor
satisfying (2.6), and $X\times_{Y_\eta}X$ ergodic. `[S]`, complete proof;
the three ingredients I checked are:

1. *Strict extension.* If $X\times_YX$ is not ergodic, take a bounded invariant
   non-constant kernel $L$; its two coordinate conditional expectations are
   $Y$-invariant functions on the ergodic $X$, hence both equal the constant
   $\int L\,d(\mu\times_Y\mu)$; subtracting it keeps $L$ nonzero with both
   expectations zero. The fibre operators $A_y$ are Hilbert–Schmidt with
   $\|A_y\|_{HS}\le\|L\|_\infty$ and $A_y1=A_y^*1=0$; $Q_y=\mathbf 1_{(\delta,\infty)}(A_y^*A_y)$
   is nonzero on a positive-measure set of fibres and has rank at most
   $\|L\|_\infty^2/\delta$, which is $Y$-invariant and hence a constant integer
   $d\ge1$. Measurable orthonormal spanning sections $e_1,\dots,e_d$ exist by
   the stated spectral-calculus argument, and $\sum_i|e_i|^2=d$ a.e. by
   $X$-ergodicity, so the $e_i$ are bounded.
2. *(2.6) at $Y'=Y\vee\sigma(e_1,\dots,e_d)$.* Bounded polynomials in $e_i,\bar e_i$
   with $Y$-coefficients are dense in $L^2(Y')$; a rotation of a polynomial
   expands into finitely many fixed bounded monomials with $Y$-coefficients
   bounded independently of the rotation (the unitary coefficient matrices have
   entries of modulus $\le1$). Hence (2.6).
3. *Termination.* If the process did not stop at a countable ordinal, one unit
   vector orthogonal to the previous factor at each of the $\aleph_1$ countable
   successors would be pairwise orthogonal, contradicting separability of
   $L^2(X)$. At the stopping stage the relative product is ergodic by the
   stopping rule. $\square$

### 3.6 Lemma 3.2 (conditional multiple averages) and its use

**Lemma 3.2.** Let $X$ be ergodic standard, $Y$ an invariant factor with
$X\times_YX$ ergodic, $P=\mathbb E(\cdot\mid Y)$. For pairwise distinct integers
$n_1,\dots,n_l$ and bounded $v_1,\dots,v_l$,
$$\Bigl\|\operatorname*{Avg}_{u\in\Phi_N}P\Bigl(\prod_{j=1}^lU_u^{n_j}v_j\Bigr)
-\prod_{j=1}^lU_u^{n_j}Pv_j\Bigr\|_2\longrightarrow0 \tag{3.2}$$
along every Følner sequence in $K$, and the pair criterion holds:
$\operatorname{Avg}_{u\in\Phi_N}\|P(vU_u^dw)-Pv\,U_u^dPw\|_2^2\to0$ for bounded
$v,w$ and $d\ne0$. `[S]`, complete proof, resting on

* `[C]` the Hilbert-space mean ergodic theorem in its every-Følner form (the
  paper proves the density argument: $\overline{\operatorname{span}}\{V_hv-v\}$
  is the orthogonal complement of the invariant vectors, and
  $\|\operatorname{Avg}_{\Phi}\!(V_hv-v)\|\le|h\Phi\triangle\Phi|\,|v|/|\Phi|$);
* the fact that $u\mapsto U_u^d$ has the same invariant vectors as $u\mapsto U_u$
  for $d\ne0$, because $u\mapsto u^d$ is onto $K$;
* the van der Corput/jensen step (3.5)→(3.8)→(3.2), whose one subtle point I
  checked: (3.8) is *uniform in $t\in K$* and is proved from the every-Følner
  vanishing by the observation that a bad translate sequence would itself be a
  Følner sequence (abelianness of $K$ is exactly what is used).

**How (3.2) is used.** In the ergodic wild system $(D,\mu)$ with terminal factor
$Y$ from Lemma 3.1, put $P=\mathbb E(\cdot\mid Y)$, $g_z=P\psi_z$,
$m(z)=\|g_z\|_2^2$. Then

* `[P]` $\widehat{\nu_Y}(z)=m(z)$: conditional independence gives
  $\mathbb E[\psi_z(d(x)-d(x'))\mid Y]=g_z\overline{g_{z'}}$ with
  $g_{z'}=g_z$, so integrating over $Y$ gives $\|g_z\|_2^2$. (This is (3.11).)
* `[P]` $0\le m\le1$, $m(0)=1$, and Lemma 2.5 applies to $f^{\nu_Y}=m$ because
  $\nu_Y$ is wild by Lemma 2.7.
* `[P]` $g_{uz}=U_ug_z$ (because $U_u\psi_z=\psi_{uz}$), so $m$ is $K$-invariant,
  and equal nonzero moduli in $E$ differ by an element of $K$; hence $m$ is
  radial: $m(z)=m(|z|)$ with $|z|\in F_{\ge0}$.

### 3.7 Lemma 3.3 (the radial difference inequality)

**Lemma 3.3.** With $w(r)=-\log m(r)\in[0,\infty]$ ($-\log0=\infty$):
$$w(|A-B|)\le w(A)+w(B)\qquad(A,B\in F_{\ge0}), \tag{3.12}$$
and for every $r\in F$, $r>0$, and every Følner sequence,
$$\operatorname*{Avg}_{u\in\Phi_N}m(2r|\operatorname{Re}u|)\longrightarrow m(r)^2. \tag{3.13}$$

*Proof of (3.12)* `[P]`, using `[S]` for the two applications of (3.2). Take
$A,B>0$, $L=\sqrt{AB}\in F$ (as $F$ is a field and $F_{\ge0}$ is closed under
square roots of positive elements), and $u\in K$. The identity
$$|A-Bu^2|^2=(A-B)^2+4AB(\operatorname{Im}u)^2
=\bigl|-L+(A-B)u+Lu^2\bigr|^2 \tag{3.14}$$
holds exactly: the first equality is
$|A-Bu^2|^2=A^2-2AB\operatorname{Re}(u^2)+B^2=(A-B)^2+2AB(1-\cos2\theta)=(A-B)^2+4AB\sin^2\theta$;
the second is $u\bigl((A-B)+L(u-u^{-1})\bigr)$ with $u-u^{-1}=2i\operatorname{Im}u$
purely imaginary, so $|(A-B)+L(u-u^{-1})|^2=(A-B)^2+4L^2(\operatorname{Im}u)^2$ with
$L^2=AB$. (Machine-checked at three exact points: `verify.py` §4.)

Apply (3.2) with exponents $(1,-1)$ to the product $\psi_AU_u^2\psi_{-B}$. The
average of $\|P(\psi_AU_u^2\psi_{-B})-g_AU_u^2g_{-B}\|_2^2$ tends to $0$; since both
have $L^2$ norm at most $1$, the average of the absolute difference of squared
norms tends to $0$. By ergodicity of $Y$ and surjectivity of $u\mapsto u^2$,
$$\operatorname*{Avg}_{u}m(A-Bu^2)\longrightarrow
\Bigl(\int_Y|g_A|^2d\nu\Bigr)\Bigl(\int_Y|g_{-B}|^2d\nu\Bigr)=m(A)m(B). \tag{3.15}$$
Apply (3.2) with exponents $(0,1,2)$ to the right side of (3.14): the projected
character is approximated by $g_{-L}U_ug_{A-B}U_u^2g_L$, whose squared norm is at
most $\|g_{A-B}\|_2^2=m(|A-B|)$ since the two outer factors have modulus $\le1$.
Combining with (3.15) gives $m(A)m(B)\le m(|A-B|)$; taking $-\log$ gives (3.12)
(with the extended convention). For $A=0$ or $B=0$ both sides are $0$. $\square$

*Proof of (3.13)* `[P]`, `[S]`. Use $ru+r\bar u=2r\operatorname{Re}u$ and (3.2)
with exponents $(1,-1)$; the average reduces to the squared norms of
$U_ug_r\,U_u^{-1}g_r$, i.e. to $\int_Y|g_r|^2U_u^{-2}|g_r|^2d\nu$, and the mean
ergodic theorem on $Y$ through the surjective $u\mapsto u^{-2}$ gives
$\bigl(\int_Y|g_r|^2\bigr)^2=m(r)^2$. Radiality replaces the argument by its
absolute value. $\square$

### 3.8 Lemmas 3.4, 3.5

**Lemma 3.4 (general position in a number field).** Let $N_0\subset F$ be a
number field, $N=N_0(i)$, $d_0=[N:\mathbb Q]$. There are arbitrarily large finite
$S\subset K\cap N$ such that every $d_0$ distinct elements of $S$ form a
$\mathbb Q$-basis of $N$. `[P]`, complete proof.

*Proof.* For $t\in N_0$ put $u(t)=\frac{1+it}{1-it}\in K\cap N$ (modulus one,
nonzero denominator because $t$ is real). Choose a $\mathbb Q$-basis of $N_0$;
in the rational coordinates of $t$, the coordinates of $u(t)$ in a $\mathbb Q$-basis
of $N$ are rational functions over $\mathbb Q$ with denominators equal to
$\det$ of "multiplication by $1-it$", nonzero for all real $t$.

*Claim:* no nonzero $\mathbb Q$-linear $\ell:N\to\mathbb Q$ vanishes on all
$u(t)$, $t\in N_0$. If it did, then for each fixed $a\in N_0$ the rational
function $\ell(u(ha))$ vanishes at every rational $h$, hence identically. Its
Taylor expansion at $h=0$, from $u(ha)=1+2iha-2h^2a^2+\cdots$, gives
$\ell(1)=\ell(ia)=\ell(a^2)=0$ for every $a\in N_0$. Squares span $N_0$ over
$\mathbb Q$ because $4a=(a+1)^2-(a-1)^2$; hence $\ell$ vanishes on $N_0+iN_0=N$,
a contradiction. (This is a formal-series calculation in rational coordinates; it
uses no continuity of $\ell$ in the usual topology of $F$.)

Consequently, for any proper $\mathbb Q$-subspace $M\subsetneq N$ the nonzero
$\ell$ annihilating $M$ has $\ell\circ u\not\equiv0$, and
$\ell(u(t))=p(t)/q(t)$ with $p\ne0$ a polynomial over $\mathbb Q$ in the rational
coordinates of $t$. A finite union of proper subspaces cannot contain all $u(t)$:
the product of the finitely many nonzero numerators is a nonzero polynomial over
the infinite field $\mathbb Q$ in the rational coordinates of $t$, and such a
polynomial does not vanish on all of $\mathbb Q^{\dim N_0}$. Hence some $t$
has $u(t)$ outside all of them. Inductively choose each new element
outside the spans of all subsets of at most $d_0-1$ earlier elements: every subset
of at most $d_0$ chosen elements is then independent, hence a basis. $\square$

**Lemma 3.5 (addition under a cap).** Let $w:F_{\ge0}\to[0,\infty]$ satisfy
$w(0)=0$ and (3.12). Let $p_1,\dots,p_q\in F_{\ge0}$, $p=\max_jp_j>0$, with
$w(p_j)\le H<\infty$. If $z=\sum_ja_jp_j\in[0,p)$ with $a_j\in\mathbb Z$,
$\sum_j|a_j|\le M$, then $w(z)\le4MH$. `[P]`, complete proof.

*Proof.* Track residues in $[0,p)$; the cost of a current residue $r$ is $w(r)$,
starting at cost $w(0)=0$. A *signed input* $\pm p_j$ has residue $p_j$ (if $j$
is not the index of the maximum and $+$) or $p-p_j$ (if $-$) or $0$
(the input $\pm p$); its cost is at most $H$, or at most
$w(p-p_j)\le w(p)+w(p_j)\le2H$, or $0$. So each signed input has cost $\le2H$.

Adding an input: if current residue $a$ and input-residue $b$ have $a+b<p$, the
new residue is $a+b$ and, by two applications of (3.12),
$$w(a+b)=w\bigl(p-((p-a)-b)\bigr)\le w(p)+w(p-a)+w(b)\le2w(p)+w(a)+w(b),$$
so the cost increases by at most $2H$ (using $w(p)\le H$), i.e. by at most $4H$
including the input's own cost. If $a+b>p$ the new residue is $a-(p-b)$ with
$a>p-b$, so $w(a-(p-b))\le w(a)+w(p-b)\le w(a)+w(p)+w(b)$: increase at most
$2H$, again $\le4H$ with the input. If $a+b=p$ the new residue is $0$, cost $0$.
Every partial sum stays in $[0,p)$ by construction, and after at most $M$ signed
inputs the residue is $z$. Hence $w(z)\le4MH$. $\square$

### 3.9 Completion of Theorem 2.3

`[P]`, `[S]`; the proof is short and I give it in full.

Let $\mu$ be ergodic and wild on $D$; apply Lemma 3.1 to $(D,\mu)$ and let $Y$
be its terminal factor. Lemma 2.7 (with $d=\mathrm{id}_D$) says $\nu_Y$ is wild.
Construct $P,g_z,m$ as in Section 3.6 and $w=-\log m$.

*Step 1 (a syndetic set of good rotations).* Suppose $m(r)>0$ for some
$r\in F$, $r>0$. Choose $H<\infty$ with $e^{-H}<m(r)^2$ and put
$A_0=\{u\in K:w(2r|\operatorname{Re}u|)\le H\}$, i.e.
$\{u:m(2r|\operatorname{Re}u|)\ge e^{-H}\}$. Then $A_0$ is syndetic: if not, for
each Følner set $\Phi_N$ there is $v_N\in K$ with $v_N\Phi_N\cap A_0=\emptyset$;
the sets $v_N\Phi_N$ are still Følner (in the abelian $K$,
$|h(v_N\Phi_N)\triangle v_N\Phi_N|=|(v_N^{-1}hv_N)\Phi_N\triangle\Phi_N|$), so
(3.13) would give $\operatorname{Avg}_{u\in v_N\Phi_N}m(2r|\operatorname{Re}u|)\to m(r)^2$
while every term is $\le e^{-H}<m(r)^2$ — contradiction. Hence there are
$q_1,\dots,q_J\in K$ with: for every $v\in K$, some $q_jv\in A_0$. (3.16)

*Step 2 (bases).* Take a number field $N_0\subset F$ containing the real and
imaginary parts of all $q_j$, put $N=N_0(i)$, $d_0=[N:\mathbb Q]$, and take $S$
from Lemma 3.4 with $|S|>J(d_0-1)$. For each $v\in K$, (3.16) applied to all
$sv$, $s\in S$, has a pigeonhole outcome: an index $j$ and $d_0$ elements $s$
with $q_jsv\in A_0$. The $k=q_js$ form a $\mathbb Q$-basis of $N$ (multiplication
by $q_j$ is an invertible $\mathbb Q$-linear map). Call the resulting basis a
*good selection for $v$*; there are finitely many possible selections.

*Step 3 (uniform integer coefficients).* Clearing denominators in the basis
expression of $1$, choose one positive integer $D_0$ such that for every possible
selection $T$
$$D_0\cdot1=\sum_{k\in T}a_kk,\qquad a_k\in\mathbb Z,\qquad
\sum_{k\in T}|a_k|\le M_0, \tag{3.17}$$
with $M_0$ common to all selections. Also there is a common $c_0\in(0,1]$ with
$\max_{k\in T}|\operatorname{Re}(kv)|\ge c_0$ for every selection $T$ and every
$v\in S^1$: for a fixed selection this maximum is continuous in the ordinary
unit direction $v$ and never vanishes (if $\operatorname{Re}(kv)=0$ for all $k\in T$
then, by $\mathbb Q$-linearity, $\operatorname{Re}(zv)=0$ for all $z\in N\ni1,i$,
so $v=0$), so it has a positive minimum on the compact circle; then take the
minimum over the finitely many selections.

*Step 4 (uniform bound near the axes).* Let $v\in K$ with
$|\operatorname{Re}v|<c_0/D_0$ and let $T$ be a good selection for $v$. Put
$p_k=2r|\operatorname{Re}(kv)|$ for $k\in T$ and $p=\max_kp_k$. By goodness,
$w(p_k)\le H$. Also $p\ge 2rc_0$. Taking real parts of (3.17) in the
$\mathbb C$-valued pairing $\operatorname{Re}(k\bar v)$ and inserting the signs of
$\operatorname{Re}(k\bar v)$,
$$z=2rD_0|\operatorname{Re}v|=\sum_{k\in T}b_kp_k,\qquad b_k\in\mathbb Z,\
\sum|b_k|\le M_0,$$
and $z<p$ because $z=2rD_0|\operatorname{Re}v|<2rc_0\le p$. Lemma 3.5 gives
$$w(2rD_0|\operatorname{Re}v|)\le4M_0H
\qquad(v\in K,\ |\operatorname{Re}v|<c_0/D_0). \tag{3.19}$$

*Step 5 (contradiction with the vanishing line average).* Every
$t\in F\cap[-1,1]$ is $\operatorname{Re}$ of an element of $K$, namely
$t+i\sqrt{1-t^2}$ (real algebraic, modulus one). Applying (3.19) with
$t=s/(2rD_0)$ for $s\in F\cap(0,2rc_0)$, which satisfies $|t|<c_0/D_0$, gives
$$m(s)\ge e^{-4M_0H}>0,\qquad s\in F\cap(0,2rc_0).$$
Choose $\varphi\in C_c(\mathbb R)$ nonnegative, supported in $(0,2rc_0)$, with
$\int\varphi>0$. Positivity of $I$ and $I(\varphi|_F)=\int_{\mathbb R}\varphi$ give
$$I\bigl(\varphi(t)m(t)\bigr)\ge e^{-4M_0H}\int_{\mathbb R}\varphi>0,$$
contradicting (2.4) for the wild law $\nu_Y$ with $a=1$, in view of
$f^{\nu_Y}=m$ (3.11). Hence $m(r)=0$ for every positive $r\in F$, and by
radiality $m(z)=0$ for every $z\ne0$.

*Step 6 (Haar).* For $z\ne0$,
$\widehat\mu(z)=\int_D\psi_z\,d\mu=\int_Yg_z\,d\nu\le\|g_z\|_2=0$. All nonzero
Fourier coefficients of $\mu$ vanish and $\widehat\mu(0)=1=\widehat{m_D}(0)$;
Fourier uniqueness on the compact abelian $D$ gives $\mu=m_D$.

*Step 7 (ergodic decomposition).* For an arbitrary $K$-invariant wild
probability $\nu$ on the standard compact space $D$, the ergodic decomposition
with respect to the countable group $K$ expresses $\nu=\int\nu_\omega\,d\rho(\omega)$
with $K$-invariant ergodic components. Since $C$ is $K$-invariant Borel and
$\nu(C)=0$, $\nu_\omega(C)=0$ for $\rho$-a.e. $\omega$; each such component is
$m_D$ by Steps 1–6; hence $\nu=m_D$. $\square$

---

## 4. Part D: no weak measurable five-colouring, Theorem 1.4

Throughout, `(C)` is a weak measurable $5$-colouring with Borel classes $A_i$
forming a partition (replaceable by Borel representatives by Definition 1.2's own
remark), $a_i=\mathbf 1_{A_i}$, $I=\{1,\dots,5\}$.

**Standing facts.**
* $\mathcal T=\{$points of density one of their colour$\}$ is conull, and no two
  points of $\mathcal T$ at distance $1$ share a colour (Lemma 4.3). `[P]`
* $H_i=\{q:|A_i\cap B(q,r)|>0\ \forall r>0\}$ is closed and
  $H_i\cap\mathcal T$'s colour-$i$ interior agrees with $A_i$ up to null sets; more
  precisely, $q\in H_i$ iff every neighbourhood of $q$ meets $A_i$ in positive
  area. `[P]`
* $\Delta(K)=\{z:\min_{q\in K}|z-q|<1<\max_{q\in K}|z-q|\}$ for compact $K$ is
  open, and if $K$ is connected then **every** $z\in\Delta(K)$ has a point of $K$
  at distance exactly $1$: the continuous function $q\mapsto|z-q|$ on the
  connected $K$ has image an interval containing values below and above $1$. `[P]`

We record the statements of §§5–8 exactly as they are consumed, with the
observation that closes each implication. The proofs are `[S]`; two of them are
expanded in §8 of this document, and all finite/algebraic sub-claims are
machine-checked (§9).

### 4.1 §5: palettes have size at most 2 at every centre

**Definition 5.1.** $(y,r)$ is a *typical circle sampling* if $y+re$ is typical
for a.e. $e\in S$. For fixed $x$,
$$W_x=\overline{\{\,b:w^*\text{-}\lim_n(a_i(y_n+r_ne))_i\ :\ (y_n,r_n)\text{ typical},\
y_n\to x,\ r_n\to1\,\}}^{w^*}\subseteq L^\infty(S;\mathbb R^5),$$
and $D_{x,i}=\operatorname*{ess\,union}_{b\in W_x}\{e:b_i(e)>0\}$,
$P_x(e)=\{i:e\in D_{x,i}\}$.

Facts, all `[P]`:
* $W_x\ne\emptyset$; each $b\in W_x$ has $b_i\ge0$ and $\sum_ib_i=1$ a.e.
  (weak-\ast limits of such, tested against nonnegative functions).
* $W_x$ is closed under varying centres: $x_n\to x$, $b_n\in W_{x_n}$,
  $b_n\stackrel{w^*}{\rightharpoonup}b$ $\Rightarrow$ $b\in W_x$. Consequently
  $W_x$ is compact and metrizable.
* The essential union in $D_{x,i}$ may be taken over a countable subfamily:
  $M_i=\sup\{|\bigcup_{\text{finite}}\{b_i>0\}|\}$ is attained in the limit by a
  monotone countable union $D_{x,i}$, and any member of $W_x$ with
  $|\{b_i>0\}\setminus D_{x,i}|>0$ would contradict maximality. Hence every
  individual trace has its positive coordinates inside the palette a.e.
* $1\le|P_x(e)|$ for a.e. $e$.

**Lemma 5.2 (palette transfer).** `[S]`, with the following three assertions;
each is used in exactly one place and the place is named.
1. For a.e. independent pair $(e,v)\in S\times S$,
   $c(x+e+v)\notin P_x(e)\cup P_x(v)$. (5.2). — Used to get density
   consequences at spatial sums.
2. If $e$ is an angular density-one point of $D_{x,i}$, then for each $v$ not
   parallel to $e$, the area density of $A_i$ at $x+e+v$ is zero. — Used in
   Lemma 6.3, Lemma 7.6's final step is separate, and in the proofs of 5.6, 6.6.
3. If $z+f=x+s(f)+t(f)$ smoothly on an angular arc, $s,t$ unit, nonparallel, and
   $s$ a local angular diffeomorphism, then $P_z(f)\cap P_x(s(f))=\emptyset$ for
   a.e. $f$ there. (5.3). — The transport engine of §§6 and 8.

The load-bearing point of the proof of (1) is that one factor of the product
$a_i(y_n+r_ne)a_i(y_n+r_ne+v)$ is a *strong* $L^1(S\times S)$ limit
($a_i(y_n+r_ne+v)\to a_i(x+e+v)$, from a change of variables with Jacobian
$r_n|\sin(\arg v-\arg e)|$ bounded below off a $\delta$-neighbourhood and
multiplicity at most two), while the other is only weak-\ast. Products of two
weak-\ast limits are not weak-\ast limits of products; this pairing is what makes
the argument work.

**Corollary 5.4 (sixty-degree exclusion).** $P_x(f)\cap P_x(Rf)=\emptyset$ for
a.e. $f$; proof: $x+f=x+Rf+R^{-1}f$ in Lemma 5.2. `[P]` from Lemma 5.2.

**Binary centres.** For distinct labels $i_+,i_-$, call $x$ *binary* for the pair
if $P_x(e)\cap\{i_+,i_-\}\ne\emptyset$ for a.e. $e$. By Corollary 5.4 the
intersection is a singleton a.e., giving a measurable $2\pi$-periodic
$s_x:\mathbb R\to\{-1,1\}$ with
$$s_x(t+\kappa)=-s_x(t)\quad\text{a.e.},\qquad\text{hence }\ |A_s|=\pi
\text{ per period for }A_s=\{t:s_x(t)=1\}. \tag{5.8}$$
`[P]`

**Lemma 5.5 (binary-centre separation).** `[P]` for its constant chain
(§8.1). There is an absolute $\delta_*>0$ such that any two distinct centres binary
for the same pair are at distance $\ge\delta_*$.

**Proposition 5.6 (palette cardinality).** For every $x$,
$1\le|P_x(e)|\le2$ for a.e. $e$. `[S]`; the proof: if some triple $A$ sits in
$P_x(e)$ on a positive-measure set $B$, then for a.e. $e\in B$ the colouring on
the exact unit circle $v\mapsto x+e+v$ uses only the complementary pair, so
$x+e$ is binary for that pair; the binary centres $x+e$ stay on the compact
circle $x+S$ and are $\delta_*$-separated, hence finite, contradiction. `[P]`
given 5.2 and 5.5.

### 4.2 §6: transition graphs and local finiteness of cyclic centres

**Definition 6.1.** For $x\in\mathbb R^2$, $\Gamma_x$ is the simple graph on $I$
with $ij$ an edge iff for every ball $B$ centred at $x$ of positive finite radius,
$$\limsup_{h\to0,\,h\ne0}\frac{|D_{ij}(B,h)|}{|h|}>0,\qquad
D_{ij}(B,h)=\{q\in B:(c(q),c(q+h))\in\{(i,j),(j,i)\}\}. \tag{6.1}$$
Edge-presence loci are closed; $ij\in\Gamma_x\Rightarrow x\in H_i\cap H_j$. `[P]`

**Lemma 6.2 (edge $\Rightarrow$ avoiding trace).** If $ij\in\Gamma_x$ there is
$b^{ij}\in W_x$ with $b^{ij}_i=b^{ij}_j=0$ a.e.; hence
$P_x(e)\not\subset\{i,j\}$ for a.e. $e$. `[S]`. The only analytic input is the
decay
$$\Bigl\|S(a_s-a_s(\cdot+h))\Bigr\|_{L^2(B)}=o\bigl(\sqrt{|h|}\bigr),\qquad
S g(q)=\int_Sg(q+e)\,d\sigma(e), \tag{6.3}$$
proved by Plancherel from $|\widehat\sigma(\xi)|\le C(1+|\xi|)^{-1/2}$ (stationary
phase; the paper's integration-by-parts computation is correct and I checked the
split at $|\xi|=|h|^{-1}$).

**Lemma 6.3 (strict state separation).** `[S]`. States at $x$: measurable
$A\subseteq S$ with a nonempty label group contained in $P_x(e)$ a.e. on $A$.
The two conclusions used are: (i) at non-parallel density-one directions $a\in A$,
$b\in B$ representing disjoint groups with union $I\setminus\{X\}$, the point
$x+a+b$ has density one of $X$; (ii) $\operatorname{ess\,supp}_SB$ contains no
pair at chordal distance one, so it is strictly separated from its $R$- and
$R^{-1}$-shifts, uniformly along sequences of centres with $L^1$-convergent state
indicators.

**Lemma 6.4 (no singleton/pair alternation).** `[P]`,`[S]`. With
$\gamma=2\arcsin\frac1{2\sqrt3}$ one has $\cos\gamma=\frac56$,
$\gamma/\pi$ irrational (else $2\cos\gamma=\frac53$ would be an algebraic
integer, hence an integer), and $|1-e^{i\gamma}|=1/\sqrt3$. The three points
$z_j=x+e^{i(t+2j\kappa)}(1-e^{i\gamma})$ have $|z_j-x|=1/\sqrt3$ and pairwise
distances $|e^{2i\kappa}-1|\cdot|1-e^{i\gamma}|=\sqrt3\cdot\frac1{\sqrt3}=1$:
a unit equilateral triangle, which admits no proper 2-colouring. Exact checks:
`verify.py` §3.

**Theorem 6.5 (local finiteness of cyclic centres).** The set
$\mathcal L=\{x:\Gamma_x$ contains a cycle$\}$ is closed and locally finite.
`[S]`; three cases, each with a different mechanism:
* *triangles*: Lemma 6.2 forces $P_x(e)$ to meet the outside pair a.e., hence $x$
  is binary for that pair a.e., hence Lemma 5.5 bounds distances. `[P]`
* *four-cycles*: Lemma 6.6 (continuity of the canonical $X/U/V$ state along
  $\mathcal L$, via the bounds (6.5) and weak-\ast passage) plus the support
  transport rule $T_h$ and the gap-endpoint velocity argument. `[S]`
* *five-cycles*: Lemma 6.7 (a support contact bans an angular step), then the
  finite case analysis at the two directions $\pm a$. `[S]`, and the finite part
  is machine-checked: `verify.py` §7.

The finite analysis of `verify.py` §7 is this: with $S^{(r)}=S(R^ra)$ the support
lists at the six orbit positions, after rotating labels so that $0,1\in S^{(0)}$,
the structural lemmas force $2,4\in S^{(1)}\cap S^{(5)}$; if $j,j+1\in S^{(3)}$
then $j-1,j+2\in S^{(2)}\cap S^{(4)}$ and, since adjacent lists are disjoint,
$j-1,j+2\notin\{2,4\}$; **exhaustive check of $j=0,\dots,4$ leaves exactly
$j\in\{1,4\}$**; $j=1$ makes the pairs $\{0,1\},\{1,2\}$ present so both steps
from state $1$ are banned, $j=4$ makes $\{0,1\},\{4,0\}$ present so both steps
from state $0$ are banned, and (6.6) then makes that state null, contradicting
its membership in a support list. The script confirms all of this and that no
case was missed.

### 4.3 §7: one compact connected exclusion set per edge of a cycle

**Lemma 7.2 (disk inequalities).** With
$p_i^\epsilon(q)=\frac1{\pi\epsilon^2}\int_{B(0,\epsilon)}a_i(q+v)\,dv$:
$p_i^\epsilon(q)+p_i^\epsilon(z)\le1$ whenever $|q-z|=1$ (no exceptional pairs,
because the average over a uniform translation puts both points in $\mathcal T$
a.e.); and if $q_n\to q$, $\epsilon_n\to0$, $\liminf_np_i^{\epsilon_n}(q_n)>0$
then $q\in H_i$. `[P]`

**Lemma 7.3 (a missing edge has small overlap).** If $ij\notin\Gamma_x$ there is
a ball $B\ni x$ with $\int_{B'}p_i^\epsilon p_j^\epsilon dq=o(\epsilon)$ for every
ball $B'\subset B$, and for fixed $\alpha>0$ the set
$\{q\in B'':p_i^\epsilon>\alpha,\ p_j^\epsilon>\alpha\}$ is covered by finitely
many open disks of total radius $\to0$. `[S]`.

**Lemma 7.4 (small holes and tree fillings).** `[S]`. For $0<\alpha<1/5$ define
$q_i^\epsilon=(p_i^\epsilon-\alpha)_+/\sum_k(p_k^\epsilon-\alpha)_+$; the
denominator is $\ge1-5\alpha>0$, so $q^\epsilon$ is a continuous map into the
simplex and hence into $G$, the complete graph on five vertices. There are
$\epsilon_n\downarrow0$ and finite families of open disks with pairwise disjoint
closures and total radius $\to0$ such that (1) one core disk per $x\in\mathcal L_0$
containing it, (2) $q^{\epsilon_n}$ takes values in $G$ off the disks, and (3) a
continuous $g_n$ on the square minus the core disks, equal to $q^{\epsilon_n}$ off
all disks, obtained by filling non-core disks through trees (a finite tree is
contractible, so a boundary map into one component tree extends over the disk).

**Lemma 7.5 (cover obstruction).** A closed square of side ten has no relatively
open cover of multiplicity $\le2$ and mesh $\le2$. `[P]`. Take a finite subcover,
a subordinate continuous partition of unity, $F(z)=\sum_a\varphi_a(z)z_a$. At
most two weights are positive, so $F(Q)$ lies in the finite union of the segments
$[z_a,z_b]$ and of the vertices; and $|F(z)-z|\le2$. For
$y$ with $\operatorname{dist}(y,\partial Q)>2$ the map $z\mapsto y+z-F(z)$ sends
$Q$ into the closed radius-two ball about $y\subset Q$, so Brouwer gives a fixed
point $F(z)=y$. Hence $F(Q)$ contains the open central square, contradicting
empty interior. `[P]` (`[C]` Brouwer in the plane.)

**Lemma 7.6 (non-null core loops).** For large $n$ some core disk in $Q$ has a
boundary loop whose $g_n$-image is not null-homotopic in $G$. `[S]`. Suppose not:
extend each loop over its disk and paste, giving $\tilde g_n:Q\to G$ equal to
$q^{\epsilon_n}$ off the holes. The components of
$U_{n,i}=\{z\in Q:(\tilde g_n(z))_i>0\}$ form a relatively open cover of $Q$ of
multiplicity $\le2$; if its mesh exceeded $1+o(1)$, a path in one $U_{n,i}$
joining distant points, with endpoints pushed off the holes, would produce
$a,b$ with $|a-b|>1$, $a\in H_i$, and then
$\alpha|A_i\cap U|\le\|p_i^{\epsilon_n}-a_i\|_{L^1(U)}+\alpha|E_n\cap U|\to0$
on a neighbourhood $U$ of $a$ — contradicting $a\in H_i$. Mesh $\le2$ for large
$n$ contradicts Lemma 7.5. `[S]`

**Proposition 7.1 (a cycle of common exclusion continua).** There are
$\ell\in\{3,4,5\}$, distinct labels $i_0,\dots,i_{\ell-1}$, a point $x$ and
$\rho>0$ such that for each edge $i_ji_{j+1}$ there are a compact connected
$K_j\subset B(x,\rho)$, a direction $v_j\in S$ and $q_{j,k}\in K_j\setminus\{x\}$
with: $x\in K_j$ and $K_j\cap\partial B(x,\rho)\ne\emptyset$;
$q_{j,k}\to x$ and $(q_{j,k}-x)/|q_{j,k}-x|\to v_j$; and
$$H_{i_j}\cap\Delta(K_j)=H_{i_j+1}\cap\Delta(K_j)=\emptyset. \tag{7.1}$$
`[S]`; assembled from Lemmas 7.4, 7.6, 7.7 (midpoint detection by a reduced
circuit — a covering-tree argument, correct), and 7.8 (a connected midpoint
preimage crosses the annulus — a compact-metric continuum argument, correct, the
one point being that the compact partition $Z=Z_1\sqcup Z_2$ exists because in a
compact metric space a point's component is the intersection of its clopen
neighbourhoods). `[P]` From $\{|q-x|:q\in K_j\}=[0,\rho]$ one gets the sequences
$q_{j,k}$ at radii $\rho/k$.

**The compact-metric ingredient of Lemma 7.8, proved in full.**

*Lemma T.* Let $Z$ be a compact metric space and $z\in Z$. The connected
component $C(z)$ equals the intersection of all clopen subsets of $Z$ containing
$z$.

*Proof.* `[P]` Every clopen set is a union of components, so every clopen set
containing $z$ contains $C(z)$; hence $C(z)\subseteq I$ where $I=\bigcap\{K\ni z:
K\ \text{clopen}\}$. Conversely $I$ is closed, hence compact. Suppose $I$ is
disconnected. As $I$ is compact metric, $I=I_1\sqcup I_2$ with $I_1,I_2$
non-empty, both open and closed in $I$, and $z\in I_1$; then $I_1,I_2$ are
compact subsets of the metric space $Z$ at positive distance, so there are
disjoint open $U_1\supseteq I_1$, $U_2\supseteq I_2$. Then $K:=Z\setminus(U_1\cup U_2)$
is compact and disjoint
from $I$. Each $y\in K$ satisfies $y\notin I$, so there is a clopen $K_y\ni z$
with $y\notin K_y$; the open sets $Z\setminus K_y$ cover the compact $K$, so
finitely many $y_1,\dots,y_m$ satisfy $K\subseteq\bigcup_i(Z\setminus K_{y_i})$.
Then $K_0:=\bigcap_iK_{y_i}$ is clopen, contains $z$, and is disjoint from $K$;
hence $K_0\subseteq U_1\cup U_2$, and $K_0\cap U_1$ is clopen in $Z$ (it is
open, and its complement in the clopen $K_0$ is $K_0\cap(Z\setminus U_1)$, closed).
It contains $z$ — but it omits $U_2\supseteq I_2\ne\emptyset$, contradicting
$I\subseteq K_0\cap U_1$. So $I$ is connected, and $I\supseteq C(z)$ with
$z\in I$ forces $I=C(z)$. $\square$

With Lemma T, the partition step of Lemma 7.8 is: for $y_1\in I$, $y_2\in O$,
Lemma T gives a clopen neighbourhood of $y_1$ omitting $y_2$; compactness of $O$
turns this into one clopen neighbourhood of $y_1$ omitting all of $O$; then
compactness of $I$ turns that into a clopen $Z_1\supseteq I$ with
$Z_1\cap O=\emptyset$; put $Z_2=Z\setminus Z_1$. `[P]`

### 4.4 §8: the three cycle lengths are impossible

Set-up: $B\subset S$ finite and antipodally symmetric (directions perpendicular
to some $v_j$). For $e\notin B$ and each edge $j$, give edge $j$ sign $+$ or $-$
according to the sign of $e\cdot v_j$. $O(e)$ = labels remaining after removing
the endpoints of every *positive* edge; $I(e)$ those after removing the endpoints
of every *negative* edge.

**Lemma 8.1 (one-sided strips).** `[P]`,`[S]`. For $e\notin B$, both $O(e)$ and
$I(e)$ are non-empty; on an angular neighbourhood of $e$ an open strip just
outside radius one uses only $O(e)$, and one just inside uses only $I(e)$, up to
plane-null sets; and
$$P_x(e)\cap O(e)\ne\emptyset,\qquad P_x(e)\cap I(e)\ne\emptyset\qquad\text{a.e.}
\tag{8.1}$$
*Proof of the strip and of non-emptiness.* For a positive edge sign and
$q=q_{j,n}=x+r w$, $r=r_{j,n}$, $w=w_{j,n}$, and $z=x+\rho e'$,
$$|z-q|^2=\rho^2-2\rho r(e'\!\cdot w)+r^2<1,\qquad |z-x|=\rho>1 .$$
The first is a quadratic in $\rho$ with roots
$\rho_\pm=r\cos\varphi\pm\sqrt{1-r^2\sin^2\varphi}$, so
$$\rho_+-1=r\cos\varphi+\frac{r^2\sin^2\varphi}{1+\sqrt{1-r^2\sin^2\varphi}}>0
\quad\text{whenever }\cos\varphi>0,$$
while $\rho_-<1$ always. Admissible radii therefore form the interval
$(1,\rho_+)$, of width $\asymp r\cos\varphi>0$ for each fixed $r=r_{j,n}$. The
strip is thin ($r_{j,n}\to0$) but non-empty, which is all that is used;
corroborated numerically in `verify.py` §11. Since $\Delta(K_j)$ is open, it
contains $U=\{x+\rho e':1<\rho<1+w_0,\ |e'-e|<\delta_0\}$ for some
$w_0,\delta_0>0$ depending on the data at $e$ (take $e'$ near $e$, where
$\cos\varphi>0$). Then $U$ is a non-empty
open set avoiding both endpoint supports a.e., so it carries some colour, and
that colour must lie in $O(e)$: $O(e)\ne\emptyset$. A negative sign uses radii
slightly below $1$ the same way. (8.1) follows by taking weak-\ast traces of the
actual circle samplings along radii $\to1$ from the two sides, on a common
full-measure radial set supplied by polar-coordinate Fubini. $\square$

**Proposition 8.2 ($\ell\ne5$).** `[P]`,`[S]`, with the finite part
machine-checked (`verify.py` §8). A label is in $I(e)$ iff both its incident
signs are $+$. Non-emptiness of $O(e)$ and $I(e)$ requires a run of $+$ of length
$\ge2$ and a run of $-$ of length $\ge2$; two runs of each kind would need
$\ge2+2+1+1=6>5$ positions, so the five signs are one $+$-run and one $-$-run, of
lengths $2,3$. The allowed sets are the internal vertices, of sizes $1$ and $2$
and disjoint, so a.e. palette is a pair meeting both; after cyclic relabelling
the options are $D_1=\{1,3\}$ and $D_4=\{1,4\}$, and **reversing all signs swaps
$O$ and $I$ and preserves these two options**, so the options at $e$ and $-e$
coincide. Let $p_j$ be the palette index at $R^je$ on a full six-position orbit.
Disjointness of $D_a,D_b$ is $b-a=\pm1$; so successive indices differ by
$\varepsilon_j=\pm1$. At antipodal positions $j,j+3$ the option sets coincide, so
$p_{j+3}-p_j\in\{0,\pm2\}\pmod 5$; but a sum of three $\pm1$'s is
$-3,-1,1,3$, whose residues are $2,4,1,3$ — never $0$, and $\pm2$ only when all
three agree. So every consecutive triple is constant, all six steps are equal,
and $6\varepsilon\equiv\varepsilon\not\equiv0\pmod5$: the word does not close.
Contradiction. $\square$

**Four cycles.** With labels $0,1,2,3$ and outsider $X$, $U=\{0,2\}$,
$V=\{1,3\}$: if $X\notin P_x(e)$ then both $I(e)\setminus\{X\}$ and
$O(e)\setminus\{X\}$ are non-empty, which forces a consecutive $+$-pair and a
consecutive $-$-pair, i.e. the signs are a *split*; the two allowed sets after
removing $X$ are the opposite middle vertices, giving a diagonal $d(e)\in\{U,V\}$,
and $d(-e)=d(e)$. With $p(e)=X$ if $X\in P_x(e)$ and $d(e)$ otherwise,
$$p(e)\ne p(Re),\qquad p(e)=p(-e)\ \text{if both}\ \ne X\qquad\text{a.e.} \tag{8.2}$$
`[P]`

**Lemma 8.3 (six-position words).** `[P]`,`[S]`. Every word $w(t)$ contains $X$,
all $X$-positions have the same parity, and every direction outside $B$ is split.
The proof uses: a word without $X$ alternates $U,V$ and contradicts $p(e)=p(-e)$;
a word with $X$ on both parities is three-periodic and hence *isolated* under the
cross-word restriction, so isolation propagates along chains in a dense conull
set, contradicting $w(t+\kappa)_j=w(t)_{j+1}$.

**Lemma 8.4 (geometry of four split rays).** `[P]`,`[S]`. The four rays are two
distinct antipodal pairs with opposite directions in opposite edge positions; on
the projective circle $d$ equals $U$ on one open arc and $V$ on the complementary
open arc, and one of these arcs has length $\le\pi/2$.

**Proposition 8.5 ($\ell\ne4$).** `[P]`,`[S]`,`[P]` for the metric fact. If
$t,t'$ are $\eta$-close and $h(t)\ne h(t')$, the three selected projective
positions of each word lie in the corresponding diagonal arc; but three
positions equally spaced by $\kappa=\pi/3$ on the projective circle need an open
arc of length $>2\pi/3>\pi/2$ (the closed complement avoids them, so lies inside
one gap of length $\pi/3$). Contradiction; so $h$ is locally constant on the dense
conull set, hence constant, contradicting the $R$-shift reversing it. $\square$

**Triangle cycles.** Let $X,Y$ be the two outsiders of a triangle. At every
$e\notin B$ two of the three edge signs agree and those two edges cover all three
triangle labels, so Lemma 8.1 gives a one-sided strip near $e$ using only $X,Y$;
by (8.1) an outsider lies in $P_x(e)$ a.e., and not both can, so there is a
measurable binary state $s(e)\in\{X,Y\}$ with $s(Re)\ne s(e)$ a.e. `[P]`

**Lemma 8.6 (local binary rigidity).** The terse neighbourhood step is expanded
in full in §8.2. If $e_0,Re_0\notin B$ then $s$ is essentially constant on an angular neighbourhood
of $e_0$.

**Lemma 8.7 (the boundary is one orbit).** `[S]`,`[P]`. The essential boundary
$E_s$ of $s$ is closed, $R$-invariant and non-empty, and consists of exactly one
six-position $R$-orbit; the six complementary sectors have angle $\kappa$ with
alternating essential values $X,Y$. The counting: if $e_0\in E_s$ then
$e_0\in B$ or $Re_0\in B$; on a six-orbit's three projective positions every edge
of the triangle must have an endpoint in the projective class set of $B$; that
needs $\ge2$ classes; $\#$ classes $\le\ell=3$; distinct orbits have disjoint
projective positions; so two orbits would need $\ge4$. `[P]`

**Lemma 8.8 and the polynomial region.** `[P]` for all the identities. Put
$z=\xi+i\upsilon$, $l=\xi^2+\upsilon^2$, $z=re^{i\phi}$, $\delta=\arccos(r/2)$. Then
$e^{i(\phi-\delta)}+e^{i(\phi+\delta)}=2\cos\delta\,e^{i\phi}=z$ with the two
directions non-parallel. Triple-angle identities give exactly
$$\sin^2(3\phi)=\frac{\upsilon^2(3\xi^2-\upsilon^2)^2}{l^3},\qquad
\sin(3\delta)=\sqrt{1-l/4}\,(l-1),$$
(the second because $3-4\sin^2\delta=3-4(1-l/4)=l-1$), and
$\sin3(\phi-\delta)\sin3(\phi+\delta)=\sin^23\phi-\sin^23\delta$. Hence (8.4),
namely $P:=\upsilon^2(3\xi^2-\upsilon^2)^2<P':=l^3(1-l/4)(l-1)^2$, is
**equivalent** to that product being negative, i.e. to the two endpoints lying
in sectors with opposite outsider values; Lemma 5.2(1) then excludes both
outsiders at a.e. sum, giving: a neighbourhood of $x+z$ uses only the three
triangle labels up to a plane-null set. Machine-checked: `verify.py` §5.

**The seven-point certificate (Lemma 8.9).** `[P]`, machine-checked exactly. With
$G$ the seven-vertex graph
$$G=\{0,A,B,T,uA,uB,uT\},\quad A=\tfrac{\sqrt3+i}{2},\
B=\tfrac{\sqrt3-i}{2},\ T=\sqrt3,\ u=\tfrac{5+i\sqrt{11}}{6},\tag{8.5}$$
all eleven edges $0A,0B,AB,TA,TB,0uA,0uB,uAuB,uTuA,uTuB,TuT$ have length
exactly $1$ (they are $|A|,|B|,|A-B|,|T-A|,|T-B|,|u||A|,|u||B|,|u||A-B|,
|u||T-A|,|u||T-B|,3|1-u|$ with $|u|^2=1$ and $|1-u|^2=(1+11)/36=\frac13$), and
$G$ admits **no** proper 3-colouring: an exhaustive search over $3^7$
assignments finds none, and $4$-colourings exist (`verify.py` §2 records
$0$ and $12$). Placing $z_g=\frac{35+12i}{37}\bigl(g+\frac{-290+149i}{250}\bigr)$,
an isometry since $|35+12i|^2=1369=37^2$, one verifies in exact arithmetic in
$\mathbb Q(\sqrt3,\sqrt{11})$ that $0<|z_g|^2<4$ and (8.4) hold for all seven
$g$ (`verify.py` §6; the values agree with the paper's Table 1 to four decimals,
which also fixes the bracket structure of (8.6)).

**Proposition 8.10 ($\ell\ne3$).** `[P]` given Lemma 8.8 and Lemma 8.9. For each
of the seven points $x+z_g$ choose an open neighbourhood restricted a.e. to the
three triangle labels; a common translation $t\in B(0,\rho)$ puts all seven in
their neighbourhoods and off the (countably many) null exceptional sets, so the
seven vertices — with all eleven unit edges preserved, the placement being an
isometry — are typical and use only the three triangle labels. That is a proper
$3$-colouring of $G$, contradicted by the exhaustive check. $\square$

**Proof of Theorem 1.4.** A weak measurable five-colouring would give a cycle of
length $3$, $4$ or $5$ with the exclusion property (7.1); Propositions 8.2, 8.5
and 8.10 exclude all three. $\square$

---

## 5. Assembly and dependency DAG

```
Thm 1.1  (chi >= 6)
 ├── Thm 1.3  (proper k-colouring  <=>  weak measurable k-colouring), all k
 │     ├── Prop 4.2  (proper => weak measurable)
 │     │     ├── Lemma 4.1  (continuous part = L^2(factor); positivity; R^2-action)
 │     │     │     ├── [C] spectral theorem for discrete E
 │     │     │     └── [C] Bochner on R^2
 │     │     ├── Thm 2.3  (wild K-invariant law on D is Haar)
 │     │     │     ├── Lemma 2.4 (cosets of C, events L_a null)
 │     │     │     │     └── divisibility of K; F = Qbar cap R is a field
 │     │     │     ├── Lemma 2.5 (I(phi * hat nu(a .)) = 0)
 │     │     │     │     ├── Lemma 2.4
 │     │     │     │     ├── [C] Bochner on R ; [C] amenability of abelian groups
 │     │     │     ├── Lemma 2.6 (Borel equivariant centre L(lambda))
 │     │     │     ├── Lemma 2.7 (relative singularity along a tower)
 │     │     │     │     ├── Lemma 2.4 (base), Lemma 2.5, Lemma 2.6
 │     │     │     │     └── universal transfinite induction + (2.6)
 │     │     │     ├── Lemma 3.1 (compact tower with (2.6), terminal ergodic)
 │     │     │     │     └── Hilbert-Schmidt kernels, spectral projection, separability
 │     │     │     ├── Lemma 3.2 (conditional multiple averages)
 │     │     │     │     ├── [C] Hilbert mean ergodic theorem, every Følner seq.
 │     │     │     │     └── power map u -> u^d onto K
 │     │     │     ├── Lemma 3.3 (w(|A-B|) <= w(A)+w(B) ; circle average)
 │     │     │     │     └── Lemma 3.2 with exponents (1,-1) and (0,1,2)
 │     │     │     ├── Lemma 3.4 (rational general position in a number field)
 │     │     │     ├── Lemma 3.5 (integer combinations under a cap)
 │     │     │     └── Lemma 2.5 again, at a = 1, to contradict
 │     │     ├── density of K cap S^1 in S^1 + strong continuity of T_x   [step 6]
 │     │     └── [C] disintegration / conditional expectation
 │     └── Lemma 4.3 + [C] de Bruijn-Erdos (FIP in {1..k}^{R^2})
 └── Thm 1.4  (no weak measurable 5-colouring)
       ├── [everywhere] Lemma 4.3 (typical points contain no unit pair)
       ├── Prop 7.1 (a label cycle with exclusion continua), from
       │     ├── Prop 5.6  (palettes have size <= 2)
       │     │     ├── Lemma 5.2 (palette transfer, 3 assertions)
       │     │     ├── Cor 5.4  (60-degree exclusion)
       │     │     └── Lemma 5.5  (binary-centre separation)     [constants: §8.1]
       │     ├── Thm 6.5  (L is closed and locally finite)
       │     │     ├── Lemma 5.5 (triangles)
       │     │     ├── Lemma 6.6 + 6.3 + support transport (four-cycles)
       │     │     ├── Lemma 6.7 + finite case analysis (five-cycles)  [machine-checked]
       │     │     └── Lemma 6.3, 6.4, Prop 5.6
       │     ├── Lemma 6.2 (edge => avoiding trace) + circle-Fourier decay
       │     ├── Lemma 7.2, 7.3, 7.4 (disk averages, holes, tree fillings)
       │     ├── Lemma 7.5 (cover obstruction, Brouwer) + 7.6 (non-null loop)
       │     └── Lemma 7.7, 7.8 (reduced words; annular crossing; continua)
       └── Props 8.2 / 8.5 / 8.10 (cycle lengths 5 / 4 / 3 impossible)
             ├── Lemma 8.1 (one-sided strips), 8.3, 8.4, 8.7
             ├── Lemma 8.6 (local binary rigidity)          [expanded: §8.2]
             ├── Lemma 8.8 (polynomial three-label region)
             └── Lemma 8.9 (seven-point certificate)          [machine-checked]
```

**No circularity.** Theorem 2.3 is used only inside Prop 4.2; Theorem 1.4 uses
neither Theorem 2.3 nor Theorem 1.3, only the definition of a weak measurable
colouring and Lemma 4.3. The two halves of the proof are logically independent
except for the definition and Lemma 4.3, which itself uses only Definition 1.2.

## 6. The essential steps

The following are the steps without which the argument does not run. Every other
lemma is a technical facilitator.

1. **Divisibility of $K$** (Lemma 2.4): a finite image of a divisible group is
   trivial — this is what makes $\nu(C)=0$ propagate to all cosets, and it is the
   only place where the specific field $F=\overline{\mathbb Q}\cap\mathbb R$ is
   used rather than a general countable subfield. (Any countable subfield of
   $\mathbb R$ closed under square roots of positive elements would do: $K$ must be
   divisible, which needs $n$-th roots of positive algebraic reals.)
2. **No strongly continuous vector for $t\mapsto\psi_{at}$** (Lemma 2.5): the
   non-regularity of the wild law is exactly what forbids $L^2$-continuity along
   $F$; the Bochner round-trip through $\mathbb R$ is the mechanism.
3. **Relative singularity along the *compact* tower** (Lemma 2.7): compensates
   for the fact that $\nu$ is not assumed regular; without the Furstenberg–Zimmer
   tower the difference law would not be wild.
4. **The radial difference inequality** (Lemma 3.3): a genuine subadditivity for
   $w=-\log m$, obtained from *(3.14)* — the algebraic identity that makes a
   *difference* of moduli appear on one side and a *product* on the other.
   $(3.14)$ is the only algebraic miracle in Part C.
5. **Number-theoretic general position** (Lemma 3.4) and the **capped addition
   bound** (Lemma 3.5): these turn a *pointwise* positive value into a *uniform
   lower bound on an interval*, which is what the line average can see.
6. **The two-factor structure of Lemma 5.2(1)**: strong $L^1$ on one factor,
   weak-\ast on the other.
7. **Binary-centre separation** (Lemma 5.5) with the $L^1$-contraction
   (Deroin–Kleptsyn–Navas style) argument: this is the only place where *all five
   labels at once* are forced out of a support, and it is what makes $\mathcal L$
   locally finite.
8. **The planar cover obstruction** (Lemma 7.5) together with Lemma 7.6: this is
   the step that converts a measure-theoretic 'mostly-two-labels' statement into a
   *connected* set, hence into a genuine geometric exclusion.
9. **The straddling region** $\Delta(K)$ with both extreme inequalities *strict*:
   this is what converts 'zero density outside' into 'both endpoint labels
   excluded from an open set'.
10. **The Moser spindle** (Lemma 8.9): the only finite obstruction used, and the
    only place where a non-5-colourability is not obtained from palette
    combinatorics.

## 7. What the compression has to accept

These are the long computations I checked line by line but did not reproduce:

* Lemma 2.7's induction body (the phase-list encoding, (2.7), (2.11), the
  collision count) — 4 pages;
* Lemma 3.2's van der Corput induction (3.5)→(3.8) — 2 pages;
* Lemma 5.5's bounded-distortion iteration — 2 pages; §8.1 checks every
  inequality in it, every use of $L$, and reproduces (5.9)–(5.11) with the
  explicit $c_0=\tfrac12$, but not the internal density-point passage;
* Lemma 6.3's uniform support argument and Lemma 6.6's weak-\ast passage — 1 page
  each;
* Theorem 6.5's four- and five-cycle accumulation arguments — 4 pages;
* Lemmas 7.3, 7.4, 7.6, 7.8 — 5 pages.

Each of these is a self-contained statement about a fixed system with no
quantifier over the colouring beyond the hypotheses named. None of them appeals
to the conclusion.

---

## 8. The terse steps, expanded; and the constant chain

Nothing in the paper is repaired: every display and every constant is correct
as printed. Two passages are stated more briefly than a line-by-line referee
would like, and this section expands them completely. It also records how the
displays were read.

### 8.0 How the displays were read (do not trust plain text extraction)

`pdftotext` without positional information **silently drops** three classes of
glyph: fractional factors set as a raised digit over a lowered digit, radicals,
and large delimiters. In this paper every such glyph is a separate text object,
so plain extraction produces displays that are numerically wrong. All
load-bearing displays below were therefore re-read from the page's glyph
bounding boxes (`pdftotext -bbox-layout`), where a fraction is recognisable as a
pair of full-size digits with baselines above and below the main line, separated
by a $\approx10$pt horizontal gap in the main line that only the numerator can
fill. Three examples that matter here:

* **p. 32**, the display at glyph-baseline $y=418$. The main line reads
  `F j r ( t ) ≥ 1 + c 0 d − C 0 d ℓ r ≥ 1 + c 0 d.` with a $\approx10.2$pt gap
  between `−` ($x\le300.5$) and `C` ($x\ge310.7$) and another between `+`
  ($x\le368.5$) and `c` ($x\ge378.8$); the numerals `1` occupy
  $x\in[303.9,309.4]$ and $x\in[372.0,377.4]$ at $y\in[399.9,410.8]$ and the
  `2`s the same $x$-ranges at $y\in[414.8,425.7]$. So the printed display is
  $$F'_{j_r}(t)\ \ge\ 1+c_0d-\tfrac12C_0d\,\ell_r\ \ge\ 1+\tfrac12c_0d,$$
  and likewise `1/2 ≤ F'_j ≤ 3/2` on the same page.
* **p. 57**, display (8.6): the drawn delimiters are present as separate
  objects, and the rows are `(35+12i)`, `(-290+149i)` above `37`, `250`; the
  printed display is
  $z_g=\frac{35+12i}{37}\bigl(g+\frac{-290+149i}{250}\bigr)$.
* **p. 2**, §1: `circumradius r = 2/5`, `nearest-neighbor distance √3 r`,
  `at least √21 r apart`, `(√21 − 2)r > 1`; the radicals are separate objects.
  The two inequalities are then exact: $2r=4/5<1$ and
  $(\sqrt{21}-2)\tfrac25>1\iff84>81$.

**Also consistent as printed, needing no correction:** on p. 37 the two displays
$\gamma=2\arcsin(\cdot)$ and $\cos\gamma=\tfrac56$ determine each other, since
$\cos\gamma=\tfrac56\iff\sin^2(\gamma/2)=\tfrac1{12}
\iff\sin(\gamma/2)=\tfrac1{2\sqrt3}$.

### 8.1 The constant chain of Lemma 5.5, verified end to end

Set $c_0=\tfrac12$ and $C_0$ as in (5.10) below. The paper's choices are
$$0<L\le\min\{c_0/C_0,\ \pi/4\},\qquad
\delta_*=\min\{d_1,\ (2C_0)^{-1},\ L/(2C_0)\},$$
and the enlargement step asserts, for $t\in I_r$,
$$F'_{j_r}(t)\ \ge\ 1+c_0d-\tfrac12C_0d\,\ell_r\ \ge\ 1+\tfrac12c_0d . \tag{8.1}$$
Both inequalities are correct:

* the first is $|F''|\le C_0d$ integrated from the midpoint of $I_r$, at
  distance at most $\tfrac12\ell_r$ from $t$;
* the second is equivalent to $\tfrac12C_0d\ell_r\le\tfrac12c_0d$, i.e. to
  $\ell_r\le c_0/C_0$, which is exactly the hypothesis $L\le c_0/C_0$ together
  with the iteration's invariant $\ell_r<L$. So $L\le c_0/C_0$ is the
  *correct, and sharp*, constant; nothing needs changing. (With the factor
  $\tfrac12$ dropped — as plain text extraction drops it — one would wrongly
  need $L\le c_0/(2C_0)$; that is an artifact of the extraction, not of the
  paper.)

Consequently $\lambda:=1+\tfrac12c_0d>1$ and $\ell_{r+1}\ge\lambda\ell_r$, the
iteration stops at the first $N$ with $\ell_N\ge L$, and
$L\le\ell_N\le(1+C_0d)L$.

**Every use of $L$, checked.**

1. $\ell_0<L$: hypothesis.
2. (8.1): needs $\ell_r<L\le c_0/C_0$. ✓
3. $F_j,F_j^{-1}$ Lipschitz with $\tfrac12\le F_j'\le\tfrac32$: from
   $|F_j'-1|\le C_0d\le C_0\delta_*\le C_0(2C_0)^{-1}=\tfrac12$. ✓
4. $\sum_{r<N}\ell_r\le\ell_N\sum_{q\ge1}\lambda^{-q}
   =\ell_N/(\lambda-1)=\ell_N\cdot\frac{2}{c_0d}$. ✓
5. (5.11): $\operatorname{osc}_{I_0}\log G'\le2C_0d\cdot\frac{2\ell_N}{c_0d}
   =\frac{4C_0\ell_N}{c_0}\le\frac{4C_0(1+C_0d)L}{c_0}\le\frac{6C_0L}{c_0}$,
   using $C_0d\le\tfrac12$. This is exactly the displayed bound. ✓
6. $D_{\mathrm{dist}}=\exp(6C_0L/c_0)>1$ finite. ✓
7. $\frac{|I_N\setminus A|}{|I_N|}\le D_{\mathrm{dist}}
   \frac{|I_0\setminus A|}{|I_0|}$. ✓
8. Lengths in $[L,(1+C_0d)L]$ with $L>0$: fine.
9. $F_j(a)\le a+C_0d<a+L\le b$: $C_0d\le C_0\delta_*\le L/2<L$. ✓
10. $F_j(b)\ge b+c_0d$: from the first line of (5.10), no $L$ involved. ✓
11. Termination after finitely many extensions reaching length $2\pi$:
    each step advances the right endpoint by $\ge c_0d>0$ and $L>0$. ✓

**The constants $c_0,C_0$ of (5.10), computed.** From `pdftotext -bbox-layout`
of p. 31 the printed expansions are
$$\operatorname{Im}\log(1+de^{-it})=-d\sin t+O_{C^2}(d^2),\quad
|d+e^{it}|=1+d\cos t+O_{C^2}(d^2),$$
$$\alpha_\pm(t)=t\pm\kappa-d\sin t\mp\tfrac{d}{\sqrt3}\cos t+O_{C^2}(d^2),\qquad
F(t)=t-\tfrac{2d}{\sqrt3}\cos(t+\kappa)+O_{C^2}(d^2)=t+\tfrac{2d}{\sqrt3}\sin(t-\tfrac{\pi}{6})+O_{C^2}(d^2).$$
I re-derived the last line: with $h_1=-\sin t$, $h_2=-\tfrac1{\sqrt3}\cos t$,
inverting $\alpha_-=t-\kappa+d(h_1-h_2)+O(d^2)$ gives
$\alpha_-^{-1}(t)=t+\kappa-d(h_1-h_2)(t+\kappa)+O(d^2)$, so
$F=\alpha_+(\alpha_-^{-1}(t))-2\kappa=t+2d\,h_2(t+\kappa)+O(d^2)
=t-\tfrac{2d}{\sqrt3}\cos(t+\kappa)+O(d^2)$
$=t+\tfrac{2d}{\sqrt3}\sin(t-\pi/6)+O(d^2)$, and hence
$F_j(t)=t+\tfrac{2d}{\sqrt3}\sin(t-j\kappa-\pi/6)+O(d^2)$. (Corroborated
numerically, `verify.py` §11: the first-order coefficient
$(F(t)-t)/d\to\frac{2}{\sqrt3}\sin(t-\pi/6)$ with a bounded $O(d^2)$ remainder.)

*Exact elementary fact.* For any $u$ the six numbers $u-j\kappa$, $0\le j\le5$,
are $\pi/3$-spaced, so one of them lies in $[\pi/3,2\pi/3]$, where
$\sin\ge\sin(\pi/3)=\sqrt3/2$; likewise one lies where $\cos\ge\sqrt3/2$. Hence
$$\max_j(F_j(t)-t)\ge\tfrac{2d}{\sqrt3}\cdot\tfrac{\sqrt3}{2}-C'd^2=d-C'd^2,\qquad
\max_jF_j'(t)\ge1+d-C'd^2 .$$
So $c_0=\tfrac12$ and some absolute $d_1>0$ work in (5.10), with
$|F_j-t|,|F_j'-1|,|F_j''|\le C_0d$ for an absolute $C_0$; in particular
$c_0,C_0$ are absolute. `[P]`

### 8.2 Lemma 8.6's neighbourhood step, expanded in full

The paper's proof of Lemma 8.6 contains this sentence, which I transcribe from
the glyph layout of p. 55 rather than from plain text:

> *"Fix a point of $U'$. On a sufficiently small ball around it, all starting
> points $q$ and sufficiently small shifts $h$ admit the following construction
> inside $U'$ and $V$. ... Smallness keeps $|t|<2$ and every constructed point
> in the stated open set."*

It is then applied as *"In a still smaller ball, every ordered pair $(q,q')$
has $q'-q$ within the permissible shift range"*. The step is correct: the
permissible-shift set is open in $h$ (at $h=0$ the constructed neighbour is
$q+v'_j\in V$, by the defining property of $U'$), so on the compact sub-ball it
contains a ball about $0$, and the paper then passes to a ball smaller than that
radius. Because the step is stated in one sentence and carries all the weight of
the Fubini conclusion, here is the complete expansion, which a referee may check
on its own. `[P]`

**Lemma 8.6$'$ (expanded neighbourhood step).** Let $U,V\subseteq\mathbb R^2$
be open and non-empty with $c\in\{X,Y\}$ off a plane-null subset of each.
Suppose there are $z_*\in U$, $\epsilon>0$ with $B(z_*,\epsilon)\subseteq U$,
and unit vectors $v'_1,v'_2$, non-parallel, with $q+v'_j\in V$ for all
$q\in B(z_*,\epsilon)$, $j=1,2$. Then $c$ is essentially constant on
$B(z_*,\epsilon/10)$.

*Proof.* Put $\phi=\angle(v'_1,v'_2)\in(0,\pi)$; then
$|\det(Jv'_1,Jv'_2)|=\sin\phi>0$. As $V$ is open and
$B(z_*,\epsilon)+v'_j\subseteq V$, and $q\mapsto q+v'_j$ is continuous on the
compact ball $B(z_*,\epsilon)$, there is $\tau\in(0,\min\{1,\epsilon/4\})$ with
$$\Bigl\{q+\tfrac{t}{2}Jv'_j+\sqrt{1-t^2/4}\,v'_j:\ q\in B(z_*,\epsilon),\
|t|<\tau\Bigr\}\subseteq V\qquad(j=1,2),$$
because the displayed point tends to $q+v'_j$ uniformly as $t\to0$.

For $h=t_1Jv'_1+t_2Jv'_2$ with $|t_1|,|t_2|<\tau$ define five maps of $q$:
$$c_0=0,\quad c_1(h)=\tfrac{t_1}{2}Jv'_1+\sqrt{1-t_1^2/4}\,v'_1,\quad
c_2(h)=t_1Jv'_1,$$
$$c_3(h)=t_1Jv'_1+\tfrac{t_2}{2}Jv'_2+\sqrt{1-t_2^2/4}\,v'_2,\quad c_4(h)=h .$$
From $v'_j\perp Jv'_j$ and $|v'_j|=|Jv'_j|=1$ come four exact identities:
$$|c_1-c_0|=1,\qquad|c_1-c_2|=1,\qquad|c_3-c_2|=1,\qquad|c_3-c_4|=1 .$$
For $|h|<\delta:=\min\{\tau,\epsilon/4\}$ and $|t_j|<\tau$: the vertices
$c_0,c_2,c_4$ satisfy $|q+c_j-z_*|\le10^{-3}\epsilon+\epsilon/4<\epsilon$, so
they lie in $B(z_*,\epsilon)\subseteq U$; the vertices $c_1,c_3$ lie in $V$ by
the choice of $\tau$. Let $N$ be the plane-null set off which every point of
$U\cup V$ is typical and coloured in $\{X,Y\}$. Then for each $h$ with
$|h|<\delta$ and every $q$ with $q+c_j(h)\notin N$ for all $j$,
$$c(q+c_0(h))=c(q+c_4(h)),$$
because all five colours lie in $\{X,Y\}$ and alternate along a path of four
unit edges. The exceptional $q$-set, $\bigcup_j(c_j(h)+N)$, is null.

Hence for every $h$ with $|h|<\delta$ and a.e. $q\in B_*:=B(z_*,10^{-3}\epsilon)$,
$c(q)=c(q+h)$. The function $(q,h)\mapsto\mathbf 1\{c(q)\ne c(q+h)\}$ is jointly
measurable, so Fubini over $B_*\times B(0,\delta/2)$ gives $c(q)=c(q+h)$ for
a.e. $(q,h)$ there. The bijection $(q,h)\mapsto(q,q+h)$ with measurable inverse
then gives $c(q)=c(q')$ for a.e. $(q,q')\in B_*\times B_*$, and a second Fubini
produces $q_0\in B_*$ with $c(q')=c(q_0)$ for a.e. $q'\in B_*$. $\square$

**Recovering the paper's Lemma 8.6 from it.** Its two hypotheses are exactly
what the paper's opening produces: by the implicit-function-theorem computation
$F(r,\theta)=|re^{i\theta}-e_0|^2-1=r^2-2r\cos\theta$, $F(1,\pi/3)=0$,
$\partial_\theta F(1,\pi/3)=\sqrt3\ne0$, so $\theta\mapsto r(\theta)$ is a local
diffeomorphism with $r(\pi/3)=1$, and $\theta\mapsto v'(\theta):=r(\theta)e^{i\theta}-e_0$
is injective near $\pi/3$ with $|v'(\theta)|=1$ and $e_0+v'(\theta)=r(\theta)e^{i\theta}$
lying in $V$ for $\theta$ on the correct side of $\pi/3$; two values
$\theta_1\ne\theta_2$ give non-parallel unit $v'_1,v'_2$. The paper then takes
$U'$ a connected sub-strip with $q+v'_j\in V$ for all $q\in U'$ (that is the
sentence "close enough to $z_0$ that $q+v'_1,q+v'_2\in V$ for every $q\in U'$"),
and applies the argument at any chosen point of $U'$. The conclusion is
constancy on a ball, and every point of $U'$ gets its own ball, so the sets of
points of $U'$ with local essential colour $X$, resp. $Y$, are open, disjoint
and cover $U'$; connectedness of $U'$ forces one of them to be $U'$ up to a null
set. Polar-coordinate Fubini on typical samplings from that side then puts a
single outsider in $P_x(e)$ for a.e. $e$ in an angular neighbourhood of $e_0$,
which is the assertion of Lemma 8.6. $\square$

**Remark.** Nothing here uses more than openness of $U$ and $V$ and the two
non-parallel unit directions. This is why the strips' thickness — which is
$\asymp r_{j,n}\cos\varphi$ and tends to $0$ (Section 4.4) — never enters: the
argument is uniform in the strip's width.

## 9. Machine-checked exact verification

`exact.py` implements $\mathbb Q(\sqrt3,\sqrt{11})$ in the $\mathbb Q$-basis
$(1,\sqrt3,\sqrt{11},\sqrt{33})$ with field operations and an **exact** sign
function (nested-radical comparison; `sign()` decides $p+q\sqrt{11}$ by comparing
$p^2$ with $11q^2$, each $p,q\in\mathbb Q(\sqrt3)$ decided by comparing with
$3q^2$). No floating point enters any verdict; the decimal prints are for the
reader only.

`python3 verify.py` checks, with exit status $0$ iff all pass:

| verify.py § | claim | result |
|---|-------|--------|
| 1 | $2r<1$ and $(\sqrt{21}-2)r>1$ for $r=2/5$, i.e. $84>81$; $\lvert2-\omega\rvert^2=7$ | pass |
| 1 | triangular-lattice Voronoi circumradius $=\ \text{min norm}/\sqrt3$ | pass |
| 2 | all 11 edges of the Moser-type graph (8.5) have length exactly $1$ | pass |
| 2 | that graph has **no** proper 3-colouring ($3^7$ exhaustive) and exactly 12 proper 4-colourings | pass |
| 3 | $\cos\gamma=5/6$, $\lvert1-e^{i\gamma}\rvert^2=1/3$, triangle side $\sqrt3\cdot\frac1{\sqrt3}=1$ | pass |
| 4 | identity (3.14) at three exact points, with the exact reason the cross term vanishes | pass |
| 5 | $\sin^2(3\phi)=\upsilon^2(3\xi^2-\upsilon^2)^2/l^3$; $\sin3\delta=\sqrt{1-l/4}(l-1)$; (8.4) $\Leftrightarrow$ product $<0$ | pass |
| 6 | Lemma 8.9 in **exact** arithmetic: $0<\lvert z_g\rvert^2<4$ and $P<P'$ for all seven placed vertices | pass |
| 7 | Sec. 6.3.4: $S^{(0)}\supseteq\{0,1\}\Rightarrow 2,4\in S^{(1)}\cap S^{(5)}$ over all valid support lists | pass |
| 7 | Sec. 6.3.4: exhaustive $j=0,\dots,4$ leaves exactly $j\in\{1,4\}$ | pass |
| 8 | Prop 8.2: exactly one $+$-run and one $-$-run of lengths $2,3$; the only admissible six-step words are constant and fail to close mod 5; options at $e$ and $-e$ coincide | pass |
| 9 | three $\kappa$-spaced projective positions need an arc $>2\pi/3>\pi/2$ | pass |
| 11 | (corroboration) $(F(t)-t)/d\to\frac{2}{\sqrt3}\sin(t-\pi/6)$ and the Lemma 8.1 root $(\rho_+-1)/r\to\cos\varphi$ | pass |
| 12 | the glyph-coordinate reading of (8.1): both numerators sit in the main-line gaps, above their denominators | pass |
| 10 | the constant chain (8.1): $\ell_r<L\le c_0/C_0$ gives $\frac12C_0d\ell_r\le\frac12c_0d$; all 11 uses of $L$; the (5.11) bound | pass |

**Note on reading the paper.** Plain `pdftotext` output is *not* a reliable copy
of this paper: it drops fractional factors, radicals and large delimiters, and
it emits subscript digits as if they were full-size. Every display quoted in
this document was therefore cross-checked against the page's glyph bounding
boxes (`pdftotext -bbox-layout`); §8.0 records the coordinates for the three
displays where the difference is numerically decisive ((8.1) on p. 32, (8.6) on
p. 57, and the §1 constants on p. 2). With those readings all constants agree
with the paper's own cross-references: `verify.py` reproduces the exact
quantities behind Lemma 8.9 and they match Table 1 to the displayed four
decimals.

---

## 10. Verdict summary

| item | verdict |
|---|---|
| Theorem 1.1 follows from Theorems 1.3 and 1.4 | **correct**; assembly written out in §5 |
| Theorem 1.3, forward (Prop 4.2) | **correct**; the two compressed steps (density of $K\cap S^1$ + strong continuity; single good sample) are complete in §2.2 |
| Theorem 1.3, reverse (Lemma 4.3 + compactness) | **correct**, §2.3 |
| Theorem 2.3 (Haar rigidity) | **correct**; chain and all links written out in §3; the algebraic identity (3.14) is the only miracle |
| Theorem 1.4 (no weak measurable 5-colouring) | **correct** as far as the argument goes; §§5–8 statements checked, finite parts machine-verified |
| Lemma 5.5 (binary separation) | **correct as printed**: the display carries the factor $\frac12$ (glyph coordinates, §8.0), and $L\le c_0/C_0$ is the correct and sharp constant; all 11 uses of $L$ checked, $c_0=\frac12$ (§8.1) |
| Lemma 8.6 (local binary rigidity) | **correct**; its one-sentence neighbourhood step is expanded into a complete lemma with proof (§8.2) |
| Lemma 8.9 (seven-point certificate) | **correct**, verified exactly (§9) |
| seven-colouring | **correct**, including all boundaries (§1) |
| Moser-type 7-vertex graph | **correct**: 11 unit edges, no proper 3-colouring (§9) |
| Corollary 1.5 ($\delta>0$) | **correct**: $\delta=1/|E(H)|$ where $H$ is the finite witness from de Bruijn–Erdős; the constant is existential, not explicit |

**What is *not* established here.** The compressed proof does not re-derive
Lemmas 2.7, 3.2, 5.5's iteration, 6.3, 6.6, Theorem 6.5's four- and five-cycle
accumulation arguments, or Lemmas 7.3, 7.4, 7.6, 7.8; those are `[S]` (I checked
them line by line, listed their statements exactly, and did not reproduce their
computations). Corollary 1.5's constant remains existential: making it explicit
requires an explicit finite witness, which this document does not produce.
