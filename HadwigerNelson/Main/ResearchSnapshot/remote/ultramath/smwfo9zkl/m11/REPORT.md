# m11 report (sprint B, direction d6)

## What is delivered

**Theorem A (proved; machine-checked in `lean/K6Ternary.lean`).** For a weak measurable
`k`-colouring with `k >= 6`, at every centre `x`
`sigma{e : |P_x(e)| = k-3} <= 1/2`. At `k = 6` this reads: three-label palettes occupy at
most half the direction circle, at every centre. Proof: (5.2) forbids
`P_x(e) ∪ P_x(v) = I` for a.e. pairs, (5.7) makes `P_x(e)` and `P_x(Re)` disjoint; at
`k = 6` two disjoint ternary palettes are exactly complementary (the label count
`2(k-3) = k`, special to `k = 6`), so `|P_x(e)| = |P_x(Re)| = 3` is impossible a.e.

**Theorem B (proved).** For any nonempty label set `T` and any centre,
`sigma{e : T ⊆ P_x(e)} <= 1/2`. Hence no centre has an a.e. constant palette, at any `k`.
Corollary: at a `k = 6` triangle centre, the palette equals the full triangle triple on at
most half the directions, hence meets the outsider triple on at least half.

**Theorem C (a trap, proved).** There is **no** 120-degree single-centre exclusion
`P_x(f) ∩ P_x(R²f) = empty`. At a single centre (5.3) reads `x + F = x + s(F) + t(F)`, so
`s` and `t` are each at 60 degrees from `F`; every single-centre exclusion coming from
(5.3) is (5.7) again. Using the false 120-degree constraint makes the finite system of §5
unsatisfiable at `k = 5`, which is how the error showed up.

**Decided finite computation (two independent procedures).** All single-centre palette state
systems at a `k = 6` cyclic centre, for cycle lengths 3, 4, 5, 6: exact counts, and
* the maximal density of three-label palettes is `1/2` in every case (so Theorem A is sharp
  for this constraint list);
* for every cycle length there are admissible systems with **no** fixed pair meeting all
  palettes — so the paper's `k = 5` triangle mechanism (a fixed binary pair, then Lemma 5.5)
  cannot be transferred to `k = 6` from these constraints;
* the `k = 5` control: all 2600 admissible triangle state systems are binary for the outside
  pair, reproducing paper Theorem 6.5's triangle conclusion.

**Certificate in §5.4** of `k6-ternary-palette.md`: an explicit seven-centre palette system
satisfying the 60-degree exclusion, the (5.2) union constraint, the palette bound, the (6.2)
exclusions of a triangle, **and** the two-centre translation exclusion at all twelve
unit-separated centre pairs, with three-label palettes on three of six directions at `x`.
So the constant `1/2` is not improved by the two-centre exclusion on that configuration.

## What is not delivered

`|P_x(e)| <= 2` at `k = 6` — the missing input of `results/K6-BARRIER.md` §5 — is not
proved, and §6 of `k6-ternary-palette.md` explains why the constraint list used here cannot
give it. Consequently no local-finiteness statement, no §7 transfer and no `chi(R^2)` claim
is made. This is a partial result about the `k = 6` palette system, not a solution of the
sprint problem.

## Files

| file | content |
|---|---|
| `k6-ternary-palette.md` | Theorems A, B, C, Corollary, finite classification, seven-centre certificate, hypothesis audit, gap statement |
| `lean/K6Ternary.lean` | machine-checked finite lemma + `2 * mu {e : |P e| = 3} <= 1` + no a.e. constant palette |
| `lean/K6Finite.lean` | same finite lemma with light imports, plus the six-cycle independent-set bound and its attainment |
| `verify/state_models.py` | the two independent decision procedures (streaming DFS; MILP via HiGHS) |
| `verify/state_models_results.json` | their output |
| `verify/joint_centres.py` | exact seven-centre certificate of §5.4 |

## Commands (all run in this VM)

```
lean lean/K6Finite.lean          # exit 0, ~1 min
lean lean/K6Ternary.lean         # exit 0, ~5-15 min; only deprecation warnings
python3 verify/state_models.py   # ~70 s, prints the table and writes the JSON
python3 verify/joint_centres.py  # prints "ALL CONSTRAINTS PASS"
```

## Cross-checks against the rest of the swarm

* My per-cycle palette counts at `k = 6` (`35, 33, 31, 29`) and at `k = 5` for the triangle
  (`9`) agree with m5's independent computation (direction d4,
  `.ultramath/smwfo9zkl/m5/cycle_strata.py`, closed form plus brute force).
* Theorem A is consistent with the two explicit objects the swarm has: m3's proper measurable
  7-colouring with accumulating cyclic centres has `|P_x(e)| <= 3 < 4 = k-3` everywhere
  (direction d11, `.ultramath/smwfo9zkl/m3/w/verify.py`), and m13's `k = 6` palette model
  with the triangle at every point has `|P| = 2` everywhere (direction d5,
  `.ultramath/smwfo9zkl/m13/model_check2.py`). Neither can test sharpness; the finite models
  of §5 do.
* Relation to the current state of the route: m5 proved `L` is nonempty (indeed `5 sqrt 2`
  dense) at every `k >= 3` and identified the input §7 really needs (finiteness of `L` in one
  closed square of side `> 2`); m3 proved local finiteness of `L` fails for every `k >= 7`;
  m13 proved the triangle case of Theorem 6.5 cannot be recovered at `k = 6` from
  palette-level data. The present note adds a palette-cardinality fact (`1/2`) that is
  independent of all three, with a machine-checked proof and a sharpness computation; it does
  not close any of them.
