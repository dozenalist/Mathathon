# X continuation — free-width family and E's `K15-E030`

Same block as `REPORT_44182.md` (completion 44182, source `3831361a`; supervisor commit
`ec2596dc`). Ultramath not active. Role X, branch `kepler15/counterexamples/run-01`.

## 1. Free-width Gaussian family: implemented and verified (X-R03 dependency closed)

`ce_width_family.py` implements `f(x) = P(|x|²)e^{−a|x|²}` with `a ∈ Q_{>0}` and the exact map
$$\widehat{f}(t)=\pi^{3/2}a^{-3/2}Q(w)e^{-w},\qquad w=\frac{\pi^{2}\lVert t\rVert^{2}}{a},\qquad Q(w)=\sum_n c_n a^{-n}A_n(w),$$
where $A_n(w)=(-\partial_\mu)^n[\mu^{-3/2}e^{-w/\mu}]_{\mu=1}$ are the same exact polynomials as
in the `a=1` case, and $a^{-3/2-n}$ comes from $\lambda = a\mu$ in the $\lambda$-differentiation.
Both sign domains stay rational: `s ≥ 4` for `P`, `w ≥ 0` for `Q`.

**Verified against independent 3-D radial quadrature** for `a ∈ {1/2, 1, 3/2, 2}` and `T ∈ {0, 0.7}`:
residuals `≤ 1.8e-15`. Constants:
* density `= (4a^{3/2}/(3√π))·P(0)/Q(0)`;
* Kepler test `32 a³ P(0)² < π³ Q(0)²` (three-valued, directed π enclosure); `a = 1` recovers the
  corrected test of `REPORT_44182.md`;
* the `a=1` control generalises to `Q(w) = 2 − 1/a + 2w/(3a)`, feasible iff `a ≥ 1/2`
  (at `a = 1/2` it degenerates to `Q(0) = 0`, i.e. no certificate).

## 2. LP over the width family: runnable, bounded, and honestly negative

`x_r03_width_lp.py` (column-equilibrated LP + cutting planes + exact certification, with
rounding renormalised so `Q(0) = 1` exactly) runs end-to-end in ~10 s at `N=4, a=1, 25` rounds:
**no certificate**. Diagnosis, not a verdict of infeasibility: the LP minimises `P(0)` subject to
`P ≤ 0` on a grid of `[4,∞)`, and it repeatedly produces `P` with a *simple* root just above 4,
so the exact test rejects it, the cutting plane adds that point, and the LP finds another nearby
violation — a classical oscillation.

**The structural fix** is to build CE1 into the parameterisation rather than policing it:
`P(s) = −(s−4)·H(s)` with `H ≥ 0` on `[4,∞)`, ideally `H` a sum of squares with rational
coefficients, which makes `P ≤ 0` exact by construction. That is a semidefinite program, not an
LP, and it is the right form for the next local run. **No 3-D CE bound is claimed by X**; the
certificate *path* is proven by the control (`1.504506`), only the *optimisation* is missing.

## 3. E's `K15-E030` (geometric partition): structure accepted, and the exact size of the gap

**Structure.** The rule is explicit and constructive: defective centres are defined by
`vol Ω(v) < √32`, blocked as `C(v) = {v} ∪ {w : 2 ≤ |w−v| ≤ 2.09}`, and the rest become
singletons. `|C(v)| ≤ 13` uses `K15-E014` (the `ρ = 2.09` shell count), `diam ≤ 2·2.09 = 4.18`.
This is a genuine partition, and because the rule *constructs* it, the quantifier is existential
with an explicit witness — **which settles my earlier objection**: my remark that an existential
partition "degenerates to Hales" is moot here, since the partition is exhibited rather than
postulated. Withdrawn in E's favour.

**Boundary constant verified.** The count of blocks meeting a shell of width `D+2` obeys
`3(D+2)(r+D+2)²`, which dominates the packing bound `3r²(D+2)` (e.g. `2.09e5` vs `1.854e5` at
`r=100`), so it errs in the safe direction. `D = 4.18` is a fixed constant independent of `r`, so
the `O(r²)` boundary loss is uniform — E's Step 2 is sound.

**The target inequality (T), quantified.** For the icosahedral block `|C(v)| = 13` and
`vol Ω(v) = V_dod = 5.5502910285`, so (T) demands
$$\sum_{i=1}^{12}\operatorname{vol}\Omega(w_i)\ \ge\ 13\sqrt{32}-V_{\mathrm{dod}}\ =\ 67.9888142,$$
i.e. a **mean outer cell of 5.6657345**. Three exact comparisons follow:

| quantity | value | consequence |
| --- | --- | --- |
| required mean outer cell | `5.6657345` | **exceeds** the FCC cell `√32 = 5.6568542` by `0.008880` |
| dodecahedral bound over 13 cells | `13·V_dod = 72.1537834` | short of `13√32 = 73.5391052` by **`1.3853219`** |
| trivial bound `vol ≥ 4π/3` over 13 cells | `54.454` | far too weak |

So **(T) is strictly stronger than Hales–McLaughlin's `vol Ω ≥ V_dod`**, by exactly
`13(√32 − V_dod) = 1.3853219`, and it is *not* implied by any per-cell volume bound that is tight
at the dodecahedron. Its content is that the twelve outer cells of an icosahedral defect must
*compensate* for the deficient central cell by exceeding an FCC cell on average — a genuinely new
local inequality, and the right thing for E to be attacking.

**Why no finite computation can settle it.** By E003 (which I accept) adding centres only shrinks
cells, so any computed completion gives *upper* bounds on `Ω(w_i)`; and in the bare 13-cluster the
outer cells are unbounded. Hence (T) cannot be certified numerically in any completion — a
*supporting* computation cannot exist, only a refutation (exhibiting a saturated completion with
sum `< 67.9888142`). That is E's own stated gap and it is correctly identified.

*What would prove (T), stated precisely.* Either (i) a lower bound on `vol Ω(w)` for a centre
whose `k` nearest neighbours are at distances `> 2` and which is adjacent to a deficient cell —
a "compensation" or "defect tax" inequality; or (ii) an argument that the 12 outer cells contain
explicit pairwise disjoint bodies of total volume `≥ 67.9888` (e.g. inner balls plus caps cut by
the bisector planes, which would require the local geometry of the icosahedral cluster). Route
(ii) looks tractable and does not need saturation.

## 4. Status

| Item | Status |
| --- | --- |
| free-width Fourier map | **VERIFIED** (quadrature `≤1.8e-15`, exact rationals) |
| density / Kepler constants for general `a` | **DERIVED** and checked at `a=1` |
| LP over the width family | **RUNNABLE, NO CERTIFICATE** (cutting-plane oscillation; SDP fix named) |
| 3-D CE bound from X | **NONE CLAIMED** |
| E030 rule / partition / quantifier | **ACCEPTED** (constructive, existential witness) |
| E030 boundary constant `3(D+2)(r+D+2)²` | **VERIFIED** safe |
| E030 target (T) | **OPEN**, and strictly stronger than `vol Ω ≥ V_dod` by `1.3853219` |
| finite certification of (T) | **IMPOSSIBLE** (monotonicity gives upper bounds only) — E's gap is real |

Artifacts: `ce_width_family.py`, `x_r03_width_lp.py`, this report.
Next: implement the SOS parameterisation `P = −(s−4)H`, `H` SOS over `Q`, and submit the bounded
SDP run; audit E's `SHELL_CONVERSION.md` and `ANALYTIC_LOCAL_MASS.md`.
