from fast import ok
import collections
seen=collections.Counter(); ex={}
for a2 in range(5,360,10):
 for a3 in range(5,360,10):
  for a4 in range(5,360,10):
   for a5 in range(5,360,10):
    al=[0,0,a2,a3,a4,a5]
    if len(set(al))!=5: continue
    if not ok(al): continue
    order=tuple(sorted([2,3,4,5], key=lambda i: al[i]))
    seen[order]+=1; ex.setdefault(order,(a2,a3,a4,a5))
for o,c in seen.most_common():
    print(o,c,ex[o])
print('orders seen:',len(seen))
