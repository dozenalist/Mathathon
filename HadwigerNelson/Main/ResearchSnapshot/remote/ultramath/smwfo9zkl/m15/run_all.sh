#!/bin/bash
# Check everything in this directory.  About 4 minutes on one core.
set -u
cd "$(dirname "$0")"
fail=0
run () { echo; echo "########## $* ##########"; "$@" || { echo "FAILED: $*"; fail=1; }; }
run python3 -u construction.py
run python3 -u verify.py
run python3 -u nonvacuity.py
run python3 -u k5_control.py
run python3 -u step_relation.py
run python3 -u make_witnesses.py
echo
if [ "$fail" -eq 0 ]; then echo "=== ALL CHECKS PASSED ==="; else echo "=== THERE WERE FAILURES ==="; fi
exit "$fail"
