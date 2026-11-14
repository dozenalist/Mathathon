import re,sys,collections
lines=[l.split() for l in open('imports.txt')]
file={};imps={}
for t in lines:
    file[t[0]]=t[1]; imps[t[0]]=t[2:]
def lines_of(p):
    return sum(1 for _ in open('/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/'+p))
nlines={m:lines_of(file[m]) for m in file}
# reverse reachability
rev=collections.defaultdict(set)
for m,ii in imps.items():
    for i in ii:
        rev[i].add(m)
# roots = modules imported by nothing? find top-level consumers
allimps=set()
for ii in imps.values(): allimps.update(ii)
roots=[m for m in file if m not in allimps]
print("ROOTS (imported by nothing):")
for r in roots: print("  ",r, nlines[r])
def closure(seed):
    seen=set();stack=[seed]
    while stack:
        m=stack.pop()
        if m in seen: continue
        seen.add(m)
        stack.extend(imps.get(m,[]))
    return seen
def rclosure(seed):
    seen=set();stack=[seed]
    while stack:
        m=stack.pop()
        if m in seen: continue
        seen.add(m)
        stack.extend(rev.get(m,()))
    return seen
for t in ['OAI.MeasureTheory.CompactFactors.ConditionalLimits','OAI.MeasureTheory.CompactFactors.Approximation','OAI.MeasureTheory.CompactFactors.Stationary']:
    d=closure(t); u=rclosure(t)
    d2=[m for m in d if m in nlines]
    print(f"\n{t}: deps={len(d2)} lines={sum(nlines[m] for m in d2)}")
    print("   importers (upward closure):", sorted(u))
