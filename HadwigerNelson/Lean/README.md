# Lean sources and evidence

The preserved environment is Lean 4.34.1 (commit
`5045d0056413266e57c625dcd7c365b10e377c52`) with mathlib
`d13f23b723b8a846827a245b89c10fc7d3f11612`. This differs from the repository's
existing 4.35.0 root toolchain.

- [Cone geometry, obstruction, consumer, and axiom gate](../Main/ResearchSnapshot/local/outputs/cone/).
- [Final common-encoding replacement modules](../Main/ResearchSnapshot/local/outputs/encoding-refactor/).
- [R4 sources, frozen manifests, binder and fidelity checks](../Main/ResearchSnapshot/local/work/lean-queue/encoding-r4/).
- [Fixed/moving three-centre sources and checks](../Main/ResearchSnapshot/local/outputs/three-centre/).
- [Joint-pair support source and check](../Main/ResearchSnapshot/local/outputs/joint-support/).
- [Other local source packets and compiler logs](../Main/ResearchSnapshot/local/work/lean-queue/).
- [Downloaded baseline source closure](../Main/ResearchSnapshot/local/work/encoding-integration/full-original/).
- [Latest remote proof tree](../Main/ResearchSnapshot/remote/lean/).

The historical scripts and manifests preserve the actual commands and dependency
ordering. Absolute paths in those files belong to the original machine and must
be adapted for a fresh environment. The supplied OAI baseline and experimental
replacement trees are separate; select the exact frozen revision identified by
the relevant validation record.

Compiled `.olean`/`.ilean` files and toolchain/mathlib caches are excluded. The
existing logs are evidence of prior runs; copied caches never count as newly
rebuilt modules. Failed earlier packets are deliberately retained, and some
experimental sources may contain placeholders. The status table identifies the
accepted versions. `lake build` at the repository root does not check this archive.
