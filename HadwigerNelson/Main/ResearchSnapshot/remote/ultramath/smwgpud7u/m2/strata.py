from fast import ok
# ---- 4-distinct: two disjoint adjacent collisions ----
# the 9 unordered pairs of disjoint adjacent index pairs (adjacent = {i,i+1})
pats=[]
for i in range(6):
    for j in range(i+1,6):
        Pi={i,(i+1)%6}; Pj={j,(j+1)%6}
        if Pi & Pj: continue
        pats.append((tuple(sorted(Pi)),tuple(sorted(Pj))))
found={}
for (P,Q) in pats:
    for a in range(10,360,10):
        for b in range(10,360,10):
            for c in range(10,360,10):
                al=[None]*6
                for i in P: al[i]=0
                for i in Q: al[i]=a
                rest=[i for i in range(6) if al[i] is None]
                al[rest[0]]=b; al[rest[1]]=c
                if len(set(al))!=4: continue
                if ok(al):
                    found.setdefault((P,Q),tuple(al)); break
            if (P,Q) in found: break
        if (P,Q) in found: break
for k,v in found.items(): print(k,v)
