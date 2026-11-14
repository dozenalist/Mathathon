# Local normalization check

On November 13, 2026, Astra checked a targeted-import variant of Main's
`Normalisation.lean` from commit
`c91007ff11844f179921fadfb2e90d352b8c0090` locally. The checked artifact is
[NormalisationTargeted.lean](NormalisationTargeted.lean), SHA-256
`bd4be2e99c6d7fa0d42c930558342807f154beaeb78547ace9057bf47d37cba7`.
The theorem body and definitions are unchanged. The variant replaces
`import Mathlib` with four specific imports and adds
`#print axioms Kepler15.centreDensity_eq`.

The pinned Lean version is 4.35.0, commit
`eb6cafb7290e8bd5f2937522d8d804f58f02bafc`. Mathlib commit is
`56a005855ea17e0b0958f73ec801ae140b0a1679`. Existing matching compiled
dependencies were reused read-only through `LEAN_PATH`; no shared build
configuration or dependency files were changed. The local run exited 0. Its
[axiom output](normalisation-axioms.log) is exactly
`[propext, Classical.choice, Quot.sound]`.

In an environment with those pinned dependencies and compiled caches:

```powershell
lake env lean KeplerConjecture/Lean/Review/NormalisationTargeted.lean
```

The actual local invocation used the pinned `lean.exe`, with process `LEAN_PATH`
pointing at the matching cache directories, and the same source file. This
check is for this module only; it is not a claim that the repository's root
build imports the module or that an untouched checkout has its cache ready.
The unchanged full-import module exceeded five minutes without output and was
terminated with exit -1. That version remains unverified under the pinned
toolchain. This timeout does not invalidate the passing targeted-import check.

The original comments are retained as provenance, including its earlier draft
status and intended interpretation of center density. The checked theorem is
only the algebraic identity obtained by unfolding `centreDensity` and `volB1`.
The file does not prove the geometric unit-ball volume, the equality with an
asymptotic count of centers, or any sphere-packing upper bound. Those bridges
remain separate mathematical obligations. No Kepler theorem is claimed.
