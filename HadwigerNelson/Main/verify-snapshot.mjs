// Read-only checks for the archived research. Requires Node.js; no packages.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
import { createGunzip } from 'node:zlib';

const root = path.join(path.dirname(fileURLToPath(import.meta.url)), 'ResearchSnapshot');
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const read = relative => fs.readFileSync(path.join(root, relative));
const json = relative => JSON.parse(read(relative).toString('utf8').replace(/^\uFEFF/, ''));
const manifest = json('MANIFEST.json');
const seen = new Set();
let totalBytes = 0;
for (const entry of manifest.files) {
  assert(!entry.path.startsWith('/') && !entry.path.split('/').includes('..') && !entry.path.includes('\\'), 'Unsafe manifest path');
  assert(!seen.has(entry.path), `Duplicate manifest path: ${entry.path}`);
  seen.add(entry.path);
  const data = read(entry.path);
  assert.equal(data.length, entry.bytes, `Size mismatch: ${entry.path}`);
  assert.equal(hash(data), entry.sha256, `Hash mismatch: ${entry.path}`);
  if (entry.encoding === 'gzip') {
    const originalHash=crypto.createHash('sha256');
    let originalBytes=0;
    for await (const chunk of fs.createReadStream(path.join(root,entry.path)).pipe(createGunzip())) {
      originalHash.update(chunk);
      originalBytes+=chunk.length;
    }
    assert.equal(originalBytes,entry.uncompressedBytes,`Decompressed size mismatch: ${entry.path}`);
    assert.equal(originalHash.digest('hex'),entry.uncompressedSha256,`Decompressed hash mismatch: ${entry.path}`);
  }
  totalBytes += data.length;
}
function checkCoverage(dir) {
  for(const entry of fs.readdirSync(dir,{withFileTypes:true})) {
    const file=path.join(dir,entry.name);
    if(entry.isDirectory()){checkCoverage(file);continue;}
    const relative=path.relative(root,file).split(path.sep).join('/');
    if(relative!=='MANIFEST.json')assert(seen.has(relative),`Unmanifested archive file: ${relative}`);
  }
}
checkCoverage(root);

const out = 'local/outputs/';
const cone = json(out+'cone/VALIDATION.json');
assert.equal(cone.status, 'all_modules_consumer_and_axiom_audit_passed');
assert.equal(cone.lean, '4.34.1');
assert.equal(cone.mathlib, 'd13f23b723b8a846827a245b89c10fc7d3f11612');
assert.equal(cone.sorryAx, false);
for (const [name, digest] of Object.entries(cone.hashes)) {
  assert.equal(hash(read(out+'cone/'+name)), digest, `Cone source changed: ${name}`);
}
const audit = read(out+'cone/cone-audit-v3.log').toString('utf8');
assert(audit.includes('Status: passed') && audit.includes('Exit code: 0'));
assert(!audit.includes('sorryAx'));
assert.equal((audit.match(/depends on axioms:/g)||[]).length, 4);
for (const [name, digest] of Object.entries({
  'encoding-refactor/ConditionalSpectrum.lean': 'd26d569088faea89e5ae5cc2309809797fcbe76cf6d927f4484bc39db7880d48',
  'encoding-refactor/ConditionalLimits.lean': '24f89dd33533a0f61b9f35940e43b3a26c2b27b00424949a92cfdafc8de60d9b',
  'three-centre/MovingThreeCentres.lean': 'ee52e7412a6736736dfbc66e3b792f7294db8dd29e93fd5f1d3fe77d4cbd0a16'
})) {
  assert.equal(hash(read(out+name)), digest, `Previously checked source changed: ${name}`);
}

function verifySeparatingColourings(n, edges, colourings, expectedEdges) {
  assert.equal(edges.length, expectedEdges);
  const keys = new Set();
  for (const [a,b] of edges) {
    assert(Number.isInteger(a) && Number.isInteger(b) && 0<=a && a<b && b<n);
    keys.add(`${a},${b}`);
  }
  assert.equal(keys.size, edges.length, 'Duplicate edge');
  assert.equal(colourings.length, 34);
  for (const colours of colourings) {
    assert.equal(colours.length, n);
    assert(colours.every(c => Number.isInteger(c) && 0<=c && c<5));
    assert(edges.every(([a,b]) => colours[a]!==colours[b]), 'Improper colouring');
  }
  const signatures = new Set(Array.from({length:n}, (_,v) => colourings.map(c=>c[v]).join(',')));
  assert.equal(signatures.size,n,'A vertex pair has no separating witness');
  return {vertices:n,edges:edges.length,properFiveColourings:colourings.length,distinctSignatures:signatures.size};
}
const small=json(out+'HEULE553-NO-FORCING-CERTIFICATE.json');
assert.equal(small.vertices,553);
assert.equal(hash(small.edge_text),small.edge_sha256);
const smallEdges=small.edge_text.split(/\r?\n/).filter(x=>x.startsWith('e ')).map(x=>x.trim().split(/\s+/).slice(1).map(v=>Number(v)-1));
const heule553=verifySeparatingColourings(553,smallEdges,small.witnesses,2722);
const large=json(out+'HEULE-UNION-NO-FORCING.json');
assert.equal(large.vertices,1048);
const heule1048=verifySeparatingColourings(1048,large.edges,large.witnesses,5487);
const geometry=json(out+'HEULE-UNION-CERTIFICATE.json');
const canonical=edges=>edges.map(([a,b])=>`${a},${b}`).sort();
assert.deepEqual(canonical(large.edges),canonical(geometry.edges),'No-forcing graph differs from geometric graph');
const unionResult=JSON.parse(execFileSync(process.execPath,[path.join(root,out,'Verify-HeuleUnion.mjs')],{
  encoding:'utf8',timeout:120000,maxBuffer:1024*1024,windowsHide:true
}));
assert.equal(unionResult.passed,true);
assert.equal(unionResult.pairsTested,548628);

console.log(JSON.stringify({
  checkedAtUtc:new Date().toISOString(),status:'passed',
  snapshotIntegrity:{files:seen.size,bytes:totalBytes,algorithm:'SHA-256'},
  frozenLeanSources:{cone:true,encodingR4:true,movingThreeCentres:true,priorConeAxiomAudit:true},
  heule553,heule1048,exactUnionGeometry:unionResult,
  scope:'Archive integrity, recorded-source fidelity, and fresh finite graph/certificate checks. Existing Lean validation logs are preserved; no fresh complete Lean rebuild or new plane bound is claimed.'
},null,2));
