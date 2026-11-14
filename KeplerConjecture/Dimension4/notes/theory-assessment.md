# Dimension 4: analytic feasibility and class obstructions

This note records an independent mathematical assessment during the one-hour research sprint on 2026-11-14. The exact certificate remains conjectural. The propositions below are elementary deductions or consequences of explicitly cited theorems; no novelty is claimed, and none has been formalized in Lean.

The promising target is a function of **two vectors with genuine angular dependence**. Finite real Gaussian expansions cannot attain exactness; neither can finite-total-variation mixtures of centered real positive Gaussians with uniformly bounded polynomial degree. Products of radial four-dimensional functions cannot attain it either, even if an infinite expansion is allowed. Matrix-valued Gaussian transforms supply an appropriate analytic language, but they do not supply the missing global inequalities.

## 1. The normalization and what equality requires

Use

$$
\widehat f(\xi,\eta)=\int_{\mathbb R^4\times\mathbb R^4}
f(x,y)e^{-2\pi i(x\cdot\xi+y\cdot\eta)}\,dx\,dy.
$$

Let $D_4=\{a\in\mathbb Z^4:\sum a_i\equiv0\pmod2\}$, with covolume 2 and minimum norm $\sqrt2$. Set

$$
S=\{(x,y):|x|,|y|,|x+y|,|x-y|\in\{0\}\cup[\sqrt2,\infty)\}.
$$

The desired real Schwartz function satisfies

$$
f(0,0)=1,\qquad \widehat f(0,0)=4,\qquad
\widehat f\geq0,\qquad f|_{S\setminus\{0\}}\leq0.
$$

The lattice density bound is

$$
\operatorname{vol}(B^4_{1/\sqrt2})
\sqrt{\frac{f(0,0)}{\widehat f(0,0)}}
=\frac{\pi^2}{8}\cdot\frac12=\frac{\pi^2}{16}.
$$

