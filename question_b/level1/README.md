# Question B — Level 1: Production API & Usable Frontend

## 1. Objective

Productionize the trained Random Forest health-risk model (from Question A, Seed $S = 50$) by serving it through a **FastAPI** RESTful microservice and pairing it with a clean, responsive, and accessible **HTML/CSS/JavaScript** frontend that translates statistical probabilities into plain-language risk assessments for frontline screening.

---

## 2. Architecture & Technology Stack

```text
[ Browser / Frontend Client ]
        │  ▲
        │  │ HTTP POST /predict (JSON Payload)
        ▼  │ HTTP 200 OK (Risk Assessment + Probability)
[ FastAPI Application (main.py) ]
        │
        ├──> Pydantic Schema (Input Boundary Validation)
        ├──> Scikit-Learn Model (heart_failure_rf.joblib, Seed 50)
        └──> Relational Database Persistence (PostgreSQL / SQLite)
```

- **Backend Framework:** FastAPI (Asynchronous Python REST API)
- **ASGI Server:** Uvicorn
- **Input Validation:** Pydantic (`PatientInput` schema)
- **Model Storage:** Joblib serialization (`question_b/api/model/heart_failure_rf.joblib`)
- **Frontend:** Vanilla HTML5, Modern CSS3 (Glassmorphism design tokens), and Vanilla JavaScript (Fetch API, zero framework dependencies for ultra-fast load times).

---

## 3. Deployed Model Configuration

- **Algorithm:** Random Forest Classifier (200 estimators)
- **Random Seed ($S$):** `50`
- **Features Used:** 11 baseline patient characteristics (`time` excluded to prevent survival duration leakage)
- **Classification Threshold:** `0.50` (Standard baseline threshold)

---

## 4. REST API Endpoint Specification

### 4.1 `GET /` — Service Metadata
Confirms API status and active personal seed.
```json
{
  "message": "Heart Failure Risk Prediction API",
  "status": "running",
  "seed": 50
}
```

### 4.2 `GET /health` — Readiness & Liveness Probe
Verifies that the microservice is operational and the joblib model artifact is loaded in memory.
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### 4.3 `POST /predict` — Health Risk Inference
Consumes patient vitals and returns the predicted probability and clinical risk classification in plain words.

#### Request Body Schema (`application/json`):
```json
{
  "age": 60.0,
  "anaemia": 1,
  "creatinine_phosphokinase": 582.0,
  "diabetes": 0,
  "ejection_fraction": 30.0,
  "high_blood_pressure": 1,
  "platelets": 263358.0,
  "serum_creatinine": 1.9,
  "serum_sodium": 136.0,
  "sex": 1,
  "smoking": 0
}
```

#### Successful Response (`HTTP 200 OK`):
```json
{
  "prediction": 1,
  "risk_label": "High Risk",
  "predicted_risk": 0.51,
  "threshold": 0.50
}
```

---

## 5. Frontend Application Features

The frontend interface (`question_b/frontend/`) was built to turn raw machine learning output into an intuitive experience:
1. **Plain-Language Risk Communication:** Outputs clear, actionable categories: **"High Risk"** or **"Lower Risk"**.
2. **Visual Probability Bar:** Displays the exact model probability as a percentage (e.g., `51.0%`) with an animated visual gauge.
3. **Client-Side Real-Time Validation:** Input fields highlight immediately if values fall outside physiological boundaries (e.g., age must be 1 to 120).
4. **Transparent Threshold Reporting:** Displays the classification threshold used (`0.50`) and seed (`50`).
5. **Prominent Clinical Disclaimer:** Explicitly reminds frontline health workers that the AI tool provides screening estimates for educational purposes, not autonomous diagnostic decisions.

---

## 6. How to Run

### Step 1: Start the Backend
From the project root:
```bash
uvicorn question_b.api.main:app --reload --host 127.0.0.1 --port 8000
```
Interactive Swagger API documentation will be available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### Step 2: Open the Frontend
Open `question_b/frontend/index.html` directly in any modern browser, or serve it using Python:
```bash
python -m http.server 5500 --directory question_b/frontend
```
Visit [http://127.0.0.1:5500](http://127.0.0.1:5500) to perform live assessments.