import numpy as np

def predict_mood(model, cat_encoder, label_encoder, input_dict):
    """
    input_dict = {
        "time_of_day": 14.5,
        "activity": "sleeping",
        "tail_position": "down",
        "ear_direction": "backward",
        "food_eaten": 0.7
    }
    Returns predicted mood string.
    """
    cat_cols = ["activity", "tail_position", "ear_direction"]
    num_cols = ["time_of_day", "food_eaten"]

    cat_values = np.array([[input_dict[c] for c in cat_cols]])
    cat_encoded = cat_encoder.transform(cat_values)

    num_values = np.array([[input_dict[c] for c in num_cols]])
    X = np.hstack([num_values, cat_encoded])

    pred = model.predict(X)
    return label_encoder.inverse_transform(pred)[0]