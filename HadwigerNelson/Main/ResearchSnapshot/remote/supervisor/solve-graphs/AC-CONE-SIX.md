# Conditional cone filter: the six survivors, their symmetry classes, and every witness

**Status of the cone.** The cone extension of AC is a **NEW ASTRA PAPER CANDIDATE with independent
review in progress** (early geometry check positive, final verdict pending). Everything below is
**conditional on it and is not banked**. Grades: **[C]** exact computation, **[P]** written
argument, **[relayed]** from Astra/parent, **[conditional]** rests on the un-refereed cone.

**Scope.** Finite statement about `q ∈ {0,…,5}^6` with `q0 = 0`, six-cycle interfaces
`E_i = {i,(i+1) mod 6}`, labels `C = {0,…,5}`. No all-angle claim, no plane claim, no
`WeakColoring6`. The AC-conditional base (174 survivors) and the local fixed three-centre Lean result
are unchanged; Lemma 6.7 = `five_support_step_ban` retained.

## 1. The cone filter, applied independently **[C][conditional]**
Filter used: for every cyclic adjacent direction pair `{d, (d+1) mod 6}`,
`|⋃{E_i : q_i ∈ {d,(d+1)}}| ≤ 3`.

I rebuilt the base from scratch (not from saved files) and obtained **174** AC-survivors, matching the
audited count. Applying the cone filter:

| stage | count |
|---|---|
| declared space | 7776 |
| AC survivors | 174 |
| **cone filters** | **6** |

The six are

```
(0,0,2,2,4,4)  (0,0,4,4,2,2)  (0,1,2,3,4,5)  (0,2,2,4,4,0)  (0,4,4,2,2,0)  (0,5,4,3,2,1)
```

which agree **exactly** with the parent's list (`set(cone) == set(parent)`, checked). Applying the
cone filter directly to **all 7776** gives the **same six**, so nothing is hidden outside the 174.

## 2. Classification under the certified symmetries **[C]**
All **24** maps `q ↦ norm(ε·q∘σ)` (σ dihedral on positions, ε = ±1) that were verified last block to
preserve feasibility also preserve the **cone-filtered** table (`cone_ok(φ(q)) = cone_ok(q)` and
`feas(φ(q)) = feas(q)` for all 7776). So the cone filter is symmetry-invariant and the classification
is legitimate.

The six form exactly **2 orbits**:

| orbit | members | pattern | size |
|---|---|---|---|
| **A** | `(0,0,2,2,4,4)`, `(0,0,4,4,2,2)`, `(0,2,2,4,4,0)`, `(0,4,4,2,2,0)` | `(2,2,2)` | 4 |
| **B** | `(0,1,2,3,4,5)`, `(0,5,4,3,2,1)` | `(1,1,1,1,1,1)` | 2 |

These are precisely representatives #10 and #11 of the previous 12-orbit classification: **the cone
filter kills 10 of the 12 orbits and leaves these two.**

## 3. Complete witness enumeration: FORCES vs ADMITS **[C]**
For each of the six I enumerated **all** cyclic witnesses `(P_0,…,P_5)` satisfying C1–C5 and cyclic
adjacency — not one example.

| q | orbit | #witnesses | palettes occurring over **all** witnesses | three-disjoint-pair words | verdict |
|---|---|---|---|---|---|
| (0,0,2,2,4,4) | A | **1** | {0,3},{1,4},{2,5} | 1 of 1 | **FORCES** |
| (0,0,4,4,2,2) | A | **1** | {0,3},{1,4},{2,5} | 1 of 1 | **FORCES** |
| (0,2,2,4,4,0) | A | **1** | {0,3},{1,4},{2,5} | 1 of 1 | **FORCES** |
| (0,4,4,2,2,0) | A | **1** | {0,3},{1,4},{2,5} | 1 of 1 | **FORCES** |
| (0,1,2,3,4,5) | B | **4** | all nine admissible pairs | 2 of 4 | **ADMITS** |
| (0,5,4,3,2,1) | B | **4** | all nine admissible pairs | 2 of 4 | **ADMITS** |

