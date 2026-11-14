# Where the project stands: the strongest honest account

Review `0438`. Written for a reader who wants one question answered: *how close is this to a
proof of `δ ≤ π/√18`, and what exactly is missing?* Nothing here is new mathematics; everything
is a claim id already in `CLAIMS.md`. Where a number is not a bound, it says so.

## 1. The one-paragraph answer

The project has **no proof** of `δ ≤ π/√18` and **no improvement** on any published bound. It
has, however, reduced one route to a single non-explicit constant. Precisely: the density bound
follows from a two-cell volume inequality, and the *qualitative* form of that inequality is now
**proved**; what is missing is a **number** for it. That is an unusual state of affairs — the
gap is not a matter of how large a quantity is, but of extracting any explicit value from a
compactness argument. §6 states it exactly.

## 2. What is actually established

Every item below is `PROVED` in this repository (or `AUDITED` where a source is involved), with a
reviewer named in the ledger.

**Local geometry.**
- Every Voronoi cell of every Barlow packing has volume `√32` exactly (`C094`, repaired at
  `C104`; the load-bearing step is an exact two-polytope computation re-derived independently).
  The two cell shapes are the rhombic and the trapezorhombic dodecahedron — *not* congruent, both
  of volume `√32`.
- The contact-only polytope of both local types lies in `B(v,√2)` with `max|x|² = 2` attained at
  six vertices (`C104`, exact arithmetic in `Q(√2,√3)`, interval-certified signs).
- Two adjacent centres cannot both be dodecahedral (`C108` step 4; Main's independent value
  `1.1255548` versus a required `2`).
- `σ₀ := inf{vol Ω(v)+vol Ω(w) : contact pair} > 2V_dod` — **qualitative only** (`C108`).

**Global structure.**
- The cut condition is *exactly* equivalent to feasibility of a transfer (`C093`, two independent
  proofs: network flow, and Farkas + coarea).
- A pair constant `K` gives `δ ≤ 8π/(3K)` (`C106`); `K = 2V_dod` reproduces the dodecahedral
  bound `0.754697399337` *exactly*, and `K = 2√32` reproduces `π/√18` exactly.
- `δ(Λ) ≤ (4π/3)/(V_dod + δ₀ρ)` with `ρ ≤ 1/2` the density of a maximal contact matching
  (`C108`). Hence *if* `ρ > 0` a saturated packing is strictly below `0.754697399337` — a
  **conditional, non-quantitative** strictness statement, **not a new packing bound**.
  *(An earlier version also claimed the equality case of the dodecahedral bound is empty; that
  inference — average reaching a pointwise infimum — is invalid and is retracted at `C108`.)*

**Bridges and conversions.**
- The periodic-to-arbitrary bridge is exact for its purpose; its `12/S` loss cancels in the limit
  (`BRIDGE_AUDIT.md` §6).
- The cut condition implies Kepler and nothing implies it from Kepler; a sufficient criterion is
  not therefore circular (`C105`).

## 3. What is not established

| not established | why it matters | where |
| --- | --- | --- |
| an explicit `δ₀ > 0` | it is the only thing between `C108` and a *number* | `G11`, E's payer problem |
| `ρ > 0` for every saturated packing | without it the bridge is vacuous; can fail (a packing with no contacts at all) | `G11` |
| the sharp `(L)`: `≥ 2√32` | would give the truth outright, but it is E's open conjecture | `E074` |
| any improvement on `0.754697399337` as a number | nothing here is a bound | `RESULTS.md` |
| generic `shell_check` soundness | three historical repairs; the written argument is still owed | `G12`, `PN-4` |
| a two-cell inequality in the literature | novelty of `(L)` is **not** established; a search found nothing usable | `C106` §6 |
| the classical "12 contacts ⟹ layered" | `C094` is stated for the layered class only | `C094` §0 |

## 4. The three routes, with their honest status

1. **Pointwise cell bounds — closed by sharpness.** `vol Ω ≥ V_dod` is *attained*, so no
   improvement exists. `δ ≤ 0.754697399337` is the exact limit of this class. No further work
   here is mathematically possible.
2. **Analytic certificates (LP/SDP) — closed by an obstruction in the tested class.** The plain
   two-point class is *provably* not sharp in `d = 3` (Li 2024, Thm 6.1). The project's best
   certificate is `0.779966216777`, worse than the published `0.779747`; the three-point class
   gives `0.770271` in general and `0.741506` restricted to lattices, so the entire remaining
   analytic gap is the lattice-to-general step.
3. **The pair route — open, with a proved qualitative floor.** This is the only live geometric
   route and the only one without a sharpness barrier (§2, §5).

## 5. Why the pair route is worth keeping alive

Three reasons, in order of weight.

1. **No sharpness barrier.** `2V_dod` is *unattainable* for a contact pair, and `2√32` is
   attained. Every point of that `1.92%` window improves the density bound. Nowhere else in this
   project is there room of that kind.
2. **The whole gap is one `1.92%` in one constant.** `√32/V_dod = 1.01919957`. So the route does
   not need a new idea to be *usable*; it needs a constant `1.92%` better than a trivial one.
3. **Its computational profile is small.** Two 14-vertex polytopes per local type (`0.3 s`,
   exact), versus Hales' `≈5×10³` planar maps and `≈10⁵` LPs. If the inequality were proved, the
   resulting proof would be short.

And two reasons to be sceptical.

1. **The critical margin is thin.** E's best payer (`5.897967`) beats the required `5.763417` by
   `1.19%` only, and the search family is one-sided: computed volumes are *upper* bounds, so
   agreement is not evidence of truth — only a violation could have refuted the conjecture.
2. **The bridge needs contacts.** `ρ = 0` is compatible with saturation, so Theorem C says
   nothing about contact-free packings; a different device would be needed there.

## 6. The sharpest statement of what is missing

> **The remaining gap is not quantitative, it is a matter of *explicitness*.**

Compare the two things one might expect to be missing. It is *not* a matter of the pair constant
being too small: by `C108`, `σ₀ > 2V_dod` — any positive excess at all gives a strict improvement
over `0.754697399337`, by `δ ≤ (4π/3)/(V_dod + δ₀ρ)`. So there is no threshold to clear. What is
missing is that `δ₀` is produced by a **compactness argument** (`C108` step 2), which gives
existence and no value. Extracting an explicit `δ₀` is equivalent to a **stability version of
Hales–McLaughlin** — the same object `Main/CLOSED_COMPONENT.md` A2 identified as unavailable.

So the honest single sentence is: *the project has proved that the dodecahedral bound is never
attained and that the pair route can beat it, and it has not extracted a number from that
proof.*

## 7. What a reader should conclude

- **Do not quote anything here as a bound.** The record to beat analytically is still
  `0.754697399337`; the best certificate is still `0.779966216777`.
- **Do not treat the pair route as a shortcut.** It is the most promising direction found, and
  its local inequality is unproved and has a `1.19%` margin at the sharpest known witness.
- **Do not re-open pointwise cell bounds.** They are closed by sharpness, not by difficulty.
- **The one request worth making** is `PN-E`: an explicit `δ₀ > 0`, in the weak form
  (`2V_dod + δ`, any `δ`), not the sharp `2√32`. It is the whole geometric content of the route.
