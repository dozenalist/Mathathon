import json,sys,itertools
from pathlib import Path
from fractions import Fraction as F
R=Path(__file__).resolve().parent
sys.path.insert(0,str(Path(sys.argv[1]) if len(sys.argv)>1 else R.parents[2]/'Experimental/scripts'))
import cell_certificate as E
n=[(F(1),F(0),F(0)),(F(0),F(1),F(0)),(F(0),F(0),F(1))]
v=E.origin_interior_certificate(n)
assert v[0] is True
pts=[p for p in itertools.product((-2,0,2),repeat=3) if 0<sum(x*x for x in p)<=8]
assert len(pts)==18
sep=min(sum((a-b)**2 for a,b in zip(p,q)) for p,q in itertools.combinations(pts+[(0,0,0)],2))
assert sep==4
out=dict(experimental_source='f502b9a596be376cff60179ccd569e588876ef25',false_origin_certificate=dict(normals=[[str(x) for x in p] for p in n],returned=[v[0],str(v[1]),v[2]],reason='all convex combinations have x+y+z=1, so origin is not even in the hull',polyhedron='x<=1,y<=1,z<=1; unbounded in (-1,-1,-1)',scope='false helper acceptance; full certify may still reject via its separate radius calculation'),nearcontact_degree_witness=dict(points=pts,min_squared_separation=sep,max_squared_radius=8,neighbours=18,conclusion='degree<=12 fails already at radius sqrt(8), which is below 3.4555'),at_most_faces=dict(reason='feasible classes for <=F faces are nested; infima are nonincreasing',scope='candidate volumes alone do not determine the infima'))
(R/'independent_probes.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,indent=2))