#!/usr/bin/env python3
"""Run every executable witness of REVIEW_0523-X and print one table.

Written for the cross-checker: Computation owns the witnesses, so this is the single command that
reproduces the review's numbers. Each entry is a script in this directory; each prints its own
RESULT line and exits non-zero on failure. Nothing here needs network, GPU or more than a second
of CPU.

Run:  python3 Reviews/run_review_0523_checks.py
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKS = [
    ("witness_0438_audit.py",      "C_R index set, (M) criterion, star cluster (X-C037/38/39)"),
    ("two_dodecahedra_indep.py",   "Theorem D step 4 at d = 2, E/Main twist discrepancy (X-C043)"),
    ("crack_cell_indep.py",        "crack cells sqrt32 + 2 eps, the 6.985 row (X-C040)"),
    ("near_contact_band_indep.py", "two-dodecahedra threshold 3.4555003 vs C116 (X-C051)"),
    ("a15_pair_indep.py",          "A15 volumes 125/16, 129/16, contacts 16.125 (X-C052)"),
    ("fcc_hcp_cells_indep.py",     "fcc/hcp cells: sqrt32, circumradius sqrt2 (X-C054)"),
    ("payer_fixture_indep.py",     "C118 payer fixture 5.89801737180372 (X-C055)"),
    ("p_le_eta_independent.py",    "bounded-interval predicate, 92 cases (X-C046, X-C045)"),
    ("g8_checker_independence.py", "G8: no shared code, 52 + 50 vectors (X-C032/035)"),
]
fail = 0
rows = []
for script, what in CHECKS:
    p = os.path.join(HERE, script)
    r = subprocess.run([sys.executable, p], capture_output=True, text=True, cwd=os.path.dirname(HERE))
    tail = [l for l in r.stdout.strip().splitlines() if l.strip()][-1] if r.stdout.strip() else "(no output)"
    ok = (r.returncode == 0)
    fail += (not ok)
    rows.append((script, what, "OK" if ok else "FAILED", tail[:70]))
w = max(len(r[0]) for r in rows)
for script, what, state, tail in rows:
    print("%-*s  %-6s  %s" % (w, script, state, what))
print()
print("%d checks, %d failed" % (len(rows), fail))
sys.exit(0 if fail == 0 else 1)
