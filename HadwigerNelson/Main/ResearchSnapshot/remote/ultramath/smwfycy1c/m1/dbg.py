import sympy as sp
from itertools import product
k = sp.symbols('k')
memo = {}
def chrom(verts, edgelist):
    edgelist = tuple(sorted(set(edgelist)))
    key = (tuple(sorted(verts)), edgelist)
    if key in memo: return memo[key]
    if not edgelist:
        res = sp.Poly(k**len(verts), k)
    else:
        a,b = edgelist[0]
        rest = edgelist[1:]
        d = chrom(verts, rest)
        merged = [v for v in verts if v != b]
        contr=[]
        for x,y in rest:
            x2 = a if x==b else x
            y2 = a if y==b else y
            if x2!=y2: contr.append((x2,y2))
        c = chrom(merged, contr)
        res = sp.Poly(sp.expand(d.as_expr()-c.as_expr()), k)
    memo[key]=res
    return res

print("K2      ", sp.expand(chrom([0,1],[(0,1)]).as_expr()), "expect k*(k-1)")
print("path3   ", sp.expand(chrom([0,1,2],[(0,1),(1,2)]).as_expr()), "expect k*(k-1)**2")
print("tri     ", sp.expand(chrom([0,1,2],[(0,1),(1,2),(0,2)]).as_expr()), "expect k(k-1)(k-2)")
print("K4      ", sp.expand(chrom([0,1,2,3],[(i,j) for i in range(4) for j in range(i+1,4)]).as_expr()))
print("C5      ", sp.expand(chrom([0,1,2,3,4],[(0,1),(1,2),(2,3),(3,4),(4,0)]).as_expr()), "expect (k-1)^5-(k-1)")
