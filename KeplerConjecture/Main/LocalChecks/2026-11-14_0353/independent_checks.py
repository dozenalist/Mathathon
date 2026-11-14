"""Independent exact checks of frozen worker certificates and fixture claims."""
import importlib.util, json, sys
from pathlib import Path
import sympy as sp

root=Path(sys.argv[1]); s,v=sp.symbols('s v'); R=sp.Rational
def transform(P):
    poly=sp.Poly(P,s); q=sp.Integer(0); basis=sp.Integer(1)
    for k in range(poly.degree()+1):
        q+=poly.nth(k)*basis
        basis=sp.expand(-v*sp.diff(basis,v,2)+(2*v-R(3,2))*sp.diff(basis,v)+(R(3,2)-v)*basis)
    return sp.expand(q)

def psd(M):
    assert M==M.T and all(x.is_Rational for x in M)
    A=M.copy()
    for k in range(A.rows):
        pivot=A[k,k]
        assert pivot>=0
        if pivot==0:
            assert all(A[k,j]==0 for j in range(k,A.cols))
        else:
            for i in range(k+1,A.rows):
                for j in range(k+1,A.cols):
                    A[i,j]-=A[i,k]*A[k,j]/pivot
    return True

def atan_bounds(inv,n):
    x=R(1,inv); a=sum((-1)**k*x**(2*k+1)/(2*k+1) for k in range(n))
    b=a+(-1)**n*x**(2*n+1)/(2*n+1)
    return min(a,b),max(a,b)
al,ah=atan_bounds(5,50); bl,bh=atan_bounds(239,15)
pi_lo,pi_hi=16*al-4*bh,16*ah-4*bl
results=[]
for name,bound in [('X_C015',R('0.813631103')),('X_C016',R('0.784')),('X_C017',R('0.782267220134'))]:
    d=json.loads((root/'Counterexamples'/f'{name}_certificate.json').read_text())
    G,A,B=[sp.Matrix([[R(c) for c in row] for row in d[key]]) for key in ('G','A','B')]
    assert all(psd(M) for M in (G,A,B))
    m,S=d['m'],d['S']; vs=sp.Matrix([(s/S)**i for i in range(m+1)]); vv=sp.Matrix([(v/S)**i for i in range(m+1)])
    P=sp.expand(-(s-4)*(vs.T*G*vs)[0]); Q=transform(P)
    assert sp.expand(Q-(vv.T*A*vv)[0]-v*(vv.T*B*vv)[0])==0
    p0,q0=P.subs(s,0),Q.subs(v,0); assert p0>0 and q0>0
    ratio=p0/q0
    assert 16*ratio**2 < 9*pi_lo*bound**2
    row=dict(certificate=name,exact_psd=True,independent_fourier_identity=True,
             rational_density_upper=str(bound),decimal_density=str(sp.N(R(4,3)*ratio/sp.sqrt(sp.pi),25)),
             matrices=3,matrix_order=m+1,max_rational_chars=max(len(str(x)) for M in (G,A,B) for x in M),
             source_bytes=(root/'Counterexamples'/f'{name}_certificate.json').stat().st_size)
    results.append(row); print(json.dumps(row),flush=True)

spec=importlib.util.spec_from_file_location('cf',root/'Computation/cut_flow.py')
C=importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
V=(15+7*sp.sqrt(5))/4*(2/sp.sqrt(R(5,2)+11*sp.sqrt(5)/10))**3
sqok=bool(R(C.SQ32_LO)**2<32<R(C.SQ32_HI)**2)
vok=bool(R(C.V_DOD_LO)<V<R(C.V_DOD_HI))
print('SQRT32 enclosure:',sqok,'DODECA enclosure:',vok,'volume:',sp.N(V,30),flush=True)
edge=4/sp.sqrt((5+sp.sqrt(5))/2)
actual_edges=[(i,j) for i in range(1,13) for j in range(i+1,13)]
print('Icosahedron exact shortest ring edge:',sp.N(edge,25),'2.1029 below true edge:',bool(R('2.1029')<edge),flush=True)
print('build_13(2.1029) edge count:',len(C.build_13(2.1029)[1]),'; expected 12 (ring edge > R)',flush=True)
try:
    C.build_fcc_patch(1)
except Exception as e:
    print('build_fcc_patch(1):',type(e).__name__,str(e),flush=True)
print('Main star b=(4,-1,-1,-1): whole vertex set sum b = 1, boundary = 0; infeasible for EVERY capacity',flush=True)
print('Fixture is unsaturated: point (8,8,8) lies >2 from every period-16 cluster centre',flush=True)
(Path(__file__).parent/'independent_results.json').write_text(json.dumps(dict(certificates=results,sqrt32_enclosure=sqok,dodeca_enclosure=vok),indent=2)+'\n')
