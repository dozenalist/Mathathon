# Explain Lai’s sections 8–11

Thread ID: 01a1dc7b-d3e2-7ef0-86db-54685dc36df9
Source: codex
Snapshot: 2026-11-15T03:29:44.668Z
Export: user and assistant messages, in chronological turn order.
Credential redactions: 0

## Turn 1 — 2026-11-14T23:54:26.000Z

### User

Consider again Lai's rewrite of Fauzan's proof of the irrationality of zeta(5). In particular, I don't understand sections 8-11. The purpose is to get some bounds on some quantities that are necessary to prove zeta(5) is irrational (review the rest of the paper for context). Nonetheless, I'm explicitly interested in sections 8-11. I want the major results that are obtained to come first in the overview and for the exposition to work backwards from there; i.e. if we have propositions A and B where A implies B, first state B, then state why we need A, then explain/prove A using the same approach. In particular, I am not an LLM. Make this human readable, not AI slop. 


### Assistant (commentary)

I’ll find the rewrite, read the surrounding argument, and build the explanation backward from what sections 8–11 are meant to establish. I’ll distinguish the claimed bounds from what the proofs actually justify.


### Assistant (commentary)

I found the rewrite used in your earlier sections 1–7 work. I’m using the PDF skill to check the formulas and section numbering, and I’ll have a second reader check how the arithmetic estimates fit together.


### Assistant (commentary)

The central comparison is now clear: the arithmetic estimates bound the cost of making the polynomial integral, while section 11 proves that its value at \(\zeta(5)\) shrinks faster than that cost grows. I also found inconsistencies in Lai’s stated correction to the arithmetic bound, so I’m checking Fauzan’s formulas before explaining that step.


### Assistant (commentary)

The check resolves the arithmetic issue: Lai’s table miscomputes \(\Gamma\). With the stated definition, the original asymptotic agrees with the discrete calculation, so the proposed extra correction is unnecessary. In section 11, the main missing explanation is how one chosen measure can bound every point configuration in the determinant integral; I’ll spell out that argument.


### Assistant (final_answer)

The main result of §§8–11 is a comparison between **the cost of making a polynomial integral** and **the smallness of its value at \(\zeta(5)\)**. With \(K=40n\), the two bounds are

\[
\boxed{
\begin{aligned}
\log m_{K,200}
&\le \bigl(1.3495876977\ldots+o(1)\bigr)K^2,\\
\log F_K(\zeta(5))
&\le -1.3669955\,K^2+O(K\log K).
\end{aligned}}
\]

Here \(F_K=S_K\Delta_K\) is the rational-coefficient polynomial constructed earlier, and \(m_{K,200}\) is a positive rational number chosen so that
\[
Q_{K,200}:=m_{K,200}F_K\in\mathbb Z[X].
\]
Sections 8–10 supply the arithmetic estimate, with its numerical evaluation completed in §12; section 11 supplies the real estimate. Their combination gives
\[
\log Q_{K,200}(\zeta(5))
\le -0.0174078022\ldots\,K^2+o(K^2).
\]

That negative coefficient is what all the estimates are trying to obtain. Since \(K=40n\), it implies
\[
0<Q_{40n,200}(\zeta(5))<e^{-139n^2/5}
\]
for sufficiently large \(n\).

Recall why this proves irrationality. The degree is at most \(37n\). If \(\zeta(5)=a/b\), then
\[
b^{37n}Q_{40n,200}(a/b)
\]
would be a positive integer, while its upper bound
\[
\exp\!\left(37n\log b-\frac{139}{5}n^2\right)
\]
tends to zero. The quadratic decay overwhelms the denominator arising from evaluating a degree-\(37n\) polynomial at \(a/b\).

