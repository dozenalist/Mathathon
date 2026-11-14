# Preregistration S3: a designed, exact translation of Heule553 with two guaranteed *genuine* cross edges

Source/hand arithmetic only; nothing executed. For the graph worker's single 60 s slot (optional — see §6).
Grades: **[P]** hand-proved, **[C]** cited, **[S]** read from source, **[X]** needs the run.

## 0. The distinction the design must respect [P]

With copy A = `V(H)` and copy B = `V(H) + τ`, the union's unit pairs split into four classes:

1. **A-internal** — both endpoints in `V(H)`: already edges of `H`;
2. **B-internal** — both in `V(H) + τ`: already edges of `H` (transported);
3. **overlap incidence** — a pair with at least one endpoint in `I = V(H) ∩ (V(H)+τ)`: *inherited* from a
   copy, hence no new constraint (this is exactly what went wrong in `PREREG-S2.md` §3, retraction C1);
4. **genuine cross** — `v ∈ V(H) ∖ I`, `w + τ ∈ (V(H)+τ) ∖ I`, `|v − w − τ| = 1`.

Only class 4 couples the two colourings. The closed `τ₀ = (3/2, √3/2)` union had 58 overlaps and 184 cross
edges `[C]`, but the split between classes 3 and 4 was never reported, so its "184 cross edges" may
substantially be overlap incidence.

**The shared-vertex preimage map.** For `p ∈ I`, `p` is the A-vertex `p` and the B-vertex `w = p − τ`. The
compatibility equations are `c₁(p) = c₂(p − τ)` for every `p ∈ I`. (For a rotation `ρ` the map is `ρ⁻¹`
on `I`, as in `PREREG-S2.md` retraction C4.)

## 1. The design [P]

**Inputs from `H`:** one edge `{a, b}` of `H` (any edge — the graph is a unit-distance graph with ~5487 of
them), and one vertex `r ∈ V(H)`. Both are in the field `K` in which `H`'s coordinates are exact `[S]`.

**Construct** the apex of the equilateral triangle erected on the *difference* segment `d₁ = a − r`,
`d₂ = b − r`:

    n̂ := R_{90°}(b − a)          (a unit vector, because |b − a| = 1 — this is why an *edge* is used)
    τ  := (d₁ + d₂)/2 + s·(√3/2)·n̂,       s = ±1.

**Why this is exact and needs no search.** `d₁ + d₂ = (a + b) − 2r`, so `τ = (a + b)/2 − r + s(√3/2)·n̂`.
`n̂` is a rational rotation of the unit vector `b − a`, so `τ ∈ K²` **provided `√3 ∈ K`**; if not, the one
quadratic extension `K(√3)` suffices, and *every* field element stays exact in it.

**The two guaranteed genuine cross edges [P].** By the equilateral closure,
`|τ − d₁| = |τ − d₂| = 1`. Since `d₁ = a − r` and `d₂ = b − r`,

    |a − (r + τ)| = |d₁ − τ| = 1,        |b − (r + τ)| = |d₂ − τ| = 1.

So the *translated vertex* `r + τ` is at unit distance from **both** `a` and `b`. Both pairs are class-4
candidates: they are genuine provided (i) `r + τ ∉ V(H)` (equivalently `τ ∉ D(H)`, no overlap at `r`) and
(ii) `a − τ ∉ V(H)` and `b − τ ∉ V(H)` (so `a, b` are not themselves overlap vertices). Two exact tests
each, in `K`. **If (i) or (ii) fails, the design is void for that `(a, b, r)` and must be re-instantiated —
that is a checked-in-advance obligation, not an afterthought.**

**No overlap by preference.** Choosing `τ ∉ D(H)` (which the apex almost surely satisfies and which the test
decides) makes the union a *pure-inequality* coupling: zero equality equations, every constraint of the form
`c₁(x) ≠ c₂(y)`. This is the cleanest possible shape for §2's counting argument, and it is the structural
improvement over the closed translation, whose coupling was dominated by 58 equality equations on an
overlap pattern that also absorbed much of the cross-edge budget.

## 2. Why an interaction of this kind is the right thing to ask for — the exact missing condition [P]

To force `c₁(v) = c₂(w)` at `k = 5`, the joint set must contain **no** admissible pair with
`c₁(v) = c₂(w)`. Equality is not a distance constraint, so this can only come from *exhaustion*: every
pairing with equal colours at `(v, w)` must violate some constraint. At `k = 5` the pair `(v, w)` needs
**four** excluded colours. Two at most can come from `H`'s own geometry for a non-adjacent pair, because
the common-neighbour channel is capped at two vertices (the two points at distance `1` from both `v` and
`w`; and for `|v − w| = √3` those two are adjacent, which is the diamond mechanism, forcing only at
`k = 3`). **Therefore the missing geometric condition is:**

> **(G4)** the translation must supply **at least two further exclusions for the *same* pair `(v, w)`**,
> i.e. there must be genuine cross edges from `v` to vertices of copy B whose colours are forced distinct
> from each other and from the two common-neighbour colours — so that the joint palette of `(v, w)` drops
> to a single colour.

`S3` guarantees **two** cross edges incident to a *single* translated vertex `r + τ`, aimed at vertices
`a, b` of copy A. That satisfies the "≥ 2 cross edges" count in **(G4)** but *not* its content: the two
exclusions must attach to the pair `(v, w)` we want equal, and must exclude *different* colours. Whether
`S3`'s two edges do this is precisely what the run must settle, and I cannot decide it by hand.

**This is the honest bottom line:** `S3` is the best placement I can justify exactly (two guaranteed,
class-4, exactly verified cross edges, zero overlap if the test passes, all coordinates in `K(√3)`), but
**(G4) remains unmet by construction**, and I have no hand argument that `S3` is closer to a forced pair
than the closed translate. If the graph worker's slot is scarce, `S3` should be tried only as the cheap
exact check of §3, not as a forcing candidate.

## 3. What the run would report (four numbers, in this order)

1. `|I| = |V(H) ∩ (V(H)+τ)|` and the preimage map `p ↦ p − τ` on `I` (expected `∅`).
2. Cross-pair census **split by class**: A-internal, B-internal, overlap-incidence, **genuine cross**, with
   the two exhibited pairs `(a, r+τ)`, `(b, r+τ)` flagged as present.
3. `|joint colouring set|` at `k = 5` by the same pipeline that produced the 34 witnesses.
4. Whether that family separates every nonedge of the union (the falsifier of `PREREG-S2.md` §5, reused).

**Falsifier, stated in advance.** If `|I| > 0`, or if either exhibited pair is class-3 rather than class-4,
`S3`'s mechanism is void (a bug or a bad `(a,b,r)`, not a result). If `|I| = 0`, both pairs are class-4 and
the colouring family still separates every nonedge, then `S3` adds no forcing — the informative negative is
that *two* isolated cross edges cannot meet **(G4)**, and the next design must attach four exclusions to one
pair rather than two edges to one vertex.

## 4. What is *not* claimed

No forced pair, no non-`k`-colourability, no separation statement, no rigidity inference, and no claim that
a non-parallel or fixed-point isometry changes the separation behaviour (retraction C3 of `PREREG-S2.md`).
`H`'s coordinates and field are **[S]** (read from the worker's builder), the counts 1048/58/184 are **[C]**,
and every construction here is **[P]**.
