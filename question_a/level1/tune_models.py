import pandas as pd

from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score


# ============================================================
# QUESTION A - LEVEL 1
# MODEL TUNING EXPERIMENT
# Seed: 50
# ============================================================

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


# ------------------------------------------------------------
# 1. Load dataset
# ------------------------------------------------------------

df = pd.read_csv(DATA_PATH)

X = df[FEATURES]
y = df[TARGET]


# ------------------------------------------------------------
# 2. Same train/test split as our baseline
# ------------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=SEED,
    stratify=y
)


# ------------------------------------------------------------
# 3. Cross-validation setup
# ------------------------------------------------------------

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=SEED
)


# ============================================================
# LOGISTIC REGRESSION
# ============================================================

logistic_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(
        random_state=SEED,
        max_iter=2000
    ))
])


logistic_parameters = {
    "model__C": [0.01, 0.1, 1, 10, 100],
    "model__class_weight": [None, "balanced"]
}


logistic_search = GridSearchCV(
    estimator=logistic_pipeline,
    param_grid=logistic_parameters,
    scoring="accuracy",
    cv=cv,
    n_jobs=-1
)

logistic_search.fit(X_train, y_train)


best_logistic = logistic_search.best_estimator_

logistic_predictions = best_logistic.predict(X_test)


# ============================================================
# RANDOM FOREST
# ============================================================

random_forest = RandomForestClassifier(
    random_state=SEED
)


random_forest_parameters = {
    "n_estimators": [100, 200, 500],
    "max_depth": [None, 3, 5, 8],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 2, 4],
    "class_weight": [None, "balanced"]
}


random_forest_search = GridSearchCV(
    estimator=random_forest,
    param_grid=random_forest_parameters,
    scoring="accuracy",
    cv=cv,
    n_jobs=-1
)

random_forest_search.fit(X_train, y_train)


best_random_forest = random_forest_search.best_estimator_

random_forest_predictions = best_random_forest.predict(X_test)


# ============================================================
# EVALUATION
# ============================================================

def evaluate_model(name, y_true, y_pred):

    accuracy = accuracy_score(y_true, y_pred)

    precision = precision_score(
        y_true,
        y_pred,
        zero_division=0
    )

    recall = recall_score(
        y_true,
        y_pred,
        zero_division=0
    )

    print(f"\n{name}")
    print("-" * len(name))
    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")


# ============================================================
# RESULTS
# ============================================================

print("\n========================================")
print("LOGISTIC REGRESSION")
print("========================================")

print("\nBest parameters:")
print(logistic_search.best_params_)

print(f"\nBest CV accuracy: {logistic_search.best_score_:.4f}")

evaluate_model(
    "Logistic Regression - Tuned",
    y_test,
    logistic_predictions
)


print("\n========================================")
print("RANDOM FOREST")
print("========================================")

print("\nBest parameters:")
print(random_forest_search.best_params_)

print(f"\nBest CV accuracy: {random_forest_search.best_score_:.4f}")

evaluate_model(
    "Random Forest - Tuned",
    y_test,
    random_forest_predictions
)