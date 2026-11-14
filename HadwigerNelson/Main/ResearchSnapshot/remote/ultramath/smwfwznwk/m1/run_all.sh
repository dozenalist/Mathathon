#!/bin/bash
# Reproduce every claim in REPORT.md / proof.md.  Nothing outside this directory is touched.
set -e
cd "$(dirname "$0")"
py(){ python3 "$@"; }
echo "=== 0. domain and disjointness graph H (k=6, C_6, free label 0)"; py work/domain.py
echo; echo "=== 1. the uniform word A^2 B^2 D^(m-3) E^2 F^(m-3) for m = 5..200"; py work/check1.py
echo; echo "=== 2. certificate: extraction and verification of the witnesses m = 5,6,9,12,15,18"
py work/make_cert.py; py work/verify_cert.py
echo; echo "=== 3. exact-rational geometry GEOM + numeric sampling of (5.3)"; py work/verify_geom.py
echo; echo "=== 4. classification, two independent complete procedures (exhaustive DFS + CaDiCaL)"
py work/classify.py 2 3 4 5 6 7 8 9 10 11 12 13 14 15
echo; echo "=== 5. the m=4 obstruction: minimal uncolourable induced subgraph"; py work/minobs.py
echo; echo "=== 6. vacuity/non-vacuity: k=5 (never) and k=7 (3-block word)"; py work/contrast.py
echo; echo "ALL CHECKS PASSED"
