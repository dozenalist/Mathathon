# Preregistration S2: the 60°-rotation gluing of the spindle about its hub

## 0. CORRECTIONS (added after review; the original text is kept below, marked)

| # | what I wrote | what is right |
|---|---|---|
| C1 | "**at least one cross edge exists**: `ρ(C1)` at unit distance from `A1`" — offered as a proved *new* interaction | **Retracted: it is not a new constraint.** Since `A1 = ρ(A2)`, the pair `(ρ(C1), A1)` is the image under `ρ` of the internal edge `C1–A2`, i.e. an edge **internal to copy B**. Every unit pair whose two endpoints both lie in `V(M) ∩ ρ(V(M))`-sides of one copy is inherited. A genuine cross edge needs `v ∈ V(M) ∖ I` and `ρ(w) ∈ ρ(V(M)) ∖ I`; `§3` exhibits none. |
| C2 | the abstract `k = 5` forced-equality gadget "`K5` with edge `uv` subdivided by `w`" | **False.** `G` is 4-colourable (`u,v` share a colour, the other three take three colours, `w` reuses one), and `G + uv` is 5-colourable (`w` is not adjacent to the three others and may reuse a colour), so `uv` is **not** forced. The correct standard example is **`K6` minus one edge**: `χ = 5` (`u,v` share a colour, the other four distinct), and adding `uv` gives `K6`, which is not 5-colourable. It is geometrically unrealizable because `{u, x1, x2, x3}` is a `K4`. |
| C3 | "the gluing is by an isometry with a fixed point, so the two copies are *not* parallel translates … with it the 'everything stays separated' mechanism" | **Retracted, no proof.** Nothing shows that a fixed-point isometry prevents the union's colouring family from separating pairs. The only defensible differences from a translation are bookkeeping: overlap size, countability, and the preimage map. Separation must be *measured*, never inferred from the type of isometry. |
| C4 | the overlap conditions "`c₁(K) = c₂(K)`, `c₁(A1) = c₂(A1)`, `c₁(B−) = c₂(B−)`" | **Wrong indexing.** With `c₂` indexed by *original* `M`-vertices (`c₂(w)` is the colour of the point `ρ(w)`), the shared-point equations are `c₁(K) = c₂(K)`, **`c₁(A1) = c₂(A2)`**, **`c₁(B−) = c₂(B+)`**. The shared-vertex preimage map is `ρ⁻¹` restricted to `I`: `K ↦ K`, `A1 ↦ A2`, `B− ↦ B+`. |

Analysis only; nothing executed. For the graph worker's next compute slot (one process, 60 s,
validation included). Grades **[P]** hand-proved here, **[C]** cited, **[X]** requires the run.

## 0. Why this design, and what is honestly claimed

The closed seed's lesson is structural, and I can state it as a theorem rather than as a measurement.

**Separation-trichotomy [P].** If the proper `k`-colouring family of `G` *separates* a pair `{a,b}` (some
colouring gives them different colours), then `{a,b}` is not a forced-equal pair at `k`. Hence:

> **If the colouring family of `G` separates every nonedge, `G` has no forced-equal pair at `k`.**

The closed union had 34 five-colourings whose signatures separate all 1048 vertices and all 543141
nonedges `[C]`; by the trichotomy it *could not* have had a forced-equal pair. So the closure is not bad
luck. **Design constraint for any new seed: it must leave at least one nonedge unseparated.** (Note the
asymmetry: forced *difference* is fully compatible with separation, so this rules out only the equality
direction — the one the amplifier needs.)

**What S2 is.** A small, fully exact probe of the one gluing channel that is neither a common-neighbour
count nor a translation: a **rotation with a fixed point**, which produces a *provably non-clique,
3-point overlap* and at least one *provably* present cross edge. What it is **not**: a candidate forcing
gadget. At ≤ 11 vertices nothing can force at `k = 5`, so I do **not** claim S2 improves the forcing odds;
the improvement I do claim is verifiability and mechanism transparency (§6), plus a sharp falsifier.

