# Referee-facing equivalence argument for the encoding-core abstraction

Subject: the frozen revision `ConditionalSpectrum` `48aa378f6f6db82b…`, `ConditionalLimits`
`58707f0495837a89…` (inputs `6602b9d8…`, `ca74ba10…`). **Analysis only**: this block ran no
generator, no build, and did not touch the frozen files. `−126` lines remains a textual candidate.

**Claim.** Replacing both `def`s by `abbrev` aliases and both 153-line proofs by two-line calls into
one general theorem changes *neither* the meaning of the two definitions *nor* the quantified
statements of the two public theorems, and introduces no new assumption, instance or hypothesis. It
introduces two parameters (`P`, `S`) that separate two roles the old code ran together.

## 1. The two roles

Both old hypotheses have a four-slot shape: a family of basis functions, a pointwise bound on it, a
map selecting the coefficients that multiply it, and a read-out telling the family where it is being
sampled. The old code fused the last two because its two instances happened to fuse them:

* **`P : X → W`, the coefficient map.** Selects the coefficient vector `coeff (P x) : Fin r → ℂ`.
  It is the only object the *wildness* hypothesis sees: `hwild` is
  `IsWild (differenceLaw (μ.map P) (condDistrib b P μ))`. It must be measurable, because it is pushed
  forward (`μ.map P`) to make a probability instance.
* **`S : X → Z`, the read-out map.** Determines where the family is evaluated: the hypothesis contains
  the term `H i (S x)` and nothing else about `S`. It is never mapped or differentiated. The composite
  `H i (S x)` **is** integrated — it sits inside the `Integrable` and `∫` terms — but the regularity
  that integration needs is *assumed of the composite*, never derived from a property of `S` (§4).

Old finite: `P := q ∘ p`, `S := p`, family on `Z := Y`.
Old ambient: `P := q`, `S := id`, family on `Z := X`.

The unification is therefore not "the ambient case is a special case of the finite one" (it is not:
different coefficient map, different read-out), but "the proof never used more than these two slots".
That is an empirical claim about the proof text, and it is checkable: the complete diff of the two
153-line bodies is **6 lines**, and after deleting the two local bindings `let P : X → W := q ∘ p` and
`have hP : Measurable P := hq.comp hp`, **no occurrence of `q` or `hq` survives in the body** — the
symbol `q` disappears from the proof entirely. Its only role was to build `P`.

## 2. Every old hypothesis and where it goes

