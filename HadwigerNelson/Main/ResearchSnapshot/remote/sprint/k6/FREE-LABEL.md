# Non-proper self-avoidance kills nothing: free-label countermodels for every cycle length

**Result.** For every `ell in {3,4,5,6}` there is a translation-invariant sector palette field at
`k = 6` satisfying

* the palette bound `1 <= |P| <= 3`;
* the edge exclusions of `C_ell` (Lemma 6.2, (6.2));
* the sixty-degree exclusion `P(e) cap P(Re) = empty` at every direction (5.7);
* the exact two-centre transport (5.3) for all pairs of centres at distance `<= d_0 = pi/(9m)`;
* **non-proper self-avoidance**: there is a fixed label `i` with `i notin P_z(e)` for every
  centre `z` and every direction `e`;

and whose set of `ell`-cycle points is the whole plane, with infinitely many of them accumulating
in a disc of radius `d_0`. Consequently, adding non-proper self-avoidance to the palette
constraints does not exclude any cycle length.

**Status, updated (accepted in `smwfwi7rh` d14/d18 and `smwfwznwk` d1/d2/d3).** These fields are
not countermodels to anything, and the sentence that used to stand here — "the only constraint
that removes these models is properness" — was too weak. They are all centre-independent (or
piecewise so), so they violate the **unit-separation transport** `(TE)  P_{x+a}(f) cap P_x(f) =
empty` at `|a| = 1`, which is Lemma 5.2(3) at Remark 5.3's instance `(x+a)+f = x+f+a`; hence no
such field is any colouring's maximal palette. And the class is closed outright inside the palette
framework: a globally free label forces its own class to be plane-null by Fubini over circles
(`smwfwznwk` m2, Theorem R), and at a unit triangle the three palettes are pairwise disjoint
nonempty subsets of the five remaining labels, so `2+2+2 > 5` (`smwfwznwk` m4, machine-checked in
`../../.ultramath/smwfwznwk/m4/count_lemma.lean`). So the free-label class is empty before
properness is ever mentioned.

## The constructions

Let `m = 6`, `n = 36`, `Delta = 2 pi/n`, `L = 2m/3 = 4`, and let sector `i` be
`[i Delta, (i+1) Delta)`. For `ell = 3,4,5` use the block word

  `sigma(i) = M_{floor(i/L) mod 3}`,  `P_z(theta) = sigma(floor(theta/Delta))`,

with the three pairwise disjoint admissible palettes

| `ell` | `M_0` | `M_1` | `M_2` | free label |
|---|---|---|---|---|
| 3 | {3} | {4} | {5} | 0, 1, 2 |
| 4 | {0,2} | {1,3} | {4} | 5 |
| 5 | {0,2} | {1,3} | {5} | 4 |

For `ell = 6` the three-block table has no free label: every admissible palette for a six-cycle
has size at least 2 (every label lies in a cycle edge), so three pairwise disjoint admissible
palettes cover all six labels. A free-label field nevertheless exists, and it can be taken
**pair-valued**: the period-12 word (free label `0`)

```
[1,3] [1,3] [1,3] [1,4] [1,4] [2,4] [2,4] [2,4] [2,5] [2,5] [3,5] [3,5]   (repeated 3x)
```

satisfies all six transport offsets `{+-5,+-6,+-7} mod 36`. It is SAT for `n = 30,36,42,48,60,72`
and UNSAT for `n = 12,18,24`, by two independent complete searches agreeing on all six free
labels (`m10`, `smwfwi7rh`; `verify.py`/`verify_indep.py`). An earlier 36-sector word with the
ternary value `{2,4,5}` was withdrawn: in a centre-independent field the unit-triangle bound
gives `3|P| <= 6`, so `|P| <= 2` (m10, Corollary 6).

## Why this is the right sharpening

The transport offsets are exactly the sector displacements produced by the two exact unit
decompositions of `(z'-z) + f`: the geometric lemma (m15, exact rational arithmetic) gives
`|arg s_\pm - (arg f \pm pi/3)| <= 1.5938 d`, and `d <= d_0 = Delta/3` makes the displacement at
most `0.531` sectors, i.e. `m + k` with `k in {-1,0,1}`. The check `1.5938/9 < 1/3` is exact
(`.scratch/sprintB/free_label_all.py`). The centres `y_k = (d_0/3) 2^{-k} (3/5,4/5)` are distinct
and accumulate at `0`; the field is translation invariant, so every `y_k` is an `ell`-cycle point
in the (6.2) sense (each palette is admissible, hence not contained in any cycle edge).

## Consequence for the frontier (corrected)

Every palette-level necessary condition used in the paper's §6, **plus** non-proper
self-avoidance, is satisfied by an accumulating model for every cycle length. The singleton
triangle model even satisfies (5.2) with the constant colouring `c = 1`. But these models are all
**centre-independent**, and `m10`'s Theorem 2 removes them with the endpoint trace alone: for a
centre-independent field, the endpoint trace `c(x+e) in P_x(e)` plus self-avoidance
`c(x) notin P_x(e)` contradict by Fubini; no joint measurability is needed. `m10`'s Theorem 4
shows in addition that endpoint trace (5.7) is already properness: every unit pair is a
`(z+e, z+Re)` pair, so the endpoint trace is a proper colouring. So the frontier has no middle:

  palette axioms alone                          : satisfiable, accumulating, every length;
  palette axioms + any trace function           : satisfiable iff chi(R^2) <= 6.

The countermodels fail a condition *weaker* than properness (the endpoint trace), and adding any
trace function collapses to the original problem.

The exact certificates are `.scratch/sprintB/six_free_witness.json`,
`.scratch/sprintB/free_label_all.py`, `.scratch/sprintB/six_sat2.py`; the block-shift check for
the three-block tables is `sprint/k6/uniform_nogo.py`.
