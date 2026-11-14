import sys
sys.path.insert(0, "/workspace/nucleus/work/projects/p-9021becf3f0d47a89b3f3c794c1e872b/repo/RogersRamanujan/Computation")
from bz82 import pi_forward
from rr_core import T, Tinv

def show(p): return "(" + ",".join(map(str,p)) + ")"
def cshow(p):
    # compress runs: 1,1,1,1 -> 1^4  (only for readable output)
    out=[]; i=0
    while i < len(p):
        j=i
        while j+1 < len(p) and p[j+1]==p[i]: j+=1
        if j-i+1 >= 3: out.append("%d^%d" % (p[i], j-i+1))
        else: out.extend([str(x) for x in p[i:j+1]])
        i=j+1
    return "(" + ",".join(out) + ")"

for s in range(1, 41):
    lam = tuple([1]*s)
    b, tr = pi_forward(lam)
    print("s=%2d steps=%d" % (s, len(tr)-1))
    for k,st in enumerate(tr):
        print("    %s %-4s %s" % (["phi","psi "][k%2] if k < len(tr)-1 else "END ", "j=%d"%st[0], cshow(st[1])))
