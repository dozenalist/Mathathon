# BinderAudit v2 — instrument repair packet (block 15)

Source-only. No Lean build, no compute beyond text comparison. Supplementary instrument: this block
does **not** re-open the accepted evidence, which stays *preserved textual hypotheses + defeq +
application compatibility* (SignatureEquivalence R5, SignatureCheckFresh R5). Exact binder identity
is **not** claimed by the integration, and a PASS here would add information, not license a stronger
claim.

## 1. Defects reported, and the repair for each

| # | defect | repair in v2 |
|---|---|---|
| D1 | `BinderAudit.lean` imported only `Lean`, so every target was absent and would have printed MISSING | imports `OAI.Analysis.PlaneSpectrum.ConditionalSpectrum` and `OAI.MeasureTheory.CompactFactors.ConditionalLimits`; `Lean` arrives transitively and is imported explicitly for the meta API |
| D2 | double-backtick names (`` ``OAI.… ``) are elaborated before the command runs, so a resolution error aborts the whole file before the MISSING branch | targets are built at runtime by `mkName` from plain strings (`s.splitOn "." |>.foldl (Name.str · ·) Name.anonymous`); nothing is parsed at compile time, and a miss is `find?` returning `none` |
| D3 | `ci.ctorName` does not exist on `ConstantInfo` (only on constructor declarations) | explicit `match ci with` over all eight `ConstantInfo` constructors (`kindOf`) |
| D4 | one failure killed the remaining targets | per-target `try/catch`, printing `ERROR <fqn> <message>` and continuing |

Also: every type is flattened to one line (`flat`), so a multi-line pretty-print cannot split a
binder across records — the failure mode that made the first comparator guess.

## 2. Comparator repairs

| # | defect | repair |
|---|---|---|
| C1 | did not check definitions | now iterates `theorems` **and** `definitions` from the spec (5 declarations) |
| C2 | did not check all retained types | every instance binder's normalised type is matched against `instance_allowed`; an unseen one is `UNKNOWN EXTRA INSTANCE` |
| C3 | unknown extra instance not rejected | rejected, fail-closed (rule `rule_unknown_instance` in the spec) |
| C4 | absent declaration tolerated as *inconclusive* | now **FAIL** (`ABSENT from capture (fail closed)`); same for an `ERROR` line |
| C5 | `strictImplicit` folded into `explicit` | counted and reported **separately**, and any strict binder is a FAIL |
| C6 | type binders not verified | implicit `Type` binders must be exactly `["X","Y","W"]` in order (plus `Z` for `EncodingApproximationAt`, which is a value binder of type `Type`); any other implicit value binder is UNKNOWN → FAIL |
| C7 | total binder count unchecked | `expected_total_binders = 31` asserted for both public theorems |
| C8 | per-declaration exemptions ignored | `instance_forbidden` is read per spec, so the definitions (which legitimately retain `StandardBorelSpace Y` / `Nonempty Y`) are not failed for it — a real bug found and fixed while testing v2 |

Evidence is always printed in full, even on FAIL, so a failing run still yields the binder list.

## 3. What was actually exercised, and what it does not mean

Run in this block over **synthetic captures** written by hand:

* a faithful 31-binder capture of both theorems plus the three definitions → `SUMMARY fails=0`;
* a capture carrying `StandardBorelSpace Y`, `Nonempty Y` and `PolishSpace Y` → all three flagged
  inline (`FORBIDDEN` ×2, `UNKNOWN INSTANCE`), plus explicit-sequence and total-count FAILs;
* a `MISSING` line and an `ERROR` line → both `ABSENT … (fail closed)`, exit non-zero.

**These validate the comparator only.** They are not evidence about the R4 tree, and they are not a
substitute for a real capture. A synthetic PASS says the parser and the rules behave; it says nothing
about what `BinderAudit.lean` will print.

## 4. Residual uncertainty in the Lean half (uncompiled)

Four places a build would most likely need a small fix, all in ~100 lines:

1. `liftTermElabM` inside `run_cmd` — the standard route is `Lean.Elab.Command.liftTermElabM`; if the
   name differs the file fails to compile, it does not produce a wrong result.
2. `forallTelescopeReducing` needs `TermElabM`/`MetaM` context, which the `liftTermElabM` provides.
3. `toString (← ppExpr d.type)` relies on `MessageData`'s `ToString`; the fallback is `s!"{…}"`.
4. `flat`'s repeated `String.replace` collapses at most two consecutive spaces; the comparator
   normalises whitespace itself, so this is cosmetic.

## 5. Status

* R4 full 82-module build and 9-root axiom check — **[S] supervisor-reported PASS**, not re-run here.
* R5 packets (SignatureEquivalence: both `|>.mp` calls replaced by `happrox` directly, exploiting
  defeq and removing the helper-captured `Y` instances; both `iff` axioms printed; FreshR5 adds
  `open PlaneFiveColor.Spectral` for `D`/`IsWild`) — **[S] reported PASS, 4+4 standard axiom prints,
  no `sorry`**.
* Copied baselines ≡ originals, both public headers identical after whitespace normalisation —
  **[C] verified in block 14**, and consistent with the R5 report.
* BinderAudit v2 — **[U]** uncompiled; comparator exercised synthetically only.
* Top-level claim — **not** locally verified in this block; unchanged from `STATEMENT-AUDIT.md`, and
  certifying the supplied proof creates **no new plane bound**: `6 ≤ χ(ℝ²) ≤ 7` as before.

## 6. Limitations

* A binder audit reads the *declaration*; it cannot see whether a binder is *used* the way the
  original used it. Statement preservation for the roots remains the textual + defeq evidence, not this.
* `expected_total_binders = 31` is derived by reading the sources, not measured from a build. If Lean
  discharges an argument by unification (e.g. a binder that becomes an instance-implicit argument of
  `condDistrib`), the count will differ and the check will FAIL loudly rather than silently pass — the
  intended direction, but it means a FAIL here is *not* automatically a defect.
