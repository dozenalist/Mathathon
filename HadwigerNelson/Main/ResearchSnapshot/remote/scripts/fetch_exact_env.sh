#!/bin/bash
# Rebuild the exact environment the bundle was written for:
#   Lean 4.34.1 + mathlib @ d13f23b723b8a846827a245b89c10fc7d3f11612
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p .scratch
TC=.scratch/toolchain
if [ ! -x "$TC/bin/lean" ]; then
  echo "[1/4] downloading lean 4.34.1"
  curl -L --retry 3 -o .scratch/lean-4.34.1.tar.zst \
    https://github.com/leanprover/lean4/releases/download/v4.34.1/lean-4.34.1-linux.tar.zst
  mkdir -p "$TC"
  tar -x --zstd -f .scratch/lean-4.34.1.tar.zst -C "$TC" --strip-components=1
fi
"$TC/bin/lean" --version
export PATH="$PWD/$TC/bin:$PATH"
ML=.scratch/mathlib4
if [ ! -d "$ML/.git" ]; then
  echo "[2/4] fetching mathlib at pinned commit"
  mkdir -p "$ML"
  cd "$ML"
  git init -q
  git remote add origin https://github.com/leanprover-community/mathlib4
  git fetch -q --depth 1 origin d13f23b723b8a846827a245b89c10fc7d3f11612
  git checkout -q FETCH_HEAD
  cd - >/dev/null
fi
echo "[3/4] mathlib commit: $(git -C "$ML" rev-parse HEAD)"
echo "leanprover/lean4:v4.34.1" > "$ML/lean-toolchain"
cd "$ML"
echo "[4/4] lake exe cache get"
lake exe cache get
echo "DONE"
