import json,sys,itertools
from pathlib import Path
from fractions import Fraction as F
R=Path(__file__).resolve().parent
C=Path(sys.argv[1]) if len(sys.argv)>1 else R.parents[2]/'Computation';sys.path.insert(0,str(C))
import cut_flow as CF
d=json.loads((C/'out/fixture_dense_shell.json').read_text())
p=[tuple(map(F,q)) for q in d['coordinates']];vol=list(map(F,d['cell_volumes_exact']));lo=list(map(F,d['b_lo']));hi=list(map(F,d['b_hi']));edges=list(map(tuple,d['edges']))
assert len(p)==13 and sum(vol)==512 and vol[0]<CF.SQ32_LO
# All coordinates are in [-2,2]; a nonzero period-8 shift has at least one
# coordinate of the difference >=4. Therefore same-cell pairs suffice for
# the separation-2 check and radius-2.001 graph.
assert all(abs(x)<2 for q in p for x in q)
dist=lambda a,b:sum((x-y)**2 for x,y in zip(a,b))
minimum=min(dist(a,b) for a,b in itertools.combinations(p,2));assert minimum>=4
actual=[(i,j) for i in range(13) for j in range(i+1,13) if dist(p[i],p[j])<=F(2001,1000)**2]
assert actual==edges==[(0,i) for i in range(1,13)]
assert all(lo[i]==CF.SQ32_LO-vol[i] and hi[i]==CF.SQ32_HI-vol[i] for i in range(13))
assert lo[0]>0 and all(hi[i]<0 for i in range(1,13))
# Independent exact star flow: send hi[0]/12 from each leaf into vertex 0.
cap=hi[0]/12;div=[hi[0]]+[-cap]*12
assert all(div[i]>=hi[i] for i in range(13))
# Every noncentral cut has nonpositive sum. If the centre and k>=1 leaves
# are selected, one leaf already exceeds its positive deficit in magnitude.
assert all(hi[0]+hi[i]<0 for i in range(1,13))
out=dict(source='926cdb709a29fff7ac8dfb4b72a03a2ca1af19c0',scope='exact legality, graph and flow using supplied volume data; volume recomputation separate',minimum_squared_separation=str(minimum),period=8,volume_sum=str(sum(vol)),central_volume=str(vol[0]),central_volume_float=float(vol[0]),central_deficit_interval=list(map(str,(lo[0],hi[0]))),threshold_interval=list(map(str,(lo[0]/12,hi[0]/12))),threshold_display=[float(lo[0]/12),float(hi[0]/12)],independent_star_flow_verified=True,central_volume_provenance='worker exact engine; independently recomputed by separate bounded job if completed')
(R/'fixture_probe.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(out,indent=2))
