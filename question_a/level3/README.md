# Question A — Level 3: Classification Threshold Analysis & Reasoning

## 1. Objective

Systematically investigate how varying the classification decision threshold affects **precision**, **recall**, **overall accuracy**, and the volume of patients flagged for clinical intervention. 

The task requires:
1. Committing a hypothesis prior to running the experiment regarding the impact of adjusting the decision threshold until recall reaches $\ge 0.90$.
2. Running an empirical sweep from $\tau = 0.10$ to $\tau = 0.50$ on the held-out test split ($N = 60$, Seed $50$).
3. Explaining the exact trade-offs with empirical data.
4. Defining an optimal threshold for a real-world clinical screening tool and articulating why accuracy alone is deceptive.

---

## 2. Pre-Experiment Prediction (Committed to Git)

As recorded in `question_a/level3/prediction.md` (Commit `a436363`):

> *"I predict that lowering the classification threshold until recall reaches approximately 0.90 will increase the number of patients classified as positive.*
> *Because more borderline cases will be classified as positive, I predict that precision will decrease compared with the 0.50 threshold.*
> *Therefore, I expect: Recall will increase, Precision will decrease, Predicted positive cases will increase, and the final threshold will be well below 0.50."*

---

## 3. Experimental Methodology & Sweep Results

The Random Forest model trained in Level 1 (200 trees, Seed 50) computes a continuous posterior probability $P(\text{DEATH\_EVENT} = 1 \mid x)$. In standard binary classification, a default threshold of $\tau = 0.50$ is applied.

In this experiment, thresholds from $\tau = 0.10$ to $\tau = 0.50$ (step size 0.01) were evaluated against the 60 test patients:

### Key Threshold Sweep Milestones
| Threshold ($\tau$) | Accuracy | Precision | Recall | Predicted Positives | Clinical Note |
|---|:---:|:---:|:---:|:---:|---|
| **0.10** | 46.67% | 37.25% | **100.00%** | 51 / 60 | Flags almost everyone; high false alarm rate |
| **0.16** | **58.33%** | **42.50%** | **89.47%** | **40 / 60** | **Closest threshold to target recall $\approx 0.90$** |
| **0.20** | 71.67% | 53.12% | 89.47% | 32 / 60 | Higher accuracy while preserving 89.47% recall |
| **0.30** | 75.00% | 57.69% | 78.95% | 26 / 60 | Balanced trade-off zone |
| **0.40** | 76.67% | 63.16% | 63.16% | 19 / 60 | Moderate sensitivity |
| **0.50 (Default)** | **71.67%** | **57.14%** | **42.11%** | **14 / 60** | **Misses 11 out of 19 fatal cases (57.9% failure)** |

---

## 4. Deep-Dive: Default Threshold (0.50) vs. Selected Threshold (0.16)

| Metric | Default ($\tau = 0.50$) | Selected Screening ($\tau = 0.16$) | Net Impact |
|---|:---:|:---:|:---:|
| **Recall (Sensitivity)** | 42.11% | **89.47%** | **+47.36% (Missed cases drop from 11 to 2)** |
| **Precision (PPV)** | **57.14%** | 42.50% | -14.64% (More false alarms) |
| **Accuracy** | **71.67%** | 58.33% | -13.34% (Appears worse overall) |
| **False Negatives (Missed Fatalities)** | **11** | **2** | **-9 fatal misses (Critical benefit)** |
| **False Positives (False Alarms)** | **6** | **23** | +17 follow-up investigations required |
| **Total Flagged Patients** | 14 / 60 | 40 / 60 | +26 flagged for specialist review |

---

## 5. Reasoning with the Results

### 5.1 Why Did Precision Decrease?
At $\tau = 0.50$, the classifier requires strong positive evidence ($P \ge 0.50$) before flagging a patient. Lowering the threshold to $\tau = 0.16$ lowers the evidentiary barrier, classifying anyone with even mild risk signals as high-risk. While this successfully captures 9 additional true positive patients, it simultaneously misclassifies 17 healthy patients as high-risk. Because $\text{Precision} = \frac{TP}{TP + FP}$, the surge in $FP$ drives precision down from 57.14% to 42.50%.

### 5.2 Why Did Accuracy Decrease?
Overall accuracy dropped from 71.67% to 58.33%. This occurs because the test set contains 41 negative patients (survived). Lowering the threshold misclassifies 23 of these negative patients as positive. The loss of accuracy on the majority negative class outweighs the gain in true positive detection.

### 5.3 Why Accuracy Alone Is Dangerously Misleading in Healthcare
Accuracy treats all misclassifications as having equal cost:
$$\text{Cost}(\text{False Positive}) = \text{Cost}(\text{False Negative})$$

In heart failure clinical management, this assumption is invalid:
1. **Cost of a False Negative:** A critically ill patient is sent home without treatment, leading to preventable decompensation or death.
2. **Cost of a False Positive:** A stable patient undergoes secondary non-invasive diagnostic follow-up (e.g., echocardiogram or blood panel).

At the "high accuracy" default threshold ($\tau = 0.50$, 71.67% accuracy), **the model fails to detect 11 out of 19 fatal events (a 57.9% failure rate)**. A clinical team relying on accuracy would be deploying an ineffective tool.

---

## 6. Real-World Clinical Recommendation

For a frontline screening triage tool, the recommended operational threshold is **$\tau = 0.16$** (or $\tau = 0.20$ if hospital follow-up bandwidth is constrained):
- **Clinical Protocol:** The AI serves as an initial safety net. Patients flagged at $\tau = 0.16$ are fast-tracked for physician examination and secondary laboratory tests.
- **Outcome:** Catches ~90% of mortality risks early, while diagnostic follow-up filters out the false alarms.

---

## 7. Reproduction Command

Run from the project root:
```bash
python question_a/level3/threshold_experiment.py
```