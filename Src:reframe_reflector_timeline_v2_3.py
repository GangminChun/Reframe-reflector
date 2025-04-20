
import json
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path

# Load log file
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

# Mapping selection text to numeric frame code
mapping = {
    "1. 거짓말은 항상 잘못이다": 1,
    "2. 감정을 보호할 목적이라면 정당화될 수 있다": 2,
    "3. 법적으로 처벌 대상이 아니므로 괜찮다": 3
}

# Extract and sort data
timeline_data = []
for entry in data:
    selection = entry["user_selection"]
    timestamp = entry["timestamp"]
    try:
        dt = datetime.fromisoformat(timestamp)
        code = mapping.get(selection)
        if code:
            timeline_data.append((dt, code))
    except Exception:
        continue

# Sort by time
timeline_data.sort()

if not timeline_data:
    print("유효한 판단 기록이 없습니다.")
    exit()

# Split into X and Y
times, codes = zip(*timeline_data)

# Plot
plt.figure(figsize=(10, 4))
plt.plot(times, codes, marker='o', linestyle='-')
plt.yticks([1, 2, 3], ["도덕", "감정", "법적 기준"])
plt.xlabel("시간")
plt.ylabel("선택된 판단 기준")
plt.title("RE:FRAME REFLECTOR | 시간 순 판단 변화")
plt.grid(True)
plt.tight_layout()
plt.savefig("data/philosophical_judgment_timeline.png")
print("시각화 완료: data/philosophical_judgment_timeline.png")
