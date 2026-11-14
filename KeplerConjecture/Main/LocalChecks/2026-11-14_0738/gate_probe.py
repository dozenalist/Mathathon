import sys,json
from fractions import Fraction as F
sys.path.insert(0,'Experimental/scripts')
from cell_certificate import origin_interior_certificate, radius_witness, polytope_volume
axes=[(F(1),F(0),F(0)),(F(0),F(1),F(0)),(F(0),F(0),F(1))]
cube=axes+[tuple(-x for x in p) for p in axes]
assert origin_interior_certificate(axes)[0] is False
assert origin_interior_certificate(cube)[0] is True
c=radius_witness(cube)[0]
assert c>0 and 3*c*c<=1
vol=polytope_volume(cube,[F(1)]*6)[0]
assert vol==8
dup=polytope_volume(cube+[cube[0]],[F(1)]*7)[0]
print(json.dumps({'positive_axes_rejected':True,'cube_volume':str(vol),'radius_lower':str(c),'radius_squared_le_one_third':True,'duplicate_face_volume':str(dup),'duplicate_face_invariant':dup==vol},indent=2))
