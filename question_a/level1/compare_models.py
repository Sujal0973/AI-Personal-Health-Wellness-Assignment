import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    confusion_matrix
)

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
# Load dataset
# =========================

df = pd.read_csv(DATA_PATH)

X = df[FEATURES]
y = df[TARGET]

# Same split used throughout Question A
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=SEED,
    stratify=y
)

print("Dataset shape:", df.shape)
print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# =========================
# Baseline Random Forest
# =========================

baseline_rf = RandomForestClassifier(
    n_estimators=200,
    random_state=SEED
)

baseline_rf.fit(X_train, y_train)

baseline_pred = baseline_rf.predict(X_test)


# =========================
# Tuned Random Forest
# =========================

tuned_rf = RandomForestClassifier(
    n_estimators=100,
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=4,
    class_weight=None,
    random_state=SEED
)

tuned_rf.fit(X_train, y_train)

tuned_pred = tuned_rf.predict(X_test)


# =========================
# Evaluation function
# =========================

def evaluate_model(name, y_true, y_pred):

    cm = confusion_matrix(y_true, y_pred)

    print("\n" + "=" * 50)
    print(name)
    print("=" * 50)

    print("Confusion Matrix:")
    print(cm)

    print("\nMetrics:")
    print(f"Accuracy : {accuracy_score(y_true, y_pred):.4f}")
    print(f"Precision: {precision_score(y_true, y_pred, zero_division=0):.4f}")
    print(f"Recall   : {recall_score(y_true, y_pred, zero_division=0):.4f}")

    print("\nPredicted positive cases:", y_pred.sum())


# =========================
# Compare
# =========================

evaluate_model(
    "Baseline Random Forest",
    y_test,
    baseline_pred
)

evaluate_model(
    "Tuned Random Forest",
    y_test,
    tuned_pred
)