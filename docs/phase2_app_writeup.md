# Phase 2 — Streamlit UI & Feedback Loop

## Deliverables
- Interactive Streamlit app with behavior input form
- PIL-drawn cat sprite with five mood expressions (happy, grumpy, playful, anxious, sleepy)
- Level progression system: Rookie → Learner → Skilled → Expert → Legendary
- User corrections persisted to `data/feedback/user_corrections.csv`
- Correction history table and "most confused pairs" analysis
- Deployed to Streamlit Cloud with auto-bootstrap on cold start

## Architecture Decisions
- **PIL-drawn sprites** over external assets — fully self-contained repo, no license issues
- **Absolute paths** via `Path(__file__).resolve().parent.parent.parent` — works regardless of where Streamlit is launched
- **Lazy model bootstrap** — app regenerates dataset and trains models on first run if `.pkl` files are missing (keeps repo lightweight, enables one-click deploy)
- **Session state** via `st.session_state` for level-up detection and UI flow

## Metrics
- Model backing the UI: Random Forest, test accuracy 0.843
- Categorical encoder fitted on explicit `KNOWN_CATEGORIES` to prevent unknown-category errors on valid user inputs
- XP thresholds tuned to require ~20 interactions to reach Legendary

## Ready for Phase 3
- `user_corrections.csv` is the data source for the RL agent
- Every correction logs `(inputs, predicted_mood, corrected_mood, timestamp)`
- Most common mistakes tracked live in UI — provides qualitative check on whether the RL agent is actually learning the patterns users care about