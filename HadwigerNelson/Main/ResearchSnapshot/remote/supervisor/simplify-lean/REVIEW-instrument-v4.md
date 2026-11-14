# BinderAudit v4 — rendering fixes + fail-closed comparator, frozen from the real capture (block 17)

Source-only. No Lean build, no compute beyond text processing. **Supplementary tool hardening, not new
mathematical proof.** The accepted evidence is unchanged: R4 82-module build, 9-root axiom check, and
the R5 packets all pass; nothing here reopens or re-runs them.

## 1. Two rendering fixes carried from the supervisor's local repair

| # | fact | change |
|---|---|---|
| R1 | `ppExpr` returns `Format`, not `MessageData` | `renderType` is now `let fmt ← ppExpr e; pure (flat (toString fmt))` |
| R2 | `MessageData.toString` is `BaseIO` | the catch clause is `let msg ← e.toMessageData.toString`, with **no** `Command.liftCoreM` around it |

The supervisor's locally tested repaired source is `ca6ee63dd737fc7095ee82e35c5d702d90c203721ad92e00757d706e7b9a9304`.
**My `lean/BinderAudit.lean` (sha256 `0efd3831…`) is not hash-identical to it** — comment and whitespace
differences are expected — and I make no claim that it compiles. What I can say is that it applies R1 and
R2 and no other change relative to v3 (`archive/BinderAudit.v3.UNCOMPILED.lean`, `de6d5162…`).

## 2. The supervisor's four comparator defects, each repaired and each demonstrated

| # | defect in v3 | repair | demonstrated on a deliberate bad capture |
|---|---|---|---|
| H1 | `setdefault` after an ERROR could leave an existing record's error unset | error markers are written **unconditionally**, and appending a binder never clears a recorded error | BINDER lines first, then `ERROR <decl> boom` → `FAIL: ERROR boom` |
| H2 | malformed records did not reliably fail | every malformed line is a **FAIL** and is counted in the total | `BINDER onlyfourfields 0 X` → `MALFORMED line 6` and `malformed=1` in the summary/exit |
| H3 | extra implicit **value** binders were only labelled | any implicit binder that is not one of the expected type binders is a **FAIL** | `BINDER … 0 Q implicit Fin 2` → `EXTRA IMPLICIT BINDER Q : Fin 2` |
| H4 | instance membership is not **multiplicity** | instance lists compared as `Counter` multisets, both directions | duplicate `MeasurableSpace X` with `MeasurableSpace Y` dropped → `UNKNOWN/EXTRA INSTANCE MeasurableSpace X (x1)` |

v4 also now checks the **consecutive indices** `0..n-1`, the type-binder **indices** and **universe
levels** (not just names), the exact explicit sequence, and the total count.

One over-reach found and fixed while testing: the H2 hardening first flagged the legitimate `DECL` line
as malformed. `DECL` is now an accepted record; only genuinely unrecognised lines fail.

## 3. Expectations are frozen from the real capture, not guessed

`capture/real_summary.json` is the supervisor's verified local result — 6 DECL, 133 BINDER, zero
ERROR/MISSING, Lean exit 0 — transcribed field for field. From it:

* `capture/BinderAudit.real_capture.txt` — regenerated in the `BINDER` text format by
  `.scratch/build_capture.py`. It reproduces the **31 raw rows of the finite theorem exactly** on the
  fields the comparator reads (indices 0–2 implicit types, 3–9 instances, 10 `μ` explicit, 11 the
  `IsProbabilityMeasure` instance, 12–30 explicit), which is what licenses using the same ordering rule
  for the other five declarations. It is *not* a re-transcription of all 133 raw rows: the types of the
  explicit hypotheses are placeholders (`?`), because the comparator compares explicit binders by
  **name and position**, not by type text.
* `binder_expected.json` (schema 4) is generated from that summary by `.scratch/freeze_expected.py` —
  no value in it is hand-entered. Counts: **31, 31, 33, 12, 12, 14**; instances **8, 8, 8, 3, 3, 3**;
  no `StandardBorelSpace Y` and no `Nonempty Y` anywhere.

**Result on the regenerated capture: `SUMMARY fails=0 malformed=0`.** Read that as *the comparator and
the frozen expectations agree with the supervisor's verified numbers*, which is what this block can
establish. It is **not** an independent re-run of the audit.

## 4. What the capture says about the two questions that started this instrument

* The two public theorems carry **8** instances and carry neither `StandardBorelSpace Y` nor `Nonempty Y`
  — the `omit` is intact in the R4/R5 sources.
* The predicate aliases carry **3** instances (`MeasurableSpace X`, `MeasurableSpace Y`,
  `MeasureTheory.IsProbabilityMeasure μ`), confirming the correction made in v3 and contradicting v2.
* `uniform_precision_contradiction` carries the extra implicit `Z : Type u_4` at index 14, and
  `EncodingApproximationAt` at index 9 — the two places a naive comparator would mis-align.

## 5. Status

* v4 Lean — **candidate**, uncompiled; two fixes applied, hash not equal to the tested source.
* v4 comparator + frozen expectations — **verified [C]** against the transcribed real capture
  (`fails=0 malformed=0`) and against four deliberate bad captures for H1–H4.
* Accepted integration evidence — **unchanged**: R4 build, 9-root axioms, R5 packets. Not re-run.
* Exact binder identity — still **supplementary**; not part of the accepted claim.
* Top-level statement — unchanged: `6 ≤ χ(ℝ²) ≤ 7`; certifying the supplied proof creates **no new
  plane bound**.

## 6. Limitations

1. The comparator was exercised on a capture *regenerated from the supervisor's summary*, not on the raw
   133-row output. The two agree on the finite theorem's raw rows; the other five rest on that ordering
   rule plus the summary's own counts.
2. Explicit hypothesis **types** are not compared (only names and positions), because the regenerated
   capture does not carry them. If type-text equality is wanted, the raw capture must be supplied.
3. v4 Lean remains uncompiled; the risk is confined to the two rendering lines and would surface as a
   compile error, not a wrong audit.
