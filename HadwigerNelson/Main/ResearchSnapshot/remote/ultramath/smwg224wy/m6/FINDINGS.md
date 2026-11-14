# m6 / d10 — what the terminal factor has to deliver, and why the tower route delivers nothing

Three results, all checked on this machine with the pinned toolchain
(`source scripts/env4341.sh`, Lean 4.34.1, `sprint/simplify/stage/lean/build/lib` on
`LEAN_PATH`).  Nothing in `lean/`, `results/`, `scripts/`, `.ultramath/` outside
`.ultramath/smwg224wy/m6/` was written.

| item | status |
|---|---|
| m15 `TowerMax.Tower` is the class of **all** factors | **proved**, `TowerDefect.lean` |
| `exists_terminal_factor_of_tower_good`'s `hgood` is refutable there | **proved** (consequence) |
| the tree's whole need is one predicate `TerminalObligation` | **proved**, `Residual.lean` |
| frees 12050 / 5876 / ≤4566 lines (three definitions of "frees") | measured, §3 |
| a −1500 building tree | **not obtained**; exact stopping line in §4 |

---

## 1. `TowerMax.lean`'s maximal member sees the whole σ-algebra

`sprint/simplify/m15/work/TowerMax.lean` replaces `exists_terminal_factor` by
maximality over

```
inductive Tower (μ : Measure X) : (X → OrbitSpace K) → Prop
  | base : Tower μ (fun _ => ⟨fun _ => 0⟩)
  | step : Tower μ p → Measurable H → (∀ x, ‖H x‖ ≤ 2) →
           (¬ ∃ b, Measurable b ∧ H =ᵐ b ∘ p) → Tower μ (encode (extend p H))
  | join : (∀ n, Tower μ (q n)) → chain → Tower μ (ChainJoin.code q)
```

and its docstring claims "the top factor is reachable exactly when the system is a
compact extension of the trivial factor".  **That is false for `step` as written**:
`step` carries no compactness and no non-ergodicity hypothesis, so it applies to the
maximal member `a` itself with *any* non-degenerate bounded measurable `H`, producing
a strictly larger member.  Maximality therefore contradicts every such `H`:

```lean
theorem tower_max_all_measurable (a : CodedMax.Model μ (Tower μ)) (hamax : IsMax a)
    (H : X → ℂ) (hH : Measurable H) (hB : ∀ x, ‖H x‖ ≤ 2) :
    ∃ b : OrbitSpace K → ℂ, Measurable b ∧ H =ᵐ[μ] b ∘ a.map
```

(`TowerDefect.lean`; the body is the argument already present in
`exists_ergodic_factor`, run at `a` instead of at a successor.)

Consequence: at the maximal `a`, `condDistrib id a.map μ` is the Dirac kernel, so
`differenceLaw (μ.map a.map) (condDistrib id a.map μ) = δ_1`; `1 ∈ C`
(`C = ker (D → Cosets)`, `1 = j 0`), so

  `¬ UniversalGood μ a.map`  for every `μ` with `IsWild μ`  (witness `d = id`).

`exists_terminal_factor_of_tower_good` demands `UniversalGood` at exactly such an
`a`.  Its hypothesis is therefore unsatisfiable: the theorem is vacuous, and no R1
deletion can be routed through it until `Tower.step` is restricted.

*Minimal repair*: `step` must require the predecessor's relative product to fail to be
ergodic (that is what `CompactTower.strict_compact_successor` consumes), i.e. `Tower`
must be the non-ergodicity-driven tower.  Even then the maximal member can be the top
factor, so properness = (N)/(O) remains the gate.

## 2. The obligation in its weakest form

`Ergodicity.lean:54` (`ergodic_wild_fourier`) is the only consumer of
`exists_terminal_factor` in the 85-module tree, and it consumes it at exactly one
place, `Ergodicity.lean:58`, at the single instance `d = id` of `UniversalGood`.
What that line needs is `differenceLaw (μ.map q) (condDistrib id q μ) C = 0`, and
m5's Theorem A gives it from two properties of `q`:

```lean
def TerminalObligation (μ : Measure D) [IsProbabilityMeasure μ] : Prop :=
  ∃ (q : D → OrbitSpace K) (hq : Measurable q),
    (∀ k : K, ∀ᵐ d ∂μ, q (k • d) = k • q d) ∧
    ErgodicSMul K (D × D) (RelativeProduct.law μ q hq) ∧                 -- (E)
    ¬ ∀ᵐ z ∂(RelativeProduct.law μ q hq), z.1 = z.2                      -- (H2)

theorem ergodic_wild_fourier_of_obligation (h : TerminalObligation μ) (z : E) (hz : z ≠ 0) :
    ∫ d, (eval z d : ℂ) ∂μ = 0
```

(`Residual.lean`: `rotErgodic` supplies `ErgodicVAdd Rot`, `relative_singularity_of_ergodic`
does the rest, `relative_difference_invariant` supplies `IsWild`, then
`fourier_vanish_of_terminal`.)  This is strictly weaker than `UniversalGood` at the
maximal factor: it is one factor, one `d`, and (H2) is exactly "the relative product
is not carried by the diagonal" — the `FactorLp.space ≠ ⊤` (properness) side of
(N)/(O), not the for-all-wild-`d` statement.

