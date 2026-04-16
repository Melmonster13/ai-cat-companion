import pandas as pd
import numpy as np

ACTIVITIES = ["sleeping", "playing", "eating", "grooming", "hunting", "hiding"]
TAIL_POSITIONS = ["up", "down", "tucked", "swishing", "puffed"]
EAR_DIRECTIONS = ["forward", "backward", "flat", "rotating"]
MOODS = ["happy", "grumpy", "playful", "anxious", "sleepy"]

MOOD_RULES = {
    "happy": {"activity": ["eating", "grooming"], "tail": ["up"], "ear": ["forward"],
              "food_range": (0.6, 1.0)},
    "grumpy": {"activity": ["hiding", "grooming"], "tail": ["swishing", "down"], "ear": ["backward", "flat"],
               "food_range": (0.0, 0.3)},
    "playful": {"activity": ["playing", "hunting"], "tail": ["up", "swishing"], "ear": ["forward", "rotating"],
                "food_range": (0.3, 0.7)},
    "anxious": {"activity": ["hiding", "hunting"], "tail": ["tucked", "puffed"], "ear": ["flat", "rotating"],
                "food_range": (0.1, 0.4)},
    "sleepy": {"activity": ["sleeping", "grooming"], "tail": ["down", "tucked"], "ear": ["backward"],
               "food_range": (0.4, 0.8)},
}

def generate_dataset(n_samples=2000,
                     noise_rate=0.35, seed=42):
    rng = np.random.default_rng(seed)
    rows = []

    for _ in range(n_samples):
        mood = rng.choice(MOODS)
        rules = MOOD_RULES[mood]

        if rng.random() < noise_rate:
            activity = rng.choice(ACTIVITIES)
            tail = rng.choice(TAIL_POSITIONS)
            ear = rng.choice(EAR_DIRECTIONS)
        else:
            activity = rng.choice(rules["activity"])
            tail = rng.choice(rules["tail"])
            ear = rng.choice(rules["ear"])

        food_lo, food_hi = rules["food_range"]
        food_eaten = round(float(rng.uniform(food_lo, food_hi)), 2)
        time_of_day = round(float(rng.uniform(0, 24)), 1)

        rows.append({
            "time_of_day": time_of_day,
            "activity": activity,
            "tail_position": tail,
            "ear_direction": ear,
            "food_eaten": food_eaten,
            "mood": mood,
        })

    return pd.DataFrame(rows)

if __name__ == "__main__":
    from pathlib import Path
    project_root = Path(__file__).resolve().parent.parent.parent
    output_path = project_root / "data" / "raw" / "cat_behavior_synthetic.csv"
    df = generate_dataset()
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} rows -> {output_path}")
    print(df["mood"].value_counts())
