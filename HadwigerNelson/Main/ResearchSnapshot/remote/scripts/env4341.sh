#!/bin/bash
# Environment for the exact toolchain the bundle was written for (Lean 4.34.1 + pinned Mathlib).
R="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PATH="$R/.scratch/toolchain/bin:$PATH"
ML="$R/.scratch/mathlib4"
LP="$R/.scratch/toolchain/lib/lean:$ML/.lake/build/lib/lean"
for p in "$ML"/.lake/packages/*; do LP="$LP:$p/.lake/build/lib/lean"; done
export LEAN_PATH="$R/lean/build/lib:$LP"
