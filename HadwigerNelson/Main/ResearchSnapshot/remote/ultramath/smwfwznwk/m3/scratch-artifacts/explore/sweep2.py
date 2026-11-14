"""Deviation sweep with sign-matched branch + interior-margin attainment of each offset."""
import numpy as np

def sweep(m, nf=241, nd=31, verbose=True):
    n=6*m; Delta=2*np.pi/n; d0=np.pi/(9*m)
    argf=(np.arange(nf)+0.5)*2*np.pi/nf
    arga=np.arange(nf)*2*np.pi/nf
    F1=np.stack([np.cos(argf),np.sin(argf)],1); A1=np.stack([np.cos(arga),np.sin(arga)],1)
    seen=set(); worst=0.0; minst=1e9; minfrac_dev=1e9; maxfrac_dev=-1e9
    for j in range(1,nd+1):
        d=d0*j/nd
        P=(F1[:,None,:]+d*A1[None,:,:]).reshape(-1,2); f=np.repeat(F1,nf,0)
        rho=np.linalg.norm(P,axis=1); ok=rho<=2; P,f,rho=P[ok],f[ok],rho[ok]
        h=np.sqrt(1-rho**2/4); perp=np.stack([-P[:,1],P[:,0]],1)/rho[:,None]
        for sgn in (1.0,-1.0):
            S=P/2+sgn*h[:,None]*perp; T=P-S
            ang=np.arctan2(S[:,1],S[:,0]); base=np.arctan2(f[:,1],f[:,0])
            dev=np.mod(ang-(base+sgn*np.pi/3)+np.pi,2*np.pi)-np.pi
            worst=max(worst,float(np.abs(dev).max()))
            minfrac_dev=min(minfrac_dev,float((dev/Delta).min())); maxfrac_dev=max(maxfrac_dev,float((dev/Delta).max()))
            cross=S[:,0]*T[:,1]-S[:,1]*T[:,0]; dot=(S*T).sum(1)
            minst=min(minst,float(np.abs(np.arctan2(cross,dot)).min()))
            i0=np.floor(base/Delta); i1=np.floor(ang/Delta)
            for jj in np.unique((i1-i0)%n): seen.add(int(jj))
    exp=sorted({(m+k)%n for k in (-1,0,1)}|{(-m+k)%n for k in (-1,0,1)})
    if verbose:
        print(f"m={m:3d}: |dev| max = {worst:.6g}  (dev/Delta in [{minfrac_dev:.4f},{maxfrac_dev:.4f}])"
              f"  bound 1.666*d0 = {1.666*d0:.6g}")
        print(f"        shifts {sorted(seen)} == offsets {exp}: {sorted(seen)==exp};"
              f" min angle(s,t) = {minst:.4f}")
    return sorted(seen)==exp

for m in (3,4,5,6,7,8,9,12,15,18):
    sweep(m)

print()
print("=== interior-margin attainment, m=6 ===")
m=6; n=36; Delta=2*np.pi/n; d0=np.pi/54
best={}
for i in range(1440):
    argf=2*np.pi*(i+0.5)/1440
    for k in range(2880):
        arga=2*np.pi*k/2880
        a=d0*np.array([np.cos(arga),np.sin(arga)])
        fx,fy=np.cos(argf)+a[0],np.sin(argf)+a[1]
        rho=np.hypot(fx,fy); h=np.sqrt(1-rho**2/4)
        for sgn in (1,-1):
            sx,sy=fx/2+sgn*h*(-fy)/rho, fy/2+sgn*h*fx/rho
            args=np.arctan2(sy,sx)
            i0=int(np.floor(argf/Delta)); i1=int(np.floor(args/Delta))
            j=(i1-i0)%n; offs={5,6,7,29,30,31}
            if j not in offs: continue
            # margin: distance of argf, args to the nearest sector boundary, in sectors
            marg=min((argf/Delta)%1,1-((argf/Delta)%1),(args/Delta)%1,1-((args/Delta)%1))
            if j not in best or marg>best[j][0]:
                best[j]=(float(marg),float(argf),float(arga),float(d0),sgn if False else int(sgn))
for j in sorted({5,6,7,29,30,31}):
    print(f"  offset {j:2d}: margin {best[j][0]:.4f} sectors, arg f={best[j][1]:.5f}, arg a={best[j][2]:.5f}, d=d0, branch {best[j][4]:+d}")
print("all six with margin > 0.1 sector:", all(b[0]>0.1 for b in best.values()))
