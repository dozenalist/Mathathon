# Viazovska’s proof of optimal sphere packing in dimension 8

This note explains the architecture of Viazovska’s proof that the (E_8) lattice gives the densest packing of equal balls in ℝ^8. It is aimed at readers who know analysis and algebra but have not studied sphere packing. The proof combines a general Fourier-analytic upper bound due to Cohn and Elkies with a highly structured function built from modular forms.

## 1. The packing and its target density

Scale so that packed balls have radius (1/2); then their centers must be at least distance (1) apart. Let Λ₈ be the (E_8) lattice normalized to have covolume (1) and shortest nonzero vector length √2. The lattice Λ₈ is even and unimodular: its squared vector lengths are even integers, and its dual lattice is itself.

The packing with centers Λ₈/√2 has minimum distance (1). Scaling a lattice by (1/√2) in dimension 8 scales its covolume by (1/16), so this packing has density

\[
\frac{\operatorname{vol}(B_8(1/2))}{1/16}
=16\frac{\pi^4}{6144}
=\frac{\pi^4}{384}.
\]

The theorem says every packing, including nonlattice packings, has density at most this number. Since the (E_8) packing attains it, it is optimal.

## 2. The Cohn–Elkies bound

Cohn and Elkies’s key observation is that one can certify an upper bound for every packing by finding a suitable test function. In the radius-(1/2) normalization, it is enough to find an admissible function (f:\mathbb R^8\to\mathbb R) such that

\[
f(x)\le 0 \quad (|x|\ge 1),
\qquad \widehat f(t)\ge 0 \quad (t\in\mathbb R^8).
\]

Then

\[
\text{packing density}\le
\operatorname{vol}(B_8(1/2))\,\frac{f(0)}{\widehat f(0)}.
\]

Here admissibility is a decay condition ensuring the sums and Poisson summation below converge. One may average (f) over rotations, so it suffices to use radial functions.

Here is the pair-sum argument. First take a periodic packing whose centers are the union of (N) translates (v_1,\dots,v_N) of a lattice \(\Lambda\), and normalize the minimum center separation to (1). Sum (f(x+v_j-v_k)) over lattice translations (x\in\Lambda) and pairs (j,k). On the spatial side, the diagonal terms contribute (Nf(0)). Every off-diagonal term is evaluated at distance at least (1), so is nonpositive. Thus the whole sum is at most (Nf(0)).

Poisson summation rewrites the same sum as

\[
\frac{1}{|\Lambda|}\sum_{t\in\Lambda^*}\widehat f(t)
\left|\sum_{j=1}^N e^{2\pi i\langle v_j,t\rangle}\right|^2.
\]

Every term is nonnegative. Keeping just the (t=0) term gives a lower bound (N^2\widehat f(0)/|\Lambda|). Comparing the two sides yields the density bound. Periodic packings approximate the supremal packing density, so this proves the bound for general packings as well.

### Why this is linear programming in spirit

A linear program has feasible objects one wants to optimize, and a dual feasible solution certifies an upper bound on every feasible object. Here the packing is the object being optimized, while (f) is the certificate: its spatial sign and Fourier sign force the pair sum to lie between two quantities, giving an upper bound on density. Finding the best such (f) is analogous to optimizing a dual solution. This is an analogy rather than a finite-dimensional LP: the certificate is a function and the packing constraints are geometric.

## 3. What sharpness requires

It is convenient to seek a radial Schwartz function (g) with

\[
g(x)\le0\quad (|x|\ge\sqrt2),\qquad
\widehat g(x)\ge0,\qquad
g(0)=\widehat g(0)=1.
\]

Set (f(x)=g(\sqrt2 x)). Then (f\le0) outside radius (1), and scaling the Fourier transform gives \(\widehat f(0)=2^{-4}\widehat g(0)=1/16\). Thus \(f(0)/\widehat f(0)=16\), and the Cohn–Elkies bound is exactly \(\pi^4/384\), the (E_8) density.

The lattice itself tells us what zeros such a sharp function should have. Poisson summation on the self-dual lattice \(\Lambda_8\) gives

\[
\sum_{\ell\in\Lambda_8}g(\ell)=
\sum_{\ell\in\Lambda_8}\widehat g(\ell).
\]

The tail sign of (g) makes the left side at most (g(0)=1); nonnegativity of \(\widehat g\) makes the right side at least \(\widehat g(0)=1\). Therefore equality holds, forcing both functions to vanish at every nonzero lattice vector. Because the functions have fixed signs at those radii, these are double zeros. The squared (E_8) lengths are (2,4,6,\ldots), so the prescribed radii are \(\sqrt{2n}\).