| old hypothesis | new location | comment |
|---|---|---|
| `μ : Measure X`, `[IsProbabilityMeasure μ]` | unchanged | drives `ν := differenceLaw (μ.map P) …` |
| `p : X → Y`, `hp : Measurable p` | unchanged | `p` fixes both the kernel `condDistrib b p μ` and (finite instance) the read-out |
| `q : Y → W` (finite) / `q : X → W` (ambient) | **eliminated into `P`** by the wrapper | `q` survives only in the wrapper's own public statement |
| `hq : Measurable q` | `hP : Measurable P`, supplied as `hq.comp hp` (finite, the old proof's first line) or `hq` (ambient, likewise) | not a new assumption: the old proofs already carried exactly these two lines to build `hP` |
| `b : X → D`, `hb` | unchanged | kernel of the encoding |
| `m : ℕ`, `hm : 0 < m` | unchanged | `(m:ℝ)` positivity, `NeZero M`, the `1/(4m²)` budget |
| `g : Y → Fin m → D`, `hg` | unchanged | the only place `Y` (hence `FiniteEncodingApproximation`'s atoms) enters |
| `hwild : IsWild (differenceLaw (μ.map (q∘p)) (condDistrib b (q∘p) μ))` (finite) / at `q` (ambient) | `hwild : IsWild (differenceLaw (μ.map P) (condDistrib b P μ))` | under `P := q ∘ p` this is the finite statement's hypothesis; under `P := q` the ambient one. `q ∘ p` and `fun x => q (p x)` are delta-beta equal, so the two are defeq |
| `ρ c N`, `hρ hc hN`, `harc` | unchanged | `harc`'s `Measure Circle`/`ω.real` ride on the pre-existing `local instance` pair, untouched |
| `happrox : FiniteEncodingApproximationAt μ p q b m γ` (finite) | `happrox : EncodingApproximationAt μ p P S b m γ` at `(Z,S,P) := (Y, p, q∘p)` | the alias makes the two *the same term*, §3 |
| `happrox : AmbientEncodingAt μ p q b m γ` (ambient) | same, at `(Z,S,P) := (X, id, q)` | likewise |

Nothing is dropped, reordered or strengthened. The two slots that were *never* hypotheses stay
hypotheses of nobody: the family `H` carries no measurability in either old definition (only the
composite `Integrable` assumption), and `S` carries none either (§4).

## 3. The two `def` → `abbrev` substitutions preserve meanings and statements

Write `E` for the general hypothesis with parameters `(Z, S, P)`, `F_in` for the old finite body,
`A_in` for the old ambient body.

**(i) Binders.** Both aliases restate the old binder list exactly — `(μ : Measure X)`,
`[IsProbabilityMeasure μ]`, `(p : X → Y)`, `(q : …)`, `(b : X → D)`, `(m : ℕ)`, `(γ : ℝ)` — in the
same order with the same explicitness and the same types. Hence the *type* of the constant is
literally unchanged; every application in the tree keeps its meaning, including the two proofs
`ConditionalLimits:227` and `:592` whose *conclusions* are of this type.

**(ii) Bodies.** After one delta step on the alias and one beta step,
`FiniteEncodingApproximationAt μ p q b m γ ↝ E μ p (fun x => q (p x)) p b m γ ↝ F_in`, because
`(fun x => q (p x)) x ↝ q (p x)` and the bound's binder `z : Y` is the old binder `y : Y`. Likewise
`AmbientEncodingAt … ↝ E μ p q id b m γ ↝ A_in`, because `id x ↝ x`. The only residual difference is
the name of a bound variable (alpha). So each alias denotes the *same proposition* as before, by
definitional equality.

**(iii) Transparency.** The old constants were `def`s with explicit bodies — transparent, unfoldable
at semireducible transparency. `abbrev` is `def` + `@[reducible]`, i.e. unfoldable at *every*
transparency. Elaboration therefore remains at least as permissive as before. There is no proof in
the tree that depends on the *unfolding* of either name: a read-only scan finds seven occurrences (lines 267, 284, 323 of `ConditionalSpectrum`; 227, 369, 398, 592 of `ConditionalLimits`),
all of them the declaration itself, an application in a hypothesis slot, or the conclusion of a
construction lemma (`ConditionalLimits:227`, `:592`); **no** `simp`/`rw`/`unfold` ever names them and
no attribute is attached. So `abbrev` cannot perturb any existing proof.

**(iv) Quantified public statements.** A theorem's statement is `Π (binders), False`. The binders'
texts are byte-identical (measured: statement hash `2dde28358ab09934…` for the finite root,
`ab6dd548d3a6bb53…` for the ambient), and by (ii)–(iii) each hypothesis type is unchanged as a term.
So the two quantified propositions are preserved as *terms*, not merely up to equivalence — the
strongest available form. The one caveat a referee should hold onto: what `#check` *prints* may unfold
the alias, i.e. display a different surface syntax for the same term. That is a printing matter, and it
is settled by comparing `#check` output before and after (recorded as a build item below).

## 4. Why no measurability assumption on `S` was silently dropped

The composite `H i (S x)` does appear inside the `Integrable` and `∫` terms: `S` participates in
integration, and nothing here claims otherwise. The claim is about the *direction* of the assumption.
`S` occurs in the hypothesis exactly as `H i (S x)`; the proof touches it only through `H k (S x)` and
`hH (S x)`, in `Ap`, `Am`, the `hbins` application and the two `change` lines. The bound
`∀ z, ∑ i ‖H i z‖ ≤ C` transfers pointwise, so `∑ i ‖H i (S x)‖ ≤ C` for every `x` with no regularity
on `S`. Regularity of the composite integrand is **not derived** — it is a hypothesis of the encoding
statement, exactly as it was in both old definitions. So a measurability hypothesis on `S` would be
unused, and adding an unused hypothesis is precisely what "no new assumptions" forbids.

Two further points, so that this is not merely "we got away with it":

* The old definitions were equally silent about the *family's* measurability: `H` carries no
  `Measurable` hypothesis, only the pointwise bound, because the integrability of the composite is
  assumed outright. Silence about `S` mirrors the existing silence about `H`, and for the same reason:
  in both cases the composite's regularity is taken as a hypothesis, not inferred from its parts.
* At both instances `S` *is* measurable anyway (`p` with `hp`, `id` trivially), so the abstraction
  cannot be blamed for proving anything about a non-measurable read-out: no such instance is formable
  in the tree. What the abstraction does is *not demand* what the old interface also did not demand.

The genuine measurable data are `p`, `P` and `b`, and each keeps its hypothesis (`hp`, `hP`, `hb`).

## 5. Genuinely new assumptions or instances: none

| item | status |
|---|---|
| `{Z : Type*}` | new parameter, **no** instances required (no `MeasurableSpace`, no `Nonempty`, no `Type` class) |
| `(S : X → Z)` | new parameter, **no** hypothesis |
| `hP : Measurable P` | the old `hq` under the name the old proofs already used for it |
| `hwild` at `P` | the same hypothesis, at the map it was always about |
| new typeclass requirements | **none**; the section context is the old one |
| new universes | **one, in the general core only**: `EncodingApproximationAt` quantifies `{Z : Type u}` in a fresh universe. The two *public wrappers* keep their signatures, because each instance instantiates `Z` with an existing type in its own universe (`Y`, `X`). No public universe changes. |
| hidden strengthening | none: `E` at `(Y,p,q∘p)` *is* the old finite hypothesis and at `(X,id,q)` *is* the old ambient one |

One downstream cost, stated so the ledger is honest: the alias makes `S := id` visible in the goals it
reaches, so the conversion lemma `CompactApproximation.At → AmbientEncodingAt`
(`ConditionalLimits:457`) needed its closing term changed from
`by rw [← integral_congr_ae he]; exact hae` to
`by simpa only [id_eq] using ((integral_congr_ae he) ▸ hae)` — the same integral equality, with `id`
beta-normalised. One line, no hypothesis changed. The merge is therefore not literally free
downstream; it costs exactly that line.

A remark for the referee, deliberately **not** part of the patch: the transplanted proof actually
proves something stronger, namely the version where the family is an arbitrary ambient family
`Kf : Fin r → X → Fin m → ℂ` (no factorisation through any `S`). That version is *strictly weaker* as
a hypothesis, hence a strictly stronger theorem. We do not state it, because it would change the two
public statements (the finite hypothesis would no longer be `FiniteEncodingApproximationAt`), and the
task is an exact merge. It is available later as a genuine strengthening if the house wants one.

## 6. Status, and what would falsify this argument

`−126` lines (`ConditionalSpectrum` `+33`, `ConditionalLimits` `−159`) is a **textual candidate**.
Nothing in this document is compiled. The argument above would be refuted by any of:

1. a build error at the anchor of the common theorem (ordering already repaired: helpers at 299/305,
   theorem at 325);
2. `refine ⟨r, B, C, H, …⟩` at `ConditionalLimits:592` no longer elaborating against the `abbrev`
   (the existential arity `r, B, C, H` is preserved because `S` and `P` are parameters);
3. the four `change` lines or the `hbins` application failing at `S`;
4. `EncodingApproximationAt μ p q id b m γ` failing to elaborate with `S := id`;
5. `#print axioms` on either root, on `uniform_precision_contradiction`, or on any of the three
   consumers (`finite_uniform_successor_contradiction`, its caller at `Approximation:414`, the
   cross-module call at `ConditionalLimits:322`) showing anything beyond
   `[propext, Classical.choice, Quot.sound]`.

**Grades.** §§1–5 are *arguments on source text*, verified by reading the two proofs and the seven
occurrences of the two names; they are not machine-checked. The equality of the two hypothesis
instances is a **defeq claim**, evidenced by the byte-identical statement texts and the alias
construction, and confirmable only by elaboration. The line count is measured but not compiled.
