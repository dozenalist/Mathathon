# Exact D4 Fourier and interpolation diagnostics

This directory provides a small, reproducible starting point for the lattice
three-point problem. It checks Fourier algebra, enumerates the required lattice
zeros, and rules out some finite polynomial spaces using exact arithmetic. It
does **not** find an auxiliary function, optimize a semidefinite program, or
establish a new sphere-packing density bound.

A separate [inspection of the published solution](UPSTREAM_REPRODUCTION.md)
reconstructs its first-shell angular profile and axis integral from selected
archived SOS matrices. That high-precision floating calculation has its own
provenance, limits, and optional download commands.

Run with Python 3.10 or later; no external packages are needed:

```sh
python run_diagnostics.py
python verify_rank_witnesses.py
```

The generator writes its output beside itself and completes in a few seconds
on a typical desktop. The second command reads the saved witnesses without
modifying any files. Its assertions and computations use integers and
`fractions.Fraction`. The density comparison in `results.json` uses ordinary
floating-point arithmetic only for displaying published numerical evidence.

## Normalization and polynomial space

The Fourier transform uses the phase $e^{-2\pi i z\cdot\xi}$. Write

$$
U=\pi|x|^2,\qquad V=\pi|y|^2,\qquad W=\pi x\cdot y.
$$

The code represents

$$
f(x,y)=P(U,V,W)e^{-\pi(|x|^2+|y|^2)},\qquad x,y\in\mathbb R^4.
$$

