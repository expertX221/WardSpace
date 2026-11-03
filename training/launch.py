"""Launch a new experiment. Existing competition run is in run-config.json."""
import argparse
import json
import time
from pathlib import Path
from adaption import Adaption

parser = argparse.ArgumentParser()
parser.add_argument('--launch', action='store_true', help='Upload training data and start a new AutoScientist run')
args = parser.parse_args()
if not args.launch:
    parser.exit(message='Use monitor.py to inspect the existing run. Pass --launch to create a new experiment.\n')
root = Path(__file__).resolve().parent
state_path = root / 'new-experiment.json'
state = json.loads(state_path.read_text()) if state_path.exists() else {}
client = Adaption()
if 'dataset_id' not in state:
    dataset = client.datasets.upload_file(root / 'train.csv', name='WardSpace synthetic handoff', processing_mode='raw', column_mapping={'prompt':'instruction', 'completion':'response'})
    state['dataset_id'] = dataset.dataset_id
    state_path.write_text(json.dumps(state, indent=2))
for _ in range(120):
    status = client.datasets.get_status(state['dataset_id'])
    if status.status == 'failed':
        raise RuntimeError('Dataset ingestion failed')
    if status.row_count is not None:
        break
    time.sleep(5)
else:
    raise RuntimeError('Dataset is still ingesting. Rerun this command to resume.')
if 'run_id' not in state:
    run = client.autoscientist.create(dataset_id=state['dataset_id'], max_iterations=3, idempotency_key='wardspace-' + state['dataset_id'])
    state['run_id'] = run.id
    state_path.write_text(json.dumps(state, indent=2))
print(json.dumps(state, indent=2))
