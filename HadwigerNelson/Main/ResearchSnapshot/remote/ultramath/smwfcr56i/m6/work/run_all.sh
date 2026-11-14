#!/bin/sh
# Reproduce every check of this audit.  Run from this directory.
#   sh run_all.sh
# Requirements: python3 (+ sympy, mpmath), lean 4.33.1 with Mathlib on LEAN_PATH.
set -e
echo "############ 1. Lean 4 / Mathlib formalisation of the section 8.5 certificate"
lean --version
lean OAI_Audit_Moser.lean
echo
echo "############ 2. exact verification of section 8.5 / 8.6 (coordinates, edges,"
echo "################ non-3-colourability, placement, Lemma 8.9 certificate, Table 1/2)"
python3 verify_sec8.py
echo
echo "############ 3. exact values for the report"
python3 exact_values.py
echo
echo "############ 3b. decimal-free exact rational certificate for Lemma 8.9"
python3 exact_certificate.py
echo
echo "############ 4. section 5.3: uniform expansion (5.9) and constants (5.10)"
python3 verify_53.py
echo
echo "############ 5. finite combinatorics of sections 8.2, 8.3/8.5, 6.3.4"
python3 verify_combinatorics.py
echo
echo "############ ALL CHECKS COMPLETE"
