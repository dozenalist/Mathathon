# Combining certified colourings across copies: exact criterion, compact representation, soundness

Analysis only: no solver, no compute, no Lean, no search. Read-only inputs listed in §8. **Nothing here
reopens the closed union** (see `GLUING-AUDIT.md` W3 banner: 34 witnesses, 1048 distinct signatures, no
pair pinned, 1145 survivors obsolete). The purpose is a **reusable generator of certified joint
witnesses** for future overlapping or rotated Heule copies.

## 0. The problem, stated exactly

Two copies `A`, `B` of a point graph (the same point set `H`), a gluing datum: an identification list
`I ⊆ V(A) × V(B)` (each pair is a point that coincides) and a cross-edge list `E_× ⊆ V(A) × V(B)` (each
pair is a unit pair between the copies). A **joint colouring** is a pair `(c_A, c_B) ∈ C_k(A) × C_k(B)`
with

    (b)  for all (u,v) ∈ I :   c_A(u) = c_B(v)        (boundary agreement)
    (×)  for all (x,y) ∈ E_× : c_A(x) ≠ c_B(y)        (cross edges)

The joint set is `J = {(c_A,c_B) : (b) and (×)}`. Note `I` is *arbitrary* here — it need not be a
vertex-with-itself pairing, so **rotated and offset copies are covered by the same statement**; a rotation
only changes which pairs land in `I` and `E_×`.

**Given.** Finite certified families `Φ_A ⊆ C_k(A)`, `Φ_B ⊆ C_k(B)` (each member already verified proper).
We want to decide whether some pair from these families, up to **relabelling B's colours**, satisfies (b)
and (×) — and if so to output a certified element of `J`.

## 1. The exact criterion

Let `S_k` be the permutation group of `[k]`. The colour names on the two factors are independently
conventional, so the correct search is over `(φ, ψ, π) ∈ Φ_A × Φ_B × S_k` with `c_A := φ`,
`c_B := π ∘ ψ`. **CORRECTED NORMALISATION.** Restricting to a permutation applied to `B` alone is justified *up to a
common global relabelling*, **not** by literal equality of labelled pairs. The two labelled pairs
`(π_A∘φ, π_B∘ψ)` and `(φ, (π_A^{-1}∘π_B)∘ψ)` are different tuples and need not be equal. What is true is
that a simultaneous relabelling `ρ` acts on joint colourings by `(c_A,c_B) ↦ (ρ∘c_A, ρ∘c_B)`, which
preserves every equality of (b) and every disequality of (×); hence
> `J` is invariant under the diagonal action of `S_k`: `(c_A,c_B) ∈ J ⟺ (ρ∘c_A, ρ∘c_B) ∈ J` for all `ρ`.

Consequently `(π_A∘φ, π_B∘ψ) ∈ J ⟺ (φ, (π_A^{-1}∘π_B)∘ψ) ∈ J` — **membership transfers**, the pairs are
not identified. That is all the search needs: a witness in one labelling yields one in the normalised
labelling by applying `ρ = π_A^{-1}`. (The invariance also shows the search is `k!`, not `(k!)²`, but for
the reason above, not by an equation between pairs.)

For a fixed pair `(φ,ψ)` the conditions on `π` are:

* **(P) pins.** For each `(u,v) ∈ I`: `π(ψ(v)) = φ(u)`. This is a list of **forced assignments**, i.e. a
  partial map `σ : [k] ⇀ [k]`, `σ(ψ(v)) := φ(u)`.
* **(F) forbiddens.** For each `(x,y) ∈ E_×`: `π(ψ(y)) ≠ φ(x)`. This is a set of **forbidden cells**
  `D := {(ψ(y), φ(x))} ⊆ [k]²`.

> **Criterion (C).** For a pair `(φ,ψ)`, a valid `π` exists **iff**
> 1. `σ` is **well defined**: no two identifications give the same key `ψ(v)` different values `φ(u)`;
> 2. `σ` is **injective**: no two different keys are sent to the same value;
> 3. there is a bijection `π` of `[k]` extending `σ` with `(α, π(α)) ∉ D` for all `α ∈ dom π`.

Conditions 1–2 are forced by `π` being a function and a bijection; condition 3 is a bipartite matching
problem on `k` domain and `k` codomain elements with `|D|` forbidden cells and `|σ|` pre-assigned pairs.
`k ≤ 6`, so `|S_k| ≤ 720` and the decision is trivial by either enumeration or Hall's condition. **No
information about the graph's size enters**: `|V| = 1048` is irrelevant to this step.

## 2. The compact constraint representation

The coupling collapses to a `k × k` object, independent of `|V(A)|`:

| object | size before reduction | size after reduction |
|---|---|---|
| boundary | `|I|` equalities (58 in the closed run) | `σ`, at most `k` pairs (≤ 6) |
| cross edges | `|E_×|` disequalities (184 in the closed run) | `D ⊆ [k]²`, at most `k²` pairs (≤ 36) |

