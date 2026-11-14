# Angular harmonic lifts of radial Fourier functions

Angular harmonics give a concrete way to reuse radial Fourier constructions in
other dimensions while retaining the angle between two vectors in dimension 4.
They also expose a restriction: one nonconstant angular sector, however flexible
its radial coefficient, cannot produce an exact $D_4$ certificate.

The Fourier identities below are classical. Their application and the small
angular diagnostics are deductions for this feasibility study, not claims of
new theorems in the literature. No global packing certificate is constructed.

## 1. The dimension shift

For $x,y\in\mathbb R^4$, put $r=|x|$, $s=|y|$, and $c=(x\cdot y)/(rs)$
when $rs>0$. The Gegenbauer polynomials appropriate to the three-sphere are
$C_\ell^1(c)=U_\ell(c)$, the Chebyshev polynomials of the second kind. Define
the polynomial

$$
Z_\ell(x,y)=(rs)^\ell U_\ell(c).
$$

It extends across the axes and is homogeneous harmonic of degree $\ell$ in
each vector separately. In Gram variables it obeys

$$
Z_0=1,\quad Z_1=2t,\quad
Z_{\ell+1}=2tZ_\ell-uvZ_{\ell-1}.
$$

For example,

$$
Z_2=4t^2-uv,
$$

$$
Z_6=64t^6-80uvt^4+24u^2v^2t^2-u^3v^3.
$$

Let $\mathcal F_n a$ denote the radial Fourier transform in dimension $n$ of
the radial function with profile $a(r)$, with the $e^{-2\pi i x\cdot\xi}$
convention. For smooth rapidly decreasing radial profiles, Bochner's identity
gives

$$
\mathcal F_{\mathbb R^4\times\mathbb R^4}
\big[Z_\ell(x,y)a(r)b(s)\big](\xi,\eta)
=(-1)^\ell Z_\ell(\xi,\eta)
(\mathcal F_{4+2\ell}a)(|\xi|)
(\mathcal F_{4+2\ell}b)(|\eta|).
$$

