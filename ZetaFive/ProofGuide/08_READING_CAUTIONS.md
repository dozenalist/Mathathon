# 8. Reading cautions and the extra approximation claim

[Overview](../PROOF_OVERVIEW.md) · [Previous: moments](07_MOMENT_REPRESENTATION.md)

**The structural argument reduces irrationality to precise estimates; the estimates still need valid proofs.** This file works backward from the places where those estimates are used. It distinguishes a problem in Lai's printed exposition from a failure of the overall method.

The discussion concerns [Lai's version 1, dated 29 September 2026](https://ai.vixra.org/pdf/2609.0080v1.pdf). Notation from companions 1–7 is retained: in particular $\xi=\zeta(5)$, $Q_{K,M}=m_{K,M}F_K$, and $F_K=S_K\det G_K$.

## To finish the irrationality proof, the full arithmetic cost must leave a negative margin

[Companion 2](02_NORMALIZATION_AND_DECAY.md) needs a justified upper bound $A$ for $\log m_{K,M}/K^2$ with $A+U<0$. A displayed negative difference between two constants is not sufficient if an additional cost has been omitted.

Recall from [companion 3](03_ARITHMETIC_ESTIMATES.md) that

$$
m_{K,M}=\prod_{p\le2h}p^{-L_p},\qquad
\log m_{K,M}=-\sum_{p\le2h}L_p\log p.
$$

If a correction replaces $L_p$ by $L_p-c_p$ with $c_p>0$, it increases the logarithmic cost by $c_p\log p$.

Lai's Remark 8.6 describes a downward correction to an inner-range valuation estimate. Theorem 9.3 introduces the associated term

$$
E_M=\int_3^M\frac{c(x)}{x^3}\,dx,
$$

where $c(x)$ is the positive correction function discussed there. Equations (106)–(107) include $+E_M$ in the cost. The following paragraph instead treats it as improving the negative margin. These signs are incompatible.

The required repair is a proved bound for the **corrected** cost, or a replacement family of local bounds whose full cost is sufficiently small. Merely changing the sign in the final paragraph cannot supply that estimate. Nor does this discrepancy, by itself, prove that no suitable normalization exists.

The [exponent catalog](../EXPONENT_CATALOG.md) follows a different, explicitly identified source convention: Fauzan's original Section 5.1 uses $\ell(x,z)=\lfloor x-z\rfloor+\lfloor x+z\rfloor+1$, whereas Lai's equation (71) prints absolute values. The catalog reconstructs the original floor-function integrals and Proposition 5.2 without Lai's $E_M$ term. Its $k=7$ column is a derived extension calculation with separate local proof obligations, rather than a consequence of Lai's Theorem 9.3 as printed.

## To bound the integral, the potential inequality must hold between sample points and in the tail

[Companion 4](04_ANALYTIC_ESTIMATES.md) uses

$$
u(t):=2U^\rho(t)-V(t)\le M_0
\quad\text{for every }t\ge0.
$$

The new symbol $u$ abbreviates this potential difference. Lai reports evaluations at 4,100 points in $[0,10]$. Such evaluations can locate likely maxima, but cannot exclude a larger value between samples or beyond the sampled interval.

For example, on a smooth interval where $|u'|\le L$, a grid with spacing at most $d$ gives

$$
u(t)\le\max_{\text{grid points }s}u(s)+Ld/2,
$$

provided the endpoints are included. Here $L$ is a derivative bound and $d$ is the mesh spacing. This would turn samples into a proof if the error were smaller than the available margin. With arcsine potentials, derivatives may be unbounded near interval endpoints, so those neighborhoods require separate estimates. The infinite tail also requires a bound, using the explicit formulas and the dominant negative square-root term.

The energy constant is another obligation: the logarithms occurring in $I(\rho)$ and $C_*$ must be bounded accurately enough to prove $C_*+\lambda M_0-I(\rho)\le U$. High-precision decimal output is useful evidence, but rigorous error bounds are what establish the inequality.

## To make every coefficient integral, do not discard primes merely because they exceed $K$

The factorial normalization contains $(2i)!$ for $1\le i<h$. Its largest argument is $2h-2$, which exceeds $K$ in this family. Primes above $K$ can therefore occur in its denominator.

For a concrete example, take $n=1$, so $K=40$, $N=3$, and $h=37$. At the prime $41$, neither $40!$ nor $3!$ contributes a factor. But $(2i)!$ contains one factor of $41$ for each $i=21,\ldots,36$. Consequently

$$
v_{41}(S_K)=-2\cdot16=-32.
$$

The determinant may supply compensating factors; that is an arithmetic assertion requiring proof. This example explains why the normalization runs through primes up to $2h$, and why primes above that range still need a separate integrality argument for the determinant's coefficients.

## A documented route that uses different arithmetic estimates

[mo271's formalization](https://github.com/mo271/zeta5) reports a complete proof using Lean's standard axioms. Its README specifies changes to the arithmetic argument: it uses direct partial fractions for residue classes, allows the full rank loss in the outer-range estimate, and takes $M=400$. Its resulting bound $A_{\mathrm{eff}}=1.36$ satisfies

$$
A_{\mathrm{eff}}+U=-0.0069955<0.
$$

The repository also describes rigorous potential and energy bounds. This gives a documented route for the dependencies identified above, while changing the local estimates and normalizing factor. It should not be described as verification of every printed step of Lai's version. This guide has not independently rebuilt that formalization.

## To obtain the exponent 260, one needs a further perturbation estimate

Theorem 2.2 also claims that, for all sufficiently large positive integers $b$ and all integers $a$,

$$
|\xi-a/b|>b^{-260}.
$$

Lemma 3.1 does not supply this rate. Its contradiction evaluates the polynomial at $\xi$ under the assumption $\xi=a/b$. For an approximation result, we must instead control the value at a nearby rational number.

Here is the additional argument and the estimate it requires. Fix the cutoff and abbreviate $Q_K=Q_{K,M}$. Put

$$
G_*=G_K(\xi),\qquad
B_K=G_*^{-1/2}G_1G_*^{-1/2},
$$

where $G_1$ is the coefficient matrix of $X$ from [companion 6](06_HANKEL_CONSTRUCTION.md). Positive definiteness ensures that the positive square root of $G_*$, and its inverse, exist. The matrix $B_K$ is real symmetric. Let $\|B_K\|$ be its operator norm, equivalently the largest absolute value of its eigenvalues, and let $I_h$ be the $h\times h$ identity matrix.

For a real number $x$, factorization gives

$$
\frac{Q_K(x)}{Q_K(\xi)}
=\det\bigl(I_h+(x-\xi)B_K\bigr).
$$

If $|x-\xi|\,\|B_K\|\le1/(2h)$, every eigenvalue of the matrix on the right lies between $1-1/(2h)$ and $1+1/(2h)$. Its determinant is positive and at most $e^{1/2}<2$. Therefore

$$
0<Q_K(x)<2Q_K(\xi).
$$

So a quantitative approximation argument needs **both** of the following bounds, for positive constants $\varepsilon$ and $\gamma$:

$$
\log Q_K(\xi)\le-\varepsilon K^2+o(K^2),
\qquad
\|B_K\|\le\exp\bigl(\gamma K+o(K)\bigr).
$$

The notation $o(K^r)$ means an error whose ratio to $K^r$ tends to zero. The first bound concerns decay at the center. The second controls how quickly the determinant can change nearby; it is additional work.

To see how they combine, choose $K$ to be an allowed multiple of 40 with $K=s\log b+O(1)$, where $s>\lambda/\varepsilon$ is fixed. Then the decay beats denominator clearing:

$$
\log\bigl(2b^hQ_K(\xi)\bigr)
\le(\lambda s-\varepsilon s^2)(\log b)^2
+o((\log b)^2)<0
$$

for large $b$. If $|a/b-\xi|\le b^{-\beta}$ with $\beta>\gamma s$, the norm bound also puts $a/b$ inside the required perturbation radius. Thus $b^hQ_K(a/b)$ would be a positive integer smaller than one.

A choice of $s$ satisfying both conditions is possible whenever

$$
\beta>\frac{\gamma\lambda}{\varepsilon}.
$$

This explains what must be proved to obtain the stated exponent 260: valid decay and perturbation constants with $\gamma\lambda/\varepsilon<260$. A negative arithmetic–analytic margin alone does not give it. Lai points to Fauzan's Section 8 for this extra branch; [Giraudin's later treatment](https://arxiv.org/html/2611.01708v1) studies this perturbation step conditional on the underlying estimates.

For expository sources and attempted extensions to higher zeta values, see the separate [literature document](../Literature/EXPOSITION_AND_EXTENSIONS.md).
