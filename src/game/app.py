import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import joblib
import streamlit as st
from src.models.predict import predict_mood
from src.game.xp_system import (
    load_state, save_state, record_prediction,
    record_correction, get_accuracy, xp_to_next_level,
    XP_THRESHOLDS,
)
from src.game.sprite_manager import get_cat_image, LEVEL_STYLE, get_mood_caption
from src.game.feedback_loop import save_correction, correction_count, load_corrections

# ── Page config ──────────────────────────────────────────────
st.set_page_config(page_title="AI Cat Companion", page_icon="🐱", layout="centered")

# ── Load models ───────────────────────────────────────────────
@st.cache_resource
def load_models():
    root = Path(__file__).resolve().parent.parent.parent
    models = root / "artifacts" / "models"
    return (
        joblib.load(models / "rf_model.pkl"),
        joblib.load(models / "cat_encoder.pkl"),
        joblib.load(models / "label_encoder.pkl"),
    )

model, cat_enc, label_enc = load_models()

# ── Session state ─────────────────────────────────────────────
if "xp_state" not in st.session_state:
    st.session_state.xp_state = load_state()
if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None
if "last_input" not in st.session_state:
    st.session_state.last_input = None
if "just_levelled_up" not in st.session_state:
    st.session_state.just_levelled_up = None

state = st.session_state.xp_state

# ── Header ────────────────────────────────────────────────────
st.title("🐱 AI Cat Companion")
st.caption("Enter your cat's behavior and see what mood the AI predicts.")

# ── Level-up banner ───────────────────────────────────────────
if st.session_state.just_levelled_up:
    new_level = st.session_state.just_levelled_up
    label = XP_THRESHOLDS[new_level]["label"]
    badge = LEVEL_STYLE[new_level][2]
    st.success(f"## {badge} LEVEL UP! You reached **{label}**! {badge}")
    st.session_state.just_levelled_up = None

# ── Cat display ───────────────────────────────────────────────
mood_to_show = st.session_state.last_prediction or "happy"
cat_img = get_cat_image(mood_to_show, state["level"])

col_cat, col_info = st.columns([1, 2])
with col_cat:
    st.image(cat_img, width=220)

with col_info:
    level_label = XP_THRESHOLDS[state["level"]]["label"]
    badge = LEVEL_STYLE[state["level"]][2]
    st.markdown(f"### {badge} {level_label}")
    st.markdown(f"**XP:** {state['xp']}")
    st.markdown(f"**Accuracy:** {get_accuracy(state)*100:.1f}%")
    st.markdown(f"**Predictions:** {state['total_predictions']}")
    st.progress(min(state['xp'] / 100, 1.0))

    needed_xp, needed_acc = xp_to_next_level(state)
    if needed_xp:
        st.caption(f"Next level: {needed_xp} more XP + "
                   f"{needed_acc*100:.0f}% accuracy needed")
    else:
        st.caption("👑 Maximum level reached!")

    st.markdown(get_mood_caption(mood_to_show))

# ── Mood history ──────────────────────────────────────────────
if "mood_history" not in st.session_state:
    st.session_state.mood_history = []

if st.session_state.last_prediction:
    history = st.session_state.mood_history
    if not history or history[-1] != st.session_state.last_prediction:
        history.append(st.session_state.last_prediction)
        st.session_state.mood_history = history[-8:]  # keep last 8

if st.session_state.mood_history:
    st.caption("Recent moods: " + "  →  ".join(st.session_state.mood_history))

st.divider()

# ── Input form ────────────────────────────────────────────────
st.subheader("What is your cat doing?")

with st.form("behavior_form"):
    col1, col2 = st.columns(2)
    with col1:
        time_of_day  = st.slider("Time of day (hour)", 0.0, 23.9, 12.0, step=0.1)
        food_eaten   = st.slider("Food eaten (0 = none, 1 = full bowl)", 0.0, 1.0, 0.5, step=0.01)
    with col2:
        activity     = st.selectbox("Activity", ["sleeping", "playing", "eating",
                                                  "grooming", "hunting", "hiding"])
        tail_position = st.selectbox("Tail position", ["up", "down", "tucked",
                                                        "swishing", "puffed"])
        ear_direction = st.selectbox("Ear direction", ["forward", "backward",
                                                        "flat", "rotating"])
    submitted = st.form_submit_button("Predict Mood 🐾")

# ── Prediction ────────────────────────────────────────────────
if submitted:
    input_data = {
        "time_of_day":   time_of_day,
        "activity":      activity,
        "tail_position": tail_position,
        "ear_direction": ear_direction,
        "food_eaten":    food_eaten,
    }
    prediction = predict_mood(model, cat_enc, label_enc, input_data)
    st.session_state.last_prediction = prediction
    st.session_state.last_input = input_data
    st.rerun()

# ── Feedback ──────────────────────────────────────────────────
if st.session_state.last_prediction:
    pred = st.session_state.last_prediction
    st.success(f"Predicted mood: **{pred.upper()}**")

    st.subheader("Was the prediction correct?")
    col_yes, col_no = st.columns(2)

    with col_yes:
        if st.button("✅ Yes, that's right!"):
            prev_level = state["level"]
            state = record_prediction(state, correct=True)
            save_state(state)
            st.session_state.xp_state = state
            if state["level"] != prev_level:
                st.session_state.just_levelled_up = state["level"]
            st.balloons()
            st.rerun()

    with col_no:
        correct_mood = st.selectbox(
            "What mood was it actually?",
            [m for m in label_enc.classes_ if m != pred],
            key="correction_select"
        )
        if st.button("❌ Correct the prediction"):
            prev_level = state["level"]
            save_correction(st.session_state.last_input, pred, correct_mood)
            state = record_prediction(state, correct=False)
            state = record_correction(state, pred, correct_mood,
                                      st.session_state.last_input)
            save_state(state)
            st.session_state.xp_state = state
            if state["level"] != prev_level:
                st.session_state.just_levelled_up = state["level"]
            st.info(f"Saved correction: {pred} → {correct_mood}. "
                    f"Total corrections: {correction_count()}")
            st.rerun()

    # XP progress hint
    needed_xp, needed_acc = xp_to_next_level(state)
    if needed_xp:
        st.caption(f"Next level in {needed_xp} XP "
                   f"(need {needed_acc*100:.0f}% accuracy)")

# ── Correction history ────────────────────────────────────────
corrections = load_corrections()
if corrections:
    st.divider()
    st.subheader("📋 Correction History")
    st.caption(f"{len(corrections)} correction(s) saved — "
               f"this data will train the RL agent in Phase 3.")

    # Most confused pairs
    from collections import Counter
    pairs = Counter(
        f"{c['predicted_mood']} → {c['corrected_mood']}"
        for c in corrections
    )
    st.markdown("**Most common mistakes:**")
    for pair, count in pairs.most_common(3):
        st.markdown(f"- `{pair}` × {count}")

    # Recent corrections table
    import pandas as pd
    df_corrections = pd.DataFrame(corrections[-10:]).iloc[::-1]
    df_corrections = df_corrections[
        ["timestamp", "predicted_mood", "corrected_mood",
         "activity", "food_eaten"]
    ]
    df_corrections.columns = [
        "Time", "Predicted", "Corrected", "Activity", "Food"
    ]
    st.dataframe(df_corrections, use_container_width=True, hide_index=True)