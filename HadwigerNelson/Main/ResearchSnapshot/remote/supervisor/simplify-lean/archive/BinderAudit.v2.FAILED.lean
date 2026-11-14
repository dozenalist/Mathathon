/-
  BINDER AUDIT v2 -- supplementary instrument.  UNCOMPILED HERE; source review only.

  Repairs to the block-14 version, each for a defect found by source review:

   D1  It imported only `Lean`, so every target was absent and would have printed MISSING.
       FIX: import the two OAI modules that actually declare the targets. `Lean` comes with them.
   D2  Targets were written with double-backtick quotations, which are elaborated BEFORE `report`
       runs, so a name typo/resolution failure aborted the whole command instead of reaching the
       MISSING branch.
       FIX: names are built from strings at runtime (`mkName`), so nothing is parsed at compile time
       and a miss is a runtime `find?` returning none.
   D3  `ci.ctorName` does not exist on `ConstantInfo` (only on constructor declarations).
       FIX: an explicit `match ci with` over ConstantInfo's constructors.
   D4  A failure inside one declaration killed the rest.
       FIX: `try/catch` per target; a failure prints `ERROR <name> ...` and the audit continues.

  Also new: every printed line is single-line (newlines in pretty-printed types are flattened), so
  downstream parsing cannot silently split a binder across lines.

  OUTPUT (one record per line, whitespace-normalised by the comparator, not here):
      DECL <fqn> <kind>
      BINDER <fqn> <index> <binderName> <info> <type>
      MISSING <fqn>
      ERROR <fqn> <message>
  where <info> is exactly one of explicit / implicit / strict / instance.

  THIS FILE MAKES NO CLAIM. It is an inspection tool; the accepted evidence for the integration is
  the textual hypotheses + defeq + application-compatibility set already established by
  SignatureEquivalence R5 and SignatureCheckFresh R5. Exact binder identity is NOT claimed by
  anything here, and a PASS from BinderAudit adds information only.
-/

import OAI.Analysis.PlaneSpectrum.ConditionalSpectrum
import OAI.MeasureTheory.CompactFactors.ConditionalLimits
import Lean

open Lean Elab Command Meta

namespace BinderAudit

/-- Build `OAI.Foo.Bar` from the string "OAI.Foo.Bar" without a compile-time quotation. -/
def mkName (s : String) : Name :=
  s.splitOn "." |>.foldl (fun acc p => Name.str acc p) Name.anonymous

/-- Flatten a rendered type to one line: newlines and tabs to spaces, runs collapsed. -/
def flat (s : String) : String :=
  let s := (s.replace "\n" " ").replace "\t" " "
  let s := s.replace "  " " "
  (s.replace "  " " ").trim

/-- Kind tag for a constant, without relying on a non-existent `ctorName`. -/
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

/-- Print one `BINDER` line per forall binder of the named constant. Never throws. -/
def report (s : String) : CommandElabM Unit := do
  let n := mkName s
  try
    match (← getEnv).find? n with
    | none => logInfo m!"MISSING {n}"
    | some ci =>
      logInfo m!"DECL {n} {kindOf ci}"
      liftTermElabM do
        let mut i : Nat := 0
        forallTelescopeReducing ci.type fun xs _ => do
          for x in xs do
            let d ← getFVarLocalDecl x
            let info := match d.binderInfo with
              | .explicit       => "explicit"
              | .implicit       => "implicit"
              | .strictImplicit => "strict"
              | .instImplicit   => "instance"
            let t := flat (toString (← ppExpr d.type))
            logInfo m!"BINDER {n} {i} {d.userName} {info} {t}"
            i := i + 1
          pure ()
  catch e =>
    logInfo m!"ERROR {n} {flat (toString e.toMessageData)}"

-- Exported public theorems (binder identity in question).
run_cmd report "OAI.PlaneFiveColor.Spectral.finite_uniform_precision_contradiction"
run_cmd report "OAI.PlaneFiveColor.Spectral.ambient_uniform_precision_contradiction"

-- The shared core and the three predicate definitions.
run_cmd report "OAI.PlaneFiveColor.Spectral.uniform_precision_contradiction"
run_cmd report "OAI.PlaneFiveColor.Spectral.FiniteEncodingApproximationAt"
run_cmd report "OAI.PlaneFiveColor.Spectral.AmbientEncodingAt"
run_cmd report "OAI.PlaneFiveColor.Spectral.EncodingApproximationAt"

end BinderAudit
