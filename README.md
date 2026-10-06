# AI for Personal Health and Wellness

[![Technical Assignment](https://img.shields.io/badge/B.E._AI_%26_ML-Assignment_Oct_2026-blue.svg)](https://github.com/)
[![Candidate USN](https://img.shields.io/badge/USN-1DA23AI050-green.svg)](https://github.com/)
[![Random Seed](https://img.shields.io/badge/Random_Seed_S-50-orange.svg)](https://github.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-brightgreen.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-teal.svg)](https://fastapi.tiangolo.com)

A comprehensive, production-grade health-tech system developed for the **AI for Personal Health and Wellness** assignment. This repository implements complete end-to-end solutions for **Question A** (Health Risk Prediction) and **Question B** (Production API & Usable Application) across all three required levels (Build, Code-It-Yourself, and Reason).

---

## 1. Candidate Information

- **Candidate USN:** `1DA23AI050`
- **Personal Seed ($S$):** `50` *(Derived from last 4 digits of USN: `0050` &rarr; `50`)*
- **Selected Questions:**
  - **Question A:** Predict a health risk (UCI Heart Failure Clinical Records)
  - **Question B:** Turn a model into a usable app (FastAPI, PostgreSQL/SQLite, Hand-written SQL, Frontend UI, 100-user Concurrency)
- **Target Reviewer:** `mnaveennk@iisc.ac.in`

---

## 2. Dataset & Clinical Feature Selection

This project utilizes the **UCI Heart Failure Clinical Records Dataset** (299 patient records, 13 features).

### Prevention of Data Leakage (`time` exclusion)
The dataset includes a `time` column representing patient follow-up duration (in days). In clinical screening, follow-up duration is **not available** at the time a new patient walks in for screening. Furthermore, shorter follow-up times strongly correlate with in-hospital mortality (target leakage). 

**Decision:** The `time` feature was deliberately **excluded**, training all models strictly on the **11 baseline physiological and demographic features**:
- `age`: Patient age in years (Demographic)
- `anaemia`: Decrease of red blood cells or hemoglobin (0/1)
- `creatinine_phosphokinase`: Level of CPK enzyme in blood (mcg/L)
- `diabetes`: Whether patient has diabetes (0/1)
- `ejection_fraction`: Percentage of blood leaving heart per contraction (%)
- `high_blood_pressure`: Whether patient has hypertension (0/1)
- `platelets`: Platelets in blood (kiloplatelets/mL)
- `serum_creatinine`: Level of serum creatinine in blood (mg/dL)
- `serum_sodium`: Level of serum sodium in blood (mEq/L)
- `sex`: Biological sex (0 = female, 1 = male)
- `smoking`: Whether patient smokes (0/1)
- **Target:** `DEATH_EVENT` (0 = survived, 1 = deceased during observation)

---

## 3. Repository Architecture

```text
AI-Personal-Health-Wellness-Assignment/
├── README.md                                  # Root documentation and execution guide
├── PERSONAL_INTELLIGENCE.md                   # Mandatory decision log & AI usage declaration
├── requirements.txt                           # Complete project dependencies
├── data/
│   └── heart_failure_clinical_records_dataset.csv
│
├── question_a/                                # Question A: Predict a Health Risk
│   ├── level1/
│   │   ├── README.md                          # Baseline model evaluations & metrics
│   │   ├── train_models.py                    # Scikit-learn LR & Random Forest baseline
│   │   ├── compare_models.py                  # In-depth model comparison script
│   │   └── tune_models.py                     # Hyperparameter sensitivity experiments
│   ├── level2/
│   │   ├── README.md                          # NumPy scratch implementation & comparison
│   │   ├── logistic_regression_numpy.py       # Scratch Sigmoid, BCE Loss, GD & Confusion Matrix
│   │   ├── compare_sklearn.py                 # Side-by-side verification script vs sklearn
│   │   └── data_quality_check.py              # Data sanity and integrity verification
│   └── level3/
│       ├── README.md                          # Threshold sensitivity analysis & reasoning
│       ├── prediction.md                      # Pre-experiment hypothesis (committed first)
│       └── threshold_experiment.py            # Systematic threshold sweep (0.10 - 0.50)
│
└── question_b/                                # Question B: Production Health Risk Application
    ├── api/
    │   ├── main.py                            # FastAPI app, endpoints (/predict, /stats, /health)
    │   ├── database.py                        # Hand-written parameterized SQL & connection logic
    │   └── model/
    │       └── heart_failure_rf.joblib        # Serialized trained model (Seed 50)
    ├── frontend/
    │   ├── index.html                         # Usable assessment UI & screening dashboard
    │   ├── style.css                          # Modern, accessible styling
    │   └── script.js                          # Client-side input validation & API communication
    ├── level1/
    │   └── README.md                          # API architecture & schema documentation
    ├── level2/
    │   └── README.md                          # Database persistence, SQL queries & test overview
    ├── level3/
    │   ├── README.md                          # Break/Fix experiments & concurrency report
    │   ├── prediction.md                      # Pre-experiment failure & scale predictions
    │   └── concurrency_test.py                # 100 concurrent requests stress test benchmark
    └── tests/
        └── test_api.py                        # Pytest automated test suite (valid, bad-input, health)
```

---

## 4. Key Results Summary

### Question A: Health Risk Prediction (Seed = 50)
| Model / Configuration | Accuracy | Precision | Recall | Notes |
|---|:---:|:---:|:---:|---|
| **Logistic Regression (sklearn)** | 71.67% | 57.14% | 42.11% | Baseline linear model |
| **Random Forest (sklearn)** | 75.00% | 66.67% | 42.11% | Baseline ensemble model |
| **Logistic Regression (NumPy Scratch)** | **71.67%** | **57.14%** | **42.11%** | **100% match with scikit-learn** |
| **Random Forest (Threshold = 0.50)** | 71.67% | 57.14% | 42.11% | Misses 11 out of 19 fatal cases |
| **Random Forest (Threshold = 0.16)** | **58.33%** | **42.50%** | **89.47%** | **Misses only 2 fatal cases; target recall reached** |

**Top 3 Features Identified (Scratch vs Sklearn):**
1. `ejection_fraction`: Scratch `-0.8349` | Sklearn `-0.8100` *(Higher ejection fraction decreases mortality risk)*
2. `serum_creatinine`: Scratch `+0.7161` | Sklearn `+0.6934` *(Elevated serum creatinine strongly increases risk)*
3. `age`: Scratch `+0.6655` | Sklearn `+0.6485` *(Advanced age increases mortality risk)*

---

### Question B: Usable Application & Concurrency Benchmark
- **Backend:** FastAPI microservice with Pydantic validation and hand-written SQL persistence.
- **Automated Tests:** 3 automated tests via `pytest` passing (including HTTP 422 boundary rejection).
- **100-User Concurrency Benchmark (`concurrency_test.py`):**
  - **Requests Dispatched:** 100 concurrent requests
  - **Success Rate:** 100% (100 successful, 0 failed)
  - **Total Elapsed Time:** 3.924 seconds
  - **Average Latency:** 2.715 seconds
  - **Database Persistence:** Confirmed +100 records recorded accurately via `/stats`.

---

## 5. Quickstart & Execution Guide

Follow these reproduction steps to run any part of the project locally.

### 5.1 Environment Setup
```bash
# Clone the repository
git clone <repo-url>
cd AI-Personal-Health-Wellness-Assignment

# Create and activate Python virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On Linux / macOS:
source .venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

---

### 5.2 Running Question A (Risk Prediction)

```bash
# Level 1: Train and evaluate baseline models (Logistic Regression & Random Forest)
python question_a/level1/train_models.py

# Level 2: Run NumPy scratch Logistic Regression & confusion matrix
python question_a/level2/logistic_regression_numpy.py

# Level 2: Run exact comparison between scratch model and scikit-learn
python question_a/level2/compare_sklearn.py

# Level 3: Run classification threshold sweep (0.10 to 0.50)
python question_a/level3/threshold_experiment.py
```

---

### 5.3 Running Question B (API, Database, Tests & Frontend)

#### Step 1: Database Setup
The application connects to PostgreSQL. Set your password in the environment:
```bash
# Windows PowerShell:
$env:DB_PASSWORD="your_password"

# Windows Command Prompt:
set DB_PASSWORD=your_password

# Linux/macOS:
export DB_PASSWORD=your_password
```
*(Optionally customize `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` if different from defaults `localhost`, `5432`, `health_wellness`, `postgres`).*

#### Step 2: Run the Automated Tests (Pytest)
```bash
python -m pytest question_b/tests -v
```

#### Step 3: Start the FastAPI Backend Server
```bash
uvicorn question_b.api.main:app --reload --host 127.0.0.1 --port 8000
```
- Interactive Swagger API Documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Health Check: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
- Aggregated SQL Statistics: [http://127.0.0.1:8000/stats](http://127.0.0.1:8000/stats)

#### Step 4: Run the 100-User Concurrency Stress Test
*(Ensure the backend server is running in another terminal)*
```bash
python question_b/level3/concurrency_test.py
```

#### Step 5: Open the Frontend Application
Simply open `question_b/frontend/index.html` in your web browser, or serve it using Python:
```bash
python -m http.server 5500 --directory question_b/frontend
```
Then visit [http://127.0.0.1:5500](http://127.0.0.1:5500).

---

## 6. Deliverables & Submission Checklist

- [x] **Source Code & Files:** Organized by question folders (`question_a/`, `question_b/`) across Levels 1–3.
- [x] **Commit History:** 8 commits distributed throughout the assignment window; Level 3 predictions committed prior to running experiments.
- [x] **Seed $S$:** Explicitly configured as `50` across all random seeds and splits.
- [x] **Personal Intelligence Note:** Complete [PERSONAL_INTELLIGENCE.md](file:///c:/Users/sujal/OneDrive/Documents/AI-Personal-Health-Wellness-Assignment/AI-Personal-Health-Wellness-Assignment/PERSONAL_INTELLIGENCE.md) with two justified decisions per question and transparent AI usage declaration.
- [x] **Automated Tests:** Comprehensive pytest suite testing edge cases and input validation.
- [x] **Demo Video:** 3 to 5-minute screen recording uploaded to Google Drive with open view permissions.