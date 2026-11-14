import fs from 'node:fs';
import assert from 'node:assert/strict';
import path from 'node:path';

// Independent certificate checker. Does not import either lead's search code.
const root = path.resolve(import.meta.dirname, '..', '..');
const start = performance.now();
const six = JSON.parse(fs.readFileSync(path.join(root, 'work/astra-six-colour/exact-obstacles.json'), 'utf8'));
const joint = JSON.parse(fs.readFileSync(path.join(root, 'work/astra-joint-state/joint-word-audit.json'), 'utf8'));
const intersection = (a, b) => a.filter(x => b.includes(x));
const same = (a, b) => [...new Set(a)].sort().join(',') === [...new Set(b)].sort().join(',');
const mod = (n, m) => ((n % m) + m) % m;
const adjacent = (a, b) => mod(a - b, 5) === 1 || mod(b - a, 5) === 1;
const edge = (a, b) => [a, b].sort().join(',');

// The sector-distance bounds are rational consequences of the stated
// trigonometric estimates; those trigonometric estimates are checked on paper.
assert.equal(4 * 3 + 2 * 10201, 2 * 10207);
assert(10207 < 15000);
assert.equal(4 * 9801, 12 * 3267);
assert(3267 > 2500);
let sameColourPairs = 0;
for (let a = 0; a < 9; a++) for (let b = a + 1; b < 9; b++) {
  if (a % 3 !== b % 3) continue;
  sameColourPairs++;
  const circularIndexGap = Math.min(b - a, 9 - (b - a));
  assert.equal(circularIndexGap, 3); // sector angular distance infimum = 80 degrees
}
assert.equal(sameColourPairs, 9);

const cosSigns = [1, 1, 0, 0, 0, 1]; // cos(j*pi/3), none zero
const finiteCycles = [];
for (const cert of six.interface_orbits) {
  const m = cert.cycle_length;
  assert(m >= 3 && m <= 6);
  assert.equal(cert.palettes.length, 6);
  assert.equal(cert.vector_angle_units_pi_over_3.length, m);
  const edges = Array.from({length: m}, (_, i) => [i, (i + 1) % m]);
  for (let j = 0; j < 6; j++) {
    const palette = cert.palettes[j];
    assert(palette.length >= 1 && palette.length <= 2);
    assert(palette.every(x => Number.isInteger(x) && x >= 0 && x < 6));
    assert.equal(new Set(palette).size, palette.length);
    assert.equal(intersection(palette, cert.palettes[(j + 1) % 6]).length, 0);
    const signs = cert.vector_angle_units_pi_over_3.map(q => cosSigns[mod(j - q, 6)]);
    assert.deepEqual(signs, cert.signs[j]);
    assert(signs.every((s, i) => 1 - s === cert.signs[(j + 3) % 6][i]));
    for (const side of [0, 1]) {
      const excluded = edges.flatMap((e, i) => signs[i] === side ? e : []);
      const allowed = [0, 1, 2, 3, 4, 5].filter(x => !excluded.includes(x));
      assert(intersection(palette, allowed).length > 0);
    }
    for (const e of edges) assert(!palette.every(x => e.includes(x)));
  }
  finiteCycles.push({m, accepted: true});
}
assert.deepEqual(finiteCycles.map(x => x.m), [3, 4, 5, 6]);

const words = [];
for (let code = 0; code < 5 ** 6; code++) {
  let n = code;
  const w = [];
  for (let i = 0; i < 6; i++) { w.push(n % 5); n = Math.floor(n / 5); }
  if (w.every((x, i) => adjacent(x, w[(i + 1) % 6]))) words.push(w);
}
assert.equal(words.length, 100);
const primary = [];
for (const cert of joint.models) {
  const lists = cert.lists;
  assert.equal(lists.length, 6);
  assert(lists.every(x => x.length > 0));
  assert(lists[0].includes(0) && lists[0].includes(1));
  for (const j of [0, 3]) assert(lists[j].some(x => lists[j].some(y => adjacent(x, y))));
  for (let j = 0; j < 6; j++) {
    const a = lists[j], b = lists[(j + 1) % 6];
    assert.equal(intersection(a, b).length, 0);
    assert(a.every(x => b.some(y => adjacent(x, y))));
    assert(b.every(x => a.some(y => adjacent(x, y))));
  }
  const compatible = words.filter(w => w.every((x, i) => lists[i].includes(x)));
  assert(lists.every((list, i) => same(list, compatible.map(w => w[i]))));
  assert.equal(compatible.length, cert.jointWords.length);
  assert(same(compatible.map(w => w.join('')), cert.jointWords.map(w => w.join(''))));
  const bans = new Set(lists.flatMap(list => list.flatMap(x =>
    list.filter(y => adjacent(x, y)).map(y => edge(x, y)))));
  const survivors = compatible.filter(w => w.every((x, i) => !bans.has(edge(x, w[(i + 1) % 6]))));
  assert(same([...bans], cert.contacts));
  assert(same(survivors.map(w => w.join('')), cert.survivors.map(w => w.join(''))));
  const projectionRetained = lists.every((list, i) => same(list, survivors.map(w => w[i])));
  assert(!projectionRetained);
  primary.push({compatible: compatible.length, survivors: survivors.length, projectionRetained});
}
assert.equal(primary.length, 8);
const result = {
  status: 'PASS', scope: 'Certificate verification; no global-colouring realization or completeness of model search asserted',
  sameColourPairs, closedC5Words: words.length, finiteCycles, primary,
  milliseconds: Math.round(performance.now() - start)
};
fs.writeFileSync(path.join(root, 'work/astra-referee/certificate-check.json'), JSON.stringify(result, null, 2) + '\n');
console.log(JSON.stringify(result));
