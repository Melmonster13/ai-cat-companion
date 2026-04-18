import csv
from pathlib import Path
from datetime import datetime

FEEDBACK_PATH = Path("data/feedback/user_corrections.csv")
FIELDNAMES = [
    "timestamp", "time_of_day", "activity", "tail_position",
    "ear_direction", "food_eaten", "predicted_mood", "corrected_mood"
]

def save_correction(input_data: dict, predicted: str, corrected: str):
    FEEDBACK_PATH.parent.mkdir(parents=True, exist_ok=True)
    write_header = not FEEDBACK_PATH.exists()
    with open(FEEDBACK_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if write_header:
            writer.writeheader()
        writer.writerow({
            "timestamp":      datetime.now().isoformat(),
            "predicted_mood": predicted,
            "corrected_mood": corrected,
            **input_data,
        })

def load_corrections():
    if not FEEDBACK_PATH.exists():
        return []
    with open(FEEDBACK_PATH) as f:
        return list(csv.DictReader(f))

def correction_count():
    return len(load_corrections())