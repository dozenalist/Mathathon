# Accepted lemmas, open gaps, and closest sources — the one-page account

> **Supervisor review, 05:23 Pacific:** the generic flow checker at a25f5be
> falsely accepts isolated positive deficits; its acceptance is suspended.
> Main's exact FCC/HCP contact-polytope calculation and X's finite checker
> comparisons pass locally. All eight numerical pilots found no refutation.
> C106-C108 and universal geometric improvements remain pending independent
> review; no new best bound or simpler proof is accepted. This current scope
> overrides conflicting author labels. See [the review](REVIEW_2026-11-14_0523.md).

> **Supervisor review, 04:38 Pacific:** named C input repairs now pass,
> and the smaller C017 certificate independently verifies <0.782267254857.
> X reviewed the repaired conditional graph theorem. Geometric cut inequalities
> and fully exact Barlow/C5 certification remain open; the latter scripts still
> use floating decisions. See [the current review](REVIEW_2026-11-14_0438.md).

> **Supervisor review, 03:53 Pacific:** specific X-C015/016/017 matrix
> certificates independently pass, strongest < 0.782267220134. Geometric
> fixture thresholds are suspended for a false volume enclosure and edge tests.
> C093's repaired cut/flow proof awaits X; C094's Barlow proof has a circular
> redundancy step; C095 crack geometry remains pending. The negative-eta checker
> defect is repaired and 37 tests pass, but generic soundness stays suspended.
> These decisions override conflicting author labels. See
> [REVIEW_2026-11-14_0353.md](REVIEW_2026-11-14_0353.md).

> **Supervisor scope, 03:08 Pacific:** C081 is withdrawn. The singleton witness
> gives a necessary floor for a constant serving all packings, or the specific
> witness packing; it does not justify rejecting every individual positive-deficit
> fixture with a smaller optimum. C-CUT-001's corresponding acceptance rule is
> pending correction. Other newly proposed claims retain the scope and pending
> obligations in [the independent review](REVIEW_2026-11-14_0308.md).

Status of every mathematical statement the project may rely on. "Accepted" means
proved in this repository or published and checked; nothing here is accepted on the
strength of its author's label.

## Accepted

| Lemma | Status | Closest source | Difference from the source |
| --- | --- | --- | --- |
| Density normalisation: `δ = (4π/3)c`, counting-to-volume, older-convention conversions (`K15-C007`, `K15-C024`) | `PROVED` | CE 2003 §1–2; Hales 2005 Ch. 3 | written out with the boundary term `O(R²)`; the conversions `c = n/8`, `δ = (π/6)n` are this project's (trivial) bookkeeping |
| Two-point bound for all packings, with an explicit periodic approximation (`K15-C002b`) | `AUDITED` (Main, `C037`); **outside check outstanding (`G1`)** — the ledger's own token said `PROPOSED` until this block, an inconsistency now repaired | CE 2003 Thm 3.1 + App. A (Groemer) | no extremal packing assumed; explicit relative loss `12/S`, which cancels in the limit (`BRIDGE_AUDIT.md` §6); no Groemer, no uniformity in `Λ` |
| Count-price hybrid bound (`K15-C003r`) | `PROVED` | CE truncation idea; DLOV14-style counting | the "price is a count, not an integral" form is this project's |
| Contact-shell relaxation is vacuous (`K15-C004`) | `PROVED` | folklore | holds for any set of empty interior; the first version's counterexample was wrong |
| Counting envelope on a shell (`K15-C013`) and its reduction to one Tammes inequality (`K15-C019`) | `PROVED` | Schütte–van der Waerden; Musin–Tarasov Thm 1 | the reduction `cos θ_min = 1 − 2/ρ²` and the ρ-table are this project's |
| Tammes-13 enclosure, hence `n(ρ) ≤ 12` for every `ρ ≤ 2.09` (`K15-C027`, `C060`) | `ACCEPTED WITH SCOPE` (E; re-run by M) | Musin–Tarasov (arXiv:1002.1439v3) | the interval arithmetic is E's; the *identification* of the constant rests on their enumeration |
| Signed defect estimate `θ#(D_θ) ≤ C₁r² + N_A` (`K15-C029r`) | `PROVED` | none (the naive form is false) | new; the withdrawn `C029` assumed `A ≥ 0` |
| Transfer ⇒ negligibility with `C₁ = 3ΦR(R+1)⁵` (`K15-C035`, factor `R` restored) | `PROVED` | Hales 2005 Ch. 5 / Lemma 7.10 (the same content, differently organised) | a two-line estimate instead of the `Q`-system; *not* a new idea (`C067`) |
| Transfer feasibility = Hoffman cut condition (`K15-C044`); compactness needs bounded degree (`C067`) | `PROVED` | Hoffman/Gale flow duality | the application is this project's |
| Transfer graph has degree ≤ 12 at `R ≤ 2.09` (`K15-C054`) | `PROVED` | — | follows from `C013`/`E014` |
| `Φ ≥ 0.0088803` for any transfer on a packing containing the 13-cluster (`K15-C081r`) | `PROVED` | — | singleton cut; the cluster-level `0.0104949` is withdrawn (review 0308) |
| Hales Lemma 3.3 chain (`K15-C043`) | `AUDITED` | Hales 2005 p. 34 | re-derived, no gap |
| No finite completion can verify the pointwise cell inequality (`K15-C036`) | `PROVED` | E's `K15-E003` (same idea, independently) | stated as an obstruction to a route |
| `(Q)` is false (`C069`) | `PROVED` | Hales–McLaughlin (the dodecahedral cell) | the observation that this kills the shortcut is this project's |
| Finite-to-infinite cut/flow theorems with a free boundary (`K15-C093`, `Main/CUT_FLOW_THEOREM.md`) | `PROVED` | Gale–Hoffman / Hoffman cut condition; Tychonoff | the free-boundary formulation is what makes the finite reduction go through; the infinite theorem needs compactness only, local finiteness only for `div` to be a finite sum |
| Cut condition ⟹ Kepler (`K15-C087`) — **one direction only** | `PROVED` (as an implication; statement of the hypothesis is open) | none | the `O(r²)` boundary term needs saturation (`Ω(v) ⊆ B(v,2)`), which `K15-C087` did not state; see §"One-way implications" |
| Every Voronoi cell of a Barlow packing has volume `√32` (`K15-C094`, `Main/BARLOW_CELLS.md`) | `PROVED` | folklore for fcc/hcp; `K15-C091` for the average | uniformity is new: cell = 12-contact cell (covering radius `≤ √2`), exactly two contact configurations up to isometry, both volumes `√32`; stated for the layered class only |
| K33 / K33b certificates: `Δ ≤ 0.779966497784`, `0.779966216777` | `VERIFIED_CROSS` (C's two implementations + Main's, after three repairs) | CE 2003 (0.779747) | not an improvement; a checked component |

