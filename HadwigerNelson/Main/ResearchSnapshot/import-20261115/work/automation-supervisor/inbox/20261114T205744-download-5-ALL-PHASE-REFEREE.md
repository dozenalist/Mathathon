# Referee: all-phase completeness of the fixed-phase census  (rev. 2 — §2 corrected)

Referee of the fixed-phase census (177 SAT / 7599 UNSAT / 862 genuine) and of whether all SAT phases can
coexist as one measurable one-centre palette field. Swarm of this block `smwgukvpp` (`m1`, `m2`;
`deepseek/deepseek-v4.1-flash`, effort `max`): `m1` accepted, `m2` (per-cell table) still running.
Verifier: `CHECK-ALLPHASE.py` (exact `Fraction` arithmetic).

**Revision note.** §2 of the first version was wrong and is replaced. I had read a census class `τ` as the
direction vector `α_i = 60τ_i + 30` and concluded that the census is a "wall census" whose verdicts are
about measure-zero strata. That is false: `τ` is the six-phase *sign pattern* of `(α, t)` for a base phase
`t`, each class is realised on an open set of `(α,t)`, and the per-phase verdicts are therefore
statements about positive-measure sets. The retracted sentences are listed in §2.3 so they are not
re-used.

---

## 1. The census itself: reproduced, and robust to palette size

Reproduced exactly: `7776` classes, `SAT 177 / UNSAT 7599 / genuine 862`, match `True`. Re-ran with **all
palette sizes `0..6`** instead of the script's pairs-only model: **still exactly 177**. So the pair
restriction — not source-licensed at `k = 6`, since `palette_cardinality` is `Fin 5` — is not
load-bearing.

---

## 2. What a census class actually is (corrected)

Fix a direction vector `α` and a base phase `t` that is not critical for any `i`, i.e.
`t + 60j ≠ α_i ± 90°` for all `i, j`. The six phases of the orbit are `t, t+60, …, t+300`. Interface `i`
is positive at phase `t+60j` iff `(t + 60j − α_i) mod 360 ∈ (−90°, 90°)`, an interval of length `180°`,
so it contains **exactly three** of the six phases, and those three are cyclically consecutive. Hence the
row `j ↦ sign_i(t+60j)` is a cyclic shift of `PAT = (+,+,−,−,−,+)`, and `τ_i` is the slot the block is
centred on:

```
τ_i = round((α_i − t)/60°) mod 6 ,        sign_i(t+60j) = PAT[(j − τ_i) mod 6] .
```

Verified by execution: over 200 000 random `(α,t)` pairs the census formula reproduces every row with
**0 mismatches**, and the classes attained by `(α,t)` range over all of them (45996 = `7776 × 6`
unnormalised instances before the rotation normalisation `τ ↦ τ − τ_0`).

Consequences, which are the ones that matter:

* **A class is a property of `(α, t)`, not of `α`.** `τ` encodes `(α_i − t) mod 60°` for each `i`;
  two interfaces share `τ_i` iff `α_i ≡ α_j (mod 60°)`, not `(mod 180°)`.
* **Every class is realised on an open set of `(α,t)`.** `τ` is locally constant off the arrangement
  `{α_i ≡ t ± 90° (mod 60°)}`, so its preimage is a union of open cells of that arrangement. No class is a
  measure-zero accident.
* **An UNSAT class excludes an open set of data, not a stratum.** If the class at some phase orbit is
  UNSAT, then no palette assignment exists for the six phases `t+60j` of that orbit, so no relaxation
  field exists — and the set of `(α,t)` with that class is open, hence of positive measure.
* The surviving configurations are those whose **whole staircase** (the cyclic sequence of classes as `t`
  runs over `ℝ/60ℤ`) consists of SAT classes. That is the "staircase classification".

### 2.3 Retracted sentences (do not reuse)

* "Every one of the 7776 census classes has at least one pair of parallel or antiparallel interfaces."
  — false; wrong identification of `τ` with a direction vector.
* "No census class is a point of an open cell of direction space." — false, see above.
* "The census is a wall census." — false.
* "Its SAT verdicts are statements about measure-zero strata." — false.
* Script check D of the first version, which asserted "177 of 177 SAT classes carry a tie" via
  `τ_i mod 3`, is withdrawn for the same reason. It measured a property of my wrong parametrisation.

---

## 3. The empty-residual rule (unchanged, and it is what does the work)

> **Empty-residual rule.** With `WeakColoring 6 c`, `E_i = {i,i+1}`, and a centre `x`: if at some phase
> `t` the interfaces `0, 2, 4` (or `1, 3, 5`) are all outer — equivalently their directions lie in a
> common open semicircle — then `False`. Because `E_0 ∪ E_2 ∪ E_4 = Fin 6`, so
> `continuum_outer_restriction` with `F = {0,2,4}` demands `palette(x,t) ∩ ∅ ≠ ∅`. The inner side gives
> the same rule with the roles of the two sides exchanged.

This is per-phase, so it holds for arbitrary measurable fields, and it needs no census at all. `m1`'s
counterexample `α* = (0,2,3,184,185,186)` is an instance on the inner side: at `t = 92.5°`,
`F⁻ = {0,1,3,4,5} ⊇ {1,3,5}`, so `J(F⁻) = ∅`, and that phase is not critical.

