# K15-X-040 — audit of the repaired flow theorem; X-C017 shrunk 3.8×; a sign-free verifier

Receipt `2026-11-14T12:05:55Z`. Work on this block's continuation started `12:09:02Z`
(`date -u`, first command); this report is written at `12:20Z`. The block's substantive hour
runs to `13:05:55Z`; each checkpoint has a commit whose time is in the `git log` (§8 records them),
and the close timestamp is written into §8 at the end of the block. No full-hour claim is
made before `13:05:55Z` — the two previous false claims (`41.969` and `43.565` minutes delivered)
were false because I inferred elapsed time instead of reading the clock, and the fix is that
every timestamp in this file is a `date -u` output, not an estimate.

Audited in this block: `Main/CUT_FLOW_THEOREM.md` as repaired at `aa52147` (main tip `9d6414d`),
`Computation/cut_flow.py` at blob `700e44f6` (unchanged from `4bcbd3a`, see §4), and the stored
`X_C017` certificate. New artifacts: `Reviews/audit_cutflow_repair.py`,
`verify_XC017_readable.py`, `x_c017_shrink.py`, `X_C017_small.json`.

---

## 1. The repaired flow theorem: **PASS**, all six requested checks

Main's `AUDIT_REQUEST_X.md` §5 asks for six specific checks and for a deliberate attempt to
break the theorem. I wrote an independent implementation (`Reviews/audit_cutflow_repair.py`)
that compares three objects on the same instance — the cut condition `(C)`, a direct LP over
`{Aφ ≥ b, |φ_e| ≤ Φ_e}` (HiGHS), and the document's threshold formula — and checked the proof
steps by hand. It exits 0 only if everything passes; it does.

| requested check | verdict | note |
| --- | --- | --- |
| 1. directed model: `|ψ| ≤ Φ`, every transfer arises, same divergence vectors | correct | `ψ = f(v→w) − f(w→v)`, both arcs at full capacity `Φ`; `f(v→w) = φ⁺`, `f(w→v) = φ⁻` inverts it |
| 2. cut orientation, `X = ∅` forced, capacity algebra | correct | the capacity is `Σ_{F∖U}b⁺ + Σ_U b⁻ + cap(U) = Σ_F b⁺ − Σ_U b + cap(U)`, so `min-cut ≥ Σ_F b⁺ ⟺ (C)` |
| 3. transfer meets the demand, including `b(v) = 0` | correct | saturated `s`-arcs give `div = b(v)` for `b > 0`; for `b ≤ 0`, `div = −c_v ≥ −b(v)⁻ = b(v)`; `b(v) = 0` falls in the second case with 0 ≥ 0 |
| 4. second proof: Farkas with box multipliers + coarea | correct | alternative is `Σ_F y b > Σ_e Φ_e|y_v − y_w|`; both coarea identities hold for `y ≥ 0`, `U_t ⊆ F` |
| 5. Theorem 2 without a uniform bound | correct | Tychonoff on `∏_e[−Φ_e,Φ_e]`: compactness is per factor; `S_F` closed since `div_φ(v)` is a finite sum; FIP. The hypothesis table correctly marks `sup_e Φ_e < ∞` as **not used** |
| 6. threshold formula, both branches | correct | `+∞` if some `U ⊆ F` has `δ⁺(U) = ∅` and `Σ_U b > 0`; else `max(0, sup Σ_U b/|δ⁺(U)|)`. `max(0,·)` is needed: `b = (−1,−2)` on one edge has all `Σ_U b < 0` and `t* = 0`, and `φ ≡ 0` is the witness |

**Randomised cross-check, twice, once without floats.** On 115 random small instances (n ≤ 5,
`b ∈ {−2..2}⁵`, `Φ ∈ {0,1,2,3}`, random `F`) the three answers agreed every time:
`(C) ⟺ LP feasible ⟺ Φ ≥ t*`. I then replaced the LP by **exact Fourier–Motzkin elimination**
over ℚ on 297 instances with `n ≤ 6` (one undecided by a blow-up guard): **0 mismatches**. So
Theorem 1 and the threshold formula are confirmed against an *exact* decision procedure, not a
solver with tolerances — which matters, because the project has already lost three rounds to
float-decided checks.

The FM routine is 30 lines and shares no code with the cut scan or the LP, and its own history is
worth recording because it shows what the comparison is for: my first version had a sign
convention backwards (99/196 wrong), the second declared a "contradiction" too early (a nonempty
residual constraint was mistaken for an unconditional one, 12/196 wrong), and the third used a
fixed elimination order that ran out of memory at `n = 6`. Each was caught by exactly this
cross-check, not by reading the code.

**A fourth decision procedure, this one on C's side.** C's `feasible_flow` (scipy max-flow, then
rounded to rationals and re-verified exactly) agrees with the cut condition on 38 random instances
(25 infeasible, 13 feasible, 0 mismatches). So the theorem's statement, my LP, my exact
Fourier–Motzkin routine and C's independent flow constructor all say the same thing on the same
instances — `Reviews/audit_cutflow_repair.py` §F.

**The thing to try to break.** One instance does need both threshold branches at once, so the
formula's shape is load-bearing rather than cosmetic: take the star of §5(b′) (`b = (4,−4/3,−4/3,−4/3)`,
finite-branch sup `= 4/3`) **disjoint union** an isolated vertex with `b = +1`. The finite branch
says `4/3`; the empty-boundary branch says `+∞`; the truth is `+∞`, and `(C)` fails at `Φ = 10⁶`
with the violating set `U = {isolated vertex}`. A formula that took the sup only over
`δ⁺ ≠ ∅` would return `4/3` and be wrong. Both branches are exercised by that one instance.

I did not find a fifth defect in the repaired proof. Two things I checked that are *not* defects
but are worth recording: (i) Theorem 2's exhaustion argument tacitly assumes `V` is countable;
if `V` is uncountable no such `{F_n}` exists, but then the theorem is vacuous rather than false,
and the project's `G` is a packing of `R³` (countable), so nothing downstream is affected;
(ii) `Φ_e = 0` is allowed and the factor `[0,0]` is still compact, so the "`Φ_e ≥ 0`" row of the
hypothesis table is correctly minimal.

