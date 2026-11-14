/-
  BINDER AUDIT v4 -- supplementary inspection.  NOT COMPILED IN THIS BLOCK.

  HISTORY. v2 failed to compile (three errors). v3 fixed those but was not built before the supervisor's
  local repair; that repair needed two further rendering fixes, applied here as R1/R2. The supervisor's
  locally tested repaired source has sha256
      ca6ee63dd737fc7095ee82e35c5d702d90c203721ad92e00757d706e7b9a9304
  This file is NOT claimed to be hash-identical to it -- comment and whitespace differences are
  expected. It applies the same two rendering fixes and nothing else.

  R1  `ppExpr` returns `Format`, not `MessageData`:
          let fmt ← ppExpr e
          pure (flat (toString fmt))
  R2  `MessageData.toString` is `BaseIO`, so the catch clause must NOT lift it through CoreM:
          let msg ← e.toMessageData.toString

  VALIDITY RULE (from the earlier run). `run_cmd` does not abort the file when the metaprogram has
  elaboration errors -- Lean leaves placeholders and continues, so a green parse can hide an audit that
  never ran. IF `lean` REPORTS ANY ERROR FOR THIS FILE, THE WHOLE CAPTURE IS VOID. No `unsafe`/`#eval`
  route is used to force execution; that would hide exactly this failure mode.

  OUTPUT (one record per line):
      DECL <fqn> <kind>
      BINDER <fqn> <index> <binderName> <info> <type>   info in explicit|implicit|strict|instance
      MISSING <fqn>
      ERROR <fqn> <message>

  Supplementary only. Exact binder identity is NOT part of the accepted integration evidence, which
  remains textual hypotheses + defeq + application compatibility (SignatureEquivalence R5,
  SignatureCheckFresh R5).
-/

import OAI.Analysis.PlaneSpectrum.ConditionalSpectrum
import OAI.MeasureTheory.CompactFactors.ConditionalLimits
import Lean

open Lean Elab Command Meta

namespace BinderAudit

def mkName (s : String) : Name :=
  s.splitOn "." |>.foldl (fun acc p => Name.str acc p) Name.anonymous

def flat (s : String) : String :=
  ((s.replace "\n" " ").replace "\t" " ").trim

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

/-- R1: `ppExpr` yields a `Format`; stringify that. -/
def renderType (e : Expr) : TermElabM String := do
  let fmt ← ppExpr e
  pure (flat (toString fmt))

def report (s : String) : CommandElabM Unit := do
  let n := mkName s
  try
    match (← getEnv).find? n with
    | none => logInfo m!"MISSING {n}"
    | some ci =>
      logInfo m!"DECL {n} {kindOf ci}"
      liftTermElabM do
        forallTelescopeReducing ci.type fun xs _ => do
          let mut i : Nat := 0
          for x in xs do
            let d ← getFVarLocalDecl x
            let info := match d.binderInfo with
              | .default        => "explicit"
              | .implicit       => "implicit"
              | .strictImplicit => "strict"
              | .instImplicit   => "instance"
            let t ← renderType d.type
            logInfo m!"BINDER {n} {i} {d.userName} {info} {t}"
            i := i + 1
          pure ()
  catch e =>
    -- R2: `MessageData.toString` is BaseIO; do not route it through Command.liftCoreM.
    let msg ← e.toMessageData.toString
    logInfo m!"ERROR {n} {flat msg}"

run_cmd report "OAI.PlaneFiveColor.Spectral.finite_uniform_precision_contradiction"
run_cmd report "OAI.PlaneFiveColor.Spectral.ambient_uniform_precision_contradiction"
run_cmd report "OAI.PlaneFiveColor.Spectral.uniform_precision_contradiction"
run_cmd report "OAI.PlaneFiveColor.Spectral.FiniteEncodingApproximationAt"
run_cmd report "OAI.PlaneFiveColor.Spectral.AmbientEncodingAt"
run_cmd report "OAI.PlaneFiveColor.Spectral.EncodingApproximationAt"

end BinderAudit
