# Theorem 22 Implies Irrationality

Thread ID: 6af8b2e2-3c04-83e8-8651-43fc243265b9
Source: chatgpt
Snapshot: 2026-11-15T03:29:44.671Z
Export: user and assistant messages, in chronological turn order.
Credential redactions: 0

## Turn 1 — 2026-11-14T19:14:11.792Z

### User

Use this paper as context. Why does theorem 2.2 imply irrationality?

[User attached 1 file; file contents were not included]

## Turn 2 — 2026-11-14T19:15:18.818Z

### User

Relate it to other results like dirichlet's theorem on diophantine approximation

### Assistant

**The connection is that Dirichlet’s theorem guarantees good rational approximations, while Theorem 2.2 puts a limit on how accurate those approximations can be.** Taking the paper’s estimate as given, the two results together imply
\[
\boxed{2\le \mu(\zeta(5))\le260,}
\]
where \(\mu\) is the *irrationality exponent*. Here is how that relates to your original question.

## 1. Why the bound in Theorem 2.2 implies irrationality

Theorem 2.2, equation (4), on page 2 asserts that there is a threshold \(b_0\) such that
\[
\left|\zeta(5)-\frac ab\right|>\frac1{b^{260}}
\qquad
\text{for every }a\in\mathbb Z,\ b\in\mathbb Z_{\ge1},\ b\ge b_0.
\]
The crucial feature is **“for every \(a,b\)”**, with no requirement that the fraction be in lowest terms. :chatgpt-content-reference{index="5"}

Suppose \(\zeta(5)=p/q\) were rational. We could write the same number as
\[
\zeta(5)=\frac{kp}{kq}
\]
for any positive integer \(k\). Choose \(k\) large enough that \(kq\ge b_0\). The theorem would then give
\[
0=\left|\zeta(5)-\frac{kp}{kq}\right|
>\frac1{(kq)^{260}}>0,
\]
which is impossible.

This also handles the possibility that the reduced denominator \(q\) is smaller than \(b_0\): its multiples eventually exceed the threshold.

**The exponent \(260\) plays no role in this particular contradiction.** Any strictly positive lower bound, valid for all integer pairs with sufficiently large denominators, would rule out rationality. The exponent supplies additional information about approximation.

## 2. What Dirichlet’s theorem says

Dirichlet’s approximation theorem implies that for every irrational real number \(\alpha\), there are infinitely many distinct reduced fractions \(a/b\) satisfying
\[
0<\left|\alpha-\frac ab\right|<\frac1{b^2}.
\]
Thus every irrational number admits rational approximations whose error is smaller than the inverse square of the denominator. :chatgpt-content-reference{index="0"}

Compare the quantifiers and directions:

| Result | Which fractions? | Bound on the approximation error |
|---|---|---|
| Dirichlet, for an irrational \(\alpha\) | Infinitely many distinct fractions | \(\displaystyle \left|\alpha-\frac ab\right|<b^{-2}\) |
| Theorem 2.2, for \(\zeta(5)\) | Every fraction with sufficiently large denominator | \(\displaystyle \left|\zeta(5)-\frac ab\right|>b^{-260}\) |

Once the paper’s bound has established irrationality, Dirichlet applies to \(\zeta(5)\). Along infinitely many fractions, both estimates therefore hold:
\[
\boxed{
\frac1{b^{260}}
<
\left|\zeta(5)-\frac ab\right|
<
\frac1{b^2}.
}
\]

There is plenty of room between these bounds: for large \(b\), \(b^{-260}\) is vastly smaller than \(b^{-2}\).

Dirichlet guarantees that some approximations are good. The paper’s estimate says that no approximation with sufficiently large denominator is exceptionally accurate beyond its specified threshold.

### Why Dirichlet alone does not prove that a particular number is irrational

The infinitely-many-distinct-fractions conclusion above assumes irrationality. The finite form of Dirichlet applies to every real \(\alpha\): for each positive integer \(Q\), one can find \(a,b\) with
\[
1\le b\le Q,
\qquad
\left|\alpha-\frac ab\right|<\frac1{bQ}.
\]
For rational \(\alpha\), this can be satisfied by an exact representation once \(Q\) is large enough. So applying Dirichlet to an unknown number does not by itself determine whether it is rational. :chatgpt-content-reference{index="1"}

## 3. The elementary fact connecting approximation and irrationality

