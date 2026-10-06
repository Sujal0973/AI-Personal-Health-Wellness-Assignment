# Personal Intelligence Note

**Course:** B.E. (AI & ML) — Technical Assignment (October 2026)  
**Candidate USN:** `1DA23AI050`  
**Personal Random Seed ($S$):** `50`  
**Selected Questions:**
- **Question A:** Predict a health risk (UCI Heart Failure Clinical Records)
- **Question B:** Turn a model into a usable app (FastAPI, Relational Database, Hand-written SQL, Frontend UI, Concurrency Benchmark)

---

## 1. Decision Log (Mandatory Section 4.1)

### Question A: Health Risk Prediction

#### Decision 1 — Clinical Feature Selection (`time` Exclusion)
- **Chosen Option:** Exclude the `time` feature and train all models strictly on the 11 baseline clinical and demographic features (`age`, `anaemia`, `creatinine_phosphokinase`, `diabetes`, `ejection_fraction`, `high_blood_pressure`, `platelets`, `serum_creatinine`, `serum_sodium`, `sex`, `smoking`).
- **Rejected Option:** Include all 12 non-target features (including `time`) as provided in the raw dataset.
- **Evidence-Based Rationale:** The `time` column denotes follow-up duration (in days) during the clinical study. In real-world frontline screening, follow-up duration is nonexistent when a new patient walks into a clinic. Furthermore, acute mortality strongly correlates with short follow-up time, which constitutes severe target leakage. While including `time` artificially inflated model accuracy to >85%, it produced a clinically invalid model. Excluding `time` produced an honest, clinically defensible baseline (Accuracy: 75.00%, Recall: 42.11%).

#### Decision 2 — Baseline Model Selection for Deployment
- **Chosen Option:** Baseline Random Forest Classifier (200 trees, `random_state=50`).
- **Rejected Option:** Hyperparameter-tuned Random Forest (100 trees, `min_samples_leaf=4`, `random_state=50`).
- **Evidence-Based Rationale:** Both models achieved an identical test accuracy of **75.00%**. Although the tuned model improved precision from 66.67% to 70.00%, its recall dropped from **42.11% down to 36.84%**, resulting in **12 missed fatalities (false negatives)** compared to **11** for the baseline model. In personal health risk screening, false negatives carry catastrophic clinical consequences. I prioritized higher recall over marginal precision gains, selecting the 200-tree baseline for productionization in Question B.

#### Decision 3 — From-Scratch Logistic Regression Architecture
- **Chosen Option:** Implement pure NumPy vectorized batch gradient descent with sigmoid activation, numerical clipping ($\epsilon = 10^{-9}$), and analytical gradients.
- **Rejected Option:** Rely on scikit-learn's built-in `LogisticRegression(solver='lbfgs')` for Level 2.
- **Evidence-Based Rationale:** Hand-crafting the optimization loop verified internal mathematical understanding. After 5,000 epochs at $\alpha = 0.01$, the scratch model achieved **71.67% accuracy, 57.14% precision, 42.11% recall, and identical confusion matrix `[[35, 6], [11, 8]]`**, perfectly matching scikit-learn. Furthermore, both models identified the exact same top-3 clinical drivers in identical rank order: `ejection_fraction` (-0.83), `serum_creatinine` (+0.72), and `age` (+0.67).

---

### Question B: Usable Health Application

#### Decision 1 — Database Engine Selection
- **Chosen Option:** PostgreSQL as the primary relational database with hand-written parameterized SQL.
- **Rejected Option:** File-based SQLite.
- **Evidence-Based Rationale:** Question B Level 3 evaluates system resilience under approximately 100 concurrent requests. File-based SQLite locks the entire database file on write transactions (`SQLITE_BUSY`), creating severe concurrency bottlenecks. PostgreSQL's Multi-Version Concurrency Control (MVCC) and row-level locking safely supported 100 simultaneous prediction inserts without deadlocks or corrupted transactions ($105 - 5 = 100$ records verified via `/stats`).

#### Decision 2 — Multi-Tier Boundary Validation Strategy
- **Chosen Option:** Enforce strict Pydantic schema validation at the FastAPI API gateway in addition to client-side HTML5 constraints.
- **Rejected Option:** Rely exclusively on client-side JavaScript validation in the browser.
- **Evidence-Based Rationale:** Client-side validation is easily bypassed by sending requests directly through cURL, Postman, or automated scripts. Backend validation establishes an immutable boundary. In automated testing, passing `age: -5` or `age: "not-a-number"` was immediately caught by FastAPI with `HTTP 422 Unprocessable Entity` before invoking the model or executing SQL inserts, preventing database pollution.

#### Decision 3 — Production API Decision Threshold
- **Chosen Option:** Maintain the deployed production API classification threshold at the standardized baseline of **0.50**.
- **Rejected Option:** Immediately deploy the experimental **0.16** threshold identified in Question A Level 3.
- **Evidence-Based Rationale:** While $\tau = 0.16$ achieved target recall $\approx 0.90$ (89.47%), it simultaneously dropped precision from 57.14% down to 42.50% and overall accuracy to 58.33% on a single test split of 60 patients. Deploying an experimental threshold without comprehensive calibration and external multi-center clinical validation is irresponsible in healthcare. The application therefore defaults to 0.50 with a prominent educational disclaimer.