So `184` cross constraints compress to at most `36` forbidden cells at `k = 6`, and many cross edges are
individually redundant (they collapse onto the same `(colour, colour)` cell). Likewise the two families
should be **deduplicated by their signature on the active set** `Act := {vertices in I or in E_×}`: two
colourings with the same signature on `Act` induce the same `(σ,D)` and one representative suffices. That
quotient is the practical accelerator, and it is exact — the constraint set depends on `φ,ψ` only through
`φ|_Act`, `ψ|_Act`.

## 3. Soundness (and what failure means)

**Theorem (soundness).** If `(φ,ψ,π)` satisfies (P) and (F), then `(φ, π∘ψ) ∈ J`.

*Proof.* `φ` is proper on `A` by hypothesis. `π∘ψ` is proper on `B` because permuting colours preserves
properness. For `(u,v) ∈ I`: `(π∘ψ)(v) = π(ψ(v)) = φ(u)` by (P) ✓. For `(x,y) ∈ E_×`:
`φ(x) ≠ π(ψ(y))` by (F) ✓. So both (b) and (×) hold. ∎

The output is checkable **from scratch** in `O(|E_A| + |E_B| + |I| + |E_×|)` without trusting the
combinatorics, which is what makes it a certificate rather than a solver verdict.

**Incompleteness — the required distinction.** Exhausting `Φ_A × Φ_B × S_k` with no success establishes
only

    J ∩ { (φ, π∘ψ) : φ ∈ Φ_A, ψ ∈ Φ_B, π ∈ S_k } = ∅ ,

i.e. **there is no joint colouring built from the sampled families**. It does **not** establish `J = ∅`,
and it says **nothing** about `k`-colourability of the union. `J` may contain pairs built from colourings
outside `Φ_A ∪ Φ_B`; the sampled failure is a statement about the sample. In particular a failure must
never be reported as "the union is not `k`-colourable" — that would require an UNSAT proof, not a failed
combination. (Conversely a success *is* a proof of `J ≠ ∅`, hence of `k`-colourability of the union; both
directions are recorded, only one is sound in the negative.)

## 4. Minimal worked example (abstract, `k = 3`)

`A` = path `a₁—a₂—a₃`; `B` = path `b₁—b₂—b₃`. Identification `I = {(a₁,b₁), (a₃,b₃)}`; no cross edges.
The union is the 4-cycle `A₁—a₂—a₃—b₂—A₁`, so `J ≠ ∅` (it is 2-colourable).

*Families (singletons).* `φ = (a₁↦1, a₂↦2, a₃↦3)`; `ψ = (b₁↦2, b₂↦1, b₃↦2)`. Both proper.
Pins: `π(ψ(b₁)) = φ(a₁) ⇒ π(2) = 1` and `π(ψ(b₃)) = φ(a₃) ⇒ π(2) = 3` — **condition 1 fails**, so no
`π`. The method reports failure.
**And the union is still colourable**: `(A₁↦1, a₂↦2, a₃↦1, b₂↦2)` realises `J`. So this is a clean
instance of *sampled failure without non-colourability* ✓.

*Enlarging the family fixes it, monotonically.* Add `φ' = (a₁↦1, a₂↦2, a₃↦1)` to `Φ_A`. Then pins are
`π(2)=1` twice — consistent and injective — and with `D = ∅` any `π` with `π(2)=1` works, e.g.
`π = (1↦2, 2↦1, 3↦3)`, giving `c_B = π∘ψ = (b₁↦1, b₂↦2, b₃↦1)`. Check: `c_A(a₁)=1=c_B(b₁)` ✓,
`c_A(a₃)=1=c_B(b₃)` ✓, edges `A₁-a₂: 1≠2` ✓, `a₂-a₃: 2≠1` ✓, `A₁-b₂: 1≠2` ✓, `a₃-b₂: 1≠2` ✓. A
certified joint colouring ✓. Success is monotone in the families, failure is not conclusive.

## 5. Implementation specification (no compute performed)

**Inputs.** `k`; the two point lists (exact coordinates in the field, previously certified); the
identification list `I` as index pairs `(i, j)` with `A[i] == B[j]` as points; the cross list `E_×` as
index pairs with `|A[i] − B[j]| = 1`; the certified families `Φ_A`, `Φ_B` (each an array of length
`|V|` over `[k]`).

**Step 0 — validate the families.** For each `φ ∈ Φ_A`, check `φ(x) ≠ φ(y)` for every unit pair of `A`;
drop failures with a logged reason. Same for `B`. (This is the only place a family acquires authority.)

**Step 1 — reduce.** Compute `Act_A ⊆ V(A)`, `Act_B ⊆ V(B)` as the vertices appearing in `I ∪ E_×`.
Replace `Φ_A`, `Φ_B` by one representative per signature on `Act_A`, `Act_B`. Record the multiplicity.