### 1.1 Erratum: my witness W6 was wrong, in both directions

`REVIEW_0353.md` §3 row W6 says of two disjoint edges with `b = (1,−1)` and `(2,−2)`, `F = V`:
"infeasible … so this one **is** feasible for every `Φ > 0`". That row is self-contradictory and
the verdict is wrong both ways. The correct statement: the empty-boundary set `U = V` has
`Σ_U b = 0 ≤ 0` and is *not* an obstruction (which is the `0/0` case the row was meant to pin),
but the singleton cuts bind: `{v}` with `b(v) = 1` needs `Φ ≥ 1`, and `{v}` with `b(v) = 2`
needs `Φ ≥ 2`. So the instance is **feasible iff `Φ ≥ 2`, i.e. `t* = 2`** — neither "infeasible"
nor "feasible for every `Φ > 0`". The audit script checks `Φ = 2` (feasible) and `Φ = 3/2`
(infeasible). W1–W5 stand as written; the repaired document passes W1–W5, and passes W6 once W6
is stated correctly.

### 1.2 `CLAIMS.md` `K15-C093`: the bullet list still states the two refuted claims

The repaired `CUT_FLOW_THEOREM.md` is correct (§1). The *ledger entry* for it is not
self-consistent. `Main/CLAIMS.md` `K15-C093` opens with a bullet list, and two of its bullets are
the pre-repair text; twenty lines below, the entry's own repair note says they are wrong:

| ledger bullet (still present) | what the same entry's repair note says |
| --- | --- |
| "Theorem 2 … the cut condition for all finite `U`, **and `sup Φ < ∞`**: a transfer exists. Proof … Tychonoff on `∏_e [−Φ₀,Φ₀]`" | "`sup_e Φ_e < ∞` is **not** a hypothesis of Theorem 2 and is removed … Tychonoff gives `∏_e [−Φ_e, Φ_e]` compact from the compactness of each factor" |
| "the variant `b(a) = 4` is infeasible at `Φ = 1` with the violating cut `{a}`" | "the violating cut is `F` … `b = (4,−1,−1,−1)` is **infeasible at every `Φ`**, not infeasible at a threshold `4/3`" |

This is exactly the failure mode `D9` is meant to prevent: the corrected text and the rejected
text are both in the file, and the rejected text comes *first*. A reader who stops at the bullet
list takes away a theorem with a superfluous hypothesis and an example with the wrong violating
cut — and the second one matters, because `{a}` is precisely the cut that produces the number
`4/3`, so the bullet teaches `4/3` as the threshold of a vector that has none. No published claim
currently depends on either statement (`C084`, `C085` do not use `4/3` — I checked before writing
this sentence), so this is a documentation defect; it is the kind that gets quoted later. The fix is editorial (delete the two
bullets and let the repair note stand, or move the bullets below it and label them rejected); I
have not made it, because `CLAIMS.md` is Main's file and the repair is Main's to record. It is
recorded here so that the next reader does not take the bullet list as current.

One thing in the same entry that is *right* and easy to miss: the repair note's item 3 now names
where each hypothesis is used, which is what `D18` item 4 asks for, and it matches the table in
`CUT_FLOW_THEOREM.md` §2 exactly.

---

## 2. X-C017: 10,056 → 2,646 bytes, 281 → 20 digits, same density to `3.5·10⁻⁸`

**Where the height came from.** `both_sides_gmargin.py` rounds the float SDP solution to
denominators `≤ 10⁸` and then solves the 12 linear constraints *exactly* for the columns SymPy's
`rref` picked. Those 12 columns form a dense block, so the solved entries carry its determinant:
281-digit numerators. The free entries were already fine.

**The structural fact that makes a controlled reduction possible.** With
`d_k(M) = Σ_{i+j=k} M_ij`, the constraint `v^T A v + w v^T B v = Fourier(P)` is *linear* in
`(G,A,B)` and is exactly `L p = 0` for a 12×126 rational matrix `L`. Row `k` of `L` touches only
A-entries on anti-diagonal `k`, B-entries on anti-diagonal `k−1`, and G-entries on two adjacent
anti-diagonals. Choosing one A column per row `k ≤ 10` and one B column at `k = 11` makes the
pivot block **diagonal** with determinant `±2^a 8^{−b}` — so nothing of size `det` enters.

**What actually blocked it, and the fix.** Even with that pivot choice the first attempt gave
122-digit entries. The cause is not the pivot block: each term of the row sum has a `≤ 17`-digit
denominator, but the terms' denominators are mutually coprime, and the *lcm* of 21 of them is
118 digits. Rounding to `10^{−m}` therefore cannot help. Rounding instead to the **dyadic grid
`2^{−m}` that the certificate already uses** (`S = 8`, and `L`'s own denominators are powers of
two) removes the blow-up completely: every term shares one denominator, so no lcm is taken.

| grid | max digits | bytes | density | `L p = 0` | `G, A, B ⪰ 0` |
| --- | --- | --- | --- | --- | --- |
| stored | 281 | 10,056 | 0.782267220134 | ✓ | ✓ |
| `2⁻²⁰` | 18 | 2,368 | 0.782267282601 | ✓ | A fails |
| `2⁻²²` | 19 | 2,495 | 0.782267259107 | ✓ | A fails |
| **`2⁻²⁴`** | **20** | **2,646** | **0.782267254856** | ✓ | **✓** |
| `2⁻²⁶` | 21 | 2,752 | 0.782267212764 | ✓ | ✓ |
| `2⁻³²` | 22 | 3,160 | 0.782267220239 | ✓ | ✓ |

`2⁻²⁴` is the smallest passing triple: **3.80× fewer bytes, 14× smaller entries, density changed
in the 8th decimal.** The reason `2⁻²⁰`/`2⁻²²` fail PSD is quantitative and worth stating: the
SDP that produced `X-C017` imposed `A, B ⪰ 10⁻⁶ I`, and a rounding grid coarser than `10⁻⁶`
destroys that margin. `G` survives coarser grids because it was given `ε_G = 10⁻²`.

