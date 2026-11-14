import copy,json,sys
from fractions import Fraction as F
sys.path.insert(0,'Computation')
import exact_volume as EV
planes=[(1,0,0,1),(-1,0,0,1),(0,1,0,1),(0,-1,0,1),(0,0,1,1),(0,0,-1,1)]
vol,cert=EV.certify_volume(planes,(F(0),F(0),F(0)))
assert vol==8 and EV.check_certificate(cert)==8
double=copy.deepcopy(cert);double['facets']*=2;double['volume']='16'
try:result=EV.check_certificate(double);double_result={'accepted':True,'volume':str(result)}
except ValueError as e:double_result={'accepted':False,'reason':str(e)}
omitted=copy.deepcopy(cert);omitted['planes'].append(['1','0','0','1/2'])
try:result=EV.check_certificate(omitted);omitted_result={'accepted':True,'volume':str(result),'true_volume':'6'}
except ValueError as e:omitted_result={'accepted':False,'reason':str(e)}
print(json.dumps({'original_cube_volume':str(vol),'doubled_facets':double_result,'unverified_non_candidate_cut':omitted_result},indent=2))
