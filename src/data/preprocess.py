import pandas as pd
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder

CATEGORICAL_COLS = ["activity", "tail_position", "ear_direction"]
NUMERIC_COLS = ["time_of_day", "food_eaten"]
TARGET = "mood"

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
    cat_encoder = OrdinalEncoder()
    df[CATEGORICAL_COLS] = cat_encoder.fit_transform(df[CATEGORICAL_COLS])

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(df[TARGET])
    X = df[NUMERIC_COLS + CATEGORICAL_COLS].values

    return X, y, cat_encoder, label_encoder

def get_feature_names():
    return NUMERIC_COLS + CATEGORICAL_COLS
