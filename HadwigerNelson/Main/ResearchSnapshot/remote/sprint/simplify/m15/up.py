import collections
lines=[l.split() for l in open('imports.txt')]
file={};imps={}
for t in lines:
    file[t[0]]=t[1]; imps[t[0]]=t[2:]
def lines_of(p): return sum(1 for _ in open('/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/'+p))
nl={m:lines_of(file[m]) for m in file}
rev=collections.defaultdict(set)
for m,ii in imps.items():
    for i in ii: rev[i].add(m)
def up(m):
    seen=set();st=[m]
    while st:
        x=st.pop()
        for y in rev.get(x,()):
            if y not in seen and y in file: seen.add(y);st.append(y)
    return seen
CUT={'OAI.MeasureTheory.CompactFactors.Approximation','OAI.MeasureTheory.CompactFactors.ConditionalLimits'}
cand=[]
for m in file:
    u=up(m)|{m}
    if u <= CUT: cand.append(m)
print("modules only used by {Approximation, ConditionalLimits}:")
tot=0
for m in sorted(cand):
    tot+=nl[m]; print(f"  {nl[m]:6d}  {m}")
print("TOTAL deletable lines:",tot,"modules:",len(cand))
print()
print("upward closure of each module (size, and whether ⊆CUT):")
for m in sorted(file):
    u=up(m)|{m}
    print(f"  {nl[m]:6d} {len(u):3d} {m}  {'CUT' if u<=CUT else ''}")
