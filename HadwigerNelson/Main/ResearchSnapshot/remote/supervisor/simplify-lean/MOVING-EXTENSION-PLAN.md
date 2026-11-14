# Moving-centre extension V2 — packet, manifest, and what remains (block 22)

Source/verification block. **No Lean run.** Grades: **[C] computed**, **[M] paper argument checked**,
**[P] proposed/uncompiled**, **[S] reported**.

## 1. Contents of the packet

`supervisor/simplify-lean/threecentre/MovingThreeCentres.lean` — 259 lines, sha256
`bfed2bad744e08156e8a26a4009220e01826c78e4556ea3ce9135fe1af30ede9`. Six items, in the order the
task asked for:

| § | declaration | role |
|---|---|---|
| 1 | `avoidingTraceCentre K` | `Z_K`, a set in the plane depending only on `c` and `K` |
| 2 | `triangle_no_unit_of_avoiding_traces` | the factorised core: two **actual** `K`-avoiding traces at `x + direction a_y`, `x + direction a_z`, positive `J`-state at `x` |
| 3 | `fixed_state_no_unit_three_centres` | V1's statement, now a 5-line wrapper over §2 |
| 4 | `avoidingTraceCentre_seqClosed`, `isClosed_avoidingTraceCentre` | sequential closedness of `Z_K` |
| 5 | `strict_state_sequence_no_unit_three_centres` | converging centres |
| 6 | `four_support_sequence_no_unit` (own section, `c : ℂ → Fin 5`) | unchanged four-support consumer |

V1 is **preserved byte-identically** at `threecentre/FixedStateThreeCentres.V1.lean`, sha256
`af45ff16cfe059ce3534a8c3362ec941211ea0cc15e6d30503e558371364135b`. V2 uses the three repaired API
idioms throughout: `RealState hc x A J` (`c` implicit), `QuotientAddGroup.mk_surjective` to turn the
`Angles` returned by `direction_exists` into a real angle, and
`((frequently_ae_mem_iff.mpr hp.ne').and_eventually hae).exists` for the positive-AE witness.

## 2. [C] Hole scan

Comment-stripped count in `MovingThreeCentres.lean`: `sorry` 0, `admit` 0, `BLOCKER` 0, `sorryAx` 0.
Sections are balanced (`section Generic`/`end Generic`, `section FourState`/`end FourState`). There is
no admitted goal anywhere and nothing is left as a named hole.

## 3. [M] The sequential-closure lemma, as implemented

`IsSeqClosed (Z_K)`: given `y_n → y` and `β_n` a `K`-avoiding trace at `y_n`, extract a convergent
subsequence with `isCompact_univ … .isSeqCompact.subseq_of_frequently_in` (the same call
`BoundaryTrace:24` uses), then:

* `trace_limit c hc (fun n => hβ (φ n)) (hylim.comp hφ.tendsto_atTop) hcon` gives `IsTrace` at `y`;
* for `i ∈ K`, `traceCode_tendsto_iff.mp hcon i (traceValue β₀ i)` tests the weak convergence at the
  limit coordinate itself; every term is `⟪0, ·⟫ = 0`, so `tendsto_nhds_unique` gives
  `⟪traceValue β₀ i, traceValue β₀ i⟫ = 0`, and `inner_self_eq_zero` gives `traceValue β₀ i = 0`.

This is the `BoundaryTrace:24-52` idiom, and it deliberately **does not assert continuity of
`traceValue`** — only the inner products along the sequence are tested, which is exactly what
`traceCode_tendsto_iff` provides. No projection-of-closed-set API is used either; `ℂ` is metrizable so
`IsSeqClosed.isClosed` suffices.

## 4. [M] The converging-centre theorem, and why two different subsequences are legitimate

`x_n → y`, `B_n` a `K`-state at `x_n`, `A` a positive `J`-state at `y`, `b_n → b₀`, `d_n → d₀` with
`b_n, d_n ∈ supp(volume|B_n)`. Then `‖direction b₀ − direction d₀‖ ≠ 1`.

Proof: (S) puts each `x_n + direction b_n` and `x_n + direction d_n` in `Z_K`; continuity of `x ↦ x +
direction x` gives convergence to `y + direction b₀` and `y + direction d₀`; closedness puts both
limits in `Z_K`; §2 applied at centre `y` with those two traces gives the conclusion.

The two limiting traces may come from different subsequences. That is harmless here and I want it on
the record: each is an *actual* trace at its own limit centre, and the palette theorem used in §2 is
stated for the entire palettes at those two centres. Only a finite intersection of their conull
constraints is taken afterwards. This is not the same as selecting unrelated angular state values and
claiming they form one joint word.