There is a difficulty with [Lai’s rewrite](https://ai.vixra.org/pdf/2609.0080v1.pdf) that matters for your reading: it omits several essential explanations and introduces an incorrect numerical “correction” in §8.6. Below I explain the argument underlying these sections, using Fauzan’s original where necessary. I will identify the relevant errors at the points where they would otherwise cause confusion.

---

**Consider first the arithmetic bound.** We want to make \(F_K\) an integer polynomial while keeping the multiplier \(m_{K,M}\) sufficiently small. The natural way to do this is to examine one prime at a time.

For a rational-coefficient polynomial \(P\), write
\[
v_p^G(P):=\min\{v_p(c):c\text{ is a nonzero coefficient of }P\}.
\]
Thus \(v_p^G(P)\ge -3\) means that multiplying by \(p^3\) removes every power of \(p\) from the coefficients’ denominators. Conversely, \(v_p^G(P)\ge2\) means that we may divide by \(p^2\) and still have coefficients integral at \(p\).

Suppose we have proved
\[
v_p^G(F_K)\ge L_p
\]
for every relevant prime. Then we can take
\[
m_{K,M}=\prod_{p\le2h}p^{-L_p},
\qquad h=\frac{37}{40}K.
\]
The resulting polynomial is integral at every prime, hence has integer coefficients.

This explains why the signs of the \(L_p\) matter. Negative bounds require denominator clearing; positive bounds allow common factors to be removed. Both affect
\[
\boxed{\log m_{K,M}=-\sum_{p\le2h}L_p\log p.}
\]

The substantial conclusion of §9 is an upper bound for this sum:
\[
\boxed{
\limsup_{K\to\infty}\frac{\log m_{K,M}}{K^2}
\le
I_{\mathrm{out}}+\frac{6\lambda}{M}
+\int_3^M\frac{R(x)}{x^3}\,dx,
\qquad \lambda=\frac{37}{40}.
}
\tag{1}
\]
Here \(M\) is fixed while \(K\) tends to infinity. The three terms come from three ranges of primes:

| Primes | Contribution to the bound |
|---|---:|
| \(p\le K/M\) | \(6\lambda/M\) |
| \(K/M<p\le K/3\) | \(\displaystyle\int_3^M R(x)x^{-3}\,dx\) |
| \(K/3<p\le2h\) | \(\displaystyle I_{\mathrm{out}}=\frac{127751}{96000}\) |

The explicit integral calculations and tail bounds then give the number \(A_{200}=1.3495876977\ldots\) used above.

Why split the primes? The simplest denominator estimate is too expensive if applied everywhere. It is adequate for the small primes because there are relatively few of them. The larger primes require more information about the determinant.

For the middle range, §8 supplies
\[
v_p^G(\Delta_K)\ge\gamma_p^{\mathrm{in}},
\qquad
\gamma_p^{\mathrm{in}}=p\Gamma(K/p)+O_M(1).
\tag{2}
\]
The factorial expression \(S_K\) separately gives
\[
v_p(S_K)=p\mathcal N(K/p)+O_M(1),
\tag{3}
\]
by Legendre’s formula
\[
v_p(r!)=\sum_{j\ge1}\left\lfloor\frac r{p^j}\right\rfloor.
\]
I use \(\mathcal N\) for the function that the paper calls \(N(x)\), to distinguish it from the integer \(N=3K/40\).

Since \(F_K=S_K\Delta_K\), equations (2)–(3) explain the definition
\[
R(x)=-\Gamma(x)-\mathcal N(x).
\]
It is the signed contribution to the normalization cost.

The prime number theorem turns that cost into an integral:
\[
\frac1{K^2}
\sum_{K/M<p\le K/3}pR(K/p)\log p
\longrightarrow
\int_3^M\frac{R(x)}{x^3}\,dx.
\]
The factor \(x^{-3}\) has a simple origin. A prime sum weighted by \(\log p\) behaves asymptotically like an ordinary integral. In that integral, substitute \(p=K/x\): the summand contributes \(K/x\), and the differential contributes \(K/x^2\).

So the integral in §9 is the accumulated effect of the local divisibility estimates in §8.

**The crucial result of §8 is the first inequality in (2).** Lai spends considerable space proving that \(\gamma_p^{\mathrm{in}}\) is an integer, but the more important question is why it bounds the valuation of the determinant.

The elementary principle is this:
\[
v_p^G(B_{ij})\ge w_i+w_j
\quad\Longrightarrow\quad
v_p^G(\det B)\ge2\sum_iw_i.
\tag{4}
\]
Indeed, every determinant term contains one entry from each row and each column. Its valuation is therefore at least
\[
\sum_i(w_i+w_{\pi(i)})=2\sum_iw_i.
\]
Adding the determinant terms cannot lower this bound.

Thus we need a basis in which the entries admit useful row weights \(w_i\). Finding that basis is the main work.

The poles of our rational functions occur at \(t=-j^2\). Modulo \(p\), two such poles coincide precisely when their indices are congruent up to sign. This motivates
\[
\ell_A(a)
=
\#\{1\le j\le A:j\equiv a\text{ or }-a\pmod p\}.
\]
The number \(\ell_K(a)\) counts denominator factors concentrated at the residue class \(t=-a^2\); \(\ell_N(a)\) counts the corresponding numerator factors.

Suppose the two row polynomials vanish there to orders \(\nu_i(a)\) and \(\nu_j(a)\). The local estimate is
\[
\nu_i(a)+\nu_j(a)+6\ell_N(a)-\ell_K(a)-4.
\tag{5}
\]
Each term has a specific source:

- The zeros of the row polynomials supply the first two terms.
- \(D_N^6\) supplies \(6\ell_N(a)\).
- \(D_K\) costs \(\ell_K(a)\).
- The distribution formula for the auxiliary functional from §7 costs another four powers of \(p\).

One sees these powers by making the substitution \(x=a+pz\) in the pullback formula. Factors vanishing modulo \(p\) contribute powers of \(p\); the remaining factors are units. Fauzan’s local lemmas justify applying this count to the entire functional.

Now allocate \(L_a\) basis vectors to each residue class. For the vector numbered \(i\) in class \(a\), take
\[
E_{a,i}(t)
=
(t+a^2)^i\prod_{c\ne a}(t+c^2)^{L_c},
\qquad 0\le i<L_a.
\tag{6}
\]
This polynomial has a prescribed order of vanishing at its own class and high orders of vanishing at all the others. The factors \(t+c^2\) are distinct modulo \(p\), so the Chinese remainder theorem shows that these polynomials form a basis whose change-of-basis determinant is a \(p\)-adic unit. Consequently, changing to this basis preserves the determinant’s valuation.

The choice of \(L_a\) is designed to balance the vanishing supplied by the basis against the vanishing already supplied by \(D_N^6\). Put
\[
b_a=3\ell_N(a),
\qquad
L_a=T_p-b_a+\varepsilon_a,
\qquad \varepsilon_a\in\{0,1\}.
\tag{7}
\]
Then
\[
L_a+b_a=T_p+\varepsilon_a
\]
is almost the same in every class. Classes with more numerator zeros need fewer basis vectors.

The resulting row weights are
\[
w_{a,i}=i+b_a-\frac{\ell_K(a)+4}{2}.
\tag{8}
\]
The extra rows, where \(\varepsilon_a=1\), are assigned first to classes with larger \(\ell_K(a)\). That ordering ensures that the contribution from another residue class does not give a worse bound than the assigned weight.

The zero residue class requires a separate block of \(L_0=4M+10\) vectors, because \(t=-x^2\) has double vanishing at \(x=0\). Its size depends only on fixed \(M\), so it does not affect the leading asymptotic.

This is what the short counting lemmas accomplish. First,
\[
\sum_{a=1}^{(p-1)/2}\ell_N(a)
=N-\lfloor N/p\rfloor
\]
counts every nonmultiple of \(p\) exactly once. Using this identity, \(T_p\) and the number of extra rows are chosen so that
\[
L_0+\sum_aL_a=h.
\]
Thus (6) contains exactly the required number of basis vectors.

Second, summing the arithmetic progression (8) gives
\[
2\sum_{i=0}^{L_a-1}w_{a,i}
=
(T_p-b_a+\varepsilon_a)
(T_p+b_a+\varepsilon_a-\ell_K(a)-5).
\tag{9}
\]
Equation (4) now proves
\[
v_p^G(\Delta_K)\ge
2\sum_{a,i}w_{a,i}
=\gamma_p^{\mathrm{in}}.
\]
Equation (9) also explains why the exponent is an integer.

The limiting function \(\Gamma\) is obtained by averaging this calculation over the residue classes. Set
\[
x=K/p,\qquad z=a/p.
\]
The pole count has the exact expression
\[
\ell_A(a)=\ell(A/p,a/p),
\qquad
\ell(x,z)=\lfloor x-z\rfloor+\lfloor x+z\rfloor+1.
\]
A sum over \(a\) therefore becomes \(p\) times an integral over \(0<z<1/2\).

The integral part of \(\Gamma\),
\[
\int_0^{1/2}(T-b)(T+b-\ell-5)\,dz,
\]
is just (9) with no extra row, averaged over the classes. Here
\[
T=\lfloor2Hx\rfloor,\qquad
b=3\ell(\alpha x,z),\qquad
\alpha=\frac3{40},\quad H=1+2\alpha.
\]
The remaining terms in \(\Gamma\) count the extra rows: use the classes with larger pole count first, then the others.

This also explains the error \(O_M(1)\). For fixed \(M\), the floor functions have only a bounded number of jumps, and replacing each interval’s number of grid points by \(p\) times its length makes a bounded error.

There are two corrections to Lai worth making here. His finite allocation quotient \(T_p\) and the limiting quantity \(\lfloor2Hx\rfloor\) need separate notation; they need not be exactly equal. More seriously, his table in Remark 8.6 miscalculates \(p\Gamma(K/p)\). For example, at
\[
(M,K,p)=(40,320000,8009),
\]
the definitions give
\[
\gamma_p^{\mathrm{in}}=7390051,
\qquad
p\Gamma(K/p)=7389902,
\]
a difference of \(149\). The next row with \(M=40\) again gives difference \(149\). Exact calculation reproduces all his discrete \(\gamma_p^{\mathrm{in}}\) values, but not his printed \(\Gamma\) values. The original Riemann-sum argument gives (2); the proposed additional \(E_M\) is unnecessary.

**Section 10 belongs to the other branch of the arithmetic argument: the outer primes.** Its result is the exact saving
\[
\boxed{\int_{1/3}^{1/2}d(y)\,dy=\frac9{640}.}
\tag{10}
\]

Why is there a saving to calculate? In the outer range, Fauzan separates the matrix into a part controlled by row weights and a nonintegral correction of bounded rank. If the correction has rank at most \(r\), and exactly \(z\) row weights are zero, its effect on the determinant loses at most
\[
\min(r,z)
\]
powers of \(p\). Charging the full rank \(r\) would sometimes overestimate the loss. The function \(d(p/K)\) records that improvement, and its integral reduces \(I_{\mathrm{out}}\).

Once that purpose is understood, §10 is elementary. With \(\alpha=3/40\),
\[
d(y)=
\begin{cases}
9/40,&1/3\le y\le43/120,\\
13/10-3y,&43/120\le y\le13/30,\\
0,&13/30\le y\le1/2.
\end{cases}
\]
Its area is a rectangle plus a triangle:
\[
\frac9{40}\cdot\frac1{40}
+\frac12\cdot\frac3{40}\cdot\frac9{40}
=
\frac9{1600}+\frac{27}{3200}
=\frac9{640}.
\]
This improves the arithmetic constant by \(0.0140625\). It is unrelated to the logarithmic-energy integral of §11.

---

**Now return to the real bound from §11:**
\[
\boxed{
0<F_K(\zeta(5)),\qquad
\log F_K(\zeta(5))
\le -1.3669955K^2+24K\log K+200K.
}
\tag{11}
\]

There are two ingredients in this estimate because \(F_K=S_K\Delta_K\). The determinant bound has the form
\[
\log\Delta_K(\zeta(5))
\le
0.69375K^2\log K
+\bigl(\lambda M_0-I(\rho)\bigr)K^2
+O(K\log K),
\tag{12}
\]
while the factorial expression \(S_K\) gives
\[
\log S_K
\le
-0.69375K^2\log K+C_*K^2+O(K\log K).
\tag{13}
\]
The \(K^2\log K\) terms cancel exactly. The remaining coefficient is
\[
\lambda M_0-I(\rho)+C_*
=
-1.3669955645\ldots
<-1.3669955.
\]

Thus the choice of \(S_K\) is important on the real side as well as the arithmetic side.

The difficult part of (12) is controlling all configurations of points that occur in the determinant integral. The required estimate is
\[
2\sum_{i<j}\log|t_i-t_j|
-K\sum_iV(t_i)
\le
\bigl(\lambda M_0-I(\rho)\bigr)K^2+O(K\log K).
\tag{14}
\]
Before proving it, let us see why this particular expression appears.

The positive moment representation and Andréief’s identity give
\[
\Delta_K(\zeta(5))
=
\frac1{h!}\int_{(0,\infty)^h}
\prod_{i<j}(y_i^2-y_j^2)^2
\prod_{i=1}^h
\frac{D_N(y_i^2)^6}{D_K(y_i^2)}w(y_i)\,dy_i.
\tag{15}
\]
This also proves strict positivity.

Set \(y_i=K\sqrt{t_i}\). After extracting powers of \(K\), the principal exponential factor in the integrand is
\[
\exp\!\left(
2\sum_{i<j}\log|t_i-t_j|-K\sum_iV(t_i)
\right),
\]
where
\[
V(t)=2\pi\sqrt t
+\int_0^1\log(t+u^2)\,du
-6\int_0^\alpha\log(t+u^2)\,du.
\]

Each term comes directly from (15). The pairwise logarithms come from the squared Vandermonde. The term \(2\pi\sqrt t\) comes from the decay of \(w(K\sqrt t)\). The two integrals approximate the logarithms of the denominator product \(D_K\) and numerator product \(D_N^6\).

Both sums in (14) have size \(K^2\): there are order \(K^2\) pairs, and order \(K\) individual points, each multiplied by \(K\).

The question is therefore: **how can one bound this expression for every possible arrangement of the points?**

The answer is the comparison measure \(\rho\). Write
\[
U^\rho(t)=\int\log|t-u|\,d\rho(u),
\qquad
I(\rho)=\iint\log|t-u|\,d\rho(t)d\rho(u).
\]
What we need from \(\rho\) is
\[
\rho([0,\infty))=\lambda,
\qquad
2U^\rho(t)-V(t)\le M_0
\quad\text{for every }t\ge0.
\tag{16}
\]

Here is why those conditions are sufficient. Let \(\sigma\) be any positive measure of mass \(\lambda\), initially assuming finite energy and compact support. Expanding the energy of \(\sigma-\rho\) gives
\[
\begin{aligned}
I(\sigma)-\int V\,d\sigma
&=
I(\sigma-\rho)
+\int(2U^\rho-V)\,d\sigma-I(\rho)\\
&\le \lambda M_0-I(\rho).
\end{aligned}
\tag{17}
\]
There are exactly two reasons for the inequality:

1. The equal masses give \((\sigma-\rho)(\mathbb C)=0\), so the zero-mass energy lemma gives \(I(\sigma-\rho)\le0\).
2. Integrating (16) against the positive measure \(\sigma\) gives at most \(\lambda M_0\).

Equation (17) is the central idea of §11. A pointwise inequality involving one chosen measure bounds the energy of every competing measure of the same mass.

For our point configuration, the natural candidate is
\[
\sigma=\frac1K\sum_{i=1}^h\delta_{t_i},
\]
whose mass is \(h/K=\lambda\). Its off-diagonal energy gives exactly the pairwise sum in (14), divided by \(K^2\).

But point masses have infinite negative self-energy because \(\log|t_i-t_i|=-\infty\). We cannot apply (17) directly.

Fauzan replaces each point by uniform mass on a small circle of radius \(\varepsilon\) in the complex plane. The circle’s self-energy is \(\log\varepsilon\), its interactions with other circles bound the original point interactions from above, and averaging the potential of \(\rho\) over a circle introduces an error of order \(\sqrt\varepsilon\). This yields
\[
2\sum_{i<j}\log|t_i-t_j|-K\sum_iV(t_i)
\le
(\lambda M_0-I(\rho))K^2
+120\lambda K^2\sqrt\varepsilon-h\log\varepsilon.
\]
Choosing \(\varepsilon=K^{-2}\) makes the error \(O(K\log K)\), which is small compared with \(K^2\). This proves the required leading bound.

One more detail is necessary before integrating: a constant upper bound does not control an integral over an unbounded region. Fauzan retains a factor \(e^{-\sqrt{t_i}}\) for each variable. The remaining one-variable integral is
\[
\int_0^\infty t^{-1/2}(1+\sqrt t)^5e^{-\sqrt t}\,dt=652.
\]
Thus its contribution is only \(652^h\), whose logarithm is \(O(K)\). This completes the passage from the configuration bound to (12).

**It remains to explain how a suitable \(\rho\) is obtained.** We need a measure for which both the potential in (16) and the energy in (17) can be calculated accurately. Fauzan chooses
\[
\rho=\sum_{j=1}^{16}c_j\omega_{[a_j,b_j]},
\qquad
\sum_jc_j=\lambda,
\]
where \(\omega_{[a,b]}\) is the probability arcsine measure
\[
d\omega_{[a,b]}(t)
=\frac{dt}{\pi\sqrt{(t-a)(b-t)}}.
\]

The useful property is that its logarithmic potential is constant on its interval:
\[
U^{\omega_{[a,b]}}(t)=\log\frac{b-a}{4}
\qquad(a\le t\le b).
\]
Outside the interval, the potential also has an explicit formula.

The intervals are nested, with each new interval containing the earlier ones. Consequently, the interaction between its mass \(c_j\) and all the preceding mass \(S_{j-1}\) is easy to calculate. Including its self-interaction gives
\[
I(\rho)
=
\sum_{j=1}^{16}
\bigl(S_j^2-S_{j-1}^2\bigr)
\log\frac{b_j-a_j}{4},
\qquad S_j=\sum_{i\le j}c_i.
\]
The coefficient is simply
\[
c_j^2+2c_jS_{j-1}=S_j^2-S_{j-1}^2.
\]

The chosen rational intervals and weights give
\[
M_0=-6.645,\qquad
I(\rho)=-2.1265934451\ldots,\qquad
C_*=2.6530359903\ldots,
\]
and hence the negative coefficient in (11).

We do not need \(\rho\) to be the exact measure maximizing the energy. We need it to satisfy the two inequalities with enough room to obtain the desired constant.

Lai’s numerical grid does not prove the uniform inequality (16): sampling finitely many points leaves the intervals between them unchecked. Fauzan’s Appendix A supplies the needed argument, using rational upper and lower bounds on a finite partition of \([0,2]\), followed by an analytic estimate for \(t\ge2\).

Finally, the zero-mass energy lemma used in (17) has a short explanation. For a signed measure \(\nu\), define
\[
J(s)=\iint e^{-s|z-w|^2}\,d\nu(z)d\nu(w).
\]
The Gaussian kernel can be expressed as an integral of products of translated Gaussians, making \(J(s)\) an integral of a square. Thus \(J(s)\ge0\).

The integral representation of \(\log|z-w|\), together with \(\nu(\mathbb C)=0\), then gives
\[
I(\nu)=-\frac12\int_0^\infty\frac{J(s)}s\,ds\le0.
\]
Truncating the integral first and then taking limits justifies the calculation under the finite logarithmic-integrability hypothesis. The mass-zero condition is precisely what cancels the constant term in that representation.

The source texts used here are :codex-file-citation{path="C:/Users/andre/Documents/ChatGPT/Zeta 5/sources/Lai_2026_zeta5_rewrite.pdf" purpose="source"} and :codex-file-citation{path="C:/Users/andre/Documents/ChatGPT/Zeta 5/sources/Fauzan_2026_zeta5.pdf" purpose="source"}. The correction to Lai’s table is reproducible with this [exact-arithmetic check](</C:/Users/andre/Documents/ChatGPT/Zeta 5/tmp/lai_section_checks/check_arithmetic.py>).

## Turn 2 — 2026-11-15T00:54:06.000Z

### User

It seems there are two parts: analytic estimates and arithmetic estimates. Is this correct? Be brief in this response.


### Assistant (final_answer)

Yes.

- **Arithmetic estimates (§§8–10):** Show that \(Q_{K,M}=m_{K,M}F_K\) has integer coefficients and bound how much the multiplier \(m_{K,M}\) can grow.
- **Analytic estimates (§11):** Show that \(F_K(\zeta(5))\) is positive and decays sufficiently rapidly.

The analytic decay exceeds the arithmetic growth, leaving a positive integer polynomial value small enough to force irrationality.

## Turn 3 — 2026-11-15T00:54:30.000Z

### User

Do the arithmetic estimates include sectio 11


### Assistant (final_answer)

No. Section 11 provides the **analytic estimates**. Sections 8–10 provide the **arithmetic estimates**, and section 12 combines the two.

## Turn 4 — 2026-11-15T00:54:45.000Z

### User

Wrong section, sorry; section 7


### Assistant (final_answer)

Yes. Section 7 provides the **algebraic preparation for the arithmetic estimates**: its pullback identity rewrites the functional in a form suited to the \(p\)-adic analysis in §8.

Thus §§7–10 form the arithmetic part, with the estimates themselves in §§8–10.

