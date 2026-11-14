# Shared measurement + verification harness (m10, direction d4)

All paths are relative to the repo root. Nothing here writes outside
`sprint/simplify/m10/` (and the scratch tree you point `--root` at).

## 1. Line counts (cheap, no build)

```bash
python3 sprint/simplify/m10/harness/graph.py count                 # per module, sorted
python3 sprint/simplify/m10/harness/linecount.py \
    --base sprint/simplify/m10/harness/BASELINE.json --root <TREE> --md
```
`BASELINE.json` is the frozen measurement of the unmodified `lean/OAI`:
**31277 raw lines / 29100 non-comment, non-blank lines in 83 modules**.
`linecount.py` prints the per-module before/after table and exits non-zero
below the 1500-line target, so it is usable as a CI gate.

## 2. Build one tree (one toolchain)

```bash
python3 sprint/simplify/m10/harness/hbuild.py --root <TREE> --env scripts/env4341.sh -j2
```
Topological, parallel, writes `<TREE>/lean/build/lib`. `--fresh` wipes first,
`--only MOD` builds just that module's cone. Baseline: 83/83 modules, 348 s of
module time sequentially under 4.34.1. **Use `-j2` at most** — 16 members share
4 cores.

`<TREE>` need only contain `lean/OAI/**`; the mathlib side comes from `--env`
(pinned: `scripts/env4341.sh`; stock: omit `--env` and rely on the ambient
`LEAN_PATH` for Lean 4.33.1 + `/opt/mathlib`).

## 3. Statement + axiom certificate

```bash
python3 sprint/simplify/m10/harness/certify.py --root <TREE> --env scripts/env4341.sh \
    --out /dev/stdout
```
Runs two Lean files against the tree:
* `.certify_gen.lean` — `#check @T` and `#print axioms T` for the 7 headline
  declarations (prints `[propext, Classical.choice, Quot.sound]` on the baseline);
* `frozen.lean` — the 7 headline statements written out **verbatim**
  (`¬ ∃ c : ℂ → Fin 5, ∀ x y : ℂ, ‖x-y‖ = 1 → c x ≠ c y`, etc.) each closed by the
  tree's own declaration. A restructure that adds a hypothesis, changes
  `ProperColoring`, or swaps a side of `proper_iff_weak` fails here.

Diff the output against `BASELINE.cert`. 4 s on a built tree.

## 4. What counts as a deliverable

`(1)` per-module table from `linecount.py`, total ≥ 1500 lines,
`(2)` `hbuild.py` exit 0 under the pinned toolchain,
`(3)` `certify.py` exit 0 with output equal to `BASELINE.cert`,
`(4)` the same under stock 4.33.1 (port patch `m8/patches2/all.patch`).
