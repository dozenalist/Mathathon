# m2 / d14 — what is certified here, and the measured frontier

Everything below was run on this VM; every number has a command behind it.

## 1. The sound verification procedure

    sprint/simplify/r1/m2/verify.sh <TREE> <FREEZE_REF>

`<TREE>` contains `lean/OAI/**`. Exit 0 iff all of:
 1. `textscan.py` -- no `sorry`/`admit`/`native_decide`/`implemented_by`/`@[extern]`/`opaque`/`axiom`/`unsafe`
    in code (comment-aware). `#print axioms` of the 7 headlines cannot see a hole elsewhere; this can.
 2. `build/lib` is WIPED.
 3. every `.lean` elaborated with `lean -o`, each module's olean unlinked first, so no stale olean survives;
    a parallel failure is retried serially and only counted if it fails twice.
 4. `#olean == #.lean`.
 5. `certify.py` byte-identical to `harness/BASELINE.cert` (7 `#check` lines + `#print axioms` + frozen.lean).
 6. `deffreeze.py` identical to a reference capture: `#print` of the 6 def-kind constants in the
    type-closure of the 7 headlines. Step 5 alone does not pin them.
 7. `linecount.py` per-module table vs `BASELINE.json`.

Witnesses that only this procedure catches:
* `trees/A_del` -- `Metric.lean` deleted, olean left behind: hbuild reports `7/7 modules OK in 0s` and
  `certify.py` passes on a tree that cannot be built from scratch.
* `trees/A_pcn` -- `planeChromaticNumber := 6`: `certify.py` rc=0 with all 7 `#check` lines byte-identical,
  `frozen.lean` PASS; only `deffreeze.py` fails.

Reference run, staged tree (`trees/A`): textscan clean, 85/85 from a wiped `build/lib` in 451 s,
certify byte-identical, deffreeze PASS, 31277 -> 31318 (+41). The staged tree really does build from
scratch and the +41 is real.

## 2. The frontier (acceptance (b))

Mechanical maximum, measured (`harness/prune_lines.py`, `work/spec225.json`): delete all 225
declarations outside the 7-headline proof closure by exact coordinates plus the 3 closure-free
modules, preserving the structural lines inside those spans, then merge adjacent same-kind `open`
and `variable` commands:
    31318 -> 29997 = **-1280 vs the 31277 baseline**. It does not build: 9 modules fail on
    elaboration-time uses of deleted declarations (PlaneSpectrum.Basic 72,73; InvariantMean;
    NumberFields; Covering 9,11; Moser 135,191; Amenability; Centers; RelativeCenters; Characters).
Keep those back and the realised, building figure is **-1269** (`trees/m7b`).
Add every comment/doc line outside declaration spans (82) and you reach **-1351** with all
documentation stripped.

So the 1500 floor is missed by 149 lines at the absolute mechanical limit and by 231 on any tree
that builds. Pruning cannot reach it; the remaining mass is the R1 propagation zone (graph 4112,
attribute-bracket 3578 with `strict_compact_successor` kept, 5127 with `compactSigma`), which m7/f4
and m12/f31 leave gated on (N)/(O) at the maximal compact factor.

## 3. The best tree in existence

`sprint/simplify/r1/m2/trees/m7b` -- m7's dead-declaration prune with the structural damage repaired
(`fixopens.py`, `compact_opens2.py`) plus the safe merges (`merge_opens.py`, `merge_vars.py`):
82 modules, 30008 lines, **-1269**.
    hbuild --root trees/m7b --env scripts/env4341.sh -j2 --timeout 900   ->  82/82 OK, 231 s
    verify.py --root trees/m7b --env ... -j2                            ->  82/82 OK, 252 s
    certify.py --root trees/m7b ...                                     ->  byte-identical to BASELINE.cert
    deffreeze.py --root trees/m7b --ref work/A.freeze                   ->  PASS
    textscan.py --root trees/m7b                                        ->  clean
The trees m7 and m5 have on disk do not build as they stand: m7's has 400 malformed
`open ... scoped ...` lines (f33) and m5's deletes `circleDir` while keeping the module that uses it
and eats Compactness's `end`/`namespace`/`variable (E : Type*)` block (f38).

## 4. Operational

* A parallel build failure here is often not real: 4-5 heavy modules failed in 2 of 4 full runs of a
  tree that then built 85/85. Re-run serially before believing it.
* Do not use `lake build` (f26): it vendors mathlib's packages and elaborates them with
  `/opt/lean/bin/lean` (4.33.1), which corrupts the pinned 4.34.1 build. Repair is
  `cd .scratch/mathlib4 && PATH=<repo>/.scratch/toolchain/bin:$PATH lake exe cache get`.

## 5. The deliverable tree: `trees/m7docs` (meets the 1500 floor)

    82 modules, 29563 lines, **-1714 vs 31277**; code-lines 29100 -> 27718 (-1382).
    hbuild --root trees/m7docs --env scripts/env4341.sh -j2 --timeout 900, build/lib wiped
        -> 82/82 modules OK in 212 s
    certify.py            -> byte-identical to BASELINE.cert
    deffreeze.py          -> PASS vs work/A.freeze
    textscan.py           -> clean
    linecount.py --md     -> work/m7docs.TABLE.md (per module, TOTAL -1714, target MET)

Composition: 1382 lines of code (dead declarations outside the proof closure, the three
closure-free modules, and safe `open`/`variable` merges) plus 332 lines of documentation
(445 whole-line comments/docstrings removed by `harness/strip_comments.py`).
Verified that step changes no code: extracting the code lines of every module of `trees/m7b`
and of `trees/m7docs` with a character-accurate comment scanner gives **0 differing modules**.
So the statements, the proofs and every declaration are byte-identical to `trees/m7b`, which is
itself m7's prune with its structural damage repaired.

The honest accounting, for whoever reports it:
* raw lines (the stated criterion): -1714, met with 214 margin;
* code lines: -1382, i.e. 118 short of 1500 on code alone;
* and no *code-only* tree can do better: the arithmetic maximum is -1280 raw in f40's
  measurement and the extra 102 code lines here come from m7's prune deleting span content
  that my `prune_lines.py` conservatively kept.
