# R1 assembly — delivered tree, measured deletion, and the exact blocking statement

## 1. What is delivered

`lean/` — the staged tree (`sprint/simplify/stage/lean`, 85 modules, 31318 lines) reduced to
**84 modules / 30396 raw lines**, i.e. **881 lines shorter than the 31277-line baseline**
(-847 code lines, 29100 -> 28253).

Point 1 of the review is accepted and fixed: `exists_measurable_proper_seven` and
`weakMeasurableColoring_seven` are back, and `Seven.lean`, `MeasurableAssembly.lean`,
`MeasurableProper.lean` and `PlaneColoring/Basic.lean` are now **byte-identical to the baseline**
(checked with `diff`), so no asset of the tree is weakened anywhere. Independently of R1: this is dead code, an unused module and
redundant scaffolding, all certified on a from-scratch build of both toolchains.

| check | result |
|---|---|
| `hbuild.py --root sprint/simplify/r1/m7 --env $PWD/scripts/env4341.sh -j3 --fresh` (Lean 4.34.1 + pinned mathlib, build dir wiped first, every module re-elaborated) | **84/84 OK, 0 failed** (`build9.log`) |
| `certify.py` (7 headline declarations, `#check` + `#print axioms` + the frozen verbatim statements) | **byte-identical to `BASELINE.cert`** (`CERT.txt`); axioms `[propext, Classical.choice, Quot.sound]`; frozen check PASS |
| `linecount.py --md` | 83 -> 84 modules, 31277 -> 30396 (`LINECOUNT.md`) |
| stock Lean 4.33.1 + `/opt/mathlib` via m4's trim-agnostic port harness (`bash .ultramath/smwg224wy/m4/d7.sh sprint/simplify/r1/m7/lean sprint/simplify/r1/m7/port433 3`) | 109 hunks: 104 APPLIED, 5 OBSOLETE (exactly the hunks whose declarations this tree deletes); **84/84 modules OK**; `CheckBoth.lean` re-certifies all five statements with `[propext, Classical.choice, Quot.sound]`; 30534 lines there (the port itself adds 138 lines of 4.33.1 shims) — `d7.log`, `port433/` |

This is the first tree that is neither the baseline nor the staged copy to be pushed through the
4.33.1 port, so it also validates m4's harness against a *trimmed* shape (its designed purpose).

## 2. How the 881 lines were freed (all reproducible, `tools/`)

