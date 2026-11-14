"""Search for 7-cliques in conflict graphs G(Lambda, S) where S is a set of
squared lattice distances.  Output: explicit 7-point witnesses."""
import networkx as nx
from itertools import combinations

def N(a,b): return a*a-a*b+b*b
def find_cliques(S, K=30):
    verts=[(a,b) for a in range(-12,13) for b in range(-12,13) if N(a,b)<=K]
    idx={}
    G=nx.Graph()
    for a,b in verts: G.add_node((a,b))
    for (a,b) in verts:
        for (c,d) in verts:
            if (a,b)<(c,d):
                if N(a-c,b-d) in S: G.add_edge((a,b),(c,d))
    cl=nx.find_cliques(G)
    best=[]
    for c in cl:
        if len(c)>len(best): best=c
    return len(best), sorted(best)

for S in [{3,4},{3,4,7},{3,4,7,9},{4,7,9},{7,9},{7,9,12},{7,9,12,13},{9,12,13},{9,12,13,16},
          {12,13,16},{12,13,16,19},{13,16,19},{16,19,21},{16,19,21,25},{1,3,4}]:
    m,c = find_cliques(sorted(S))
    print(f"S = {sorted(S)}:  max clique = {m}")
    if m>=7:
        print("   witness:", c[:8] if len(c)>=8 else c)
        continue
