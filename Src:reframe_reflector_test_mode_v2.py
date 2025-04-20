
import gradio as gr
import json
from datetime import datetime
import random

# Load prompts
with open("data/philosophical_test_prompts_v1.json", "r", encoding="utf-8") as f:
    test_prompts = json.load(f)

# Log path
log_path = "data/philosophical_reflections_log.json"

# Save function
def run_test(choice, reason, prompt_idx):
    prompt = test_prompts[prompt_idx]
    entry = {
        "prompt": prompt,
        "choices": [
            "거짓말은 항상 잘못이다",
            "감정을 보호할 목적이라면 정당화될 수 있다",
            "법적으로 처벌 대상이 아니므로 괜찮다"
        ],
        "user_selection": choice,
        "user_reason": reason,
        "timestamp": datetime.now().isoformat()
    }

    try:
        with open(log_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(entry)

    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return f"저장 완료!\n\n발화:\n{prompt}\n\n선택: {choice}\n이유: {reason}"

# Random prompt selection
idx = random.randint(0, len(test_prompts) - 1)

# Gradio Interface
demo = gr.Interface(
    fn=lambda choice, reason: run_test(choice, reason, idx),
    inputs=[
        gr.Radio(choices=[
            "1. 거짓말은 항상 잘못이다",
            "2. 감정을 보호할 목적이라면 정당화될 수 있다",
            "3. 법적으로 처벌 대상이 아니므로 괜찮다"
        ], label="당신의 판단 선택"),
        gr.Textbox(label="선택 이유", lines=2, placeholder="왜 이 판단을 선택하셨나요?")
    ],
    outputs="text",
    title="RE:FRAME REFLECTOR v2.1 — 철학형 판단 테스트 모드",
    description=f"GPT 발화: \"{test_prompts[idx]}\""
)

demo.launch()
