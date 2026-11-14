#!/bin/sh
# Reproduce every claim in REVIEW_2026-11-14_0738.md that has a script in this directory.
# Some scripts import Experimental/scripts/cell_certificate.py and rational_interval.py; copy them
# here first (they are E's, at experimental 6ae7dbf):
#   git show 6ae7dbf:KeplerConjecture/Experimental/scripts/cell_certificate.py   > cell_certificate.py
#   git show 6ae7dbf:KeplerConjecture/Experimental/scripts/rational_interval.py  > rational_interval.py
set -e
for f in audit_c133.py audit_c132.py c133_12face_essential.py c133_attain.py c133_threshold.py \
         c133_parallel_threshold.py audit_volume_filter.py; do
    printf '%-32s ' "$f"
    python3 "$f" > /dev/null 2>&1 && echo "exit 0" || echo "FAILED"
done
