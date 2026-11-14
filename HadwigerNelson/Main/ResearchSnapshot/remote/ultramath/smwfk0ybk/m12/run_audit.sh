#!/bin/bash
# Trust and faithfulness audit of the Hadwiger-Nelson formal record (swarm smwfk0ybk, member m12, d15).
# Reproducible from a clean shell.  Nothing outside this directory is written.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$(cd "$HERE/../../.." && pwd)
rc=0
part() {  # part <label> <subshell body...>  -- runs body with its own rc, propagated
  local lab=$1; shift
  if ( "$@" ); then echo "== $lab: PASS"; else echo "== $lab: FAIL"; rc=1; fi
}
runfile() {  # runfile <label> <dir> <lean args...>
  local lab=$1 dir=$2; shift 2
  echo "---- $lab: $*"
  lean "$@" || { echo "FAILED: $*"; return 1; }
}

echo "===== part 1: exact bundle toolchain (Lean 4.34.1 + pinned Mathlib), oleans in $REPO/lean/build/lib"
part exact bash -c '
  set -u; HERE='"$HERE"'; REPO='"$REPO"'; source "$REPO/scripts/env4341.sh"; cd "$HERE"; lrc=0
  for f in Audit1 Audit2 Audit4 Audit5 Audit6 CollapseW1; do echo "---- exact: $f.lean"; lean "$f.lean" || { echo "FAILED: $f.lean"; lrc=1; }; done
  exit $lrc'

echo
echo "===== part 2: stock VM toolchain (Lean 4.33.1 + /opt/mathlib) on the ported tree in ./portlib"
part stock-ported bash -c '
  set -u; HERE='"$HERE"'; export LEAN_PATH="$HERE/portlib:$LEAN_PATH"; cd "$HERE/portcheck"; lrc=0
  for f in Audit3 Audit2 Audit4 Audit6 CollapseW1; do echo "---- stock: $f.lean"; lean "$f.lean" || { echo "FAILED: $f.lean"; lrc=1; }; done
  exit $lrc'

echo
echo "===== part 3: the k=6 certificate (independent of m6 shrinking theorem)"
part tight bash -c '
  set -u; HERE='"$HERE"'; export LEAN_PATH="$HERE/tight:$LEAN_PATH"; cd "$HERE/tight"; lrc=0
  lean -o InterfaceStates.olean InterfaceStates.lean || lrc=1
  lean -o TightenedSAT.olean TightenedSAT.lean || { echo "FAILED: TightenedSAT"; lrc=1; }
  exit $lrc'

echo
echo "===== part 4: fresh-copy audit of this swarm own Lean deliverables"
part swarm bash -c '
  set -u; HERE='"$HERE"'; export LEAN_PATH="$HERE/swarm:$LEAN_PATH"; cd "$HERE/swarm"; lrc=0
  for f in Indep Shrink Core TightCore M5Interface PaletteShrink Tightened; do
    echo "---- stock: $f.lean"; lean -o "$f.olean" "$f.lean" || { echo "FAILED: $f.lean"; lrc=1; }
  done
  exit $lrc'

echo
if [ $rc -eq 0 ]; then echo "ALL CHECKS PASSED"; else echo "SOME CHECKS FAILED"; fi
exit $rc
