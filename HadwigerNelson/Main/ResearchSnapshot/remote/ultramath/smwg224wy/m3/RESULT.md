# m3 / d7 — route search beyond R1, and the measured ceiling

Direction: find deletions outside the R1 zone, quantify them, and say exactly where the
deletable zone stops.  Everything here is recomputed on the staged tree
(85 modules, 31318 raw lines; baseline 31277) from `sprint/simplify/m10/harness/`.
The shared figure was reproduced first, byte for byte:

    python3 sprint/simplify/m10/harness/analyze.py free \
        OAI.PlaneFiveColor.Spectral.exists_terminal_factor \
        OAI.EuclideanFiveColor.CodedMax.exists_maximal \
        --keep OAI.EuclideanFiveColor.CompactTower.strict_compact_successor
    # freed 404 of 3538 declarations, 4112 lines; empties PhaseCollision, PhaseEncoding,
    # SmallArcs, Centers                                        -> matches ACCOUNTING.md

## Result 1 — the architecture, not the proof, sets the prize

`--keep NAME` = "the replacement still uses NAME with its proof cone".  Dropping
`exists_terminal_factor` + `CodedMax.exists_maximal`:

| engine kept | freed decl lines (graph) | keep-cost | freed, attribute fixpoint |
|---|---|---|---|
| `CompactTower.strict_compact_successor` (D1) | 4120 | 1578 | 3578 |
| `OrbitFactor.compact_orbit_extension` | 4785 | 905 | — |
| `CompactFunctions.compactSigma` (D2) | 5135 | 563 | 4590 |
| nothing | 5690 | — | 4590 |

D2 is worth ~1015 more freed lines than D1 in both accountings.  `compactSigma` really
is the lattice top (Functions.lean:652, `[instance_reducible] def compactSigma`,
`compactSigma_le`, join by `compact_iUnion`), so D2's engine is already in the tree.
The only two expensive leaves are `strict_compact_successor` (1578) and
`compact_orbit_extension` (905); every other lemma a replacement might need costs
28–111 lines (`compact_shift` 28, `at_of_finite` 39, `SeparableZorn.exists_maximal` 59,
`compact_of_l2_approximation` 68, `compact_descend` 111).

## Result 2 — realised raw-line accounting

`analyze.py` sums declaration spans.  The deliverable is raw file lines, so an emptied
module also loses its preamble (imports/namespace/open), and the three closure-free
modules go entirely.  `realised.py` adds both:

| route | decl lines | emptied preambles | closure-free | realised raw lines | tree after |
|---|---|---|---|---|---|
| D1 graph | 4120 | 157 | 198 | 4475 | 26843 |
| D1 fixpoint | 3578 | 101 | 198 | 3877 | 27441 |
| D2 graph | 5135 | 157 | 198 | 5490 | 25828 |
| D2 fixpoint | 4590 | 101 | 198 | 4889 | 26429 |
| D1, Zorn engine kept | 3396 | 101 | 198 | 3695 | 27623 |
| D2, Zorn engine kept | 4391 | 101 | 198 | 4690 | 26628 |

Against the 31277 baseline: 4434 (D1 graph), 3836 (D1 fixpoint), 4848 (D2 fixpoint).
Smallest number anywhere in this table is 3695 — 2.4× the 1500 target.

## Result 3 — the shared graph is not a use-graph (blocks naive deletion)

`DECLGRAPH.log` records explicit constants in the elaborated value, not the global
attribute sets.  `grep embed_mul DECLGRAPH.log` is empty although `def j`'s
`map_mul'` is `by simp only [embed_mul, ...]`.  Consequences, all build-tested:

* deleting all 213 declarations outside the closure (+3 modules) gives 29743 lines and
  fails at level 0 in 8 modules (`build2.log`);
* the attribute fixpoint keeps back 19 declarations / 89 lines inside R1's freed set,
  of which `Centers` 17 and `PhaseEncoding` 12 lie in modules R1 claims to empty —
  those two "modules emptied" claims are graph-only and need a build;
* a span-based mechanical trim cannot be certified at all: spans swallow the commands
  between declarations (`variable`, `open scoped`, `attribute`, `local instance`,
  `section`/`end`), and `simp` sets are global, so "never mentioned" says nothing.
  Best mechanical attempt: 29971 lines, 6/82 modules building (`build4.log`).

## Result 4 — where the zone stops

On top of R1 the only remaining structural threshold is the tower engine itself
(+1517, i.e. 5690 graph / 4590 fixpoint).  Above that, `ergodic_wild_fourier` from
scratch is worth 6037 and `residual_fourier` 7215, but both need a second, independent
proof of Theorem 2.3; 13249 is the headline itself.  The zone stops at
`Ergodicity.lean:52`: the restructure must supply exactly
`IsWild (differenceLaw (mu.map q) (condDistrib id q mu))` and nothing above it is
deletable.

## Deliverables in this directory

| file | what |
|---|---|
| `ROUTES.md` | the full table, per-module savings, the frontier, hazards |
| `TABLE_D1.md`, `TABLE_D2.md` | per-module predicted deletion (module / decls / lines / file lines) |
| `CANDIDATES_D1.txt`, `CANDIDATES_D2.txt` | every freed declaration as `module:line-end name`, 206 and 249 entries |
| `scan.py` | `free` / `single` / `marginal` route scan in-process on m10's graph |
| `realised.py` | raw-file accounting (`--attr` = attribute fixpoint, `--md` = per-module table) |
| `candidates.py` | writes a deletion list for a route |
| `bracket.py` | the attribute/instance closure bracket |
| `ownercheck.py`, `deadcheck.py` | textual cross-check of "dead" declarations (`SAFE.json`, `REVIEW.json`) |
| `trim.py`, `trim2.py` | the mechanical trimmer (first version, corrected span-tail clipping) |
| `build1..4.log` | the builds that support Result 3 |

Check commands:

    cd <repo>
    python3 sprint/simplify/m10/harness/analyze.py free \
        OAI.PlaneFiveColor.Spectral.exists_terminal_factor \
        OAI.EuclideanFiveColor.CodedMax.exists_maximal \
        --keep OAI.EuclideanFiveColor.CompactFunctions.compactSigma     # 5135
    python3 .ultramath/smwg224wy/m3/realised.py \
        OAI.PlaneFiveColor.Spectral.exists_terminal_factor \
        OAI.EuclideanFiveColor.CodedMax.exists_maximal \
        --keep OAI.EuclideanFiveColor.CompactFunctions.compactSigma --attr
    # -> 4590 declaration lines, +101 +198, realised 4889; tree 31318-4889 = 26429
