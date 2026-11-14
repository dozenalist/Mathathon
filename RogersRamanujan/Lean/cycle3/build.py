#!/usr/bin/env python3
"""Assemble ShiftT.lean = Staircase.lean (verbatim slice) + the cycle-3 blocks.

Usage, from this directory:
    python3 build.py block1.lean block2.lean      # writes ShiftT.lean
"""
import hashlib
import os
import sys

REPO = os.environ.get(
    "RR_REPO",
    "/workspace/nucleus/work/projects/p-9021becf3f0d47a89b3f3c794c1e872b/repo")
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(REPO, "RogersRamanujan", "Lean", "Staircase.lean")

raw = open(SRC, "rb").read()
base = raw.decode("utf-8")
digest = hashlib.sha256(raw).hexdigest()
if base.count("end RR127") != 1:
    sys.exit("Staircase.lean: expected exactly one 'end RR127'")
body, tail = base.split("end RR127")
base_body = body.split("#print axioms")[0].rstrip() + "\n"
base_prints = "\n".join(l for l in tail.splitlines() if l.strip().startswith("#print axioms"))
blocks = [open(os.path.join(HERE, b), encoding="utf-8").read() for b in sys.argv[1:]]

hdr = (
    "-- GENERATED FILE -- do not edit by hand; rebuild with build.py from\n"
    "--   RogersRamanujan/Lean/Staircase.lean  (sha256 " + digest + ")\n"
    "-- plus the cycle-3 blocks named on build.py's command line.\n"
    "-- The Staircase.lean part is byte-identical to that source slice; only its\n"
    "-- trailing '#print axioms' lines are re-emitted at the end.\n"
)
out = hdr + base_body + "\n" + "\n".join(blocks) + "\nend RR127\n\n" + base_prints + "\n"
dest = os.path.join(HERE, "ShiftT.lean")
open(dest, "w", encoding="utf-8").write(out)
print("wrote", dest, "base sha256", digest)
