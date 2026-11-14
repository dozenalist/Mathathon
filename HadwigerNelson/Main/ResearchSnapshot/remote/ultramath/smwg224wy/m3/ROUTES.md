# Route table beyond R1, and where the deletable zone stops (m3 / d7)

All figures recomputed here from `sprint/simplify/m10/harness/DECLGRAPH.log` and a
`spans.py` run on the **staged** tree (85 modules, 31318 raw lines; baseline 31277 / 83).
Nothing below is copied from `ACCOUNTING.md` without being reproduced first.

    # reproduce the shared figure, byte for byte
    python3 sprint/simplify/m10/harness/analyze.py free \
        OAI.PlaneFiveColor.Spectral.exists_terminal_factor \
        OAI.EuclideanFiveColor.CodedMax.exists_maximal \
        --keep OAI.EuclideanFiveColor.CompactTower.strict_compact_successor
    # -> freed 404 of 3538 declarations, 4112 lines

    # my scripts (this directory)
    python3 .ultramath/smwg224wy/m3/spans.py-driven runs, see the files listed at the end

## 1. The engine you keep decides the prize

`exists_terminal_factor` is reproved either by the `CompactTower` engine (D1) or by
maximality over `CompactFunctions.compactSigma` (D2).  The harness's `free` keeps a
named declaration *with its proof cone*, so `--keep` is exactly "the replacement still
uses this engine".  Dropping `exists_terminal_factor` + `CodedMax.exists_maximal`:

| engine kept | freed decl lines (graph) | freed decl lines (+ attribute closure) |
|---|---|---|
| `CompactTower.strict_compact_successor`  (D1 / R1) | **4120** | **3578** |
| `CompactFunctions.compactSigma`  (D2) | **5135** | **4590** |
| `compactSigma` + the 6 join/algebra lemmas | 5084 | 4547 |
| nothing (absolute bound) | 5690 | 5145 |

`--keep` cost of each engine, in lines that cannot be deleted
(drop the two targets, keep exactly one declaration with its proof cone; freed = 5690 − cost):

| declaration the replacement needs | keep-cost (lines) |
|---|---|
| `CompactTower.strict_compact_successor` | **1578** |
| `OrbitFactor.compact_orbit_extension` | 905 |
| `CompactFunctions.compact_of_measurable_compactSigma` | 606 |
| `CompactFunctions.compactSigma` | 563 |
| `CompactFunctions.compact_iUnion` | 543 |
| `CompactFunctions.compact_descend` | 111 |
| `CompactFunctions.compact_of_l2_approximation` | 68 |
| `SeparableZorn.exists_maximal` | 59 |
| `CompactFunctions.at_of_finite` | 39 |
| `CompactFunctions.compact_shift` | 28 |

So the whole cost of a `compactSigma`-style replacement is one big leaf
(`compactSigma`, 563 — the join of compact *functions*, unavoidable for maximality)
plus a handful of tens-of-lines lemmas.  The 1578-line `CompactTower.strict_compact_successor`
is the single most expensive thing a replacement can need, and no replacement needs it
if it takes the sigma-algebra supremum instead of an ordinal tower.

**D2 dominates D1 by ~1000 freed lines in every accounting.**  Keeping the tower buys
nothing that `compactSigma` does not buy more cheaply.

## 2. The deliverable is measured in raw lines, not declaration spans

`analyze.py` sums *declaration spans*.  A module that empties loses its whole file, so
its preamble (imports, namespace, `open`, instances) goes too; and the three
closure-free modules can be dropped outright.  `realised.py` adds both back:

| engine kept | decl lines | + preamble of emptied modules | + closure-free modules | = realised raw lines | tree after (31318 −) |
|---|---|---|---|---|---|
| `strict_compact_successor` (D1) | 4120 | 157 | 198 | **4475** | 26843 |
| `compactSigma` (D2) | 5135 | 157 | 198 | **5490** | 25828 |
| nothing | 5690 | 201 | 198 | 6089 | 25229 |
| **attribute fixpoint** — `strict_compact_successor` (D1) | 3578 | 101 | 198 | **3877** | 27441 |
| **attribute fixpoint** — `compactSigma` (D2) | 4590 | 101 | 198 | **4889** | 26429 |
| **attribute fixpoint** — nothing kept | 4590 | 101 | 198 | 4889 | 26429 |

`--attr` in `realised.py` closes the freed set over the attribute/instance closure to a
fixpoint (it keeps back whatever the graph dropped that carries a global attribute).
The fixpoint ceiling is 4590 decl lines whatever the explicit keep set: `compactSigma`
itself is inside the attribute closure, so a replacement that needs only
attribute-carrying lemmas costs nothing beyond the bracket.

Sensitivity to the Zorn engine: if the replacement still needs
`CodedMax.exists_maximal`, D1 falls from 4120/3578 to **3924/3396** declaration lines
(realised 4279/3695) and D2 from 5135/4590 to **4919/4391** (realised 5274/4690).
Nothing in this paragraph is close to 1500.

So even the pessimistic accounting of the cheapest architecture clears the 1500-line
target by a factor of 2.5 (D1) or 3.2 (D2), and the pessimistic accounting with the
Zorn engine kept clears it by 2.4 (D1) or 3.1 (D2).

## 3. The shared graph is incomplete: freed-span figures are upper bounds

`DECLGRAPH.log` has **no edge for a use through a global attribute set**.  Evidence
that is a build, not an opinion:

