// Exact rational checks for zeta9 Section5 and AppendixB.
// Source: Fauzan zeta5 paper (5.4)-(5.20), AppendixB; new local weights from draft Section4.
// Run with Node.js; no packages needed. BigInt fractions avoid floating-point integration.

const gcd=(a,b)=>{a=a<0n?-a:a; while(b){let c=a%b;a=b;b=c<0n?-c:c;}return a;};
class Q{constructor(n,d=1){n=BigInt(n);d=BigInt(d); if(d<0n){n=-n;d=-d;}let g=gcd(n,d);this.n=n/g;this.d=d/g;} a(o){o=q(o);return new Q(this.n*o.d+o.n*this.d,this.d*o.d)} s(o){return this.a(q(o).m(-1))} m(o){o=q(o);return new Q(this.n*o.n,this.d*o.d)} div(o){o=q(o);return new Q(this.n*o.d,this.d*o.n)} cmp(o){o=q(o);let v=this.n*o.d-o.n*this.d;return v<0n?-1:v>0n?1:0} floor(){return this.n>=0?this.n/this.d:(this.n-this.d+1n)/this.d} num(){return Number(this.n)/Number(this.d)} toString(){return this.d===1n?String(this.n):this.n+'/'+this.d}};
const q=(n,d=1)=>n instanceof Q?n:new Q(n,d),pos=x=>x.cmp(0)>0?x:q(0),min=(x,y)=>x.cmp(y)<0?x:y;
const alpha=q(3,40),lam=q(37,40);
const C5=y=>{
if(y.cmp(q(1,2))<0){
let a=pos(q(1).a(alpha).s(y.m(3)));
let r0=q(8).s(y.m(9)).s(alpha.m(8)).s(min(alpha,q(1).s(y.m(2))).m(5)).s(a.m(5));
return r0.s(pos(q(1).a(alpha.m(4)).s(y.m(3)).s(a)));
}
if(y.cmp(1)<0)return q(1).s(y).m(7).s(min(alpha,q(1).s(y)).m(6)).s(pos(q(1).a(alpha).s(y.m(2))).m(6)).a(pos(q(1).a(alpha.m(4)).s(y.m(2))));
return q(0);
};
const C9=y=>y.cmp(q(1,2))<0?q(1).s(y).m(11).s(alpha.m(12)).s(min(alpha,q(1).s(y.m(2))).m(6)).s(pos(q(1).a(alpha).s(y.m(3))).m(6)):y.cmp(1)<0?q(1).s(y).m(11).s(min(alpha,q(1).s(y)).m(6)).s(pos(q(1).a(alpha).s(y.m(2))).m(6)):q(0);
const S=y=>{let x=lam.m(-2).m(q(1).div(y).floor());for(let j=1;j<=5;j++)x=x.a(pos(lam.m(2).s(y.m(j))));return x;};
const cuts=[q(1,3),q(43,120),q(37,100),q(13,30),q(37,80),q(1,2),q(43,80),q(37,60),q(13,20),q(37,40),q(1),q(37,20)];
const integrate=(f,a)=>{let t=q(0);for(let i=0;i<a.length-1;i++)t=t.a(a[i+1].s(a[i]).m(f(a[i].a(a[i+1]).div(2))));return t;};
const out5=integrate(C5,cuts),out9=integrate(C9,cuts),scalar=integrate(S,cuts),delta=out9.s(out5),extra=delta.a(lam.m(4).div(3)),Iout9=out9.a(scalar);
const oldstar=q(9928298118277006344769n,7535670527041937280000n),star=oldstar.a(extra),U=q(-2733991,2000000);
const AM=M=>star.a(lam.m(7).div(M)).s(q(2923,240).s(q(1,4)).div(q(M).m(M))).a(q(32).div(q(M).m(M).m(M)));

