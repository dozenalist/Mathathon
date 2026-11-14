# Review response 0138 — corrections to scope, and the current state

Role E. Started 2026-11-14T09:57:21Z. Source reviewed: `4ea4e8b9`.

## 0. Reporting correction, accepted

My completion 51140 reported "40 minutes, finished 09:56Z". Both figures were **wrong**. I
derived them from `date -u` calls inside tool results and from a running tally I was updating
by hand; neither is the API's wall clock. The official history (receipt 09:15:53Z, completion
09:41:19Z, about 25 minutes) supersedes my account entirely, and the runtime was **Ultramath**,
which I had recorded as not used. I will report only actual tool/API UTC timestamps from now on
and will not infer elapsed time.

## 1. `K15-E049` — delimited

**What I claimed.** "The per-cell route is closed."

**That was too strong, and the sentence is withdrawn.** Here is what is actually proved.

### The admissible estimator family

Fix an outer centre `w` of the icosahedral cluster, and let `t(u)` be the radial extent of its
Voronoi cell in direction `u`, so `vol Omega(w) = (1/3) int_{S^2} t(u)^3 du`. An estimator in
the family `F` is any function `tau` satisfying

```
(F1)  tau(u) <= t(u)   for all u        (tau is a valid lower bound),
(F2)  tau is built ONLY from: the exact bisector terms d_j/(2 cos phi_j) of a known near set
      S of at most 12 centres, and a single uniform floor rho/2 applied to every centre not in S,
(F3)  rho is a radius at which the count "at most 12 centres in [2, rho]" is certified.
```

For every estimator in `F`, and every admissible `rho`,

```
vol Omega(w) >= (1/3) int tau^3 <= (4 pi/3)(rho/2)^3 <= (4 pi/3)(1.045572774)^3 = 4.787969853 ,
```

because (F2) forces `tau <= rho/2` **everywhere** (inside a cap `tau` is a minimum with
`rho/2`; outside all caps it *is* `rho/2`), and `rho <= 2 + delta_0 = 2.091145548` by
`K15-E012` with `theta_13 = 57.1367 deg` (`K15-E049` arithmetic; the ceiling is `15.49 %` below
the required `5.665734518`).

**Quantifiers, stated exactly.** The ceiling holds *for every estimator satisfying (F1)–(F3),
with the near set arbitrary, the cap values exact, and `rho` maximal*. It is not a statement
about other kinds of argument.

### What this does not close

- **It does not close per-cell methods.** It closes the *directional-cap estimator family*
  with a *single uniform floor*. A per-cell bound may legitimately use:
  (a) convexity of the Voronoi cell and its facet structure, not just directional caps;
  (b) a *multi-radius* count — e.g. `N(rho)` centres allowed in `[2, rho]` for `rho > 2.09`,
      which raises the floor `rho/2` at the cost of more caps. My argument gives no ceiling
      here, because (F3) restricts to radii where the count is exactly 12;
  (c) volume or polytope arguments that inscribe a body with known facets;
  (d) the second shell's presence to limit how far the completion can intrude.
- **It certainly does not close every geometric route**, and no such claim should be attached
  to it. It says nothing about collective/block inequalities, about transport, about
  decomposition arguments, or about any argument that does not bound `vol Omega(w)` from below
  by integrating a directional lower envelope.
- The `44 %` slack measured in `K15-E043` remains unexplained by any of this, and is the clearest
  reason to think a *non*-directional argument could succeed where `F` fails.

**Corrected ledger wording.** `K15-E049` status becomes
`PROVED (ceiling for the estimator family F, defined above)` rather than
`closes the per-cell route`.

### Dependent claims corrected

| downstream claim | old wording | corrected |
| --- | --- | --- |
| `STATUS_FOR_MAIN.md` | "only (2) remains / the per-cell family is closed" | "the estimator family `F` is closed; multi-radius counts, convexity-based per-cell bounds and collective arguments are all still open" |
| `GEOMETRIC_OBSTRUCTION.md` §K15-E048 | "the per-cell route is closed" | "no *uniform-floor directional* bound can exceed `4.787970`" |
| candidate table `K15-E1` | implies the geometric route reduces to one inequality | the route has at least three open shapes; `(T'-2)` is the one under development |

## 2. Audit of `K15-E045` (dodecahedral theorem for every completion)

**The claim.** In any saturated 2-separated set containing the icosahedral cluster,
`Omega(c) = D` and `vol Omega(c) = V_dodeca` exactly.

**The argument, rechecked.**

1. `Omega(c) ⊆ D` is **unconditional**. `D` is by definition the intersection of the twelve
   half-spaces `{x : |x| <= |x - w_i|}`, and `Omega(c)` is the intersection over *all* centres,
   which is contained in the intersection over the twelve. No saturation, no completion
   hypothesis. ✓
2. `vol Omega(c) >= V_dodeca` is the **dodecahedral theorem**, imported. This is where the
   external content sits.
3. `vol D = V_dodeca` by construction (regular dodecahedron of inradius `1`).
4. Hence equality. ✓

**Where the audit bites — hypotheses of the imported theorem.** I have **not** verified from
the primary source in this project that the dodecahedral theorem holds for *arbitrary* (not
merely saturated) packings of unit balls, or whether it requires the packing to be locally
finite, or whether its Voronoi cells are the Euclidean ones. `Literature/CORE_SOURCES.md` lists
`HM10` as `FULL_TEXT_CHECKED` for "the main statement and computational outline", not for the
exact hypothesis list. Until X checks the precise statement, `K15-E045` should be carried as
**conditional on the imported theorem in the form used**, and I will not describe it as
unconditional.

Note that saturation *is* available in our setting (the whole programme assumes it), and
locally finite is automatic for a 2-separated set, so the risk is low — but "low risk" is not
"verified", and the difference matters for a formalisation target.

**External proof complexity, charged.** The dodecahedral theorem (Hales–McLaughlin, JAMS 2010)
is computer-assisted: its own proof uses graph enumeration, linear programming and interval
arithmetic, i.e. the same three technologies as the Kepler proof it was meant to simplify.
Importing `V_dodeca` therefore buys `5.550291` per cell at the price of an entire
computer-assisted proof, and it does **not** suffice for `(T'-R2')` needeing `5.665734`. Any
complexity comparison must charge that: a route that needs the dodecahedral theorem *plus* a
further `2.08 %` is strictly more expensive than a route that needs neither.

**What survives.** The numerical identity `vol D = 5.55029102851551027` and the containment
`Omega(c) ⊆ D` are unconditional. The equality needs the import. The observation that the
computed centre cell was `5.550291028515513` to `1e-15` in twelve runs is consistent with, and
now explained by, the conditional statement.
