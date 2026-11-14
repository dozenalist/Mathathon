# Corrections, the referee's palette audit restated, and one global coupling with its consumer chain

Analysis only; no computation, no placement. Sources read: `BinaryPalettes.lean`, `PaletteTransport.lean`,
`States.lean`, `Palettes.lean`. Grades **[S]** source-read with lines, **[P]** hand-proved here,
**[C]** cited from the referee/Astra, **[X]** not in the tree.

## 1. Two corrections to `ANNULUS-LOCAL-GLOBAL-AUDIT.md`

**(1a) "At `k = 6` the nullity is false" — retracted as an overstatement.** Without a global
`WeakColoring 6` counterexample I may not assert falsity. Correct wording: *the `k = 5` proof does not
generalise*, because its last step needs the complement of a 3-set to be a 2-set (so that the pair is
binary) — at `k = 6` the complement has 3 labels and the binary step is unavailable. So: **`k = 6`
palette-nullity is unproved, and the `k = 5` argument's mechanism fails.** That is a statement about the
proof, not about the truth.

**(1b) The `0.005` centre ball is not an error.** The candidate's `|x| < 0.005` is a *valid sufficient*
bound. What I computed is the sharp containment threshold: every circle of radius `≈1` about `x` lies in
`0.99 < |z| < 1.01` iff `|x| ≤ 0.01`. Both bounds are legitimate; `0.01` is simply the largest radius for
which the containment is automatic, and I should not have called `0.005` unnecessary.

## 2. The referee's palette verification, restated exactly [C]→[P]

Referee's claim: *near centres the unit circles remain in the annulus; only finitely many radial boundary
intersections occur; all trace limits equal the actual singleton indicator.* Reconstructed:

1. `IsTrace x b` means `(x,1,b) ∈ closure(sampleSet)`, so `b` is a **norm** limit of
   `sampleCode (y_n) (r_n)` with `y_n → x`, `r_n → 1`, all `TypicalSampling` (Compactness.lean:261–265).
2. For `|x| ≤ 0.005` and all large `n`, `|y_n| + r_n ≤ 1.005 + 2ε ≤ 1.01` and
   `r_n − |y_n| ≥ 0.995 − 2ε ≥ 0.99`, so **every sample circle lies in the annulus**.
3. On such a circle the sample code is the indicator of `e ↦ ` *(sector label of `y_n + r_n e`)*. The
   annulus colouring is piecewise constant with **finitely many discontinuity rays** (nine sector
   boundaries, plus the two circular boundaries which the circle never meets by 2), so the circle meets the
   discontinuity set in **finitely many points**, an angular null set.
4. Hence the codes converge pointwise off a null set and are dominated by `1`, so by dominated convergence
   they converge in `L²` to the indicator of the **limit colouring**, i.e. `b = 1_{c_A(x + ·)}` a.e.
5. Therefore `P_x(e) = {c_A(x + e)}` for a.e. `e`, **independently of how the colouring is extended off
   `D ∪ A`** — because step 2 uses only `|x| ≤ 0.005`.

So the referee is right, and the conclusion is stronger than "local": for `|x| ≤ 0.005` the palette statement
is **extension-independent**. What remains outside is centres with `|x| > 0.005` — in particular the ring
`|x| ≈ 1`, whose unit circles cross the *hole* (they pass through `x + e = y` with `|y| < 0.005` when
`e ≈ −x/|x|`), so their palettes are **not** determined by the local data. That distinction is what the
scenario below turns on.

## 3. The one global coupling I can license, with producer / centre / quantifiers / consumer

**Producer.** `States.two_state_impossible` (States.lean:243):

> `{k : ℕ} {c : ℂ → Fin k} (hc : Measurable c) (hw : WeakColoring k c) (x : ℂ) (J K : Finset (Fin k))
> (hcard : (univ ∖ (J ∪ K)).card ≤ 2) (s : Angles → Bool) (hs : Measurable s)
> (hJ : RealState hc x {t | s t = false} J) (hK : RealState hc x {t | s t = true} K)
> (hflip : ∀ᵐ t, s (t + π/3) = !(s t)) : False`

with `RealState x A J := MeasurableSet A ∧ ∀ i ∈ J, A ≤ᵐ[volume] liftPalette c hc x i`
(States.lean:92): on the direction set `A`, only labels from `J` occur in the palette a.e.

* **Centre:** a **single** centre `x`; the statement is about the direction circle at `x` only.
* **Quantifiers:** for all `k`, all measurable `c`, all `x`, all label sets `J, K` with
  `|[k] ∖ (J ∪ K)| ≤ 2`, all measurable Boolean `s`. Note the `k`-dependence is *only* through that
  cardinality: at `k = 5` two groups must cover `3` labels, at `k = 6` they must cover `4`.
* **Consumer:** the four-state lemma at States.lean:378 (`apply two_state_impossible … (fourGroup 0)
  (fourGroup r) hcard …`), hence the four-group exclusion chain feeding `Interfaces`/`Exclusion`, i.e. the
  §8 machinery — and **`Lemma 6.7 = step_ban` is retained** downstream of it.
