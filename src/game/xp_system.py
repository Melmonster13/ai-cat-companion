import json
from pathlib import Path

XP_THRESHOLDS = {
    "rookie":    {"min_xp": 0,   "required_accuracy": 0.0,  "label": "Rookie Cat"},
    "learner":   {"min_xp": 10,  "required_accuracy": 0.75, "label": "Learner Cat"},
    "skilled":   {"min_xp": 25,  "required_accuracy": 0.80, "label": "Skilled Cat"},
    "expert":    {"min_xp": 50,  "required_accuracy": 0.85, "label": "Expert Cat"},
    "legendary": {"min_xp": 100, "required_accuracy": 0.90, "label": "Legendary Cat"},
}

DEFAULT_STATE = {
    "xp": 0,
    "total_predictions": 0,
    "correct_predictions": 0,
    "level": "rookie",
    "corrections": [],
}

def load_state(path="data/feedback/xp_state.json"):
    p = Path(path)
    if p.exists():
        with open(p) as f:
            return json.load(f)
    return DEFAULT_STATE.copy()

def save_state(state, path="data/feedback/xp_state.json"):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(state, f, indent=2)

def record_prediction(state, correct: bool):
    state["total_predictions"] += 1
    if correct:
        state["correct_predictions"] += 1
        state["xp"] += 2
    else:
        state["xp"] += 1   # partial XP for engagement
    state["level"] = _calculate_level(state)
    return state

def record_correction(state, original_pred, corrected_mood, input_data):
    state["corrections"].append({
        "original": original_pred,
        "corrected": corrected_mood,
        "input": input_data,
    })
    return state

def get_accuracy(state):
    if state["total_predictions"] == 0:
        return 0.0
    return state["correct_predictions"] / state["total_predictions"]

def _calculate_level(state):
    acc = get_accuracy(state)
    xp  = state["xp"]
    level = "rookie"
    for name, rules in XP_THRESHOLDS.items():
        if xp >= rules["min_xp"] and acc >= rules["required_accuracy"]:
            level = name
    return level

def xp_to_next_level(state):
    levels = list(XP_THRESHOLDS.keys())
    current_idx = levels.index(state["level"])
    if current_idx == len(levels) - 1:
        return None, None   # already legendary
    next_level = levels[current_idx + 1]
    needed_xp  = XP_THRESHOLDS[next_level]["min_xp"]
    needed_acc = XP_THRESHOLDS[next_level]["required_accuracy"]
    return needed_xp - state["xp"], needed_acc