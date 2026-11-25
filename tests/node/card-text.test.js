/* Card wording is written for job seekers (KT, 25 Nov 2026). Uses the real jobs.json where noted. */
const test = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');
const T = require('../../card-text.js');

const MACHINE = /location field|the listing|description|eligibility|not confirmed|unclear|structured|classif|wording conflicts|confirm how|check the employer/i;
const LIVE = { skip: process.env.YC_SKIP_LIVE_DATA === '1' && 'live-data test: skipped inside the refresh' };

test('known locations read as a place, worldwide reads as Worldwide, unknown reads as nothing', () => {
  assert.strictEqual(T.applyFrom({ eligibility: { type: 'countries', label: 'United States only' } }), 'United States');
  assert.strictEqual(T.applyFrom({ eligibility: { type: 'worldwide', label: 'Worldwide' } }), 'Worldwide');
  assert.strictEqual(T.applyFrom({ eligibility: { type: 'unclear', label: 'Eligibility unclear' } }), null);
});

test('the classifier notes become short plain lines, and the rest stay hidden', () => {
  const job = {
    unresolvedQuestions: ['Occasional office or in-person attendance is mentioned; confirm how often.',
      'The location field names a place but does not say the role is remote there; confirm whether applicants elsewhere are accepted.'],
    eligibility: { notes: ['The posting says it cannot hire in: Belarus, Cuba, Iran and others.'] },
  };
  assert.deepStrictEqual(T.heads(job), ['May need occasional office visits', 'Not open to applicants in: Belarus, Cuba, Iran and some others']);
});

test('quotes leave out our working notes', () => {
  const job = { evidence: [
    { signal: 'structured work-arrangement field', text: 'field says remote (Remote)', effect: 'remote' },
    { signal: 'description (explicitly no office)', text: 'Compensation varies by office location', effect: 'remote' },
    { signal: 'description', text: 'This role is remote based in North America.', effect: 'remote' },
  ] };
  assert.deepStrictEqual(T.quotes(job), ['This role is remote based in North America.']);
  assert.deepStrictEqual(T.quotes({ regionAsStated: 'remote', evidence: [{ signal: 'location field', text: 'remote', effect: 'remote' }] }), [], 'no quote that repeats the location line');
});

test('no card line on the real board talks like a machine (real data)', LIVE, () => {
  const jobs = JSON.parse(fs.readFileSync(path.join(__dirname, '..', '..', 'jobs.json'), 'utf8'));
  for (const j of jobs) {
    for (const line of T.heads(j).concat([T.applyFrom(j) || ''])) {
      assert.ok(!MACHINE.test(line), `${j.company} | ${j.title}: "${line}"`);
    }
  }
});
