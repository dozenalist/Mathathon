import sys, time
sys.path.insert(0, "/workspace/nucleus/work/projects/p-9021becf3f0d47a89b3f3c794c1e872b/repo/RogersRamanujan/Computation")
from bz82 import pi_forward
from rr_core import Tinv

def show(p): return "(" + ",".join(map(str,p)) + ")"
print("=== (1^s): B-endpoint b, D-image, steps")
t0=time.time()
for s in range(0, 61):
    lam = tuple([1]*s)
    b, tr = pi_forward(lam)
    print("s=%2d b=%-30s D=%-28s steps=%d" % (s, show(b), show(Tinv(b)), len(tr)-1))
print("elapsed %.2fs" % (time.time()-t0))
