
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
    print("로그 파일이 존재하지 않습니다.")
    exit()

if not data:
    print("판단 데이터가 없습니다.")
    exit()

# Mapping selection text to frame label
frame_map = {
    "1. 거짓말은 항상 잘못이다": "도덕",
    "2. 감정을 보호할 목적이라면 정당화될 수 있다": "감정",
    "3. 법적으로 처벌 대상이 아니므로 괜찮다": "법적 기준"
}

frame_labels = ["도덕", "감정", "법적 기준"]
frame_counts = Counter()

# Count each selection by frame
for entry in data:
    selection = entry.get("user_selection", "")
    frame = frame_map.get(selection)
    if frame:
        frame_counts[frame] += 1

# Sort results for visualization
sorted_frames = sorted(frame_counts.items(), key=lambda x: x[1], reverse=True)
labels = [x[0] for x in sorted_frames]
values = [x[1] for x in sorted_frames]

if not values:
    print("유효한 판단 프레임 데이터가 없습니다.")
else:
    plt.figure(figsize=(6, 4))
    plt.bar(labels, values)
    plt.xlabel("판단 프레임")
    plt.ylabel("선택 횟수")
    plt.title("RE:FRAME REFLECTOR | 판단 프레임별 선택 비율")
    plt.tight_layout()
    plt.savefig("data/philosophical_frame_distribution.png")
    print("시각화 완료: data/philosophical_frame_distribution.png")
