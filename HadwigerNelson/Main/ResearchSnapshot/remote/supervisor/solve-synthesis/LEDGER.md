# Adversarial ledger, solve track (ranked)

Ranking key: value = how much a proof of the item would move `chi(R^2)`; status = what I could
check in this block. Grades: [A] machine-checked here, [P] paper-level argument, [C] computation
by me, [X] record only.

## R1. VIABLE, does not reach a numeral: (W) implies the §7 interface at k = 6
`(W)`: exists `y`, `R > 1`, `|L cap B(y,R)| < infinity`, `L = {x : Gamma_x contains a cycle}`.
Then Prop 7.1 holds at `k = 6` (Theorem A, `sprint/k6/REPORT.md` §2; four independent audits;
combinatorial core `card_le_two_of_isClique_of_acyclic` machine-checked under pinned Lean).
Status [P]. Its hypotheses are the weakest that the printed argument supports (`sprint/k6/WEAKEST.md`,
`supervisor/solve-geometry/STATUS.json` corrects its constants: `2 < s < sqrt2 r`, and `(LF) => (ISO)`
is false).
**Why it is ranked first and still moves nothing:** it is the only implication in the record that
converts a hypothesis about `L` into the exclusion-continua cycle. It produces no bound on
`chi(R^2)` by itself.

## R2. FAILED at the palette level: extending §8 to k = 6
The step after R1 must exclude a cycle of compact connected common exclusion continua at `k = 6`.
`m6` decides the strip layer exactly: `STRIP(k,ell)` is UNSAT exactly at `(4,3), (4,4), (5,5)` and
SAT for every `k >= 6`, with explicit witnesses at `k = 6` for every `ell` (report §4b). So the
printed §8 cases fail at `k = 6` for attributable reasons and the strip layer is powerless.
Combined with Theorem C (palette axioms + (5.7) + (5.3) admit an `ell`-cycle locus equal to the
whole plane, every `ell`) and T3 (palette axioms + any trace function is satisfiable iff
`chi <= 6`), the conclusion is: **no argument that uses only palette data can close §8 at k = 6.**
This is why R1 does not deliver `chi >= 7`. Status [P]+[C] (record; I re-read the paper's
Lemma 7.4/7.6 multiplicity claim and it is k-uniform, see R5).
Surviving sub-target: a §8-at-6 exclusion that uses trace-consistency, i.e. the colouring itself —
which by T3 is the original problem. No route through this gate is currently live.

## R3. VIABLE, the sharpest attack surface on (W): the singleton reduction
`m4` Theorem 3: in the class `S_1` (maximal palettes are singletons a.e. — contains every
cell-constant colouring with piecewise `C^1` boundaries, in particular the paper's `c_0`),
at `k = 6` there is no 5-cycle and no 6-cycle in any `Gamma_x`, the 4-cycle locus is locally
finite, so **`L` locally finite iff the 3-cycle locus is**. Status [X] (recorded with 33 checks
PASS); I verified only its first input (R4). It is the only statement in the record that reduces
`(W)` to a single geometric mechanism. Its consequence is sharp because `m3`'s proper `k >= 7`
colouring accumulates exactly at 3-cycle centres, and `m3` Lemma 1 shows `(W)` holds in the tame
class at every `k`, so a `k = 6` countermodel to `(W)` must be non-tame.

## R4. VIABLE, repaired this block: Lemma D (self-avoidance)
At a density-one point `x` of its own colour class, `i = c(x)` is not in `P_x(e)` for a.e. `e`.
The proof recorded in `sprint/k6/REPORT.md` §5 is **invalid**: it applies Lemma 5.2(2) on the
circle of radius one about `x + e_0`, which meets the unit circle about `x` in exactly two points,
and the one that is `x` is the excluded antiparallel direction [A]. A valid proof exists and uses
(5.2) with the sector Jacobian: a positive-measure angular set `D` of directions with `i in P_x(e)`
kills a sector of measure fraction `|iD u -iD|/(2 pi) >= |D|/(2 pi)` of every `B(x,h)`, so the
`A_i`-density at `x` is at most `1 - |D|/(2 pi) < 1` [P]+[A]. Full statement, proof and the
machine-checked geometry: `notes/LEMMA-D-REPAIRED.md`, `checks/sector_lemma.py` (rc 0).
Consequence: the 510-word orbit count, `m4`'s reduction and the "self-avoidance is the frontier"
claim are supported, but their citation must change. This is the one adversarial attack this
block that **failed to falsify**, and the rescue is new.

## R5. Adjudicated, no error: the cover obstruction's multiplicity constant
`results/continuation/SUMMARY.md` (run `smwfhd5sl`, m3) says "multiplicity-3 covers of
arbitrarily fine mesh exist, so Lemma 7.5 never applies at `k >= 6`". That inference is a
non-sequitur for the paper's argument. Lemma 7.5 (paper p. 46) is stated for multiplicity at most
**two** and mesh at most two, and Lemma 7.6's component cover has multiplicity at most two *for
every `k`*, because a point of the geometric realization of a graph has at most two positive
barycentric coordinates (paper p. 47). So the multiplicity-2 obstruction is `k`-uniform, the
`1 + o(1)` mesh and the `R > 1` threshold in (W) survive, and the continuation note's claim must
not be quoted against §7. Status [P] (I read both proofs).

## R6. FAILED (already paid for in the record, do not restart)
* Any finite two-centre palette CSP as a route to `chi >= 7`: satisfiable at `k = 6` iff the
  pullback conflict graph is 6-colourable, i.e. iff a 7-chromatic finite unit-distance graph
  exists (`m10`). This is the classical open problem, not a relaxation.
* Any finite palette system at `k = 6` forcing a ternary palette: impossible (`m14` neutrality).
* `(W)` from a size/content/porosity/density bound on `L`: impossible (`m5`: punctured-annulus
  failure of Lemma 7.8, plus a perfect 1-dense porous zero-content closed set).
* Recolouring `m3`'s `k >= 7` gadget down to `k = 6`: circular (a `k = 6` gadget needs a
  6-colouring outside).

## The alternative route that survives this block's falsification attempt
Since R4's conclusion holds, R3 stands, and the alternative is to attack **R3's residual case
directly**: "in `S_1` at `k = 6`, no 3-cycle centre is an accumulation point of 3-cycle centres",
using only proved inputs — (5.2), (5.3) via Remark 5.3 (`P_{x+a}(f) cap P_x(f) = empty` at every
unit `a`), (5.7), `m2`'s two-ternary bound `|P_x(e)|+|P_y(e)| <= 5` at unit `x,y`, Lemma 6.2's
avoiding trace, Lemma 5.5's binary separation. This route touches no palette-level theorem, so
R2's failure does not harm it, and it is the only formulation of `(W)` that is both sharp
(`m3`) and reachable without a colouring. First falsifiable sub-lemma for the next block:
at a 3-cycle centre with `|P_x(e)| = 3` on a positive-measure angular set, the unit neighbours
`y = x + a` must satisfy `|P_y(e)| <= 2` on a positive-measure set of `e`; decide by exhaustive
finite check over the 6-label palette systems whether that is consistent with (5.7) and the
Lemma 6.2 avoiding trace at three consecutive centres.
