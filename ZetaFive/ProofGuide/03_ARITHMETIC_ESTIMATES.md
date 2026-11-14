# 3. The arithmetic branch: integrality at an affordable cost

[Overview](../PROOF_OVERVIEW.md) · [Previous: normalization](02_NORMALIZATION_AND_DECAY.md) · [Next: analysis](04_ANALYTIC_ESTIMATES.md)

**Proposition 9.2 makes $Q_{K,M}$ an integer polynomial; Theorem 9.3 bounds the size of its multiplier.** Working backward, both conclusions require lower bounds on the prime divisibility of every coefficient of $F_K=S_K\Delta_K$.

The parameters $K,N,h,M$ and the factors $S_K,F_K,m_{K,M}$ are defined in [companion 2](02_NORMALIZATION_AND_DECAY.md).

## From prime bounds to integer coefficients

For a prime $p$ and a nonzero rational number $r$, let $v_p(r)$ be the exponent of $p$ in its numerator minus the exponent in its denominator. Set $v_p(0)=+\infty$. For a rational polynomial $P(X)=\sum_j a_jX^j$, define its **Gauss valuation** by

$$
v_p^{\mathrm G}(P)=\min_j v_p(a_j).
$$

The superscript $\mathrm G$ means Gauss; it does not refer to the matrix $G_K$. The condition $v_p^{\mathrm G}(P)\ge L$ says that **every** coefficient has valuation at least $L$.

Suppose integer bounds $L_p$ satisfy

$$
v_p^{\mathrm G}(F_K)\ge L_p\quad(p\le2h),
\qquad
v_p^{\mathrm G}(F_K)\ge0\quad(p>2h).
$$

Then choose

$$
m_{K,M}=\prod_{p\le2h}p^{-L_p}.
$$

For each prime in the product, multiplication adds $-L_p$ to the valuation of every coefficient. All resulting valuations are nonnegative, including those for $p>2h$. A rational number with no prime in its denominator is an integer. Applying this observation to each coefficient proves $Q_{K,M}\in\mathbb Z[X]$.

For a small example, take $F(X)=(6/5)X+12/5$. Its Gauss valuations at $2,3,5$ are $1,1,-1$. The factor $2^{-1}3^{-1}5=5/6$ changes it to $X+2$. Positive valuation bounds are useful: they allow division by common factors and can lower the cost.

The quantity to estimate is therefore

$$
\log m_{K,M}=-\sum_{p\le2h}L_p\log p.
$$

This identity also fixes the sign: decreasing a bound $L_p$ increases the cost.

## What gives a useful determinant valuation

We need a little of the construction before studying its arithmetic. For a nonnegative integer $r$, put

$$
D_r(t)=\prod_{j=1}^{r}(t+j^2),\qquad D_0(t)=1,
\qquad W(t)=\frac{D_N(t)^6}{D_K(t)}.
$$

Here $t$ is a rational-function variable, independent of $X$. Let $\mu_X$ denote the rational-linear rule that sends such rational functions, with simple poles at negative integer squares, to affine polynomials in $X$. Its exact values are given in [companion 7](07_MOMENT_REPRESENTATION.md). Define a bilinear form on polynomials of degree less than $h$ by

$$
\beta_X(f,g)=\mu_X(Wfg).
$$

The matrix $G_K$ represents this form in the basis $1,t,\ldots,t^{h-1}$.

Fix a prime $p$. Write $\mathbb Z_{(p)}$ for rationals whose denominators are not divisible by $p$. A change of basis with matrix $C$ is harmless for valuation purposes when both $C$ and $C^{-1}$ have entries in $\mathbb Z_{(p)}$. Equivalently, $C$ has entries there and $v_p(\det C)=0$; its determinant is a **$p$-adic unit**.

The matrix in the new basis is $H=C^{\mathsf T}G_KC$, where $\mathsf T$ denotes transpose. Since $\det H=(\det C)^2\det G_K$, the determinant valuation is unchanged.

Now suppose the new basis has weights $w_0,\ldots,w_{h-1}$ such that

$$
v_p^{\mathrm G}(H_{ij})\ge w_i+w_j.
$$

In every product appearing in the determinant expansion, each row index and each column index occurs exactly once. Consequently each product has valuation at least $2\sum_i w_i$, and so does their signed sum. Cancellation can raise the valuation, but cannot lower it. Thus

$$
v_p^{\mathrm G}(\Delta_K)\ge2\sum_{i=0}^{h-1}w_i.
$$

The weights may be half-integers; only their sums enter the inequalities. No fractional power of $p$ is needed in the basis change.

## Why residues modulo a prime help choose the basis

The poles of $W$ occur at some of the points $-j^2$. For an odd prime $p$, the residues $a$ and $-a$ have the same square. They should therefore be treated together.

