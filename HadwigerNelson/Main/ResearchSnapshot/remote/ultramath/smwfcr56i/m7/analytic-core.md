# The analytic core of "The Euclidean plane is not five-colorable": a self-contained verification

This document referees and re-derives **§2, §3 and §4 of the paper** (the spectral/ergodic core), i.e. the two
statements

* **Theorem B** (= paper Theorem 2.3, *Rigidity of wild character laws*). Every $K$-invariant Borel probability
  $\nu$ on $D = \widehat{E}_{\mathrm{disc}}$ with $\nu(C) = 0$ is normalised Haar measure $m_D$.
* **Theorem A** (= paper Theorem 1.3, *Transfer of colorability*). For every positive integer $k$, a proper
  $k$-colouring of $\mathbb{R}^2$ exists iff a weak measurable $k$-colouring (paper Definition 1.2) exists.

Everything is in $\mathsf{ZFC}$. The paper's lower bound $\chi(\mathbb{R}^2)\ge 6$ is
Theorem B $\Rightarrow$ (no weak measurable 5-colouring, paper Theorem 1.4, which lives in §§5–8) $\Rightarrow$ (no
proper 5-colouring, Theorem A). I verify the two arrows that are in §2–§4 and I do **not** verify §§5–8
(see §5 below).

Notation follows the paper. Each numbered step below is either proved in full, or reduced to one of the classical
theorems listed in §0.2 with an exact statement. Nothing is left at the level of "routine".

---

## 0. Verdict, and what is assumed

### 0.1 Verdict table for §2–§4

| # | Claim | Location in paper | Verdict |
|---|-------|-------------------|---------|
| 1 | $\langle K\rangle = E$; every $z\in E$ with $\lvert z\rvert\le 2$ is a sum of two elements of $K$ | not stated (implicit) | **new, proved here** (Lemma 1.3). Used to justify that Theorem B is not vacuous |
| 2 | $C$ is a dense proper Borel subgroup and $m_D(C)=0$ | implicit in §2.1 | **proved here** (Lemma 1.2(5)) |
| 3 | Lemma 2.4 (cosets of $C$; the events $L_a$) | §2.1 | **correct**, proof completed here (no gap found) |
| 4 | Lemma 2.5 (vanishing line average) | §2.2 | **correct**, proof completed here (no gap found) |
| 5 | Lemma 2.6 (measurable, isometry-equivariant minimiser) | §2.3 | **correct**; Borel-measurability of $J_\lambda(s)$ in $\lambda$ is even continuity in the weak topology — see remark 2.6.4 |
| 6 | Lemma 2.7 (relative singularity, "universal transfinite induction") | §2.4 | **correct**; the induction statement is written out with all quantifiers in §2.4.0, and the induction hypothesis is applied in exactly one place, Step 5 (prepared by the reduction in Step 1) |
| 7 | Lemma 3.1 (compact tower) | §3.1 | **correct**, but the selection of measurable fibre-orthonormal bases is asserted in three lines; a complete proof is supplied in Lemma 3.1.5 |
| 8 | Lemma 3.2 (conditional multiple averages) | §3.2 | **correct as printed**: $a(h)=\lVert PF_{j^*,h}\rVert_2$ is the norm, the pair criterion gives $\operatorname{Avg}a^2\to0$, and Cauchy–Schwarz gives $\operatorname{Avg}a\to0$, exactly as the paper says (Remark 3.2.6) |
| 9 | Lemma 3.3 (radial identities, (3.12)–(3.13)) | §3.3 | **correct as printed**: (3.2) with exponents $0,1,2$ is applied to the second side $R_u=-L+(A-B)u+Lu^2$ of (3.14) (no character identity is asserted), the bound uses $\lvert g_{\pm L}\rvert\le1$, and the two sides are compared by the modulus identity (3.14) plus radiality of $m$ (Remark 3.3.7) |
| 10 | Lemmas 3.4, 3.5 and the completion of Theorem B | §3.4–3.5 | **correct**, no gap found |
| 11 | Lemma 4.1, Prop. 4.2, Lemma 4.3, Theorem A | §4 | **correct**, no gap found; sharpened in §4.2 (the weak colouring can be taken Borel) |

**No false lemma was found in §2–§4, and no step in it needs repair.** (Two items in an earlier version of this
file, concerning $a(h)$ in Lemma 3.2 and concerning (3.14) in Lemma 3.3, were withdrawn as misreadings; see §4.0.)
Consequently the analytic core is sound and the whole mathematical burden of
$\chi(\mathbb{R}^2)\ge 6$ rests on §§5–8 (paper Theorem 1.4).

### 0.2 Classical theorems used (and used only)

* **(T1) Pontryagin duality / Fourier uniqueness.** For a countable discrete abelian $E$, the characters
  $\psi_z$, $z\in E$, are a unital conjugation-closed $\mathbb{C}$-algebra separating points of $D=\widehat E$;
  hence they are uniformly dense in $C(D)$ (Stone–Weierstrass), and two finite regular Borel measures on $D$ with
  the same Fourier coefficients coincide.
* **(T2) Spectral theorem for a single unitary operator / for a unitary representation of a countable discrete
  abelian group.** For unitary $(T_z)_{z\in E}$ on a Hilbert space $\mathcal H$ and $v\in\mathcal H$ there is a
  finite positive measure $\lambda_v$ on $D$ with $\langle v,T_zv\rangle=\int\psi_z\,d\lambda_v$ and
  $\lVert T_zv-v\rVert_2^2=\int\lvert\psi_z-1\rvert^2\,d\lambda_v$.
* **(T3) Bochner's theorem** on $\mathbb{R}^2$ (and on $\mathbb{R}$): a continuous positive-definite function is the
  Fourier transform of a unique finite positive measure.
* **(T4) Amenability of abelian groups.** A countable abelian group carries a two-sided invariant mean on
  $\ell^\infty$, and admits a Følner sequence; every Følner sequence works in the mean ergodic theorem.
* **(T5) Mean ergodic theorem** for a unitary representation of a countable abelian group along every Følner
  sequence: $\mathrm{Avg}_{g\in\Phi_N}U_g f\to P_{\mathrm{inv}}f$ in norm.
* **(T6) Disintegration.** A factor map $\pi:X\to Y$ of standard Borel probability spaces admits a probability
  kernel $y\mapsto\mu_y$, concentrated on $\pi^{-1}(y)$, with $\mu=\int\mu_y\,d\nu(y)$; it is unique a.e. and
  equivariant when $\pi$ is (Tao, Theorem 4 and Remark 5, as cited by the paper).
* **(T7) Lebesgue differentiation / density points** (Besicovitch) in $\mathbb{R}^2$.
* **(T8) de Bruijn–Erdős compactness** (paper reference [4]).
* **(T9)** Steinhaus' theorem in the form: a Borel subgroup of a compact group with positive Haar measure is open.

Each of (T1)–(T9) is a standard theorem; the paper cites them and so do I. No statement equivalent in strength to
$\chi(\mathbb{R}^2)\ge 6$ is assumed anywhere.

---

## 1. The algebraic setting

### 1.1 Definitions

