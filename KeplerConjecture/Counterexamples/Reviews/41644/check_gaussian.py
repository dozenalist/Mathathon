"""Audit the submitted rational Gaussian handoff with an explicit feasible point."""
import importlib.util
import json
from pathlib import Path
import sys
import time
import numpy as np
from scipy.optimize import linprog
import scipy
import sympy as sp

HERE=Path(__file__).resolve().parent
SOURCE=HERE / 'source'
sys.path.insert(0,str(SOURCE))
import ce_exact_gauss as G
import x_r01_driver as D

start=time.monotonic()
P=2-sp.Rational(2,3)*G.s_
Q=G.apply_map(P)
assert sp.expand(Q-(1+sp.Rational(2,3)*G.v_)) == 0
AP,S,AQ,V,p0,q0=D.build(6)
coeff=np.array([2.,-2./3.,0.,0.,0.,0.,0.])
eps=1e-9
A=np.vstack([AP,-AQ])
b=np.concatenate([np.full(len(AP),-eps),np.zeros(len(AQ))])
raw=linprog(p0,A_ub=A,b_ub=b,A_eq=q0.reshape(1,-1),b_eq=[1.],bounds=[(None,None)]*7,method='highs')
data={
 'source_commit':'87db0319217b99eafd66d96fff0e9ab75caa2127',
 'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'sympy':sp.__version__,
 'exact_feasible_P':str(P),'exact_feasible_Q':str(Q),
 'proof':'For s>=4, P(s)<=-2/3; for v>=0, Q(v)>=1; Q(0)=1.',
 'minimum_grid_slack':float(np.min(b-A@coeff)),
 'normalization_value':float(q0@coeff),
 'max_abs_matrix_entry':float(np.max(np.abs(A))),
 'raw_solver_status':int(raw.status),'raw_solver_success':bool(raw.success),'raw_solver_message':raw.message,
 'correct_density_formula':'(4/(3*sqrt(pi)))*P(0)/Q(0)',
 'submitted_density_formula':'(4*sqrt(pi)/3)*P(0)/Q(0)',
 'submitted_over_correct_factor':'pi',
 'correct_kepler_comparison':'32*P(0)^2 < pi^3*Q(0)^2, assuming positive P(0), Q(0)',
 'elapsed_seconds':round(time.monotonic()-start,3),
}
(HERE/'audit.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
print(json.dumps(data,indent=2))
assert data['minimum_grid_slack']>0 and abs(data['normalization_value']-1)<1e-12
