# Nonuniform radial shell allowance: design, and why the negative result is not an artefact

Status: **design + argument**. Nothing here is a computed certificate. It exists so that
`K15-C-SHELLGAIN-003` (uniform allowance, gain exactly 0 at seven degrees) is not over-quoted,
and so that the one variant that *could* still pay is identified precisely.

## 1. The nonuniform chain

Let `f` be admissible with `f̂ ≥ 0`. Suppose we have a **count function** `m(r)`: for every
centre `p` in a packing of minimum separation 2,

$$\#\{q \in X : q \ne p,\ |q-p| \le r\} \;\le\; m(r).$$

Take a partition `2 = r_0 < r_1 < … < r_k = ρ` and allowances `η_1, …, η_k ≥ 0` with
`f ≤ η_j` on the annulus `[r_{j-1}, r_j]` and `f ≤ 0` beyond `ρ`. Charging each neighbour by the
allowance of the annulus it lies in bounds the off-diagonal mass by `Σ_j c_j η_j` with

$$c_j \;=\; m(r_j) - m(r_{j-1})$$

the number of neighbours whose distance falls in the `j`-th annulus. The same Poisson chain as in
`shell_bench.py` then gives

$$\Delta \;\le\; \frac{4\pi}{3}\,\frac{f(0) + \sum_j c_j\eta_j}{\widehat f(0)} . \tag{N}$$

The uniform case is `k = 1`, `c_1 = n`, `ρ` fixed. **(N) is the general object**; the uniform
benchmark is its crudest instance.

## 2. What is provable about `m`

* **Kissing number:** `m(2) ≤ 12` (Schütte–van der Waerden; equality for FCC). This is a theorem.
* **Volume bound:** `m(r) ≤ ⌊(r+1)³⌋ − 1` for all `r`, since unit balls about the neighbours are
  disjoint inside `B(p, r+1)`. At `r = 2.05` this gives `m ≤ 26` from `3.05³ = 28.4`… more
  precisely `⌊3.05³⌋ − 1 = 27` as used in `K15-C013a`. **This is the unconditional count behind
  the `n = 27, ρ = 2.05` rows.**
* **Tammes-13 / conditional:** `m(r) ≤ 12` for `r < ρ` with `ρ = 2.09` reduces to a Tammes-13
  enclosure (`K15-C019`) and is **not** proved here.

## 3. The argument that nonuniformity cannot rescue the uniform failure

### 3.0 What this section assumes (added after review 0353-C)

The argument below is an argument, not a proof, and the review asked for its assumptions to be
written down rather than carried implicitly. They are four:

1. **A count function exists.** `m(r) < ∞` for every `r`. Proved only at `r = 2` (kissing number
   `≤ 12`) and by the volume bound `m(r) ≤ ⌊(r+1)³⌋ − 1`. Everywhere else `m` is conjectural
   (Tammes) or simply not available, so (N) can be instantiated only at radii where one of those
   two holds.
2. **A local scale function `s(r)` exists.** The configurational strengthening this section says
   would be needed has the shape: *at most `c` of the twelve contacts can be at distance `> r`
   simultaneously with the remaining geometry*, i.e. a function `s(r) ∈ (0,1]` attached to each
   centre such that the cell of that centre, shrunk by `s(r)`, is covered by the balls of the
   neighbours at distance `≤ r`. **`s(r)` existing is an assumption about the packing class, not a
   theorem**: two packings with the same count function `m` can have different `s(r)`, and nothing
   in this directory computes it. Everything in §3 is conditional on it.
3. **FCC is extremal for the count.** "`m = 12` is attained, so no smaller count is available"
   treats FCC as the object at which the bound must be sharp. That is a statement about which
   packing the bound must survive, not a proof that FCC maximises anything.
4. **(N) is a relaxation.** `Σ_j c_j η_j` charges each neighbour by the allowance of its annulus,
   so it bounds the off-diagonal mass from above. (N) is valid but never tight, and a failure of
   (N) to pay says nothing about a tighter charging scheme.

### 3.1 Four failure modes of the cut condition (C044)

