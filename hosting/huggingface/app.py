"""Serve the AutoScientist-exported WardSpace LoRA adapter on ZeroGPU."""
import json
from pathlib import Path

import spaces
import gradio as gr
import torch
from peft import PeftModel
from transformers import AutoTokenizer, Qwen3_5ForConditionalGeneration
from evaluation import validate_prediction

RUN_ID = 'fe9d6d0f-7c4a-4ede-b198-aca407971185'
BASE_MODEL = 'Qwen/Qwen3.5-4B'
ROOT = Path(__file__).resolve().parent
INSTRUCTION = ('Summarize this synthetic WardSpace handoff. Return JSON with pending (alert ID to status) and needs_visit (sorted IDs). Only an explicit alert-specific attended event establishes attendance. Building check-in and notes do not. Closed alerts are excluded. A raised event reopens that alert. Acknowledgment after attendance preserves attended status. Include attended alerts in pending until closed.\n')
EXAMPLE = '00 min: A1 alert raised\n03 min: A1 acknowledged\n06 min: note: will attend soon\n09 min: A2 alert raised\n12 min: A2 attended'

tokenizer = AutoTokenizer.from_pretrained(ROOT, local_files_only=True)
base = Qwen3_5ForConditionalGeneration.from_pretrained(BASE_MODEL, dtype=torch.bfloat16, low_cpu_mem_usage=True)
model = PeftModel.from_pretrained(base, ROOT, is_trainable=False).eval().to('cuda')


@spaces.GPU(duration=60)
def predict(history):
    if not isinstance(history, str) or not history.strip() or len(history) > 20000:
        raise gr.Error('Enter a synthetic history between 1 and 20,000 characters.')
    messages = [{'role': 'user', 'content': INSTRUCTION + history.strip()}]
    inputs = tokenizer.apply_chat_template(messages, add_generation_prompt=True, enable_thinking=False, tokenize=True, return_dict=True, return_tensors='pt').to('cuda')
    if inputs['input_ids'].shape[-1] > 8192:
        raise gr.Error('History exceeds the 8,192 token demo limit.')
    with torch.inference_mode():
        output = model.generate(**inputs, max_new_tokens=512, do_sample=False, use_cache=True, pad_token_id=tokenizer.pad_token_id)
    text = tokenizer.decode(output[0, inputs['input_ids'].shape[-1]:], skip_special_tokens=True).strip()
    try:
        result = validate_prediction(text)
    except (ValueError, TypeError, json.JSONDecodeError):
        raise gr.Error('The trained model returned an invalid structured answer. Please retry with a shorter synthetic history.')
    return result, {'run_id': RUN_ID, 'base_model': BASE_MODEL, 'source': 'AutoScientist trained LoRA adapter', 'platform_win_rate': 0.9154}


with gr.Blocks(title='WardSpace · trained handoff model') as demo:
    gr.Markdown('# WardSpace handoff intelligence\nSynthetic workflow histories · AutoScientist by Adaption · platform win rate **91.54%**')
    gr.Markdown('[Open the original 3D WardSpace experience](https://wardspace-healthcare.vercel.app/)')
    history = gr.Textbox(label='Synthetic events, oldest first', value=EXAMPLE, lines=10, max_lines=24)
    submit = gr.Button('Run trained model', variant='primary')
    result = gr.JSON(label='Model prediction')
    evidence = gr.JSON(label='Model provenance')
    submit.click(predict, inputs=history, outputs=[result, evidence], api_name='predict', concurrency_limit=1)
    gr.Markdown('This demo loads the exported trained adapter on the public Qwen3.5-4B base. The export names a Together-hosted mirror of that model. Held-out evaluation must verify the deployed combination. All cases are synthetic. GPU availability and quotas affect response times.')

demo.queue(max_size=8).launch()
