#!/bin/sh
# K15-C148 -- one-command acceptance for the M-CERT-002 handoff.
#
# Usage:  sh KeplerConjecture/Computation/l1_handoff_check.sh [Q] [X]
#   Q = your rigorous lower bound for lam_min/2   (default: absent)
#   X = your rigorous third-derivative bound      (default: absent)
#
# Runs the pinned command plus every required control and prints one verdict.
# Nothing here writes outside this tree; runtime is a few seconds.
set -u
HERE=$(dirname "$0")
PY=${PYTHON:-python3}
Q=${1:-}
X=${2:-}
fail=0

say() { printf '%s\n' "$*"; }
check() { # name expected_exit command...
  name=$1; want=$2; shift 2
  "$@" >/dev/null 2>&1
  got=$?
  if [ "$got" = "$want" ]; then say "  [ok]   $name (exit $got)"; else
    say "  [FAIL] $name (exit $got, want $want)"; fail=1; fi
}

say "M-CERT-002 handoff check"
say "  source: $(sha256sum "$HERE/l1_remainder.py" | cut -d' ' -f1)"
say "  python: $($PY -c 'import numpy,scipy;print(numpy.__version__,scipy.__version__)' 2>&1)"

say ""
say "pilot self-test (13 cases: exit codes, agreement, radius)"
check "self-test" 0 $PY "$HERE/l1_remainder.py" --self-test

say ""
say "T1/T2 margins on the eps = 1 ball"
check "margins" 0 $PY "$HERE/l1_remainder.py" --margins

say ""
say "required controls"
check "c = 0.30 is rejected (inert pilot)"        3 $PY "$HERE/l1_remainder.py" --certify --c 0.30 --seed 3
check "eps = 0.2 is outside the type region"       2 $PY "$HERE/l1_remainder.py" --certify --eps 0.2
check "a negative allowance is invalid"            4 $PY "$HERE/l1_remainder.py" --certify --eps 3.0
check "c = 0 is invalid"                           4 $PY "$HERE/l1_remainder.py" --certify --c 0

say ""
if [ -n "$Q" ] && [ -n "$X" ]; then
  say "value bound with the supplied rigorous inputs Q=$Q X=$X"
  "$PY" "$HERE/l1_remainder.py" --certify --eps 1.0 --c 0.13 \
        --hessian-bound "$Q" --m3-bound "$X" 2>&1 | tail -4
  got=$?
  if [ "$got" = 0 ]; then
    say "  => the LOCAL RATE is certified.  C147's global-to-local entry remains open."
  else
    say "  => NOT certified: X exceeds 6(Q-c)/theta_max.  Report the ladder row."
  fi
else
  say "value bound: no rigorous inputs supplied, so it cannot be certified."
  say "  rerun as: sh $0 <Q> <X>   (Q >= 0.20 is what the chain needs; X <= 2.7151 at Q = 0.20)"
  check "uncertified without inputs"               1 $PY "$HERE/l1_remainder.py" --certify --eps 1.0 --c 0.13
fi

say ""
if [ "$fail" = 0 ]; then say "HANDOFF CHECK: PASS (T1/T2 and all controls)"; else
  say "HANDOFF CHECK: FAIL"; fi
exit $fail
