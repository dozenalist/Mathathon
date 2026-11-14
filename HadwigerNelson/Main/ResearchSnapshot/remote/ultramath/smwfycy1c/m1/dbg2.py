import sympy as sp
k = sp.symbols('k')
def chrom(verts, edgelist, use_memo=True, memo=None):
    if memo is None: memo = {}
    edgelist = tuple(sorted(set(edgelist)))
    key = (tuple(sorted(verts)), edgelist)
    if use_memo and key in memo: return memo[key]
    if not edgelist:
        res = sp.Poly(k**len(verts), k)
    else:
        a,b = edgelist[0]
        rest = edgelist[1:]
        d = chrom(verts, rest, use_memo, memo)
        merged = [v for v in verts if v != b]
        contr=[]
        for x,y in rest:
            x2 = a if x==b else x
            y2 = a if y==b else y
            if x2!=y2: contr.append((x2,y2))
        c = chrom(merged, contr, use_memo, memo)
        res = sp.Poly(sp.expand(d.as_expr()-c.as_expr()), k)
    if use_memo: memo[key]=res
    return res

diamond = [(0,2),(0,3),(1,2),(1,3),(2,3)]
print("diamond nomemo", sp.expand(chrom([0,1,2,3],diamond,False).as_expr()))
print("diamond memo  ", sp.expand(chrom([0,1,2,3],diamond,True).as_expr()))
K4=[(i,j) for i in range(4) for j in range(i+1,4)]
print("K4 nomemo", sp.expand(chrom([0,1,2,3],K4,False).as_expr()))
print("K4 memo  ", sp.expand(chrom([0,1,2,3],K4,True).as_expr()))
