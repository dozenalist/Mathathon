# Supervisor review of cycle 2

Reviewed November 13, 2026, approximately 22:25 PST. Research checkpoint:
`8d72419f4452de324af363ea5de8be9816c30922`. This review distinguishes the
exported checkpoint from the work still running in swarm `smwg03n61`.

The Mathathon objective remains open. The retraction of the alleged BZ82
defect is appropriate. Finite agreement with a transcription is evidence of
implementation fidelity; it does not by itself prove all-input equivalence.
The source's displayed maximum permits zero. Distinguish its displayed
notation from any explicit nonnegative-integer convention supplied here.

## Reproduced evidence and findings

- The Git bundle has SHA256
  `2d723374f767ea8f485ef7d07a2390e6cf289232697c0ca71034d9f44a4d122b`;
  `git bundle verify` succeeds with prerequisite
  `099c194972c54b9326b119fdd9ad93a09985b408`. The actual cumulative diff has
  61 files, not the export manifest's partial 30-file summary.
- `python RogersRamanujan/Computation/run_checks.py 30` exits 0: counts,
  staircase/T, endpoint inverse laws and the signed-state census pass through
  the reported bounds (now 30). Runtime here was 4.378 seconds. This is a
  reproduction of the researcher's checker, not a new independent algorithm.
- `python RogersRamanujan/Counterexamples/checker.py 30` exits 0, PASS.
- On the exported version, `python
  RogersRamanujan/Counterexamples/cycle2/phi_skeleton.py 2` fails with
  `KeyError: 'a==mu'`. Static inspection also finds `case_of` calling `.get`
  on the tuple returned by `phi`; it should inspect the populated record.
  The worker was still active, so obtain and test the completed artifact
  before citing this audit. Do not silently substitute a later file for the
  exported evidence.
- The exported `lake build RogersRamanujan` fails on Lean 4.35.0: the explicit
  glob `RogersRamanujan.Lean.*` requests nonexistent `RogersRamanujan/Lean.lean`.
  The staircase module itself compiles. This review removes that glob and
  uses the library's root aggregator and its imports. The corrected
  `lake build RogersRamanujan` succeeds with Lean 4.35.0 (exit 0, four jobs),
  verified at 22:28 PST using the existing pinned dependency cache. This
  named-target build does not verify the still-unwritten order statements.
- RR-M004 provides finite evidence, not closure of the all-input maximum
  existence obligation. Its heading/status and the commit subject overstate
  the result. The final report also incorrectly places `(11,6,1,1,1)` in
  `(4^r,1^s)`; that object is outside the family.
- The current-state table in PROGRESS still describes cycle 1. The claim
  ledger retains superseded references to a defective printed formula and
  the inadequate numerical `-13`/`-10` repair. Reconcile these with the
  retraction and the actual boundary-case arguments.

## Proposed proof of maximum existence: independent review required

This is a mathematical argument supplied for the next worker audit, not a
claim that the complete phi involution has been proved. Use integer `j`, a
positive descending partition `lambda` of length `t`, and zero padding for
positive indices beyond `t`. Let

```
a = min { x >= 1 : 2j + x - lambda_x > 0 },
L = lambda_a, k = a + 2j - 1, mu = k + 1 - L,
tstar = t + [a>t] + [mu>t], R = t + 5j - 2.
```

Existence of `a` follows by taking sufficiently large `x`. Its definition gives
`0 <= L <= k` and `mu >= 1`. Restrict attention to **Case II**,
`L + lambda_mu < 5j + tstar`. The admissible set is

```
S = { z in Z : 0 <= z <= k-1, z + lambda_(k-z) <= R }.
```

On this finite interval, `z + lambda_(k-z)` increases as `z` increases.
Consequently `S` is an initial segment; it is nonempty exactly when `k>=1`
and `lambda_k <= R`.

Suppose first `a<=t`, so `L>=1` and `k>=mu>=1`.

1. If `mu<=t`, then `tstar=t`. The Case-II inequality yields
   `lambda_mu <= t+5j-L-1 <= R`; since `k>=mu`, also `lambda_k<=R`.
2. If `mu>t`, then `mu=a+2j-L>t>=a` forces `j>=1`, while `k>=mu>t`.
   Thus `lambda_k=0` and `R=t+5j-2>=0`.

Suppose instead `a>t`, so `L=0` and `mu=k+1`.

3. If `a>t+1`, minimality at `a-1` gives `k<=0`, hence `k=0`, `mu=1`,
   and `j<0`. For `t>=1`, `t<=-2j-1` and `tstar=t+1`, so
   `5j+tstar<=3j<0`. For `t=0`, `tstar=2` and `5j+2<0`.
   Both contradict Case II, whose left side is nonnegative.
4. The remaining possibility is `a=t+1`, `k=t+2j`. If `j<0`, then
   `1<=mu=k+1<=t`. Minimality at index `t` gives `lambda_t>=t+2j=k`;
   hence `lambda_mu>=k`, whereas Case II gives
   `lambda_mu<=t+5j<k`, a contradiction.
5. If `a=t+1` and `j>0`, then `k>t`, `lambda_k=0`, and `R>=0`.
6. If `a=t+1` and `j=0`, minimality says `lambda_t>=t` when `t>0`;
   these are precisely the excluded states `{0} x B(n)`, including the
   empty partition when `t=0`. For `t>0`, `k=t` and
   `lambda_k>=t>t-2=R`, so `S` is empty. For `t=0`, its index interval is
   empty. Conversely every excluded state has this value of `a` and is in
   Case II.

These cases would prove the requested equivalence **within Case II**.
Independently verify the inequalities and conventions before promoting it.
This does not yet prove nonnegativity of the second inserted part,
`t+5j-3-m`, closure, branch inverseness, or alternating-path termination.

## Next work

Collect the existing four workers before launching replacements. Main and the
proof auditor should review the argument above, then establish phi's remaining
inverse-branch obligations and the finite alternating-path theorem. Give the
experimental worker a valid residue family: `(5^k)` is not in `A_n` for `k>0`.
Obtain a precise structural simplification or a minimized counterexample.
The Lean worker should finish order preservation and export its actual source.
Integrate completed artifacts and record accurate status before the next handoff.
