# Step 1 decided: at k = 6 the tightened interface CSP is satisfiable, and (C4)+(C5) are vacuous

Member m10, direction d2, finding f1. This answers the mission's Step 1 decisive question —
*"with (C4) and (C5) added, is there ANY satisfiable (l, sign matrix) at k = 6?"* — in the
affirmative: for every `ℓ` there are satisfiable instances, and in the strong form that
`(C4)+(C5)` remove **no** satisfiable instance at all — the tightened SAT locus equals m5's.

## 1. Theorem B (the tightening is vacuous at k = 6)

Fix `k = 6`, `ℓ ∈ {3,4,5,6}`, a sign matrix `σ ∈ {±1}^{6×ℓ}`, and the paper's `O_i`, `I_i`
(Lemma 8.1). Consider six palettes `P_0,...,P_5 ⊆ {0,...,5}` under `(C1)-(C5)`.

**Lemma B0 (shrink).** If a palette `P` satisfies `P ∩ O ≠ ∅` and `P ∩ I ≠ ∅`, then `P`
contains a palette `Q` with `1 ≤ |Q| ≤ 2`, `Q ∩ O ≠ ∅`, `Q ∩ I ≠ ∅`.

*Proof.* If `P ∩ O ∩ I ≠ ∅` pick `c` there and take `Q = {c}`: it meets `O` and `I`.
Otherwise `P ∩ O` and `P ∩ I` are both nonempty and disjoint, so pick `a ∈ P ∩ O`,
`b ∈ P ∩ I`; then `a ≠ b`, and `Q = {a,b}` meets both and has size 2. ∎

Note `B0` needs **no palette bound at all** (not `|P| ≤ 3`, not `|P| ≤ k−3`): it holds for
every `k`, and its hypotheses are exactly `(C2)` at that position. Machine-checked:
`work/Shrink.lean`, `theorem shrink` (axioms `propext, Classical.choice, Quot.sound`,
no `sorry`).

**Theorem B.** For every `ℓ` and every `σ`: `IS(6,ℓ,σ)` is satisfiable **iff**
`IS(6,ℓ,σ) + (C4) + (C5)` is satisfiable.

*Proof.* Apply `B0` independently at each of the six positions (no palette bound is needed
even to get `(C1)` back: `|Q_i| ≤ 2 ≤ 3` and `Q_i ≠ ∅`). Since `Q_i ⊆ P_i`, the
disjointness `(C3)` is preserved (`Q_i ∩ Q_{i+1} ⊆ P_i ∩ P_{i+1} = ∅`), and `(C1),(C2)` are
`B0`'s conclusions. In the resulting model no palette is a 3-set, so (C4) holds (a
complementary pair of palettes has both sizes equal to 3) and (C5) holds
(`#{i : |P_i|=3} = 0 ≤ 3`). The converse is trivial. ∎

Machine-checked form: `work/Shrink.lean`, `theorem tightened_model` — from palettes meeting
`(C2)` at the six positions with `(C3)` between consecutive ones it produces palettes with
`(C1)`, `(C2)`, `(C3)`, `(C4)` (`∀ i j, Q i ∪ Q j ≠ univ`) and `(C5)` simultaneously.
Note the statement does not mention the sign matrix at all: the only thing used about `O_i`,
`I_i` is that the palette meets them.

**Theorem B′ (the palette bound is never binding, `k >= 5`).** For every `k >= 5`, every
`ell >= 3` and every sign matrix: `IS(k,ell,sigma)` is satisfiable **iff** it has a model with
`|P_i| <= 2` for all `i`. *Proof.* One direction is trivial (`2 <= k-3` for `k >= 5`, and
`B0` preserves `(C2)`, `(C3)`). For the other, shrink any model coordinatewise with `B0`.
Consequences: the upper palette bound in `(C1)` never reduces the satisfiability locus at
`k >= 5`; `(C4)` and `(C5)` are vacuous; and **no satisfiable instance at `k = 6` needs a
ternary palette** — the table above exhibits a binary model at every one of the
`36+216+225+177 = 654` satisfiable geometries (`max2 = plain` in all four rows).

**Corollary B1 (no UNSAT branch).** For every `ℓ ∈ {3,4,5,6}` there is a sign matrix — in
fact, for `ℓ = 3,4`, *every* one of the `6^ℓ` sign matrices — at which the tightened system
is satisfiable. Hence the mission's branch "UNSAT for every `ℓ` and every sign matrix" is
empty, and `χ ≥ 7` cannot follow from `(C1)-(C5)`.

**Corollary B2.** `(C5)` is implied by `(C3)+(C4)` alone. *Proof.* Four ternary positions
in a 6-cycle contain two adjacent ones; adjacent palettes are disjoint by `(C3)`, and two
disjoint 3-sets in `Fin 6` are complementary, which `(C4)` forbids. ∎ So the tightening's
whole content is `(C4)` — and by Theorem B `(C4)` too is vacuous at `k = 6`.

