# Audit of the new mathematics in the R1 restructure (m1, swarm smwg224wy)

Scope: the *mathematical* claims the restructure rests on. The deletion accounting itself is
d5's. Everything below was checked here against a copy of `sprint/simplify/stage/lean`
(`tree/`), pinned toolchain 4.34.1 from `repo/.scratch`, and independently under stock
Lean 4.33.1 + `/opt/mathlib` (`tree433/`, ported with m4's `d7.sh`).

## How to check (all commands run from this directory)

```bash
source env.sh                      # 4.34.1, LEAN_PATH rooted at tree/build/lib
cd tree
lean CheckBoth.lean                # 5 headline statements, [propext, Classical.choice, Quot.sound]
lean CheckAudit.lean               # axioms of the audit theorems
lean Chk2.lean ; lean Chk3.lean    # axioms of the remaining audit theorems
cd .. && python3 build.py          # 90/90 modules, 0 failures (13m28s cold)
# stock toolchain:  bash ../m4/d7.sh tree tree433 3   -> 90/90 modules, CheckBoth re-certified
```

State: `tree/OAI` = staged tree + the scaffolding compaction of `MEASURE.md` + the five
modules below. 90 modules, 31956 lines, `CheckBoth.lean` re-certifies all five headline
statements with `[propext, Classical.choice, Quot.sound]`. Under stock 4.33.1 the same tree
(plus the m8 port edits) is 90/90 and re-certifies identically.

## V1. m15's tower is vacuous — REFUTED, machine-checked

`tree/OAI/MeasureTheory/CompactFactors/TowerAudit.lean` (323 lines, axiom-clean) transcribes
m15's `Tower` verbatim and proves:

* `tower_max_all_factorizable`, `tower_max_generating`: at a maximal member of that class
  **every** bounded measurable function — in particular the identity — is factorizable
  through the member. The proof is m15's own maximality argument from
  `exists_ergodic_factor`, with its `_hc` field discarded. The defect is internal:
  `Tower.step` accepts any bounded non-factorizable `H` and has no compactness hypothesis,
  so the class is the class of all countably generated factors.
* `diffLaw_id_eq_dirac_of_generating`: at a generating factor `condDistrib id p μ` is
  deterministic, so the identity's relative difference law is `Measure.dirac 1` on `D`.
* `diffLaw_id_apply_C_of_generating`: its `C`-mass is `1`, because `1 = j 0 ∈ C`.
* `not_universalGood_of_generating`, `relDiffLaw_id_ne_zero_of_generating`: `GoodId` —
  hence `UniversalGood` at `d = id` — fails at every generating factor of a wild `μ`.
  **Necessary condition:** no factor witnessing `TerminalObligation` can be generating.
* `hgood_false`: for every wild `μ` with `ErgodicSMul K D μ`, the hypothesis `hgood` of
  `exists_terminal_factor_of_tower_good` — equivariance + `Tower` + maximality + ergodic
  relative square + `UniversalGood` — is **false**. m15's drop-in replacement is vacuous,
  and its `exists_ergodic_factor` is true but trivial (its `p` is generating for every `μ`).

## V2. The missing hypothesis, restored — `TowerCorrect.lean`

`TowerC` is m15's tower with `step` carrying the clause `strict_compact_successor` actually
returns:

```
∀ F, Measurable F → (∃ C, ∀ z, ‖F z‖ ≤ C) → Compact (μ.map (extend p H)) Prod.fst F
```

Proved there (153 lines, axiom-clean): `TowerC.toTower` (the correction removes members,
adds none), `exists_towerC_maximal`, `exists_ergodic_factor_C` (maximality plus ergodicity
of the relative square — same proof as m15, the successor's clause is exactly what
`strict_compact_successor` supplies), and `exists_terminal_factor_of_towerC_good`.
`TowerAudit.tower_max_all_factorizable` does **not** apply to `TowerC`.

## V3. `At`/`Compact` vs precompact orbits — true at the point factor, false elsewhere

`OrbitBridge.lean` (157 lines): `orbit_totallyBounded_of_compact_point`. If
`CompactFunctions.Compact μ (pointFactor X) H` then the `K`-orbit of `H` is totally bounded
in the `L²(μ)` seminorm (`OrbitTB`). At the point factor the coefficient functions are
evaluated at a constant, so the approximating family is a bounded subset of a
finite-dimensional space; a finite net of the coefficient ball then nets the orbit.

At a non-point factor the implication fails: `a` ranges over all `q`-measurable coefficient
functions with `‖a‖ ≤ B`, and `{a * f}` is not totally bounded in `L²` for nonzero `f`. So
`At` is strictly weaker there, `At` is not composable, and `strict_compact_successor`'s
output can be used one level deep only. Concretely: the *first* step of the corrected tower
puts the new factor inside `A := {H : orbit totally bounded}` (apply V3 to its `hc` clause,
which is compactness over the point factor); every later step needs the
Furstenberg–Zimmer transition lemma (abandoned d6) to transfer `A` from `p` to `extend p H`.

## V4. The ready-made components are real

`tree/audit/` keeps m5's `A.lean`, `B.lean`, `C.lean` (Theorem A:
`relative_singularity_of_ergodic`) and m7's `TerminalGlue.lean` as they were delivered; all
elaborate here unmodified and `TerminalGlue`'s theorems are axiom-clean. `TerminalGlue` is
also installed as a first-class module (`tree/OAI/Analysis/PlaneSpectrum/TerminalGlue.lean`),
so the obligation is part of the tree:

