# AC-conditional finite filter for six-cycle common interfaces, and its exhaustion

**Scope of everything here.** A finite statement about `q ∈ {0,…,5}^6` with `q0 = 0`, six-cycle
interfaces `E_i = {i, (i+1) mod 6}`, labels `C = {0,…,5}`, **conditional on Theorem AC**. It is *not*
an all-angle statement, *not* a plane statement, and *not* `WeakColoring6`.

Grades: **[P]** argument written here; **[C]** exact computation, reproducible by one command;
**[relayed]** from Astra; **[conditional]** depends on AC, which is paper-level and **not**
Lean-checked.

## 1. The AC-conditional filter, derived **[P][conditional]**
Theorem AC (relayed, paper-level, initial independent Astra acceptance): if a finite family
`{K_i}` all approach a common centre `x` in the **same** direction `v`, and each `K_i` excludes a
finite label set `H_i`, and `⋃_i H_i` leaves at most two labels, then `False`.

For a same-direction group at a six-cycle, the indices with `q_i = d` have `v_i = e^{i d π/3}` — one
common direction — and `H_i = E_i`. So:

> **(AC-filter)** for every direction `d`, `|⋃{E_i : q_i = d}| ≤ 3`.

Equivalently: a same-direction group whose cycle edges cover **≥ 4 of the 6 labels** (complement
≤ 2) is forbidden. This is the exact finite shadow of AC — nothing is added to it.

## 2. The fixed `q` named in the consumer note is excluded — twice **[C]**
`q = (0,3,3,3,0,0)`:

| direction | group | `⋃ E_i` | size |
|---|---|---|---|
| `d = 0` | `{0,4,5}` | `{0,1,4,5}` | **4** |
| `d = 3` | `{1,2,3}` | `{1,2,3,4}` | **4** |

Both violate the filter; the `d = 3` group leaves exactly `{0,5}`, matching the consumer note. So
that configuration is impossible for **actual common interfaces** — while remaining, as recorded, a
valid counterexample to the weaker orbitwise/recurrence reduction (the four-state model fails this
stronger source input at the jump of its `{0,5}` choice at `t = 0`).

## 3. Six-orbit constraints used **[relayed → C]**
At each angle `j` (and cell `c`): C1 `P_j ≠ ∅`; C2 `|P_j| ≤ 2`; C3 `P_j ∩ P_{j+1} = ∅` cyclically;
C4 `P_j ⊄ E_i` for every `i`; C5 `P_j` meets `C \ ⋃{E_i : s[i][j] = σ}` for **both** `σ`, where
`s[i][j] = sign cos((c + j − q_i)π/3)`.

**Structural reductions, both exact [P][C]:**
* With six labels every singleton satisfies C4 for no `i`, so C4 kills all singletons: only the
  **9 non-adjacent pairs** survive C4 — `{0,2} {0,3} {0,4} {1,3} {1,4} {1,5} {2,4} {2,5} {3,5}`.
* Since `(c + j) mod 6` only **rotates** the cyclic list of allowed palettes, the six cells are
  equivalent and **one feasibility check per `q`** suffices (a 6× saving, and a reason the result is
  not an artifact of one cell).
* The normalization `q0 = 0` is exactly one representative per **rotation class** (a global shift of
  all `q_i` is the same as relabelling `c`), so `6^6 / 6 = 7776` is the complete space.

## 4. Exhaustive result over the declared space **[C]**
One process, 0.02 s:

| stage | count |
|---|---|
| candidates `q ∈ {0,…,5}^6`, `q0 = 0` | **7776** |
| fail AC filter | 6356 |
| pass AC filter | **1420** |
| **pass AC *and* six-orbit feasible** | **95** |

So AC + the six-orbit constraints cut the space from 7776 to **95 rotation classes**, but **do not
eliminate it**. AC alone is not enough at this stage.

## 5. Certificate: one explicit survivor **[C]**
`q = (0, 0, 1, 3, 3, 4)` passes AC (direction groups `{0,1}`→size 3, `{2}`→2, `{3,4}`→3, `{5}`→2) and
admits the cyclic palette assignment

```
j :  0      1      2      3      4      5
P :  {1,4}  {2,5}  {0,3}  {1,4}  {2,5}  {0,3}
```
adjacent-disjoint at every step including the wrap `P_5 ∩ P_0 = ∅`. Note this uses **three** distinct
palettes on one orbit — consistent with the retraction: the earlier "exactly two palettes" finding was
for `q ∈ {0,3}^6` only, and the wider family admits richer phase behaviour.

## 6. What this says and does not say
* **Does:** with AC as a source, the six-cycle stage has a specific checkable exclusion, the named `q`
  is excluded, and the *joint* filter leaves exactly **95** rotation classes — an exhaustive count over
  a declared finite space, not a partial scan.
* **Does not:** AC is **not** the full `F6` theorem — general direction configurations, including
  **nonaligned** vectors, remain outside it, and its novelty relative to unpublished worker work or the
  literature has **not** been investigated. No all-angle claim, no plane claim, no `WeakColoring6`.
  A single-orbit palette certificate is **not** a global field; palettes here are phase-dependent and
  the certificate is one orbit's worth of data.

## 7. Constraint table — sources and status
| id | relation | source | status |
|---|---|---|---|
| AC | aligned exclusion continua: same approach **direction**, `\|C \ ⋃H_i\| ≤ 2` ⇒ `False` | Astra, paper-level corollary | **initial independent acceptance; NOT Lean-checked** [relayed] |
| AC-filter | `∀d: \|⋃{E_i : q_i = d}\| ≤ 3` | derived here from AC | [P], conditional on AC |
| C1–C5 | six-orbit two-side constraints | Astra finite-interface spec, independently checked in earlier blocks | [relayed → C] |
| G1,G2 | generic contact-ban; `five_support_no_sixty_joint_pair` | local bank SHA `9a904d4d…` | Lean 4.34.1 / mathlib `d13f23b`, standard axioms [relayed] |
| T1 | larger three-centre replacement | target | **PAPER CANDIDATE**, pending independent review and Lean |

## 8. Reproduce
```
cd supervisor/solve-graphs && python3 ac_filter_enum.py     # 0.02 s, sole compute process
```
