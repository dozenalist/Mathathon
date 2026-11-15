"""Exact arithmetic certificates for the global normalization bound.

Mathematical inputs: A. Fauzan, zeta(5) is irrational (2026), Section 5;
Moritz Firsching et al., mo271/Zeta5, commit
7fe736760f4b96bfdb4334b68e3b3124ecbe10b0, Apery/Growth/{TablePrime,
OuterPrime,TailPrime,TailIntegral,InnerTable,OuterTable}.lean.

This is a new Python implementation of their rational formulas.  It does
not copy the source repository's sampling-based generator.  All affine
pieces are obtained by symbolic operations on exact rational coefficients.
Midpoints select branches only after the complete list of possible branch
crossings has been inserted.  The lower envelope is certified on entire
intervals by affine endpoint inequalities.  No floating-point value enters
any assertion or certificate.

Run: python growth_exact.py
Writes exact CSV tables and growth_exact_result.json beside this script.
"""
from fractions import Fraction as F
from pathlib import Path
import csv
import json
import re

LAM, ALPHA = F(37, 40), F(3, 40)
ZERO, ONE = (F(0), F(0)), (F(0), F(1))

def add(u, v):
    return u[0] + v[0], u[1] + v[1]

def scale(c, u):
    return c * u[0], c * u[1]

def sub(u, v):
    return add(u, scale(-1, v))

def at(u, x):
    return u[0] * x + u[1]

def floor(x):
    return x.numerator // x.denominator

def ceil(x):
    return -floor(-x)

def grids(lo, hi, outer=False):
    # All changes of floor(x), floor(alpha*x), floor(2*lambda*x),
    # and all crossings among 0,1/2,{x},1-{x},{alpha*x},1-{alpha*x}.
    steps = [F(1, 2), F(20, 3), F(20, 37), F(40, 37), F(40, 43)]
    if outer:
        steps.append(F(20, 13))  # rank-loss hinge
    pts = {lo, hi}
    for d in steps:
        for k in range(ceil(lo/d), floor(hi/d)+1):
            pts.add(k*d)
    return sorted(pts)

def branch_data(lo, hi):
    x = (lo+hi)/2
    q, qp, mu = floor(x), floor(ALPHA*x), floor(2*LAM*x)
    f, g = (F(1), -F(q)), (ALPHA, -F(qp))
    candidates = [ZERO, (F(0), F(1,2)), f, sub(ONE,f), g, sub(ONE,g)]
    # Check that every pair has constant order on the entire interval.
    for u in candidates:
        for v in candidates:
            d = sub(u,v)
            assert at(d,lo)*at(d,hi) >= 0
    edges = sorted(set(v for v in candidates if 0 <= at(v,x) <= F(1,2)),
                   key=lambda v: at(v,x))
    strips=[]
    for a,b in zip(edges,edges[1:]):
        if at(a,x)==at(b,x):
            continue
        z=(at(a,x)+at(b,x))/2
        ac=int(z < at(f,x))+int(z > 1-at(f,x))
        bc=int(z < at(g,x))+int(z > 1-at(g,x))
        strips.append((sub(b,a),ac,bc))
    assert add_all(s[0] for s in strips)==(F(0),F(1,2))
    return q,qp,mu,strips

def add_all(items):
    result=ZERO
    for item in items:
        result=add(result,item)
    return result

