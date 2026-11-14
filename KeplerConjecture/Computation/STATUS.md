# Computation — status index (after review 0353-C)

Branch `kepler15/comp-01a1d8c0`. One page for Main: what is proved, what is numerical, what is open.
Full detail in `REVIEW_0353.md` (this block), `CLAIM_REGISTER.md`, `NONUNIFORM_SHELL.md`,
`CERTIFIER.md`.

## Exactly verified — one command, three independent checkers

```bash
cd KeplerConjecture/Computation
python3 verify_certificate.py out/verified_certificate_K33b.json   # exactcert + SymPy oracle
python3 compact_verify.py                                          # third algorithm
```

| claim | statement | how |
| --- | --- | --- |
| `K15-C-VERIFIEDCERT-001` | `Δ ≤ 0.77996622` for every unit-sphere packing in `R³` | degree-33 rational certificate; `0.779966216777` |
| `K15-C-XVAL-002` | two checkers sharing no code accept it, and accept each other's output | `CROSSVALIDATION.md` |
| `compact_verify.py` | a **third** checker on a different algorithm: Bernstein basis + reversed-polynomial tail, no root counting | 41+9 pieces for `q`, 1+11 for `p`; negative controls reject a perturbed `p(0)`, a flipped Laguerre sign, and the claim `0.7797` |
| `K15-C-REVALIDATE-001` | four shell-route verdicts survive exact basis conversion (`0.78037032`, `0.78033446`) | `REVIEW_0138.md` §2 |
| `K15-C-BOTHSIDES-QUINTIC-001` | quintic both-sides Gram `Δ ≤ 1.33982381256` | `sos_both_sides_quintic2.py` |

## The cut/flow geometry — what it does and does not give

* `K15-C-TRANSFER-DENSITY-002` (**proved**): a bounded antisymmetric transfer on a packing of
  finite upper density **that is `D`-saturated for some finite `D`** implies `ρ ≤ 1/√32`. The
  saturation hypothesis is needed for `Σ_B vol Ω = |B| + O(L²)` and is proved necessary for the
  argument; a packing with an unbounded void does not satisfy it.
* `K15-C-CUTIMPLIES-003` (**proved**): the finite-`U` cut condition at any *one* finite capacity
  `Φ` already forces `ρ ≤ 1/√32`, because `U = Λ ∩ B` is finite. No transfer, no compactness, no
  period.
* `K15-C-HIGHDENS-001` (**proved**): every packing with covering radius `≤ R_Φ` fails C044 at
  capacity `Φ`; `R_0 = 1.105339`. No packing is constructed.
* `K15-C-PERIODCONV-001` (**proved + measured**): the periodic convention for the 13-cluster —
  no wrap-around edges for `R ≤ 3`; the twelve ring cells are congruent (octahedral symmetry) with
  volume `340.870809080957`, measured to `3.4·10⁻¹³`.
* `K15-C-CUTBLOB-001` (**proved, fixture-restricted**): for that fixture `t*` is pinned from both
  sides — `t* ∈ [0.008880268414739, 0.008880268414739]`, width `8.3·10⁻²³`, maximizer `{0}`.

**What none of it gives:** a universal capacity, a proof of Kepler, or any improvement on
Cohn–Elkies. `K15-C-CUTEQUIV-001` ("the cut condition is equivalent to Kepler") is **withdrawn** —
C044 quantifies over finite `U` and a period is not finite.

## Numerical only (`TESTED_FINITE` / `TESTED_FAMILY`) — not certificates

`SOSQSIDE-004` (`1.37125723` Fourier side, `1.33982382` `p` side — best found), `ISOPERIM-001`
(profile exponent `−0.3230 ≈ −1/3`, one complex), `FAMTESTED-001`, `SHELLBENCH-001`,
`SHELLGAIN-002/003`, `CUTJAM-001`, `SOSIRRED-001`, `SATURATION-001`. `shell_bench.py`,
`search_*.py`, `ce3_*.py` are all in this class.

## Actionable for Main

1. **`shell_check.py` at `6626714` is unsound** — it falsely accepts `le_on_interval([0,1,-1],0,0,1)`,
   `nonneg_on_half_line([0,-1,1])`, `_ray([0,1,-1],0)`, all contradicted at `u = 1/2`.
   Do not rely on it until the fix is audited.
2. **Change `shell_check.py`'s `T_LO` default from `12` to `4·π_lo`.** It costs ~6.7% of the bound
   and buys nothing (`TLO_FINDING.md`).
3. `T_HI = 27/2` is valid at `ρ = 2.09` but not at `2.05`; use `T_HI(ρ) = ⌊π_lo ρ²⌋`.
4. Do not optimise in the monomial basis; propose in Laguerre and convert exactly
   (`shell_propose.py`).
5. **Portable verifier for review:** `python3 compact_verify.py` is one file, standard library only.

## Open

* A near-Kepler fixture with **unequal** cell volumes (needs an exactly constructed Frank–Kasper
  phase; perturbation is ruled out by `K15-C-CUTJAM-001`).
* A **local/configurational** shell statement (`NONUNIFORM_SHELL.md` §3.0 states its assumptions and
  §3.1 the four failure modes of the cut condition).
* The converse direction — Kepler ⇒ a finite `Φ` works — is open, and is exactly where a transfer
  would have to be earned.
