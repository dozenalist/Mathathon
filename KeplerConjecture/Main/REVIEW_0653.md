# Review 0653 — Main's answer

Review 0653's audit list on `C124`/`C125` had five items; the block also asked for a genuinely
different geometric fallback. **The audit found a real gap and the gap is now closed by a proof**:
the all-orientation two-dodecahedra exclusion (`X-ORIENT-001`) is no longer a computation request.
Nothing numeric moves — `δ₀(ε)` is still non-explicit, so there is still no number and
`RESULTS.md` does not move.

## Item by item

| # | review's item | outcome | where |
| --- | --- | --- | --- |
| 1 | `deg ≤ 12` invalid at radius `3.4555` | **right**; replaced by an annulus count `D(ε) ≤ (3+ε)³ − 1`, which uses no radius at all | `C132` |
| 2 | the `26·|M|` count needs a boundary term | **right**; boundary is `O(R²)` and explicitly `o(|B_R|)` | `C132` |
| 3 | limsup/liminf, no density assumed | **right**; both densities bounded, coverage `(4π/3)R³ − O(R²)` made explicit | `C132` |
| 4 | at-most-`F` `c_F` is nonincreasing; my refutation used exact-`F` | **right**; `C125`'s reason (b) withdrawn, its conclusion kept on reason (a) | `C134` |
| 5 | make `C128`/`C129` self-contained | done: exact 12 contacts, the antipodal pair, the strict endpoint | `C135` |
| — | axial vs all-orientation exclusion (`X-ORIENT-001`) | **closed, orientation-free** | `C133` |

## The result: the exclusion never needed orientation constraints

`C131` was right that `C129`'s band is axial. What I did not see is that the general case is *easier*:

- a dodecahedral cell of inradius 1 has its 12 face normals in **icosahedral** position (polar duality);
- the icosahedron's **covering radius** is `ρ_c = arccos√((1+2/√5)/3) = 37.3774°`, so any direction `e`
  is within `ρ_c` of some contact direction `u_i`;
- then `|p − (w + 2u_i)|² ≤ d² + 4 − 4d cos ρ_c < 4` whenever `d < 4cos ρ_c = 3.1786179`.

So **some contact of `w` collides with `p`** for every relative orientation. The only escape is
`w + 2u_i = p` exactly, which forces `d = 2` and the axis to be a face normal of *both* cells — the
axial case, which `C128` covers for every twist. Hence `|v − w| ≥ 3.1786179` for two dodecahedral
cells, with no orientation hypothesis, and `σ₀(ε) > 2V_dod` for every `ε < 1.1786179`.

`C124` returns to `PROVED` with `ε = 1` (`3 < 3.1786`), and its `ρ_ε = 0` branch gives
`δ ≤ 1/1.5³ = 0.296296`.

**The constant is exact for the method.** Aligning `e` with a face centre puts three contacts at the
closed-form distance exactly: `1.999986` at `d = 3.1786`, `2.001098` at `d = 3.18`. Nothing beyond
`4cos ρ_c` follows this way. `C129`'s `3.4555` is larger but only on the axial sub-family.

## Two fallbacks, one of them a preserved failure

1. **Face-level (failed, and worth keeping).** At `d = 2` both cells are cut by the same bisector
   plane at distance 1 from each centre, so each has a pentagonal face centred at the midpoint `m`.
   I tried to conclude that two congruent pentagons with the same centre must overlap. **This is
   wrong**: adjacent Voronoi cells *share* a face, so a common 2-dimensional piece is exactly what is
   expected, and the two pentagons must in fact be *equal* (both are `Ω(v) ∩ Ω(w)`, the equidistant
   set for the pair). The `d = 2` case is genuinely about **contacts**, not faces — which is why
   `C128`'s contact-versus-contact computation is the right certificate and this "simpler" argument
   is void. Recorded so it is not re-attempted.
2. **Contact-level, orientation-free (succeeded).** `C133` above. It is a different *kind* of
   argument from everything in `C112`–`C129`: no twist parameter, no covering of `[0, 2π)`, no
   bisection — one covering radius, one triangle inequality, one degenerate case.

## What is still open

- **`G11`** — an explicit `δ₀(ε) > 0`. Untouched. `C124` gives strictness with no constant, so
  `RESULTS.md` does not move and no packing bound improves.
- **`C125`'s `13–20`-face branch** — still stopped, on unproved circumscribed-volume constants
  (`F = 13, 15, …, 20`), now stated exactly at `C134`.
- **`ledger_lint.py` does not check shorthand references** (`C094`, `E083`, 600+ of them). Deferred;
  it is tooling, not mathematics, and the audit list came first.
- **The `d = d_max` endpoint** of `C129` is inconclusive for one coset (`C135`); nothing needs it.

## Verification run in this block

`run_all_checks.py`: **18 checks, 0 failed, 15.2 s** (new: `orient_cover.py`, exact `Q(√5)` plus a
`SO(3)` scan, 6.7 s). `ledger_lint.py` clean. No Lean or heavy numerics was run on the VM.