For a positive integer $A$ and $1\le a\le(p-1)/2$, define

$$
\ell_A(a)=\#\{j:1\le j\le A,\ j\equiv a\text{ or }-a\pmod p\},
\qquad m_A=\lfloor A/p\rfloor.
$$

Here $\#$ means the number of elements, and $\lfloor\cdot\rfloor$ is the floor. The elementary identity

$$
\sum_{a=1}^{(p-1)/2}\ell_A(a)=A-m_A
$$

counts all integers up to $A$ except multiples of $p$. The zero residue class is handled separately. These counts measure how much numerator cancellation and denominator multiplicity can occur in each class.

Lemmas 8.1–8.3 and Proposition 8.4 organize an allocation of basis elements to those classes and sum their weights. The dimension count checks that the allocation uses exactly $h$ basis elements. **The additional local estimates must prove that a basis with the required entry valuations actually exists.** The counts do not establish that assertion by themselves. Lai imports the substantive estimates from Sections 3–4 of Fauzan's original paper.

## What the auxiliary functional changes

Lemma 7.3 rewrites the same bilinear form using poles at integers rather than negative squares. Its ingredients are as follows.

Define the Bernoulli numbers $B_r$ by

$$
\frac{z}{e^z-1}=\sum_{r=0}^{\infty}B_r\frac{z^r}{r!},
\qquad B_1=-\frac12,
$$

and the rational-linear functional $\mathcal L$ on polynomials in $x$ by $\mathcal L(x^r)=B_r$. Also write $H_j^{(5)}=\sum_{v=1}^jv^{-5}$ and $H_0^{(5)}=0$.

The auxiliary rule $\tau_X$ is defined on polynomial parts and simple integer poles by

$$
\tau_X(P)=\frac{\mathcal L(P''')}{24},\qquad
\tau_X\!\left(\frac1{x-r}\right)=H_{d(r)}^{(5)}-X,
\qquad
d(r)=\begin{cases}r,&r\ge0,\\-r-1,&r<0.\end{cases}
$$

Here $r$ is an integer, $P'''$ is the third derivative, and $x$ is another rational-function variable. Linearity defines $\tau_X$ on sums of these terms. Lemma 7.3 says

$$
\mu_X(R(t))=\tau_X\bigl(x^5R(-x^2)\bigr).
$$

Under $t=-x^2$, the poles at $-j^2$ become poles at $x=\pm j$. This makes the residue classes used above directly accessible to the arithmetic argument. It is a new expression for the same entries, not a new approximation to $\xi$.

## How the local bounds become an asymptotic cost

The proof uses rough bounds for small primes and sharper basis estimates for the remaining primes. The small-prime range is cut off at $K/M$; the other main ranges meet at $K/3$. The estimates continue beyond $K$ when necessary, up to $2h$. A separate argument deals with primes larger than $2h$.

The valuation of $F_K$ is the sum of the valuation of $\Delta_K$ and that of $S_K$. The latter is explicit. Legendre's formula gives, for a nonnegative integer $r$,

$$
v_p(r!)=\sum_{s\ge1}\left\lfloor\frac r{p^s}\right\rfloor,
$$

and hence

$$
v_p(S_K)=2h\,v_p(K!)+(h-1)v_p(4)
-12h\,v_p(N!)-2\sum_{i=1}^{h-1}v_p((2i)!).
$$

Theorem 9.3 then sums the local bounds with weight $\log p$. The prime number theorem, in the form $\vartheta(x)=\sum_{p\le x}\log p\sim x$, turns suitable weighted prime sums into integrals. The symbol $\sim$ means that the ratio tends to one.

For example, on a fixed interval $0<a\le p/K\le b$, a piecewise continuous bound of the form $L_p=Kf(p/K)+O(1)$ contributes asymptotically

$$
-\frac1{K^2}\sum_{aK<p\le bK}L_p\log p
\longrightarrow-\int_a^b f(y)\,dy.
$$

Here $O(1)$ means a uniformly bounded error. If instead the local expression is written $L_p=p\,g(K/p)$, substituting $x=K/p$ gives an integral with the factor $x^{-3}$. This explains that factor in Lai's arithmetic constants.

**What must be imported:** the actual local inequalities, their uniform errors, and the resulting cost bound. This companion explains how those assertions imply integrality and control the multiplier; it does not replace their proofs. The sign problem in the printed final cost and a documented alternative implementation are discussed in [companion 8](08_READING_CAUTIONS.md).

For the numerical contribution of each prime range and its proposed change at $k=7$, see the [exponent catalog](../EXPONENT_CATALOG.md). It reconstructs Fauzan's original floor-function formulas, distinguishes their numbering from Lai's, and includes an exact-arithmetic reproduction script.
