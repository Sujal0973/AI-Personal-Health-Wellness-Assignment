import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score


# ============================================================
# QUESTION A - LEVEL 1
# Health Risk Prediction
# Seed: 50
# ============================================================

SEED = 50

DATA_PATH = "data/heart_failure_clinical_records_dataset.csv"


# ------------------------------------------------------------
# 1. Load dataset
# ------------------------------------------------------------

df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())


# ------------------------------------------------------------
# 2. Separate features and target
# ------------------------------------------------------------

TARGET = "DEATH_EVENT"

# 'time' represents follow-up duration rather than a
# baseline screening measurement, so it is excluded.
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

X = df[FEATURES]
y = df[TARGET]


# ------------------------------------------------------------
# 3. Train-test split
# ------------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=SEED,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ------------------------------------------------------------
# 4. Logistic Regression
# ------------------------------------------------------------

logistic_model = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(
        random_state=SEED,
        max_iter=1000
    ))
])

logistic_model.fit(X_train, y_train)

logistic_predictions = logistic_model.predict(X_test)


# ------------------------------------------------------------
# 5. Random Forest
# ------------------------------------------------------------

random_forest_model = RandomForestClassifier(
    n_estimators=200,
    random_state=SEED
)

random_forest_model.fit(X_train, y_train)

random_forest_predictions = random_forest_model.predict(X_test)


# ------------------------------------------------------------
# 6. Evaluation function
# ------------------------------------------------------------

def evaluate_model(name, y_true, y_pred):
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)

    print(f"\n{name}")
    print("-" * len(name))
    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")


# ------------------------------------------------------------
# 7. Evaluate both models
# ------------------------------------------------------------

evaluate_model(
    "Logistic Regression",
    y_test,
    logistic_predictions
)

evaluate_model(
    "Random Forest",
    y_test,
    random_forest_predictions
)