import numpy as np
from scipy.spatial import cKDTree
from scipy.optimize import minimize
pi=np.pi
I1=(-pi/2,-pi/6); I2=(pi/6,pi/2); I3=(pi/2,5*pi/6)
def pt(t,u): return np.stack([np.cos(t)+np.cos(u), np.sin(t)+np.sin(u)],-1)
Pcs={
 'V1':(I1,I2,lambda t,u: (t-u)/2 <= -pi/3,False),
 'V4':(I1,I2,lambda t,u: (t-u)/2 >= -pi/3,False),
 'W1':(I1,I2,lambda t,u: (t-u)/2 >= -pi/3,True),
 'W4':(I1,I2,lambda t,u: (t-u)/2 <= -pi/3,True),
 'H1':(I2,I3,lambda t,u:(t+u)/2<=pi/2,False),
 'H4':(I2,I3,lambda t,u:(t+u)/2>=pi/2,False),
 'G1':(I2,I3,lambda t,u:(t+u)/2>=pi/2,True),
 'G4':(I2,I3,lambda t,u:(t+u)/2<=pi/2,True),
}
N=500
np.random.seed(1)
S={}
for k,((l1,h1),(l2,h2),cf,neg) in Pcs.items():
    t=l1+(h1-l1)*np.random.rand(N*N); u=l2+(h2-l2)*np.random.rand(N*N)
    m=cf(t,u); t,u=t[m],u[m]; p=pt(t,u)
    if neg: p=-p
    S[k]=(p,np.stack([t,u],-1))
def mind(a,b):
    pa,ta=S[a]; pb,tb=S[b]
    tr=cKDTree(pb); d,j=tr.query(pa)
    i=np.argmin(d)
    return d[i],ta[i],tb[j[i]]
names1=['V1','W1','H1','G1']; names4=['V4','W4','H4','G4']
def deg(x): return np.degrees(x)
for lab,names in (('c1',names1),('c4',names4)):
    print('---',lab)
    for i in range(4):
        for j in range(i+1,4):
            d,ta,tb=mind(names[i],names[j])
            print(f"{names[i]}-{names[j]} d={d:.7f} deg t1,u1,t2,u2 = {deg(ta[0]):.3f},{deg(ta[1]):.3f},{deg(tb[0]):.3f},{deg(tb[1]):.3f}")
VA=np.vstack([S['V1'][0],S['V4'][0]]); HB=np.vstack([S['H1'][0],S['H4'][0]]); GB=np.vstack([S['G1'][0],S['G4'][0]])
tr=cKDTree(HB); d,j=tr.query(VA); print('V-H min',d.min())
tr=cKDTree(GB); d,j=tr.query(HB); print('H--H min',d.min())
for nm,A in [('V',VA),('H',HB),('Vneg',-VA),('Hneg',-HB),('V1',S['V1'][0]),('V4',S['V4'][0]),('H1',S['H1'][0]),('H4',S['H4'][0]),('W1',S['W1'][0]),('G1',S['G1'][0])]:
    tr=cKDTree(A); d,j=tr.query(A); print('diam',nm,round(d.max(),7))
