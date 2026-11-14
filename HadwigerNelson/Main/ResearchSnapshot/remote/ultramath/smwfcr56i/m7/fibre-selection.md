# A named black box of the paper, proved in full

**Measurable fibre-orthonormal-basis selection in the compact-tower construction.**

This document does one thing. It isolates a single step that the paper asserts in one sentence and proves it
completely, self-contained, with every estimate explicit. Nothing here depends on the two claims I withdrew
(§5 records the retractions).

---

## 0. The black box, as stated in the paper

Paper §3.1, in the proof of Lemma 3.1 (compact tower), after introducing the field of spectral projections
$Q_y = \mathbf 1_{(\delta,\infty)}(A_y^*A_y)$ on the fibre Hilbert spaces $H_y = L^2(\mu_y)$:

> "Their fiber scalar products make rank and linear-independence tests measurable. Selecting the first available
> independent section at each step and applying fiberwise Gram–Schmidt gives measurable fiber-orthonormal sections
> $e_1,\dots,e_d$ spanning the range of $Q_y$."

Everything downstream in §3 of the paper depends on this: the boundedness estimate (3.1)
$\sum_i\lvert e_i(x)\rvert^2 = d$, the fact that $Y' = Y\vee\sigma(e_1,\dots,e_d)$ is a *strict* extension of $Y$,
and the approximation property (2.6) which the whole of Lemma 2.7 consumes. The sentence above contains no proof.
Below, Lemma S is that statement, proved.

---

## 1. Setting: measurable fields of Hilbert spaces

This is the standard (von Neumann–Dixmier) formalism, stated in the smallest form that suffices.

**Definition 1.1 (measurable field of Hilbert spaces).** Let $(Y,\nu)$ be a standard probability space. A
*measurable field of separable Hilbert spaces* over $Y$ is a family $(H_y)_{y\in Y}$ of separable complex Hilbert
spaces together with a countable set $\Gamma$ of *sections* $\xi = (y\mapsto\xi(y)\in H_y)$ such that

* **(F1)** $y\mapsto\langle\xi(y),\eta(y)\rangle_{H_y}$ is $\nu$-measurable for all $\xi,\eta\in\Gamma$;
* **(F2)** for $\nu$-almost every $y$, $\Gamma_y := \{\xi(y) : \xi\in\Gamma\}$ is dense in $H_y$.

A section $\xi$ is *measurable* if $y\mapsto\langle\xi(y),\gamma(y)\rangle$ is measurable for every $\gamma\in\Gamma$.
Write $\mathcal S$ for the set of measurable sections.

**Definition 1.3 (measurable field of operators).** A family $y\mapsto Q_y\in\mathcal B(H_y)$ is a *measurable
field of operators* if $y\mapsto\langle Q_y\xi(y),\eta(y)\rangle$ is measurable for all $\xi,\eta\in\mathcal S$;
it is a field of *orthogonal projections* if $Q_y = Q_y^* = Q_y^2$ for a.e. $y$, and *contractive* if
$\lVert Q_y\rVert\le1$.

**Lemma 1.2 (closure properties).** (i) $\Gamma\subseteq\mathcal S$, $\mathcal S$ is closed under finite linear
combinations with measurable coefficients, and for $\xi,\eta\in\mathcal S$ the functions
$y\mapsto\lVert\xi(y)\rVert_{H_y}$ and $y\mapsto\langle\xi(y),\eta(y)\rangle$ are measurable.
(ii) If $\xi_n\in\mathcal S$ and $\xi_n(y)\to\xi(y)$ in $H_y$ for $\nu$-a.e. $y$, then $\xi\in\mathcal S$.
(iii) If $\xi\in\mathcal S$ and $y\mapsto Q_y$ is a measurable field of operators then $Q\xi\in\mathcal S$.

