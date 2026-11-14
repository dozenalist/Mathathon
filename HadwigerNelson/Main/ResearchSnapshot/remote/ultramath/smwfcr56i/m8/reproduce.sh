#!/bin/bash
# Reproduce the Lean 4.33.1 port of the OAI Hadwiger-Nelson development.
#   usage: ./reproduce.sh [target-dir]
# Requires the ambient LEAN_PATH (Mathlib oleans) already set, as in this VM.
set -eu
REPO=${REPO:-/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo}
HERE=$(cd "$(dirname "$0")" && pwd)
T=${1:-$HERE/repro}
rm -rf "$T"; mkdir -p "$T"
cp -r "$REPO/lean/OAI" "$T/OAI"
echo "== pristine modules: $(find "$T/OAI" -name '*.lean' | wc -l)"
( cd "$T" && patch -p1 --no-backup-if-mismatch < "$HERE/patches2/all.patch" )
echo "== patches applied"
cd "$HERE"
PORT_SRC="$T" PORT_LIB="$T/lib" PORT_LOG="$T/status.json" python3 port.py
cp "$HERE/audit/Axioms.lean" "$T/Audit.lean"
( cd "$T" && LEAN_PATH="$T/lib:$LEAN_PATH" lean Audit.lean )
python3 - "$T/status.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
bad=[k for k,v in d.items() if not v.get('ok')]
print("== modules compiled: %d/%d" % (len(d)-len(bad), len(d)), "failures:", bad)
PY
