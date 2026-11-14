# Computational assessment of the D4 lattice certificate

The numerical evidence for an exact lattice three-point certificate is
promising, but a finite Gaussian polynomial is an approximation space rather
than a possible exact endpoint. The calculations in
[the computation directory](../computation/README.md) make this distinction
concrete and provide exact Fourier and interpolation machinery for follow-up
work.

## Results obtained in this sprint

- Exact arithmetic verifies the Gram-coordinate Fourier operator against
  involution, Laguerre, harmonic, and independent Cartesian Hermite formulas.
  The run passes 388 algebra checks.
- Enumeration through squared norm 12 produces 409 D4 vectors and 101
  canonical Gram classes from 167,281 ordered pairs. The corresponding D4*
  classes are obtained by halving every Gram entry.
- The finite necessary interpolation equations exclude the fixed-width
  Gaussian polynomial space of Gram degree at most 9, already using shells
  through squared norm 6 together with appropriate stationary-zero
  conditions. The exclusion is an exact rank argument using a rational
  specialization and the transcendence of pi. Degree 10 remains inconclusive
  in this particular test; it is not globally feasible merely because this
  test does not exclude it.
- A separate determinant checker verifies all 24 saved augmented-rank
  witnesses modulo the prime 1,000,003, independently of the rational
  elimination used to generate the rank table.
- A bounded download of the authors' stored degree-13 D4 solution recovers
  its first-shell angular profile. At origin normalization one, its value at
  cosine 0.75 is about +0.00141895, while its angular average is about
  +0.000388739. These positive values occur in precisely the caps excluded
  from the lattice nonpositivity condition. The reconstruction agrees at 60
  and 90 decimal digits and reproduces the stored objective; it is inspection
  of floating-point data, not a rerun of the authors' rigorous verifier.

The scripts use only Python's standard library. The exact rank work does not
depend on a numerical optimizer or a floating-point rank tolerance. The
published-solution inspection has a separate scope label and its own
[provenance and reproduction instructions](../computation/UPSTREAM_REPRODUCTION.md).
Neither calculation gives a new upper bound.

There is also a useful analytic tail check. A nonzero feasible polynomial
times the fixed isotropic Gaussian must have odd highest Gram degree: the
leading term is nonpositive on every ray, while its Fourier leading term is
multiplied by $(-1)^k$. An even degree would force that leading polynomial to
vanish on the open Gram cone. Consequently global sign feasibility in degree
at most 10 reduces to degree at most 9, even though the degree-10 linear test
alone remains inconclusive. The computation README gives the full argument.

## Reading the published evidence correctly

[Cohn–de Laat–Salmon, Table 6.2](https://arxiv.org/html/2206.15373#S6.SS2)
gives a lattice upper bound 0.616858175 at parameter d=13. Its gap from
pi^2/16 is about 7.90e-6, or 12.81 parts per million of the target density.
Their parameter permits ordinary Gram degree 26 and Cartesian degree 52.
These published values are rigorous upper bounds; their apparent convergence
to the target remains numerical evidence for the exact conjecture.

The much smaller spaces used in this sprint do not reproduce that
optimization. Their purpose is to check formulas and identify the exact
zero/interpolation requirements before investing in a larger search.

## Most useful next computational step

Extend the present inspection to more radii and polynomial degrees, and run
the authors' interval verifier before interpreting exported coefficients as
certified. The archive contains only degree-13 lattice outputs; comparison
with other degrees requires further optimization or additional data. An exact function
will need an infinite-dimensional construction, such as a convergent series
or integral, with separately provable global signs. Finite coefficient
fitting should be used to discover that structure, not taken as proof of
positivity away from sampled points.

It would be useful to fit the exact duality under the D4 isodual map from the
start. The dual zero data contain no independent shell-enumeration problem:
they are precisely the same pair-Gram data scaled by one half. The difficult
part is imposing the Fourier relation and both global signs simultaneously.