*Proof.* (i) The first two assertions are immediate from bilinearity of the inner product and (F1).
*Norm:* by (F2), for a.e. $y$,
$$\lVert\xi(y)\rVert = \sup_{\gamma\in\Gamma,\ \gamma(y)\ne0}\frac{\lvert\langle\xi(y),\gamma(y)\rangle\rvert}{\lVert\gamma(y)\rVert},$$
a countable supremum of measurable functions, hence measurable.
*Pairing:* for measurable $\xi,\eta$, choose (measurably, by a first-fit over an enumeration of the countable set of
finite rational combinations of $\Gamma$, using the norm formula just proved) sections $\eta_n$, each a finite
rational combination of elements of $\Gamma$, with $\eta_n(y)\to\eta(y)$ and $\lVert\eta_n(y)\rVert\le2\lVert\eta(y)\rVert$
for a.e. $y$. Then $\langle\xi(y),\eta_n(y)\rangle\to\langle\xi(y),\eta(y)\rangle$ for a.e. $y$, since
$\lvert\langle\xi,\eta_n-\eta\rangle\rvert\le\lVert\xi\rVert\,\lVert\eta_n-\eta\rVert\to0$; a pointwise limit of
measurable functions is measurable, so the pairing is measurable.
(ii) For $\gamma\in\Gamma$, $\langle\xi_n(y),\gamma(y)\rangle\to\langle\xi(y),\gamma(y)\rangle$ pointwise, and the
left side is measurable by (i); so $\xi\in\mathcal S$.
(iii) By Definition 1.3 with $\eta = \gamma\in\Gamma\subseteq\mathcal S$. $\square$

**Remark 1.4 (the paper's field satisfies this).** Take the factor $\pi:X\to Y$ of standard probability spaces with
disintegration $\mu = \int_Y\mu_y\,d\nu(y)$ ((T6) of the paper: Tao, Theorem 4 and Remark 5), $H_y = L^2(\mu_y)$, and
$\Gamma = \{\pi_y u : u\in\mathcal U\}$ where $\mathcal U\subset L^\infty(X)$ is a countable algebra generating the
Borel $\sigma$-algebra of $X$ and dense in $L^2(X)$; here $\pi_y u$ denotes the fibre class of $u$. Then (F1) and
(F2) hold, and for $u\in L^2(X)$ the section $y\mapsto\pi_y u$ is measurable: this is the standard direct-integral
description of the $L^2$-space of a factor of standard probability spaces (Furstenberg, *Ergodic behavior of diagonal
measures…*, §6; Zimmer, *Extensions of ergodic group actions*, §2; Dixmier, *Von Neumann algebras*, II.§1). The
concrete content used below is only (F1)–(F2) and Lemma 1.2. The field $Q_y = \mathbf 1_{(\delta,\infty)}(A_y^*A_y)$
is measurable in the sense of Definition 1.3: for $\xi,\eta\in\mathcal S$ the function
$y\mapsto\langle A_y\xi(y),\eta(y)\rangle = \iint L(x,x')\xi(x')\overline{\eta(x)}\,d\mu_y(x)\,d\mu_y(x')$ is
measurable (Borel kernel, fibre Fubini for the disintegration), so $\langle p_N(A_y^*A_y)\xi(y),\eta(y)\rangle$ is
measurable for every polynomial $p_N$, and $Q_y$ is the strong limit of uniformly bounded $p_N(A_y^*A_y)$.

---

## 2. Lemma S, with complete proof

**Lemma S (measurable fibre-orthonormal-basis selection).** *Let $(H_y,\Gamma)$ be a measurable field of separable
Hilbert spaces over a standard probability space $(Y,\nu)$, and let $y\mapsto Q_y$ be a measurable, contractive field
of orthogonal projections of finite rank. Then*

*(a) $y\mapsto\operatorname{rank}Q_y$ is Borel;*

*(b) if $\operatorname{rank}Q_y = d$ for $\nu$-almost every $y$ and some $d\ge1$, then there exist measurable sections
$e_1,\dots,e_d$ such that for $\nu$-almost every $y$, $(e_1(y),\dots,e_d(y))$ is an orthonormal basis of
$\operatorname{ran}Q_y$; moreover $\lVert e_i(y)\rVert = 1$ for all $i$ and a.e. $y$.*

*Proof.* Fix an enumeration $\gamma_1,\gamma_2,\dots$ of $\Gamma$. We construct the sections recursively. Suppose
$e_1,\dots,e_k$ have been constructed as measurable sections. For $j\ge1$ put
$$\zeta^{(j)}_{k+1} := \gamma_j - \sum_{m=1}^{k}\langle\gamma_j,e_m\rangle\,e_m ,$$
a measurable section by Lemma 1.2 (finite linear combination of measurable sections with measurable coefficients),
and let $Q\zeta^{(j)}_{k+1}$ also denote the corresponding section, which is measurable by Lemma 1.2(iii). Set
$$j_{k+1}(y) := \min\Big\{j\ge1 : \big\lVert Q_y\zeta^{(j)}_{k+1}(y)\big\rVert_{H_y}\ \ge\ \tfrac34\Big\},$$
with the convention $j_{k+1}(y) = \infty$ if the set is empty, and
$$e_{k+1}(y) := \begin{cases}
\dfrac{Q_y\zeta^{(j_{k+1}(y))}_{k+1}(y)}{\lVert Q_y\zeta^{(j_{k+1}(y))}_{k+1}(y)\rVert_{H_y}} & \text{if } j_{k+1}(y)<\infty,\\[1ex]
0 & \text{otherwise.}\end{cases}$$

**Step 1 ($j_{k+1}$ and $e_{k+1}$ are measurable).** Since $\zeta^{(j)}_{k+1}$ and hence $Q\zeta^{(j)}_{k+1}$ are
measurable sections, $y\mapsto\lVert Q_y\zeta^{(j)}_{k+1}(y)\rVert$ is measurable by Lemma 1.2(i). Hence
$$\{y : j_{k+1}(y) = j\} = \big\{\lVert Q_y\zeta^{(j)}_{k+1}(y)\rVert\ge\tfrac34\big\}\cap
\bigcap_{j'<j}\big\{\lVert Q_y\zeta^{(j')}_{k+1}(y)\rVert<\tfrac34\big\}$$
is Borel, so $j_{k+1}$ is measurable; on $\{j_{k+1}<\infty\}$ it is a measurable section by finitely many measurable
choices, and the denominator is $\ge\tfrac34$, so $e_{k+1}$ is a measurable section by Lemma 1.2(i),(iii).