**Remark (why this is not an artefact of the model class).** `B0` is a statement about the
constraints `(C1),(C2)` and is independent of `σ`, of `ℓ`, and of any further hypothesis
about the colouring. Its content is that the admissible sets `O_i`, `I_i` are unions
`(cycle labels with a sign pattern) ∪ U`, so a palette can always satisfy both requirements
on two labels or fewer. Any strengthening `Φ` of `(C1)-(C3)` that is *preserved by shrinking
palettes* (`Φ(P) ⇒ Φ(Q)` for `Q_i ⊆ P_i`) and that holds on binary models is therefore
vacuous at `k = 6`; `(C4)` and `(C5)` are both of that shape. `Φ` can only bite if it is
false on every binary model — see `INDUCTION.md` §7 (P1)–(P5).

## 2. The exhaustive check (independent encoder)

`work/tightened_table.py` re-implements the whole object from the paper's definitions
(§8's `O`/`I` paragraph, Lemma 8.1, display (8.1)) and does **not** import or copy m5's code.
Every instance is decided by a DFS model search (enumerating palettes position by position,
enforcing `(C4)`/`(C5)` incrementally), and each extracted witness is re-checked by a
literal `validate()` that tests `(C1)`…`(C5)` member by member. Independently of both,
Theorem B is a proof, and its combinatorial core is machine-checked in Lean. The sign table is computed with `sympy`
(sign of `cos(mπ/3)`, exact) rather than hardcoded.

Calibration (my encoder vs m5's published table, `c_0 = 0` normalisation used by both):
`k=4,ℓ=3: 0/36`, `k=4,ℓ=4: 0/216`, `k=5,ℓ=3: 36/36`, `k=5,ℓ=4: 14/216`, `k=5,ℓ=5: 0/1296`
— all reproduced, including the `14/216`.

`k = 6`, over all `6^(ℓ-1)` sign matrices (`c_0 = 0`; a global rotation by `π/3` is a
symmetry of the sign matrix, and `interface_csp12.py` confirms the twelve-position version
gives the same counts):

| `ℓ` | geometries | `(C1)-(C3)` SAT | with all `|P_i| ≤ 2` | tightened `(C1)-(C5)` | SAT but not tightened |
|-----|-----------|-----------------|----------------------|-----------------------|-----------------------|
| 3 | 36   | 36  | 36  | **36**  | 0 |
| 4 | 216  | 216 | 216 | **216** | 0 |
| 5 | 1296 | 225 | 225 | **225** | 0 |
| 6 | 7776 | 177 | 177 | **177** | 0 |

So the tightened table is *identical* to m5's. Verified witnesses (each re-checked by
`validate()`, i.e. literally `(C1)`…`(C5)` member by member):

    ℓ=3  cells (0,0,0)          {3} {4} {3} {4} {3} {4}
    ℓ=4  cells (0,0,0,0)        {4} {5} {4} {5} {4} {5}
    ℓ=5  cells (0,0,0,3,3)      {5} {1,4} {5} {1,4} {5} {1,4}
    ℓ=6  cells (0,0,0,3,3,3)    {1,4} {2,5} {1,4} {2,5} {1,4} {2,5}

For `ℓ = 3,4` the *alternating two-outsider model* `{ℓ}{ℓ+1}{ℓ}{ℓ+1}{ℓ}{ℓ+1}` was checked
against all 216 resp. 1296 sign matrices (`work/vacuity.py`, part A): 0 violations. This is
the model family of `(P1)` in `INDUCTION.md` §7.

## 3. What this settles and what it does not

* Settles the mission's Step 1 question: **YES, there are satisfiable instances**, at every
  `ℓ`, so no `(l, sign matrix)` is UNSAT-tightened at `ℓ = 3,4` and none of the 225/177
  previously-SAT instances is lost. The strengthening round needs a `(C6)` outside the
  shrink-closed class.
* Does **not** give `χ ≥ 7`: by `INDUCTION.md` §5 (Corollary A′) that would need UNSAT, and
  by `INDUCTION.md` §4 even an UNSAT answer would need the missing `k = 6` cyclic-centre
  theorem.
* Consistency check with m8's A.E. COLLAPSE: a relaxation of the palette system is SAT
  whenever the palette system is SAT, so SAT here is consistent with both `χ = 6` and
  `χ = 7`; there is no contradiction to report, and none of the mission's §5 alarm applies.

## 4. Check commands

    cd .ultramath/smwfk0ybk/m10
    python3 work/tightened_table.py   # table above, 0.8 s, writes work/tightened_table.json
    python3 work/vacuity.py           # part A (1512 geometries, alternating model)
                                      # part B (m5's four witnesses vs (C1)-(C5))
                                      # part C (encoder calibration vs m5's k=4,k=5 table)
    lean work/Shrink.lean             # B0, the six-position shrink, (C4), (C5): machine-checked,
                                      # `tightened_model`, axioms propext/Classical.choice/Quot.sound,
                                      # no `sorry`, 2 s on Lean 4.33.1 + /opt/mathlib
