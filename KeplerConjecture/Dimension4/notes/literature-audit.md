# Dimension 4: independent literature and scope audit

Sources retrieved: 14 November 2026. This note distinguishes published results,
conjectures, recent author claims, and deductions made during this investigation.
It does not claim an exact auxiliary function or an unrestricted packing proof.

## Established starting point

Rupert Li's [*Dual Linear Programming Bounds for Sphere Packing via Discrete
Reductions*, Theorem 7.1](https://arxiv.org/html/2206.09876v3#S7) proves that the
ordinary four-dimensional Cohn–Elkies optimum, in **center-density units**, is
greater than `0.12914461`. The same section records a rigorous packing upper
bound `0.12891`, whereas the $D_4$ packing has center density $1/8$.
Consequently the scalar two-point method cannot be sharp even for the true
unrestricted packing optimum. Multiplication by the unit four-ball volume

$$
\operatorname{vol}(B_1^4)=\frac{\pi^2}{2}
$$

converts these center densities to packing fractions. Merely choosing a more
sophisticated scalar modular form does not evade this obstruction.

The relevant replacement is Cohn–de Laat–Salmon,
[*Three-point bounds for sphere packing*](https://arxiv.org/html/2206.15373),
specifically **Theorem 1.4 and Conjecture 6.1**, which concern **lattice**
packings. Their unrestricted theorem is Theorem 1.1 and has different hypotheses.
Table 6.2 gives the following rigorous lattice upper bounds:

| Degree | Dimension-4 bound |
|---:|---:|
| 4 | 0.663869735 |
| 5 | 0.653653322 |
| 6 | 0.637355636 |
| 7 | 0.624695218 |
| 8 | 0.619935194 |
| 9 | 0.617926232 |
| 10 | 0.617173341 |
| 11 | 0.616946076 |
| 12 | 0.616879313 |
| 13 | 0.616858175 |

These are published values, not computations rerun in this sprint. The limiting
target is $\pi^2/16$, approximately `0.616850275068`. Finite convergence
evidence does not prove that the infimum is sharp or attained by a Schwartz
function. Section 3 distinguishes dual attainment from unknown primal
attainment for the $C$-constrained program. Appendix A.1 does prove
continuous-integrable primal attainment for the ordinary two-point problem;
it does not give a Schwartz optimizer or solve the constrained case.
Remark 4.1 suggests genus-2 Siegel modular forms for
**dual** summation formulas after adding all coprime integer-combination
constraints; it does not construct a primal certificate.

**Transcription caution.** Both the HTML statement of Conjecture 6.1 and the
[PDF, p. 32](https://arxiv.org/pdf/2206.15373#page=32), omit origin exceptions in
the two lattice zero sets, contradicting the normalization.
The intended conditions must exclude $(0,0)$; this follows independently from
Poisson summation and is not an extra conjectural assumption.

## A concrete existing modular ingredient

Daniel Lautzenheiser's [*A note on Fourier eigenfunctions in four dimensions*,
Proposition 1 and concluding discussion](https://arxiv.org/html/2208.14534v3)
constructs a radial Schwartz Fourier $+1$ eigenfunction using

$$
\varphi(z)=\frac{\Theta_4(z)^{12}
 (\Theta_3(z)^{12}+\Theta_2(z)^{12})}{\Delta(z)}.
$$

For $r>\sqrt2$, its expression is

$$
f_+(r)=4\sin^2(\pi r^2/2)
\int_0^\infty\varphi(it)e^{-\pi r^2t}\,dt.
$$

The paper continues this expression to all radii and establishes eventual
nonnegativity with sign radius $\sqrt2$. Crucially, $f_+(0)=0$: it is
**not** itself positive definite, and hence is not a packing certificate. It is
explicitly proposed as a possible ingredient related to the lattice conjecture.
This supplies a real four-dimensional precedent for modular-function
exploration, while leaving the two-vector sign inequalities unresolved. This
audit relies on Proposition 1, not on an unchecked extension of every contour
formula in the paper to a Schwartz function.

The journal version is *Hardy–Ramanujan Journal* **45** (2022), 88–93;
[the publisher's PDF](https://hrj.episciences.org/10909/pdf) is a stable source
for the formulas.

## Deductions for choosing the function class

The following are deductions checked during this investigation, not claims of
new literature results or priority.

### Independent rotational symmetry is too restrictive

Suppose a feasible lattice function has the form

$$
f(x,y)=F(|x|^2,|y|^2).
$$

For any $u,v\ge2$, choose perpendicular vectors with squared norms $u,v$.
Then all four lengths in the lattice sign condition are at least $\sqrt2$,
so $F(u,v)\le0$. Since $F$ does not depend on the angle, this inequality
holds for all pairs with these norms. The axis constraints hold as well.

Thus, after rescaling the minimum distance, this function is feasible for the
disjunctive-product program. [Cohn–de Laat–Salmon, Proposition 4.7](https://arxiv.org/html/2206.15373#S4.SS1)
identifies its optimum as $\Delta_2(4)^2$. Taking the square root shows that
this restricted lattice method cannot improve the ordinary two-point optimum.
Li's strict separation therefore excludes an exact $D_4$ certificate in this
entire class. The conclusion applies even to nonseparable $F$, not only to a
single tensor product. **Angle dependence is necessary.**

### Full eight-dimensional radial symmetry is even more restrictive

If $f(x,y)=H(|x|^2+|y|^2)$, the axis constraint implies $H(s)\le0$ for
all $s\ge2$. Consequently $f$ is an ordinary eight-dimensional
Cohn–Elkies auxiliary function. Applying its bound to $E_8$, whose minimum
length is $\sqrt2$ and covolume is 1, forces

$$
\frac{f(0,0)}{\widehat f(0,0)}\ge1.
$$

The desired $D_4$ ratio is $1/4$, a contradiction. This also explains why
the ambient dimension $4+4=8$ does not permit simply reusing Viazovska's radial
eight-dimensional function.

### Simultaneous rotations retain the needed information

Under simultaneous $O(4)$ rotations, swap symmetry, and independent sign
changes, write

$$
f(x,y)=\Phi(u,v,t),\quad u=|x|^2,\ v=|y|^2,\ t=x\cdot y,
$$

where $\Phi(u,v,t)=\Phi(v,u,t)=\Phi(u,v,-t)$. Its domain is

$$
u,v\ge0,\qquad t^2\le uv.
$$

The integration formula, derived from polar coordinates, is

$$
\widehat f(0,0)=2\pi^3
\int_0^\infty\!\int_0^\infty
\int_{-\sqrt{uv}}^{\sqrt{uv}}
\Phi(u,v,t)\sqrt{uv-t^2}\,dt\,dv\,du.
$$

For the Gaussian $e^{-\pi(u+v)}$, this gives 1, checking the constant.
An angular expansion uses even Gegenbauer sectors $C_{2k}^{1}$; the previous
obstruction rules out keeping only the angle-independent sector.

### A matrix-Gaussian route retains the angle

For a real positive-definite symmetric matrix

$$
T=\begin{pmatrix}a&b\\b&c\end{pmatrix},
$$

define

$$
G_T(x,y)=\exp\{-\pi(a|x|^2+2b\,x\cdot y+c|y|^2)\}.
$$

Applying the two-dimensional Gaussian transform separately to the four
coordinate pairs gives

$$
\widehat G_T(\xi,\eta)=\det(T)^{-2}G_{T^{-1}}(\xi,\eta).
$$

The parameter $b$ retains angular information; setting $b=0$ throughout would
return to the blocked independently radial class. Averaging the parameters
$b$ and $-b$ enforces the allowed sign symmetry without eliminating all angular
dependence.

The transform suggests weights adapted to matrix inversion, but the
real-positive matrix class has a stronger obstruction than merely wrong
signs for positive weights. The [theory assessment](theory-assessment.md)
proves that **every** finite-total-variation mixture of these real Gaussians,
even with complex signed weights, is incompatible with exact $D_4$ shell
zeros and a nonzero origin value. The same holds with uniformly bounded
polynomial degree and finite coefficient measures. Its moment proof has
been independently checked in this audit. Thus exact constructions must
leave those hypotheses, for example through genuinely complex Gaussian
parameters, unbounded-degree expansions, or regularized representations.
Their Fourier nonnegativity still requires a separate global proof.

For a smooth, sufficiently decaying weight $w$ and Lebesgue measure $dT$ on
the three independent matrix entries, inversion has Jacobian
$d(T^{-1})=\det(T)^{-3}dT$. Thus the Fourier transform of
$\int w(T)G_T\,dT$ has weight
$w(T^{-1})\det(T)^{-1}$. This is an explicit functional equation to investigate;
it is not by itself a modular-form construction or a positivity result.

### Audit of the proposed harmonic lift from dimensions 8 and 24

The harmonic lift proposed in the main investigation follows from Bochner's
relation; see [Stoller, *Fourier interpolation from spheres*,
Section 2, Proposition 2.1(iii)](https://arxiv.org/html/2002.11627#S2),
*Transactions of the AMS* **374** (2021), 8045–8079,
[doi:10.1090/tran/8440](https://doi.org/10.1090/tran/8440).
For a degree-$\ell$ homogeneous harmonic polynomial $H_\ell$ on $\mathbb R^d$
and a radial Schwartz profile $a$ in dimension $d+2\ell$, the relation is

$$
\mathcal F_d[H_\ell(x)a(|x|)](\xi)
=(-i)^\ell H_\ell(\xi)
(\mathcal F_{d+2\ell}a)(|\xi|).
$$

Consequently, for

$$
Z_\ell(x,y)=(|x||y|)^\ell
C_\ell^1\left(\frac{x\cdot y}{|x||y|}\right),
$$

which extends polynomially across the axes and is separately harmonic,

$$
\mathcal F_8[Z_\ell(x,y)a(|x|)b(|y|)](\xi,\eta)
=(-1)^\ell Z_\ell(\xi,\eta)
(\mathcal F_{4+2\ell}a)(|\xi|)
(\mathcal F_{4+2\ell}b)(|\eta|).
$$

Thus the even sectors $\ell=2$ and $\ell=10$ genuinely use radial transforms
in dimensions 8 and 24. As a check, $Z_2=4(x\cdot y)^2-|x|^2|y|^2$.
This is a legitimate way to reuse Fourier-controlled profiles from the solved
dimensions as angular building blocks.

The audit does not establish their sufficiency. Every $\ell>0$ sector vanishes
on both axes, as does its Fourier transform, so the $\ell=0$ sector must carry
the two origin normalizations. The factors $Z_\ell$ change sign, so
Fourier nonnegativity of radial factors does not imply joint Fourier
nonnegativity. Finally, the even-integer squared-norm shells of $D_4$ and
integer squared-norm shells of $D_4^*$ differ: copying or rescaling an
eight-dimensional profile does not automatically enforce both zero sets.

### Exactness imposes a partition of unity

Put $L=D_4\times D_4$, of covolume $4$. For any exact Schwartz certificate,
the Fourier zero conditions and shifted Poisson summation yield

$$
\sum_{p\in L}f(p+a)=1\qquad(a\in\mathbb R^8).
$$

The corresponding physical zeros imply the dual identity

$$
\sum_{q\in L^*}\widehat f(q+b)=4\qquad(b\in\mathbb R^8).
$$

These are necessary consistency tests for a future interpolation construction.
They follow directly from the zero sets and normalizations, rather than
providing an independent way to produce the missing signs.

## What existing interpolation actually provides

[Cohn–Kumar–Miller–Radchenko–Viazovska, *Universal optimality of the
$E_8$ and Leech lattices and interpolation formulas*,
Section 1.4 and Theorem 1.7](https://arxiv.org/html/1902.05438#S1.SS4)
provide radial Schwartz interpolation bases in dimensions 8 and 24 using
values and radial derivatives of a function and its Fourier transform at
$\sqrt{2n}$, starting at $n=1$ and $n=2$, respectively. Consequently the
$\ell=2,10$ harmonic sectors have a substantial supply of explicit
Fourier-controlled profiles. The theorem reconstructs radial functions; it
does not assert existence of a pair function with the desired Gram-node data.

There are also radial interpolation constructions beyond these two dimensions.
[Bondarenko–Radchenko–Seip, *Fourier interpolation with zeros of zeta and
$L$-functions*, Theorem 3.1 and Section 3.4.1](https://arxiv.org/html/2005.02996#S3)
construct the modular integral machinery underlying such formulas.
The recent [Radchenko–Sun preprint, arXiv:2510.04873v2, Theorems 1.1–1.2
and Corollary 1.4](https://arxiv.org/html/2510.04873v2#S1)
gives explicit dimension-4 radial interpolation functions through
Maass–Poincaré series and real-variable Kloosterman sums. Corollary 1.4
identifies them with the Schwartz profiles from the earlier construction.
This is a useful source for the essential $\ell=0$ sector. It is analytic
progress, not a sphere-packing certificate.

Two cautions matter when using the all-dimensional results of Stoller.
Section 1.2 explicitly describes the nonradial theorem as a sampling
formula rather than free interpolation: arbitrary proposed sphere data need
not be realizable. Moreover, the high-dimensional Poincaré-series profiles
in that paper are generally **not** individually Schwartz; see Proposition
8.1. They cannot simply be inserted as finite Schwartz basis elements without
further decay analysis. One may instead choose the Schwartz families above.
If infinitely many angular sectors are used, uniform seminorm estimates in
the lifted dimension remain an additional requirement.

### Tensorization creates missing partial-transform data

Here is an elementary deduction explaining why existing radial formulas are
not yet the required two-vector interpolation theorem. In a fixed harmonic
sector, write $N=4+2\ell$ and regard $A(r,s)$ as a separately radial Schwartz
function on $\mathbb R^N\times\mathbb R^N$. Suppose a radial sampling formula is

$$
h(r)=\sum_m h(r_m)a_m(r)+
       \sum_m(\mathcal F_Nh)(r_m)\widetilde a_m(r).
$$

Applying it in each variable gives, with the usual convergence justification,

$$
\begin{aligned}
A(r,s)=\sum_{m,n}\big[
 &A(r_m,r_n)a_m(r)a_n(s)\\
 &+(\mathcal F_1 A)(r_m,r_n)\widetilde a_m(r)a_n(s)\\
 &+(\mathcal F_2 A)(r_m,r_n)a_m(r)\widetilde a_n(s)\\
 &+(\mathcal F_1\mathcal F_2 A)(r_m,r_n)
       \widetilde a_m(r)\widetilde a_n(s)\big].
\end{aligned}
$$

Here $\mathcal F_j$ is the $N$-dimensional radial transform in variable $j$.
Value-and-derivative formulas have analogous extra derivative channels.
The pair conjecture specifies spatial and **full** Fourier zeros, not the
two partial-transform channels. Furthermore, its zeros are at discrete
angles on each pair of shells, whereas extracting $A_\ell(r,s)$ requires
an angular projection using all angles. The available data couple harmonic
sectors instead of independently determining each sector.

Thus a meaningful research route is to use these explicit profiles as a
complete supply of ingredients and solve the coupled interpolation and
positivity problem. It is not legitimate to declare that tensorizing known
magic functions has solved that problem.

A related warning comes from [Radchenko–Stoller, *Fourier non-uniqueness sets
from totally real number fields*, Theorem 1 and Section 4](https://arxiv.org/html/2108.11828#S4).
They show that natural multivariate arithmetic square-root node sets can
admit infinitely many nonzero Schwartz Fourier eigenfunctions vanishing on
all nodes. Their attempted Hilbert-modular interpolation encounters genuine
higher-rank group-theoretic obstructions. Those node sets and groups are
different from the present Gram-node/Siegel problem, so this is **not** a
no-go theorem for Conjecture 6.1. It is evidence against assuming that a
multivariate modular interpolation theory follows formally from the
one-variable case.

### A limitation of copying the genus-1 construction literally

There is also a precise structural distinction between elliptic and Siegel
modular forms. For genus greater than one, Koecher's principle forces the
Fourier indices of a modular form holomorphic on Siegel upper half-space
to be positive semidefinite; no independent cusp-growth condition is needed.
See [van der Geer, *Siegel Modular Forms*, Theorem 4.4 and the preceding
definition, pp. 8–11](https://arxiv.org/pdf/math/0605346#page=8).
In the full-group setting stated there, a holomorphic genus-2 modular form
cannot have the cusp-only polar principal parts used by a genus-1
weakly holomorphic construction. This obstructs that literal template,
not genus-2 methods in general. Meromorphic forms with interior poles,
nonholomorphic modular objects, and appropriately regularized integrals
require separate investigation.

## Current-claim audit

Some September 2026 search results point to
[arXiv:2609.25120v2](https://arxiv.org/abs/2609.25120v2), whose abstract claims a
complete solution. However, the authors' [current repository
README](https://github.com/creelie/d4-voronoi-cells) explicitly lists optimality
of $D_4$ and the general 24-cell conjecture as **open**. It advertises restricted
results and an upper bound below `0.630996`; those computations were not audited
here. Accordingly, this sprint does not treat the old abstract as an established
solution.

The independent November 2026 preprint by Tomar,
[*The 24-cell conjecture in the all-contact case and near D4*, introduction,
pp. 2–3](https://hexagonmath.org/pdf/2611.00390v1), explicitly discusses the
narrower scope of the later draft and states results for special classes.
Its full proof and accompanying formalization were not checked here.
These geometric developments do not supply the exact Fourier certificate
sought here.

The [SpherePackingUpperBounds repository](https://github.com/alexlegeartis/SpherePackingUpperBounds)
advertises an unrestricted four-dimensional upper bound near `0.63343`.
This is likewise different from the exact lattice conjecture. A one-hour
feasibility study should neither call a historical 2022 upper bound the latest
bound nor promote every new repository assertion to an independently checked
theorem.

## Search scope and adjacent progress

Queries for the exact conjecture, its arXiv identifier with modular forms and
interpolation, and two-vector/genus-2 Fourier certificates did not locate a
checked solution of Conjecture 6.1. This is a bounded literature search, not
a proof that no relevant unpublished or less-indexed result exists.

A substantial adjacent result is de Laat–Leijenhorst–de Muinck Keizer,
[*Optimality and uniqueness of the $D_4$ root system*,
arXiv:2404.18794v2, Section 5.1](https://arxiv.org/html/2404.18794v2#S5.SS1).
Its exact semidefinite certificate proves uniqueness of the 24-point optimal
kissing configuration. This is a compact spherical problem, and the
second Lasserre level is stronger than the usual three-point spherical bound.
The result neither proves optimality of an infinite packing nor constructs
the lattice Fourier function, but it demonstrates that exact higher-order
certificates can capture four-dimensional root geometry.

The July 2026 preprint [Andrew Salmon, *Linear Programming Bounds for
Fibered Sphere Packings*, Theorem 11 and Section 4.2](https://arxiv.org/html/2607.25254v1)
studies a different, restricted problem with prescribed translational
symmetry. It gives an exact triangular auxiliary function for the
one-dimensional-base $D_4$-over-$D_3$ problem. Its $D_4$-over-$A_2$ problem
is conjectural and related to the planar linear program, which is stated
as unresolved in that July 2026 preprint.
These results are not a proof that arbitrary four-dimensional packings have
the required fibers, nor a solution of the two-vector lattice conjecture.
They do provide current examples of exact auxiliaries after restricting the
geometric class.

Later September 2026 manuscripts in [OpenAI's mathematical
release](https://github.com/openai/math) claim a sharp planar Fourier
certificate and triangular-lattice universal optimality. The repository
itself distinguishes differing verification stages. Those planar claims
and their accompanying formalizations were not audited in this sprint,
and no conclusion about their validity is needed for the dimension-4
obstructions proved here.

Henry Cohn's [*From sphere packing to Fourier interpolation*,
Section 2](https://arxiv.org/html/2407.14999#S2), published in *Bulletin of the
AMS* **61** (2024), 3–22, is useful exposition for the role of complementary
zeros and Fourier interpolation. It gives no two-vector interpolation formula
solving the present conjecture. The absence of such a formula in the checked
sources is one of the main analytic gaps in the proposed program.

## Audit conclusion

The promising problem is an exact, angle-dependent **lattice three-point**
certificate. The scalar two-point, independently radial two-vector, and fully
radial eight-dimensional classes are blocked. Existing modular eigenfunctions
are plausible ingredients but do not provide the required global positivity.
No checked source in this audit constructs the full conjectured function.
