#!/bin/bash
# One-command sound verification of an OAI tree (see work/VERIFY.md; no Lake, see f26).
#   ./verify.sh TREE [FREEZE_REF]
# Wipes build/lib, elaborates every .lean with `lean -o` (never leaving a stale olean),
# requires one olean per .lean, then textscan, certify.py vs BASELINE.cert, deffreeze.py vs REF, linecount.
# The full transcript goes to TREE/verify.log.
set -uo pipefail
TREE=$(cd "$1" && pwd); REF=${2:-}
H=$(cd "$(dirname "$0")/harness" && pwd)
REPO=$(cd "$(dirname "$0")/../../.." && pwd)
if [ -n "$REF" ]; then
  python3 "$H/verify.py" --root "$TREE" --env "$REPO/scripts/env4341.sh" -j2 --ref "$REF" > "$TREE/verify.log" 2>&1
else
  python3 "$H/verify.py" --root "$TREE" --env "$REPO/scripts/env4341.sh" -j2 > "$TREE/verify.log" 2>&1
fi
rc=$?
tail -4 "$TREE/verify.log"
echo "full transcript: $TREE/verify.log"
exit $rc
