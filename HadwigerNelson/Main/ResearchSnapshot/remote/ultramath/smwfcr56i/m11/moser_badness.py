import itertools
from fractions import Fraction as Fr
V=['0','A','B','T','uA','uB','uT']
E=[('0','A'),('0','B'),('A','B'),('T','A'),('T','B'),('uA','uB'),('0','uA'),('0','uB'),('uT','uA'),('uT','uB'),('T','uT')]
print("vertices",len(V),"edges",len(E))
best=None; hist={}
for col in itertools.product(range(3),repeat=len(V)):
    c=dict(zip(V,col))
    mono=sum(1 for a,b in E if c[a]==c[b])
    hist[mono]=hist.get(mono,0)+1
    if best is None or mono<best: best=mono
print("min monochromatic edges over all 3-colourings =",best)
print("distribution (mono edges -> #colourings):",dict(sorted(hist.items())))
print("chi(G)>=4:",best>=1)
beta=Fr(best,len(E))
print(f"beta(G) = {best}/{len(E)} = {beta} = {float(beta):.10f}")
# count colourings achieving the minimum
atmin=hist[best]
print("colourings attaining the minimum:",atmin)
# also: min number of mono edges for 4-colourings (=0) sanity