```
TerminalObligation μ  ≡  ∃ p, Measurable p ∧ (∀ k, p (k • d) = k • p d a.e.)
                          ∧ GoodId μ p ∧ ErgodicVAdd Rot (D×D) (RelativeProduct.law μ p hp)
TerminalObligation μ → (IsWild μ) → z ≠ 0 → ∫ d, eval z d ∂μ = 0
```

`WeakMixingTerminal.lean` (95 lines) adds the positive witness: `law_const` (at a constant
factor the relative product *is* `μ.prod μ`) and hence
`terminalObligation_of_square_ergodic : IsWild μ → ErgodicVAdd Rot (D×D) (μ.prod μ) →
TerminalObligation μ`. So the obligation is satisfiable with no new mathematics whenever
`μ` is weakly mixing — the endpoint of the census.

## V5. The census cannot discharge the one call site

`ergodic_wild_fourier` is consumed only at `Ergodicity.lean:351`, inside `wild_fourier`, on
the ergodic-decomposition fibre `condDistrib id (InvariantDecomposition.code μ M) μ y`.
`fiber_ergodic` gives ergodicity of that fibre and nothing else. There is an ergodic wild
measure on `D` that is not weakly mixing: **Haar measure on `D`** — K-invariant (the action
is by automorphisms), ergodic (`L²(D) = ⊕_y ℂ·eval y` and the K-orbits of characters are
infinite, so invariants are constants), not weakly mixing
(`(x,x') ↦ eval y x · conj(eval y x')` is a non-constant invariant unit vector in
`L²(μ×μ)`), and wild (`μ(C) = 0`: `C` is a Borel, non-open subgroup, hence meagre by
Banach–Pettis, hence null). So the point factor is unavailable at that site and a
nontrivial terminal factor is genuinely needed. This part is a paper-level argument, not
machine-checked; the three nontrivial inputs are named above.

## Verdict on the 1500-line target

The chain is: headline → `wild_fourier` → `ergodic_wild_fourier` (ergodic case) → a factor
with `GoodId` and ergodic relative square. Maximality over the corrected tower gives the
ergodicity half for free (V2). The remaining input is properness of that factor, i.e.
`L²(p) ⊆ A` for corrected-tower members together with `(N)`. V3 says the tree's `At`
predicate supplies `L² ⊆ A` at the first step and fails afterwards; so the precise place
where the deletion stops being collectable is the transition lemma

```
Compact(over p) ∧ L²(p) ⊆ A  ⟹  L²(extend p H) ⊆ A
```

(abandoned d6) together with `(N)` (abandoned d3). With both, the corrected tower gives
`TerminalObligation` and the whole `UniversalGood` induction — the 4112 declaration-line
zone — is dead code. Without them no route I can certify reaches 1500 lines: V5 removes the
weak-mixing shortcut, and `MEASURE.md` records that the only mechanical savings available
are 174 lines of scaffolding (net −133 against the 31277-line baseline).

This is acceptance (b): the realised figure with a certificate, and the exact lemma at
which the zone stops being deletable.
