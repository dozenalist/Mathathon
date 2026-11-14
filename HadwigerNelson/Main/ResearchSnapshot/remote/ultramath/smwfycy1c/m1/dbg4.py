import sympy as sp
from itertools import combinations, product
k = sp.symbols('k')

def make(canon):
    def chrom(verts, edgelist):
        verts=tuple(verts)
        if canon:
            edgelist = tuple(sorted(set(tuple(sorted(e)) for e in edgelist)))
        else:
            edgelist = tuple(sorted(set(edgelist)))
        if not edgelist: return sp.Poly(sp.expand(k**len(verts)), k)
        a,b = edgelist[0]; rest = edgelist[1:]
        d = chrom(verts, rest)
        merged = tuple(v for v in verts if v != b)
        contr=[]
        for x,y in rest:
            x2 = a if x==b else x
            y2 = a if y==b else y
            if x2!=y2: contr.append((x2,y2))
        c = chrom(merged, contr)
        return sp.Poly(sp.expand(d.as_expr()-c.as_expr()), k)
    return chrom

good, bad = make(True), make(False)
n=4
allpairs=list(combinations(range(n),2))
for r in range(0, len(allpairs)+1):
    for sub in combinations(allpairs, r):
        # oriented at random to exercise the bug: use only original orientation here
        pg = good(list(range(n)), list(sub)); pb = bad(list(range(n)), list(sub))
        if sp.expand(pg.as_expr()-pb.as_expr()) != 0:
            print("MISMATCH on", sub)
            print("  canon:", sp.expand(pg.as_expr()))
            print("  plain:", sp.expand(pb.as_expr()))
            raise SystemExit
print("no mismatch over all 4-vertex graphs with original orientation")
