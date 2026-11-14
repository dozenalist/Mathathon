# Updated local normalization check

Source: `a08f378be6a03f80ac075b34f8ba99aeb8201d9e`,
`KeplerConjecture/Lean/Kepler15/Normalisation.lean`. Its only change from the
previous Main revision is the comment explaining that `volB1` is a definition.

The checked `NormalisationTargeted.lean` replaces `import Mathlib` with the
same four targeted imports used in the prior local check, and appends
`#print axioms Kepler15.centreDensity_eq`. All mathematical declarations are
unchanged. Local Lean 4.35.0 exited 0 with axioms
`[propext, Classical.choice, Quot.sound]`. The exact artifact hash and pinned
Mathlib revision are in `verification.json`; output is in `axioms.log`.

Reproduction in the pinned environment:

```powershell
lake env lean KeplerConjecture/Lean/Review/27616/NormalisationTargeted.lean
```

The actual local command used the pinned `lean.exe` and process `LEAN_PATH`
pointing at the existing matching caches, without modifying them. This remains
a normalization-only kernel check. It proves neither geometric ball volume nor
the counting/occupied-volume bridge nor the Kepler bound. The full-import
version was not rerun after the previous timeout.
