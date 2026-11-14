import json,sys
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(Path(sys.argv[1]) if len(sys.argv)>1 else ROOT.parents[2]/'Computation'))
import cut_flow as C
out={}
b=list(map(F,[-1,-1,-1,-1,1]));edges=[(0,1),(1,2),(2,3)]
cap,divok,div=C.verify_flow_exact(b,edges,F(1),{})
cut=C.find_violating_cut(b,edges,F(1));flow=C.feasible_flow(b,edges,F(1))
assert not divok and len(div)==5 and cut is not None and flow is None
assert not C.verify_flow_exact([F(1)],[],F(0),{})[1]
assert C.feasible_flow([F(1)],[],F(0)) is None
out['flow_repair']={'isolated_positive_rejected':True,'edgeless_positive_rejected':True,'violating_cut':str(cut),'scan_isolated':str(C.exhaustive_cut_scan(b,edges)),'scan_edgeless':str(C.exhaustive_cut_scan([F(1)],[])),'scan_all_negative':str(C.exhaustive_cut_scan([F(-1),F(-1)],[(0,1)]))}
sys.path.insert(0,str(Path(sys.argv[2]) if len(sys.argv)>2 else ROOT.parents[2]/'Experimental/scripts'))
import rigorous_cell_volume as E
from rational_interval import Iv
n0=[F(1),F(0),F(0)];n=[F(3,5),F(4,5),F(0)];y=[F(-4,9),F(8,9),F(0)]
dn=[a-b for a,b in zip(n,n0)];e=max(map(abs,dn));dot=sum(a*b for a,b in zip(y,dn))
assert sum(t*t for t in n)==sum(t*t for t in n0)==1
assert sum(t*t for t in y)<1 and dot>e
out['norm_bound_counterexample']={'n0':list(map(str,n0)),'n':list(map(str,n)),'y':list(map(str,y)),'R':'1','component_error':str(e),'dot':str(dot),'y_norm_squared':str(sum(t*t for t in y)),'claimed_upper':str(e)}
centres=[(2,0,0),(-2,0,0),(0,2,0),(0,-2,0),(0,0,-2)]
vals=E.sandwich([tuple(Iv(x) for x in p) for p in centres],F(2))
out['unbounded_cell_false_enclosure']={'centres':centres,'R':'2','reported_lower':str(vals[0]),'reported_upper':str(vals[1]),'vertex_counts':list(vals[2:]),'recession_ray':[0,0,1],'true_volume':'infinite','reported_upper_float':float(vals[1])}
print(json.dumps(out,indent=2));(ROOT/'independent_probes.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
