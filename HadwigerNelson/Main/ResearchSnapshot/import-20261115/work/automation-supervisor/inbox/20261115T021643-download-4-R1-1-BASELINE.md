# R1-1 acceptance baseline (judge side) — L-R1

**Status of this file.** This is the *parent's own* exact reproduction of the R1-1 model, written
from the R1-1 statement only, for use as the acceptance standard when judging swarm
`smwh3mq7r`. It is not a swarm submission and it is not a new claim about the paper or about
`chi(R^2)`. Code: `checks/r11_baseline.py` (+ `checks/r11_baseline.json`),
`checks/signcell_confirm.py` (+ `.json`). No other lane's script is imported or read.

Method: three structurally different SAT deciders —
(A) recursive DFS over minimal hitting-set palettes; (B) non-recursive reachable-set DP;
(C) *unrestricted* search over all non-empty masks (minimality not assumed) —
plus label-level and palette-level unit propagation. Angles are `Fraction` degrees; every cos
sign is decided by exact rational comparison against ±90. No float in any decision.

## 1. Every R1-1 figure, with its verdict

| R1-1 claim | R1-1 value | this reproduction | verdict |
|---|---|---|---|
| (a) SAT classes | 177 | **177** | MATCH |
| (a) UNSAT classes | 7599 | **7599** | MATCH |
| (a) UNSAT with Rp, Rn non-empty at all six phases | 862 | **862** | MATCH |
| (a) UNSAT classes with an empty side somewhere | (6737) | **6737** | MATCH (177+6737+862 = 7776) |
| (a) `propagation_incomplete` (label-level unit propagation) | 0 | **0** | MATCH |
| (b) survivors by k = 1..6 | [177, 2576, 12762, 26928, 25200, 8640] | **[177, 2576, 12762, 26928, 25200, 8640]** | MATCH |
| (b) total / space | 76283 / 36415008 | **76283 / 36415008** | MATCH |
| (b) Fubini(6) slices | 1, 62, 540, 1560, 1800, 720 | **1, 62, 540, 1560, 1800, 720**, sum **4683** | MATCH |
| (c) resonance cells | 933120 | **933120** = 5!·6^5 | MATCH |
| (c) cells admitting a field | 1440 | **1440** | MATCH |
| (c) cells failing by an empty Rp or Rn on some arc | 919512 | **919512** | MATCH |
| (c) cells failing by the cyclic disjointness system alone | 12168 | **12168** | MATCH |
| (c) field-set measure | 1/648 | **1/648** exactly | MATCH |
| (d) sign-cell total | 3840 | **3840** = 5!·2^5 | MATCH (on the total) |
| (d) **sign cells meeting the SAT set** | **16** | **720** | **NOT REPRODUCED** |
| (d) base chambers total | 120 | **120** = 5! | MATCH |
| (d) **base chambers meeting the SAT set** | **16** | **120** | **NOT REPRODUCED** |
| (e) (0,30,90,150,240,300) has a field | yes | **yes** | MATCH |
| (e) (0,108.75,123.75,142.5,292.5,315) has none | none | **none** | MATCH |
| (e) the two lie in one sign cell | claimed | **ill-posed / false** | **NOT REPRODUCED** |

Partition check for (c): 1440 + 919512 + 12168 = **933120** exactly.
Two-implementation check: DFS vs reachable-set DP **0 mismatches** on all 7776 classes; minimal
palettes vs unrestricted masks **0 mismatches** on all 7776 classes. So the `|P_j| <= 2`
reduction is *verified*, not assumed, over the whole class space.

## 2. (d) in detail — both systems defined, both counts computed

* **Sign cell** (mod 180): write `alpha_0 = 0` and `alpha_i = 180 u_i`, `u_i = n_i + f_i` with
  `n_i in Z/2`, `f_i in [0,1)`. A sign cell is `(n_1..n_5 mod 2, ordering of f_1..f_5)`;
  total `2^5 * 5! = 3840`. Every sign cell contains exactly `3^5 = 243` resonance cells
  (mod 60), and `3840 * 243 = 933120`.
* **Base chamber** (mod 60): `(ordering of the fractional parts f_1..f_5)`, total `5! = 120`.
* Counted: **720** sign cells meet the SAT set, each containing **exactly 2** of its 243
  resonance cells (multiplicity histogram is `{2: 720}` — no cell has 1 or 3). **All 120**
  base chambers meet it; each of the 120 orderings has **exactly 12** field cells of its 7776.
* Consequence: the statements "16 of 3840" and "16 of 120" are both **false** under the R1-1
  definitions, and the "contained-in" readings are trivially false too (a sign cell would need
  243 field cells, a base chamber 7776; the true counts are 2 and 12). The reproducible
  statements are **720 of 3840** and **120 of 120**.
