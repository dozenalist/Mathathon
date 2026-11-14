#!/usr/bin/env bash
# One-command reproduction of every Experimental check.
# One CPU, under 1 GiB, under 10 minutes total (measured: ~2 min).
# Usage: bash Experimental/scripts/run_all_checks.sh
set -u
cd "$(dirname "$0")/../.." || exit 1
fail=0
printf '%-28s %-8s %s\n' "script" "status" "note"
printf '%-28s %-8s %s\n' "----------------------------" "------" "----"
run() {
  local f="$1" note="$2"
  if timeout 300 python3 "Experimental/scripts/$f.py" >/dev/null 2>&1; then
    printf '%-28s %-8s %s\n' "$f" "PASS" "$note"
  else
    printf '%-28s %-8s %s\n' "$f" "FAIL" "$note"; fail=1
  fi
}
run verify_all_claims       "exact rational re-derivation of every published constant"
run interval_selfaudit      "soundness + corruption-detection of the interval primitives"
run tammes13_enclosure      "delta_13 enclosure; count 12 at 2.05 and 2.09; kissing control"
run shell_2p09_interval     "exact rational endpoint 23681/43681"
run shell_conversion        "cap identity and radius conversion table"
run barlow_shell_check      "Barlow stackings: 12 in [2,2.09]"
run outer_cell_angular_bound "directional ceiling (exploratory)"
run block_evaluator         "blocks, disjointness, overlap, (T') accounting"
run transfer_evaluator      "antisymmetric transfer, pointwise FCC, cancellation"
run multi_defect_test       "defect isolation; 2x2x2 grid"
run frank_kasper_test       "A15 saturated fixture"
run periodic_relax          "periodic relaxation recovers fcc / pi/sqrt18"
# evidence integrity: every JSON must parse, every TXT must be non-empty
bad=0
for f in Experimental/evidence/*.json; do
  [ -e "$f" ] || continue
  python3 -c "import json,sys; json.load(open('$f'))" 2>/dev/null || { echo "INVALID JSON: $f"; bad=1; }
done
for f in Experimental/evidence/*.txt; do
  [ -e "$f" ] || continue
  [ -s "$f" ] || { echo "EMPTY: $f"; bad=1; }
done
if [ "$bad" -eq 0 ]; then
  printf '%-28s %-8s %s\n' "evidence integrity" "PASS" "all JSON parses, all TXT non-empty"
else
  printf '%-28s %-8s %s\n' "evidence integrity" "FAIL" "see above"; fail=1
fi

echo
if [ "$fail" -eq 0 ]; then
  echo "ALL CHECKS PASSED"
else
  echo "SOME CHECKS FAILED (see above)"; exit 1
fi
echo
echo "Reminder: runs marked exploratory (outer_cell_angular_bound, block_evaluator,"
echo "transfer_evaluator, multi_defect_test, periodic_relax, frank_kasper_test) produce"
echo "TESTED_FINITE numbers, not certificates. See Experimental/REVIEW_0138.md section 5"
echo "for the retraction of the S-D magnitudes."