Suppose \(\alpha=p/q\) is rational. For every *different* fraction \(a/b\),
\[
\left|\frac pq-\frac ab\right|
=
\frac{|pb-aq|}{qb}
\ge\frac1{qb},
\]
because \(pb-aq\) is a nonzero integer.

This gives a useful principle:

> A fixed rational number cannot have nonzero rational approximation errors that become arbitrarily small compared with \(1/b\).

For example, if \(b>q\), then
\[
\frac1{qb}>\frac1{b^2}.
\]
Consequently, a rational number cannot have infinitely many distinct approximations satisfying
\[
0<\left|\alpha-\frac ab\right|<\frac1{b^2}.
\]

Together with Dirichlet, this gives an equivalence:
\[
\boxed{
\alpha\text{ is irrational}
\quad\Longleftrightarrow\quad
0<\left|\alpha-\frac ab\right|<\frac1{b^2}
\text{ for infinitely many distinct fractions}.
}
\]

There is a subtle distinction here that matters for Theorem 2.2. A rational number **does** satisfy
\[
\left|\frac pq-\frac ab\right|>b^{-260}
\]
for every *different* fraction with sufficiently large denominator, since
\[
\frac1{qb}>b^{-260}
\quad\text{once }b^{259}>q.
\]

Thus a lower bound restricted to nonzero errors would not establish irrationality. Theorem 2.2 works because its quantifiers include every pair \(a,b\), including the arbitrarily large representations \(kp/(kq)\) that would give zero error.

## 4. What the exponent \(260\) means

For an irrational number \(\alpha\), define its irrationality exponent by
\[
\mu(\alpha)
=
\sup\left\{
\nu>0:
0<\left|\alpha-\frac ab\right|<b^{-\nu}
\text{ for infinitely many reduced fractions }a/b
\right\}.
\]

A larger exponent means that exceptionally accurate approximations occur infinitely often.

The two bounds now have a precise interpretation:

- **Dirichlet gives \(\mu(\alpha)\ge2\)** for every irrational \(\alpha\).
- **Theorem 2.2 gives \(\mu(\zeta(5))\le260\)**, because approximations with error below \(b^{-260}\), or below any higher power threshold, are eventually excluded.

Hence
\[
\boxed{2\le\mu(\zeta(5))\le260.}
\]

The upper bound does not identify the exact exponent. It remains compatible, for example, with \(\mu(\zeta(5))=2\). Also, the non-strict inequality \(\mu\le260\) is deliberate: a supremum can equal \(260\) even when the defining approximation property fails at the endpoint \(260\).

There is an easy direction-of-inequality trap here: **a smaller exponent makes a lower bound stronger**. For \(b>1\),
\[
b^{-3}>b^{-260}.
\]
So replacing \(260\) by \(3\) in the paper’s lower bound would be a substantial improvement.

At exponent \(2\), constants and quantifiers become critical. An eventual bound
\[
\left|\alpha-\frac ab\right|>b^{-2}
\quad\text{for every }a,b
\]
would contradict Dirichlet for any irrational \(\alpha\).

## 5. Connections with Liouville’s and Roth’s theorems

These classical results also limit rational approximation, under an algebraicity assumption.

| Result | Assumption | Approximation restriction | Consequence |
|---|---|---|---|
| **Liouville’s theorem** | \(\alpha\) is algebraic of degree \(d\ge2\) | \(\displaystyle \left|\alpha-\frac ab\right|>\frac{C(\alpha)}{b^d}\) for some \(C(\alpha)>0\) | \(\mu(\alpha)\le d\) |
| **Roth’s theorem** | \(\alpha\) is algebraic and irrational | For every \(\varepsilon>0\), only finitely many fractions satisfy \(\displaystyle \left|\alpha-\frac ab\right|<b^{-(2+\varepsilon)}\) | Together with Dirichlet, \(\mu(\alpha)=2\) |
| **Theorem 2.2 in the paper** | The specific number \(\zeta(5)\) | Eventually, \(\displaystyle \left|\zeta(5)-\frac ab\right|>b^{-260}\) for every \(a,b\) | Irrationality and \(\mu(\zeta(5))\le260\) |

Liouville’s inequality and Roth’s improvement are stated in Roth’s original paper. :chatgpt-content-reference{index="2"}

Roth cannot simply be applied to obtain the paper’s result: it assumes that the number is an algebraic irrational. The paper’s estimate addresses a particular constant without making that assumption.

