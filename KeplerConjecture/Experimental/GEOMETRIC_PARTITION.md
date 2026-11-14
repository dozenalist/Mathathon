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

## Honest verdict

The rule is explicit, bounded (`diam <= 4.18`, `|K| <= 13`), and correct on FCC and HCP
with equality. It is **not proved**, for two separate reasons: the target inequality (T)
on the icosahedral block, and the ordering defect `K15-E031`. I make no claim that this
route is simpler than Hales's; it reduces the global partition problem to one inequality
about a specific 13-centre configuration, and that inequality is open.
