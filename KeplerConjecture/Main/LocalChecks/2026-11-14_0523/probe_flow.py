import sys,json
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parent
source=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT.parents[2]/'Computation'
sys.path.insert(0,str(source))
import cut_flow as c
cases=[('isolated_positive',list(map(F,[-1,-1,-1,-1,1])),[(0,1),(1,2),(2,3)]),('edgeless_positive',[F(1)],[]),('all_negative',[F(-1),F(-1)],[(0,1)])]
out=[]
for name,b,edges in cases:
    r={'name':name,'b':[str(x) for x in b],'edges':edges}
    for label,fn in [('verify_zero',lambda:c.verify_flow_exact(b,edges,F(1),{})),('violating_cut',lambda:c.find_violating_cut(b,edges,F(1))),('feasible_flow',lambda:c.feasible_flow(b,edges,F(1))),('scan',lambda:c.exhaustive_cut_scan(b,edges))]:
        try:r[label]=str(fn())
        except Exception as e:r[label]=type(e).__name__+': '+str(e)
    out.append(r)
print(json.dumps(out,indent=2))
(ROOT/'flow_probe.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
assert out[0]['verify_zero'].startswith('(True, True,')
assert out[1]['verify_zero'].startswith('(True, True,')
print('FALSE ACCEPT REPRODUCED on actual a25f5be; positive isolated deficit is mathematically infeasible.')
