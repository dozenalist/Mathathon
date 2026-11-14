import sympy as sp
k = sp.symbols('k')
def chrom(verts, edgelist):
    verts=tuple(verts); edgelist = tuple(sorted(set(tuple(sorted(e)) for e in edgelist)))
    if not edgelist:
        return sp.Poly(sp.expand(k**len(verts)), k)
    a,b = edgelist[0]
    rest = edgelist[1:]
    d = chrom(verts, rest)
    merged = tuple(v for v in verts if v != b)
    contr=[]
    for x,y in rest:
        x2 = a if x==b else x
        y2 = a if y==b else y
        if x2!=y2: contr.append((x2,y2))
    c = chrom(merged, contr)
    return sp.Poly(sp.expand(d.as_expr()-c.as_expr()), k)

cases = {
 "isolated + triangle": ([0,1,2,3],[(1,2),(1,3),(2,3)]),
 "triangle": ([0,1,2],[(0,1),(1,2),(0,2)]),
 "path with iso": ([0,1,2],[(0,1)]),
 "K4-e diamond": ([0,1,2,3],[(0,2),(0,3),(1,2),(1,3),(2,3)]),
 "K4": ([0,1,2,3],[(i,j) for i in range(4) for j in range(i+1,4)]),
}
for n,(v,e) in cases.items():
    print(f"{n:20s}", sp.expand(chrom(v,e).as_expr()))
print("expected iso+tri: k**2*(k-1)*(k-2) =", sp.expand(k**2*(k-1)*(k-2)))
print("expected K4-e   :", sp.expand(k*(k-1)*(k-2)**2))