**Step 2 (the test succeeds whenever there is room).** Suppose $e_1(y),\dots,e_k(y)$ are orthonormal in
$\operatorname{ran}Q_y$ and $\dim\operatorname{ran}Q_y\ge k+1$. Choose a unit $w\in\operatorname{ran}Q_y$ with
$w\perp e_m(y)$ for $m\le k$; by (F2) choose $j$ with $\lVert\gamma_j(y)-w\rVert<1/4$. Since $w\perp e_m(y)$,
$$\zeta^{(j)}_{k+1}(y) - w = (\gamma_j(y)-w) - \sum_{m=1}^k\langle\gamma_j(y)-w,e_m(y)\rangle e_m(y)
= (\gamma_j(y)-w)^{\perp},$$
the orthogonal projection of $\gamma_j(y)-w$ onto the orthocomplement of $\operatorname{span}\{e_1(y),\dots,e_k(y)\}$;
its norm is therefore at most $\lVert\gamma_j(y)-w\rVert<1/4$. Since $Q_y$ is an orthogonal projection fixing $w$
and $\lVert Q_y\rVert\le1$,
$$\big\lVert Q_y\zeta^{(j)}_{k+1}(y)\big\rVert \ \ge\ \lVert Q_yw\rVert - \big\lVert Q_y\big(\zeta^{(j)}_{k+1}(y)-w\big)\big\rVert
\ \ge\ 1-\tfrac14\ =\ \tfrac34 .$$
So $j_{k+1}(y)<\infty$. Consequently $e_{k+1}(y)\ne0$, $\lVert e_{k+1}(y)\rVert = 1$, $e_{k+1}(y)\in\operatorname{ran}Q_y$,
and $\langle e_{k+1}(y),e_m(y)\rangle = 0$ for $m\le k$ (as $Q_y\zeta^{(j)}_{k+1}(y)\perp e_m(y)$: indeed
$\zeta^{(j)}_{k+1}(y)\perp e_m(y)$ and $e_m(y)\in\operatorname{ran}Q_y$). So the vectors remain orthonormal.

**Step 3 (the test fails once the range is exhausted).** Suppose $\dim\operatorname{ran}Q_y = k$ and
$e_1(y),\dots,e_k(y)$ span $\operatorname{ran}Q_y$. Then $\zeta^{(j)}_{k+1}(y)\perp\operatorname{ran}Q_y$ for every
$j$, so $Q_y\zeta^{(j)}_{k+1}(y) = 0 < \tfrac34$ and $j_{k+1}(y) = \infty$, $e_{k+1}(y) = 0$.