## 1. The exact object

`M` = Moser spindle, `7` vertices, `11` edges, `χ = 4`, in `Q(√3, √11)` (`udg/build.py::moser`):
hub `K = (0,0)`; tips `C1 = (√3, 0)`, `C2 = √3·(5/6, √11/6)` (so `|C1| = |C2| = √3` and
`|C1 − C2| = 1`); apexes `A1 = (√3/2, 1/2)`, `A2 = (√3/2, −1/2)` of diamond `K–C1`; apexes `B±` of
diamond `K–C2`. In polar form about `K`: `A1` at `(1, 30°)`, `A2` at `(1, −30°)`, and `B±` at `(1, θ_c ± 30°)`
with `cos θ_c = 5/6` (`θ_c = 33.557°`), because an apex of a diamond is at radius `1` and at `±30°` from
the diamond's axis.

**Isometry.** `ρ = R_{60°}` about the origin (the hub): entries `cos 60° = 1/2`, `sin 60° = √3/2`, both in
`Q(√3) ⊂ Q(√3,√11)`. **Coordinates stay in the same field; no extension, no float.**

**Seed.** `S2 = V(M) ∪ ρ(V(M))`, with `V(M)` and `ρ(V(M))` identified wherever the points are equal.

## 2. The overlap, proved exactly [P]

`ρ` preserves the radius from `K` and adds `60°` to the angle. Vertex by vertex:

| `v` | radius, angle | `ρ(v)` | in `M`? |
|---|---|---|---|
| `K` | `0` | `K` | yes (fixed) |
| `A2` | `1, −30°` | `1, 30° = A1` | **yes** |
| `B+` | `1, θ_c − 30°` | `1, θ_c + 30° = B−` | **yes** |
| `C1, C2, A1, B−` | `√3, 0°`; `√3, θ_c`; `1, 30°`; `1, θ_c+30°` | angles `60°`, `θ_c+60°`, `90°`, `θ_c+90°` | no (no vertex at those angles) |

So the overlap is **exactly `I = {K, A1, B−}`**, three points, and `ρ` has a fixed point, so the two copies
are *not* parallel translates.

**The overlap is non-clique, with an exact metric [P].** `|K − A1| = |K − B−| = 1` (both are apexes), so
`KA1` and `KB−` are edges; and
`|A1 − B−| = 2 sin(θ_c/2) = 1/√3 ≈ 0.5774` — exact, since `sin(θ_c/2) = √((1 − 5/6)/2) = 1/(2√3)` —
so `A1B−` is **not** an edge. The overlap is a 3-vertex path `A1 – K – B−`: non-clique, exactly as the
informative case of `GLUING-CORRECTED.md` §4 requires, and it is *proved*, not sampled.

## 3. ~~A cross edge, proved exactly~~ — RETRACTED, see C1: the pair is a B-internal edge.

`|ρ(C1) − A1|`: radii `√3` and `1`, angle difference `60° − 30° = 30°`, so

    |ρ(C1) − A1|² = 3 + 1 − 2·√3·1·cos 30° = 4 − 2·√3·(√3/2) = 4 − 3 = 1.