**The answer is not uniform.**

* **Orbit A forces the three-disjoint-pair word.** Each of its four members has a **unique** witness,
  and that witness is exactly the partition `{0,3},{1,4},{2,5}` — e.g. for `(0,0,2,2,4,4)`:
  `{1,4},{2,5},{0,3},{1,4},{2,5},{0,3}`. Uniqueness makes this a *forcing*, not a choice.
* **Orbit B merely admits one.** It has **four** witnesses, of which two are three-disjoint-pair words
  and **two are not**. The non-forcing witnesses use six **distinct** palettes, e.g.
  `{1,3},{2,4},{3,5},{0,4},{1,5},{0,2}` (and its rotation by three), which uses no pair of the
  canonical partition at all. So for orbit B the three-disjoint-pair word is one option among several,
  and **no argument from these constraints alone can conclude it**.

Up to cyclic rotation orbit B has exactly **two** distinct cyclic words: one of the partition type and
one genuinely different. That is the obstruction to forcing.

## 4. Explicit full-circle step palettes **[C][P]**
Critical phases: `t ≡ (2k+1)π/6`, six points, where some `cos(t + jπ/3 − q_iπ/3)` vanishes. These
divide the circle into **six open sign cells**. On cell `c` — i.e. `t ∈ ((2c−1)π/6, (2c+1)π/6)` — the
sign pattern is constant, and for a witness `W = (W_0,…,W_5)` the palette at angle `j` is
`W_{(c+j) mod 6}`; the **base-direction step palette** is `t ↦ W_c`.

| orbit | q | base-direction step palette, `c = 0..5` |
|---|---|---|
| A | (0,0,2,2,4,4) | {1,4} {2,5} {0,3} {1,4} {2,5} {0,3} |
| A | (0,0,4,4,2,2) | {1,4} {0,3} {2,5} {1,4} {0,3} {2,5} |
| A | (0,2,2,4,4,0) | {0,3} {1,4} {2,5} {0,3} {1,4} {2,5} |
| A | (0,4,4,2,2,0) | {0,3} {2,5} {1,4} {0,3} {2,5} {1,4} |
| B | (0,1,2,3,4,5) | {0,3} {1,4} {2,5} {0,3} {1,4} {2,5} *(one of 4; see §3)* |
| B | (0,5,4,3,2,1) | {0,3} {2,5} {1,4} {0,3} {2,5} {1,4} *(one of 4)* |

**Boundary-null qualification.** The step function is defined on the complement of the six critical
points, a **Lebesgue-null** set. At a critical phase some sign is `0`, so the side-unions `U_σ` are
not defined by sign and the constraints say nothing there; the model is silent on those six phases and
they carry no measure. Nothing here is claimed at the boundary.

**Existence vs all possible palettes.** For orbit A the step palette above is the **only** one (unique
witness). For orbit B it is **one of four**; presenting it as "the" palette would overstate, and §3
lists all four.

## 5. What this does and does not establish
* **Does**, conditionally: the cone filter cuts 174 → **6**, in **2** orbits; orbit A **forces** the
  three-disjoint-pair word, orbit B only **admits** it. That is a precise, checkable statement about a
  declared finite space.
* **Does not:** nothing here proves the cone. The cone extension is a **paper candidate under
  independent review**, treated as conditional and **not banked**. No claim about all angles, the
  plane, or `WeakColoring6`. No AC-axis, no mixed-orientation filter — mixed orientations do not share
  a common strip, so AC and its cone version do not apply to them and no constraint was invented.
* **Consumer.** This is the six-colour common-interface stage: orbit A is closed by the cone plus the
  orbit constraints; **orbit B is not** — it survives with a non-partition witness, so a further input
  is needed exactly for the permutation family.

## 6. Reproduce
```
cd supervisor/solve-graphs && python3 cone_filter_6.py     # 0.47 s, one process, one thread
```
