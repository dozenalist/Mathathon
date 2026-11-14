# m2 / d10 — audit of the k=6 palette layer

**Main document: [AUDIT.md](AUDIT.md).**

| file | what it is |
|---|---|
| `AUDIT.md` | the audit: Theorem R (the single-centre layer collapses to two constraints), the k=5 calibration, three-way verified orbit tables, exact verification of the paper's Lemma 8.9 / Table 1, the exact range of `alpha` in §7, the sharp cover lemma, the `(T)` correction, and seven errata. |
| `certify_orbit.py` | Theorem R + the four orbit rows by three independent procedures + the per-constraint ablation. |
| `certify_8_9.py` | exact verification of Lemma 8.9 and Table 1, and of both readings of the printed (8.6). |
| `calibrate_k5.py` | the k=5 calibration (the paper's §6.3 triangle conclusion falls out of the alphabet alone). |
| `k6_orbit_count.lean` | **UNCHECKED.** A kernel-`decide` proof that `tr(A^6) = 510`; `import Mathlib` did not finish on this VM under the 16-agent load. Do not cite as machine-checked. |

Reproduce everything (about 85 s):

```
cd .ultramath/smwfwi7rh/m2
python3 certify_orbit.py
python3 certify_8_9.py
python3 calibrate_k5.py
```
