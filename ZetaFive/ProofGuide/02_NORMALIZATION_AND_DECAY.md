# 2. Smallness after making the coefficients integers

[Overview](../PROOF_OVERVIEW.md) · [Previous: the criterion](01_IRRATIONALITY_CRITERION.md) · [Next: arithmetic](03_ARITHMETIC_ESTIMATES.md)

**The final comparison needs the cost of integrality to be smaller than the analytic decay.** Section 12 combines these estimates. This is the point at which the two long branches of the proof meet.

We retain $\xi=\zeta(5)$, the polynomial variable $X$, and the positive integer $n$ from [companion 1](01_IRRATIONALITY_CRITERION.md).

## The quantities being compared

The construction uses the following parameters throughout:

| Symbol | Definition | Role |
| --- | --- | --- |
| $K$ | $40n$ | Overall size parameter. Limits involving $K$ run through these multiples of 40. |
| $N$ | $3n$ | Controls the numerator of the rational functions used in the matrix. |
| $h$ | $K-N=37n$ | Number of rows and columns of the matrix. |
| $\alpha$ | $N/K=3/40$ | Fixed proportion used in the analytic estimates. |
| $\lambda$ | $h/K=37/40$ | Fixed proportion controlling both degree and measure mass. |
| $M$ | A fixed integer cutoff, at least 40 | Divides the primes into ranges for the arithmetic estimates. It is chosen before $n$ tends to infinity. |

Let $G_K(X)$ be the $h\times h$ matrix of affine polynomials with rational coefficients constructed in [companion 6](06_HANKEL_CONSTRUCTION.md). An affine polynomial has the form $aX+b$. Define

$$
\Delta_K(X)=\det G_K(X),\qquad
F_K(X)=S_K\Delta_K(X),\qquad
Q_{K,M}(X)=m_{K,M}F_K(X).
$$

There are two scalar factors:

$$
S_K=
\frac{(K!)^{2h}\,4^{h-1}}
{(N!)^{12h}\displaystyle\prod_{i=1}^{h-1}((2i)!)^2},
\qquad m_{K,M}>0.
$$

Both are rational and independent of $X$. The factorial factor $S_K$ removes predictable arithmetic factors and compensates for the scale of the determinant. The remaining factor $m_{K,M}$ is selected from prime valuation bounds to make $Q_{K,M}$ integral. It may divide out common factors as well as clear denominators, so it need not be an integer.

The polynomial used in Lemma 3.1 is $Q_n=Q_{40n,M}$, with one fixed choice of $M$.

## What the final estimate needs

Suppose the two branches establish

$$
\limsup_{K\to\infty}\frac{\log m_{K,M}}{K^2}\le A,
\qquad
\log F_K(\xi)\le UK^2+24K\log K+200K.
$$

Here $A$ is an upper bound for the arithmetic cost and $U$ is the analytic bound. The first inequality means that, for each $\varepsilon>0$, eventually $\log m_{K,M}\le(A+\varepsilon)K^2$. Strict positivity, proved in [companion 5](05_POSITIVITY.md), makes the second logarithm legitimate.

Adding the estimates yields

$$
\limsup_{K\to\infty}
\frac{\log Q_{K,M}(\xi)}{K^2}\le A+U,
$$

because $(K\log K)/K^2$ and $K/K^2$ tend to zero. **We need a proved bound with $A+U<0$.**

For clarity, set $\delta=-(A+U)>0$. Absorbing all smaller terms into half this margin gives, eventually,

$$
0<Q_{40n,M}(\xi)
\le\exp\!\left(-\frac\delta2(40n)^2\right)
=\exp(-800\delta n^2).
$$

This supplies the constant required in Lemma 3.1. A slightly smaller positive constant makes its strict upper inequality immediate. No particular numerical value of that constant is necessary for irrationality.

## Which results supply the two bounds

| Input | Source | Work hidden in that input |
| --- | --- | --- |
| Integer coefficients and a bound for $\log m_{K,M}$. | Proposition 9.2 and Theorem 9.3. | Divisibility estimates for every prime, followed by a weighted sum over primes. See [companion 3](03_ARITHMETIC_ESTIMATES.md). |
| A negative bound for $\log F_K(\xi)$. | Proposition 11.7. | A multiple integral, a logarithmic energy estimate, and factorial estimates. See [companion 4](04_ANALYTIC_ESTIMATES.md). |
| Positivity and degree at most $h$. | Proposition 5.6 and Corollary 5.5. | The moment representation and affine dependence of each entry on $X$. |

Multiplying by a nonzero scalar does not change degree. Multiplying by positive scalars preserves positivity. Thus normalization leaves those two requirements intact; its effect on size is the issue.

## How to read the displayed numerical margin

Lai's Section 12 displays

$$
A_{200}\approx1.3495876977,
\qquad U=-\frac{2733991}{2000000}=-1.3669955.
$$

Their sum is approximately $-0.0174078023$. Multiplying by $40^2$ gives approximately $-27.85248$, explaining the proposed decay rate $139/5=27.8$ in terms of $n^2$.

Those arithmetic operations are correct. The difficulty is justifying the use of $A_{200}$ as the full cost: the exposition introduces an additional positive correction and then handles its sign inconsistently. The displayed difference alone therefore does not complete the printed argument. See [companion 8](08_READING_CAUTIONS.md).

A separate arithmetic implementation in [mo271's formalization](https://github.com/mo271/zeta5) reports a bound $A_{\mathrm{eff}}=1.36$ with the same $U$. Their sum is $-0.0069955$, which is still negative. That construction uses different local estimates and $M=400$; its normalizing factor must be used with its own bound. One cannot simply substitute its constant into an unverified normalization from the exposition.

**Working backward:** a negative difference is enough, but both terms must have been proved for the same construction. The next two companions explain those obligations separately.