$F = \overline{\mathbb{Q}}\cap\mathbb{R}$ (real algebraic numbers, a real closed subfield of $\mathbb{R}$),
$E = F(i) = F + iF$, $K = \{u\in E : u\bar u = 1\}$. $E$ is an additive discrete group, $K$ a multiplicative
discrete group. $D = \widehat{E}_{\mathrm{disc}}$ is the compact abelian group of all homomorphisms
$E\to\mathbb{T}$; we write it additively, $(d+d')(z) = d(z)d'(z)$, and set
$$\psi_z(d) = d(z),\qquad (ad)(z) = d(az)\ \ (a\in E),\qquad (ud)(z) = d(uz)\ \ (u\in K).$$
$j:\mathbb{R}^2\to D$, $j(\xi)(z) = e^{i\,\xi\cdot z}$ (the dot product is the real scalar product of $z$ viewed in
$\mathbb{C}\cong\mathbb{R}^2$), and $C = j(\mathbb{R}^2)$.

$\nu$ is **wild** if $\nu(C) = 0$. $m_D$ is normalised Haar measure.

### 1.2 Elementary structural facts

**Lemma 1.1.** (1) $E$ is a $2$-dimensional $F$-vector space and $E\cap\mathbb{R} = F$.
(2) $K$ is an abelian group, and for $u\in K$, $u\neq 0$, so $u^{-1} = \bar u\in K$.
(3) $K$ is divisible: for $n\ge 1$ and $u\in K$ there is $v\in K$ with $v^n = u$.
(4) For $z\in E$, $\lvert z\rvert = \sqrt{z\bar z}\in F_{\ge 0}$.
(5) If $z,w\in E$ are nonzero with $\lvert z\rvert = \lvert w\rvert$, then $w = uz$ for some $u\in K$.

*Proof.* (1) is $E = F + iF$ with $i\notin F$; a real element $a+ib$ has $b = 0$.
(2) clear. (3) a complex $n$-th root of an algebraic number of modulus $1$ is algebraic (the polynomial
$X^n-u$ has algebraic coefficients) and of modulus $1$; negative powers are inverses. (4) $\lvert z\rvert^2 = z\bar z\in F$
and $F$ is real closed, so $\lvert z\rvert\in F$. (5) $u = w/z\in E$ and $\lvert u\rvert = 1$, so $u\in K$. $\square$

**Lemma 1.2** (the group $C$). (1) $j$ is a continuous injective homomorphism; $\psi_z\circ j$ is the continuous
character $\xi\mapsto e^{i\xi\cdot z}$ of $\mathbb{R}^2$, so $\{\psi_z\circ j\}_{z\in E}$ separates points of
$\mathbb{R}^2$.
(2) $C = \bigcup_{n} j(\overline{B}(0,n))$ is a Borel subgroup of $D$; $j^{-1}:C\to\mathbb{R}^2$ is Borel.
(3) $C$ is dense in $D$.
(4) $C\neq D$.
(5) $m_D(C) = 0$; in particular $m_D$ is wild.
(6) $C$ is $K$-invariant, indeed $k\,j(\xi) = j(k^{-1}\xi)$; on the frequency parameter the action of $k\in K$ is
the orthogonal map $\xi\mapsto k^{-1}\xi$.

*Proof.* (1) $j(\xi+\eta) = j(\xi)j(\eta)$; injectivity: if $e^{i\xi\cdot z} = 1$ for all $z\in E$ then taking
$z\in\mathbb{Q}^2\subset E$ gives $\xi = 0$; continuity and separation are clear.
(2) images of compact sets are compact, so $C$ is $\sigma$-compact; the inverse on $j(\overline B(0,n))$ is the
continuous inverse of a continuous injection on a compact set.
(3) Let $H\subseteq E$ be the annihilator $\{z : j(\xi)(z) = 1\ \forall\xi\in\mathbb{R}^2\} = \{z : \xi\cdot z\in
2\pi\mathbb{Z}\ \forall\xi\}$. Replacing $\xi$ by $t\xi$, $t\in\mathbb{R}$, gives $\xi\cdot z = 0$ for all $\xi$, so
$z = 0$; thus $H = 0$, and $\overline{C} = H^{\perp} = D$ by duality.
(4) $C\neq D$: explicit witness below. (4') $\;$*Explicit* $d\notin C$. Since $E = F(i)$ is countable, $E$ is a
$\mathbb{Q}$-vector space of countable dimension and $\lvert D\rvert = \lvert\mathbb{T}\rvert^{\aleph_0} = \mathfrak c =
\lvert C\rvert$, so cardinality does **not** separate $C$ from $D$; an explicit character is needed. The elements
$1,\ i,\ i/\sqrt2$ of $E$ (note $\sqrt2/2\in F$) are $\mathbb{Q}$-linearly independent: if $a+bi+ci/\sqrt2 = 0$ with
$a,b,c\in\mathbb{Q}$ then $a = 0$ and $b+c/\sqrt2 = 0$, so $c = 0 = b$ (else $\sqrt2\in\mathbb{Q}$). Extend them to a
$\mathbb{Q}$-basis of $E$ and let $f:E\to\mathbb{R}$ be the $\mathbb{Q}$-linear map with $f(1) = 0$, $f(i) = \sqrt2$,
$f(i/\sqrt2) = 0$, $f = 0$ on the remaining basis elements. Then $d := e^{2\pi if}$ is a character of $E$, i.e.
$d\in D$. If $d = j(\xi)$ then $h(z) := f(z) - \xi\cdot z/(2\pi)$ is $\mathbb{Q}$-linear and integer-valued, hence
$h = 0$ (as $h(z/n) = h(z)/n\in\mathbb{Z}$ for all $n$), so $f$ would be $\mathbb{R}$-linear; but then
$\sqrt2 = f(i) = f(\sqrt2\cdot i/\sqrt2) = \sqrt2f(i/\sqrt2) = 0$, a contradiction. So $d\notin C$.
(5) $C$ is a Borel subgroup of the compact group $D$; if $m_D(C) > 0$ then by (T9) $C$ is open and closed, hence
$C = D$ by (3), contradicting (4). So $m_D(C) = 0$.
(6) $(uj(\xi))(z) = j(\xi)(uz) = e^{i\xi\cdot(uz)} = e^{i(\bar u\xi)\cdot z} = j(\bar u\xi)(z)$. $\square$

**Lemma 1.3** (unit-sum lemma; cf. paper §2.4, "each $\lvert x_j\rvert<1$ is a sum of two elements of $K$").
Let $z\in E$ with $\lvert z\rvert\le 2$. Then there are $u,v\in K$ with
$$u = \frac z2 + i\,\frac{z}{\lvert z\rvert}\sqrt{1-\tfrac{\lvert z\rvert^2}{4}},\qquad
  v = \frac z2 - i\,\frac{z}{\lvert z\rvert}\sqrt{1-\tfrac{\lvert z\rvert^2}{4}},\qquad u+v = z,\quad \lvert u\rvert = \lvert v\rvert = 1$$
(the formula for $z = 0$ is read as $u = 1, v = -1$). Consequently:

*(i)* $\langle K\rangle = E$ (the subgroup of $(E,+)$ generated by $K$ is all of $E$);
*(ii)* the only $K$-invariant subgroups of $(E,+)$ are $\{0\}$ and $E$;
*(iii)* the only $K$-invariant closed subgroups of $D$ are $\{0\}$ and $D$; consequently the only $K$-invariant
measures on $D$ of the form "Haar measure of a closed subgroup or of one of its cosets" are $m_D$ and the point mass
$\delta_0$ at the trivial character, and $\delta_0$ is **not** wild ($j(0) = 0\in C$). So the standard guess at a
counterexample to Theorem B — a coset-Haar measure supported off $C$ — cannot exist.

*Proof.* $\lvert z\rvert^2 = z\bar z\in F$, so $\lvert z\rvert\in F$ (Lemma 1.1(4)), $z/\lvert z\rvert\in E$,
$1-\lvert z\rvert^2/4\in F_{\ge0}$ and its square root lies in $F$ ($F$ real closed); thus $u,v\in E$ and
$\lvert u\rvert = \lvert v\rvert = 1$, i.e. $u,v\in K$. Put $\zeta = z/2$ and $\eta = i\tfrac z{\lvert z\rvert}s$ with
$s = \sqrt{1-\lvert z\rvert^2/4}\in\mathbb{R}$; then $\lvert u\rvert^2 = \lvert\zeta\rvert^2+s^2+2\mathrm{Re}(\bar\zeta\eta)
= \tfrac{\lvert z\rvert^2}{4}+1-\tfrac{\lvert z\rvert^2}{4}+\tfrac{2s}{\lvert z\rvert}\mathrm{Re}(\tfrac{\bar z}{2}iz)
= 1+\tfrac{s}{\lvert z\rvert}\mathrm{Re}(i\lvert z\rvert^2/2) = 1$, and $\lvert v\rvert = 1$, $u+v = z$ similarly.

*(i)* For $0\neq z\in E$ choose $n\in\mathbb{N}$ with $\lvert z\rvert/n\le 2$; then $z = n\cdot(z/n)$ is a sum of
$2n$ elements of $K$. *(ii)* A nonzero $K$-invariant subgroup contains $Kz$ for some $z\neq 0$, hence $u+(-v)$ for
all $u,v\in K$; by (i) these generate $E$. *(iii)* Closed subgroups $H\subseteq D$ are exactly the annihilators
$M^{\perp}$, $M\subseteq E$, and $H$ is $K$-invariant iff $M$ is ($M = \{z : d(z)=1\ \forall d\in H\}$; use
$(ud)(z) = d(uz)$). By (ii), $H\neq\{0\}$ forces $M = 0$, i.e. $H = D$. $\square$

**Remark 1.4** ($K$-invariance cannot be dropped in Theorem B). For $d\notin C$ the point mass $\delta_d$ is a Borel
probability with $\delta_d(C) = 0$ and $\delta_d\neq m_D$, but $\delta_d$ is not $K$-invariant. Hence Theorem B is a
genuine statement about the *action* of $K$, and no counterexample of the "coset-Haar" type exists by Lemma 1.3(iii).

---

## 2. Haar rigidity (Theorem B)

Throughout, $\nu$ is a $K$-invariant Borel probability on $D$ and $f^\nu(z) = \int_D\psi_z\,d\nu$.

### 2.1 Lemma 2.4 (no mass on cosets of $C$; the events $L_a$)

**Lemma 2.4** (paper §2.1). *Let $\nu$ be wild. Then*

*(a) every coset $d+C$ of $C$ has $\nu$-measure $0$;*
*(b) the law $\mu$ of $d-d'$ for two independent $\nu$-samples satisfies $\mu(C) = 0$;*
*(c) for every $a\in E\setminus\{0\}$ the set $L_a = \{d\in D : t\mapsto d(at)\ \text{is continuous on } F \text{ in the
usual topology}\}$ is Borel and $\nu(L_a) = 0$.*

*Proof.* (a) Suppose $\nu(d_0+C) = p > 0$. Since $C$ is $K$-invariant, $K$ permutes the cosets of $C$
transitively on the orbit, and every coset in the orbit $\mathcal O = \{ud_0 + C : u\in K\}$ has mass $p$. The
cosets are pairwise disjoint, so $\lvert\mathcal O\rvert\le 1/p < \infty$. Hence the action of $K$ on $\mathcal O$
gives a homomorphism $K\to \mathrm{Sym}(\mathcal O)$ into a finite abelian group. $K$ is divisible (Lemma 1.1(3)),
and a quotient of a divisible group is divisible; a finite divisible abelian group is trivial. So every $u\in K$
fixes $d_0+C$, i.e. $(u-1)d_0\in C$ for all $u\in K$. Pick $u\in K$, $u\neq 1$ (e.g. $u = i$). Since $E$ is a field
and $u-1\neq 0$, $w = (u-1)^{-1}\in E$; from $(u-1)d_0\in C$, i.e. $z\mapsto d_0((u-1)z) = j(\xi)(z)$ for some
$\xi$, we get $d_0(y) = d_0((u-1)w y) = j(\xi)(wy) = e^{i\xi\cdot (wy)}$ for all $y\in E$, and $y\mapsto\xi\cdot(wy)$
is a real-linear functional, so $d_0\in C$, contradicting wildness. Hence $p = 0$.
(b) $\mu(C) = \int_D\nu(d+C)\,d\nu(d) = 0$ by (a) (the relation $d'-d\in C$ is Borel in $(d,d')$).
(c) $\rho_a:D\to \widehat{F}_{\mathrm{disc}}$, $\rho_a(d)(t) = d(at)$, is a continuous homomorphism; the set of
continuous characters of $F_{\mathrm{disc}}$ is $\{t\mapsto e^{i\lambda t} : \lambda\in\mathbb{R}\} = \Phi$, the
continuous injective image of $\mathbb{R}$, hence Borel ($\sigma$-compact), and $L_a = \rho_a^{-1}(\Phi)$ is Borel.
For the vanishing: if $d\in L_a\cap L_b$ with $aF$, $bF$ non-parallel then $a,b$ are an $F$-basis of $E$ (they are
$F$-independent: otherwise $b/a\in F\subseteq\mathbb{R}$ and the lines are parallel; note $E\cap\mathbb{R} = F$).
Writing $z = at+bs$ we get $d(z) = e^{i\lambda t}e^{i\eta s}$, and $(t,s)\mapsto\lambda t+\eta s$ is
$\mathbb{Q}$-linear and hence $\mathbb{R}$-linear on $E\cong\mathbb{R}^2$ (both lines are real), so it is
$\xi\cdot z$ for some $\xi\in\mathbb{R}^2$; thus $L_a\cap L_b\subseteq C$. Now fix $a\neq 0$: the lines $uaF$ for
$u\in K\setminus\mathbb{R}$ are pairwise distinct real lines (if $uaF = u'aF$ then $u'/u\in\mathbb{R}\cap E = F$,
so $u' = (u'/u)u$ with $\lvert u'\rvert = \lvert u\rvert = 1$ forces $u'/u = \pm1$, and $\pm u$ give the same line).
All $L_{ua} = uL_a$ have the same $\nu$-measure, and any $n$ of them are pairwise disjoint modulo the
$\nu$-null set $C\supseteq L_{ua}\cap L_{u'a}$. Hence $n\,\nu(L_a)\le 1$ for every $n$, so $\nu(L_a) = 0$. $\square$

### 2.2 Lemma 2.5 (a line average that needs no measurability)

Fix, by (T4), a two-sided translation-invariant mean $\mathfrak m$ on the bounded functions on the discrete group
$F/\mathbb{Z}$. For bounded $h:F\to\mathbb{C}$ with bounded support set
$$I(h) = \mathfrak m\Big(t+\mathbb{Z}\mapsto \sum_{k\in\mathbb{Z}}h(t+k)\Big).$$
Then (i) $I\ge 0$ (positivity), (ii) $I(h(\cdot+s)) = I(h)$ for $s\in F$, (iii) $I(\varphi|_F) = \int_{\mathbb{R}}\varphi$
for continuous compactly supported $\varphi$ (the periodisation is continuous and $1$-periodic, and $\mathfrak m$
restricted to continuous periodic functions is Lebesgue integration: every non-constant ordinary circle character
is multiplied by a non-trivial scalar by some translation from $F/\mathbb{Z}$, hence has mean zero, and
trigonometric polynomials are dense), (iv) for a bounded, boundedly supported Hilbert-valued $V$ the weak integral
$I(V)$ exists and $\lVert I(V)\rVert\le I(\lVert V\rVert)$ (dualise and use (i)).

**Lemma 2.5** (paper §2.2). *If $\nu$ is wild, $a\in E\setminus\{0\}$ and $\varphi\in C_c(\mathbb{R})$, then*
$$I\big(\varphi(t)\,f^\nu(at)\big) = 0. \tag{2.4}$$

*Proof.* **Step 1** (no non-zero strongly continuous vector). Let $T_tv = \psi_{at}v$ on $L^2(\nu)$, a unitary
representation of the discrete group $F$. Claim: if $v$ is strongly continuous for the usual topology of $F$ then
$v = 0$. Replacing $v$ by $\min(\lvert v\rvert,N)\cdot v/\lvert v\rvert$ (which is in $L^\infty$ and stays in the
closed space of strongly continuous vectors) we may assume $\lVert v\rVert_\infty<\infty$; and
$v\mapsto c_v(t) = \int_D\lvert v\rvert^2\psi_{at}\,d\nu$ is positive definite
($\sum_{i,j}c_v(t_i-t_j)\lambda_i\bar\lambda_j = \int\lvert v\rvert^2\lvert\sum_i\lambda_i\psi_{at_i}\rvert^2d\nu\ge0$)
and uniformly continuous:
$\lvert c_v(t+s)-c_v(t)\rvert\le\lVert v\rVert_\infty^2\int\lvert\psi_{as}-1\rvert\,d\nu
\le\lVert v\rVert_\infty^2\lVert T_s1-1\rVert_2\to0$, where $\lVert T_s1-1\rVert_2^2 = \int\lvert\psi_{as}-1\rvert^2d\nu\to0$
by dominated convergence. So $c_v$ extends to a continuous positive-definite function on $\mathbb{R}$; by (T3)
$c_v(t) = \int_{\mathbb{R}}e^{i\lambda t}\,d\rho(\lambda)$ for a finite positive $\rho$.
Consider the two finite measures on $\widehat F_{\mathrm{disc}}$: the pushforward $\Phi_*\rho$ of $\rho$ under
$\lambda\mapsto(t\mapsto e^{i\lambda t})$, and the pushforward $\rho_{a*}(\lvert v\rvert^2\nu)$ under
$\rho_a(d) = d(a\,\cdot)$. Their Fourier coefficients at $t\in F$ are $\int e^{i\lambda t}d\rho = c_v(t)$ and
$\int_D d(at)\lvert v\rvert^2d\nu = c_v(t)$. By (T1) they coincide; hence
$\lvert v\rvert^2\nu(D) = \rho_{a*}(\lvert v\rvert^2\nu)(\Phi) = \lvert v\rvert^2\nu(\rho_a^{-1}(\Phi)) =
\lvert v\rvert^2\nu(L_a) \le \lVert v\rVert_\infty^2\,\nu(L_a) = 0$ by Lemma 2.4(c). So $v = 0$.
**Step 2.** For $\varphi\in C_c(\mathbb{R})$ put $V_\varphi = I(\varphi(t)T_t1)\in L^2(\nu)$, so that
$T_sV_\varphi - V_\varphi = I\big((\varphi(\cdot - s)-\varphi)\cdot T_\cdot1\big)$ by (ii), whence
$\lVert T_sV_\varphi - V_\varphi\rVert_2\le I(\lvert\varphi(\cdot-s)-\varphi\rvert) = \int_{\mathbb{R}}\lvert\varphi(t-s)-\varphi(t)\rvert\,dt\to0$
by (iii) as $s\to0$ in $F$. So $V_\varphi$ is strongly continuous, hence $V_\varphi = 0$ by Step 1.
**Step 3.** Pairing with the constant function $1$ (a legitimate pairing against the weak integral),
$0 = \langle V_\varphi,1\rangle = I\big(\varphi(t)\langle T_t1,1\rangle\big) = I\big(\varphi(t)\int_D\psi_{at}d\nu\big) = I(\varphi f^\nu(a\,\cdot))$. $\square$

### 2.3 Lemma 2.6 (a canonical centre for a Borel probability on the plane)

Define $J_\lambda(s) = \int_{\mathbb{R}^2}\big(\sqrt{1+\lvert s-t\rvert^2}-\sqrt{1+\lvert t\rvert^2}\big)\,d\lambda(t)$,
$\lambda\in\mathcal P(\mathbb{R}^2)$, $s\in\mathbb{R}^2$.

**Lemma 2.6** (paper §2.3). *For every Borel probability $\lambda$ on $\mathbb{R}^2$, $J_\lambda$ has a unique
minimiser $L(\lambda)$; $\lambda\mapsto L(\lambda)$ is Borel; and $L$ is equivariant:
$L(\lambda\ast\delta_{-r}) = L(\lambda)-r$ for translations and $L(O_*\lambda) = O L(\lambda)$ for orthogonal $O$.*

*Proof.* The integrand is continuous with $\big\lvert\sqrt{1+\lvert s-t\rvert^2}-\sqrt{1+\lvert t\rvert^2}\big\rvert\le
\lvert s\rvert$, so $J_\lambda$ is finite and $\lvert s\rvert$-Lipschitz. Each $s\mapsto\sqrt{1+\lvert s-t\rvert^2}$ is
strictly convex ($C^2$ with positive definite Hessian), hence so is $J_\lambda$ (strictly, because the integrand is
strictly convex at every $t$ and $\lambda$ is a probability). Coercivity: choose $R$ with
$p = \lambda(\overline B(0,R))>1/2$; on $\overline B(0,R)$ the integrand is at least
$\lvert s\rvert - R - \sqrt{1+R^2}$ and elsewhere at least $-\lvert s\rvert$, so
$J_\lambda(s)\ge(2p-1)\lvert s\rvert - p(R+\sqrt{1+R^2})\to+\infty$. A continuous coercive strictly convex
function has exactly one minimiser. Enumerate $\mathbb{Q}^2$ and let $q_n(\lambda)$ be the first rational point
whose value is less than $\inf J_\lambda + 1/n$; each $\{\lambda : J_\lambda(q)<c\}$ is open in the weak topology
since $s\mapsto\sqrt{1+\lvert s-t\rvert^2}-\sqrt{1+\lvert t\rvert^2}$ is a bounded continuous function of $t$, so
each $q_n$ is Borel; and $q_n(\lambda)\to L(\lambda)$ for fixed $\lambda$ by coercivity. A pointwise limit of Borel
maps is Borel. The two equivariance identities are
$J_{\lambda\ast\delta_{-r}}(s) = J_\lambda(s+r)-J_\lambda(r)$ and $J_{O_*\lambda}(Os) = J_\lambda(s)$, both immediate
from the definitions. $\square$

**Remark 2.6.4.** The paper says "$\lambda\mapsto J_\lambda(s)$ is Borel"; in fact $s\mapsto
\sqrt{1+\lvert s-t\rvert^2}-\sqrt{1+\lvert t\rvert^2}$ is bounded and continuous, so $\lambda\mapsto J_\lambda(s)$ is
*continuous* for the weak topology (the defining property of that topology), and the argument above is
unnecessary. No first moment is needed, exactly as the paper says.

### 2.4 Lemma 2.7 (relative singularity along a compact tower)

**Setting.** $X$ is an ergodic standard probability-preserving $K$-system (countable discrete abelian $K$ acting by
measure-preserving automorphisms), $d:X\to D$ is measurable with $d(kx) = k\,d(x)$ ($K$-equivariant) and with
wild law $\nu$; $(Y_\alpha)_{\alpha\le\theta}$ is a tower of factors of $X$: $Y_0$ trivial, limit stages are
generated by their predecessors, and each successor $Y$ over its predecessor $W$ satisfies

> **(2.6)** for every bounded $H$ on $Y$ and every $\varepsilon>0$ there are bounded $H_1,\dots,H_q$ on $Y$ and
> $B<\infty$ such that for every $k\in K$ there are $b^r_k\in L^\infty(W)$ with $\lVert b^r_k\rVert_\infty\le B$ and
> $\big\lVert U_kH-\sum_r b^r_kH_r\big\rVert_2<\varepsilon$.

For a factor $Y$ write $\kappa_y$ for the conditional law of $d$ over $y\in Y$ (T6), so that
$X\times_YX$ conditional independence means: sample $y\sim\nu_Y$, then two independent $\kappa_y$-samples.

**Lemma 2.7** (paper §2.4). *In the above setting, for every factor $Y$ of the tower, the law $\nu_Y$ of
$d(x)-d(x')$ for two conditionally independent samples over $Y$ satisfies $\nu_Y(C) = 0$.*

**2.4.0 The induction statement.** For an ordinal $\xi$ let $\mathsf P(\xi)$ be the following assertion, with
*all* ambient data universally quantified:

> for every ergodic standard probability-preserving $K$-system $X'$, every $K$-equivariant measurable
> $d':X'\to D$ with wild law, every tower $(Y'_\alpha)_{\alpha\le\xi}$ of factors of $X'$ satisfying (2.6) at each
> successor, and every $\beta\le\xi$, the relative difference law $\nu'_{Y'_\beta}$ satisfies
> $\nu'_{Y'_\beta}(C) = 0$.

This is a statement about sets (not a proper class): it can be phrased as a first-order formula over the universe
with parameters allowed, so transfinite induction on $\xi$ is legitimate. Lemma 2.7 for a tower of length $\theta$
is $\mathsf P(\theta)$; we prove $\mathsf P(\xi)$ for all countable $\xi$ by induction.

**Step 0 (base).** $\beta = 0$: $Y_0$ is the trivial factor, $\kappa_y = \nu$ for the unique $y$, and
$\nu_{Y_0}$ is the law of $d-d'$ for two independent $\nu$-samples, which is wild by Lemma 2.4(b).

**Step 1 (reduction to a single factor with (2.9)).** Let $\xi>0$ and assume $\mathsf P(\zeta)$ for all
$\zeta<\xi$; let $X', d'$, $(Y'_\alpha)_{\alpha\le\xi}$ be data for $\xi$ and let $\beta\le\xi$. If $\beta<\xi$ we are
done by the induction hypothesis, so let $\beta = \xi$. Two cases.

*Successor* $\xi = \zeta+1$: put $Y = Y'_\zeta$, $W = Y'_{\zeta-1}$; (2.6) holds by hypothesis, hence so does (2.9)
below for every bounded $H$ on $Y$ (apply (2.6) to the finitely many coordinates of a $\mathbb{C}^m$-valued $H$ and
combine).

*Limit* $\xi$: $Y'_\xi$ is generated by $\bigcup_{\alpha<\xi}Y'_\alpha$, and $\xi$ is countable, so for every
bounded $H$ on $Y'_\xi$ and every $\delta>0$ there is $\alpha<\xi$ and a bounded $H'$ on $Y'_\alpha$ with
$\lVert H-H'\rVert_2<\delta$ (conditional expectations onto an increasing family of factors converge;
equivalently, the union of the $L^2(Y'_\alpha)$ is dense in $L^2(Y'_\xi)$ because it is a unital algebra generating
$Y'_\xi$). Taking $\alpha$ a successor $\zeta+1$ (increase $\alpha$ if necessary; $\xi$ is a limit ordinal),
$H'$ is a function on $Y'_{\zeta+1}$ and (2.6) at that successor gives bounded $H_r$ on $Y'_{\zeta+1}$ and
coefficients over $Y'_\zeta =: W$ with the required bound. So in both cases we have

> **(2.9)** for every bounded $H$ on $Y$ and $\gamma>0$ there are bounded $\mathbb{C}^m$-valued
> $H_1,\dots,H_q$ on $Y$, $B<\infty$ and, for every $k\in K$, $b^r_k\in L^\infty(W)$ with
> $\lVert b^r_k\rVert_\infty\le B$ and $\big\lVert U_kH-\sum_r b^r_kH_r\big\rVert_2<\gamma$,

for an "earlier" factor $W\le Y$ which is itself a member of the tower (for the limit case, $W = Y'_\zeta$ with
$\zeta+1\le\xi$, so $W<Y'_\xi$). **This is the only place where the induction hypothesis is used**, namely in
Step 5 below applied to $W<Y$ and to the *new* ambient system $Z$ (which is legitimate because $\mathsf P(\zeta)$
is universally quantified over ambient systems, maps and towers).

Assume now that $\nu_Y(C) = \alpha > 0$ and derive a contradiction.

**Step 2 (positive-mass cosets).** $r(y,z) = \kappa_y(z+C) = \int_D\mathbf 1_C(d'-z)\,d\kappa_y(d')$ is Borel in
$(y,z)$ (Borel parameter integration; only that $C$ is Borel). The function $x\mapsto r(y(x),d(x))$ is $K$-invariant
— because $\kappa_{ky} = (k)_*\kappa_y$ and $C$ is $K$-invariant — and
$\int r(y(x),d(x))\,d\mu = \iint\mathbf 1_C(d'-d)d\kappa_y(d')d\kappa_y(d) = \nu_Y(C) = \alpha$. By ergodicity it
equals $\alpha$ a.e. Hence for a.e. $y$: for $\kappa_y$-a.e. $z$, $\kappa_y(z+C) = \alpha$. Distinct cosets are
disjoint and each has mass $\alpha$, so there are exactly $m := 1/\alpha\in\mathbb{N}$ of them and they carry all
of $\kappa_y$; $m$ does not depend on $y$. None of them is $C$ itself (a.e.), since $\nu(C) = 0$.

**Step 3 (an equivariant centre in each coset).** On $\{r>0\}$ put
$$\lambda_{y,z}(A) = \frac1{r(y,z)}\int_D\mathbf 1_C(d'-z)\,\mathbf 1_A\big(j^{-1}(d'-z)\big)\,d\kappa_y(d'),$$
a Borel probability kernel on $\mathbb{R}^2$ (the Borel inverse $j^{-1}:C\to\mathbb{R}^2$ of Lemma 1.2(2) is used),
and $b(y,z) = z + j\big(L(\lambda_{y,z})\big)$ with $L$ from Lemma 2.6. If $\delta = j(r_0)\in C$ then the
conditioning event $\{d'-z-\delta\in C\}$ equals $\{d'-z\in C\}$ and $j^{-1}(d'-z-\delta) = j^{-1}(d'-z)-r_0$, so
$\lambda_{y,z+\delta} = (\cdot-r_0)_*\lambda_{y,z}$, and Lemma 2.6 gives $L(\lambda_{y,z+\delta}) = L(\lambda_{y,z})-r_0$,
i.e. $b(y,z+\delta) = b(y,z)$: $b$ is constant on cosets and $b(y,z)\in z+C$. For $k\in K$,
$\lambda_{ky,kz} = (k^{-1})_*\lambda_{y,z}$ (here $k\,j(\xi) = j(k^{-1}\xi)$, Lemma 1.2(6), and $C$ is
$K$-invariant), so by orthogonal covariance of $L$,
$$b(ky,kz) = kz + j\big(k^{-1}L(\lambda_{y,z})\big) = kz + k\,j\big(L(\lambda_{y,z})\big) = k\,b(y,z).$$
Thus $x\mapsto b(x) := b(y(x),d(x))$ is $K$-equivariant, measurable, and satisfies $b(x)-d(x)\in C$; consequently
$\{b\in C\}\subseteq\{d\in C\}$ and the law of $b$ is wild. Let $Z = Y\vee\sigma(b)$, a standard factor; $b$ is
$Z$-measurable, and its conditional law $\beta_y$ over $y$ is the uniform law on the $m$ centres of the
positive-mass cosets of $\kappa_y$.

**Step 4 (encoding the finite phase list).** For $y$ let $\Psi(y)\in\mathbb{T}^m/\mathfrak S_m$ be the unordered
list, with repetitions, of the $m$ numbers $\psi_1(z') = z'(1)$ for $z'$ in the support of $\beta_y$ (i.e. the
centre of each positive-mass coset). Let $H(y)\in\mathbb{C}^m$ be the vector of elementary symmetric functions of
that list (for $m=0$ conventions are irrelevant since $m\ge1$). $H$ is a bounded measurable $\mathbb{C}^m$-valued
function on $Y$: the power sums are $\int\psi_1^n\,d\beta_y$, measurable in $y$, and Newton's identities recover the
elementary symmetric functions. Encoding is a continuous injection $\mathbb{T}^m/\mathfrak S_m\to\mathbb{C}^m$ with
uniformly continuous inverse for the matching metric
$\mathsf d_{\mathrm{match}}([z],[z']) = \min_{\pi\in\mathfrak S_m}\max_r\lvert z_r-z'_{\pi(r)}\rvert$. Because
$\beta_{ky} = (k)_*\beta_y$ and $\psi_1(kz') = \psi_k(z')$, the rotation $U_kH$ encodes the list of $\psi_k$-values at
$\beta_y$.

**Step 5 (the induction hypothesis inside $Z$; the coefficient function).** The tower of factors below $Y$ is also a
tower of factors of $Z$ (since $W\le Y\le Z$), the action and all measures are unchanged, and (2.6) is an
$L^2(X)$-identity hence unchanged. Apply $\mathsf P(\zeta)$ (Step 1) in the ambient system $Z$ to the equivariant
wild map $b$: the law of $b(z)-b(z')$ over conditionally independent samples over $W$ is wild. Its Fourier
coefficient at $a\in E$ is
$$p(a) := \Big\lVert \mathbb E_Z\big(\psi_a(b)\,\big|\,W\big)\Big\rVert_2^2\ \ge 0,$$
the equality being conditional independence. By Lemma 2.5, $I(\varphi(t)p(at)) = 0$ for every $a\neq0$ and
$\varphi\in C_c(\mathbb{R})$.

**Step 6 (choosing small parameters, once and for all).** Fix $\rho>0$ with
$\sigma\{z\in\mathbb{T}:\lvert z-1\rvert\le5\rho\}<1/(16m^2)$. Choose $N\ge1$ and $c>0$ such that
$$\Big\lvert\int z^n\,d\omega(z)\Big\rvert<c\ (1\le n\le N)\ \Longrightarrow\ \omega\{\lvert z-1\rvert\le4\rho\}<\frac1{4m^2}
\tag{2.7}$$
for every probability $\omega$ on $\mathbb{T}$: take a continuous $\eta$ with $\mathbf 1_{\{\lvert z-1\rvert\le4\rho\}}
\le\eta\le\mathbf 1_{\{\lvert z-1\rvert\le5\rho\}}$, approximate $\eta$ uniformly within $1/(64m^2)$ by a real
trigonometric polynomial $\sum_{\lvert n\rvert\le N}a_ne^{in\theta}$, note $\lvert a_0-\int\eta\rvert<1/(64m^2)$, and
choose $c$ with $c\sum_{1\le\lvert n\rvert\le N}\lvert a_n\rvert<1/(32m^2)$; then
$\int\eta\,d\omega<1/(8m^2)$. Choose $s>0$ so that two encoding vectors at distance $<s$ have phase lists matching
within $\rho$ (uniform continuity of the inverse encoding); put $\tau = s/100$, so $\tau^2/s^2 = 10^{-4}$, and choose
$\gamma>0$ with
$$2\gamma^2/\tau^2<10^{-4}. \tag{2.8}$$
Choose finitely many bins $L$ for the coefficient arrays (see Step 8) and then $M\ge2$ with
$$\frac{0.9M}{L}>10m^2. \tag{2.9'}$$
All of $\rho,N,c,s,\tau,\gamma,L,M$ are fixed *before* $t$ is chosen.

**Step 7 (a small non-zero $t$ and a good set of fibres).** By Lemma 2.5 applied to the finitely many non-zero
elements $a = n(j-l)$, $1\le n\le N$, $1\le j\neq l\le M$, and a non-negative $\varphi\in C_c((-1/M,1/M))$ with
$\int\varphi>0$: if every one of the non-negative functions $t\mapsto p(n(j-l)t)$ were $\ge\varepsilon$ on the support
of $\varphi$, then $I(\varphi\cdot\sum p(n(j-l)\cdot))\ge\varepsilon I(\varphi)>0$ would contradict
$I(\varphi\,p(a\,\cdot)) = 0$ summed over the finitely many $a$. Hence there is $t\in F$ with $\lvert t\rvert<1/M$
and $p(n(j-l)t)<\varepsilon$ for all the indicated pairs, for any prescribed $\varepsilon>0$; and $t\neq0$ as soon
as $\varepsilon<1$, because $p(0) = 1$. Choosing $\varepsilon$ small enough that Markov's inequality and a finite
union bound give (with $x_j := jt$)
$$\mathbb P\Big(\big\lvert\mathbb E_Z(\psi_{n(x_j-x_l)}(b)\mid W=w)\big\rvert<c\Big)>0.99
\quad\text{for all }1\le j<l\le M,$$
and applying (2.7) to the conditional law of $\psi_{x_j-x_l}(b)$ on that set of fibres $w$,
$$\mathbb P_Z\big(\lvert\psi_{x_j}(b)-\psi_{x_l}(b)\rvert\le4\rho\ \big|\ W=w\big)<\frac1{4m^2},
\qquad 1\le j<l\le M. \tag{2.11}$$

**Step 8 (a common bin on a good fibre).** Every $\lvert x_j\rvert<1$ is a sum of two elements of $K$:
$$k_j = \frac{x_j}2 + i\sqrt{1-\frac{x_j^2}4},\qquad k'_j = \frac{x_j}2 - i\sqrt{1-\frac{x_j^2}4},\qquad k_j+k'_j = x_j$$
(with real $x_j$, this is Lemma 1.3 read on the real axis; $\sqrt{1-x_j^2/4}\in F$ because $F$ is real closed).
Apply (2.9) to $H$ with both rotations $k_j$ and $k'_j$, for all $j\le M$. Two coefficient arrays live in a fixed
bounded subset of $\mathbb{C}^{2q}$; choose $L$ bins fine enough that arrays in one bin give approximating functions
differing pointwise by at most $\tau$ for each of the two vectors (coordinate diameters $\tau/(1+\sum_r\lVert H_r\rVert_\infty)$
suffice). $L$ does not depend on the fibre or on $k$. Let $e^+_j(w),e^-_j(w)$ be the conditional squared $L^2$
errors of the two approximations on the fibre of $Y$ over $w$; their global integrals are $<\gamma^2$. By (2.8),
on a set of $w$ of probability $>0.99$ more than $0.9M$ indices $j$ have both conditional errors $<\tau$ (Markov:
otherwise $\mathrm{Avg}_j(e^+_j+e^-_j)\ge0.1\tau^2$ on a set of probability at most $20\gamma^2/\tau^2<0.001$).
Fix $w$ outside the two exceptional sets, $j_0$ in a bin containing more than $10m^2$ good indices $J$. For
$j,j_0\in J$ the conditional $L^2$ distance from $U_{k_j}H$ to $U_{k_{j_0}}H$ is at most $3\tau$ (two approximation
errors $<\tau$ plus a pointwise difference $\le\tau$). Hence for uniform $j\in J$ and conditional $y$,
$\mathbb P(\text{either encoding distance}\ge s)\le 2\cdot(3\tau)^2/s^2 = 18\cdot10^{-4} = 0.0018$, so with
probability $>0.95$ both phase lists at $j$ match those at $j_0$ within $\rho$. Writing $q(y)$ for the fraction of
$j\in J$ for which both matches hold:
$$\mathbb E(q\mid W=w)>0.95. \tag{2.12}$$

**Step 9 (the collision contradiction).** Fix such $y$ and any $b_0$ in the support of $\beta_y$ (the conditional
law of $b$ given $Y$). For each matching $j$, $\psi_{k_j}(b_0)$ is within $\rho$ of an entry of the $j_0$-list, i.e. of
some $\psi_{k_{j_0}}(z_1)$ with $z_1\in\mathrm{supp}\,\beta_y$, and $\psi_{k'_j}(b_0)$ is within $\rho$ of some
$\psi_{k'_{j_0}}(z_2)$. Hence
$\psi_{x_j}(b_0) = \psi_{k_j}(b_0)\psi_{k'_j}(b_0)$ lies within $2\rho$ of one of the at most $m^2$ products
$\psi_{k_{j_0}}(z_1)\psi_{k'_{j_0}}(z_2)$, $(z_1,z_2)\in(\mathrm{supp}\,\beta_y)^2$ (the matchings need not select the
same centre, which is why all $m^2$ products are allowed). Assign each of the $q(y)\lvert J\rvert$ matching indices
to one such product; by Cauchy–Schwarz one product receives at least $q(y)^2\lvert J\rvert^2/m^2$ ordered pairs.
Discarding the at most $\lvert J\rvert$ diagonal pairs, for independent uniform $j,l\in J$
$$\mathbb P\big(j\neq l,\ \lvert\psi_{x_j}(b_0)-\psi_{x_l}(b_0)\rvert\le4\rho\big)\ \ge\ \frac{q(y)^2}{m^2}-\frac1{\lvert J\rvert}.$$
This holds for every $b_0$, so integrating over $\beta_y$ and then over $y\mid w$, Jensen's inequality and (2.12) give
$$\mathbb P\big(j\neq l,\ \lvert\psi_{x_j}(b)-\psi_{x_l}(b)\rvert\le4\rho\ \big|\ W=w\big)
\ >\ \frac{0.95^2}{m^2}-\frac1{\lvert J\rvert}\ >\ \frac{0.9025-0.1}{m^2}\ >\ \frac1{4m^2},$$
using $\lvert J\rvert>10m^2$ by (2.9'). This contradicts (2.11), which bounds *every* pair $j\neq l$ of indices in
$\{1,\dots,M\}$ and hence their average over $J$. $\square$

**Remark 2.7.1 (why the "universal" form is needed).** In Step 5 the induction hypothesis is applied to a *different*
system, namely $Z=Y\vee\sigma(b)$ inside the same $X$, and to the *different* equivariant map $b$. If
$\mathsf P(\zeta)$ were stated only for a fixed ambient system, the induction would break at the first extension; this
is why the paper insists on the universal statement, and $\mathsf P(\xi)$ in 2.4.0 is exactly that statement.
**Remark 2.7.2.** Steps 2 and 3 use only that $C$ is Borel, $K$-invariant, and that $j^{-1}$ is Borel on $C$; no
closedness of $C$ is needed, as the paper notes. **Remark 2.7.3.** All the "null sets" in Steps 2–9 are
$\nu_Y$- or $\kappa_y$-null sets attached to countably many Borel identities, so a common conull set exists.

### 2.5 Lemma 3.1 (the compact tower) with the measurability detail filled in

**Lemma 3.1** (paper §3.1). *Let $X$ be an ergodic standard probability-preserving $K$-system. Then there are a
countable ordinal $\eta$ and an increasing tower of factors $(Y_\alpha)_{\alpha\le\eta}$, $Y_0$ trivial, limit stages
generated by their predecessors, each successor satisfying (2.6), such that $X\times_{Y_\eta}X$ is ergodic.*

*Proof.* **(i) One strict extension.** Let $Y$ be a factor with $X\times_YX$ not ergodic. Choose a bounded invariant
non-constant kernel $L(x,x')$ on the relative product, i.e. $L\in L^\infty(\mu\times_Y\mu)$ with $U_k^{\otimes2}L = L$
for all $k$; its conditional expectation onto either coordinate is an invariant function on $X$, hence constant;
after subtracting that constant $L\neq0$ still, is invariant, and has both coordinate conditional expectations $0$.

For a.e. $y$ the kernel $L$ defines an integral operator $A_y$ on $H_y = L^2(\mu_y)$ with
$\lVert A_y\rVert_{HS}\le\lVert L\rVert_\infty$ and $A_y1 = A_y^*1 = 0$; the field is equivariant for the unitary maps
between fibres induced by $U_k$, and $\int_Y\lVert A_y\rVert^2_{HS}\,d\nu_Y(y) = \lVert L\rVert^2_{L^2(\mu\times_Y\mu)}>0$.
**Existence of a level $\delta>0$** (this is the only point where the paper is terse): since
$\mathbf 1_{(1/n,\infty)}(A_y^*A_y)\downarrow0$ as $n\to\infty$ whenever $A_y = 0$, and $A_y^*A_y = 0$ iff
$\mathbf 1_{(1/n,\infty)}(A_y^*A_y) = 0$ for every $n$, the alternative "$\mathbf 1_{(1/n,\infty)}(A_y^*A_y) = 0$
$\nu_Y$-a.e. for every $n$" would force $A_y = 0$ a.e. (C*-identity) and hence $L = 0$, contrary to the choice of
$L$. So there is $n$ with $Q_y := \mathbf 1_{(1/n,\infty)}(A_y^*A_y)\neq0$ on a set of $y$ of positive measure; fix
such a $\delta := 1/n$. Because $\mathbf 1_{(\delta,\infty)}(A_y^*A_y)\le\delta^{-1}A_y^*A_y$,
$$\operatorname{rank}Q_y \le \delta^{-1}\operatorname{tr}(A_y^*A_y) = \delta^{-1}\lVert A_y\rVert^2_{HS}\le\delta^{-1}\lVert L\rVert_\infty^2$$
for *every* $y$; the rank is invariant on $Y$ (the $Q_{ky}$ are unitarily equivalent to $Q_y$) and $Y$ is ergodic
(a factor of $X$), so by Lemma 3.1.5(a) below $\operatorname{rank}Q_y = d$ for a fixed integer $d$, and $d\ge1$
because $Q_y\neq0$ on a set of positive measure. Note that the finite rank bound, not positivity of the spectrum
alone, is what makes $d$ finite.

**(ii) Measurable fibre-orthonormal bases.** This is the step the paper compresses into "selecting the first
available independent section at each step and applying fiberwise Gram–Schmidt"; here is a complete proof.

**Lemma 3.1.5.** *Let $V$ be a separable complex Hilbert space, $(Y,\nu)$ a standard probability space and
$y\mapsto Q_y\in\mathcal B(V)$ a strongly measurable field of orthogonal projections ($Q_y = Q_y^* = Q_y^2$) with
finite rank. Then* (a) *$y\mapsto\operatorname{rank}Q_y$ is measurable, and* (b) *if $\operatorname{rank}Q_y = d$
$\nu$-a.e. then there are measurable maps $e_1,\dots,e_d:Y\to V$ with $(e_1(y),\dots,e_d(y))$ an orthonormal basis
of $\operatorname{ran}Q_y$ for $\nu$-a.e. $y$.*

*Proof.* Fix a sequence $(f_j)_{j\ge1}$ dense in the unit ball of $V$. Define recursively, simultaneously in $y$,
$$j_{k+1}(y) = \min\Big\{j : \big\lVert Q_y\big(f_j-\textstyle\sum_{m\le k}\langle f_j,e_m(y)\rangle e_m(y)\big)\big\rVert\ge\tfrac34\Big\},$$
$\;e_{k+1}(y) = $ the normalised vector in braces (and $e_{k+1}(y) = 0$, $j_{k+1}(y) = \infty$ if the set is empty).
*Measurability:* the sets $\{j_{k+1} = j\}$ are measurable — $y\mapsto Q_y$ is strongly measurable, each $e_m$ is
measurable by induction, and $y\mapsto\langle f_j,e_m(y)\rangle$ and $y\mapsto\lVert Q_y(\cdot)\rVert$ are then
countable compositions of measurable functions — so the recursion produces measurable $e_k$.
*Correctness:* if $\dim\operatorname{ran}Q_y\ge k+1$ and $e_1,\dots,e_k$ are orthonormal in $\operatorname{ran}Q_y$,
choose a unit $w\in\operatorname{ran}Q_y$ orthogonal to $e_1,\dots,e_k$ and $f_j$ with $\lVert f_j-w\rVert<\tfrac14$;
with $f_j^{\perp} = f_j-\sum_{m\le k}\langle f_j,e_m\rangle e_m$ and $Q_ye_m = e_m$ one has
$Q_yf_j^{\perp} = Q_yf_j-\sum_m\langle f_j,e_m\rangle e_m$, while $f_j^{\perp}-w = (f_j-w)^{\perp}$ because $w\perp e_m$;
so $\lVert Q_yf_j^{\perp}-w\rVert = \lVert Q_y(f_j-w)\rVert\le\lVert f_j-w\rVert<\tfrac14$ (as $Q_y$ is a contraction
fixing $w$) and hence $\lVert Q_yf_j^{\perp}\rVert\ge\tfrac34$: the set in the definition is non-empty. If
$\dim\operatorname{ran}Q_y = k$ and $e_1,\dots,e_k$ span it, then $f_j^{\perp}\perp\operatorname{ran}Q_y$ for every $j$,
so $Q_yf_j^{\perp} = 0$ and the set is empty. Hence the recursion produces non-zero vectors for
$k = 1,\dots,d$ and zero at $k = d+1$, and $\{y:\operatorname{rank}Q_y\ge k\} = \{j_k<\infty\}$ is measurable,
proving (a) and (b). $\square$

**(iii) The extension factor and its boundedness.** Choose $e_1,\dots,e_d$ fibrewise orthonormal, spanning
$\operatorname{ran}Q_y$; note $Q_y1 = 0$ since $A_y1 = 0$, so $e_i\perp1$, i.e. $\mathbb E(e_i\mid Y) = 0$ in fibre norm
and $\lVert e_i\rVert_{L^2(\mu_y)} = 1$. For $k\in K$ there is a unitary $d\times d$ matrix $c(k,y)$ with
$U_ke_i = \sum_j c_{ij}(k,y)e_j$; hence $\sum_i\lvert e_i(x)\rvert^2$ is $K$-invariant, has integral $d$, and by
ergodicity of $X$
$$\sum_{i=1}^d\lvert e_i(x)\rvert^2 = d \quad\text{a.e.}, \tag{3.1}$$
so each $e_i$ is bounded by $\sqrt d$. Let $Y' = Y\vee\sigma(e_1,\dots,e_d)$, a standard factor; it is a strict
extension because $e_i$ has conditional mean zero over $Y$ but fibre norm $1$, so $e_i\notin L^2(Y)$.

**(iv) Property (2.6) for $Y'\to Y$.** Bounded polynomials in $e_i,\bar e_i$ with coefficients in $L^\infty(Y)$ form a
bounded unital conjugation-closed algebra generating $Y'$, hence are dense in $L^2(Y')$. Fix $k\in K$; on the fibre
above $y$ one has $U_ke_i = \sum_jc_{ij}(k,y)e_j$ with a unitary matrix $c(k,y)$, so $U_k$ of a monomial of degree $N$
in $e,\bar e$ expands into finitely many monomials of degree $N$ whose coefficients are obtained from the entries of
$c(k,\cdot)^{\pm1}$ and from $U_k$ applied to the $Y$-coefficients. All these coefficients are bounded by the original
sup norms times $1$, since matrix entries of a unitary have modulus $\le1$ and $U_k$ is an isometry of $L^\infty$.
Fixing a polynomial approximation of a given bounded $H$ once, the rotated function has the same approximation error,
so (2.6) holds with $H_r$ the finitely many monomials and $B$ depending only on the degree and on the coefficient
bounds.

**(v) Iteration and stopping.** Start at $Y_0$ trivial and apply (i)–(iv) whenever $X\times_{Y}X$ is not ergodic,
taking generated joins at limit ordinals. If the process never stopped, then for every successor stage $\alpha+1$
choose a unit vector $v_{\alpha+1}\in L^2(Y_{\alpha+1})\ominus L^2(Y_\alpha)$; for $\alpha<\beta$ nestedness gives
$v_{\alpha+1}\perp v_{\beta+1}$, so we would have $\aleph_1$ pairwise orthogonal unit vectors in the separable space
$L^2(X)$: impossible. Hence the process stops at a countable ordinal $\eta$, and by the stopping rule
$X\times_{Y_\eta}X$ is ergodic. $\square$

**Remark 2.5.1.** Steps (i) and (iv) are the paper's; step (ii) replaces the paper's three-line assertion by a proof;
step (v) is the paper's. The whole lemma is the Furstenberg–Zimmer compact-factor step; the point of the proof above
is that nothing beyond (T2), (T6) and the ergodicity of factors is used.

### 2.6 Lemma 3.2 (conditional multiple averages)

**Lemma 3.2** (paper §3.2). *Let $X$ be ergodic, $Y$ an invariant factor with $X\times_YX$ ergodic, $P = \mathbb E(\cdot\mid Y)$.
For pairwise distinct integers $n_1,\dots,n_l$ and bounded $v_1,\dots,v_l$ on $X$, along every Følner sequence
$(\Phi_N)$ in $K$,*
$$\operatorname*{Avg}_{u\in\Phi_N}\Big\lVert P\Big(\prod_{j=1}^lU_u^{n_j}v_j\Big)-\prod_{j=1}^lU_u^{n_j}Pv_j\Big\rVert_2^2\longrightarrow0. \tag{3.2}$$
*The pair criterion used is, for bounded $v,w$ and $d\neq0$,*
$$\operatorname*{Avg}_{u\in\Phi_N}\big\lVert P(v\,U_{u^d}w)-Pv\,U_{u^d}Pw\big\rVert_2^2\longrightarrow0. \tag{3.3}$$

*Proof (structure).* Put $R = X\times_YX$ with conditional expectation $P_R$. (3.3): writing $v_0 = v-Pv$,
$w_0 = w-Pw$, the difference equals $P(v_0U_{u^d}w_0)$, and
$\lVert P(v_0U_{u^d}w_0)\rVert_2^2 = \int_R(v_0\otimes\bar v_0)U_{u^d}(w_0\otimes\bar w_0)\,d\mu_R$ by conditional
independence; since $\int_R w_0\otimes\bar w_0\,d\mu_R = \int_Y\lvert Pw_0\rvert^2d\nu = 0$, and $u\mapsto U_{u^d}$ on
the ergodic system $R$ has the same invariant vectors as $U$ (the power map is onto $K$), the mean ergodic theorem
(T5) gives the vanishing along every Følner sequence. The same criterion on $R$ follows for simple tensors from
$P_R((a_1\otimes a_2)U_{u^d}(b_1\otimes b_2)) = P(a_1U_{u^d}b_1)\,P(a_2U_{u^d}b_2)$, then for bounded functions by
$L^2$-approximation with a uniform sup bound (conditional expectations contract).
Next the vector assertion (3.5): if $n_1,\dots,n_l$ are distinct and non-zero and $Pv_{j^*}=0$ for some $j^*$, then
$\operatorname{Avg}_{u\in\Phi_N}\big\lVert\prod_jU_u^{n_j}v_j\big\rVert_2\to0$. Induction on $l$: $l=1$ is mean
ergodicity; for the step use $\int V_{hu}\overline{V_u}\,d\mu = \int F_{l,h}\prod_{j<l}U_u^{n_j-n_l}F_{j,h}\,d\mu$
(measure preservation; the shifted exponents are distinct and non-zero), expand into projected and centred factors,
use the induction hypothesis for the centred terms to bound the limsup by
$a(h) = \lVert PF_{j^*,h}\rVert_2^2$, then note that (3.3) with $v = \bar v_{j^*}$, $w = v_{j^*}$, $d = n_{j^*}$
gives $\operatorname{Avg}_h a(h)\to0$ along every Følner sequence, hence
$\sup_{t\in K}\operatorname{Avg}_{h\in\Psi_M}a(ht)\to0$ (a bad sequence of translates is itself a Følner sequence,
as $K$ is abelian); expand $\lVert V_u\rVert^2$ in pairwise shifts over a finite Følner set $S = \Psi_M$ and use the
Følner property, Jensen and (3.7) to conclude. Finally (3.2): expand each $v_j = Pv_j + (v_j-Pv_j)$; a term with at
least one centred factor $w_j$ has
$\lVert PW_u\rVert_2^2 = \int_R\prod_jU_u^{n_j}(w_j\otimes\bar w_j)\,d\mu_R$, whose tensor is centred over $Y$, and
(3.5) on $R$ (after adding a common integer to the exponents so none is zero) makes its average vanish; there are
finitely many centred terms. $\square$

**Remark 3.2.6 (nothing to correct here; an earlier version of this file misread it).** In (3.7) the paper defines
$a(h) = \lVert PF_{j^*,h}\rVert_2$ \emph{the norm}, not its square. With $v = \bar v_{j^*}$, $w = v_{j^*}$,
$d = n_{j^*}$, and using $Pv_{j^*} = 0$, the pair criterion (3.3) gives
$\operatorname{Avg}_u\lVert P(\bar v_{j^*}U_{u^{n_{j^*}}}v_{j^*})\rVert^2\to0$, and
$\lVert P(\bar v_{j^*}U_{u^{n_{j^*}}}v_{j^*})\rVert = \lVert P(U_{u^{n_{j^*}}}v_{j^*}\bar v_{j^*})\rVert = a(u)$ by
unitary invariance; so the criterion proves $\operatorname{Avg}_u a(u)^2\to0$, and Cauchy–Schwarz gives
$\operatorname{Avg}_ua(u)\le(\operatorname{Avg}_ua(u)^2)^{1/2}\to0$, which is exactly what (3.8) then uses. The
paper's sentence is correct as printed.

### 2.7 Lemma 3.3 (radial identities)

Fix an ergodic wild $K$-invariant probability $\mu$ on $D$; let $Y$ be the terminal factor of Lemma 3.1 and
$\nu_Y$ the relative difference law, which is wild by Lemma 2.7. Put
$$P = \mathbb E(\cdot\mid Y),\qquad g_z = P\psi_z,\qquad m(z) = \lVert g_z\rVert_2^2\quad(z\in E). \tag{3.10}$$
Then, by conditional independence,
$$\int_D\psi_z\,d\nu_Y = m(z), \tag{3.11}$$
$0\le m\le1$, $m(0) = 1$, so Lemma 2.5 gives (2.4) with $f^{\nu_Y} = m$; $m(uz) = m(z)$ for $u\in K$, so $m$ is
radial and, since $z/\lvert z\rvert\in K$ for $z\neq0$ (Lemma 1.1(5)), $m$ is determined by the radius:
$m(z) = m(\lvert z\rvert)$; also $g_{-z} = \overline{g_z}$ and $\lVert g_z\rVert_\infty\le1$.

**Lemma 3.3** (paper §3.3). *With $w(r) = -\log m(r)\in[0,\infty]$, $-\log0=\infty$:*
$$w(\lvert A-B\rvert)\le w(A)+w(B)\qquad(A,B\in F_{\ge0}), \tag{3.12}$$
*and for every $r\in F$, $r>0$, and every Følner sequence in $K$,*
$$\operatorname*{Avg}_{u\in\Phi_N}m(2r\lvert\operatorname{Re}u\rvert)\longrightarrow m(r)^2. \tag{3.13}$$

*Proof.* (3.14): for $A,B>0$, $L = \sqrt{AB}\in F$ and $u\in K$,
$$\lvert A-Bu^2\rvert^2 = (A-B)^2+4AB(\operatorname{Im}u)^2 = \big\lvert-L+(A-B)u+Lu^2\big\rvert^2 . \tag{3.14}$$
Indeed the middle expression comes from $\operatorname{Re}u^2 = 1-2(\operatorname{Im}u)^2$, and the last from
$-L+(A-B)u+Lu^2 = u\big((A-B)+L(u-u^{-1})\big) = u\big((A-B)+2iL\operatorname{Im}u\big)$.

*First side.* $\psi_{A-Bu^2} = \psi_A\,U_{u^2}\psi_{-B}$ (exponents $0,2$: check
$(U_{u^2}\psi_{-B})(d) = \psi_{-B}(u^2d) = d(-Bu^2)$). By (3.2) the projection of the product is approximated, in
averaged squared $L^2$-error, by $g_AU_{u^2}g_{-B}$; both factors have $L^2$-norm $\le1$, so the two squared norms
differ in averaged absolute value by $o(1)$. The squared norm of $g_AU_{u^2}g_{-B}$ is
$\int_Y\lvert g_A\rvert^2U_{u^2}\lvert g_{-B}\rvert^2d\nu$, and mean ergodicity on $Y$ through the surjective power
map $u\mapsto u^2$ (whose invariant vectors are those of $U$, since $\{u^2\} = K$) gives
$$\operatorname*{Avg}_{u\in\Phi_N}m(A-Bu^2)\longrightarrow m(A)\,m(B). \tag{3.15}$$

*Second side.* Let $R_u = -L+(A-B)u+Lu^2$. Then $\psi_{R_u} = \psi_{-L}U_u\psi_{A-B}U_{u^2}\psi_L$ (exponents
$0,1,2$, pairwise distinct), so (3.2) approximates $P\psi_{R_u}$ by $g_{-L}U_ug_{A-B}U_{u^2}g_L$ in averaged
squared error, and
$$\lVert g_{-L}U_ug_{A-B}U_{u^2}g_L\rVert_2^2\le\lVert g_{A-B}\rVert_2^2 = m(\lvert A-B\rvert),$$
because $\lvert g_{\pm L}\rvert\le1$ pointwise. Since $\lVert P\psi_{R_u}\rVert_2^2 = m(R_u)$ **and $m$ is radial**,
$m(R_u) = m(\lvert R_u\rvert) = m(\lvert A-Bu^2\rvert)$ by (3.14), so
$$\operatorname*{Avg}_{u}m(A-Bu^2)\ \le\ m(\lvert A-B\rvert).$$
Comparing with (3.15) gives $m(A)m(B)\le m(\lvert A-B\rvert)$, i.e. (3.12) after taking $-\log$. (If $A = 0$ or
$B = 0$, (3.12) is an equality since $w(0) = 0$.)

For (3.13): $ru+r\bar u = 2r\operatorname{Re}u$, so
$\psi_{2r\operatorname{Re}u} = U_u\psi_r\,U_{u^{-1}}\psi_r$ (exponents $1,-1$); (3.2) approximates the projection by
$U_ug_r\,U_{u^{-1}}g_r$, whose squared norm is $\int_Y\lvert g_r\rvert^2U_{u^{-2}}\lvert g_r\rvert^2d\nu$; mean
ergodicity on $Y$ through the surjective power map $u\mapsto u^{-2}$ gives the limit $m(r)^2$. Finally
$m(2r\operatorname{Re}u) = m(\lvert2r\operatorname{Re}u\rvert)$ by radiality. $\square$

**Remark 3.3.7 (the step at (3.14), read correctly).** In an earlier version of this file I recorded the derivation of
(3.12) as a defect; it is not one. The paper applies (3.2) with exponents $0,1,2$ to the \emph{second side} of (3.14),
i.e. to the character $\psi_{R_u}$ with $R_u = -L+(A-B)u+Lu^2$; that gives
$\lVert P\psi_{R_u}\rVert_2^2\le\lVert g_{-L}U_ug_{A-B}U_{u^2}g_L\rVert_2^2\le\lVert g_{A-B}\rVert_2^2 = m(\lvert A-B\rvert)$,
using only $\lvert g_{\pm L}\rvert\le1$ pointwise. No identification of $\psi_{A-Bu^2}$ with $\psi_{R_u}$ is made
anywhere (they are indeed different characters: for $A=1$, $B=4$, $u=e^{i\pi/3}$, $L=2$ the two arguments are
$3-2\sqrt3\,i$ and $-\tfrac92-\tfrac{\sqrt3}{2}i$, of equal modulus $\sqrt{21}$). The passage from the second side
back to the first is the \emph{modulus} identity (3.14) together with the paper's own next sentence, "equal moduli give
equal m-values", i.e. radiality of $m$: $m(A-Bu^2) = m(\lvert R_u\rvert) = m(\lvert A-Bu^2\rvert)$. Averaging and
(3.15) then give $m(A)m(B)\le m(\lvert A-B\rvert)$. The argument is complete as printed.

### 2.8 Lemmas 3.4 and 3.5

**Lemma 3.4** (general position in a number field; paper §3.4). *Let $N_0\subset F$ be a number field, $N = N_0(i)$,
$d_0 = [N:\mathbb{Q}]$. Then there are arbitrarily large finite $S\subset K\cap N$ such that every $d_0$ distinct
elements of $S$ form a $\mathbb{Q}$-basis of $N$.*

*Proof.* For $t\in N_0$ put $u(t) = (1+it)/(1-it)\in K\cap N$. In rational coordinates $u(t)$ is a rational function
of $t$ with denominator nonzero for real $t$. No nonzero $\mathbb{Q}$-linear $\ell:N\to\mathbb{Q}$ vanishes on all
$u(t)$: for fixed $a\in N_0$, $h\mapsto\ell(u(ha))$ is a rational function vanishing on $\mathbb{Q}$, hence
identically zero, and the expansion $u(ha) = 1+2iha-2h^2a^2+\dots$ gives $\ell(1) = \ell(ia) = \ell(a^2) = 0$ for
every $a\in N_0$; since $4a = (a+1)^2-(a-1)^2$, squares span $N_0$, so $\ell$ vanishes on $N_0+iN_0 = N$. Hence for
each proper $\mathbb{Q}$-subspace of $N$ the numerator polynomial of $\ell\circ u$ is nonzero, and a finite union of
proper subspaces cannot contain all $u(t)$ (a product of nonzero polynomials over the infinite field $\mathbb{Q}$ does
not vanish identically). Choose the elements one at a time outside the spans of all subsets of at most $d_0-1$
previously chosen ones. $\square$

**Lemma 3.5** (addition under a cap; paper §3.4). *Let $w:F_{\ge0}\to[0,\infty]$ satisfy $w(0) = 0$ and (3.12). Let
$p_1,\dots,p_q\in F_{\ge0}$ with $p = \max_jp_j>0$ and $w(p_j)\le H<\infty$. If
$z = \sum_ja_jp_j\in[0,p)$ with $a_j\in\mathbb{Z}$ and $\sum_j\lvert a_j\rvert\le M$, then $w(z)\le4MH$.*

*Proof.* Keep partial sums as residues in $[0,p)$. Each signed input $\pm p_j$ has a residue of cost at most $2H$
(if $p_j<p$: cost $\le H$; the inverse residue $p-p_j$ satisfies $w(p-p_j)\le w(p)+w(p_j)\le2H$; the input $p$ has
zero residue and cost $0$). Adding a residue $b$ (cost $\le2H$) to a current residue $a$ costs at most
$2w(p)+w(a)+w(b)\le2H+w(a)+w(b)$ when $a+b<p$ — from $w(a+b) = w\big(p-((p-a)-b)\big)\le w(p)+w\big((p-a)-b\big)\le
w(p)+w(p-a)+w(b)\le2w(p)+w(a)+w(b)$ — and at most $w(a)+w(p)+w(b)$ when $a+b>p$ (new residue $a-(p-b)$), and cost
$0$ when $a+b = p$. So each of the at most $M$ signed inputs raises the cost by at most $4H$, and starting from
residue $0$ (cost $0$) the final residue $z$ has $w(z)\le4MH$. $\square$

### 2.9 Completion of Theorem B (paper §3.5)

Assume $m(r)>0$ for some $r\in F$, $r>0$, and choose $H<\infty$ with $e^{-H}<m(r)^2$. Then
$A_0 = \{u\in K : w(2r\lvert\operatorname{Re}u\rvert)\le H\}$ is **syndetic**: otherwise for each Følner set $\Phi_N$
there is $v_N$ with $\Phi_Nv_N\cap A_0 = \emptyset$; the sets $\Phi_Nv_N$ are again Følner (abelian group), and on
them $m(2r\lvert\operatorname{Re}u\rvert)<e^{-H}$ for every $u$, so the averages are $\le e^{-H}$, contradicting
(3.13) which gives the limit $m(r)^2>e^{-H}$. Hence there are $q_1,\dots,q_J\in K$ with
$$\forall v\in K\ \exists j:\ q_jv\in A_0. \tag{3.16}$$
Let $N_0\subset F$ be a number field containing $\operatorname{Re}q_j,\operatorname{Im}q_j$ for all $j$, $N = N_0(i)$,
$d_0 = [N:\mathbb{Q}]$, and let $S\subset K\cap N$ from Lemma 3.4 have $\lvert S\rvert>J(d_0-1)$. For $v\in K$, (3.16)
applied to each $sv$, $s\in S$, and pigeonhole give $j$ and $d_0$ elements $s$ with $q_jsv\in A_0$; the $k = q_js$
form a $\mathbb{Q}$-basis $T$ of $N$ (multiplication by $q_j$ is an invertible $\mathbb{Q}$-linear map and every $d_0$
elements of $S$ form a basis). There are finitely many possible $T$; clearing denominators in the basis expansion of
$1$ gives $D_0\in\mathbb{N}$ and $M_0$ with
$$D_0\cdot1 = \sum_{k\in T}a_kk,\qquad a_k\in\mathbb{Z},\quad\sum_{k\in T}\lvert a_k\rvert\le M_0 \tag{3.17}$$
for every $T$, and a common $c_0\in(0,1]$ with
$$\max_{k\in T}\lvert\operatorname{Re}(kv)\rvert\ge c_0\qquad(v\in T\ \text{a selection}) \tag{3.18}$$
— the maximum is a continuous function of the unit direction $v$ which never vanishes (its $\mathbb{Q}$-span is $N\ni1,i$,
so vanishing would force $\operatorname{Re}v = \operatorname{Re}(iv) = 0$, i.e. $v = 0$), and there are finitely many
selections. Now fix $v\in K$ with $\lvert\operatorname{Re}v\rvert<c_0/D_0$ and its selection $T$. By (3.16)–(3.18) the
numbers $p_k = 2r\lvert\operatorname{Re}(kv)\rvert$ ($k\in T$) satisfy $w(p_k)\le H$ and $p = \max_Tp_k\ge2rc_0$.
Taking real parts in (3.17) gives $D_0 = \sum_ka_k\operatorname{Re}k$, hence
$$z := 2rD_0\lvert\operatorname{Re}v\rvert = \Big\lvert\sum_{k\in T}(a_k\operatorname{sgn}\operatorname{Re}(kv))\,p_k\Big\rvert
\ \in[0,p),\qquad \sum_k\lvert a_k\rvert\le M_0,$$
so Lemma 3.5 gives $w(2rD_0\lvert\operatorname{Re}v\rvert)\le4M_0H$ whenever $\lvert\operatorname{Re}v\rvert<c_0/D_0$.
Every $t\in F\cap[-1,1]$ is $\operatorname{Re}$ of $t+i\sqrt{1-t^2}\in K$, so for $s\in F\cap(0,2rc_0)$, applying this
to $t = s/(2rD_0)$,
$$m(s)\ \ge\ e^{-4M_0H}>0\qquad(s\in F\cap(0,2rc_0)).$$
Choose $\varphi\in C_c(\mathbb{R})$, $\varphi\ge0$, $\varphi\not\equiv0$, supported in $(0,2rc_0)$. Then by
positivity of $I$ and its agreement with the Lebesgue integral on continuous compactly supported functions,
$$I\big(\varphi\,m\big)\ \ge\ e^{-4M_0H}I(\varphi) = e^{-4M_0H}\int_{\mathbb{R}}\varphi>0,$$
contradicting (2.4) for the wild law $\nu_Y$ with $a = 1$, in view of (3.11). Hence $m(r) = 0$ for every positive
$r\in F$, and by radiality $m(z) = 0$ for every $z\in E\setminus\{0\}$. Therefore
$$\int_D\psi_z\,d\mu = \int_Yg_z\,d\nu \le \lVert g_z\rVert_2 = 0\qquad(z\neq0),$$
and by (T1) $\mu = m_D$.

Finally, an arbitrary wild $K$-invariant probability $\mu$ has an ergodic decomposition for the countable group $K$ on
the standard compact space $D$. Since $\mathbf 1_C$ is $K$-invariant and Borel, it agrees a.e. with its conditional
expectation on the invariant $\sigma$-algebra, i.e. on a.e. ergodic component $C$ has measure $0$ or $1$; the average
$\mu(C) = 0$ forces measure $0$ a.e. The ergodic case then makes each component equal to $m_D$, so $\mu = m_D$. $\blacksquare$

**Theorem B is proved** (modulo the cited theorems (T1)–(T9) and Lemma 2.7/Lemma 3.1, proved above).

---

## 3. Transfer (Theorem A)

### 3.1 Lemma 4.1 (the continuous part of a stationary system)

**Lemma 4.1** (paper §4.1). *Let a standard probability space carry a measure-preserving action $(T_z)_{z\in E}$ of
the additive group $E$ (Koopman operators on $L^2$), and (possibly) a commuting action $(V_u)_{u\in K}$ with
$V_uT_zV_u^{-1} = T_{uz}$. Put*
$$H_c = \Big\{v\in L^2 : \lim_{z\to0,\,z\in E}\lVert T_zv-v\rVert_2 = 0\Big\}$$
*(the limit in the usual topology of $E\subset\mathbb{R}^2$). Then:*
*(1) $H_c$ is a closed translation-invariant subspace containing $1$;*
*(2) $H_c$ is the spectral subspace of the Borel set $C$, i.e. $v\in H_c\iff\lambda_v(C^c) = 0$;*
*(3) $H_c = L^2(\mathcal F_c)$ for the factor $\mathcal F_c$ generated by its bounded elements, so the orthogonal
projection onto $H_c$ is a conditional expectation (hence positive, unital, $L^\infty$-contractive);*
*(4) the operators extend to a strongly continuous unitary representation $(T_x)_{x\in\mathbb{R}^2}$ of
$\mathbb{R}^2$ on $H_c$, preserving the positive cone and fixing $1$;*
*(5) if the $V_u$ are present, $H_c$ is $V_u$-invariant and its projection commutes with $V_u$.*

*Proof.* (1) If $v_n\to v$ in $L^2$ and $v_n\in H_c$ then
$\lVert T_zv-v\rVert\le2\lVert v-v_n\rVert+\lVert T_zv_n-v_n\rVert$; constants are fixed by $T_z$, and $T_zH_c\subset H_c$.
(2) By (T2), $\lVert T_zv-v\rVert^2 = \int_D\lvert\psi_z-1\rvert^2d\lambda_v$. If $\lambda_v(C^c) = 0$ the integrand
vanishes on $C$ and tends to $0$ pointwise on $C$ as $z\to0$ in $\mathbb{R}^2$ (continuity of the characters
$j(\xi)$), so dominated convergence gives $v\in H_c$. Conversely, if $v\in H_c$ then
$F_v(z) = \langle v,T_zv\rangle$ satisfies $\lvert F_v(z+h)-F_v(z)\rvert\le\lVert v\rVert_2\lVert T_hv-v\rVert_2$, so
$F_v$ is uniformly continuous on $E$ and extends continuously to $\mathbb{R}^2$; the extension is positive definite
(approximate each finite list of real points by elements of $E$ and pass to the limit in the defining quadratic
form), so (T3) gives a finite measure $\rho$ on $\mathbb{R}^2$ with $F_v(z) = \int e^{i\xi\cdot z}d\rho$; the
pushforward $j_*\rho$ has the same Fourier coefficients on $D$ as $\lambda_v$, so by (T1) $j_*\rho = \lambda_v$ and
$\lambda_v(C^c) = \lambda_v(D)-\lambda_v(C) = \lVert v\rVert^2-j_*\rho(j(\mathbb{R}^2)) = \lVert v\rVert^2-\lVert v\rVert^2 = 0$.
(3) For bounded $v,w\in H_c$, $\lVert T_z(vw)-vw\rVert\le\lVert v\rVert_\infty\lVert T_zw-w\rVert+\lVert w\rVert_\infty\lVert T_zv-v\rVert$,
so $vw\in H_c$; for Lipschitz $\Phi$, $\lVert T_z\Phi(v)-\Phi(v)\rVert\le\mathrm{Lip}(\Phi)\lVert T_zv-v\rVert$, so
$H_c$ is closed under bounded Borel functional calculus and (by truncation) closed under the $L^2$-limits of its
bounded elements. Hence $H_c = L^2(\mathcal F_c)$ where $\mathcal F_c$ is generated by the bounded elements of $H_c$
(which form a bounded unital $*$-algebra): polynomials in finitely many generators approximate continuous functions
of the finite-dimensional distributions by Stone–Weierstrass, and monotone classes give all $\mathcal F_c$-measurable
functions. (4) For $x\in\mathbb{R}^2$ pick $z_n\in E$, $z_n\to x$; then
$\lVert T_{z_n}v-T_{z_m}v\rVert = \lVert T_{z_n-z_m}v-v\rVert\to0$ for $v\in H_c$, so $T_xv := \lim_nT_{z_n}v$ exists
and is independent of the sequence; unitarity, the group law, strong continuity and $T_x1 = 1$ follow by taking
limits, and $T_x$ preserves the closed positive cone as a strong limit of operators that do. (5) If $v\in H_c$ then
$\lVert T_zV_uv-V_uv\rVert = \lVert V_uT_{u^{-1}z}v-V_uv\rVert = \lVert T_{u^{-1}z}v-v\rVert\to0$; so $V_uH_c\subset H_c$
and $V_u^{-1}H_c\subset H_c$, i.e. equality, and the projection (an orthogonal projection onto an invariant subspace)
commutes with the unitary $V_u$. $\square$

### 3.2 Proposition 4.2 (proper $\Rightarrow$ weak measurable) and Theorem A

**Proposition 4.2** (paper §4.2). *Let $k\ge1$. If the plane has an unrestricted proper $k$-colouring then it has a
weak measurable $k$-colouring. Moreover the weak colouring produced has Borel colour classes and the exceptional
unit pairs form a Borel null set.*

*Proof.* *(i) An invariant law.* Restrict the colouring to $E$; the set $\Omega\subseteq\{1,\dots,k\}^E$ of proper
labelings of the unit-distance graph on $E$ is closed and non-empty, and $E\rtimes K$ acts on it continuously. That
group is amenable (extension of two abelian groups, (T4)), so averaging a point mass along a Følner sequence and
passing to a weak-* limit gives an invariant Borel probability $\mu$ on $\Omega$.
*(ii) Zero correlations.* Let $f_i$ be the indicator that the origin has label $i$, so $T_zf_i$ is the indicator that
$z$ has label $i$; rotations about the origin fix $f_i$, and properness gives
$$\int_\Omega f_i\,T_uf_i\,d\mu = 0\qquad(u\in K,\ 1\le i\le k). \tag{4.1}$$
Put $p_i = \mathbb E(f_i\mid\mathcal F_c)$, $b_i = f_i-p_i$. Then $0\le p_i\le1$, $\sum_ip_i = 1$, both are
rotation-fixed, the scalar spectral measure $\lambda_{b_i}$ is supported on $C^c$ (Lemma 4.1(2)) and is
$K$-invariant: $\langle b_i,T_{uz}b_i\rangle = \langle V_ub_i,T_{uz}V_ub_i\rangle = \langle b_i,T_zb_i\rangle$ using
$V_ub_i = b_i$ and $V_uT_zV_u^{-1} = T_{uz}$. If $\lambda_{b_i}\neq0$, normalise it and apply Theorem B: it is $m_D$,
whose Fourier coefficients vanish at every $z\neq0$. Hence
$\langle b_i,T_zb_i\rangle = 0$ for $z\in E\setminus\{0\}$. Since $H_c$ and $H_c^\perp$ are translation invariant,
the two cross terms in (4.1) vanish, so
$$\int_\Omega p_i\,T_up_i\,d\mu = -\int_\Omega b_i\,T_ub_i\,d\mu = 0\qquad(u\in K).$$
The algebraic unit directions are dense in $S^1$ (rational points of the circle lie in $K$), and
$u\mapsto T_up_i$ is strongly continuous on $\mathbb{R}^2$ by Lemma 4.1(4), so
$\langle p_i,T_up_i\rangle = 0$ for all $u\in S^1$; then for all $x\in\mathbb{R}^2$ and $u\in S^1$,
$$\int_\Omega(T_xp_i)(T_{x+u}p_i)\,d\mu = \langle T_xp_i,T_xT_up_i\rangle = \langle p_i,T_up_i\rangle = 0. \tag{4.2}$$
*(iii) A measurable field and one sample.* $x\mapsto T_xp_i$ is continuous from $\mathbb{R}^2$ to the separable
Hilbert space $L^2(\mu)$. Approximating by finite-valued simple maps with summable squared errors on each annulus of
a countable exhaustion, and taking measurable representatives of the finitely many values, one obtains a jointly
measurable field $(x,\omega)\mapsto\widetilde H_i(x,\omega)$ on $\mathbb{R}^2\times\Omega$ which represents
$T_xp_i$ in $L^2(\mu)$ for a.e. $x$: on each bounded annulus a subsequence converges a.e. in $x$, so its
product-space limit represents $T_xp_i$ at almost every $x$. Clamping $H_i = \max(0,\min(1,\mathrm{Re}\,\widetilde H_i))$
keeps this property and makes every field non-negative.
Let $N\subset\mathbb{R}^2$ be a null set outside which all the representations are correct, and note that
$\{(x,u) : x\in N\text{ or }x+u\in N\}$ is null for $dx\,d\sigma(u)$ by Fubini. Tonelli applied to (4.2) gives, for
every $m\in\mathbb{N}$,
$$\int_\Omega\sum_{i=1}^k\int_{B(0,m)}\int_{S^1}H_i(x,\omega)H_i(x+u,\omega)\,d\sigma(u)\,dx\,d\mu(\omega) = 0;$$
there are only countably many conditions (one per $m$ and $i$, plus $\sum_iH_i(x,\omega) = 1$ a.e. in $x$), so there
is a single $\omega$ satisfying all of them. Define $c(x)$ as the least $i$ with $H_i(x,\omega)>0$ where the sum is
$1$, and $c(x) = 1$ elsewhere. Then $c$ is Lebesgue measurable (indeed Borel if the fields are chosen Borel, which is
possible on a standard Borel model), and for each $i$
$$\{(x,u)\in\mathbb{R}^2\times S^1 : c(x) = c(x+u) = i\}\subseteq\{(x,u): H_i(x,\omega)H_i(x+u,\omega)>0\},$$
which is $dx\,d\sigma(u)$-null; so $\int\int\mathbf 1_{A_i}(x)\mathbf 1_{A_i}(x+u)\,d\sigma(u)dx = 0$. $\square$

**Lemma 4.3** (density-point properness; paper §4.2). *In a weak measurable $k$-colouring, the full-density-point
set of each class $A_i$ contains no unit pair; these sets are disjoint and their union is conull.*

*Proof.* Let $x,y = x+u$, $\lvert u\rvert = 1$, both be density-one points of $A_i$. For $h>0$ let $x'$ be uniform in
$B(x,h)$ and $u'$ uniform on an arc of the unit circle with $\lvert u'-u\rvert<h$. Then
$\mathbb P(x'\notin A_i) = o(1)$ and, since $x'+u'$ has a density bounded by $1/(\pi h^2)$ supported in $B(y,2h)$,
$\mathbb P(x'+u'\notin A_i)\le\lvert B(y,2h)\setminus A_i\rvert/(\pi h^2) = 4\,o(1)$. For small $h$ the probability
that both points lie in $A_i$ is positive. The law of $(x',u')$ is absolutely continuous with respect to
$dx\,d\sigma(u)$ (uniform disk times arc measure), and on the event in question $\lvert x'-(x'+u')\rvert = 1$ and both
endpoints lie in $A_i$; this contradicts the weak condition. Disjointness: two classes are disjoint up to a null set,
and two density-one sets cannot meet. Conullity: Lebesgue differentiation. $\square$

**Proof of Theorem A.** Proposition 4.2 is "$\Rightarrow$". For "$\Leftarrow$", Lemma 4.3 gives a conull set
partitioned into strictly unit-independent measurable classes. For any finite configuration $F\subset\mathbb{R}^2$ the
set of translations $t$ with $F+t$ inside that conull set is a finite intersection of conull sets, hence non-empty;
the unit-distance graph on $F+t$ is therefore properly $k$-colourable, with the colouring induced by $c$. In the
compact product space $\{1,\dots,k\}^{\mathbb{R}^2}$ every unit-edge condition is closed and involves two coordinates,
every finite family of these conditions involves a finite configuration and is satisfiable, so by compactness (T8)
some point satisfies all of them. $\blacksquare$

**Corollary 3.3.** $\chi(\mathbb{R}^2)\ge6$ is equivalent to the non-existence of a weak measurable 5-colouring;
combined with the paper's Theorem 1.4 it also gives $\chi_m(\mathbb{R}^2)\ge6$ for the *measurable* chromatic number
(a proper measurable colouring is in particular a weak measurable one). Theorem A plus Theorem 1.4 and the hexagonal
7-colouring therefore give $6\le\chi(\mathbb{R}^2)\le7$ and $6\le\chi_m(\mathbb{R}^2)\le7$.

---

## 4. Retractions, clarifications and sharpenings

**4.0 (retraction of two earlier claims).** An earlier version of this file reported two "literal defects" in §2–§4.
Both were misreadings of the paper and are withdrawn (the corrected readings are in Remarks 3.2.6 and 3.3.7):
*(i)* $a(h)$ in (3.7) is the $L^2$ \emph{norm} $\lVert PF_{j^*,h}\rVert_2$, not its square; the pair criterion
therefore gives $\operatorname{Avg}a^2\to0$ and Cauchy–Schwarz gives $\operatorname{Avg}a\to0$, exactly as printed;
*(ii)* the proof of Lemma 3.3 never identifies $\psi_{A-Bu^2}$ with $\psi_{R_u}$: it bounds the second side of (3.14)
directly and then uses the modulus identity (3.14) with radiality of $m$. No step in §2–§4 needs repair.

**4.1 (sharpening of Theorem A).** The weak measurable colouring produced by Proposition 4.2 can be taken with
Borel colour classes and with a Borel exceptional set of unit pairs (Proposition 4.2 and its proof above). The paper
only claims Lebesgue measurability. This matters in §§5–8, where palettes are built from "Borel representatives
forming a partition of the plane": Theorem A in the Borel form yields such representatives without a further
regularity argument.

**4.2 (sharpening: measurable chromatic number).** Since a proper measurable colouring is a weak measurable one,
Theorem 1.4 gives at once $6\le\chi_m(\mathbb{R}^2)\le7$ (Corollary 3.3). The paper states only
$6\le\chi(\mathbb{R}^2)\le 7$.

**4.3 (new structural lemma).** Lemma 1.3: every $z$ in the algebraic plane with $\lvert z\rvert\le2$ is a sum of two
elements of $K$; consequently $\langle K\rangle = E$ and the only $K$-invariant closed subgroups of $D$ are $\{0\}$
and $D$. Hence
*(a)* no Haar measure of a coset of a proper closed subgroup of $D$ is a $K$-invariant wild probability, so the
standard guess at a counterexample to Theorem B is impossible;
*(b)* $K$-invariance is essential: for $d\notin C$, $\delta_d$ is wild but not Haar (Remark 1.4);
*(c)* the same lemma is exactly what §3.5 uses to write $x_j = k_j+k'_j$ with $k_j,k'_j\in K$ (there with real
$x_j$, hence in the simpler form $k_j = x_j/2+i\sqrt{1-x_j^2/4}$).

**4.4 (the one step that the paper leaves as a black box).** The measurability selection inside Lemma 3.1 is asserted
in one sentence; it is proved in full in the separate file `fibre-selection.md` (Lemma S there), together with the
rest of Lemma 3.1's measurability layer, with all estimates explicit.

---

## 5. What this document does **not** verify

The lower bound $\chi(\mathbb{R}^2)\ge6$ is, by the results verified above, *equivalent* to the paper's Theorem 1.4
(no weak measurable 5-colouring). That theorem is the content of §§5–8 and is **not** refereed here. By the verdict
table of §0.1 the analytic core is sound, so **the entire mathematical burden of the paper rests on §§5–8**: palettes
(§5), transition graphs and local finiteness of cyclic centres (§6), the extraction of exclusion continua (§7), and
the exclusion of 3-, 4- and 5-cycles (§8).

As a partial down payment I verified the very last step of the paper independently and exactly. Everything is in
`work/moser_certificate.py` (exact rational interval arithmetic in $\mathbb{Q}(\sqrt3,\sqrt{11},\sqrt{33})$, no floating
point used in any decision).

* The seven-vertex graph of (8.5) is a unit-distance graph with all eleven listed edges of length exactly $1$
  ($\lvert\cdot\rvert^2 = 1$ identically), $\lvert T-0\rvert^2 = 3$, and it is not 3-colourable (the two equilateral
  triangles on $AB$ force $0$ and $T$ to share a colour; the rotated triangles force $0$ and $uT$ to share a colour;
  $\lvert T-uT\rvert = 1$).
* The placement (8.6) has $\lvert c\rvert^2 = 1$ for $c = (35+12i)/37$, so it is a congruence.
* For all seven vertices $z_g$, the exact values of $\lvert z_g\rvert^2$, $P = \upsilon^2(3\xi^2-\upsilon^2)^2$ and
  $P' = l^3(1-l/4)(l-1)^2$ satisfy $0<\lvert z_g\rvert^2<4$ and $P<P'$ strictly:

| $g$ | $\lvert z_g\rvert^2$ | $P$ | $P'$ |
|---|---|---|---|
| $0$ | $1.7008160\ldots$ | $0.8661244\ldots$ | $1.3889728\ldots$ |
| $A$ | $1.2876371\ldots$ | $0.0895503\ldots$ | $0.1197727\ldots$ |
| $B$ | $0.0956371\ldots$ | $0.0000017\ldots$ | $0.0006983\ldots$ |
| $T$ | $0.6824581\ldots$ | $0.0221255\ldots$ | $0.0265819\ldots$ |
| $uA$ | $2.7350076\ldots$ | $9.7252413\ldots$ | $19.4762921\ldots$ |
| $uB$ | $0.4592460\ldots$ | $0.0019927\ldots$ | $0.0250710\ldots$ |
| $uT$ | $2.4934376\ldots$ | $12.5743611\ldots$ | $13.0225720\ldots$ |

  The tightest vertex is $T$, with $P/P' = 0.8324\ldots$; the paper's Table 1 bounds
  $P<P^+<P'^-<P'$ hold in all seven rows. So Lemma 8.9 (the seven-point certificate) is **correct**, and with
  comfortable margins.
* For the upper bound, $r = 2/5$ gives $2r = 4/5<1$ and $(\sqrt{21}-2)r = 1.03303\ldots>1$ exactly
  ($2\sqrt{21}>9\iff84>81$), so the hexagonal 7-colouring of §1 is proper, boundaries included.
