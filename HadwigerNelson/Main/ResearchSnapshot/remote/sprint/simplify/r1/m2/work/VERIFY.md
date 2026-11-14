# Sound verification of an OAI tree (m2 / d14)

`"the tree builds"` is not evidence on this VM, and neither is `certify.py` on a build
directory that was not wiped. This is the procedure that is evidence, plus the two witness
trees that show what it catches.

## Run

```bash
R=/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo
$R/sprint/simplify/r1/m2/verify.sh  <TREE>  <FREEZE_REF>
# e.g.
$R/sprint/simplify/r1/m2/verify.sh  $R/sprint/simplify/r1/m7/lean  $R/sprint/simplify/r1/m2/work/A.freeze
```
`<TREE>` is a directory containing `lean/OAI/**`. Exit 0 iff every step passes. It writes
`<TREE>/verify_report.json`, `<TREE>/verify.cert`, `<TREE>/verify.freeze`.

## Steps (each one has caught something in this sprint)

0. `textscan.py` — source-level `sorry/admit/native_decide/implemented_by/@[extern]/opaque/axiom/unsafe`,
   comment-aware. `#print axioms` of the 7 headlines cannot see a hole in a declaration the
   headlines do not use; this can.
1. **wipe** `<TREE>/lean/build/lib`. See `A_del` below: with the olean left in place a
   *deleted module* keeps certifying.
2. build every `.lean` with `lean -o`, topological, `-j2`; every module's olean is unlinked
   before it is elaborated, so a failed module can never leave a usable stale olean.
   A parallel failure is retried serially and only counted if it fails twice: on this
   contended 4-core box, 4-5 heavy modules failed in 2 of 4 full runs and each built alone
   in 9-20 s. Flakiness is not a build failure.
3. require `#olean == #.lean`. A module missing from the tree cannot be imported any more.
4. `certify.py` — `#check` of the 7 headlines byte-identical to `harness/BASELINE.cert`,
   `#print axioms` = `[propext, Classical.choice, Quot.sound]`, `frozen.lean` PASS.
5. `deffreeze.py --ref <FREEZE_REF>` — `#print` of the def-kind constants in the type-closure
   of the 7 headlines (exactly 6: `EuclideanFiveColor.ProperColoring`, `WeakColoring`,
   `LabelModel.Proper`, `Spectral.E`, `Problem160.ProperColoring`, `planeChromaticNumber`),
   diffed against a reference capture. Step 4 alone does **not** pin them: tree `A_pcn`
   (`planeChromaticNumber := 6`) passes step 4 with all 7 `#check` lines byte-identical and
   fails step 5.
6. `linecount.py` vs `BASELINE.json` — the per-module table and the raw-line saving.

## Reference run: the staged tree (`sprint/simplify/stage/lean`, my copy `trees/A`)

    textscan: clean
    build:    85/85 modules from a wiped build/lib, 451 s (j=2, serial retry)
    certify:  byte-identical to BASELINE.cert
    deffreeze: PASS vs work/A.freeze
    linecount: 31277 -> 31318 (+41, 83 -> 85 modules) — the documented preparation cost

So the staged tree genuinely builds from scratch and genuinely certifies; the +41 is real.

## Witness 1 — `trees/A_del`: a deleted module still "builds"

`OAI/Geometry/PlaneColoring/Metric.lean` (72 lines) deleted, its olean left in `build/lib`:

    hbuild --only PlaneColoring.Seven   ->  7/7 modules OK in 0s, rc=0
    rm build/lib/.../Metric.olean; rerun ->  still 7/7 OK (Seven.olean is up to date)
    touch Seven.lean; rerun             ->  FAIL object file .../Metric.olean does not exist

`certify.py` passes on that tree, because it only loads oleans. Only step 1-3 catches it.

## Witness 2 — `trees/A_pcn`: a weakened definition re-certifies

`Problem160.planeChromaticNumber := 6` (plus the two `Chromatic.lean` proofs redone):

    certify.py rc=0, all 7 #check lines byte-identical to BASELINE.cert, frozen.lean PASS
    only diff: chromaticNumber_bounds axioms [propext] vs [propext, Classical.choice, Quot.sound]
    deffreeze.py: FAIL (sInf (Set.ofPred ProperColoring) vs 6)

The axiom diff is incidental; `:= sInf {k | 6 ≤ k}` keeps it identical. The same trick makes
`algebraic_colorable_iff` vacuous (`E := ℂ`, `LabelModel.Proper := ProperColoring`).

## Do not use Lake here

`lake build` (4.34.1) resolves mathlib's dependency packages by *vendoring* them into the tree
and then invokes `/opt/lean/bin/lean` (4.33.1) on them; that wrote 285 wrong-version oleans into
the shared pinned mathlib and left two modules without any olean (repaired: `lake exe cache get`
under the pinned toolchain + `lean -o` on `Mathlib/Data/Nat/BinaryRec`, `Mathlib/Tactic/Lift`).
`lean -o` with `LEAN_PATH` from `scripts/env4341.sh` is the only safe driver.
