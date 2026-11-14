import sys
sys.path.insert(0, "/workspace/nucleus/work/projects/p-9021becf3f0d47a89b3f3c794c1e872b/repo/RogersRamanujan/Computation")
from bz82 import phi, psi, state_weight
print("phi(-2;(5)) =", phi((-2,(5,))), " wt", state_weight((-2,(5,))))
print("phi(0;(1,1,1,1,1)) =", phi((0,(1,)*5)))
print("psi((-1,(13,))) =", psi((-1,(13,))))
print("psi((-1,(8,))) =", psi((-1,(8,))))
print("phi((-2,(0,)))  skip")
print("psi((-1,(3,))) =", psi((-1,(3,))))
print("psi((-1,(1,))) =", psi((-1,(1,))))
print("phi((-1,(1,)*8)) =", phi((-1,(1,)*8)))
print("psi((0,(3,)+(1,)*8)) =", psi((0,(3,)+(1,)*8)))
print("psi((-1,(6,2))) =", psi((-1,(6,2))))
print("phi((-1,(11,2))) =", phi((-1,(11,2))))