* **What it is not:** it is *not* a centre-separation statement, and it does *not* follow from
  `WeakColoring` alone by inspection: it needs the alternating Boolean `s`, which is a genuine extra
  hypothesis on the *angular* structure at `x`.

**Honest scope.** Every consumer of this lemma is at `k = 5`. At `k = 6` the hypothesis
`|univ ∖ (J∪K)| ≤ 2` is *harder* to meet (the two groups must cover four of six labels), so the lemma is
weaker at `k = 6`, not stronger. It is therefore a **candidate** coupling at `k = 6`, usable only when a
four-label cover plus an alternating Boolean is exhibited [X].

## 4. The local triangle scenario, and the first global relation that bites

**The scenario [C].** Patches: three-sector (Mercedes) disks of radius `ρ < 0.005` near `0`, labels
`{0,1,2}`, arbitrarily small and accumulating at `0`; annulus `A` with labels `{3,4,5}`.

**Why it is locally unit-proper [P].**
* Inside a patch: diameter `2ρ < 0.01 < 1`, so it contains **no** unit pair — any colouring is proper.
* Across the patch–annulus interface: every unit-neighbour of a patch point `p` satisfies
  `|z| ∈ (0.995, 1.005) ⊂ A`, and the two label sets `{0,1,2}`, `{3,4,5}` are **disjoint** — so every
  such pair is properly coloured automatically.
* Inside `A`: Claim 1 of the previous audit (angular separation in `[59.34°, 60.66°]`, never `≡ 0 mod 120°`).
* Transitions: at each patch centre `x` the three sectors meet, so `Γ_x ⊇` the triangle `{0,1,2}`, and the
  patch centres accumulate at `0` — so `L` fails to be locally finite *for the local data*.

**Which palettes are fixed, and which are not [P].** By §2, at every centre with `|x| ≤ 0.005` the palette
is a singleton in `{3,4,5}` — in particular **the patch's own labels `{0,1,2}` never appear in any palette
at a centre within `0.005` of `0`**. That is the "outsider" pattern of the `m3` gadget, reproduced at
`k = 6` with three outsider labels.

**The first global relation that bites: the unit-scale endpoint/two-unit transport, not a centre
separation.** Consider a patch point `p` (`c(p) ∈ {0,1,2}`) and the centre `x := p − e` for a unit `e`.
Then `|x| ∈ (0.995, 1.005) ⊂ A`, so `x` is a **ring centre**, and its unit circle passes through `p`
(where the colouring is a patch label) and overwhelmingly through `A` (where it is a `{3,4,5}` label).
The dual endpoint constraint — `c(y) ∈ P_{y−e}(e)` for a.e. `(y,e)`, the constraint recorded as `m10`'s
`T1` and in the tree as `exact_sample_palette_fixed`/`trace_positive_le_palette` applied at the *ring*
centre — forces

> **(†) for a.e. patch point `p` and a.e. unit `e`, the labels `{0,1,2}` occur in the palette at `p − e`
> in direction `e`.**

So the patch labels are **not** outsiders after all: they appear in the ring-centre palettes on the arcs
where the circle dips into the patches. This is the relation that a purely local audit cannot see — it is
not a new centre separation but a **constraint linking the near-field transition structure at `0` to the
far-field palettes at radius `≈1`** — and it is exactly what the referee-accepted contact-ban/shift theorem
speaks to: with (†) in hand, the triangle `{0,1,2}` at a patch centre and the palettes at the ring centres
are no longer disjoint, so the `m3`-style outsider mechanism has nothing to stand on.

**What (†) does and does not establish (stated precisely).** (†) rules out the *specific* mechanism of the
scenario — "triangle labels in no palette" — but it does **not** by itself produce a contradiction, because
a palette may contain both a patch label and an annulus label. What is still needed, and is the honest
missing piece: **(†) plus `(5.2)` at scale one** (`palette_transport_param` instantiated at the ring centre
with the two-unit decomposition), which would force the ring-centre palette in the patch direction to avoid
the labels it must, by (†), contain — a contradiction. That instantiation is exactly what no local model can
supply, since the ring-centre palette depends on the colouring of the **region between the patches and the
annulus**, which the scenario leaves empty.

## 5. Status

* Corrections (1a), (1b): done, with the "unproved / mechanism fails" wording adopted.
* §2: the referee's palette audit is accepted and reconstructed; the key refinement is
  **extension-independence for `|x| ≤ 0.005`** and **extension-dependence for `|x| ≈ 1`**.
* §3: one licensed global coupling, with producer/centre/quantifiers/consumer and its honest `k = 6`
  limitation; it is a *candidate*, not an established instrument at `k = 6`.
* §4: the scenario is locally unit-proper and locally accumulating (proved), and the first relation that
  bites is (†), the dual endpoint constraint at ring centres — a global, far-field/near-field coupling. It
  is necessary but not sufficient; the missing complement is the unit-scale transport at the same centre.
* No claim about a global 6-colouring, (W), or `χ(ℝ²)`.