At the other extreme, **Liouville numbers** have irrationality exponent \(\infty\): they admit approximations beyond every finite power threshold. :chatgpt-content-reference{index="3"} Thus the estimate in Theorem 2.2 also rules out \(\zeta(5)\) being a Liouville number.

It does not establish transcendence. The bound is compatible with algebraic irrationality, since Roth’s exponent \(2\) lies within the interval \([2,260]\).

## 6. How this connects to the paper’s actual proof

The paper’s Lemma 3.1 uses the same basic arithmetic obstruction as
\[
|pb-aq|\ge1:
\]
**a nonzero integer has absolute value at least \(1\).**

The lemma considers integer polynomials \(Q_n\) with
\[
\deg Q_n\le dn,
\qquad
0<|Q_n(\alpha)|<e^{-cn^2},
\]
where \(c>0\).

If \(\alpha=p/q\) were rational, then clearing denominators would give
\[
q^{dn}Q_n(p/q)\in\mathbb Z\setminus\{0\}.
\]
Consequently,
\[
|Q_n(p/q)|\ge q^{-dn}=e^{-dn\log q}.
\]

But the constructed upper bound is \(e^{-cn^2}\). For fixed \(q\), it eventually becomes smaller than \(e^{-dn\log q}\), because \(n^2\) grows faster than \(n\). This contradicts the denominator-based lower bound.

So the paper’s polynomial criterion belongs to the same family of ideas as elementary Diophantine irrationality proofs: **construct a nonzero quantity that is analytically smaller than rationality would allow after clearing denominators.**

## Turn 3 — 2026-11-14T19:23:11.122Z

### User

What was the irrationality criterion in Apery's proof?

## Turn 4 — 2026-11-14T19:24:41.021Z

### User

Consider the notations in section 4.1. Do these arise naturally in the proof or are they just notational short hands for this specific argument?

### Assistant

**Both: the quantities have natural roles in the construction, while the particular numerical choice \(N/K=3/40\) is specific to this argument.** The section becomes much clearer if you rewrite its definitions as
\[
\boxed{
h=K-N,\qquad
\alpha=\frac NK,\qquad
\lambda=\frac hK=1-\alpha,\qquad
H=\frac{h+3N}{K}=1+2\alpha.
}
\]

Thus these are not six independent parameters. There is a size parameter \(K\), a chosen proportion \(N/K\), and several quantities determined by them. Section 4.1 fixes that proportion and writes
\[
K=40n,\qquad N=3n,\qquad h=37n.
\]
The relationships have structural explanations later in the paper. :chatgpt-content-reference{index="2"}

## 1. What each symbol represents

| Symbol | Meaning in the construction |
|---|---|
| \(K\) | The largest pole index in \(D_K(t)=\prod_{j=1}^{K}(t+j^2)\); the main size parameter |
| \(N\) | The cutoff in the numerator factor \(D_N(t)^6\); the first \(N\) poles cancel |
| \(h=K-N\) | The number of remaining poles, chosen as the size of the Hankel matrix |
| \(\alpha=N/K\) | The numerator cutoff as a proportion of the overall size |
| \(\lambda=h/K\) | The matrix size as a proportion of the overall size |
| \(H=(h+3N)/K\) | A normalized degree bound for the polynomial factors underlying the Gram matrix |

The most revealing relationships are \(h=K-N\) and \(HK=h+3N\).

## 2. Why \(h=K-N\) is natural

Section 5 defines the \(h\times h\) matrix
\[
G_K(X)_{ij}
=
\mu_X\!\left(
\frac{D_N(t)^6t^{i+j}}{D_K(t)}
\right),
\qquad 0\le i,j<h.
\]

Because \(D_N\) divides \(D_K\), the rational function inside the functional can be written as
\[
\frac{D_N(t)^5t^{i+j}}{D_K(t)/D_N(t)}.
\]
Its poles are precisely
\[
-(N+1)^2,\;-(N+2)^2,\;\ldots,\;-K^2.
\]
There are **\(K-N\) remaining poles**.

Now recall that the matrix entries are linear in \(X\), so
\[
G_K(X)=G_0+XG_1.
\]
In §6, the coefficient matrix \(G_1\) is factored as
\[
G_1=V\,\operatorname{diag}(d_k)\,V^{\mathsf T},
\qquad
V_{ik}=(-k^2)^i,
\]
where the columns correspond to the remaining poles \(k=N+1,\ldots,K\).

