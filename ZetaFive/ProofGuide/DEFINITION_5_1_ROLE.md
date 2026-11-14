# What Definition 5.1 is doing in the proof

[Overview](../PROOF_OVERVIEW.md) · [Detailed Hankel companion](06_HANKEL_CONSTRUCTION.md)

**The Hankel matrix turns the moment identities from Section 4 into a polynomial that can be used to prove irrationality. The object ultimately used is its determinant.**

Its particular arrangement lets the proof establish three things about that determinant: controlled degree, strict positivity at $\zeta(5)$, and a useful upper bound on its size.

For a positive integer $n$, the parameters are $K=40n$, $N=3n$, and $h=K-N=37n$. Write

$$
D_m(t)=\prod_{j=1}^{m}(t+j^2),
\qquad
W(t)=\frac{D_N(t)^6}{D_K(t)}.
$$

Here $t$ is the rational-function variable, and $X$ is a separate polynomial variable. The rule $\mu_X$ from Section 4 sends the relevant rational functions in $t$ to affine polynomials in $X$ with rational coefficients. [Definition 5.1](https://ai.vixra.org/pdf/2609.0080v1.pdf#page=6) sets

$$
G_K(X)_{ij}=\mu_X\!\left(W(t)t^{i+j}\right),
\qquad 0\le i,j<h.
$$

The reason for **$i+j$** is simply that $t^{i+j}=t^it^j$. The matrix records the bilinear form

$$
(f,g)\longmapsto\mu_X(Wfg)
$$

on the space spanned by $1,t,\ldots,t^{h-1}$. Entries depend only on the sum of their indices; this is what makes the matrix Hankel.

## 1. Its determinant is a polynomial of manageable degree

Each entry is a rational linear expression in $X$. Taking a determinant multiplies $h$ entries in each term, so

$$
\deg\det G_K(X)\le h=37n.
$$

Thus the construction combines many linear expressions into one polynomial while keeping its degree proportional to $n$. This is the consequence of Corollary 5.5 needed for the irrationality criterion.

## 2. The moment interpretation guarantees nonvanishing at $\zeta(5)$

Put $\xi=\zeta(5)$. For a real coefficient vector $\mathbf q=(q_0,\ldots,q_{h-1})^{\mathsf T}$, let $q(t)=\sum_{i=0}^{h-1}q_it^i$. The superscript $\mathsf T$ denotes transpose. The arrangement of the entries gives

$$
\mathbf q^{\mathsf T}G_K(\xi)\mathbf q
=\int_0^\infty W(y^2)\,q(y^2)^2\,w(y)\,dy.
$$

Here $y>0$ is the integration variable, and $w$ is the positive weight from Section 4, described in the [moment companion](07_MOMENT_REPRESENTATION.md). Also $W(y^2)>0$. For nonzero $q$, the integral is strictly positive because a nonzero polynomial cannot vanish on an interval.

Consequently $G_K(\xi)$ is positive definite and its determinant is positive. The Hankel structure makes the quadratic form assemble into a **square inside the integral**. This is the argument of Proposition 5.6.

## 3. The same structure makes the determinant accessible to the size estimate

Andréief's identity rewrites this moment determinant as a multiple integral containing

$$
\prod_{1\le i<j\le h}(y_i^2-y_j^2)^2,
$$

where $y_1,\ldots,y_h$ are the integration variables. That product brings in interactions between every pair of variables. There are $h(h-1)/2$ pairs, which helps explain the quadratic scale of the later logarithmic energy estimate.

After the prescribed normalization, that estimate supplies the required strong decay. The passage from the integral to the bound is explained in the [analytic companion](04_ANALYTIC_ESTIMATES.md).

## How this fits the final contradiction

The arithmetic argument studies divisibility of this same determinant, using changes of polynomial basis to expose common prime factors. It supplies a positive rational scaling factor that makes the coefficients integers, while controlling the effect on size.

The crucial achievement is the combination: degree growing like $n$, a value guaranteed to be nonzero, and—after the difficult estimates and denominator clearing—a value decaying like $\exp(-cn^2)$, where $c>0$ is independent of $n$.

Definition 5.1 selects a construction for which all three requirements can be approached together. These are the requirements that the [irrationality criterion](01_IRRATIONALITY_CRITERION.md) uses to produce the impossible integer at the end of the proof.