* What *is* 16-shaped in this data: nothing I could reproduce. 720 = 16·45 and 1440 = 16·90 are
  arithmetic coincidences unless someone names a symmetry of order 45 or 90; no such action
  appears.

## 3. (e) in detail

* `(0,30,90,150,240,300)`: two arcs of `R/60Z` (boundaries {0°,30°}). Classes at t = 15°, 45° are
  `(0,5,4,2,1)` and `(5,4,3,2,1)`, both SAT. Field exists. **But** its fractional parts mod 60 are
  `(0, 1/2, 1/2, 1/2, 0, 0)` — **not** pairwise distinct, so this vector is *on walls* of the
  mod-60 arrangement and lies in no open resonance cell, hence in no open sign cell.
* `(0,108.75,123.75,142.5,292.5,315)`: six arcs; classes `(5,4,4,1,1)` and `(4,4,4,1,1)` are
  UNSAT with **both sides non-empty**, i.e. refuted by the cyclic disjointness system alone;
  the other four arcs are SAT. No field. Fractional parts `(0, 13/16, 1/16, 3/8, 7/8, 1/4)` are
  pairwise distinct, so it *is* interior to a sign cell.
* Therefore "they lie in one sign cell" cannot be literally true: the first is a wall point of
  the mod-180 arrangement and the second is interior. The pair does illustrate the *correct*
  reading — the field property is constant on resonance (mod 60) cells, not on sign
  (mod 180) cells — which is exactly the correction m2's (4.3) records.

## 4. Where I expect members to go wrong (checked, not speculative)

1. **`1440` vs `177` is not a contradiction.** The all-phase test is a *six-class chain*: as `t`
   crosses `alpha_i + 30`, exactly the `i`-th coordinate of the class increments, so the chain is
   `tau + 1_{A_m}` for the ordered partition of crossing order — a `k = 6` staircase. So
   `1440 = 120 * 12`, `|chain-SAT classes| = 12` per ordering, while `|SAT classes| = 177`.
   Both hold. Any member deriving `|S| = 12` *and* `|S| = 177` from one set `S` has confused
   "SAT at a phase" with "field exists".
2. **Cross-lane consistency, not contradiction:** `1440 * 6 = 8640`, the `(1^6)` staircase
   stratum of `supervisor/solve-graphs/CENSUS-HANDOFF.md`, because the unfixed model counts the
   six rotations of `alpha_0` separately (`7776 * 720 = 5598720 = 6 * 933120`, and
   `8640 = 6 * 1440`). Hence `8640/5598720 = 1/648` and `1440/933120 = 1/648` are the same
   number in two normalisations. Members reporting "F2 and F4 are incompatible" hold the wrong
   premise.
3. **Palette-level propagation is weaker than label-level.** Label-level unit propagation refutes
   every UNSAT class (0 incomplete); palette-level (propagating forced *labels* between adjacent
   positions only when a whole palette domain forces them) leaves **72** classes unrefuted. So
   "every UNSAT class is refuted by unit propagation" is true for the label encoding and false
   for that palette encoding; the report must say which one it ran.

## 5. Runtime

| stage | seconds |
|---|---|
| (a) fixed phase: 7776 classes × (DFS + DP + propagation) | 0.6 |
| (a) unrestricted cross-check on all 7776 classes | included above |
| (b) staircase DP over the 64-subset lattice, vectorised | 0.5 |
| (c)+(d) all phases: 120 orderings × 7776 cells × 6 arcs | 87 |
| (d) confirmation pass (field cells, sign-cell multiplicities) | 95 |

Only (c)+(d) exceed 1 s; both run as a single local `python3` call with no arguments.

A SAT cell is never a colouring. Nothing here bounds `chi(R^2)`.

## 6. The all-phase figure and the staircase census are one computation (verified)

`checks/staircase_bridge.py` (`staircase_bridge.json`), same code base, exact integers:

| object | count |
|---|---|
| SAT classes `tau` | 177 |
| `tau -> -tau` preserves SAT (all 7776 classes) | **true** — so `+1_A` and `-1_A` conventions cannot diverge |
| `#(tau, ordering of all 6 coordinates)` with every prefix `tau + 1_A` SAT | **8640** |
| same with `tau - 1_A` | **8640** |
| graphs-lane `(1^6)` stratum (`supervisor/solve-graphs/CENSUS-HANDOFF.md`) | **8640** |
| ratio `8640 / 1440` | **exactly 6** |

So the `1440` of R1-1 (c) and the `8640` of the staircase census are the same set in two
normalisations, the difference being exactly the six rotations of `alpha_0`
(`5598720 = 6 * 933120`). Consequently `1/648 = 1440/933120 = 8640/5598720` is one number,
and no member may report (c) and (b) as mutually inconsistent. The `(1^6)` stratum figure is
now reproduced by an independent route (prefix DP in the subset lattice, my own code), not
merely quoted.

A SAT cell is never a colouring. Nothing here bounds `chi(R^2)`.
