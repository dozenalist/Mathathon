import sys
sys.path.insert(0,'work')
from csp import offsets
A,E,B,F,D,C = (frozenset(x) for x in [(1,3),(2,5),(1,4),(3,5),(2,4),(1,5)])
NAMES={A:'A',E:'E',B:'B',F:'F',D:'D',C:'C'}
H=[A,E,B,F,D,C]
ADJ={X:set(Y for Y in H if not (X&Y)) for X in H}
def prop(m, fix0, trace=False):
    n=6*m; offs=[o for o in offsets(m) if o%n!=0]
    dom={i:set(H) for i in range(n)}
    dom[0]={fix0}
    it=0
    while True:
        it+=1; changed=False
        for i in range(n):
            if len(dom[i])==0: return False,dom,it
            for o in offs:
                j=(i+o)%n
                # every value in dom[i] must be disjoint from some value in dom[j]:
                # i.e. for each X in dom[i], dom[j] & ADJ[X] nonempty
                for X in list(dom[i]):
                    if not (dom[j]&ADJ[X]):
                        dom[i].discard(X); changed=True
        if not changed: return all(len(dom[i])>0 for i in range(n)),dom,it
for m in (2,3,4,5,6):
    for start in (A,B,D,C):
        ok,dom,it=prop(m,start)
        print(f"m={m} w(0)={NAMES[start]}: propagation {'consistent' if ok else 'CONTRADICTION'} ({it} rounds); domain sizes {[len(dom[i]) for i in range(6*m)]}")
    print()
