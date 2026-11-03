'use strict';
const examples = {
  open: '00 min: A1 alert raised\n03 min: A1 acknowledged\n06 min: note: will attend soon\n09 min: A2 alert raised\n12 min: A2 attended',
  reopened: '00 min: A1 alert raised\n03 min: A1 attended\n06 min: A1 closed\n09 min: A1 alert raised\n12 min: A1 acknowledged',
  distractor: '00 min: A1 alert raised\n03 min: caregiver checked in to building\n06 min: note: previous shift mentioned attendance\n09 min: A2 alert raised\n12 min: A2 attended\n15 min: A2 acknowledged'
};
function reconstruct(history) {
  if (history.length > 20000) throw new Error('Limit the history to 20,000 characters.');
  const states = {};
  const lines = history.split('\n').filter(line => line.trim());
  let previousMinute = -1;
  for (const line of lines) {
    const entry = line.match(/^(\d+) min: (.+)$/);
    if (!entry) throw new Error('Use one event per line in the format 00 min: A1 alert raised.');
    const minute = Number(entry[1]);
    if (minute < previousMinute) throw new Error('Place events in chronological order.');
    previousMinute = minute;
    const event = entry[2].match(/^(A[1-9]\d*) (alert raised|acknowledged|attended|closed)$/);
    if (!event) {
      if (entry[2].startsWith('note: ') || entry[2] === 'caregiver checked in to building') continue;
      throw new Error('Unknown event. Use alert raised, acknowledged, attended, closed, note: text, or caregiver checked in to building.');
    }
    const [, id, action] = event;
    if (action === 'alert raised') states[id] = 'unacknowledged';
    else if (states[id] && states[id] !== 'closed') {
      if (action !== 'acknowledged' || states[id] !== 'attended') states[id] = action;
    }
  }
  const pending = Object.fromEntries(Object.keys(states).sort().filter(id => states[id] !== 'closed').map(id => [id, states[id]]));
  return {pending, needs_visit: Object.keys(pending).filter(id => pending[id] !== 'attended')};
}
if (typeof module !== 'undefined') module.exports = {reconstruct};
if (typeof document !== 'undefined') {
  const byId = id => document.getElementById(id);
  function analyze() {
    byId('error').textContent = '';
    byId('output').textContent = '';
    byId('alertCards').replaceChildren();
    try {
      const result = reconstruct(byId('history').value);
      byId('output').textContent = JSON.stringify(result, null, 2);
      for (const [id, status] of Object.entries(result.pending)) {
        const card = document.createElement('div'); card.className = 'alert-card';
        const name = document.createElement('strong'); name.textContent = id;
        const label = document.createElement('b'); label.textContent = status;
        card.append(name, label); byId('alertCards').append(card);
      }
    } catch (error) { byId('error').textContent = error.message; }
  }
  byId('scenario').addEventListener('change', () => { byId('history').value = examples[byId('scenario').value]; analyze(); });
  byId('analyze').addEventListener('click', analyze);
  byId('history').value = examples.open; analyze();
  fetch('/training-run.json', {cache: 'no-store'}).then(response => { if (!response.ok) throw new Error('Run snapshot unavailable'); return response.json(); }).then(run => {
    byId('runStatus').textContent = run.status;
    byId('winRate').textContent = run.best_win_rate == null ? 'Pending' : `${(run.best_win_rate * 100).toFixed(1)}%`;
    byId('runId').textContent = run.id;
    byId('checked').textContent = new Date(run.checked_at).toLocaleString();
    byId('iterations').textContent = `${run.iterations_completed} / ${run.max_iterations}`;
    byId('runError').textContent = run.error || 'Snapshot of the last verified API response. Refreshes require the training monitor.';
  }).catch(() => { byId('runStatus').textContent = 'Unavailable'; });
  const canvas = byId('network'), ctx = canvas.getContext('2d');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let paused = reduced.matches, frame = null, angle = 0;
  function draw() {
    const width = canvas.width = innerWidth, height = canvas.height = innerHeight;
    ctx.clearRect(0, 0, width, height);
    const points = Array.from({length: 36}, (_, i) => {
      const a = i * 2.4 + angle, y = (i / 35 - .5) * 460;
      const z = Math.sin(a) * 140, scale = 650 / (650 + z);
      return {x: width * .75 + Math.cos(a) * 210 * scale, y: height * .45 + y * scale, z};
    });
    ctx.strokeStyle = '#70cbbd55'; ctx.fillStyle = '#8affdb';
    for (let i = 0; i < points.length; i++) {
      const p = points[i];
      if (i > 0) { ctx.beginPath(); ctx.moveTo(points[i-1].x, points[i-1].y); ctx.lineTo(p.x, p.y); ctx.stroke(); }
      ctx.beginPath(); ctx.arc(p.x, p.y, p.z < 0 ? 3 : 2, 0, Math.PI * 2); ctx.fill();
    }
    if (!paused && !document.hidden) { angle += .003; frame = requestAnimationFrame(draw); }
  }
  function restart() { cancelAnimationFrame(frame); byId('motion').textContent = paused ? 'Play motion' : 'Pause motion'; draw(); }
  byId('motion').addEventListener('click', () => { paused = !paused; restart(); });
  reduced.addEventListener('change', () => { paused = reduced.matches; restart(); });
  document.addEventListener('visibilitychange', restart);
  addEventListener('resize', restart); restart();
}
