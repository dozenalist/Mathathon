# The role of Lai's Sections 8–12 in the final argument

[Overview](../PROOF_OVERVIEW.md) · [Reading cautions](08_READING_CAUTIONS.md)

**Sections 8–12 establish that making the determinant's coefficients integral does not destroy its small value at $\zeta(5)$.** This is the main quantitative difficulty.

Section and result numbers in this document refer to [Chun Wing Lai's exposition, version 1](https://ai.vixra.org/pdf/2609.0080v1.pdf). They are the paper's numbers, rather than the thematic numbering of our overview.

Write $Q=mF$, where $F$ is the normalized Hankel determinant and $m$ is a positive rational factor chosen to make all coefficients integers. Both depend on the size parameter $K=40n$, with $n$ a positive integer. We suppress the subscripts and hold the prime cutoff fixed. The matrix size is $h=37n$.

Read the following from the final comparison back to its inputs.

## Section 12 combines the arithmetic cost and the analytic decay

It needs bounds of the form

$$
\log m\le AK^2+o(K^2),
\qquad
\log F(\zeta(5))\le UK^2+o(K^2).
$$

Here $A$ measures the arithmetic cost, $U<0$ measures the analytic decay, and $o(K^2)$ denotes terms whose ratio to $K^2$ tends to zero. All logarithms are natural.

Adding the two inequalities bounds $\log Q(\zeta(5))$. **The decisive requirement is $A+U<0$.** Sections 9 and 11 supply the two bounds. Once the sum is negative, the terms of smaller order can be absorbed to give

$$
0<Q(\zeta(5))<\exp(-cn^2)
$$

for some constant $c>0$ independent of $n$, and all sufficiently large $n$.

## Section 11 supplies the analytic decay

It rewrites the determinant as a multiple integral and bounds that integral using logarithmic energy. Its output, Proposition 11.7, says that $F(\zeta(5))$ is exponentially small on the $K^2$ scale. This establishes how much arithmetic cost the construction can afford.

The main inputs are Andréief's determinant identity, a comparison measure with an explicit potential bound, and the nonpositivity of logarithmic energy for a signed measure of total mass zero. The [analytic companion](04_ANALYTIC_ESTIMATES.md) explains how they fit together.

## Section 9 supplies integrality and bounds its cost

For each prime $p$, it takes an integer lower bound $L_p$ for the exponent of $p$ in every coefficient of $F$. For a rational coefficient, this exponent is the exponent in its numerator minus the exponent in its denominator. Choosing

$$
m=\prod_{p\le2h}p^{-L_p}
$$

makes the coefficients integral, provided the separate estimates for larger primes also hold. A positive $L_p$ permits division by a common factor; a negative $L_p$ requires clearing a denominator. This is Proposition 9.2.

Theorem 9.3 then estimates

$$
\log m=-\sum_{p\le2h}L_p\log p.
$$

Thus Section 9 turns many local divisibility statements into one global cost bound. Section 8 supplies the inner-range estimates; Section 10 evaluates one saving in the outer-range contribution. The [arithmetic companion](03_ARITHMETIC_ESTIMATES.md) explains the prime ranges and the summation.

## Section 10 calculates a particular arithmetic saving

Lemma 10.1 evaluates an integral as $9/640$. That quantity is subtracted from the outer-prime cost. Its role is to improve the final numerical margin. It is one component of the arithmetic estimate, not an independent irrationality argument.

This calculation matters because the difference between the total arithmetic cost and the available analytic decay is small. The [exponent catalog](../EXPONENT_CATALOG.md) places this saving among the other contributions.

## Section 8 supplies the local divisibility information

It groups poles by residue classes modulo a prime and allocates basis elements to those classes. The resulting weights describe divisibility that can be extracted from the determinant.

Lemmas 8.1–8.3 organize the counts and weight sums. Proposition 8.4 checks that the resulting exponent is an integer. The substantive assertion that this exponent bounds the determinant's coefficient valuations requires the local estimates imported from Fauzan. Theorem 8.5 concerns the asymptotic form needed when Section 9 sums over primes; Remark 8.6 raises the correction issue discussed in the reading cautions.

## How these sections finish the argument

Earlier sections already supply **controlled degree and strict positivity**. Once Sections 8–12 also give integrality and sufficient decay, Lemma 3.1 finishes.

Indeed, suppose $\zeta(5)=a/b$, with $a$ an integer and $b$ a positive integer. Since $Q$ has integer coefficients and degree at most $37n$, the number $b^{37n}Q(a/b)$ is an integer. The bounds above would give, for sufficiently large $n$,

$$
0<b^{37n}Q(a/b)
<\exp(37n\log b-cn^2)<1.
$$

This is impossible. The quadratic decay defeats the linear cost of clearing the fixed denominator $b$.

These are the intended dependencies. In Lai's printed version, the correction-term sign and the justification of the uniform energy bound remain the qualifications identified in the [reading cautions](08_READING_CAUTIONS.md).