**Step 4 (conclusion).** Assume $\operatorname{rank}Q_y = d$ for $\nu$-a.e. $y$ and let $Y_0$ be a conull set on which
(F2) holds and $\operatorname{rank}Q_y = d$. For $y\in Y_0$, Steps 2 and 3 applied inductively show: if
$k<d$ then $j_{k+1}(y)<\infty$ and $e_1(y),\dots,e_{k+1}(y)$ are orthonormal in $\operatorname{ran}Q_y$; if $k = d$
then $e_1(y),\dots,e_d(y)$ span $\operatorname{ran}Q_y$ (they are $d$ orthonormal vectors in a $d$-dimensional space)
and $j_{d+1}(y) = \infty$. Hence $(e_1(y),\dots,e_d(y))$ is an orthonormal basis of $\operatorname{ran}Q_y$ for every
$y\in Y_0$, proving (b). For (a): Step 2 gives $j_k(y)<\infty$ whenever $\operatorname{rank}Q_y\ge k$; conversely,
if $\operatorname{rank}Q_y = k' < k$ then $e_1,\dots,e_{k'}$ span $\operatorname{ran}Q_y$ by Step 2, Step 3 gives
$j_{k'+1}(y) = \infty$, and the same test is repeated at every later stage (because $e_{k'+1}(y) = 0$), so
$j_m(y) = \infty$ for all $m>k'$ and in particular $j_k(y) = \infty$. Hence
$\{y : \operatorname{rank}Q_y\ge k\} = \{j_k<\infty\}$, which is Borel for each $k$. $\square$

**Remark 2.1 (what is used, and what is not).** The proof uses only: separability of $H_y$, the two axioms (F1)–(F2),
orthogonality of $Q_y$, and $\lVert Q_y\rVert\le1$. It uses no compactness of $Q_y$, no symmetry, no continuity in $y$,
no measurability of $y\mapsto Q_y$ beyond Definition 1.3, and no countability of $Y$. The constants $1/4$, $3/4$,
$1$ are the only estimates, and they are uniform in $y$ and in $k$.

---

## 3. Application: the measurability layer of Lemma 3.1, complete

We now run the paper's construction with Lemma S inserted, so that no assertion is left unchecked. Retain the
setting of Remark 1.4 and let $L\in L^\infty(\mu\times_Y\mu)$ be $K$-invariant with both coordinate conditional
expectations $0$ (paper §3.1: this is how a non-ergodic relative product $X\times_YX$ produces a kernel).

**(3.1) The fibre operators.** For a.e. $y$ let $A_y$ be the integral operator on $H_y$ with kernel
$L_y(x,x') = L(x,x')$. Then $\lVert A_y\rVert_{HS}^2 = \iint\lvert L\rvert^2d\mu_y\,d\mu_y$, so
$$\int_Y\lVert A_y\rVert^2_{HS}\,d\nu(y) = \lVert L\rVert^2_{L^2(\mu\times_Y\mu)},\qquad
\lVert A_y\rVert_{HS}\le\lVert L\rVert_\infty \ \text{a.e.}$$
Also $A_y1 = A_y^*1 = 0$ because the two coordinate conditional expectations of $L$ vanish.

**(3.2) A level $\delta>0$.** Choose $\delta = 1/n$ with $n$ such that
$Q_y := \mathbf 1_{(\delta,\infty)}(A_y^*A_y)$ is non-zero on a set of $y$ of positive measure. Such an $n$ exists:
if $\mathbf 1_{(1/n,\infty)}(A_y^*A_y) = 0$ a.e. for every $n$, then $A_y^*A_y = 0$ a.e., hence $A_y = 0$ a.e. by the
$C^*$-identity, contradicting $\int_Y\lVert A_y\rVert^2_{HS}d\nu = \lVert L\rVert^2_{L^2}>0$.

**(3.3) Finite rank, uniformly.** Since $\mathbf 1_{(\delta,\infty)}(A_y^*A_y)\le\delta^{-1}A_y^*A_y$ and
$\operatorname{tr}(A_y^*A_y) = \lVert A_y\rVert^2_{HS}$,
$$\operatorname{rank}Q_y\ \le\ \delta^{-1}\lVert A_y\rVert^2_{HS}\ \le\ \delta^{-1}\lVert L\rVert_\infty^2
\qquad\text{for a.e. } y .$$
$Q_y$ is an orthogonal projection with $\lVert Q_y\rVert\le1$, and the field is measurable (Remark 1.4).