This is the setting of Cohn–de Laat–Salmon, Theorem 1.4 and Conjecture 6.1, and concerns lattice packings. It does not certify unrestricted sphere packing. [Primary source](https://arxiv.org/html/2206.15373#S4).

For a Schwartz function Poisson summation is absolutely convergent, and gives

$$
1\ \geq\sum_{x,y\in D_4}f(x,y)
=\frac14\sum_{\xi,\eta\in D_4^*}\widehat f(\xi,\eta)
\ \geq\frac14\widehat f(0,0)=1.
$$

Every non-origin term on the left has a nonpositive sign, and every non-origin term on the right has a nonnegative sign. Equality therefore forces

$$
f|_{(D_4\times D_4)\setminus\{0\}}=0,
\qquad
\widehat f|_{(D_4^*\times D_4^*)\setminus\{0\}}=0.
$$

The origin must be excluded from both zero sets. These are necessary conditions, not replacements for the inequalities on the full continuum.

## 2. Exactness excludes every finite real Gaussian expansion

**Proposition.** A function of the form

$$
f(z)=\sum_{j=1}^N P_j(z)e^{-z^{\mathsf T}A_jz},
\qquad z\in\mathbb R^8,
$$

where the $P_j$ are polynomials and the $A_j$ are real positive-definite symmetric matrices, cannot be an exact certificate with $f(0)=1$.

**Proof.** Fix a nonzero $v\in D_4$, put $w=(v,0)$, and restrict to the ray $z=sw$. Group terms with equal positive numbers $w^{\mathsf T}A_jw$, obtaining

$$
f(sw)=\sum_{k=1}^M q_k(s)e^{-a_ks^2},\qquad a_1<\cdots<a_M.
$$

Complementary slackness gives $f(mw)=0$ for every positive integer $m$. After multiplication by $e^{a_1m^2}$,

$$
q_1(m)=-\sum_{k=2}^M q_k(m)e^{-(a_k-a_1)m^2}\longrightarrow0.
$$

A nonzero polynomial cannot tend to zero along the positive integers, so $q_1=0$. Repeating proves $q_k=0$ for every $k$. Consequently $f(sw)=0$ for every real $s$, including $s=0$, a contradiction. $\square$

The same proof covers finitely many real shifted Gaussians. Along the ray their exponents are $-a_js^2+b_js+c_j$; grouping equal $(a_j,b_j)$ and ordering first by smallest $a_j$, then largest $b_j$, again leaves one asymptotically dominant polynomial. Oscillatory complex phases are excluded from this statement.

This proposition does **not** prohibit arbitrarily close numerical upper bounds from polynomial–Gaussian spaces. It prohibits exact attainment in any fixed finite such space. Infinite Hermite series and modular contour formulas remain possible, subject to the further integral-class restriction below.

### A stronger obstruction for absolutely convergent real Gaussian integrals

For simultaneously invariant functions, the whole sequence of D4 shell radii gives a stronger obstruction than the single lattice ray. Every even positive integer $2m$ is the squared norm of a D4 vector: Lagrange's four-square theorem represents $2m$ by four integer squares, and the parity of their sum equals the parity of the sum of their squares. Hence an exact invariant certificate must satisfy

$$
f(\sqrt{2m}e_1,0)=0\qquad(m=1,2,\ldots).
$$

Here is an elementary moment argument that applies to a large integral class.

**Bounded-degree Laplace-profile obstruction.** Suppose

$$
H(u)=\sum_{k=0}^K u^k\int_{(0,\infty)}e^{-au}\,d\mu_k(a),
\qquad u\geq0,
$$

where $K$ is finite and every $\mu_k$ is a complex measure of finite total variation. If $H(2m)=0$ for every positive integer $m$, then $H(0)=0$.

**Proof.** Push $\mu_k$ forward by $q=e^{-2a}\in(0,1)$, obtaining finite complex measures $\nu_k$. On polynomials let $D=q\,d/dq$ and define

$$
T(p)=\sum_{k=0}^K 2^k\int D^kp(q)\,d\nu_k(q).
$$

Since $D^kq^m=m^kq^m$, the assumed zeros say $T(q^m)=0$ for every integer $m\geq1$. In particular,

$$
p_N(q)=1-(1-q)^N
\quad\Longrightarrow\quad T(p_N)=0,
$$

because $p_N$ has no constant term. For $k=0$, $0\leq p_N\leq1$ and $p_N(q)\to1$ on $(0,1)$. For $k\geq1$,

$$
D^kp_N(q)
=\sum_{j=1}^k(-1)^{j+1}
\left\{\begin{matrix}k\\j\end{matrix}\right\}
(N)_j q^j(1-q)^{N-j},
$$

where the braces denote Stirling numbers of the second kind and $(N)_j$ is a falling factorial. For $N\geq k$, each summand tends to zero at every $q\in(0,1)$, and

$$
0\leq (N)_j q^j(1-q)^{N-j}
=j!\binom Nj q^j(1-q)^{N-j}\leq j!.
$$

Thus all $D^kp_N$ have bounds independent of $N$, and dominated convergence with respect to the total-variation measures yields

$$
0=\lim_{N\to\infty}T(p_N)=\nu_0((0,1))=H(0).
$$

This proves the claim. No restriction on the number of sign changes of the measures is needed. $\square$

**Matrix-Gaussian consequence.** Consider

$$
f(X)=\int_{Y>0}e^{-\pi\operatorname{tr}(YX^{\mathsf T}X)}\,d\mu(Y),
$$

where $Y$ ranges over real positive-definite symmetric $2\times2$ matrices and $\mu$ is any complex measure of finite total variation. This function is simultaneously orthogonally invariant. Its axis restriction is

$$
H(u)=f(\sqrt u e_1,0)
=\int e^{-\pi Y_{11}u}\,d\mu(Y),
$$

which is a Laplace profile with $K=0$. Therefore it cannot have the required shell zeros and $f(0)=1$. The same conclusion holds if the integrand includes polynomial factors in $u,v,t$ of uniformly bounded degree, provided their coefficient measures have finite total variation: the axis restriction then has the displayed form with finite $K$.

There is also a corollary for arbitrary centered real positive-definite Gaussian matrices on $\mathbb R^8$. If such a finite-total-variation mixture were an exact certificate with the stated normalization, simultaneous $O(4)$ averaging would preserve exact feasibility and the mixture class. The averaged axis restriction is again a finite-measure Laplace profile, and the same contradiction follows. Uniformly bounded polynomial degree is covered when all polynomial coefficient measures have finite total variation.

The assumptions matter. This does not exclude unbounded-degree Hermite expansions, non-absolutely convergent representations requiring regularization, or genuinely complex Gaussian parameters. Signed or complex **weights alone**, with real positive Gaussian matrices and the stated absolute convergence, do not escape the obstruction. The Gaussian parameters themselves make $q=e^{-2a}$ lie in the real interval $(0,1)$ used in the proof; changing coefficient signs does not change that interval.

## 3. The angular variable is indispensable

Write $u=|x|^2$, $v=|y|^2$, and $t=x\cdot y$. Averaging over simultaneous orthogonal transformations, interchange of $x,y$, and independent sign changes preserves feasibility. Thus one may search for

$$
f(x,y)=\Phi(u,v,t),\qquad
\Phi(u,v,t)=\Phi(v,u,t)=\Phi(u,v,-t).
$$

These compact symmetries do not justify averaging over separate orthogonal transformations of $x$ and $y$: that would erase $t$, which is mathematically necessary.

**Proposition.** If $f(x,y)=F(|x|^2,|y|^2)$, then its three-point lattice objective is at least the ordinary two-point Cohn–Elkies optimum $\Delta_2(4)$.

**Proof.** If $|x|,|y|\geq r$, choose perpendicular vectors with these same lengths. Their sum and difference have length $\sqrt{|x|^2+|y|^2}\geq r$, so the lattice sign condition and angle independence imply $f(x,y)\leq0$ for all such $x,y$. The axis signs $f(x,0)\leq0$, $f(0,y)\leq0$ also hold for norms at least $r$.

These are precisely the signs in the disjunctive-product optimization. At arbitrary scale $r$, its objective is

$$
\operatorname{vol}(B^4_{r/2})^2\frac{f(0,0)}{\widehat f(0,0)}.
$$

Cohn–de Laat–Salmon, Definition 4.5 and Proposition 4.7, identify its infimum with $\Delta_2(4)^2$. Taking square roots proves the claim. [Product theorem](https://arxiv.org/html/2206.15373#S4.SS1).

Li's rigorous dual bounds imply $\Delta_2(4)>\pi^2/16$, so angle-independent functions cannot be exact D4 certificates. [Li, *Dual Linear Programming Bounds for Sphere Packing via Discrete Reductions*](https://arxiv.org/abs/2206.09876).

This rules out any convergent ansatz consisting entirely of products of radial functions of $x$ and $y$, regardless of whether its ingredients come from modular forms. It does not rule out factors depending on $x+y$, $x-y$, or other expressions that retain angular dependence.

**Adding kernel positivity is also too restrictive.** Suppose, in addition to the required full Fourier positivity, one imposes positive semidefiniteness of $f$ as a kernel on $\mathbb R^4$: every matrix $(f(x_i,x_j))_{i,j}$ is positive semidefinite. Its diagonal is nonnegative, whereas the lattice sign condition gives $f(x,x)\leq0$ whenever $|x|\geq\sqrt2$. Hence $f(x,x)=0$ there. The kernel Cauchy–Schwarz inequality

$$
|f(x,y)|^2\leq f(x,x)f(y,y)
$$

forces $f(x,y)=0$ whenever either argument has norm at least $\sqrt2$. In particular, all disjunctive-product signs hold, so the same two-point obstruction excludes exactness. Thus positive semidefiniteness as a two-argument kernel cannot be added as a convenient sufficient condition here. It is a different condition from nonnegativity of the full eight-dimensional Fourier transform.

**Necessary positive region.** More generally, any exact certificate must take a positive value at some pair with

$$
|x|,|y|\geq\sqrt2,
\qquad
0<\min\{|x-y|,|x+y|\}<\sqrt2.
$$

Otherwise it would have all disjunctive-product signs and the same obstruction would apply. Thus the exact function must exploit the excluded neighborhoods of the diagonal or antidiagonal. The exact diagonal and antidiagonal themselves belong to $S$, where the function must be nonpositive. This is a useful qualitative diagnostic for a computed candidate.

**An elementary special case.** Full radial symmetry in $\mathbb R^8$ is impossible even without Li's bound. An axis pair $(x,0)$ occurs at every total radius at least $\sqrt2$. Therefore a fully radial feasible $f$ would be nonpositive at every point of $\mathbb R^8$ outside that ball. Poisson summation on the covolume-one lattice $E_8$, whose minimum norm is $\sqrt2$, would then give $f(0)\geq\widehat f(0)$, contradicting $1<4$.

## 4. Isodual scaling gives a useful Fourier-eigenfunction formulation

Let

$$
A=\frac12\begin{pmatrix}
1&1&0&0\\1&-1&0&0\\0&0&1&1\\0&0&1&-1
\end{pmatrix},\qquad Q=\sqrt2 A.
$$

Then $AA^{\mathsf T}=I/2$, $Q$ is orthogonal, and $AD_4=D_4^*$. To check the latter identity directly, the image of an even-sum integer vector has either four integer coordinates or four half-integer coordinates. These give exactly

$$
D_4^*=\mathbb Z^4\cup\left(\mathbb Z^4+(1/2,1/2,1/2,1/2)\right).
$$

Now put $L_0=2^{-1/4}D_4$. It has covolume 1, minimum norm $2^{1/4}$, and $L_0^*=QL_0$. For a candidate $f$, define

$$
g(x,y)=f(2^{1/4}x,2^{1/4}y).
$$

Because the ambient dimension is eight,

$$
\widehat g(\xi,\eta)=\frac14\widehat f(2^{-1/4}\xi,2^{-1/4}\eta),
\qquad g(0)=\widehat g(0)=1.
$$

After simultaneous orthogonal averaging, both $g$ and $\widehat g$ vanish on $(L_0\times L_0)\setminus\{0\}$. The Fourier-even and Fourier-odd parts

$$
g_+=\frac{g+\widehat g}{2},\qquad
g_-=\frac{g-\widehat g}{2}
$$

satisfy $\widehat g_+=g_+$, $\widehat g_-=-g_-$, $g_+(0)=1$, and $g_-(0)=0$. Here $g$ is even, so the square of its Fourier transform is the identity.

With the sign threshold rescaled to $2^{1/4}$, the remaining inequalities are

$$
g_+-g_-\geq0\quad\hbox{everywhere},\qquad
g_++g_-\leq0\quad\hbox{on the rescaled }S\setminus\{0\}.
$$

In particular, $g_-\leq-|g_+|$ on that sign region. The eigenfunction decomposition organizes the problem; it does not make either sign condition automatic, and neither component is independently a packing certificate.

## 5. A matrix-Gaussian route that preserves the angle

Let $X=[x\ y]$ be a real $4\times2$ matrix and $G=X^{\mathsf T}X$. For a complex symmetric $2\times2$ matrix $Z$ with positive-definite imaginary part, define

$$
K_Z(X)=\exp\!\left(\pi i\operatorname{tr}(ZG)\right).
$$

The ordinary two-dimensional Gaussian Fourier integral, applied to each of the four rows of $X$, yields

$$
\widehat K_Z(Y)
=\det(-iZ)^{-2}\exp\!\left(\pi i\operatorname{tr}(-Z^{-1}Y^{\mathsf T}Y)\right).
$$

This formula is exact. Its exponent includes $u$, $v$, and $t$; it does not discard angular information. It suggests studying integrals of $K_Z$ over suitable contours with weights adapted to $Z\mapsto-Z^{-1}$. Section 2 excludes the simplest version with $Z=iY$, $Y>0$, and finite-total-variation coefficient measures. A successful integral would have to use features outside that class, such as genuinely complex Gaussian parameters or a justified regularization.

There is a useful conditional calculation for a three-real-dimensional contour integral $f(X)=\int_\Gamma\varphi(Z)K_Z(X)\,dZ_{11}\,dZ_{12}\,dZ_{22}$. Under $Z=-W^{-1}$, the differential on symmetric matrices has Jacobian $\det(W)^{-3}$, while the Fourier Gaussian factor becomes $\det(W)^2$. The net multiplier is therefore $\det(W)^{-1}$. If the transformed contour agrees with the original with its orientation, the necessary exchanges and changes of contour are justified, and no residues or boundary terms occur, the relation

$$
\varphi(-W^{-1})=\varepsilon\det(W)\varphi(W)
$$

would give $\widehat f=\varepsilon f$. This is a weight-one transformation under inversion for this particular ansatz, not an existence theorem for a suitable Siegel modular form or contour. Level, characters, vector-valued forms, other integration cycles, or regularization may alter the construction; regularity and signs remain separate requirements.

For a rank-four lattice $L$, define the degree-two theta series

$$
\Theta_L^{(2)}(Z)=\sum_{x,y\in L}
\exp\!\left(\pi i\operatorname{tr}(ZX^{\mathsf T}X)\right).
$$

Poisson summation and the preceding Gaussian identity give

$$
\Theta_L^{(2)}(-Z^{-1})
=\frac{\det(-iZ)^2}{\operatorname{covol}(L)^2}
\Theta_{L^*}^{(2)}(Z).
$$

Consequently D4 has the explicit inversion relation

$$
\Theta_{D_4}^{(2)}(-Z^{-1})
=\frac14\det(-iZ)^2\Theta_{D_4^*}^{(2)}(Z)
=\frac14\det(-iZ)^2\Theta_{D_4}^{(2)}(Z/2).
$$

For $L_0$, the covolume factor disappears and its dual theta series equals its own. These identities provide a coherent analytic starting point. They leave open the choice of weights, contours, convergence, nonzero origin value, all required lattice zeros, and both global signs.

The appearance of genus two must be interpreted carefully. Cohn–de Laat–Salmon's Remark 4.1 discusses Siegel modular forms for **dual summation formulas** after additional lattice constraints are included. This is not a construction of a primal exact certificate. [Remark 4.1](https://arxiv.org/html/2206.15373#S4).

Moreover, the original four-length region is not invariant under all of $\mathrm{GL}_2(\mathbb Z)$. For example, take

$$
y=(1,1,0,0),\qquad x=(-3/2,-5/2,0,0).
$$

The four squared lengths are $17/2,2,5/2,37/2$, so $(x,y)\in S$. After the shear $(x,y)\mapsto(x+y,y)$, one required vector is $x+2y=(1/2,-1/2,0,0)$, with squared length $1/2$, so the new pair is outside $S$. Adding constraints for all primitive integer combinations changes the optimization problem and restores this group action. Averaging over the resulting infinite group still requires a separate convergence argument.

## 6. Constraints worth testing before guessing a closed form

### A single angular harmonic correction is still insufficient

There is a sharper obstruction than angle independence. Suppose a simultaneously invariant candidate has the form

$$
f(x,y)=A(r,s)+(rs)^\ell C_\ell^1(c)B(r,s),
\qquad r=|x|,\ s=|y|,\ c=\frac{x\cdot y}{rs},
$$

for one positive even integer $\ell$, with the expression extending smoothly across the axes. The radial profiles may be arbitrary; they need not be finite polynomial–Gaussian sums.

**Proposition.** No such function can beat the ordinary two-point optimum in the three-point lattice bound.

**Proof.** The Gegenbauer polynomial here is the Chebyshev polynomial of the second kind:

$$
C_\ell^1(\cos\theta)=\frac{\sin((\ell+1)\theta)}{\sin\theta}.
$$

For even $\ell$, it has a root

$$
c_\ell=\sin\!\left(\frac{\pi}{2(\ell+1)}\right)\in(0,1/2].
$$

For every $r,s\geq r_0$, choose the angle $c=c_\ell$. Then

$$
|x\pm y|^2\geq r^2+s^2-rs\geq\min(r^2,s^2)\geq r_0^2.
$$

Thus the lattice sign condition forces $A(r,s)=f(x,y)\leq0$ for all $r,s\geq r_0$. On the axes, the same sign holds. Independent rotational averaging removes the nonconstant spherical harmonic, so the function $(x,y)\mapsto A(|x|,|y|)$ has nonnegative Fourier transform and retains both origin normalizations. It therefore satisfies all disjunctive-product conditions, and Section 3 applies. $\square$

The argument also excludes any collection of nonconstant angular sectors sharing a zero in $[-1/2,1/2]$. For example, all even degrees $\ell\equiv2\pmod6$ vanish at $c=1/2$. With an infinite expansion this conclusion requires convergence sufficient to evaluate the sum and perform rotational averaging.

There is a useful extension. Suppose the nonconstant angular degrees form a set $E$, and a probability measure $\nu$ supported on $[-1/2,1/2]$ satisfies

$$
\int U_\ell(c)\,d\nu(c)=0\qquad(\ell\in E).
$$

Integrating the required signs at these safe angles again gives $A(r,s)\leq0$ for all $r,s\geq r_0$. Ordinary independent rotational averaging still shows that $A$ is Fourier-positive with unchanged normalization. Thus the same obstruction applies. The common-zero criterion is the case of a point mass, but it is not the only case.

For example, the two sectors $E=\{4,6\}$ have no common root, yet

$$
\nu=\tfrac12\delta_0+\tfrac12\delta_{1/2}
$$

annihilates both: $U_4(0)=1$, $U_4(1/2)=-1$, $U_6(0)=-1$, and $U_6(1/2)=1$. So the class with angular degrees $0,4,6$ cannot beat the two-point optimum either. The same measure excludes any collection of even degrees congruent to $4$ or $6$ modulo $12$. This provides a small positive-moment feasibility test for proposed angular families before their radial functions are chosen.

This is especially relevant to importing Viazovska ingredients. The solid harmonic

$$
Z_\ell(x,y)=(rs)^\ell C_\ell^1(c)
$$

is harmonic of degree $\ell$ in each four-dimensional variable. The Hecke–Bochner identity gives, for radial Schwartz profiles $a,b$,

$$
\mathcal F_{\mathbb R^4\times\mathbb R^4}
\bigl[Z_\ell(x,y)a(r)b(s)\bigr]
=(-1)^\ell Z_\ell(\xi,\eta)
(\mathcal F_{4+2\ell}a)(|\xi|)
(\mathcal F_{4+2\ell}b)(|\eta|).
$$

One can obtain this by applying the harmonic Gaussian transform separately in the two variables and then extending by density. Stoller's Proposition 2.1 records the corresponding dimension-shifting Fourier relation with the same Fourier convention. [Primary reference](https://arxiv.org/html/2002.11627#S2).

Hence $\ell=2$ uses radial transforms in dimension 8 and $\ell=10$ uses dimension 24. This is an exact bridge to known modular Fourier eigenfunctions. However, each such sector vanishes on the axes and at the origin, so it cannot provide the normalization. More strongly, the preceding proposition says that adding just one of these sectors to an angle-independent base still cannot be sharp. At least two nonconstant angular sectors without a common safe-angle zero are needed in this kind of ansatz. This is a necessary condition, not a sufficiency theorem.

### Zeros, derivatives, and shellwise angular profiles

The axis also carries a useful scalar constraint. Take a swap-symmetric candidate, as allowed by the averaging above, and set $h(x)=f(x,0)$. Fourier inversion in the second variable gives

$$
\widehat h(\xi)=\int_{\mathbb R^4}\widehat f(\xi,\eta)\,d\eta\geq0.
$$

Since $h(0)=1$ and $h(x)\leq0$ for $|x|\geq\sqrt2$, it is an admissible ordinary Cohn–Elkies function. Its integral $\alpha=\widehat h(0)$ is positive, because $\widehat f(0,0)=4$ and $\widehat f$ is continuous. Therefore

$$
\alpha\leq\frac{\operatorname{vol}(B^4_{1/\sqrt2})}{\Delta_2(4)}<2.
$$

In contrast, the full integral of $f$ must equal four. The marginal $g(x)=\int f(x,y)\,dy$ has $g(0)=\alpha$, $\widehat g(0)=4$, and $\widehat g(\xi)=\widehat f(\xi,0)\geq0$. It cannot also be nonpositive for every $|x|\geq\sqrt2$: that would make it another scalar certificate and imply $\alpha\geq4\Delta_2(4)/\operatorname{vol}(B^4_{1/\sqrt2})>2$. Thus integration in the second argument must produce positive values somewhere outside the exclusion radius, despite the nonpositive axis restriction.

On the first primal shell pair, $r=s=\sqrt2$, the lattice angles are $c=0,\pm1/2,\pm1$. An even angular polynomial can be written $p(w)$ with $w=c^2$. If it is nonzero and has all required zeros, its degree in $w$ is at least three, because $w(w-1/4)(w-1)$ divides it. Thus an angular cutoff below six forces this entire shell slice to vanish.

There is a stronger Fourier-side condition at the first dual shell pair, $r=s=1$. A nonzero polynomial $p(w)\geq0$ on $[0,1]$ with zeros at $0,1/4,1$ must have at least a double zero at the interior point $1/4$. Its degree is therefore at least four, corresponding to angular degree at least eight. Consequently, angular cutoff at most six forces the entire first dual shell slice to vanish. These are restrictions on shellwise radial coefficient values, not proofs that the whole finite-angular class is impossible: an entire shell slice is allowed to be zero.

At every nonzero dual-lattice pair, $\widehat f$ has a global nonnegative minimum of zero. Therefore its full gradient vanishes and its Hessian is positive semidefinite. At a primal lattice pair where all four lengths are nonzero and strictly greater than $\sqrt2$, the point is interior to $S$: the gradient of $f$ vanishes and its Hessian is negative semidefinite. Boundary points and the axes require separate treatment; a root at the minimum radius need not have the same multiplicity as an interior zero.

These conditions are stronger than a finite table of function values. A useful next computation would recover normalized jets at several Gram triples, compare their stability as the Gaussian degree grows, and test the necessary positive regions described above. Stable jets and signs could guide a matrix-integral ansatz. A handful of nearly zero samples, or a fitted rational coefficient list without global positivity, would not establish an exact certificate.

### A sufficient compactness condition for an exact limiting function

Suppose a sequence of feasible Schwartz functions satisfies $f_j(0)=1$, $\widehat f_j(0)\to4$, and, for every nonnegative integer $N$ and every derivative multi-index $\alpha$,

$$
\sup_j\sup_{z\in\mathbb R^8}
(1+|z|)^N|\partial^\alpha f_j(z)|<\infty.
$$

Then a subsequence converges in the Schwartz topology to an exact certificate. Indeed, uniform bounds on successive derivatives give a diagonal Arzelà–Ascoli subsequence on compact sets; the higher weighted bounds control tails and upgrade convergence to every Schwartz seminorm. The Fourier transform is continuous in this topology. Both normalization values converge, and the two pointwise sign inequalities are closed under this convergence.

This is a sufficient criterion, not an estimate established here. Convergence of objective values does not imply these uniform derivative and tail bounds. Thus proving that the infimum equals the target and proving the existence of a Schwartz optimizer remain different tasks. This distinction is consistent with the attainment questions discussed in Section 3 of [Cohn–de Laat–Salmon](https://arxiv.org/html/2206.15373#S3).

The specific mathematical milestone is now narrow: construct or obstruct an angular function beyond the excluded finite Gaussian families that satisfies the two global signs at ratio $1/4$. Finding such a function would give a new analytic lattice proof. Extending it to arbitrary packings would require another theorem, because the closure conditions $x\pm y\in L$ used here do not hold for a general packing.
