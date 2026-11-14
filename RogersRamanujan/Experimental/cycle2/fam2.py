import sys
sys.path.insert(0, "/workspace/nucleus/work/projects/p-9021becf3f0d47a89b3f3c794c1e872b/repo/RogersRamanujan/Computation")
from bz82 import forward, pi_forward
from rr_core import weight, T, Tinv

def show(p): return "(" + ",".join(map(str,p)) + ")"
def run(lam):
    b, tr = pi_forward(lam)
    return Tinv(b), b, len(tr)-1

print("=== (4^r) family")
for r in range(0, 13):
    lam = tuple([4]*r); n = 4*r
    d, b, L = run(lam)
    print("r=%2d n=%2d %-22s -> D %-24s B %-24s steps=%d" % (r, n, show(lam), show(d), show(b), L))

print("=== (4^r,1^s) family, r+s>0")
for r in range(0, 9):
    for s in range(0, 13):
        if r+s == 0: continue
        lam = tuple([4]*r + [1]*s); n = 4*r+s
        d, b, L = run(lam)
        print("r=%d s=%d n=%2d %-26s -> D %-28s steps=%d" % (r, s, n, show(lam), show(d), L))
