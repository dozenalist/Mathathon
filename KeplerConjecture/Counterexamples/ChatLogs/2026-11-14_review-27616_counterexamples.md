# ChatLog — Counterexamples (X), review 27616

Date: 2026-11-14 (America/Los_Angeles). Session `i-ve-attached-viazovska-f7hh`.
Role X. Branch `kepler15/counterexamples/run-01`. Ultramath OFF (nothing started or resumed).

Inputs audited: `kepler15/main` @ `a08f378be6a03f80ac075b34f8ba99aeb8201d9e`;
`kepler15/experimental/run-01` @ `7cdec5deee2b3c60845be49c9c5cecc1f3592f78`;
`kepler15/comp-01a1d8c0` @ `4b509e33fe1f5d50d37f7dd19b698d708312d35a`;
`kepler15/setup-01a1d8c0` @ `391ea0c807675808577bdcaabff925f8c94b0d43` (review text supplied
in the prompt; `Main/SUPERVISOR_REVIEW_27616.md` and `Computation/Reviews/27616/` are NOT present
on that branch).

Actions, in order.
1. Confirmed `kepler15/main` has advanced to `0c3ee751254b1b61f16eb175d9bd8d571f842b18`; noted that
   `m2-proof.md` and `m1-certificate.json` are byte-identical at both commits, so the proof
   findings transfer, while `CLAIMS.md` (+192 lines) is unaudited.
2. Read `Main/Evidence/m2-proof.md` lines 110–140 and 246–270 and confirmed both review defects:
   the division by `#C_in` keeps a lower bound (wrong direction) and the bad-index count is per
   `j` but used as a total (`nk` vs `nk²`).
3. Derived the hybrid score mean from the definition, `mean_v B_kappa = kappa c fhat(0) > 0`,
   which refutes C005(ii) with the opposite sign; computed the icosahedral second-shell radius
   `2.102924` to bound the validity of the 12-contact formula.
4. Confirmed `||fhat||_1 = f(0)` in the Fourier-positive class, so C010b's log term is identically
   zero there and the product counterexample refutes only the unrestricted claim.
5. Recomputed C013's thresholds: `θ ≤ 2 arccos(11/13) = 64.41°`, `δ < 28^(1/3) − 3 = 0.036589`.
6. Located the Tammes-13 primary source (Musin–Tarasov, DCG 48 (2012) 128–141, arXiv:1002.1439,
   `d13 ≈ 57.1367°`) and derived the varying-radius reduction, giving the explicit tolerance
   `δ₀ = √(2/(1−cos d13)) − 2 = 0.091146` (conservative `0.091035`).
7. Replaced the X-R01 sketch by an exact family with an exact Fourier map and a sign test that
   accepts even-multiplicity zeros (`ce_exact_gauss.py`, quadrature cross-check `≤1.8e-15`) and a
   runnable driver (`x_r01_driver.py`); degree 6 with fixed Gaussian width is LP-infeasible,
   diagnosed as width rigidity, filed as X-R03.
8. Accepted E002 (closed form reproduces `5.5502910285`; realisation YES) and E003; accepted E001's
   boundary step and showed its hypotheses hold with `D=4, Vmax=27`.

Not done: C's baseline certification fields (G2), C014 artifact hash (missing, G3), E3 locator
(G4), post-a08f378 `CLAIMS.md` (G1).

Reports: `Counterexamples/REPORT_27616.md`, evidence in `Counterexamples/evidence/`.
