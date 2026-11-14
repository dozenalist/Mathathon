# Sprint A, phase 2: assembled record

Swarm `smwg224wy`, 8 members, 6 submissions accepted. Two trees produced, both
building and re-certified; the 1500-line code target was NOT met; the reason is
identified and is a single open lemma.

## The trees

| tree | modules | raw lines | vs baseline 31277 | code lines | status |
|---|---|---|---|---|---|
| `sprint/simplify/r1/m7/lean` | 84 | 30396 | **-881** | -881 | 84/84 both toolchains, cert byte-identical |
| `sprint/simplify/r1/m2/trees/m7docs` | 82 | 29563 | **-1714** | **-1382** | 82/82, cert byte-identical, definitions frozen |

The second is shorter only because it also deletes 445 comment/docstring lines (332 of the
1714). The code-line figure, which is the one that matters for "a shorter proof", is 1382 -
118 short of the target. Both trees delete the same 99 declarations, of which eight are cited
in reference documents (`palette_transfer_pair`, `relative_singularity_limit`,
`binary_pair_distinct`, `four_split_antipodes`, `diam_le_one_of_preconnected_unitFree`,
`not_straddle_of_isPreconnected`), so both prove the headline theorem while formalising
fewer of the paper's numbered statements. That is a scope choice, not an error.

## Why 1500 code lines is not reachable by reduction

Six independent measurements agree:

* dead declarations: 669-692 lines; consumerless modules: 73 (not 198); redundant `open`: 180;
* mechanical ceiling from all pruning rules together: -1280 (m2 f40);
* R1 restructure would be worth 3695-4889, but see below;
* R2/R5/R6 free 0 and add code; R3 frees 354; the `k=4` architecture is empty;
* the automatable-tactic route saves ~25 lines; header hygiene 174; statement subsumption 43;
* no module is dead weight: 82 of 83 lie in the five roots' closure.

## The one blocking lemma

The deletion zone stops at `exists_terminal_factor`. Its consumer (`Ergodicity.lean:52-57`)
needs ONE factor `q` with BOTH

  (E) `ErgodicSMul K (D x D) (RelativeProduct.law mu q)`, and
  (H2) `not (forall^a.e. z, d z.1 = d z.2)`,

which is m6's `TerminalObligation`. Facts established in this phase:

* trivial factor: (H2) holds, (E) fails.  Top factor: (E) holds, (H2) fails
  (`differenceLaw = delta_1`, `1 = j 0` in `C`) - machine-checked as
  `differenceLaw_C_eq_one_of_diag`, `not_universalGood_of_factorizable`.
* m15's `Tower` is VACUOUS: `Tower.step` carries no compactness, so `Tower` is the class of
  ALL factors and its maximal member determines the whole sigma-algebra. Machine-checked twice
  (`TowerDefect.lean`, `TowerAudit.lean`). `TowerCorrect.lean` restores the `hc` clause and is
  the first non-vacuous version.
* The weak-mixing shortcut is dead at its only call site: Haar on `D` is ergodic, wild and NOT
  weakly mixing, so `TerminalObligation` cannot be obtained from ergodicity of `mu x mu`.
* The tree's `At`/`Compact` cannot compose (coefficients depend on `k`), giving precompact
  orbits only at the point factor.
* Therefore the missing input is **properness of a maximal compact factor** - statement (N).
  The "cheap proof" of (N) is WITHDRAWN as wrong (`eval z d` is a number, not a character).
  (N) is OPEN.

## What is proved

Theorem A survives and is machine-checked: at a factor with ergodic relative square and a
non-factor-measurable `d`, the relative difference law is `C`-null, with no `IsWild` hypothesis
needed (`relative_singularity_of_ergodic`). `TerminalGlue.lean` proves `GoodId` holds at the
point factor, `UniversalGood => GoodId`, and `GoodId + ergodic relative square => integral
eval z dmu = 0`. So the whole restructure reduces to: produce one factor satisfying (E)+(H2).

## Next concrete step

Prove (N) against the tree's own definitions: a wild ergodic `K`-invariant `mu` on `D` is not a
compact extension of the trivial factor, stated with `Compact` and `IsWild` as `Functions.lean`
and `Basic.lean` define them. Everything else in the deletion path is built and waiting.
