# The exact remaining lemma, against Hales' accounting and the literature

Block `K15-REVIEW-0308-M`. The project's geometric route now reduces to **one**
statement. This file states it exactly, compares it with the accounting lemma Hales
actually uses, and names the closest literature.

## 1. The statement

For a saturated packing `Λ`, `b(v) = √32 − vol Ω(v)`, a range `R` and a bound `Φ`:

> **Cut condition.** `Σ_{v∈U} b(v) ≤ Φ·|δ⁺_R(U)|` for every finite `U ⊆ Λ`,

equivalently (`K15-C044`, `K15-C067`): there is an antisymmetric transfer `φ` on the
`R`-graph with `|φ| ≤ Φ` and `Σ_w φ(v,w) ≥ b(v)` for every `v`. Sufficiency in the
infinite case uses Tychonoff compactness, which needs the degree bound `≤ 12` that
`K15-C054` supplies at `R ≤ 2.09`.

Valid necessary condition: `Φ ≥ (√32 − V_dod)/12 = 0.0088803…` (`K15-C081r`,
singleton cut; the cluster-level `0.0104949` is withdrawn).

What is *not* implied: any `|U|^{2/3}` form for arbitrary `U` (`K15-C079`
corrected). For ball cuts `U = B(x,r) ∩ Λ` one has `|δ⁺(U)| ≤ 3k_RR r²`, so the
slack is explicit there; for general `U` the only bound is `k_R|U|`.

## 2. Hales' accounting lemma, from his own text

Read from `Literature/Papers/Hales2005-unabridged.pdf`, Ch. 7 (§7.3–7.4):

> **Definition 7.12.** `σ(D) = −4δ_oct(vol Ω(D) + A₀(D)) + 16π/3`, "the score of the
> decomposition star".
>
> **Lemma 7.13.** The following are equivalent: (1) the minimum over `DS` of
> `vol Ω(D) + A₀(D)` is `√32`; (2) the maximum of `σ` on `DS` is `8 pt`
> (`pt ≈ 0.05537`). Moreover these imply that `A` is fcc-compatible for every
> saturated packing.
>
> **Theorem 7.14.** If `max_DS σ = 8 pt`, then every saturated packing admits a
> negligible fcc-compatible `A`.
>
> **Definition 7.15.** A *standard cluster* is a pair `(R, D)` …; §7.4 expresses `σ`
> as a sum of terms attached to standard regions, and Ch. 10 bounds the score in
> triangular and quadrilateral regions.

**The decisive structure.** `DS` — the set of *decomposition stars* — is a **compact,
finite-dimensional** space of local configurations (bounded radius, finitely many
combinatorial types after tameness). Hales' Lemma 7.13 converts the pointwise
inequality over *all packings* into an optimisation over `DS`, and §7.4 + Ch. 10 convert
that into finitely many LP problems. That is where his finitisation happens, and it is
what makes his proof computable.

Our cut condition has **no analogue of `DS`**: it quantifies over subsets of a packing,
not over local configurations, so there is no compact reduction to appeal to. This is
the precise structural difference, and it is sharper than "finite vs infinite": Hales'
obligation is an optimisation over a compact space; ours is a family of inequalities
indexed by all cuts.

## 3. Comparison

| | Hales | cut condition |
| --- | --- | --- |
| quantifier | every Delaunay star (finitely many combinatorial types) | every finite `U` in every packing |
| the identity | exact rearrangement + cancellation | flow duality (Hoffman) |
| finitisation | yes — tame graphs, exhaustive enumeration | **no** — the cut is an arbitrary subset |
| equality structures | 8 quasi-regular tetrahedra + 6 quad clusters (fcc) | `φ ≡ 0` on fcc/hcp (`K15-C078`) |
| verification cost | `~10⁵` configurations, `~10⁵` LPs | one min-cut per *packing*; not reducible to a finite list |
| what it needs from geometry | star inequalities, interval arithmetic | a cell-volume lower bound uniform over cuts |

**The exact difference.** Hales' accounting is a *rearrangement into finitely many
local shapes*; the cut condition is an *averaged inequality over arbitrary subsets*.
The transfer packaging (`K15-C035`) replaces Hales' negligibility bookkeeping with a
two-line estimate, but it does **not** finitise the geometric obligation — and
`K15-C036` shows no finite completion can verify it either. So the remaining lemma is
strictly harder to verify *mechanically* than Hales' star inequalities, and strictly
weaker *as a statement* (it permits the transfer to be funded across- cuts). Whether
that trade is favourable depends on an analytic cell-volume bound that nobody has.

## 4. Closest literature

| Source | Statement | Relation |
| --- | --- | --- |
| L. Fejes Tóth, 1953/1964 (weighted averaging over ≤ 13 Voronoi cells) | a weighted average of cell volumes ≥ the rhombic dodecahedron would give Kepler; needs an explicit form of the Newton–Gregory problem | the *averaged* ancestor of the cut condition, with a specific weight rule; never completed |
| Muder 1998 | `vol Ω ≥ 5.41848` pointwise, by cone decomposition + convexity | pointwise, thus capped at `V_dod` (`K15-C029`'s ceiling argument, `X-C003`) |
| Hales–McLaughlin 2010 | `vol Ω ≥ V_dod` pointwise | the best pointwise bound; below `√32` by `1.92%` |
| Rogers 1958 | `vol Ω ≥ 5.372754` from a simplex decomposition | weaker pointwise; the same simplex device is the natural tool for a *cluster* bound |
| Bezdek's surface-area method | bounds `vol Ω` via `∂Ω` | a different functional; not obviously compatible with the cut condition |

**Assessment.** No published source proves anything of the cut form, and none of the
pointwise results can reach `√32` (Hales–McLaughlin is optimal pointwise, by the
dodecahedral theorem). So the remaining lemma is genuinely open and is *not* a
rephrasing of a known result. Its value is that it isolates the difficulty in one
statement with an explicit constant, and that the negligibility half is proved.

## 5. What a block should do with it

1. **Prove it for ball cuts** first (the boundary term is explicit there), then ask
   whether ball cuts suffice — they do not suffice for Hoffman in general, so this
   needs a separate argument or a *specific* `φ` built by a local formula.
2. ~~Try an explicit local `φ`~~ — **attempted and refuted** in `K15-C085`: the ansatz
   `φ(v,w) = ψ(v−w)(b(v)−b(w))` reduces the requirement to `(s−1)b(v) ≥ (ψ*b)(v)`,
   which fails on a three-line defect model at exactly the vertices that must fund the
   deficit (the formula overshoots). The remaining honest route is a genuine
   min-cut flow; a closed local form is not expected.
3. Keep `Φ` bounded: the rate in Lemma 3.3 is `O(Φ/r)`.
