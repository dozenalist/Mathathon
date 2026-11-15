// Exact check of two admissible rows in Lai, Table 1 (Remark 8.6).
// Uses Fauzan (4.4)-(4.8) for gamma_in and (5.4) for Gamma.
// No floating-point arithmetic is used in either calculation.
// Source: sources/Fauzan_2026_zeta5.txt, printed pp. 10 and 14.
// Run: node tmp/exposition-audit/check_lai_gamma_exact.cjs
function gcd(a,b) { a=a<0n?-a:a; b=b<0n?-b:b; while(b) [a,b]=[b,a%b]; return a; }
function R(n,d=1n) { n=BigInt(n); d=BigInt(d); if(d<0n){n=-n;d=-d;} const g=gcd(n,d); return {n:n/g,d:d/g}; }
const add=(a,b)=>R(a.n*b.d+b.n*a.d,a.d*b.d);
const neg=a=>R(-a.n,a.d);
const sub=(a,b)=>add(a,neg(b));
const mul=(a,b)=>R(a.n*b.n,a.d*b.d);
const div=(a,b)=>R(a.n*b.d,a.d*b.n);
const cmp=(a,b)=>a.n*b.d<b.n*a.d?-1:a.n*b.d>b.n*a.d?1:0;
const fl=a=>a.n>=0n?a.n/a.d:-((-a.n+a.d-1n)/a.d);
const ce=a=>-fl(neg(a));
const repr=a=>a.d===1n?String(a.n):`${a.n}/${a.d}`;
const max=(a,b)=>cmp(a,b)>=0?a:b;
const min=(a,b)=>a<b?a:b;
const Z=R(0), HALF=R(1,2), TWO=R(2);
function isPrime(p) { for(let i=2n;i*i<=p;i++) if(p%i===0n)return false; return p>1n; }
function check(M,K,p,laiPGamma) {
  M=BigInt(M); K=BigInt(K); p=BigInt(p);
  const N=3n*K/40n,h=37n*K/40n,m=(p-1n)/2n,L0=4n*M+10n,mN=N/p,mK=K/p;
  const total=h-L0+3n*(N-mN),T=total/m,E=total%m;
  const ell=(A,a)=>fl(R(A-a,p))+fl(R(A+a,p))+1n;
  let rows=[];
  for(let a=1n;a<=m;a++)rows.push({a,ell:ell(K,a),b:3n*ell(N,a)});
  // Ties may be ordered arbitrarily by Fauzan (4.4).
  rows.sort((a,b)=>a.ell>b.ell?-1:a.ell<b.ell?1:0);
  let gamma=0n,cap=null,dimensions=L0,minDimension=L0;
  rows.forEach((r,i)=>{
    const eps=BigInt(i)<E?1n:0n,L=T-r.b+eps,Zc=T+eps;
    dimensions+=L; minDimension=min(minDimension,L);
    // Twice the sum of weights i+b-(ell+4)/2 over i=0,...,L-1.
    gamma+=L*(L-1n+2n*r.b-r.ell-4n);
    const c=2n*Zc-r.ell-4n;
    cap=cap===null?c:min(cap,c);
  });
  for(let i=0n;i<L0;i++)gamma+=min(4n*i+12n*mN-2n*mK+1n,cap);
  const x=R(K,p),alpha=R(3,40),H=R(23,20),ax=mul(alpha,x);
  const Tc=fl(mul(mul(TWO,H),x)),q=fl(mul(TWO,x));
  const s=sub(mul(H,x),R(Tc,2)),nplus=sub(x,R(q,2));
  // Partition [0,1/2] at every discontinuity of ell(x,z), ell(alpha*x,z).
  const breakMap=new Map([[repr(Z),Z],[repr(HALF),HALF]]);
  for(const u of [x,ax])for(let j=fl(u)-2n;j<=ce(u)+2n;j++){
    for(const v of [sub(u,R(j)),sub(R(j),u)])
      if(cmp(v,Z)>0&&cmp(v,HALF)<0)breakMap.set(repr(v),v);
  }
  const breaks=[...breakMap.values()].sort(cmp);
  let integral=Z;
  for(let i=0;i+1<breaks.length;i++){
    const a=breaks[i],b=breaks[i+1],z=div(add(a,b),TWO);
    const lc=fl(sub(x,z))+fl(add(x,z))+1n;
    const bc=3n*(fl(sub(ax,z))+fl(add(ax,z))+1n);
    integral=add(integral,mul(sub(b,a),R((Tc-bc)*(Tc+bc-lc-5n))));
  }
  const Gamma=add(add(integral,mul(s,R(2n*Tc-q-5n))),max(sub(s,nplus),Z));
  const pGamma=mul(R(p),Gamma);
  const result={M:String(M),K:String(K),p:String(p),
    admissible:M>=40n&&K%40n===0n&&K>=200n*M*M&&p*M>K&&3n*p<=K&&isPrime(p),
    discrete_T:String(T),E:String(E),dimension_sum:String(dimensions),h:String(h),minimum_L:String(minDimension),
    limiting_T:String(Tc),breakpoints:breaks.map(repr),Gamma:repr(Gamma),
    gamma_in:String(gamma),p_Gamma:repr(pGamma),difference:repr(sub(R(gamma),pGamma)),
    Lai_printed_p_Gamma:String(laiPGamma)};
  if(dimensions!==h||minDimension<0n)throw new Error('allocation check failed');
  return result;
}
console.log(JSON.stringify({method:'Exact BigInt rational arithmetic; not a uniform asymptotic proof',
  results:[check(40,320000,8009,7661701),check(40,640000,16001,15342855)]},null,2));