**(3.4) The rank is constant.** The field is $K$-equivariant: $Q_{ky} = U_kQ_yU_k^{-1}$ (the field $A_y$ is
equivariant because $L$ is $K$-invariant, and functional calculus commutes with unitary conjugation), so
$\operatorname{rank}Q_{ky} = \operatorname{rank}Q_y$. By Lemma S(a) the function $y\mapsto\operatorname{rank}Q_y$ is
Borel and $K$-invariant, hence constant a.e. by ergodicity of $Y$ (a factor of the ergodic system $X$). Since $Q_y\neq0$
on a set of positive measure, the constant is $d\ge1$.

**(3.5) The sections.** Lemma S(b) now applies and gives measurable sections $e_1,\dots,e_d$ with
$\lVert e_i(y)\rVert_{H_y} = 1$ and $(e_1(y),\dots,e_d(y))$ an orthonormal basis of
$\operatorname{ran}Q_y$ for a.e. $y$. Since $Q_y1 = 0$ (because $A_y1 = 0$), each $e_i(y)\perp1$, i.e.
$\int e_i\,d\mu_y = 0$.

**(3.6) Boundedness, (3.1) of the paper.** For $k\in K$ put $\tilde e_i := U_ke_i$, whose fibre over $y$ is
$U_k\big(e_i(k^{-1}y)\big)$; this lies in $\operatorname{ran}Q_y$ because $e_i(k^{-1}y)\in\operatorname{ran}Q_{k^{-1}y}$
and $Q_y = U_kQ_{k^{-1}y}U_k^{-1}$, and $(\tilde e_1(y),\dots,\tilde e_d(y))$ is orthonormal because $U_k$ is unitary
from $H_{k^{-1}y}$ onto $H_y$. As $\operatorname{rank}Q_y = d$, it is an orthonormal basis, so there is a unitary
$d\times d$ matrix $c(k,y)$ with $\tilde e_i(y) = \sum_jc_{ij}(k,y)e_j(y)$ for a.e. $y$. Hence the measurable function
$\Phi(x) := \sum_{i=1}^d\lvert e_i(x)\rvert^2$ satisfies, for $y = y(x)$,
$$\Phi(kx) = \sum_i\lvert e_i(kx)\rvert^2 = \sum_i\lvert\tilde e_i(x)\rvert^2
= \sum_i\Big\lvert\sum_jc_{ij}(k,y)e_j(x)\Big\rvert^2 = \sum_j\lvert e_j(x)\rvert^2 = \Phi(x),$$
using unitarity of $c(k,y)$. So $\Phi$ is $K$-invariant, and
$$\int_X\Phi\,d\mu = \sum_{i=1}^d\int_Y\lVert e_i(y)\rVert^2_{H_y}d\nu(y) = d .$$
Ergodicity of $X$ gives $\Phi = d$ a.e., i.e. (3.1), and in particular $\lVert e_i\rVert_\infty\le\sqrt d$.

**(3.7) The extension factor.** Let $Y' = Y\vee\sigma(e_1,\dots,e_d)$, a standard factor of $X$. It is a *strict*
extension: $\mathbb E(e_i\mid Y) = \int e_i\,d\mu_y = 0$ in fibre norm by (3.5), whereas
$\lVert e_i\rVert_{L^2(X)} = 1$, so $e_i\notin L^2(Y)$.

