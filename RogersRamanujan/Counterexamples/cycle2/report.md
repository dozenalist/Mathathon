# Cycle 2, direction B (proof audit) — member m1

Deliverables in `RogersRamanujan/Counterexamples/cycle2/`:

| file | contents |
|---|---|
| `AMENDED_PROOF.md` | the amended all-`n` proof that `psi` is an involution on `X(n)\{0}xA(n)`; both boundary errors repaired; complete virtual-zero/multiplicity census; `phi` skeleton audit with an exact gap list |
| `psi_audit.py` | independent transcription of `psi` from the brief + an assertion for **every proof step**, run over all of `X(n)`, `n <= 30` |
| `phi_skeleton.py` | `phi` skeleton audit P0–P9, plus the Monotonicity Lemma for the Case II maximum |
| `crosscheck.py` | proves the transcriptions are the same maps as `Computation/bz82.py` (0 disagreements, n <= 26) |
| `log_*.txt` | the runs quoted in the proof |

## Results

1. **`psi`: the amended proof is complete. Gap list empty.** E1 (`t0'=t0-1` in
   II(b)) and E2 (`m3'<=m3-5` in II(a)/`nu=0`) are repaired, and *two further*
   steps that were true but unargued are closed: I(b) never runs with `m2=0`
   (which also makes its `k` a non-negative integer) and II(a) never runs with
   `m3=0` (which is what makes `nu = 0 (mod 5)` and hence `m2'=0`).
2. **Sharp forms.** In II(b), `t0'=t0-1` **iff** `m0>0`; `m0=0` gives
   `t0'=t0=0`. In II(a) with `nu=0`, `m3'=m3` **iff** `m3` is repeated; the
   committed bound fails in two ways (repeated `m3`, and `m3=3` simple where
   `m3'=0 > -2`) — 1 721 of 1 949 such states at `n<=30`, 0 violations of the
   replacement `m3' <= m3`.
3. **`phi`.** New all-`n` results: `a` always exists with `a <= max(t+1,1-2j)`;
   `mu >= 1`; and **`a = mu` never occurs in Case I**, so the printed
   "delete the slots at `a` and `mu`" multiplicity is never ambiguous (the
   tie-break carried in `bz82.py` for that case is unreachable).
   **Monotonicity Lemma:** `lam(i)-i` is non-increasing, so the Case II
   admissible `z`-set is a *down-set*; hence the maximum exists **iff**
   `a+2j-2 >= 0` and `lam(a+2j-1) <= t+5j-2`. The "max may not exist" worry
   reduces to that single inequality and nothing else.
   Gaps for `phi`: G1 that inequality (open, finite to `n=30`); G2 case
   stability (open, measured); G3 `phi^2=id` (open, measured); G4 a genuine
   *specification ambiguity* in the printed `t*` — under the alternative
   reading "pad to length `t*` and increment every remaining slot", `phi` Case I
   does **not** preserve weight (`(-1;())` would give weight 4, not 3). The
   reference code uses the other reading; `t*` must be quoted with that reading
   attached.

## Exact commands and key output lines

```
$ cd RogersRamanujan/Counterexamples/cycle2
$ python3 psi_audit.py 30
0 failures: every step of the amended proof (a)-(d), every branch, ...
states in Dom(n): 66658   (F(n) = {0}xA(n): 893)
branch counts:    I(a)=29924 I(b)=29924 II(a)=3405 II(b)=3405
$ python3 phi_skeleton.py 30
0 failures on every skeleton step P0-P9 over the whole range.
$ python3 crosscheck.py 26
VERDICT: identical maps on the tested range
```

## Honest limits

* Everything here is a write-up plus a finite machine check. `psi`'s theorem is
  PROVED on paper and the paper argument is machine-asserted step by step; the
  machine check is not a proof and is not offered as one.
* The three tie-break readings are *used* in 4.2 and 4.4 and are **not**
  re-proved here beyond isolating exactly where equality occurs (4.2a, 4.4a).
  Their forcing is cycle-1 evidence (RR-X006 / D-3a).
* `phi`'s involution is not proved here and is not claimed; RR-C009 stays
  TESTED_FINITE.
* I did not run git, and did not touch anything outside this folder.
