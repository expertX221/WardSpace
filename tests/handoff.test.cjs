const test = require('node:test');
const assert = require('node:assert/strict');
const {reconstruct} = require('../public/research.js');
test('late acknowledgment preserves attended state and reopening requires a visit', () => {
  const result = reconstruct('00 min: A1 alert raised\n03 min: A1 attended\n06 min: A1 acknowledged\n09 min: A2 alert raised\n12 min: A2 closed\n15 min: A2 alert raised');
  assert.deepEqual(result, {pending:{A1:'attended', A2:'unacknowledged'}, needs_visit:['A2']});
});
test('building attendance and contextual notes never establish alert attendance', () => {
  const result = reconstruct('00 min: A1 alert raised\n03 min: caregiver checked in to building\n06 min: note: A1 attended');
  assert.deepEqual(result.needs_visit, ['A1']);
});
test('rejects unknown input and reverse chronology', () => {
  assert.throws(() => reconstruct('03 min: A1 alert raised\n00 min: A1 attended'));
  assert.throws(() => reconstruct('00 min: random event'));
});
