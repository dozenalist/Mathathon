# Independent review: `EncodingApproximationAt` common core (block 8)

Reviewing a **frozen** snapshot, not live files:
`supervisor/simplify-lean/snapshots/enc-feb15b727d97c29c/` —
`EncodingCore.lean` sha256 `feb15b727d97c29ce63c48feffeed6d8efa21b2904d7fa7bc564624323ac4c92`,
`Wrappers.lean` sha256 `7f13628d3c10955cb368be6f065adf5373c726445bd564628c919bb869e569d8`,
`PLAN.md` sha256 `70ae8dc1c05897fa1c4ea9b82be6c0110aea2077d9b945ff7ddc8c61b5209706`.
Taken at 2026-11-14T08:41Z from `supervisor/simplify-architecture/encoding-core/`. Live files may move;
this review does not follow them. **Nothing below is compiled.** Grade legend: [R] read/cited from
source, [C] computed by script in this block, [U] unverified pending a build.

## Verdict

The **design is sound and the public statements are byte-identical**. The **standalone preview
file cannot compile**, for a reason that does not affect integration. One quantitative correction
to PLAN §5/§6. Details below, each with a citation.

## F1 [C] `EncodingCore.lean` is missing 13 identifier definitions — preview only

`EncodingCore.lean` imports exactly `FourierTests`, `SmallArcs`, `ConditionalSelection`. That
three-import closure is **9 modules**, and `ConditionalSpectrum` is *not* in it (computed). But the
transplanted body uses identifiers that are defined **only inside `ConditionalSpectrum.lean`**:

| identifier | defined at |
|---|---|
| `eval` | `ConditionalSpectrum.lean:47` (`def eval (a : E) : D →* Circle`) |
| `measurable_eval` | `ConditionalSpectrum.lean:56` |
| `predecessor_moment_sq` | `ConditionalSpectrum.lean:85` |
| `MomentTest` | `ConditionalSpectrum.lean:181` |
| `two_array_norm_bound` | `ConditionalSpectrum.lean:286` |
| `simultaneous_test_budget` | `ConditionalSpectrum.lean:292` |
| plus `eval_add`, `integrable_predecessor_moment_sq`, `measurable_eval_coe`, `momentArgument`, `pair_collision_upper`, `real_algebraic_sum_two_rotations`, `exists_simultaneous_moment_parameter` | all `ConditionalSpectrum.lean` |

Script: `python3 supervisor/simplify-lean/.scratch/check_scope.py` (this block; 0.3 s).

**Consequence, stated precisely:** the file as written will fail with unknown-identifier errors.
This is a defect of the *preview packaging*, **not of the merge**. The declared home is inside
`ConditionalSpectrum.lean` immediately before `finite_uniform_precision_contradiction`, where all 13
are in scope by construction. So:

* do **not** "fix" it by adding `import OAI.Analysis.PlaneSpectrum.ConditionalSpectrum` *and* also
  integrating into that same file (that is a self-import);
* for a standalone pre-check, the correct packaging is a module importing `ConditionalSpectrum`
  (the `'`-primed shadows already avoid the two `def` name clashes), or the two helpers copied in.

## F2 [C] The two public statements are byte-identical to the originals

Extracted statement text (from `theorem` to the `:=`) and compared after whitespace normalisation:

* `finite_uniform_precision_contradiction` (wrapper) vs `ConditionalSpectrum.lean:310` → **identical**
* `ambient_uniform_precision_contradiction` (wrapper) vs `ConditionalLimits.lean:385` → **identical**

The only textual difference found was my own trailing-proof stripping artefact. So the delta of
public statements is **∅**, and the `open`/`omit`/binder names are reproduced exactly. This is the
strongest single check available without a build, and it passes.

## F3 [C] Import direction is acyclic, exactly as PLAN §2 claims

Scripted BFS over `^import` lines of all 83 modules: `ConditionalLimits → ConditionalSpectrum` is
**True**; `ConditionalSpectrum → ConditionalLimits` is **False**. No cycle; the core belongs in
`ConditionalSpectrum`, the ambient wrapper in `ConditionalLimits`. Confirmed.

## F4 [R] The abstraction needs no `Measurable S` — the key design question, answered yes

The claim that `H i (S x)` can be abstracted without adding a measurability hypothesis on `S` is
correct, and the reason is a specific property of the downstream consumer, not luck.
`FiniteModule.common_fiber_contradiction` (`MeasureTheory/CompactFactors/ConditionalSelection.lean:259–271`)
demands, for its four families `(Hp Hm Ap Am : ι → X → Fin m → ℂ)`:

* `hHp : ∀ j, Measurable (Hp j)`, `hHm : ∀ j, Measurable (Hm j)` — **only** `Hp`/`Hm`;
* `hIp : ∀ j, Integrable (fun x => dist (Hp j x) (Ap j x)^2) μ`, likewise `hIm` — **supplied by
  `happrox`**, not derived.

There is **no measurability requirement on `Ap`/`Am`**. Since `Ap`/`Am` are exactly the terms
carrying `H i (S x)`, and `Hp`/`Hm` are `enc (u j) (p x)` — built from `p`, never from `S` — no
`Measurable S` is needed anywhere. This also explains why the *ambient* original never needed
`Measurable (H i ·)`. Verified against the signature, not inferred from the plan.

