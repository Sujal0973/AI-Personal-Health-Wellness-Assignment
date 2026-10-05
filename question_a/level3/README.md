# Question A — Level 3: Classification Threshold Analysis

## Objective

Investigate how lowering the classification threshold affects precision,
recall, accuracy, and the number of patients classified as high-risk.

The experiment tests thresholds from 0.10 to 0.50 using the final
Random Forest model selected in Level 1.

The goal is to determine the threshold closest to a recall of 0.90 and
evaluate whether the observed result matches the prediction committed
before running the experiment.

---

## Seed and Experimental Setup

- Seed: 50
- Dataset: UCI Heart Failure Clinical Records Dataset
- Target: `DEATH_EVENT`
- Model: Random Forest
- Number of trees: 200
- Random state: 50
- Train/test split: 80/20
- Stratification: Yes
- Test samples: 60
- Default classification threshold: 0.50

The same features and train/test split used in Levels 1 and 2 were used
for this experiment.

The `time` feature was excluded because it represents follow-up duration
rather than a baseline screening input.

---

## Pre-Experiment Prediction

Before running the experiment, the following prediction was committed
to GitHub:

- Lowering the threshold would increase recall.
- Precision would decrease.
- The number of predicted positive cases would increase.
- The threshold required to reach approximately 0.90 recall would be
  below 0.50.

This prediction was committed before the experiment was run.

---

## Experiment

The Random Forest model produces a probability for the positive class.
Instead of using the default threshold of 0.50, thresholds from 0.10 to
0.50 were tested.

For each threshold, the following were calculated:

- Accuracy
- Precision
- Recall
- Number of predicted positive cases

The threshold closest to a target recall of 0.90 was then selected.

---

## Result

The threshold closest to a recall of 0.90 was:

**Threshold = 0.16**

Results:

- Accuracy: 58.33%
- Precision: 42.50%
- Recall: 89.47%
- Predicted positive cases: 40

---

## Default Threshold vs Selected Threshold

| Metric | Threshold 0.50 | Threshold 0.16 |
|---|---:|---:|
| Accuracy | 71.67% | 58.33% |
| Precision | 57.14% | 42.50% |
| Recall | 42.11% | 89.47% |
| Predicted positive cases | 14 | 40 |

---

## Prediction vs Actual Result

The experimental result supported the main prediction.

### Predicted

- Recall would increase.
- Precision would decrease.
- More cases would be classified as positive.
- The required threshold would be below 0.50.

### Observed

- Recall increased from 42.11% to 89.47%.
- Precision decreased from 57.14% to 42.50%.
- Predicted positive cases increased from 14 to 40.
- The selected threshold was 0.16.

Therefore, the direction of the pre-experiment prediction was correct.

---

## Why Precision Decreased

At a threshold of 0.50, the model requires a relatively high predicted
probability before classifying a patient as positive.

Lowering the threshold to 0.16 makes the classifier more sensitive to
borderline cases. This increases the number of positive predictions.

While this allows the model to identify more actual positive cases,
it also creates more false-positive predictions. As a result, precision
decreases.

---

## Why Accuracy Decreased

Accuracy decreased from 71.67% to 58.33%.

This happened because lowering the threshold substantially increased
the number of positive predictions. Although this increased the number
of correctly detected positive cases, it also caused additional negative
cases to be classified as positive.

The increase in false positives was large enough to reduce overall
accuracy.

---

## Why Accuracy Alone Is Not Sufficient

For a health-risk screening task, false negatives can be particularly
important because they represent positive cases that the model failed
to identify.

At the default threshold:

- Recall was only 42.11%.
- 11 of the 19 actual positive cases were missed.

At the selected threshold:

- Recall increased to 89.47%.
- Only 2 of the 19 actual positive cases were missed.

Therefore, although accuracy decreased, the selected threshold detected
substantially more of the actual positive cases.

This demonstrates why accuracy alone is not sufficient when evaluating
a health-risk screening model.

---

## Screening Threshold Decision

For this assignment, a threshold of **0.16** is selected for a
recall-oriented screening scenario because it provides approximately
0.90 recall on the held-out test set.

The choice prioritizes reducing false negatives over maximizing overall
accuracy.

This should be interpreted only as an assignment-level experimental
threshold. The model and threshold are not clinically validated and
should not be used as a real medical decision-making system.

---

## Limitations

- The dataset contains only 299 records.
- The experiment uses one fixed train/test split with seed 50 as required
  by the assignment.
- The selected threshold is based on this test set.
- The model has not undergone clinical validation.
- A real healthcare screening system would require larger and
  representative datasets, external validation, calibration analysis,
  and clinical evaluation.

---

## How to Run

From the project root:

```bash
python question_a\level3\threshold_experiment.py