#!/bin/bash
# Reproduce every number in NOTE.md.  Run from .ultramath/smwg1r9lg/m1.
set -e
echo "== implementation A: per-cell system alone (no extras, no rim) =="
python3 implA_fast.py 3 6 | tail -1
python3 implA_fast.py 4 6 | tail -1
python3 implA_fast.py 5 6 | tail -1
python3 implA_fast.py 6 6 | tail -1
echo "== implementation A: COMBO (per-cell + (L5),(C1),(MON) + hexagon (TE)) =="
for e in 3 4 5 6; do python3 combo.py $e 6 L5,C1,MON | tail -1; done
echo "== calibration k=5 =="
for e in 3 4 5; do python3 combo.py $e 5 L5,C1,MON | tail -1; done
echo "== implementation B: transfer computation =="
python3 implB.py 3 6 | tail -1
python3 implB.py 4 6 | tail -1
python3 implB.py 5 6 | tail -1
python3 implB.py 6 6 | tail -1
echo "== geometric validation of the row model =="
python3 geom.py | tail -1
echo "== certificates for k=6 =="
for e in 3 4 5 6; do python3 cert2.py build $e 6; done
python3 cert2.py build 5 5
echo "== verification of every certificate (re-runs the decision and every checker) =="
for a in "3 6" "4 6" "5 6" "6 6" "5 5"; do python3 cert2.py verify $a | tail -1; done
echo "== saturation census =="
cat wordcensus.txt