Choosing
\[
h=K-N
\]
makes \(V\) a **square Vandermonde matrix**. Its nodes are distinct, so it is invertible. Together with the nonzero \(d_k\), this gives
\[
\det G_1\ne0,
\]
and therefore
\[
\deg_X\det G_K(X)=h.
\]

So \(h=37n\) has a concrete explanation: it matches the \(40n-3n\) surviving poles.

This equality is a natural design choice for this determinant argument. It is not forced on every conceivable construction. For example, if one chose \(h>K-N\), then
\[
\operatorname{rank}G_1\le K-N<h,
\]
so the coefficient of \(X^h\) would vanish. The particular degree argument in §6 would fail.

## 3. Why \(H=1+2\alpha\) appears

At first glance, \(H=23/20\) looks like an arbitrary abbreviation. A useful interpretation follows directly from the matrix formula.

Split the sixth power into two third powers:
\[
G_K(X)_{ij}
=
\mu_X\!\left(
\frac{
\bigl(D_N(t)^3t^i\bigr)
\bigl(D_N(t)^3t^j\bigr)
}{D_K(t)}
\right).
\]

The polynomial factors here belong to the space
\[
\mathcal V
=
\left\{
D_N(t)^3q(t):\deg q<h
\right\}.
\]
Every polynomial in this space has degree
\[
\deg(D_N^3q)<3N+h.
\]

Consequently,
\[
H=\frac{3N+h}{K}
\]
records the degree bound relative to the main scale \(K\). Using \(h=K-N\),
\[
H
=
\frac{K+2N}{K}
=
1+2\alpha.
\]

With the chosen parameters,
\[
3N+h=9n+37n=46n,
\qquad
H=\frac{46n}{40n}=\frac{23}{20}.
\]

This also explains why the combination appears in the \(p\)-adic dimension allocation in §8. There the terms \(3\ell_N(a)\) and
\[
h-L_0+3(N-m_N)
\]
reflect the same third-power divisibility and degree count.

Thus **\(H\) is shorthand for a naturally recurring degree bound**. The paper does not spell out this motivation in §4.1, but it is visible from the later construction.

## 4. Why introduce \(\alpha\) and \(\lambda\) instead of keeping \(N\) and \(h\)?

These ratios become especially useful when the proof passes from finite products and matrices to asymptotic integrals.

### \(\alpha\) becomes an integration endpoint

Under the scaling \(y=K\sqrt t\),
\[
D_N(K^2t)
=
K^{2N}
\prod_{j=1}^{N}
\left(t+\left(\frac jK\right)^2\right).
\]
After taking logarithms and dividing by \(K\), the product produces a Riemann sum:
\[
\frac1K
\sum_{j=1}^{N}
\log\left(t+\left(\frac jK\right)^2\right)
\longrightarrow
\int_0^\alpha\log(t+u^2)\,du,
\]
because \(N/K=\alpha\).

This explains the upper endpoint \(\alpha\) in the external field of §11:
\[
V(t)
=
2\pi\sqrt t
+\int_0^1\log(t+u^2)\,du
-6\int_0^\alpha\log(t+u^2)\,du.
\]

So \(\alpha\) expresses a proportion that survives in the limiting problem.

### \(\lambda\) becomes the mass of a measure

The determinant integral has \(h\) integration variables. A normalized counting measure associated with them is
\[
\frac1K\sum_{i=1}^{h}\delta_{t_i}.
\]
Its total mass is
\[
\frac hK=\lambda.
\]

That is why the comparison measure \(\rho\) in §11 has mass \(\lambda=37/40\). The ratio is part of the limiting energy problem.

## 5. What is special about \(3/40\)?

**The paper fixes \(3/40\); it does not derive it from a uniqueness or optimality theorem.** Nor does §4.1 explain how the author found it.

Its later use shows what such a choice must accomplish. The proof has to balance:

- the arithmetic cost of making the polynomial coefficients integral;
- the analytic decay of the determinant at \(X=\zeta(5)\).

After combining these estimates, the desired outcome is
\[
\log|Q_{K,M}(\zeta(5))|
\le CK^2+o(K^2)
\qquad\text{with }C<0.
\]
The chosen ratio affects both sides of that balance.

