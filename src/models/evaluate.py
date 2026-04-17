import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import (
    classification_report,
    ConfusionMatrixDisplay,
)

def evaluate_model(model, X_test, y_test, label_names, model_name="Model"):
    y_pred = model.predict(X_test)
    print(f"\n{'='*40}\n{model_name}\n{'='*40}")
    print(classification_report(y_test, y_pred, target_names=label_names))

    fig, ax = plt.subplots(figsize=(7, 5))
    ConfusionMatrixDisplay.from_predictions(
        y_test, y_pred,
        display_labels=label_names,
        ax=ax,
        cmap="Blues",
        colorbar=False,
    )
    ax.set_title(f"{model_name} — Confusion Matrix")
    plt.tight_layout()
    return fig, y_pred

def plot_feature_importance(model, feature_names):
    importances = model.feature_importances_
    idx = np.argsort(importances)
    fig, ax = plt.subplots(figsize=(6, 4))
    colors = ["steelblue" if i == idx[-1] else "lightsteelblue" for i in range(len(idx))]
    ax.barh(np.array(feature_names)[idx], importances[idx],
            color=[colors[i] for i in range(len(idx))])
    ax.set_title("Random Forest — Feature Importance")
    ax.set_xlabel("Mean Decrease in Impurity")
    plt.tight_layout()
    return fig