The same review asked for the ways the cut condition can fail to carry information, each with an
instance from this record. These are not hypothetical: every one of them has occurred here.

| # | failure mode | what it looks like | instance |
| --- | --- | --- | --- |
| 1 | **Vacuous at the extremal packing** | `b(v) = 0` at every vertex, so the condition holds at every `Φ` and discriminates nothing | FCC and HCP: `b = 0` exactly, `cut_flow.py` rows 0–1 |
| 2 | **Test set not finite** | testing on a period or a blob, which C044 does not quantify over — a period is not a finite `U` | the withdrawn full-period derivation (`REVIEW_0308.md` §2); the valid replacement takes `U = Λ ∩ B`, which *is* finite (`K15-C-CUTIMPLIES-003`) |
| 3 | **Capacity is per-packing, not universal** | a `Φ` that works for one fixture is not a `Φ` that works for all; a singleton cut yields only a per-fixture lower bound | `0.008880268414739` for the 13-cluster — `PROVED` for that fixture, and *not* a universal capacity |
| 4 | **Patch is not packing** | verifying every finite `U` *inside the patch* does not verify the finite `U` that straddle copies; `PATCH_FEASIBLE` is evidence about that patch only | `flow_status = PATCH_FEASIBLE` in `cut_flow.py`; and by `K15-C-CUTIMPLIES-003` the all-finite-`U` condition is strong enough to force `ρ ≤ 1/√32`, so a patch check should not be expected to give it |

A fifth thing that is *not* a failure mode but is often mistaken for one: a violated cut at a
singleton is a genuine obstruction for the infinite packing (the test set is finite), so a negative
result of that kind is unconditional. What is conditional is the *sufficiency* direction.

The cheapest possible nonuniform allowance puts all its mass where `m` is smallest, i.e. just
above `r = 2`, where `m = 12` is the kissing bound. Its cost is therefore

$$\sum_j c_j\eta_j \;\ge\; 12\,\eta_{\text{near}} \quad\text{whenever the allowance is used near contact.}$$

Concentrating the allowance near contact with cost `12` is **exactly the `n = 12` uniform case**
already measured: at every degree 9–21 the LP sets `η = 0` and the gain is exactly `0`
(`K15-C-SHELLGAIN-003`). So:

> Within the family (N), a nonuniform allowance can beat the `n = 12` uniform case only by using
> an allowance at radii where `m(r) < 12`.

And at the most favourable radius — just above contact — `m = 12` **is attained** by FCC: all
twelve contacts sit exactly at distance 2. So there is no radius at which a smaller count is
both available and compatible with an extremal configuration. Any count function with
`m(r) < 12` for `r > 2` would have to be *false* for FCC, which has 12 neighbours at distance
exactly 2 and (for the second shell) 6 more at `2√2 ≈ 2.83`. Hence:

**Conclusion (argument, not proof).** The uniform negative result is not an artefact of taking a
single annulus: the nonuniform family (N) reduces to the already-measured `n = 12` case at the
only place where the count is minimal, and every radius beyond `2` has larger count on the
extremal FCC configuration. To get strength from a shell allowance one would need a **local**
statement — "at most `c` of the twelve contacts can be at distance `> r` *simultaneously with*
the remaining geometry" — which is a constraint on configurations, not a count. That is a
different mechanism and is not excluded by anything here.

## 4. What this changes in the record

* `K15-C-SHELLGAIN-003` says: *uniform* allowance at fixed degree and `n ∈ {12, 27}` does not pay.
  It does **not** say no shell-type strengthening can ever pay.
* The precise gap: a configurational (local) constraint, not a count. Candidates would be
  statements like "if `k` neighbours are at distance `> r`, the remaining ones are at distance
  `< r'` with `r' < r`", which is exactly the kind of statement Experimental's local-mass route
  is meant to supply.
* The chain (N) is implemented in no file here; only the uniform case is (`shell_bench.py`,
  `shell_propose.py`). Anyone implementing (N) should note that it needs `m` at every breakpoint,
  and that the only *proved* values available today are `m(2) ≤ 12` and the volume bound.
