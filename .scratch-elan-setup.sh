#!/bin/bash
# Task-local Lean/Mathlib v4.35.0 setup for this checkout. Does NOT touch /opt,
# does NOT change lean-toolchain or lakefile.toml pins.
set -eu
REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
export ELAN_HOME="$REPO_ROOT/.scratch/elan"
export PATH="$ELAN_HOME/bin:$PATH"
elan toolchain install leanprover/lean4:v4.35.0     # into $ELAN_HOME, official release
lake exe cache get                                  # official Mathlib v4.35.0 olean cache
lake build ZetaFive
