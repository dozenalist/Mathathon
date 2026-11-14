# Local numerical review, completion 27616

These are local reproductions, not sphere-packing certificates. Source revisions,
SHA-256 hashes, commands, environment and measured times are in `manifest.json`.
Python 3.12.14 used isolated numpy 2.3.5, scipy 1.16.3, sympy 1.14.0 and
mpmath 1.3.0. No shared Python installation or other project was changed.

## Main implementation failure

`main-original.py` is the submitted script verbatim, including its incorrect
interpretation of its output. It omits the Fourier-positivity matrix from both
LP calls. Its coefficient bounds are finite, and solver status 0 means a
finite optimum, not unboundedness. The negative objective reproduced exactly
as `-18719434.7288689`.

`main-repaired.py` adds that matrix to both calls and replaces the unsupported
output conclusion. This is a minimal diagnostic repair, not a certified solver.
Both objectives become `0.21820243547088458`. The resulting candidate still
violates Fourier positivity in the tail. Its `audit_min_fhat` and
`audit_max_f_on_region` fields are evaluations of Q and P without the Gaussian
factor. `delta_from_floor` is merely the fixed `1/8` floor, not the candidate's
density. The original comments and field names remain provenance requiring
repair in Main's canonical implementation.

```powershell
python main-original.py --degree 8 --grid 1200 --tmax 40 --out main-original.json
python main-repaired.py --degree 8 --grid 1200 --tmax 40 --out main-repaired.json
```

## Independent Computation implementation

The `comp/` files are exact exports from
`4b509e33fe1f5d50d37f7dd19b698d708312d35a`. This implementation includes both
sign matrices. The scalar below is its finite-grid objective converted to
occupied-volume density, not an established upper bound for sphere packings.
Its original output field `Delta_bound` should be interpreted with this limit.

| Degree | Grid points per sign condition | Reported density value | Maximum exterior f on audit grid | Minimum fhat on audit grid |
| --- | --- | --- | --- | --- |
| 31 | 1200 | 0.7797024457856065 | 1.20e-7 | -2.97e-6 |
| 31 | 4000 | 0.779748765 | 1.28e-8 | -2.64e-7 |
| 41 | 4000 | 0.7797457680828066 | 1.11e-8 | -2.64e-7 |

All three solves exited 0, but all three candidates have sign violations.
At fixed degree, the refined grid raises the optimistic objective. Degree 41
on the fine grid does not satisfy the requested tolerance of `1e-5` around the
old coarse value `0.7797024`. Changing degree and grid simultaneously would
confound their effects. No interval, Sturm, SOS or global-tail certificate was
produced. Saved coefficients are rounded by the submitted script; diagnostics
were computed on the unrounded optimizer, which is another certification gap.

```powershell
python comp/k15conv.py
python comp/fixtures.py
python comp/ce3_baseline.py --degree 31 --grid 1200 --r0 1.0 --out comp-K31-g1200.json
python comp/ce3_baseline.py --degree 31 --grid 4000 --r0 1.0 --out comp-K31-g4000.json
python comp/ce3_baseline.py --degree 41 --grid 4000 --r0 1.0 --out comp-K41-g4000.json
```

The normalization assertions passed. The five fixture outputs passed their
reported checks, with finite FCC Gaussian Poisson residual approximately
`2.012e-29`; this numerical quadrature/truncation result is not an exact proof.
The script prints several checks rather than asserting all of them; their
values were inspected in `comp-fixtures.log`.

The requested `r0=2^(1/6)` experiment is deferred until the reported density
incorporates the radius change (`r0^3`). The exact-certificate drivers requested
by Main/X and Experimental's interval job remain unimplemented. Those gaps
were returned to their authors rather than treated as executable jobs.
