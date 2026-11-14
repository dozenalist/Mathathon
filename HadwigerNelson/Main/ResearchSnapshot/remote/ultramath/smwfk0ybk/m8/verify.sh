#!/bin/bash
# Verify both extractions:
#   (a) the transfer `proper_iff_weak`           49 modules / 21813 lines -> 41 / 16478
#   (b) the paper's Thm 1.1 `no_proper_five_coloring` 70 / 30351         -> 70 / 29691
# Usage: bash .ultramath/smwfk0ybk/m8/verify.sh     (about 8 minutes)
set -e
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
source "$REPO/scripts/env4341.sh"
cd "$HERE/work"
MLPATH=$(echo "$LEAN_PATH" | sed 's|[^:]*lean/build/lib:||')

echo "=== (a) transfer: 49 modules / 21813 lines -> 41 modules / 16478 lines"
rm -rf minbuild
python3 build.py            # LEAN_PATH has the shared OAI build dir removed
echo "--- extracted tree:"; LEAN_PATH="$(pwd)/minbuild/lib:$MLPATH" lean Check.lean
echo "--- original tree:";  lean Check.lean

echo "=== (b) Theorem 1.1: 70 modules / 30351 lines -> 70 modules / 29691 lines"
rm -rf min5build
python3 build5.py
echo "--- extracted tree:"; LEAN_PATH="$(pwd)/min5build/lib:$MLPATH" lean Check5.lean
echo "--- original tree:";  lean Check5.lean
