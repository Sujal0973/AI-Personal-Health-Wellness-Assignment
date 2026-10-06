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

#### Decision 3 — Scratch Logistic Regression Implementation

**Chosen:** Implement Logistic Regression from scratch using NumPy,
including sigmoid, binary cross-entropy loss, gradient descent,
standardization, prediction, and an own confusion matrix.

**Rejected:** Use only the sklearn Logistic Regression implementation
for Level 2 without implementing the optimization process manually.

**Reason:** The assignment requires a from-scratch NumPy implementation
for Level 2. The implementation was validated against sklearn using the
same seed, features, train/test split, and standardization procedure.
Both models produced identical accuracy, precision, recall, and test-set
confusion matrices. The top three features by absolute weight were also
the same.

### Question B

#### Decision 1 — Database Selection

**Chosen:** PostgreSQL for storing prediction requests and results.

**Rejected:** SQLite.

**Reason:** Question B Level 3 requires explaining how the application can
be made safe for 100 users at once, so concurrent database access was an
important consideration. PostgreSQL is better suited for concurrent
requests and multiple database connections than a file-based SQLite
database. I also verified the database integration by sending prediction
requests and checking that the stored request count, average predicted risk,
and high-risk share changed correctly.

#### Decision 2 — Backend Validation

**Chosen:** Validate all patient inputs at the FastAPI backend using
Pydantic, in addition to frontend validation.

**Rejected:** Rely only on JavaScript validation in the frontend.

**Reason:** Frontend validation can be bypassed by sending requests directly
to the API. Backend validation therefore provides the actual input boundary
for the application. The pytest suite includes an invalid age test, and the
API correctly rejected the invalid request with HTTP 422. This confirmed
that invalid input is blocked even when it reaches the backend directly.

#### Decision 3 — Deployed Prediction Threshold

**Chosen:** Keep the deployed API classification threshold at 0.50.

**Rejected:** Immediately deploy the 0.16 threshold identified during the
Question A Level 3 experiment.

**Reason:** The 0.16 threshold increased recall to approximately 0.90 but
also reduced precision and accuracy substantially on the test set. Since
this threshold was obtained from an assignment experiment and was not
clinically validated, I chose not to use it as a real-world medical
screening threshold in the application. The deployed API therefore uses
0.50 and is treated as an educational/demo system rather than a clinical
decision tool.

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