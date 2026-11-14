"""Independent exact matrix and geometry-input checks, reusing reviewed arithmetic."""
import ast,sys,json,importlib.util
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;root=Path(sys.argv[1]);R=sp.Rational;s,v=sp.symbols('s v')
tree=ast.parse((HERE.parent/'2026-11-14_0353/independent_checks.py').read_text(encoding='utf-8'))
defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('transform','psd','atan_bounds')]
exec(compile(ast.Module(defs,type_ignores=[]),'independent_arithmetic','exec'),globals())
al,ah=atan_bounds(5,50);bl,bh=atan_bounds(239,15);pi_lo=16*al-4*bh
d=json.loads((root/'Counterexamples/X_C017_small.json').read_text())
G,A,B=[sp.Matrix([[R(c) for c in row] for row in d[key]]) for key in ('G','A','B')]
assert all(psd(M) for M in (G,A,B))
m,S=d['m'],d['S'];vs=sp.Matrix([(s/S)**i for i in range(m+1)]);vv=sp.Matrix([(v/S)**i for i in range(m+1)])
P=sp.expand(-(s-4)*(vs.T*G*vs)[0]);Q=transform(P)
assert sp.expand(Q-(vv.T*A*vv)[0]-v*(vv.T*B*vv)[0])==0
ratio=P.subs(s,0)/Q.subs(v,0);assert P.subs(s,0)>0 and Q.subs(v,0)>0
bound=R('0.782267254857');assert 16*ratio**2<9*pi_lo*bound**2
print('SMALL CERTIFICATE: exact PSD and independent Fourier identity PASS; density < 0.782267254857')
print('density approx:',sp.N(R(4,3)*ratio/sp.sqrt(sp.pi),25),'max rational characters:',max(len(str(x)) for M in (G,A,B) for x in M))
sys.path.insert(0,str(root/'Computation'));import cut_flow as C
V=(15+7*sp.sqrt(5))/4*(2/sp.sqrt(R(5,2)+11*sp.sqrt(5)/10))**3
assert bool(R(C.V_DOD_LO)<V<R(C.V_DOD_HI));print('DODECAHEDRON exact interval: PASS')
assert len(C.build_13(R('2.1029'))[1])==12
assert len(C.build_13(R('2.103'))[1])==42
print('RING edge threshold controls: PASS')
sites,period=C.build_fcc_patch(1);assert len(sites)==1;print('FCC constructor: PASS')
assert not C.validate_icos_fixture()['V4_saturated'];print('SPARSE FIXTURE explicitly unsaturated: PASS')
print('These controls do not certify every flow verdict or the new geometric theorems.')
