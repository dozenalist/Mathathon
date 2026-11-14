#!/usr/bin/env bash
# d7.sh -- port an OAI tree to stock Lean 4.33.1, build it, re-certify it, count it.
#
#   bash d7.sh SRC_TREE DST_TREE [--jobs N]
#
# SRC_TREE must contain OAI/ (and CheckBoth.lean for the certificate step).
# Steps: copy -> content-addressed port -> build 4.33.1 oleans -> #print axioms -> line count.
# Exits non-zero if any module, the certificate, or the line count fails.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$HERE/../../.."
PATCH="$REPO/.ultramath/smwfcr56i/m8/patches2/all.patch"
SRC="${1:?source tree}"; DST="${2:?destination tree}"
JOBS="${3:-3}"
[ -e "$DST" ] && { echo "refusing: $DST exists"; exit 2; }

echo "== 1. copy $SRC -> $DST"
cp -a "$SRC" "$DST"
rm -rf "$DST/build"

echo "== 2. port to 4.33.1 (content-addressed, trim-tolerant)"
python3 "$HERE/port.py" apply "$DST" "$PATCH" --json "$DST/port.json" | tee "$DST/port.log"

echo "== 3. build under stock Lean ($(lean --version | head -1))"
python3 "$HERE/build.py" "$DST" --jobs "$JOBS" --log "$DST/build_status.json" | tail -5

echo "== 4. certificate"
( cd "$DST" && LEAN_PATH="build/lib:${LEAN_PATH:-}" lean CheckBoth.lean ) | tee "$DST/checkboth.log"

echo "== 5. line count"
python3 - "$DST" <<'PY'
import pathlib, sys
root = pathlib.Path(sys.argv[1])
mods = sorted(root.glob("OAI/**/*.lean"))
tot = 0
for p in mods:
    t = p.read_text()
    tot += len(t.split("\n")) - (1 if t.endswith("\n") else 0)
print(f"{len(mods)} modules, {tot} lines")
PY
