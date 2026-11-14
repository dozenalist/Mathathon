# m7 / swarm smwfo9zkl / direction d7 — index

**Direction.** The four-cycle case of local finiteness of cyclic centres at `k = 6`
(`§6.3.1`–`§6.3.2` of the paper; Theorem 6.5).

**Outcome.** `§6.3` is a `k <= 5` argument. I locate its two exact `k`-thresholds, prove them with
complete arguments and exact enumerations, prove a `k`-general form of Lemma 6.4 whose `k = 6`
content is a sharp restriction on the palette map, show the remaining pointwise system at `k = 6`
is *satisfiable* (so no pointwise argument can decide the stratum), and exhibit an explicit proper
measurable 6-colouring with four-cycle centres (so the stratum is not vacuous). **This does not
prove or disprove local finiteness of `L` at `k = 6`, and it gives no new bound on `chi(R^2)`.**

---

## Read in this order

| file | what it is |
|---|---|
| `RESULT.md` | the results, with complete proofs: `§2` Theorem 1 (state-reduction threshold), `§3` Theorem 2 / 2' (the `K_3` mechanism and 2-valued palette maps), `§4` Theorem 3 (the outsider deficit — no palette hypothesis repairs `§6.3.2`), `§5` Theorem 4 (the pointwise system is satisfiable) and Theorem 4' (so is the distance-one two-centre exclusion, on a Moser spindle of four-cycle centres), `§6` Theorem 5 (an explicit 6-colouring of a strip with four-cycle centres), `§7` exactly what a `k = 6` proof must add |
| `AUDIT.md` | the line-by-line dependence of `§6.3.1`–`§6.3.2` on `k = 5`: nine rows, each with the paper's page, the inequality it consumes, and its status at `k = 6`; plus the two-extraction check of every displayed formula used |
| `verify.py` | every exact computation behind the above (sections A–H); writes `verify.out` |
| `verify_indep.py` | an independently coded second implementation (bitmask enumeration, direct construction of the escape list, `sympy` maximisation); writes `verify_indep.out` and ends `ALL INDEPENDENT CHECKS PASSED` |
| `verify.out`, `verify_indep.out` | the logs |
| `paper/paper.txt` | `pdftotext -layout` of the paper |
| `work/pages/` | per-page `-layout` and `-raw` extractions plus 150 dpi PNGs of pp. 27, 29, 30, 33–40, i.e. every page carrying an input used |

## Commands (from the repository root)

```
python3 .ultramath/smwfo9zkl/m7/verify.py        | tail -40     # ~4 s
python3 .ultramath/smwfo9zkl/m7/verify_indep.py  | tail -3      # ~3 s
grep -c OK .ultramath/smwfo9zkl/m7/verify_indep.out             # 82, no FAIL
```

## The one-paragraph version of the mathematics

At a centre `x` whose transition graph contains the four-cycle `0-1-2-3`, put `U = {0,2}`,
`V = {1,3}` and let `O = I \ {0,1,2,3}` be the outsiders. `(6.2)` and the palette bound
`1 <= |P| <= k-3` say the palette is admissible: no singleton of a cycle label, no cycle edge, size
`<= k-3`. The paper's `§6.3.1` needs the palette to determine a three-valued state, which fails as
soon as a palette can carry two state groups, i.e. as soon as `|{X} ∪ U| = 3 <= k-3` — that is,
from `k = 6` on (at `k = 6` exactly two of the 33 palettes do: `{0,2,X}`, `{1,3,X}`). The paper's
`§6.3.2` needs the label set outside the two state groups to be a *single* label; Lemma 5.2(2)
only gives `density one of I \ (G_1 ∪ G_2)`, and for the two diagonal groups that set has size
`k-4`, i.e. `1` only at `k = 5`. Both failures are independent, and the second is a label-count
failure that survives the strongest palette hypothesis, so no statement about palettes can repair
`§6.3`. The one part of Lemma 6.4 that does survive is the `K_3` mechanism of `RESULT.md` `§3`: two
disjoint palette groups whose total size is `>= k-2` cannot straddle the two angles
`t+2j kappa`, `t+pi+gamma+2j kappa`, because the three sum points form a unit equilateral triangle
and a proper colouring of a triangle needs three labels. At `k = 6` this excludes every 2-valued
palette map at a six-cycle centre, and all but 13 of the 110 disjoint palette pairs at a four-cycle
centre — the 13 being exactly "an outsider singleton plus a set of size `<= 2`". That residue is
genuinely consistent: the model `P = {4}` on the even sextants and `P = {0,2}` on the odd ones
satisfies the palette bound, `(6.2)`, `(5.7)`, `(5.2)` and the mechanism. Better, the same style of
model survives the two-centre constraint `(5.3)` at distance exactly one *on the seven vertices of
the Moser spindle*, a `4`-chromatic unit-distance graph (`RESULT.md` Theorem 4'). So the palette
combinatorics of `§6.3.1` and the distance-one centre coupling are both *powerless* at `k = 6`, and
any proof of the four-cycle case must use the multi-scale content of `(5.3)` and the accumulation
device — which is the one constraint this analysis leaves untested.