## Open

| Gap | What closes it |
| --- | --- |
| `G1` audit of `K15-C002b` (uniformity bookkeeping, `δ = 0` case, Zorn step) | X |
| `G4` specified partition for the cluster criterion | E |
| `G5` analytic averaged cell bound `Σ_U vol Ω ≥ √32|U| − O(|U|^{2/3})` | E/M — **the whole remaining content** (`NEXT_PACKAGE.md`) |
| `G8` independence audit of the two checkers | X |
| `G9` Lean bridge: ball volume and counting-to-volume | local build; `Volume.lean` is `Prop`-only |
| `G10` whether the shell allowance ever pays | C; `C028` explains why it does not at low degree |
| Checker soundness (general) | **suspended** after three repairs (`C049`, `C058`, `C068`); X's audit of `Main/AUDIT_REQUEST_X.md` |

## One-way implications the project relies on

Every implication below is used in one direction only. They are listed together because
three of them have already been read as equivalences at least once in this ledger, and
because a mis-read arrow is the cheapest way to make the whole programme look better than
it is.

**A standing caution about this table (added at `K15-REVIEW-0438-M`).** A one-way arrow is
not a defect in the antecedent. In particular, "the cut condition implies Kepler" does *not*
make the transfer route circular or pointless: it is a **sufficient** condition, and proving a
sufficient condition is how a proof strategy works. The error to avoid is narrow — presenting
the cut form as a *weaker* target than Kepler. An earlier version of this project wrote
"the route is a reorganisation, not a simplification" as though the implication settled its
value; it does not, and that phrasing is withdrawn here and in `C087`/`C100`/`COMPLEXITY.md`.
Whether the route is *practically* simpler is a separate, open question about the cost of
verifying the cuts — not a logical consequence of the implication. A criterion is circular
only if it **assumes** the conclusion, which is a different matter entirely (and which is
exactly the defect found in `C094`'s Lemma 1 and repaired at `C104`).

| Arrow | Proved? | Converse | Consequence of a mis-read |
| --- | --- | --- | --- |
| `(T')` ⟹ cut condition (`C080`) | yes (`Φ|δ⁺| ≥ 0`) | **no** — the cut form is strictly weaker whenever `δ⁺ ≠ ∅` | reading it as an equivalence would make the cut form a restatement of `(T')` |
| cut condition ⟹ `δ ≤ π/√18` (`C087`) | yes | **no** — nothing in the density bound gives a local cut inequality | the only error this direction forbids is reading the cut form as a *weakening* of Kepler. It does **not** make the route circular, and it does **not** make it worthless: a sufficient condition that implies the target is exactly what a proof strategy is, and a stronger statement can perfectly well be *simpler* to prove. See the correction recorded under `C087` |
| `b ≡ 0` on Barlow packings (`C094`) | yes | **no** — `b ≡ 0` forces densest, but "densest ⟹ Barlow" is the (open) classification of densest packings | reading it as a characterisation would silently assume the equality case of Kepler |
| 12 contacts ⟹ layered (`C094`'s scope note) | **not verified here** | not used | the theorem is stated for the layered class; a non-layered 12-contact packing is outside it |
| transfer exists ⟺ cut condition (`C044`, `C093`) | yes, **both** ways | — | this is the one genuine equivalence, and it is pure graph theory: all the geometry is in *verifying* the cuts |

## What is *not* claimed

No new density bound. No improvement over `0.779747` (2-point), `0.770271`
(3-point) or `0.754697` (dodecahedral). No claim that any route is closed — the
shell, two-point and transfer routes are "no gain found in the tested scope" or
"not verifiable by computation", not impossible. No compact reduction exists *for the
cut formulation as stated* (`C088`); that is not a claim about every reformulation.
`b ≡ 0` holds on Barlow packings (`C094`), which does **not** characterise them.
