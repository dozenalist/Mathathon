#!/bin/sh
# Reproduce every number in ../proof.md.  Run from this directory.
set -e
echo "== 1. calibration: ell=5, k=5 (Table A) =="
python3 -c "import rigorous; rigorous.walk(5,5,2,True)"
python3 -c "import rigorous; rigorous.analyse(5,5,2,use_sa=False)"
echo "== 2. ledger at k=6 (Table B) =="
for e in 3 4 5 6; do python3 -c "import rigorous; rigorous.walk($e,6,3,True)"; done
echo "== 3. exact geometry =="
python3 geomcheck.py
echo "== 4. two-procedure cross-check =="
python3 -c "import check; check.verify(6,6,3,nrandom=100)"
python3 -c "import check; check.verify(5,5,2,nrandom=80)"
echo "== 5. arc widths and the monochromatic-strip test =="
python3 -c "import strips; strips.check()"
echo "== 6. the open-set form of (5.2) =="
python3 -c "import openset; openset.main(6,6,3)"
