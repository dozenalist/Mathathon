from fractions import Fraction as F

alpha=F(3,40)
lam=1-alpha
pos=lambda x:max(F(0),x)

def c5(y):
    if y<F(1,2):
        r0=8-9*y-8*alpha-5*min(alpha,1-2*y)-5*pos(1+alpha-3*y)
        d=pos(1+4*alpha-3*y-pos(1+alpha-3*y))
        return r0-d
    return 7*(1-y)-6*min(alpha,1-y)-6*pos(1+alpha-2*y)+pos(1+4*alpha-2*y)

def c7(y):
    if y<F(1,2):
        return 9*(1-y)-12*alpha-6*min(alpha,1-2*y)-6*pos(1+alpha-3*y)+pos(1+4*alpha-3*y)
    return 9*(1-y)-6*min(alpha,1-y)-6*pos(1+alpha-2*y)

breaks=sorted({F(1,3),F(1,2),F(1),1-alpha,(1+alpha)/2,(1+4*alpha)/2,(1-alpha)/2,(1+alpha)/3,(1+4*alpha)/3})

def piecewise_integral(f, points):
    # Interior points avoid discontinuities at x=1/2; affine on every interval.
    total=F(0)
    for a,b in zip(points,points[1:]):
        total+=(b-a)*f((a+b)/2)
    return total

old=piecewise_integral(c5,breaks)
new=piecewise_integral(c7,breaks)
print('raw outer zeta5',old,float(old))
print('raw outer zeta7',new,float(new))
print('extra outer cost',new-old,float(new-old))
print('inner extra M=200',2*lam*(F(1,3)-F(1,200)),float(2*lam*(F(1,3)-F(1,200))))
print('small prime extra M=200',2*lam/F(200),float(2*lam/F(200)))
print('combined extra independent M',new-old+2*lam/3,float(new-old+2*lam/3))
print('Iout7',F(127751,96000)+new-old,float(F(127751,96000)+new-old))
