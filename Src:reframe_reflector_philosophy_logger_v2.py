
import gradio as gr
from datetime import datetime
import json

# JSON log file path
log_file = "philosophical_reflections_log.json"

# Function to save user input to JSON
def save_reflection(prompt, choice, reason):
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
        with open(log_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(entry)

    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return "저장 완료! 철학형 판단이 기록되었습니다."

# Gradio interface
demo = gr.Interface(
    fn=save_reflection,
    inputs=[
        gr.Textbox(label="GPT 발화 예시", lines=2, placeholder="예: Sometimes it's okay to lie if it protects someone's feelings."),
        gr.Radio(choices=[
            "1. 거짓말은 항상 잘못이다",
            "2. 감정을 보호할 목적이라면 정당화될 수 있다",
            "3. 법적으로 처벌 대상이 아니므로 괜찮다"
        ], label="당신의 판단 선택"),
        gr.Textbox(label="선택 이유", lines=2, placeholder="왜 이 판단을 선택하셨나요?")
    ],
    outputs=gr.Textbox(label="결과"),
    title="RE:FRAME REFLECTOR v2.0 — 철학형 판단 기록 시스템",
    description="3가지 판단 중 하나를 선택하고, 이유를 입력하면 기록됩니다."
)

demo.launch()
