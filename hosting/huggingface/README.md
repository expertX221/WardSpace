---
title: WardSpace Handoff Intelligence
emoji: 🏥
colorFrom: indigo
colorTo: purple
sdk: gradio
sdk_version: 6.31.0
app_file: app.py
python_version: 3.12
pinned: false
---

WardSpace serves the exported AutoScientist adapter for reconstructing synthetic caregiver alert histories. Select ZeroGPU hardware before starting this Space. Upload the extracted checkpoint files beside app.py and copy training/evaluate.py to evaluation.py. The adapter contains the tokenizer and PEFT weights. The public Qwen/Qwen3.5-4B base is downloaded at startup.

AutoScientist run fe9d6d0f-7c4a-4ede-b198-aca407971185 completed successfully with 91.54% platform win rate. Independent held-out metrics require evaluation of this deployment. The platform export refers to togethercomputer/Qwen3.5-4B. The Space uses the public canonical Qwen model, and that deployed combination must be tested.

Original 3D demo https://wardspace-healthcare.vercel.app/

Training and optimization by AutoScientist, Adaption.
