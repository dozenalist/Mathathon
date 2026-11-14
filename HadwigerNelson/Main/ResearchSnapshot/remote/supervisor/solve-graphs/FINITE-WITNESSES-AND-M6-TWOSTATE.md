> ## ⚠ PARTIALLY RETRACTED — see `FOUR-STATE-RETRACTION.md`
>
> §4 and §5 of this file claim that "no model with >= 3 distinct palette values exists for m = 6" and that
> "the two-state form is forced". **That is FALSE as a global statement and is withdrawn.** The 4^6
> enumeration ranged over the six angles of a *single* 60-degree orbit for a *single* `q` pattern, so it
> proves only the orbit-local bound. On the whole circle a valid **four-palette** angular model exists
> (`fourstate_verify.py`, ALL CHECKS PASS): each orbit uses 2 palettes, the whole circle uses 4, and no
> single `(J,K)` pair covers all angles. §§1–3 (the constraint table and the four witnesses) stand
> unchanged and are not affected.

# Four finite interface witnesses verified; m6 two-state form is FORCED (not merely available)

**Verdict.** All four Astra witnesses verify under the stated constraints **[C]**. And the
pre-registered relaxation for `m=6` comes out **negative**: **no model with ≥ 3 distinct palette values
exists**, because the finite system admits only 4 palettes and exactly 2 adjacent-compatible pairs, so
every model is a two-valued alternation **[P][C]**. This *validates* the two-state reduction at the
finite-orbit level; it does not refute it.

Grades: **[P]** = argument written here, reviewable; **[C]** = exact combinatorial computation,
reproducible by one command; **[relayed]** = from Astra, not independently established by me.

## 1. Constraint table — every row has its source and quantifier **[relayed → C]**
Labels `C = {0,…,5}`; `m`; `q ∈ {0,3}^m`; `P_j` = palette at angle `j` (`j = 0..5`);
`E_i = {i, (i+1) mod m}`; `v_i = e^{i q_i π/3}`; `u_j = e^{i(t + jπ/3)}`;
`s[i][j] = sign ⟨v_i, u_j⟩ = sign cos(t + jπ/3 − q_i π/3)`.

| id | constraint | source (relayed wording) | quantifier |
|---|---|---|---|
| C1 | `P_j ≠ ∅` | "P_j nonempty" | ∀ j |
| C2 | `|P_j| ≤ 2` | "size ≤ 2" | ∀ j |
| C3 | `P_j ∩ P_{j+1 mod 6} = ∅` | "adjacent P_j disjoint" | ∀ j |
| C4 | `P_j ⊄ E_i` for every `i` | "P_j not contained in any E_i" | ∀ j, ∀ i |
| C5 | `P_j ∩ (C \ U_σ) ≠ ∅` for **both** `σ = ±`, where `U_σ = ⋃{E_i : s[i][j] = σ}` | "both sides require P_j intersects C minus union(E_i on that side)" | ∀ j, ∀ σ |
| ALT | witness shape `P_j = J` (j even), `K` (j odd) | "Palettes alternate J, K" | — |

Nothing beyond these rows is imposed; no constraint was added to force any outcome.

## 2. The four witnesses all pass **[C]**
| m | q | J | K | result |
|---|---|---|---|---|
| 3 | (0,0,0) | {3} | {4} | **PASS** |
| 4 | (0,0,0,0) | {4} | {5} | **PASS** |
| 5 | (0,3,3,0,0) | {0,2} | {5} | **PASS** |
| 6 | (0,3,3,3,0,0) | {0,2} | {3,5} | **PASS** |

Checked at all six angle cells and all six angles: C1, C2, C3, C4, C5 all hold. Note C3 forces
`J ∩ K = ∅` and C2 gives `|J|, |K| ≤ 2`, matching the relayed data.