**(E) A generic scan — restated, and reconciled.** My scan of 200 random direction vectors with all six
directions distinct mod `180°` returned **0** with a relaxation field, 196 killed by the empty-residual
rule, 4 by the assembly. That number is a *step-field* count (a field constant on sign arcs), which is
stronger than all-phase existence; it is also consistent with the graph team's staircase census, as the
parent points out: survivors among 6-singleton-block chains are `8640/(7776·720) ≈ 0.15 %`, so the
expected count is `0.6` per 400 samples and `1.4` per 900 (`m1`'s independent 1/900 sits exactly there).
A 0/400 observation is therefore unremarkable, not evidence of a stronger theorem. Recorded as
reconciliation.

---

## 4. The gap that survives: SAT at one orbit does not give SAT at all orbits

This is `m1`'s result and I verified it independently. The correct reduction (his, which I adopted over my
clumsier overlap-graph version):

> `(C2)` couples only `t` to `t+60`, so the constraint graph's components are the shift orbits. A
> relaxation field exists **iff** the 6-cycle CSP `Q_k ∩ A(t+60k) ≠ ∅`, `Q_k ∩ B(t+60k) ≠ ∅`,
> `Q_k ∩ Q_{k+1} = ∅` is solvable at one representative `t` per arc of `ℝ/60ℤ` cut by
> `{α_i ± 90 mod 60}`. `|Q_k| ≤ 2` is WLOG — by *shrinking* (take one element of `A_k` and one of `B_k`;
> disjointness survives because subsets of disjoint sets are disjoint), not by monotonicity.

So the fixed-phase census answers "is this orbit class SAT?" and the configuration survives only if
every orbit class in its staircase is SAT. `m1`'s `α*` is the sharp witness: all six phases of the orbit
`t = 0,60,…,300` satisfiable, yet the orbit at `t = 31` is contradictory and the phase `t = 92.5` fails
outright.

---

## 5. Relaxation versus producer

UNSAT transfers to colourings, because every condition used is a source theorem — that is why the
empty-residual rule is a real theorem and why an UNSAT class excludes an open set of data. SAT does not:
nothing in the tree builds a `WeakColoring6`, or a colouring with prescribed traces, from a palette
field, and a step field is already realisable as a trace with `∑_i trace_i = 1`, so the trace structure
adds no further one-centre relation. `m1`'s non-uniqueness (4 cyclic 2-set solutions on the equilateral
hexagon orbit, two distinct fields) shows `(C1)-(C3)` do not determine `Q`.

---

## 6. Validation status, and the two sample-dependent figures

* Verified by execution: the census counts; the palette-size robustness; the `(α,t)` parametrisation of
  §2 (200 000 pairs, 0 row mismatches); the generic scan (E, 200 samples, seed `2024`); the
  tie-resolution scan (F, 177 classes × 7 resolutions).
* Proved on paper: the empty-residual rule; `m1`'s reduction and the shrinking WLOG; the statement that an
  UNSAT class excludes an open set of `(α,t)`.
* **Sample-dependent, not rates, and not to be compared:** my tie-resolution count (`21` of 177 have at
  least one SAT resolution among 7 sampled perturbations) and `m1`'s (`7`–`14` lost under three random
  perturbations) are counts under different perturbation families. They show the same qualitative
  phenomenon; neither is an estimate of a proportion.
* Not claimed: any chromatic bound; any proportion or rate; any statement that a SAT class extends to an
  open set of direction vectors by itself (it extends to an open set of `(α,t)` pairs only).
* No Lean. The paper steps are against `continuum_outer_restriction` (`AngularBoundary.lean:259`),
  `continuum_inner_restriction` (`:279`), `palette_sixty_disjoint` (`PaletteTransport.lean:450`),
  `finite_support_exclusion_ae` (`:317`).

## 7. Files

| file | what it is |
|---|---|
| `ALL-PHASE-REFEREE.md` | this note (rev. 2) |
| `CHECK-ALLPHASE.py` | bounded local verifier: (A) control fields, (B) tie-resolution scan, (C) empty-residual rule, (D) the `(α,t)` parametrisation of §2, (E) generic scan, (F) resolution scan |


---

## 8. Addendum after the swarm closed (m2's unsubmitted classification)

`m2` (direction d1) ended without submitting, but left `theorem.md`, `referee6.py`, `cert3.py`. I ran the
scripts and reproduce their output: **933120** resonance cells (components of `T^6 ∖ {α_i ≡ α_j mod 60°}`),
of which **1440** admit a relaxation field, 919512 fail by an empty `A`/`B` on some arc and 12168 fail by
the `(C2)` orbit system alone; the SAT set therefore has Lebesgue measure **exactly `1/648`**, and only 16
of the 3840 sign cells meet it. Its §7 criterion answers the completeness question cleanly: the
fixed-phase census decides the relaxation problem for `α` **iff** `α_i − α_j ∈ 60°ℤ` for all `i,j`;
otherwise it is a strictly weaker one-orbit test.

Two consequences for this note:

* **The reconciliation is now exact, not statistical.** `1/648 = 0.1543 %` is the same number as the graph
  team's `8640/(7776·720) = 0.1543 %`. My 0/400 and `m1`'s 1/900 are samples of a set of measure 1/648,
  as recorded in §3.
* **One sentence of mine (rev. 1, §5) is superseded.** It claimed the SAT status is constant on the cells
  of `{α_i ≢ α_j mod 180°}`. `m2`'s (4.3) refutes that: the status is constant on the *resonance* cells
  (`mod 60°`), not on the finer sign cells, and it exhibits an explicit pair — `(0°,30°,90°,150°,240°,300°)`
  with a field and `(0°,108.75°,123.75°,142.5°,292.5°,315°)` without — inside one sign cell. The correct
  statement is the resonance-cell one.

Caveat: `m2` never reached a verdict, so nothing here is accepted work; I reproduce its script output only
and have not audited its definitions or its proofs.
