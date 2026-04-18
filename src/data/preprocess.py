import pandas as pd
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
from src.data.generate_synthetic import ACTIVITIES, TAIL_POSITIONS, EAR_DIRECTIONS, MOODS

CATEGORICAL_COLS = ["activity", "tail_position", "ear_direction"]
NUMERIC_COLS = ["time_of_day", "food_eaten"]
TARGET = "mood"

# Explicit category lists ensure the encoder accepts all valid inputs
# regardless of which values happened to appear in the training split
KNOWN_CATEGORIES = [
    sorted(ACTIVITIES),
    sorted(TAIL_POSITIONS),
    sorted(EAR_DIRECTIONS),
]

def load_and_clean(path="data/raw/cat_behavior_synthetic.csv"):
    df = pd.read_csv(path)
    df = df.dropna()
    df = df.drop_duplicates()
    df["food_eaten"] = df["food_eaten"].clip(0.0, 1.0)
    df["time_of_day"] = df["time_of_day"].clip(0.0, 23.9)
    return df

def encode_features(df):
    """Returns X (numpy), y (numpy), and fitted encoders for inverse transform."""
    df = df.copy()
    cat_encoder = OrdinalEncoder(categories=KNOWN_CATEGORIES)
    df[CATEGORICAL_COLS] = cat_encoder.fit_transform(df[CATEGORICAL_COLS])

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(df[TARGET])
    X = df[NUMERIC_COLS + CATEGORICAL_COLS].values

    return X, y, cat_encoder, label_encoder

def get_feature_names():
    return NUMERIC_COLS + CATEGORICAL_COLS
