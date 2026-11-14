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

---

## 5. Producer side: `initialDisks → small_hole_map → fullApprox_exists` (block 15)

### 5.1 The construction

```
def initialDisks (L C : Finset ℂ) (δ u : ℝ) : Finset MarkedDisk :=
  L.image (fun x => ⟨x, δ, true⟩) ∪ C.image (fun x => ⟨x, u, false⟩)        -- HoleApproximation.lean:59-60
lemma mem_initialDisks : d ∈ initialDisks L C δ u ↔ (∃x∈L, d = ⟨x,δ,true⟩) ∨ (∃x∈C, d = ⟨x,u,false⟩)   -- :61-63
lemma initialDisks_valid (hδ : 0<δ) (hu : 0<u) : ∀ d ∈ initialDisks L C δ u, d.Valid L   -- :64-70, core case uses mem_ball_self
```

and the producer statement, verbatim (`HoleApproximation.lean:115-125`):

```
theorem small_hole_map (hc : Measurable c) (hα : 0<α) (hα' : α<1/5) (L : Finset ℂ)
    (hL : ∀ x ∈ closedBall 0 8, ¬(transitionGraph c x).IsAcyclic → x ∈ L)
    (ht : 0<t) (ht' : t<1/2) :
    ∃ e > 0, ∀ ε, 0<ε → ε<e → ∃ S : Finset MarkedDisk,
      (∀ d∈S, d.Valid L) ∧ (S pairwise closed-ball disjoint) ∧ (∑ d∈S, d.radius) < t ∧
      ∃ g : C(↥(closedBall 0 7 \ coreHoles S), GraphSpace ⊤),
        ∀ z, z.val ∉ diskHoles S → (g z).val = thresholdMap c ε α z.val
```
consumed by `holeApprox_exists` (`:291`, taking `ε := min (e/2) (t/2)`) and hence by
`fullApprox_exists` (`FullApproximation.lean:330`) after `eventually_fill_cores` adds the centre disks.

### 5.2 Paper item (1) clause by clause, against the construction (not against `Valid`)

| paper clause (l. 2361–2366) | Lean | status |
|---|---|---|
| one designated core disk `B_{n,x}` per `x ∈ L₀` | `initialDisks`'s **L-part**: `L.image (fun x => ⟨x, δ, true⟩)`, i.e. the disk is *built from* `x` | **holds by construction** [S+] |
| contains `x` in its interior | centre is `x`, radius `δ > 0`, so `x ∈ ball x δ`; this is literally used in `initialDisks_valid`'s core case (`Metric.mem_ball_self hδ`) | **holds** [S+] |
| different points give different disks | `Finset.image` of the injective map `x ↦ ⟨x, δ, true⟩`; `mem_initialDisks` characterises members | **holds by construction** [S+] |
| `B_{n,x} ⊂ int Q` for `x ∈ Q`; `B_{n,x} ∩ Q = ∅` for `x ∉ Q` | no such statement. The Lean fixes the ambient balls (`closedBall 0 7` for the map, `closedBall 0 5` for the cover), chooses `δ ≤ t/2` small, restricts centres by `activeCenters (dist · 0 ≤ 6)`, and preserves each disk by containment in `separate` (`d.ball ⊆ e.ball`) | **substituted, not stated** [S]; equivalence with the paper's clause is [C] my reading |

So **uniqueness and "contains its own point" are not assumed from `Valid` — they are structural facts of
`L.image (fun x => ⟨x, δ, true⟩)`**, which is exactly what the paper's item (1) asserts, minus the `Q`
containment.

### 5.3 Correction to §4 of this note (the "core flag" trap)

§4 said the Lean's `core` flag does not mean the paper's core disk. That is right for `centerDisks` but was
stated too broadly. The full picture:

| family | built as | `core` | role |
|---|---|---|---|
| `initialDisks`’ L-part | `L.image (fun x => ⟨x, δ, true⟩)` (`HoleApproximation.lean:60`) | **true** | the paper's `B_{n,x}`: excluded from the map's domain via `coreHoles`, exempt from `noncoreCost`, filled by nothing |
| `initialDisks`’ C-part | `C.image (fun x => ⟨x, u, false⟩)` | false | the disks that *are* filled through trees |
| `centerDisks L R` | `L.image (fun x => ⟨x, R, false⟩)` (`GraphPatches.lean:245`) | false | **extra** disks added in `fullApprox_exists_of_finite_core` around cyclic centres; charged to the budget (`centerDisks_sum`), disjoint by `centerDisks_disjoint`/`hRsep` |

So the paper's core disks ↔ the **L-part of `initialDisks`** (`core := true`), and `centerDisks` is a
different, additional family that happens to be built over the same index set `L`. Reading "`core = true`"
as "paper core disk" is correct; reading `centerDisks` as the paper's core disks is what is wrong.

### 5.4 Why the Lean can be weaker and still be right

The formal development deliberately proves the *sufficient* statement: `Valid` records only what the three
consumers need (§1), and the geometric content the paper puts into item (1) is delivered by the
*construction* (5.2) rather than as a hypothesis on an arbitrary `HoleApprox`. That is weaker as an
interface and stronger as a fact: nothing downstream has to re-derive uniqueness. The paper's wording is
therefore not imposed where the formal statement does not need it.

### 5.5 Exact remaining wiring obligation

1. **Item (1)** is discharged at source level for uniqueness/containment-in-own-point, and *substituted* for
   the `Q`-containment. The remaining obligation is a **derived statement, not a new hypothesis**: for
   `x ∈ L` with `dist x 0 ≤ 6`, the L-part disk `⟨x, δ, true⟩` lies inside `closedBall 0 7` (and inside the
   cover region once `δ ≤ 1/2`), which follows from `dist x 0 + δ ≤ 7`. Nobody needs it in the current
   proof (the map's domain is *defined* by `coreHoles`), so it is a documentation/referee item.
2. **Wiring to `Five.lean`**: none of this changes `Five.lean`. The chain
   `no_measurable_weak_five_coloring → fullApprox_exists → …` is unchanged, and the cover obstruction is
   applied at `Five.lean:54` to `PlanarCover.compact_open_cover_impossible` over the positive-coordinate
   components. The only outstanding *wiring* remains the substitution edge: no module of `lean/` references
   `paper_lemma_7_5` / `compact_cover_obstruction_gen`, so re-pointing `Five.lean:54` (plus a rebuild of the
   25-module cone) is still the single structural step between the topology substitution and use.
