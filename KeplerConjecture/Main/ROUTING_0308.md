# Routing the four sessions through the current mathematical plan

Written by M at block `K15-REVIEW-0308-M` for Astra to deliver. Every assignment
names the exact artifact it consumes and the acceptance test, so a worker cannot
report "done" without an artifact that passes.

## The plan in one paragraph

The geometric route is one statement: the **cut condition** `Σ_U b ≤ Φ|δ⁺_R(U)|` for
every finite `U` (`K15-C044`), with `b = √32 − vol Ω`, `R ≤ 2.09`, and the only
valid floor `Φ ≥ 0.0088803` from the singleton cut (`K15-C081r`). Negligibility is
free for any antisymmetric transfer (`K15-C035`, constant `3ΦR(R+1)⁵`). What is
missing is (i) a *proof* of the cut condition, or a *verified* `φ` for a real
packing, and (ii) the cell volumes that both need. The higher-point route is not
chosen this cycle (`D17`).

## C — Computation

1. **`C-CUT-001` (new, highest value).** Implement the bounded cut/flow solver of
   `C-TRANSFER-001` for *periodic* packings: periodic Voronoi volumes (replicate
   `3×3×3`), `b(v)`, the `R`-graph at `R = 2.09`, and the minimal `Φ` by LP
   (`min t s.t. div φ ≥ b, |φ| ≤ t`). **Acceptance (corrected):**
   (i) `fcc` and `hcp` return `t* = 0`;
   (ii) for **every** packing, `t* ≥ max_v b(v)/deg(v)` — the singleton cut `{v}` gives
   `b(v) ≤ Φ·deg(v)`, so a smaller `t*` is a bug;
   (iii) the *universal* floor `0.0088803` applies **only** to packings containing the
   icosahedral singleton witness, where `b(v₀) ≥ 0.1065632` and `deg(v₀) = 12`; it is
   not a rejection rule for arbitrary packings, whose `b(v)/deg(v)` may be smaller.
   The binding cut is reported.
2. **`C-GRAM-001`.** Keep the exact Gram certificates at their current best
   (`1.3398` p-side, `1.3713` Fourier-side, `2.0017` both-sides) and record them as
   controls; **do not** spend the block improving them — they are three orders from
   competitive, and `D17` records why they are not the target.
3. Freeze the certifier at degree 33 as the project's acceptance pipeline.

## E — Experimental

1. **`E-FIXTURE-001`.** Certified geometric fixtures for the cut condition: for each
   of the 13-cluster, a defect pair, and a vacancy in fcc, report
   `b(v)` for every cell **with a validated packing** (minimum separation over all
   pairs, including core–background — Main's own fixture failed this twice, see
   `K15-C039`), and state which cells are below `√32`.
2. **`E-COMPONENT-001`.** Attack the component assumptions: does a *closed* component
   of the `2.09`-graph exist in a saturated packing? (`K15-C080` shows that a closed
   component reduces the cut condition to `(T')`, so an example would show `(T')`
   cannot be avoided; a proof that none exists would remove that case.)
3. Keep `(T'-R2')` as the open statement; do **not** re-derive `(Q)` (`K15-C069`).

## X — Counterexamples

1. **`X-CHECK-001`.** Audit `Computation/shell_check.py` at the revision Main pushes
   this block: the predicates were repaired three times (`C049`, `C058`, `C068`); the
   four questions are in `Main/AUDIT_REQUEST_X.md`. Their own `exact_sign` already
   agrees with Main's on 10 claims (`K15-C077`).
2. **`X-IMPL-001`.** Audit the two implications Main relies on: `K15-C080` (cut form
   vs `(T')`, including the closed-component case) and `K15-C081r` (the singleton
   floor; check that only monotonicity is used, not Hales–McLaughlin).
3. **`X-C014`** is being checked locally by Astra; record the outcome either way.

## What nobody should do

- Re-derive the pointwise `(Q)` (settled, `C069`).
- Use the withdrawn cluster floor `0.0104949` or the arbitrary-`U` `|U|^{2/3}` slack.
- Try the naive explicit-transfer ansatz `φ = ψ(b(v)−b(w))` (`K15-C085` refutes it).
- Claim a `Φ` below `0.0088803`.
