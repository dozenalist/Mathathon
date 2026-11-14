#!/usr/bin/env python3
"""Run every check in Main/Computation and report a single verdict (K15-C053).

Each check is a separate process; a non-zero exit is a failure.  The certificate
check needs an external file and is skipped unless --cert is given.

Usage:
    python3 run_all_checks.py [--cert path/to/verified_certificate.json] [--quick]
Exit 0 iff every check that ran succeeded.
"""
import argparse, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = sys.executable

CHECKS = [
    ("constants: every ledger constant re-derived", ["constants_check.py"], []),
    ("sign predicates: self-test", ["shell_check.py", "--self-test"], []),
    ("sign predicates: 19 adversarial cases", ["checker_adversarial.py"], []),
    ("sign predicates: differential fuzz", ["predicate_fuzz.py", "--n", "300", "--seed", "7"], ["--quick"]),
    ("transfer lemma: negligibility on fcc", ["transfer_check.py", "--R", "2", "--rmax", "4"], []),
    ("cluster fixture: dodecahedral cell", ["cluster_fixture.py"], []),
    ("interface: Main <-> Computation dictionary", ["interface_xcheck.py", "--degree", "3"], []),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cert", default=None)
    ap.add_argument("--quick", action="store_true", help="skip the slower checks")
    args = ap.parse_args()
    rows = []
    t0 = time.time()
    for name, cmd, skip_when in CHECKS:
        if args.quick and skip_when and "--quick" in skip_when:
            rows.append((name, "SKIPPED (--quick)", 0.0))
            continue
        t = time.time()
        r = subprocess.run([PY, str(HERE / cmd[0])] + cmd[1:], cwd=str(HERE.parent.parent),
                           capture_output=True, text=True)
        rows.append((name, "PASS" if r.returncode == 0 else "FAIL", time.time() - t))
        if r.returncode != 0:
            print(r.stdout[-2000:])
            print(r.stderr[-2000:])
    if args.cert:
        t = time.time()
        r = subprocess.run([PY, str(HERE / "verify_comp_cert.py"), args.cert],
                           capture_output=True, text=True)
        rows.append(("certificate: %s" % Path(args.cert).name,
                     "PASS" if r.returncode == 0 else "FAIL", time.time() - t))
    print("%-52s %-8s %6s" % ("check", "verdict", "secs"))
    for name, verdict, secs in rows:
        print("%-52s %-8s %6.1f" % (name, verdict, secs))
    bad = [n for n, v, _ in rows if v == "FAIL"]
    print("\nTOTAL %.1f s ; %d checks ; %d failed" % (time.time() - t0, len(rows), len(bad)))
    print("RESULT:", "ALL CHECKS PASS" if not bad else "FAILURES: %s" % bad)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
