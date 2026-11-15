# The determinant argument and its quantitative inputs

The construction reduces irrationality of $\xi=\zeta(5)$ to integer polynomials of degree $O(n)$ whose nonzero values at $\xi$ decay like $\exp(-cn^2)$. The algebra, positivity, and final contradiction are separate from the difficult arithmetic and analytic estimates. The project’s reviewed [overview](artifacts/ProofOverview/zeta5_irrationality_overview.pdf), with [editable source](artifacts/ProofOverview/zeta5_irrationality_overview.tex), makes the latter two estimates explicit assumptions. In particular, it uses Fauzan’s original arithmetic estimate, not Lai’s corrected statement literally as printed.

For a longer backward exposition, start with the existing [proof overview](../PROOF_OVERVIEW.md) and [ProofGuide](../ProofGuide/SECTIONS_8_12_ROLE.md). Section numbers below refer to [Chun Wing Lai’s version 1, 29 September 2026](https://ai.vixra.org/pdf/2609.0080v1.pdf); original arithmetic formulas refer to [Aabir Fauzan’s 17 September 2026 manuscript](https://zenodo.org/records/22826419).

## The final implication needs an upper degree bound

Suppose that for all sufficiently large integers $n$ there are $Q_n\in\mathbb Z[X]$ with

$$
\deg Q_n\le37n,\qquad 0<|Q_n(\xi)|\le e^{-cn^2},\qquad c>0.
$$

If $\xi=a/b$ with $b>0$, then $b^{37n}Q_n(a/b)$ is a nonzero integer, whereas

$$
0<|b^{37n}Q_n(a/b)|\le\exp(37n\log b-cn^2)\longrightarrow0.
$$

This is Lai’s Lemma 3.1. Exact degree and small individual coefficients are unnecessary. The essential comparison is quadratic exponential decay against the linear exponent incurred by clearing a fixed rational denominator. Apéry’s small nonzero integer linear forms use the same obstruction: if $u_n,v_n\in\mathbb Z$ and $0<|u_n\xi-v_n|\to0$, rationality would produce a nonzero integer tending to zero after multiplication by the fixed denominator of $\xi$.

## Why the parameters have these meanings

Set

$$
K=40n,\quad N=3n,\quad h=K-N=37n,\quad
\alpha=N/K=3/40,\quad\lambda=h/K=37/40,\quad H=(h+3N)/K=23/20.
$$

These record structural counts rather than independent choices:

| Quantity | Role |
| --- | --- |
| $K$ | Main scale and largest index in $D_K(t)=\prod_{j=1}^K(t+j^2)$. |
| $N$ | Numerator cutoff; the first $N$ poles cancel. |
| $h=K-N$ | Number of remaining poles and chosen matrix size. |
| $\alpha$ | Endpoint in the limiting numerator integral. |
| $\lambda$ | Mass of the empirical measure $K^{-1}\sum_{i=1}^h\delta_{t_i}$. |
| $H=1+2\alpha$ | Degree bound for factors $D_N(t)^3q(t)$ with $\deg q<h$. |

The ratio $3/40$ is a design choice used to balance arithmetic cost and analytic decay. The source does not characterize it as uniquely forced or optimal. A different rational ratio preserves these structural meanings but requires new quantitative estimates.

## The functional connects rational algebra to a positive integral

For rational functions with polynomial part and finitely many simple poles at negative integer squares, define $\mu_X$ by linearity from

$$
\mu_X(t^e)=\frac{(-1)^e B_{2e+2}(2e+3)(2e+4)(2e+5)}{24},
$$

$$
\mu_X\!\left(\frac1{t+j^2}\right)
=j^4\bigl(X-H_j^{(5)}\bigr)-\frac14+\frac1{2j},
\qquad H_j^{(5)}=\sum_{v=1}^jv^{-5}.
$$

Here $B_1=-1/2$. Every value is affine in $X$: polynomial inputs contribute rational constants, and only pole inputs contribute $X$. At $X=\xi$,

$$
\mu_\xi(R)=\int_0^\infty R(y^2)w(y)\,dy,
\qquad
w(y)=\frac{(2\pi)^4y^5}{12}\sum_{\ell\ge1}\ell^4e^{-2\pi\ell y}>0.
$$

The weight is bounded near zero and decays exponentially at infinity. The identity is checked on monomials by Euler’s formula for even zeta values and on simple fractions by the Hurwitz zeta integral, then extended by partial fractions and linearity. See [the moment companion](../ProofGuide/07_MOMENT_REPRESENTATION.md) and the overview source for the explicit calculations.

Define

$$
A_K(t)=\frac{D_N(t)^6}{D_K(t)}
=\frac{D_N(t)^5}{D_{\rm tail}(t)},\qquad
D_{\rm tail}(t)=\prod_{k=N+1}^K(t+k^2),
$$

$$
G_K(X)_{ij}=\mu_X(A_K(t)t^{i+j}),\quad 0\le i,j<h,
\qquad \Delta_K(X)=\det G_K(X).
$$

The entries are affine in $X$, so $\deg\Delta_K\le h$. At $\xi$, this is the Gram matrix of $1,y^2,\ldots,y^{2h-2}$ against $A_K(y^2)w(y)\,dy$. For nonzero $q$, the integral of $q(y^2)^2A_K(y^2)w(y)$ is strictly positive. Thus $G_K(\xi)$ is positive definite and $\Delta_K(\xi)>0$.

## Exact degree comes from the remaining poles

Write $G_K(X)=G_0+XG_1$. The coefficient of $X^h$ in its determinant is $\det G_1$, since an $X^h$ term selects the linear part from every entry in a determinant product. Partial fractions give

$$
G_1=V\operatorname{diag}(d_{N+1},\ldots,d_K)V^{\mathsf T},\qquad
V_{ik}=(-k^2)^i,\qquad
d_k=\frac{k^4D_N(-k^2)^5}{D_{\rm tail}'(-k^2)}.
$$

There are exactly $h$ distinct nodes and every $d_k$ is nonzero. The square Vandermonde matrix $V$ is invertible, proving exact degree $h$. Cancelling the derivative denominators gives the stronger identity

$$
[X^h]\Delta_K(X)
=(-1)^{h(h-1)/2}\prod_{k=N+1}^K k^4D_N(-k^2)^5\in\mathbb Z\setminus\{0\}.
$$

The powers of the auxiliary variable $t$ do not contribute to degree in $X$. Also, choosing a larger matrix size than the number of remaining poles would make the top coefficient vanish by rank. See [the Hankel companion](../ProofGuide/06_HANKEL_CONSTRUCTION.md).

## Andréief explains the squared Vandermonde and the factorial

With $W_K(y)=A_K(y^2)w(y)$, Andréief’s identity yields

$$
\Delta_K(\xi)=\frac1{h!}\int_{(0,\infty)^h}
\prod_{i<j}(y_i^2-y_j^2)^2\prod_{i=1}^h W_K(y_i)\,dy_i.
$$

The evaluation matrix has rows $1,y^2,\ldots,y^{2h-2}$, hence is Vandermonde in the squared variables. Expanding two determinants and grouping by the relative permutation produces $h!$ copies of the Gram determinant. For $h=2$, the formula is simply

$$
\frac12\iint(y_1^2-y_2^2)^2W_K(y_1)W_K(y_2)\,dy_1dy_2=M_0M_2-M_1^2,
\quad M_r=\int y^{2r}W_K(y)\,dy.
$$

Lai’s printed Lemma 11.6 mixes ordinary moments and even moments. Ordinary moments in $t$ produce $(t_i-t_j)^2$; even moments in $y$ produce $(y_i^2-y_j^2)^2$. The actual application in equation (98) uses the appropriate even moments. [Forrester’s account, equation (1.7)](https://arxiv.org/pdf/1806.10411), supplies the general identity.

## Arithmetic and analytic estimates must use the same normalization

The factorial rescaling is

$$
F_K=S_K\Delta_K,\qquad
S_K=\frac{(K!)^{2h}4^{h-1}}{(N!)^{12h}\prod_{i=1}^{h-1}((2i)!)^2}>0.
$$

It preserves degree and positivity but does not by itself give integer coefficients. A further positive rational factor $m_{K,M}$ is chosen so that $Q_{K,M}=m_{K,M}F_K\in\mathbb Z[X]$.

Under Fauzan’s original arithmetic estimate at fixed $M=200$ and the analytic estimate, the reviewed overview uses the convenient eventual bounds

$$
\log m_{K,200}\le1.35K^2,\qquad
\log F_K(\xi)\le-1.36K^2.
$$

Their sum is $-K^2/100=-16n^2$, sufficient for Lemma 3.1. The source constants are $A_{200}=1.3495876977\ldots$ and $U=-1.3669955$, leaving $A_{200}+U=-0.0174078022\ldots$. Keeping those stronger estimates gives the advertised eventual exponent $-139n^2/5$. This numerical conclusion is conditional on the estimates, not a new proof of them.

### Local divisibility controls the cost

For $P\in\mathbb Q[X]$, let $v_p^G(P)$ be the minimum valuation of its nonzero coefficients. Integer lower bounds $v_p^G(F_K)\ge L_p$, together with integrality for the primes outside the product, allow

$$
m_{K,M}=\prod_{p\le2h}p^{-L_p},\qquad
\log m_{K,M}=-\sum_{p\le2h}L_p\log p.
$$

Positive $L_p$ permit removal of common factors; negative $L_p$ require denominator clearing. Consequently $m$ need not be an integer. The original leading cost splits into

| Prime range | Contribution |
| --- | --- |
| $p\le K/M$ | $6\lambda/M$ |
| $K/M<p\le K/3$ | $\int_3^M R(x)x^{-3}\,dx$ |
| $K/3<p\le2h$ | $I_{\rm out}=127751/96000$ |

Here $R=-\Gamma-\mathcal N$ combines the determinant and factorial valuation profiles. The substitution $p=K/x$ in the prime sum explains $x^{-3}$: one factor $K/x$ comes from the summand and $K/x^2$ from the differential.

The core determinant principle is

$$
v_p^G(B_{ij})\ge w_i+w_j\ \Longrightarrow\ v_p^G(\det B)\ge2\sum_iw_i.
$$

To obtain useful $w_i$, group poles by $j\equiv\pm a\pmod p$ and set

$$
\ell_A(a)=\#\{1\le j\le A:j\equiv\pm a\pmod p\},\qquad
b_a=3\ell_N(a),\qquad L_a=T_p-b_a+\varepsilon_a.
$$

A basis adapted to these residue classes has prescribed vanishing and a change-of-basis determinant that is a $p$-adic unit. Its typical row weights are $w_{a,i}=i+b_a-(\ell_K(a)+4)/2$. The count $L_0+\sum_aL_a=h$, with $L_0=4M+10$, and the associated arithmetic-progression sums explain the proposed integer exponent. The substantive local functional estimates are still needed to prove that exponent bounds the determinant; Proposition 8.4’s integrality of the exponent alone does not establish this.

Section 10 supplies the distinct outer-prime saving $\int_{1/3}^{1/2}d(y)\,dy=9/640$. For the stated parameters, $d$ equals $9/40$ on $[1/3,43/120]$, then $13/10-3y$ on $[43/120,13/30]$, then zero. Its area is $9/1600+27/3200=9/640$. This is an arithmetic saving, not the logarithmic-energy integral.

### One comparison measure bounds every configuration

After $y_i=K\sqrt{t_i}$, the determinant integral has leading exponent

$$
2\sum_{i<j}\log|t_i-t_j|-K\sum_iV(t_i),\qquad
V(t)=2\pi\sqrt t+\int_0^1\log(t+u^2)\,du-6\int_0^\alpha\log(t+u^2)\,du.
$$

Let $\rho$ have mass $\lambda$ and satisfy $2U^\rho(t)-V(t)\le M_0$ uniformly. For any competing positive measure $\sigma$ supported on $[0,\infty)$ with the same mass and the requisite finite energies,

$$
I(\sigma)-\int V\,d\sigma
=I(\sigma-\rho)+\int(2U^\rho-V)\,d\sigma-I(\rho)
\le\lambda M_0-I(\rho).
$$

The equal masses make $I(\sigma-\rho)\le0$. One proof writes the zero-mass energy as $-\tfrac12\int_0^\infty J(s)\,ds/s$, where $J(s)=\iint e^{-s|z-w|^2}\,d\nu(z)d\nu(w)\ge0$ by positive definiteness of the Gaussian kernel. Truncation and logarithmic-integrability hypotheses justify the limits.

For discrete point configurations, atomic self-energy is infinite, so the argument first replaces each atom by mass on a small circle. Separate circle-average estimates transfer the real-axis inequality to this regularization with controlled error; equal masses alone do not justify applying the real-axis field on complex circles. Radius $\varepsilon=K^{-2}$ yields an $O(K\log K)$ error. Integrating over the unbounded domain also requires retaining tail decay; the residual one-variable integral is

$$
\int_0^\infty t^{-1/2}(1+\sqrt t)^5e^{-\sqrt t}\,dt=652,
$$

whose $h$-fold contribution has logarithm only $O(K)$.

The chosen $\rho$ is a sum of sixteen arcsine measures on nested intervals. If its masses have cumulative sums $S_j$, then

$$
I(\rho)=\sum_{j=1}^{16}(S_j^2-S_{j-1}^2)\log\frac{b_j-a_j}{4}.
$$

The numerical inputs $M_0=-6.645$, $I(\rho)=-2.1265934451\ldots$, and $C_*=2.6530359903\ldots$ give $\lambda M_0-I(\rho)+C_*=-1.3669955645\ldots$. Opposite $\pm0.69375K^2\log K$ terms from the determinant and $S_K$ cancel. This produces the stated bound $\log F_K(\xi)\le-1.3669955K^2+24K\log K+200K$.

The uniform potential inequality must hold between sample points and in the infinite tail. Lai’s finite grid alone does not establish it. The chat’s fuller explanation invokes Fauzan’s Appendix A interval bounds on $[0,2]$ and analytic tail estimate. The comparison measure need not be an exact optimizer.

## Corrections and the exact arithmetic check

Two distinct issues should be retained.

1. **Printed correction sign.** Lai’s equations (78), (82), and (106) introduce a positive additional cost $E_M$, while later prose treats it as a favorable subtraction. If that corrected bound is retained, the displayed original margin cannot simply be reused. The overview states that an extra bound $E_{200}<0.017407802258\ldots$ would be needed to retain some negative exponent.
2. **The later table check.** The sections 8–11 chat recomputed the definitions in Lai’s Remark 8.6 using exact rational arithmetic. It reproduced all eight printed discrete $\gamma_p^{\rm in}$ entries but found different values of $p\Gamma(K/p)$. It also distinguished the finite quotient $T_p$ from $\lfloor2HK/p\rfloor$; these need not be equal.

The preserved [script](artifacts/LaiArithmetic/check_arithmetic.py) and [results](artifacts/LaiArithmetic/results.txt) make the latter finding reproducible:

| $M$ | $K$ | $p$ | Discrete $\gamma$ | Recomputed $p\Gamma$ | Difference | Lai’s printed $p\Gamma$ |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 5 | 5000 | 1009 | -6712 | -6734 | 22 | 2779 |
| 5 | 8000 | 2003 | -16845 | -16863 | 18 | 1183 |
| 10 | 20000 | 2003 | 43873 | 43838 | 35 | 70527 |
| 10 | 40000 | 4001 | 87981 | 87946 | 35 | 141426 |
| 20 | 80000 | 4001 | 739790 | 739712 | 78 | 817708 |
| 20 | 160000 | 8009 | 1477486 | 1477408 | 78 | 1633369 |
| 40 | 320000 | 8009 | 7390051 | 7389902 | 149 | 7661701 |
| 40 | 640000 | 16001 | 14799027 | 14798878 | 149 | 15342855 |

The script also checks the proposed identity $R=xF+Q$ at 5,738 rational inputs, including floor-function breakpoints. Rerunning it during consolidation reproduced the stored results. These are exact finite checks of transcribed formulas. They rebut the printed table and support the chat’s return to the original fixed-$M$ asymptotic, but are not by themselves a proof of the general asymptotic, all local valuation bounds, or the full irrationality theorem. The reviewed overview therefore retains its explicit assumed-estimate formulation.

## The exponent 260 is a separate conclusion

Taken as an assumption, a bound

$$
|\xi-a/b|>b^{-260}\quad\text{for every }a\in\mathbb Z\text{ and all sufficiently large }b>0
$$

implies irrationality: if $\xi=p/q$, the representations $kp/(kq)$ eventually have denominator above the threshold and give zero error. The quantifier must include these unreduced representations. A bound only for nonzero errors would not suffice, since rational numbers already satisfy lower bounds $|p/q-a/b|\ge1/(qb)$ for different fractions.

Dirichlet’s theorem gives infinitely many approximations with error below $b^{-2}$ for an irrational number. Together with the assumed bound, this yields $2\le\mu(\xi)\le260$ for the irrationality exponent. A smaller exponent in the lower bound would be stronger. Liouville’s theorem bounds the exponent of an algebraic irrational of degree $d$ by $d$; Roth sharpens it to $2$. A finite exponent rules out a Liouville number, whose exponent is infinite, but does not prove transcendence: Roth’s value is compatible with the interval. Dirichlet’s finite approximation theorem applies to every real number and can be satisfied by an exact rational representation, so it alone does not decide irrationality of a specified constant.

The determinant’s small value at $\xi$ establishes qualitative irrationality, but does not alone prove the bound with exponent 260. That conclusion additionally needs control of the determinant near $\xi$, through the perturbation argument in Fauzan’s Appendix C, especially C.1–C.2. See the existing [reading cautions and perturbation explanation](../ProofGuide/08_READING_CAUTIONS.md).

## Pending exposition expansion

A new follow-up in **Draft parallel constructions for sections…** requests a fuller version of the overview, retaining its narrative but making the argument essentially complete except for the estimates borrowed from Sections 8–11. Its particular priority is to derive the integral representation of $\mu_\xi$, apply it entry by entry to $G_K(\xi)$, and then derive the quadratic-form integral and positivity. The active response plans to spell out the pole formula and put classical identities and optional exact-degree/pullback calculations in appendices. This request was still in progress at the archive snapshot; the report preserved here is the last completed, reviewed version.
