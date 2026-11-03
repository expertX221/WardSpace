"""Refresh the public run snapshot without publishing credentials."""
import json
from datetime import datetime, timezone
from pathlib import Path
from adaption import Adaption

root = Path(__file__).resolve().parents[1]
config = json.loads((root / 'training/run-config.json').read_text())
run = Adaption().autoscientist.get(config['run_id'])
snapshot = run.model_dump(mode='json')
snapshot['checked_at'] = datetime.now(timezone.utc).isoformat()
(root / 'public/training-run.json').write_text(json.dumps(snapshot, indent=2))
print(run.id, run.status, run.iterations_completed, run.best_win_rate)
