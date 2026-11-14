import numpy as np
from scipy.optimize import minimize
pi=np.pi
# piece: type 'V' (t in I1,u in I2) or 'H' (t in I2,u in I3); csplit: None or ('s',pm) or ('a',pm)
class Pc:
    def __init__(self,typ,c=None,neg=False):
        self.typ=typ; self.c=c; self.neg=neg
    def box(self):
        return ((-pi/2,-pi/6),(pi/6,pi/2)) if self.typ=='V' else ((pi/6,pi/2),(pi/2,5*pi/6))
    def point(self,t,u):
        p=np.array([np.cos(t)+np.cos(u),np.sin(t)+np.sin(u)])
        return -p if self.neg else p
    def cons(self):
        # returns list of functions x->value >=0 meaning feasible
        (lo1,hi1),(lo2,hi2)=self.box()
        f=[]
        if self.c is not None:
            kind,pm=self.c
            if kind=='s':   # (t-u)/2
                if pm>0: f.append(lambda x: (x[0]-x[1])/2 + pi/3)   # s >= -pi/3
                else:    f.append(lambda x: -((x[0]-x[1])/2 + pi/3)) # s <= -pi/3
            else:           # (t+u)/2 - pi/2
                if pm>0: f.append(lambda x: (x[0]+x[1])/2 - pi/2)
                else:    f.append(lambda x: -((x[0]+x[1])/2 - pi/2))
        return f
    def bounds(self):
        (lo1,hi1),(lo2,hi2)=self.box()
        return [(lo1,hi1),(lo2,hi2)]
    def sample(self,n,seed=0):
        rng=np.random.default_rng(seed)
        (lo1,hi1),(lo2,hi2)=self.box()
        pts=[];pars=[]
        for _ in range(n):
            t=lo1+(hi1-lo1)*rng.random(); u=lo2+(hi2-lo2)*rng.random()
            ok=all(g(np.array([t,u]))>=0 for g in self.cons())
            if ok: pts.append(self.point(t,u)); pars.append((t,u))
        return np.array(pts),np.array(pars)

def mindist(A,B,n=40,tries=60,seed=3):
    rng=np.random.default_rng(seed)
    pa,_=A.sample(4000,seed); pb,_=B.sample(4000,seed+1)
    from scipy.spatial import cKDTree
    tr=cKDTree(pb); d,idx=tr.query(pa)
    order=np.argsort(d)[:tries]
    best=(1e9,None)
    bA=A.bounds(); bB=B.bounds()
    ca=[{'type':'ineq','fun':g} for g in A.cons()]
    cb=[{'type':'ineq','fun':g} for g in B.cons()]
    def f(x):
        return np.sum((A.point(x[0],x[1])-B.point(x[2],x[3]))**2)
    for k in order:
        x0=np.array([pa[k,0],pa[k,1],pb[idx[k],0],pb[idx[k],1]])
        r=minimize(f,x0,method='SLSQP',bounds=bA+bB,constraints=ca+cb,options={'ftol':1e-16,'maxiter':800})
        if r.fun<best[0]-1e-15: best=(r.fun,r.x)
    return np.sqrt(max(best[0],0)),best[1]

def diam(A,n=40,tries=40,seed=5):
    pts,pars=A.sample(4000,seed)
    from scipy.spatial import cKDTree
    tr=cKDTree(pts); d,idx=tr.query(pts)
    order=np.argsort(-d)[:tries]
    bA=A.bounds(); ca=[{'type':'ineq','fun':g} for g in A.cons()]
    def f(x): return -np.sum((A.point(x[0],x[1])-A.point(x[2],x[3]))**2)
    best=(1e9,None)
    for k in order:
        x0=np.array([pars[k,0],pars[k,1],pars[idx[k],0],pars[idx[k],1]])
        r=minimize(f,x0,method='SLSQP',bounds=bA+bA,constraints=ca+ca,options={'ftol':1e-16,'maxiter':800})
        if -r.fun<best[0]-1e-15: best=(-r.fun,r.x)
    return np.sqrt(max(best[0],0)),best[1]

def deg(x): return np.degrees(x)
PIECES={
 'V1':Pc('V',('s',-1)),'V4':Pc('V',('s',1)),
 'W1':Pc('V',('s',1),True),'W4':Pc('V',('s',-1),True),
 'H1':Pc('H',('a',-1)),'H4':Pc('H',('a',1)),
 'G1':Pc('H',('a',1),True),'G4':Pc('H',('a',-1),True),
}
if __name__=='__main__':
    import sys
    names1=['V1','W1','H1','G1']; names4=['V4','W4','H4','G4']
    for lab,names in (('colour1',names1),('colour4',names4)):
        print('===',lab)
        for i in range(4):
            for j in range(i+1,4):
                d,x=mindist(PIECES[names[i]],PIECES[names[j]])
                print(f"{names[i]}-{names[j]} inf={d:.9f}  params(deg)={np.round(deg(x),4)}")
    print('=== (a) V vs H, (b) H vs -H')
    V=Pc('V');H=Pc('H')
    d,x=mindist(V,H); print('V-H inf=',d,np.round(deg(x),4))
    d,x=mindist(H,Pc('H',None,True)); print('H-(-H) inf=',d,np.round(deg(x),4))
    print('=== diameters')
    for nm,p in [('V',V),('H',H),('V1',PIECES['V1']),('V4',PIECES['V4']),('H1',PIECES['H1']),('H4',PIECES['H4']),('W1',PIECES['W1']),('G1',PIECES['G1']),('W4',PIECES['W4']),('G4',PIECES['G4'])]:
        d,x=diam(p); print(nm,'diam=',d,np.round(deg(x),4))
