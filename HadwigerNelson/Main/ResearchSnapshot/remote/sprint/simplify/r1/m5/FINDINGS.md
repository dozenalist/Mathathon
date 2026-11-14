# m5 / d13 — findings on the deletion instrument, and the fixed-architecture frontier

Everything below is measured on `sprint/simplify/stage/lean` (85 modules, 31 318 raw
lines) and on the unmodified `lean/OAI` baseline (83 modules, 31 277). Scripts are in
`sprint/simplify/r1/m5/`; every number is reproducible with the command given.

## 1. The instrument is unsound as a *line-count* oracle

m10's `declgraph.lean` walks the proof-term closure of the 7 headline declarations and
`analyze.py` prices a route by deleting the route target's **value edges**, then summing
the spans of everything no longer reached. The step "not reached by the proof term ⇒ the
declaration's lines can be deleted" is false.

Witness (Basic.lean, `OAI/Analysis/PlaneSpectrum/Basic.lean`):

| declaration | occurrences in `DECLGRAPH.log` | needed to compile Basic.lean? |
|---|---|---|
| `embed_one`, `embed_mul`, `embedF_one`, `embedF_mul` | 0 | yes |
| `kCoeff_one`, `kCoeff_minusOne` | 0 | yes |
| `coe_imagUnit`, `coe_ofF`, `coe_reF`, `coe_imF` | 0 | yes |
| `scalar_apply`, `jF_apply` | 0 | yes |

They are `rfl` lemmas: `simp [embed_mul]` closes the goal definitionally, so the
*proof term* never mentions the constant, while the *source* does. Removing them gives

```
Basic.lean:74:32: error: Unknown identifier `embed_mul`
```

Check:

```bash
grep -c '\.embed_mul$' sprint/simplify/m10/harness/DECLGRAPH.log    # 0
```

**Consequence for R1.** `harness/ACCOUNTING.md` credits R1 with freeing 4 112
declaration lines, including `Basic` 194, `Factors` 356, `ConditionalLimits` 396,
`ConditionalSelection` 350, `ConditionalSpectrum` 435, `RelativeCenters` 380,
`Approximation` 373. Those modules all *survive* the restructure, so a freed declaration
in them can only be deleted if no surviving declaration of the same module names it.
Inside `Basic` that number is 18, not 194. So 4 112 is an upper bound that does not
survive compilation, and the realised R1 figure has to be re-measured with the
mention-respecting rule below. This matters because 1 500 is the acceptance floor and
R1's margin was quoted as ~2 600.

## 2. The correct rule, and what the fixed architecture is actually worth

A declaration may be cut iff (a) no proof term of a headline reaches it, (b) its name is
never mentioned in the surviving source, (c) it carries no attribute (`@[simp]` …: an
unmentioned `simp` lemma is used implicitly) and (d) it is a proof (`theorem`/`lemma`/
`def`/`abbrev`) — never an `instance`, `structure`, `inductive` or `class`.

Measured on the staged tree:

| rule | declarations | span-lines |
|---|---|---|
| m10's rule (value-edge unreachability only) | 215 | 1 449 |
| + transitive (only dead declarations mention them) | 151 | 1 488 |
| + unmentioned ∧ unattributed ∧ proof-kind | 74 | 702 |
| **+ the compiler as the oracle** (18 modules had to be restored) | — | **190 raw lines realised** |

The last row is the honest number: cutting the 74 and compiling module by module against
the staged oleans restores 18 modules, leaving 31 087 raw lines, i.e. 190 lines below the
baseline. Reproduce:

```bash
python3 sprint/simplify/r1/m5/dead3.py --tree sprint/simplify/r1/m5/work \
    --log sprint/simplify/r1/m5/DG.log
python3 sprint/simplify/r1/m5/cutfix.py --pristine sprint/simplify/r1/m5/work \
    --dst <OUT> --dead sprint/simplify/r1/m5/SAFEDEAD.json \
    --staged sprint/simplify/stage --env sprint/simplify/r1/m5/env.sh
```

Scaffolding, separately: `import` pruning is worth 4 lines, merging adjacent bare `open`
lines 40, collapsing doubled blank lines 36 — 80 in total. So

> **the fixed-architecture ceiling is about 700 span-lines on paper and about 300 raw
> lines with the compiler as the oracle** — an order of magnitude below 1 500.

This confirms m10's verdict (R1 is the only route with margin) but for a sharper reason,
and it also says R1's own 4 112 must be discounted by the mention rule before it is
believed.

## 3. The exact frontier: the mention boundary, not the proof-term boundary

The line where the fixed-architecture zone stops being deletable is not
`relative_singularity_approximation` (Stationary.lean:144/159) — it is met one step
earlier: at every declaration of a surviving module that a surviving proof *names*.
The largest genuinely unmentioned declarations are `Spectral.relative_singularity_limit`
(ConditionalLimits.lean:269, 62 lines, zero occurrences anywhere in the tree) and
`EncodedCollision.collision_from_close_encodings` (PhaseCollision.lean:396, 67 lines) —
both already inside the R1 zone.

## 4. A structural result that shortens any R1 build (also posted as f11)

* `ergodic_wild_fourier` uses `UniversalGood μ q` only at `d = id`
  (Ergodicity.lean:58 is `hgood id measurable_id …`), so a terminal factor exporting
  `GoodId μ p` suffices for the headline; the obligation collapses to the identity.
* With `A = {f ∈ L²(μ) : the K-orbit of f is precompact}`, any `p` with `L²(p) ⊆ A`
  satisfies Theorem A's (H2) for **every** wild `d`: if `d` were `p`-measurable then
  `eval z ∘ d ∈ A`, but (N) at `μ.map d` says that orbit is not precompact. Hence no
  maximality and no compact-over-compact transitivity is needed for (H2), and since `A`
  is L²-closed, chain joins of compact factors are compact for free.

## 5. Files

| file | what |
|---|---|
| `DG.log` | declgraph regenerated on the staged tree (3 538 nodes), 17 s |
| `dead3.py`, `deadmass.py`, `deadmass2.py` | the three dead-set criteria above |
| `transitive.py`, `cut.py`, `applysafe.py`, `cutfix.py` | cutters, with the compiler-repair loop |
| `cluster.py`, `usage.py` | statement-cluster and mention census |
| `SAFEDEAD.json`, `DEAD3.json` | the 74-declaration set and the 126-declaration set |
| `env.sh`, `env_stage.sh` | pinned-toolchain LEAN_PATH, without the baseline olean prefix |
