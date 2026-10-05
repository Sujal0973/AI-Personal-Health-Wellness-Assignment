import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
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
# Load data
# =========================

df = pd.read_csv(DATA_PATH)

X = df[FEATURES]
y = df[TARGET]

# Same split used in Level 1 and Level 2
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=SEED,
    stratify=y
)

# =========================
# Standardization
# =========================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# =========================
# Train sklearn model
# =========================

model = LogisticRegression(
    random_state=SEED,
    max_iter=1000
)

model.fit(X_train_scaled, y_train)

# =========================
# Predictions
# =========================

y_pred = model.predict(X_test_scaled)

# =========================
# Metrics
# =========================

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)

print("Sklearn Logistic Regression")
print("=" * 40)

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")

# =========================
# Confusion matrix
# =========================

cm = confusion_matrix(y_test, y_pred)

print("\nConfusion Matrix")
print("=" * 40)
print(cm)

# =========================
# Feature weights
# =========================

weights = model.coef_[0]

feature_weights = list(zip(FEATURES, weights))

feature_weights.sort(
    key=lambda item: abs(item[1]),
    reverse=True
)

print("\nTop 3 Features by Absolute Weight")
print("=" * 40)

for feature, weight in feature_weights[:3]:
    print(f"{feature}: {weight:.6f}")