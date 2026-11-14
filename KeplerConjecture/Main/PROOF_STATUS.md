# Proof status — one page

Written at review `0523`. Every line is a claim id. **Read this before quoting anything from
`CLAIMS.md`**: the ledger is 120+ entries with a history of retractions, and this page says what is
actually standing.

## The one-line answer

**No proof of `δ ≤ π/√18`, and no improvement on any published bound.** The project's live route is
a *two-cell* inequality, and its qualitative form is proved; its quantitative form is not. The
single missing object is an explicit constant.

## Proved here

| what | id | notes |
| --- | --- | --- |
| Every Voronoi cell of every Barlow packing has volume `√32` | `C094` | repaired at `C104`; the load-bearing step is an exact two-polytope computation, independently re-derived |
| The contact polytope satisfies `K ⊆ B(v,√2)`, both local types | `C104` | exact arithmetic in `Q(√2,√3)`, interval-certified signs |
| The cut condition ⟺ transfer existence | `C093` | two independent proofs; four defects repaired at `D18` |
| Two adjacent dodecahedral centres are impossible, **for all twists** | `C112` | arc cover, zero gaps; supersedes a sampled grid |
| Same, for centre separation `< 6/√5 = 2.6832816`, and sharp | `C116` | |
| `σ₀ > 2V_dod` (the pair functional exceeds twice the dodecahedral volume) | `C108` | **non-explicit**; compactness |
| Monotone bridge: pair constant `K` ⟹ `δ ≤ 8π/(3K)` | `C106`, `C107` | `K = 2V_dod` reproduces `0.754697399337` exactly; `K = 2√32` reproduces `π/√18` |
| The dodecahedral bound is implied by the trivial inball bound for `d ≥ 2.1967082` | `C119` | locates the route: it is needed only on `2 ≤ d < 2.1967082` |
| E's payer fixture reproduced to `1e−15`, and its family scanned | `C118`, `C120` | independent of E's code |
| **A one-pair proof** that two adjacent dodecahedral centres are impossible | `C128` | one pair has a violation set of `135.09° > 72°`, so it meets every coset; hand-checkable |
| **An explicit `δ₀` candidate** `3.76·10⁻³` (`C142`, conditional on one lemma `L1`; `L2` proved) — gives a rate in the contact density `ρ_ε`, **no uniform improvement** (`C143`) | `C142`/`C143` | `G11` open until `M-CERT-002` returns; `M-CERT-002` pinned (1 CPU / 1 GiB / 120 s) |
| **Pair chain audited link by link** (`C141`): ten links, no gap, no circularity; the only open dependency is `G11` | `C108`–`C141` | `C124` is `PENDING_REVIEW`, **not** reviewed |
| **No contact-density hypothesis needed**: `δ < 0.754697399337` strictly for every saturated packing | `C124` | two-case split (`2(1+D_ε)·|M|` counting with `D_ε ≤ (3+ε)³−1` and an explicit `O(R²)` boundary term — `C132` — vs the inball bound); `ρ_ε > 0` is *not* assumed; the two-dodecahedra exclusion is **orientation-free** (`C133`) |
| **Explicit stability**: `≤ 12`-face cell with all neighbours `≥ 2ρ` has `vol ≥ V_dod·ρ³` | `C121` | the first *explicit* stability bound here; at `ρ = 1.045` it gives `b(v) < 0` with `12%` margin |

## Conditional, non-explicit, or open

| what | status | why it matters |
| --- | --- | --- |
| `(L)`: pair bound `≥ 2√32` | **open** (E's conjecture) | would give `π/√18` outright |
| An explicit `δ₀ > 0` | **open** | the only thing between `C108` and a *number* |
| A `≤ 20`-face circumscribed-polyhedron bound at `c ≥ 4.958`, and whether an isolated cell can have `> 12` faces | **open** (`C122`) | the two finite-dimensional sub-problems that would close the singleton case outright |
| `ρ_ε > 0` (density of close pairs) | **no longer a hypothesis** — removed by `C124` | was `G13`; the strictness no longer depends on it |
| `σ₀` attained by a legal configuration | n/a | the infimum is attained in the compactified local space only |
| Emptiness of the dodecahedral equality case | **closed on a sound proof** (`C124`) — was retracted at `C113` for the invalid average-to-pointwise step; the new argument has no such step | `G14` |
| Equality in `(L)` implies Barlow | **not claimed** | Barlow ⟹ equality only (`C106`) |
| Generic `shell_check` soundness | **suspended** | `G12`; a soundness argument is owed |
| Novelty of the two-cell inequality | **not established** | a search found nothing usable |

## What is *not* a bound

Nothing in this project improves `0.754697399337` for all packings. The best certificate is
`Δ ≤ 0.779966216777`, which is **not** an improvement on the published `0.779747`. Any statement of
the form "packings with such-and-such a property are strictly below X" is **conditional and
non-quantitative** and must not be called a new packing bound (`C113`, `C117`).

## The single most useful sentence

The pair route's remaining gap is **not** a matter of the constant being too small: by `C108` any
positive excess over `2V_dod` improves the bound, so there is no threshold to clear. What is missing
is an **explicit value** for that excess, and extracting one is equivalent to a stability version of
Hales–McLaughlin — which the primary source does not provide (`C115`).

## Cost reality check

Hales–McLaughlin's own proof — the closest precedent for any multi-cell tightening — is
**Kepler-scale**: hypermap classification, several hundred linear programs, an interval-arithmetic
prover, and a local-deformation argument (`C117`, read from the primary source). So there is no
evidence that proving `(L)` would be cheap. What is defensible is narrower: *if* `(L)` were proved,
the remaining step to `π/√18` is the elementary bridge of `C106`.