## F5 [R] `harc`'s `Measure Circle` has no competing instance — statement identity on that axis is safe

Six files declare `local instance : MeasurableSpace Circle := borel Circle` (+ `BorelSpace Circle := ⟨rfl⟩`),
with identical terms: `ConditionalSpectrum.lean:43,178,260`, `ConditionalLimits.lean:363`,
`ConditionalSelection.lean:251`, `SmallArcs.lean:201`, `PhaseCollision.lean:386`
(`rg 'local instance : (MeasurableSpace|BorelSpace) Circle'`). I checked the hazard the plan does not
name: a **global** competing instance would make `harc`'s `Measure Circle` a different proposition in
different files. `Mathlib/Analysis/Complex/Circle.lean` contains **no** `MeasurableSpace` or
`BorelSpace` for `Circle` (`rg -n 'MeasurableSpace|BorelSpace'` → no match), so the local declaration
is the *only* candidate and resolution cannot diverge. `harc` therefore transfers across the three
files as the same term.

## F6 [R] `hwild` at `P`: no hypothesis added, dropped or disguised

Merged core takes `hwild : IsWild (differenceLaw (μ.map P) (condDistrib b P μ))` with `P` a
*parameter*. At `P := fun x => q (p x)` this is `μ.map (q ∘ p)` / `condDistrib b (q ∘ p) μ` up to
delta-reduction of `Function.comp`; at `P := q` it is literally the ambient hypothesis. Nothing about
weak mixing, `(W)` or the compact tower is introduced. Agrees with PLAN §5. The one honest
qualification: the core is **strictly more general** than either statement (it accepts any measurable
`P`, not only `q` or `q ∘ p`). That is a small net gain, and it does not weaken the roots, because
the wrappers' statements are unchanged (F2).

## F7 [R] Quantifiers and the γ constant are positionally faithful

Merged: `happrox : EncodingApproximationAt μ p P S b m (((ρ^m/(m : ℝ))/100)/100)`, and the body's
`let τ := (ρ^m/(m : ℝ))/100`, `let γ := τ/100` — so `γ` matches the hypothesis constant exactly, as
in both originals. The `def`'s existential shape `∃ (r) (B C) (H), 0 ≤ B ∧ 0 ≤ C ∧ (∀ z, ∑ i, ‖H i z‖ ≤ C) ∧ ∀ k, ∃ coeff, (∀ w, ‖coeff w‖ ≤ B) ∧ Integrable … ∧ ∫ … < γ^2`
is order- and binder-identical to both originals (the ambient one names its binder `y` for what is an
`X`; merged calls it `z` — cosmetic). `condDistrib id P μ` and `condDistrib b p μ` are used in the
merged body in exactly the places both originals use them (spot-checked at
`ConditionalSpectrum.lean:389,423,438` / `ConditionalLimits.lean:463,497,512`).

## F8 [C] Correction to PLAN §6: the transplant is 8 sites, not 7

PLAN §6 lists "delete `let P`, delete `have hP`, and rewrite the 6 sites `H ?_ (p x)`". Counting the
actual occurrences in the source body: `Ap`, `Am` (2), `hbins … (fun k => H k (p x)) (hH (p x))` (2),
and the two `change` lines carry **two** occurrences each (4) — total **6 rewritten + 2 deleted = 8**
edit sites. PLAN's own §6 item 7 says "4 occurrences", which makes its arithmetic (7) inconsistent
with its own enumeration. The delivered `EncodingCore.lean` does the rewrite consistently, so this is
a documentation defect, not a code defect.

## F9 [U] Residual build risks, ranked, with the test that settles each

1. **`abbrev` vs `def` (PLAN Risk 2).** Turning the two `def`s into aliases changes printed types of
   downstream items (`ConditionalSpectrum.lean:479` and the conversion lemmas near
   `ConditionalLimits.lean:592`). Defeq should absorb it. Test: `#check @finite_uniform_successor_contradiction`
   and the two `… → EncodingApproximationAt` lemmas must still elaborate, and the whole 83-module build
   must be rc 0 — not just the two files.
2. **Definitional equality of the aliases.** `Wrappers.lean`'s `Iff.rfl` certificates are the right
   test; `S := id` needs `H i (id x) ≡ H i x` (beta/delta on a reducible `def`), which should pass at
   default transparency. UNCOMPILED.
3. **`let : IsProbabilityMeasure (μ.map P)` route unification (PLAN Risk 1).** The merged body uses
   the explicit `.map` route that the *ambient* original does not. The route is available in both
   (`hP := hq` in the ambient wrapper, so `hq.aemeasurable` is in scope), but only elaboration decides.
4. **`Z` universe / instance binding.** `{Z : Type*}` is instantiated to `Y` and `X` respectively, both
   in the same universe as `X Y W` in both originals; no universe lift is introduced. Low risk,
   UNCOMPILED.

## F10 [R] No smuggled contradiction, no `sorry`

`rg -n '\bsorry\b|\badmit\b|^axiom |native_decide|@\[implemented_by|^opaque '` over both frozen
`.lean` files → **no match** (PLAN §8's "one `sorry` in SCAFFOLD.lean" refers to an earlier file that is
no longer in the directory; the delivered sources are sorry-free). The contradiction `False` is produced
by `common_fiber_contradiction`, not assumed. `hwild` and `harc` remain hypotheses.
