import sys
import os
def _computation_dir():
    here = os.path.dirname(os.path.abspath(__file__))
    cands = [os.path.join(here, "..", "..", "Computation"),
             os.path.join(here, "..", "..", "..", "repo", "RogersRamanujan", "Computation"),
             "/workspace/nucleus/work/projects/p-9021becf3f0d47a89b3f3c794c1e872b/repo/RogersRamanujan/Computation",
             os.environ.get("RR_COMPUTATION", "")]
    for c in cands:
        if c and os.path.isfile(os.path.join(c, "bz82.py")):
            return os.path.abspath(c)
    raise SystemExit("cannot locate RogersRamanujan/Computation/bz82.py")
BASE = _computation_dir()
sys.path.insert(0, BASE)
from rr_core import enumerate_residue, enumerate_gap, weight
from bz82 import pi_forward

def inB(p):
    k=len(p); return all(x>=k for x in p)

print("n  |A_n|  |A_n cap B_n|  maxsteps  meansteps  #(<=2)  #(<=6)")
tot_f=[0,0]
for n in range(0, 41):
    A = enumerate_residue(n)
    w = [a for a in A if inB(a)]
    steps = [len(pi_forward(a)[1])-1 for a in A]
    tot_f[0]+= len(w); tot_f[1]+= len(A)
    print("%2d  %4d   %4d   %6d %9.2f %6d %6d" % (n, len(A), len(w), max(steps) if steps else 0,
          (sum(steps)/len(steps)) if steps else 0, sum(1 for s in steps if s<=2), sum(1 for s in steps if s<=6)))
print("free-window fraction over n<=40: %d/%d = %.3f" % (tot_f[0], tot_f[1], tot_f[0]/tot_f[1]))
