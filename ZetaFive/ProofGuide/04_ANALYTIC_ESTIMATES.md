# 4. The analytic branch: why the determinant is small

[Overview](../PROOF_OVERVIEW.md) · [Previous: arithmetic](03_ARITHMETIC_ESTIMATES.md) · [Next: positivity](05_POSITIVITY.md)

**Proposition 11.7 supplies the decay that must pay for the arithmetic multiplier.** Its conclusion is

$$
0<F_K(\xi),\qquad
\log F_K(\xi)\le UK^2+24K\log K+200K,
\qquad U=-\frac{2733991}{2000000}.
$$

Recall $F_K=S_K\det G_K$, $\xi=\zeta(5)$, $\alpha=N/K=3/40$, and $\lambda=h/K=37/40$. These are defined in [companion 2](02_NORMALIZATION_AND_DECAY.md); $W=D_N^6/D_K$ is defined in [companion 3](03_ARITHMETIC_ESTIMATES.md).

Read the argument backward as follows: **the determinant estimate needs a bound for every integration configuration; that bound comes from one comparison measure; the comparison works because the energy of a signed measure of mass zero is nonpositive.**

## What is needed to bound the integral

The positive weight underlying the matrix is

$$
w(y)=\frac{(2\pi)^4}{12}y^5
\sum_{\ell=1}^{\infty}\ell^4e^{-2\pi\ell y},\qquad y>0.
$$

Its origin is explained in [companion 7](07_MOMENT_REPRESENTATION.md). For now, its exponential tail and the positive moment representation are the relevant facts.

The determinant becomes an integral over $h$ positive variables $y_1,\ldots,y_h$. After the substitution $t_i=(y_i/K)^2$, its main exponential factor is $e^{E_K}$, where

$$
E_K(t_1,\ldots,t_h)
=2\sum_{i<j}\log|t_i-t_j|-K\sum_{i=1}^h V(t_i).
$$

The **external field** is the function

$$
V(t)=2\pi\sqrt t+
\int_0^1\log(t+u^2)\,du
-6\int_0^\alpha\log(t+u^2)\,du,
\qquad t\ge0.
$$

Its name simply distinguishes the one-variable penalty from the pairwise logarithms. The three terms come respectively from the exponential tail of $w$, the denominator $D_K$, and the numerator $D_N^6$. Lemma 11.2 evaluates the integrals explicitly, so $V$ can be bounded using elementary functions.

The needed finite-configuration estimate, displayed as equation (99) in Lai, is

$$
E_K(t_1,\ldots,t_h)+\sum_{i=1}^h\sqrt{t_i}
\le\bigl(\lambda M_0-I(\rho)\bigr)K^2
 +(120+\sqrt2)h+2h\log K.
$$

Here $\rho$ is the comparison measure, $I(\rho)$ its energy, and $M_0=-1329/200$; their definitions and the reason for this bound appear below.

The extra term $\sum_i\sqrt{t_i}$ matters. Moving it to the right leaves the factor $\exp(-\sum_i\sqrt{t_i})$ in the integrand. An upper bound by a constant alone would not control an integral over an unbounded domain. This remaining tail, together with the estimates for the weight and Jacobian, makes integration possible. For instance, the Jacobian is $dy_i=K\,dt_i/(2\sqrt{t_i})$, and

$$
\int_0^\infty t^{-1/2}e^{-\sqrt t}\,dt=2.
$$

The powers of $K$ from scaling the determinant cancel the terms of order $K^2\log K$ in $\log S_K$. The remaining contribution of order $K^2$ from those factors is

$$
C_*=-2\lambda+12\alpha\lambda(1-\log\alpha)
 +3\lambda^2-2\lambda^2\log(2\lambda).
$$

Thus the crucial numerical comparison is

$$
C_*+\lambda M_0-I(\rho)\le U.
$$

Bounds for factorials and the remaining integral supply the lower-order terms $24K\log K+200K$. This is the final step in Proposition 11.7.

## Where the configuration estimate comes from

For a positive measure $\sigma$ on the real line, define its logarithmic energy by

$$
I(\sigma)=\iint\log|s-t|\,d\sigma(s)\,d\sigma(t).
$$

The corresponding potential at a point is

$$
U^\sigma(t)=\int\log|t-s|\,d\sigma(s).
$$

We use the same energy notation for signed measures when the integrals are finite. This is the $+\log|s-t|$ convention; sources using $-\log|s-t|$ reverse the energy inequalities. Also, $U^\rho$ is a function, whereas the symbol $U$ without a superscript is the numerical decay constant above.

For integration points $t_i$, the natural measure is

$$
\sigma_K=\frac1K\sum_{i=1}^h\delta_{t_i},
$$

where $\delta_t$ is a unit point mass at $t$. Its total mass is $h/K=\lambda$, not one. The field term satisfies $K^2\int V\,d\sigma_K=K\sum_iV(t_i)$.