* 213 declarations lie outside the closure (1314 span lines).
* deleting them + the 3 closure-free modules gives a 29743-line tree that **fails at
  level 0** with 8 root errors.  Example: `PlaneSpectrum/Basic.lean`, `def j`, whose
  `map_mul'` is `by simp only [embed_mul, ...]`; `grep embed_mul DECLGRAPH.log` returns
  nothing at all, while `def j` is a node.  Same shape in `InvariantMean:44`,
  `NumberFields:59`, `SmallArcs:159`, `Covering:34`, `Moser:130`, `Amenability:65`,
  `Centers:39`.
* the attribute closure (`bracket.py`) keeps back 19 attributed/instance declarations
  (89 lines) inside R1's freed set, of which `Centers` 17 and `PhaseEncoding` 12 lie in
  modules R1 claims to *empty*.  Those two "modules emptied" claims need a build; the
  other side of the ledger (`PhaseCollision`, `SmallArcs`, `Approximation`) is clean.

**Consequence.** Do not certify a deletion from the graph.  Keep every declaration that
carries an attribute or is an `instance`, or close the graph over the attribute sets,
and confirm by `hbuild.py`.  The bracket column above is the conservative, defensible
figure.

Second hazard, for anyone who trims by span: `spans.py` runs a declaration to the line
before the next one, so a span **swallows every command in between** — `variable`,
`open scoped`, `attribute`, `local instance`, `section`/`end`.  Deleting a span
silently removes those and breaks later proofs in the same file in ways that look
unrelated.  Clip span ends at those keywords.

## 4. Where the remaining zone stops

On top of R1 (graph accounting, `scan.py marginal`), the marginal gains, largest first:

| next thing reproved | extra freed lines |
|---|---|
| `CompactTower.strict_compact_successor` (drop the tower engine as well) | **1517** |
| `OrbitFactor.compact_orbit_extension` | 854 |
| `finitary core` lemmas: `Arithmetic.uniform_selection` 613, `FiveCenter.*` 630/616 | — |
| `ergodic_wild_fourier` (Theorem 2.3 from scratch) | 6037 |
| `residual_fourier` | 7215 |
| `no_proper_five_coloring_algebraic` (i.e. the headline) | 13249 |

The zone stops at `exists_terminal_factor`'s consumer: `Ergodicity.lean:52`
(`ergodic_wild_fourier`) needs exactly one thing from the restructure —
`IsWild (differenceLaw (μ.map q) (condDistrib id q μ))` — so
**everything only used to produce that statement is deletable, and nothing above it is.**
The compact-factors tower machinery is worth 5690 graph / 5145 bracket; the Fourier and
plane-topology cones above `Ergodicity.lean` are not reachable by any restructure of the
terminal factor (6037+ requires a second, independent proof of Theorem 2.3, and
13249 is the headline itself).  Within that, the only structural threshold left is the
1570-line tower engine: keep it and the ceiling is 4120/3578, drop it and it is
5690/5145.

## 5. Files

* `scan.py` — route scan (`single`, `marginal`, `free`) in-process on m10's graph.
* `realised.py` — raw-file accounting: declaration spans + emptied-module preambles +
  closure-free modules.  `--md` prints a per-module table.
* `bracket.py` — attribute/instance closure bracket.
* `ownercheck.py`, `deadcheck.py` — are "dead" declarations textually referenced from a
  live declaration's span (`SAFE.json` / `REVIEW.json`)?
* `trim.py` — the mechanical trimmer used for the level-0 failure above.
* `build2.log`, `build3.log` — the failing builds that support §3.

## 6. The purely mechanical route, measured, and why it falls short

Before touching the restructure I tried the zero-proof route: delete every declaration
that lies outside the closure, plus the three closure-free modules.

* all 213 (1314 span lines): tree 29743 lines, **build fails**, 8 level-0 modules.
* only the 103 with no attribute and no textual occurrence inside a live declaration's
  span (979 lines): tree 30086 lines, **build fails** on 4 level-0 modules
  (`Basic`, `Fourier`, `SmallArcs`, `PhaseEncoding`) — all through `simp`/instance
  uses the graph never recorded.
* after fixing the span-tail clipping (a span swallows `variable`, `open scoped`,
  `attribute`, `local instance`, `section`/`end`): 1147 span lines, tree 29971 lines
  (82 modules), still 6/82 modules building (`build4.log`).

Conclusion: a span-based mechanical trim cannot certify anything in Lean, because
(1) the graph is blind to attributes and instances and (2) `simp` sets are global, so
"this declaration is never mentioned" says nothing about a proof in another module.
The realised mechanical floor is ~1300 lines and it does not build without individual
repair; it is **not** a substitute for the restructure and not additive to it as a
block (the restructure also removes declarations that the mechanical pass keeps).

## 7. Deletion lists a builder can apply directly

`candidates.py` writes, for a route, every declaration the route frees as
`module:line-end name`, sorted by module, with the attribute closure kept:

* `CANDIDATES_D1.txt` — 206 declarations, 3578 span lines, 11 modules
  (keep `CompactTower.strict_compact_successor`).
* `CANDIDATES_D2.txt` — 249 declarations, 4590 span lines, 13 modules
  (keep `CompactFunctions.compactSigma`).

Per-module predicted savings (bracket, D1): PhaseCollision 445, ConditionalSpectrum 426,
ConditionalLimits 396, Approximation 381, RelativeCenters 357, ConditionalSelection 350,
Factors 342, SmallArcs 290, Centers 233, PhaseEncoding 212, Basic 146.
Add the preamble of the modules that empty completely (PhaseCollision 26, SmallArcs 32,
Approximation 43 by the stage layout) and the 198 closure-free lines.

Numbers to check against, in the order the certificate asks for them:
`len(linecount.py)` total = 31318 − 4475 = 26843 (graph) or 31318 − 3877 = 27441
(bracket); baseline 31277, so 4434 or 3836 lines under.
