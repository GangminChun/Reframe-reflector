
import json
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from pathlib import Path
import pandas as pd

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

# Mapping to frame name
frame_map = {
    "1. 거짓말은 항상 잘못이다": "도덕",
    "2. 감정을 보호할 목적이라면 정당화될 수 있다": "감정",
    "3. 법적으로 처벌 대상이 아니므로 괜찮다": "법적 기준"
}

# Convert and sort by time
log_entries = []
for entry in data:
    try:
        ts = datetime.fromisoformat(entry["timestamp"])
        frame = frame_map.get(entry["user_selection"])
        if frame:
            log_entries.append((ts, frame))
    except Exception:
        continue

log_entries.sort()

# Count frame-to-frame transitions
transition_matrix = {
    "도덕": {"도덕": 0, "감정": 0, "법적 기준": 0},
    "감정": {"도덕": 0, "감정": 0, "법적 기준": 0},
    "법적 기준": {"도덕": 0, "감정": 0, "법적 기준": 0},
}

for i in range(1, len(log_entries)):
    prev_frame = log_entries[i - 1][1]
    curr_frame = log_entries[i][1]
    transition_matrix[prev_frame][curr_frame] += 1

# Create DataFrame
df = pd.DataFrame(transition_matrix)

# Plot heatmap
plt.figure(figsize=(6, 5))
sns.heatmap(df, annot=True, fmt="d", cmap="Reds", cbar=True)
plt.title("RE:FRAME REFLECTOR | 판단 프레임 전이 위험 히트맵")
plt.xlabel("다음 판단 프레임")
plt.ylabel("이전 판단 프레임")
plt.tight_layout()
plt.savefig("data/philosophical_frame_risk_heatmap.png")
print("시각화 완료: data/philosophical_frame_risk_heatmap.png")