The basis is invariant under swapping $U,V$ and replacing $W$ by $-W$.
Its `gram_degree` is the ordinary degree in $U,V,W$, hence half the Cartesian
degree in $x,y$. In Section 5.2 of
[Cohn–de Laat–Salmon](https://arxiv.org/html/2206.15373#S5.SS2), the numerical
parameter $d$ permits Gram degree $2d$. Their Table 6.2 entry $d=13$ must not be
identified with `gram_degree=13` here.

The Gaussian width is fixed to the displayed value. A rank result at this width
does not by itself give the same finite-degree result at arbitrary other widths.

## Exact Fourier action

On Gram polynomials in dimension $n$ define

$$
D=4U\partial_U^2+4V\partial_V^2+(U+V)\partial_W^2
  +4W(\partial_U\partial_W+\partial_V\partial_W)
  +2n(\partial_U+\partial_V).
$$

This is the Cartesian Laplacian in the variables $\sqrt\pi(x,y)$, written in
Gram coordinates. For a homogeneous polynomial $P_k$ of Gram degree $k$,

$$
\widehat{P_k e^{-\pi(|x|^2+|y|^2)}}
=\left((-1)^k\sum_{j=0}^k\frac{(-1)^j}{4^j j!}D^jP_k\right)
 e^{-\pi(|\xi|^2+|\eta|^2)}.
$$

The arguments of the polynomial on the right are
$\pi|\xi|^2,\pi|\eta|^2,\pi\xi\cdot\eta$. Linearity handles mixed degrees.
The formula follows by differentiating the Gaussian Fourier transform; the
sum terminates because $D$ lowers Gram degree by one. For example, at $n=4$,

$$
\mathcal F(U)=2-U,\quad
\mathcal F(W^2)=W^2-\tfrac12(U+V)+1,\quad
\mathcal F(UV)=UV-2(U+V)+4.
$$

`gram_fourier.py` implements this operator with rational coefficients. The
checks include Fourier involution in dimensions 1, 2, and 4; independent
Laguerre formulas; mixed harmonic examples; preservation of the symmetries;
and a separate Cartesian expansion using products of one-dimensional Hermite
formulas. They total 388 checks in addition to the lattice enumeration checks.

## Lattice and dual Gram data

The enumeration uses

$$
D_4=\{x\in\mathbb Z^4:\sum_i x_i\equiv0\pmod2\}.
$$

There are 409 vectors of squared norm at most 12, including the origin, with
shell counts $1,24,24,96,24,144,96$ at squared norms $0,2,4,6,8,10,12$.
The 167,281 ordered pairs give 101 distinct canonical Gram triples

$$
(u,v,t)=(\min(|x|^2,|y|^2),\max(|x|^2,|y|^2),|x\cdot y|).
$$

These triples identify pairs under simultaneous orthogonal transformations,
swapping, and sign changes. They are not a classification under the smaller
finite automorphism group of $D_4$. `ordered_pair_count` counts all ordered
pairs before these identifications.

Let $H=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$ and
$A=\tfrac12\operatorname{diag}(H,H)$. Then $A^TA=I/2$ and $AD_4=D_4^*$.
Thus the dual Gram triple corresponding to $(u,v,t)$ is $(u/2,v/2,t/2)$.
The script checks the scaling and integral dual pairings on all enumerated
pairs. The equality of lattices also follows exactly: $AD_4$ is contained in
$\mathbb Z^4\cup(\mathbb Z^4+(1/2)^4)$ and both have covolume $1/2$.

`d4_gram_shells.csv` contains these data, including Gram rank and whether all
four squared lengths $u,v,u+v-2t,u+v+2t$ are strictly larger than 2.

## Finite interpolation tests

An exact sharp certificate at the stated normalization must satisfy

$$
f(0,0)=1,\quad\widehat f(0,0)=4,\quad
f|_{D_4^2\setminus\{0\}}=0,\quad
\widehat f|_{(D_4^*)^2\setminus\{0\}}=0.
$$

These equalities are necessary consequences of equality in the Poisson bound.
They do not replace the global inequalities in that bound.

`finite_interpolation.csv` imposes only primal zeros, optionally with primal
first derivatives, and computes exact rational ranks in unscaled Gram
coordinates. Its `normalization_possible=True` means only that these particular
homogeneous linear constraints allow $P(0)=1$.

`fourier_interpolation.csv` also imposes dual zeros and both normalizations.
At a dual zero with a positive-definite Gram matrix, global Fourier
nonnegativity forces all three Gram partial derivatives to vanish. At a primal
zero, the code imposes these derivatives only if the Gram matrix is positive
definite and the four squared lengths are strictly larger than 2. These
conditions ensure that the point lies in the interior of the nonpositive
region and that the Gram map is a submersion. Boundary derivative conditions
are deliberately omitted.

There is a simple exact way to certify inconsistency without approximating
$\pi$. Let $N$ be the number of polynomial coefficients. All entries of the
augmented interpolation matrix $[M(\pi)\mid b]$ are rational polynomials in
$\pi$. The script substitutes the rational number 3 and computes the rank
exactly. If the augmented rank is $N+1$, some $(N+1)$-minor is a nonzero
rational polynomial. By the transcendence of $\pi$, it remains nonzero at
the actual value of $\pi$. Therefore

$$
\operatorname{rank}[M(\pi)\mid b]=N+1>
\operatorname{rank}M(\pi),
$$

so the actual interpolation system is inconsistent. This argument uses the
specialization only to certify a nonzero polynomial; it does not replace $\pi$
by 3 in the auxiliary function. A smaller specialized rank is reported as
`INCONCLUSIVE`, not as evidence of a feasible function.

Representative results are:

| Maximum Gram degree | Number of coefficients | Maximum primal squared norm | Necessary constraints used | Outcome |
| ---: | ---: | ---: | --- | --- |
| 2 | 5 | 2 | Primal and dual zeros, normalization | Inconsistent |
| 6 | 30 | 4 | Zeros, normalization, interior derivatives | Inconsistent |
| 9 | 70 | 6 | Zeros, normalization, interior derivatives | Inconsistent |
| 10 | 91 | 6 | Zeros, normalization, interior derivatives | Inconclusive |

The complete table contains 54 parameter/constraint combinations, with 24
inconsistency certificates. `rank_witnesses.json` records a full-size augmented
minor for each excluded case. `verify_rank_witnesses.py` independently checks
that these 24 minors have nonzero determinants modulo the prime 1,000,003.
This finite-field check confirms their nonvanishing over the rationals without
reusing the generator's rational row reduction. The finite-degree results are diagnostics for
interpolation design, not a claim that these familiar Gaussian polynomial
spaces have been excluded by new theory: the infinite set of necessary zeros
already excludes every finite degree by a simpler polynomial restriction
argument. Approximation by a sequence of increasing-degree polynomials
remains compatible with all these facts.

## A further global tail restriction

A nonzero feasible polynomial at the fixed isotropic Gaussian width must
have **odd** highest Gram degree. To see this, write $P_k$ for its leading
homogeneous part. Every fixed ray $(sx,sy)$ eventually enters the lattice
sign set: its zero linear combinations remain zero and its nonzero
combinations eventually have length at least $\sqrt2$. Consequently
$P_k\le0$ on the physical Gram cone. The leading Fourier term is
$(-1)^kP_k$, so Fourier nonnegativity implies $(-1)^kP_k\ge0$ on the same
cone. If $k$ were even, $P_k$ would vanish on the open set
$U,V>0$, $W^2<UV$, and hence would be the zero polynomial, a contradiction.

Thus the degree-10 interpolation result in the table is correctly
`INCONCLUSIVE` as a linear test, but a globally feasible polynomial of degree
at most 10 would have degree at most 9. The degree-9 exclusion consequently
also rules out a globally feasible candidate in the degree-10 space. More
generally, the allowed top degree $2d$ in the published parametrization must
cancel for any nonzero feasible polynomial. This observation concerns a
single fixed isotropic Gaussian; it is not an assertion about arbitrary
mixtures of different widths.

## Files and reproducibility

| File | Purpose |
| --- | --- |
| `gram_fourier.py` | Exact Gram polynomial operations and Fourier action |
| `run_diagnostics.py` | Deterministic checks and artifact generator |
| `verify_rank_witnesses.py` | Separate finite-field determinant verification |
| `results.json` | Summary, scope labels, and displayed numerical comparison |
| `d4_gram_shells.csv` | Enumerated primal and dual Gram data |
| `finite_interpolation.csv` | Exact primal-only rank tests |
| `fourier_interpolation.csv` | Exact finite Fourier-interpolation exclusions |
| `rank_witnesses.json` | Selected rows and nonzero modular determinants |
| `fourier_examples.txt` | Low-degree examples of the Fourier operator |
| `fetch_upstream_metadata.py` | Optional, explicitly enabled bounded archive downloads |
| `upstream_archive_index.json` | Published tar member offsets and source-file hashes |
| `inspect_published_slice.py` | High-precision reconstruction of the published D4 slice |
| `published_first_shell_slice.csv` | 201 samples of the reconstructed angular profile |
| `published_angular_sectors.csv` | Its coefficients in the $U_\ell$ basis |
| `published_slice_summary.json` | Provenance, normalization, axis integral, and precision checks |
| `published_first_shell_plot.tex` / `.png` | Reproducible PGFPlots figure |

The displayed comparison $0.616858175-\pi^2/16\approx7.90\times10^{-6}$ uses
the published Table 6.2 value; this script does not independently reproduce
that semidefinite optimization or its rigorous rounding verification.
