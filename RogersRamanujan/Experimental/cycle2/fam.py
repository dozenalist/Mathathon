import sys, json
sys.path.insert(0, "/workspace/nucleus/work/projects/p-9021becf3f0d47a89b3f3c794c1e872b/repo/RogersRamanujan/Computation")
from bz82 import forward, pi_forward, pi_inverse
from rr_core import weight, T, Tinv, is_residue, is_gap

def show(p): return "(" + ",".join(map(str,p)) + ")"

print("=== A-side: (1^s) -> D_s")
for s in range(0, 31):
    lam = tuple([1]*s)
    f = forward(lam)
    print(s, show(lam), "->", show(f), "  |b|=", len(f))
