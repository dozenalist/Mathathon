# 5. Why the constructed value cannot vanish

[Overview](../PROOF_OVERVIEW.md) · [Previous: analysis](04_ANALYTIC_ESTIMATES.md) · [Next: the matrix](06_HANKEL_CONSTRUCTION.md)

**Proposition 5.6 gives $\Delta_K(\xi)>0$.** Since $S_K$ and $m_{K,M}$ are positive, this also gives $Q_{K,M}(\xi)>0$. It supplies the nonvanishing required by Lemma 3.1.

Recall $\xi=\zeta(5)$ and $\Delta_K=\det G_K$. The matrix has size $h=37n$. The positive measure introduced in [companion 4](04_ANALYTIC_ESTIMATES.md) is

$$
d\nu_K(y)=W(y^2)w(y)\,dy,\qquad y>0,
$$

where $W=D_N^6/D_K$ and $w$ is the positive exponential-series weight. This companion introduces the coefficient vector $\mathbf q$ and its associated polynomial $q$.

## To get a positive determinant, prove a positive quadratic form

A real symmetric matrix is **positive definite** if $\mathbf q^{\mathsf T}G\mathbf q>0$ for every nonzero real vector $\mathbf q$. Here $\mathsf T$ denotes transpose, as in companion 3.

A positive definite matrix has positive eigenvalues. Its determinant, the product of those eigenvalues, is therefore positive. This is why Proposition 5.6 proves positive definiteness rather than trying to estimate a determinant expansion with many signs.

Having positive entries alone would not suffice. For example, the matrix with rows $(1,2)$ and $(2,1)$ has positive entries and determinant $-3$.

## To get a positive quadratic form, use the moment representation

Take a nonzero vector $\mathbf q=(q_0,\ldots,q_{h-1})^{\mathsf T}$ and form

$$
q(t)=\sum_{i=0}^{h-1}q_i t^i.
$$

The matrix entries and the integral identity imply

$$
\begin{aligned}
\mathbf q^{\mathsf T}G_K(\xi)\mathbf q
&=\sum_{i,j=0}^{h-1}q_iq_j\int_0^\infty y^{2i+2j}\,d\nu_K(y)\\
&=\int_0^\infty q(y^2)^2\,d\nu_K(y)\\
&=\int_0^\infty W(y^2)q(y^2)^2w(y)\,dy.
\end{aligned}
$$

All sums here are finite. The integrals exist because the rational factor has no pole on the positive axis, while the exponential decay of $w$ dominates polynomial growth at infinity. Near zero both $W(y^2)$ and $w(y)$ are bounded.

Every factor in the integrand is nonnegative, and $W(y^2)w(y)>0$ for every $y>0$. A nonzero polynomial has only finitely many real zeros. Thus there is an interval on which $q(y^2)^2>0$, and the integral is strictly positive.

This proves positive definiteness, then positive determinant, then positive normalized polynomial value.

## What must be known to justify this identity

| Needed fact | Where it comes from |
| --- | --- |
| The entry in position $(i,j)$ is $\mu_\xi(Wt^{i+j})$. | Definition 5.1; [companion 6](06_HANKEL_CONSTRUCTION.md). |
| $\mu_\xi(R)=\int_0^\infty R(y^2)w(y)\,dy$ for the rational functions in question. | Corollary 4.7, obtained from Lemmas 4.5–4.6; [companion 7](07_MOMENT_REPRESENTATION.md). |
| $W(y^2)>0$ for $y>0$. | Each factor $y^2+j^2$ in its numerator and denominator is positive. |
| $w(y)>0$ and the relevant moments are finite. | The explicit series for $w$ and its endpoint behavior; [companion 7](07_MOMENT_REPRESENTATION.md). |

Although the functional was originally defined with rational coefficients, this finite quadratic-form calculation permits real $q_i$ by real linearity of the integral. No assumption about the rationality or irrationality of $\xi$ is involved.

## A two-dimensional example of the same argument

For any positive measure with these moments, put $m_r=\int y^{2r}\,d\nu(y)$ for $r=0,1,2$. The matrix of the functions $1,y^2$ is

$$
\begin{pmatrix}m_0&m_1\\m_1&m_2\end{pmatrix}.
$$

Normalize the measure to the probability measure $P=\nu/m_0$, and let $Z(y)=y^2$. Then

$$
m_0m_2-m_1^2=m_0^2\operatorname{Var}_P(Z).
$$

Here $\operatorname{Var}_P(Z)=\int Z^2\,dP-(\int Z\,dP)^2$. The variance is positive because $y^2$ is not constant on a measure supported throughout the positive axis. The larger determinant expresses the corresponding linear independence of $1,y^2,\ldots,y^{2h-2}$ in the integral inner product. This is what calling $G_K(\xi)$ a **Gram matrix** means.

The argument gives strict positivity, with no quantitative lower bound. That is enough for irrationality. Bounds on how the determinant changes near $\xi$ are an additional task, discussed in [companion 8](08_READING_CAUTIONS.md).
