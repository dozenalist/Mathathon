# Claim ledger for the dimension-4 feasibility study

This ledger separates mathematical deductions, exact finite computations,
inspection of published numerical data, and research proposals. The deductions
are independently reviewed exposition; no claim of novelty or formal Lean
verification is made.

| Claim | Status and evidence | Scope |
|---|---|---|
| Ordinary four-dimensional Cohn–Elkies bounds cannot be sharp | Published theorem: [Li, Theorem 7.1](https://arxiv.org/html/2206.09876v3#S7) | Obstruction to the ordinary two-point method |
| The target $f(0)=1$, $\widehat f(0)=4$ would prove lattice density at most $\pi^2/16$ | Published framework plus displayed Poisson derivation in [report §2](REPORT.md#2-exact-certificate-and-normalization) | Lattice packings only |
| An exact certificate has both nonzero lattice zero sets | Derived directly from equality in Poisson summation | Necessary, not sufficient |
| Angle-independent functions, full eight-dimensional radial functions, and additionally PSD two-argument kernels cannot attain the target | Reviewed proofs in [theory note](notes/theory-assessment.md) | Distinct restrictions; full Fourier positivity is not kernel PSD in $(x,y)$ |
| No finite real polynomial–Gaussian expansion attains exactness | Reviewed lattice-ray proof, including finitely many real shifts | Does not prevent increasingly accurate approximations |
| Finite-total-variation centered real Gaussian integrals with uniformly bounded polynomial degree cannot be exact | Reviewed moment proof using all $D_4$ shell radii, [theory §2](notes/theory-assessment.md#2-exactness-excludes-every-finite-real-gaussian-expansion) | Includes complex weights; excludes genuinely complex Gaussian parameters and does not address nonabsolute regularizations or unbounded degrees |
| A base plus one nonconstant even angular sector cannot be exact | Reviewed safe-angle argument in [harmonic note](notes/harmonic-lift.md) | Arbitrary radial coefficients, not just Gaussian ones |
| Positive safe-angle quadrature excludes further angular families | Reviewed proof and exact examples | A sufficient obstruction, not a classification of viable families |
| Bochner lifting connects angular degree $\ell$ to radial dimension $4+2\ell$ | Classical identity, sourced and independently checked | Fourier transform control does not imply the packing signs |
| First-shell primal and dual angular profiles have the stated zeros, signs, and expansions | Exact rational algebra in [angular_profiles.py](experiments/angular_profiles.py) | Separate local profiles; not a Fourier-transform pair |
| 409 vectors and 101 canonical Gram classes occur through squared norm 12 | Exhaustive integer enumeration | Finite shells, under continuous rotational and stated discrete symmetries |
| The polynomial Fourier operator passes 388 checks | Exact rational checks, including an independent Cartesian formulation | Tests finite algebra, not all analytic hypotheses |
| Twenty-four finite interpolation systems are inconsistent | Rational rank plus saved minors independently checked modulo a prime | Fixed Gaussian width and stated finite degree/shell constraints |
| The fixed-width degree-at-most-10 class cannot meet the exact target | Degree-9 finite exclusion plus odd-leading-degree argument | A diagnostic consequence; all finite real Gaussian expansions already face the general exactness obstruction |
| Published $d=13$ lattice bound is $0.616858175$ | [Cohn–de Laat–Salmon, Table 6.2](https://arxiv.org/html/2206.15373#S6.SS2) | Published rigorous bound; its interval verification was not rerun |
| Stored $d=13$ output has the displayed positive angular cap and sector coefficients | Reconstructed at 60 and 90 decimal digits; source ranges and hashes recorded | Numerical inspection, not certified coefficient error bounds or continuum positivity |
| A Schwartz function can meet normalization, Fourier positivity, and both lattice zero sets while failing the packing sign | Explicit construction and sign violation in [cardinal note](notes/cardinal-near-certificate.md) | Not a proposed certificate; not rotation invariant |
| Coupled angular modular/interpolation profiles or complex matrix contours might yield an exact certificate | Research proposal | No existence theorem, global sign proof, or convergence proof supplied |
| Exactness of the lattice three-point bound in dimension 4 | Open target in the sources checked | Not proved or disproved by this study |
| Optimality of $D_4$ among arbitrary packings | Not established here | An exact certificate for the lattice theorem would not settle it |

## Verification commands

Run these from `KeplerConjecture/Dimension4` with Python 3.10 or later:

```sh
python computation/run_diagnostics.py
python computation/verify_rank_witnesses.py
python experiments/angular_profiles.py
```

The optional reconstruction of the published solver output is documented in
[UPSTREAM_REPRODUCTION.md](computation/UPSTREAM_REPRODUCTION.md). Its network
fetch stores raw inputs in an ignored cache and retrieves bounded byte ranges;
the full archive is not downloaded or independently checksum-verified.

An assertion that these commands pass means that the stated computations were
performed. It does not promote numerical observations or proposed constructions
to proved packing certificates.
