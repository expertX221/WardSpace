"""Download the completed run's best artifact with atomic replacement."""
import hashlib
import json
import os
from pathlib import Path
from adaption import Adaption

root = Path(__file__).resolve().parents[1]
config = json.loads((root / 'training/run-config.json').read_text())
client = Adaption()
run = client.autoscientist.get(config['run_id'])
if run.status != 'succeeded' or not run.download_available:
    raise SystemExit(f'Checkpoint unavailable. Run status is {run.status}.')
artifacts = root / 'artifacts'
artifacts.mkdir(exist_ok=True)
target = artifacts / 'best-checkpoint.tgz'
temporary = target.with_suffix('.part')
with client.autoscientist.with_streaming_response.download(run.id) as response:
    response.stream_to_file(temporary)
os.replace(temporary, target)
digest = hashlib.file_digest(target.open('rb'), 'sha256').hexdigest()
(artifacts / 'manifest.json').write_text(json.dumps({'run_id': run.id, 'sha256': digest, 'bytes': target.stat().st_size}, indent=2))
print(target, digest)