**(3.8) Property (2.6), with explicit basis and bound.** Bounded polynomials in $e_i,\bar e_i$ with coefficients in
$L^\infty(Y)$ form a bounded unital conjugation-closed algebra generating $Y'$, hence are dense in $L^2(Y')$
(Stone–Weierstrass on the finite-dimensional distributions, then the monotone class theorem for countably many
generators). Fix a bounded $H\in L^2(Y')$ and a polynomial $P$ of degree $N$ with $\lVert H-P\rVert_2<\varepsilon$
and coefficient sup norms at most $M$. On the fibre over $y$, $U_k$ acts through the unitary matrix $c(k,\cdot)$, so
$U_kP$ is a finite sum $\sum_{r=1}^{q}b^k_rH_r$ where $H_1,\dots,H_q$ are the monomials of $P$ and each
$\lVert b^k_r\rVert_\infty$ is bounded by a constant $B$ depending only on the degree $N$ and on $M$ (entries of a
unitary matrix have modulus $\le1$, and the expansion of a rotated monomial of degree $N$ has at most $(d+1)^N$ terms).
Since $U_k$ is an isometry of $L^2$,
$$\Big\lVert U_kH-\sum_{r=1}^q b^k_rH_r\Big\rVert_2 \le \lVert U_kH-U_kP\rVert_2 + 0 = \lVert H-P\rVert_2 < \varepsilon ,$$
which is exactly (2.6), with the basis $H_r$ and the bound $M$ fixed before $k$ is chosen.

**(3.9) The iteration stops.** If the construction could be repeated at every successor stage through all countable
ordinals, choosing a unit vector $v_{\alpha+1}\in L^2(Y_{\alpha+1})\ominus L^2(Y_\alpha)$ at each stage would give
$\aleph_1$ pairwise orthogonal unit vectors in the separable space $L^2(X)$ (nestedness gives
$v_{\alpha+1}\perp v_{\beta+1}$ for $\alpha\ne\beta$), which is impossible. So the process stops at a countable
ordinal $\eta$, and by the stopping rule $X\times_{Y_\eta}X$ is ergodic.

**Conclusion.** Lemma 3.1 of the paper is proved, with the black box replaced by Lemma S and the estimates
$\delta^{-1}\lVert L\rVert_\infty^2$ (rank), $d$ (bound (3.1)), $\sqrt d$ (sup norm) and $\varepsilon$ ((2.6))
explicit.

---

## 4. Why this is the right black box to close

The paper's Lemma 3.1 is the structural heart of the rigidity theorem: it produces the factor above which
conditional correlations decouple, which is what Lemma 2.7 and Lemma 3.2 consume. The only assertion in it that is
not a standard argument is the selection sentence quoted in §0; that assertion is where a hidden measurable-choice
or non-measurability error would sit, and it is exactly what Lemma S settles, with a *canonical* (first-fit) choice
and a uniform spectral gap $3/4-1/4$.

---

## 5. Retractions

For the record, two claims in my first report were wrong and are withdrawn.

1. **Retracted:** "In the proof of Lemma 3.2, *averages of $a(h)^2$ tend to zero* should read *averages of $a(h)$*."
   The paper defines $a(h) = \lVert PF_{j^*,h}\rVert_2$ in (3.7) — the $L^2$ **norm**, not its square. With
   $v = \bar v_{j^*}$, $w = v_{j^*}$, $d = n_{j^*}$, the pair criterion (3.3) gives
   $\operatorname{Avg}_u\lVert P(\bar v_{j^*}U_{u^{n_{j^*}}}v_{j^*})\rVert^2\to0$, and
   $P(v_{j^*}) = 0$ together with unitary invariance identifies this with
   $\operatorname{Avg}_u a(u)^2\to0$; Cauchy–Schwarz then gives $\operatorname{Avg}_ua(u)\to0$, which is what (3.8)
   uses. The paper's sentence is correct as printed and there is nothing to repair.

2. **Retracted:** "The proof of Lemma 3.3 identifies $\psi_{A-Bu^2}$ with $\psi_{-L+(A-B)u+Lu^2}$." The paper does not
   make that identification. It applies (3.2) with exponents $0,1,2$ to the *second side* of (3.14), i.e. to
   $R_u = -L+(A-B)u+Lu^2$, obtaining $\lVert P\psi_{R_u}\rVert_2^2\le\lVert g_{-L}U_ug_{A-B}U_{u^2}g_L\rVert_2^2\le
   \lVert g_{A-B}\rVert_2^2 = m(\lvert A-B\rvert)$ from $\lvert g_{\pm L}\rvert\le1$ — no character identity is used
   in that step. The comparison with the first side is then the *modulus* identity (3.14) together with the paper's
   own next sentence, "equal moduli give equal m-values", which is radiality of $m$; so
   $m(A-Bu^2) = m(\lvert R_u\rvert)$ and (3.12) follows. No gap, no repair needed.

Nothing in §§1–4 above depends on either withdrawn claim.