def psi(k,beta):
    length=max(0,(k-beta+1)//2)
    return F(length*(k-beta-length+1),2)

def j_affine(mu):
    return (mu*LAM,-F(mu*(mu+1),4))

def inner_line(data,k):
    q,qp,mu,strips=data
    base=(-2*LAM*q+12*LAM*qp-LAM*k,F(0))
    result=add(base,scale(2,j_affine(mu)))
    for length,a,b in strips:
        result=add(result,scale(2*psi(k,12*qp-2*q-4+6*b-a),length))
    return result

def go(q,a,d):
    return sum((min(F(0),i+3*d-F(2*q+a+4,2))
                for i in range(max(0,2*q+a-2))),F(0))

def outer_line(lo,hi):
    q,qp,mu,strips=branch_data(lo,hi)
    assert qp==0
    result=add((-2*LAM*q,F(0)),scale(2,j_affine(mu)))
    for length,a,b in strips:
        result=add(result,scale(-2*go(q,a,b),length))
    if F(13,10)*(lo+hi)/2 > 2:
        result=add(result,(F(13,10),F(-2)))
    return result

def lower_envelope(lines,lo,hi):
    # For increasing x, slopes of a lower envelope decrease.
    byslope={}
    for k,(a,b) in lines.items():
        if a not in byslope or (b,k)<(byslope[a][1],byslope[a][2]):
            byslope[a]=(a,b,k)
    hull=[]
    starts=[]
    for line in sorted(byslope.values(),reverse=True):
        a,b,k=line
        start=None
        while hull:
            aa,bb,kk=hull[-1]
            start=(b-bb)/(aa-a)
            if starts[-1] is not None and start<=starts[-1]:
                hull.pop()
                starts.pop()
            else:
                break
        if not hull:
            start=None
        hull.append(line)
        starts.append(start)
    pieces=[]
    for i,(a,b,k) in enumerate(hull):
        left=lo if starts[i] is None else max(lo,starts[i])
        right=hi if i+1==len(hull) else min(hi,starts[i+1])
        if left>=right:
            continue
        # This proves dominance throughout [left,right], not at samples.
        for aa,bb in lines.values():
            assert a*left+b<=aa*left+bb
            assert a*right+b<=aa*right+bb
        pieces.append((left,right,k,a,b))
    assert pieces[0][0]==lo and pieces[-1][1]==hi
    assert all(p[1]==q[0] for p,q in zip(pieces,pieces[1:]))
    return pieces

def merge(pieces):
    result=[]
    for p in pieces:
        if result and result[-1][1]==p[0] and result[-1][2:]==p[2:]:
            result[-1]=(result[-1][0],p[1])+p[2:]
        else:
            result.append(p)
    return result

def integral_piece(lo,hi,a,b):
    return a*(1/lo-1/hi)+b/2*(1/lo**2-1/hi**2)

def inner_table():
    pts=grids(F(3),F(20))
    pieces=[]
    for lo,hi in zip(pts,pts[1:]):
        data=branch_data(lo,hi)
        q=data[0]
        lines={k:inner_line(data,k) for k in range(-2*q-6,8*q+21)}
        pieces.extend(lower_envelope(lines,lo,hi))
    return merge(pieces)

def outer_table():
    pts=grids(F(20,37),F(3),True)
    pieces=[(lo,hi,*outer_line(lo,hi)) for lo,hi in zip(pts,pts[1:])]
    return merge(pieces)

def G0(v):
    return v*(1-v)*(2*v-1)/6

def Phi(x):
    f=x-floor(x)
    g=ALPHA*x-floor(ALPHA*x)
    P=74*g*(1-g)-LAM*f*(1-f)
    C=F(74)/ALPHA*G0(g)-LAM*G0(f)
    Pbar=F(2923,240)
    return P/x**2+2*C/x**3-Pbar/x**2+LAM/x-F(27,32)/x**2

def output_csv(name,header,rows):
    with Path(__file__).with_name(name).open("w",newline="",encoding="utf-8") as f:
        out=csv.writer(f)
        out.writerow(header)
        out.writerows([[str(x) for x in row] for row in rows])

def tex_number(x):
    x=F(x)
    if x.denominator==1:
        return str(x.numerator)
    sign="-" if x<0 else ""
    return sign+r"\frac{"+str(abs(x.numerator))+"}{"+str(x.denominator)+"}"

def output_tex(rows):
    lines=[
        r"\section{The exact inner arithmetic table}\label{growth:table-appendix}",
        "For each row, the selected level is \\(k\\), and",
        r"\(E_{\rm in}(x,k)=Ax+B\) on the open interval \((a,b)\).",
        "The derivation, admissibility check and integration rule are given",
        r"in Section~\ref{growth:section}. These are the 125 pieces of",
        r"\cite[\texttt{Growth/InnerTable.lean}, \texttt{InnerSum.lean}]{firsching},",
        "regenerated by the exact affine-branch algorithm supplied with this draft.",
        r"{\small",
        r"\setlength{\LTleft}{0pt}\setlength{\LTright}{0pt}",
        r"\renewcommand{\arraystretch}{1.15}",
        r"\begin{longtable}{@{\extracolsep{\fill}}rrrrr}",
        r"\toprule \(a\)&\(b\)&\(k\)&\(A\)&\(B\)\\\midrule\endfirsthead",
        r"\toprule \(a\)&\(b\)&\(k\)&\(A\)&\(B\)\\\midrule\endhead",
        r"\midrule\multicolumn{5}{r}{Continued on the next page}\\\endfoot",
        r"\bottomrule\endlastfoot",
    ]
    for row in rows:
        lines.append(" & ".join("$"+tex_number(v)+"$" for v in row)+r" \\")
    lines.extend([r"\end{longtable}",r"}",""])
    Path(__file__).with_name("growth_inner_table.tex").write_text("\n".join(lines),encoding="utf-8")

def compare_source_table(rows):
    source=(Path(__file__).resolve().parents[1]/
            "source-excerpts/InnerSum.lean")
    if not source.exists():
        source=(Path(__file__).resolve().parents[2]/
                "sources/mo271-Zeta5/Apery/Growth/InnerSum.lean")
    if not source.exists():
        return None  # comparison unavailable, not a mismatching table
    text=source.read_text(encoding="utf-8")
    arrays={}
    for name in ("tInL","kInL","aInL","bInL"):
        raw=re.search(r"def "+name+r" : List [^:]+ := \[([^\]]+)\]",text).group(1)
        arrays[name]=[F(v.strip().strip("()")) for v in raw.split(",")]
    source_rows=[(arrays["tInL"][i],arrays["tInL"][i+1],arrays["kInL"][i],
                  arrays["aInL"][i],arrays["bInL"][i]) for i in range(125)]
    assert rows==source_rows
    return True

def main():
    inside=inner_table()
    outside=outer_table()
    inner=sum((integral_piece(a,b,c,d) for a,b,k,c,d in inside),F(0))
    outer=sum((integral_piece(a,b,c,d) for a,b,c,d in outside),F(0))
    tail=Phi(F(400))-Phi(F(20))+34*(F(1,20**3)-F(1,400**3))
    small=6*LAM/400
    assert inner==F(322437603634266857629,7535670527041937280000)
    assert outer==F(129101,96000)
    assert tail==-F(6843153,128000000)
    total=small+inner+tail+outer
    assert total<F(27,20)
    output_csv("growth_inner_table.csv",["left","right","k","slope","intercept"],inside)
    output_csv("growth_outer_table.csv",["left","right","slope","intercept"],outside)
    output_tex(inside)
    matched=compare_source_table(inside)
    data={"method":"exact rational affine-branch certificates",
          "inner_pieces":len(inside),"outer_pieces":len(outside),
          "all_125_rows_equal_pinned_Lean_table":matched,
          "small":str(small),"inner":str(inner),"tail_upper_bound":str(tail),
          "outer":str(outer),"total_upper_bound":str(total),
          "gap_below_1_35":str(F(27,20)-total),
          "decimal_total_for_orientation_only":float(total)}
    Path(__file__).with_name("growth_exact_result.json").write_text(json.dumps(data,indent=2)+"\n",
                                                                   encoding="utf-8")
    print(json.dumps(data,indent=2))

if __name__=="__main__":
    main()
