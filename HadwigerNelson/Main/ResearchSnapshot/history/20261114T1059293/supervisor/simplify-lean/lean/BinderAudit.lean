/-
  BINDER AUDIT: declaration inspection, not application testing.  NOT COMPILED HERE.

  WHY. `SignatureCheckFresh.lean` is an APPLICATION-COMPATIBILITY test: it shows the theorem can be
  used from a context that supplies only the arguments we chose. It cannot show the converse --
  that no EXTRA binder exists -- because an extra instance binder is discharged silently whenever it
  is synthesizable, and a DROPPED binder is invisible because passing fewer arguments still works.
  Binder equality needs the environment, not a use site.

  WHAT THIS DOES. For each declaration it reads the constant's type out of the environment and walks
  the forall telescope, printing one line per binder: index, user name, binderInfo (explicit /
  implicit / strict / instance), and the pretty-printed binder type. It does not elaborate any use of
  the declaration, so it is meaningful even when nothing else about the file elaborates: a missing
  name is reported as missing, not as an error that hides the rest.

  OUTPUT FORMAT (one line per binder, deliberately trivial to parse):
      BINDER <decl> <index> <name> <info> <type>

  RUN:
      source scripts/env4341.sh
      LEAN_PATH="$OUT:$LEAN_PATH" lean supervisor/simplify-lean/lean/BinderAudit.lean > binders.txt
      python3 supervisor/simplify-lean/binder_snapshot.py binders.txt

  The python side owns the EXPECTED signature (supervisor/simplify-lean/binder_expected.json), so the
  Lean side stays dumb and cannot encode the answer it is supposed to be testing for.
-/

import Lean

open Lean Elab Command Meta

namespace BinderAudit

/-- Print one `BINDER` line per forall binder of `n`. Missing names are reported, not fatal. -/
def report (n : Name) : CommandElabM Unit := do
  let env ← getEnv
  match env.find? n with
  | none => logInfo m!"MISSING {n}"
  | some ci =>
    logInfo m!"DECL {n} KIND {toString ci.ctorName}"
    liftTermElabM do
      let ty := ci.type
      let mut i : Nat := 0
      forallTelescopeReducing ty fun xs _ => do
        for x in xs do
          let d ← getFVarLocalDecl x
          let info := match d.binderInfo with
            | .explicit      => "explicit"
            | .implicit      => "implicit"
            | .strictImplicit => "strict"
            | .instImplicit  => "instance"
          let t ← ppExpr d.type
          logInfo m!"BINDER {n} {i} {d.userName} {info} {t}"
          i := i + 1
        pure ()

/-! Metric-independent spelling of `Circle`'s instances is not needed here: the audit reads types,
  it does not elaborate `Measure Circle`. -/

-- The two exported theorems whose binder equality is in question.
run_cmd report ``OAI.PlaneFiveColor.Spectral.finite_uniform_precision_contradiction
run_cmd report ``OAI.PlaneFiveColor.Spectral.ambient_uniform_precision_contradiction
run_cmd report ``OAI.PlaneFiveColor.Spectral.uniform_precision_contradiction

-- The predicate definitions, where `abbrev`-vs-`def` and the `S` parameter live.
run_cmd report ``OAI.PlaneFiveColor.Spectral.FiniteEncodingApproximationAt
run_cmd report ``OAI.PlaneFiveColor.Spectral.AmbientEncodingAt
run_cmd report ``OAI.PlaneFiveColor.Spectral.EncodingApproximationAt

end BinderAudit
