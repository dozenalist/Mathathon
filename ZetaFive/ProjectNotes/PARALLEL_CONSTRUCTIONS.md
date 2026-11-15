# Parallel constructions and their provenance

The useful organizing picture is one summation functional and one rational bilinear pencil. It explains how the algebraic formulas, positive integral, local arithmetic, and determinant estimates fit together. The construction and its main connections are Fauzan's; the project adds classical interpretations, alternative packaging, elementary corollaries, and a proposed teaching order. This is an explanatory companion, not a new irrationality proof or an independent verification of the source's quantitative estimates.

This note consolidates the final, corrected conclusions from the chats **Find parallel constructions in the Zeta(5)…** and **Draft parallel constructions for sections…**, reviewed on 14 November 2026. The first follows Fauzan's [17 September 2026 v1](https://zenodo.org/records/22826419). The six-page draft follows sections 1–7 of Chun Wing Lai's [29 September 2026 v1](https://ai.vixra.org/pdf/2609.0080v1.pdf). Their section and equation numbering differ. The earlier chat used “Chung Wing Lai”; the preserved source and draft identify the author as **Chun Wing Lai**.

Read the [revised framework companion](artifacts/UnifiedFramework/zeta5_unified_framework.pdf), its [editable source](artifacts/UnifiedFramework/zeta5_unified_framework.tex), or the narrower [sections 1–7 draft](artifacts/ParallelSections/lai_parallel_constructions.pdf). The revised framework includes attribution corrections made after the earlier snapshot in `ZetaFive/Literature/ParallelConstructions/`.

## The two objects

Use $\xi=\zeta(5)$, $K=40n$, $N=3n$, $h=K-N=37n$, and

$$
D_m(t)=\prod_{j=1}^m(t+j^2),\qquad T=D_K/D_N,\qquad W=D_N^5.
$$

For rational functions with polynomial part and only simple negative-square poles,

$$
\mu_X(R)=\tau_X\bigl(x^5R(-x^2)\bigr),\qquad
\mathcal B_{K,X}(p,q)=\mu_X(Wpq/T),\quad p,q\in\mathbb Q[t]_{<h}.
$$

The factor $x^5$ is essential: this is a **weighted** pullback, not substitution alone. The two expressions $D_N^6/D_K$ and $W/T$ are the same rational modifier after cancellation. The poles remaining in $W/T$ are exactly $-j^2$ for $N<j\le K$, and their number equals $h$.

In monomial coordinates, $G_K(X)=[\mathcal B_{K,X}(t^i,t^j)]$ is simultaneously:

- **Hankel:** its entry depends on $i+j$.
- **Affine:** $G_K(X)=G_0+XG_1$, because the polynomial part of $\mu_X$ is independent of $X$ and pole values are affine.
- **Gram at $X=\xi$:** the exact positive moment representation makes $G_K(\xi)$ positive definite.

These are descriptions of one matrix, not separate determinant constructions.

## The functional dictionary

Let $B_1=-1/2$, $L(x^k)=B_k$, and $H_j^{(5)}=\sum_{v=1}^jv^{-5}$ with $H_0^{(5)}=0$. The polynomial functional is

$$
\tau(P)=\frac1{24}L(P''')
=\left[\frac{\partial^4}{24(e^\partial-1)}P\right](0),\qquad \partial=d/dx.
$$

The operator notation is a terminating formal series on every polynomial. It does not assert convergence of an infinite differential operator on arbitrary rational functions. Its exponential symbol is $u^4/[24(e^u-1)]$.

On rational functions with polynomial part and simple integer poles, $\tau_X$ is characterized by

$$
\tau_X(g(x+1)-g(x))=g^{(4)}(0)/24\quad(g\text{ regular at }0),
$$
$$
\tau_X(g(-1-x))=-\tau_X(g(x)),\qquad \tau_X(1/x)=-X.
$$

The regularity restriction in the difference identity cannot be removed. If $a_r=\tau_X((x-r)^{-1})$, the difference law gives $a_r-a_{r-1}=r^{-5}$ for $r\ne0$; reflection supplies the negative half-lattice. Thus

$$
\tau_X((x-r)^{-1})=H_{d(r)}^{(5)}-X,
\qquad d(r)=\begin{cases}r&r\ge0,\\-r-1&r<0.\end{cases}
$$

This explains the harmonic increments and the single boundary parameter. It reorganizes Fauzan's own difference/reflection and uniqueness reasoning.

The pullback recovers the two defining clauses

$$
\mu_X(t^e)=\frac{(-1)^eB_{2e+2}(2e+3)(2e+4)(2e+5)}{24},
$$
$$
\mu_X((t+j^2)^{-1})=j^4(X-H_j^{(5)})-\frac14+\frac1{2j}.
$$

The pole calculation uses

$$
\frac{x^5}{j^2-x^2}=-x^3-j^2x-\frac{j^4}{2}\left(\frac1{x-j}+\frac1{x+j}\right).
$$

The $-1/4$ comes from $\tau(-x^3)$; the $1/(2j)$ comes from the difference between $H_j^{(5)}$ and $H_{j-1}^{(5)}$. Basic checks are $\tau(x^3)=1/4$, $\mu_X(1)=5/12$, and $\mu_X((t+1)^{-1})=X-3/4$.

## Real and p-adic readings of the same summation data

Set $f(y)=(e^{2\pi y}-1)^{-1}$. Fauzan's exact positive representation is

$$
\mu_\xi(R)=\int_0^\infty R(y^2)w(y)\,dy,
\qquad w(y)=\frac{y^5}{12}f^{(4)}(y)
=\frac{(2\pi)^4y^5}{12}\sum_{\ell\ge1}\ell^4e^{-2\pi\ell y}>0.
$$

An Abel–Plana boundary representation for $\tau_\xi$, followed by the weighted pullback and four integrations by parts, gives this same density. The exact Hermite identity is

$$
\Phi(a):=a^4\zeta(5,a)-\frac1{2a}-\frac14
=\int_0^\infty\frac{w(y)}{a^2+y^2}\,dy,\qquad a>0.
$$

This entire identity already appears in Fauzan's Proposition 2.2. Calling it $\Phi$ does not introduce a new object. Its integer samples give the pole values, while its asymptotic coefficients give the polynomial moments. In $z=a^2$, $\Phi(\sqrt z)$ is a Stieltjes transform. The precise finite remainder is

$$
\Phi(a)=\sum_{e=0}^{m-1}\frac{(-1)^e\mu_\xi(t^e)}{a^{2e+2}}
+\frac{(-1)^m}{a^{2m}}\int_0^\infty\frac{y^{2m}w(y)}{a^2+y^2}\,dy.
$$

The remainder has sign $(-1)^m$ and absolute value at most $\mu_\xi(t^m)a^{-2m-2}$. The associated infinite real series is generally divergent and is only asymptotic. That series alone neither identifies the transform nor proves positivity.

On polynomials, the p-adic Volkenborn integral gives

$$
\tau(P)=\frac1{24}I_p(P'''),\qquad
I_p(P)=\lim_{m\to\infty}p^{-m}\sum_{a=0}^{p^m-1}P(a),
$$

with the limit taken p-adically. It is not translation-invariant Haar integration. Integer poles require the specified algebraic extension. The same Bernoulli Laurent series converges for a far pole $|a|_p>1$, although its real interpretation is asymptotic. These are realizations of common formal data in different fields, not literal values in a common numerical field.

The residue-class identity has scale $p^{-4}$, and rescaling a simple pole contributes another $p^{-1}$. Requiring the identity at $1/x$ therefore forces $Y=p^5X+C_p$. The extended and analytic functionals complete the same data on appropriate domains. This mechanism, including why $Y$ is forced, is already in Fauzan's sections 3.1–3.2.

An optional regularized half-lattice formula is available by taking the finite part of a differentiated Hurwitz-regularized sum. Differentiation must occur **after** regularization. The naive formula $-\sum_{n\ge0}g^{(4)}(n)/24$ fails on polynomial parts: for $g=x^3$ it gives zero instead of $1/4$. Ordinary Abel–Plana evaluation also does not directly include the endpoint pole $1/x$.

## Residue slope, degree, and spectral consequences

For $R=P+\sum_j c_j/(t+j^2)$,

$$
\Lambda(R)=\sum_jc_jj^4=[t^{-3}]_\infty R(t),\qquad
\mu_X(R)=\mu_\xi(R)+(X-\xi)\Lambda(R).
$$

Consequently the bilinear pencil is exactly

$$
\mathcal B_{K,X}(p,q)=\int p(t)q(t)\,d\nu_K(t)+(X-\xi)\mathcal R_K(p,q),
$$
$$
d\nu_K(t)=\frac{W(t)}{T(t)}\frac{w(\sqrt t)}{2\sqrt t}\,dt,
\qquad \mathcal R_K(p,q)=[t^{-1}]_\infty\frac{t^2Wpq}{T}.
$$

The finite residue pairing lives on $\mathbb Q[t]/(T)$. With $a_j=-j^2$ and $d_j=j^4W(a_j)/T'(a_j)$,

$$
\mathcal R_K(p,q)=\sum_{j=N+1}^K d_jp(a_j)q(a_j),\qquad
G_1=V\operatorname{diag}(d_j)V^{\mathsf T}.
$$

There are $h$ distinct nodes and nonzero weights, hence

$$
\det G_1=(-1)^{h(h-1)/2}\prod_{j=N+1}^Kj^4D_N(-j^2)^5\ne0.
$$

This is the signed resultant of $T$ and $t^2W$, and proves $\deg\Delta_K=h$. The finite pairing describes the slope, not the whole functional: polynomial quotients still contribute to its constant part. Nor is it positive quadrature for the positive-axis measure. One parameter does **not** mean rank one; the slope has rank $h$.

The signed measure $\nu_K+(X-\xi)\sum_jd_j\delta_{a_j}$ gives an all-$X$ Andréief identity. At $X=\xi$ the positive measure proves nonvanishing; its highest parameter coefficient selects all distinct atoms and reproduces the slope determinant. This is an elementary combination of Fauzan's existing residue and Andréief formulas.

For $G=G_K(\xi)$, $M=G_1$, and $B=G^{-1/2}MG^{-1/2}$,

$$
\Delta_K(\xi+\delta)=\Delta_K(\xi)\det(I+\delta B)
=\Delta_K(\xi)\prod_j(1+\delta\beta_j).
$$

The $\beta_j$ are real and nonzero. All determinant roots are therefore real (multiplicities allowed), and their exact nearest distance to $\xi$ is $\|B\|^{-1}$. Fauzan already defines the relative matrix and eigenvalue product in Appendix C; the root statements are immediate corollaries. They explain the norm estimate as root exclusion.

For the basic irrationality criterion, exact degree is optional: affine entries already give $\deg\Delta_K\le h$, and positive definiteness gives $\Delta_K(\xi)>0$. The degree calculation remains useful structurally but need not precede the irrationality contradiction.

## The local bases and normalization costs

All arithmetic bases estimate $\mathcal B_{K,X}$, with different coordinates suited to different prime ranges.

| Construction | Role and necessary distinction |
|---|---|
| $q_i$ and $f_i=(D_N/(N!)^2)^3q_i$ | Integer-valued pullbacks; their rational change-of-basis determinant contributes to $S_K$. This is not generally a unimodular change from monomials. |
| $E_{a,i}$ in the inner range | Prescribed local jet vanishing. Their Chinese-remainder argument uses an auxiliary modulus $\prod_a(t+a^2)^{L_a}$, not generally $T$. |
| $P_aq_{a,i}$ in the outer range | Exact localization and pole cancellation using factors of $T$. The appropriate local bases are unimodular. |
| Row weights | $v_p^G(B_{ij})\ge w_i+w_j$ implies $v_p^G(\det B)\ge2\sum_iw_i$. Half-integral weights can be used directly as inequalities; $p^{1/2}$ is not presumed to lie in $\mathbb Q_p$. |
| Polynomial correction | For $G=A+p^{-1}L$ with $\operatorname{rank}_{\mathbb Q_p}L\le r$, nonpositive half-integral weights, and $z$ zero weights, the loss is at most $\min(r,z)$. The proof uses complementary minors; it cannot discard polynomial terms. |
| $\ell,\Gamma,\mathcal N,R,R_0,d$ | Exact rescaled counts or limiting profiles of local valuation budgets, not additional functionals. |

The Gauss valuation must remain coefficientwise: $v_p^G(\sum a_jX^j)=\min_jv_p(a_j)$. Evaluation at a favorable $X$ would lose coefficient control. Local lower bounds $L_p$ give $m=\prod_pp^{-L_p}$ and $mF_K\in\mathbb Z[X]$, with signed cost $\log m=-\sum_pL_p\log p$. Positive valuations permit dividing out primes; they must not be discarded. These are lower bounds, not claims of exact content.

The normalization chain $\Delta_K$, $F_K=S_K\Delta_K$, $Q_{K,M}=m_{K,M}F_K$, and the primitive representative $P_K$ changes scale while preserving roots and degree. A general basis change $C$ multiplies the Gram determinant by $(\det C)^2$. An integral leading coefficient alone does not show that the full polynomial, or $F_K$, is integral.

For rational content $\operatorname{cont}_{\mathbb Q}(A)$ chosen positive,

$$
\mathcal J_\xi(A)=\log|A(\xi)|-\sum_pv_p^G(A)\log p
=\log|A(\xi)/\operatorname{cont}_{\mathbb Q}(A)|
$$

is invariant under nonzero rational scaling. The criterion becomes $\deg A_K=O(K)$, $A_K(\xi)\ne0$, and $\mathcal J_\xi(A_K)\le-cK^2+o(K^2)$. If $\xi=a/b$, integrality forces $\mathcal J_\xi(A_K)\ge-\deg(A_K)\log b$, giving a contradiction. Fauzan already uses primitive normalization; this notation foregrounds its purpose.

## Bernoulli tails, integer-lattice products, and energy

With $\alpha=3/40$, $\lambda=37/40$, and $\widetilde B_k(x)=B_k(\{x\})$, the arithmetic tail functions satisfy

$$
F(x)+\lambda=2\lambda\widetilde B_1(x)-12\lambda\widetilde B_1(\alpha x),
$$
$$
P(x)-\overline P=\lambda\widetilde B_2(x)-74\widetilde B_2(\alpha x),
\qquad C(x)=\frac\lambda3\widetilde B_3(x)-\frac{74}{3\alpha}\widetilde B_3(\alpha x),
$$

where $\overline P=2923/240$. Thus $P'=F+\lambda$ and $C'=P-\overline P$ away from breakpoints. These continuous periodic primitives explain the two integrations by parts in the tail estimate. The functions and integrations already appear in Fauzan; the Bernoulli notation is explanatory.

The finite products also satisfy

$$
\frac{D_m(-x^2)}{(m!)^2}=\binom{m-x}{m}\binom{m+x}{m}
=\prod_{j=1}^m(1-x^2/j^2)\longrightarrow\frac{\sin\pi x}{\pi x}
$$

for fixed $x$, and

$$
D_m(y^2)=\frac{\Gamma(m+1+iy)\Gamma(m+1-iy)}{\Gamma(1+iy)\Gamma(1-iy)}.
$$

The fixed-$x$ sine limit cannot be substituted unchanged into the determinant regime $x=O(K)$. The corrected logarithmic derivative is $\pi\cot\pi x-1/x$. The small-prime $q_i$ are Newton/central-factorial type polynomials on $0,-1,-4,\ldots$; no unproved orthogonality identification is needed.

The exact cotangent-row kernel is

$$
\mathcal E_5(z)=\sum_{n\in\mathbb Z}(z+n)^{-5}
=\frac1{24}\frac{d^4}{dz^4}(\pi\cot\pi z),\qquad
w(y)=\frac{i}{\pi}y^5\mathcal E_5(iy).
$$

This is a single periodic lattice row. The full odd-weight level-one Eisenstein lattice sum cancels. A weight-six Eichler-integral connection gives useful context for $\zeta(5)$ but supplied no demonstrated replacement for local valuation bounds or the energy certificate.

A direct useful uniform estimate in the supporting arithmetic note is

$$
0\le E_m(t):=\sum_{j=1}^m\log(t+(j/K)^2)
-K\int_0^{m/K}\log(t+u^2)\,du
\le E_m(0)=2\log(m!)-2m\log m+2m.
$$

It follows from monotonicity of the logarithm and its derivative and holds for all $t\ge0$. Thus, for fixed $a>0$ and $m=aK\in\mathbb Z$,

$$
\log D_m(K^2t)=2m\log K+K\int_0^a\log(t+u^2)\,du+O(\log K)
$$

uniformly through $t=0$. The field in the real determinant estimate is consequently

$$
V(t)=2\pi\sqrt t+\int_0^1\log(t+u^2)\,du
-6\int_0^\alpha\log(t+u^2)\,du.
$$

At finite primes, Legendre's formula evaluates the same factorial/product data through floors instead. These are related inputs evaluated at different places, not identical functions or error analyses.

Taking logarithms of the Vandermonde integral gives $2\sum_{i<j}\log|t_i-t_j|-K\sum_iV(t_i)$. For equal-mass positive measures $\eta,\rho$ of mass $\lambda$, suitable logarithmic integrability, and $2U^\rho-V\le M_0$, the zero-mass energy inequality gives

$$
I(\eta)-\int V\,d\eta\le\lambda M_0-I(\rho).
$$

The measure $\rho$ is an auxiliary comparison certificate; it is neither the original positive moment measure nor asserted to be an equilibrium measure. The circle measure $\sigma$ regularizes an empirical configuration. A real-axis potential inequality does not automatically hold on its complex circles: circle-average and self-energy errors remain necessary. The comparison-measure distinction and these controls are already explicit in Fauzan's section 6.

## What belongs in a better exposition

The user preferred a better explanation, not necessarily a shorter proof. A useful ordering is: state the integer-polynomial criterion; introduce the summation functional; derive the weighted pullback and exact positive integral; state the Gram-plus-residue identity; separate finite-prime and real estimates; compare the two costs; and present Appendix C as perturbation consequences of the same pencil.

Keep three layers distinct: intrinsic functional identities; designed parameters and determinant family; and quantitative certificates. The derivative order reflects the target $\zeta(5)$, but numerator power six, $N/K=3/40$, local bases, and the sixteen-arcsine measure are choices for balancing estimates. No classical reinterpretation makes their quantitative verification automatic.

The six-page **Parallel constructions in Lai's sections 1–7** stops before the later prime, energy, and perturbation estimates. Its scope is the functional, pullback, modifier, Hankel/Gram/affine descriptions, continuous and discrete pairings, and normalization. Subsequent turns in that same chat produced a separate whole-argument overview and correctness review. That overview is conditional on its two stated estimates, with Fauzan's arithmetic estimate explicitly used because Lai's printed correction still needs an extra bound; the rounded $1.35K^2$ and $-1.36K^2$ estimates give $e^{-16n^2}$ when $K=40n$.

## Attribution and validation

| Connection | Already explicit in Fauzan v1 | Added presentation |
|---|---|---|
| Weighted pullback and pole laws | (3.1)–(3.3), p. 6; Lemma 3.2, pp. 7–8 | Euler–Maclaurin symbol and axiomatic opening |
| Exact continuous-$a$ Hurwitz integral and density | Proposition 2.2, p. 5 | Stieltjes language, integer samples versus asymptotic moments |
| Positive Gram and residue slope | Sections 2.3–2.4, pp. 4–5 | Residue algebra/resultant and all-$X$ signed-measure packaging |
| Relative matrix and eigenvalue product | Appendix C, pp. 29–31 | Real-root and exact root-distance corollaries |
| Forced $Y$, local bases, rank lemma | Sections 3–4; Lemma 4.2, p. 12 | Volkenborn, jets, and determinant-line interpretations |
| Periodic primitives | Section 5.3, p. 16 | Periodic Bernoulli notation |
| Comparison measure and energy controls | Section 6, pp. 17–20 | Abstract certificate formulation |
| Primitive normalization | Appendix C.3, p. 31 | Scale-invariant logarithmic evaluation notation |

The chat's last turn explicitly withdrew earlier suggestions of substantial novelty. Even the broad architecture is explained in Fauzan's introduction. No research-priority claim is made.

Independent reviews in the source chats rederived the central identities and corrected the sine derivative, function-domain qualifications, and energy regularization wording. The standard-library `framework_checks.py` checks polynomial laws through degree 24, weighted moments through degree 11, three exact residue/resultant examples, periodic Bernoulli identities, and numerical Stieltjes/cotangent sanity checks. These finite and numerical checks support the exposition; they do not independently verify all local estimates or the final irrationality claim.

Classical references used in the preserved companion include [DLMF Bernoulli formulas](https://dlmf.nist.gov/24.4), [Hurwitz-zeta identities](https://dlmf.nist.gov/25.11), [sine products and cotangent partial fractions](https://dlmf.nist.gov/4.22), [Volkenborn's original paper](https://www.numdam.org/book-part/MSMF_1974__39-40__375_0/), and the [Chinese remainder theorem](https://stacks.math.columbia.edu/tag/00DT). The project consolidates their use in the chats; it does not claim a fresh external literature review.
