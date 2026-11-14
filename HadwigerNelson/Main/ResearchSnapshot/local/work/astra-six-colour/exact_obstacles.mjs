// Independent plain-integer implementation; no dependencies or numeric geometry.
import { writeFileSync } from 'node:fs';
import assert from 'node:assert/strict';
const start = Date.now();
const sign = (j,v) => [0,1,5].includes((j-v+6)%6);
const popcount = n => n.toString(2).replaceAll('0','').length;
const palettes = Array.from({length:63},(_,i)=>i+1).filter(p=>popcount(p)<=2);
const asList = p => Array.from({length:6},(_,i)=>i).filter(i=>(p&(1<<i))!==0);
function allowed(m,dirs,j,b) {
  let a = 63;
  for(let e=0;e<m;e++) if(sign(j,dirs[e])===b) a &= ~(1<<e | 1<<((e+1)%m));
  return a;
}
function verify(m,dirs,word) {
  assert.equal(dirs.length,m); assert.equal(word.length,6);
  for(let j=0;j<6;j++) {
    let p=word[j];
    assert(p>0 && p<64 && popcount(p)<=2);
    assert.equal(p&word[(j+1)%6],0);
    for(let e=0;e<m;e++) {
      let edge=1<<e | 1<<((e+1)%m);
      assert((p & ~edge)!==0);
      assert.notEqual(sign((j+3)%6,dirs[e]),sign(j,dirs[e]));
    }
    for(let b of [true,false]) assert((p&allowed(m,dirs,j,b))!==0);
  }
}
function solve(m) {
  for(let code=0;code<6**(m-1);code++) {
    assert(Date.now()-start<45000,'45 second internal limit');
    let dirs=[0], n=code;
    for(let e=1;e<m;e++) {dirs.push(n%6);n=Math.floor(n/6);}
    let opts=Array.from({length:6},(_,j)=>palettes.filter(p=>(p&allowed(m,dirs,j,true)) && (p&allowed(m,dirs,j,false))));
    if(opts.some(o=>!o.length)) continue;
    function dfs(w) {
      if(w.length===6) return w;
      for(let p of opts[w.length]) {
        if(w.length && (p&w.at(-1))) continue;
        if(w.length===5 && (p&w[0])) continue;
        let out=dfs([...w,p]); if(out) return out;
      }
      return null;
    }
    let w=dfs([]);
    if(w) {
      verify(m,dirs,w);
      return {cycle_length:m,vector_angle_units_pi_over_3:dirs,palettes:w.map(asList),
        signs:Array.from({length:6},(_,j)=>dirs.map(v=>Number(sign(j,v))))};
    }
  }
  return null;
}
// Rational bounds in the annulus proof, checked only by exact integers.
assert(9>8);                    // 1/2 > (2/3)^2.
assert(3*81>14*14);             // sqrt(3)>14/9; hence cos(75 degrees)<1/3.
assert(2**2*3+2*101**2<3*100**2); // (1/50)^2+(2/3)(101/100)^2<1.
assert(4*99**2>3*100**2);       // (4/3)(99/100)^2>1.
let pairs=[];
for(let a=0;a<9;a++) for(let b=a+1;b<9;b++) if(a%3===b%3) {
  assert.equal(Math.min(b-a,9-(b-a)),3); pairs.push([a,b]);
}
let result={scope:'Local relaxations only; no global weak plane colouring',
  annulus:{inner_radius:'99/100',outer_radius:'101/100',
    same_sector_distance_squared_upper:'10207/15000',
    different_same_colour_distance_squared_lower:'3267/2500',
    same_colour_sector_pairs:pairs,ternary_centre_ball_radius:'1/200'},
  interface_orbits:[]};
for(let m=3;m<=6;m++) {let w=solve(m);assert(w);result.interface_orbits.push(w);}
result.milliseconds=Date.now()-start;
let json=JSON.stringify(result,null,2)+'\n';
writeFileSync(new URL('exact-obstacles.json',import.meta.url),json);
process.stdout.write(json);
