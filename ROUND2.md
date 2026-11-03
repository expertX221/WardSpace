# WardSpace handoff intelligence

Round 2 adds an AutoScientist experiment for reconstructing unfinished caregiver alerts from synthetic event histories. The model learns to emit a JSON object with each open alert's state and the alerts requiring a visit. Reopened alerts, late acknowledgments, closure, contextual notes, and building check-ins appear in the data.

## Current experiment

- AutoScientist run `fe9d6d0f-7c4a-4ede-b198-aca407971185`
- Dataset `09fe8fa8-3537-476d-b586-e0fbf71596c0`
- Platform-selected Qwen/Qwen3.5-4B with instruction training
- Up to three optimization iterations, platform target win rate 0.7
- 1,800 synthetic training examples and 300 held-out examples
- Held-out inputs are excluded from the upload and checked for exact prompt overlap
- Training hyperparameters are selected by AutoScientist and recorded in `public/training-run.json` when returned

The run completed successfully with a 91.54% platform best win rate after one iteration. The checkpoint was downloaded and its archive and hash verified. See MODEL_CARD.md for the recorded training setup and runtime limitations.

The separate seeds sample the same generator distribution. A held-out score would measure synthetic task performance. Independent real workflow evaluation remains future work. The interactive research page runs a deterministic reference engine. Trained inference and held-out metrics require a supported endpoint for the exported adapter.

## Open in VS Code

Open the extracted project folder, run `python server.py`, and visit `http://127.0.0.1:8000/research.html`. The existing 3D room and care console remain available at the root. The research page adds a perspective event network with pause and reduced-motion controls.

## Training tools

Create a Python virtual environment, activate it, and install `pip install -r training/requirements.txt`. Set `ADAPTION_API_KEY` in your terminal environment. Keep credentials outside the project and source control.

- `python training/generate.py` regenerates the checked training and held-out files.
- `python training/monitor.py` refreshes the existing run snapshot.
- `python training/download.py` downloads the best checkpoint after the run succeeds and records its SHA-256 hash.
- `python training/evaluate.py predictions.jsonl --model-id MODEL --run-id RUN` scores real model predictions against the held-out cases. It counts missing predictions as failures and rejects duplicate case indices.
- `python training/launch.py --launch` starts a separate experiment, with resumable dataset ingestion and an idempotency key.

The monitor writes a public snapshot. Publish it after checking the API result. If your network uses an enterprise certificate authority, set `SSL_CERT_FILE` to an approved certificate bundle.

## Verification

Run `python -m unittest discover -s tests`, `node --test tests/*.test.cjs`, and `npm ci && npm run build`. The handoff tests cover reopening, late acknowledgment, distracting notes, and malformed chronology.

## Evaluation and submission status

Planned held-out metrics are exact JSON match, per-alert state accuracy, and false attendance or omission rate. These remain unmeasured. The verified platform best win rate is 91.54%. Training completion and artifact availability are verified. Organizer form submission is handled by the participant.

Project URL after deployment is `https://wardspace-healthcare.vercel.app/research.html`. The public training snapshot records the last checked timestamp so judges can distinguish a snapshot from live monitoring.

The original 3D room, cinematic journey, telemetry HUD, care console, and original CSS are retained from the supplied project. Round 2 is an added section below the console. Its standalone lab is available at `/research-lab.html`.

The public Adaption interface is published at `https://wardspace-handoff.adaptionlabs.app/`. Its training result is verified. It displays the model export status and leaves trained inference disabled.

The trained adapter repository is `https://huggingface.co/Saiyv43/WardSpace-Handoff-Qwen3.5-4B-LoRA`. Hugging Face hosting code is prepared under `hosting/huggingface`. This account's Gradio and Docker compute options require PRO. The participant chose to retain the exported model and published Adaption demo without paid hosting, so live trained inference and the separate 300-case evaluation remain pending.
