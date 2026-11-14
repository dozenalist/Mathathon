import sys
sys.path.insert(0,'work')
from solve import solve
from csp import *
names={(1,3):'A',(1,4):'B',(1,5):'C',(2,4):'D',(2,5):'E',(3,5):'F'}
for m in [5,6,7,8,9,10,11,12]:
    w,nc,st=solve(m,sizes=(2,),timeout=60)
    print("m",m,st)
    print("  ","".join(names[tuple(sorted(S))] for S in w))