## 3. Structural lemma: the side-unions are constant in `j` and in the cell **[P][C]**
Because `q_i ∈ {0,3}`, we have `v_i ∈ {+1,−1}`, so
`s[i][j] = a_j · (q_i = 0 ? +1 : −1)` where `a_j = sign cos(t + jπ/3)`. Hence the partition
`{i : s[i][j] = +}` is either `{i : q_i = 0}` or its complement, according to the **single bit** `a_j`.
Since **C5 quantifies over both sides simultaneously**, the conjunction is unaffected by swapping them.
Therefore the side-union data seen by C5 depends only on `q` — not on `j` and not on the angle cell.
Verified computationally: for each `m` the set of side-unions `{U_+, U_−}` is identical across all 6
cells and all 6 angles (output [2]).

This is the reason the answer in §4 is decisive rather than one of six cases: there is only one case.

## 4. m = 6: the ≥ 3-palette relaxation is exhaustively infeasible **[P][C]**
For `m = 6`, `q = (0,3,3,3,0,0)`: the side-unions are `U = {0,1,4,5}` and `V = {1,2,3,4}`, so
`C\U = {2,3}` and `C\V = {0,5}`. C5 with `|P| ≤ 2` forces `P` to meet both `{2,3}` and `{0,5}`, and
since those two sets are disjoint, `|P| = 2` exactly, with one element from each:

```
admissible palettes = {0,2}, {0,3}, {2,5}, {3,5}.
```

C4 holds for all four. Adjacent-disjointness (C3) is then compatible only for the two **diagonal**
pairs:

```
{0,2} — {3,5}      and      {0,3} — {2,5}.
```

Each admissible palette is adjacent-compatible with only its partner, so a cyclic sequence
`P_0…P_5` must alternate inside one diagonal pair. Hence **exactly two distinct palette values**, and
the model is forced to the form `P_j = J, K, J, K, J, K` — the same shape as the accepted witness.

Exhaustively confirmed by enumerating all `|adm|^6 = 4^6` cyclic assignments: **maximum number of
distinct palettes = 2**.

**Answer to the pre-registered question:** *no* model with ≥ 3 distinct palettes and no single fixed
`(J,K)` covering all angles exists for `m = 6`. The two-state form is forced by the constraints, not
chosen by the witness.

## 5. Contrast across m — the effect appears exactly at the full orbit **[C]**
| m | \|admissible\| | max distinct palettes in a cyclic model |
|---|---|---|
| 3 | 15 | 6 |
| 4 | 11 | 6 |
| 5 | 8 | 5 |
| **6** | **4** | **2** |

At `m ≤ 5` multi-valued palette models abound; only at `m = 6` — the complete 60° orbit — does the
system collapse to two states. So the two-state structure is a property of the **closed orbit**, which
is consistent with (and helps explain) why the failure of the whole-circle version reported in the
relay is a *global/measurable* obstruction rather than a finite one.

## 6. What this does and does not say
* **Does:** the four finite witnesses are correct **[C]**; and for `m = 6` under these constraints the
  two-state alternation is the **only** solution, so no finite multi-state model exists at the full
  orbit **[P][C]**.
* **Does not:** these are **finite orbit models, not actual whole-circle trace fields** [relayed]. The
  generic `States.two_state_impossible` forbids a whole-circle measurable `Bool` flipping at 60° with
  real-state representations `J, K` and ≤ 2 labels outside `J ∪ K`. **An exact angular model is not a
  global colouring**, and the **absence of a global two-state form does not certify realizability** of
  anything. No claim of palette transport, global completion, or `chi(ℝ²)` is made.
* **Consumer requirement.** Anything using §4 must take C5 as *"both sides"* (as relayed) together with
  `q ∈ {0,3}^m`. If the intended semantics makes the side-union depend on `j` — e.g. if C5 is required
  only for the side matching a designated sign rather than for both — then §3's lemma fails, §4 no
  longer applies, and the ≥ 3-palette question must be re-put. I did **not** invent that variant.

## 7. Reproduce
```
cd supervisor/solve-graphs && python3 m6_twostate_check.py    # ALL CHECKS PASS, ~3.8 s, sole compute process
```
Log: `logs/m6_twostate.out`.