The pairwise logarithms would also resemble $K^2I(\sigma_K)$, except that this energy includes diagonal terms $\log|t_i-t_i|=-\infty$. One therefore cannot substitute the atomic measure directly into a finite-energy argument.

The passage to a finite configuration requires smoothing the point masses, estimating the changes in potential and interaction, and then recovering the sum with the diagonal omitted. Those estimates, with additional control at infinity, give equation (99). The explicit error in that equation is an input to this guide, not a consequence of merely writing down $\sigma_K$.

## Why one comparison measure controls every competitor

The two properties needed from $\rho$ are

$$
\rho([0,\infty))=\lambda,
\qquad 2U^\rho(t)-V(t)\le M_0\quad\text{for every }t\ge0.
$$

Take any compactly supported positive measure $\sigma$ on $[0,\infty)$ with the same mass and with the required finite energy integrals. The signed measure $\eta=\sigma-\rho$ has mass zero. **Lemma 11.5 gives $I(\eta)\le0$.** Expanding the energy gives the useful identity

$$
I(\sigma)-\int V\,d\sigma
=I(\eta)+\int(2U^\rho-V)\,d\sigma-I(\rho).
$$

The first term is nonpositive. The middle term is at most $\lambda M_0$, since $\sigma$ is positive and has mass $\lambda$. Therefore

$$
I(\sigma)-\int V\,d\sigma
\le\lambda M_0-I(\rho).
$$

This deduction explains the two requirements on the comparison measure. Equal mass is what permits Lemma 11.5; the pointwise potential bound is what permits integration against every positive competitor. There is no need to identify the exact maximizing measure.

## How the comparison measure is made computable

Lemmas 11.3–11.4 use a sum of sixteen arcsine measures,

$$
\rho=\sum_{j=1}^{16}c_j\omega_{[a_j,b_j]},
\qquad c_j>0,\qquad \sum_{j=1}^{16}c_j=\lambda.
$$

For $a<b$, $\omega_{[a,b]}$ is the probability measure on $(a,b)$ with density

$$
\frac{d\omega_{[a,b]}}{dt}
=\frac1{\pi\sqrt{(t-a)(b-t)}}.
$$

The rational endpoints and weights are chosen in Fauzan's Table 1, which Lai references. The intervals lie in $[0,2]$ and are nested, with

$$
a_{16}<\cdots<a_1<b_1<\cdots<b_{16}.
$$

Thus the interval with the larger index contains the one with the smaller index. The potential of an arcsine measure is constant on its own interval:

$$
U^{\omega_{[a,b]}}(t)=\log\frac{b-a}{4}
\quad(a\le t\le b).
$$

Outside the interval it equals

$$
\log\left(\frac{|t-(a+b)/2|+\sqrt{(t-a)(t-b)}}2\right).
$$

Consequently both the potential and energy of $\rho$ are explicit. Set $C_j=\sum_{i=1}^j c_i$ and $C_0=0$; these are partial sums, distinct from the constant $C_*$. Nestedness gives

$$
I(\rho)=\sum_{j=1}^{16}(C_j^2-C_{j-1}^2)
\log\frac{b_j-a_j}{4}.
$$

To see the coefficient, the self-interaction of component $j$ contributes $c_j^2$, and its interactions with all earlier, inner components contribute $2c_jC_{j-1}$. Their sum is $C_j^2-C_{j-1}^2$.

These formulas reduce the choice of a measure to checking explicit inequalities. **The potential inequality must still hold for every $t\ge0$.** The numerical grid reported in Lai does not establish that by itself. See [companion 8](08_READING_CAUTIONS.md) for the distinction and for a source providing rigorous bounds.

## What connects this analysis to the original matrix

Everything above applies because the matrix is a moment matrix. Define the positive measure

$$
d\nu_K(y)=W(y^2)w(y)\,dy\quad(y>0).
$$

Its moments give $G_K(\xi)_{ij}=\int y^{2i+2j}\,d\nu_K(y)$. Andréief's identity, Lemma 11.6, then gives

$$
\Delta_K(\xi)=\frac1{h!}
\int_{(0,\infty)^h}
\prod_{i<j}(y_i^2-y_j^2)^2
\prod_{i=1}^h d\nu_K(y_i).
$$

The product of differences is a Vandermonde determinant squared. It appears by expanding two determinants of the monomials and integrating; the $h!$ accounts for permutations of the integration variables. [Forrester's account](https://arxiv.org/html/1806.10411v1) explains this identity.

This is the source of the pairwise logarithms in $E_K$. The remaining positive weights produce the external field after scaling and estimating the finite products by integrals. The moment representation itself is proved in [companion 7](07_MOMENT_REPRESENTATION.md); [companion 5](05_POSITIVITY.md) first explains its simpler consequence, strict positivity.
