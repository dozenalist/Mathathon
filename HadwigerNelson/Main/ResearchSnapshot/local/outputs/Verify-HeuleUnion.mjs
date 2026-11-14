// Independent exact verifier for H union (H + (3/2,sqrt(3)/2)).
// Run: node Verify-HeuleUnion.mjs (uses the two adjacent input files).
import fs from 'node:fs/promises';
import crypto from 'node:crypto';
const hash = x => crypto.createHash('sha256').update(x).digest('hex');
const source = await fs.readFile(new URL('./HEULE553-COORDINATES.vtx', import.meta.url), 'utf8');
const certText = await fs.readFile(new URL('./HEULE-UNION-CERTIFICATE.json', import.meta.url), 'utf8');
const cert = JSON.parse(certText);
const rad = [1n,3n,5n,15n,11n,33n,55n,165n]; // XOR mask basis
function gcd(a,b) { a=a<0n?-a:a; while(b) [a,b]=[b,a%b]; return a; }
function Q(a,b=1n) { if(!b) throw Error('zero denominator'); if(b<0n){a=-a;b=-b;} const g=gcd(a,b);return [a/g,b/g]; }
const addQ=(a,b)=>Q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const mulQ=(a,b)=>Q(a[0]*b[0],a[1]*b[1]);
const zero=()=>Array.from({length:8},()=>[0n,1n]);
function scalar(q){const z=zero();z[0]=q;return z;}
const add=(a,b)=>a.map((v,i)=>addQ(v,b[i]));
const neg=a=>a.map(([p,q])=>[-p,q]);
function mul(a,b){const out=zero();for(let i=0;i<8;i++)for(let j=0;j<8;j++)if(a[i][0]&&b[j][0])out[i^j]=addQ(out[i^j],mulQ(mulQ(a[i],b[j]),[rad[i&j],1n]));return out;}
function div(a,b){const nonzero=b.map((x,i)=>x[0]?i:-1).filter(i=>i>=0);if(nonzero.length!==1)throw Error('denominator not monomial');const i=nonzero[0],inv=zero();inv[i]=Q(b[i][1],b[i][0]*rad[i]);return mul(a,inv);}
function parse(text){
 const s=text.replace(/\s/g,'');const tok=s.match(/Sqrt\[(?:11\/3|\d+)\]|\d+|[-+*/()]/g)||[];
 if(tok.join('')!==s)throw Error('unrecognized coordinate syntax');
 let p=0;
 function atom(){const t=tok[p++];if(t==='('){const v=expr();if(tok[p++]!==')')throw Error('parenthesis');return v;}if(/^\d+$/.test(t))return scalar(Q(BigInt(t)));
 if(t?.startsWith('Sqrt[')){const n=t.slice(5,-1);const r=n==='11/3'?33n:BigInt(n);const i=rad.indexOf(r);if(i<0)throw Error('unknown radical');const z=zero();z[i]=Q(1n,n==='11/3'?3n:1n);return z;}throw Error('bad atom');}
 function unary(){if(tok[p]==='-'){p++;return neg(unary());}if(tok[p]==='+'){p++;return unary();}return atom();}
 function term(){let v=unary();while(tok[p]==='*'||tok[p]==='/'){const op=tok[p++],b=unary();v=op==='*'?mul(v,b):div(v,b);}return v;}
 function expr(){let v=term();while(tok[p]==='+'||tok[p]==='-'){const op=tok[p++],b=term();v=add(v,op==='+'?b:neg(b));}return v;}
 const result=expr();if(p!==tok.length)throw Error('unconsumed tokens');return result;
}
const rows=source.trim().split(/\r?\n/);
if(rows.length!==553)throw Error('expected553 source vertices');
const original=rows.map(line=>{if(!/^\{[^{}]*\}$/.test(line))throw Error('invalid row');const xy=line.slice(1,-1).split(',');if(xy.length!==2)throw Error('not2coordinates');return xy.map(parse);});
const tx=scalar(Q(3n,2n)),ty=zero();ty[1]=Q(1n,2n);
const translated=original.map(([x,y])=>[add(x,tx),add(y,ty)]);
const all=[...original,...translated];
let den=1n;for(const point of all)for(const coordinate of point)for(const [,d] of coordinate)den=den/gcd(den,d)*d;
const ints=all.map(p=>p.map(c=>c.map(([n,d])=>n*(den/d))));
const pts=[],index=new Map(),map=[];
for(const p of ints){const key=p.flat().join(',');if(!index.has(key)){index.set(key,pts.length);pts.push(p);}map.push(index.get(key));}
const n=pts.length;if(n!==1048||cert.n!==n)throw Error('vertex count');
if(new Set(map.slice(0,553)).size!==553||new Set(map.slice(553)).size!==553)throw Error('source duplicates');
const ranges=[0,1].map(axis=>rad.map((_,i)=>{const xs=pts.map(p=>p[axis][i]);return xs.reduce((a,b)=>a>b?a:b)-xs.reduce((a,b)=>a<b?a:b);}));
const bounds=Array(8).fill(0n);
for(let axis=0;axis<2;axis++)for(let i=0;i<8;i++)for(let j=0;j<8;j++)bounds[i^j]+=ranges[axis][i]*ranges[axis][j]*rad[i&j];
const maxBound=bounds.reduce((a,b)=>a>b?a:b);
if(maxBound>9007199254740991n||den*den>9007199254740991n||pts.some(p=>p.flat().some(x=>x>9007199254740991n||x< -9007199254740991n)))throw Error('unsafe integer range');
// Every product and intermediate sum is bounded above by these triangle-inequality
// bounds. IEEE integer operations are therefore EXACT, not approximate geometry.
const P=pts.map(p=>p.map(c=>c.map(Number))),R=rad.map(Number),unit=Number(den*den),edges=[];
let pairs=0,nonconstantTests=0;
for(let a=0;a<n;a++)for(let b=a+1;b<n;b++){
 pairs++;const dx=P[a][0].map((x,i)=>x-P[b][0][i]),dy=P[a][1].map((x,i)=>x-P[b][1][i]);
 let c0=0;for(let i=0;i<8;i++)c0+=R[i]*(dx[i]*dx[i]+dy[i]*dy[i]);
 if(c0!==unit)continue;
 nonconstantTests++;const co=Array(8).fill(0);co[0]=c0;
 for(let i=0;i<8;i++)for(let j=i+1;j<8;j++)co[i^j]+=2*R[i&j]*(dx[i]*dx[j]+dy[i]*dy[j]);
 if(co.slice(1).every(x=>x===0))edges.push([a,b]);
}
const canon=e=>e.map(([a,b])=>{if(!Number.isInteger(a)||!Number.isInteger(b)||a<0||a>=b||b>=n)throw Error('bad edge');return a+','+b;}).sort();
if(JSON.stringify(canon(edges))!==JSON.stringify(canon(cert.edges)))throw Error('induced edges differ');
if(edges.length!==5487)throw Error('edge count');
const w=cert.witness;
if(!Array.isArray(w)||w.length!==n||w.some(c=>!Number.isInteger(c)||c<0||c>=5))throw Error('invalid coloring');
if(edges.some(([a,b])=>w[a]===w[b]))throw Error('monochromatic unit pair');
const E=new Set(canon(edges)),A=new Set(map.slice(0,553)),B=new Set(map.slice(553));
let ea=0,eb=0,fresh=0;
for(const [a,b] of edges){const inA=A.has(a)&&A.has(b),inB=B.has(a)&&B.has(b);if(inA)ea++;if(inB)eb++;if(!inA&&!inB)fresh++;}
const overlap=[...A].filter(x=>B.has(x));let overlapClique=true;
for(let i=0;i<overlap.length;i++)for(let j=i+1;j<overlap.length;j++){const a=Math.min(overlap[i],overlap[j]),b=Math.max(overlap[i],overlap[j]);if(!E.has(a+','+b))overlapClique=false;}
if(ea!==2722||eb!==2722||fresh!==184||overlap.length!==58||overlapClique)throw Error('structure mismatch');
export const result={at:new Date().toISOString(),passed:true,method:'Independent strict expression parser, exact multiquadratic arithmetic; all pairs tested, no distance prefilter; safe integer bound proved with BigInt',coordinateSha256:hash(source),certificateSha256:hash(certText),basis:rad.map(String),commonDenominator:String(den),maximumAbsoluteIntermediateBound:String(maxBound),pairsTested:pairs,nonconstantTests,vertices:n,edges:edges.length,overlap:overlap.length,internalA:ea,internalB:eb,newEdges:fresh,overlapClique,properFiveColoring:true,scope:'Exact induced unit-distance graph and explicit5coloring. Lower bound5 uses the independently certified embedded Heule553 subgraph; this program does not recheck its4UNSAT proof. No forcing pair or new plane bound.'};
console.log(JSON.stringify(result,null,2));
