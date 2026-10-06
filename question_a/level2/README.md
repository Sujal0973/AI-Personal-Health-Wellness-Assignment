# Question A — Level 2: Logistic Regression from Scratch (NumPy)

## 1. Objective

Implement binary Logistic Regression and confusion matrix calculation completely from scratch using **NumPy**—without relying on scikit-learn for optimization or metrics. Validate that the scratch model's convergence, decision boundary, accuracy, and top-3 feature weights match scikit-learn's standard `lbfgs` implementation under the identical random seed ($S = 50$).

---

## 2. Mathematical Formulation & Architecture

The scratch implementation in `logistic_regression_numpy.py` consists of four analytical components:

### 2.1 The Sigmoid Activation
Maps any real-valued linear score $z = Xw + b$ to a probability $p \in (0, 1)$:
$$\sigma(z) = \frac{1}{1 + e^{-z}}$$

### 2.2 Binary Cross-Entropy Loss (with Epsilon Stability)
To prevent numerical overflow or $\ln(0)$ errors, predicted probabilities are clipped to $[\epsilon, 1 - \epsilon]$ where $\epsilon = 10^{-9}$:
$$L(w, b) = -\frac{1}{m} \sum_{i=1}^{m} \left[ y^{(i)} \ln(\hat{y}^{(i)}) + (1 - y^{(i)}) \ln(1 - \hat{y}^{(i)}) \right]$$

### 2.3 Vectorized Gradient Descent Updates
Analytical gradients derived with respect to weights $w$ and bias $b$:
$$\frac{\partial L}{\partial w} = \frac{1}{m} X^T (\hat{y} - y)$$
$$\frac{\partial L}{\partial b} = \frac{1}{m} \sum_{i=1}^{m} (\hat{y}^{(i)} - y^{(i)})$$

Parameters are iteratively updated across $E = 5000$ epochs at learning rate $\alpha = 0.01$:
$$w \leftarrow w - \alpha \frac{\partial L}{\partial w}$$
$$b \leftarrow b - \alpha \frac{\partial L}{\partial b}$$

---

## 3. Data Preprocessing & Leakage Control

- **Dataset:** UCI Heart Failure Clinical Records (299 records, 11 baseline features; `time` excluded).
- **Split:** 80% train (239 records), 20% test (60 records), stratified by `DEATH_EVENT` with seed `50`.
- **Standardization:**
  $$\mu = \frac{1}{m}\sum X_{\text{train}}, \quad \sigma = \sqrt{\frac{1}{m}\sum (X_{\text{train}} - \mu)^2}$$
  The mean $\mu$ and standard deviation $\sigma$ computed on the training set were applied to scale both $X_{\text{train}}$ and $X_{\text{test}}$, strictly preventing data leakage.

---

## 4. Hand-Crafted Confusion Matrix & Metrics

The confusion matrix was constructed purely using boolean array indexing in NumPy:
```python
true_positive = np.sum((y_test == 1) & (y_pred == 1))
true_negative = np.sum((y_test == 0) & (y_pred == 0))
false_positive = np.sum((y_test == 0) & (y_pred == 1))
false_negative = np.sum((y_test == 1) & (y_pred == 0))

confusion_matrix = np.array([
    [true_negative, false_positive],
    [false_negative, true_positive]
])
```

Derived from first principles:
- **Accuracy:** $\frac{TP + TN}{TP + TN + FP + FN} = \frac{8 + 35}{60} = \mathbf{71.67\%}$
- **Precision:** $\frac{TP}{TP + FP} = \frac{8}{8 + 6} = \mathbf{57.14\%}$
- **Recall:** $\frac{TP}{TP + FN} = \frac{8}{8 + 11} = \mathbf{42.11\%}$

---

## 5. Scratch vs. Scikit-Learn Side-by-Side Comparison

Both models were evaluated on the identical test split ($N = 60$, Seed $50$):

| Evaluation Metric | NumPy Scratch Model | Scikit-Learn (`lbfgs`) | Discrepancy |
|---|:---:|:---:|:---:|
| **Accuracy** | **71.67%** | **71.67%** | **0.00%** |
| **Precision** | **57.14%** | **57.14%** | **0.00%** |
| **Recall** | **42.11%** | **42.11%** | **0.00%** |
| **True Negatives (TN)** | 35 | 35 | 0 |
| **False Positives (FP)** | 6 | 6 | 0 |
| **False Negatives (FN)** | 11 | 11 | 0 |
| **True Positives (TP)** | 8 | 8 | 0 |
| **Final Loss** | 0.4916 | 0.4914 | 0.0002 |

---

## 6. Comparison of Top 3 Feature Weights

Sorting all 11 standardized weights by their absolute magnitude $|\beta|$ reveals that both models converged on the exact same hierarchy and directional signs:

| Feature Name | Scratch Weight ($w_{\text{numpy}}$) | Sklearn Weight ($w_{\text{sklearn}}$) | Relative Difference | Clinical Direction |
|---|:---:|:---:|:---:|---|
| **`ejection_fraction`** | **-0.834882** | **-0.809977** | 3.0% | **Strong Protective Factor** (Higher ejection fraction reduces mortality risk) |
| **`serum_creatinine`** | **+0.716070** | **+0.693352** | 3.2% | **Strong Risk Factor** (Elevated creatinine indicates kidney impairment & heart failure severity) |
| **`age`** | **+0.665528** | **+0.648512** | 2.6% | **Strong Risk Factor** (Older patients face higher mortality risk) |

### Clinical Interpretation:
- The scratch gradient descent optimizer accurately learned the cardinal pathophysiological indicators of heart failure:
  1. A low **ejection fraction** indicates systolic dysfunction (the heart muscle cannot pump blood effectively).
  2. Elevated **serum creatinine** signals cardiorenal syndrome, where impaired cardiac output causes kidney damage.
  3. Increasing **age** exacerbates cardiovascular vulnerability.

---

## 7. Reproduction Commands

```bash
# 1. Run the NumPy scratch model and confusion matrix
python question_a/level2/logistic_regression_numpy.py

# 2. Run the direct verification and comparison script against scikit-learn
python question_a/level2/compare_sklearn.py
```