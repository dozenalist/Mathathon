# Retraction of the global ≥3-palette impossibility, and verification of the four-state model

## 1. Retraction (mine, and it is a real error)
Last block I concluded, and wrote into `FINITE-WITNESSES-AND-M6-TWOSTATE.md` §4–5 and STATUS:

> "for `m = 6` … **no model with ≥ 3 distinct palette values exists** … the two-state form is forced,
> not chosen", supported by an exhaustive `4^6` enumeration.

**That is wrong as a global statement and is retracted.** The enumeration ranged over the **six angles
of a single 60° orbit** for **one** `q` pattern. It therefore proves only:

> For `q = (0,3,3,3,0,0)` and the six directions `t + jπ/3` of a **single** orbit, at most 2 distinct
> palettes occur.

It says nothing about the whole circle. On the whole circle the phase can advance, so **different
orbits may select different compatible pairs**, and a globally 4-valued model exists — verified below.
The inference "orbitwise 2 states ⇒ one global `(J,K)` pair" is invalid, and my §5 reading of the
`m`-table ("the collapse happens at the full orbit, so the two-state form is a property of the closed
orbit") was the same error wearing different clothes: `m = 6` *is* one orbit, so of course it is
orbit-local.

Grades: **[P]** argument written here; **[C]** exact computation, reproducible by one command;
**[relayed]** from Astra, not established by me.

## 2. The four-palette whole-circle model — independently verified **[C]**
`h = π/6`, `f(t) = floor(6t/π) mod 4` on `ℝ/(2π)`; cell `k = [kπ/6, (k+1)π/6)` has `f = k mod 4`,
`k = 0..11`; `P(t) = ((0,2),(0,3),(3,5),(2,5))[f(t)]`.

| check | result |
|---|---|
| **[S1]** `f(t + jπ/3) = f(t) + 2j (mod 4)`, all 12 cells, `j = 0..5` | **PASS** |
| **[S2]** 60° shift lands on a **disjoint** palette: `P(k) ∩ P(k+2) = ∅`, all `k` | **PASS** |
| **[S3]** 120° shift **preserves** the palette: `P(k) = P(k+4)` | **PASS** |
| **[S4]** every palette meets **both** side-allowed sets `{2,3}` and `{0,5}` (m6 `q`) | **PASS** |
| **[S5]** every single 60° orbit uses exactly **2** palettes; whole circle uses **4** | **PASS** |
| **[S6]** `A_0 = {f even}`, `A_1 = {f odd}`: 60°-invariant, 6 cells each, measure `π` of `2π` | **PASS** |
| **[S7]** `γ = arccos(5/6)` satisfies `30° < γ < 40°` | **PASS** |
| **[S8]** `δ := 6γ/π ∈ (1, 4/3)` ⇒ no **same-phase** γ-return anywhere | **PASS** |
| **[S9]** cross-type (`Δf = 1`) occupies fraction `2 − δ ≥ 2/3` of the circle | **PASS** |

Consequently: **no single `(J,K)` pair covers all angles** — the model is genuinely 4-valued globally
while being 2-valued on each orbit. That is exactly the refutation of the inference, and nothing more.

## 3. `γ = arccos(5/6)` with no floating-point proof **[P][C]**
`cos` is strictly decreasing on `[0°,180°]`, so it suffices to bracket `5/6` between two exact
cosine values.

* `cos 60° = 1/2 < 5/6` — immediate.
* `cos 30° = √3/2 > 5/6`: both sides positive, so square; `25/36 < 27/36`. ✔
* `cos 40° < 767/1000 < 5/6`: from `8c³ − 6c + 1 = 0` at `c = cos 40°` with `f` increasing there,
  and the exact sign test `f(767/1000) = 967663/125000000 > 0`; then `767·6 = 4602 < 5000 = 5·1000`. ✔

Hence `30° < γ < 40°`, i.e. `δ = 6γ/π ∈ (1, 4/3) ⊂ (1,2)`.

**Why `δ ∈ (1,2)` settles the γ-shift.** `floor(x+δ) − floor(x)` with `δ ∈ (1,2)` is exactly `1` or
`2`, never `0` or `4`. So `f(t+γ) ≠ f(t) (mod 4)` for **every** `t`, hence `P(t+γ) ≠ P(t)` for every
`t`: the same-phase γ-return set is not merely null, it is **empty**. In particular **both** `A_i`
same-phase return sets are empty. Restricted to a fixed `A_i`, `Δf = 2`, so the palette moves to its
**disjoint partner** — the "opposite Boolean phase" of the relay.

**Positive cross-type measure.** `Δf = 1` occupies fraction `2 − δ ≥ 2/3` of the circle and `Δf = 2`
occupies `δ − 1 > 0`, so both regimes are positive-measure and the phase genuinely varies. The bound
`2/3` is rigorous because `δ < 4/3` follows from `γ < 40°`.

## 4. Constraint table — only what is actually supplied
Every row states its source and quantifier. **No constraint below is added by me**, and in particular
**no global γ-return relation is asserted**.

| id | relation | source | quantifier | status |
|---|---|---|---|---|
| G1 | generic contact-ban theorem | local bank, source SHA `9a904d4d7165889a5b12c77ea4e1646e436a0f5de4d4d057e2ee20d5e6f82ba1` | as stated in source | **Lean 4.34.1 / mathlib `d13f23b`, standard axioms** [relayed] |
| G2 | `five_support_no_sixty_joint_pair` | same bank, same SHA | as stated in source | **Lean 4.34.1 / mathlib `d13f23b`, standard axioms** [relayed] |
| L1 | **no SAME-phase γ-return on `A`** | Astra localized triangle/density argument | `∀ t ∈ A` — **local, not global** | paper candidate; the ergodic step to globalize **fails for partial `A`** [relayed] |
| L2 | cross-type (`A_0 ↔ A_1`) transition constraints | — | — | **NOT supplied**; requires actual source production |
| T1 | larger three-centre replacement | target of this programme | — | **PAPER CANDIDATE**, pending independent review and Lean |

The strongest **global** triangle-return relation supplied by geometry or by an independent argument is
therefore: **none**. `L1` is a statement about `A`, and the relay explicitly records that the ergodic
global step fails for partial `A`. So `L2` and any global same-phase return constraint remain
**unproved**, and I do not add them to make any search decide.

## 5. What this does and does not establish
* **Does:** the four-palette whole-circle angular model is valid on all nine checks **[C]**; and the
  inference "orbitwise 2 states ⇒ one global pair" is **refuted** **[P][C]**.
* **Does not:** it does **not** refute `WeakColoring6` and gives no `ℝ²` colouring. This is an
  **exact angular model with piecewise-constant palettes**, not a whole-circle trace field and not a
  weak colouring. Nothing here is a global conclusion from a local/angular object.
* Original proof files were not modified; Lemma 6.7 is retained.

## 6. Reproduce
```
cd supervisor/solve-graphs && python3 fourstate_verify.py     # ALL CHECKS PASS; sole compute process
```

## 7. Clarification (typo in earlier reporting)
An earlier summary compressed a sentence to "both `A_i` are null". **That is a misstatement and is
corrected here.** The correct facts are:

* `A_0 = {f even}` and `A_1 = {f odd}` are each **60°-invariant with measure exactly one half** of the
  circle (`π` of `2π`: 6 of the 12 cells). They are large sets, not null.
* The **same-phase γ-return sets** — the sets of `t` with `t + γ` in the same `A_i` **and** the same
  Boolean phase — are **null**, indeed **empty**. Those are different objects.