At the level of parameterization, one could instead start with a rational proportion
\[
\alpha=\frac rs,\qquad 0<r<s,
\]
and write
\[
K=sn,\qquad N=rn,\qquad h=(s-r)n.
\]
Then
\[
\lambda=1-\alpha,\qquad H=1+2\alpha
\]
would retain exactly the same structural meanings. But obtaining the required decay would require redoing the arithmetic and analytic estimates for that ratio.

Once \(3/40\) is chosen, the remaining numerical values follow:

\[
\begin{aligned}
K=40n& &&\text{ensures that }N=\alpha K\text{ is integral},\\
N=3n& &&\text{uses the chosen proportion},\\
h=37n& &&\text{counts the surviving poles},\\
\lambda=37/40,\quad H=23/20& &&\text{record the resulting size and degree ratios}.
\end{aligned}
\]

## 6. Connection to your Apéry question

Apéry’s irrationality criterion was the elementary **small nonzero integer linear form criterion**:

> If there are integers \(P_n,Q_n\) such that
> \[
> Q_n\xi-P_n\ne0,
> \qquad
> |Q_n\xi-P_n|\longrightarrow0,
> \]
> then \(\xi\) is irrational.

Indeed, if \(\xi=a/b\), then
\[
b(Q_n\xi-P_n)=aQ_n-bP_n
\]
would be a nonzero integer tending to zero, which is impossible.

Apéry’s achievement was to construct approximations to \(\zeta(3)\) whose errors still tend to zero **after clearing their denominators**. The relevant exponential comparison is
\[
e^3(\sqrt2-1)^4\approx0.5913<1:
\]
the denominator-clearing factor grows at exponential rate \(e^3\), while the unscaled linear-form errors decrease at rate \((\sqrt2-1)^4\). :chatgpt-content-reference{index="0"}

The uploaded paper uses a related criterion with integer polynomials of growing degree:
\[
\deg Q_n\le37n,
\qquad
0<|Q_n(\zeta(5))|<e^{-cn^2}.
\]
For a hypothetical rational value \(a/b\), clearing denominators costs a factor \(b^{37n}\), which the quadratic exponential decay defeats.

This is what gives the parameter choices their purpose: **they arrange the determinant’s dimension, pole structure, divisibility, and real size so that the final decay survives all denominator clearing.** The notation records that structure; the specific proportion \(3/40\) is the chosen numerical input.

## Turn 5 — 2026-11-14T19:36:20.877Z

### User

Create a dependency map of the proof including all the lemmas in the paper. It should start with the final result, then what results were needed, etc...

### Assistant

Created a **backward dependency map starting at Theorem 2.2**, covering **all 15 lemmas and all 25 numbered results**. It includes the supporting definitions, external inputs, and page references from the uploaded paper. :chatgpt-content-reference{index="2"}

**How to read it:** each result expands into the ingredients it uses. Thus \(A\to B\) means **“A depends on B.”** Shared-prerequisite links jump to results that appear in more than one branch.



::chatgpt-content-reference{index="0" is_streaming="false"}



### Printable version

:chatgpt-content-reference{index="1"}[Zeta5_Proof_Dependency_Map.pdf](sandbox:/workspace/scratch/ce8fb01f0cda/output/pdf/Zeta5_Proof_Dependency_Map.pdf)

The **11-page reference** contains seven branch diagrams followed by a complete register giving each numbered result’s statement, immediate prerequisites, role, and source pages.

### Important distinctions preserved in the map

- **The two conclusions of Theorem 2.2 have different dependencies.** Qualitative irrationality uses Lemma 3.1 and the constructed integer polynomials. The exponent-\(260\) bound additionally invokes the perturbation argument in §8 of the original preprint, which this paper does not reproduce.
- **Exact degree is stronger than necessary.** The completion cites Proposition 6.1, but Corollary 5.5 already gives the degree upper bound needed by Lemma 3.1. Both routes are shown.
- **Proposition 8.4 is not the determinant valuation bound.** It establishes that \(\gamma_p^{\mathrm{in}}\) is an integer. The inequality controlling the determinant’s coefficient valuations is a separate external input used in Proposition 9.2.

The map also flags a substantive problem in the final assembly: **equations (78), (82), and (106) add a positive correction \(E_M\), while the prose after (109) treats it as a favorable subtraction.** I have marked that transition as unresolved rather than drawing it as a justified implication. Theorem 8.5 is likewise marked because Remark 8.6 explicitly says its printed statement is not literally correct.

## Attachment metadata

- 2609.0080v1.pdf: Attachment metadata only; binary not exported by read_thread
