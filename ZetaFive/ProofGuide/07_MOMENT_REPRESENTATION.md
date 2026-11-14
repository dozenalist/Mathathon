# 7. The starting bridge: a rational rule and a positive integral

[Overview](../PROOF_OVERVIEW.md) · [Previous: the matrix](06_HANKEL_CONSTRUCTION.md) · [Next: reading cautions](08_READING_CAUTIONS.md)

**Corollary 4.7 identifies the algebraic entries with positive moments when $X=\xi=\zeta(5)$.** This is the common source of the positivity argument and the analytic determinant estimate. Working backward, it follows by checking two elementary types of rational function.

We retain $B_r$, the Bernoulli numbers with $B_1=-1/2$, and $H_j^{(5)}=\sum_{v=1}^jv^{-5}$ from [companion 3](03_ARITHMETIC_ESTIMATES.md). The variable $t$ belongs to the rational functions, $X$ is the formal polynomial variable, and $y>0$ is the integration variable.

## The identity that the later arguments need

Let $\mathcal R$ consist of rational functions of the form

$$
R(t)=P(t)+\sum_{j\in J}\frac{c_j}{t+j^2},
$$

where $P\in\mathbb Q[t]$, $J$ is a finite set of positive integers, and $c_j\in\mathbb Q$. In words, these are polynomial parts plus simple poles at negative integer squares. The partial fraction expansions in [companion 6](06_HANKEL_CONSTRUCTION.md) belong to this space.

Corollary 4.7 asserts that, for $R\in\mathcal R$,

$$
\mu_\xi(R)=\int_0^\infty R(y^2)w(y)\,dy,
\qquad
w(y)=\frac{(2\pi)^4}{12}y^5
\sum_{\ell=1}^{\infty}\ell^4e^{-2\pi\ell y}.
$$

Each term of the series is positive. Moreover, $w(y)\to1/\pi$ as $y\downarrow0$, and $w(y)=O(y^5e^{-2\pi y})$ as $y\to\infty$. Here $O$ means bounded in absolute value by a constant multiple in the indicated limit. These facts ensure integrability for every $R\in\mathcal R$: there are no poles on $y\ge0$, and polynomial growth is dominated by the tail.

This does not say that the integral is positive for every $R$. It says the **weight** is positive; the positivity application uses $R=Wq^2$.

## To obtain the identity, it is enough to check two kinds of input

Define $\mu_X$ first, without an integral, by rational linearity and the following values:

$$
\mu_X(t^e)
=\frac{(-1)^eB_{2e+2}(2e+3)(2e+4)(2e+5)}{24},
\qquad e=0,1,2,\ldots,
$$

and

$$
\mu_X\!\left(\frac1{t+j^2}\right)
=j^4\bigl(X-H_j^{(5)}\bigr)-\frac14+\frac1{2j},
\qquad j=1,2,\ldots.
$$

Partial fractions are unique, so these prescriptions define one rule on $\mathcal R$. The output is always an affine polynomial with rational coefficients. The rule is linear, but is not asserted to preserve products.

The required integral identity now reduces to:

| Input | Integral calculation | Result |
| --- | --- | --- |
| $t^e$ | Integrate the exponential series and use Euler's formula for even zeta values. | Lemma 4.5. |
| $1/(t+j^2)$ | Use Hermite's formula for the Hurwitz zeta function at 5. | Lemma 4.6. |

Once these are established, linearity gives Corollary 4.7. No further calculation is needed for an individual matrix entry.

## Why polynomial moments are rational

For real $s>1$, write $\zeta(s)=\sum_{v=1}^\infty v^{-s}$. All summands in the following integral are nonnegative, so termwise integration is justified by Tonelli's theorem:

$$
\begin{aligned}
\int_0^\infty y^{2e}w(y)\,dy
&=\frac{(2\pi)^4}{12}
\sum_{\ell=1}^\infty\ell^4
\int_0^\infty y^{2e+5}e^{-2\pi\ell y}\,dy\\
&=\frac{(2e+5)!}{12(2\pi)^{2e+2}}\,\zeta(2e+2).
\end{aligned}
$$

The second line uses $\int_0^\infty y^m e^{-ay}\,dy=m!/a^{m+1}$ for an integer $m\ge0$ and $a>0$.

Euler's formula is

$$
\zeta(2r)=\frac{(-1)^{r+1}B_{2r}(2\pi)^{2r}}{2(2r)!},
\qquad r\ge1.
$$

Substituting $r=e+1$ cancels the powers of $\pi$ and leaves exactly the prescribed value of $\mu_X(t^e)$. For example,

$$
\int_0^\infty w(y)\,dy=\frac5{12},
\qquad
\int_0^\infty y^2w(y)\,dy=\frac7{24}.
$$

Thus the polynomial part of a rational function contributes only a rational constant to $\mu_X(R)$.

## Why a simple pole introduces exactly $\zeta(5)$

For $a>0$, define the Hurwitz zeta value by

$$
\zeta(5,a)=\sum_{v=0}^\infty(a+v)^{-5}.
$$

The useful intermediate identity is

$$
\int_0^\infty\frac{w(y)}{y^2+a^2}\,dy
=a^4\zeta(5,a)-\frac1{2a}-\frac14.
$$

At a positive integer $a=j$, the series splits as

$$
\zeta(5,j)=\xi-H_j^{(5)}+j^{-5}.
$$

Substitution gives

$$
\int_0^\infty\frac{w(y)}{y^2+j^2}\,dy
=j^4(\xi-H_j^{(5)})-\frac14+\frac1{2j},
$$

which is exactly the value of the algebraic rule at $X=\xi$. This is the only place where the unknown odd zeta value enters the basic moments.

## What produces the intermediate identity

Set

$$
f(y)=\frac1{e^{2\pi y}-1},\qquad
g_a(y)=\frac{y^5}{12(y^2+a^2)}.
$$

Differentiating the exponential series four times shows $w(y)=y^5f^{(4)}(y)/12$, where the superscript denotes the fourth derivative. Four integrations by parts therefore give

$$
\int_0^\infty\frac{w(y)}{y^2+a^2}\,dy
=\int_0^\infty g_a(y)f^{(4)}(y)\,dy
=\int_0^\infty g_a^{(4)}(y)f(y)\,dy.
$$

The boundary terms vanish. Near zero, each product $g_a^{(r)}f^{(3-r)}$ is $O(y)$ for $0\le r\le3$. At infinity, the derivatives of $f$ decay exponentially while those of $g_a$ grow at most polynomially. Direct differentiation gives

$$
g_a^{(4)}(y)=
\frac{2a^4y(y^4-10a^2y^2+5a^4)}{(a^2+y^2)^5}.
$$

[Hermite's integral formula](https://dlmf.nist.gov/25.11.E29), specialized to 5, says

$$
\zeta(5,a)=\frac1{2a^5}+\frac1{4a^4}
+2\int_0^\infty
\frac{y(5a^4-10a^2y^2+y^4)}{(a^2+y^2)^5}
\frac{dy}{e^{2\pi y}-1}.
$$

Multiplying this formula by $a^4$ and comparing the integrands proves the intermediate identity. This explains the otherwise rather specific fourth derivative and fifth power in the weight.

The construction is not circular. The rational rule $\mu_X$ is defined for a formal $X$ using rational numbers. Separately, the moment calculations identify its value at the real number $\xi$ with an integral. Irrationality is only deduced much later, after determinants, normalization, and decay have been established.
