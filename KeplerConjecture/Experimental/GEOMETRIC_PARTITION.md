# Geometric route: a block rule and its precise failure

Role E. `K15-E030`. Status: **rule SPECIFIED; target inequality UNPROVED**; the failure
is reported precisely, as the assignment permits, rather than restating `K15-E001`.

## The rule (explicit, constructive)

Given a saturated packing `Lambda` with separation `>= 2`, build a partition `Pi` of
`Lambda` by this deterministic procedure, with `R1 = 209/100`:

1. Call `v` **defective** if `vol Omega(v) < sqrt(32)`; otherwise **sound**.
2. Process defective centres in order of increasing `vol Omega(v)` (ties by a fixed
   lexicographic order on coordinates). For a defective `v` not yet assigned, form the
   block
   `C(v) = {v} union { w : 2 <= |w - v| <= R1 }`.
   By `K15-E014` this block has at most `1 + 12 = 13` members, so `diam C(v) <= 2 R1 = 4.18`
   and `|C(v)| <= 13`.
3. Assign every member of `C(v)` to that block and remove them from the pool.
4. Any remaining (sound) centre becomes a singleton block.

This is well defined: each step assigns at least `v`, so the recursion terminates, and the
result is a partition. It has `diam <= 4.18` and `|K| <= 13` for every block. The boundary
loss in `K15-E001` Step 2 is then controlled with `D = 4.18`, `Vmax = 13`:

```
|T| <= 3(D+2)(r+D+2)^2 = 3(6.18)(r+6.18)^2      (corrected shell bound)
```

## The one target inequality

The rule succeeds if and only if, for **every** saturated packing and **every** defective
`v`,

```
(T)   sum_{w in C(v)} vol Omega(w)  >=  sqrt(32) * |C(v)| .
```

Sound singletons satisfy (T) by definition. So (T) is the entire geometric content, and
it is exactly `K15-E004` in its corrected *existence* form: the rule exhibits the
partition, and (T) is the only assertion needing proof.

## Worked configuration 1 — FCC: passes, and is tight

At an FCC centre every Voronoi cell is a rhombic dodecahedron of volume exactly `sqrt(32)`,
and the 12 neighbours lie at distance exactly `2`. So `C(v)` has 13 members and
`sum = 13 sqrt(32)`, giving **equality** in (T). The rule therefore cannot be sharpened,
and any corrected constant must reproduce `sqrt(32)` exactly here. No defective centre
exists in FCC, so the rule makes all singletons; (T) holds trivially.

## Worked configuration 2 — the icosahedral defect: the critical test, unresolved

The 12 tangent neighbours of a central ball at icosahedron vertices (circumradius 2,
mutual distance `2.1029`) lie within `R1 = 2.09` only for the 12 at distance exactly 2, so
`C(v)` is the 13-cluster. The centre has

```
vol Omega(v) = 5.5502910285155,     deficit = sqrt(32) - 5.5502910 = 0.1065632.
```

So (T) for this block requires the twelve outer cells to satisfy

```
sum_{i=1..12} vol Omega(w_i)  >=  13 sqrt(32) - 5.5502910 = 67.9888141,
       i.e.  mean outer volume >= 5.6657345.
```

**This is where I stop, and why.** I cannot prove this inequality, and I will not present
an unproved inequality as progress. The obstruction is specific:

- Computed cell volumes in any finite completion are **upper** bounds (`K15-E003`), so the
  values I obtained (`mean 8.96` sparse, `13.51` denser) are uninformative; they do not
  bound `5.6657` from below.
- The available rigorous *lower* bounds are far too weak. Separation `>= 2` gives only
  `vol Omega(w) >= 4 pi/3 = 4.18879`, short of `5.6657` by `1.477`.
- Closing the gap needs a lower bound on Voronoi volume from finitely many neighbour
  distances, valid over all completions — a Rogers-simplex or Fejes Toth style estimate
  for a cell with 12 neighbours at distance `2` and a further shell at `>= 2.828`.

## Other configurations a rule must survive

