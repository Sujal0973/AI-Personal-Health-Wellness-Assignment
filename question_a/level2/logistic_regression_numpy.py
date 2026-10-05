import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
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
# Sigmoid function
# =========================

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# =========================
# Binary cross-entropy loss
# =========================

def compute_loss(y, probabilities):
    epsilon = 1e-9

    probabilities = np.clip(
        probabilities,
        epsilon,
        1 - epsilon
    )

    loss = -np.mean(
        y * np.log(probabilities)
        + (1 - y) * np.log(1 - probabilities)
    )

    return loss

# =========================
# Logistic Regression from scratch
# =========================

class LogisticRegressionScratch:

    def __init__(self, learning_rate=0.01, epochs=5000):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weights = None
        self.bias = 0.0
        self.loss_history = []

    def fit(self, X, y):

        # Initialize weights and bias
        self.weights = np.zeros(X.shape[1])
        self.bias = 0.0

        # Gradient descent
        for epoch in range(self.epochs):

            # Linear combination
            z = np.dot(X, self.weights) + self.bias

            # Convert scores to probabilities
            probabilities = sigmoid(z)

            # Calculate loss
            loss = compute_loss(y, probabilities)
            self.loss_history.append(loss)

            # Calculate prediction error
            error = probabilities - y

            # Calculate gradients
            weight_gradient = np.dot(X.T, error) / len(y)
            bias_gradient = np.mean(error)

            # Update parameters
            self.weights -= self.learning_rate * weight_gradient
            self.bias -= self.learning_rate * bias_gradient

    def predict_proba(self, X):

        z = np.dot(X, self.weights) + self.bias

        return sigmoid(z)

    def predict(self, X, threshold=0.5):

        probabilities = self.predict_proba(X)

        return (probabilities >= threshold).astype(int)

# =========================
# Load and prepare data
# =========================

df = pd.read_csv(DATA_PATH)

X = df[FEATURES].values
y = df[TARGET].values

# Same train/test split used in Level 1
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
# Standardize features
# =========================

X_mean = np.mean(X_train, axis=0)
X_std = np.std(X_train, axis=0)

# Prevent division by zero
X_std[X_std == 0] = 1

X_train = (X_train - X_mean) / X_std
X_test = (X_test - X_mean) / X_std

# =========================
# Train scratch model
# =========================

model = LogisticRegressionScratch(
    learning_rate=0.01,
    epochs=5000
)

model.fit(X_train, y_train)

print("\nTraining complete.")
print("Final loss:", model.loss_history[-1])

# =========================
# Predictions
# =========================

y_pred = model.predict(X_test)

print("\nPredictions generated.")

# =========================
# Evaluation
# =========================

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)

print("\nScratch Logistic Regression")
print("=" * 40)
print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")

# =========================
# Own confusion matrix
# =========================

true_positive = np.sum((y_test == 1) & (y_pred == 1))
true_negative = np.sum((y_test == 0) & (y_pred == 0))
false_positive = np.sum((y_test == 0) & (y_pred == 1))
false_negative = np.sum((y_test == 1) & (y_pred == 0))

confusion_matrix_own = np.array([
    [true_negative, false_positive],
    [false_negative, true_positive]
])

print("\nOwn Confusion Matrix")
print("=" * 40)
print(confusion_matrix_own)

print("\nConfusion Matrix Components")
print(f"True Negatives : {true_negative}")
print(f"False Positives: {false_positive}")
print(f"False Negatives: {false_negative}")
print(f"True Positives : {true_positive}")

# =========================
# Top 3 feature weights
# =========================

feature_weights = list(zip(FEATURES, model.weights))

feature_weights.sort(
    key=lambda item: abs(item[1]),
    reverse=True
)

print("\nTop 3 Features by Absolute Weight")
print("=" * 40)

for feature, weight in feature_weights[:3]:
    print(f"{feature}: {weight:.6f}")