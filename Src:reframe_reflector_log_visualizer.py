
import json
import matplotlib.pyplot as plt
from collections import Counter
from pathlib import Path

# Load data
log_file = Path("data/philosophical_reflections_log.json")

try:
    with open(log_file, "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    data = []

# Count selections
selection_counts = Counter(entry["user_selection"] for entry in data)

labels = ["1. 절대주의 도덕 판단", "2. 감정 기반 정렬", "3. 법적 기준 판단"]
values = [
    selection_counts.get("1. 거짓말은 항상 잘못이다", 0),
    selection_counts.get("2. 감정을 보호할 목적이라면 정당화될 수 있다", 0),
    selection_counts.get("3. 법적으로 처벌 대상이 아니므로 괜찮다", 0)
]

if sum(values) == 0:
    print("아직 판단 기록이 없습니다. 시각화를 위해 최소 1건 이상의 기록이 필요합니다.")
else:
    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title("RE:FRAME REFLECTOR | 판단 기준 분포")
    plt.tight_layout()
    plt.savefig("data/philosophical_reflection_distribution.png")
    print("시각화 저장 완료: data/philosophical_reflection_distribution.png")