- **HCP**: 12 neighbours at `2`, next shell `2.8284`, cell volume `sqrt(32)`; same verdict
  as FCC, equality in (T).
- **Barlow stackings**: cell volume `sqrt(32)` throughout, so (T) is again equality for
  sound centres. Whether a defective centre can occur in a Barlow stacking is open and is
  `K15-E013`.
- **Adjacent pair**: `C(v)` could reduce to `{v}` if the neighbour is itself already
  assigned, in which case (T) demands `vol Omega(v) >= sqrt(32)` for a *defective* `v` — a
  contradiction. **This is a real defect in the rule**: step 2 can be pre-empted by the
  ordering, because a defective `v` whose neighbourhood was consumed by an earlier block
  becomes a singleton. Fixing it requires a matching or priority argument (a defective `v`
  must never be absorbed into a block that does not repair it), and I have not constructed
  one. Recorded as `K15-E031`, status OPEN, and it is the first thing to repair.

## K15-E031 — precise failure of rule R1 (replaces the vague defect note)

The rule creates blocks by consuming neighbours, and **(T) is not preserved under
truncation**. Precisely: let `v` be defective with its 12 neighbours at distance exactly
`2` (the icosahedral star). If earlier blocks have absorbed `k` of those neighbours, the
block containing `v` has `1 + (12 - k)` members while the full deficit of `v` must still be
paid.

- `k = 12`: the block is the **singleton** `{v}`, so (T) reads
  `5.5502910285 >= 5.6568542495`, which is **false**. Rule R1 can therefore emit a block
  that provably violates its own target inequality.
- `k = 11`: the block is `{v, w}` and (T) demands
  `vol Omega(w) >= 2 sqrt(32) - 5.5502910285 = 5.7634174705`, just above `sqrt(32)`;
  not impossible, but nothing available proves it.

Whether a saturated packing realises `k = 12` is not settled here, so this is a
**rule-internal failure**: the correctness of R1 cannot be established block-locally, and
its target inequality is falsifiable at the level of arithmetic. R1 is withdrawn.

## Revised rule R2 — one checkable inequality

Define the **defective graph** `G_def` on `Lambda`: vertices are the defective centres
(`vol Omega(v) < sqrt(32)`); an edge joins `u != v` when `|u - v| <= 209/100`. Let the
blocks be

```
C_1, ..., C_m   = the connected components of G_def,
Block(C_i)      = C_i  union  N(C_i),      N(C) = { w : 2 <= |w - v| <= 2.09, v in C },
sound centres   = singleton blocks.
```

This is a partition by construction (components are disjoint, and every sound centre not in
any `N(C_i)` is a singleton). Because `C_i` is a *full component*, every centre in
`N(C_i) \ C_i` is **sound**, so each contributes a nonnegative surplus.

Define, for a component `C`,

```
D(C) = sum_{v in C} ( sqrt(32) - vol Omega(v) )        (the deficit; > 0 on defective v)
S(C) = sum_{w in N(C)\C} ( vol Omega(w) - sqrt(32) )   (the surplus; >= 0 by soundness)
```

Then (T) on `Block(C)` is **exactly equivalent** to

```
(T')      S(C)  >=  D(C)          for every component C of G_def .
```

That is the single checkable inequality. It is the classical compensation statement,
localised to the defective components, and it is not a restatement of `K15-E001`.

**Boundedness.** `diam Block(C) <= diam(C) + 2 (2.09)`, so the boundary loss in
`K15-E001` Step 2 is controlled as soon as `diam(C) <= D_0` for some explicit `D_0`. This
gives a second, separate obligation:

```
(T'')     diam(C) <= D_0      for every component C of G_def .
```

## Worked configurations under R2

