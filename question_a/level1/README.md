# Question A — Level 1

## Objective

Build baseline machine-learning models to predict health risk using the
UCI Heart Failure Clinical Records dataset.

## Dataset

The dataset contains 299 patient records and 13 columns.

The target variable is:

- `DEATH_EVENT`

The feature `time` was excluded because it represents follow-up duration
rather than a baseline patient characteristic available at the time of
initial screening.

The remaining 11 baseline features were used for prediction.

## Data Quality Check

Before model training, the dataset was checked for common data-quality
issues.

The checks found:

- 0 missing values
- 0 duplicate rows
- Binary features contained only 0 and 1
- The target variable contained only 0 and 1
- All model input features were numeric

Therefore, no data-cleaning transformations such as missing-value
imputation, duplicate removal, or categorical encoding were required.

## Experimental Setup

- Seed: 50
- Train/test split: 80/20
- Stratification: Yes
- Test samples: 60
- Logistic Regression: StandardScaler + Logistic Regression
- Random Forest: 200 trees
- Random state: 50

## Baseline Results

### Logistic Regression

| Metric | Result |
|---|---:|
| Accuracy | 71.67% |
| Precision | 57.14% |
| Recall | 42.11% |

### Random Forest

| Metric | Result |
|---|---:|
| Accuracy | 75.00% |
| Precision | 66.67% |
| Recall | 42.11% |

## Random Forest Confusion Matrix

```text
[[37, 4],
 [11, 8]]