# 1. The last step: an impossible integer

[Overview](../PROOF_OVERVIEW.md) · [Next: normalization and decay](02_NORMALIZATION_AND_DECAY.md)

**Lemma 3.1 finishes the irrationality argument once four properties of the constructed polynomials are available.** This file explains that last deduction, then works backward to its inputs. Result numbers throughout this guide refer to [Lai's version 1](https://ai.vixra.org/pdf/2609.0080v1.pdf), unless another source is named.

**Notation introduced here.** Write

$$
\xi=\zeta(5)=\sum_{v=1}^{\infty}\frac1{v^5}.
$$

The letter $X$ is a formal polynomial variable; $Q_n(\xi)$ means evaluation at the real number $\xi$. The index $n$ runs through positive integers. The notation $\mathbb Z[X]$ means polynomials with integer coefficients, and $\deg Q$ denotes degree. All logarithms are natural. Constants called $c$ and $d$ below are independent of $n$.

## What Lemma 3.1 gives us

The lemma says that $\xi$ is irrational if, for every sufficiently large $n$, there is a polynomial satisfying

$$
Q_n\in\mathbb Z[X],\qquad
\deg Q_n\le dn,\qquad
0<|Q_n(\xi)|<e^{-cn^2},
$$

where $d$ is a positive integer and $c>0$. In this construction, $d=37$, and the values are actually positive.

The decisive comparison is between two rates: clearing the denominator of a hypothetical rational value costs an exponential in $n$, while the polynomial value decays exponentially in $n^2$.

## Why a rational value would give a contradiction

Suppose $\xi=a/b$, where $a$ is an integer and $b$ is a positive integer. Write

$$
Q_n(X)=\sum_{j=0}^{dn}q_{n,j}X^j,
\qquad q_{n,j}\in\mathbb Z,
$$

putting zero coefficients above the actual degree. Then

$$
b^{dn}Q_n(a/b)
=\sum_{j=0}^{dn}q_{n,j}a^j b^{dn-j}
\in\mathbb Z.
$$

Every exponent of $b$ is nonnegative. This is precisely where the degree bound and integer coefficients enter.

The smallness and nonvanishing assumptions now give

$$
0<\left|b^{dn}Q_n(a/b)\right|
<\exp(dn\log b-cn^2).
$$

For $n>d\log b/c$, the expression on the right is less than one. A nonzero integer cannot have absolute value less than one.

Here $b$ is fixed by the hypothetical equality $\xi=a/b$. We are free to take $n$ as large as necessary after fixing $b$. There is no claim at this stage about how well varying rational numbers approximate $\xi$.

## What must be proved before applying the lemma

| Required fact | Result supplying it | Why it is needed |
| --- | --- | --- |
| $Q_n$ has integer coefficients. | Proposition 9.2; [companion 3](03_ARITHMETIC_ESTIMATES.md). | Makes $b^{37n}Q_n(a/b)$ an integer. |
| $\deg Q_n\le37n$. | Corollary 5.5; [companion 6](06_HANKEL_CONSTRUCTION.md). | Limits the power of $b$ needed to clear denominators. Proposition 6.1 proves equality, which is more than needed here. |
| $Q_n(\xi)>0$. | Proposition 5.6; [companion 5](05_POSITIVITY.md). | Excludes zero, which would not contradict integrality. |
| $\log Q_n(\xi)\le-cn^2$ eventually, for some $c>0$. | The combination in Section 12; [companion 2](02_NORMALIZATION_AND_DECAY.md). | Makes the resulting nonzero integer smaller than one. |

The size of the individual coefficients is irrelevant to this deduction. Large coefficients are acceptable if the value of the whole polynomial is small. Conversely, very small rational coefficients would not suffice: the constant polynomial $2^{-n^2}$ is tiny at every real number, but has no integer coefficients.

## Where the work moves next

The lemma is elementary. The substantial task is producing polynomials that satisfy all four requirements **simultaneously**. In particular, clearing denominators can increase the value enough to destroy the desired decay.

The [next companion](02_NORMALIZATION_AND_DECAY.md) explains the comparison that keeps this from happening. Its conclusion depends on valid arithmetic and analytic estimates; the qualifications concerning Lai's printed estimates are collected in [companion 8](08_READING_CAUTIONS.md).