So `ρ(C1)` is at unit distance from `A1`: `S2` has **at least this one cross edge**, proved by hand, with
`cos 30° = √3/2` exact. (By the same 3-4-3 pattern, every pair with radii `√3, 1` and angle `30°` is a unit
pair — a reusable rule for the worker's enumeration: `Δθ = 30°`, radii `√3` and `1`.)

## 4. The colouring-compatibility obligation it introduces [P]/[X]

A colouring of `S2` is a pair `(c₁, c₂)` of proper `k`-colourings of `M` with

* **overlap equations:** `c₁(K) = c₂(K)`, `c₁(A1) = c₂(A1)`, `c₁(B−) = c₂(B−)` — three equations, and the
  *same* boundary datum on `I` for both copies (products over different data are inadmissible,
  `GLUING-CORRECTED.md` §4);
* **overlap-internal constraint:** `c(K) ≠ c(A1)` and `c(K) ≠ c(B−)` (those are edges), with `c(A1)` and
  `c(B−)` unconstrained *by the overlap itself* because `|A1 − B−| = 1/√3 ≠ 1`;
* **cross-edge inequalities:** `c₁(v) ≠ c₂(w)` for every pair `(v, w)` with `|ρ(v) − w| = 1`. This set is
  **[X]** — only one element is proved (§3), the rest must be enumerated exactly; the enumeration is
  `O(|V|²) = 49` exact comparisons in `Q(√3,√11)`.

Feasibility is joint: the number of boundary data `γ` extendible in *both* copies is the quantity to
report, together with `|joint colouring set|`.

## 5. Falsifier, stated before the run

1. **Count check:** `|V(S2)| = 7 + 7 − |I| = 11` and `|I| = 3`. If the run reports `|I| ≠ 3`, the overlap
   argument of §2 is wrong and everything downstream is void (**this is a test of my arithmetic, and I
   expect it to pass**).
2. **Cross-edge count `≥ 1`** with the exhibited edge `ρ(C1)–A1` present. If the enumerated set misses it,
   the enumeration is buggy; if it contains it, §3 is confirmed.
3. **The falsifier proper:** at `k = 5`, if the joint colouring set separates every nonedge of `S2`, then
   by the trichotomy `S2` has no forced-equal pair — and, at 11 vertices, that is the outcome I expect. The
   informative content then is: *the non-clique 3-point overlap channel produces no forcing at this scale*,
   which kills the hope that "make the overlap non-clique" alone suffices and redirects effort to
   mechanisms that supply four simultaneous exclusions (`k = 5`) at planar cost.
4. **Red flag:** if `S2` is not 4-colourable, stop: that would mean `χ ≥ 5` from 11 vertices, is
   implausible, and must be treated as a bug until DRAT-checked.

## 6. What is and is not justified as an improvement

**Justified [P]:**
* The overlap and one cross edge are *proved*, not hoped for, with exact `Q(√3,√11)` arithmetic — unlike
  the closed translation, whose 58/184 counts were obtained by computation and whose union was too large to
  check by hand.
* The gluing is by an isometry with a **fixed point**, so the copies are not in parallel position; the
  closed route's symmetry (a translate of a set against itself) cannot recur, and with it the
  "everything stays separated" mechanism.
* At 11 vertices the whole joint analysis is hand-checkable, so the *mechanism* can be certified rather
  than merely measured.
* The separation-trichotomy of §0 turns the closure into a **design constraint** (a new seed must leave a
  nonedge unseparated), which the closed route could not satisfy by construction.

**Not justified — stated rather than invented:** I cannot argue that `S2` has a better *chance* of
producing a forced-equal pair than any other seed. It is too small to force anything at `k = 5`; its value
is calibration of the non-clique-overlap channel and a cheap exact test of my own §2 arithmetic. If the
graph worker's new-seed job is aimed at forcing, `S2` should not displace it.

## 7. Distinguishing the abstract gadget from its induced realization [P]

The abstract mechanism I would *like* at `k = 5` is transparent and **geometrically impossible**:
`G_abs` = `K5` with the edge `uv` subdivided by a new vertex `w` is `5`-colourable, `G_abs + uv` is not
(`uv` becomes a `K5`), so `{u,v}` is forced equal at `k = 5` — but `G_abs` contains a `K4` (`u` together
with the `K3` on the other three vertices), and **no four points of the plane are pairwise at distance
`1`**. So this abstract gadget has *no* induced unit-distance realization, and any realizable substitute
must build the four exclusions out of triangles and cross-copy constraints instead. `S2` is the first
step of that programme, not a solution of it.
