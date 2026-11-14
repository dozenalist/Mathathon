import {writeFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
const V=[0,1,2,3,4];
const adj=(i,j)=>[1,4].includes((j-i+5)%5);
const edge=(i,j)=>[i,j].sort((a,b)=>a-b).join(',');
const labels=s=>V.filter(i=>(s>>i)&1);
const valid=s=>labels(s).some(i=>labels(s).some(j=>adj(i,j)));
const compatible=(a,b)=>!(a&b)&&labels(a).every(i=>labels(b).some(j=>adj(i,j)))&&labels(b).every(j=>labels(a).some(i=>adj(i,j)));
const states=Array.from({length:31},(_,i)=>i+1);
const nexts=Object.fromEntries(states.map(a=>[a,states.filter(b=>compatible(a,b))]));
const models=[];
function extend(seq){
  if(seq.length===6){if(compatible(seq[5],seq[0]))models.push(seq); return;}
  for(const b of nexts[seq.at(-1)])if(seq.length!==3||valid(b))extend([...seq,b]);
}
for(const s of states)if((s&3)===3)extend([s]);
const allWords=[];
function words(seq){
  if(seq.length===6){if(adj(seq[5],seq[0]))allWords.push(seq); return;}
  for(const j of V)if(!seq.length||adj(seq.at(-1),j))words([...seq,j]);
}
words([]);
const audits=models.map(ss=>{
  const lists=ss.map(labels);
  const jointWords=allWords.filter(w=>w.every((x,k)=>lists[k].includes(x)));
  const projections=lists.map((_,k)=>[...new Set(jointWords.map(w=>w[k]))].sort());
  const contacts=[...new Set(lists.flatMap(ls=>ls.flatMap(i=>ls.filter(j=>adj(i,j)).map(j=>edge(i,j)))))].sort();
  const survivors=jointWords.filter(w=>w.every((x,k)=>!contacts.includes(edge(x,w[(k+1)%6]))));
  const survivingProjections=lists.map((_,k)=>[...new Set(survivors.map(w=>w[k]))].sort());
  return {lists,jointWords,exactProjection:JSON.stringify(projections)===JSON.stringify(lists),contacts,survivors,survivingProjections,allSupportMembershipsRetained:JSON.stringify(survivingProjections)===JSON.stringify(lists)};
});
const result={rawWords:5**6,closedC5Words:allWords.length,normalizedHistoricModels:models.length,models:audits};
const output=fileURLToPath(new URL('joint-word-audit.json',import.meta.url));
writeFileSync(output,JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({rawWords:result.rawWords,closedC5Words:allWords.length,normalizedHistoricModels:models.length,exactProjectionCount:audits.filter(a=>a.exactProjection).length,jointWordCounts:audits.map(a=>a.jointWords.length),survivingCounts:audits.map(a=>a.survivors.length),supportProjectionSurvivesContactBans:audits.map(a=>a.allSupportMembershipsRetained),output},null,2));
