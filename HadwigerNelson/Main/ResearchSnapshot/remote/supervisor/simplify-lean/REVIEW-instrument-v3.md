# BinderAudit v3 — repair after the local compile failure (block 16)

Source-only. No Lean, no cloud build, no compute. The accepted checks (R4 82-module build, V4, R5
SignatureEquivalence/SignatureCheckFresh) are **unchanged by this block** and are not re-run here.

## 1. The failed version is preserved, not overwritten

| artefact | sha256 |
|---|---|
| `archive/BinderAudit.v2.FAILED.lean` | `648afda2bd84f73169d26d5e2ccd2886803d46df9ea599cf39d2ddf3a0a06049` |
| `archive/binder_expected.v2.FAILED.json` | `fb575764b0d145e7e95b926258d27bbe74669b869946af45c2e1c30cef6e9f88` |
| `archive/binder_snapshot.v2.FAILED.py` | `977878b409010c8182f428b66aadf5b2d4838d0f4556b5488795ceb5abc7ebc5` |

## 2. Three compile diagnostics, three repairs

| # | diagnostic | repair |
|---|---|---|
| E1 | line 84: `mutable i` declared outside the `forallTelescopeReducing` callback cannot be mutated inside | the counter is now declared **inside** the callback, so the mutation is local to it |
| E2 | line 87: no `ToString MessageData` instance | types are rendered with the **monadic** `MessageData.toString`, called in `CoreM` and lifted (`renderType`) |
| E3 | line 78: `BinderInfo.explicit` unknown | Lean's `BinderInfo` is `default | implicit | strictImplicit | instImplicit`; the ordinary explicit binder is **`default`**, which is now matched |

## 3. The `run_cmd` hazard, and the rule it imposes

The run also showed that `run_cmd` does **not** abort the file when the metaprogram has elaboration
errors — Lean inserts placeholders and continues. A green parse can therefore hide an audit that never
ran. Two consequences, both now written into the file header:

* **A capture is valid only if `lean` reported no error for `BinderAudit.lean`.** Any error voids the
  whole capture; a missing or partial capture is not a pass.
* No `unsafe` / `#eval` route is used to force execution. Reaching the environment that way would hide
  precisely this failure mode, which is the opposite of what an audit is for.

## 4. The comparator's false assumption — the substantive correction

v2 asserted that the predicate aliases retain `StandardBorelSpace Y` and `Nonempty Y`. **Wrong.** The
accepted `#check` shows `FiniteEncodingApproximationAt` carries only

```
[MeasurableSpace X] [MeasurableSpace Y] [IsProbabilityMeasure μ]
```

with three type parameters. The error was structural: I read the instance set off the `variable` block
instead of off the declaration header. Lean keeps only the instances a declaration actually needs, and
`W` needs none — it occurs only through `coeff : W → Fin r → ℂ`, a function type.

**Design change, not just a value change.** Rather than guess a second time:

* **definitions are FROZEN** against the actual accepted header: `{MeasurableSpace X, MeasurableSpace Y,
  IsProbabilityMeasure μ}`, type binders `X Y W` (`EncodingApproximationAt` additionally `Z`), explicit
  `μ p q b m γ` (`μ p P S b m γ` for the core);
* **the two theorems are UNFROZEN on purpose.** Only what the sources justify is enforced — the two
  omitted instances are forbidden, the type binders are `X Y W`, the explicit sequence is the 20-name
  source list. The instance multiset is *printed* and emitted as `FREEZE-CANDIDATE`, not judged;
* **freeze protocol**: the first real capture's printed multiset is pasted into `instance_allowed` and
  `unfrozen` set to `false`; from then on an unknown extra instance is a FAIL.

This keeps the fail-closed property where the ground truth exists and refuses to manufacture it where
it does not.

## 5. What was exercised, and what it does not mean

On **synthetic** captures only:

* a capture built to the *actual* definition header plus a plausible theorem instance set →
  `SUMMARY fails=0`; the two theorems print `FREEZE-CANDIDATE instances = [MeasurableSpace X,
  MeasurableSpace Y, MeasurableSpace W, IsProbabilityMeasure μ]`; the three definitions pass their
  frozen check and the `Z` binder is placed correctly for `EncodingApproximationAt`;
* a negative capture → `FORBIDDEN` flagged on `StandardBorelSpace Y` and `Nonempty Y`, `UNKNOWN
  INSTANCE` on `PolishSpace Y` against a *frozen* definition, plus `ABSENT (fail closed)` for a
  `MISSING` line and `ERROR` for an error line.

Both exercise the comparator. Neither is a capture of the OAI tree, and a synthetic PASS says nothing
about what `BinderAudit.lean` prints.

## 6. Residual uncertainty (uncompiled)

1. `liftCoreM (MessageData.toString md)` — if `MessageData.toString` is `IO`-based rather than
   `CoreM`-based, this needs `liftIO`; the failure is a compile error, not a wrong audit.
2. `forallTelescopeReducing` under `liftTermElabM` — standard, but unverified here.
3. The *theorems'* instance sets remain unknown until a real capture; the `W` question (whether
   `MeasurableSpace W` is a binder) is exactly what the freeze step answers.
4. `EncodingApproximationAt`'s instance set is borrowed from the `FiniteEncodingApproximationAt`
   header; if the real capture disagrees this is the first entry to correct.

## 7. Status

* v2 Lean — **FAILED locally** (three compile errors, quoted above). Preserved.
* v3 Lean — **candidate**, uncompiled.
* v3 comparator/expected — **verified [C]** on synthetic captures only: parser, frozen-definition
  checks, unfrozen/theorem freeze path, forbidden/unknown/absent/ERROR failures all behave as stated.
* Accepted integration evidence — **unchanged**: R4 82-module build PASS, 9-root axiom PASS, R5 packets
  PASS with 4+4 standard axiom prints and no `sorry`. Not re-run; not reopened.
* Exact binder identity — still **supplementary**, still not claimed. The accepted scope is preserved
  textual hypotheses + defeq + application compatibility.
* Top-level statement — unchanged: `6 ≤ χ(ℝ²) ≤ 7`; certifying the supplied proof creates **no new
  plane bound**.
