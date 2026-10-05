# Personal Intelligence Note

## Candidate
USN: 1DA23AI050

## Seed
50

## Questions Selected
- Question A: Predict a health risk
- Question B: Turn a model into a usable app

---

## Decision Log

### Question A

#### Decision 1 — Feature Selection

**Chosen:** Exclude the `time` feature from the prediction inputs.

**Rejected:** Use all 12 non-target columns, including `time`.

**Reason:** The `time` feature represents follow-up duration rather than a
baseline patient characteristic available at the time of initial screening.
Therefore, the 11 baseline patient features were used for prediction.

#### Decision 2 — Model Selection

**Chosen:** Baseline Random Forest with 200 trees and random state 50.

**Rejected:** Tuned Random Forest with 100 trees, minimum leaf size 4,
and random state 50.

**Reason:** Both models achieved 75.00% accuracy. The tuned model improved
precision from 66.67% to 70.00%, but recall decreased from 42.11% to 36.84%.
The tuned model also had 12 false negatives compared with 11 for the
baseline model. Since this is a health-risk screening task, the baseline
model was selected because it maintained the same accuracy while achieving
higher recall.

### Question B

#### Decision 1
Decision will be recorded after implementation and testing.

#### Decision 2
Decision will be recorded after robustness testing.

---

## Level 3 Predictions

### Question A
Prediction will be committed before running the threshold experiment.

### Question B
Prediction will be committed before running the required robustness experiments.

---

## AI Usage Declaration

AI tools used:
- ChatGPT

Use of AI:
- Project planning
- Concept explanations
- Code assistance
- Debugging assistance
- Documentation review

AI weakness/error:
To be documented based on an actual issue encountered during development.

---

## Final Reflection

To be completed after both questions are finished.