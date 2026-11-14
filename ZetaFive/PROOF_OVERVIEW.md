# The ζ(5) proof read backward

**The proof aims to produce a nonzero integer smaller than one.** It does this by constructing integer polynomials whose values at ζ(5) become extremely small. The difficult part is keeping those values small while making every coefficient an integer.

The numbered results below refer to Chun Wing Lai, [*On Fauzan’s Proof that ζ(5) is Irrational*, version 1, 29 September 2026](https://ai.vixra.org/pdf/2609.0080v1.pdf). They are **Lai’s numbers**, which differ from the original paper’s. Read the numbered sections below from top to bottom to work backward through the argument.

**A note about this version:** Lai’s exposition abbreviates some essential arguments and contains an inconsistent correction term. The map below explains the intended dependencies; the [reading cautions](#reading-cautions) identify where a fuller source is needed.

## 1 The last step is an impossible integer

**Lemma 3.1 gives irrationality.** To apply it to ζ(5), we need a sequence of polynomials with all four properties below.

| What we need | Where it comes from |
| --- | --- |
| Every coefficient is an integer. | Proposition 9.2, using prime-by-prime divisibility estimates. |
| Degree grows at most linearly with n. | Corollary 5.5; Proposition 6.1 gives the exact degree 37n. |
| The value at ζ(5) is strictly positive. | Proposition 5.6, using the positive integral representation. |
| That value is smaller than exp(−c n²), for a fixed c > 0. | Section 12, combining Theorem 9.3 with Proposition 11.7. |

**Why these conditions finish the proof.** Suppose ζ(5) = a/b. An integer polynomial of degree at most 37n, evaluated at a/b, has denominator dividing b to the power 37n. Therefore

$$
0 < b^{37n}Q_n(a/b) < \exp(37n\log b-cn^2).
$$

The middle expression is an integer. The right side eventually drops below one, because n² grows faster than n. That is impossible.

Notice what this argument does **not** require: small coefficients. The coefficients may be enormous. What matters is the degree and the value of the whole polynomial at ζ(5).

**Working backward:** we now need to construct the polynomials and establish those four properties.

## 2 Smallness must survive making the coefficients integers

**Section 12 joins two estimates.** The polynomial used there is

$$
Q_{K,M}(X)=m_{K,M}\,F_K(X),
\qquad F_K(X)=S_K\,\det G_K(X).
$$

Here K = 40n, and the matrix has h = 37n rows. Think of F as the determinant after a first explicit rescaling, and m as the remaining arithmetic adjustment. M is a fixed cutoff used to organize the prime estimates.

The final comparison is between:

- **Arithmetic cost:** an upper bound A on log(m)/K².
- **Analytic decay:** a negative upper bound U on log(F(ζ(5)))/K².

Adding them bounds log(Q(ζ(5)))/K². **The proof needs A + U < 0.** Terms of smaller order disappear in this comparison.

For orientation, Section 12 displays A₂₀₀ ≈ 1.349588 and U ≈ −1.366996: a small negative difference, about −0.017408. These figures explain the intended margin; Lai’s additional correction term needs separate attention below.

**Working backward:** the next two sections explain where the arithmetic cost and analytic decay come from.

## 3 The arithmetic branch makes the coefficients integral at an affordable cost

**Proposition 9.2 gives integer coefficients. Theorem 9.3 estimates the price.** These are separate tasks: an arbitrarily large multiplier would clear the denominators but could destroy the smallness.

For each prime p, the proof finds a lower bound Lₚ for the exponent of p in **every coefficient** of F. Negative exponents mean denominators. For example, a bound of −2 means that multiplying by p² removes that prime from all denominators.

It then takes m to be the product of p to the power −Lₚ. After multiplying, no coefficient has a prime left in its denominator. The coefficients are therefore integers. If Lₚ is positive, this operation divides out a common factor instead. Thus m is a **positive rational scaling factor**, not necessarily an integer.

**What supplies Lₚ?** Sections 7–9 organize the arithmetic:

| Ingredient | Its job |
| --- | --- |
| Lemma 7.3, the identity involving the auxiliary functional τ | Rewrites the same matrix entries in a form suited to divisibility calculations. |
| Lemmas 8.1–8.3 and Proposition 8.4 | Count the available basis elements and sum the proposed divisibility exponents. |
| Local estimates imported from Fauzan’s original Sections 3–4 | Prove that those exponents really bound the matrix entries and determinant. |
| Legendre’s formula, equation (75) | Counts prime factors in the factorials of the first scaling factor S. |
| Theorem 9.3 and the prime number theorem | Add the contributions of all primes to estimate the total size of m. |

The underlying idea is to change the polynomial basis so that divisibility becomes visible. The poles lie at negative squares. Modulo p, the integers a and −a have the same square, so poles group together. A basis adapted to these groups exposes common prime factors that an entry-by-entry denominator bound would miss.

The change of basis must itself be arithmetically harmless: its determinant is a p-adic unit, meaning it introduces no extra factor of p into the determinant. The detailed local estimates are the hard part; counting the basis elements alone does not establish them. The [formalization’s dependency notes](https://github.com/domino14/zeta5/blob/main/Zeta5/NOTES.md) help locate these separate obligations.

## 4 The analytic branch turns the determinant into an integral and bounds it

**Proposition 11.7 gives the bound for F(ζ(5)).** It needs three earlier ingredients.

**First, Lemma 11.6, Andréief’s identity, turns the determinant into a multiple integral.** Its integrand contains a squared product of all pairwise differences, together with one positive weight for each integration variable. This is the bridge from linear algebra to analysis. See also [Forrester’s explanation of Andréief’s identity](https://arxiv.org/html/1806.10411v1).

Why take logarithms? A large product becomes a sum. The pairwise differences become logarithms of distances; the remaining weights contribute a penalty called the **external field**, V. Definition 11.1 specifies that penalty, and Lemma 11.2 makes it explicitly computable.

**Second, Lemma 11.4 supplies one comparison distribution ρ that bounds every configuration.** It is assembled from sixteen simple distributions on nested intervals. Their potentials are explicit, and Lemma 11.3 computes their combined logarithmic energy.

The central requirement is a bound valid **at every point**, not just at the chosen interval endpoints:

$$
2U^\rho(t)-V(t)\leq M_0.
$$

Here Uρ(t) is the average logarithmic distance from t to the comparison distribution.

**Third, Lemma 11.5 lets that one comparison control all other distributions of the same mass.** Subtract ρ from a competing distribution σ. The difference has total mass zero, so its logarithmic energy is nonpositive. Expanding this statement gives

$$
I(\sigma)-\int V\,d\sigma
\leq \lambda M_0-I(\rho).
$$

This is why one carefully chosen comparison can bound the entire integral. The comparison need not be an exact optimizer.

For the actual finite collection of integration points, the proof must also handle the singularity of log distance at zero. Smoothing the points and controlling the resulting errors bridges that gap. Scaling the variables and estimating the factorials in S then yield Proposition 11.7. [Saff’s introduction](https://arxiv.org/html/1010.3760v1) explains the potential-theory background; its logarithmic sign convention differs from Lai’s.

## 5 Strict positivity prevents the construction from vanishing

**Proposition 5.6 says the matrix at ζ(5) is positive definite.** This is stronger than having positive entries.

Its input is **Corollary 4.7**, the positive integral representation. For any nonzero coefficient vector, form the corresponding polynomial q. The matrix’s quadratic form becomes an integral of q² against a weight that is positive throughout the positive real axis.

A nonzero polynomial cannot vanish throughout that axis. The integral is therefore strictly positive. All eigenvalues of the matrix are positive, so its determinant is positive. The scaling factors are positive too.

**Working backward:** we need a matrix whose quadratic form really is that integral. This is why the construction uses a moment matrix.

## 6 The matrix packages many simple expressions into one polynomial

**Definitions 5.1–5.2 construct the matrix and determinant.** Start with

$$
D_m(t)=\prod_{j=1}^{m}(t+j^2),
\qquad W(t)=\frac{D_N(t)^6}{D_K(t)},
\qquad N=3n.
$$

The entry in row i and column j is μₓ applied to $W(t)t^{i+j}$. A matrix whose entries depend only on i+j is called a **Hankel matrix**.

**Lemma 5.4 breaks each rational function into a polynomial part and simple fractions. Corollary 5.5 then shows that each matrix entry has the form aX+b, with rational a and b.** In a determinant of size h, each term multiplies h such entries. Its degree is consequently at most h.

**Proposition 6.1 goes further:** a Vandermonde determinant on distinct pole locations shows that the top coefficient does not cancel. The degree is exactly h. The upper bound already suffices for Lemma 3.1.

The modifier W serves two purposes at once: it preserves positivity on the integration domain and creates useful arithmetic cancellations. These purposes compete—altering W can improve divisibility while worsening the size estimate. [Calegari’s reconstruction](https://galoisrepresentations.org/2026/09/24/zeta5-is-irrational/) explains this design choice and its connection to earlier approximation methods.

**Working backward:** everything now rests on the rule μₓ and its integral interpretation.

## 7 The starting bridge is one rule with two interpretations

**Lemmas 4.5 and 4.6 identify μ evaluated at ζ(5) with integration against a positive weight:**

$$
\mu_{\zeta(5)}(R)=\int_0^\infty R(y^2)\,w(y)\,dy,
\qquad w(y)>0.
$$

The rule is specified on two kinds of building block.

- **Powers of t.** Lemma 4.5 computes their integrals using Euler’s formula for even zeta values. The answers are rational.
- **Simple fractions 1/(t+j²).** Lemma 4.6 expresses their integrals as a rational multiple of ζ(5), plus a rational number. Replace ζ(5) by the symbol X to define μₓ.

Partial fractions and linearity extend the equality to the rational functions used in the matrix. This explains why the **same object** can be studied arithmetically as a polynomial in X and analytically as a positive integral when X = ζ(5). The moment representation also has an earlier source in [Prévost’s work on Hurwitz zeta approximants](https://arxiv.org/html/1709.05389v1).

## Reading cautions

Two points in the linked version should remain visible when following the map.

- **The correction term changes the final comparison.** Remark 8.6 describes a decrease in a valuation bound. Since m contains p to the power −Lₚ, such a decrease increases the arithmetic cost. Equations (106)–(107) add a positive correction Eₘ, but the following paragraph calls it favorable and treats it as subtracted. That inference does not follow as printed.
- **A grid is not a uniform bound.** Lemma 11.4 reports checks at 4,100 points in [0,10]. That alone does not establish the required inequality for every t ≥ 0.

These are limitations of this exposition as a complete proof. For a documented route around them, [mo271’s formalization](https://github.com/mo271/zeta5) uses revised local estimates, cutoff M = 400, and rigorous energy bounds. Its README reports a negative final margin and a proof using only Lean’s standard axioms. That is a different arithmetic implementation; it should not be presented as checking every printed step of Lai’s version.

**The extra approximation bound is a separate branch.** Theorem 2.2 also states |ζ(5)−a/b| > b⁻²⁶⁰ for sufficiently large b. Lemma 3.1 alone does not give that rate. It additionally requires control of how the determinant changes near ζ(5), using the perturbation argument cited from Fauzan’s Section 8.

For further reading and the obstruction to higher zeta values, see [Exposition and extensions](Literature/EXPOSITION_AND_EXTENSIONS.md).