---

## 2. Predictions Before Results (Mandatory Section 4.2)

To satisfy the integrity requirement (*"Commit each Level 3 prediction to GitHub before you run the test. The commit time is your proof."*), all hypotheses were committed prior to execution.

### Question A: Classification Threshold Sweep
- **Git Proof:** Committed in `question_a/level3/prediction.md` (Commit: `a436363`).
- **Pre-Experiment Prediction:**
  > *"Lowering the classification threshold until recall reaches approximately 0.90 will increase the number of patients classified as positive. Because more borderline cases will be classified as positive, precision will decrease compared with the 0.50 threshold. The required threshold will be well below 0.50."*
- **Observed Empirical Result:**
  - Lowering threshold from **0.50 to 0.16** increased Recall from **42.11% to 89.47%** (missed fatal cases dropped from 11 to 2).
  - Precision decreased from **57.14% to 42.50%** (false alarms increased from 6 to 23).
  - Predicted positive volume increased from 14 to 40 patients.
- **Verdict:** **Prediction confirmed.** The empirical trade-off matches the analytical mechanics of moving the decision boundary along the ROC curve.

### Question B: Fault Tolerance & 100-User Concurrency
- **Git Proof:** Committed in `question_b/level3/prediction.md` (Commit: `460dbfc`).
- **Pre-Experiment Predictions:**
  1. *Missing Model:* Application will fail during startup because model deserialization happens on module load; prediction endpoints will be unavailable.
  2. *Invalid Data Type:* Non-numeric strings in numeric fields will be caught by Pydantic before reaching business logic, returning HTTP 422 with zero database writes.
  3. *100 Concurrent Users:* Application will process concurrent requests without incorrect outputs; database connection overhead will emerge as the primary production bottleneck.
- **Observed Empirical Results:**
  1. Renaming model file resulted in `FileNotFoundError` during Uvicorn startup (HTTP connection refused). Restoring file fully restored health and prediction endpoints.
  2. Sending `{"age": "not-a-number"}` returned `HTTP 422 Unprocessable Entity` with `float_parsing` error detail. Database table row count remained unchanged.
  3. 100 concurrent requests completed with 100% success rate (3.924s total time, 2.715s avg latency). Exactly 100 rows were inserted into PostgreSQL.
- **Verdict:** **All three predictions confirmed.**

---

## 3. AI Usage Declaration (Mandatory Section 4.3)

### AI Tools Utilized
- **Tools:** ChatGPT (GPT-4o) & Antigravity (Gemini).
- **Scope of Assistance:**
  - Drafting initial boilerplate for FastAPI REST routing and Pydantic schemas.
  - Generating responsive CSS glassmorphism styling tokens for the frontend UI.
  - Reviewing LaTeX mathematical notation for gradient formulations.
  - Debugging test environment dependency mismatches.

### Documented AI Weaknesses & How I Fixed Them

#### Weakness 1: Missing Testing Dependency in Generated Setup
- **Issue:** During early test setup, running `pytest question_b/tests` failed during collection because FastAPI's `TestClient` required an underlying HTTP transport package that was missing from the generated environment.
- **How I Found & Fixed It:** Instead of assuming the API endpoint logic was broken, I inspected the traceback:
  ```text
  RuntimeError: The starlette.testclient module requires httpx.
  ```
  I diagnosed the missing dependency, installed `httpx2`, added it to `requirements.txt`, and verified that all 3 automated tests passed cleanly.

#### Weakness 2: AI Suggestion of Data Leakage Features
- **Issue:** When prompting the AI for feature engineering strategies to maximize classification accuracy in Question A, it suggested utilizing the `time` column to easily reach >85% accuracy.
- **How I Found & Fixed It:** As a domain student, I recognized that `time` represents survival follow-up duration recorded *after* patient admission—a clear case of **target leakage** that renders the model useless for prospective screening. I actively overrode the AI's recommendation, dropped `time`, and built the model solely on genuine frontline physiological markers.

---

## 4. Final Reflection & Live Walkthrough Readiness

This assignment bridged the gap between theoretical machine learning and production health software engineering:
1. **Clinical Machine Learning vs. Academic Metrics:** In healthcare, accuracy is often a vanity metric. Understanding the asymmetric cost of false negatives (a patient dying from untreated heart failure) versus false positives (an extra blood panel) makes threshold tuning a vital clinical decision rather than a mathematical afterthought.
2. **Production System Hardening:** A trained `.joblib` model is only 20% of a production system. Building Pydantic boundaries, parameterizing hand-written SQL queries, verifying database transactions under 100 concurrent threads, and providing plain-language explanations in an accessible UI is what makes AI safe for human use.
3. **Live Walkthrough Preparation:** I have thoroughly verified every script from first principles. I am prepared to modify model hyperparameters, adjust decision thresholds, alter Pydantic validation rules, or derive the batch gradient equations live without AI assistance.