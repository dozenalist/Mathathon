# Accepted lemmas, open gaps, and closest sources — the one-page account

Status of every mathematical statement the project may rely on. "Accepted" means
proved in this repository or published and checked; nothing here is accepted on the
strength of its author's label.

## Accepted

| Lemma | Status | Closest source | Difference from the source |
| --- | --- | --- | --- |
| Density normalisation: `δ = (4π/3)c`, counting-to-volume, older-convention conversions (`K15-C007`, `K15-C024`) | `PROVED` | CE 2003 §1–2; Hales 2005 Ch. 3 | written out with the boundary term `O(R²)`; the conversions `c = n/8`, `δ = (π/6)n` are this project's (trivial) bookkeeping |
| Two-point bound for all packings, with an explicit periodic approximation (`K15-C002b`) | `PROVED` (audited in `C037`) | CE 2003 Thm 3.1 + App. A (Groemer) | no extremal packing assumed; explicit losses `O(S/R)+O(1/S)`; see `Main/BRIDGE_AUDIT.md` |
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

## What is *not* claimed

No new density bound. No improvement over `0.779747` (2-point), `0.770271`
(3-point) or `0.754697` (dodecahedral). No claim that any route is closed — the
shell, two-point and transfer routes are "no gain found in the tested scope" or
"not verifiable by computation", not impossible.
