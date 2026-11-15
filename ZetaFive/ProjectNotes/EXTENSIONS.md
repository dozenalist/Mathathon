# Extensions to zeta(7) and zeta(9)

The project explored what survives when Fauzan's zeta(5) determinant construction is transferred to higher odd zeta values. Positivity, dependence on a single zeta value, and the determinant degree survive. The inherited arithmetic bounds do not: exact finite examples contradict a literal reuse, and the revised normalization costs overwhelm the available real-decay budget. These are diagnoses of specified constructions, not proofs of irrationality or impossibility results for all variants.

The source is Aabir Fauzan, *ζ(5) is irrational*, 17 September 2026, Zenodo v1, 32 pages, [DOI 10.5281/zenodo.22826419](https://zenodo.org/records/22826419). Equation and page references in the preserved notes refer to this version. The source PDF's recorded SHA-256 is `a42c05ccc46b9a7c36428913453c4617202c59109713ba20f464ab9ec640d0da`. The original Appendix A numerical certificate was used as an input; the extension work did not independently rerun its complete 684-interval verification.

## Common construction for odd orders

For odd integers $s\geq3$, let $H_j^{(s)}=\sum_{v=1}^jv^{-s}$. The functional must change with the order. Substituting $\zeta(7)$ into the old fifth-order functional does not give the intended positive moment functional.

$$
\mu_s(t^e)=\frac{(-1)^e B_{2e+2}}{(s-1)!}
                 \prod_{r=3}^{s}(2e+r),\qquad
\mu_{s,X}\!\left(\frac1{t+j^2}\right)
=j^{s-1}(X-H_j^{(s)})-\frac1{s-1}+\frac1{2j}.
$$

Polynomial division and simple partial fractions extend these definitions uniquely to the rational-function domain. At $X=\zeta(s)$, the positive representation is

$$
\mu_{s,\zeta(s)}(R)=\int_0^\infty R(y^2)w_s(y)\,dy,\qquad
w_s(y)=\frac{2(2\pi)^{s-1}y^s}{(s-1)!}
       \sum_{\ell\geq1}\ell^{s-1}e^{-2\pi\ell y}>0.
$$

The moments follow from a gamma integral and Euler's even-zeta formula. The pole identity has two derivations in `algebra_notes.txt`: a direct hyperbolic-cotangent calculation and an integration-by-parts transfer using Hermite's Hurwitz-zeta formula. For the latter, $s-1$ integrations by parts replace the original four; the boundary products vanish. Supporting identities are [DLMF 25.6.2](https://dlmf.nist.gov/25.6.E2) and [DLMF 25.11.29](https://dlmf.nist.gov/25.11.E29).

Keep $K=40n$, $N=3n$, $h=37n$, and $D_m(t)=\prod_{j=1}^m(t+j^2)$. With

$$
G_{s,K}(X)_{ij}=\mu_{s,X}\!\left(\frac{D_N(t)^6t^{i+j}}{D_K(t)}\right),
\quad 0\leq i,j<h,
\qquad \Delta_{s,K}(X)=\det G_{s,K}(X),
$$

the matrix at $\zeta(s)$ is a positive definite Gram matrix. It introduces no other odd zeta values. Its leading coefficient is

$$
[X^h]\Delta_{s,K}(X)=(-1)^{h(h-1)/2}
       \prod_{j=N+1}^{K}j^{s-1}D_N(-j^2)^5\ne0.
$$

Thus the degree is exactly $h$. The changed pole factors do not destroy positivity or degree.

The transformed functional makes the arithmetic change transparent:

$$
\tau_s(P)=\frac{L(P^{(s-2)})}{(s-1)!},\quad L(x^k)=B_k,
\qquad \mu_{s,X}(R)=\tau_{s,X}(x^sR(-x^2)).
$$

The pole prescription is $\tau_{s,X}((x-r)^{-1})=H_{d(r)}^{(s)}-X$, where $d(r)=r$ for $r\geq0$, and $-r-1$ otherwise. Reflection stays odd. For functions regular at zero, the translation difference is the $(s-1)$-st Taylor coefficient at zero. The distribution factor becomes $p^{-(s-1)}$, explaining the extra loss in ordinary residue classes; at the zero class, the extra powers in $x^s$ compensate.

## What the zeta(7) audit established

The detailed source is the 11-page `output/zeta7_argument_audit.pdf`, supported by `algebra_notes.txt`, `arithmetic_notes.txt`, and exact Python checks.

1. **Normalization factors matter.** The correct first moment is $\mu_7(1)=7/12$, not $7/6$. The pole value is $j^6(X-H_j^{(7)})-1/6+1/(2j)$.
2. **The copied local bound is false.** At $K=40,N=3,p=29$, the old bound predicts $v_{29}(\Delta_{7,40}(0))\geq-60$, whereas its exact value is $-82$. Rational Gaussian elimination and modular elimination with tracked precision agree. Integrality concerns every coefficient, so a constant-coefficient counterexample is decisive for this copied bound.
3. **Not every arithmetic term worsens.** For $p\geq7$, Bernoulli-factor cancellation makes $\mu_7(t^e)$ integral for $e<3p-4$, improving the fifth-order cutoff $e<2p-3$. The polynomial correction rank improves to $\max(0,K+4N-3p+3)$. This gain is included in the revised budget.
4. **There is a small-prime exception.** The far-pole correction satisfies $C_{p,7}\in p^7\mathbb Z_p$ for $p\geq11$, but $v_7(C_{7,7})=6$. Treating 7 among the small primes avoids confusing this fixed exception with the asymptotic obstruction.
5. **The real bound survives at leading order.** With the same $D_N^6$, scalar $S_K$, comparison measure and source numerical certificate, the transferred derivation gives
   $$
   0<F_{7,K}(\zeta(7)),\qquad
   \log F_{7,K}(\zeta(7))\leq UK^2+26K\log K+200K,
   \quad U=-2733991/2000000.
   $$
   The extra polynomial factor in the positive weight changes lower-order terms, not the quadratic constant.
6. **The corrected arithmetic loses the final sign.** Ordinary inner classes add $2\lambda(1/3-1/M)$, the small-prime range adds $2\lambda/M$, and the outer range adds $1387/3840$, where $\lambda=37/40$. Their sum is exactly $751/768$. At cutoff $M=200$, the combined coefficient changes from $-0.017407802258\ldots$ to $+0.960456781075\ldots$. A positive upper bound does not prove actual growth; it fails to provide the negative bound needed for the contradiction.

For a small illustration outside the asymptotic parameter restrictions, $K=2,N=0$ gives the integer polynomial

$$
144\Delta_{7,2}(X)=-9216X^2+13656X-4399.
$$

Its positive value at $\zeta(7)$, about $0.48139987525$, illustrates the mechanism but does not supply a sequence proving irrationality.

### Attempted repairs and their exact scope

Replacing $D_N^6$ by $D_N^8$ improves some local arithmetic. It also changes the scalar to

$$
S_8=\frac{(K!)^{2h}4^{h-1}}
 {(N!)^{16h}\prod_{i=1}^{h-1}((2i)!)^2}
$$

and changes the external field, so keeping the old real constant without recalculation is invalid. Exact integration gives the proposed arithmetic coefficient $A_{8,200}=1.723096570942415\ldots$. At $t=3/4$, rational interval arithmetic gives a lower witness for the best possible upper-bound coefficient obtainable from the **original comparison measure**, original parameters and specified arithmetic certificate:

$$
[1.305909182511730956,\ 1.305909182511731277].
$$

Thus that particular repair cannot close the budget even with a perfect potential supremum bound. It does not exclude another measure, different parameters, or stronger coefficient-content estimates.

For the original $D_N^6$ transfer, exact finite integration over 1430 rational intervals sharpens the arithmetic coefficient to $2.323379348180366491\ldots$. The same single-point method then bounds the combined certificate coefficient below by a number in

$$
[0.949462611584646939,\ 0.949462611584647235].
$$

Improving only numerical enclosures of this measure and these local estimates cannot repair the sign. Both single-point checks are exact rational interval certificates, not numerical guesses for a supremum. The optional NumPy probes are exploratory and are not their proof inputs.

Fixed rational rescaling of the functional changes an $h$-dimensional determinant only at the $O(K)$ logarithmic scale; primitive integer normalization removes a scalar presentation change. A fixed rational affine change of $X$ preserves the polynomial Gauss valuation at all but finitely many primes. Neither operation removes the general large-prime obstruction. Parameter-dependent changes with growing denominators require separate analysis.

## Eisenstein series and the modulo-four question

The positive integration weight and the valuation row weights $w_{a,i}$ are different objects. The former contains $F_r(q)=\sum_{\ell\geq1}\ell^r q^\ell$, a building block in Eisenstein Fourier expansions. Summing over another lattice coordinate gives

$$
\sum_{m\geq1}F_{k-1}(q^m)=\sum_{n\geq1}\sigma_{k-1}(n)q^n.
$$

For example, $F_6(q)=q+64q^2+729q^3+\cdots$, while the extra sum starts $q+65q^2+730q^3+\cdots$. The full ordinary level-one lattice sum of odd weight vanishes by pairing opposite lattice points. This does not make the positive one-row kernel vanish. See [Stein, Fourier expansions of Eisenstein series](https://wstein.org/books/modform/modform/level_one.html#fourier-expansions-of-eisenstein-series).

The first Eisenstein answer was incomplete: odd zeta values also occur in periods or integrals of **even-weight** Eisenstein series. For $\zeta(s)$, this connection uses weight $s+1$. At $\tau=i$, the transformation's zeta term has factor $1-i^{s-1}=1-(-1)^{(s-1)/2}$.

| Value | Even-weight series in the period connection | Factor at $i$ |
|---|---|---:|
| $\zeta(5)$ | $E_6$ | 0 |
| $\zeta(7)$ | $E_8$ | 2 |
| $\zeta(9)$ | $E_{10}$ | 0 |

This is a genuine modulo-four distinction for that specialization, not an obstruction to the positive moment representation or an irrationality result. See [Berndt–Straub, Ramanujan's Formula for ζ(2n+1)](https://arminstraub.com/downloads/pub/ramanujanzeta.pdf), Theorem 1.1, equation (1.2), equation (2.13), and Section 5, equation (5.4).

## The zeta(9) formal analogue

The later 30-page draft covers Sections 1–7 and Appendices A–C of the same source paper. It retains $D_N^6$, $K=40n,N=3n,h=37n$, and $S_K$. Its four status labels must travel with the text: **Derived**, **Formal analogue**, **Conditional**, and **Blocked conclusion**. In particular, the inner analytic transfer remains formal; exact calculations of its proposed budget do not verify that missing input.

Key substitutions include $\tau_9(P)=L(P^{(7)})/8!$, distribution factor $p^{-8}$, pole coefficient $j^8$, and positive weight

$$
w_9(y)=\frac{(2\pi)^8y^9}{20160}
        \sum_{\ell\geq1}\ell^8e^{-2\pi\ell y}.
$$

The finite example at $K=40,N=3,p=29$ gives constant-coefficient valuations $-60,-82,-104$ for orders 5, 7, 9 respectively. The ninth-order value passed both exact rational and modular calculations. Sharing the residue class $1\pmod4$ with 5 does not recover the old denominator bound.

The later draft extends this finite observation to a **proposed, conditional asymptotic certificate**:

$$
A_{9,M}=A_{5,M}+\frac{116581}{57600},\qquad
R_9(x)=R_5(x)+4\lambda x.
$$

Exact arithmetic checks reproduce an outer increment $45541/57600$, the revised finite inner integral, and the total increment. The combined coefficients are

| Cutoff $M$ | $A_{9,M}+U$ |
|---|---:|
| 200 | $2.006567892186\ldots$ |
| 100000 | $1.974551870160\ldots$ |
| Infinite-cutoff limit | $1.974487121353\ldots$ |

The real transfer retains $U$ and yields $UK^2+28K\log K+200K$, using the source comparison-measure certificate. The arithmetic estimate has remainder $o_M(K^2)$ at **fixed** cutoff. The explicit real remainder does not upgrade that arithmetic remainder to $O(K\log K)$, and comparing cutoff constants does not justify choosing $M$ as a growing function of $K$.

The last irrationality step remains conditional on a future negative budget. If an integral degree-$h$ polynomial sequence satisfied $0<Q_K(\zeta(9))\leq e^{-\varepsilon K^2}$, rationality $\zeta(9)=a/b$ would give positive integers $b^hQ_K(a/b)\to0$. The present bounds do not supply this decay.

Appendix C preserves a relative matrix perturbation calculation. With $B_K=G^{-1/2}([X]G)G^{-1/2}$, its proposed bound is $\|B_K\|\leq e^{\rho K}$, $\rho=6933/500=13.866$, using the source's strict numerical enclosure. The identity

$$
Q_K(\xi+\delta)=Q_K(\xi)\det(I+\delta B_K)
$$

would, together with the missing decay, exclude sufficiently good rational approximations with exponent $\nu>\rho\lambda/\varepsilon$. The source's exponent 260 is not established for this ninth-order construction. Primitive normalization passes existing upper bounds to the primitive polynomial but provides no new negative budget without an additional estimate for the removed content.

The earlier `zeta9_parity_notes.txt` says no full ninth-order budget had yet been established. That sentence describes the earlier finite-check stage. The subsequent draft supplies the conditional budget above; it still does not establish irrationality.

## Reproduction and retained artifacts

Preserve the original relative layout of the extension scripts: `experiments/main_measure_certificate.py` imports the root `arithmetic_exact_inner.py` and the sibling `single_point_certificate.py`; the latter reads the root `arithmetic_variant_results.json`.

From the retained extension artifact root, the core checks use standard-library Python:

```text
python experiments/exact_checks.py
python arithmetic_costs.py
python arithmetic_exact_inner.py
python experiments/single_point_certificate.py
python experiments/main_measure_certificate.py
```

`arithmetic_exact_inner.py` verifies the complete exact fraction in source equation (5.18), not only its decimal approximation. It regenerates the JSON used by the interval certificates. The first command checks fifth- and seventh-order examples; `experiments/zeta9_local_check.json` records the separate ninth-order check, reproducible by calling `matrix_affine(9,40,3)` and both determinant algorithms in that module.

For the ninth-order exact budget, run `node zeta9_draft/checks/section5_exact.mjs`; its JSON output can be compared with `section5_exact_results.json`. This checks rational arithmetic, not the unverified analytic completion. To typeset the draft, run Tectonic or two `pdflatex` passes from `zeta9_draft/`. Its standard TeX dependencies need no shell escape or external images. The seventh-order `build_report.py` uses ReportLab and Windows Cambria fonts; those dependencies concern PDF reproduction, not the mathematical checks.

The original chat reported successful exact-check reruns and visual review of the reports. This consolidation preserves that provenance and the recorded results; it does not claim a new full proof audit or formal Lean/Isabelle verification.
