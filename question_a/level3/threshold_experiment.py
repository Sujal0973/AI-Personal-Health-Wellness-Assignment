import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score


# =========================
# Configuration
# =========================

SEED = 50

DATA_PATH = "data/heart_failure_clinical_records_dataset.csv"
TARGET = "DEATH_EVENT"

FEATURES = [
    "age",
    "anaemia",
    "creatinine_phosphokinase",
    "diabetes",
    "ejection_fraction",
    "high_blood_pressure",
    "platelets",
    "serum_creatinine",
    "serum_sodium",
    "sex",
    "smoking"
]


# =========================
# Load data
# =========================

df = pd.read_csv(DATA_PATH)

X = df[FEATURES]
y = df[TARGET]


# =========================
# Same train/test split
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=SEED,
    stratify=y
)


# =========================
# Train final Level 1 model
# =========================

model = RandomForestClassifier(
    n_estimators=200,
    random_state=SEED
)

model.fit(X_train, y_train)


# =========================
# Get probabilities
# =========================

probabilities = model.predict_proba(X_test)[:, 1]


# =========================
# Threshold experiment
# =========================

thresholds = np.arange(0.10, 0.51, 0.01)

results = []

for threshold in thresholds:

    predictions = (probabilities >= threshold).astype(int)

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )
    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )

    results.append({
        "threshold": threshold,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "predicted_positive": predictions.sum()
    })


results_df = pd.DataFrame(results)


# =========================
# Display threshold results
# =========================

print("\nThreshold Experiment")
print("=" * 80)

print(
    results_df.to_string(
        index=False,
        formatters={
            "threshold": "{:.2f}".format,
            "accuracy": "{:.4f}".format,
            "precision": "{:.4f}".format,
            "recall": "{:.4f}".format
        }
    )
)


# =========================
# Find threshold closest to recall = 0.90
# =========================

target_recall = 0.90

results_df["recall_difference"] = abs(
    results_df["recall"] - target_recall
)

best_row = results_df.loc[
    results_df["recall_difference"].idxmin()
]


print("\n" + "=" * 80)
print("THRESHOLD CLOSEST TO RECALL = 0.90")
print("=" * 80)

print(f"Threshold          : {best_row['threshold']:.2f}")
print(f"Accuracy           : {best_row['accuracy']:.4f}")
print(f"Precision          : {best_row['precision']:.4f}")
print(f"Recall             : {best_row['recall']:.4f}")
print(
    f"Predicted positive : "
    f"{int(best_row['predicted_positive'])}"
)


# =========================
# Default threshold comparison
# =========================

default_row = results_df[
    np.isclose(results_df["threshold"], 0.50)
].iloc[0]


print("\n" + "=" * 80)
print("DEFAULT 0.50 vs SELECTED THRESHOLD")
print("=" * 80)

print("\nDefault threshold = 0.50")
print(f"Accuracy : {default_row['accuracy']:.4f}")
print(f"Precision: {default_row['precision']:.4f}")
print(f"Recall   : {default_row['recall']:.4f}")

print(
    f"\nSelected threshold = "
    f"{best_row['threshold']:.2f}"
)

print(f"Accuracy : {best_row['accuracy']:.4f}")
print(f"Precision: {best_row['precision']:.4f}")
print(f"Recall   : {best_row['recall']:.4f}")