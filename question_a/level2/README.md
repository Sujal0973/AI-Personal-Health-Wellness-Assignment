# Question A — Level 2

## Objective

Implement Logistic Regression from scratch using NumPy and compare the
results with the sklearn Logistic Regression model from Level 1.

## Data Preparation

The same dataset, features, seed, and train/test split from Level 1 were
used.

- Dataset: UCI Heart Failure Clinical Records
- Seed: 50
- Train/test split: 80/20
- Stratification: Yes
- Training samples: 239
- Testing samples: 60
- Target: `DEATH_EVENT`
- Features: 11 baseline features
- `time` was excluded because it represents follow-up duration.

The training data was used to calculate the mean and standard deviation
for feature standardization. The same training statistics were then
applied to the test data to avoid data leakage.

## Data Quality Check

The dataset was checked for common data-quality issues.

Results:

- Missing values: 0
- Duplicate rows: 0
- Binary features contained only 0 and 1
- Target values were 0 and 1
- Model input features were numeric

Therefore, no data-cleaning transformations such as missing-value
imputation or duplicate removal were required.

## Implementation

The Logistic Regression model was implemented using NumPy.

The implementation includes:

1. Sigmoid function
2. Binary cross-entropy loss
3. Gradient calculation
4. Gradient descent
5. Weight and bias updates
6. Probability prediction
7. Threshold-based classification

Training configuration:

```text
Learning rate: 0.01
Epochs: 5000
Classification threshold: 0.50