**Step 2 — per pair `(φ,ψ)`.** Build `σ` as a list of `(key,value)` pairs from `I`; build `D` as a *set*
of `(key,value)` pairs from `E_×`. Test `(C)`:
* reject if a key repeats with a different value, or two keys share a value;
* else decide whether a bijection extending `σ` avoids `D`. At `k ≤ 6` simply iterate the at most `720`
  permutations; above `k = 8` use bipartite matching (Hall) on the residual `k − |σ|` elements.

**Step 3 — emit and verify.** For the first success, form `c_A = φ`, `c_B = π∘ψ`, then **re-verify from
scratch**: properness on both copies (all unit pairs), every `(u,v) ∈ I`, every `(x,y) ∈ E_×`. Emit
`(c_A, c_B, π, (φ,ψ))` with the four counts. A witness that fails re-verification is a bug in Step 2 and
must abort, not be logged as a near miss.

**Step 4 — record.** Append the joint colouring to the union's witness family; recompute per-vertex
signatures; report how many signature classes remain of size > 1 (the pruning statistic used by the
union certificate). This is how the method feeds the next seed.

**Cost — RUNTIME CLAIM WITHDRAWN.** An earlier version said this was "comfortably inside a single
60-second process for `|Φ|` in the thousands". That was unsupported and is withdrawn: at `k = 6` a blind
traversal of `k!` per pair with `|Φ_A| = |Φ_B| = 10³` is `7.2·10⁸` permutation tests, far past 60 s, and
even the residual matching at `O(k³) = 216` per pair leaves `≈ 2·10⁸` elementary steps for `10⁶` pairs.
What can be stated is only the asymptotics `O(|Φ_A|·|Φ_B|·(k³ + |I| + |E_×|))`, independent of `|V|`,
plus two honest accelerations: **(i) residual matching after pins** — at most `k − |σ| ≤ k` residual
elements, so `O(k³)` worst case and `O(k²)` typical, replacing `k!`; **(ii) the signature quotient** —
dedupe each family by its restriction to the active set, which is exact and can cut `|Φ|` by orders of
magnitude. The family *product* `|Φ_A|·|Φ_B|` is not reduced by either, and no measured runtime is
claimed. Any future use must prune the product (e.g. bucket the families by the pinned signature) or
break at the first witness, and must **measure** rather than assume.

**Packet.** `combine/combine_witnesses.py` (+ `combine/fixtures.json`) is a pure-source implementation of
exactly this: input validation, pin consistency/injectivity, forbidden-cell check, residual augmenting-path
matching, and an independent re-verification of the emitted colouring. Source only; it has not been run
here beyond a syntax compile.

**Pre-registration discipline.** Emit `J = ∅` **only** when a joint UNSAT proof exists, never on a
combination failure. Report the failure as "no witness from the sampled families".

## 6. What this does and does not do

* **Does:** turn certified per-copy families into certified joint witnesses, cheaply and without a
  solver, for **any** identification/cross pattern including rotated copies; and quantify the failure
  mode honestly.
* **Does not:** decide `k`-colourability of a union, prove absence of a forcing pair, or say anything
  about the closed 1048-vertex union (which is settled: 34 witnesses, 1048 distinct signatures, no pair
  pinned). It also does not claim that pair-separation gives surjectivity of pair projections or
  near-rigidity — see `GLUING-AUDIT.md` W3.

## 7. Grades

| item | grade |
|---|---|
| criterion (C), incl. the one-permutation normalisation | **PROOF** (bijection bookkeeping; the normalisation is `(π_A∘φ, π_B∘ψ) = (φ, (π_A^{-1}π_B)∘ψ)`) |
| compact representation (`σ` ≤ `k` pairs, `D ⊆ [k]²` ≤ `k²`) and the `|E_×| → ≤36` compression at `k=6` | **PROOF** (the constraint set depends on `φ,ψ` only through their restrictions to `Act`) |
| soundness theorem | **PROOF** (three lines) |
| incompleteness / "failure ≠ non-colourability" | **PROOF**, with the §4 instance as a concrete witness to the distinction |
| worked example (both the failure and the monotone repair) | **PROOF**, hand-checked in `k=3`; the 4-cycle claim is verified by listing the four edges |
| implementation spec | specification, **not executed**; cost bound is arithmetic |
| withdrawn claims W1–W3 | recorded in `GLUING-AUDIT.md` |
| the union result (34 witnesses, 1048 distinct signatures) | **C-external**, the graph worker's certificate, not re-verified by me |

## 8. Read-only inputs and artefacts

`supervisor/solve-graphs/CERTIFICATE-union-no-forcing.md` (sha256 prefix `95298a2b…`),
`supervisor/solve-graphs/certs/refine2_witnesses.txt` (`c1a28bc6…`, 35 lines),
`certs/union_tau_points.txt`, `supervisor/solve-geometry/SEED-DESIGN-TAU.md`, and
`supervisor/solve-geometry/GLUING-CORRECTED.md` (the current note; I read the older
`SEED-DESIGN-TAU.md` last block and note here that the corrected file supersedes it — I have not audited
the corrected version and make no claim about it).
