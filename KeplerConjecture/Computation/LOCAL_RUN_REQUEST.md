# Computation local run request (bounded) — Astra

Written 2026-11-14T09:2xZ for block K15-HOUR-20261114-C. Owner: Computation
(`kepler15/comp-01a1d8c0`). Reviewer: X, then Main. Main integrates.

Everything below is small: **1 CPU, under 1 GB, under 5 minutes**. No Lean, no SDP, no
degree sweep beyond the stated caps. The VM has already run these; the purpose of the local
run is independent reproduction on the pinned environment, not discovery.

## The frozen object (already checked in and pushed)

| item | path | revision |
| --- | --- | --- |
| verified certificate, degree 33, `Delta <= 0.77996622` | `Computation/out/verified_certificate_K33b.json` | `50727f1`, `90cc632` |
| second verified certificate, `Delta <= 0.77996650` | `Computation/out/verified_certificate_K33.json` | `50727f1` |
| rational checker (own Sturm + Yun) | `Computation/exactcert.py` | `ad7dd1c` |
| independent exact oracle (SymPy `sqf_list` + `count_roots`) | `Computation/exactcert_oracle.py` | `ad7dd1c` |
| re-verification driver | `Computation/verify_certificate.py` | `50727f1` |
| regression suite (incl. the 48443 counterexample) | `Computation/exactcert_tests.py` | `ad7dd1c` |
| shell proposer (this block) | `Computation/shell_sos.py` | this commit |

Source commit for this request: the tip of `kepler15/comp-01a1d8c0` after this block.

## Commands

```bash
cd KeplerConjecture/Computation

# 1. certificate + checkers, ~25 s, stdlib + sympy
python3 verify_certificate.py out/verified_certificate_K33b.json
python3 verify_certificate.py out/verified_certificate_K33.json
python3 exactcert_tests.py
python3 exactcert_oracle.py

# 2. shell proposer, ~5 s for degree 9 (shell_check at 6626714 is UNSOUND -- see
#    REVIEW_0138.md; use it only to reproduce, and take verdicts from exactcert)
python3 shell_propose.py --checker /tmp/shell_check.py --degree 9
# best exact value in the family (~10 s):
python3 shell_propose.py --checker /tmp/shell_check.py --degree 33 --tlo-exact --Umax 120
python3 audit_fourier.py /tmp/shell_check.py
python3 sos_family.py          # explicit rational Gram, p-side by expansion
python3 sos_family2.py         # degree 5, two-square Gram
python3 sos_shell_variant.py   # proved family-restricted shell comparison
python3 cut_deficit.py         # periodic cut-deficit fixtures
python3 tests_0138.py          # every review-0138 claim, exact

# longer search for a better explicit-Gram certificate (the natural offload):
# 12 runs on the VM span 1.3713..1.9989; a few hundred runs would sharpen it.
for S in $(seq 100 300); do
  python3 sos_qside_polish.py --degree 7 --iters 4000 --seed $S --uphill 0.05 \
    --out out/hop_$S.json
done
# ~40 s per run, 1 CPU, < 300 MB; keep the best by its "delta" field.
```

For (2) copy Main's checker next to the run, or pass its absolute path:

```bash
git show omm/kepler15/main:KeplerConjecture/Computation/shell_check.py > /tmp/shell_check.py
python3 shell_sos.py --checker /tmp/shell_check.py --degree 7   # ODD and <= 7 only
```

Dependencies: Python 3.12, `numpy`, `scipy` (HiGHS), `sympy`. No other packages. Versions
used on the VM: numpy 2.5.3, scipy 1.18.1, sympy current.

## Expected outputs and success criteria

| command | expected | success criterion |
| --- | --- | --- |
| `verify_certificate.py K33b` | `ACCEPT` from both checkers, `0.779966216777` rounded up | exit 0; `Delta upper` identical to 12 dp |
| `verify_certificate.py K33` | `ACCEPT`, `0.779966497785` | exit 0 |
| `exactcert_tests.py` | `ALL TESTS PASS` | exit 0, including the `K21` refutation |
| `exactcert_oracle.py` | `ALL ORACLE CHECKS PASS` | exit 0 |
| `shell_propose.py --degree 9` | `eta=0` and `eta_free` both EXACT PASS at `Delta <= 0.87227746`; gain exactly 0 | both rows PASS; gain printed as `+0.00000000` |
| `shell_propose.py --degree 33 --tlo-exact --Umax 120` | `Delta <= 0.78037031`, gain exactly 0 | PASS at degree 33 |
| `audit_fourier.py` | `AUDIT PASS` | exit 0, A1/A2 exact and A3 quadrature agree |

## Caps

`timeout 300`, 1 CPU, `OMP_NUM_THREADS=1`, peak RAM well under 1 GB (the largest object is a
degree-41 polynomial over `Q`). Disk: under 5 MB of JSON.

## What these checkers actually prove (and do not)

`verify_certificate.py` proves: the rational polynomials `p, q` in `out/verified_certificate_*.json`
satisfy `p < 0` on `[8*PI_LO, ∞)` and `q > 0` on `[0, ∞)`, where `PI_LO < π`, so the region
verified is *strictly larger* than `[8π, ∞)`; hence `f = p·e^{-t/2}` satisfies the
Cohn–Elkies hypotheses, and `Δ ≤ (4π/3)·p(0)/q(0)` for every packing, by the cited CE theorem.

**Tails are not an obligation for this basis.** `f = p(t)e^{-t/2}` is a polynomial times a
Gaussian, so it is Schwartz: integrable, decaying faster than any power, and admissible in the
sense the CE theorem requires. That is the one structural advantage of this family over
compact-support or power-law candidates, and it is why the certificate needs no separate tail
estimate.

What it does **not** prove: that `0.77996622` is optimal in any sense, or that any other
degree improves it (measured: it does not, see `CERTIFIER.md`), or anything about the shell
count hypothesis (that is X's and E's).