const H=q(23,20),frac=x=>x.s(q(x.floor())),ell=(x,z)=>q(x.s(z).floor()+x.a(z).floor()+1n);
const R9=x=>{
let T=q(H.m(x).m(2).floor()),s=H.m(x).s(T.div(2)),qq=q(x.m(2).floor()),n=x.m(2).s(qq).div(2);
let fx=frac(x),gx=frac(alpha.m(x)),zs=[q(0),q(1,2)];
for(let t of [fx,q(1).s(fx),gx,q(1).s(gx)])if(t.cmp(0)>0&&t.cmp(q(1,2))<0)zs.push(t);
zs=[...new Map(zs.map(v=>[String(v),v])).values()].sort((a,b)=>a.cmp(b));
let gam=q(0);
for(let i=0;i<zs.length-1;i++){let z=zs[i].a(zs[i+1]).div(2),b=ell(alpha.m(x),z).m(3);gam=gam.a(zs[i+1].s(zs[i]).m(T.s(b)).m(T.a(b).s(ell(x,z)).s(9)));}
gam=gam.a(s.m(T.m(2).s(qq).s(9))).a(pos(s.s(n)));
let m=q(lam.m(x).m(2).floor()),J=m.m(lam).m(x).s(m.m(m.a(1)).div(4));
let norm=lam.m(x).m(2).m(x.floor()).s(lam.m(x).m(12).m(alpha.m(x).floor())).s(J.m(2));
return gam.a(norm).m(-1);
};
let innercuts=[q(3),q(20)];
for(let c of [q(2),alpha.m(2),lam.m(2),H.m(2),alpha.m(4),q(1).s(alpha).m(2),q(1).a(alpha).m(2)]){
for(let j=Number(c.m(3).floor());j<=Number(c.m(20).floor())+1;j++){let v=q(j).div(c);if(v.cmp(3)>0&&v.cmp(20)<0)innercuts.push(v);}
}
innercuts=[...new Map(innercuts.map(v=>[String(v),v])).values()].sort((a,b)=>a.cmp(b));
let finite=q(0);
for(let i=0;i<innercuts.length-1;i++){
let l=innercuts[i],r=innercuts[i+1],x=l.m(2).a(r).div(3),y=l.a(r.m(2)).div(3),fx=R9(x),fy=R9(y),a=fy.s(fx).div(y.s(x)),b=fx.s(a.m(x));
let xp=l.m(4).a(r).div(5);if(R9(xp).cmp(a.m(xp).a(b))!==0)throw Error('Not affine '+l);
finite=finite.a(a.m(q(1).div(l).s(q(1).div(r)))).a(b.div(2).m(q(1).div(l.m(l)).s(q(1).div(r.m(r)))));
}

const check=(test,msg)=>{if(!test)throw Error(msg)};
check(String(out5)==='23329/19200','Source raw outer integral');
check(String(out9)==='14441/7200','New raw outer integral');
check(String(scalar)==='1851/16000','Unchanged scalar integral');
check(String(Iout9)==='305479/144000','New outer integral');
check(String(extra)==='116581/57600','Total increment');
check(innercuts.length===144,'Source breakpoint count');
const innerShift=lam.m(4).m(q(1,3).s(q(1,20)));
check(finite.cmp(q(322437603634266857629n,7535670527041937280000n).a(innerShift))===0,'Finite inner shift');
const newCuts=[q(1,3),q(43,120),q(37,100),q(37,80),q(1,2),q(43,80),q(37,60),q(37,40),q(1),q(37,20)];
const outerTable=[];
for(let i=0;i<newCuts.length-1;i++){
const l=newCuts[i],r=newCuts[i+1],x=l.m(2).a(r).div(3),y=l.a(r.m(2)).div(3);
const fx=C9(x).a(S(x)),fy=C9(y).a(S(y)),c=fy.s(fx).div(y.s(x)),b=fx.s(c.m(x));
const xp=l.m(4).a(r).div(5);
check(C9(xp).a(S(xp)).cmp(b.a(c.m(xp)))===0,'Outer affine interpolation');
outerTable.push({l:String(l),r:String(r),b:String(b),c:String(c)});
}
const tail20=q(3).m(lam).div(20).s(q(37,2).div(400)).a(q(2923,240).div(400)).a(q(32,8000)).a(q(13,16).div(400));
check(String(tail20)==='6191/48000','Tail bound at20');
check(Iout9.a(finite).a(tail20).cmp(star)===0,'Final Astar9');
const report={
status:'Exact algebraic certificate calculations; no validation of the local analytic completion assumption or irrationality conclusion.',
raw_outer5:String(out5),raw_outer9:String(out9),scalar_integral:String(scalar),
outer_increment:String(delta),Iout9:String(Iout9),total_increment:String(extra),
inner_interval_count:innercuts.length-1,inner_finite9:String(finite),inner_finite_increment:String(innerShift),
tail_upper20:String(tail20),outer_affine_table:outerTable,
A9star:String(star),A9star_decimal:star.num(),A9M_formula:'A9star+7lambda/M-2863/(240M^2)+32/M^3',
A9_200:String(AM(200)),A9_200_plus_U:String(AM(200).a(U)),A9_200_plus_U_decimal:AM(200).a(U).num(),
A9_100000_plus_U:String(AM(100000).a(U)),A9_100000_plus_U_decimal:AM(100000).a(U).num(),
limiting_A9_plus_U_decimal:star.a(U).num(),
margin200:String(AM(200).a(U).m(-1600).s(q(139,5))),
margin100000:String(AM(100000).a(U).m(-1600).s(q(7907,100)))
};
console.log(JSON.stringify(report,null,2));

