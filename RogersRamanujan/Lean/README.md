# Lean (L) -- RR127

## Verification command and result

```sh
lean RogersRamanujan/Lean/Staircase.lean     # exit 0, ~14 s, no output
```

`#print axioms` for all six theorems reports `[propext, Quot.sound]` only, which
is inside the event's allowed set (`propext`, `Classical.choice`,
`Quot.sound`). No `sorry`, no `admit`, no `sorryAx`, no custom axiom.

| theorem | statement |
| --- | --- |
| `RR127.head_bound` | `Pos (a::rest) -> Gap (a::rest) -> 2*rest.length+1 <= a` |
| `RR127.addStair_subStair` | `addStair (subStair l) = l` (positive gap partitions) |
| `RR127.subStair_addStair` | `subStair (addStair l) = l` (unconditional) |
| `RR127.sum_addStair` | `(addStair l).sum = l.sum + l.length * l.length` |
| `RR127.weight_subStair` | `lam.sum = n -> (subStair lam).sum = n - lam.length * lam.length` |
| `RR127.subStair_nonneg` | every staircase coordinate of a positive gap partition is `>= 0` |

## Two environment limitations, both blocking for a "full" Lean claim

1. **Lean version mismatch.** `lean --version` is **4.33.1**, while
   `lean-toolchain` pins `v4.35.0` and `lake-manifest.json` names mathlib
   `56a005855ea17e0b0958f73ec801ae140b0a1679`. The kernel-checked evidence above
   is therefore *not* the pinned toolchain's. Re-running on 4.35.0 is a
   prerequisite for quoting these theorems in a submission.
2. **`import Mathlib` does not elaborate here.** A one-line
   `import Mathlib` file exceeded 240 s wall with 1.5 s user and 27 s sys: the
   6.4 GB olean import is being read from disk against 15 GB RAM with 0 GB free
   and 7 GB available. Consequently `Staircase.lean` imports only `Init` and
   uses only `omega` and `simp` (`ring` is not available in core Lean).
   **No `lake build` is claimed, and none was run.**

## What is *not* formalized (dependency table)

| Obligation | Why it matters | Status |
| --- | --- | --- |
| `subStair` is weakly decreasing | the other half of "mu is a partition" | computational only (checker) |
| `Nat.Partition` bridge | the repo pin is `Nat.Partition`, which is a `Multiset` without consecutive indices | not started |
| `T` and `B_n` (= smallest part >= length) | bridges to BZ82/BP06 notation | not started |
| BZ82 `phi`/`psi` definitions | would let a kernel check replace RR-C007's finite test | not started, and blocked by D-3 |
| root library integration in `lakefile.toml` | `RogersRamanujan/Lean/` is outside the `Mathathon` hierarchy | not done; `Mathathon.lean` is empty, so the default target validates nothing |

The last row is the one to fix first: adding a `RogersRamanujan` lib to
`lakefile.toml` is a root-build edit owned by Main and must be done together with
a working `import Mathlib`, which limitation 2 currently prevents.
