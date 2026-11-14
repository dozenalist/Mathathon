import numpy as np
from scipy.optimize import minimize
pi = np.pi
I1 = (-pi/2, -pi/6); I2 = (pi/6, pi/2); I3 = (pi/2, 5*pi/6)

def e(t):
    return np.stack([np.cos(t), np.sin(t)], axis=-1)

def pt(t,u):
    return e(t)+e(u)

# pieces: name -> (lo1,hi1,lo2,hi2, constraint fn(t,u)->bool mask, negate)
Pcs = {
 'V1': (I1,I2, lambda t,u: t-u <= -2*pi/3, False),
 'V4': (I1,I2, lambda t,u: t-u >= -2*pi/3, False),
 'W1': (I1,I2, lambda t,u: t-u >= -2*pi/3, True),
 'W4': (I1,I2, lambda t,u: t-u <= -2*pi/3, True),
 'H1': (I2,I3, lambda t,u: (t+u)/2 <= pi/2, False),
 'H4': (I2,I3, lambda t,u: (t+u)/2 >= pi/2, False),
 'G1': (I2,I3, lambda t,u: (t+u)/2 >= pi/2, True),
 'G4': (I2,I3, lambda t,u: (t+u)/2 <= pi/2, True),
}
N=400
def sample(name):
    (lo1,hi1),(lo2,hi2),cf,neg = Pcs[name]
    t = lo1 + (hi1-lo1)*np.random.rand(N*N)
    u = lo2 + (hi2-lo2)*np.random.rand(N*N)
    m = cf(t,u)
    t,u = t[m],u[m]
    p = pt(t,u)
    if neg: p = -p
    return p, np.stack([t,u],-1)

np.random.seed(0)
S = {k: sample(k) for k in Pcs}
for k in S: print(k, len(S[k][0]), S[k][0].min(0), S[k][0].max(0))

def mind(A,B):
    # sample based min
    best=(1e9,None,None)
    for i in range(0,len(A),1):
        d = np.linalg.norm(B-A[i],axis=1)
        j = np.argmin(d)
        if d[j]<best[0]: best=(d[j],A[i],B[j])
    return best

names1=['V1','W1','H1','G1']; names4=['V4','W4','H4','G4']
print("--- colour1 pairs ---")
for i in range(4):
    for j in range(i+1,4):
        a,b=names1[i],names1[j]
        d,pa,pb = mind(S[a][0],S[b][0])
        print(a,b,round(d,6),pa,pb)
print("--- colour4 pairs ---")
for i in range(4):
    for j in range(i+1,4):
        a,b=names4[i],names4[j]
        d,pa,pb = mind(S[a][0],S[b][0])
        print(a,b,round(d,6),pa,pb)
print("--- (a) V vs H ---")
VA=np.vstack([S['V1'][0],S['V4'][0]]); HB=np.vstack([S['H1'][0],S['H4'][0]])
d,pa,pb=mind(VA,HB); print('V,H',round(d,6),pa,pb)
print("--- (b) H vs -H ---")
d,pa,pb=mind(HB,np.vstack([S['G1'][0],S['G4'][0]])); print('H,-H',round(d,6),pa,pb)
print("--- (c) diameters ---")
import itertools
for nm,A in [('V',VA),('H',HB),('-V',-VA),('-H',-HB)]:
    dd=0;pp=None
    for i in range(0,len(A),7):
        d_=np.linalg.norm(A-A[i],axis=1); j=np.argmax(d_)
        if d_[j]>dd: dd=d_[j];pp=(A[i],A[j])
    print(nm,round(dd,6),pp)
