# Does the weak `MarkedDisk.Valid` suffice? Every consumer, every obligation

Question: paper Lemma 7.4 item (1) (l. 2361–2366) demands, for each `x ∈ L₀`, *precisely one* core disk
`B_{n,x}` containing `x` in its interior, *different points different disks*, and `B_{n,x} ⊂ int Q` if
`x ∈ Q` (else disjoint from `Q`). The Lean records only

```
def MarkedDisk.Valid (L : Set ℂ) (d : MarkedDisk) : Prop :=
  0 < d.radius ∧ (d.core = true → ∃ x ∈ L, x ∈ d.ball)          -- DiskExtension.lean:17-18
```

Is the weaker property enough? Grades: **[S]** source read; **[S+]** source read and the obligation
follows by the cited lines; **[P]** paper argument; **[C]** my inference.

## 1. Complete consumer list (grep over `lean/OAI`, `--include=*.lean`)

| consumer | file:line | which part of `Valid` is used | obligation discharged? |
|---|---|---|---|
| `MarkedDisk.closedBall_near_core` | `HoleApproximation.lean:31` | `.2`: `core = true → ∃ x ∈ L, x ∈ d.ball`; concludes `d.closedBall ⊆ ball x (2·d.radius)` | **yes [S+]**: `hd.2 hc` yields the point; the containment is `dist_triangle` + `hz` |
| `MarkedDisk.merge` | `DiskExtension.lean:20-24` | both `ha hb`; result `d.Valid L` with `d.core = (a.core ‖ b.core)` | **yes [S+]**: if the merged disk is core, one of `a`,`b` was; its witness point lies in `a.ball ⊆ a.closedBall ⊆ d.ball` (the containment clauses in the conclusion) |
| `MarkedDisk.separate` | `DiskExtension.lean:90-94` | hypothesis `hS`, conclusion `∀ d ∈ T, d.Valid L` plus `∀ d ∈ S, ∃ e ∈ T, d.ball ⊆ e.ball ∧ (d.core = true → e.core = true)` | **yes [S+]**: the covering clause plus core-marker preservation carry each witness into its covering disk |
| `MarkedDisk.radius_le_sum` (usage) | `HoleApproximation.lean:308` | `.1` only: `0 < d.radius` | **yes [S+]** (positivity bookkeeping) |
| sum-nonneg for `ε`/annuli limits | `HoleApproximation.lean:318`, `:323` | `.1.le` only | **yes [S+]** |
| `HoleApprox.valid` field itself | `HoleApproximation.lean:285` | carrier; consumed at `FullApproximation.lean:311-314` to feed `separate` | — |
| `initialDisks` producer | `HoleApproximation.lean:63` | produces `∀ d ∈ initialDisks, d.Valid L` | — |
| `centerDisks` producer | `FullApproximation.lean:307-309` | `⟨hR0, by simp⟩`: the second conjunct is **vacuous** because `centerDisks` are built with `core := false` | — |

There are **exactly three** uses of the `.2` conjunct (`closedBall_near_core`, `merge`, `separate`) and
**four** uses of `.1` (positivity/budget bookkeeping). No consumer anywhere uses "precisely one disk per
point", injectivity of `x ↦ B_{n,x}`, or the `int Q` / disjoint-from-`Q` clauses.

**Verdict: for every consumer in the tree, the weak property suffices** — verified at source level, with
the obligations discharged as tabled. This does **not** say the paper's item (1) is unnecessary; it says
nothing in the Lean's proof consumes more.

## 2. Where the paper's extra clauses actually live in the Lean — by construction, not by `Valid`

| paper clause | Lean carrier | status |
|---|---|---|
| for each `x ∈ L₀` a disk, injectively | `centerDisks L R := L.image (fun x => ⟨x, R, false⟩)` (`GraphPatches.lean:245`) + `mem_centerDisks : d ∈ centerDisks L R ↔ ∃ x ∈ L, d = ⟨x,R,false⟩` (`:246`) | **[S+]** injectivity comes from `Finset.image`, i.e. from the *construction* |
| disks disjoint | `centerDisks_disjoint` (`GraphPatches.lean:251`) and the separation hypothesis `hsep`/`hRsep : 2R < dist x y` (`:280`, `FullApproximation.lean:280-283`) | **[S+]** |
| `B_{n,x} ⊂ int Q` / disjoint from `Q` | replaced by the choice of ambient balls: cover on `closedBall 0 5`, map on `closedBall 0 7`, centres restricted to `activeCenters L = L.filter (fun x => dist x 0 ≤ 6)` (`GraphPatches.lean:274`), `R ≤ 1/2`, `R ≤ s/4` | **[S] substituted, not stated**; the paper's containment clause has no direct Lean counterpart |

## 3. A trap worth recording (statement-level)

The Lean's `core : Bool` flag does **not** mean the paper's "core disk". `centerDisks` — the fixed disks
around the cyclic centres — are built with `core := false`. `coreHoles` (= the disks excluded from the
map's domain, `DiskExtension.lean:519`) collects `core = true`. So:

* paper "core disk `B_{n,x}`" ↔ Lean **`centerDisks` entry**, which has `core = false`;
* Lean `core = true` ↔ the disks that are `initialDisks` entries in `small_hole_map` and that are
  *removed from the map's domain* and *exempt from the non-core radius budget* (`noncoreCost`).

A reader who maps "paper core disk" to "Lean `d.core = true`" gets the partition backwards. The paper's
item (1) content is carried by `centerDisks` + `hRsep` + `activeCenters`, i.e. by the construction of the
disk family, while `Valid`'s second conjunct is used only for the *other* class of disks.

## 4. What is still missing (precise, not a gap assertion)

* Nothing in the tree states "for each `x ∈ L₀` there is a disk of the family containing `x` in its
  interior" as a *property of an arbitrary `HoleApprox`*; it holds only because `fullApprox_exists` adds
  `centerDisks A R` at that point (`FullApproximation.lean:306`). If a future proof needed the property
  from `HoleApprox` alone, it would be missing. **[S]**
* The paper's `Q`-containment/outside-`Q` clause has no Lean counterpart as a statement; the Lean gets the
  same effect from `activeCenters`' cut at `dist ≤ 6`, `R ≤ 1/2` and the `5`/`7` ball choice. Whether that
  is equivalent for the later use (Lemma 7.6's "core disk contained in `Q`") is **[C] my reading, not
  verified**.
* Consequence for the earlier worry, stated carefully: the *consumer* audit is closed (no consumer needs
  more than the weak property); the *producer* comparison (does `fullApprox_exists` produce disks with all
  the geometric properties item (1) promises, at the paper's radii) is **not** closed here.
