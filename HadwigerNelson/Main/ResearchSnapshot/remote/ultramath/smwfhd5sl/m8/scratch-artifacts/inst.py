import numpy as np
def decompose(w):
    w=complex(w); a=abs(w)
    h=np.sqrt(max(0.0,1-(a/2)**2)); u=w/a
    return (a/2*u+1j*h*u, a/2*u-1j*h*u)
for d in [1, 1j, np.exp(1j*0.7), np.exp(1j*2.3)]:
    for f in [np.exp(1j*0.3), 1j, (-0.4+0.9165j)/abs(-0.4+0.9165j)]:
        f=f/abs(f); w=d+f
        s,t=decompose(w)
        print(f"d={d:.4f} f={f:.4f} s={s:.6f} t={t:.6f} s==f:{abs(s-f)<1e-9} t==d:{abs(t-d)<1e-9}")
