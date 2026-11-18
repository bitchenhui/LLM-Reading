const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const {searchEvidence, containsTerm} = require('../scripts/site_discovery.js');
const page = fs.readFileSync('site/index.html', 'utf8');
const data = JSON.parse(page.split('const DATA = ')[1].split(';\nconst DN = ')[0]);
const items = Object.values(data.items_by_domain).flat();
const search = query => searchEvidence(query, items, data.topics);

test('Chinese VVenC question retrieves the paper through its encoding protocol', () => {
  const found = search('VVenC 怎么优化');
  assert.deepEqual(found.topics.map(t => t.id), ['impl:VVenC']);
  const paper = found.matches.find(h => h.item.id === 'paper:arxiv:2601.10607');
  assert.ok(paper);
  assert.equal(paper.claims.filter(c => c.evidence_url).length, 3);
});
test('Inter-4K query preserves exact evidence and signed decoding tradeoff', () => {
  const hit = search('Inter-4K').matches.find(h => h.item.id === 'paper:arxiv:2601.10607');
  const claim = hit.claims.find(c => c.id === '032cdc0cf07f');
  assert.match(claim.statement, /增加 52.16%/);
  assert.equal(claim.confidence, 'reported');
  assert.match(claim.evidence_url, /#S5.T2.6.1.22.3$/);
});
test('claim-only terms are searchable; unrelated queries return no invented answers', () => {
  const claim = {statement:'特殊实验结论XYZ', id:'example', metrics:[]};
  const item = {...items[0], claims:[claim], entities:[], protocol:{}};
  assert.equal(searchEvidence('特殊实验结论XYZ', [item], []).matches.length, 1);
  assert.equal(search('not-a-real-codec-zzzz98765').matches.length, 0);
  assert.equal(searchEvidence('怎么优化', items, []).matches.length, 0);
});
test('English aliases respect boundaries and nested aliases do not over-constrain', () => {
  assert.equal(containsTerm('available', 'AV1'), false);
  assert.equal(containsTerm('VVenC怎么优化', 'VVenC'), true);
  assert.equal(containsTerm('VVenCExtra', 'VVenC'), false);
  const result = search('SVT-AV1');
  assert.ok(result.topics.some(t => t.id === 'impl:SVT-AV1'));
  assert.ok(!result.topics.some(t => t.id === 'codec:AV1'));
});
test('every surfaced claim resolves to its generated article anchor', () => {
  for (const item of items) {
    const [file, hash] = item.detail.split('#');
    const detail = fs.readFileSync('site/' + file, 'utf8');
    for (const claim of item.claims) {
      const anchor = decodeURIComponent(hash) + '/' + claim.id;
      assert.ok(detail.includes(`id="${anchor}"`), anchor);
    }
  }
});
