# Roadmap: a sharp packing bound in three dimensions, Cohn–Elkies style

Companion to `Literature/sharp-bounds-in-dimension-3.md` (the study, with numbers and proofs)
and to `Literature/hales-2005-proof-summary.md` (the architecture that actually works).

The conclusion of the study, in one line: **no single-function (two-point, Cohn–Elkies-type)
linear-programming certificate can be sharp in $d=3$ — that is Li's theorem, and it has an
arithmetic explanation, $A_3$ being the first extremal lattice that is not isodual — so a sharp
$d=3$ bound must be *local*, and the $d=3$ analogue of "find the magic function" is "find the
score on decomposition stars".**

The tasks below are ordered by (expected value)/(effort), with a success criterion each.
Everything is stated so that a negative result is also a result.

## T1. Certify the $d=3$ LP value (weeks; mostly bookkeeping)

My computation gives the LP value as $1.48920$ (normalisation: minimal distance 1, centre
density); CE's $m=6$ construction gives the rigorous upper bound $1.48928$; Li's dual bound gives
$>1.471847$. Make the gap rigorous from below by a Sturm argument: the optimal certificate has
$f(r)=e^{-\pi r^2}P(2\pi r^2)$, $\widehat f(s)=e^{-\pi s^2}Q(2\pi s^2)$ with $P,Q$ of degree 31 and
rational coefficients (take the LP solution, round $c$ to rationals with denominator $10^{12}$,
rescale); then "$f\le0$ on $[1,\infty)$" and "$\widehat f\ge0$ on $[0,\infty)$" are univariate
polynomial sign conditions, decidable exactly (Sturm/Descartes). That turns $1.48920$ into a
certified bound and shows CE 2003 was within $10^{-4}$ of optimal.

*Success criterion:* a rational certificate with a Sturm transcript, i.e. a rigorous
$\mathrm{LP}_3\le1.4892$ (and $\ge1.4718$ from Li), pinning the LP value to two decimals.

## T2. The local inverse problem: find the score (the real target)

Take Hales' Q-system/decomposition-star marking as given (Ch. 4–7 of the 2005 volume), but treat
the score as an unknown:

* parametrise $\sigma(D)=\sum_{\text{features}}\lambda_{\text{feature}}\,\Phi_{\text{feature}}(D)$
  over a basis of local functionals (volume of the Voronoi region in $D$, face areas, solid
  angles, edge lengths, $\mathrm{pt}$-normalised tetrahedron scores);
* impose the equality conditions: $\sigma(\text{FCC star})=\sigma(\text{HCP star})=8\,\mathrm{pt}$,
  regular tetrahedron of edge 2 scores $1\,\mathrm{pt}$, flat square of side 2 scores $0$;
* solve the resulting LP (or SDP) for $\lambda$ subject to $\sigma(D)\le8\,\mathrm{pt}$ on a
  discretisation of star space; then certify on the complement by interval arithmetic.

This is the exact analogue of "solve for the weight-$(-2)$ modular form from the forced zeros",
and it is *not* excluded by Li's theorem because the score is a local object.

*Success criterion:* a re-derivation of Hales' local bound $\max_{D}\sigma=8\,\mathrm{pt}$ by a
systematic search rather than by hand. *Failure mode worth publishing:* if the LP is infeasible for
every natural basis, the local bound needs a genuinely nonlinear ingredient — that would explain
why Hales' local analysis is as hard as it is and would redirect the search.

## T3. Beat the dodecahedral bound $1.441366$ (the real record)

The best bound in $d=3$ after Kepler is *not* Fourier: it is the dodecahedral inequality
(Hales–McLaughlin, JAMS 2010), $\delta\le1.441366$, i.e. $1.9\%$ above $\sqrt2$. The Fourier
records are $1.471112$ (three-point) and $1.489207$ (two-point). So the frontier is a *local*
one, and the natural next step is a **cluster** version of it: an inequality over two or three
adjacent Voronoi cells and their shared facet (a small LP over cell shapes), instead of the
single-cell volume bound. Hales' Kepler proof uses precisely this "average over clusters"
mechanism; the question is how much of the $1.9\%$ window two-cell inequalities can close.

A hard constraint, proved by swarm member m6 (and rechecked here): every *per-point volume*
certificate is capped at $1/V_{\mathrm{dod}}=1.4413658597$, because the periodised 13-point
icosahedral cluster has a Voronoi cell of volume $0.6937864<1/\sqrt2$. So the cluster inequality is
not an optimisation of the dodecahedral method — it is the *only* way forward in the local family,
and the cap must be beaten by averaging over several cells, not by a better single-cell bound.

*Success criterion:* a certified $\delta_3<1.441366$ other than Kepler's theorem itself — that
would be the best known bound in dimension three, and the first one to improve on classical
Voronoi geometry.

## T4. An analytic proof of non-sharpness in $d=3$ (removes the computer)

Li's $d=3$ non-sharpness proof is a $7000$-digit rational dual certificate. An analytic proof
would come from the modular side: show that any Gaussian superposition
$F=\int_C\varphi(z)G_z\,dz$ with $\varphi$ of weight $1/2$ modular for $\tau:z\mapsto-1/z$ produces
$F$ and $\widehat F$ vanishing on the *same* radius family, hence can satisfy at most one of the two
zero conditions forced at FCC (the families differ: $3\in\mathcal S(A_3)\setminus\mathcal S(A_3^*)$,
$\tfrac32\in\mathcal S(A_3^*)\setminus\mathcal S(A_3)$). This is the same program
de Courcy-Ireland–Dostert–Viazovska are running for $d=6$.

*Success criterion:* a proof that no weight-$1/2$ modular Gaussian superposition is a sharp
certificate at $A_3$; combined with T1 and a density argument for the rest of the space, an
analytic non-sharpness theorem.

## T5. Sharpen the three-point bound at FCC

The three-point equality system at FCC is a finite system (kernel vanishing on triple differences,
sign conditions, normalisation). Determine whether it has a solution at all: if not, three-point
bounds can never be sharp in $d=3$ either, and the hierarchy must be pushed to four points or
localised — a useful negative result.

*Success criterion:* either an explicit solution (then a plausible route to sharpness), or an
obstruction with a proof.

## What not to do

* Do not search for a "magic function" $f$ for the Cohn–Elkies LP in $d=3$: it does not exist
  (Li), and adding the forced zeros makes the bound worse, not better (measured: $1.489\to1.53$–$1.76$).
* Do not try to transplant the $d=8$ modular construction: the Fricke involution has nothing to
  close on, because $A_3$ is not similar to $A_3^*$ ($12$ versus $8$ minimal vectors).
* Do not look for a pointwise Voronoi-volume inequality: individual cells can be smaller than
  $1/\sqrt2$; the truth is an average statement.
