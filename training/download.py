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
temporary = artifacts / 'best-checkpoint.part'
with client.autoscientist.with_streaming_response.download(run.id) as response:
    response.stream_to_file(temporary)
with temporary.open('rb') as archive:
    magic = archive.read(4)
suffix = {b'\x28\xb5\x2f\xfd': '.tar.zst', b'PK\x03\x04': '.zip'}.get(magic, '.tar.gz' if magic.startswith(b'\x1f\x8b') else '.archive')
target = artifacts / ('best-checkpoint' + suffix)
os.replace(temporary, target)
with target.open('rb') as archive:
    digest = hashlib.file_digest(archive, 'sha256').hexdigest()
(artifacts / 'manifest.json').write_text(json.dumps({'run_id': run.id, 'sha256': digest, 'bytes': target.stat().st_size, 'format': suffix}, indent=2))
print(target, digest)
