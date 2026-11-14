#!/bin/sh
# Exact reproduction commands for RogersRamanujan/Experimental/cycle2.
# Run from this directory.  Only stdlib Python 3; bz82.py is imported read-only.
set -e
cd "$(dirname "$0")"
python3 lemma_checks.py          # the five lemmas + Theorem F end-to-end
python3 family_rules.py          # M1/M2 against the baseline, C1/C2 held-out tests
python3 make_data.py > DATA.md   # regenerate the raw tables
python3 window.py                # free-window sizes and path-length counts
