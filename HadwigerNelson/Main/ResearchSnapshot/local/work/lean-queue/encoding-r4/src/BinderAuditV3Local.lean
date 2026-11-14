/-
  BINDER AUDIT v3 -- supplementary inspection.  UNCOMPILED HERE (block 16, source-only).

  v2 FAILED to compile locally. Three diagnostics, three repairs; the exact failed source is preserved
  at archive/BinderAudit.v2.FAILED.lean (sha256 648afda2bd84f73169d26d5e2ccd2886803d46df9ea599cf39d2ddf3a0a06049).

  E1  "mutable i declared outside forallTelescopeReducing callback cannot be mutated inside"
      -> the counter is now declared INSIDE the callback, so the mutation is local to it.
  E2  "ToString MessageData absent"
      -> `MessageData.toString` is monadic; called in CoreM and lifted, never coerced with `toString`.
  E3  "BinderInfo.explicit unknown"
      -> Lean's BinderInfo is an enum `default | implicit | strictImplicit | instImplicit`; the
         ordinary explicit binder is `default`, and that is what is matched here.

  HARD RULE (from the same run): `run_cmd` does not abort the file when the metaprogram has
  elaboration errors -- Lean inserts placeholders and continues, so a *green* parse can hide a failed
  audit. Therefore:
      IF `lean` REPORTS ANY ERROR FOR THIS FILE, THE WHOLE CAPTURE IS VOID.
  Discard it; do not read a partial or "successful" run. This is why no `unsafe`/`#eval` path is used
  to force execution: reaching the environment that way would hide exactly this failure mode.

  OUTPUT (one record per line; the comparator normalises whitespace):
      DECL <fqn> <kind>
      BINDER <fqn> <index> <binderName> <info> <type>      info in explicit|implicit|strict|instance
      MISSING <fqn>
      ERROR <fqn> <message>

  THIS FILE MAKES NO CLAIM. Exact binder identity is supplementary. The accepted evidence for the
  integration remains textual hypotheses + defeq + application compatibility (SignatureEquivalence R5,
  SignatureCheckFresh R5).
-/

import OAI.Analysis.PlaneSpectrum.ConditionalSpectrum
import OAI.MeasureTheory.CompactFactors.ConditionalLimits
import Lean

open Lean Elab Command Meta

namespace BinderAudit

/-- Build `OAI.Foo.Bar` from a plain string; no compile-time quotation. -/
def mkName (s : String) : Name :=
  s.splitOn "." |>.foldl (fun acc p => Name.str acc p) Name.anonymous

/-- Flatten to one line: newlines/tabs to spaces, then trim. (Runs of spaces are collapsed by the
comparator, not here.) -/
def flat (s : String) : String :=
  ((s.replace "\n" " ").replace "\t" " ").trim

/-- Kind tag, matching ConstantInfo's constructors explicitly (v2's `ctorName` does not exist). -/
def kindOf (ci : ConstantInfo) : String :=
  match ci with
  | .axiomInfo _  => "axiom"
  | .defnInfo _   => "def"
  | .thmInfo _    => "thm"
  | .opaqueInfo _ => "opaque"
  | .quotInfo _   => "quot"
  | .inductInfo _ => "induct"
  | .ctorInfo _   => "ctor"
  | .recInfo _    => "rec"

/-- Render a type to a single-line string via the MONADIC `MessageData.toString`. -/
def renderType (e : Expr) : TermElabM String := do
  let fmt ← ppExpr e
  pure (flat (toString fmt))

/-- Print one BINDER line per forall binder. Never throws. -/
def report (s : String) : CommandElabM Unit := do
  let n := mkName s
  try
    match (← getEnv).find? n with
    | none => logInfo m!"MISSING {n}"
    | some ci =>
      logInfo m!"DECL {n} {kindOf ci}"
      liftTermElabM do
        forallTelescopeReducing ci.type fun xs _ => do
          -- E1: the counter lives inside the callback.
          let mut i : Nat := 0
          for x in xs do
            let d ← getFVarLocalDecl x
            let info := match d.binderInfo with
              | .default        => "explicit"   -- E3: BinderInfo has no `.explicit`
              | .implicit       => "implicit"
              | .strictImplicit => "strict"
              | .instImplicit   => "instance"
            let t ← renderType d.type          -- E2: monadic toString
            logInfo m!"BINDER {n} {i} {d.userName} {info} {t}"
            i := i + 1
          pure ()
  catch e =>
    let msg ← e.toMessageData.toString
    logInfo m!"ERROR {n} {flat msg}"

run_cmd report "OAI.PlaneFiveColor.Spectral.finite_uniform_precision_contradiction"
run_cmd report "OAI.PlaneFiveColor.Spectral.ambient_uniform_precision_contradiction"
run_cmd report "OAI.PlaneFiveColor.Spectral.uniform_precision_contradiction"
run_cmd report "OAI.PlaneFiveColor.Spectral.FiniteEncodingApproximationAt"
run_cmd report "OAI.PlaneFiveColor.Spectral.AmbientEncodingAt"
run_cmd report "OAI.PlaneFiveColor.Spectral.EncodingApproximationAt"

end BinderAudit
