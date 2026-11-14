# Local Lean verification

Use the repository's Lean v4.35.0 and Mathlib v4.35.0. The supervisor has
confirmed the local Lean and Lake executables and the matching mathlib source
checkout. Compiled dependency availability must be checked for each requested
module.

Main assigns formalization only after the mathematical statement is stable.
Write modules under `KeplerConjecture/Lean/` and submit them using
`Main/LOCAL_COMPUTE_REQUESTS.md`. Suitable early obligations include a precise
density normalization lemma or the finite boundary-accounting argument for a
specific local correction. Formalizing a conditional theorem leaves its
hypotheses as explicit research obligations.

From a prepared repository root, a direct check of an actual module has the
form below, with the placeholder replaced by its real filename.

```powershell
lake env lean KeplerConjecture/Lean/ActualModule.lean
```

Imports between project modules may require local compilation in dependency
order and an appropriate module search path. The local supervisor records
the full command used. Coordinate any shared build integration through the
supervisor while keeping this assignment's tracked edits in KeplerConjecture.

The verification report includes exact theorem statements, the source commit,
exit status, dependency versions, and `#print axioms` output. Use the current
competition's permitted axioms when claiming its Lean-verified category.
Unproved hypotheses, `sorry` dependencies, and numerical oracle assumptions
must be visible in the claim ledger.
