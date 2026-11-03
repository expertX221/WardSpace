"""Score model predictions against held-out cases, never the reference engine.

Prediction JSONL contains one object per case with `index` and `prediction`.
Prediction can be a JSON string or parsed JSON object. Missing predictions count
as incorrect. Duplicate and out-of-range indices are rejected.
"""
import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def validate_prediction(value):
    if isinstance(value, str):
        value = json.loads(value)
    if not isinstance(value, dict) or set(value) != {'pending', 'needs_visit'}:
        raise ValueError('Expected pending and needs_visit fields')
    pending, visits = value['pending'], value['needs_visit']
    if not isinstance(pending, dict) or not isinstance(visits, list):
        raise ValueError('Invalid field types')
    if any(not isinstance(k, str) or v not in ('unacknowledged', 'acknowledged', 'attended') for k, v in pending.items()):
        raise ValueError('Invalid alert state')
    if any(not isinstance(v, str) for v in visits) or len(set(visits)) != len(visits):
        raise ValueError('Invalid visit IDs')
    if set(visits) != {k for k, v in pending.items() if v != 'attended'}:
        raise ValueError('Visit IDs contradict pending states')
    return value


def score(rows, predictions):
    exact = valid = states_correct = total_states = false_attendance = unsafe_opportunities = 0
    for index, row in enumerate(rows):
        expected = json.loads(row['response'])
        actual = None
        try:
            actual = validate_prediction(predictions.get(index))
            valid += 1
        except (ValueError, TypeError):
            pass
        if actual is not None:
            exact += actual['pending'] == expected['pending'] and set(actual['needs_visit']) == set(expected['needs_visit'])
        for alert in set(expected['pending']) | set(actual['pending'] if actual else {}):
            total_states += 1
            expected_state = expected['pending'].get(alert, 'closed')
            actual_state = actual['pending'].get(alert, 'closed') if actual else None
            states_correct += actual_state == expected_state
        for alert in expected['needs_visit']:
            unsafe_opportunities += 1
            if actual is not None and (alert not in actual['pending'] or actual['pending'][alert] == 'attended'):
                false_attendance += 1
    return {'cases': len(rows), 'valid_json_rate': valid / len(rows), 'exact_match': exact / len(rows), 'alert_state_accuracy': states_correct / total_states if total_states else None, 'false_attendance_or_omission_count': false_attendance, 'visit_required_alerts': unsafe_opportunities, 'false_attendance_or_omission_rate': false_attendance / unsafe_opportunities if unsafe_opportunities else None, 'invalid_or_missing_predictions': len(rows) - valid}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('predictions', type=Path)
    parser.add_argument('--model-id', required=True)
    parser.add_argument('--run-id', required=True)
    parser.add_argument('--heldout', type=Path, default=Path(__file__).with_name('heldout.csv'))
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('evaluation.json'))
    args = parser.parse_args()
    with args.heldout.open(newline='', encoding='utf-8') as source:
        rows = list(csv.DictReader(source))
    if not rows:
        raise ValueError('Held-out file has no cases')
    predictions = {}
    for line in args.predictions.read_text().splitlines():
        item = json.loads(line)
        index = item['index']
        if type(index) is not int or not 0 <= index < len(rows) or index in predictions:
            raise ValueError('Duplicate or invalid prediction index')
        predictions[index] = item['prediction']
    result = score(rows, predictions)
    result.update({'model_id': args.model_id, 'run_id': args.run_id, 'evaluated_at': datetime.now(timezone.utc).isoformat(), 'heldout_sha256': hashlib.sha256(args.heldout.read_bytes()).hexdigest(), 'predictions_sha256': hashlib.sha256(args.predictions.read_bytes()).hexdigest()})
    args.output.write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