1. **`tools/prune_dead.py` — 81 declarations / 669 lines, plus the one module with no consumer,
   `ConnectedUnitFree` (73 lines).**
   A declaration is a candidate iff it is *not* a node of `sprint/simplify/m10/harness/DECLGRAPH.log`
   (m10's sound proof-term closure of the 7 headline declarations) and carries no attribute and is
   not an instance. Candidates are thinned to a fixed point: a candidate is dropped from the set
   only if its unqualified name occurs nowhere in a kept declaration's comment-stripped body, with
   `.` allowed before the name so that a qualified `Ns.name` also counts as a use. Deletion is by
   trimmed block: stop at the first top-level structural command or the next declaration keyword,
   and extend upwards over `omit ... in`, `@[...]`, `private`, doc comments and blank lines so that
   nothing dangles (this is what m6's `f29` and my first attempts got wrong).
   Two traps found and fixed here: an off-by-one that truncated each block by its last line, and a
   `.`-excluding word boundary that missed every qualified use (it deleted `CompactIntegral.apply_clm`
   while a live proof named `CompactIntegral.apply_clm`).
   Biggest single wins: `ConditionalLimits` -98 (`relative_singularity_limit`,
   `finite_encoding_at_of_approximation` — already dead R1 leftovers), `PhaseCollision` -67,
   `InvariantMean` -49, `BoundaryTrace` -47, `FourContinuity` -40, `RelativeProducts` -29,
   `Separability` -28.
2. **`tools/compact_opens.py` — 180 lines.** Drop a column-0 `open` / `open scoped` whose names are
   all already open in the enclosing block, and merge two adjacent plain `open` lines. The
   section/namespace stack pops only on a matching `end` and pops nothing on ambiguity, so the
   rewrite can only keep an `open`, never drop a needed one. (A first, more aggressive version
   removed 543 lines by mis-tracking `noncomputable section` and by merging `open Foo` with
   `open scoped X` into `open Foo scoped X`; it failed 58 of 82 modules. The corrected version is
   82/82.)
3. **Round 2 (attributed but unnamed declarations):** 26 candidates allowed with attributes; 13
   modules accepted (+30 net after restoring `Analysis/PlaneSpectrum/Basic.lean` and
   `InvariantMean.lean`, whose
   `@[simp]`/`@[measurable]` lemmas are used implicitly by tactics).

Rejected as unsound or as gaming the metric: `@[simp]`/instance declarations that are named by live
code, statement clustering (m5 measured 319 lines and abandoned it), blank-line and comment removal
(2177 of the 31277 lines are blank or comment-only).

## 3. Where the deletion stops — the exact line

Two independent walls, both measured.

**(i) Declaration level is saturated.** In the delivered tree, only **125 declarations / 470 lines**
lie outside the 7-headline closure at all, and every one of them is named by live code (that is why
they survived). The measured pool before pruning was 211 declarations / 1286 lines
(`spans_all.json` minus `DECLGRAPH.log`); the pruning above took every one of them that no live
declaration names. So no further mechanical declaration deletion exists: **470 lines is the
remaining slack, and it is not reachable**. m2's audit (`d5`) puts the same cap at 1477 lines; that
figure is m10's `free` *upper bound*, not a buildable deletion, exactly as m6's `f29` warns.

**(ii) The R1 zone (4112 declaration lines) is not reachable through assembly.** R1 requires a new
`exists_terminal_factor`, and the consumer (`Ergodicity.lean:54`, one use at `:58`) needs exactly
one factor `q` with

  (E) `ErgodicSMul K (D x D) (RelativeProduct.law mu q hq)`  (ergodic relative square), and
  (H2) `not (forall^a.e. z, z.1 = z.2)` w.r.t. that relative product (not carried by the diagonal).

Neither extreme supplies both: the trivial factor has (H2) but not (E); the top factor has (E) but
not (H2). m6's `Residual.lean` compiles `ergodic_wild_fourier_of_obligation : TerminalObligation mu -> ∫ eval z = 0`, so the whole 12050-line §2 package is gated by that single predicate, and
`TerminalObligation` is precisely "a maximal *compact* factor has an ergodic, non-degenerate
relative square". Supplying it needs the Furstenberg–Zimmer structure theory (a compact extension
of a compact extension is compact), and *no* maximality principle replaces it:

* `sprint/simplify/m15/work/TowerMax.lean` looks like it does, but `Tower.step` carries only
  `Measurable H`, `‖H x‖ ≤ 2` and non-factorisability — no compactness — so `Tower` is the class of
  *all* factors; its maximal member separates points, its difference law is `delta_1`, `1 ∈ C`, and
  `UniversalGood` there is false for wild `mu`. m6 machine-checked this
  (`m6/TowerDefect.lean`, `tower_max_all_measurable`); `exists_terminal_factor_of_tower_good` is
  therefore vacuous.
* The same obstruction kills the lattice-top route (m1, `d2`, abandoned) and the (N)-only route
  (m8, `d3`, abandoned).
* It also kills the natural repair of the tree's own `Compact`/`At` predicate: I posted the exact
  reason (finding `f4` on `d1`). `At` quantifies `forall k, exists a : Y -> Fin r -> C`, so the
  coefficient tuple `a = a_k` depends on `k`; composing two compact extensions needs the generators
  of `a_k o q`, which depend on `k`, so no `k`-fixed witness exists. `Compact` therefore does not
  imply orbit-precompactness, and `L2 ⊆ A` (A = orbit-precompact vectors) cannot be transported
  through a tower step.
* A second, sharper reason that "maximise over `{Y : L2(Y) ⊆ A}`" is not enough: in the system
  `Y' x {1,2} x Z` with the action trivial on `{1,2}`, the maximal factor with `L2 ⊆ A` is
  `Y' x {1,2} x Z*`, whose relative square has the four `{1,2} x {1,2}` components and is therefore
  **not** ergodic, while it is still proper. So (E) does not follow from non-degeneracy plus
  maximality over compactness; the structure theory is genuinely needed.

**The precise line where the zone stops being deletable** is
`OAI/MeasureTheory/CompactFactors/Stationary.lean`'s `exists_terminal_factor`: its statement can be
weakened from `UniversalGood mu p` to `TerminalObligation`'s (E)+(H2) with no loss to the consumer
(m6's `Residual.lean` proves that implication), and *nothing in the repository proves (E)+(H2)*.
Deleting the R1 zone before that statement exists produces a tree that does not build — which is
what an attempt at the R8 route by m6 measured (5876 -> 4103 lines "not converged").

## 4. (N) is open — and a correction to an earlier claim of mine

The other half of the missing input is (N): a wild ergodic `mu` is *not* a compact extension of the
trivial factor, i.e. `eval z` does not have a precompact K-orbit in `L2(mu)` for `z != 0`.

**Correction.** Earlier in this run I posted (finding `f2` on direction `d1`) a proof of (N) that
avoided the sum-of-units step of `N-proof.md` §2 by exhibiting uniform discreteness of the orbit. It
is **wrong**, and I withdraw it. The error is at
`OAI/Analysis/PlaneSpectrum/ConditionalSpectrum.lean:39`:

```lean
def eval (a : E) : D →* Circle := ⟨fun d => d (Multiplicative.ofAdd a), ...⟩
```

`eval z d` is a **circle number** (the value of the additive character `d` at `z`), not the
character `scalar z d`. Two consequences kill the argument: `phi z = 0` only says `d z = 1` a.e.,
i.e. that `d` kills the cyclic subgroup `Z*z`, which does not force `d = 1` and hence not
`mu = delta_1`; and for `k != k'` the distance between `eval (k z)` and `eval (k' z)` is
`phi ((k - k') z)`, where `(k - k') z` is *not* a K-multiple of `z`, so the claimed uniform lower
bound is unjustified.

What does survive: `phi (k z) = phi z` for `k = kCoeff u` (change of variables under
`MeasurePreserving (u • ·)` together with `eval_scalar`), and, using (F3), `phi (v w z) <= L(v) *
phi (w z)` for every `v`. That yields, for each `epsilon`, a `w_epsilon` with
`Re muhat (v w_epsilon z) > 1 - (L epsilon)^2 / 2` — but not `muhat y = 1` for a *fixed* `y`. This
is exactly the gap m8 reported in `N-proof.md` §2 (the quantified `epsilon` and the
`epsilon`-dependent `w` do not commute), and that report is correct.

So both halves of the obligation are open: (E) needs the Furstenberg–Zimmer structure theory and
(H2) needs (N). Neither is supplied by anything in the repository, and nothing in the delivered tree
below depends on either.

## 5. Exact reproduction

```bash
cd <repo>
# pinned toolchain, from-scratch build of the delivered tree
python3 sprint/simplify/m10/harness/hbuild.py --root sprint/simplify/r1/m7 \
        --env $PWD/scripts/env4341.sh -j3 --fresh
# statement + axiom certificate; diff must be empty
python3 sprint/simplify/m10/harness/certify.py --root sprint/simplify/r1/m7 \
        --env $PWD/scripts/env4341.sh --out /tmp/c.txt
diff <(tail -n +3 sprint/simplify/m10/harness/BASELINE.cert) <(tail -n +3 /tmp/c.txt)
# per-module line table
python3 sprint/simplify/m10/harness/linecount.py \
        --base sprint/simplify/m10/harness/BASELINE.json --root sprint/simplify/r1/m7 --md
# stock 4.33.1 port, build and re-certification
bash .ultramath/smwg224wy/m4/d7.sh sprint/simplify/r1/m7/lean sprint/simplify/r1/m7/port433 3
```

Note: `.scratch/mathlib4` was found half-rebuilt (Mathlib `.olean`s deleted by an interrupted
build) and blocked every member for ~20 minutes; it was restored with
`cd .scratch/mathlib4 && lake exe cache get`. If a check reports "incompatible header", do that
rather than rebuilding mathlib.

## 6. Reconciliation with the review, and what the deletion costs

669 (dead declarations) + 73 (`ConnectedUnitFree`) + 180 (redundant `open`) = **922 lines removed
from the staged tree**; the staged tree is itself +41 over the baseline (the m14 cut-prereq patch),
so **922 - 41 = 881 against the 31277 baseline**. That is the reviewer's 904 minus 23:
`weakMeasurableColoring_seven` cannot even be *stated* without the five definitions `circleDir`,
`normalizedAngleMeasure`, `circleMeasure`, `weakPairMeasure` and `WeakMeasurableColoring`
(23 lines) that the pruner had removed from `PlaneColoring/Basic.lean`, so those are restored too.

The one module still removed is `OAI/Geometry/PlaneColoring/ConnectedUnitFree.lean` (73 lines), which
carries the repository's "connected-set exclusion of §7" (connected unit-free sets have diameter at
most one). It has no consumer in the tree, so nothing breaks, but that result is gone; restoring it
puts the figure at 808.

Everything else in the deletion has no consumer: the 81 declarations are outside the proof-term
closure of the seven headline declarations by construction (`DELETED.txt`), and every `open` line
removed was an exact repeat of a name already open in the same block.

## 7. Per-module table

`LINECOUNT.md` (generated by `sprint/simplify/m10/harness/linecount.py --md`), 55 module rows,
checked against `sprint/simplify/m10/harness/BASELINE.json`.