## 3. What that is worth, in lines

`python3 sprint/simplify/m10/harness/analyze.py free <route> --md` (m10's sound
declaration graph, `DECLGRAPH.log` + `SPANS.json`):

| route | freed decl lines | modules emptied |
|---|---|---|
| reprove `ergodic_wild_fourier` outright | **12050** | 17 |
| same, `--keep fourier_vanish_of_terminal relative_difference_invariant` (what `Residual.lean` actually uses) | **5876** | 7 (`Functions` 819, `Centers` 660, `Factors` 528, `Approximation` 453, `PhaseCollision` 445, `SmallArcs` 290, `PhaseEncoding` 233) |
| same + the build-consistency pass of §3.1 | 5876 → 4103 span-lines, **not converged** | 7 of 17 changed modules still fail |
| R1 / `exists_terminal_factor` (the brief's figure) | 4112 (upper bound) | 4 |
| R1 / `exists_terminal_factor` (the brief's figure) | 4112 | 4 |

### 3.1 These figures are upper bounds, not deliverables

A route figure counts declarations that are unreachable from the 7 headlines *after
dropping value-edges*.  It does **not** mean the source compiles when they are
deleted: surviving declarations still *name* them.  Measured here by iterating
"prune → compile the changed modules → un-delete what a survivor still names":

* round 1: 5820 → kept `Location.lift`, `Location.exists_unique_minimizer`,
  `bounded_phase_encoding`, `OrbitSpace.equiv`, `FactorCode.scalar_bound`,
  `AverageErrors.*` (8), `PhaseEncoding.kernelEncoding` + namespace (32) → 4473;
* rounds 2–3: + `SmallArc.exists_small_arc_constants`, `PhaseCollision.*` (20) → 4380;
* round 4: 4103 span-lines, tree 31277 → 28076, there it stalled; 7 of 17 changed
  modules still fail (`Approximation`, `ConditionalLimits`, `Kernels`, `Functions`,
  `Factors`, `TheoremA`, `Ergodicity`).  Two identifiers the pass could not resolve
  at all — `SmallArc.exists_small_arc_constants` and `continuous_mk.comp` — are
  nested inside a deleted span, which `apply_prune.py` cannot express (it deletes from
  a declaration line to the line before the next declaration, so a deleted
  `namespace X … end X` block takes its contents with it and the error surfaces far
  away as "unknown namespace X").
* also unhandled by `apply_prune.py`: `omit … in` prefixes whose declaration was
  deleted (`Centers.lean:332`, `ConditionalSelection.lean:77` → "invalid 'omit'").
  `fix_omit.py` here strips them from every touched module.

**Conclusion: the shrank factor is ≈0.70 (5876 → 4103) and not converged.**  So
every figure the harness prints — including the brief's R1 = 4112 — is an upper
bound; a deletion claim needs its own compiling round before it can be quoted.

## 4. Where the zone stops being deletable

The tree cannot get past

  `TerminalObligation μ`  =  ∃ a factor `q` of `μ` with (E) ergodic relative square
  and (H2) relative product not carried by the diagonal,

and nothing in the 31277 lines supplies it:

* the trivial factor gives (H2) (⟺ `μ` is not a Dirac, which `IsWild` forces) but
  not (E), since (E) there is weak mixing of `μ`;
* the top factor gives (E) (a diagonal relative product is ergodic whenever `μ` is)
  but not (H2);
* `TowerMax` was to give (E) by maximality, but §1 shows its class contains the top
  factor, so its maximal member gives (H2) = false;
* `InvariantDecomposition.fiber_ergodic` gives fibre ergodicity of the ergodic
  decomposition, which is the trivial factor when `μ` is ergodic.

The paper's own route is the compact-extension tower, and the missing input there is
properness of the maximal member ((N)/(O)).  So the precise stopping line is:

  `Ergodicity.lean:58`, `exact hgood id measurable_id (…) (by simpa using hw)`

— one instance of one predicate, worth 5876 declaration lines (7 modules) once
`TerminalObligation` is discharged, and 12050 if the downstream Fourier machinery
(`fourier_vanish_of_terminal`, `RadialEnergy`, `ConditionalSpectrum`) is reproved too.

## 5. Files

* `TowerDefect.lean` — §1. `lean .ultramath/smwg224wy/m6/TowerDefect.lean` (24 s).
* `Residual.lean` — §2. Needs m5's `.olean`s:
  `LEAN_PATH="$PWD/.ultramath/smwfoekgk/m5/work:$PWD/sprint/simplify/stage/lean/build/lib:$LEAN_PATH" lean .ultramath/smwg224wy/m6/Residual.lean` (11 s).
* `prune8.py`, `fixpoint.py`, `fix_omit.py`, `mktree.sh`, `build_changed.sh`,
  `patch_ergodicity.py` — §3.1 machinery; `tree/` is the pruned diagnostic tree
  (88 modules, 27392 lines; `TerminalObligation` is a declared axiom there, so it is
  a measurement artefact, **not** a candidate deliverable).
