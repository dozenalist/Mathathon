#!/bin/bash
# Reproduce every check of no-go.md.  Runtime about 30 s.
set -e
cd "$(dirname "$0")"
echo "### alpha_bounds.py  (Proposition 3.1: the two-angle maps and their deviation)"
python3 alpha_bounds.py
echo
echo "### model_check2.py  (Theorem 2: models (M') and (M), checks A-H)"
python3 model_check2.py
echo
echo "### structural_check.py  (S1-S5: k=5 census, k=6 palette census, candidate hypotheses)"
python3 structural_check.py
echo
echo "### all checks done"
