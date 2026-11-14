# m3 — sound compression patch, per-module measurement, and the tower interface

Everything here is measured against `lean/OAI` (read-only). The patched tree is
`tree/OAI`; `orig/OAI` is the untouched copy; `work/compress.diff` is the diff
(`patch -p1` inside a directory holding `OAI/`).

## 1. The patch: 31277 -> 30011 lines (-1266), 62 of 83 modules touched

Per-module before/after: `work/per_module.txt`. Deleted declarations with file,
name, kind and size: `work/removed_list.txt` (70 rows).

### 1a. Redundant `open` commands: -657 lines (`work/redundant_open.py`)

There are 971 `open`/`open scoped` lines. 657 of them are deleted by two rules,
each of which leaves **the set of opened names in force at every later token
unchanged**, so every declaration elaborates to exactly the same term:

1. delete an `open` whose names are all already open in the same scope stack;
2. fold an `open` into the previous `open` of the same kind *in the same scope*
   when only comment/blank/`open` lines lie between them (so no name-resolving
   line observes the difference).

A new scope invalidates every recorded position (sibling `section`s share a
scope key but are not the same scope) — the first version of the script got this
wrong and produced uncompilable files, and the fix is why the count is 657 and
not 677. `open ... in`, `renaming`, `hiding` are never touched.

This part is provable without a build, and it composes with every other patch:
657 free lines on top of any architecture.

### 1b. Unreferenced declarations: -609 lines, 70 declarations (`work/remove_dead.py`)

Deleted only if: its last name component occurs in the whole tree text no more
often than the number of declarations carrying that component (so no proof,
type, `variable`, attribute list or doc string mentions it — Lean references are
identifier tokens and the tree contains no `exact?`/`apply?`/`library_search`,
while `aesop`/`simp` only search attribute-tagged lemmas); it carries **no
attribute**; it is not an `instance`/`structure`/`class`/`inductive`; it is not
one of the 11 named results; its name is not cited in `README.md` or any
`results/*.md`; and it is not namespace-qualified (a name like `DensityOne.compl`
is reachable by dot notation, which a token scan cannot resolve, so all such
names are kept). Iterated to a fixpoint (7 rounds).

**Two defects I found and fixed, which affect every other dead-weight
measurement on this tree:**

* a deletion range must stop at the next *structure* line (`end`, `namespace`,
  `section`, `open`, `variable`, `omit`, `attribute`, `noncomputable`, `local`,
  `#`, `/-!`, `@[`), not merely at the next declaration. Ranges computed as
  "start of decl .. start of next decl" swallow the `end`s, `namespace`s and
  `variable`s between them: my first version deleted
  `variable (E : Type*) [InnerProductSpace ℝ E]` out of `Compactness.lean` and
  the file no longer resolved `E`. That is why counts differ from a naive scan;
* attributed declarations must be excluded. My first version silently deleted
  `@[simp] lemma char_apply`, `meanCLM_apply`, `coe_asN`, … (30 such lines),
  exactly the change that breaks `simp` calls elsewhere without any name
  appearing in the text.

After both fixes no `end`/`namespace`/`section` line is removed anywhere:
scope-balance counts (`^end`, `^section`, `^namespace`) agree with `orig` in all
83 modules.

### 1c. What is left, measured, and why it is not in the patch

* 54 never-referenced `@[simp]`/`@[simps]`/`@[fun_prop]` declarations, ~125
  lines. Removing them is *not* statically safe (`simp` may use an unnamed
  lemma) but is cheap to test: delete, build, restore the ones whose module
  fails.
* 34 never-referenced `instance`s, ~170 lines. Same situation via typeclass
  search.
* namespaced declarations reachable by dot notation: unattributable statically.

So the honest ceiling of *statically justified* deletion on this tree is
~1.27k lines; a ~1.77k figure obtained by token-suffix matching needs a build to
separate the safe part from the part that breaks `simp`/inference.

## 2. Build status

Blocked by machine load, not by the patch: a trivial `import Mathlib` file does
not finish in 280 s, and one 34-line module of the patched tree took 15 min wall
(5.7 s user, 113 s sys). Every `lean` process re-reads Mathlib's 6.4 GB of
oleans and ~16 members run them concurrently.

The first version of the patch did build six modules to failure — `Basic`,
`Compactness`, `CircleOperator`, `Multipliers`, `FourierTests`, `SmallArcs` —
and those failures are what exposed the three defects above; all are fixed and
the over-deleted material is restored.

Exact commands:

```bash
cd .ultramath/smwfoekgk/m3
export TMPDIR=$PWD/.scratch ORIG=$PWD/orig
python3 work/build.py tree build ../../../lean/build/lib     # incremental, resumable
LEAN_PATH=$PWD/build:$PWD/tree:$LEAN_PATH lean .scratch/CheckAll.lean   # #print axioms
```

`work/check1.py tree build ../../../lean/build/lib <modules…>` compiles a named
subset and prints the full error of each failure.

## 3. Tower interface and the two constraints on the tower routes

* `Five.lean` closure = 70 of 83 modules, 30351 of 31277 lines; almost every
  module has one consumer, so module-level deletion yields at most 926 lines.
* Stationary + Approximation + ConditionalLimits + RelativeCenters = 1996 lines,
  exporting only 5 declarations: `exists_terminal_factor` (one use,
  `Ergodicity.lean:54`), `relative_difference_invariant`, `invariant`,
  `StationaryMean.inner`, `StationaryMean.integral`. The last two are not tower
  material: `StationaryMean` (~125 of the 201 lines of `Stationary.lean`) is the
  invariant-measure construction consumed by `Representations`, `Energy`,
  `SpectralMeasure` and `RadialEnergy` — move it, do not delete it.
* The 16 tower-only modules (8469 lines) export 31 declarations
  (`work/iface_tower.txt`); those used outside the cluster total ~150 lines, so
  ~6000 lines are deletable behind a small replacement.
* `CompactTower.strict_compact_successor` (`Factors.lean:206`) needs only
  "relative product not ergodic" and returns a strict compact successor;
  `compact_union`, `compact_iUnion`, `compactSigma_le`, `compact_descend`,
  `compact_base`, `compact_shift` already give join closure of `Compact`. R1's
  missing pieces are the maximality argument and (H2).
* The trivial factor can never be used: `D` is an abelian Pontryagin dual, so
  `d/d'` is a non-constant invariant of the diagonal K-action and `μ ⊗ μ` is
  never ergodic, even though `relative_singularity_base`
  (`ConditionalLimits.lean:352`, 8 lines) already gives `UniversalGood` there.
