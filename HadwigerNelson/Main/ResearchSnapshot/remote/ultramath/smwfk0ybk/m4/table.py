from fractions import Fraction as F
from math import sqrt
import json
from q3 import Q3, q3, ONE
from cellbar import reachable, offsets_within, form
from verify import max_clique, chi_induced

def min_coset_index(rnum, mmax=40):
    r=q3(rnum); target=((ONE+Q3(2)*r)*(ONE+Q3(2)*r)/(Q3(3)*r*r)).float()
    from cellbar import max_min_norm_by_index
    m,_=max_min_norm_by_index(mmax)
    for k in sorted(m):
        if m[k]>target: return k, target
    return None, target

rows=[]
for rnum in [F(1,20),F(1,10),F(1,8),F(3,20),F(1,5),F(1,4),F(267,1000),F(27,100),F(3,10),F(7,20),F(19,50),F(2,5),F(9,20),F(49,100)]:
    cl,_,n = max_clique(rnum, cap=12)
    ci,nv,tr = chi_induced(rnum)
    k,tgt = min_coset_index(rnum)
    rows.append(dict(r=str(rnum), rf=round(float(rnum),4), offsets=n, clique=cl,
                     chi_induced=ci, vertices=nv, truncated=tr, coset_index=k,
                     exact=(k is not None and ci==k), gap=None if k is None else k-ci))
    print(rows[-1], flush=True)
json.dump(rows, open("table_results.json","w"), indent=1)
