# WardSpace handoff intelligence

WardSpace reconstructs unresolved caregiver alerts from synthetic event histories. It emits `pending` alert states and `needs_visit` IDs. An explicit attended event is required to establish attendance. Notes and building check-in do not establish a visit. Closure removes an alert, and a later raised event reopens it.

## Verified AutoScientist result

- Run `fe9d6d0f-7c4a-4ede-b198-aca407971185`
- Trained model `adaption_qwen3_5_4b_wardspace_caregiver_hand_fe9d6d0f`
- Dataset `09fe8fa8-3537-476d-b586-e0fbf71596c0`
- Platform-selected base model `Qwen/Qwen3.5-4B`
- Successful instruction training, one completed iteration of a maximum of three
- Platform best win rate 91.54%, exceeding the configured 70% target
- Started November 3, 2026 at 4:05:46 PM IST and completed at 4:29:31 PM IST
- LoRA rank 16, alpha 32, dropout 0, one epoch, learning rate 0.00005
- Cosine schedule, warmup ratio 0.03, maximum gradient norm 2, completion-only loss
- Exported trainer state contains 23 global steps and final evaluation loss 0.0293486118

The platform win rate compares model responses on platform evaluations. It is distinct from exact accuracy on the separately reserved 300 cases. Those held-out metrics remain unmeasured because a working inference endpoint for the trained adapter is required.

## Data

The training split contains 1,800 unique synthetic inputs. The held-out split contains 300 unique inputs. Exact input overlap is zero. Both splits sample the same generator distribution with separate seeds. Files, seeds, counts, and hashes are recorded in `training/dataset-manifest.json`. The held-out split was excluded from the Adaption upload.

## Artifact

The downloaded checkpoint is a Zstandard-compressed tar archive, 81,981,852 bytes. It contains 12 archive entries, including LoRA adapter weights, adapter configuration, tokenizer files, and trainer state. Its SHA-256 is `3f215d5df52a60e88a18cad085490765f48c0f99838871753bb6241c1eb9664f`.

The adapter configuration names the training base as `togethercomputer/Qwen3.5-4B`. Deployment must load a compatible base model and this adapter. The adapter archive alone does not contain full base-model weights.

## Runtime status

The original WardSpace 3D demo and deterministic handoff reference engine are functional. The trained adapter is exported. Adaption's public Responses API returned HTTP 404 Model not found for the trained model name. The Adaption interface reports the verified training result and keeps trained inference disabled until a supported endpoint is configured. The current machine reports CPU-only PyTorch and approximately 3.3 GB of available RAM during inspection.

## Scope

All training examples represent fabricated workflow histories. Clinical validation and independent workflow evaluation remain future work. Results do not establish that a patient is safe or that attendance was independently verified.

Training and model optimization were performed with AutoScientist by Adaption.

## Published artifacts

- Original 3D experience and research tools at https://wardspace-healthcare.vercel.app/research.html
- Adaption interface at https://wardspace-handoff.adaptionlabs.app/
- Trained adapter at https://huggingface.co/Saiyv43/WardSpace-Handoff-Qwen3.5-4B-LoRA

The participant chose to retain these artifacts without paid inference hosting. The Hugging Face serving code is prepared, and its deployment remains untested behind the account's compute plan gate. The public leaderboard search did not show a listing for this account during verification. Adaption's domain evaluation was still processing.
