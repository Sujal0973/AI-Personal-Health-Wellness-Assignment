# Question A — Level 1: Health Risk Prediction (Baseline Models)

## 1. Objective

Build, evaluate, and compare baseline machine-learning classification models to predict mortality risk in heart failure patients using the **UCI Heart Failure Clinical Records dataset** under a strictly fixed random seed ($S = 50$).

---

## 2. Dataset & Clinical Feature Selection

The dataset comprises **299 patient records** with 12 clinical features and one binary target variable (`DEATH_EVENT`).

### Target Variable
- `DEATH_EVENT`: Patient deceased during observation period (`1 = Deceased`, `0 = Survived`).
- **Class Distribution:**
  - Negative class (`0`): 203 patients (67.89%)
  - Positive class (`1`): 96 patients (32.11%)
  - *Observation:* The presence of a ~2:1 class imbalance demonstrates why raw accuracy alone is insufficient for evaluating a medical screening model.

### Clinical Justification for Feature Selection (`time` exclusion)
- The raw dataset includes a `time` column denoting the follow-up duration (in days).
- In clinical screening, follow-up duration is **not available** when evaluating a prospective patient. Furthermore, patients who suffer acute mortality have systematically shorter follow-up times, introducing profound target leakage.
- **Decision:** The `time` feature was excluded. All models are trained purely on the **11 baseline physiological and demographic features**:
  1. `age`: Patient age in years
  2. `anaemia`: Decrease in red blood cells or hemoglobin (0/1)
  3. `creatinine_phosphokinase`: Level of CPK enzyme in blood (mcg/L)
  4. `diabetes`: Patient has diabetes (0/1)
  5. `ejection_fraction`: Percentage of blood pumped out of heart with each contraction (%)
  6. `high_blood_pressure`: Patient has hypertension (0/1)
  7. `platelets`: Platelet count in blood (kiloplatelets/mL)
  8. `serum_creatinine`: Level of serum creatinine in blood (mg/dL)
  9. `serum_sodium`: Level of serum sodium in blood (mEq/L)
  10. `sex`: Biological sex (0 = female, 1 = male)
  11. `smoking`: Smoking history (0/1)

---

## 3. Data Integrity & Quality Check

Prior to modeling, automated data sanity checks verified:
- **Missing values:** 0 (no imputation necessary)
- **Duplicate rows:** 0
- **Data types:** All 11 features are strictly numeric (continuous floats or binary integers)
- **Binary constraints:** `anaemia`, `diabetes`, `high_blood_pressure`, `sex`, `smoking`, and `DEATH_EVENT` contain only `{0, 1}`.

---

## 4. Experimental Setup

- **Random Seed ($S$):** `50` (derived from USN `1DA23AI050`)
- **Train/Test Split:** 80% train (239 patients), 20% test (60 patients)
- **Stratification:** Enabled (`stratify=y`) to maintain the 32.11% death-event prevalence across both splits.
- **Test Set Breakdown:** 41 negative cases (`0`), 19 positive cases (`1`).

### Models Trained:
1. **Logistic Regression Pipeline:**
   - Preprocessing: `StandardScaler` (fit on train split only, transformed onto test split to prevent leakage).
   - Estimator: `LogisticRegression(random_state=50, max_iter=1000)`
2. **Random Forest Classifier:**
   - Estimator: `RandomForestClassifier(n_estimators=200, random_state=50)`

---

## 5. Baseline Evaluation Results

Evaluated on the held-out test split of 60 patients:

| Metric | Logistic Regression | Random Forest | Advantage |
|---|:---:|:---:|:---:|
| **Accuracy** | 71.67% | **75.00%** | Random Forest (+3.33%) |
| **Precision** | 57.14% | **66.67%** | Random Forest (+9.53%) |
| **Recall** | 42.11% | **42.11%** | Tie |
| **F1-Score** | 48.48% | **51.61%** | Random Forest (+3.13%) |

---

## 6. Confusion Matrix Analysis

### Logistic Regression
```text
                Predicted Negative (0)    Predicted Positive (1)
Actual Survived (0)         35 (TN)                   6 (FP)
Actual Deceased (1)         11 (FN)                   8 (TP)
```

### Random Forest
```text
                Predicted Negative (0)    Predicted Positive (1)
Actual Survived (0)         37 (TN)                   4 (FP)
Actual Deceased (1)         11 (FN)                   8 (TP)
```

### Key Insights:
1. **False Positives Reduction:** Random Forest reduced false positives from 6 to 4, increasing precision from 57.14% to 66.67%.
2. **The Clinical False Negative Bottleneck:** Both models missed 11 out of 19 high-risk patients at the default 0.50 threshold (Recall = 42.11%). In health screening, a 57.89% false negative rate is unacceptable, which motivates the threshold reasoning explored in **Level 3**.
3. **Selected Production Model:** Random Forest achieved higher accuracy and precision with identical recall, making it the superior baseline model to export for **Question B**.

---

## 7. Reproduction Command

Run from the project root:
```bash
python question_a/level1/train_models.py
```