## 4. Why modular forms can build the function

With the Fourier convention used in Viazovska’s paper, Gaussians transform by

\[
\mathcal F\left(e^{\pi i|x|^2z}\right)(y)
=z^{-4}e^{\pi i|y|^2(-1/z)}
\qquad (\operatorname{Im}z>0).
\]

Thus a radial function built as a contour integral of Gaussians against a function of (z) will have a controlled Fourier transform if that (z)-function transforms predictably under (z\mapsto-1/z). That transformation is the central symmetry of modular forms. The factor \(z^{-4}\) matches modular weight (4), a dimension-specific coincidence that is central to the dimension-8 construction.

The modular forms’ Fourier expansions in \(q=e^{2\pi iz}\), inserted into the Gaussian integrals, also create the required radial zeros. In the final formulas these appear through

\[
\sin^2\left(\frac{\pi r^2}{2}\right),
\]

which vanishes when \(r^2\) is a positive even integer. Modular symmetry and the Gaussian Fourier transform arrange the zeros and Fourier behavior together.

## 5. Viazovska’s construction

Viazovska constructs two radial Schwartz functions (a,b:\mathbb R^8\to i\mathbb R), each as explicit contour integrals of Gaussians against modular-form expressions. Their Fourier eigenvalues are opposite:

\[
\widehat a=a,\qquad \widehat b=-b.
\]

Both have double zeros at the (E_8) lattice radii beyond the minimal one. The form used for (a) comes from modular and quasimodular forms for the full modular group. The form used for (b) uses theta functions and a level-two modular form. The transformation laws of these forms are chosen so that the Gaussian-transform identity makes (a) and (b) Fourier eigenfunctions.

The desired function is the following precise linear combination:

\[
g(x)=\frac{\pi i}{8640}a(x)+\frac{i}{240\pi}b(x),
\qquad
\widehat g(x)=\frac{\pi i}{8640}a(x)-\frac{i}{240\pi}b(x).
\]

Although (a) and (b) are purely imaginary on real radii, the factors of (i) make (g) and its Fourier transform real. The coefficients are tuned so that both functions have value (1) at the origin, and so that the signs required by the linear programming bound hold.

## 6. Verifying the signs

The modular-form formulas can be reorganized as Laplace transforms. For (r>\sqrt2),

\[
g(r)=\frac{\pi}{2160}\sin^2\left(\frac{\pi r^2}{2}\right)
\int_0^\infty A(t)e^{-\pi r^2t}\,dt,
\]

and for (r>0),

\[
\widehat g(r)=\frac{\pi}{2160}\sin^2\left(\frac{\pi r^2}{2}\right)
\int_0^\infty B(t)e^{-\pi r^2t}\,dt.
\]

The exponential and squared-sine factors are nonnegative. It therefore suffices to prove

\[
A(t)<0,\qquad B(t)>0\quad (t>0).
\]

This is the technically delicate sign check. The paper uses modular transformations and Fourier expansions to obtain rapidly convergent series near (t=0) and (t=\infty), plus explicit bounds on the omitted tails from estimates on modular-form coefficients. It then reports interval-arithmetic checks that the truncated expressions have the stated signs and dominate those tail bounds on the two ranges \((0,1]\) and \([1,\infty)\). This establishes the inequalities on the entire positive axis, not just numerically sampled values. The paper gives the expansions, error bounds, and interval-check claims in its final section.

## 7. Conclude optimality and periodic uniqueness

The sign checks establish the hypotheses of the Cohn–Elkies bound, and the normalization gives the exact bound \(\pi^4/384\). Since the scaled (E_8) lattice attains that density, it is optimal among all packings.

There is also rigidity in the equality case. Equality forces pairwise differences between centers to lie at zeros of the certificate, so their squared lengths are even integers. These distance constraints make the group generated by the centers an even integral lattice. The density forces it to be unimodular, and the even unimodular lattice of rank eight is (E_8). This yields uniqueness among periodic packings of maximal density.

## References

- Maryna Viazovska, [“The sphere packing problem in dimension 8,” *Annals of Mathematics* 185 (2017), 991–1015](https://annals.math.princeton.edu/2017/185-3/p07). [arXiv version](https://arxiv.org/abs/1603.04246).
- Henry Cohn and Noam Elkies, [“New upper bounds on sphere packings I,” *Annals of Mathematics* 157 (2003), 689–714](https://annals.math.princeton.edu/wp-content/uploads/annals-v157-n2-p09.pdf).
