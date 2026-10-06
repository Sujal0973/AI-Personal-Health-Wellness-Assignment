import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


SEED = 50

DATA_PATH = "data/heart_failure_clinical_records_dataset.csv"
MODEL_PATH = "question_b/api/model/heart_failure_rf.joblib"

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
    "smoking",
]


# Load dataset
df = pd.read_csv(DATA_PATH)

X = df[FEATURES]
y = df[TARGET]

# Same split used throughout Question A
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=SEED,
    stratify=y,
)

# Final model selected in Question A Level 1
model = RandomForestClassifier(
    n_estimators=200,
    random_state=SEED,
)

model.fit(X_train, y_train)

# Save model and feature order together
model_package = {
    "model": model,
    "features": FEATURES,
    "seed": SEED,
}

os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

joblib.dump(model_package, MODEL_PATH)

print("Model trained and saved successfully.")
print(f"Model path: {MODEL_PATH}")
print(f"Features: {FEATURES}")
print(f"Seed: {SEED}")