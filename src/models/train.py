from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
import joblib

def train_models(X, y, test_size=0.2, seed=42):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=seed, stratify=y
    )

    rf = RandomForestClassifier(n_estimators=100, random_state=seed)
    rf.fit(X_train, y_train)

    lr = LogisticRegression(max_iter=1000, random_state=seed)
    lr.fit(X_train, y_train)

    return {
        "random_forest": rf,
        "logistic_regression": lr,
        "splits": (X_train, X_test, y_train, y_test),
    }

def tune_random_forest(X_train, y_train, seed=42):
    param_grid = {
        "n_estimators": [50, 100, 200],
        "max_depth":    [None, 10, 20],
        "min_samples_split": [2, 5],
    }
    grid = GridSearchCV(
        RandomForestClassifier(random_state=seed),
        param_grid,
        cv=5,
        scoring="accuracy",
        n_jobs=-1,
    )
    grid.fit(X_train, y_train)
    print(f"Best RF params: {grid.best_params_}")
    print(f"Best CV score:  {grid.best_score_:.3f}")
    return grid.best_estimator_

def save_model(model, path):
    joblib.dump(model, path)
    print(f"Saved → {path}")

def load_model(path):
    return joblib.load(path)