import numpy as np, sys
sys.path.insert(0,'work')
from sumtest import member, in_set
IA=np.array([(0,10),(30,40),(120,130),(140,150),(250,270),(280,290)],dtype=float)
IB=np.array([(90,110),(180,190),(210,230),(300,310),(330,350)],dtype=float)
th, ph = 35.0, 95.0
w = np.exp(1j*np.radians(th))+np.exp(1j*np.radians(ph))
print("w =", w, " |w| =", abs(w))
r=abs(w); beta=np.degrees(np.arccos(r/2)); argw=np.angle(w,deg=True)
print("r",r,"beta_deg",beta,"argw",argw)
for s in (1,-1):
    t=argw+s*beta; u=np.exp(1j*np.radians(t)); v=w-u
    print("  s",s,"theta'",t,"|v|",abs(v),"arg v",np.angle(v,deg=True), "inA?",bool(in_set(np.array([t]),IA)), "inB?",bool(in_set(np.array([np.angle(v,deg=True)]),IB)))
print("member:", member(np.array([w]),IA,IB))
print("IA dtype/shape", IA.dtype, IA.shape)