## 5. [C] The four-support instantiation is hypothesis-for-hypothesis

`r := if s = 1 then 2 else 1`, `K := fourGroup s`, `J := fourGroup r`, `X := 4`:

* `hlabels` from the same `by decide` computation the original uses;
* `B n := fourRealState (x n) s` with `RealState` from `fourState_represents c hc hw (hx n) s`;
* `A := fourRealState y r` with `RealState` from `fourState_represents c hc hw hy r` and positivity
  from `four_realState_positive c hc hw hy hr`;
* the support hypotheses are definitionally `fourSupport`.

So `four_support_sequence_no_unit` is proved with **every original hypothesis and binder unchanged**,
and the proof consumes neither `four_realState_continuity` nor `strict_state_sequence_false`. Note
that `four_realState_positive` goes through `fourState_diagonal_positive`, which uses the older
`two_state_impossible` — not the strict-state chain. The source's separate
`four_support_continuity` still uses L1 continuity and is untouched.

## 6. [P] What a first local run may need, in likelihood order

1. `avoidingTraceCentre_seqClosed`'s `choose β hβ hβK using hy` on a hypothesis of the shape
   `∀ n, ∃ β, P β ∧ Q β` — if `choose` balks, `Classical.choose` + `choose_spec` is the fallback;
2. `IsSeqClosed.isClosed` needing a `FrechetUrysohnSpace ℂ` instance — present in recent Mathlib, but
   this is the one instance I could not confirm from the tree's own usage;
3. `traceCode_tendsto_iff.mp hcon i (traceValue β₀ i)` argument order (the tree uses the same shape at
   `BoundaryTrace:24-52` and `Compactness:302`, so low risk);
4. `hxt.add (direction_continuous.continuousAt.tendsto.comp hbA)` — `Tendsto.add` on `ℝ`-valued
   coercions; `direction` is `Angles`-valued on `(b n : Angles)`, so the term is `ℂ`-valued and adds
   cleanly.

None is a mathematical gap; each is a name or instance question that fails at one line.

## 7. Manifest

| item | sha256 |
|---|---|
| `threecentre/MovingThreeCentres.lean` | `bfed2bad744e08156e8a26a4009220e01826c78e4556ea3ce9135fe1af30ede9` |
| `threecentre/FixedStateThreeCentres.V1.lean` (preserved) | `af45ff16cfe059ce3534a8c3362ec941211ea0cc15e6d30503e558371364135b` |
| `lean/OAI/Geometry/PlaneColoring/FiveSupport.lean` | `6d54703f840a1b4d20b81f5f206b18d79a1fbacde9a481990049b3c41b9c4813` |
| `lean/OAI/Geometry/PlaneColoring/BoundaryTrace.lean` | `c3c0c75a0fb2e2184e8ff39562faac2c38e3d372864ddeca9eb942fa0f2a692f` |
| `lean/OAI/Geometry/PlaneColoring/FourContinuity.lean` | see STATUS |
| `lean/OAI/Geometry/PlaneColoring/States.lean` | `941fcbdcd90fb50426d4588d62ea10f9bdc882d455f546f2095ead91a0439340` |

Imports: `FiveSupport`, `BoundaryTrace`, `FourContinuity` — three modules, all read-only. Build:
`source scripts/env4341.sh; lean supervisor/simplify-lean/threecentre/MovingThreeCentres.lean`.
The four `#print axioms` lines are the last statements before `end`; each must be a subset of
`{propext, Classical.choice, Quot.sound}`.

## 8. Scope, stated precisely

* The V2 contract **adds** `x_n → y` and a genuine positive `J`-state at `y`; it **removes** all `A_n`
  and their local L1 convergence. I do not claim the two contracts are equivalent in general, and I do
  not claim the arbitrary-centre `strict_state_sequence_false` under its unchanged hypotheses.
* `Z_K` closedness is a statement about a *global* closed set in the plane. It is **not** a claim that
  angular state supports vary upper semicontinuously with the base centre — the avoiding-trace set is
  larger, which is exactly why it is closed and why it suffices.
* Nothing here is a global colouring result. No deletion is performed, and none is claimed: the
  strict-state chain is still present, and `indicator_inter_positive` in particular must not be deleted
  (`FourContinuity:326` uses it).
* The dependency-reduction claim of the A2 note (that all *used* paths to the chain can be removed) is
  a **candidate**, contingent on both application proofs being independently accepted; this packet
  supplies one of the two (the four-support one) and the earlier banked pair covers FiveSupport.
  `strict_state_uniform_on_compact` has no consumers in the source, so it would retain the chain only
  as unused library content.
