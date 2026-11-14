# Direction B — Lean `T` bridge (cycle 3, member m2)

Scope: formalise the same-weight shift

    T(lam)_i = lam_i - k + 2i - 1        (1 <= i <= k, k = lam.length)
    T^-1(b)_i = b_i + k - 2i + 1

for `RogersRamanujan/Main/CLAIMS.md` row **RR-C006** ("Shift `T : D_n -> B_n`
(smallest part >= length), both laws", previously TESTED_FINITE).
`import Init` only; no Mathlib; no `lake`; no `sorry`; no new axiom.

## Files

| file | role |
| --- | --- |
| `ShiftT.lean` | **the verified artefact** (generated, self-contained, 511 lines) |
| `block1.lean`, `block2.lean` | the new material, as written (the required bullets; the order bonus) |
| `build.py` | assembles `ShiftT.lean` = `RogersRamanujan/Lean/Staircase.lean` (sha256 `c7acbcd7…b280`, unmodified slice) + `block1.lean` + `block2.lean` |
| `check_encoding.py` | independent Python check that the truncating `Nat` encoding is the intended integer map, `n <= 20` |
| `types.log` | `#check` output: the exact type of every theorem |
| `verify.log` | full stdout of the verification run |

`ShiftT.lean` is a single self-contained target so that no `.olean` for
`RogersRamanujan.Lean.Staircase` is needed (this VM has none). The
`Staircase.lean` part is copied byte-for-byte by `build.py`; only its trailing
`#print axioms` lines are re-emitted at the end of the file.

## Exact commands

```sh
cd /workspace/nucleus/work/projects/p-9021becf3f0d47a89b3f3c794c1e872b/repo
lean RogersRamanujan/Lean/cycle3/ShiftT.lean          # exit 0, all axioms clean
python3 RogersRamanujan/Lean/cycle3/check_encoding.py # exit 0, 10/10 PASS
```

Lean 4.33.1 (`lean --version`: `Lean (version 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6)`).
Wall clock ~1 s per run. The supervisor's pinned toolchain is 4.35.0; only
4.33.1 is installed here, so this is verified on 4.33.1 and **not** re-verified
on 4.35.0.

## Encoding, and why it is faithful

    def shiftT   (l : List Nat) : List Nat := (subStair l).map (fun x => x + l.length)
    def shiftInv (l : List Nat) : List Nat := (addStair l).map (fun x => x - l.length)

`shiftT` is literally "subtract the staircase `mu` of `Staircase.lean`, then add
the constant `k`", i.e. `T(lam)_i = mu_i + k`: obligation (iv) holds by
construction, and the construction is the *printed formula* redistributed.
Everything rests on `Nat` subtraction in `subStair` not truncating. The
kernel-checked statement of that is `RR127.addStair_subStair`
(`addStair (subStair lam) = lam` for `Pos`/`Gap`): if any staircase subtraction
truncated, `addStair` could not recover `lam`. `check_encoding.py` additionally
checks the pointwise identity `shiftT_lean lam == lam_i - k + 2i - 1` in the
integers for every `lam` in `D_n`, `n <= 20` (all 197 objects).

## Theorems proved — exact types

Types below are verbatim `#check` output (`types.log`).

### (i) the sum is preserved exactly

```
RR127.Shift.sum_shiftT : ∀ {lam : List Nat}, RR127.Pos lam → RR127.Gap lam →
  (RR127.Shift.shiftT lam).sum = lam.sum
```
Proof: `(T lam).sum = (subStair lam).sum + k*k` (`sum_map_add`) and
`lam.sum = (subStair lam).sum + k*k` (`sum_addStair` + `addStair_subStair`),
so the two agree. Note no inequality is used: `k*k` cancels, which is the
telescoping `2*(1+…+k) - k*k - k = 0`. Supporting:
`sum_map_add`, `addStair_map_add`.

### (ii) the image satisfies the `B_n` membership condition

```
@RR127.Shift.mem_shiftT_ge : ∀ {lam : List Nat} (x : Nat), x ∈ RR127.Shift.shiftT lam → lam.length ≤ x
```
Honest note: given the encoding this half is cheap (`x = mu_i + k`), since `Nat`
entries are `>= 0`. The *substantive* half of "`T` lands in `B_n`" is that the
image is a partition (`WeakDec`), which the task did not list but which the
`D_n -> B_n` claim needs; it is proved below.

### (iii) both inverse laws, on the correctly stated subtypes

```
@RR127.Shift.shiftInv_shiftT : ∀ {lam : List Nat}, RR127.Pos lam → RR127.Gap lam →
  RR127.Shift.shiftInv (RR127.Shift.shiftT lam) = lam

@RR127.Shift.shiftT_shiftInv : ∀ {b : List Nat}, (∀ (x : Nat), x ∈ b → b.length ≤ x) →
  RR127.Shift.shiftT (RR127.Shift.shiftInv b) = b
```
Length is retained as data throughout: the constant is `l.length` of the very
list, and `length_shiftT : (shiftT l).length = l.length`,
`length_shiftInv : (shiftInv l).length = l.length` hold unconditionally.
Supporting: `map_add_sub_cancel`, `map_sub_add_of_le`,
`subStair_addStair_map_sub` (the last one needs no hypothesis: `omega` covers
the truncation).

### (iv) `T(lam)_i = mu_i + k`

```
RR127.Shift.mem_shiftT_iff : ∀ (l : List Nat) (x : Nat),
  x ∈ RR127.Shift.shiftT l ↔ ∃ y, y ∈ RR127.subStair l ∧ x = y + l.length
RR127.Shift.shiftT_entry : ∀ (l : List Nat) (i : Nat),
  (shiftT l)[i]? = Option.map (fun x => x + l.length) (subStair l)[i]?
RR127.Shift.shiftInv_entry : ∀ (l : List Nat) (i : Nat),
  (shiftInv l)[i]? = Option.map (fun x => x - l.length) (addStair l)[i]?
```

### Bonus: `T : D_n → B_n` really is a bijection

`WeakDec` = weakly decreasing list; `DGap` = `{l // Pos l ∧ Gap l}`;
`BSmall` = `{b // WeakDec b ∧ ∀ x ∈ b, b.length ≤ x}` = the `B_n` side.

```
RR127.Shift.weakDec_shiftT : ∀ {l : List Nat}, RR127.Pos l → RR127.Gap l →
  RR127.Shift.WeakDec (RR127.Shift.shiftT l)
@RR127.Shift.shiftInv_pos : ∀ {b : List Nat}, (∀ (x : Nat), x ∈ b → b.length ≤ x) →
  RR127.Pos (RR127.Shift.shiftInv b)
@RR127.Shift.shiftInv_gap : ∀ {b : List Nat}, RR127.Shift.WeakDec b →
  (∀ (x : Nat), x ∈ b → b.length ≤ x) → RR127.Gap (RR127.Shift.shiftInv b)
RR127.Shift.toD_toB : ∀ (l : RR127.Shift.DGap), RR127.Shift.toD (RR127.Shift.toB l) = l
RR127.Shift.toB_toD : ∀ (b : RR127.Shift.BSmall), RR127.Shift.toB (RR127.Shift.toD b) = b
RR127.Shift.weight_toB : ∀ (l : RR127.Shift.DGap), (RR127.Shift.toB l).val.sum = l.val.sum
```
so `toB : DGap → BSmall` and `toD : BSmall → DGap` are mutually inverse, and
`T` carries weight `n` to weight `n`. Supporting lemmas (all with exact types
in `types.log`): `weakDec_map_add`, `weakDec_subStair`, `addStair_pos`,
`weakDec_addStair`, `addStair_gt`, `pos_map_sub`, `gap_map_sub`.

## `#print axioms` — every theorem

Command: `lean RogersRamanujan/Lean/cycle3/ShiftT.lean` (the file ends with 34
`#print axioms` lines). Output, complete:

* `[propext]` only: `map_add_sub_cancel`, `map_sub_add_of_le`, `length_shiftT`,
  `length_shiftInv`, `shiftT_entry`, `shiftInv_entry`, and (base)
  `subStair_addStair`.
* `[propext, Quot.sound]`: `sum_map_add`, `addStair_map_add`,
  `subStair_addStair_map_sub`, `sum_shiftT`, `mem_shiftT_ge`, `mem_shiftT_iff`,
  `shiftInv_shiftT`, `shiftT_shiftInv`, `weakDec_map_add`, `weakDec_subStair`,
  `weakDec_shiftT`, `addStair_pos`, `weakDec_addStair`, `addStair_gt`,
  `pos_map_sub`, `gap_map_sub`, `shiftInv_pos`, `shiftInv_gap`, `toD_toB`,
  `toB_toD`, `weight_toB`, and (base) `head_bound`, `addStair_subStair`,
  `sum_addStair`, `weight_subStair`, `subStair_nonneg`.
* no axioms at all: the seven `by decide` witnesses
  `witness_T_531`, `witness_T_41`, `witness_T_641`, `witness_inv_443`,
  `witness_gap_needed`, `witness_not_injective`, `witness_weakDec_needed`.
* `sorryAx`: **absent**. `Classical.choice`, `native_decide`, custom axioms:
  **absent** (grep over `ShiftT.lean`: the only hit for `sorry` is the prose of
  the inherited `Staircase.lean` header).

So the axiom set is exactly the event-allowed `[propext, Quot.sound]`, the same
set the supervisor recorded for `Staircase.lean`.

## What is *not* proved, and the false-as-posed case

* Nothing was weakened silently. No statement from the brief turned out false;
  three plausible *strengthenings* are false, and are recorded as kernel-checked
  negative controls (`by decide`, no axioms):
  * `witness_gap_needed : (shiftT [1, 3]).sum ≠ [1, 3].sum` — `Pos` alone
    does not give (i); `[1,3]` is positive but not a gap partition and `T`
    there computes `[2,4]`, weight 6 against 4. So `Gap` is not decoration.
  * `witness_not_injective : shiftT [0] = shiftT [1] ∧ [0] ≠ [1]` — `Pos` is
    needed for injectivity (`T` collapses `[0]` and `[1]`).
  * `witness_weakDec_needed : ¬ Gap (shiftInv [2, 5])` — the entry bound
    `b.length ≤ every entry` alone is *not* enough to put `shiftInv b` into
    `D_n`: `[2,5]` has length 2 and every entry `>= 2`, but
    `shiftInv [2,5] = [3,4]` is not a gap list. Hence `shiftT_shiftInv` needs
    only the entry bound (it is a one-sided inverse), while `shiftInv_gap`
    needs `WeakDec` as well. Anyone quoting (iii) should keep that asymmetry
    visible.
* Positive witnesses: `shiftT [5,3,1] = [3,3,3]`, `shiftT [4,1] = [3,2]`,
  `shiftT [6,4,1] = [4,4,3]`, `shiftInv [4,4,3] = [6,4,1]` (all `by decide`).
* **Not** proved here: anything about `phi`/`psi`/BZ82 (directions A/C), and
  anything about alternating-path termination. This file is only RR-C006.
* The order lemma `weakDec_subStair` is the same proof as
  `RogersRamanujan/Lean/StaircaseOrder.lean` (cycle 2, by Main), restated so
  this file is one self-contained target. If Main prefers, `StaircaseOrder.lean`
  can be imported instead and the copy deleted.

## Independent numeric cross-check (`check_encoding.py`, exit 0)

```
PASS  encoding: shiftT_lean == integer formula T(lam)_i = lam_i-k+2i-1 on all D_n, n<=20
PASS  image: T(D_n) subset of B_n (descending, smallest part >= k), n<=20
PASS  weight: sum(T(lam)) == sum(lam) on all D_n, n<=20
PASS  injectivity: T is injective on D_n, n<=20
PASS  inverse laws: shiftInv(shiftT lam) == lam and shiftT(shiftInv b) == b
PASS  bijection: T(D_n) == B_n as sets, for every n<=20
PASS  counts: |D_n| == |B_n| for n<=20 (both enumerated independently)
PASS  control: [1,3] is Pos but not Gap and T loses weight there
PASS  control: T collapses [0] and [1] (Pos is needed for injectivity)
PASS  control: [2,5] meets the entry bound but is not descending, and shiftInv [2,5] is not a gap list

total: 10 checks, 0 FAIL
objects: 197 D-objects, 197 B-objects for n <= 20
```
This is a check of the *encoding*, not a substitute for the proof; the proof is
in `ShiftT.lean`.

## Proposed change to `Main/CLAIMS.md` (Main to apply; I did not edit outside my folder)

RR-C006: "Shift `T : D_n -> B_n` (smallest part >= length), both laws" —
`TESTED_FINITE` → **LEAN_VERIFIED**, evidence
`RogersRamanujan/Lean/cycle3/ShiftT.lean` (Lean 4.33.1, exit 0, axioms
`[propext, Quot.sound]`, no `sorryAx`), statement `RR127.Shift.toD_toB` /
`RR127.Shift.toB_toD` / `RR127.Shift.weight_toB`. Caveat to keep in the ledger:
verified on 4.33.1 only; the repository pin is 4.35.0 and this VM cannot run it.
Also worth adding the asymmetry recorded above (`shiftT_shiftInv` needs only the
entry bound; `shiftInv_gap` needs `WeakDec`) so no later reader over-claims.
