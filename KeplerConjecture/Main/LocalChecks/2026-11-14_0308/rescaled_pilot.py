"""One frozen rescaled SDP instance; proposals remain pending independent checks."""
import json, sys
from pathlib import Path
import sympy as sp
sys.path.insert(0,str(Path.cwd()))
import x_r03b_rescaled as worker
out,msg=worker.sdp_R(5,8,solver='CLARABEL')
print('m=5 S=8 CLARABEL:',msg,flush=True)
records=[]
if out is not None:
    value,gram=out; print('solver objective',value,flush=True)
    for den in (10**6,10**9,10**12):
        qs=worker.qs_from_G(gram,5,8,den)
        result=worker.certify(qs)
        row=dict(denominator_cap=den,worker_accepted=result is not None)
        if result:
            row.update(ratio=str(result[0]),density_float=result[1],q=[[str(c) for c in sp.Poly(q,worker.s_).all_coeffs()] for q in qs])
        records.append(row); print(json.dumps(row),flush=True)
Path('pilot_m5_s8.json').write_text(json.dumps(dict(status='finite pilot; worker acceptance only',records=records),indent=2))