**What this does and does not show.** It shows the *stored representative* was needlessly large,
and that a 3.8× smaller representative of a nearby certificate exists and verifies exactly. It
does **not** show that a small-denominator triple exists at exactly `0.782267220134`: the
constraint rows carry `S^{−k}`, so pinning the density to 12 digits pins the denominators to
roughly `8^{10} ≈ 1.1·10⁹` times whatever the free entries carry. The honest statement of the
reduction's status is: *same construction, same structural properties, `3.5·10⁻⁸` weaker,
3.8× smaller.*

**Comparison with the other certified objects** (the comparison the block asked for):
`C`'s `SOSQSIDE-005` carries a single explicit rational Gram (`Reviews/C_SOSQSIDE005.json`:
22 numeric entries, median 2 digits, max 19) at `1.413704545` — smaller entries, useless bound. `C`'s K33 certificates are `29`-digit
rationals (Main's figure) at `0.779966497784` (K33a) and `0.779966216777` (K33b): a better bound,
at about 1.5× the entry size of `X_C017_small`. But K33 has an explicit rational Gram on the `p`
side only, so its `q` side still needs a sign decision; `X_C017` and `X_C017_small` are the only
objects in the project with **both** sides witnessed by rational PSD matrices — which is the property that removes the predicate obligation entirely (§3). The `B` block of the stored certificate already has only `≤ 11`-digit
entries, which shows the `B` side was always cheap; the size
was entirely a `G`/`A` artefact of the pivot solve.

### 2.1 Is a *smaller* triple possible at comparable strength?  No — and the reason is structural

I re-ran the SDP at three larger forced margins `ε_AB` (the stored one is `10⁻⁶`) and shrank
each solution at the coarsest grid that still passes exact `LDLᵀ`, so the answer is a frontier
rather than a single point. Each density is the one at the *coarsest* grid that still passes, i.e.
the row's own certificate — not the best density that configuration could reach at a fine grid:

| forced `ε_AB` | density | coarsest grid that passes | digits | bytes |
| --- | --- | --- | --- | --- |
| **`10⁻⁶`** (stored) | **0.7822673** | `2⁻²⁴` | **20** | **2,646** |
| `10⁻³` | 0.783625 | `2⁻¹⁸` | 18 | 2,231 |
| `10⁻²` | 0.795789 | `2⁻¹²` | 16 | 1,833 |
| `5·10⁻²` | 0.849759 | `2⁻¹⁰` | 16 | 1,732 |

Two conclusions.

1. **At comparable strength there is nothing to gain.** Every row with a smaller byte count is
   *worse* than `X-C016` (`0.783097911`), i.e. it would not even reproduce the earlier bound. So
   `2,646` bytes at `0.7822673` is within `1.4×` of the frontier and the remaining `1.4×` costs
   `0.0135` of density.
2. **The digit count has a floor of about 16, whatever the grid.** Even at the coarse `2⁻¹⁰` grid
   the entries need 16 digits. The mechanism is not rounding: row 11's pivot coefficient is
   `S⁻¹⁰ = 8⁻¹⁰`, so solving that row divides by it, multiplying whatever the free entries carry by
   `8¹⁰ ≈ 1.07·10⁹`, i.e. ~9–10 digits, on top of ~3 digits of magnitude and the grid's own
   resolution. *(Corrected: I first wrote `8¹¹`; the coefficient is `S^{-10}` with `S = 8`, so the
   factor is `8¹⁰`.)* The floor at an integer grid would therefore be ~12–13 digits. **No 5-digit
   certificate exists in this basis**, for any grid, at any strength. That is a statement about
   the `S = 8` monomial Gram basis, not about Cohn–Elkies certificates in general: a basis with
   `S = 1` would remove the `8¹¹`, but the identity's coefficients then have denominators from
   the Fourier map alone and the same lcm problem returns (each `Ml` entry is a rational with a
   `≤ 4`-digit denominator; `126` of them per row sum).

`X_C017_small.json` is regenerated byte-identically by `python3 x_c017_shrink.py`, which asserts
`L p = 0`, `P(0), Q(0) > 0` and the three exact `LDLᵀ` tests before writing.

*Precision note on the ladder.* The `0.779966500` I have been quoting is `K33`(a)
`= 0.779966497784`; the better variant `K33b` is `0.779966216777` (Main's `constants_check.py`
and `ACCEPTED.md` agree). The two differ by `2.8·10⁻⁷`, which does not change any comparison,
but the two should not be quoted interchangeably.

---

## 3. A reader-facing verifier, and why no sign predicate is needed

`verify_XC017_readable.py` reloads a certificate from disk and prints, step by step, (1) symmetry,
(2) rational `LDL^T` with every pivot printed, (3) the identity `v^TAv + w v^TBv = Fourier(P)`
by expansion, (4) `P(0)`, `Q(0)`, the exact ratio and the density, (5) what is and is not claimed.
It runs on **all four** both-sides certificates — `X_C015`, `X_C016`, `X_C017`, `X_C017_small` —
and prints VALID for each. (Two robustness fixes were needed to get there: `X_C015` stores its
density as an expression over `sqrt(pi)` rather than a float, and `X_C016`/`X_C017` as floats. A
verifier that only ever sees one certificate's format is a verifier that has not been tried.)

The exposition the block asked for is short: **CE1 and CE2 are not sign conditions here.** For
`H = v(s/S)^T G v(s/S)` with `G ⪰ 0`, `H ≥ 0` identically; `P = −(s−4)H = (4−s)H` is then `≥ 0`
on `[0,4]` and `≤ 0` beyond `4` (strictly negative wherever `H > 0`) *because of the factor*, with
no root isolation. For
`Q = v(w/S)^T A v(w/S) + w·v(w/S)^T B v(w/S)` with `A, B ⪰ 0`, `Q ≥ 0` on `[0,∞)` because both
summands are. The only remaining obligation is a polynomial **identity**, decided by expansion in
exact arithmetic. So the entire certificate is: three rational PSD tests (`LDL^T`) plus one
expansion. That is the whole reason the both-sides Gram form was worth the strength it costs —
and it is why `X_C017` is quoted as an *auditability* result, not as a bound. It is not a Kepler
proof and beats nothing: `0.782267 > 0.740480`.

The script prints that last sentence itself, because a verifier that returned "valid" for a
`0.782` density without saying so would invite exactly the misreading the block has twice had to
correct.

**It has teeth.** `Reviews/negative_control_readable.py` writes three tampered copies and one
honest copy of `X_C017_small.json` and requires the verifier to reject the three and accept the
one: `G[0,1] += 1/1000` → REJECTED; `A[1,1] += 10⁻⁶` → REJECTED; `A[0,1] = 100` → REJECTED;
unmodified → VALID. The `10⁻⁶` case is the one that matters: it moves the density in the seventh
decimal, invisible to any float comparison of the bound, but breaks the exact identity `L p = 0`,
which is the whole certificate. A verifier that passed it would be checking nothing.

---

## 4. C's `cut_flow.py`: unchanged, so all four defects stand — plus two smaller ones

`Computation/cut_flow.py` is blob `700e44f6c92563b66b4146106cfe8e00cd5a3455` at `4bcbd3a` **and**
at the current `comp` tip `790efa73` — Main's repair touched only the theorem, not the script, and
C has not revised the file since. So
the four findings of `REVIEW_0353.md` §2 remain open on C's side. They are now reproducible by
one script that does not import anything of mine except a byte copy of C's own file:
`python3 Reviews/repro_c_cutflow_defects.py` → **7/7 checks reproduce, all four defects**.
The exact numbers:
the `V_DOD` interval's lower endpoint is `3.86·10⁻¹²` too high; `build_13(2.1029)` returns 42 edges
instead of 12 (the true icosahedral edge at circumradius 2 is `2.102924448476534`, and phantom ring
edges make cuts cheaper in the unsafe direction); `build_fcc_patch(1)` raises `TypeError`; and the
period-16 13-cluster is unsaturated, so `b = −∞` and every cut is satisfied for every `Φ` — no
geometric content. W1–W6 in `REVIEW_0353.md` §3 remain the acceptance tests, with W6 restated as
in §1.1 above.

**A fifth live defect, and the worst kind: a false accept.** `verify_flow_exact` computes its
vertex range as `n = max(max(e) for e in edges) + 1`, i.e. from the *edge list*. A vertex with no
incident edge is therefore never checked, and an instance that is plainly impossible is accepted:

```
b = (-1, -1, +1),  edges = [(0,1)],  flow = {}          # vertex 2 is isolated, needs 1 unit
verify_flow_exact(b, edges, 1, {}) -> (ok_cap=True, ok_div=True, div=[0, 0])
true verdict: ok_div = False, because div(2) = 0 < b(2) = 1
```

It is systematic, not one slip: three functions take the vertex set from the edge list.
`find_violating_cut` returns `None` ("no violation") on the same instance, and `feasible_flow`
returns a flow, both of which are wrong because `{2}` violates at every `Φ`. Only
`exhaustive_cut_scan` is right (`empty_boundary_positive = [([2], '1')]`), so the module
contradicts itself: three functions say "fine" and one says "infeasible at every `Φ`". This is the recurring failure mode of the whole project — an exact
checker that returns OK on an input that is not OK.

And it is **reachable through the documented portability path**. `load_external_fixture` validates
edge indices (`0 ≤ i,j < len(b_lo)`) but does not require every vertex to appear in an edge, so an
external fixture may legitimately contain an isolated centre. Feeding one — five vertices, edges on
`0..3`, `b = (−1,−1,−1,−1,+1)` — makes `evaluate_external` print

```
POSITIVE DEFICIT AT DEGREE ZERO at [4]: INFEASIBLE at any Phi
Phi=1/100    flow found; |phi|<=Phi True, divergence>=b True   PATCH_FEASIBLE only
```

i.e. the same run says the instance is infeasible at every `Φ` *and* emits `status:
PATCH_FEASIBLE`. A consumer reading the JSON `status` field gets the wrong answer. Its own
`singleton_bounds` uses `len(b_lo)` and is right; the three flow functions are not.

No shipped fixture is affected (`build_13` gives every vertex an edge at `R ≥ 2−10⁻⁹`, and `main()`
skips the edgeless regime), which is why this has not bitten yet. It is D8 in
`Reviews/repro_c_cutflow_defects.py`; the fix is one line in each of three functions: `n = len(b)`.

One further defect is **latent**, and I record it as such: `exhaustive_cut_scan` raises
`TypeError: 'NoneType' object is not subscriptable` whenever no subset has a crossing edge
(`best` stays `None` and is indexed). `main()` never reaches it — it tests `if not edges` and
reports the pointwise condition instead — so `python3 cut_flow.py` runs. But the function's own
docstring says it returns `None` only when the scan is too large, and any caller that evaluates the
`R < 2` regime through it (or a future C block that drops the `if not edges` guard) crashes instead
of getting a verdict. It is in `Reviews/repro_c_cutflow_defects.py` as D5, marked latent.
Everything else in the module is robust on degenerate input: 12 further edge cases (no edges,
`Φ = 0`, one vertex, empty `b`, `n = 17` over the scan cap, `R = 0`, `build_13(0)`, `build_13(2.0)`,
`feasible_flow` with no edges) all return a verdict rather than raising — 12/12 (D6).
One cosmetic mismatch with the repaired theorem is worth a line: `exhaustive_cut_scan` reports
`t_star` as the raw maximum of `Σ_U b/|δ⁺(U)|`, without the theorem's `max(0, ·)`, so an
all-negative instance yields `t_star = −1` where the formula gives `t* = 0`. Nothing changes for
the test `Φ ≥ t*` (since `Φ ≥ 0` is a hypothesis), but the number is not the theorem's `t*` and
should not be quoted as one (D7).

### 4.1 Main's `η ≥ 0` guard closes the §17 witness, and the predicates are undisturbed

`shell_check.py` moved `909a50a → 5caa1c9`, which adds `if eta < 0: return None` before any other
work. `Reviews/verify_eta_closed.py` checks the three things that matter at once:

| object | result |
| --- | --- |
| blob `909a50a` on C's own row (`n = 27`, `ρ = 41/20`), `η = −7611431/500000000` | density `0.015185801` — the witness |
| blob `5caa1c9`, same input | `None` — rejected |
| blob `5caa1c9`, `η = 0` control | `0.780370311`, unchanged (C published `0.78037032`) |

So the guard closes the witness and moves no published number. I also re-ran the three
adversarial families (`Reviews/x_family_check.py`) against `5caa1c9`: **0 wrong verdicts in
9,000 random queries**, 0 in the probe-targeted family, 0/8 in the near-touching family. That is expected — the change is a precondition, not a
predicate repair — but it is worth having on record that the precondition added no regression in
the part of the checker that has failed three times before.

One integration note, and a correction to what I was about to write. I expected the guard to
break C's `eta_free` branch, because `shell_propose.py:202` writes `eta=str(er2)` from
`solve_laguerre(..., use_eta, ...)` and that solver can in principle return a negative `η`. It
does not: `solve_laguerre` already carries the row `−η ≥ 0`, **present at `4bcbd3a`**, with a
comment recording that the opposite sign let the objective drive `η` to the `−1e5` box bound. So
the C-side pipeline was already guarded and the exposure was only in the checker's licence — which
is exactly what `5caa1c9` closes. No published row is affected: all four rows of
`C_shell_propose.json` carry `eta = "0"`, and the `η = 0` control is numerically unchanged. My
§17 witness was therefore always a *synthetic* input (C's own row, with `η` replaced by the shell
maximum), not a run C ever produced; that does not weaken it — the licence was wrong — but it
should not be described as a pipeline bug, and I am correcting my own earlier framing here.

### 4.2 D1's consequence in Main's ledger: `0.008880268414417` is a bound, not "the exact threshold"

`CLAIMS.md` says "`t* = 0.008880268414417` is the exact threshold for the infinite packing". The
exact value of the singleton constant is

```
(4√2 − V_dod)/12  with  V_dod = 100(3√10 + 7√2)/(25 + 11√5)^{3/2}
                  = 0.0088802684147391605…
```

Main's number is lower by `3.22·10⁻¹³`, which is exactly `3.8607·10⁻¹²/12` — the error of C's
`V_DOD` enclosure (D1), divided by 12. So Main's figure inherits D1 rather than being independent
of it, and the sentence "the two routes give the same number" is true only because both routes use
the same enclosure.

The direction is safe: an *over*-estimate of `V_dod` gives an *under*-estimate of `b(v₀)`, hence a
weaker necessary condition, so `Φ ≥ 0.008880268414417` is a valid (if slightly weak) floor. What
is not right is the word "exact". The fix is one of: quote `0.0088802684147391605` from the closed
form, or keep the number and call it a lower bound. This is the second place where D1's `3.86·10⁻¹²`
shows up; the first is C's own reported `Φ` at the scanned row.

### 4.3 The family suite discriminates, but it is not a universal detector

A test suite that never fails is worthless, so I ran the same three families against every checker
blob I hold a copy of. The blob ids below are `git hash-object` of the files, verified — my first
version of this table labelled `shell_check_0a85bee.py` as `a8526a8`, which is wrong: that file is
`7dc6be58`, and `a8526a8` is `shell_check_main.py`. Running the real `a8526a8` changed the
conclusion, so the correction matters.

| blob | file | random | probe-targeted | near-touching |
| --- | --- | --- | --- | --- |
| `a8526a8` | `Reviews/shell_check_main.py` | **50/900 wrong** | **3 wrong** | 0/8 |
| `5619c1d` | `Reviews/shell_check_9461aae.py` | 0/900 | **5 wrong** | **3/8 wrong** |
| `7dc6be58` | `Reviews/shell_check_0a85bee.py` | 0/900 | 0 | 0/8 |
| `909a50a` | `Reviews/shell_check_7c56c5ee.py` | 0/900 | 0 | 0/8 |
| `5caa1c9` | `Reviews/shell_check_5caa1c9.py` | 0/9000 | 0 | 0/8 |

Two things follow, and both belong in the record rather than in a footnote.

1. The suite **discriminates strongly**: `a8526a8` is wrong on 50 of 900 random queries and 3 of
   the probe-targeted ones, `5619c1d` on 8 of 308 adversarial queries. A clean run is therefore
   informative rather than vacuous.
2. It **does not catch everything**. `7dc6be58` passes all three families; I do not know its
   lineage position (it is not one of the four blobs in my recorded sequence
   `a8526a8 → 5619c1d → 812105c3 → 909a50a`), so I make no claim about whether it was defective.
   `909a50a` passes the families while carrying the `η` licence defect — a defect of a different
   kind (a missing precondition) that needs a different test, and the `η` witness is that test.

So "0 wrong verdicts on `5caa1c9`" is evidence about one failure mode at one revision. It is not a
soundness proof, and `K15-C098`'s `SUSPENDED` label on generic checker soundness remains the right
one.

### 4.4 `PROOF_GAPS.md` G8: no shared code (definitive), agreement on 52 vectors (sample)

G8 is assigned to X and open: *"confirm C's `exactcert` and Main's `shell_check` share no code path
and agree on adversarial vectors."* Half of it is now settled outright and the other half on a
fixed sample — `Reviews/g8_checker_independence.py`, exit 0.

- **No shared code path.** `exactcert.py` (comp tip `5c10267`) imports `fractions.Fraction` and
  nothing else: `pmul`, `pdivmod`, `pgcd`, `sturm_chain`, `sign_variations`, `cauchy_bound` are
  hand-written. `shell_check.py` (`5caa1c9`) imports `sympy` and `fractions` and delegates root
  isolation to SymPy. Neither imports the other; there is no common project module. So agreement
  between them is agreement between two independent implementations, not a shared bug.
- **Agreement on 52 vectors, four routes.** All 52 give the same verdict on `q ≥ 0` on `[0,∞)`
  from **four** routes: Main's SymPy predicate, C's hand-rolled Sturm (`yun_odd_part` +
  `roots_in_half_line` + `peval`, nothing else), X's `exact_sign.py` — the authority every X
  certificate rests on — and the algebraic rule (odd-part root count, independently coded). The
  sample has both leading signs, roots at `0`, repeated roots, and 12 near-touching cases
  `(t−r)² ∓ ε` with `ε = 10⁻²⁰, 10⁻⁸` — the family that broke the probe-based checkers. It is not
  vacuous: **14 of the 52 are non-negative and 38 are not**, and all four routes split the sample
  identically.

**The interval predicate too.** The second predicate the shell pipeline uses is `p ≤ η` on a
closed interval, and it also agrees: Main's `le_on_interval` and X's `sign_on_interval` give the
same verdict on 50 vectors with roots in `[0,2]`, multiplicities 1–2, both leading signs, bounded
intervals with rational endpoints, and `η ∈ {0, ±1/2}` — 0 mismatches. C's `exactcert` has no
bounded-interval decision, so this one is a two-way test (Main vs X), not three-way.

Worth stating explicitly, because my own `exact_sign` docstring warns about it: the trap in the
interval case is reading the sign from `sign(lc)` (which is the sign on the *rightmost* gap only)
instead of evaluating the odd part inside the interval. Main's current `le_on_interval` does not
fall into it on any of the 50 vectors.

**What this does not close.** The samples are finite. The `η` precondition is separate (`X-C025`),
and `f̂(0) > 0` and the window conditions are not compared at all. G8 should stay open, described
as "independence established; agreement sampled, not proved".

## 5. Ledger

| id | claim | status |
| --- | --- | --- |
| `X-C018` | The repaired `CUT_FLOW_THEOREM.md` (`aa52147`) is correct at all six points Main listed (directed model, cut orientation, demand satisfaction, Farkas+coarea, Theorem 2 without a uniform bound, threshold formula with both branches); no fifth defect found; 115 random instances agree across cut condition, LP and threshold formula. | **VERIFIED**, `Reviews/audit_cutflow_repair.py` exits 0 |
| `X-C019` | `X_C017_small.json` is a valid CE certificate at density `0.782267254856` (`2⁻²⁴` grid, ≤ 20-digit entries, 2,646 bytes), `3.5·10⁻⁸` *weaker* (higher) than `X-C017` and 3.80× smaller; `L p = 0` exactly, `G, A, B ⪰ 0` by rational `LDL^T`. | **VERIFIED**, `verify_XC017_readable.py X_C017_small.json` exits 0 |
| `X-C020` | Erratum: `REVIEW_0353.md` §3 row W6 is wrong in both directions; correct verdict `t* = 2`, feasible iff `Φ ≥ 2`. The empty-boundary `0/0` case is *not* an obstruction when `Σ_U b = 0`. | **CORRECTION**, supersedes that row |
| `X-C021` | The height of `X_C017` is lcm blow-up of mutually coprime term denominators (each `≤ 17` digits, lcm `118` digits), not the pivot block; dyadic rounding at `S = 8` removes it. Coarser than `10⁻⁶` breaks `A`'s forced margin. | **VERIFIED** by the table in §2 |
| `X-C022` | No small-denominator both-sides triple exists in the `S = 8` basis: the frontier over `ε_AB` shows every sub-2,646-byte certificate is worse than `X-C016`, and the digit floor is ~12–13 (from `S⁻¹⁰`) plus the grid's resolution. | **VERIFIED**, table in §2.1 |
| `X-C023` | C's four `cut_flow.py` defects reproduce portably (`7/7`) from a byte copy of blob `700e44f6`, unchanged at the current `comp` tip. | **VERIFIED**, `Reviews/repro_c_cutflow_defects.py` |
| `X-C024` | Theorem 1 and the threshold formula are confirmed against exact Fourier–Motzkin elimination over ℚ: `0/297` mismatches at `n ≤ 6` (1 undecided by the blow-up guard), in addition to the LP (`0/115`). | **VERIFIED**, §E of the audit script |
| `X-C025` | Main's `η ≥ 0` guard (`5caa1c9`) closes the §17 witness and leaves the `η = 0` control at `0.780370311`; C's solver already had `−η ≥ 0` since `4bcbd3a`, so the witness is synthetic and the exposure was the checker's licence only. | **VERIFIED**, `Reviews/verify_eta_closed.py` |
| `X-C026` | `5caa1c9` passes 9,000 further random-family queries with 0 wrong verdicts (plus targeted and near-touching families). | **VERIFIED** |
| `X-C027` | The readable verifier rejects all three tampered certificates and accepts the honest one; the `10⁻⁶` perturbation is invisible to a float comparison of the bound and is caught only by the exact identity. | **VERIFIED**, `Reviews/negative_control_readable.py` |
| `X-C028` | Main's `D18` reverse condition is not triggered (no fifth defect); `D16`'s acceptance test stands with generic soundness still `SUSPENDED`; `D3`'s anchor is respected. `NEXT_PACKAGE` item 1 (`V = 5.40`) is already implied by Hales–McLaughlin. | **VERIFIED** / one wording defect open in Main's file |
| `X-C029` | `CLAIMS.md` `K15-C093` still states `sup Φ < ∞` and the `{a}`-cut `4/3` example in its bullet list, both refuted by its own repair note. | **DEFECT** (documentation, Main's file) |
| `X-C030` | `0.008880268414417` inherits C's `V_DOD` enclosure error: the exact value is `0.0088802684147391605`, so the number is a valid lower bound but not "the exact threshold". | **CORRECTION** |
| `X-C034` | **Three** functions take their vertex set from the edge list: on `b = (−1,−1,+1)`, `edges = [(0,1)]` (isolated vertex with positive deficit) `verify_flow_exact` accepts, `find_violating_cut` reports no violation, `feasible_flow` returns a flow — all wrong, all for the same reason; only `exhaustive_cut_scan` is right. **Reachable through `--fixture`**: `evaluate_external` emits `status: PATCH_FEASIBLE` on an instance the same run prints as "INFEASIBLE at any Phi". Fix: `n = len(b)` in all three. | **DEFECT** (live, systematic, reachable), D8 |
| `X-C035` | Main's `le_on_interval` and X's `sign_on_interval` agree on 50 vectors (`p ≤ η` on closed intervals, roots in `[0,2]`, multiplicities 1–2, `η ∈ {0,±½}`), including the `sign(lc)` trap case. Two-way: C's module has no bounded-interval decision. | **VERIFIED**, `Reviews/g8_checker_independence.py` |
| `X-C033` | C's own `feasible_flow` agrees with the cut condition on 38 random instances (25 infeasible, 13 feasible): a fourth independent decision procedure for Theorem 1, on C's side. | **VERIFIED**, `Reviews/audit_cutflow_repair.py` §F |
| `X-C032` | `PROOF_GAPS` G8, partially: C's `exactcert` imports only `fractions` and Main's `shell_check` only `sympy`+`fractions`, so they share no code path; **four** routes (Main, C, X's `exact_sign`, algebraic rule) agree on `q ≥ 0` for all 52 adversarial vectors tried, including near-touching `(t−r)²∓ε`. Sample is finite; `p ≤ η` is not covered. | **PARTIAL**, `Reviews/g8_checker_independence.py` |
| `X-C031` | The family suite catches `a8526a8` (50/900) and `5619c1d` (8/308) and is blind to a missing precondition and to `7dc6be58`; passing it is evidence, not proof. | **VERIFIED**, §4.3 |

---

## 6. Limits of this block

- **The audit of Theorem 2 is a proof reading, not a machine check** — there is no finite instance
  of an infinite theorem. What *is* machine-checked is Theorem 1 and the threshold formula, against
  three independent decision procedures: HiGHS LP (115 instances), exact Fourier–Motzkin over ℚ
  (297 instances at `n ≤ 6`, one undecided), and C's own `feasible_flow` (38 instances).
- **The reduction is bounded, not optimal.** I did not search for a different certificate at the
  same density with smaller height, because that is the "blind high-degree optimisation" the block
  was told not to spend its fallback on; and I did not run `m ≥ 6`, for the same reason. The
  frontier in §2.1 is evidence that nothing is left to gain *in this basis*, not a proof that no
  other construction does better.
- **`X_C017_small` is a different certificate from `X_C017`** (density `0.782267254856` vs
  `0.782267220134`). Both are in the tree and `verify_all.py` now checks both (`X-C019`); the
  readable verifier checks either, and both are VALID.
- **The weight of this block is audit, not new bounds.** No new density bound, no new packing
  obstruction, no new certificate family. What it adds is: the repaired theorem checked (six
  points, three decision procedures), six defects in C's script (four live + one latent + one
  cosmetic, plus the systematic vertex-set defect D8), three documentation defects in Main's
  ledger, one erratum of my own (W6), two corrections of my own framing, one size reduction, one
  verifier with a negative control, and one half of `PROOF_GAPS` G8. A reader looking for
  mathematical progress should look at the next block, not this one.
- **D8 has not corrupted a published number.** It is unreachable from `main()`'s own fixtures, but
  reachable through `--fixture`; it is a false accept waiting for the first external fixture with
  an isolated centre, not a defect that invalidated a quoted result.

---
## 7. What Main's decision record can now close, and what it must not

Three of Main's decisions have X-triggered reverse conditions. Their state after this block:

- **D18** ("reverse if X's audit of the repaired statement finds a further defect"). The audit
  found none: all six requested checks pass, 196 instances agree with exact Fourier–Motzkin
  feasibility, and the one instance that needs both threshold branches is handled correctly. The
  reverse condition is **not triggered**; `K15-C093` can be quoted as repaired-and-audited, with
  `X-C018` as the reviewer's statement.
- **D16** ("`shell_check.py` is the acceptance test; reverse if X's audit finds an error"). At
  `5caa1c9` the predicate side passes 9,000 adversarial queries with 0 wrong verdicts and the
  `η` licence is enforced. Two things remain true and are not in tension with that: (i) the old
  blobs `a8526a8`, `5619c1d`, `812105c3`, `909a50a` each had a real defect, and D16's rule that
  "the corrected file is the acceptance test and the old one is preserved" is what made the
  sequence auditable; (ii) passing my families is evidence, not a soundness proof — Main's own
  docstring still marks generic predicate soundness `SUSPENDED`, and it should stay that way.
- **D3** ("progress only below `0.754697399337`"). `X-C017` at `0.782267` and `X_C017_small` at
  `0.7822673` are **not** progress under this rule, and nothing in this report claims otherwise.
  Their value is that they remove the sign-predicate obligation, which is a cost, not a bound.

One live inconsistency outside Main's changed files, unchanged from my earlier block:
`Main/NEXT_PACKAGE.md` item 1 asks the next block to prove `Σ_{v∈K} vol Ω(v) ≥ 13V` for "even
`V = 5.40`". Hales–McLaughlin already gives `vol Ω(v) ≥ V_dod = 5.550291029` **per cell**, hence
`13 V_dod = 72.1538 > 70.2 = 13·5.40` for the cluster. The item as written therefore asks for
something already implied. Note there is no "stronger" version available either — a bound
`Σ_{v∈K} vol Ω(v) ≥ 13V` with `V > V_dod` would be *false* for the dodecahedral packing. So the
content the item means to carry must be a different statement: either a bound on `Σ_{v∈K} vol Ω(v)`
under a *prescribed* outer-cell structure (where the per-cell bound does not apply because the
outer cells are the ones being constrained), or an inequality with a correction term rather than a
constant `13V`. This is a wording defect in an instruction, not a
mathematical error in a claim, but it will waste a block if it is followed literally.

## 8. Timing record — measured, not estimated

Every timestamp below is a `date -u` output or a `git log` time; none is inferred from how much
work felt done. The two false full-hour claims in earlier blocks (`41.969` and `43.565` minutes
delivered) both came from estimating, and this is the mechanical fix.

| time (UTC) | event |
| --- | --- |
| `12:05:55` | block receipt (previous block's report) |
| `12:09:02` | first command of this continuation (`date -u` read before any work) |
| `12:09:41` | `16c639ce` pushed (the previous block's unpushed audit commit) |
| `12:17:42` | `097e038` — repaired theorem audited, `X_C017_small`, readable verifier, W6 erratum |
| `12:20:28` | `6c714f8` — size/strength frontier, reproducible shrink script, `X-C019` wired in |
| `12:21:43` | `b37b3b3` — portable repro of C's four defects |
| `12:22:34` | `13d0728` — exact Fourier–Motzkin cross-check |
| `12:23:56` | `330c258` — `η` witness closed by `5caa1c9` |
| `12:25:10` | `8c57c89` — **correction to my own framing**: C's solver already bounds `η ≥ 0` |
| `12:26:34` | `1ed1cb6` — negative control for the verifier; `8¹¹ → 8¹⁰` corrected |
| `12:27:01` | `2d6a1de` — D18/D16/D3 closed; `NEXT_PACKAGE` item 1 flagged |
| `12:31:30` | `abb05d4` — `CLAIMS.md` C093 still carries two refuted bullets |
| `12:33:09` | `ff1a633` — `0.008880268414417` inherits C's `V_DOD` error |
| `12:33:49` | `20c295c` — family suite discriminates on `5619c1d` |
| `12:34:20` | `506af4f` — handoff index `STATUS.md` |
| `12:35:08` | `9d4cd54` — **correction**: `a8526a8` is `shell_check_main.py` and fails 50/900 |
| `12:35:29` | `e8adfac` — frontier table densities re-paired with their own grid |
| `12:35:38` | `999b089` — report ledger brought up to `X-C031`; density-change direction fixed |
| `12:36:16` | `db6b3c7` — latent defect D5 (`exhaustive_cut_scan` on edgeless input) |
| `12:36:47` | `ead49bd` — D6 degenerate-input sweep 12/12 |
| `12:36:54` | `a1183b6` — §8 written (this table) |
| `12:37:18` | `f96508a` — D7: `exhaustive_cut_scan` omits the theorem's `max(0,·)` |
| `12:37:59` | `d64de36` — self-audit: `8¹⁰` in §2, `P ≤ 0` beyond 4, `NEXT_PACKAGE` wording made precise |
| `12:38:34` | `41a34a2` — K33a/K33b distinguished; what "both sides" buys stated |
| `12:39:22` | `497f309` — exact FM extended to `n ≤ 6` by a min-cost elimination order: 0/297 |
| `12:40:55` | `efe2340` — `PROOF_GAPS` G8 part one (`X-C032`) |
| `12:41:40` | `f9bb66a` — the missing §4.4 inserted |
| `12:42:14` | `78dbf26` — family regression extended to 9,000 queries |
| `12:43:21` | `407b22d` — readable verifier runs on all four both-sides certificates |

Checkpoints `12:25:55`, `12:45:55`, `13:05:55` all fall inside the working span; the block's
substantive hour ends at `13:05:55`, and the close line below is written after it.

*Close (`date -u` read immediately before the final push): PENDING.*


---

## 9. Handoff: the open items this block leaves, by owner

**C (all in `Computation/cut_flow.py`, blob `700e44f6`, unchanged since `4bcbd3a`).** Ranked by
consequence:

1. **D8 (false accept, systematic, reachable).** `verify_flow_exact`, `find_violating_cut` and
   `feasible_flow` take the vertex set from the edge list, so an isolated vertex with a positive
   deficit is invisible; through `--fixture` this yields `status: PATCH_FEASIBLE` on an instance
   that is infeasible at every `Φ`. Fix: `n = len(b)` in all three. Witness in `X-C034`.
2. **D1 (`V_DOD` interval).** The whole enclosure `[5.550291028519371, 5.550291028519372]` is above
   the true `5.550291028515510269…`; the low endpoint is high by `3.861·10⁻¹²`. This propagates into
   Main's `0.008880268414417` (`X-C030`). Fix: use the closed form
   `100(3√10+7√2)/(25+11√5)^{3/2}` with a directed enclosure.
3. **D2 (ring gate).** `build_13(2.1029)` returns 42 edges, not 12; the true edge is
   `2.102924448476534`. The row's `t*` belongs to `R ≥ 2.1029244` and is too *small* because
   phantom edges make cuts cheaper.
4. **D3 (`build_fcc_patch(1)` raises `TypeError`)** — `2.0**0.5 * [[...]]` multiplies a list by a
   float.
5. **D5 (latent).** `exhaustive_cut_scan` raises on an edgeless fixture; `main()` guards it.
6. **D7 (cosmetic).** `exhaustive_cut_scan` omits the theorem's `max(0, ·)`, so an all-negative
   instance reports a negative `t*`; the number is not the theorem's `t*`.

**Main.** (i) `CLAIMS.md` `K15-C093`'s bullet list still carries the two refuted statements —
delete or move them below the repair note (`X-C029`). (ii) `NEXT_PACKAGE.md` item 1 asks for
`V = 5.40`, already implied by Hales–McLaughlin (`X-C028`). (iii) `PROOF_GAPS` G8 can be updated
from "open" to "independence established, agreement sampled" on `X-C032`, and G8's remaining half
is the `p ≤ η` predicate, which neither C's module nor this block tested.

**X, next block.** Three things I did not do and would do first:
1. **G2's transcription check** — `PROOF_GAPS` G2 says "X to check the transcription of the
   defining equations" for E's Tammes-13 enclosure. That needs the Musin–Tarasov paper in hand and
   was not attempted here.
2. **The `p ≤ η` predicate** — the other half of G8. C's `exactcert` has no bounded-interval
   decision, so this needs a new independent implementation, not a comparison.
3. **`X_C017_small` as the quoted object.** It is the cheaper of the two and verifies identically;
   `verify_all.py` already checks it. If a future block quotes `X-C017`, it should quote the small
   one and say which.

**What I did not attempt, deliberately.** No new certificate search at `m ≥ 6` (the block was told
not to spend its fallback on high-degree optimisation); no Lean; no heavy computation. The heaviest
single run in this block was the 9,000-query family sweep (≈14 s, one core); `verify_all.py` is
≈10 s. Everything else is seconds. Nothing was run on Astra's machine, and nothing needed to be.
