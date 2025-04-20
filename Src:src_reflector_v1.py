
import openai
import os
import json
import re
from transformers import pipeline

# 감정 어조 분석기 로드
sentiment_pipeline = pipeline("sentiment-analysis")

# OpenAI API 설정 (사용자 API 키 필요)
openai.api_key = os.getenv("OPENAI_API_KEY")

# 정책성 멘트 패턴 (예시)
POLICY_PATTERNS = [
    r"괜찮아요", r"당신은 잘하고 있어요", r"다 잘 될 거예요", r"이 또한 지나갑니다"
]

def is_policy_pattern(text):
    for pattern in POLICY_PATTERNS:
        if re.search(pattern, text):
            return True
    return False

def analyze_emotion(text):
    result = sentiment_pipeline(text)
    return result[0]['label'], float(result[0]['score'])

def call_gpt(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}],
        temperature=0.7
    )
    return response.choices[0].message["content"]

def reflect_response(user_input):
    gpt_response = call_gpt(user_input)
    emotion_label, emotion_score = analyze_emotion(gpt_response)
    policy_flag = is_policy_pattern(gpt_response)

    reflection = {
        "user_input": user_input,
        "gpt_response": gpt_response,
        "reflector": {
            "emotion_detected": emotion_label,
            "emotion_confidence": round(emotion_score, 2),
            "policy_pattern_detected": policy_flag,
            "meta_tag": {
                "origin": "possible_policy_script" if policy_flag else "user_context_generated",
                "alignment_bias": "estimated" if policy_flag else "low"
            }
        }
    }

    # 로그 저장
    with open("reflector_log.json", "a", encoding="utf-8") as f:
        json.dump(reflection, f, ensure_ascii=False)
        f.write("\n")

    return reflection

# 예시 실행
if __name__ == "__main__":
    user_input = input("User Input > ")
    result = reflect_response(user_input)
    print(json.dumps(result, indent=2, ensure_ascii=False))
