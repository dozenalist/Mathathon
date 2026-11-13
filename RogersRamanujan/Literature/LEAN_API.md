# Lean reference and implementation handoff

Inspected locally on 2026-11-13, not inferred from current online documentation.

## Pinned environment

- `lean-toolchain`: `leanprover/lean4:v4.35.0`.
- `lakefile.toml`: mathlib requirement `v4.35.0`.
- `lake-manifest.json`: mathlib commit
  `56a005855ea17e0b0958f73ec801ae140b0a1679`.
- Root default target: `Mathathon`; its root file was empty at preparation time.
- No project Lean implementation or build verification was added by this
  literature/roadmap update.

## Existing API inspected

The links below pin the same mathlib commit as the checkout.

| File | Observed declarations / use |
| --- | --- |
| [Partition/Basic.lean](https://github.com/leanprover-community/mathlib4/blob/56a005855ea17e0b0958f73ec801ae140b0a1679/Mathlib/Combinatorics/Enumerative/Partition/Basic.lean) | `Nat.Partition n`, `parts : Multiset Nat`, `parts_pos`, `parts_sum`; `DecidableEq`; a `Fintype` instance; `Nat.Partition.restricted` |
| [Partition/Glaisher.lean](https://github.com/leanprover-community/mathlib4/blob/56a005855ea17e0b0958f73ec801ae140b0a1679/Mathlib/Combinatorics/Enumerative/Partition/Glaisher.lean) | Restricted-part generating functions; `Nat.Partition.card_odds_eq_card_distincts`; useful precedent but not Rogers--Ramanujan |
| [Partition/YoungDiagram.lean](https://github.com/leanprover-community/mathlib4/blob/56a005855ea17e0b0958f73ec801ae140b0a1679/Mathlib/Combinatorics/Enumerative/Partition/YoungDiagram.lean) | Available module to inspect if a Durfee route is selected; its detailed API was not audited |

A targeted text search of the local Combinatorics and NumberTheory trees did
not identify a Rogers--Ramanujan implementation. This is not a proof that no
relevant theorem exists elsewhere. Search the pinned checkout before writing
duplicate infrastructure.

## Representation decision

Use `Nat.Partition n` for abstract finite families, or a positive sorted-list
structure for executable maps, with a proved conversion between them. A
multiset stores multiplicity but has no consecutive indices. If defining gaps
on a sorted list, prove that the chosen sorting/representation agrees with
the abstract family; do not pretend `parts` is already a list.

Keep `k` when encoding a partition by a weakly decreasing nonnegative vector.
Trailing zero padding is data in the staircase representation but not a
positive partition. A proof that silently drops `k` cannot establish the
inverse law. Natural-number subtraction also needs inequalities preventing
truncation; alternatively work in integers until nonnegativity is established.

## First proof targets

1. Empty and singleton membership; normalization/conversion preserves weight.
2. Gap inequalities imply `lambda_i >= 2(k-i)+1` in 1-based notation.
3. Staircase subtraction yields a weakly decreasing nonnegative vector and
   changes weight by exactly `k^2`.
4. Adding the staircase is inverse in both directions with padding retained.
5. The same-weight shift `T` yields smallest part at least length; prove its
   inverse and compatibility with staircase coordinates.
6. For a selected candidate, define concrete maps, prove termination and
   membership, then package both inverse laws as an `Equiv`.

Do not replace an executable construction by `Classical.choice` from a
cardinality equality and call that the new natural bijection. A theorem with
unproved input assumptions must retain and disclose those assumptions.

## Build integration and evidence

`RogersRamanujan/Lean/` is outside the existing `Mathathon` module hierarchy.
L and M must explicitly arrange a Lake library/root that includes these
modules. One possible design is a `RogersRamanujan` library with a new
`RogersRamanujan.lean` aggregator importing the proof modules; M owns the root
configuration change and ensures it does not interfere with the other projects.
Confirm Lake's accepted configuration in the pinned environment before editing.

For an individual source, start with the actual command
`lake env lean RogersRamanujan/Lean/<file>.lean`; once imports are integrated,
build the actual project library and root targets. Placeholder filenames above
are planned, not existing files. A default build that omits these modules is
not validation of them.

For a formal milestone, save theorem names, exact command and exit status,
source commit, and `#print axioms` output. No `sorry`, `admit`, `sorryAx`, or
custom unproved axiom may be hidden in a claimed complete result. Explain any
nonstandard trusted computation. Document finite executable checks separately
from all-input proofs; neither the kernel nor a passing build establishes
the aesthetic claim of naturalness.