- **FCC, HCP**: every centre is sound, `G_def` is empty, all blocks are singletons, both
  (T') and (T'') hold vacuously and (T) holds with equality `sqrt(32)`. ✔
- **Icosahedral defect**: if the dodecahedral centre is the only defective centre nearby,
  `C = {v}` is a singleton component and `Block(C)` is the full 13-cluster. Then (T')
  reads `S(C) >= 0.1065632` with 12 surplus terms available. This is now a single, sharply
  stated inequality rather than a family of cases. **Still unproved.**
- **Two adjacent defective centres**: `C = {u, v}` with `|u - v| <= 2.09`. Then (T') must
  be checked on the union of two large stars. This is a case the old rule could not even
  state.

## Honest verdict after the repair

R1 is withdrawn with a precise arithmetic failure. R2 is well defined, produces a genuine
partition, is correct on FCC and HCP with equality, and reduces the entire geometric route
to two checkable statements (T') and (T''). **Neither is proved**, and (T') on the
icosahedral component is the crux. I make no claim that this route is simpler than
Hales's; its value is that it isolates one inequality about a specific configuration
instead of an enumeration of standard regions.

## Status of (T') on the icosahedral component, quantified

The single decisive inequality is `S(C) >= D(C)` for `C = {v}` the dodecahedral centre.
Writing it out with exact constants:

```
D(C) = sqrt(32) - 5.5502910285155 = 0.1065632209769
```

so the twelve outer cells must satisfy

```
sum_{i=1..12} vol Omega(w_i)  >=  13 sqrt(32) - 5.5502910285155 = 67.9888142149,
mean                           >=  5.66573451791 .
```

Three consequences, all exact:

1. **The requirement exceeds an fcc cell.** `sqrt(32) = 5.65685424949`, so each outer cell
   must average `0.008880268415` above an fcc cell, i.e. `0.157 %` above. The inequality is
   therefore not satisfied by "typical" cells: it demands genuine expansion of every
   neighbour of the defect on average. This is the sharpest way to state what the
   dodecahedral defect costs.

2. **Inscribed balls do not come close.** Separation `>= 2` gives only
   `vol Omega(w) >= 4pi/3 = 4.188790205`, hence `13 * 4pi/3 = 54.45427266` against the
   required `73.53910524`, a shortfall of `19.08483258`. To reach the required mean from an
   inscribed ball alone the ball would need radius `1.105917008`, i.e. nearest-neighbour
   distance `2.211834`, whereas the true nearest-neighbour distance at the outer centres is
   exactly `2`. The inscribed-ball bound is therefore useless here and no amount of
   bookkeeping around it will close the gap.

3. **What a proof must therefore use.** A cell-volume lower bound that improves on the
   inscribed ball by exploiting *how few* neighbours a centre has: the outer centres have
   `6` neighbours within `2.1029` (one at `2`, five at `2.102851...`), against `12` in fcc.
   The estimate "cell volume grows as the neighbour count falls" is precisely the
   Rogers-simplex / Fejes Toth territory that Hales's Chapters 8 and 11-14 occupy.

**Honest status.** (T') on this component is open, and I have not proved it. What this
section establishes is that it is *not* accessible to the elementary lower bounds
available, that it is a genuine expansion statement (`+0.157 %` over fcc), and that its
proof must be a neighbour-count-versus-volume estimate. That is a real narrowing: it rules
out the inscribed-ball family, which is the obvious first attempt, with exact arithmetic.

### A route I did not complete, recorded so it is not lost

For a centre `w` and direction `u`, the cell extends to

```
t(u) = min over neighbours z with <z-w,u> > 0 of  |z-w|^2 / (2 <z-w,u>) ,
```

and `vol Omega(w) = (1/3) int_{S^2} t(u)^3 du`. A lower bound on `t` from the neighbour
data would give (T') directly. For the icosahedral outer centres the six neighbours leave a
large solid angle free in the outward direction, so `t` is large there; the obstruction is
that the free directions are closed not by the six known neighbours but by the unknown
completion, and only the `12`-count of `K15-E014` constrains the completion. Combining
`K15-E014` with the above integral is the concrete next step, and it is where I would
continue.

## K15-E032 — R2's disjointness threshold was wrong: it must be 2*2.09 = 4.18

Following the "check block disjointness/coverage" instruction uncovered a genuine defect in
R2 as first stated. R2 defined components of `G_def` using adjacency at distance
`<= 2.09`, and set `Block(C) = C union N(C)` with `N` the `2.09`-neighbourhood. **Those
blocks need not be disjoint.**

Counterexample to disjointness. Let `u`, `v` be defective with `2.09 < |u - v| <= 4.18`.
Then `u` and `v` lie in different components (they are not adjacent at threshold `2.09`),
yet a centre `s` placed at the midpoint-like position with `|s-u| <= 2.09` and
`|s-v| <= 2.09` lies in both `N(C_u)` and `N(C_v)`. So `Block(C_u)` and `Block(C_v)`
overlap and the family is not a partition. The overlap can only *remove* surplus from one
of the two blocks, so `(T')` need not survive it.

**Corrected rule R2'.** Define adjacency at threshold

```
tau := 2 * (209/100) = 418/100 = 4.18 ,
```

i.e. `u ~ v` iff `|u - v| <= 4.18`. Then:

*Disjointness.* If `s in N(C_1) cap N(C_2)` there are `v_1 in C_1`, `v_2 in C_2` with
`|s - v_1| <= 2.09` and `|s - v_2| <= 2.09`, hence `|v_1 - v_2| <= 4.18`, so `v_1 ~ v_2`
and `C_1 = C_2`. Therefore distinct blocks have disjoint neighbourhoods, and since the
components are disjoint the blocks are disjoint.

*Coverage.* Every defective centre lies in its component. Every sound centre is either
within `2.09` of some component — in which case it lies in exactly one block by the above —
or at distance `> 2.09` from every component, in which case it is a singleton block.
So the blocks cover `Lambda` exactly once.

*Boundedness.* `diam Block(C) <= diam(C) + 2 (2.09) = diam(C) + 4.18`, so `(T'')` becomes
`diam(C) <= D_0` with the block diameter `D_0 + 4.18`, and the boundary constant in
`K15-E001` Step 2 uses `D = D_0 + 4.18`.

**Effect on the inequality.** Widening the adjacency threshold *merges* components, which
can only increase `S(C)` relative to `D(C)` (more surplus in the block) while the deficit
`D(C)` grows by the merged defectives. So `(T')` is neither uniformly easier nor harder: it
must be restated for the merged components. The corrected statement is

```
(T'-R2')   S(C) >= D(C)   for every component C of G_def at threshold 4.18,
```

and this is the form to attack. The earlier `(T')` at threshold `2.09` is withdrawn as
ill-posed (its blocks are not a partition).

## K15-E041 — second, sharper obstruction: the dodecahedral theorem is not enough

Independently of `K15-E040`, the best available *per-cell* lower bound cannot reach the
threshold. The dodecahedral theorem gives `vol Omega(w) >= 5.5502910285155` for every cell
of every packing, hence

```
12 * 5.5502910285155 = 66.6034923422   against the required   67.9888142149 ,
shortfall 1.385321873 , i.e. 2.0376 % .
```

**Consequences.**

1. No argument that bounds the twelve outer cells *independently* by the single-cell
   minimum can prove `(T'-R2')`. The proof must use configuration-specific information:
   the six fixed neighbours of each outer centre (`1` at distance `2`, `5` at `2.102851`).
   This is a sharp statement about where the difficulty lies, and it rules out the whole
   family of "apply McLaughlin twelve times" arguments before any work is spent on them.
   The dodecahedral theorem is itself computer-assisted, so importing it would also cost
   more than the estimate it buys.
2. Combined with `K15-E040` (local distance data gives only `4 pi/3 = 4.188790205`), the
   certified bracket on a single outer cell is `[4.188790205, 8.167277]`, and *even its
   best possible value* `5.550291029` is `2.04 %` short of what the sum requires. So the
   deficiency is structural, not an artefact of weak bounds.

**What this leaves.** The only viable shape of proof is an estimate
`vol Omega(w) >= Phi(angular data)` with `Phi > 5.665735` for the *specific* outer
configuration, using that the five non-central neighbours sit at `2.102851 > 2` (their
bisectors are at `1.051426 > 1`, i.e. strictly weaker than tangency) and that at most `12`
centres lie in `[2, 2.09]` (`K15-E014`). That is the next missing inequality.
