#!/bin/bash
# Own tree's toolchain env: pinned Lean 4.34.1 + mathlib, WITHOUT the baseline
# lean/build/lib prefix (so no stale olean can be picked up).
R="/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo"
export PATH="$R/.scratch/toolchain/bin:$PATH"
ML="$R/.scratch/mathlib4"
LP="$R/.scratch/toolchain/lib/lean:$ML/.lake/build/lib/lean"
for p in "$ML"/.lake/packages/*; do LP="$LP:$p/.lake/build/lib/lean"; done
export LEAN_PATH="$LP"
