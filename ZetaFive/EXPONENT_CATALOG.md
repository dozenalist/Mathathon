# Exponent contributions from zeta five to zeta seven

[Proof overview](PROOF_OVERVIEW.md) · [Arithmetic guide](ProofGuide/03_ARITHMETIC_ESTIMATES.md) · [Exact arithmetic script](Computation/exponent_catalog.mjs)

**With the original determinant geometry held fixed, the adapted arithmetic estimate increases by $751/768=0.977864583\ldots$, while the leading real-value estimate stays unchanged.** The resulting upper-bound coefficient changes from $-0.017407802\ldots$ to $+0.960456781\ldots$. The latter estimate does not supply the decay required by the irrationality criterion.

Throughout, use $K=40n$, $N=3n$, $h=37n$, $\alpha=N/K=3/40$, $\lambda=h/K=37/40$, and the numerator $D_N^6$. The prime cutoff is $M=200$. All entries below multiply **$K^2$**, not $n^2$; multiply by $1600$ to convert.

**Source and claim status.** **F** denotes [Fauzan's original paper](https://zenodo.org/records/22826419/files/ZETA5_IS_IRRATIONAL.pdf?download=1); **L** denotes [Lai's exposition, version 1](https://ai.vixra.org/pdf/2609.0080v1.pdf). The $k=5$ column reconstructs F's estimates. The $k=7$ column is our extension calculation using the local replacements below, not a theorem stated in either source. The accompanying script verifies the rational formulas, integrals, and totals. It does not certify the uniform local determinant estimates for $k=7$; those remain proof obligations for a fully verified extension.

| Contribution to the coefficient of $K^2$ | $k=5$ | $k=7$ | Change | Source of the $k=5$ bound and the adaptation |
| --- | ---: | ---: | ---: | --- |
| Small-prime estimate: $\sqrt{5K}<p\le K/200$ | $+0.027750000$ | $+0.037000000$ | $+0.009250000$ | [F Lemma 3.3 and (3.12)][F-small]; [Proposition 5.2][F-primes]. Replace the local loss $6$ by $8$. |
| Inner range: $3\le K/p\le20$ | $+0.042788177$ | $+0.566954844$ | $+0.524166667$ | [F Proposition 4.1][F-inner], [(5.4)–(5.7)][F-limits], [(5.18)][F-totals] and [Appendix B.1][F-appendix]. Use $R_7=R_5+2\lambda x$. |
| Inner tail: $20\le K/p\le200$, using the tail bound | $-0.051690063$ | $+0.031559938$ | $+0.083250000$ | [F Section 5.3, (5.12)–(5.17)][F-tail]. Integrate the same added term $2\lambda x$. |
| Outer range: $K/3<p\le2h$ | $+1.330739583$ | $+1.691937500$ | $+0.361197917$ | [F Lemma 4.2 and Proposition 4.3][F-outer], [(5.8)–(5.10)][F-primes]; [L Lemma 10.1][L-outer]. Recompute residue weights, polynomial rank, and zero-weight saving. |
| **Arithmetic subtotal $A_{200}^{(k)}$** | **$1.349587698$** | **$2.327452281$** | **$+0.977864583$** | [F Proposition 5.2][F-primes], [(5.19)–(5.21)][F-totals]; [L Lemma 12.2][L-total] for the displayed $k=5$ number. |
| **Real-value estimate $U$** | **$-1.366995500$** | **$-1.366995500$** | **$0$** | [F Lemmas 6.1–6.2][F-energy] and [Proposition 6.3][F-real]; [L Lemmas 11.4–11.6 and Proposition 11.7][L-real]. The fixed change in weight affects lower orders. |
| **Final coefficient $A_{200}^{(k)}+U$** | **$-0.017407802$** | **$+0.960456781$** | **$+0.977864583$** | [F Section 7][F-real]; compare [L Lemma 3.1][L-criterion]. Only a negative coefficient gives the required decay. |

The tail row is an **upper bound**, not an exact evaluation of the tail integral. A positive final upper bound is not a lower bound on the polynomial's actual value. It proves neither growth of that value nor impossibility of a better construction or estimate.

## What the coefficients estimate

Put

$$
D_m(t)=\prod_{j=1}^m(t+j^2),\qquad
G_{K,k}(X)=\left[\mu_{k,X}\!\left(\frac{D_N(t)^6t^{i+j}}{D_K(t)}\right)\right]_{0\le i,j<h},
\qquad \Delta_{K,k}(X)=\det G_{K,k}(X).
$$

Keep the same scalar normalization at both values of $k$:

$$
S_K=\frac{(K!)^{2h}4^{h-1}}{(N!)^{12h}\prod_{i=1}^{h-1}((2i)!)^2},
\qquad F_{K,k}=S_K\Delta_{K,k},\qquad Q_{K,M,k}=m_{K,M,k}F_{K,k}.
$$

For a rational polynomial $P$, its Gauss valuation $v_p^{\mathrm G}(P)$ is the minimum of the $p$-adic valuations of its coefficients. Integer lower bounds $L_p^{(k)}\le v_p^{\mathrm G}(F_{K,k})$ give

$$
m_{K,M,k}=\prod_{p\le2h}p^{-L_p^{(k)}},\qquad
\log m_{K,M,k}=-\sum_{p\le2h}L_p^{(k)}\log p.
$$

The sign matters: a positive valuation bound permits division by a common factor, so $m$ is a positive **rational** number. Negative entries in the table represent arithmetic savings. [F Proposition 5.1][F-limits], or [L Proposition 9.2][L-primes], converts these local bounds into integrality. The target estimates are

$$
\limsup_{K\to\infty}\frac{\log m_{K,M,k}}{K^2}\le A_M^{(k)},\qquad
\limsup_{K\to\infty}\frac{\log F_{K,k}(\zeta(k))}{K^2}\le U.
$$

The arithmetic sum and the real estimate therefore add. Once positivity, integrality, and degree at most $h$ are available, $A_M^{(k)}+U<0$ would allow L Lemma 3.1 to apply.

**Convention needed to reproduce the table.** In [F Section 5.1][F-limits], the pole-count function is

$$
\ell(x,z)=\lfloor x-z\rfloor+\lfloor x+z\rfloor+1.
$$

[L equation (71)][L-inner] instead prints absolute values. That expression does not count residue classes. The table follows F's floor functions and Proposition 5.2, without L's additional $E_M$ correction. It must not be described as an application of L Theorem 9.3 exactly as printed. The inconsistency of the correction's sign in L is discussed in the [reading cautions](ProofGuide/08_READING_CAUTIONS.md). Also, the $M=400$ arithmetic implementation described in [mo271's formalization](https://github.com/mo271/Zeta5) has different constants; it is not the calculation tabulated here.

## The functional changes before any prime estimate

The natural higher-$k$ versions of L Lemmas 4.5–4.6 and 7.3 use

$$
\mu_{k,X}(t^e)=
\frac{(-1)^eB_{2e+2}(2e+k)!}{(k-1)!(2e+2)!},
$$

$$
\mu_{k,X}\!\left(\frac1{t+j^2}\right)
=j^{k-1}\bigl(X-H_j^{(k)}\bigr)-\frac1{k-1}+\frac1{2j},
\qquad H_j^{(k)}=\sum_{v=1}^j v^{-k}.
$$

If $\mathcal L(x^d)=B_d$, the auxiliary polynomial functional becomes

$$
\tau_k(P)=\frac{\mathcal L(P^{(k-2)})}{(k-1)!},\qquad
\mu_{k,X}(R(t))=\tau_{k,X}\bigl(x^kR(-x^2)\bigr).
$$

Thus $\mathcal L(P''')/24$ changes to $\mathcal L(P^{(5)})/720$. The general positive moment representation is also explained in [Calegari's reconstruction](https://galoisrepresentations.org/2026/09/24/zeta5-is-irrational/), building on the Hurwitz-zeta moment formulas.

The distribution identity in [F Lemma 3.2][F-distribution] has prefactor $p^{-(k-1)}$. Its change from $p^{-4}$ to $p^{-6}$ is the source of the inner-range loss. The local analytic-functional argument in F Lemma 3.1 must use the new derivative functional and degree thresholds. This is a different lemma from **L Lemma 3.1**, the unchanged irrationality criterion.

The harmonic loss is real at the level of an individual pole. At $p=11$ and $j=12$, all terms of $H_{12}^{(7)}$ except $11^{-7}$ are $11$-integral. Since $12^6$ is a unit,

$$
v_{11}^{\mathrm G}\!\left(\mu_{7,X}\!\left(\frac1{t+144}\right)\right)=-7.
$$

An unchanged lower bound of $-5$ for all such pole values is false. Any improvement must exploit the special determinant or its cancellations, rather than a universal pole bound.

## Small primes contribute an additional 0.00925

[F Lemma 3.3][F-small] combines an integer-valued polynomial estimate with bounds on the simple-pole terms. Equation (3.12), after the basis normalization defining $S_K$, gives

$$
v_p^{\mathrm G}(F_{K,5})\ge
-6h\lfloor\log_p(5K)\rfloor-hv_p(24).
$$

The derivative loss grows from three to five derivatives, and the harmonic loss grows from five to seven. The corresponding estimate to establish for $k=7$ is

$$
v_p^{\mathrm G}(F_{K,7})\ge
-8h\lfloor\log_p(5K)\rfloor-hv_p(720).
$$

The same $5K$ degree envelope works: the pullback numerator degree increases from at most $12N+4h+1$ to $12N+4h+3$, whose degree plus one is at most $5K$ for sufficiently large $K$.

For $p\le\sqrt{5K}$, even these coarse bounds cost only $O(K^{3/2}\log K)=o(K^2)$. On $\sqrt{5K}<p\le K/M$, the logarithmic floor is one. The prime number theorem, used in [F Proposition 5.2][F-primes], then gives coefficients

$$
\frac{6\lambda}{M}\quad\hbox{and}\quad\frac{8\lambda}{M}.
$$

At $M=200$ they are $111/4000$ and $37/1000$, with difference $37/4000=0.00925$. The fixed denominator change $24\to720$ affects only finitely many primes and adds no $K^2$ coefficient.

## The compact inner range contributes an additional 0.524166667

For $K/M<p\le K/3$, [F Proposition 4.1][F-inner] uses a basis grouped by square classes modulo $p$. Set

$$
\ell_A(a)=\#\{1\le j\le A:j\equiv\pm a\pmod p\}.
$$

The ordinary row weights in F (4.6) are

$$
w^{(5)}_{a,i}=i+3\ell_N(a)-\frac{\ell_K(a)+4}{2}.
$$

Replacing the distribution factor $p^{-4}$ by $p^{-6}$ changes them to

$$
w^{(7)}_{a,i}=i+3\ell_N(a)-\frac{\ell_K(a)+6}{2}
=w^{(5)}_{a,i}-1.
$$

The determinant bound uses twice the sum of the row weights. The reserved zero-class block has $O_M(1)$ rows. At the zero source the added $x^2$ in the pullback compensates the extra distribution loss; the cap supplied by ordinary sources changes only that bounded number of rows. Thus the proposed inner determinant bounds satisfy

$$
\gamma_{p,7}^{\mathrm{in}}
=\gamma_{p,5}^{\mathrm{in}}-2h+O_M(1).
$$

The counting and dimension statements corresponding to L Lemmas 8.1–8.3 still organize the same basis. They do not, by themselves, prove the changed entry bounds. The uniform functional estimate and the source-by-source comparisons in F Proposition 4.1 remain the required local justification.

Here is the limiting formula used in the computation. Put $x=K/p$, $H=\lambda+3\alpha=23/20$, and

$$
T=\lfloor2Hx\rfloor,\quad s=Hx-T/2,\quad
q=\lfloor2x\rfloor,\quad n_+=(2x-q)/2,\quad b=3\ell(\alpha x,z).
$$

Then the adapted version of F (5.4) is

$$
\Gamma_k(x)=\int_0^{1/2}(T-b)(T+b-\ell(x,z)-k)\,dz
+s(2T-q-k)+(s-n_+)_+.
$$

Writing $u_+=\max(u,0)$, and defining

$$
J(u)=mu-\frac{m(m+1)}4,\quad m=\lfloor2u\rfloor,\qquad
\mathcal N(x)=2\lambda x\lfloor x\rfloor
-12\lambda x\lfloor\alpha x\rfloor-2J(\lambda x),
$$

the arithmetic integrand is $R_k=-\Gamma_k-\mathcal N$. The scalar contribution $\mathcal N$ is unchanged. Directly integrating the change in the displayed formula gives

$$
\Gamma_7(x)=\Gamma_5(x)-2\lambda x,\qquad
R_7(x)=R_5(x)+2\lambda x.
$$

The prime number theorem introduces the measure $dx/x^3$. Therefore

$$
\int_3^{20}\frac{R_7(x)-R_5(x)}{x^3}\,dx
=2\lambda\left(\frac13-\frac1{20}\right)
=\frac{629}{1200}.
$$

[F (5.18) and Appendix B.1][F-appendix] supply the baseline

$$
\int_3^{20}\frac{R_5(x)}{x^3}\,dx
=\frac{322437603634266857629}{7535670527041937280000}.
$$

Adding $629/1200$ yields the $k=7$ value in the table. The script independently reconstructs this integral on the 143 rational intervals of F Appendix B.1, using the floor-function definition of $\Gamma_k$.

## The inner tail contributes an additional 0.08325

[F (5.16)–(5.17)][F-tail] bound two infinite tails. Subtracting the lower bound for the tail after $M$ from the upper bound for the tail after $20$ gives, for $40\mid M$,

$$
\int_{20}^M\frac{R_5(x)}{x^3}\,dx
\le T_5(M):=-\frac{2689}{48000}
+\frac{\lambda}{M}-\frac{2863}{240M^2}+\frac{32}{M^3}.
$$

The $k=7$ change is exact even though the baseline is an upper bound:

$$
T_7(M)=T_5(M)+2\lambda\left(\frac1{20}-\frac1M\right).
$$

At $M=200$,

$$
T_5=-\frac{827041}{16000000},\qquad
T_7=\frac{504959}{16000000},\qquad
T_7-T_5=\frac{333}{4000}.
$$

The negative tail contribution at $5$ is therefore replaced by a positive contribution at $7$. The same estimates on the periodic remainder in F Section 5.3 can be retained, because the additional term is just $2\lambda x$.

The small-prime and entire inner-range increments have an instructive sum:

$$
\frac{2\lambda}{M}
+2\lambda\left(\frac13-\frac1M\right)
=\frac{2\lambda}{3}=\frac{37}{60}.
$$

Changing the cutoff $M$ moves this extra cost between ranges; it does not remove it.

## The outer range contributes an additional 0.361197917

The outer calculation combines three ingredients: residue bounds from [F Proposition 4.3][F-outer], the rank correction from F Lemma 4.2, and the scalar factorial valuation from F (5.3). Here is the full decomposition. The source of each $k=7$ entry is the adapted formula described immediately below.

| Outer contribution | $k=5$ | $k=7$ | Change |
| --- | ---: | ---: | ---: |
| Bulk contribution of large poles | $14/9$ | $2$ | $+4/9$ |
| Savings from numerator zeros | $-2731/6400$ | $-351/800$ | $-77/6400$ |
| Full polynomial-correction rank cost | $361/3600$ | $3/200$ | $-307/3600$ |
| Additional saving from zero row weights | $-9/640$ | $0$ | $+9/640$ |
| Scalar normalization for $K/3<p\le K$ | $-3929/16000$ | $-3929/16000$ | $0$ |
| Scalar normalization for $K<p\le2h$ | $289/800$ | $289/800$ | $0$ |
| **Total** | **$127751/96000$** | **$27071/16000$** | **$1387/3840$** |

### Residues and numerator zeros

For an ordinary square class, write $\ell=\ell_K(a)$ and $\delta=1$ if $a\le N$, otherwise $\delta=0$. The remaining class dimension is $\ell-\delta$. The adapted weights from F (4.12) are

$$
w^{(k)}_{a,i}=
\begin{cases}
\min\!\left(0,i+3\delta-\dfrac{\ell+k-1}{2}\right),&i<\ell-2,\\
0,&i\ge\ell-2.
\end{cases}
$$

For $\delta=0$, their total cost $-2\sum_iw_{a,i}$ changes from $7(\ell-2)$ to $9(\ell-2)$. For a class with a numerator zero, the weight sum and the number $z$ of zero weights change as follows:

| $\ell$ | Cost at $5$ | Cost at $7$ | $z$ at $5$ | $z$ at $7$ |
| --- | ---: | ---: | ---: | ---: |
| 2 | 0 | 0 | 1 | 1 |
| 3 | 1 | 3 | 1 | 1 |
| 4 | 2 | 6 | 2 | 1 |
| 5 | 4 | 9 | 2 | 1 |
| 6 | 6 | 12 | 3 | 2 |

These are exact sums of the displayed weights. Counting the classes gives the first two rows of the outer table. This incorporates the increased harmonic denominator loss while preserving the congruence between the two small pole values in a class for odd $k$.

### Polynomial moments supply a compensating improvement

There is a useful gain at $7$:

$$
\mu_{7,X}(t^e)=\mu_{5,X}(t^e)\frac{(2e+6)(2e+7)}{30}.
$$

For sufficiently large primes, the von Staudt–Clausen argument preceding F (4.10) shows integrality for $e<2p-3$ at $5$. At $7$ it extends to $e<3p-4$. To see the cancellation, put $m=2e+2$. A possible Bernoulli denominator $p$ occurs when $m=a(p-1)$. For $a=1,\ldots,5$, the product $(m+1)\cdots(m+5)$ contains a factor divisible by $p$. The first uncancelled case is $a=6$, or $e=3p-4$.

Consequently the proposed correction ranks are

$$
r_{p,5}=(K+4N-2p+2)_+,\qquad
r_{p,7}=(K+4N-3p+3)_+.
$$

The rank bound comes from a block of zero rows and columns: the polynomial quotient of a matrix entry has degree at most $i+j+6N-K$, so entries below the moment threshold require no correction. This is the same mechanism as F (4.10), with a later threshold. Its limiting integrated cost falls from $361/3600$ to $3/200$.

### The zero-weight rank saving disappears at leading order

F Lemma 4.2 itself is unchanged. If the integral correction matrix has rank at most $r$ and the nonpositive row weights contain exactly $z$ zeros, it bounds the additional loss by $\min(r,z)$, rather than $r$.

At $5$, the distinction saves $9/640$, the integral evaluated in [L Lemma 10.1][L-outer]. At $7$, with the revised ranks and row weights above, the limiting rank is already no greater than the zero-weight count throughout the outer range. There is no further leading saving from taking the minimum. The improved rank cost and loss of this separate saving must both be counted.

More explicitly, on $1/3<y<1/2$ the limiting zero-weight count at $7$, divided by $K$, is $y-\alpha+(1+\alpha-3y)_+$. It exceeds $(1+4\alpha-3y)_+$ throughout this interval. For $y\ge1/2$, the latter rank bound is zero. These comparisons explain why the additional saving vanishes.

### Explicit limiting functions for the outer integral

For reproduction, set $y=p/K$, $B=1+4\alpha=13/10$, and

$$
t_<(y)=\min(\alpha,1-2y)+(1+\alpha-3y)_+,
\qquad
t_>(y)=\min(\alpha,1-y)+(1+\alpha-2y)_+.
$$

On $1/3<y<1/2$, the residue costs are

$$
c_5(y)=7(1-y)-12\alpha-5t_<(y),\qquad
c_7(y)=9(1-y)-12\alpha-6t_<(y).
$$

On $1/2<y<1$, they are $c_k(y)=(k+2)(1-y)-6t_>(y)$. Set $c_k=0$ above $1$. The full rank costs are

$$
r_5(y)=(B-2y)_+,\qquad r_7(y)=(B-3y)_+,
$$

and the extra savings are

$$
d_5(y)=\bigl(B-3y-(1+\alpha-3y)_+\bigr)_+\,\mathbf 1_{(1/3,1/2)}(y),
\qquad d_7(y)=0.
$$

The scalar integrand, common to both values of $k$, is

$$
s(y)=-2\lambda\lfloor1/y\rfloor+\sum_{j=1}^{5}(2\lambda-jy)_+.
$$

Thus

$$
I_{\mathrm{out}}^{(k)}=\int_{1/3}^{2\lambda}
\bigl(c_k(y)+r_k(y)-d_k(y)+s(y)\bigr)\,dy.
$$

Every piece is affine on rational subintervals, so this calculation is exact rational arithmetic. The script reconstructs both outer totals from these functions, rather than taking the totals as numerical input.

**Primes above $K$ remain in this integral.** The determinant is integral there by the mechanism in F Proposition 4.3, but $S_K$ contains factorials through $(2h-2)!$. On $1<y<2\lambda$, $s(y)=2\lambda-y$, giving

$$
\int_1^{2\lambda}(2\lambda-y)\,dy
=\frac{(2\lambda-1)^2}{2}=\frac{289}{800}.
$$

Omitting this contribution would substantially understate both arithmetic costs.

## The real-value coefficient remains unchanged

The higher-$k$ weight is

$$
w_k(y)=\frac{2(2\pi)^{k-1}y^k}{(k-1)!}
\sum_{\ell\ge1}\ell^{k-1}e^{-2\pi\ell y}>0.
$$

It obeys $w_k(y)\le C_k(1+y)^k e^{-2\pi y}$ for fixed $k$. The polynomial factor changes, but the exponential tail does not. The analogues of L Corollary 4.7 and Proposition 5.6 therefore retain positivity. Andréief's identity, L Lemma 11.6 or F (6.10), gives the determinant integral with the same squared Vandermonde and rational modifier.

Under $y_i=K\sqrt{t_i}$, the external field remains

$$
V(t)=2\pi\sqrt t+\int_0^1\log(t+x^2)\,dx
-6\int_0^\alpha\log(t+x^2)\,dx.
$$

It depends on the modifier and the fixed geometry, not on whether $k$ is $5$ or $7$. The same comparison measure of mass $\lambda$ can therefore supply the leading coefficient. [F Lemma 6.1 and Appendix A][F-energy] give the potential and energy certificate; F Lemma 6.2 supplies the zero-mass energy inequality. The corresponding statements in L are Lemmas 11.4–11.5. L's reported grid check alone is not a uniform certificate; see the [analytic guide](ProofGuide/04_ANALYTIC_ESTIMATES.md).

The real $K^2$ contributions at both $k$ values are

| Contribution | Value | Source or calculation |
| --- | ---: | --- |
| Comparison-potential term $\lambda M_0$ | $-6.146625000000$ | $M_0=-1329/200$ in F Lemma 6.1 / L Lemma 11.4. |
| Negative comparison energy $-I(\rho)$ | $+2.126593445147\ldots$ | F Appendix A; L Lemmas 11.3–11.4. |
| Factorial normalization $C_*$ | $+2.653035990340\ldots$ | F (6.15), also L Lemma 11.4. |
| Sum before rounding upward | $-1.366995564512\ldots$ | $\lambda M_0-I(\rho)+C_*$. |
| Adopted rational upper bound $U$ | $-1.366995500000$ | F Lemma 6.1 / Proposition 6.3; L Proposition 11.7. |

Here

$$
C_*=-2\lambda+12\alpha\lambda(1-\log\alpha)
+3\lambda^2-2\lambda^2\log(2\lambda).
$$

The four terms are respectively $-1.85$, $+2.988897415234\ldots$, $+2.566875$, and $-1.052736424893\ldots$. They come from Stirling estimates for the factorials in $S_K$ and are unchanged.

Before this finite $K^2$ coefficient can be used, the larger $K^2\log K$ terms cancel:

| Source of $K^2\log K$ | Coefficient at both $k$ values |
| --- | ---: |
| Squared Vandermonde | $2\lambda^2=1.71125$ |
| Rational modifier $D_N^6/D_K$ | $\lambda(12\alpha-2)=-1.0175$ |
| Raw determinant subtotal | $0.69375$ |
| Scalar $S_K$ | $-0.69375$ |
| Total | $0$ |

The extra $y^2$ in the weight does not disturb this cancellation. Using the estimates of F (6.11)–(6.15), it adds $2h\log K+O(K)$ to the coarse real bound. For example, the resulting $24K\log K$ allowance at $5$ can be enlarged to $26K\log K$ at $7$, with a new constant multiplying $K$. Both disappear after division by $K^2$.

## Terms below quadratic order

These terms cannot repair a fixed positive $K^2$ coefficient within the same estimate scheme.

| Contribution | Size | Effect of changing $5$ to $7$ |
| --- | --- | --- |
| Primes $p\le\sqrt{5K}$ under the coarse local bound | $O(K^{3/2}\log K)$ | Changes the constant, not the order. |
| Fixed denominator $(k-1)!$ | $O(K)$ for its explicit factorial-valuation term | $24$ becomes $720$. |
| Bounded counting errors in the inner range | $O_M(K)$ for fixed $M$ | Includes the reserved zero block. |
| Polynomial factor in the real weight | $O_k(K\log K)$ | Adds $2h\log K$ to the same coarse estimate. |
| Remaining one-variable integral | $O_k(K)$ in the logarithm | Its constant changes with $k$. |
| Prime-number-theorem error | $o(K^2)$ | Needed in both cases; no numerical leading coefficient. |
| Clearing a hypothetical rational value $a/b$ in L Lemma 3.1 | $h\log b=O_b(K)$ | Same degree bound $h$. |

For the one-variable integral arising after the energy bound, an explicit constant is

$$
J_k=\int_0^\infty t^{-1/2}(1+\sqrt t)^k e^{-\sqrt t}\,dt
=2\sum_{j=0}^k\binom{k}{j}j!.
$$

It changes from $J_5=652$ to $J_7=27400$. Its contribution changes by $h\log(J_7/J_5)$, which is linear in $K$.

## What must improve to recover the irrationality criterion

Adding the exact arithmetic increments gives

$$
A_{200}^{(7)}-A_{200}^{(5)}
=\frac{37}{60}+\frac{1387}{3840}
=\frac{751}{768}.
$$

In particular,

$$
A_{200}^{(7)}+U
=\frac{90471073220559134733281}{94195881588024216000000}
=0.960456781075\ldots.
$$

At $5$, F's constants give $-0.017407802258\ldots$, or $-27.8524836133\ldots$ as a coefficient of $n^2$. At $7$, the adapted coefficient is $+1536.73084972\ldots$ in units of $n^2$. L Lemma 3.1 remains valid; this calculation fails to establish its smallness hypothesis.

For cutoffs $M$ divisible by $40$, the same accounting gives $A_M^{(7)}=A_M^{(5)}+751/768$. Even letting the cutoff tend to infinity leaves an upper-bound coefficient about $+0.928376$. A larger cutoff alone is therefore insufficient. The improved polynomial-moment threshold is already credited in the table and cannot be counted as an additional future gain.

The following directions address terms of the necessary quadratic size:

1. **Find determinant-specific cancellation in the local bounds.** A universal improvement of the individual pole bound is ruled out by the explicit $p=11$ example. The useful question is whether the worst-denominator contributions lie in low-rank subspaces or cancel in the determinant. Any saving must survive across enough primes to affect the $K^2$ term.
2. **Compare the row-weight estimate with exact primitive polynomial normalization.** Removing the actual rational content of $\Delta_{K,7}$ can reveal divisibility missed by the bounds. Finite computations would diagnose slack, while a uniform content estimate would be needed for a proof. A rational basis change by itself only multiplies the determinant by a rational square and does not change its primitive integer polynomial up to sign.
3. **Change the determinant family and recompute both sides together.** Varying $N/K$, $h/K$, the numerator multiplicity, or the pole geometry changes both the arithmetic integrals and the external field. More numerator zeros may improve local divisibility while worsening the real estimate. The equality $h=K-N$ is convenient for the exact degree formula, but the irrationality criterion only needs a linear degree upper bound and nonvanishing.
4. **Improve the real energy estimate if it is substantially loose.** This requires a certified improvement of the comparison bound or a different external field. Higher numerical precision in the existing constants cannot remove a gap of approximately $0.96$; their rounding slack is only about $6.5\times10^{-8}$.

## Reproducing the arithmetic

From the repository root, run:

```sh
node ZetaFive/Computation/exponent_catalog.mjs
```

The script uses only Node's standard library and exact `BigInt` fractions. It reconstructs the compact inner integral on 143 rational intervals, checks the identity $R_7-R_5=2\lambda x$, integrates all pieces of the outer formulas, sums the ordinary-class weights, and checks the tail bounds and final totals. Its JSON output includes exact fractions and the nine-decimal values in the opening table. The main table's numbers all pass these checks.

This computation verifies the numerical accounting. Completing the mathematical extension also requires uniform proofs of the proposed $k=7$ analogues of F Lemmas 3.1–3.3 and Propositions 4.1 and 4.3, including their exceptional classes and primes. The positive moment representation and L Lemma 3.1 do not remove those arithmetic obligations.

[F-small]: https://zenodo.org/records/22826419/files/ZETA5_IS_IRRATIONAL.pdf?download=1#page=8
[F-distribution]: https://zenodo.org/records/22826419/files/ZETA5_IS_IRRATIONAL.pdf?download=1#page=7
[F-inner]: https://zenodo.org/records/22826419/files/ZETA5_IS_IRRATIONAL.pdf?download=1#page=10
[F-outer]: https://zenodo.org/records/22826419/files/ZETA5_IS_IRRATIONAL.pdf?download=1#page=12
[F-limits]: https://zenodo.org/records/22826419/files/ZETA5_IS_IRRATIONAL.pdf?download=1#page=14
[F-primes]: https://zenodo.org/records/22826419/files/ZETA5_IS_IRRATIONAL.pdf?download=1#page=15
[F-tail]: https://zenodo.org/records/22826419/files/ZETA5_IS_IRRATIONAL.pdf?download=1#page=16
[F-totals]: https://zenodo.org/records/22826419/files/ZETA5_IS_IRRATIONAL.pdf?download=1#page=17
[F-appendix]: https://zenodo.org/records/22826419/files/ZETA5_IS_IRRATIONAL.pdf?download=1#page=26
[F-energy]: https://zenodo.org/records/22826419/files/ZETA5_IS_IRRATIONAL.pdf?download=1#page=17
[F-real]: https://zenodo.org/records/22826419/files/ZETA5_IS_IRRATIONAL.pdf?download=1#page=20
[L-criterion]: https://ai.vixra.org/pdf/2609.0080v1.pdf#page=3
[L-inner]: https://ai.vixra.org/pdf/2609.0080v1.pdf#page=12
[L-primes]: https://ai.vixra.org/pdf/2609.0080v1.pdf#page=13
[L-outer]: https://ai.vixra.org/pdf/2609.0080v1.pdf#page=14
[L-real]: https://ai.vixra.org/pdf/2609.0080v1.pdf#page=15
[L-total]: https://ai.vixra.org/pdf/2609.0080v1.pdf#page=17
