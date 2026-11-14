# `combine/` — pure-source witness combination packet

Source only. Nothing here has been executed except `python3 -m py_compile` (a syntax check, no algorithm
run, no benchmark). Prepared for later review; the mathematical contract is in
`../audit-amplifier/WITNESS-COMBINATION.md`.

| file | role |
|---|---|
| `combine_witnesses.py` | library + one bounded entry point `python3 combine_witnesses.py fixtures.json` |
| `fixtures.json` | nine tiny fixtures with **expected outcomes** — the specification |

## What the entry point does

For one gluing datum it validates the inputs, then searches the product of the two certified colouring
families for a colour permutation `π` making one pair satisfy the boundary equalities and the cross
disequalities, and emits an independently re-verified joint colouring. Exit code 0 iff every fixture
agrees with its expected outcome. Bounded: it iterates only over the fixtures, never over a graph.

## Design decisions worth reviewing

1. **Validation confers authority, and it is the first thing that runs.** A family member that is not a
   proper colouring, a wrong-length vector, or a colour outside `[k]` rejects the whole call. There is no
   path by which an unvalidated colouring contributes to a witness.
2. **Seed-level vs pair-level failures are separated.** `SEED_LEVEL` reasons (`BAD_INDEX`,
   `DUPLICATE_INDEX`, `MISSING_BOUNDARY`, `EXTRA_BOUNDARY`, `SEED_INCONSISTENT`, `FAMILY_NOT_PROPER`,
   `FAMILY_BAD_SHAPE`) abort; the per-pair reasons (`PIN_INCONSISTENT`, `PIN_NOT_INJECTIVE`,
   `PIN_FORBIDDEN`, `NO_MATCHING`) only skip that pair and are tallied in `pair_failures`.
3. **`MISSING_BOUNDARY` needs an external certificate.** Completeness of the identification list cannot be
   checked combinatorially, so the caller must pass `coincident` (the full certified coincidence set) and
   the validator checks `I == coincident`. That is the one input whose provenance is *not* internal.
4. **Residual matching, not `k!` traversal.** After the pins only `k − |σ|` elements remain, so the
   perfect-matching step is augmenting paths on a residual bipartite graph (≤ `k×k` cells), `O(k³)`.
5. **The emitted witness is re-verified from scratch** by `verify_joint`, which shares no code with the pin
   or matching logic. If the two disagree the call returns `internal_inconsistency` — a bug signal, never
   a "near miss".
6. **Duplicates are rejected, not silently deduped** (`F4`): a repeated index pair signals a malformed
   geometric pipeline upstream, and swallowing it would hide that.

## The distinction the packet must never blur

`no_witness` / `sampled_families_only` means *the sampled families contain no joint colouring*. It is
**not** a proof that the union is not `k`-colourable. Fixture `F1` is the standing example: the two
singleton families clash (`π(2)=1` and `π(2)=3`), yet the union is the 4-cycle
`A₀—a₁—a₂(=b₂)—b₁—A₀`, which is 2-colourable. Enlarging `Φ_A` by one colouring (`F2`) produces a witness
with an explicit `π`, so success is monotone in the families while failure is inconclusive.

## Fixture summary (expected data, hand-traced)

| fixture | expected | why it is in the set |
|---|---|---|
| `F1_4cycle_negative_sample` | `no_witness` / `sampled_families_only` | sampled failure with a colourable union |
| `F2_4cycle_enlarged_family_succeeds` | `witness` | same seed, one more colouring, success |
| `F3_cross_edge_forces_a_nonidentity_permutation` | `witness` | forbidden cell is what forces `π(2)≠2` |
| `F4_duplicate_cross_edge_entry` | `seed_rejected` / `DUPLICATE_INDEX` | malformed input |
| `F5_cross_edge_on_an_identified_pair` | `seed_rejected` / `SEED_INCONSISTENT` | seed not colourable |
| `F6_missing_boundary_entry` | `seed_rejected` / `MISSING_BOUNDARY` | incomplete identification list |
| `F7_improper_family_member` | `seed_rejected` / `FAMILY_NOT_PROPER` | unvalidated colouring |
| `F8_pin_lands_in_a_forbidden_cell` | `no_witness` / `sampled_families_only` | pair fails at the pin/forbidden check |
| `F9_bad_index` | `seed_rejected` / `BAD_INDEX` | out-of-range index |

`F5`'s `Φ_B` is also improper; the seed-level check fires first, which is the intended order.

## Not in scope

No claim about the closed 1048-vertex union (settled: 34 witnesses, all signatures distinct, no pair
pinned). No colourability decision. No runtime claim: see the withdrawal in `WITNESS-COMBINATION.md` §5 —
the family *product* is not reduced by the two accelerations and must be pruned or measured.