Apply the one-vector harmonic identity twice: each transform contributes
$(-i)^\ell$, and each uses radial dimension $4+2\ell$.
[Stoller, *Fourier interpolation from spheres*, §2, Proposition 2.1(iii)](https://arxiv.org/html/2002.11627).

Independent sign symmetry of $x$ and $y$ permits only even $\ell$.

| Angular degree $\ell$ | Effective radial dimension $4+2\ell$ |
|---:|---:|
| 0 | 4 |
| 2 | 8 |
| 4 | 12 |
| 6 | 16 |
| 10 | 24 |

Thus radial Fourier eigenfunctions in dimensions 8 and 24 can be lifted into
angular building blocks for this dimension-4 problem. This is different from
making the entire eight-variable function radial, which is impossible at the
required normalization.

If $a,b$ have Fourier eigenvalues $\varepsilon_a,\varepsilon_b$ in the
effective dimension, the lifted block has eigenvalue
$(-1)^\ell\varepsilon_a\varepsilon_b$. Symmetrizing the radial factors in
$r,s$ preserves the desired swap symmetry.

## 2. What an angular modular expansion would need

A possible class has the form

$$
f(x,y)=\sum_{\ell\in2\mathbb Z_{\ge0}}Z_\ell(x,y)
\sum_{j,k}a_{\ell jk}\,\psi_{\ell j}(|x|)\psi_{\ell k}(|y|),
\qquad a_{\ell jk}=a_{\ell kj},
$$

where the $\psi_{\ell j}$ have explicit radial transforms in dimension
$4+2\ell$. Finite or infinite collections of modular functions, interpolation
basis functions, and their suitable radial combinations are candidates for the
profiles. Infinite sums require a topology of convergence that preserves
Schwartz regularity and permits termwise Fourier transformation.

The coefficient matrices are symmetric, but should not automatically be
required to be positive semidefinite. With the zonal addition formula, that
extra restriction would make $f(x,y)$ a positive-semidefinite kernel and
fall under the kernel obstruction. The needed positivity is pointwise
nonnegativity of the full Fourier transform; cancellation between angular
sectors is allowed.

This describes a function class to investigate, not a claim that suitable
coefficients exist. Several constraints remain:

* Every sector with $\ell>0$ vanishes on the axes, as does its Fourier
  transform. The $\ell=0$ part must supply the entire origin normalization,
  axis data, and integral. Higher sectors can change signs away from the axes.
* Known shell zeros in dimensions 8 and 24 do not automatically match both
  $D_4$ and $D_4^*$: their squared lengths occur at even integers and integers,
  respectively. Dilation changes spatial and Fourier scales reciprocally.
* A Fourier eigenfunction identity does not imply Fourier nonnegativity.
  Different sectors must cooperate to establish both global signs.
* Fixing finitely many angular sectors is different from a finite
  polynomial–Gaussian expansion. Nonpolynomial radial profiles may avoid that
  elementary obstruction, but face the angular restrictions below.

## 3. One nonconstant angular sector is insufficient

Suppose a candidate has the form, for $r,s>0$,

$$
f(x,y)=A(r,s)+B(r,s)U_{2k}(c),\qquad k\ge1,
$$

and extends smoothly across the axes. Let

$$
c_k=\sin\frac{\pi}{2(2k+1)}\in(0,1/2].
$$

This is a zero of $U_{2k}$, since
$U_m(\cos\theta)=\sin((m+1)\theta)/\sin\theta$.
For any $r,s\ge r_0=\sqrt2$, vectors with cosine $c_k$ satisfy

$$
|x\pm y|^2\ge r^2+s^2-rs
=(r-s)^2+rs\ge r_0^2.
$$

The sign condition at these vectors therefore forces $A(r,s)\le0$ on the
entire product region $r,s\ge r_0$. The axis signs hold as well.

Independent rotation averaging of $f$ selects $A$. This averaging preserves
Fourier nonnegativity, the origin value, and the integral. Hence $A$ satisfies
the disjunctive-product bound with the same objective, which cannot beat the
ordinary two-point optimum. An exact $D_4$ certificate is impossible in this
class. The argument also excludes any collection of sectors sharing a zero
$c\in[-1/2,1/2]$.

In particular, neither an 8-dimensional lift alone nor a 24-dimensional lift
alone can repair an angle-independent base. At least two nonconstant sectors
without this common-zero obstruction are needed. Their presence is necessary
for this strategy, not sufficient.

## 4. An exact first-shell angular profile

For two shortest $D_4$ vectors, $u=v=2$ and the possible cosines are
$0,\pm1/2,\pm1$. Consider

$$
q(c)=c^2(c^2-1/4)(1-c^2)
=\frac{U_0(c)+2U_2(c)-U_6(c)}{64}.
$$

It vanishes at every one of those lattice angles. It is nonpositive on
$[-1/2,1/2]$ and positive on $1/2<|c|<1$, while vanishing on the exact
diagonal and antidiagonal. These are exactly the allowed signs on this
particular equal-radius slice.

For two independent uniform directions on the three-sphere, $c$ has density
$(2/\pi)\sqrt{1-c^2}$ on $[-1,1]$. Orthogonality of the $U_\ell$ gives

$$
\mathbb E[q(c)]=\frac1{64}>0.
$$

One can also verify it from
$\mathbb E[c^2]=1/4$, $\mathbb E[c^4]=1/8$,
and $\mathbb E[c^6]=5/64$.

This is a local example of how angular coupling escapes the no-angle
obstruction: the angular average can be positive even while all required
angles on this slice have the correct sign. It uses sectors $0,2,6$, whose
effective dimensions are $4,8,16$. It proves neither that a radial extension
exists nor that its Fourier transform could be nonnegative.

The direct combination $\ell=0,2,10$ has a different first-shell constraint.
Its evaluation matrix at $c=0,1/2,1$ is

$$
\begin{pmatrix}1&-1&-1\\1&0&-1\\1&3&11\end{pmatrix},
\qquad\det=12.
$$

Consequently a function using only these three sectors and satisfying all
first-shell zeros must have all three radial coefficients zero at this pair
of radii. The same holds on the first dual shell. This does not rule out the
entire class: a whole shell slice may vanish. It does reject guesses that
require nonzero coefficients there, and cautions against expecting the known
8- and 24-dimensional functions to fit automatically.

The exact polynomial identity, signs, moments, and evaluation determinant are
checked by [angular_profiles.py](../experiments/angular_profiles.py).

## 5. A stronger screen using positive angular quadrature

Let $E$ be the chosen set of nonconstant even angular degrees. Suppose a
probability measure $\nu$ supported in $[-1/2,1/2]$ satisfies

$$
\int U_\ell(c)\,d\nu(c)=0\qquad(\ell\in E).
$$

Every angle in this interval is allowed for every $r,s\ge\sqrt2$. Integrating
the sign inequalities against $\nu$ forces the angular constant coefficient
$A(r,s)$ to be nonpositive throughout the product region. Independent rotation
averaging then gives the same two-point obstruction as before.

For example, $\nu=(\delta_0+\delta_{1/2})/2$ annihilates both $U_4$ and $U_6$.
Thus degrees $0,4,6$ cannot give an exact certificate, even though $U_4$ and
$U_6$ do not have a common zero. More generally the same measure annihilates
every even degree congruent to $4$ or $6$ modulo $12$. Searching for such a
positive quadrature is a useful preliminary check before investing in radial
modular coefficients. Absence of this obstruction is not a feasibility proof.

## 6. What Fourier positivity adds on the first dual shell

An even polynomial angular profile is a polynomial in $w=c^2$. A nonzero
profile vanishing at $c=0,\pm1/2,\pm1$ has degree at least $6$ in $c$, because
it must be divisible by $w(w-1/4)(w-1)$. The primal profile above attains this
minimum.

For a nonnegative Fourier-side profile, the interior zero $w=1/4$ must have
even multiplicity. A nonzero profile therefore has angular degree at least
$8$. In particular, any angular cutoff at degree $6$ forces the entire first
dual-shell slice to vanish, which imposes additional radial interpolation
conditions rather than an immediate global contradiction.

One possible nonnegative local shape is

$$
\widetilde q(c)=c^2(c^2-1/4)^2(1-c^2)
=\frac{2U_0+3U_2+U_4-U_6-U_8}{256}.
$$

It has all required first-shell zeros, is nonnegative for $|c|\le1$, and has
continuous spherical mean $1/128$. The scripts verify this identity exactly.
There is no assertion that $\widetilde q$ is the Fourier transform of $q$:
these are separate angular slices, with no radial extension supplied.

There is a precise interpolation consequence. With angular cutoff $8$, any
nonzero nonnegative first-dual-shell profile satisfying these zeros is a
positive scalar multiple of $\widetilde q$: its degree-four polynomial in
$w$ is already exhausted by the required factors. Its coefficients in sectors
$0,2,4,6,8$ must therefore have ratio

$$
2:3:1:-1:-1.
$$

All five sectors are necessary for a nonzero slice at this cutoff. Omitting
any of them forces the whole slice to vanish. Similarly, a nonzero primal
profile at cutoff $6$ is a positive scalar multiple of $q$, with sector
ratios $1:2:-1$ in degrees $0,2,6$. These are conditional local uniqueness
statements, not restrictions on certificates with higher angular degree.

This suggests a concrete class for further testing: retain several coupled
sectors, such as $0,2,4,6,8$, and use radial transform-controlled profiles in
dimensions $4,8,12,16,20$. The first-shell shapes are compatible with this
choice, but the complete interpolation, tail behavior, and coupled Fourier
signs remain unresolved. Restricting ingredients to the solved packing
dimensions $8$ and $24$ is not supported by these local constraints.
