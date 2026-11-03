import csv, json, random
from pathlib import Path
ROOT = Path(__file__).resolve().parent
def generate(seed, count, destination, excluded=frozenset()):
    rng = random.Random(seed)
    prompts = set()
    rows = []
    while len(rows) < count:
        events = []
        alert_states = {}
        for step in range(rng.randint(5, 24)):
            alert = 'A' + str(rng.randint(1, 4))
            action = rng.choice(['raised', 'acknowledged', 'attended', 'closed', 'note', 'attendance'])
            minute = step * 3 + rng.randint(0, 2)
            if action == 'raised':
                alert_states[alert] = 'unacknowledged'
                text = f'{alert} alert raised'
            elif action in ('acknowledged', 'attended', 'closed'):
                if alert not in alert_states or alert_states[alert] == 'closed':
                    continue
                if action == 'acknowledged' and alert_states[alert] != 'attended':
                    alert_states[alert] = 'acknowledged'
                elif action != 'acknowledged':
                    alert_states[alert] = action
                text = f'{alert} {action}'
            elif action == 'note':
                text = rng.choice(['note: will attend soon', 'note: no visit confirmed', 'note: alert discussed by phone', 'note: previous shift mentioned attendance'])
            else:
                text = 'caregiver checked in to building'
            events.append(f'{minute:02d} min: {text}')
        if not alert_states:
            continue
        prompt = ('Summarize this synthetic WardSpace handoff. Return JSON with pending (alert ID to status) and needs_visit (sorted IDs). Only an explicit alert-specific attended event establishes attendance. Building check-in and notes do not. Closed alerts are excluded. A raised event reopens that alert. Acknowledgment after attendance preserves attended status. Include attended alerts in pending until closed.\n' + '\n'.join(events))
        if prompt in prompts or prompt in excluded:
            continue
        prompts.add(prompt)
        pending = {a: s for a, s in sorted(alert_states.items()) if s != 'closed'}
        response = json.dumps({'pending': pending, 'needs_visit': [a for a, s in pending.items() if s != 'attended']}, separators=(',', ':'))
        rows.append({'instruction': prompt, 'response': response})
    with destination.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['instruction', 'response'])
        writer.writeheader()
        writer.writerows(rows)
    return prompts

train = generate(221, 1800, ROOT / 'train.csv')
test = generate(8173, 300, ROOT / 'heldout.csv', train)
assert not train.intersection(test)
